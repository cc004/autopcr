from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *


@timetype("time_cron1", "执行时间", "00:00")
@booltype("clanbattle_run_cron1", "会战期间执行", False)
@description('定时执行')
@name("定时任务1")
@default(False)
@notrunnable
class cron1(Module):
    async def do_task(self, client: pcrclient):
        pass


@timetype("time_cron2", "执行时间", "00:00")
@booltype("clanbattle_run_cron2", "会战期间执行", False)
@description('定时执行')
@name("定时任务2")
@default(False)
@notrunnable
class cron2(Module):
    async def do_task(self, client: pcrclient):
        pass


@timetype("time_cron3", "执行时间", "00:00")
@booltype("clanbattle_run_cron3", "会战期间执行", False)
@description('定时执行')
@name("定时任务3")
@default(False)
@notrunnable
class cron3(Module):
    async def do_task(self, client: pcrclient):
        pass


@timetype("time_cron4", "执行时间", "00:00")
@booltype("clanbattle_run_cron4", "会战期间执行", False)
@description('定时执行')
@name("定时任务4")
@default(False)
@notrunnable
class cron4(Module):
    async def do_task(self, client: pcrclient):
        pass
