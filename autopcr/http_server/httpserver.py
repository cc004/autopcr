import quart
from quart import request, render_template
import os
import re
import json
from ..module.modulebase import ModuleManager

class HttpServer:
    pathsyntax = re.compile(r'[a-zA-Z0-9_]{1,32}')
    def __init__(self, host = '0.0.0.0', port = 2):
        self.app = quart.Quart(__name__)
        self.host = host
        self.port = port
        self.configure_routes()
        self.config_path = os.path.join(os.path.dirname(__file__), 'config')

    def configure_routes(self):
        # backend
        @self.app.route('/api/config', methods = ['GET'])
        async def get_config():
            file = request.args.get('account')
            fn = os.path.join(self.config_path, file) + '.json'

            if not HttpServer.pathsyntax.match(file) or not os.path.exists(fn):
                return 'Invalid account', 400
            mgr = ModuleManager(fn)
            return mgr.generate_config()
        
        @self.app.route('/api/config', methods = ['POST'])
        async def update_config():
            data = await request.get_json()
            file = request.args.get('account')
            fn = os.path.join(self.config_path, file) + '.json'

            if not HttpServer.pathsyntax.match(file) or not os.path.exists(fn):
                return 'Invalid account', 400
            with open(fn, 'w') as f:
                f.write(json.dumps(data))
            return '', 204

        @self.app.route('/api/config', methods = ['PUT'])
        async def new_config():
            data = await request.get_json()
            file = request.args.get('account')
            fn = os.path.join(self.config_path, file) + '.json'

            if not HttpServer.pathsyntax.match(file):
                return 'Invalid account', 400
            if os.path.exists(fn):
                return 'Account already exists', 400
            with open(fn, 'w') as f:
                f.write(json.dumps(data))
            return '', 204
        @self.app.route('/api/do_task', methods= ['GET'])
        async def do_task():
            file = request.args.get('account')
            fn = os.path.join(self.config_path, file) + '.json'

            if not HttpServer.pathsyntax.match(file) or not os.path.exists(fn):
                return 'Invalid account', 400
            mgr = ModuleManager(fn)

            return await mgr.do_task()
        # frontend
        @self.app.route('/', methods = ['GET'])
        async def index():
            return await render_template('index.html')
        
        @self.app.route('/config.html', methods = ['GET'])
        async def config():
            return await render_template('config.html')
        

    def run_forever(self, loop):
        self.app.run(host=self.host, port=self.port, loop=loop)
    
