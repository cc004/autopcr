from httpserver import HttpServer
from autopcr.modules import register_all

register_all()

server = HttpServer()
server.run_forever()