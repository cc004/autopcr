import base64
import asyncio
import hashlib
import importlib
import os
import struct
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import msgpack
from Crypto.Cipher import AES
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from autopcr.core.apiclient import apiclient
from autopcr.core.datamgr import datamgr
from autopcr.core.sdkclient import account, platform
from autopcr.core.sessionmgr import sessionmgr
from autopcr.db.models import EquipmentDatum, UnitDatum, UnitEnemyDatum
from autopcr.model.common import LoadDeckData, StorySkipInfo
from autopcr.model.enums import ePartyType
from autopcr.model.error import PanicError
from autopcr.model.requests import CheckAgreementRequest
from autopcr.model.responses import (
    GachaExecResponse,
    HomeIndexResponse,
    PresentIndexResponse,
    ShopBuyMultipleResponse,
)
from autopcr.model.sdkrequests import (
    CheckGameStartRequest,
    TwCheckGameStartRequest,
)
from autopcr.module.modulelistmgr import (
    ModuleListManager,
    TW_SUPPORTED_MODULES,
)
from autopcr.sdk.sdkclients import twsdkclient
from autopcr.sdk.twplayerprefs import decode_xml


_UDID_COMPACT = "00112233445566778899aabbccddeeff"
_UDID = "00112233-4455-6677-8899-aabbccddeeff"
_VIEWER_ID = "2123456789"
_SHORT_UDID = "987654321"
_KEY = b"0123456789abcdef0123456789abcdef"


def _pad(data: bytes) -> bytes:
    count = 16 - len(data) % 16
    return data + bytes([count]) * count


def _encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return AES.new(key, AES.MODE_CBC, iv).encrypt(_pad(data)) + key


def _decrypt(data: bytes, iv: bytes):
    key = data[-32:]
    padded = AES.new(key, AES.MODE_CBC, iv).decrypt(data[:-32])
    return padded[:-padded[-1]], key


def _tw_sdk(
    password=f"{_UDID_COMPACT}:{_VIEWER_ID}:2",
    *,
    viewer_id="",
    server_id=0,
    username=_SHORT_UDID,
):
    info = account(
        username,
        password,
        platform.Android,
        viewer_id=viewer_id,
        server_id=server_id,
    )
    with patch.dict(os.environ, {"AUTOPCR_TW_API_ROOT": ""}):
        return twsdkclient(info)


class TaiwanProtocolTests(unittest.TestCase):
    def setUp(self):
        # IsolatedAsyncioTestCase closes its loop between test classes.  Keep
        # these synchronous transport vectors independent from discovery order
        # when the compatibility suite is run on Python 3.8.
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def test_unknown_server_campaign_ids_are_ignored(self):
        known_campaign_id = 5188
        unknown_campaign_id = 5189
        condition = Mock(side_effect=lambda campaign_id: True)
        fake_db = SimpleNamespace(
            campaign_schedule={known_campaign_id: object()},
            get_campaign_times=Mock(return_value=4000),
            is_level_effective_scope_in_campaign=Mock(return_value=True),
        )
        manager = datamgr(
            campaign_list=[unknown_campaign_id, known_campaign_id],
            team_level=200,
        )

        datamgr_module = importlib.import_module("autopcr.core.datamgr")
        with patch.object(datamgr_module, "db", fake_db):
            campaign_times = manager.get_campaign_times(condition)

        self.assertEqual(2000, campaign_times)
        condition.assert_called_once_with(known_campaign_id)
        fake_db.get_campaign_times.assert_called_once_with(known_campaign_id)
        fake_db.is_level_effective_scope_in_campaign.assert_called_once_with(
            manager.team_level,
            known_campaign_id,
        )

    def test_audited_tw_modules_are_allowlisted_without_protocol_exceptions(self):
        audited_direct_modules = {
            "chara_fortune", "free_gacha", "travel_round",
            "travel_quest_sweep", "ex_equip_recycle",
            "special_underground_skip", "mirage_floor_receive",
            "mirage_nemesis_sweep", "tower_cloister_sweep",
            "abyss_quest_sweep", "abyss_boss_sweep", "talent_sweep",
            "talent_sweep2", "xinsui1_sweep", "xinsui2_sweep",
            "xinsui3_sweep", "xinsui4_sweep", "xinsui5_sweep",
            "xinsui6_sweep", "xinsui7_sweep", "xinsui8_sweep",
            "xinsui9_sweep", "starcup1_sweep", "starcup2_sweep",
            "starcup3_sweep", "hatsune_dear_reading", "smart_sweep",
            "mirai_very_hard_sweep", "smart_shiori_sweep",
            "mirai_sp1_h_sweep", "mirai_sp1_shiori_sweep",
            "all_in_hatsune", "master_shop_talent", "master_shop",
            "love_up", "shiori_mission_check", "alces_story_reading",
            "seven_obtent_reading", "ex_equip_power_maximun",
            "set_my_party2", "find_talent_quest",
            "find_clan_talent_quest", "ex_equip_rank_up",
            "ex_equip_enhance_up", "half_schedule", "caravan_play",
            "caravan_shop_buy", "clan_battle_knive", "ex_equip_info",
            "travel_team_view", "missing_emblem",
            "get_clan_support_unit", "clear_my_party",
            "remove_cb_ex_equip", "remove_cb_support",
            "redeem_unit_swap", "search_unit", "missing_unit",
            "refresh_box", "unit_promote", "unit_memory_buy",
            "unit_set_unique_equip_growth", "unit_exceed",
            "unit_evolution", "get_library_import_data",
            "get_need_equip", "get_normal_quest_recommand",
            "get_need_memory", "get_need_pure_memory",
            "get_need_sp_memory", "get_need_xinsui", "gacha_start",
            "gacha_exchange_chara", "ex_equip_rainbow_enchance",
            "seasonpass_accept", "seasonpass_reward",
        }
        protocol_exceptions = {
            "monthly_gacha",
        }

        self.assertEqual(76, len(audited_direct_modules))
        self.assertLessEqual(
            audited_direct_modules,
            set(ModuleListManager.name_to_modules),
        )
        self.assertLessEqual(audited_direct_modules, TW_SUPPORTED_MODULES)
        self.assertTrue(protocol_exceptions.isdisjoint(TW_SUPPORTED_MODULES))

    def test_encrypted_request_short_udid_signature_and_sid(self):
        sdk = _tw_sdk()
        client = apiclient(sdk)
        request = CheckAgreementRequest()
        api_module = importlib.import_module("autopcr.core.apiclient")

        # Deterministic random digits make SHORT-UDID a reproducible vector.
        with patch.object(api_module, "randint", return_value=0):
            wire = client._prepare_request(request, _KEY)

        iv = _UDID_COMPACT[:16].encode("ascii")
        packed, returned_key = _decrypt(wire, iv)
        payload = msgpack.unpackb(packed, raw=False, strict_map_key=False)

        expected_viewer = base64.b64encode(
            _encrypt(_VIEWER_ID.encode("ascii"), _KEY, iv)
        ).decode("ascii")
        expected_payload = {
            "viewer_id": expected_viewer,
            "tw_server_id": "2",
        }
        expected_packed = msgpack.packb(expected_payload, use_bin_type=False)

        self.assertEqual(_KEY, returned_key)
        self.assertEqual(expected_payload, payload)
        self.assertEqual(_encrypt(expected_packed, _KEY, iv), wire)
        self.assertEqual(
            hashlib.sha1(
                (
                    _UDID
                    + "/check/check_agreement"
                    + base64.b64encode(expected_packed).decode("ascii")
                    + _VIEWER_ID
                ).encode("utf-8")
            ).hexdigest(),
            client._headers["PARAM"],
        )

        encoded_short = client._headers["SHORT-UDID"]
        self.assertEqual(f"{len(_SHORT_UDID):04x}", encoded_short[:4])
        self.assertEqual(4 + 4 * len(_SHORT_UDID) + 32, len(encoded_short))
        self.assertEqual(
            _SHORT_UDID,
            "".join(
                chr(ord(encoded_short[4 + 4 * index + 2]) - 10)
                for index in range(len(_SHORT_UDID))
            ),
        )
        self.assertEqual(
            hashlib.md5(
                (_VIEWER_ID + _UDID + "r!I@nt8e5i=").encode("utf-8")
            ).hexdigest(),
            client._headers["SID"],
        )
        self.assertEqual(
            hashlib.md5(_UDID.encode("utf-8")).hexdigest(),
            client._headers["DEVICE-ID"],
        )
        self.assertEqual("6000.0.58f2", client._headers["X-Unity-Version"])
        self.assertIn("libcurl/8.10.1-DEV", client._headers["User-Agent"])
        self.assertEqual("00500030", client._headers["RES-VER"])
        self.assertFalse(sdk.use_system_proxy)

    def test_unknown_regional_party_type_is_preserved(self):
        known = LoadDeckData(deck_number=ePartyType.QUEST.value)
        regional = LoadDeckData(deck_number=141)

        self.assertEqual(ePartyType.QUEST, known.deck_number)
        self.assertEqual(141, regional.deck_number)

    def test_game_start_exposes_tw_570_optional_schema(self):
        request = TwCheckGameStartRequest(
            app_type=0,
            campaign_data="",
            campaign_sign="signature",
            campaign_user=2,
            adid="advertising-id",
            endpointArn="endpoint",
            countrycode="TW",
            FOXYOROKOBINODANCE="dance",
            FOXYOROKOBINOMAI="mai",
        )

        self.assertEqual(
            {
                "app_type": 0,
                "campaign_data": "",
                "campaign_sign": "signature",
                "campaign_user": 2,
                "adid": "advertising-id",
                "endpointArn": "endpoint",
                "countrycode": "TW",
                "FOXYOROKOBINODANCE": "dance",
                "FOXYOROKOBINOMAI": "mai",
            },
            request.dict(exclude_none=True),
        )
        self.assertEqual(
            {
                "apptype": 0,
                "campaign_data": "",
                "campaign_user": 2,
            },
            CheckGameStartRequest(
                apptype=0,
                campaign_data="",
                campaign_user=2,
            ).dict(exclude_none=True),
        )

    def test_tw_570_response_extensions_are_preserved(self):
        tw_gacha = GachaExecResponse.parse_obj({
            "remain_limit_count_bonus_list": [
                {"target_unit_id": 100101, "count": 2}
            ],
            "exchange_point_bonus_reward_list": [],
        })
        cn_gacha = GachaExecResponse.parse_obj({
            "remain_limit_count_bonus_list": [
                {
                    "target_unit_id": 100101,
                    "remain_limit_count_bonus": 3,
                }
            ]
        })
        home = HomeIndexResponse.parse_obj({
            "battlepass_info_list": [{
                "season_id": 1,
                "line_received_level_list": [{"line_id": 2, "level": 3}],
            }],
            "mirage_info": {
                "nemesis_progress": [{
                    "nemesis_id": 4,
                    "is_unlock_quest": True,
                }]
            },
            "direct_reward_list": [],
        })
        presents = PresentIndexResponse.parse_obj({
            "gift_message": [{
                "id": 5,
                "discription": "message",
                "type_1": 6,
            }]
        })
        shop = ShopBuyMultipleResponse.parse_obj({
            "user_jewel": {"jewel": 7, "free_jewel": 8}
        })

        self.assertEqual(2, tw_gacha.remain_limit_count_bonus_list[0].count)
        self.assertEqual(
            3,
            cn_gacha.remain_limit_count_bonus_list[0].remain_limit_count_bonus,
        )
        self.assertEqual(
            3,
            home.battlepass_info_list[0].line_received_level_list[0].level,
        )
        self.assertTrue(
            home.mirage_info.nemesis_progress[0].is_unlock_quest
        )
        self.assertEqual(6, presents.gift_message[0].type_1)
        self.assertEqual(8, shop.user_jewel.free_jewel)
        self.assertEqual(
            [10, 20],
            StorySkipInfo(movie_list=[10, 20]).movie_list,
        )

    def test_encrypted_response_round_trip_uses_udid_iv(self):
        sdk = _tw_sdk()
        client = apiclient(sdk)
        response = {
            "data_headers": {
                "result_code": 1,
                "required_res_ver": "00007025",
            },
            "data": {"maintenance_message": ""},
        }
        packed = msgpack.packb(response, use_bin_type=False)
        wire = base64.b64encode(_encrypt(packed, _KEY, client._request_iv))

        decoded, returned_key = apiclient._unpack(wire, client._request_iv)

        self.assertEqual(response, decoded)
        self.assertEqual(_KEY, returned_key)

    def test_short_udid_layout_for_decimal_characters(self):
        api_module = importlib.import_module("autopcr.core.apiclient")
        value = "1029384756"
        with patch.object(api_module, "randint", return_value=7):
            encoded = apiclient._encode_short_udid(value)

        self.assertEqual(f"{len(value):04x}", encoded[:4])
        self.assertEqual("7" * 32, encoded[-32:])
        self.assertEqual(
            value,
            "".join(
                chr(ord(encoded[4 + 4 * index + 2]) - 10)
                for index in range(len(value))
            ),
        )

    def test_session_identifiers_are_redacted_from_logs(self):
        safe = apiclient._safe_for_log({
            "SID": "secret",
            "data_headers": {"viewer_id": _VIEWER_ID},
            "ordinary": "kept",
        })
        self.assertEqual("<redacted>", safe["SID"])
        self.assertEqual(
            "<redacted>", safe["data_headers"]["viewer_id"]
        )
        self.assertEqual("kept", safe["ordinary"])


class TaiwanCredentialTests(unittest.TestCase):
    def test_composite_credentials_are_normalized_and_use_merged_server(self):
        sdk = _tw_sdk()

        self.assertEqual(_UDID, sdk.udid)
        self.assertEqual(_VIEWER_ID, sdk.viewer_id)
        self.assertEqual(2, sdk.server_id)
        self.assertEqual("https://api5-pc.so-net.tw/", sdk.apiroots[0])
        self.assertIn("https://api2-pc.so-net.tw/", sdk.apiroots)

    def test_explicit_credentials_infer_server_and_honor_api_override(self):
        info = account(
            _SHORT_UDID,
            _UDID,
            platform.Android,
            viewer_id="4123456789",
        )
        with patch.dict(
            os.environ,
            {"AUTOPCR_TW_API_ROOT": "https://localhost:9443/test"},
        ):
            sdk = twsdkclient(info)

        self.assertEqual(4, sdk.server_id)
        self.assertEqual("https://localhost:9443/test/", sdk.apiroots[0])
        self.assertEqual("https://api5-pc.so-net.tw/", sdk.apiroots[1])
        self.assertIn("https://api4-pc.so-net.tw/", sdk.apiroots)

    def test_explicit_viewer_overrides_composite_viewer_but_keeps_udid_and_server(self):
        explicit_viewer_id = "4123456789"
        info = account(
            _SHORT_UDID,
            f"{_UDID_COMPACT}:{_VIEWER_ID}:2",
            platform.Android,
            viewer_id=explicit_viewer_id,
        )
        with patch.dict(os.environ, {"AUTOPCR_TW_API_ROOT": ""}):
            sdk = twsdkclient(info)

        self.assertEqual(_UDID, sdk.udid)
        self.assertEqual(explicit_viewer_id, sdk.viewer_id)
        self.assertEqual(2, sdk.server_id)

    def test_pool_key_separates_transport_profiles(self):
        def make_sdk(app_version: str, api_root: str):
            info = account(
                _SHORT_UDID,
                _UDID,
                platform.Android,
                viewer_id=_VIEWER_ID,
                server_id=2,
                app_version=app_version,
            )
            with patch.dict(os.environ, {"AUTOPCR_TW_API_ROOT": api_root}):
                return twsdkclient(info)

        baseline = make_sdk("4.9.1", "https://tw-a.example.test/api")
        different_version = make_sdk("4.9.2", "https://tw-a.example.test/api")
        different_roots = make_sdk("4.9.1", "https://tw-b.example.test/api")

        self.assertNotEqual(baseline.pool_key, different_version.pool_key)
        self.assertNotEqual(baseline.pool_key, different_roots.pool_key)

    def test_invalid_credentials_are_rejected(self):
        cases = (
            account("", f"{_UDID}:{_VIEWER_ID}:2", platform.Android),
            account("short-udid", f"{_UDID}:{_VIEWER_ID}:2", platform.Android),
            account(_SHORT_UDID, f"not-a-uuid:{_VIEWER_ID}:2", platform.Android),
            account(_SHORT_UDID, f"{_UDID}:not-digits:2", platform.Android),
            account(_SHORT_UDID, _UDID, platform.Android, viewer_id=_VIEWER_ID, server_id=9),
        )
        for info in cases:
            with self.subTest(username=info.username, password=info.password):
                with self.assertRaises(ValueError):
                    twsdkclient(info)


class RegionalSchemaCompatibilityTests(unittest.TestCase):
    def test_query_fills_columns_missing_from_older_schema(self):
        engine = create_engine("sqlite://")
        with engine.begin() as connection:
            connection.exec_driver_sql(
                "CREATE TABLE unit_data ("
                "unit_id INTEGER PRIMARY KEY, unit_name TEXT NOT NULL)"
            )
            connection.exec_driver_sql(
                "INSERT INTO unit_data (unit_id, unit_name) "
                "VALUES (100101, '佩可莉姆')"
            )

        with Session(engine) as session:
            rows = UnitDatum.query(session).to_list()
            missing_table = UnitEnemyDatum.query(session).to_list()

        self.assertEqual(1, len(rows))
        self.assertEqual(100101, rows[0].unit_id)
        self.assertEqual("佩可莉姆", rows[0].unit_name)
        self.assertEqual("", rows[0].comment)
        self.assertEqual(0, rows[0].rarity)
        self.assertEqual(0, rows[0].normal_atk_cast_time)
        self.assertEqual([], missing_table)

    def test_query_uses_orm_attribute_key_for_renamed_database_column(self):
        engine = create_engine("sqlite://")
        with engine.begin() as connection:
            connection.exec_driver_sql(
                "CREATE TABLE equipment_data ("
                "equipment_id INTEGER PRIMARY KEY, def REAL NOT NULL)"
            )
            connection.exec_driver_sql(
                "INSERT INTO equipment_data (equipment_id, def) "
                "VALUES (101001, 12.5)"
            )

        with Session(engine) as session:
            rows = EquipmentDatum.query(session).to_list()

        self.assertEqual(1, len(rows))
        self.assertEqual(101001, rows[0].equipment_id)
        self.assertEqual(12.5, rows[0].def_)
        self.assertEqual("", rows[0].equipment_name)


class TaiwanSessionTests(unittest.IsolatedAsyncioTestCase):
    async def test_tw_transport_bypasses_system_proxy_by_default(self):
        sdk = _tw_sdk()
        sdk.use_system_proxy = False
        client = apiclient(sdk)
        response = {
            "data_headers": {
                "result_code": 1,
                "servertime": 123456789,
                "viewer_id": _VIEWER_ID,
            },
            "data": {},
        }
        wire = base64.b64encode(
            _encrypt(
                msgpack.packb(response, use_bin_type=False),
                _KEY,
                client._request_iv,
            )
        )

        class FakeResponse:
            status_code = 200
            headers = {}

            @property
            async def content(self):
                return wire

        post = AsyncMock(return_value=FakeResponse())
        api_module = importlib.import_module("autopcr.core.apiclient")
        with patch.object(api_module.aiorequests, "post", new=post):
            await client.request(CheckAgreementRequest())

        self.assertEqual(
            {"http": "", "https": ""},
            post.await_args.kwargs["proxies"],
        )

    async def test_game_start_request_has_no_cn_campaign_fields(self):
        requests = []

        class FakeHandler:
            async def request(self, request):
                requests.append(request)
                if request.url == "check/game_start":
                    return SimpleNamespace(
                        now_tutorial=True,
                        bundle_ver="00570000",
                    )
                if request.url == "load/index":
                    return SimpleNamespace(daily_reset_time=123456789)
                if request.url == "home/index":
                    return SimpleNamespace(quest_list=[])
                return SimpleNamespace()

        sdk = _tw_sdk()
        manager = sessionmgr(sdk)
        manager._container = SimpleNamespace(
            _headers={"RES-VER": "00017004"}, time=0
        )
        ensure_database = AsyncMock(return_value=600001)
        with patch(
            "autopcr.db.dbstart.ensure_database",
            new=ensure_database,
        ):
            await manager._login_tw(FakeHandler())

        game_start = next(
            request
            for request in requests
            if isinstance(request, TwCheckGameStartRequest)
        )
        self.assertEqual({}, game_start.dict(exclude_none=True))
        self.assertTrue(manager._logged)
        self.assertEqual("00017004", manager._container._headers["RES-VER"])
        self.assertEqual("00570000", manager._container._headers["BUNDLE-VER"])
        ensure_database.assert_awaited_once_with("tw", "00017004")

    async def test_incomplete_tutorial_does_not_start_database_extraction(self):
        class FakeHandler:
            async def request(self, request):
                if request.url == "check/game_start":
                    return SimpleNamespace(
                        now_tutorial=False,
                        bundle_ver=None,
                    )
                return SimpleNamespace()

        manager = sessionmgr(_tw_sdk())
        manager._container = SimpleNamespace(
            _headers={"RES-VER": "00500030"}, time=0
        )
        ensure_database = AsyncMock()
        with patch(
            "autopcr.db.dbstart.ensure_database",
            new=ensure_database,
        ), self.assertRaisesRegex(PanicError, "未完成教程"):
            await manager._login_tw(FakeHandler())

        ensure_database.assert_not_awaited()


class TaiwanZDailyModuleTests(unittest.IsolatedAsyncioTestCase):
    async def test_seven_gacha_exchange_does_not_repeat_index(self):
        # Import lazily: the modules package intentionally re-exports many
        # classes and should not perturb core module names during collection.
        from autopcr.module.modules.hatsune import hatsune_gacha_exchange

        event_id = 10080
        ticket_id = 900001
        event = SimpleNamespace(event_id=event_id)
        fake_db = SimpleNamespace(
            event_name={event_id: "test event"},
            get_open_event=lambda: [event],
            get_event_gacha_ticket_id=lambda _: ticket_id,
            is_seven_event=lambda _: True,
        )

        class FakeData:
            settings = SimpleNamespace(loop_box_multi_gacha_count=100)

            def __init__(self):
                self.ticket = 2

            def get_inventory(self, _):
                return self.ticket

            def set_inventory(self, _, value):
                self.ticket = value

        client = SimpleNamespace(
            data=FakeData(),
            get_event_top=AsyncMock(),
            get_event_gacha_index=AsyncMock(
                side_effect=[
                    SimpleNamespace(
                        event_gacha_info=SimpleNamespace(
                            gacha_step=1,
                            box_set_list=[],
                        )
                    ),
                    AssertionError("seven/gacha_index called twice"),
                ]
            ),
            exec_event_gacha=AsyncMock(return_value=SimpleNamespace()),
        )
        parent = SimpleNamespace(
            id="tw-seven-gacha-test",
            get_config=lambda _key, default=None: default,
        )
        module = hatsune_gacha_exchange(parent)

        with patch("autopcr.module.modules.hatsune.db", fake_db):
            await module.do_task(client)

        client.get_event_top.assert_awaited_once_with(event_id)
        client.get_event_gacha_index.assert_awaited_once_with(event_id)
        client.exec_event_gacha.assert_awaited_once_with(event_id, 2, 2)
        self.assertEqual(0, client.data.ticket)


class PlayerPrefsDecoderTests(unittest.TestCase):
    _secret = b"e806f6"

    @staticmethod
    def _xor(data: bytes, key: bytes) -> bytes:
        return bytes(
            value ^ key[index % len(key)]
            for index, value in enumerate(data)
        )

    @classmethod
    def _entry(cls, key: str, payload: bytes) -> str:
        encoded_key = base64.b64encode(
            cls._xor(key.encode("utf-8"), cls._secret)
        ).decode("ascii")
        encrypted_value = cls._xor(
            payload,
            key.encode("utf-8") + cls._secret,
        )
        # A seven-byte trailer with byte -5 == 0 selects the seven-byte trim.
        encoded_value = base64.b64encode(
            encrypted_value + b"\x00" * 7
        ).decode("ascii")
        return f'<string name="{encoded_key}">{encoded_value}</string>'

    @staticmethod
    def _encoded_udid(value: str) -> bytes:
        raw = bytearray(4 * 36 + 3)
        for index, char in enumerate(value):
            raw[4 * index + 6] = ord(char) + 10
        return bytes(raw)

    def test_decode_xml_extracts_udid_and_recombines_split_ids(self):
        entries = (
            self._entry("UDID", self._encoded_udid(_UDID)),
            self._entry("TW_SERVER_ID", struct.pack("<i", 2)),
            self._entry("VIEWER_ID_lowBits", struct.pack("<I", 12345)),
            self._entry("VIEWER_ID_highBits", struct.pack("<I", 1)),
            self._entry("SHORT_UDID", struct.pack("<i", 987654321)),
        )
        xml = "<map>" + "".join(entries) + "</map>"

        result = decode_xml(xml)

        self.assertEqual(_UDID, result["UDID"])
        self.assertEqual("2", result["TW_SERVER_ID"])
        self.assertEqual(str((2 << 30) | 12345), result["VIEWER_ID"])
        self.assertEqual("2987654321", result["SHORT_UDID"])

    def test_decode_xml_requires_a_valid_server_id(self):
        xml = "<map>" + self._entry(
            "TW_SERVER_ID", struct.pack("<i", 5)
        ) + "</map>"
        with self.assertRaisesRegex(ValueError, "1, 2, 3 or 4"):
            decode_xml(xml)


if __name__ == "__main__":
    unittest.main()
