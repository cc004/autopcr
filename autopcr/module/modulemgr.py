from dataclasses import dataclass

from dataclasses_json import dataclass_json
from typing import List, Dict

from ..model.error import *
from ..model.enums import *
from ..db.database import db
from .modulebase import Module, ModuleResult, eResultStatus

import traceback

@dataclass_json
@dataclass
class TaskResult:
    order: List[str]
    result: Dict[str, ModuleResult]

    def get_last_result(self) -> ModuleResult:
        if self.order:
            return self.result[self.order[-1]]
        else:
            return ModuleResult()

class ModuleManager:
    _modules: List[type] = []

    def __init__(self, config, parent):
        from .modulelistmgr import ModuleListManager
        from .accountmgr import Account

        self.parent: Account = parent
        self.modules_list: ModuleListManager = ModuleListManager(self)
        self.client = self.parent.get_client()
        self._load_config(config)
    
    def _load_config(self, config):
        try:
            for key, value in config.items():
                self.client.keys[key] = value
        except:
            traceback.print_exc()
            raise
    
    async def is_cron_run(self, hour: int, minute: int) -> bool:
        for cron in self.modules_list.cron_modules:
            if await cron.is_cron_run(hour, minute):
                await cron.update_client(self.client)
                return True
        else:
            return False
    
    def get_config(self, name, default):
        return self.client.keys.get(name, default)

    def generate_modules_info(self, key: str):
        return self.modules_list.generate_info(key)

    def generate_tab(self, clan: bool = False, batch: bool = False):
        return self.modules_list.generate_tab(clan, batch)
    
    async def do_daily(self, isAdminCall: bool = False) -> "TaskResultInfo":
        resp = await self.do_task(self.client.keys, self.modules_list.daily_modules, isAdminCall)
        status = eResultStatus.SUCCESS
        if any(m.status == eResultStatus.WARNING or m.status == eResultStatus.ABORT for m in resp.result.values()):
            status = eResultStatus.WARNING
        if any(m.status == eResultStatus.PANIC or m.status == eResultStatus.ERROR for m in resp.result.values()):
            status = eResultStatus.ERROR
        res = await self.parent.save_daily_result(resp, status)
        return res

    async def do_from_key(self, config: dict, key: str, isAdminCall: bool = False) -> "ModuleResultInfo":
        config.update({
            key: True,
        })
        modules = [self.modules_list.get_module_from_key(key)]
        raw_resp = await self.do_task(config, modules, isAdminCall)
        resp = raw_resp.result[key] 
        res = await self.parent.save_single_result(key, resp)
        return res

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
            if resp.result[module.key].status == eResultStatus.PANIC:
                break
        return resp

