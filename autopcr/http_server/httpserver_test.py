from .httpserver import HttpServer
from ..module.modules import register_all
from ..module.crons import queue_crons
import asyncio

register_all()

server = HttpServer(port=13200)

queue_crons()

server.run_forever(asyncio.get_event_loop())
