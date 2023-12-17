import json
import os
import asyncio

PATH = os.path.dirname(__file__)
RESULT = os.path.join(PATH, "result")
DATA = os.path.join(PATH, "data")

async def get_result(alian, qid):
    file = os.path.join(RESULT, f"{alian}_{str(qid)}.jpg")
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

    import pandas as pd
    df = pd.DataFrame(tmp)
    df = df.style.set_table_styles([{'selector': 'thead tr', 'props': [('background-color', '#F5F5D5!important')]},
                                    {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#E0E0FF')]},
                                    {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#F8F8F8')]}])
    file = os.path.join(RESULT, f"{alian}_tmp.jpg")
    import imgkit
    imgkit.from_string(df.to_html(index=False, escape=False), file)
    return file


async def old_draw(data: dict, alian: str, qid: int):
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

    import pandas as pd
    df = pd.DataFrame(tmp)
    df = df.style.applymap(hightlight_rule, subset=['status']).set_table_styles(
        [{'selector': 'thead tr', 'props': [('background-color', '#F5F5D5!important')]},
         {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#E0E0FF')]},
         {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#F8F8F8')]}])
    file = os.path.join(RESULT, f"{alian}_{str(qid)}.jpg")
    import imgkit
    imgkit.from_string(df.to_html(index=False, escape=False), file)
    return file

def color():
    return {
        'bg': 'white',
        'odd_row_cell_bg': '#EEEEEE',
        'even_row_cell_bg': 'white',
        'header_bg': '#C8C8C9',
        'font': 'black',
        'rowline': 'black',
        'colline': 'black',
        'success': '#E1FFB5',
        'skip': '#C8D6FA',
        'abort': 'yellow',
        'error': 'red',
    }

async def draw(data: dict, alian: str, qid: int):
    content = []
    header = ["序号", "名字","配置","状态","结果"]
    result = data['result']
    for i, key in enumerate(data['order']):
        value = result[key]
        if value['log'] == "功能未启用":
            continue
        content.append([str(i), value['name'].strip(), value['config'].strip(), "#"+value['status'].strip(), value['log'].strip()])
    from .draw_table import grid2img
    from PIL import ImageFont 
    font_path = os.path.join(DATA, "微软雅黑.ttf")
    img = grid2img(content, header, colors=color(), font=ImageFont.truetype(font_path, size=30), stock=True)
    file = os.path.join(RESULT, f"{alian}_{str(qid)}.jpg")
    img.save(file, format='JPEG')
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
    import time
    st = time.time()
    asyncio.run(draw(json.loads(open("test.json" ,"r").read()), "test", 1))
    ed = time.time()
    print(ed - st)
