from typing import List, Tuple
import os
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.module.modules import register_all
from .autopcr.db.database import db
from .autopcr.core.datamgr import datamgr
from .autopcr.constants import CACHE_DIR
import asyncio
import os
import glob
import aiocqhttp
from traceback import print_exc

import nonebot
from nonebot import MessageSegment
from nonebot import on_startup
import hoshino
from hoshino import HoshinoBot, Service, priv
from hoshino.config import SUPERUSERS
from hoshino.util import escape
from hoshino.typing import CQEvent, MessageSegment
from ._util import get_info, get_result
from ._task import DailyClean, FindEquip, FindMemory, FindXinsui, Task, GetLibraryImport, QuestRecommand
import datetime
import random
import asyncio

register_all()

address = None # 填你的公网IP或域名，不填则会自动尝试获取
useHttps = False

server = HttpServer(qq_only=True)
app = nonebot.get_bot().server_app
app.register_blueprint(server.app)

ROOT_PATH = os.path.dirname(__file__)
cron_group = "" # 定时任务的通知群

sv_help = """
[#清日常 [昵称]] 开始清日常，当该qq下有多个账号时需指定昵称
[#清日常所有] 开始清该qq号下所有号的日常
[#配置日常] 配置日常
[#日常报告] 获取最近一次清日常的报告
[#查心碎 [昵称]] 查询缺口心碎
[#查记忆碎片 [昵称]] 查询缺口记忆碎片
[#查装备 [昵称] [rank] [fav]] 查询缺口装备，[rank]为数字，只查询>=rank的角色缺口装备，fav表示只查询favorite的角色
[#刷图推荐 [昵称] [rank] [fav]] 查询缺口装备的刷图推荐，格式同上
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
    dbs = glob.glob(os.path.join(CACHE_DIR, "db", "*.db"))
    if dbs:
        db = max(dbs)
        version = int(os.path.basename(db).split('.')[0])
        await datamgr.try_update_database(version)

async def consumer(task):
    global inqueue
    token = task.token
    try:
        await task.do_task()
    except Exception as e:
        sv.logger.error(f"执行清日常出错:" + str(e))
        print_exc()
        await report_to_su(None, "", "执行清日常出错:" + str(e))
    finally:
        inqueue.remove(token)

'''
async def manual_validate():
global cur_task
while True:
    (challenge, gt, userid) = await validate_queue.get()
    alian, _, bot, ev, qid, gid = cur_task.info 
    url = f"https://help.tencentbot.top/geetest/?captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    if ev:
        await bot.send(ev, f'[CQ:reply,id={ev.message_id}]pcr账号登录需要验证码，请完成以下链接中的验证内容后将第一行validate=后面的内容复制，并用指令#pcrval xxxx将内容发送给机器人完成验证\n验证链接')
        await bot.send(ev, f'[CQ:reply,id={ev.message_id}]{url}')
    else:
        await bot.send_group_msg(group_id = gid, msg = f"【定时任务】帐号需要验证码，【{alian}】定时任务自动取消[CQ:at,qq={qid}]")
        await validate_ok_queue.put("xcwcancle")

@sv.on_prefix("#pcrval")
async def receive_validate(bot, ev):
global consuming
if not consuming:
        await bot.finish(ev, "[CQ:reply,id={ev.message_id}]你在干什么？")
    validate = ev.message.extract_plain_text().strip()
    await validate_ok_queue.put(validate)

@sv.on_prefix("#取消")
async def cancle_validate(bot, ev):
    global consuming
    if not consuming:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]你在干什么？")
    alian, _, _, c_ev, _, _ = cur_task.info 
    await validate_ok_queue.put("xcwcancle")
    if c_ev:
        await bot.send(c_ev, f"[CQ:reply,id={c_ev.message_id}]已取消当前【{alian}】的任务")
    else:
        await bot.send(c_ev, f"[CQ:reply,id={ev.message_id}]已取消当前【{alian}】的任务")
'''

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
    now = f"{hour}".rjust(2, '0') + ":" + f"{minute}".rjust(2, '0')
    await asyncio.sleep(random.randint(1, 10)) 
    data = await get_info()
    bot = hoshino.get_bot()
    loop = asyncio.get_event_loop()

    def run(config):
        for key in [key for key in config if key.startswith("cron")]:
            enable = config[key]
            time = config["time_" + key]
            clan_battle_run = config["clan_battle_run_" + key]
            if enable and time == now and (not db.is_clan_battle_time() or clan_battle_run):
                return True
        return False

    for user_id, configs in data.items():
        for config, target in configs:
            if run(config):

                alian = escape(config['alian'])
                token = (alian, target)
                if token in inqueue:
                    await bot.send_group_msg(group_id = gid, message = f"【定时任务】{alian}已在执行任务")
                    continue

                inqueue.add(token)

                loop.create_task(consumer(DailyClean(token, bot, None, user_id, gid)))

@sv.on_fullmatch("#清日常所有")
@pre_process_all
async def clear_daily_all(bot: HoshinoBot, ev: CQEvent, tokens: List[Tuple[str, str]]):
    loop = asyncio.get_event_loop()
    for token in tokens:
        loop.create_task(consumer(DailyClean(token, bot, ev)))

@sv.on_prefix("#查心碎")
@pre_process
async def find_xinsui(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(FindXinsui(token, bot, ev))

@sv.on_prefix("#查记忆碎片")
@pre_process
async def find_memory(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(FindMemory(token, bot, ev))

@sv.on_prefix("#查装备")
@pre_process
async def find_equip(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    fav = False
    try:
        if ev.message.extract_plain_text().split(' ')[-1].strip() == 'fav':
            fav = True
            start_rank = int(ev.message.extract_plain_text().split(' ')[-2]) 
        else:
            start_rank = int(ev.message.extract_plain_text().split(' ')[-1]) 
    except:
        start_rank = None

    await consumer(FindEquip(token = token, like_unit_only = fav, start_rank = start_rank, bot = bot, ev = ev))

@sv.on_prefix("#刷图推荐")
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

    await consumer(QuestRecommand(token = token, like_unit_only = like_unit_only, start_rank = start_rank, bot = bot, ev = ev))


@sv.on_prefix("#获取导入")
@pre_process
async def get_library_import(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(GetLibraryImport(token = token, bot = bot, ev = ev))

@sv.on_prefix("#清日常")
@pre_process
async def clear_daily(bot: HoshinoBot, ev: CQEvent, token: Tuple[str, str]):
    await consumer(DailyClean(token, bot, ev))

@sv.on_prefix("#日常报告")
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
    data = await get_info()
    user_id = None
    alian = ""
    target = ""
    token = (alian, target)

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

    if user_id not in data:
        return False, "[CQ:reply,id={ev.message_id}]请发送【#配置日常】配置", token

    tokens = []
    alian = escape(alian)

    for config, file in data[user_id]:
        if not alian or config['alian'] == alian or len(data[user_id]) == 1:
            target = file
            tokens.append((escape(config['alian']), target))

    if not tokens:
        return False, f"[CQ:reply,id={ev.message_id}]未找到昵称为【{alian}】的账号", token

    if tot:
        return True, "", tokens

    if len(tokens) > 1:
        if not alian:
            name = ' '.join([i[0] for i in tokens])
            msg = f"[CQ:reply,id={ev.message_id}]存在多个帐号，请指定一个昵称：\n{name}"
            return False, msg, token
        else:
            msg = f"[CQ:reply,id={ev.message_id}]存在{len(tokens)}个同为{alian}的帐号，请更改为不同昵称\n"
            return False, msg, token

    token = tokens[0]

    return True, "", token

@sv.on_fullmatch("#配置日常")
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
