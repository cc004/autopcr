import asyncio
import datetime
from ..module.accountmgr import instance as accountmgr


async def _cron(task):
    hour = datetime.datetime.now().hour
    while True:
        await asyncio.sleep(60)
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        await task(hour, minute)


async def _run_crons(hour, minute):
    for account in accountmgr.accounts():
        async def task(account):
            async with accountmgr.load(account) as mgr:
                print(f'Doing cron#{hour}:{minute} for {account}, crons = {mgr._crons}')
                await mgr.do_cron(hour, minute)

        asyncio.get_event_loop().create_task(task(account))


def queue_crons():
    async def task(hour, minute):
        await _run_crons(hour, minute)

    asyncio.get_event_loop().create_task(_cron(task))
