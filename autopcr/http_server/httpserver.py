import quart
from quart import redirect, request, render_template, Blueprint, session, url_for
from quart_session import Session
import os
from typing import Callable, Coroutine, Any
from ..module.accountmgr import Account, instance as accountmgr, AccountException
from ..constants import CACHE_DIR
from .tokenmgr import instance as tokenmgr
from .emailmgr import instance as emailmgr

CACHE_HTTP_DIR = os.path.join(CACHE_DIR, 'http_server')

class HttpServer:
    def __init__(self, host = '0.0.0.0', port = 2, qq_only = False):

        self.web = Blueprint('web', __name__, static_folder='assets', static_url_path='/assets')
        self.web_qid = Blueprint('web_qid', __name__, static_folder='assets', static_url_path='/assets', url_prefix = "/account")
        self.web_account = Blueprint('web_account', __name__, static_folder='assets', static_url_path='/assets', url_prefix = "/<string:acc>")

        self.api = Blueprint('api', __name__, url_prefix = "/api")
        self.api_token = Blueprint('api_token', __name__, url_prefix = "/token")
        self.api_qid = Blueprint('api_qid', __name__, url_prefix="/account")
        self.api_account = Blueprint('api_account', __name__, url_prefix="/<string:acc>")

        self.app = Blueprint('app', __name__, url_prefix = "/daily")

        self.quart = quart.Quart(__name__)
        self.quart.config['SESSION_TYPE'] = 'redis'
        # self.quart.config['SESSION_USE_SIGNER'] = True
        self.quart.config['PERMANENT_SESSION_LIFETIME'] = 60 * 10
        self.quart.config['SECRET_KEY'] = "<++>"
        Session(self.quart)

        self.api_qid.register_blueprint(self.api_account)
        self.api.register_blueprint(self.api_qid)
        self.api.register_blueprint(self.api_token)
        self.web_qid.register_blueprint(self.web_account)
        self.web.register_blueprint(self.web_qid)
        self.app.register_blueprint(self.web)
        self.app.register_blueprint(self.api)

        self.host = host
        self.port = port
        self.configure_routes()
        self.qq_only = qq_only

    @staticmethod
    def wrapaccount(readonly: bool = False, create_when_no_exist = False):
        def wrapper(func: Callable[[Account], Coroutine[Any, Any, Any]]):
            async def inner(qid: str, *args, **kwargs):
                acc = kwargs.get('acc')  # 获取路由中的参数
                if acc:
                    try:
                        async with accountmgr.load(qid, acc, readonly, create_when_no_exist) as mgr:
                            return await func(mgr)
                    except AccountException:
                        return "Invalid account", 400
                else: 
                    return "Please specify an account", 400
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @staticmethod
    def wrapqid(func: Callable[..., Coroutine[Any, Any, Any]]):
        async def wrapper(*args, **kwargs):
            if 'qid' not in session:
                return "Unauthorized. Please log in", 400
            return await func(qid = session['qid'], *args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    
    def configure_routes(self):
        # backend

        @self.api_qid.route('/', methods = ['GET', 'POST', "DELETE"])
        @HttpServer.wrapqid
        async def account_list(qid: str):
            if request.method == "GET":
                accounts_info = [accountmgr.load(qid, account, readonly = True).generate_info() for account in accountmgr.accounts(qid)]
                return accounts_info, 200
            elif request.method == "POST":
                return 'ok', 200
            elif request.method == "DELETE":
                accountmgr.delete(qid)
                return "ok", 200
            else:
                return "", 404

        @self.api_account.route('/', methods = ['POST'])
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly=False, create_when_no_exist=True)
        async def new_config(mgr):
            return 'ok', 200

        @self.api_account.route('/', methods = ['DELETE'])
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly=False)
        async def delete_account(mgr):
            mgr.delete()
            return "ok", 200

        @self.api_account.route('/info', methods = ['GET', "PUT"])
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly=False)
        async def get_info(mgr: Account):
            if request.method == 'GET':
                return mgr.generate_info()
            elif request.method == "PUT":
                data = await request.get_json()
                if not(data['username'] or mgr.data['username'] ) or not (data['password'] or mgr.data['password']):
                    return 'Incomplete Account!', 400
                for key in ['alian', 'username', 'password']:
                    if data[key] and len(data[key]) <= 64:
                        mgr.data[key] = data[key]
                return "ok", 200
            else:
                return "", 404

        @self.api_account.route('/config', methods = ['GET', "PUT"]) # TODO config -> daily
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly=False)
        async def get_config(mgr: Account):
            if request.method == 'GET':
                return mgr.generate_daily_info()
            elif request.method == "PUT":
                data = await request.get_json()
                mgr.data['config'] = data
                return "ok", 200
            else:
                return "", 404

        @self.api_account.route('/do_task', methods= ['GET']) # TODO do_task -> do_daily
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly=False)
        async def do_task(mgr: Account):
            if self.qq_only:
                return 'Please use in group', 400
            try:
                return await mgr.do_daily(), 200
            except Exception as e:
                return str(e), 502

        @self.api_account.route('/do_single', methods = ['POST'])
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly = False)
        async def do_single(mgr: Account):
            data = await request.get_json()
            config = data['config']
            module = data['order'] # list
            try:
                return await mgr.do_from_key(config, module), 200
            except Exception as e:
                return str(e), 502

        @self.api_account.route('/tools', methods = ['GET', 'PUT'])
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly=False)
        async def update_tools(mgr: Account):
            if request.method == "GET":
                return mgr.generate_tools_info()
            elif request.method == "PUT":
                # TODO save 
                return "ok", 200
            else:
                return "", 404

        @self.api.route('/login', methods = ['GET'])
        async def login_token():
            token = request.args.get('token')
            if not token:
                return "no token", 404
            ok, qid = tokenmgr.validate_token(token)
            if ok:
                session['qid'] = qid
                return redirect(url_for('app.web.web_qid.account'))
            else:
                return "no yet", 400

        @self.api.route('/validate', methods = ['POST'])
        async def validate(): # TODO think to check login or not
            data = await request.get_json()
            from ..bsdk.validator import validate_ok_dict
            if 'id' not in data:
                return "incorrect", 403
            id = data['id']
            validate_ok_dict[id] = data
            return "", 200

        @self.api_account.route('/query_validate', methods = ['GET'])
        @HttpServer.wrapqid
        @HttpServer.wrapaccount(readonly = True)
        async def query_validate(mgr: Account):
            from ..bsdk.validator import validate_dict
            if mgr.username not in validate_dict:
                return "empty", 404
            elif validate_dict[mgr.username] == "ok":
                del validate_dict[mgr.username]
                return "ok", 200
            else:
                url = validate_dict[mgr.username]
                del validate_dict[mgr.username]
                return url, 401

        # /api/token
        @self.api_token.route('/qq', methods = ['GET'])
        async def token_qq():
            token = tokenmgr.generate_token()
            return {"msg": "请在60秒内群里发送如下信息", "token": f"#login " + token}, 200

        @self.api_token.route('/email', methods = ['GET'])
        async def token_email():
            qid = request.args.get('qid')
            if not qid:
                return "", 401
            token = tokenmgr.generate_token(qid)
            from ...server import address
            url = address + f"/login?token={token}"
            to = qid + "@qq.com"
            await emailmgr.send_email(to, "autopcr", f'<a target="_blank" href="{url}">点击登录</a>')
            return "已发送邮件，请查收", 200

        # /api/token
        @self.api_token.route('/test', methods = ['GET'])
        async def token_test():
            token = tokenmgr.generate_token("1")
            print(token)
            return {"msg": "请在60秒内群里发送如下信息", "token": f"#login " + token}, 200

        # frontend
        @self.web.route('/', methods = ['GET'])
        async def index():
            return await render_template('index.html')

        @self.web_qid.route('/', methods = ['GET'])
        async def account():
            return await render_template('account.html')

        @self.web_account.route('/info', methods = ['GET'])
        async def tools(*args, **kwargs):
            acc = kwargs.get('acc')  # 获取路由中的参数
            return await render_template('info.html', acc = acc, url="tools")
        
        @self.web_account.route('/config', methods = ['GET'])
        async def config(*args, **kwargs):
            acc = kwargs.get('acc')  # 获取路由中的参数
            return await render_template('config.html', acc = acc, url="info")

        @self.web_account.route('/action', methods = ['GET'])
        async def action(*args, **kwargs):
            acc = kwargs.get('acc')  # 获取路由中的参数
            return await render_template('action.html', acc = acc, url="config")

        @self.web_account.route('/geetest.html', methods = ['GET'])
        async def geetest():
            return await render_template('geetest.html')

    def run_forever(self, loop):
        self.quart.register_blueprint(self.app)
        for rule in self.quart.url_map.iter_rules():
            print(f"{rule.rule}\t{', '.join(rule.methods)}")
        self.quart.run(host=self.host, port=self.port, loop=loop)
