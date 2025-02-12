import asyncio

from .httpserver import HttpServer
from ..constants import SERVER_PORT
from ..db.dbstart import db_start
from ..module.crons import queue_crons

server = HttpServer(port=SERVER_PORT)

queue_crons()

asyncio.get_event_loop().create_task(db_start())

server.run_forever(asyncio.get_event_loop())
