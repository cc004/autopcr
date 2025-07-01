from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *
from ...db.database import db

class CronModule(Module):
    def get_cron_time(self) -> str: ...

    async def is_cron_condition(self) -> bool: ...

    async def is_cron_time(self, nhour: int, nminute: int) -> bool:
        time_args = self.get_cron_time().split(":")
        hour, minute = time_args[0], time_args[1]
        return nhour == int(hour) and nminute == int(minute)

    async def update_client(self, client: pcrclient):
        client.set_cron_run()

    async def is_cron_run(self, hour: int, minute: int) -> bool:
        enable: bool = self.get_config(self.key)
        if enable and await self.is_cron_time(hour, minute) and await self.is_cron_condition():
            return True
        else:
            return False

class NormalCronModule(CronModule):
    def get_clanbattle_run_status(self) -> bool: ...
    def get_module_exclude_type(self) -> List[str]: ...

    async def is_cron_condition(self) -> bool:
        is_clan_battle_run = self.get_clanbattle_run_status()
        is_clan_battle_time = db.is_clan_battle_time()
        return not is_clan_battle_time or is_clan_battle_run

    async def update_client(self, client: pcrclient):
        await super().update_client(client)
        module_exclude_type = self.get_module_exclude_type()
        if "体力获取" in module_exclude_type:
            client.set_stamina_get_not_run()
        if "体力消耗" in module_exclude_type:
            client.set_stamina_consume_not_run()


@multichoice("module_exclude_type_cron1", "不执行日常模块", [], ['体力获取', '体力消耗'])
@booltype("clanbattle_run_cron1", "会战期间执行", False)
@timetype("time_cron1", "执行时间", "00:00")
@description('定时执行')
@name("定时任务1")
@default(False)
@notrunnable
class cron1(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron1")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron1")
    def get_module_exclude_type(self) -> List[str]:
        return self.get_config("module_exclude_type_cron1")

@multichoice("module_exclude_type_cron2", "不执行日常模块", [], ['体力获取', '体力消耗'])
@booltype("clanbattle_run_cron2", "会战期间执行", False)
@timetype("time_cron2", "执行时间", "00:00")
@description('定时执行')
@name("定时任务2")
@default(False)
@notrunnable
class cron2(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron2")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron2")
    def get_module_exclude_type(self) -> List[str]:
        return self.get_config("module_exclude_type_cron2")


@multichoice("module_exclude_type_cron3", "不执行日常模块", [], ['体力获取', '体力消耗'])
@booltype("clanbattle_run_cron3", "会战期间执行", False)
@timetype("time_cron3", "执行时间", "00:00")
@description('定时执行')
@name("定时任务3")
@default(False)
@notrunnable
class cron3(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron3")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron3")
    def get_module_exclude_type(self) -> List[str]:
        return self.get_config("module_exclude_type_cron3")

@multichoice("module_exclude_type_cron4", "不执行日常模块", [], ['体力获取', '体力消耗'])
@booltype("clanbattle_run_cron4", "会战期间执行", False)
@timetype("time_cron4", "执行时间", "00:00")
@description('定时执行')
@name("定时任务4")
@default(False)
@notrunnable
class cron4(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron4")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron4")
    def get_module_exclude_type(self) -> List[str]:
        return self.get_config("module_exclude_type_cron4")

@conditional_execution2('run_condition_cron5', [], desc='执行庆典', check=False)
@timetype("time_cron5", "执行时间", "00:00")
@description('该定时任务不执行体力消耗的操作')
@name("特别定时任务1")
@default(False)
@notrunnable
class cron5(CronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron5")

    async def is_cron_condition(self) -> bool:
        condition = self.get_config_instance("run_condition_cron5")
        ok, _ = await condition.do_check()
        return ok

    async def update_client(self, client: pcrclient):
        await super().update_client(client)
        client.set_stamina_consume_not_run()

@conditional_execution2('run_condition_cron6', [], desc='执行庆典', check=False)
@timetype("time_cron6", "执行时间", "00:00")
@description('该定时任务不执行体力获取的操作')
@name("特别定时任务2")
@default(False)
@notrunnable
class cron6(CronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron6")

    async def is_cron_condition(self) -> bool:
        condition = self.get_config_instance("run_condition_cron6")
        ok, _ = await condition.do_check()
        return ok

    async def update_client(self, client: pcrclient):
        await super().update_client(client)
        client.set_stamina_get_not_run()
