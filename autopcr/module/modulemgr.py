from dataclasses import dataclass

from dataclasses_json import dataclass_json
from typing import List, Dict
from abc import abstractmethod, abstractproperty

from ..util.logger import instance as logger
from ..util.draw import instance as drawer
from ..model.error import *
from ..model.enums import *
from ..db.database import db
from .modulebase import Module, ModuleResult, eResultStatus
from ..core.clientpool import PoolClientWrapper
import traceback
import os
import base64

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

@dataclass_json
@dataclass
class ResultInfo:
    alias: str = ""
    key: str = ""
    path: str = ""
    time: str = ""
    url: str = ""
    _type: str = ""
    status: eResultStatus = eResultStatus.SKIP

    def save_result(self, result):
        with open(self.path, 'w') as f:
            f.write(result.to_json())
    def delete_result(self):
        if os.path.exists(self.path):
            os.remove(self.path)
    def get_result(self):
        raise NotImplementedError
    def response(self, url_format: str):
        url = url_format.format(self.alias)
        return ResultInfo(alias = self.alias, key = self.key, time = self.time, url = url, status = self.status)

@dataclass_json
@dataclass
class TaskResultInfo(ResultInfo):
    _type: str = "daily_result"
    def get_result(self) -> TaskResult:
        with open(self.path, 'r') as f:
            return TaskResult.from_json(f.read())

@dataclass_json
@dataclass
class ModuleResultInfo(ResultInfo):
    _type: str = "single_result"
    def get_result(self) -> ModuleResult:
        with open(self.path, 'r') as f:
            return ModuleResult.from_json(f.read())

class ModuleManager:
    _modules: List[type] = []

    @abstractproperty
    def id(self) -> str: ...

    @abstractmethod
    async def get_client() -> PoolClientWrapper: ...

    @abstractmethod
    async def save_daily_result(self, resp: TaskResult, status: eResultStatus) -> TaskResultInfo: ...

    @abstractmethod
    async def save_single_result(self, key: str, resp: ModuleResult) -> ModuleResultInfo: ...

    @abstractmethod
    def is_clan_battle_forbidden(self) -> bool: ...

    def __init__(self, config: dict):
        from .modulelistmgr import ModuleListManager
        self.modules_list: ModuleListManager = ModuleListManager(self)
        self.config = config
    
    async def __aenter__(self):
        self.client = await self.get_client()
        self.client.set_config(self.config)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def is_cron_run(self, hour: int, minute: int) -> bool:
        for cron in self.modules_list.cron_modules:
            if await cron.is_cron_run(hour, minute):
                return True
        else:
            return False
    
    async def pre_cron_run(self, hour: int, minute: int):
        for cron in self.modules_list.cron_modules:
            if await cron.is_cron_run(hour, minute):
                await cron.update_client(self.client)
                return
    
    def get_config(self, name, default):
        return self.config.get(name, default)

    def generate_modules_info(self, key: str):
        return self.modules_list.generate_info(key)

    def generate_tab(self, clan: bool = False, batch: bool = False):
        return self.modules_list.generate_tab(clan, batch)
    
    async def do_daily(self, isAdminCall: bool = False) -> "TaskResultInfo":
        resp = await self.do_task(self.config, self.modules_list.daily_modules, isAdminCall)
        status = eResultStatus.SUCCESS
        if any(m.status == eResultStatus.WARNING or m.status == eResultStatus.ABORT for m in resp.result.values()):
            status = eResultStatus.WARNING
        if any(m.status == eResultStatus.PANIC or m.status == eResultStatus.ERROR for m in resp.result.values()):
            status = eResultStatus.ERROR
        res = await self.save_daily_result(resp, status)
        await self.report_result(resp, status)
        return res

    async def do_from_key(self, config: dict, key: str, isAdminCall: bool = False) -> "ModuleResultInfo":
        config.update({
            key: True,
        })
        modules = [self.modules_list.get_module_from_key(key)]
        raw_resp = await self.do_task(config, modules, isAdminCall)
        resp = raw_resp.result[key] 
        res = await self.save_single_result(key, resp)
        return res

    async def do_task(self, config: dict, modules: List[Module], isAdminCall: bool = False) -> TaskResult:
        await db.enter_cache_scope()
        try:
            if db.is_clan_battle_time() and self.is_clan_battle_forbidden() and not isAdminCall:
                key = 'clan_battle' if not modules else modules[0].key
                return TaskResult(
                    order = [key],
                    result = {
                        key: ModuleResult(
                            status = eResultStatus.PANIC,
                            log = "会战期间禁止执行任务"
                        )
                    }
                )

            client = self.client
            activated = False
            await client.activate()
            activated = True
            try:
                self.config["stamina_relative_not_run"] = any(db.is_campaign(campaign) for campaign in self.config.get("stamina_relative_not_run_campaign_before_one_day", []))

                self.config.update(config)

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
            finally:
                if activated:
                    client.deactivate()
        finally:
            await db.exit_cache_scope()


    async def report_result(self, resp: TaskResult, status: eResultStatus) -> None:
        """任务执行完成后发送邮件报告"""
        try:
            # 使用 Drawer 绘制图片            
            img = await drawer.draw_tasks_result(resp)
            
            # 转为 Base64
            img_byte_arr = await drawer.img2bytesio(img, format='PNG')
            img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            
            # 构建 HTML
            html_body = f"""
            <html>
                <body>
                    <h2>📊 任务执行报告</h2>
                    <p>状态: {status.value}</p>
                    <img src="data:image/png;base64,{img_base64}" style="max-width: 100%;">
                </body>
            </html>
            """
            
            # 发送邮件
            notify_list = self.modules_list.notify_modules
            for notify in notify_list:
                
                if notify.is_configured():
                    await notify.send_notification(
                        subject=f"【AutoPCR】任务报告 - {status.value}",
                        body=html_body,
                        is_html=True
                    )
                    
        except Exception:
            logger.exception("发送邮件报告失败: ")
