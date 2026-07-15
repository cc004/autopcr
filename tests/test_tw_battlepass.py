import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from autopcr.core.datamgr import datamgr
from autopcr.core.pcrclient import pcrclient
from autopcr.core.region import REGION_CN, REGION_TW, reset_region, set_region
from autopcr.model.common import (
    InventoryInfo,
    UserBattlepassInfo,
    UserBattlepassLevelInfo,
    UserBattlepassLineInfo,
    UserBattlepassLineReceivedLevel,
    UserMissionInfo,
    UserMissionProgressInfo,
)
from autopcr.model.enums import eInventoryType, eMissionStatusType
from autopcr.model.requests import (
    BattlepassReceiveLevelRewardRequest,
    BattlepassReceiveMissionRewardRequest,
    BattlepassTopRequest,
    HomeIndexRequest,
)
from autopcr.model.responses import (
    BattlepassReceiveLevelRewardResponse,
    BattlepassReceiveMissionRewardResponse,
    BattlepassTopResponse,
    HomeIndexResponse,
    SeasonPassIndexResponse,
    SeasonPassMissionAcceptResponse,
    SeasonPassRewardAcceptResponse,
)
from autopcr.module.modules import daily as daily_module
from autopcr.module.modules.daily import seasonpass_accept, seasonpass_reward


def _module_instance(module_type):
    module = object.__new__(module_type)
    module.log = []
    module.warn = []
    module.is_warn = False
    return module


class TaiwanBattlepassProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_client_builds_exact_battlepass_requests(self):
        client = pcrclient.__new__(pcrclient)
        client.request = AsyncMock(side_effect=lambda request: request)

        top = await client.battlepass_top()
        mission = await client.battlepass_receive_mission_reward(
            26031, [260311020, 260312050]
        )
        level = await client.battlepass_receive_level_reward(26031, 17)

        self.assertIsInstance(top, BattlepassTopRequest)
        self.assertEqual("battlepass/top", top.url)
        self.assertEqual({}, top.dict(exclude_none=True))
        self.assertIsInstance(mission, BattlepassReceiveMissionRewardRequest)
        self.assertEqual("battlepass/receive_mission_reward", mission.url)
        self.assertEqual(
            {
                "season_id": 26031,
                "mission_id_list": [260311020, 260312050],
            },
            mission.dict(exclude_none=True),
        )
        self.assertIsInstance(level, BattlepassReceiveLevelRewardRequest)
        self.assertEqual("battlepass/receive_level_reward", level.url)
        self.assertEqual(
            {"season_id": 26031, "target_level": 17},
            level.dict(exclude_none=True),
        )

    async def test_home_response_caches_battlepass_state(self):
        manager = datamgr()
        response = HomeIndexResponse(
            battlepass_info_list=[
                UserBattlepassInfo(season_id=26031, max_level=9)
            ],
            is_battlepass_mission_receive_auto=True,
            is_battlepass_level_receive_auto=False,
        )

        await response.update(manager, HomeIndexRequest(is_first=0))

        self.assertEqual(9, manager.battlepass_info[26031].max_level)
        self.assertTrue(manager.is_battlepass_mission_receive_auto)
        self.assertFalse(manager.is_battlepass_level_receive_auto)

    def test_response_models_match_recovered_wire_fields(self):
        top = BattlepassTopResponse.parse_obj({
            "line_list": [{
                "line_id": 260311,
                "level_list": [{
                    "level": 3,
                    "highlight": 1,
                    "type": int(eInventoryType.Item),
                    "id": 23001,
                    "count": 2,
                }],
            }]
        })
        mission = BattlepassReceiveMissionRewardResponse.parse_obj({
            "reward_list": [{"type": int(eInventoryType.Item), "id": 1}]
        })
        level = BattlepassReceiveLevelRewardResponse.parse_obj({
            "reward_list": [],
            "add_present_count": 2,
        })

        self.assertEqual(3, top.line_list[0].level_list[0].level)
        self.assertEqual(1, mission.reward_list[0].id)
        self.assertEqual(2, level.add_present_count)


class TaiwanBattlepassModuleTests(unittest.IsolatedAsyncioTestCase):
    def _info(self, levels, max_level=10, point=7000):
        return UserBattlepassInfo(
            season_id=26031,
            point=point,
            max_level=max_level,
            line_received_level_list=[
                UserBattlepassLineReceivedLevel(line_id=line_id, level=level)
                for line_id, level in levels.items()
            ],
        )

    def test_stamina_exclusion_uses_safe_prefix(self):
        info = self._info({260311: 2, 260312: 3})
        lines = {
            260311: UserBattlepassLineInfo(
                line_id=260311,
                level_list=[
                    UserBattlepassLevelInfo(
                        level=4, type=int(eInventoryType.Item)
                    ),
                    UserBattlepassLevelInfo(
                        level=6, type=int(eInventoryType.Stamina)
                    ),
                ],
            ),
            260312: UserBattlepassLineInfo(
                line_id=260312,
                level_list=[
                    UserBattlepassLevelInfo(
                        level=8, type=int(eInventoryType.Item)
                    )
                ],
            ),
        }

        target, incomplete = seasonpass_reward._tw_safe_target_level(
            info, lines, 8
        )

        self.assertEqual(5, target)
        self.assertFalse(incomplete)

    def test_stamina_exclusion_never_moves_an_advanced_line_backwards(self):
        info = self._info({260311: 2, 260312: 8})
        lines = {
            260311: UserBattlepassLineInfo(
                line_id=260311,
                level_list=[
                    UserBattlepassLevelInfo(
                        level=4, type=int(eInventoryType.Stamina)
                    )
                ],
            ),
            260312: UserBattlepassLineInfo(line_id=260312, level_list=[]),
        }

        target, incomplete = seasonpass_reward._tw_safe_target_level(
            info, lines, 8
        )

        self.assertEqual(2, target)
        self.assertFalse(incomplete)

    def test_stamina_exclusion_blocks_on_missing_line_data(self):
        target, incomplete = seasonpass_reward._tw_safe_target_level(
            self._info({260311: 2}), {}, 8
        )

        self.assertEqual(0, target)
        self.assertTrue(incomplete)

    async def test_tw_accept_submits_only_receivable_mission_ids(self):
        module = _module_instance(seasonpass_accept)
        info = UserBattlepassInfo(
            season_id=26031,
            mission_progress_list=[
                UserMissionProgressInfo(
                    mission_id=10, status=eMissionStatusType.EnableReceive
                ),
                UserMissionProgressInfo(
                    mission_id=11, status=eMissionStatusType.AlreadyReceive
                ),
                UserMissionProgressInfo(
                    mission_id=12, status=eMissionStatusType.EnableReceive
                ),
            ],
        )
        client = SimpleNamespace(
            data=SimpleNamespace(battlepass_info={26031: info}),
            refresh=AsyncMock(),
            battlepass_receive_mission_reward=AsyncMock(
                return_value=BattlepassReceiveMissionRewardResponse(
                    reward_list=[InventoryInfo(type=eInventoryType.Item, id=1)]
                )
            ),
            serialize_reward_summary=AsyncMock(return_value="points"),
        )
        token = set_region(REGION_TW)
        try:
            await module.do_task(client)
        finally:
            reset_region(token)

        client.battlepass_receive_mission_reward.assert_awaited_once_with(
            26031, [10, 12]
        )
        client.refresh.assert_awaited_once_with()
        self.assertIn("points", module.log[0])

    async def test_tw_reward_stops_before_stamina_level(self):
        module = _module_instance(seasonpass_reward)
        module.get_config = lambda _: True
        info = self._info({260311: 2}, max_level=8)
        client = SimpleNamespace(
            data=SimpleNamespace(battlepass_info={26031: info}),
            refresh=AsyncMock(),
            battlepass_top=AsyncMock(
                return_value=BattlepassTopResponse(
                    line_list=[UserBattlepassLineInfo(
                        line_id=260311,
                        level_list=[
                            UserBattlepassLevelInfo(
                                level=4, type=int(eInventoryType.Item)
                            ),
                            UserBattlepassLevelInfo(
                                level=6, type=int(eInventoryType.Stamina)
                            ),
                        ],
                    )]
                )
            ),
            battlepass_receive_level_reward=AsyncMock(
                return_value=BattlepassReceiveLevelRewardResponse(
                    reward_list=[InventoryInfo(type=eInventoryType.Item, id=2)]
                )
            ),
            serialize_reward_summary=AsyncMock(return_value="items"),
        )
        token = set_region(REGION_TW)
        fake_db = SimpleNamespace(
            battlepass_season={
                26031: SimpleNamespace(next_level_point=1000)
            },
            is_stamina_type=lambda reward_type: (
                reward_type == int(eInventoryType.Stamina)
            ),
        )
        try:
            with patch.object(daily_module, "db", fake_db):
                await module.do_task(client)
        finally:
            reset_region(token)

        client.refresh.assert_awaited_once_with()
        client.battlepass_top.assert_awaited_once_with()
        client.battlepass_receive_level_reward.assert_awaited_once_with(
            26031, 5
        )
        self.assertTrue(module.is_warn)
        self.assertTrue(any("items" in line for line in module.log))

    async def test_tw_reward_uses_current_level_instead_of_max_level(self):
        module = _module_instance(seasonpass_reward)
        module.get_config = lambda _: False
        info = self._info({260311: 2}, max_level=99, point=4000)
        client = SimpleNamespace(
            data=SimpleNamespace(battlepass_info={26031: info}),
            refresh=AsyncMock(),
            battlepass_receive_level_reward=AsyncMock(
                return_value=BattlepassReceiveLevelRewardResponse(
                    reward_list=[InventoryInfo(type=eInventoryType.Item, id=2)]
                )
            ),
            serialize_reward_summary=AsyncMock(return_value="items"),
        )
        fake_db = SimpleNamespace(
            battlepass_season={
                26031: SimpleNamespace(next_level_point=1000)
            }
        )
        token = set_region(REGION_TW)
        try:
            with patch.object(daily_module, "db", fake_db):
                await module.do_task(client)
        finally:
            reset_region(token)

        client.battlepass_receive_level_reward.assert_awaited_once_with(
            26031, 5
        )

    async def test_cn_accept_keeps_season_ticket_flow(self):
        module = _module_instance(seasonpass_accept)
        client = SimpleNamespace(
            season_ticket_new_index=AsyncMock(
                return_value=SeasonPassIndexResponse(
                    missions=[UserMissionInfo(
                        mission_id=1,
                        mission_status=eMissionStatusType.EnableReceive,
                    )]
                )
            ),
            season_ticket_new_accept=AsyncMock(
                return_value=SeasonPassMissionAcceptResponse(
                    rewards=[], seasonpass_level=3
                )
            ),
            serialize_reward_summary=AsyncMock(return_value="old rewards"),
        )
        original = daily_module.db.get_active_seasonpass
        daily_module.db.get_active_seasonpass = lambda: [
            SimpleNamespace(season_id=77)
        ]
        token = set_region(REGION_CN)
        try:
            await module.do_task(client)
        finally:
            reset_region(token)
            daily_module.db.get_active_seasonpass = original

        client.season_ticket_new_index.assert_awaited_once_with(77)
        client.season_ticket_new_accept.assert_awaited_once_with(77, 0)

    async def test_cn_reward_keeps_season_ticket_request_body(self):
        module = _module_instance(seasonpass_reward)
        module.get_config = lambda _: False
        client = SimpleNamespace(
            season_ticket_new_index=AsyncMock(
                return_value=SeasonPassIndexResponse(
                    is_buy=False,
                    received_rewards=[10],
                )
            ),
            season_ticket_new_reward=AsyncMock(
                return_value=SeasonPassRewardAcceptResponse(
                    rewards=[InventoryInfo(type=eInventoryType.Item, id=1)]
                )
            ),
            serialize_reward_summary=AsyncMock(return_value="old rewards"),
        )
        fake_db = SimpleNamespace(
            get_open_seasonpass=lambda: [SimpleNamespace(season_id=77)],
            seasonpass_level_reward_full_sign=lambda _level, _vip: 1,
        )
        token = set_region(REGION_CN)
        try:
            with patch.object(daily_module, "db", fake_db):
                await module.do_task(client)
        finally:
            reset_region(token)

        client.season_ticket_new_index.assert_awaited_once_with(77)
        client.season_ticket_new_reward.assert_awaited_once_with(77, 0, 0)


if __name__ == "__main__":
    unittest.main()
