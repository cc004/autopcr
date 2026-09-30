import unittest
from types import SimpleNamespace
from unittest.mock import patch

from autopcr.db.database import db
from autopcr.model.enums import eMissionStatusType
from autopcr.model.error import AbortError, SkipError
from autopcr.module.modules import daily_modules
from autopcr.module.modules.autosweep import daily_quest_mission


class FakeParent:
    id = "test"

    def __init__(self, config=None):
        self.config = config or {}

    def get_config(self, key, default):
        return self.config.get(key, default)


class FakeClient:
    def __init__(self, mission=None, zen=False, stop_after=None):
        self.mission = mission
        self.zen = zen
        self.stop_after = stop_after
        self.mission_index_calls = 0
        self.sweep_calls = []

    async def mission_index(self):
        self.mission_index_calls += 1
        missions = [] if self.mission is None else [self.mission]
        return SimpleNamespace(missions=missions)

    def is_stamina_consume_not_run(self):
        return self.zen

    async def quest_skip_aware(self, quest_id, count, recover, is_total):
        self.sweep_calls.append((quest_id, count, recover, is_total))
        if self.stop_after is not None and len(self.sweep_calls) > self.stop_after:
            return [], 0, True
        return [], count, False

    async def serialize_reward_summary(self, rewards):
        return str(rewards)


def make_mission(clear_num=0, status=eMissionStatusType.NoClear):
    return SimpleNamespace(
        mission_id=123,
        mission_status=status,
        clear_num=clear_num,
    )


class DailyQuestMissionTest(unittest.IsolatedAsyncioTestCase):
    def make_module(self):
        module = daily_quest_mission(FakeParent())
        module._get_mission_ids = lambda: {123}
        return module

    async def run_sweep(self, clear_num):
        module = self.make_module()
        client = FakeClient(make_mission(clear_num))
        with patch.object(db, "last_normal_quest", return_value=[301, 300, 299, 298]), \
             patch.object(db, "get_quest_name", side_effect=lambda quest: str(quest)):
            await module.do_task(client)
        return module, client

    async def test_completed_mission_does_not_sweep_or_recheck(self):
        for status in (eMissionStatusType.EnableReceive, eMissionStatusType.AlreadyReceive):
            with self.subTest(status=status):
                module = self.make_module()
                client = FakeClient(make_mission(status=status))
                with self.assertRaisesRegex(SkipError, "已完成"):
                    await module.do_task(client)
                self.assertEqual(client.mission_index_calls, 1)
                self.assertEqual(client.sweep_calls, [])

    async def test_sweeps_latest_three_quests_until_exact_target(self):
        cases = {
            0: [(301, 3), (300, 3), (299, 3), (301, 3), (300, 3), (299, 3), (301, 2)],
            12: [(301, 3), (300, 3), (299, 2)],
            19: [(301, 1)],
        }
        for clear_num, expected in cases.items():
            with self.subTest(clear_num=clear_num):
                module, client = await self.run_sweep(clear_num)
                self.assertEqual(
                    [(quest, count) for quest, count, _, _ in client.sweep_calls],
                    expected,
                )
                self.assertTrue(all(recover and is_total for _, _, recover, is_total in client.sweep_calls))
                self.assertEqual(client.mission_index_calls, 1)
                self.assertFalse(module.is_warn)

    async def test_stamina_shortage_warns_with_remaining_count(self):
        module = self.make_module()
        client = FakeClient(make_mission(), stop_after=1)
        with patch.object(db, "last_normal_quest", return_value=[301, 300, 299]), \
             patch.object(db, "get_quest_name", side_effect=lambda quest: str(quest)):
            await module.do_task(client)
        self.assertTrue(module.is_warn)
        self.assertIn("尚需通关17次", module.log[-1])

    async def test_zen_mode_warns_without_sweeping(self):
        module = self.make_module()
        client = FakeClient(make_mission(clear_num=5), zen=True)
        await module.do_task(client)
        self.assertTrue(module.is_warn)
        self.assertEqual(client.sweep_calls, [])
        self.assertIn("尚需通关15次", module.log[-1])

    async def test_missing_account_mission_is_skipped(self):
        module = self.make_module()
        with self.assertRaisesRegex(SkipError, "无需补刷"):
            await module.do_task(FakeClient())

    async def test_missing_master_mission_aborts_before_request(self):
        module = daily_quest_mission(FakeParent())
        module._get_mission_ids = lambda: set()
        client = FakeClient()
        with self.assertRaisesRegex(AbortError, "主数据中未找到"):
            await module.do_task(client)
        self.assertEqual(client.mission_index_calls, 0)

    async def test_missing_latest_quest_aborts(self):
        module = self.make_module()
        with patch.object(db, "last_normal_quest", return_value=[]):
            with self.assertRaisesRegex(AbortError, "没有可供补刷"):
                await module.do_task(FakeClient(make_mission()))

    def test_module_metadata_and_order(self):
        module = daily_quest_mission(FakeParent())
        self.assertTrue(module.default)
        self.assertEqual(module.config, {})
        self.assertTrue(module.stamina_relative)
        self.assertIn("体力消耗", module.tags)

        order = [module.__name__ for module in daily_modules.modules]
        self.assertEqual(order.index("daily_quest_mission"), order.index("all_in_hatsune") + 1)


if __name__ == "__main__":
    unittest.main()
