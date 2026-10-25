import os
import secrets
import math
import time
from copy import deepcopy
from datetime import timedelta
from typing import Callable, Coroutine, Any, Dict

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
APP_VERSION_MINOR = 9

CACHE_HTTP_DIR = os.path.join(CACHE_DIR, 'http_server')

PATH = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(PATH, 'ClientApp')

# clan_prep响应缓存：key -> (monotonic_ts, ttl_or_None, resp)。
# 成功响应无TTL永久有效（更新只由"重拉box/重拉作业"按钮refresh=1与会战日自动链路触发）；
# 登录失败响应短TTL自愈（修完密码后不用手动清）。条目量=账号数，内存几MB无界风险可忽略。
_clan_prep_cache: Dict[str, tuple] = {}


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
        self.register_cooldowns = {}
        Compress(self.quart)
        # 会话签名密钥持久化到 cache 卷：进程每次启动随机生成会让重启/崩溃后所有登录 cookie 失效（用户被莫名登出）
        secret_path = os.path.join(CACHE_DIR, '.secret_key')
        secret_key = ''
        try:
            with open(secret_path, 'r') as f:
                secret_key = f.read().strip()
        except Exception:
            pass
        if not secret_key:
            secret_key = secrets.token_urlsafe(32)
            try:
                os.makedirs(CACHE_DIR, exist_ok=True)
                with open(secret_path, 'w') as f:
                    f.write(secret_key)
            except Exception:
                pass  # 写不进则退回进程内随机：仅重启掉登录，不影响服务
        self.quart.secret_key = secret_key

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

    def consume_register_rate_limit(self):
        key = request.access_route[0]
        now = asyncio.get_running_loop().time()
        retry_after = self.register_cooldowns.get(key, now) - now
        if retry_after > 0:
            raise RateLimitExceeded(math.ceil(retry_after))
        self.register_cooldowns[key] = now + timedelta(minutes=1).total_seconds()

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
            retry_after = max(1, error.retry_after)
            return "您冲得太快了，休息一下吧", 429, {"Retry-After": str(retry_after)}

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

        @self.api.route('/schedule', methods = ["GET"])
        async def get_schedule():
            """半月刊结构化日程（字段化，无账号依赖）。网页端通知与本 module 渲染共用数据源。"""
            from ..db.database import db
            return db.schedule_entries(), 200

        @self.api.route('/role', methods = ["GET"])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        async def get_role(accountmgr: AccountManager):
            return await accountmgr.generate_role(), 200

        @self.api.route('/running_status', methods = ["GET"])
        @HttpServer.login_required()
        async def get_running_status():
            from ..core.clientpool import instance as clientpool
            sema, farm_sema = clientpool.sema_status()
            ret = []
            for i, (running, waiting, max_count) in enumerate([sema, farm_sema]):
                ret.append({
                    'name': f"运行状态{i}",
                    'running': running,
                    'waiting': waiting,
                    'max_running': max_count,
                })
            return {'statuses': ret}, 200

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

        @self.api.route('/account/<string:acc>/clan_prep', methods = ['GET'])
        @HttpServer.login_required()
        @HttpServer.wrapaccountmgr(readonly = True)
        @HttpServer.wrapaccount(readonly=True)
        async def get_clan_prep(account: Account):
            # 响应缓存：refresh=1/force=1强制重建；账号名跨用户不唯一，key带用户id
            key = f'{current_user.auth_id}:{account.alias}'
            refresh = request.args.get('refresh') == '1' or request.args.get('force') == '1'
            force = request.args.get('force') == '1'
            # 顺手清扫带TTL的过期条目（登录失败的自愈项）
            now_mono = time.monotonic()
            for k in [k for k, (ts, ttl, _) in _clan_prep_cache.items() if ttl is not None and now_mono - ts >= ttl]:
                del _clan_prep_cache[k]
            cached = _clan_prep_cache.get(key)
            if cached and not refresh:
                _, ttl, resp = cached
                if ttl is None or now_mono - cached[0] < ttl:
                    return resp, 200
            # 延迟导入：httpserver 在容器入口早期加载，顶部导入 db 会循环导入炸启动
            from ..db.database import db
            from ..core.pcrclient import eLoginStatus
            from ..model.enums import eSystemId
            from ..util.caimogu import fetch_latest, parse_battle
            try:
                battle = parse_battle(await fetch_latest(force = force))
            except Exception as e:
                # 唯一没有兜底的失败路径：作业数据彻底不可用时给可读错误，让前端走"拉取失败"提示而非500
                return f'踩蘑菇作业数据不可用: {e}', 503
            # 池化客户端必须 async with 归还：否则本临时实例会一直占用SDK登录uid，
            # 后续模块登录将报「用户的另一项请求正在进行中」
            client = await account.get_client()
            async with client:
                # 与模块执行框架同样时序：activate -> 按需登录 -> finally deactivate
                await client.activate()
                try:
                    # 缓存可用就直接用；登录失败(凭证失效等)降级为无box数据，不炸500
                    login_error = ''
                    try:
                        if client.logged == eLoginStatus.NEED_REFRESH:
                            client.data.update_stamina_recover()
                            await client.refresh()
                        elif client.logged == eLoginStatus.NOT_LOGGED or not client.data.ready:
                            await client.login()
                    except Exception as e:
                        if not client.data.ready:
                            login_error = str(e) or e.__class__.__name__

                    box_ready = bool(client.data.unit)
                    owned = {}
                    if box_ready:
                        for game_id, unit in client.data.unit.items():
                            base = game_id // 100
                            cur = owned.get(base)
                            if cur is None or unit.unit_rarity > cur[0] or (unit.unit_rarity == cur[0] and unit.unit_level > cur[1]):
                                owned[base] = (unit.unit_rarity, unit.unit_level)

                    # 每角色按刀型的统计(尾刀口径已在caimogu定死进knife)，供前端按刀型筛选名单表；
                    # 名单口径=全阶段对照(含A面)，与推荐刀的B/C/DE口径不同
                    comp_stat: Dict[int, Dict[str, Dict]] = {}
                    for c in battle['comps']:
                        ktype = c['knife']
                        for uid in c['unit']:
                            st = comp_stat.setdefault(uid, {}).setdefault(ktype, {'usage': 0, 'best': 0, 'bosses': set()})
                            st['usage'] += 1
                            st['best'] = max(st['best'], c['damage'])
                            st['bosses'].add(c['boss'])

                    # 每阶段各boss位的分数倍率表，供前端图例（从全量comp聚合，不受截取影响）
                    stage_rates: Dict[str, Dict] = {}
                    for c in battle['comps']:
                        sk = c['stage_key']
                        if sk is None or c['rate'] is None or c['boss_idx'] is None:
                            continue
                        stage_rates.setdefault(sk, {}).setdefault(c['boss_idx'], c['rate'])

                    # 支援名单：与box同一次客户端会话拉取，随本响应一起缓存（更新box=更新会战支援，
                    # 非会战期支援名单为空就按空算，当天下次更新box前不再单独请求）。
                    # 会战支援一次只能借1人：缺超过1人，或缺的人不在支援名单里 → 该作业不可行，不下发。
                    support_ids: Dict[int, str] = {}
                    if box_ready:
                        try:
                            await client.get_clan_battle_top(1, client.data.get_shop_gold(eSystemId.CLAN_BATTLE_SHOP))
                            support = await client.get_clan_battle_support_unit_list()
                            for su in support.support_unit_list:
                                support_ids.setdefault(su.unit_data.id // 100, su.owner_name)
                        except Exception as e:
                            logger.warning(f"拉取公会支援列表失败，按无支援处理: {e}")
                    owned_base = set(owned.keys())
                    knife_rows = []
                    if box_ready:
                        seen_sns = set()
                        for c in battle['comps']:
                            stage = c['stage_key']
                            if stage is None or c['sn'] in seen_sns:
                                continue
                            seen_sns.add(c['sn'])
                            not_owned = [uid for uid in c['unit'] if uid not in owned_base]
                            borrow = len(not_owned) == 1 and not_owned[0] in support_ids
                            if not_owned and not borrow:
                                continue
                            names = []
                            for uid in c['unit']:
                                name = db.get_unit_name(uid * 100 + 1)
                                if name.startswith('未知角色') and uid in battle['unit_names']:
                                    name = battle['unit_names'][uid]
                                names.append(f'{name}(借)' if uid in support_ids and uid not in owned_base else name)
                            # 链接只放行http(s)（第三方数据防javascript:注入）
                            links = [{'text': v['text'], 'url': v['url']} for v in c['videos']
                                     if v['url'].startswith(('http://', 'https://'))]
                            knife_rows.append({
                                'sn': c['sn'],
                                'stage': stage,
                                'boss': c['boss_idx'],
                                'knife': c['knife'],
                                'damage': c['damage'],
                                'rate': c['rate'],
                                'names': names,
                                'members': c['unit'],
                                'borrow': borrow,
                                'text': c['text'],
                                'links': links,
                            })

                    units = []
                    for base_id, usage in sorted(battle['unit_usage'].items(), key=lambda kv: (-kv[1], int(kv[0]))):
                        base_id = int(base_id)
                        own = owned.get(base_id)
                        if own is None:
                            continue  # 响应瘦身：只保留已拥有且本期被用到的角色
                        name = db.get_unit_name(base_id * 100 + 1)
                        if name.startswith('未知角色') and base_id in battle['unit_names']:
                            name = battle['unit_names'][base_id]
                        units.append({
                            'unit_id': base_id,
                            'name': name,
                            # 顶层不再重复usage/best/bosses：前端聚合只按by_knife，按刀型筛选后即可得出
                            'by_knife': {t: {'usage': s['usage'], 'best': s['best'], 'bosses': sorted(s['bosses'])}
                                         for t, s in comp_stat.get(base_id, {}).items()},
                            'star': own[0],
                        })

                    resp = {
                        'updated_at': battle['fetched_at'],
                        'stale': battle['stale'],
                        'period': battle.get('period', ''),
                        'box_ready': box_ready,
                        'login_error': login_error,
                        'units': units,
                        'stage_rates': {sk: {str(b): r for b, r in sorted(bd.items())} for sk, bd in stage_rates.items()},
                        'knife_rows': knife_rows,
                    }
                    # 写缓存：登录失败时box数据不全，用短TTL让它尽快自愈
                    _clan_prep_cache[key] = (time.monotonic(), 60 if login_error else None, resp)
                    return resp, 200
                finally:
                    client.deactivate()

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
            qq = str(qq)
            password = str(password)
            self.consume_register_rate_limit()
            usermgr.create(qq, password)
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
                # index.html 是前端唯一无内容哈希的入口。Quart 默认 SEND_FILE_MAX_AGE_DEFAULT=12h 会把它缓存住：
                # 前端更新后用户最长 12 小时还在跑旧 JS，且被版本校验拒绝（「后端期望前端版本为X.Y，请更新」）。
                # no-cache 强制每次回源校验；send_from_directory 自带 ETag/条件请求，未变化直接 304，无额外开销。
                # 带哈希的静态资源（上一个分支）不受影响，仍走默认长缓存。
                response = await send_from_directory(str(self.web.static_folder), 'index.html')
                response.cache_control.no_cache = True
                response.cache_control.max_age = 0
                return response

    def run_forever(self, loop):
        self.quart.register_blueprint(self.app)
        self.quart.run(host=self.host, port=self.port, loop=loop)
