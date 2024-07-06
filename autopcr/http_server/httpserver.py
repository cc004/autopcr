from copy import deepcopy
from datetime import timedelta
import traceback
import quart
from quart import request, Blueprint, send_file, send_from_directory
from quart_rate_limiter import RateLimiter, rate_limit, RateLimitExceeded
from quart_auth import AuthUser, QuartAuth, Unauthorized, current_user, login_required, login_user, logout_user
from quart_compress import Compress
import secrets, os, io
from typing import Callable, Coroutine, Any

from ..module.accountmgr import Account, AccountManager, UserException, instance as usermgr, AccountException
from ..constants import CACHE_DIR
from ..util.draw import instance as drawer

CACHE_HTTP_DIR = os.path.join(CACHE_DIR, 'http_server')

PATH = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(PATH, 'ClientApp')

class HttpServer:
    def __init__(self, host = '0.0.0.0', port = 2, qq_mod = False):

        self.web = Blueprint('web', __name__, static_folder=static_path)

        self.api = Blueprint('api', __name__, url_prefix = "/api")

        self.app = Blueprint('app', __name__, url_prefix = "/daily")

        self.quart = quart.Quart(__name__)
        QuartAuth(self.quart, cookie_secure=False)
        RateLimiter(self.quart)
        Compress(self.quart)
        self.quart.secret_key = secrets.token_urlsafe(16)

        self.app.register_blueprint(self.web)
        self.app.register_blueprint(self.api)

        self.host = host
        self.port = port
        self.configure_routes()
        self.qq_mod = qq_mod

    @staticmethod
    def wrapaccount(readonly = False):
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
            async def inner(accountmgr: AccountManager, acc: str, *args, **kwargs):
                if acc:
                    try:
                        async with accountmgr.load(acc, readonly) as mgr:
                            return await func(mgr, *args, **kwargs)
                    except AccountException as e:
                        return str(e), 400
                    except Exception as e:
                        print(e)
                        return "服务器发生错误", 500
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

        @self.api.errorhandler(RateLimitExceeded)
        async def handle_rate_limit_exceeded_error(error):
            return "您冲得太快了，休息一下吧", 429

        @self.api.errorhandler(Unauthorized)
        async def redirect_to_login(*_: Exception):
            return "未登录，请登录", 401

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
            try:
                data = await request.get_json()
                acc = data.get("alias", "")
                accountmgr.create_account(acc.strip())
                return "创建账号成功", 200
            except AccountException as e:
                return str(e), 400
            except Exception as e:
                print(e)
                return "服务器发生错误", 500

        @self.api.route('/account/sync', methods = ["POST"])
        @login_required
        @HttpServer.wrapaccountmgr()
        async def sync_account_config(accountmgr: AccountManager):
            try:
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
            except AccountException as e:
                return str(e), 400
            except Exception as e:
                print(e)
                return "服务器发生错误", 500

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
                if 'password' in data:
                    account.data.password = data['password']
                return "保存账户信息成功", 200
            elif request.method == "DELETE":
                account.delete()
                return "删除账户信息成功", 200
            else:
                return "", 404

        @self.api.route('/account/<string:acc>/daily', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def get_daily_config(mgr: Account):
            if request.method == 'GET':
                return mgr.generate_daily_info()
            else:
                return "", 404

        @self.api.route('/account/<string:acc>/tools', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def get_tools_config(mgr: Account):
            if request.method == 'GET':
                return mgr.generate_tools_info()
            else:
                return "", 404

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
            try:
                await mgr.do_daily()
                return mgr.generate_result_info(), 200
            except ValueError as e:
                return str(e), 400
            except Exception as e:
                traceback.print_exc()
                return "服务器发生错误", 500

        @self.api.route('/account/<string:acc>/daily_result/<string:safe_time>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def daily_result(mgr: Account, safe_time: str):
            try:
                resp = await mgr.get_daily_result_from_time(safe_time)
                if not resp:
                    return "无结果", 404
                img = await drawer.draw_tasks_result(resp)
                bytesio = await drawer.img2bytesio(img)
                return await send_file(bytesio, mimetype='image/jpg')
            except ValueError as e:
                return str(e), 400
            except Exception as e:
                traceback.print_exc()
                return "服务器发生错误", 500

        @self.api.route('/account/<string:acc>/do_single', methods = ['POST'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly=True)
        @HttpServer.wrapaccount()
        async def do_single(mgr: Account):
            data = await request.get_json()
            order = data.get("order", "")
            resp_text = request.args.get('text', 'false').lower()
            try:
                resp, _ = await mgr.do_from_key(deepcopy(mgr.client.keys), order)
                if resp_text == 'false':
                    img = await drawer.draw_task_result(resp)
                    bytesio = await drawer.img2bytesio(img)
                    return await send_file(bytesio, mimetype='image/jpg')
                else:
                    return resp.log, 200
            except ValueError as e:
                return str(e), 400
            except Exception as e:
                traceback.print_exc()
                return "服务器发生错误", 500

        @self.api.route('/account/<string:acc>/single_result/<string:order>', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def single_result(mgr: Account, order: str):
            resp_text = request.args.get('text', 'false').lower()
            try:
                resp = await mgr.get_single_result(order)
                if not resp:
                    return "无结果", 404

                if resp_text == 'false':
                    img = await drawer.draw_task_result(resp)
                    bytesio = await drawer.img2bytesio(img)
                    return await send_file(bytesio, mimetype='image/jpg')
                else:
                    return resp.log, 200
            except ValueError as e:
                return str(e), 400
            except Exception as e:
                traceback.print_exc()
                return "服务器发生错误", 500

        @self.api.route('/account/<string:acc>/query_validate', methods = ['GET'])
        @login_required
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly = True)
        async def query_validate(mgr: Account):
            from ..bsdk.validator import validate_dict, ValidateInfo
            if mgr.data.username not in validate_dict:
                return ValidateInfo(status="empty").to_dict(), 200
            else:
                ret = validate_dict[mgr.data.username].to_dict()
                del validate_dict[mgr.data.username]
                return ret, 200

        @self.api.route('/validate', methods = ['POST'])
        async def validate(): # TODO think to check login or not
            data = await request.get_json()
            from ..bsdk.validator import validate_ok_dict
            if 'id' not in data:
                return "incorrect", 403
            id = data['id']
            from ..bsdk.validator import ValidateInfo
            validate_ok_dict[id] = ValidateInfo.from_dict(data)
            return "", 200

        @self.api.route('/login/qq', methods = ['POST'])
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

        @self.api.route('/register', methods = ['POST'])
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
            try:
                usermgr.create(str(qq), str(password))
                login_user(AuthUser(qq))
                return "欢迎回来，" + qq, 200
            except UserException as e:
                return str(e), 400
            except Exception as e:
                print(e)
                return "服务器发生错误", 500

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
