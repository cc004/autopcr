import os
import secrets
from copy import deepcopy
from datetime import timedelta
from typing import Callable, Coroutine, Any

import asyncio
import quart
from quart import request, Blueprint, send_file, send_from_directory
from quart_auth import AuthUser, QuartAuth, Unauthorized, current_user, login_user, logout_user, login_required
from quart_compress import Compress
from quart_rate_limiter import RateLimiter, rate_limit, RateLimitExceeded

from .validator import validate_dict, ValidateInfo, validate_ok_dict, enable_manual_validator
from ..constants import CACHE_DIR, ALLOW_REGISTER, SUPERUSER
from ..module.accountmgr import Account, AccountManager, instance as usermgr, AccountException, UserData, \
    PermissionLimitedException, UserDisabledException, UserException
from ..util.draw import instance as drawer
from ..util.logger import instance as logger

APP_VERSION_MAJOR = 1
APP_VERSION_MINOR = 5

CACHE_HTTP_DIR = os.path.join(CACHE_DIR, 'http_server')

PATH = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(PATH, 'ClientApp')


class HttpServer:
    def __init__(self, host = '0.0.0.0', port = 2, qq_mod = False):

        self.web = Blueprint('web', __name__, static_folder=static_path)

        # version check & rate limit
        self.api_limit = Blueprint('api_limit', __name__, url_prefix = "/")
        self.api = Blueprint('api', __name__, url_prefix = "/api")

        self.app = Blueprint('app', __name__, url_prefix = "/daily")

        self.quart = quart.Quart(__name__)
        QuartAuth(self.quart, cookie_secure=False)
        RateLimiter(self.quart)
        Compress(self.quart)
        self.quart.secret_key = secrets.token_urlsafe(16)

        self.app.register_blueprint(self.web)
        self.app.register_blueprint(self.api)
        self.api.register_blueprint(self.api_limit)

        self.host = host
        self.port = port
        self.validate_server = {}
        self.configure_routes()
        self.qq_mod = qq_mod

        self.app.after_request(self.log_request_info)

        enable_manual_validator()

    def log_request_info(self, response):
        logger.info(
            f"{request.method} {request.url} - {response.status_code} - {request.remote_addr}"
        )
        return response

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

    @staticmethod
    def login_required():
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
            async def inner(*args, **kwargs):
                if not await current_user.is_authenticated:
                    raise Unauthorized()
                else:
                    async with usermgr.load(current_user.auth_id, True) as mgr:
                        disabled = mgr.secret.disabled
                if not disabled:
                    return await func(*args, **kwargs)
                else:
                    raise UserDisabledException()
            inner.__name__ = func.__name__
            return inner
        return wrapper

    @staticmethod
    def admin_required():
        def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
            async def inner(*args, **kwargs):
                if SUPERUSER == current_user.auth_id:
                    admin = True
                else:
                    async with usermgr.load(current_user.auth_id, True) as mgr:
                        admin = mgr.secret.admin
                if admin:
                    return await func(*args, **kwargs)
                else:
                    raise PermissionLimitedException()
            inner.__name__ = func.__name__
            return inner
        return wrapper

    def configure_routes(self):

        @self.api_limit.before_request
        async def check_app_version():
            version = request.headers.get('X-App-Version', "0.0.0")
            try:
                major, minor, patch = map(int, version.split("."))
                if major != APP_VERSION_MAJOR or minor != APP_VERSION_MINOR:
                    return f"后端期望前端版本为{APP_VERSION_MAJOR}.{APP_VERSION_MINOR}，请更新", 400
                else:
                    return None
            except Exception:
                return "无法解析前端版本号，请更新", 400

        @self.api_limit.errorhandler(RateLimitExceeded)
        async def handle_rate_limit_exceeded_error(error):
            return "您冲得太快了，休息一下吧", 429

        @self.api.errorhandler(Unauthorized)
        async def redirect_to_login(*_: Exception):
            return "未登录，请登录", 401

        @self.api.errorhandler(PermissionLimitedException)
        async def limited(*_: Exception):
            return "无权使用此接口", 403

        @self.api.errorhandler(UserDisabledException)
        async def disabled(*_: Exception):
            return "用户被禁用，请联系管理员", 403

        @self.api.errorhandler(UserException)
        async def handle_user_exception(e):
            logger.exception(e)
            return str(e), 400

        @self.api.errorhandler(ValueError)
        async def handle_value_error(e):
            logger.exception(e)
            return str(e), 400

        @self.api.errorhandler(AccountException)
        async def handle_account_exception(e):
            logger.exception(e)
            return str(e), 400

        @self.api.errorhandler(Exception)
        async def handle_general_exception(e):
            logger.exception(e)
            return "服务器发生错误", 500

        @self.api.route('/clan_forbid', methods = ["GET"])
        @HttpServer.login_required()
        @HttpServer.admin_required()
        async def get_clan_forbid():
            accs = usermgr.get_clan_battle_forbidden()
            return '\n'.join(accs), 200

        @self.api.route('/clan_forbid', methods = ["PUT"])
        @HttpServer.login_required()
        @HttpServer.admin_required()
        async def put_clan_forbid():
            data = (await request.get_json())['accs'].split('\n')
            usermgr.set_clan_battle_forbidden(data)
            return f'设置成功，禁止了{len(data)}个账号', 200

        @self.api.route('/role', methods = ["GET"])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        async def get_role(accountmgr: AccountManager):
            return await accountmgr.generate_role(), 200

        @self.api.route('/account', methods = ['GET'])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        async def get_info(accountmgr: AccountManager):
            return await accountmgr.generate_info(), 200

        @self.api.route('/account', methods = ["PUT"])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr()
        async def put_info(accountmgr: AccountManager):
            data = await request.get_json()
            default_accont = data.get('default_account', '')
            if default_accont:
                accountmgr.set_default_account(default_accont)
            password = data.get('password', '')
            if password:
                accountmgr.set_password(password)
            return "保存成功", 200

        @self.api.route('/account', methods = ["POST"])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr()
        async def create_account(accountmgr: AccountManager):
            data = await request.get_json()
            acc = data.get("alias", "")
            accountmgr.create_account(acc.strip())
            return "创建账号成功", 200

        @self.api.route('/account/import', methods = ["POST"])
        @HttpServer.login_required()
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
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr()
        async def delete_qq(accountmgr: AccountManager):
            accountmgr.delete_mgr()
            logout_user()
            return "删除QQ成功", 200

        @self.api.route('/account', methods = ["DELETE"])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr()
        async def delete_account(accountmgr: AccountManager):
            accountmgr.delete_all_accounts()
            return "删除账号成功", 200

        @self.api.route('/account/sync', methods = ["POST"])
        @HttpServer.login_required()
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
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly=True)
        async def get_account(account: Account):
            return account.generate_info(), 200

        @self.api.route('/account/<string:acc>', methods = ["PUT", "DELETE"])
        @HttpServer.login_required()
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
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def get_modules_config(mgr: Account, modules_key: str):
            return mgr.generate_modules_info(modules_key)

        @self.api.route('/account/<string:acc>/config', methods = ['PUT'])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount()
        async def put_config(mgr: Account):
            data = await request.get_json()
            mgr.data.config.update(data)
            return "配置保存成功", 200

        @self.api.route('/account/<string:acc>/do_daily', methods = ['POST'])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly=True)
        @HttpServer.wrapaccount()
        async def do_daily(mgr: Account):
            await mgr.do_daily(mgr._parent.secret.clan)
            return mgr.generate_result_info(), 200

        @self.api.route('/account/<string:acc>/daily_result', methods = ['GET'])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def daily_result_list(mgr: Account):
            resp = mgr.get_daily_result_list()
            resp = [r.response('/daily/api/account/{}' + '/daily_result/' + str(r.key)) for r in resp]
            return resp, 200

        @self.api.route('/account/<string:acc>/daily_result/<string:key>', methods = ['GET'])
        @HttpServer.login_required()
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
        @HttpServer.login_required()
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
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly= True)
        async def single_result_list(mgr: Account, order: str):
            resp = mgr.get_single_result_list(order)
            resp = [r.response('/daily/api/account/{}' + f'/single_result/{order}/{r.key}') for r in resp]
            return resp, 200

        @self.api.route('/account/<string:acc>/single_result/<string:order>/<string:key>', methods = ['GET'])
        @HttpServer.login_required()
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

        @self.api.route('/user', methods = ['GET'])
        @HttpServer.login_required()
        @HttpServer.admin_required()
        async def get_users():
            qids = sorted(list(usermgr.qids()))
            results = []
            for qid in qids:
                async with usermgr.load(qid, readonly=True) as mgr:
                    result = {
                        "qq": qid,
                        "admin": mgr.is_admin(),
                        "clan": mgr.secret.clan,
                        "disabled": mgr.secret.disabled,
                        "account_count": mgr.account_count(),
                    }
                results.append(result)
            return results, 200

        @self.api.route('/user/<string:qid>', methods = ['POST'])
        @HttpServer.login_required()
        @HttpServer.admin_required()
        async def create_user(qid: str):
            data = await request.get_data()
            userdata = UserData.from_json(data)
            if userdata.admin and current_user.auth_id != SUPERUSER:
                # 仅超管可创建管理员
                raise PermissionLimitedException()
            async with usermgr.create(qid, userdata.admin) as mgr:
                mgr.secret = userdata
            return "创建用户成功", 200

        @self.api.route('/user/<string:qid>', methods = ['PUT'])
        @HttpServer.login_required()
        @HttpServer.admin_required()
        async def set_user(qid: str):
            data = await request.get_json()
            async with usermgr.load(qid) as mgr:
                if mgr.is_admin() and current_user.auth_id != SUPERUSER:
                    # 仅超管可更改管理员
                    raise PermissionLimitedException()
                if 'admin' in data:
                    if current_user.auth_id != SUPERUSER:
                        # 仅超管可添加管理员
                        raise PermissionLimitedException()
                    if current_user.auth_id == qid and not data['admin']:
                        return "无法取消自己的管理权限", 403
                    mgr.secret.admin = data['admin']
                if 'disabled' in data:
                    if current_user.auth_id == qid and data['disabled']:
                        return "无法禁用自己", 403
                    mgr.secret.disabled = data['disabled']
                if 'password' in data:
                    mgr.secret.password = data['password']
                if 'clan' in data:
                    mgr.secret.clan = data['clan']
            return "更新用户信息成功", 200

        @self.api.route('/user/<string:qid>', methods = ['DELETE'])
        @HttpServer.login_required()
        @HttpServer.admin_required()
        async def delete_user(qid: str):
            if qid == current_user.auth_id:
                return "无法删除自己", 403
            if qid == SUPERUSER:
                return "不可删除超级管理员", 403
            usermgr.delete(qid)
            return "删除用户成功", 200

        @self.api.route('/query_validate', methods = ['GET'])
        @HttpServer.login_required()
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
            if not usermgr.validate_password(str(qq), str(password)):
                return "无效的QQ或密码", 400
            if not usermgr.check_enabled(str(qq)):
                return "用户被禁用，请联系管理员", 403
            login_user(AuthUser(qq))
            return "欢迎回来，" + qq, 200

        @self.api_limit.route('/register', methods = ['POST'])
        @rate_limit(1, timedelta(minutes=1))
        async def register():
            if not ALLOW_REGISTER:
                return "当前禁止注册，请联系管理员", 400

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
        self.quart.run(host=self.host, port=self.port, loop=loop)
