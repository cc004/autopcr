import requests
import os
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.module.modules import register_all
from .autopcr.core.database import init_db, db
import asyncio
import os
import aiocqhttp

import nonebot
from nonebot import MessageSegment
from nonebot import on_startup
import hoshino
from hoshino import HoshinoBot, Service, priv
from hoshino.typing import CQEvent, MessageSegment
from hoshino.config import PUBLIC_ADDRESS
from .util import get_info, get_result
from .task import Task
from .autopcr.bsdk.validator import validate_ok_queue, validate_queue
import datetime
import random
import asyncio

register_all()

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
"""

address = "https://" + PUBLIC_ADDRESS + "/daily/"

queue = asyncio.Queue()
inqueue = set({})
comsuming = False
cur_task: Task = None
validate = ""
gid = ""

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

async def comsumer():
    global inqueue
    global comsuming
    global queue
    global cur_task
    while True:
        task = await queue.get()
        comsuming = True
        cur_task = task
        token = await task.do_task()
        inqueue.remove(token)
        queue.task_done()
        comsuming = False

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
    global comsuming
    if not comsuming:
        await bot.finish(ev, "[CQ:reply,id={ev.message_id}]你在干什么？")
    validate = ev.message.extract_plain_text().strip()
    await validate_ok_queue.put(validate)

@sv.on_prefix("#取消")
async def cancle_validate(bot, ev):
    global comsuming
    if not comsuming:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]你在干什么？")
    alian, _, _, c_ev, _, _ = cur_task.info 
    await validate_ok_queue.put("xcwcancle")
    if c_ev:
        await bot.send(c_ev, f"[CQ:reply,id={c_ev.message_id}]已取消当前【{alian}】的任务")
    else:
        await bot.send(c_ev, f"[CQ:reply,id={ev.message_id}]已取消当前【{alian}】的任务")

@on_startup
async def start_daily():
    global queue
    loop = asyncio.get_event_loop()
    loop.create_task(comsumer())
    loop.create_task(manual_validate())
    global gid
    global cron_group
    gid = list((await sv.get_enable_groups()).keys())[0]
    if cron_group:
        gid = cron_group

@sv.scheduled_job('cron', hour='14', minute='15')
async def auto_update_database():
    bot = hoshino.get_bot()
    global gid
    msg = await do_update_database()
    if msg.startswith("未发现新版本数据库"):
        return
    msg = "发现数据库更新，" + msg
    await bot.send_group_msg(group_id = gid, message = msg)

@sv.scheduled_job('interval', minutes=1)
async def timing():
    if db.is_clan_battle_time():
        return

    global gid
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    now = f"{hour}".rjust(2, '0') + ":" + f"{minute}".rjust(2, '0')
    await asyncio.sleep(random.randint(1, 10)) 
    data = await get_info()
    bot = hoshino.get_bot()
    for user_id, configs in data.items():
        for config, target in configs:
            if "time1" not in config or "time2" not in config:
                continue
            if config['time1open'] and config['time1'] == now or  \
            config['time2open'] and config['time2'] == now:

                alian = config['alian']
                token = (user_id, target)
                if token in inqueue:
                    await bot.send_group_msg(group_id = gid, message = f"【定时任务】{alian}已在清日常队列里")
                    continue

                inqueue.add(token)
                global comsuming, queue
                if not queue.empty() or comsuming:
                    await bot.send_group_msg(group_id = gid, message = f"【定时任务】当前有人正在清日常，已将{alian}加入等待队列中")

                await queue.put(Task(alian, target, bot, None, user_id, gid))

@sv.on_fullmatch("#cron")
async def check_schedule(bot, ev):
    if db.is_clan_battle_time():
        await bot.finish(ev, "当前处于会战期间，定时任务暂停")
    else:
        await bot.finish(ev, "当前不处于会战期间，定时任务正常运行")

@sv.on_fullmatch("#清日常所有")
async def clear_daily_all(bot: HoshinoBot, ev: CQEvent):
    data = await get_info()
    user_id = None
    alian = ""

    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            user_id = str(m.data['qq'])
        elif m.type == 'text':
            alian = str(m.data['text']).strip()
    if user_id is None: #本人
        user_id = str(ev.user_id)
    else:   #指定对象
        if not priv.check_priv(ev,priv.ADMIN):
            await bot.finish(ev, f'[CQ:reply,id={ev.message_id}]指定用户清日常需要管理员权限')

    if user_id not in data:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]请发送【配置清日常】配置")
    for config, target in data[user_id]:
        alian = config['alian'] 
        token = (ev.user_id, target)
        if token in inqueue:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]{alian}已在清日常队列里，请耐心等待")
            continue

        inqueue.add(token)
        global comsuming, queue
        if not queue.empty() or comsuming:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]当前有人正在清日常，已将{alian}加入等待队列中")

        await queue.put(Task(alian, target, bot, ev))

@sv.on_prefix("#日常报告")
async def clear_daily_result(bot: HoshinoBot, ev: CQEvent):
    ok, msg, alian, target = await get_config(bot, ev)
    if not ok:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + msg)
    ok, img = await get_result(alian)
    if not ok:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + img)
    await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))

@sv.on_prefix("#清日常")
async def clear_daily(bot: HoshinoBot, ev: CQEvent):
    ok, msg, alian, target = await get_config(bot, ev)
    if not ok:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]" + msg)

    token = (ev.user_id, target)
    if token in inqueue:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]{alian}已在清日常队列里，请耐心等待")

    inqueue.add(token)
    global comsuming, queue
    if not queue.empty() or comsuming:
        await bot.send(ev, f"[CQ:reply,id={ev.message_id}]当前有人正在清日常，已将{alian}加入等待队列中")

    await queue.put(Task(alian, target, bot, ev))


async def get_config(bot, ev):
    data = await get_info()
    user_id = None
    alian = ""
    target = ""

    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            user_id = str(m.data['qq'])
        elif m.type == 'text':
            alian = str(m.data['text']).strip()
    if user_id is None: #本人
        user_id = str(ev.user_id)
    else:   #指定对象
        if not priv.check_priv(ev,priv.ADMIN):
            return False, '[CQ:reply,id={ev.message_id}]指定用户清日常需要管理员权限', alian, target

    if user_id not in data:
        return False, "[CQ:reply,id={ev.message_id}]请发送【配置清日常】配置", alian, target

    if len(data[user_id]) != 1 and not alian:
        name = ' '.join([i[0]['alian'] for i in data[user_id]])
        msg = f"[CQ:reply,id={ev.message_id}]存在多个账号，请指定一个昵称：\n{name}"
        return False, msg, alian, target
    elif len(data[user_id]) == 1:
        config, target = data[user_id][0]
        alian = config['alian']
    else:
        for config, file in data[user_id]:
            if config['alian'] == alian:
                target = file
                break
    if not target:
        return False, f"[CQ:reply,id={ev.message_id}]未找到昵称为【{alian}】的账号", alian, target

    return True, "", alian, target

@sv.on_fullmatch("#配置日常")
async def config_clear_daily(bot: HoshinoBot, ev: CQEvent):
    await bot.finish(ev, address)

@sv.on_fullmatch("#更新数据库")
async def update_database(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, f"开始更新数据库...")
    msg = await do_update_database()
    await bot.finish(ev, msg)

@sv.on_fullmatch("#强制更新数据库")
async def force_update_database(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, f"开始强制更新数据库...")
    msg = await do_update_database(True)
    await bot.finish(ev, msg)

async def do_update_database(force: bool = False):
    info = f'https://redive.estertion.win/db'

    rsp = requests.get(info, stream=True, timeout=20)
    pos = rsp.text.find("redive_cn.db</a>")
    end = rsp.text.find("\n", pos)
    update_time = ""
    for t in rsp.text[pos:end].split(' '):
        if "-" in t:
            update_time += t + " "
        elif ":" in t:
            update_time += t

    version = os.path.join(ROOT_PATH, "db.version")
    try:
        now_version = open(version, "r").read().strip()
    except FileNotFoundError:
        now_version = None
    if not force and now_version == update_time:
        return f"未发现新版本数据库，当前版本{now_version}"

    url = f'https://redive.estertion.win/db/redive_cn.db'
    save_path = os.path.join(ROOT_PATH, "redive_cn.db")
    sv.logger.info(f'Downloading newest database from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            with open(save_path, "wb") as f:
                f.write(rsp.content)
            init_db()
        else:
            return f"下载失败：{rsp.status_code}"
    except Exception as e:
        return str(e)
    with open(version, "w") as f:
        f.write(update_time)
    return f"更新成功至：{update_time} 版本"
