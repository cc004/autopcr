import asyncio
from dataclasses import dataclass
import datetime
from enum import Enum

from dataclasses_json import dataclass_json

from ..module.modulebase import eResultStatus
from ..module.accountmgr import instance as usermgr, AccountManager
from ..db.database import db
from ..constants import CACHE_DIR
import os
from ..util.logger import instance as logger

CRONLOG_PATH = os.path.join(CACHE_DIR, "http_server", "cron_log.txt")

class eCronOperation(Enum):
    START = "start"
    FINISH = "finish"

@dataclass_json
@dataclass
class CronLog:
    operation: eCronOperation
    time: datetime.datetime
    qid: str
    account: str
    status: eResultStatus
    log: str = ""

    def __str__(self):
        return f"{db.format_time(self.time)} {self.operation.value} cron job: {self.qid} {self.account} {self.status.value}"

async def _cron(task):
    last = datetime.datetime.now() - datetime.timedelta(minutes=1)
    while True:
        await asyncio.sleep(30)
        cur = datetime.datetime.now()
        while cur.minute != last.minute or cur.hour != last.hour:
            last += datetime.timedelta(minutes=1)
            asyncio.get_event_loop().create_task(task(last))

async def real_run_cron(accountmgr: AccountManager, accounts_to_run, cur):
    async def run_one_account(account):
        nonlocal cur
        async with accountmgr.load(account) as mgr:
            try:
                await mgr.pre_cron_run(cur.hour, cur.minute)
                write_cron_log(eCronOperation.START, cur, accountmgr.qid, account, eResultStatus.SUCCESS)
                res = await mgr.do_daily()
                status = res.status
                cur = datetime.datetime.now()
                write_cron_log(eCronOperation.FINISH, cur,  accountmgr.qid, account, status)
            except Exception as e:
                logger.exception(f"error in cron job {accountmgr.qid} {account}: {e}")
                write_cron_log(eCronOperation.START, cur,  accountmgr.qid, account, eResultStatus.ERROR, str(e))
    
    await asyncio.gather(*[run_one_account(account) for account in accounts_to_run])
    
    await accountmgr.__aexit__(None, None, None)
    

async def _run_crons(cur: datetime.datetime):
    logger.info(f"doing cron check in {cur.hour} {cur.minute}")
    async def run_one_qid(qid):
        accountmgr = usermgr.load(qid, readonly=True)
        await accountmgr.__aenter__()
        try:
            accounts_to_run = []
            for account in accountmgr.accounts():
                async with accountmgr.load(account, readonly=True) as mgr:
                    if await mgr.is_cron_run(cur.hour, cur.minute):
                        accounts_to_run.append(account)
            
            if accounts_to_run:
                asyncio.get_event_loop().create_task(real_run_cron(accountmgr, accounts_to_run, cur))
                accountmgr = None
        finally:
            if accountmgr:
                await accountmgr.__aexit__(None, None, None)
    
    await asyncio.gather(*[run_one_qid(qid) for qid in usermgr.qids()])
        

def write_cron_log(operation: eCronOperation, cur: datetime.datetime, qid: str, account: str, status: eResultStatus, log: str = ""):
    if not os.path.exists(os.path.dirname(CRONLOG_PATH)):
        os.mkdir(os.path.dirname(CRONLOG_PATH))
    with open(CRONLOG_PATH, "a") as fp:
        fp.write(CronLog(operation, cur, qid, account, status, log).to_json() + "\n")

def queue_crons():
    async def task(cur):
        await _run_crons(cur)
    asyncio.get_event_loop().create_task(_cron(task))
