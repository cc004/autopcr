import asyncio
import datetime
import os
from ..module.modulebase import ModuleManager

async def _cron(task):
    hour = None
    while True:
        if datetime.datetime.now().hour != hour:
            await task(hour)
        await asyncio.sleep(60)

async def _run_crons(path, hour):
    for file in os.listdir(path):
        if file.endswith('.json'):
            mgr = ModuleManager(os.path.join(path, file))
            print(f'Running cron for {file}, crons = {mgr._crons}')
            await mgr.do_cron(hour)

def queue_crons(path):
    async def task(hour):
        await _run_crons(path, hour)
    asyncio.get_event_loop().create_task(_cron(task))