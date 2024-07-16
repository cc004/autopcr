from collections import Counter
from typing import Any, Callable, Coroutine, Dict, List, Tuple

from .autopcr.module.modulemgr import TaskResult
from .autopcr.module.modulebase import ModuleStatus
from .autopcr.util.draw_table import outp_b64
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.db.database import db
from .autopcr.module.accountmgr import Account, AccountManager, instance as usermgr
from .autopcr.db.dbstart import db_start
from .autopcr.util.draw import instance as drawer
import asyncio, datetime

import nonebot
from nonebot import on_startup
import hoshino
from hoshino import HoshinoBot, Service, priv
from hoshino.util import escape
from hoshino.typing import CQEvent
from quart_auth import QuartAuth
from quart_rate_limiter import RateLimiter
from quart_compress import Compress
import secrets

address = None  # 填你的公网IP或域名，不填则会自动尝试获取
useHttps = False

server = HttpServer(qq_mod=True)
app = nonebot.get_bot().server_app
QuartAuth(app, cookie_secure=False)
RateLimiter(app)
Compress(app)
app.secret_key = secrets.token_urlsafe(16) # cookie expires when reboot
app.register_blueprint(server.app)

prefix = '#'

sv_help = f"""
- {prefix}配置日常 一切的开始
- {prefix}清日常 [昵称] 无昵称则默认账号
- {prefix}清日常所有 清该qq号下所有号的日常
指令格式： 命令 昵称 参数，下述省略昵称，<>表示必填，[]表示可选，|表示分割
- {prefix}日常记录 查看清日常状态
- {prefix}日常报告 [0|1|2|3] 最近四次清日常报告
- {prefix}定时日志 查看定时运行状态
- {prefix}查心碎 查询缺口心碎
- {prefix}查记忆碎片 [可刷取|大师币] 查询缺口记忆碎片，可按地图可刷取或大师币商店过滤
- {prefix}查装备 [<rank>] [fav] 查询缺口装备，rank为数字，只查询>=rank的角色缺口装备，fav表示只查询favorite的角色
- {prefix}刷图推荐 [<rank>] [fav] 查询缺口装备的刷图推荐，格式同上
- {prefix}公会支援 查询公会支援角色配置
- {prefix}卡池 查看当前卡池
- {prefix}来发十连 <卡池id> [抽到出] [单抽券] [开抽] 赛博抽卡，谨慎使用。卡池id来自【{prefix}卡池】，[抽到出]表示抽到出货或达天井，[单抽券]表示仅用厕纸，[开抽]表示确认抽卡。已有up也可再次触发。
""".strip()

if address is None:
    try:
        from hoshino.config import PUBLIC_ADDRESS

        address = PUBLIC_ADDRESS
    except:
        pass

if address is None:
    try:
        import socket

        address = socket.gethostbyname(socket.gethostname())
    except:
        pass

if address is None:
    address = "127.0.0.1"

address = ("https://" if useHttps else "http://") + address + "/daily/"

validate = ""

sv = Service(
    name="自动清日常",
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=False,  # False隐藏
    enable_on_default=False,  # 是否默认启用
    bundle='pcr工具',  # 属于哪一类
    help_=sv_help  # 帮助文本
)

@on_startup
async def init():
    await db_start()
    from .autopcr.module.crons import queue_crons
    queue_crons()

class BotEvent:
    def __init__(self): ...
    async def finish(self, msg: str): ...
    async def send(self, msg: str): ...
    async def target_qq(self) -> str: ...
    async def send_qq(self) -> str: ...
    async def message(self) -> List[str]: ...
    async def is_admin(self) -> bool: ...
    async def get_group_member_list(self) -> List: ...

class HoshinoEvent(BotEvent):
    def __init__(self, bot: HoshinoBot, ev: CQEvent):
        self.bot = bot
        self.ev = ev

        self.user_id = str(ev.user_id)

        self.at_sb = []
        self._message = []
        for m in ev.message:
            if m.type == 'at' and m.data['qq'] != 'all':
                self.at_sb.append(str(m.data['qq']))
            elif m.type == 'text': # ignore other type
                self._message += m.data['text'].split()

    async def get_group_member_list(self) -> List[Tuple[str, str]]: # (qq, nick_name)
        members = await self.bot.get_group_member_list(group_id=self.ev.group_id)
        ret = [(str(m['user_id']), m['card'] if m['card'] else m['nickname']) for m in members]
        ret = sorted(ret, key=lambda x: x[1])
        return ret

    async def target_qq(self):
        if len(self.at_sb) > 1:
            await self.finish("只能指定一个用户")

        return self.at_sb[0] if self.at_sb else str(self.user_id)
    
    async def send_qq(self):
        return self.user_id

    async def message(self):
        return self._message

    async def send(self, msg: str):
        msg = f"[CQ:reply,id={self.ev.message_id}]{msg}"
        await self.bot.send(self.ev, msg)

    async def finish(self, msg: str):
        await self.bot.finish(self.ev, msg)

    async def is_admin(self) -> bool:
        return priv.check_priv(self.ev, priv.ADMIN)

def wrap_hoshino_event(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent, *args, **kwargs):
        await func(HoshinoEvent(bot, ev), *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

async def check_validate(botev: BotEvent, acc: Account):
    from .autopcr.bsdk.validator import validate_dict
    for _ in range(360):
        if acc.data.username in validate_dict:
            status = validate_dict[acc.data.username].status
            if status == "ok":
                del validate_dict[acc.data.username]
                break

            url = validate_dict[acc.data.username].url
            url = address + url.lstrip("/daily/")
            
            msg=f"pcr账号登录需要验证码，请点击以下链接在120秒内完成认证:\n{url}"
            await botev.send(msg)

            del validate_dict[acc.data.username]

        else:
            await asyncio.sleep(1)

async def is_valid_qq(qq: str):
    qq = str(qq)
    groups = (await sv.get_enable_groups()).keys()
    bot = nonebot.get_bot()
    for group in groups:
        try:
            async for member in await bot.get_group_member_list(group_id=group):
                if qq == str(member['user_id']):
                    return True
        except:
            for member in await bot.get_group_member_list(group_id=group):
                if qq == str(member['user_id']):
                    return True
    return False

def check_final_args_be_empty(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        msg = await botev.message()
        if msg:
            await botev.finish("未知的参数：【" + " ".join(msg) + "】")
        await func(botev, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

from dataclasses import dataclass
@dataclass
class ToolInfo:
    key: str
    config_parser: Callable[..., Coroutine[Any, Any, Any]]

tool_info: Dict[str, ToolInfo]= {}

def register_tool(name: str, key: str):
    def wrapper(func):
        tool_info[name] = ToolInfo(key=key, config_parser=func)
        async def inner(*args, **kwargs):
            await func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner
    return wrapper

def wrap_accountmgr(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        target_qq = await botev.target_qq()
        sender_qq = await botev.send_qq()

        if sender_qq != target_qq and not await botev.is_admin():
            await botev.finish("只有管理员可以操作他人账号")

        if target_qq not in usermgr.qids():
            await botev.finish(f"未找到{target_qq}的账号，请发送【{prefix}配置日常】进行配置")

        async with usermgr.load(target_qq, readonly=True) as accmgr:
            await func(botev = botev, accmgr = accmgr, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_account(func):
    async def wrapper(botev: BotEvent, accmgr: AccountManager, *args, **kwargs):
        msg = await botev.message()

        alias = msg[0] if msg else ""

        if alias not in accmgr.accounts():
            alias = accmgr.default_account
        else:
            del msg[0]

        if len(list(accmgr.accounts())) == 1:
            alias = list(accmgr.accounts())[0]

        if alias not in accmgr.accounts():
            if alias:
                await botev.finish(f"未找到昵称为【{alias}】的账号")
            else:
                await botev.finish(f"存在多账号且未找到默认账号，请指定昵称")

        async with accmgr.load(alias) as acc:
            await func(botev = botev, acc = acc, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_tool(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        msg = await botev.message()
        tool = msg[0] if msg else ""

        if tool not in tool_info:
            await botev.finish(f"未找到工具【{tool}】")
        del msg[0]

        tool = tool_info[tool]

        await func(botev = botev, tool = tool, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_config(func):
    async def wrapper(botev: BotEvent, tool: ToolInfo, *args, **kwargs):
        config = await tool.config_parser(botev)
        await func(botev = botev, tool = tool, config = config, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

@sv.on_fullmatch(["帮助自动清日常", f"{prefix}帮助"])
@wrap_hoshino_event
async def bangzhu_text(botev: BotEvent):
    msg = outp_b64(await drawer.draw_msgs(sv_help.split("\n")))
    await botev.finish(msg)

@sv.on_fullmatch(f"{prefix}清日常所有")
@wrap_hoshino_event
@wrap_accountmgr
async def clean_daily_all(botev: BotEvent, accmgr: AccountManager):
    loop = asyncio.get_event_loop()
    task = []
    alias = []
    is_admin_call = await botev.is_admin()
    async def clean_daily_pre(alias: str):
        async with accmgr.load(alias) as acc:
            return await clean_daily(botev, acc, is_admin_call)

    for acc in accmgr.accounts():
        alias.append(escape(acc))
        task.append(loop.create_task(clean_daily_pre(acc)))

    try:
        alias_str = ','.join(alias)
        await botev.send(f"开始为{alias_str}清理日常")
    except Exception as e:  
        print(e)

    resps = await asyncio.gather(*task, return_exceptions=True)
    header = ["昵称", "清日常结果", "状态"]
    content = [[alias[i], daily_result[0].result[daily_result[0].order[-1]].log, "#" + daily_result[1]] for i, daily_result in enumerate(resps) if not isinstance(daily_result, Exception)]
    img = await drawer.draw(header, content)
    err = [(alias[i], resp) for i, resp in enumerate(resps) if isinstance(resp, Exception)]

    msg = outp_b64(img)
    await botev.send(msg)

    if err:
        msg = "\n".join([f"{a}: {m}" for a, m in err])
        await botev.send(msg)

@sv.on_fullmatch(f"{prefix}查禁用")
@wrap_hoshino_event
async def query_clan_battle_forbidden(botev: BotEvent):
    if not await botev.is_admin():
        await botev.finish("仅管理员可以调用")

    content = ["会战期间仅管理员调用"]
    for qq in usermgr.qids():
        async with usermgr.load(qq, readonly=True) as accmgr:
            for alias in accmgr.accounts():
                async with accmgr.load(alias, readonly=True) as acc:
                    if acc.is_clan_battle_forbidden():
                        content.append(f"{acc.qq}  {acc.alias} ")
    img = outp_b64(await drawer.draw_msgs(content))
    await botev.finish(img)

@sv.on_fullmatch(f"{prefix}查群禁用")
@wrap_hoshino_event
async def query_group_clan_battle_forbidden(botev: BotEvent):
    if not await botev.is_admin():
        await botev.finish("仅管理员可以调用")

    content = []
    header = ["昵称", "QQ", "账号", "会战调用"]
    members = await botev.get_group_member_list()
    for qq, name in members:
        if qq in usermgr.qids():
            async with usermgr.load(qq, readonly=True) as accmgr:
                for alias in accmgr.accounts():
                    async with accmgr.load(alias, readonly=True) as acc:
                        msg = "仅限管理员" if acc.is_clan_battle_forbidden() else ""
                        content.append([name, qq, alias, msg])
        else:
            content.append([name, qq, "" ,""])
    img = outp_b64(await drawer.draw(header, content))
    await botev.finish(img)

@sv.on_fullmatch(f"{prefix}查内鬼")
@wrap_hoshino_event
async def find_ghost(botev: BotEvent):
    msg = []
    for qq in usermgr.qids():
        if not await is_valid_qq(qq):
            msg.append(qq)
    if not msg:
        msg.append("未找到内鬼")
    await botev.finish(" ".join(msg))

@sv.on_fullmatch(f"{prefix}清内鬼")
@wrap_hoshino_event
async def clean_ghost(botev: BotEvent):
    msg = []
    for qq in usermgr.qids():
        if not await is_valid_qq(qq):
            msg.append(qq)
    if not msg:
        msg.append("未找到内鬼")
    else:
        for qq in msg:
            usermgr.delete(qq)
        msg = [f"已清除{len(msg)}个内鬼:"] + msg
    await botev.finish(" ".join(msg))

@sv.on_prefix(f"{prefix}清日常")
@wrap_hoshino_event
@wrap_accountmgr
@wrap_account
@check_final_args_be_empty
async def clean_daily_from(botev: BotEvent, acc: Account):
    alias = escape(acc.alias)
    try:
        await botev.send(f"开始为{alias}清理日常")
    except Exception as e:  
        print(e)

    try:
        is_admin_call = await botev.is_admin()
        resp, _ = await clean_daily(botev = botev, acc = acc, is_admin_call = is_admin_call)
        img = await drawer.draw_tasks_result(resp)
        msg = f"{alias}"
        msg += outp_b64(img)
        await botev.send(msg)
    except Exception as e:
        await botev.send(f'{alias}: {e}')

async def clean_daily(botev: BotEvent, acc: Account, is_admin_call = False) -> Tuple[TaskResult, str]:
    loop = asyncio.get_event_loop()
    loop.create_task(check_validate(botev, acc))
    resp, status = await acc.do_daily(is_admin_call)
    return resp, status.value

@sv.on_prefix(f"{prefix}日常报告")
@wrap_hoshino_event
@wrap_accountmgr
@wrap_account
async def clean_daily_result(botev: BotEvent, acc: Account):
    result_id = 0
    msg = await botev.message()
    try:
        result_id = int(msg[0])
        del msg[0]
    except Exception as e:
        pass
    resp = await acc.get_daily_result_from_id(result_id)
    if not resp:
        await botev.finish("未找到日常报告")
    img = await drawer.draw_tasks_result(resp)
    await botev.finish(outp_b64(img))

@sv.on_prefix(f"{prefix}日常记录")
@wrap_hoshino_event
@wrap_accountmgr
async def clean_daily_time(botev: BotEvent, accmgr: AccountManager):
    content = []
    for alias in accmgr.accounts():
        async with accmgr.load(alias, readonly=True) as acc:
            content += [[acc.alias, daily_result.time, "#" + daily_result.status] for daily_result in acc.data.daily_result]

    if not content:
        await botev.finish("暂无日常记录")
    header = ["昵称", "清日常时间", "状态"]
    img = outp_b64(await drawer.draw(header, content))
    await botev.finish(img)

@sv.on_prefix(f"{prefix}定时日志")
@wrap_hoshino_event
async def cron_log(botev: BotEvent):
    from .autopcr.module.crons import CRONLOG_PATH, CronLog
    with open(CRONLOG_PATH, 'r', encoding='utf-8') as f:
        msg = [CronLog.from_json(line.strip()) for line in f.readlines()]
    args = await botev.message()
    cur = datetime.datetime.now()
    if is_args_exist(args, '错误'):
        msg = [log for log in msg if log.status == ModuleStatus.error]
    if is_args_exist(args, '警告'):
        msg = [log for log in msg if log.status == ModuleStatus.warning]
    if is_args_exist(args, '成功'):
        msg = [log for log in msg if log.status == ModuleStatus.success]
    if is_args_exist(args, '昨日'):
        cur -= datetime.timedelta(days=1)
        msg = [log for log in msg if log.time.date() == cur.date()]
    if is_args_exist(args, '今日'):
        msg = [log for log in msg if log.time.date() == cur.date()]

    msg = msg[-40:]
    msg = msg[::-1]
    msg = [str(log) for log in msg]
    if not msg:
        msg.append("暂无定时日志")
    img = outp_b64(await drawer.draw_msgs(msg))
    await botev.finish(img)

@sv.on_prefix(f"{prefix}定时状态")
@wrap_hoshino_event
async def cron_status(botev: BotEvent):
    from .autopcr.module.crons import CRONLOG_PATH, CronLog, CronOperation
    with open(CRONLOG_PATH, 'r', encoding='utf-8') as f:
        logs = [CronLog.from_json(line.strip()) for line in f.readlines()]
    cur = datetime.datetime.now()
    msg = await botev.message()
    if is_args_exist(msg, '昨日'):
        cur -= datetime.timedelta(days=1)
    start_logs = [log for log in logs if log.operation == CronOperation.START and log.time.date() == cur.date()]
    finish_logs = [log for log in logs if log.operation == CronOperation.FINISH and log.time.date() == cur.date()]
    status = Counter([log.status for log in finish_logs])
    msg = [f'今日定时任务：启动{len(start_logs)}个，完成{len(finish_logs)}个'] 
    msg += [f"{k.value}: {v}" for k, v in status.items()]
    # notice = [log for log in logs if log.status != ModuleStatus.success]
    # if notice:
        # msg += [""]
        # msg += [str(log) for log in notice]
    img = outp_b64(await drawer.draw_msgs(msg))
    await botev.finish(img)

@sv.on_prefix(f"{prefix}定时统计")
@wrap_hoshino_event
async def cron_statistic(botev: BotEvent):
    cnt_clanbattle = Counter()
    cnt = Counter()
    for qq in usermgr.qids():
        async with usermgr.load(qq, readonly=True) as accmgr:
            for alias in accmgr.accounts():
                async with accmgr.load(alias, readonly=True) as acc:
                    for i in range(1,5):
                        suf = f"cron{i}"
                        if acc.data.config.get(suf, False):
                            time = acc.data.config.get(f"time_{suf}", "00:00")
                            if time.count(":") == 2:
                                time = ":".join(time.split(":")[:2])
                            cnt[time] += 1
                            if acc.data.config.get(f"clanbattle_run_{suf}", False):
                                cnt_clanbattle[time] += 1

    content = [[k, str(v), str(cnt_clanbattle[k])] for k, v in cnt.items()]
    content = sorted(content, key=lambda x: x[0])
    content.append(["总计", str(sum(cnt.values())), str(sum(cnt_clanbattle.values()))])
    header = ["时间", "定时任务数", "公会战任务数"]

    img = outp_b64(await drawer.draw(header, content))
    await botev.finish(img)

@sv.on_fullmatch(f"{prefix}配置日常")
@wrap_hoshino_event
async def config_clear_daily(botev: BotEvent):
    await botev.finish(address + "login")

@sv.on_prefix(f"{prefix}")
@wrap_hoshino_event
@wrap_tool
@wrap_accountmgr
@wrap_account
@wrap_config
@check_final_args_be_empty
async def tool_used(botev: BotEvent, tool: ToolInfo, config: Dict[str, str], acc: Account):
    alias = escape(acc.alias)
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(check_validate(botev, acc))

        is_admin_call = await botev.is_admin()
        resp, _ = await acc.do_from_key(config, tool.key, is_admin_call)
        img = await drawer.draw_task_result(resp)
        msg = f"{alias}"
        msg += outp_b64(img)
        await botev.send(msg)
    except Exception as e:
        await botev.send(f'{alias}: {e}')

@sv.on_fullmatch(f"{prefix}卡池")
@wrap_hoshino_event
async def gacha_current(botev: BotEvent):
    msg = '\n'.join(db.get_cur_gacha())
    await botev.finish(msg)

def is_args_exist(msg: List[str], key: str):
    if key in msg:
        msg.remove(key)
        return True
    return False

@register_tool("公会支援", 'get_clan_support_unit')
async def clan_support(botev: BotEvent):
    return {}

@register_tool("查心碎", "get_need_xinsui")
async def find_xinsui(botev: BotEvent):
    return {}

@register_tool("jjc回刺", "jjc_back")
async def jjc_back(botev: BotEvent):
    msg = await botev.message()
    opponent_jjc_rank = -1
    try:
        opponent_jjc_rank = int(msg[0])
        del msg[0]
    except:
        pass
    config = {
        "opponent_jjc_rank": opponent_jjc_rank,
    }
    return config

@register_tool("pjjc回刺", "pjjc_back")
async def pjjc_back(botev: BotEvent):
    msg = await botev.message()
    opponent_pjjc_rank = -1
    try:
        opponent_pjjc_rank = int(msg[0])
        del msg[0]
    except:
        pass
    config = {
        "opponent_pjjc_rank": opponent_pjjc_rank,
    }
    return config

@register_tool("jjc透视", "jjc_info")
async def jjc_info(botev: BotEvent):
    use_cache = True
    msg = await botev.message()
    try:
        use_cache = not is_args_exist(msg, 'flush')
    except:
        pass
    config = {
        "jjc_info_cache": use_cache,
    }
    return config

@register_tool("pjjc透视", "pjjc_info")
async def pjjc_info(botev: BotEvent):
    use_cache = True
    msg = await botev.message()
    try:
        use_cache = not is_args_exist(msg, 'flush')
    except:
        pass
    config = {
        "pjjc_info_cache": use_cache,
    }
    return config

@register_tool("查记忆碎片", "get_need_memory")
async def find_memory(botev: BotEvent):
    memory_demand_consider_unit = '所有'
    msg = await botev.message()
    try:
        if is_args_exist(msg, '可刷取'):
            memory_demand_consider_unit = '地图可刷取'
        elif is_args_exist(msg, '大师币'):
            memory_demand_consider_unit = '大师币商店'
    except:
        pass
    config = {
        "memory_demand_consider_unit": memory_demand_consider_unit,
    }
    return config


@register_tool(f"来发十连", "gacha_start")
async def shilian(botev: BotEvent):
    cc_until_get = False
    pool_id = ""
    really_do = False
    ticket = False
    msg = await botev.message()
    try:
        pool_id = msg[0]
        del msg[0]
    except:
        pass

    try:
        cc_until_get = is_args_exist(msg, '抽到出')
    except:
        pass

    try:
        really_do = is_args_exist(msg, '开抽')
    except:
        pass

    try:
        ticket = is_args_exist(msg, '单抽券')
    except:
        pass

    current_gacha = {gacha.split(':')[0]: gacha for gacha in db.get_cur_gacha()}

    if pool_id not in current_gacha:
        await botev.finish(f"未找到该卡池{pool_id}")

    pool_id = current_gacha[pool_id]

    if not really_do:
        msg = f"卡池{pool_id}\n"
        if cc_until_get:
            msg += "抽到出\n"
        if ticket:
            msg += "单抽券\n"
        msg += "确认无误，消息末尾加上【开抽】即可开始抽卡"
        await botev.finish(msg)

    config = {
        "pool_id": pool_id,
        "cc_until_get": cc_until_get,
        "single_ticket": ticket,
    }
    return config

@register_tool(f"查装备", "get_need_equip")
async def find_equip(botev: BotEvent):
    like_unit_only = False
    start_rank = None
    msg = await botev.message()
    try:
        like_unit_only = is_args_exist(msg, 'fav')
    except:
        pass

    try:
        start_rank = int(msg[0])
        del msg[0]
    except:
        pass


    config = {
        "start_rank": start_rank,
        "like_unit_only": like_unit_only
    }
    return config

@register_tool(f"刷图推荐", "get_normal_quest_recommand")
async def quest_recommand(botev: BotEvent):
    like_unit_only = False
    start_rank = None
    msg = await botev.message()
    try:
        like_unit_only = is_args_exist(msg, 'fav')
    except:
        pass
    try:
        start_rank = int(msg[0])
        del msg[0]
    except:
        pass

    config = {
        "start_rank": start_rank,
        "like_unit_only": like_unit_only
    }
    return config


# @register_tool("获取导入", "get_library_import_data")
# async def get_library_import(botev: BotEvent):
    # return {}
