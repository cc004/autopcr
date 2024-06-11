import asyncio
import datetime
from ..module.accountmgr import instance as usermgr
from ..db.database import db
from ..constants import CACHE_DIR
import os

cron_log_buffer = asyncio.Queue()
CRONLOG_PATH = os.path.join(CACHE_DIR, "http_server", "cron_log.txt")

async def _cron(task):
    last = datetime.datetime.now() - datetime.timedelta(minutes=1)
    while True:
        await asyncio.sleep(30)
        cur = datetime.datetime.now()
        if cur.minute == last.minute: continue
        last = cur
        asyncio.get_event_loop().create_task(task(cur))

async def task(qid, account):
    async with usermgr.load(qid, readonly=True) as accountmgr:
        async with accountmgr.load(account) as mgr:
            _, status = await mgr.do_daily()
            cur = datetime.datetime.now()
            await cron_log_buffer.put(f"{db.format_time(cur)}: done cron for {qid} {account}, {status}")

async def _run_crons(cur):
    print(f"doing cron check in {cur.hour} {cur.minute}")
    for qid in usermgr.qids():
        async with usermgr.load(qid, readonly=True) as accountmgr:
            for account in accountmgr.accounts():
                async with accountmgr.load(account, readonly=True) as acc:
                    if acc.is_cron_run(cur.hour, cur.minute):
                        asyncio.get_event_loop().create_task(task(qid, account))
                        await cron_log_buffer.put(f"{db.format_time(cur)}: doing cron for {qid} {account}")

async def cron_log():
    if not os.path.exists(os.path.dirname(CRONLOG_PATH)):
        os.mkdir(os.path.dirname(CRONLOG_PATH))
    fp = open(CRONLOG_PATH, "a")
    while True:
        log = await cron_log_buffer.get()
        fp.write(log + "\n")
        fp.flush()

def queue_crons():
    async def task(cur):
        await _run_crons(cur)
    asyncio.get_event_loop().create_task(_cron(task))
    asyncio.get_event_loop().create_task(cron_log())
