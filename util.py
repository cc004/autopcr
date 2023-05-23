import pandas as pd
import json
import imgkit
import os
from collections import defaultdict
import glob
import asyncio

PATH = os.path.dirname(__file__)
CONFIG = os.path.join(PATH, "autopcr", "http_server", "config")
RESULT = os.path.join(PATH, "result")

async def get_info():
    tmp = defaultdict(list)
    for file in glob.glob(os.path.join(CONFIG, "*.json")):
        with open(file, "r") as f:
            data = json.load(f)
            tmp[data['qq']].append((data, file))
    return tmp

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

async def draw(data: dict, alian: str):
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
        if value['msg'] == "功能未启用":
            continue
        tmp["desc"].append(value['desc'])
        tmp["value"].append(value['value'])
        tmp["status"].append(value['status'])
        tmp["result"].append(value['msg'].replace("\n", "<br />"))

    df = pd.DataFrame(tmp)
    df = df.style.applymap(hightlight_rule, subset=['status']).set_table_styles([{'selector' : 'thead tr', 'props' : [('background-color', '#F5F5D5!important')]}, {'selector' : 'tr:nth-child(odd)', 'props' : [('background-color', '#E0E0FF')]}, {'selector' : 'tr:nth-child(even)', 'props' : [('background-color', '#F8F8F8')]}])
    file = os.path.join(RESULT, f"{alian}.jpg")
    imgkit.from_string(df.to_html(index=False, escape=False), file)
    return file

if __name__ == "__main__":
    asyncio.run(draw(json.loads(open("test.json" ,"r").read()), "test"))

