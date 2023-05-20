import asyncio
import datetime
import os
from ..module.modulebase import ModuleManager

async def _cron(task):
    hour = datetime.datetime.now().hour
    while True:
        await asyncio.sleep(60)
        t = datetime.datetime.now().hour
        if t != hour:
            await task(hour)
            hour = t

async def _run_crons(path, hour):
    for file in os.listdir(path):
        if file.endswith('.json'):
            mgr = ModuleManager(os.path.join(path, file))
            print(f'Running cron#{hour} for {file}, crons = {mgr._crons}')
            await mgr.do_cron(hour)

def queue_crons(path):
    async def task(hour):
        await _run_crons(path, hour)
    asyncio.get_event_loop().create_task(_cron(task))