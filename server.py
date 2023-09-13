from typing import List, Tuple
import os
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.db.database import db
from .autopcr.core.datamgr import datamgr
from .autopcr.constants import CACHE_DIR
from .autopcr.module.accountmgr import instance as accountmgr
from .autopcr.db.dbstart import db_start
import asyncio
from traceback import print_exc

import nonebot
from nonebot import MessageSegment
from nonebot import on_startup
import hoshino
from hoshino import HoshinoBot, Service, priv
from hoshino.config import SUPERUSERS
from hoshino.util import escape
from hoshino.typing import CQEvent, MessageSegment
from ._util import get_result
from ._task import DailyClean, FindEquip, FindMemory, FindXinsui, Task, GetLibraryImport, QuestRecommand, Gacha
import datetime
import random

address = None # 填你的公网IP或域名，不填则会自动尝试获取
useHttps = False

server = HttpServer(qq_only=True)
app = nonebot.get_bot().server_app
app.register_blueprint(server.app)

ROOT_PATH = os.path.dirname(__file__)
cron_group = "" # 定时任务的通知群

prefix = '#'

sv_help = f"""
[{prefix}清日常 [昵称]] 开始清日常，当该qq下有多个账号时需指定昵称
[{prefix}清日常所有] 开始清该qq号下所有号的日常
[{prefix}配置日常] 配置日常
[{prefix}日常报告] 获取最近一次清日常的报告
[{prefix}查心碎 [昵称]] 查询缺口心碎
[{prefix}查记忆碎片 [昵称] [可刷取]] 查询缺口记忆碎片，可刷取只仅查看h图可刷的碎片
[{prefix}查装备 [昵称] [rank] [fav]] 查询缺口装备，[rank]为数字，只查询>=rank的角色缺口装备，fav表示只查询favorite的角色
[{prefix}刷图推荐 [昵称] [rank] [fav]] 查询缺口装备的刷图推荐，格式同上
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

inqueue = set({})
consuming = False
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

async def check_validate(task):
    username = task.username
    alian, _, bot, ev, qid, gid = task.info 
    
    from .autopcr.bsdk.validator import validate_dict
    for _ in range(120):
        if username in validate_dict:
            url = validate_dict[username]
            if url == "ok":
                del validate_dict[username]
                break

            url = address + url.lstrip("/daily/")
            if ev:
                await bot.send(ev, f'[CQ:reply,id={ev.message_id}]pcr账号登录需要验证码，请点击以下链接在120秒内完成认证:\n{url}')
            else:
                await bot.send_group_msg(group_id = gid, msg = f"【定时任务】帐号需要验证码，【{alian}】定时任务自动取消[CQ:at,qq={qid}]")

            del validate_dict[username]

        else:
            await asyncio.sleep(1)

async def consumer(task):
    global inqueue
    token = task.token
    loop = asyncio.get_event_loop()
    loop.create_task(check_validate(task))
    try:
        await task.do_task()
    except Exception as e:
        sv.logger.error(f"执行清日常出错:" + str(e))
        print_exc()
        await report_to_su(None, "", "执行清日常出错:" + str(e))
    finally:
        inqueue.remove(token)

def pre_process_all(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent):
        ok, msg, tokens = await get_config(bot, ev, True)
        if not ok:
            await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + msg)

        res = []
        for token in tokens:
            if token in inqueue:
                await bot.send(ev, f"[CQ:reply,id={ev.message_id}]{token[0]}已在执行任务，请耐心等待")
                continue
            inqueue.add(token)
            res.append(token)

        await func(bot, ev, res)

    return wrapper

def pre_process(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent):
        ok, msg, token = await get_config(bot, ev)
        if not ok:
            await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + msg)

        if token in inqueue:
            await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]{token[0]}已在执行任务，请耐心等待")

        inqueue.add(token)

        await func(bot, ev, token)

    return wrapper

@sv.scheduled_job('interval', minutes=1)
async def timing():

    global cron_group
    gid = list((await sv.get_enable_groups()).keys())[0]
    if cron_group:
        gid = cron_group

    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    await asyncio.sleep(random.randint(1, 10)) 
    bot = hoshino.get_bot()
    loop = asyncio.get_event_loop()

    for account in accountmgr.accounts():
        async with accountmgr.load(account) as mgr:
            if not mgr.is_cron_run(hour, minute):
                continue

            alian = escape(mgr.alian)
            target = account
            user_id = mgr.qq
            token = (alian, target)
            if token in inqueue:
                await bot.send_group_msg(group_id = gid, message = f"【定时任务】{alian}已在执行任务")
                continue

            inqueue.add(token)

            loop.create_task(consumer(DailyClean(token, bot, None, user_id, gid)))

@sv.on_fullmatch(f"{prefix}清日常所有")
@pre_process_all
async def clear_daily_all(bot: HoshinoBot, ev: CQEvent, tokens: List[Tuple[str, str]]):
    loop = asyncio.get_event_loop()
    for token in tokens:
        loop.create_task(consumer(DailyClean(token, bot, ev)))

@sv.on_prefix(f"{prefix}查心碎")
@pre_process
async def find_xinsui(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(FindXinsui(token, bot, ev))

@sv.on_prefix(f"{prefix}查记忆碎片")
@pre_process
async def find_memory(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    sweep_get_able_unit_memory = False
    try:
        if ev.message.extract_plain_text().split(' ')[-1].strip() == '可刷取':
            sweep_get_able_unit_memory = True
    except:
        pass

    config = {
            "sweep_get_able_unit_memory" : sweep_get_able_unit_memory,
    }
    await consumer(FindMemory(token = token, config = config, bot = bot, ev = ev))

@sv.on_prefix(f"{prefix}来发十连")
@pre_process
async def shilian(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
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
            "pool_id" : pool_id,
            "cc_until_get" : cc_until_get,
    }
    await consumer(Gacha(token = token, config = config, bot = bot, ev = ev))

@sv.on_prefix(f"{prefix}查装备")
@pre_process
async def find_equip(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
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
            "start_rank" : start_rank,
            "like_unit_only": like_unit_only
    }
    await consumer(FindEquip(token = token, config = config, bot = bot, ev = ev))

@sv.on_prefix(f"{prefix}刷图推荐")
@pre_process
async def quest_recommand(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
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
            "start_rank" : start_rank,
            "like_unit_only": like_unit_only
    }
    await consumer(QuestRecommand(token = token, config = config, bot = bot, ev = ev))


@sv.on_prefix(f"{prefix}获取导入")
@pre_process
async def get_library_import(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(GetLibraryImport(token = token, bot = bot, ev = ev))

@sv.on_prefix(f"{prefix}清日常")
@pre_process
async def clear_daily(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(DailyClean(token, bot, ev))

@sv.on_prefix(f"{prefix}日常报告")
@pre_process
async def clear_daily_result(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    alian, target = token

    global inqueue
    inqueue.remove(token)

    ok, img = await get_result(alian)
    if not ok:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + img)
    await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))

async def get_config(bot, ev, tot = False):
    user_id = None
    alian = ""
    file = ""
    token = (alian, file)

    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            user_id = str(m.data['qq'])
        elif m.type == 'text':
            alian = str(m.data['text']).strip().split(' ')[0]
    if user_id is None: #本人
        user_id = str(ev.user_id)
    else:   #指定对象
        if not priv.check_priv(ev,priv.ADMIN):
            return False, '[CQ:reply,id={ev.message_id}]指定用户清日常需要管理员权限', token

    accounts = []
    alian = escape(alian)

    for file in accountmgr.accounts():
        async with accountmgr.load(file, readonly = True) as account:
            if account.qq == user_id:
                accounts.append((escape(account.alian), file))

    if not accounts:
        return False, "[CQ:reply,id={ev.message_id}]请发送【#配置日常】配置", token

    if tot:
        return True, "", accounts

    if len(accounts) == 1:
        return True, "", accounts[0]

    if not alian:
        name = ' '.join([i[0] for i in accounts])
        msg = f"[CQ:reply,id={ev.message_id}]存在多个帐号，请指定一个昵称：\n{name}"
        return False, msg, token
    
    accounts = [account for account in accounts if account[0] == alian]

    if not accounts:
        return False, f"[CQ:reply,id={ev.message_id}]未找到昵称为【{alian}】的账号", token

    if len(accounts) > 1:
        msg = f"[CQ:reply,id={ev.message_id}]存在{len(accounts)}个同为{alian}的帐号，请更改为不同昵称\n"
        return False, msg, token

    return True, "", accounts[0]

@sv.on_fullmatch(f"{prefix}配置日常")
async def config_clear_daily(bot: HoshinoBot, ev: CQEvent):
    await bot.finish(ev, address)

async def report_to_su(sess, msg_with_sess, msg_wo_sess):
    if sess:
        await sess.send(msg_with_sess)
    else:
        bot = hoshino.get_bot()
        sid = bot.get_self_ids()
        if len(sid) > 0:
            sid = random.choice(sid)
            await bot.send_private_msg(self_id=sid, user_id=SUPERUSERS[0], message=msg_wo_sess)
