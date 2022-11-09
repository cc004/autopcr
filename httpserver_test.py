from httpserver import HttpServer
from autopcr.modules import register_all

register_all()

server = HttpServer(port=13200)
server.run_forever()