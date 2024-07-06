import asyncio
from dataclasses import dataclass
import datetime
from enum import Enum
import traceback

from dataclasses_json import dataclass_json

from ..module.modulebase import ModuleStatus
from ..module.accountmgr import instance as usermgr
from ..db.database import db
from ..constants import CACHE_DIR
import os

CRONLOG_PATH = os.path.join(CACHE_DIR, "http_server", "cron_log.txt")

class CronOperation(Enum):
    START = "start"
    FINISH = "finish"

@dataclass_json
@dataclass
class CronLog:
    operation: CronOperation
    time: datetime.datetime
    qid: str
    account: str
    status: ModuleStatus
    log: str = ""

    def __str__(self):
        return f"{db.format_time(self.time)} {self.operation.value} cron job: {self.qid} {self.account} {self.status.value}"

async def _cron(task):
    last = datetime.datetime.now() - datetime.timedelta(minutes=1)
    while True:
        await asyncio.sleep(30)
        cur = datetime.datetime.now()
        if cur.minute == last.minute: continue
        last = cur
        asyncio.get_event_loop().create_task(task(cur))

async def task(qid, account, cur):
    async with usermgr.load(qid, readonly=True) as accountmgr:
        async with accountmgr.load(account) as mgr:
            try:
                if await mgr.is_cron_run(cur.hour, cur.minute):
                    write_cron_log(CronOperation.START, cur, qid, account, ModuleStatus.success)
                    _, status = await mgr.do_daily()
                    cur = datetime.datetime.now()
                    write_cron_log(CronOperation.FINISH, cur, qid, account, status)
            except Exception as e:
                print(f"error in cron job {qid} {account}")
                traceback.print_exc()
                write_cron_log(CronOperation.START, cur, qid, account, ModuleStatus.error, str(e))

async def _run_crons(cur):
    print(f"doing cron check in {cur.hour} {cur.minute}")
    for qid in usermgr.qids():
        async with usermgr.load(qid, readonly=True) as accountmgr:
            for account in accountmgr.accounts():
                asyncio.get_event_loop().create_task(task(qid, account, cur))

def write_cron_log(operation: CronOperation, cur: datetime.datetime, qid: str, account: str, status: ModuleStatus, log: str = ""):
    if not os.path.exists(os.path.dirname(CRONLOG_PATH)):
        os.mkdir(os.path.dirname(CRONLOG_PATH))
    with open(CRONLOG_PATH, "a") as fp:
        fp.write(CronLog(operation, cur, qid, account, status, log).to_json() + "\n")

def queue_crons():
    async def task(cur):
        await _run_crons(cur)
    asyncio.get_event_loop().create_task(_cron(task))
