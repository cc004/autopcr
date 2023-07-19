from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *

@timetype("time1", "执行时间", "00:00")
@description('定时任务1')
@default(False)
class cron1(Module):
    async def do_task(self, client: pcrclient):
        pass

