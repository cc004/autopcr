from .httpserver import HttpServer
from ..module.crons import queue_crons
import asyncio

server = HttpServer(port=13200)

queue_crons()

server.run_forever(asyncio.get_event_loop())
