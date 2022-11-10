from .httpserver import HttpServer
from ..module.modules import register_all

register_all()

server = HttpServer(port=13200)
server.run_forever()