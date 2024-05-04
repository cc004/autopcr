from collections import Counter
from typing import Any, Callable, Coroutine, Dict
import os

from .autopcr.util.draw_table import outp_b64
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.db.database import db
from .autopcr.module.accountmgr import Account, AccountManager, instance as usermgr
from .autopcr.db.dbstart import db_start
from .autopcr.util.draw import instance as drawer
import asyncio

import nonebot
from nonebot import MessageSegment
from nonebot import on_startup
import hoshino
from hoshino import HoshinoBot, Service, priv
from hoshino.config import SUPERUSERS
from hoshino.util import escape
from hoshino.typing import CQEvent, MessageSegment
import random
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
app.secret_key = secrets.token_urlsafe(16)
app.register_blueprint(server.app)
for rule in app.url_map.iter_rules():
    print(f"{rule.rule}\t{', '.join(rule.methods)}")

ROOT_PATH = os.path.dirname(__file__)
cron_group = ""  # 定时任务的通知群
cron_notic_enable = True # 定时任务通知开关

prefix = '#'

sv_help = f"""
[{prefix}配置日常] 一切的开始
[{prefix}清日常 [昵称]] 清日常，无昵称则默认账号
[{prefix}清日常所有] 清该qq号下所有号的日常
[{prefix}日常记录] 查看清日常状态
[{prefix}日常报告[昵称] [0/1/2/3]] 最近四次清日常报告
[{prefix}定时日志] 查看定时运行状态
[{prefix}查心碎 [昵称]] 查询缺口心碎
[{prefix}查记忆碎片 [昵称] [可刷取]] 查询缺口记忆碎片，可刷取只仅查看h图可刷的碎片
[{prefix}查装备 [昵称] [rank] [fav]] 查询缺口装备，[rank]为数字，只查询>=rank的角色缺口装备，fav表示只查询favorite的角色
[{prefix}刷图推荐 [昵称] [rank] [fav]] 查询缺口装备的刷图推荐，格式同上
[{prefix}公会支援] 查询公会支援角色配置
"""

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

@sv.on_fullmatch(["帮助自动清日常"])
async def bangzhu_text(bot, ev):
    await bot.finish(ev, sv_help, at_sender=True)


@on_startup
async def init():
    await db_start()
    from .autopcr.module.crons import queue_crons
    queue_crons()

from dataclasses import dataclass
@dataclass
class ToolInfo:
    key: str
    config_parser: Callable[..., Coroutine[Any, Any, Any]]

tool_info: Dict[str, ToolInfo]= {}

async def check_validate(bot: HoshinoBot, ev: CQEvent, acc: Account):

    from .autopcr.bsdk.validator import validate_dict
    for _ in range(120):
        if acc.qq in validate_dict:
            status = validate_dict[acc.data.username].status
            if status == "ok":
                del validate_dict[acc.alias]
                break

            url = validate_dict[acc.data.username].url
            url = address + url.lstrip("/daily/")
            
            msg=f"[CQ:reply,id={ev.ev.message_id}]pcr账号登录需要验证码，请点击以下链接在120秒内完成认证:\n{url}"
            bot.send(ev, msg)

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

def register_tool(name: str, key: str):
    def wrapper(func):
        tool_info[name] = ToolInfo(key=key, config_parser=func)
        async def inner(*args, **kwargs):
            await func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner
    return wrapper

def wrap_accountmgr(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent, *args, **kwargs):
        user_id = None

        for m in ev.message:
            if m.type == 'at' and m.data['qq'] != 'all':
                user_id = str(m.data['qq'])
        if user_id is None:  # 本人
            user_id = str(ev.user_id)
        else:   
            if not priv.check_priv(ev,priv.ADMIN):
                return bot.finish(ev, f'[CQ:reply,id={ev.message_id}]指定用户清日常需要管理员权限')

        if user_id not in usermgr.qids():
            return bot.finish(ev, f'[CQ:reply,id={ev.message_id}]未找到{user_id}的账号，请发送【{prefix}配置日常】进行配置')

        async with usermgr.load(user_id, readonly=True) as accmgr:
            await func(bot = bot, ev = ev, accmgr = accmgr, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_account(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent, accmgr: AccountManager, *args, **kwargs):
        alias = ""

        for m in ev.message:
            if m.type == 'text':
                alias = str(m.data['text']).strip().split(' ')[0]
                break

        if len(list(accmgr.accounts())) == 1:
            alias = list(accmgr.accounts())[0]

        if alias not in accmgr.accounts():
            alias = accmgr.default_account

        if alias not in accmgr.accounts():
            if alias:
                bot.finish(ev, f"[CQ:reply,id={ev.message_id}]未找到昵称为【{alias}】的账号")
            else:
                bot.finish(ev, f"[CQ:reply,id={ev.message_id}]存在多账号且未设置默认账号，请指定昵称")

        async with accmgr.load(alias) as acc:
            await func(bot = bot, ev = ev, acc = acc, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_tool(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent, *args, **kwargs):
        tool = ""
        index = 0
        raw = ""
        for i, m in enumerate(ev.message):
            if m.type == 'text':
                raw = str(m.data['text']).strip().split(' ')
                tool = raw[0]
                index = i
                break

        if tool not in tool_info:
            return bot.finish(ev, f"[CQ:reply,id={ev.message_id}]未找到工具【{tool}】")

        ev.message[index].data['text'] = ' '.join(raw[1:])

        tool = tool_info[tool]

        await func(bot = bot, ev = ev, tool = tool, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_config(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent, tool: ToolInfo, *args, **kwargs):
        config = await tool.config_parser(bot, ev)
        await func(bot = bot, ev = ev, tool = tool, config = config, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

@sv.on_fullmatch(f"{prefix}清日常所有")
@wrap_accountmgr
async def clean_daily_all(bot: HoshinoBot, ev: CQEvent, accmgr: AccountManager):
    loop = asyncio.get_event_loop()
    task = []
    alias = []
    async def clean_daily_pre(alias: str):
        async with accmgr.load(alias) as acc:
            return await clean_daily(bot, ev, acc)

    for acc in accmgr.accounts():
        alias.append(escape(acc))
        task.append(loop.create_task(clean_daily_pre(acc)))

    try:
        alias_str = ','.join(alias)
        await bot.send(ev, f"[CQ:reply,id={ev.message_id}]开始为{alias_str}清理日常")
    except Exception as e:  
        print(e)

    imgs = await asyncio.gather(*task, return_exceptions=True)
    img = await drawer.horizon_concatenate([img for img in imgs if not isinstance(img, Exception)])
    err = [(alias[i], msg) for i, msg in enumerate(imgs) if isinstance(msg, Exception)]

    msg = f"[CQ:reply,id={ev.message_id}]"
    msg += outp_b64(img)
    await bot.send(ev, msg)

    if err:
        msg = f"[CQ:reply,id={ev.message_id}]"
        msg += "\n".join([f"{a}: {m}" for a, m in err])
        await bot.send(ev, msg)

@sv.on_fullmatch(f"{prefix}查内鬼")
async def find_ghost(bot: HoshinoBot, ev: CQEvent):
    msg = []
    for qq in usermgr.qids():
        if not await is_valid_qq(qq):
            msg.append(qq)
    if not msg:
        msg.append("未找到内鬼")
    await bot.finish(ev, " ".join(msg))

@sv.on_fullmatch(f"{prefix}清内鬼")
async def clean_ghost(bot: HoshinoBot, ev: CQEvent):
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
    await bot.finish(ev, " ".join(msg))

@sv.on_prefix(f"{prefix}清日常")
@wrap_accountmgr
@wrap_account
async def clean_daily_from(bot: HoshinoBot, ev: CQEvent, acc: Account):
    alias = escape(acc.alias)
    try:
        await bot.send(ev, f"[CQ:reply,id={ev.message_id}]开始为{alias}清理日常")
    except Exception as e:  
        print(e)

    try:
        img = await clean_daily(bot = bot, ev = ev, acc = acc)
        msg = f"[CQ:reply,id={ev.message_id}]{alias}"
        msg += MessageSegment.image(f'file:///{img}')
        await bot.send(ev, msg)
    except Exception as e:
        await bot.send(ev, f'[CQ:reply,id={ev.message_id}]{alias}: {e}')

async def clean_daily(bot: HoshinoBot, ev: CQEvent, acc: Account):
    loop = asyncio.get_event_loop()
    loop.create_task(check_validate(bot, ev, acc))

    img, _ = await acc.do_daily()
    return img


@sv.on_prefix(f"{prefix}日常报告")
@wrap_accountmgr
@wrap_account
async def clean_daily_result(bot: HoshinoBot, ev: CQEvent, acc: Account):
    result_id = 0
    try:
        result_id = int(ev.message.extract_plain_text().split(' ')[-1].strip())
    except Exception as e:
        pass
    img = await acc.get_daily_result_from_id(result_id)
    if not img:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + "未找到日常报告")
    await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))

@sv.on_prefix(f"{prefix}日常记录")
@wrap_accountmgr
async def clean_daily_time(bot: HoshinoBot, ev: CQEvent, accmgr: AccountManager):
    content = []
    for alias in accmgr.accounts():
        async with accmgr.load(alias, readonly=True) as acc:
            content += [[acc.alias, daily_result.time, "#" + daily_result.status] for daily_result in acc.data.daily_result]

    if not content:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + "暂无日常记录")
    header = ["昵称", "清日常时间", "状态"]
    img = outp_b64(await drawer.draw(header, content))
    await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + img)

@sv.on_prefix(f"{prefix}定时日志")
async def cron_log(bot: HoshinoBot, ev: CQEvent):
    from .autopcr.module.crons import CRONLOG_PATH
    with open(CRONLOG_PATH, 'r', encoding='utf-8') as f:
        msg = [line.strip() for line in f.readlines()]
    msg = msg[-40:]
    msg = msg[::-1]
    if not msg:
        msg.append("暂无定时日志")
    msg = outp_b64(await drawer.draw_msgs(msg))
    await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + msg)

@sv.on_prefix(f"{prefix}定时统计")
async def cron_statistic(bot: HoshinoBot, ev: CQEvent):
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

    msg = outp_b64(await drawer.draw(header, content))
    await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + msg)

@sv.on_fullmatch(f"{prefix}配置日常")
async def config_clear_daily(bot: HoshinoBot, ev: CQEvent):
    await bot.finish(ev, address + "login")

@sv.on_prefix(f"{prefix}")
@wrap_tool
@wrap_config
@wrap_accountmgr
@wrap_account
async def tool_used(bot: HoshinoBot, ev: CQEvent, tool: ToolInfo, config: Dict[str, str], acc: Account):
    alias = escape(acc.alias)
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(check_validate(bot, ev, acc))

        img = await acc.do_from_key(config, tool.key)
        msg = f"[CQ:reply,id={ev.message_id}]{alias}"
        msg += MessageSegment.image(f'file:///{img}')
        await bot.send(ev, msg)
    except Exception as e:
        await bot.send(ev, f'[CQ:reply,id={ev.message_id}]{alias}: {e}')

@sv.on_fullmatch(f"{prefix}卡池")
async def gacha_current(bot: HoshinoBot, ev: CQEvent):
    msg = '\n'.join(db.get_cur_gacha())
    await bot.finish(ev, msg)

@register_tool("公会支援", 'get_clan_support_unit')
async def clan_support(bot: HoshinoBot, ev: CQEvent):
    return {}

@register_tool("查心碎", "get_need_xinsui")
async def find_xinsui(bot: HoshinoBot, ev: CQEvent):
    return {}

@register_tool("jjc回刺", "jjc_back")
async def jjc_back(bot: HoshinoBot, ev: CQEvent):
    opponent_jjc_rank = 0
    try:
        opponent_jjc_rank = int(ev.message.extract_plain_text().split(' ')[-1].strip())
    except:
        pass
    config = {
        "opponent_jjc_rank": opponent_jjc_rank,
    }
    return config

@register_tool("pjjc回刺", "pjjc_back")
async def pjjc_back(bot: HoshinoBot, ev: CQEvent):
    opponent_pjjc_rank = 0
    try:
        opponent_pjjc_rank = int(ev.message.extract_plain_text().split(' ')[-1].strip())
    except:
        pass
    config = {
        "opponent_pjjc_rank": opponent_pjjc_rank,
    }
    return config

@register_tool("jjc透视", "jjc_info")
async def jjc_info(bot: HoshinoBot, ev: CQEvent):
    use_cache = True
    try:
        use_cache = False if ev.message.extract_plain_text().split(' ')[-1].strip() == 'flush' else True
    except:
        pass
    config = {
        "jjc_info_cache": use_cache,
    }
    return config

@register_tool("pjjc透视", "pjjc_info")
async def pjjc_info(bot: HoshinoBot, ev: CQEvent):
    use_cache = True
    try:
        use_cache = False if ev.message.extract_plain_text().split(' ')[-1].strip() == 'flush' else True
    except:
        pass
    config = {
        "pjjc_info_cache": use_cache,
    }
    return config

@register_tool("查记忆碎片", "get_need_memory")
async def find_memory(bot: HoshinoBot, ev: CQEvent):
    sweep_get_able_unit_memory = False
    try:
        if ev.message.extract_plain_text().split(' ')[-1].strip() == '可刷取':
            sweep_get_able_unit_memory = True
    except:
        pass
    config = {
        "sweep_get_able_unit_memory": sweep_get_able_unit_memory,
    }
    return config


@register_tool(f"来发十连", "gacha_start")
async def shilian(bot: HoshinoBot, ev: CQEvent):
    cc_until_get = False
    pool_id = 0
    try:
        if ev.message.extract_plain_text().split(' ')[-1].strip() == '抽到出':
            cc_until_get = True
    except:
        pass
    try:
        msg = ev.message.extract_plain_text().split(' ')
        if cc_until_get:
            pool_id = msg[-3].strip() + " " + msg[-2].strip()
        else:
            pool_id = msg[-2].strip() + " " + msg[-1].strip()
    except:
        pass

    config = {
        "pool_id": pool_id,
        "cc_until_get": cc_until_get,
    }
    return config

@register_tool(f"查装备", "get_need_equip")
async def find_equip(bot: HoshinoBot, ev: CQEvent):
    like_unit_only = False
    try:
        if ev.message.extract_plain_text().split(' ')[-1].strip() == 'fav':
            like_unit_only = True
            start_rank = int(ev.message.extract_plain_text().split(' ')[-2])
        else:
            start_rank = int(ev.message.extract_plain_text().split(' ')[-1])
    except:
        start_rank = None

    config = {
        "start_rank": start_rank,
        "like_unit_only": like_unit_only
    }
    return config

@register_tool(f"刷图推荐", "get_normal_quest_recommand")
async def quest_recommand(bot: HoshinoBot, ev: CQEvent):
    like_unit_only = False
    try:
        if ev.message.extract_plain_text().split(' ')[-1].strip() == 'fav':
            like_unit_only = True
            start_rank = int(ev.message.extract_plain_text().split(' ')[-2])
        else:
            start_rank = int(ev.message.extract_plain_text().split(' ')[-1])
    except:
        start_rank = None

    config = {
        "start_rank": start_rank,
        "like_unit_only": like_unit_only
    }
    return config


# @register_tool("获取导入", "get_library_import_data")
# async def get_library_import(bot: HoshinoBot, ev: CQEvent):
    # return {}
