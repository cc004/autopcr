import asyncio

from .httpserver import HttpServer
from ..constants import SERVER_PORT, SERVER_HOST
from ..db.dbstart import db_start
from ..module.crons import queue_crons
from ..module.accountmgr import instance as usermgr
from ..openbao import instance as openbao
from ..constants import OPENBAO_ENABLED

server = HttpServer(host=SERVER_HOST, port=SERVER_PORT)

async def startup():
    if OPENBAO_ENABLED:
        await openbao.connect()
        openbao.start_background_tasks()
    await db_start()
    await usermgr.migrate_game_credentials()
    queue_crons()

loop = asyncio.get_event_loop()
loop.run_until_complete(startup())

server.run_forever(loop)
