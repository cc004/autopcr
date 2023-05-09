import pandas as pd
import json
import imgkit
import os
from collections import defaultdict
import glob
from nonebot import MessageSegment
from hoshino.typing import MessageSegment, Message

from .autopcr.module.modulebase import ModuleManager

PATH = os.path.dirname(__file__)
CONFIG = os.path.join(PATH, "autopcr", "http_server", "config")
RESULT = os.path.join(PATH, "result")

class Task():
    def __init__(self, alian, target, bot, ev):
        self.info = (alian, target, bot, ev)

    async def do_task(self):
        alian, target, bot, ev = self.info 
        mgr = ModuleManager(target)

        await bot.send(ev, f"[CQ:reply,id={ev.message_id}]开始为{alian}清理日常")
        try:
            resp = await mgr.do_task()
            img = await draw(resp, target)
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

        return ev.user_id, target

async def get_info():
    tmp = defaultdict(list)
    for file in glob.glob(os.path.join(CONFIG, "*.json")):
        with open(file, "r") as f:
            data = json.load(f)
            tmp[data['qq']].append((data['alian'], file))
    return tmp

def hightlight_rule(value):
    if value == "success":
        color = "#e1ffb5"
    elif value == "skip":
        color = "#c8d6fa"
    elif value == "error":
        color = "#FF0000"
    else:
        color = "#FFFFFF"
    return f"background-color: {color}"

async def draw(data: dict, file: str):
    tmp = {
            # "id": [],
            # "name": [],
            "desc": [],
            "value": [],
            "status": [],
            "result": [],
            }
    for _, value in data.items():
        # tmp["id"].append(key)
        # tmp["name"].append(value['name'])
        tmp["desc"].append(value['desc'])
        tmp["value"].append(value['value'])
        tmp["status"].append(value['status'])
        tmp["result"].append(value['msg'].replace("\n", "<br />"))

    df = pd.DataFrame(tmp)
    df = df.style.applymap(hightlight_rule, subset=['status']).set_table_styles([{'selector' : 'tr, th, td, table', 'props' : [('border', '1px solid')]}])
    file = os.path.join(RESULT, f"{file}.png")
    imgkit.from_string(df.to_html(index=False, escape=False), file)
    return file

