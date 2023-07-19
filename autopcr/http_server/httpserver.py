import quart
from quart import request, render_template, Blueprint
import os
import json
from typing import Callable, Coroutine, Any
from ..module.modulemgr import ModuleManager
from ..module.accountmgr import instance as accountmgr, AccountException
from ..constants import CONFIG_PATH

class HttpServer:
    def __init__(self, host = '0.0.0.0', port = 2, qq_only = False):
        self.app = Blueprint('autopcr', __name__, static_folder='statics', static_url_path='/statics', url_prefix="/daily")
        self.quart = quart.Quart(__name__)
        self.host = host
        self.port = port
        self.configure_routes()
        self.qq_only = qq_only
    
    @staticmethod
    def wrapaccount(func: Callable[[ModuleManager], Coroutine[Any, Any, Any]]):
        async def wrapper():
            acc = request.args.get('account')
            if acc is None:
                return 'No account specified', 400
            try:
                async with accountmgr.load(acc) as mgr:
                    return await func(mgr)
            except AccountException as e:
                return str(e), 400
        wrapper.__name__ = func.__name__
        return wrapper

    def configure_routes(self):
        # backend
        @self.app.route('/api/config', methods = ['GET'])
        @HttpServer.wrapaccount
        async def get_config(mgr: ModuleManager):
            return mgr.generate_config()

        @self.app.route('/api/config', methods = ['PUT'])
        @HttpServer.wrapaccount
        async def update_config(mgr: ModuleManager):
            data = await request.get_json()
            old_data = mgr.data

            if not (data['username'] and data['password'] and (data['qq'] or not self.qq_only)):
                data['qq'] = old_data['qq']
                data['username'] = old_data['username']
                data['password'] = old_data['password']
            elif not data['username'] or not data['password'] or not data['qq'] and self.qq_only:
                return {"statusCode": 400, "message": "Incomplete account"}, 400
            
            if '_last_result' in old_data:
                data['_last_result'] = old_data['_last_result']
            
            if '_last_clean_time' in old_data:
                data['_last_clean_time'] = old_data['_last_clean_time']

            mgr.data = data
            mgr._load_from(data)

            return {"statusCode": 200}, 200

        @self.app.route('/api/config', methods = ['DELETE'])
        async def delete_config():

            file = request.args.get('account')
            if file is None or not accountmgr.pathsyntax.fullmatch(file):
                return 'Invalid account', 400

            accountmgr.delete(file)

            return {"statusCode": 200}, 200

        @self.app.route('/api/config', methods = ['POST'])
        async def new_config():
            # if self.qq_only:
            #     return 'Please contact the maintenance to register', 400
            file = request.args.get('account')
            if file is None or not accountmgr.pathsyntax.fullmatch(file):
                return 'Invalid account', 400
                
            fn = os.path.join(CONFIG_PATH, file) + '.json'

            if os.path.exists(fn):
                return 'Account already exists', 400

            data = await request.get_json()
            print(data)
            with open(fn, 'w') as f:
                f.write(json.dumps(data))
            return '', 204

        @self.app.route('/api/do_task', methods= ['GET'])
        @HttpServer.wrapaccount
        async def do_task(mgr: ModuleManager):
            if self.qq_only:
                return 'Please use in group', 400
            file = request.args.get('account')
            return await mgr.do_daily()

        @self.app.route('/api/library_import', methods = ['GET'])
        @HttpServer.wrapaccount
        async def get_library(mgr: ModuleManager):
            return await mgr.get_library_import_data()

        # frontend
        @self.app.route('/', methods = ['GET'])
        async def index():
            return await render_template('index.html')
        
        @self.app.route('/config.html', methods = ['GET'])
        async def config():
            return await render_template('config.html')
        

    def run_forever(self, loop):
        self.quart.register_blueprint(self.app)
        self.quart.run(host=self.host, port=self.port, loop=loop)
    
