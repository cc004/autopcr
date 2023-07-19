import asyncio
import datetime
from ..module.accountmgr import instance as accountmgr

async def _cron(task):
    hour = datetime.datetime.now().hour
    while True:
        await asyncio.sleep(60)
        t = datetime.datetime.now().hour
        if t != hour:
            await task(t)
            hour = t

async def _run_crons(hour):
    for account in accountmgr.accounts():
        async def task():
            async with accountmgr.load(account) as mgr:
                print(f'Doing cron#{hour} for {account}, crons = {mgr._crons}')
                await mgr.do_cron(hour)
        asyncio.get_event_loop().create_task(task())



def queue_crons():
    async def task(hour):
        await _run_crons(hour)
    asyncio.get_event_loop().create_task(_cron(task))
