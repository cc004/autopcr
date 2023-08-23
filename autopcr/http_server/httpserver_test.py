from .httpserver import HttpServer
from ..module.crons import queue_crons
from ..db.dbstart import db_start
import asyncio

server = HttpServer(port=13200)

# queue_crons()

asyncio.get_event_loop().create_task(db_start())

server.run_forever(asyncio.get_event_loop())
