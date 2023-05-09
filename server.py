import requests
import os
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.module.modules import register_all
from .autopcr.core.database import init_db
import asyncio
import os
import aiocqhttp

import nonebot
from nonebot import on_startup
from hoshino import HoshinoBot, Service, priv
from hoshino.typing import CQEvent
from hoshino.config import PUBLIC_ADDRESS
from .util import Task, get_info

register_all()

server = HttpServer(qq_only=True)
app = nonebot.get_bot().server_app
app.register_blueprint(server.app)


sv_help = """
[#清日常 [昵称]] 开始清日常，当该qq下有多个账号时需指定昵称
[#配置日常] 配置日常
"""

address = "https://" + PUBLIC_ADDRESS + "/daily/"

queue = asyncio.Queue()
inqueue = set({})
comsuming = False

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
    while True:
        task = await queue.get()
        comsuming = True
        token = await task.do_task()
        inqueue.remove(token)
        queue.task_done()
        comsuming = False

@on_startup
async def start_daily():
    global queue
    loop = asyncio.get_event_loop()
    loop.create_task(comsumer())

@sv.on_prefix("#清日常")
async def clear_daily(bot: HoshinoBot, ev: CQEvent):
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
            await bot.finish(ev, '[CQ:reply,id={ev.message_id}]指定用户清日常需要管理员权限')

    if user_id not in data:
        await bot.finish(ev, "[CQ:reply,id={ev.message_id}]请发送【配置清日常】配置")
    target = ""
    if len(data[user_id]) != 1 and not alian:
        name = ' '.join([i[0] for i in data[user_id]])
        msg = f"[CQ:reply,id={ev.message_id}]存在多个账号，请指定一个昵称：\n{name}"
        await bot.finish(ev, msg)
    elif len(data[user_id]) == 1:
        target = data[user_id][0][1]
        alian = data[user_id][0][0]
    else:
        for i in data[user_id]:
            if i[0] == alian:
                target = i[1]
                break
    if not target:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]未找到昵称为【{alian}】的账号")

    token = (ev.user_id, target)
    if token in inqueue:
        await bot.finish(ev, f"[CQ:reply,id={ev.message_id}]您已在清日常队列里，请耐心等待")

    inqueue.add(token)
    global comsuming, queue
    if not queue.empty() or comsuming:
        await bot.send(ev, f"[CQ:reply,id={ev.message_id}]当前有人正在清日常，已将{alian}加入等待队列中")

    await queue.put(Task(alian, target, bot, ev))

@sv.on_fullmatch("#配置日常")
async def config_clear_daily(bot: HoshinoBot, ev: CQEvent):
    await bot.finish(ev, address)

@sv.on_fullmatch("#更新数据库")
async def update_database(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, f"开始更新数据库...")

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

    url = f'https://redive.estertion.win/db/redive_cn.db'
    save_path = os.path.join(os.path.dirname(__file__), "redive_cn.db")
    sv.logger.info(f'Downloading newest database from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=20)
        if 200 == rsp.status_code:
            with open(save_path, "wb") as f:
                f.write(rsp.content)
            init_db()
        else:
            await bot.finish(ev, f"下载失败：{rsp.status_code}")
    except Exception as e:
        await bot.finish(ev, str(e))
    with open("db.version", "w") as f:
        f.write(update_time)
    await bot.finish(ev, f"更新成功至：{update_time} 版本")

