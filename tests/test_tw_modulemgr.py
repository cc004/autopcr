import unittest
from unittest.mock import patch

from autopcr.core.region import REGION_CN, REGION_TW, reset_region, set_region
from autopcr.module.modulebase import ModuleResult
from autopcr.module.modulemgr import ModuleManager


class _Client:
    def __init__(self, events):
        self.events = events

    async def activate(self):
        self.events.append("activate")

    async def login(self):
        self.events.append("login")

    def deactivate(self):
        self.events.append("deactivate")


class _Database:
    def __init__(self, events):
        self.events = events

    async def enter_cache_scope(self):
        self.events.append("enter_cache")

    async def exit_cache_scope(self):
        self.events.append("exit_cache")

    def is_clan_battle_time(self):
        self.events.append("clan_check")
        return False

    def is_campaign(self, _campaign):
        return False


class _Module:
    key = "probe"

    def __init__(self, events):
        self.events = events

    async def do_from(self, _client):
        self.events.append("module")
        return ModuleResult()


class _Manager(ModuleManager):
    id = "module-manager-test"

    async def get_client(self):
        return self.client

    async def save_daily_result(self, *_args, **_kwargs):
        raise NotImplementedError

    async def save_single_result(self, *_args, **_kwargs):
        raise NotImplementedError

    def is_clan_battle_forbidden(self):
        return False


class RegionalModuleManagerOrderingTests(unittest.IsolatedAsyncioTestCase):
    async def _run(self, region):
        events = []
        manager = _Manager({})
        manager.client = _Client(events)
        database = _Database(events)
        token = set_region(region)
        try:
            with patch("autopcr.module.modulemgr.db", database):
                await manager.do_task({}, [_Module(events)])
        finally:
            reset_region(token)
        return events

    async def test_tw_logs_in_once_before_master_data_checks(self):
        self.assertEqual(
            [
                "activate",
                "login",
                "enter_cache",
                "clan_check",
                "module",
                "deactivate",
                "exit_cache",
            ],
            await self._run(REGION_TW),
        )

    async def test_cn_keeps_existing_no_prelogin_order(self):
        self.assertEqual(
            [
                "enter_cache",
                "clan_check",
                "activate",
                "module",
                "deactivate",
                "exit_cache",
            ],
            await self._run(REGION_CN),
        )


if __name__ == "__main__":
    unittest.main()
