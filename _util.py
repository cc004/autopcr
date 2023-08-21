import pandas as pd
import json
import imgkit
import os
from collections import defaultdict
from .autopcr.constants import CONFIG_PATH
import glob
import asyncio

PATH = os.path.dirname(__file__)
RESULT = os.path.join(PATH, "result")

async def get_result(alian):
    file = os.path.join(RESULT, f"{alian}.jpg")
    if not os.path.exists(file):
        return False, "不存在最近一次清日常记录"
    else:
        return True, file

def hightlight_rule(value):
    if value == "success":
        color = "#e1ffb5"
    elif value == "skip":
        color = "#c8d6fa"
    elif value == "abort":
        color = "#FFFF00"
    elif value == "error":
        color = "#FF0000"
    else:
        color = "#FFFFFF"
    return f"background-color: {color}"

async def draw_line(data: list, alian: str):
    tmp = {
            "msg": [],
            }
    for value in data:
        tmp["msg"].append(value.replace("\n", "<br />"))

    df = pd.DataFrame(tmp)
    df = df.style.set_table_styles([{'selector' : 'thead tr', 'props' : [('background-color', '#F5F5D5!important')]}, {'selector' : 'tr:nth-child(odd)', 'props' : [('background-color', '#E0E0FF')]}, {'selector' : 'tr:nth-child(even)', 'props' : [('background-color', '#F8F8F8')]}])
    file = os.path.join(RESULT, f"{alian}_tmp.jpg")
    imgkit.from_string(df.to_html(index=False, escape=False), file)
    return file

async def draw(data: dict, alian: str):
    tmp = {
            "name": [],
            "config": [],
            "status": [],
            "result": [],
            }
    result = data['result']
    for key in data['order']:
        value = result[key]
        if value['log'] == "功能未启用":
            continue
        tmp["name"].append(value['name'])
        tmp["config"].append(value['config'].replace("\n", "<br />"))
        tmp["status"].append(value['status'])
        tmp["result"].append(value['log'].replace("\n", "<br />"))

    df = pd.DataFrame(tmp)
    df = df.style.applymap(hightlight_rule, subset=['status']).set_table_styles([{'selector' : 'thead tr', 'props' : [('background-color', '#F5F5D5!important')]}, {'selector' : 'tr:nth-child(odd)', 'props' : [('background-color', '#E0E0FF')]}, {'selector' : 'tr:nth-child(even)', 'props' : [('background-color', '#F8F8F8')]}])
    file = os.path.join(RESULT, f"{alian}.jpg")
    imgkit.from_string(df.to_html(index=False, escape=False), file)
    return file

def render_forward_msg(msg_list: list, uid=244115379, name='兰德索尔图书馆管理员'):
    forward_msg = []
    for msg in msg_list:
        forward_msg.append({
            "type": "node",
            "data": {
                "name": str(name),
                "uin": str(uid),
                "content": msg
            }
        })
    return forward_msg

if __name__ == "__main__":
    asyncio.run(draw(json.loads(open("test.json" ,"r").read()), "test"))

