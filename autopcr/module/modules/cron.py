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
class cron1(Module):
    async def do_task(self, client: pcrclient):
        pass

