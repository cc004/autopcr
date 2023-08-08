from ..core.pcrclient import pcrclient
from typing import List, Dict, Union
from ..model.error import *
from ..model.enums import *
from ..db.database import db
from .modulebase import Module

import json
import traceback
class ModuleManager:
    _modules: List[type] = []

    def __init__(self, config, parent):
        from .modules import daily_modules, tool_modules, cron_modules
        from .accountmgr import Account

        self.parent: Account = parent
        self.cron_modules: List[Module] = [m(self) for m in cron_modules]
        self.daily_modules: List[Module] = [m(self) for m in daily_modules]
        self.tool_modules: List[Module] = [m(self) for m in tool_modules]
        self.name_to_modules: Dict[str, Module] = {m.key: m for m in (self.daily_modules + self.tool_modules)}
        self.client = self.parent.get_client()
        self._crons = []
        self._load_config(config)
    
    def _load_config(self, config):
        try:
            self._crons.clear()
            for key, value in config.items():
                self.client.keys[key] = value

            for key in [key for key in config if key.startswith("cron")]:
                enable = config[key]
                if enable:
                    time = config.get("time_" + key, "25:00")
                    if time: # in some case time is None
                        hour, minute = time.split(":")
                        is_clan_battle_run = config.get("clanbattle_run_" + key, False)
                        self._crons.append((int(hour), int(minute), is_clan_battle_run))
        except:
            traceback.print_exc()
            raise
    
    def is_cron_run(self, nhour, nminute):
        clan_battle_time = db.is_clan_battle_time()
        for hour, minute, is_clan_battle_run in self._crons:
            if hour == nhour and minute == nminute and (is_clan_battle_run or not clan_battle_time):
                return True
        return False
    
    def get_config(self, name, default):
        return self.client.keys.get(name, default)

    def generate_config(self, modules: List[Module]):
        return {
            'config': {**{key: m.get_config(key) for m in modules for key in m.config}, **{m.key: m.get_config(m.key) for m in modules}},
            'order': [m.key for m in modules],
            'data': {m.key: m.generate_info() for m in modules},
        }

    def generate_daily_config(self):
        return self.generate_config(self.cron_modules + self.daily_modules)

    def generate_tools_config(self):
        return self.generate_config(self.tool_modules)
    
    async def do_cron(self, hour, minute):
        if self.is_cron_run(hour, minute):
            await self.do_daily()

    async def do_daily(self):
        return await self.do_task(self.client.keys, self.daily_modules)

    async def do_from_key(self, config: dict, keys: List[str]):
        config.update({key: True for key in keys})
        modules = [self.name_to_modules[m] for m in keys]
        return await self.do_task(config, modules)

    async def do_task(self, config: dict, modules: List[Module]):
        self.client.keys = config

        resp: Dict[str, Union[List[str], Dict[str, Dict[str, str]]]] = {}
        resp['order'] = [m.key for m in modules]
        resp['result'] = {}
        try:
            client = self.client
            await client.login()
            for module in modules:
                resp['result'][module.__class__.__name__] = await module.do_from(client)
        except Exception as e:
            traceback.print_exc()
            raise(e)
        finally:
            await self.parent.set_result(resp['result'])
        return resp

