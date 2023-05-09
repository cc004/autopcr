import quart
from quart import request, render_template, Blueprint
import os
import re
import json
from ..module.modulebase import ModuleManager

class HttpServer:
    pathsyntax = re.compile(r'[a-zA-Z0-9_]{1,32}')
    def __init__(self, host = '0.0.0.0', port = 2, qq_only = False):
        self.app = Blueprint('autopcr', __name__, static_folder='statics', static_url_path='/statics', url_prefix="/daily")
        self.quart = quart.Quart(__name__)
        self.host = host
        self.port = port
        self.configure_routes()
        self.qq_only = qq_only
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
        
        @self.app.route('/api/config', methods = ['PUT'])
        async def update_config():
            data = await request.get_json()
            file = request.args.get('account')
            fn = os.path.join(self.config_path, file) + '.json'

            if not HttpServer.pathsyntax.match(file) or not os.path.exists(fn):
                return 'Invalid account', 400
            if data['username'] == "" and data['password'] == "" and data['qq'] == "":
                with open(fn, 'r') as f:
                    old_data = json.load(f)
                    data['qq'] = old_data['qq']
                    data['username'] = old_data['username']
                    data['password'] = old_data['password']
            with open(fn, 'w') as f:
                f.write(json.dumps(data))
            return '', 204

        @self.app.route('/api/config', methods = ['POST'])
        async def new_config():
            # if self.qq_only:
            #     return 'Please contact the maintenance to register', 400
            data = await request.get_json()
            print(data)
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
            if self.qq_only:
                return 'Please use in group', 400
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
        

    def run_forever(self):
        self.quart.register_blueprint(self.app)
        self.quart.run(host=self.host, port=self.port)
    
