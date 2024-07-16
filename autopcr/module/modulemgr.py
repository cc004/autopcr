from dataclasses import dataclass

from dataclasses_json import dataclass_json
from typing import List, Dict, Tuple

from ..model.error import *
from ..model.enums import *
from ..db.database import db
from .modulebase import Module, ModuleResult, ModuleStatus

import traceback

@dataclass_json
@dataclass
class TaskResult:
    order: List[str]
    result: Dict[str, ModuleResult]

class ModuleManager:
    _modules: List[type] = []

    def __init__(self, config, parent):
        from .modules import daily_modules, tool_modules, cron_modules, hidden_modules
        from .modules.cron import CronModule
        from .accountmgr import Account

        self.parent: Account = parent
        self.cron_modules: List[CronModule] = [m(self) for m in cron_modules]
        self.daily_modules: List[Module] = [m(self) for m in daily_modules]
        self.tool_modules: List[Module] = [m(self) for m in tool_modules]
        self.hidden_modules: List[Module] = [m(self) for m in hidden_modules]
        self.name_to_modules: Dict[str, Module] = {m.key: m for m in (self.daily_modules + self.tool_modules + self.hidden_modules)}
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
                        hour, minute = time.split(":")[0:2]
                        is_clan_battle_run = config.get("clanbattle_run_" + key, False)
                        self._crons.append((int(hour), int(minute), is_clan_battle_run))
        except:
            traceback.print_exc()
            raise
    
    async def is_cron_run(self, hour: int, minute: int) -> bool:
        for cron in self.cron_modules:
            if await cron.is_cron_run(hour, minute):
                await cron.update_client(self.client)
                return True
        else:
            return False
    
    def get_config(self, name, default):
        return self.client.keys.get(name, default)

    def generate_config(self, modules: List[Module]):
        return {
            'config': {**{key: m.get_config(key) for m in modules for key in m.config}, **{m.key: m.get_config(m.key) for m in modules}},
            'order': [m.key for m in modules],
            'info': {m.key: m.generate_info() for m in modules},
        }

    def generate_daily_config(self):
        return self.generate_config(self.cron_modules + self.daily_modules)

    def generate_tools_config(self):
        return self.generate_config(self.tool_modules)
    
    async def do_daily(self, isAdminCall: bool = False) -> Tuple[TaskResult, ModuleStatus]:
        resp = await self.do_task(self.client.keys, self.daily_modules, isAdminCall)
        status = ModuleStatus.success
        if any(m.status == ModuleStatus.warning or m.status == ModuleStatus.abort for m in resp.result.values()):
            status = ModuleStatus.warning
        if any(m.status == ModuleStatus.panic or m.status == ModuleStatus.error for m in resp.result.values()):
            status = ModuleStatus.error
        await self.parent.save_daily_result(resp, status.value)
        return resp, status

    async def do_from_key(self, config: dict, key: str, isAdminCall: bool = False) -> Tuple[ModuleResult, str]:
        config.update({
            key: True,
            "stamina_relative_not_run": False
        })
        modules = [self.name_to_modules[key]]
        raw_resp = await self.do_task(config, modules, isAdminCall)
        resp = raw_resp.result[key] 
        await self.parent.save_single_result(key, resp)
        return resp, resp.status.value

    async def do_task(self, config: dict, modules: List[Module], isAdminCall: bool = False) -> TaskResult:
        if db.is_clan_battle_time() and self.parent.is_clan_battle_forbidden() and not isAdminCall:
            raise PanicError("会战期间禁止执行任务")

        client = self.client
        client.keys["stamina_relative_not_run"] = any(db.is_campaign(campaign) for campaign in client.keys.get("stamina_relative_not_run_campaign_before_one_day", []))

        client.keys.update(config)

        resp: TaskResult = TaskResult(
                order = [],
                result = {}
        )
        for module in modules:
            resp.order.append(module.key)
            resp.result[module.key] = await module.do_from(client)
            if resp.result[module.key].status == ModuleStatus.panic:
                break
        return resp

