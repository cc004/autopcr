from copy import deepcopy
from datetime import timedelta
import traceback
import quart, asyncio
from quart import request, Blueprint, send_file, send_from_directory
from quart_rate_limiter import RateLimiter, rate_limit, RateLimitExceeded
from quart_auth import AuthUser, QuartAuth, Unauthorized, current_user, login_required, login_user, logout_user
from quart_compress import Compress
import secrets, os, io
from typing import Callable, Coroutine, Any

from ..module.accountmgr import Account, AccountManager, UserException, instance as usermgr, AccountException
from ..constants import CACHE_DIR
from ..util.draw import instance as drawer
from .validator import validate_dict, ValidateInfo, validate_ok_dict, enable_manual_validator

APP_VERSION = "1.2.0"

CACHE_HTTP_DIR = os.path.join(CACHE_DIR, 'http_server')

PATH = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(PATH, 'ClientApp')


class HttpServer:
    def __init__(self, host = '0.0.0.0', port = 2, qq_mod = False):

        self.web = Blueprint('web', __name__, static_folder=static_path)

        # version check & rate limit
        self.api_limit = Blueprint('api_limit', __name__, url_prefix = "/api")
        self.api = Blueprint('api', __name__, url_prefix = "/api")

        self.app = Blueprint('app', __name__, url_prefix = "/daily")

        self.quart = quart.Quart(__name__)
        QuartAuth(self.quart, cookie_secure=False)
        RateLimiter(self.quart)
        Compress(self.quart)
        self.quart.secret_key = secrets.token_urlsafe(16)

        self.app.register_blueprint(self.web)
        self.app.register_blueprint(self.api)
        self.app.register_blueprint(self.api_limit)

        self.host = host
        self.port = port
        self.validate_server = {}
        self.configure_routes()
        self.qq_mod = qq_mod

        enable_manual_validator()
        

    @staticmethod
    def wrapaccount(readonly = False):
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
            async def inner(accountmgr: AccountManager, acc: str, *args, **kwargs):
                if acc:
                    async with accountmgr.load(acc, readonly) as mgr:
                        return await func(mgr, *args, **kwargs)
                else: 
                    return "Please specify an account", 400
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @staticmethod
    def wrapaccountmgr(readonly = False):
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
            async def inner(*args, **kwargs):
                qid: str = current_user.auth_id
                async with usermgr.load(qid, readonly) as mgr:
                    return await func(accountmgr = mgr, *args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper
    
    def configure_routes(self):

        @self.api_limit.before_request
        async def check_app_version():
            version = request.headers.get('X-App-Version', None)
            if version != APP_VERSION:
                return f"后端期望前端版本为{APP_VERSION}，请更新", 400
            else:
                return None

        @self.api_limit.errorhandler(RateLimitExceeded)
        async def handle_rate_limit_exceeded_error(error):
            return "您冲得太快了，休息一下吧", 429

        @self.api.errorhandler(Unauthorized)
        async def redirect_to_login(*_: Exception):
            return "未登录，请登录", 401

        @self.api.errorhandler(ValueError)
        async def handle_value_error(e):
            return str(e), 400

        @self.api.errorhandler(AccountException)
        async def handle_account_exception(e):
            traceback.print_exc()
            return str(e), 400

        @self.api.errorhandler(Exception)
        async def handle_general_exception(e):
            traceback.print_exc()
            return "服务器发生错误", 500

        @self.api.route('/account', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        async def get_info(accountmgr: AccountManager):
            return await accountmgr.generate_info(), 200

        @self.api.route('/account', methods = ["PUT"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def put_info(accountmgr: AccountManager):
            data = await request.get_json()
            default_accont = data.get('default_account', '')
            if default_accont:
                accountmgr.set_default_account(default_accont)
            return "保存成功", 200

        @self.api.route('/account', methods = ["POST"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def create_account(accountmgr: AccountManager):
            data = await request.get_json()
            acc = data.get("alias", "")
            accountmgr.create_account(acc.strip())
            return "创建账号成功", 200

        @self.api.route('/account/import', methods = ["POST"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def create_accounts(accountmgr: AccountManager):
            file = await request.files
            if 'file' not in file:
                return "请选择文件", 400
            file = file['file']
            if file.filename.split('.')[-1] != 'tsv':
                return "文件格式错误", 400
            data = file.read().decode()
            ok, msg = await accountmgr.create_accounts_from_tsv(data)
            return msg, 200 if ok else 400

        @self.api.route('/', methods = ["DELETE"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def delete_qq(accountmgr: AccountManager):
            accountmgr.delete_mgr()
            logout_user()
            return "删除QQ成功", 200

        @self.api.route('/account', methods = ["DELETE"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def delete_account(accountmgr: AccountManager):
            accountmgr.delete_all_accounts()
            return "删除账号成功", 200

        @self.api.route('/account/sync', methods = ["POST"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def sync_account_config(accountmgr: AccountManager):
            data = await request.get_json()
            acc = data.get("alias", "")
            if acc not in accountmgr.accounts():
                return "账号不存在", 400
            async with accountmgr.load(acc) as mgr:
                for ano in accountmgr.accounts():
                    if ano != acc:
                        async with accountmgr.load(ano) as other:
                            other.data.config = mgr.data.config
            return "配置同步成功", 200

        @self.api.route('/account/<string:acc>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly=True)
        async def get_account(account: Account):
            return account.generate_info(), 200

        @self.api.route('/account/<string:acc>', methods = ["PUT", "DELETE"])
        @login_required
        @HttpServer.wrapaccountmgr()
        @HttpServer.wrapaccount()
        async def update_account(account: Account):
            if request.method == "PUT":
                data = await request.get_json()
                if 'username' in data:
                    account.data.username = data['username']
                if 'password' in data and data['password'] != '*' * 8:
                    account.data.password = data['password']
                if 'channel' in data:
                    account.data.channel = data['channel']
                if 'batch_accounts' in data:
                    account.data.batch_accounts = data['batch_accounts']
                return "保存账户信息成功", 200
            elif request.method == "DELETE":
                account.delete()
                return "删除账户信息成功", 200
            else:
                return "", 404

        @self.api.route('/account/<string:acc>/<string:modules_key>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def get_modules_config(mgr: Account, modules_key: str):
            return mgr.generate_modules_info(modules_key)

        @self.api.route('/account/<string:acc>/config', methods = ['PUT'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount()
        async def put_config(mgr: Account):
            data = await request.get_json()
            mgr.data.config.update(data)
            return "配置保存成功", 200

        @self.api.route('/account/<string:acc>/do_daily', methods = ['POST'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly=True)
        @HttpServer.wrapaccount()
        async def do_daily(mgr: Account):
            await mgr.do_daily(mgr._parent.secret.clan)
            return mgr.generate_result_info(), 200

        @self.api.route('/account/<string:acc>/daily_result', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def daily_result_list(mgr: Account):
            resp = mgr.get_daily_result_list()
            resp = [r.response('/daily/api/account/{}' + '/daily_result/' + str(r.key)) for r in resp]
            return resp, 200

        @self.api.route('/account/<string:acc>/daily_result/<string:key>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def daily_result(mgr: Account, key: str):
            resp_text = request.args.get('text', 'false').lower()
            resp = await mgr.get_daily_result_from_key(key)
            if not resp:
                return "无结果", 404
            if resp_text == 'false':
                img = await drawer.draw_tasks_result(resp)
                bytesio = await drawer.img2bytesio(img, 'webp')
                return await send_file(bytesio, mimetype='image/webp')
            else:
                return resp.to_json(), 200

        @self.api.route('/account/<string:acc>/do_single', methods = ['POST'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly=True)
        @HttpServer.wrapaccount()
        async def do_single(mgr: Account):
            data = await request.get_json()
            order = data.get("order", "")
            await mgr.do_from_key(deepcopy(mgr.config), order, mgr._parent.secret.clan)
            resp = mgr.get_single_result_list(order)
            resp = [r.response('/daily/api/account/{}' + f'/single_result/{order}/{r.key}') for r in resp]
            return resp, 200

        @self.api.route('/account/<string:acc>/single_result/<string:order>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def single_result_list(mgr: Account, order: str):
            resp = mgr.get_single_result_list(order)
            resp = [r.response('/daily/api/account/{}' + f'/single_result/{order}/{r.key}') for r in resp]
            return resp, 200

        @self.api.route('/account/<string:acc>/single_result/<string:order>/<string:key>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def single_result(mgr: Account, order: str, key: str):
            resp_text = request.args.get('text', 'false').lower()
            resp = await mgr.get_single_result_from_key(order, key)
            if not resp:
                return "无结果", 404

            if resp_text == 'false':
                img = await drawer.draw_task_result(resp)
                bytesio = await drawer.img2bytesio(img, 'webp')
                return await send_file(bytesio, mimetype='image/webp')
            else:
                return resp.to_json(), 200

        @self.api.route('/query_validate', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        async def query_validate(accountmgr: AccountManager):
            if "text/event-stream" not in request.accept_mimetypes:
                return "", 400

            server_id = secrets.token_urlsafe(8)
            self.validate_server[accountmgr.qid] = server_id

            async def send_events(qid, server_id):
                for _ in range(30):
                    if self.validate_server[qid] != server_id:
                        break
                    if qid in validate_dict and validate_dict[qid]:
                        ret = validate_dict[qid].pop().to_json()
                        id = secrets.token_urlsafe(8)
                        yield f'''id: {id}
retry: 1000
data: {ret}\n\n'''
                    else:
                        await asyncio.sleep(1)

            response = await quart.make_response(
                send_events(accountmgr.qid, server_id),
                {
                    'Content-Type': 'text/event-stream',
                    'Cache-Control': 'no-cache',
                    'Transfer-Encoding': 'chunked',
                },
            )
            response.timeout = None
            return response

        @self.api.route('/validate', methods = ['POST'])
        async def validate(): # TODO think to check login or not
            data = await request.get_json()
            if 'id' not in data:
                return "incorrect", 403
            id = data['id']
            validate_ok_dict[id] = ValidateInfo.from_dict(data)
            return "", 200

        @self.api_limit.route('/login/qq', methods = ['POST'])
        @rate_limit(1, timedelta(seconds=1))
        @rate_limit(3, timedelta(minutes=1))
        async def login_qq():
            data = await request.get_json()
            qq = data.get('qq', "")
            password = data.get('password', "")

            if not qq or not password:
                return "请输入QQ和密码", 400
            ok = usermgr.validate_password(str(qq), str(password))
            if ok:
                login_user(AuthUser(qq))
                return "欢迎回来，" + qq, 200
            else:
                return "无效的QQ或密码", 400

        @self.api_limit.route('/register', methods = ['POST'])
        @rate_limit(1, timedelta(minutes=1))
        async def register():
            data = await request.get_json()
            qq = data.get('qq', "")
            password = data.get('password', "")
            if not qq or not password:
                return "请输入QQ和密码", 400
            if self.qq_mod:
                from ...server import is_valid_qq
                if not await is_valid_qq(qq):
                    return "无效的QQ", 400
            usermgr.create(str(qq), str(password))
            login_user(AuthUser(qq))
            return "欢迎回来，" + qq, 200

        @self.api.route('/logout', methods = ['POST'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @rate_limit(1, timedelta(seconds=1))
        async def logout(accountmgr: AccountManager):
            logout_user()
            return "再见, " + accountmgr.qid, 200

        # frontend
        @self.web.route("/", defaults={"path": ""})
        @self.web.route("/<path:path>")
        async def index(path):
            if os.path.exists(os.path.join(str(self.web.static_folder), path)):
                return await send_from_directory(str(self.web.static_folder), path, mimetype=("text/javascript" if path.endswith(".js") else None))
            else:
                return await send_from_directory(str(self.web.static_folder), 'index.html')

    def run_forever(self, loop):
        self.quart.register_blueprint(self.app)
        for rule in self.quart.url_map.iter_rules():
            print(f"{rule.rule}\t{', '.join(rule.methods)}")
        self.quart.run(host=self.host, port=self.port, loop=loop)
