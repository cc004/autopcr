from collections import Counter, defaultdict
from typing import Any, Callable, Coroutine, Dict, List, Tuple, Union
from pathlib import Path
import math  
from .autopcr.model.custom import UnitAttribute 
from .autopcr.constants import DAILY_ORDER_KEY

from .autopcr.module.accountmgr import BATCHINFO, AccountBatch, TaskResultInfo
from .autopcr.module.modulebase import eResultStatus
from .autopcr.util.draw_table import outp_b64
from .autopcr.http_server.httpserver import HttpServer
from .autopcr.db.database import db
from .autopcr.module.accountmgr import Account, AccountManager, instance as usermgr
from .autopcr.db.dbstart import db_start
from .autopcr.util.draw import instance as drawer
from .autopcr.util.excel_export import export_excel
import asyncio, datetime

from io import BytesIO
from PIL import Image
import nonebot
from nonebot import on_startup
import hoshino
from hoshino import HoshinoBot, Service, priv, R
from hoshino.util import escape
from hoshino.typing import CQEvent
from quart_auth import QuartAuth
from quart_rate_limiter import RateLimiter
from quart_compress import Compress
import secrets
from .autopcr.util.pcr_data import get_id_from_name
import traceback
from .autopcr.util.logger import instance as logger
import os # 新增：用于获取进程端口信息
import re
import requests
import socket
from typing import Optional
import inspect  # 新增这一行
from hoshino import log  # 确保 log 模块已导入
logger = log.new_logger('auto_pcr')  # 初始化日志记录器
def get_public_ip() -> str:
    """获取服务器的公网IP（多重备选方案）"""
    # 备选公网IP查询API列表
    ip_apis = [
        "https://api.ipify.org?format=json",
        "https://ipinfo.io/json",
        "http://ip-api.com/json",
        "https://ifconfig.me/all.json",
    ]
    
    # 尝试所有可用的API
    for api_url in ip_apis:
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # 不同API返回的字段可能不同
                if "ip" in data:
                    return data["ip"]
                elif "ip_addr" in data:
                    return data["ip_addr"]
        except:
            continue  # 如果当前API失败，尝试下一个
    
    # 如果所有API都失败，尝试最后的手段（可能返回内网IP）
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip  # 警告：可能是内网IP
    except Exception as e:
        raise ValueError(f"所有公网IP获取方法均失败，请手动填写！最后错误: {str(e)}")



def get_hoshino_port() -> int:
    """获取当前运行的HoshinoBot实际使用的端口号"""
    try:
        # 尝试从HoshinoBot配置文件中获取端口
        from hoshino.config import __bot__ as bot_config
        port = bot_config.PORT
        print(f"ℹ️ 从HoshinoBot配置中获取到端口: {port}")
        return port
    except ImportError:
        print("⚠️ 无法导入hoshino.config.__bot__，尝试从进程获取端口")
    except AttributeError:
        print("⚠️ 配置中没有PORT属性，尝试从进程获取端口")
    
    # 如果从配置文件获取失败，回退到原来的进程检测方法
    try:
        # 获取当前进程ID
        current_pid = os.getpid()
        
        # 查找可能是HoshinoBot的Python进程
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'connections']):
            try:
                # 排除当前进程和非Python进程
                if proc.info['pid'] == current_pid or 'python' not in proc.info['name'].lower():
                    continue
                
                # 检查命令行参数是否包含hoshino相关字样
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'hoshino' not in cmdline.lower():
                    continue
                
                # 获取该进程监听的端口
                for conn in proc.info['connections'] or []:
                    if conn.status == 'LISTEN' and conn.laddr:
                        return conn.laddr.port
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except Exception as e:
        print(f"⚠️ 无法从进程获取端口，使用默认8040。错误: {e}")
    
    return 8040  # 默认端口

def generate_address() -> str:
    """生成 address，格式 '公网IP:端口'"""
    try:
        public_ip = get_public_ip()
        # 检查是否是明显的私有IP
        if public_ip.startswith(("10.", "172.", "192.168.")) or public_ip == "127.0.0.1":
            raise ValueError(f"获取到内网IP: {public_ip}，请检查网络配置！")
        
        port = get_hoshino_port()
        print(f"ℹ️ 检测到运行中HoshinoBot使用的端口: {port}")  # 添加调试信息
        return f"{public_ip}:{port}"
    except ValueError as e:
        print(f"❌ 错误: {e}")
        return "请手动填写公网IP:端口"  # 获取失败时的占位文本

# ===== 自动获取 address =====
address = generate_address()
print(f"ℹ️ 当前address: {address}")

# 如果获取失败，建议手动填写
if "手动填写" in address:
    print("请手动修改下方address变量为你的公网IP和端口！")

useHttps = False  # 默认HTTP

server = HttpServer(qq_mod=True)
app = nonebot.get_bot().server_app
QuartAuth(app, cookie_secure=False)
RateLimiter(app)
Compress(app)
app.secret_key = secrets.token_urlsafe(16)  # cookie expires when reboot
app.register_blueprint(server.app)
# 自动换防停止事件字典，key: sender_qq, value: asyncio.Event  
_auto_def_stop_events = {}

prefix = '#'

sv_help = f"""
- 清日常创建    一切的开始
- {prefix}配置日常  查地址
- {prefix}清日常 [昵称] 无昵称则默认账号
- {prefix}清日常所有 清该qq号下所有号的日常
指令格式： 命令 昵称 参数，下述省略昵称，<>表示必填，[]表示可选，|表示分割
- {prefix}日常记录 查看清日常状态
- {prefix}日常报告 [0|1|2|3] 最近四次清日常报告
- {prefix}定时日志 查看定时运行状态
- {prefix}查角色 [昵称] 查看角色练度
- {prefix}查缺角色 查看缺少的限定常驻角色
- {prefix}查ex装备 [会战] 查看ex装备库存
- {prefix}查探险编队 根据记忆碎片角色编队战力相当的队伍
- {prefix}查兑换角色碎片 [开换] 查询兑换特别角色的记忆碎片策略
- {prefix}查心碎 查询缺口心碎
- {prefix}查纯净碎片 查询缺口纯净碎片，国服六星+日服二专需求
- {prefix}查记忆碎片 [可刷取|大师币] 查询缺口记忆碎片，可按地图可刷取或大师币商店过滤
- {prefix}查装备 [<rank>] [fav] 查询缺口装备，rank为数字，只查询>=rank的角色缺口装备，fav表示只查询favorite的角色
- {prefix}刷图推荐 [<rank>] [fav] 查询缺口装备的刷图推荐，格式同上
- {prefix}公会支援 查询公会支援角色配置
- {prefix}卡池 查看当前卡池
- {prefix}半月刊
- {prefix}刷新box
- {prefix}查缺称号 查看缺少的称号
- {prefix}jjc透视 查前51名
- {prefix}pjjc透视 查前51名
- {prefix}jjc回刺 比如 #jjc回刺 19 2 就是打19 选择阵容2进攻
- {prefix}pjjc回刺 比如 #pjjc回刺 -1（或者不填） 就是打记录里第一条 
- {prefix}pjjc换防 将pjjc防守阵容随机错排
- {prefix}免费十连 <卡池id> 卡池id来自【{prefix}卡池】
- {prefix}来发十连 <卡池id> [抽到出] [单抽券|单抽] [编号小优先] [开抽] 赛博抽卡，谨慎使用。卡池id来自【{prefix}卡池】，[抽到出]表示抽到出货或达天井，默认十连，[单抽券]表示仅用厕纸，[单抽]表示宝石单抽，[标号小优先]指智能pickup时优先选择编号小的角色，[开抽]表示确认抽卡。已有up也可再次触发。
- {prefix}智能刷h图
- {prefix}智能刷外传
- {prefix}刷专二
- {prefix}查深域
- {prefix}强化ex装
- {prefix}合成ex装 
- {prefix}穿ex彩装 角色名 彩装ID  示例：#穿ex彩装 凯露 12345  #查ex装备 看ID
- {prefix}穿ex粉装 角色名 粉装serial_id    #查ID 看ID
- {prefix}穿ex金装 角色名 金装serial_id    #查ID 看ID
- {prefix}查ID 泪          ← 模糊匹配，会匹配所有名称含"泪"的装备
- {prefix}领小屋体力
- {prefix}公会点赞
- {prefix}领每日体力
- {prefix}领取礼物箱
- {prefix}查公会深域进度
- {prefix}收菜  探险续航哦
- {prefix}一键编队 1 1 [拉满] 队名1 星级角色1 星级角色2 ... 星级角色5 队名2 星级角色1 星级角色2 设置多队编队，一行一个队伍
- {prefix}导入编队 第几页 第几队  如 #导入编队 1 1  ，代表第一页第一队
- {prefix}识图   用于提取图中队伍
- {prefix}兑天井 卡池id 角色名 如 #兑天井 10283 火电  用 #卡池 获取ID  
- {prefix}拉角色练度 1 1 1 1 1 1 5 5 5 5 5 5 0 0 可可萝     #代表 等级 品级 ub s1 s2 ex 装备(左上到右下) 专武1 专武2 角色名（不输入则全选）
- {prefix}大富翁 [保留的骰子数量] [搬空商店为止|不止搬空商店] [到达次数]运行大富翁游戏，支持设置保留骰子数量和是否搬空商店后停止
  示例：{prefix}大富翁 30 不止搬空商店 0 | {prefix}大富翁所有 0 搬空商店为止  0（需要去批量运行里保存账号）
- {prefix}商店购买 [上期|当期] 购买大富翁商店物品，默认购买当期
  示例：{prefix}商店购买 上期 | {prefix}商店购买所有 当期 （需要去批量运行里保存账号）
- {prefix}查玩家 uid
- {prefix}炼金 物贯 物贯 物贯 物贯 1 彩装ID +(不输入是查ID/看概率/炼成)  炼成之前去网站设置参数《1代表属性总值，需要自己改》
- {prefix}撤下会战ex装
- {prefix}撤下普通ex装
- {prefix}买记忆碎片 可可萝 5 0 开买 界限突破  #分别代表:角色 星级 专武 是否购买 是否突破
- {prefix}角色升星 5 忽略盈余 升至最高 佩可  #分别代表 星级 是否保留盈余如突破碎片 升到可升最高星 角色名
- {prefix}角色突破 忽略盈余 凯露 佩可（忽略盈余：选这个，碎片不溢出就不突破）
- {prefix}pjjc自动换防   
- {prefix}挂地下城/会战/好友支援 [星级]角色1 [[星级]角色2]  设置角色为支援，星级可选(3/4/5)，如：#挂好友支援 3水电
- {prefix}一键穿ex +角色名 试穿/数字 1 2 3      数字0表示不改动    
- {prefix}添加好友
- {prefix}日常面板 [昵称] 查看日常功能开关及配置（图片版）  
- {prefix}日常详情 [昵称] 模块名 查看模块详细配置和可选值  
- {prefix}日常开启 [昵称] 模块名/序号 开启指定日常功能  
- {prefix}日常关闭 [昵称] 模块名/序号 关闭指定日常功能  
- {prefix}日常设置 [昵称] 模块序号 选项序号 值       设置模块子选项
- {prefix}定时面板 [昵称] 查看定时任务开关及时间  
- {prefix}定时详情 [昵称] 序号 查看定时任务详细配置和可选值  
- {prefix}定时开关 [昵称] 序号 切换定时任务开启/关闭  
- {prefix}定时设置 [昵称] 任务序号 选项序号 值   设置定时任务子选项
- {prefix}保存ex状态 保存当前所有角色的普通EX装备穿戴状态
- {prefix}恢复ex状态 恢复之前保存的普通EX装备穿戴状态
- {prefix}黎明界刷开局 公会名
- {prefix}清日常排序 5 1 3  (把1、3挪到5后面)
- {prefix}黎明界积分 查询黎明界累计积分/强化点数
- {prefix}我的支援 查询支援情况
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
    visible=True,  # False隐藏
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
    async def group_id(self) -> str: ...
    async def send_qq(self) -> str: ...
    async def message(self) -> List[str]: ...
    async def message_raw(self) -> str: ...
    async def image(self) -> List[str]: ...
    async def is_admin(self) -> bool: ...
    async def is_super_admin(self) -> bool: ...
    async def get_group_member_list(self) -> List: ...
    async def call_action(self, *args, **kwargs) -> Dict: ...

class HoshinoEvent(BotEvent):
    def __init__(self, bot: HoshinoBot, ev: CQEvent):
        self.bot = bot
        self.ev = ev

        self.user_id = str(ev.user_id)

        self.at_sb = []
        self._message = []
        self._raw_message = ""
        self._image = []
        for m in ev.message:
            if m.type == 'at' and m.data['qq'] != 'all':
                self.at_sb.append(str(m.data['qq']))
            elif m.type == 'text':
                text = m.data['text']
                self._raw_message += text
                self._message += text.split()
            elif m.type == 'image':
                self._image.append(m.data['url'])

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

    async def message_raw(self):
        return self._raw_message

    async def image(self):
        return self._image

    async def send(self, msg: str):
        msg = f"[CQ:reply,id={self.ev.message_id}]{msg}"
        await self.bot.send(self.ev, msg)

    async def finish(self, msg: str):
        await self.bot.finish(self.ev, msg)

    async def is_admin(self) -> bool:
        return priv.check_priv(self.ev, priv.ADMIN)

    async def is_super_admin(self) -> bool:
        return priv.check_priv(self.ev, priv.SU)

    async def group_id(self) -> str:
        return str(self.ev.group_id)

    async def call_action(self, action: str, **kwargs) -> Dict:
        return await self.bot.call_action(action, **kwargs)


def wrap_hoshino_event(func):
    async def wrapper(bot: HoshinoBot, ev: CQEvent, *args, **kwargs):
        await func(HoshinoEvent(bot, ev), *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

async def check_validate(botev: BotEvent, qq: str, cnt: int = 1):
    from .autopcr.http_server.validator import validate_dict
    for _ in range(360):
        if qq in validate_dict and validate_dict[qq]:
            validate = validate_dict[qq].pop()
            status = validate.status
            if status == "ok":
                del validate_dict[qq]
                cnt -= 1
                if not cnt: break
                continue

            url = validate.url
            url = address + url.lstrip("/daily/")
            
            msg=f"pcr账号登录需要验证码，请点击以下链接在120秒内完成认证:\n{url}"
            await botev.send(msg)

        else:
            await asyncio.sleep(1)

async def is_valid_qq(qq: str):
    qq = str(qq)
    enable_groups = await sv.get_enable_groups()
    bot = nonebot.get_bot()
    if qq.startswith("g"):
        gid = qq.lstrip('g')
        return gid.isdigit() and int(gid) in enable_groups.keys()
    else:
        for group_id, self_ids in enable_groups.items():
            for self_id in self_ids:
                try:
                    members = await bot.get_group_member_list(group_id=group_id, self_id=self_id)
                    for member in members:
                        if qq == str(member['user_id']):
                            return True
                    break
                except Exception as e:
                    continue
        return False

def check_final_args_be_empty(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        msg = await botev.message()
        if msg:
            await botev.finish("未知的参数：【" + " ".join(msg) + "】")
        await func(botev, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

async def get_folder_id(botev: BotEvent, folder_name: str) -> Union[str, None]:
    try:
        gid = await botev.group_id()
        resp = await botev.call_action('get_group_root_files', group_id=gid)
        folders = resp.get('folders', [])
        
        for folder in folders:
            if folder.get('folder_name') == folder_name:
                folder_id = folder.get('folder_id')
                return folder_id

        await botev.send(f"本群 {gid} 未找到「{folder_name}」，尝试创建...")
        create_resp = await botev.call_action(
            'create_group_file_folder',
            group_id=gid,
            folder_name=folder_name, # napcat
            name=folder_name # Lagrange
        )
        new_folder_id = create_resp.get('folder_id')
        if not new_folder_id:
            raise Exception("非管理员无法创建文件夹")
        return new_folder_id

    except Exception as e:
        await botev.send(f"获取或创建「{folder_name}」文件夹失败: {e}")
        return None

async def upload_excel(botev: BotEvent, data: BytesIO, filename: str, folder_name: str):  
    excel_R = R.get('autopcr', 'excel', filename)  
    path = Path(excel_R.path)  
    path.parent.mkdir(parents=True, exist_ok=True)  
      
    try:  
        with open(excel_R.path, 'wb') as f:  
            f.write(data.getbuffer())  
  
        gid = await botev.group_id()  
        folder_id = await get_folder_id(botev, folder_name)  
  
        upload_kwargs = {  
            'action': 'upload_group_file',  
            'group_id': gid,  
            'file': excel_R.path,  
            'name': filename  
        }  
        if folder_id:  
            upload_kwargs['folder'] = folder_id  
        else:  
            await botev.send(f"未能获取文件夹ID,上传到根目录")  
  
        await botev.call_action(**upload_kwargs)  
        sv.logger.info(f"✅ 上传成功: {filename}")  
          
        await asyncio.sleep(0.5)  
          
    finally:  
        if path.exists():  
            try:  
                path.unlink()  
                sv.logger.info(f"✅ 已删除临时文件: {path}")  
            except Exception as e:  
                sv.logger.error(f"❌ 删除临时文件失败: {path}, 错误: {e}")


from dataclasses import dataclass
@dataclass
class ToolInfo:
    name: str
    key: str
    config_parser: Callable[..., Coroutine[Any, Any, Any]]

tool_info: Dict[str, ToolInfo]= {}

def register_tool(name: str, key: str):
    def wrapper(func):
        tool_info[name] = ToolInfo(name=name, key=key, config_parser=func)
        async def inner(*args, **kwargs):
            await func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner
    return wrapper
    
# ===== 全局禁用指令功能 =====  
import json  
  
# 禁用列表持久化文件（跟随进程重启保留）  
_disabled_tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "disabled_tools.json")  
  
# 禁用/启用指令本身的名字，禁止被禁用（自我保护）  
DISABLE_CMD = "禁用"  
ENABLE_CMD = "启用"  
DISABLE_LIST_CMD = "禁用列表"  
  
def _load_disabled_tools() -> dict:  
    try:  
        with open(_disabled_tools_path, "r", encoding="utf-8") as f:  
            data = json.load(f)  
        # 兼容旧格式（list/set）：无留言，原因置空  
        if isinstance(data, list):  
            return {name: "" for name in data}  
        if isinstance(data, dict):  
            return {str(k): str(v) for k, v in data.items()}  
        return {}  
    except Exception:  
        return {}  
  
def _save_disabled_tools(d: dict):  
    try:  
        with open(_disabled_tools_path, "w", encoding="utf-8") as f:  
            json.dump(d, f, ensure_ascii=False)  
    except Exception as e:  
        logger.error(f"保存禁用列表失败: {e}")  
  
# 内存缓存，启动时加载一次：{功能名: 禁用原因}  
disabled_tools: dict = _load_disabled_tools() 

def wrap_accountmgr(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        target_qq = await botev.target_qq()
        sender_qq = await botev.send_qq()

        if sender_qq != target_qq and not await botev.is_admin():
            await botev.finish("只有管理员可以操作他人账号")

        if target_qq not in usermgr.qids():
            await botev.finish(f"未找到{target_qq}的账号，请在群里发送  清日常创建")

        async with usermgr.load(target_qq, readonly=True) as accmgr:
            await func(botev = botev, accmgr = accmgr, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_account(func):
    async def wrapper(botev: BotEvent, accmgr: AccountManager, *args, **kwargs):
        msg = await botev.message()

        alias = msg[0] if msg else ""
        all = False

        if alias == '所有':
            alias = BATCHINFO
            all = True
            del msg[0]
        elif alias == '批量':
            alias = BATCHINFO
            all = False
            del msg[0]
        elif alias not in accmgr.accounts():
            alias = accmgr.default_account
        else:
            del msg[0]

        if alias != BATCHINFO and len(list(accmgr.accounts())) == 1:
            alias = list(accmgr.accounts())[0]

        if alias != BATCHINFO and alias not in accmgr.accounts():
            if alias:
                await botev.finish(f"未找到昵称为【{alias}】的账号")
            else:
                await botev.finish(f"存在多账号且未找到默认账号，请指定昵称")

        async with accmgr.load(alias, force_use_all=all) as acc:
            await func(botev = botev, acc = acc, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_export(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        msg = await botev.message()
        command = msg[0] if msg else ""

        export = False
        if command.startswith("导出"):
            msg[0] = msg[0].lstrip("导出")
            export = True

        await func(botev = botev, export = export, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_group(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        msg = await botev.message()
        command = msg[0] if msg else ""

        if command.startswith("群"):
            if not await botev.is_admin():
                await botev.finish("仅管理员可以操作群帐号")
            async def new_qq():
                return "g" + str(await botev.group_id())
            botev.target_qq = new_qq
            msg[0] = msg[0].lstrip("群")

        await func(botev = botev, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def wrap_tool(func):  
    async def wrapper(botev: BotEvent, *args, **kwargs):  
        msg = await botev.message()  
        tool = msg[0] if msg else ""  
  
        for tool_name in tool_info:  
            if tool.startswith(tool_name):  
                tool = tool_name  
                msg[0] = msg[0].lstrip(tool_name)  
                if not msg[0]:  
                    del msg[0]  
                break  
        else:  
            await botev.finish(f"未找到工具【{tool}，请发送#帮助】")  
  
        # 禁用拦截：被管理员全局禁用的功能，直接返回提示（含留言原因）  
        if tool in disabled_tools:  
            reason = disabled_tools.get(tool, "")  
            if reason:  
                await botev.finish(f"功能【{tool}】已被管理员禁用\n原因：{reason}")  
            else:  
                await botev.finish(f"功能【{tool}】已被管理员禁用")
                
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

def require_super_admin(func):
    async def wrapper(botev: BotEvent, *args, **kwargs):
        if await botev.target_qq() != await botev.send_qq() and not await botev.is_super_admin():
            await botev.finish("仅超级管理员调用他人")
        else:
            return await func(botev = botev, *args, **kwargs)

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
            return await acc.do_daily(is_admin_call)

    for acc in accmgr.accounts():
        alias.append(escape(acc))
        task.append(loop.create_task(clean_daily_pre(acc)))

    try:
        alias_str = ','.join(alias)
        await botev.send(f"开始为{alias_str}清理日常")
    except Exception as e:  
        logger.exception(e)

    loop = asyncio.get_event_loop()
    loop.create_task(check_validate(botev, accmgr.qid, len(alias)))

    resps: List[TaskResultInfo] = await asyncio.gather(*task, return_exceptions=True)
    header = ["昵称", "清日常结果", "状态"]
    content = []
    for i, daily_result in enumerate(resps):
        if not isinstance(daily_result, Exception):
            content.append([alias[i], daily_result.get_result().get_last_result().log, "#" + daily_result.status.value])
        else:
            content.append([alias[i], str(daily_result), "#" + eResultStatus.ERROR.value])
    img = await drawer.draw(header, content)

    msg = outp_b64(img)
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

@sv.on_prefix(f"{prefix}禁用")  
@wrap_hoshino_event  
async def disable_tool(botev: BotEvent):  
    if not await botev.is_admin():  
        await botev.finish("仅管理员可以调用")  
  
    msg = await botev.message()  
    name = msg[0] if msg else ""  
    # 第一个参数之后的内容作为禁用留言原因  
    reason = " ".join(msg[1:]).strip() if len(msg) > 1 else ""  
  
    # #禁用列表 / #禁用（无参数）：查看当前禁用的功能及原因  
    if not name or name == "列表":  
        if disabled_tools:  
            lines = []  
            for t in sorted(disabled_tools):  
                r = disabled_tools[t]  
                lines.append(f"{t}（原因：{r}）" if r else t)  
            await botev.finish("当前已禁用的功能：\n" + "\n".join(lines))  
        else:  
            await botev.finish("当前没有被禁用的功能")  
  
    # 自我保护：禁止禁用本指令  
    if name in (DISABLE_CMD, ENABLE_CMD, DISABLE_LIST_CMD):  
        await botev.finish(f"不能禁用本指令【{name}】")  
  
    # 校验功能名是否存在  
    if name not in tool_info:  
        await botev.finish(f"未找到功能【{name}】，请发送#帮助查看功能名")  
  
    disabled_tools[name] = reason  
    _save_disabled_tools(disabled_tools)  
    if reason:  
        await botev.finish(f"已全局禁用功能【{name}】\n留言：{reason}")  
    else:  
        await botev.finish(f"已全局禁用功能【{name}】")
  
@sv.on_prefix(f"{prefix}启用")  
@wrap_hoshino_event  
async def enable_tool(botev: BotEvent):  
    if not await botev.is_admin():  
        await botev.finish("仅管理员可以调用")  
  
    msg = await botev.message()  
    name = msg[0] if msg else ""  
  
    if not name:  
        await botev.finish("请指定要启用的功能名，例如：#启用 清日常")  
  
    if name not in disabled_tools:  
        await botev.finish(f"功能【{name}】当前未被禁用")  
  
    disabled_tools.pop(name, None)  
    _save_disabled_tools(disabled_tools)  
    await botev.finish(f"已恢复功能【{name}】")

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
        logger.exception(e)

    try:
        is_admin_call = await botev.is_admin()

        loop = asyncio.get_event_loop()
        loop.create_task(check_validate(botev, acc.qq))

        res = await acc.do_daily(is_admin_call)
        resp = res.get_result()
        img = await drawer.draw_tasks_result(resp)
        msg = f"{alias}"
        msg += outp_b64(img)
        await botev.send(msg)
    except Exception as e:
        await botev.send(f'{alias}: {e}')

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
    img = await drawer.draw_tasks_result(resp, skip_skipped=True)
    await botev.finish(outp_b64(img))

@sv.on_prefix(f"{prefix}日常记录")
@wrap_hoshino_event
@wrap_accountmgr
async def clean_daily_time(botev: BotEvent, accmgr: AccountManager):
    content = []
    for alias in accmgr.accounts():
        async with accmgr.load(alias, readonly=True) as acc:
            content += [[acc.alias, daily_result.time, "#" + daily_result.status.value] for daily_result in acc.get_daily_result_list()]

    if not content:
        await botev.finish("暂无日常记录")
    header = ["昵称", "清日常时间", "状态"]
    img = outp_b64(await drawer.draw(header, content))
    await botev.finish(img)

@sv.on_prefix(f"{prefix}定时日志")
@wrap_hoshino_event
async def cron_log(botev: BotEvent):
    from .autopcr.module.crons import CRONLOG_PATH, CronLog
    with open(CRONLOG_PATH, 'r') as f:
        msg = []
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            try:
                msg.append(CronLog.from_json(line))
            except Exception:
                continue
    args = await botev.message()
    cur = datetime.datetime.now()
    if is_args_exist(args, '错误'):
        msg = [log for log in msg if log.status == eResultStatus.ERROR]
    if is_args_exist(args, '警告'):
        msg = [log for log in msg if log.status == eResultStatus.WARNING]
    if is_args_exist(args, '成功'):
        msg = [log for log in msg if log.status == eResultStatus.SUCCESS]
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
    from .autopcr.module.crons import CRONLOG_PATH, CronLog, eCronOperation
    with open(CRONLOG_PATH, 'r') as f:
        logs = [CronLog.from_json(line.strip()) for line in f.readlines()]
    cur = datetime.datetime.now()
    msg = await botev.message()
    if is_args_exist(msg, '昨日'):
        cur -= datetime.timedelta(days=1)
    start_logs = [log for log in logs if log.operation == eCronOperation.START and log.time.date() == cur.date()]
    finish_logs = [log for log in logs if log.operation == eCronOperation.FINISH and log.time.date() == cur.date()]
    status = Counter([log.status for log in finish_logs])
    msg = [f'今日定时任务：启动{len(start_logs)}个，完成{len(finish_logs)}个'] 
    msg += [f"{k.value}: {v}" for k, v in status.items()]
    # notice = [log for log in logs if log.status != eResultStatus.SUCCESS]
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


async def send_llonebot_forward(botev, alias: str, content: str):
    """
    LLOneBot专用合并转发函数（修正版，固定3段，每段34行）
    参数:
        botev: 事件对象
        alias: 显示名称
        content: 要发送的内容
    """
    try:
        # 1. 安全获取所有必要参数
        bot = getattr(botev, 'bot', None)
        if not bot:
            raise ValueError("无法获取bot实例")

        # 获取机器人ID（带默认值）
        bot_id = str(getattr(bot, 'self_id', '10000'))

        # 安全获取source_id（处理协程、方法和属性三种情况）
        async def safe_get_id(attr_name: str) -> int:
            attr = getattr(botev, attr_name, None)
            if attr is None:
                return None
            if inspect.iscoroutinefunction(attr):  # 协程函数
                try:
                    result = await attr()
                    return int(result)
                except Exception as e:
                    logger.error(f"获取{attr_name}失败(协程): {str(e)}")
                    return None
            elif callable(attr):  # 普通方法
                try:
                    return int(attr())
                except Exception as e:
                    logger.error(f"获取{attr_name}失败(方法): {str(e)}")
                    return None
            else:  # 普通属性
                try:
                    return int(attr)
                except Exception as e:
                    logger.error(f"获取{attr_name}失败(属性): {str(e)}")
                    return None

        # 优先尝试获取群号，失败则获取用户QQ号
        group_id = await safe_get_id('group_id')
        user_id = await safe_get_id('user_id')
        source_id = group_id or user_id
        if not source_id:
            raise ValueError("无法获取消息来源ID")

        message_type = "group" if group_id else "private"

        # 2. 分割内容为3段，每段34行
        lines = str(content).splitlines()
        total_lines = len(lines)
        chunk_size = 34  # 每段34行
        num_chunks = 3  # 分成3段

        # 计算实际分段（如果总行数不足，则按实际行数分割）
        messages = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = (i + 1) * chunk_size if (i + 1) * chunk_size <= total_lines else total_lines
            chunk = lines[start:end]
            if not chunk:  # 如果最后一段是空的，跳过
                continue
            messages.append({
                "type": "node",
                "data": {
                    "name": str(alias),
                    "uin": bot_id,
                    "content": "\n".join(chunk).strip()
                }
            })

        # 3. 发送消息
        if message_type == "group":
            await bot.send_group_forward_msg(
                group_id=int(source_id),
                messages=messages
            )
        else:
            for msg in messages:
                await bot.send_private_msg(
                    user_id=int(source_id),
                    message=msg["data"]["content"]
                )
                await asyncio.sleep(0.5)  # 防止消息速率限制
                
    except Exception as e:
        logger.error(f"合并转发失败: {str(e)}")
        # 降级为普通消息发送
        try:
            # 直接发送原始内容，分成3段
            lines = str(content).splitlines()
            total_lines = len(lines)
            chunk_size = 34
            num_chunks = 3

            for i in range(num_chunks):
                start = i * chunk_size
                end = (i + 1) * chunk_size if (i + 1) * chunk_size <= total_lines else total_lines
                chunk = lines[start:end]
                if not chunk:
                    continue
                await botev.send("\n".join(chunk).strip())
                await asyncio.sleep(0.5)
        except Exception as fallback_error:
            logger.error(f"降级发送也失败: {str(fallback_error)}")

def _get_daily_modules(acc: Account):  
    """获取已实现的日常模块列表（带序号），返回 [(idx, module), ...]"""  
    modules = acc.modules_list.get_modules_list('daily')  
    return [(i + 1, m) for i, m in enumerate(m for m in modules if m.implmented)]  
  
def _match_modules(targets: list, indexed_modules: list):  
    """  
    根据用户输入匹配模块，支持序号、精确name、精确key、模糊name。  
    返回 (success_list, failed_list)  
    """  
    # 建立索引  
    idx_map = {idx: m for idx, m in indexed_modules}  
    name_map = {}  
    key_map = {}  
    for idx, m in indexed_modules:  
        if m.name:  
            name_map[m.name] = (idx, m)  
        key_map[m.key] = (idx, m)  
  
    success = []  
    failed = []  
  
    for target in targets:  
        target = target.strip()  
        if not target:  
            continue  
  
        matched = None  
  
        # 1. 纯数字 -> 按序号  
        if target.isdigit():  
            num = int(target)  
            if num in idx_map:  
                matched = (num, idx_map[num])  
            else:  
                failed.append(f"{target}(序号不存在)")  
                continue  
        # 2. 精确匹配 key  
        elif target in key_map:  
            matched = key_map[target]  
        # 3. 精确匹配 name  
        elif target in name_map:  
            matched = name_map[target]  
        else:  
            # 4. 模糊匹配 name  
            fuzzy = [(idx, m) for idx, m in indexed_modules if m.name and target in m.name]  
            if len(fuzzy) == 1:  
                matched = fuzzy[0]  
            elif len(fuzzy) > 1:  
                names = ', '.join(f"{idx}.{m.name}" for idx, m in fuzzy)  
                failed.append(f"{target}(匹配多个: {names})")  
                continue  
            else:  
                failed.append(f"{target}(未找到)")  
                continue  
  
        success.append(matched)  
  
    return success, failed  

@sv.on_prefix(f"{prefix}")
@wrap_hoshino_event
@wrap_export  # 确保该装饰器会注入export参数
@wrap_group
@wrap_tool
@wrap_accountmgr
@wrap_account
@wrap_config
@check_final_args_be_empty
async def tool_used(botev: CQEvent, tool, config: Dict[str, str], acc, export: bool = False):  # 增加export参数
    """
    任务执行主函数
    参数:
        botev: CQEvent事件对象
        tool: 工具对象
        config: 配置字典
        acc: 账号对象
        export: 是否导出为Excel（由装饰器注入）
    """
    alias = getattr(acc, 'alias', '未知账号')
    try:
        # 原有逻辑（任务执行）
        loop = asyncio.get_event_loop()
        loop.create_task(check_validate(botev, getattr(acc, 'qq', '')))
        
        is_admin_call = await botev.is_admin()
        resp = await acc.do_from_key(config, getattr(tool, 'key', ''), is_admin_call)
        if isinstance(resp, List):
            resp = resp[0]
        resp = resp.get_result()
        
        # 处理导出逻辑
        if export:
            # 导出为Excel
            data = await export_excel(resp.table)
            timestamp = db.format_time_safe(datetime.datetime.now())
            await upload_excel(botev, data, f"{tool.name}_{alias}_{timestamp}.xlsx", 'autopcr')
        else:
            # 仅对查公会深域进度工具生成图片
            if tool.key in ["find_clan_talent_quest", "get_box_table", "search_unit", "find_talent_quest", "one_click_ex_equip", "labyrinth_point_query", "get_my_support"]:
                # 生成深域进度图片
                img = await drawer.draw_task_result(resp)
                msg = f"{alias}"
                msg += outp_b64(img)
                await botev.send(msg)
            else:
                # 其他工具保持原有文本处理逻辑
                result_text = str(resp.log) if hasattr(resp, 'log') else str(resp)
                result_text = result_text.replace('\\n', '\n').replace('\n', '\n')
                await send_llonebot_forward(botev, alias, result_text)

    except Exception as e:
        error_msg = f"{alias} 任务执行失败（如果是指令+所有必须去网站-批量运行-BATCH_RUNNER 里保存队伍）：{str(e)[:500]}"
        try:
            await botev.send(error_msg)
        except:
            logger.error("发送错误消息失败")

@sv.on_fullmatch(f"{prefix}卡池")
@wrap_hoshino_event
async def gacha_current(botev: BotEvent):
    msg = '\n'.join(db.get_mirai_gacha())
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    await botev.finish(msg)

def is_args_exist(msg: List[str], key: str):
    if key in msg:
        msg.remove(key)
        return True
    return False

def recover_text_by_tokens(raw_text: str, tokens: List[str]) -> str:
    if not tokens:
        return ""
    pattern = r"\s+".join(re.escape(token) for token in tokens)
    match = re.search(pattern, raw_text, flags=re.S)
    if match:
        return raw_text[match.start():match.end()]
    return " ".join(tokens)

@register_tool("公会支援", 'get_clan_support_unit')
async def clan_support(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("查心碎", "get_need_xinsui")
async def find_xinsui(botev: BotEvent):
    return {}

@register_tool("jjc回刺", "jjc_back")
async def jjc_back(botev: BotEvent):
    msg = await botev.message()
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    opponent_jjc_rank = -1
    opponent_jjc_attack_team_id = 1
    try:
        opponent_jjc_rank = int(msg[0])
        del msg[0]
    except:
        pass
    try:
        opponent_jjc_attack_team_id = int(msg[0])
        del msg[0]
    except:
        pass
    config = {
        "opponent_jjc_rank": opponent_jjc_rank,
        "opponent_jjc_attack_team_id": opponent_jjc_attack_team_id,
    }
    return config
    
@register_tool("一键编队", "set_my_party2")
async def set_my_party_multi(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    raw_msg = await botev.message_raw()
    msg = await botev.message()
    party_start_num = 1
    tab_start_num = 1
    is_to_max = False
    try:
        tab_start_num = int(msg[0])
        del msg[0]
    except:
        pass
    try:
        party_start_num = int(msg[0])
        del msg[0]
    except:
        pass
    try:
        is_to_max = is_args_exist(msg, '拉满')
    except:
        pass

    teams_text = recover_text_by_tokens(raw_msg, msg)
    config = {
        "tab_start_num2": tab_start_num,
        "party_start_num2": party_start_num,
        "set_my_party_text2": teams_text,
        "set_my_party2_to_max": is_to_max,
    }
    del msg[:]
    return config

 
@register_tool("导入编队", "set_my_party")
async def set_my_party(botev: BotEvent):
    msg = await botev.message()
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    party_start_num = 1
    tab_start_num = 1
    try:
        tab_start_num = int(msg[0])
        del msg[0]
    except:
        pass
    try:
        party_start_num = int(msg[0])
        del msg[0]
    except:
        pass
    units = []
    unknown_units = []
    for _ in range(5):
        try:
            unit_name = msg[0]
            unit = get_id_from_name(unit_name)
            if unit:
                units.append(unit)
            else:
                unknown_units.append(unit_name)
            del msg[0]
        except:
            pass
    if unknown_units:
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")
    config = {
        "tab_start_num": tab_start_num,
        "party_start_num": party_start_num,
    }
    return config

async def get_pic(address: str):
    return await (await aiorequests.get(address, timeout=6)).content

@sv.on_prefix(f"{prefix}识图")
@wrap_hoshino_event
async def ocr_team(botev: BotEvent):
    try:
        from hoshino.modules.priconne.arena import getBox, get_pic
    except ImportError:
        try:
            from hoshino.modules.priconne.arena.old_main import getBox, get_pic
        except ImportError:
            await botev.finish("未安装怎么拆截图版，无法使用识图")
            return

    msg = await botev.message()  
    team_label = "队伍"  
    if msg:  
        team_label = msg[0]  
  
    img_urls = await botev.image()  
    if not img_urls:  
        await botev.finish("未识别到图片!")

    result = []
    for id, img_url in enumerate(img_urls):
        try:
            image = Image.open(BytesIO(await get_pic(img_url)))
        except Exception as e:
            await botev.send(f"图片{id+1}下载失败: {e}")
            continue
        box, s = await getBox(image)
        await botev.send(f"图片{id+1}识别结果: {s}")
        if not box:
            await botev.send(f"图片{id+1}未识别到任何队伍！")
            continue
        result += box

    if not result:
        await botev.finish("未识别到任何队伍！")

    msg = f"{prefix}一键编队 4 1\n" + "\n".join(
            f"{team_label}{id+1} {' '.join(db.get_unit_name(uid * 100 + 1) for uid in team)}"
            for id, team in enumerate(result)
    )
    await botev.finish(msg)

@register_tool("pjjc回刺", "pjjc_back")
async def pjjc_back(botev: BotEvent):
    msg = await botev.message()
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    opponent_pjjc_rank = -1
    opponent_pjjc_attack_team_id = 1
    try:
        opponent_pjjc_rank = int(msg[0])
        del msg[0]
    except:
        pass
    try:
        opponent_pjjc_attack_team_id = int(msg[0])
        del msg[0]
    except:
        pass
    config = {
        "opponent_pjjc_rank": opponent_pjjc_rank,
        "opponent_pjjc_attack_team_id": opponent_pjjc_attack_team_id,
    }
    return config

@register_tool("jjc透视", "jjc_info")
async def jjc_info(botev: BotEvent):
    use_cache = True
    msg = await botev.message()
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
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
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
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
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
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

@register_tool("查纯净碎片", "get_need_pure_memory")
async def find_pure_memory(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("查sp碎片", "get_need_sp_memory")
async def find_sp_memory(botev: BotEvent):
    return {}

@register_tool("返钻", "return_jewel")
async def return_jewel(botev: BotEvent):
    return {}

@register_tool(f"来发十连", "gacha_start")
@require_super_admin
async def shilian(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    cc_until_get = False
    pool_id = ""
    really_do = False
    single_ticket = False
    single = False
    small_first = False
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
        single_ticket = is_args_exist(msg, '单抽券')
    except:
        pass

    try:
        single = is_args_exist(msg, '单抽')
    except:
        pass

    try:
        small_first = is_args_exist(msg, '编号小优先')
    except:
        pass

    current_gacha = {gacha.split(':')[0]: gacha for gacha in db.get_cur_gacha()}

    if pool_id not in current_gacha:
        await botev.finish(f"未找到该卡池{pool_id}")

    pool_id = current_gacha[pool_id]

    if single_ticket and single:
        await botev.finish("单抽券和单抽只能选一个")

    gacha_method = "十连"
    if single_ticket:
        gacha_method = "单抽券"
    elif single:
        gacha_method = "单抽"

    if not really_do:
        msg = f"卡池{pool_id}\n"
        if cc_until_get:
            msg += "抽到出\n"
        if small_first:
            msg += "编号小优先\n"
        msg += f"{gacha_method}\n"
        msg += "确认无误，消息末尾加上【开抽】即可开始抽卡"
        await botev.finish(msg)

    config = {
        "pool_id": pool_id,
        "cc_until_get": cc_until_get,
        "gacha_method": gacha_method,
        "gacha_start_auto_select_pickup_min_first": small_first,
    }
    return config

@register_tool(f"查装备", "get_need_equip")
async def find_equip(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
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
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
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


@register_tool("pjjc换防", "pjjc_def_shuffle_team")
async def pjjc_def_shuffle_team(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("pjjc换攻", "pjjc_atk_shuffle_team")
async def pjjc_atk_shuffle_team(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}
    
@register_tool("查玩家", "query_player_profile")
async def query_player_profile(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    msg = await botev.message()
    target_viewer_id = ""
    try:
        target_viewer_id = msg[0]
        del msg[0]
    except:
        await botev.finish("请输入玩家ID")
    
    if not target_viewer_id.isdigit():
        await botev.finish("玩家ID必须是数字")
    
    config = {
        "target_viewer_id": target_viewer_id
    }
    return config
    
@register_tool("查缺角色", "missing_unit")
async def find_missing_unit(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("查缺称号", "missing_emblem")
async def find_missing_emblem(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("合成ex装", "ex_equip_rank_up")  
async def ex_equip_rank_up(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
      
    # 解析装备种类参数  
    kinds = []  
    available_kinds = ['粉', '会战金', '普通金', '会战银']  
      
    for kind in available_kinds:  
        if kind in msg:  
            kinds.append(kind)  
            msg.remove(kind)  
      
    # 如果没有指定种类，默认全部  
    if not kinds:  
        kinds = available_kinds  
      
    return {"ex_equip_rank_up_kind": kinds}

@register_tool("强化ex装", "ex_equip_enhance_up")  
async def ex_equip_enhance_up(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
      
    # 解析装备种类参数  
    kinds = []  
    available_kinds = ['粉', '会战金', '普通金', '会战银']  
      
    for kind in available_kinds:  
        if kind in msg:  
            kinds.append(kind)  
            msg.remove(kind)  
      
    # 如果没有指定种类，默认全部  
    if not kinds:  
        kinds = available_kinds  
      
    return {"ex_equip_enhance_up_kind": kinds}
@register_tool("查角色", "search_unit")
async def search_unit(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    msg = await botev.message()
    unit = None
    unit_name = ""
    try:
        unit_name = msg[0]
        unit = get_id_from_name(unit_name)
        del msg[0]
    except:
        pass

    if unit:
        unit = unit * 100 + 1;
        return {
            "search_unit_id": unit
        }
    else:
        await botev.finish(f"未知昵称{unit_name}")

@register_tool("刷新box", "refresh_box")
async def refresh_box(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("我的支援", "get_my_support")
async def refresh_box(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("查探险编队", "travel_team_view")
async def find_travel_team_view(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("查ex装备", "ex_equip_info")
async def ex_equip_info(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    ex_equip_info_cb_only = False
    msg = await botev.message()
    try:
        ex_equip_info_cb_only = is_args_exist(msg, '会战')
    except:
        pass
    config = {
        "ex_equip_info_cb_only": ex_equip_info_cb_only
    }
    return config

@register_tool("查兑换角色碎片", "redeem_unit_swap")
async def redeem_unit_swap(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    really_do = False
    msg = await botev.message()
    try:
        really_do = is_args_exist(msg, '开换')
    except:
        pass
    config = {
        "redeem_unit_swap_do": really_do
    }
    return config

@register_tool("查公会深域进度", "find_clan_talent_quest")
async def find_clan_talent_quest(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}


@register_tool("兑天井", "gacha_exchange_chara")
async def gacha_exchange_chara(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    msg = await botev.message()
    gacha_id = ""
    unit_name = ""
    try:
        gacha_id = msg[0]
        del msg[0]
    except:
        pass
    try:
        unit_name = msg[0]
        del msg[0]
    except:
        pass

    current_gacha = {gacha.split(':')[0]: gacha for gacha in db.get_cur_gacha()}

    if gacha_id not in current_gacha:
        await botev.finish(f"未找到该卡池{gacha_id}")

    unit = get_id_from_name(unit_name)
    if not unit:
        await botev.finish(f"未知角色名{unit_name}")

    config = {  
        "gacha_exchange_pool_id": current_gacha[gacha_id],  
        "gacha_exchange_unit_id": unit * 100 + 1
    }
    return config

@sv.on_fullmatch(f"{prefix}半月刊")  
@wrap_hoshino_event  
async def half_schedule_standalone(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    import importlib  
    mod = importlib.import_module('.autopcr.module.modules.nologin', __package__)  
    HalfScheduleModule = mod.half_schedule  
  
    def fmt_time(t):  
        return db.parse_time(t).strftime("%Y/%m/%d %H:%M")  
  
    def abbrev_campaign(desc: str) -> str:  
        MAP = {  
            "vh": "VH",  
            "normal": "N",  
            "hard": "H",  
            "normal&hard": "NH",  
            "圣迹": "圣迹",  
            "神殿": "神殿",  
            "探索": "探索",  
        }  
        pattern = r'^(' + '|'.join(re.escape(k) for k in MAP) + r') 掉落\*(\d+(?:\.\d+)?)$'  
        m = re.match(pattern, desc)  
        if m:  
            pfx = MAP[m.group(1)]  
            mult = float(m.group(2))  
            mult_str = str(int(mult)) if mult == int(mult) else str(mult)  
            return f"{pfx}{mult_str}"  
        return desc  
  
    FILTER_KEYWORDS = ["*2.0", "玩家经验", "活动normal", "活动hard", "mana"]  
  
    schedules_data = defaultdict(list)  
    for table, factory in HalfScheduleModule.schedules:  
        for row in table.values():  
            schedule = factory(row)  
            if schedule.enabled:  
                desc = schedule.get_description()  
                if any(kw in desc for kw in FILTER_KEYWORDS):  
                    continue  
                desc = abbrev_campaign(desc)  
                if desc.startswith("免费十连"):  
                    desc = "免费十连"  
                key = (fmt_time(schedule.start_time), fmt_time(schedule.end_time))  
                schedules_data[key].append(desc)  
  
    master_coin_pattern = re.compile(r'^.+ 大师币\*(\d+(?:\.\d+)?)$')  
    for key in schedules_data:  
        msgs = schedules_data[key]  
        master_coin_mult = None  
        new_msgs = []  
        for msg in msgs:  
            mc = master_coin_pattern.match(msg)  
            if mc:  
                master_coin_mult = float(mc.group(1))  
            else:  
                new_msgs.append(msg)  
        if master_coin_mult is not None:  
            mult_str = str(int(master_coin_mult)) if master_coin_mult == int(master_coin_mult) else str(master_coin_mult)  
            new_msgs.append(f"大师币{mult_str}")  
        schedules_data[key] = new_msgs  
  
    times = sorted(schedules_data.keys())  
    lines = []  
    mirai = False  
    for time in times:  
        st = time[0]  
        ed = time[1]  
        if not mirai and db.parse_time(st) > datetime.datetime.now():  
            mirai = True  
            lines.append("\n====未来日程====")  
        lines.append(f"{st} - {ed}")  
        for msg in schedules_data[time]:  
            lines.append(f"    {msg}")  
    await send_llonebot_forward(botev, "半月刊", '\n'.join(lines))

@register_tool("查box", "get_box_table")
async def get_box_table(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    msg = await botev.message()
    box_all_unit = False
    try:
        box_all_unit = is_args_exist(msg, '所有')
    except:
        pass

    known_units = []
    unknown_units = []
    while msg:
        unit_name = msg[0]
        unit = get_id_from_name(unit_name)
        if unit:
            known_units.append(unit * 100 + 1)
        else:
            unknown_units.append(unit_name)
        del msg[0]
    if unknown_units:
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")

    if not known_units and not box_all_unit:
        await botev.finish("请指定角色或添加【所有】参数")

    return {
        'box_unit': known_units,
        'box_all_unit': box_all_unit
    }
    
@register_tool("免费十连", "free_gacha")
async def free_gacha(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    msg = await botev.message()
    gacha_id_input = 0  
    try:  
        gacha_id_input = int(msg[0])  
        del msg[0]  
    except:  
        pass  
      
    # 匹配带名字的候选项  
    candidates = db.free_gacha_ids_candidate()  
    matched = [c for c in candidates if int(str(c).split(':')[0]) == gacha_id_input]  
    gacha_id = matched[0] if matched else str(gacha_id_input)  
      
    config = {  
        "free_gacha_select_ids": [gacha_id],  
        "today_end_gacha_no_do": False,  
    }
    return config

# @register_tool("智能刷n图", "smart_normal_sweep")
# async def smart_normal_swee(botev: BotEvent):
    # await botev.send("请稍等1-8分钟，过整点需要重新发送")
    # msg = await botev.message()
    # config = {
        # "normal_sweep_strategy": "刷最缺",
        # "normal_sweep_quest_scope": "全部",
        # "normal_sweep_consider_unit": "所有",
        # "normal_sweep_consider_unit_fav": True,
        # "normal_sweep_equip_ok_to_full": True
    # }
    
    # try:
        # if is_args_exist(msg, '新开图'):
            # normal_sweep_quest_scope = '新开图'
        # elif is_args_exist(msg, '可扫荡'):
            # normal_sweep_quest_scope = '可扫荡'
    # except:
        # pass
    # config = {
        # "normal_sweep_quest_scope": normal_sweep_quest_scope,
        # "normal_sweep_consider_unit_fav": True,
        # "normal_sweep_equip_ok_to_full": True,
    # }
    # return config
    
@register_tool("智能刷h图", "smart_hard_sweep")
async def smart_hard_sweep(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("领取礼物箱", "present_receive")
async def present_receive(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("智能刷外传", "smart_shiori_sweep")
async def smart_shiori_sweep(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}  

@register_tool("刷专二", "mirai_very_hard_sweep")
async def mirai_very_hard_sweep(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}    

@register_tool("领小屋体力", "room_accept_all")
async def room_accept_all(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}  

@register_tool("公会点赞", "clan_like")
async def clan_like(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}  

@register_tool("领每日体力", "mission_receive_first")
async def mission_receive_first(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}  

@register_tool("收菜", "travel_quest_sweep")
async def travel_quest_sweep(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}

@register_tool("查深域", "find_talent_quest")
async def find_talent_quest(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}
    
@register_tool("查刀数", "clan_battle_knive")
async def clan_battle_knive(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}
    

@register_tool("拉角色练度", "unit_promote")
async def unit_promote(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
  
    config = {  
        "unit_promote_level_when_fail_to_equip_or_skill": False,  
        "unit_promote_rank_when_fail_to_unique_equip": False,  
        "unit_promote_rank_use_raw_ore": False,  
        "unit_promote_unique2_when_fail_to_unique_equip2": False,  
        "unit_promote_to_max_level": False,  
        "unit_promote_level": 1,  
        "unit_promote_rank": 1,  
        "unit_promote_skill_ub": 1,  
        "unit_promote_skill_s1": 1,  
        "unit_promote_skill_s2": 1,  
        "unit_promote_skill_ex": 1,  
        "unit_promote_unique_equip1_level": 0,  
        "unit_promote_unique_equip2_level": 0,  
        "unit_promote_equip_0": -1,  
        "unit_promote_equip_1": -1,  
        "unit_promote_equip_2": -1,  
        "unit_promote_equip_3": -1,  
        "unit_promote_equip_4": -1,  
        "unit_promote_equip_5": -1,  
        "unit_promote_units": []  
    }  
  
    # 先解析布尔关键词参数（会从msg中移除匹配项）  
    config["unit_promote_level_when_fail_to_equip_or_skill"] = is_args_exist(msg, '自动拉等级')  
    config["unit_promote_rank_when_fail_to_unique_equip"] = is_args_exist(msg, '自动拉品级')  
    config["unit_promote_rank_use_raw_ore"] = is_args_exist(msg, '使用原矿')  
    config["unit_promote_unique2_when_fail_to_unique_equip2"] = is_args_exist(msg, '自动专武1')  
    config["unit_promote_to_max_level"] = is_args_exist(msg, '等级升至上限')  
  
    # 按顺序解析数值参数：等级 品级 ub s1 s2 ex  
    try:  
        config["unit_promote_level"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        config["unit_promote_rank"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        config["unit_promote_skill_ub"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        config["unit_promote_skill_s1"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        config["unit_promote_skill_s2"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        config["unit_promote_skill_ex"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
  
    # 解析6个装备星级（左上到右下）  
    equip_slots = ["unit_promote_equip_0", "unit_promote_equip_1",  
                   "unit_promote_equip_2", "unit_promote_equip_3",  
                   "unit_promote_equip_4", "unit_promote_equip_5"]  
    for slot in equip_slots:  
        try:  
            val = int(msg[0])  
            if val in [-1, 0, 1, 2, 3, 4, 5]:  
                config[slot] = val  
            del msg[0]  
        except:  
            pass  
  
    # 专武1等级  
    try:  
        config["unit_promote_unique_equip1_level"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
  
    # 专武2等级  
    try:  
        config["unit_promote_unique_equip2_level"] = int(msg[0])  
        del msg[0]  
    except:  
        pass  
  
    # 角色列表  
    unknown_units = []  
    while msg:  
        try:  
            unit_name = msg[0]  
            unit = get_id_from_name(unit_name)  
            if unit:  
                config["unit_promote_units"].append(unit * 100 + 1)  
            else:  
                unknown_units.append(unit_name)  
            del msg[0]  
        except:  
            break  
  
    # 错误处理  
    if unknown_units:  
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")  
    if not config["unit_promote_units"]:  
        config["unit_promote_units"] = list(range(100101, 199901, 100))  
  
    return config

@register_tool("大富翁", "caravan_play")
async def caravan_play(botev: BotEvent):
    msg = await botev.message()
    # 发送任务正在进行提示
    await botev.send("好的，马上进行大富翁任务")
    # 默认配置：保留0个骰子，搬空商店为止，到达终点次数0
    config = {
        "caravan_play_dice_hold_num": 0,
        "caravan_play_until_shop_empty": False,
        "caravan_play_goal_num": 0
    }
    
    try:
        # 解析参数（按顺序：保留骰子数量 -> 商店设置 -> 到达终点次数）
        # 解析保留骰子数量
        if msg and msg[0].isdigit():
            config["caravan_play_dice_hold_num"] = int(msg[0])
            msg.pop(0)
        
        # 解析是否搬空商店
        if msg and msg[0] in ["搬空商店为止", "不止搬空商店"]:
            config["caravan_play_until_shop_empty"] = (msg[0] == "搬空商店为止")
            msg.pop(0)
        
        # 解析到达终点次数（第三个参数）
        if msg and msg[0].isdigit():
            config["caravan_play_goal_num"] = int(msg[0])
            msg.pop(0)
    
    except Exception as e:
        logger.warning(f"解析大富翁参数出错: {e}")
    
    # 检查未识别参数
    if msg:
        await botev.finish(f"未知的参数：【{' '.join(msg)}】")
    
    return config


@register_tool("商店购买", "caravan_shop_buy")
async def caravan_shop_buy(botev: BotEvent):
    msg = await botev.message()
    # 发送任务正在进行提示
    await botev.send("购买中，请稍等1-8分钟，过整点需要重新发送")
    # 默认配置：购买当期商店
    config = {
        "caravan_shop_last_season": False
    }
    
    try:
        # 解析购买上期/当期商店（直接提取关键词）
        if is_args_exist(msg, "上期"):
            config["caravan_shop_last_season"] = True
        elif is_args_exist(msg, "当期"):
            config["caravan_shop_last_season"] = False
    except Exception as e:
        logger.warning(f"解析大富翁商店购买参数出错: {e}")
    
    # 检查未识别参数
    if msg:
        await botev.finish(f"未知的参数：【{' '.join(msg)}】")
    
    return config

@register_tool("炼金", "ex_equip_rainbow_enchance")      
async def ex_equip_rainbow_enchance_tool(botev: BotEvent):      
    await botev.send("请稍等1-8分钟，过整点需要重新发送")      
    msg = await botev.message()  
      
    # 先解析操作类型关键词(会从msg中移除)  
    operation = "看属性"      
    if is_args_exist(msg, '炼成'):      
        operation = "炼成"      
    elif is_args_exist(msg, '看概率'):      
        operation = "看概率"  
      
    # Create reverse mapping    
    ch2index = {v: k for k, v in UnitAttribute.index2ch.items()}    
    ch2index["任意"] = 0    
        
    # Parse 4 attribute parameters    
    attributes = []    
    for i in range(4):    
        try:    
            attr_name = msg[0]    
            del msg[0]    
            if attr_name in ch2index:    
                attributes.append(ch2index[attr_name])    
            else:    
                await botev.finish(f"未知属性名: {attr_name}")    
        except:    
            await botev.finish(f"请输入第{i+1}个属性参数")    
        
    # Parse target sum integer    
    target_sum = 0    
    try:    
        target_sum = int(msg[0])    
        del msg[0]    
    except:    
        pass  # Optional parameter    
      
    # Parse 彩装ID (保持为字符串!)  
    equip_id = ""  
    try:    
        equip_id = msg[0]  # 不要用 int(),保持字符串  
        del msg[0]    
    except:    
        pass  
          
    config = {    
        "ex_equip_rainbow_enchance_sub_status_1": attributes[0],    
        "ex_equip_rainbow_enchance_sub_status_2": attributes[1],    
        "ex_equip_rainbow_enchance_sub_status_3": attributes[2],    
        "ex_equip_rainbow_enchance_sub_status_4": attributes[3],    
        "ex_equip_rainbow_enchance_target_sum": target_sum,    
        "ex_equip_rainbow_enchance_id": equip_id,  # 字符串形式  
        "ex_equip_rainbow_enchance_action": operation      
    }      
    return config
  
@register_tool("撤下会战ex装", "remove_cb_ex_equip")
async def remove_cb_ex_equip(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}
  
@register_tool("撤下普通ex装", "remove_normal_ex_equip")
async def remove_normal_ex_equip(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")
    return {}  

@register_tool("买记忆碎片", "unit_memory_buy")  
async def buy_unit_memory(botev: BotEvent):  
    msg = await botev.message()  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
  
    # 解析角色名  
    unit_name = ""  
    unit_id = None  
    try:  
        unit_name = msg[0]  
        unit_id = get_id_from_name(unit_name)  
        del msg[0]  
    except:  
        pass  
  
    if not unit_id:  
        await botev.finish(f"未知昵称{unit_name}，请指定角色")  
  
    unit_id = unit_id * 100 + 1  
  
    # 解析星级（默认6）  
    star = 6  
    try:  
        star = int(msg[0])  
        del msg[0]  
    except:  
        pass  
  
    # 解析专武等级（默认0）  
    unique_level = 0  
    try:  
        unique_level = int(msg[0])  
        del msg[0]  
    except:  
        pass  
  
    # 解析开关参数  
    do_buy = is_args_exist(msg, '开买')  
    exceed_state = is_args_exist(msg, '界限突破')  
  
    config = {  
        "unit_memory_buy_unit": unit_id,  
        "unit_memory_unit_star": star,  
        "unit_memory_unique_equip_level": unique_level,  
        "unit_memory_unit_exceed_state": exceed_state,  
        "unit_memory_do_buy": do_buy,  
    }  
    return config
    
@register_tool("角色升星", "unit_evolution")  
async def unit_evolution_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
  
    # 解析目标星级（默认5）  
    target_rarity = 5  
    try:  
        val = int(msg[0])  
        if val in range(2, 6):  
            target_rarity = val  
            del msg[0]  
    except:  
        pass  
  
    # 解析开关参数  
    to_max_rarity = is_args_exist(msg, '升至最高')  
    ignore_memory = is_args_exist(msg, '忽略盈余')  
  
    # 解析角色列表  
    units = []  
    unknown_units = []  
    while msg:  
        unit_name = msg[0]  
        unit = get_id_from_name(unit_name)  
        if unit:  
            units.append(unit * 100 + 1)  
        else:  
            unknown_units.append(unit_name)  
        del msg[0]  
  
    if unknown_units:  
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")  
  
    if not units:  
        await botev.finish("请指定角色")  
  
    return {  
        "unit_evolution_units": units,  
        "unit_evolution_to_rarity": target_rarity,  
        "unit_evolution_to_max_rarity": to_max_rarity,  
        "unit_evolution_ignore_memory": ignore_memory,  
    }   

@register_tool("角色突破", "unit_exceed")  
async def unit_exceed_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
  
    # 解析保留Mana下限（亿），默认10  
    mana_keep = 10  
    try:  
        val = int(msg[0])  
        mana_keep = val  
        del msg[0]  
    except:  
        pass  
  
    # 解析开关参数  
    ignore_memory = is_args_exist(msg, '忽略盈余')  
  
    # 解析角色列表  
    units = []  
    unknown_units = []  
    while msg:  
        unit_name = msg[0]  
        unit = get_id_from_name(unit_name)  
        if unit:  
            units.append(unit * 100 + 1)  
        else:  
            unknown_units.append(unit_name)  
        del msg[0]  
  
    if unknown_units:  
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")  
  
    if not units:  
        await botev.finish("请指定角色")  
  
    return {  
        "unit_exceed_units": units,  
        "unit_exceed_ignore_memory": ignore_memory,  
        "unit_exceed_mana_keep": mana_keep,  
    }   
    


@register_tool("挂会战支援", "set_cb_support")    
async def set_cb_support(botev: BotEvent):    
    msg = await botev.message()    
    await botev.send("请稍等1-8分钟，过整点需要重新发送")    
  
    units = []    
    stars = []    
    unknown_units = []    
    for _ in range(2):    
        try:    
            unit_name = msg[0]    
            unit = get_id_from_name(unit_name)    
            if unit:    
                units.append(unit * 100 + 1)    
                stars.append(0)    
            else:    
                if unit_name[0].isdigit():    
                    star = int(unit_name[0])    
                    unit = get_id_from_name(unit_name[1:])    
                    if unit:    
                        units.append(unit * 100 + 1)    
                        stars.append(star)    
                    else:    
                        unknown_units.append(unit_name)    
                else:    
                    unknown_units.append(unit_name)    
            del msg[0]    
        except:    
            break    
  
    if unknown_units:    
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")    
  
    if not units:    
        await botev.finish("请指定至少一个角色，如：#挂会战支援 角色1 角色2")    
  
    config = {    
        "set_cb_support_unit_id_1": units[0],    
        "set_cb_support_unit_id_2": units[1] if len(units) > 1 else units[0],    
        "set_cb_support_star_1": stars[0],    
        "set_cb_support_star_2": stars[1] if len(stars) > 1 else stars[0],    
    }    
    return config


  
@register_tool("挂地下城支援", "set_dungeon_support")    
async def set_dungeon_support(botev: BotEvent):    
    msg = await botev.message()    
    await botev.send("请稍等1-8分钟，过整点需要重新发送")    
  
    units = []    
    stars = []    
    unknown_units = []    
    for _ in range(2):    
        try:    
            unit_name = msg[0]    
            unit = get_id_from_name(unit_name)    
            if unit:    
                units.append(unit * 100 + 1)    
                stars.append(0)  # 0 means no change  
            else:    
                if unit_name[0].isdigit():    
                    star = int(unit_name[0])    
                    unit = get_id_from_name(unit_name[1:])    
                    if unit:    
                        units.append(unit * 100 + 1)    
                        stars.append(star)    
                    else:    
                        unknown_units.append(unit_name)    
                else:    
                    unknown_units.append(unit_name)    
            del msg[0]    
        except:    
            break    
  
    if unknown_units:    
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")    
  
    if not units:    
        await botev.finish("请指定至少一个角色，如：#挂地下城支援 角色1 角色2")    
  
    config = {    
        "set_dungeon_support_unit_id_1": units[0],    
        "set_dungeon_support_unit_id_2": units[1] if len(units) > 1 else units[0],    
        "set_dungeon_support_star_1": stars[0],    
        "set_dungeon_support_star_2": stars[1] if len(stars) > 1 else stars[0],    
    }    
    return config
  
  
@register_tool("挂好友支援", "set_friend_support")    
async def set_friend_support(botev: BotEvent):    
    msg = await botev.message()    
    await botev.send("请稍等1-8分钟，过整点需要重新发送")    
  
    units = []    
    stars = []    
    unknown_units = []    
    for _ in range(2):    
        try:    
            unit_name = msg[0]    
            unit = get_id_from_name(unit_name)    
            if unit:    
                units.append(unit * 100 + 1)    
                stars.append(0)    
            else:    
                if unit_name[0].isdigit():    
                    star = int(unit_name[0])    
                    unit = get_id_from_name(unit_name[1:])    
                    if unit:    
                        units.append(unit * 100 + 1)    
                        stars.append(star)    
                    else:    
                        unknown_units.append(unit_name)    
                else:    
                    unknown_units.append(unit_name)    
            del msg[0]    
        except:    
            break    
  
    if unknown_units:    
        await botev.finish(f"未知昵称{', '.join(unknown_units)}")    
  
    if not units:    
        await botev.finish("请指定至少一个角色，如：#挂好友支援 角色1 角色2")    
  
    config = {    
        "set_friend_support_unit_id_1": units[0],    
        "set_friend_support_unit_id_2": units[1] if len(units) > 1 else units[0],    
        "set_friend_support_star_1": stars[0],    
        "set_friend_support_star_2": stars[1] if len(stars) > 1 else stars[0],    
    }    
    return config

@register_tool("穿ex彩装", "equip_rainbow_ex")  
async def equip_rainbow_ex_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
    unit_name = ""  
    unit_id = None  
    try:  
        unit_name = msg[0]  
        unit_id = get_id_from_name(unit_name)  
        del msg[0]  
    except:  
        pass  
    if not unit_id:  
        await botev.finish(f"未知角色名{unit_name}")  
    unit_id = unit_id * 100 + 1  
    serial_id = ""  
    try:  
        serial_id = msg[0]  
        del msg[0]  
    except:  
        await botev.finish("请输入彩装serial_id")  
    if not serial_id.isdigit():  
        await botev.finish(f"彩装ID必须是数字: {serial_id}")  
    return {  
        "equip_rainbow_unit_id": unit_id,  
        "equip_rainbow_serial_id": serial_id,  
    }  
  
  
@register_tool("穿ex粉装", "equip_pink_ex")  
async def equip_pink_ex_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
  
    unit_name = ""  
    unit_id = None  
    try:  
        unit_name = msg[0]  
        unit_id = get_id_from_name(unit_name)  
        del msg[0]  
    except:  
        pass  
  
    if not unit_id:  
        await botev.finish(f"未知角色名{unit_name}，请指定角色")  
  
    unit_id = unit_id * 100 + 1  
  
    serial_id = ""  
    try:  
        serial_id = msg[0]  
        del msg[0]  
    except:  
        await botev.finish("请输入粉装ID")  
  
    if not serial_id.isdigit():  
        await botev.finish(f"粉装ID必须是数字: {serial_id}")  
  
    return {  
        "equip_pink_unit_id": unit_id,  
        "equip_pink_serial_id": serial_id,  
    }  
  
  
@register_tool("穿ex金装", "equip_gold_ex")  
async def equip_gold_ex_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
  
    unit_name = ""  
    unit_id = None  
    try:  
        unit_name = msg[0]  
        unit_id = get_id_from_name(unit_name)  
        del msg[0]  
    except:  
        pass  
  
    if not unit_id:  
        await botev.finish(f"未知角色名{unit_name}，请指定角色")  
  
    unit_id = unit_id * 100 + 1  
  
    serial_id = ""  
    try:  
        serial_id = msg[0]  
        del msg[0]  
    except:  
        await botev.finish("请输入金装ID")  
  
    if not serial_id.isdigit():  
        await botev.finish(f"金装ID必须是数字: {serial_id}")  
  
    return {  
        "equip_gold_unit_id": unit_id,  
        "equip_gold_serial_id": serial_id,  
    }

@register_tool("一键穿ex", "one_click_ex_equip")  
async def one_click_ex_equip_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
  
    unit_name = ""  
    unit_id = None  
    try:  
        unit_name = msg[0]  
        unit_id = get_id_from_name(unit_name)  
        del msg[0]  
    except:  
        pass  
  
    if not unit_id:  
        await botev.finish(f"未知角色名{unit_name}")  
  
    unit_id = unit_id * 100 + 1  
  
    # Parse selection: "试穿" or 3 space-separated numbers  
    selection = "试穿"  
    if msg:  
        if msg[0] == '试穿':  
            del msg[0]  
        else:  
            # Collect 3 numbers from msg  
            parts = []  
            for _ in range(3):  
                try:  
                    parts.append(msg[0])  
                    del msg[0]  
                except:  
                    break  
            if len(parts) == 3:  
                selection = ' '.join(parts)  
            else:  
                await botev.finish(f"请输入3个数字(如 1 1 2)或'试穿'")  
  
    return {  
        "one_click_ex_unit_id": unit_id,  
        "one_click_ex_selection": selection,  
    }
    
@register_tool("查ID", "search_ex_equip_id")  
async def search_ex_equip_id(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
    equip_name = ""  
    try:  
        equip_name = msg[0]  
        del msg[0]  
    except:  
        await botev.finish("请输入装备名称")  
    return {  
        "search_ex_equip_name": equip_name,  
    }
  
@register_tool("添加好友", "add_friend")  
async def add_friend_tool(botev: BotEvent):  
    msg = await botev.message()  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
      
    viewer_id = ""  
    try:  
        viewer_id = msg[0]  
        del msg[0]  
    except:  
        pass  
      
    if not viewer_id:  
        await botev.finish("请输入玩家UID，如：#添加好友 123456789")  
      
    if not viewer_id.isdigit():  
        await botev.finish(f"玩家UID必须是数字: {viewer_id}")  
      
    config = {  
        "add_friend_viewer_id": viewer_id,  
    }  
    return config  
    
@sv.on_prefix(f"{prefix}日常设置")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def daily_set_config(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
  
    if not msg:  
        await botev.finish(  
            f"格式：\n"  
            f"  {prefix}日常设置 模块序号          查看选项\n"  
            f"  {prefix}日常设置 模块序号 选项序号      查看可选值\n"  
            f"  {prefix}日常设置 模块序号 选项序号 值    设置\n"  
            f"发送 {prefix}日常面板 查看模块序号"  
        )  
  
    indexed_modules = _get_daily_modules(acc)  
  
    # ---- 匹配模块 ----  
    module_target = msg[0]  
    success, failed = _match_modules([module_target], indexed_modules)  
    if failed:  
        await botev.finish(f"模块匹配失败: {failed[0]}")  
    mod_idx, target_module = success[0]  
  
    config_items = list(target_module.config.items())  # [(key, Config), ...]  
  
    # ---- 只传模块：显示选项列表 ----  
    if len(msg) == 1:  
        if not config_items:  
            await botev.finish(  
                f"【{target_module.name}】没有子选项，仅支持开关\n"  
                f"使用 {prefix}日常开启/{prefix}日常关闭 {mod_idx}"  
            )  
  
        enabled = acc.data.config.get(target_module.key, target_module.default)  
        header = ["序号", "选项", "当前值", "类型"]  
        content = []  
        for oidx, (key, cfg) in enumerate(config_items, 1):  
            try:  
                display = target_module.get_config_display(key)  
                type_label = {  
                    'bool': '布尔', 'int': '整数', 'single': '单选',  
                    'multi': '多选', 'multi_search': '多选搜索',  
                    'text': '文本', 'time': '时间',  
                }.get(cfg.config_type, cfg.config_type)  
                content.append([str(oidx), cfg.desc, display, type_label])  
            except Exception:  
                content.append([str(oidx), cfg.desc, "?", "?"])  
  
        img = await drawer.draw(header, content)  
        status = "开启" if enabled else "关闭"  
        await botev.send(  
            f"【{alias}】{mod_idx}.{target_module.name} (当前:{status})\n"  
            f"查看可选值: {prefix}日常设置 {mod_idx} 选项序号\n"  
            f"直接设置: {prefix}日常设置 {mod_idx} 选项序号 值\n"  
            + outp_b64(img)  
        )  
        return  
  
    # ---- 匹配选项 ----  
    option_target = msg[1]  
    target_config = None  
    option_idx = None  
  
    if option_target.isdigit():  
        oidx = int(option_target)  
        if 1 <= oidx <= len(config_items):  
            option_idx = oidx  
            target_config = config_items[oidx - 1][1]  
  
    if not target_config:  
        for oidx, (key, cfg) in enumerate(config_items, 1):  
            if cfg.desc == option_target or key == option_target:  
                option_idx = oidx  
                target_config = cfg  
                break  
  
    if not target_config:  
        options = ', '.join(f"{i}.{cfg.desc}" for i, (_, cfg) in enumerate(config_items, 1))  
        await botev.finish(f"未找到选项【{option_target}】\n可用: {options}")  
  
    ctype = target_config.config_type  
    current_display = target_module.get_config_display(target_config.key)  
  
    # ---- 只传模块+选项：显示候选值 ----  
    if len(msg) == 2:  
        try:  
            candidates = target_config.candidates  
        except Exception:  
            candidates = []  
  
        if ctype == 'text':  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"类型: 文本，直接输入内容\n"  
                f"设置: {prefix}日常设置 {mod_idx} {option_idx} 你的文本"  
            )  
        elif ctype == 'time':  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"类型: 时间，格式 HH:MM\n"  
                f"设置: {prefix}日常设置 {mod_idx} {option_idx} 05:30"  
            )  
        elif ctype == 'bool':  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"可选: 开启 / 关闭\n"  
                f"设置: {prefix}日常设置 {mod_idx} {option_idx} 开启"  
            )  
  
        if not candidates:  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"无预设候选值，直接输入值"  
            )  
  
        # 构建候选值表格  
        header = ["候选值", ""]  
        content = []  
        current_value = target_config.get_value()  
        for c in candidates:  
            display = str(target_config.candidate_display(c))  
            if ctype in ('multi', 'multi_search'):  
                selected = "#成功" if (isinstance(current_value, list) and c in current_value) else ""  
            else:  
                selected = "#成功" if c == current_value else ""  
            content.append([display, selected])  
  
        if len(content) > 50:  
            content = content[:50]  
            content.append([f"共{len(candidates)}项，建议去网页配置", ""])  
  
        img = await drawer.draw(header, content)  
  
        # 根据类型给出输入提示  
        if ctype in ('multi', 'multi_search'):  
            hint = f"多选用逗号分隔，如: {prefix}日常设置 {mod_idx} {option_idx} {str(target_config.candidate_display(candidates[0]))}"  
            if len(candidates) > 1:  
                hint += f",{str(target_config.candidate_display(candidates[1]))}"  
        elif ctype == 'int':  
            hint = f"直接输入数字，如: {prefix}日常设置 {mod_idx} {option_idx} {candidates[0]}"  
        else:  
            hint = f"输入候选值，如: {prefix}日常设置 {mod_idx} {option_idx} {str(target_config.candidate_display(candidates[0]))}"  
  
        await botev.send(  
            f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
            f"当前: {current_display}\n"  
            f"{hint}\n"  
            + outp_b64(img)  
        )  
        return  
  
    # ---- 设置值 ----  
    value_str = ' '.join(msg[2:])  
  
    # 特殊关键词：清空  
    if value_str in ('清空', '空', 'clear', 'none', '无'):  
        if ctype == 'multi' or ctype == 'multi_search':  
            final_value = []  
        elif ctype == 'text':  
            final_value = ""  
        elif ctype == 'bool':  
            final_value = False  
        elif ctype in ('int', 'single'):  
            # int/single 通常不能为空，恢复默认值  
            final_value = target_config.default  
        elif ctype == 'time':  
            final_value = target_config.default  
        else:  
            final_value = target_config.default  
  
        acc.data.config[target_config.key] = final_value  
  
        if isinstance(final_value, list):  
            display_val = '(空)' if not final_value else ', '.join(  
                str(target_config.candidate_display(v)) for v in final_value  
            )  
        else:  
            display_val = str(target_config.candidate_display(final_value)) if final_value is not None else '(空)'  
  
        await botev.send(  
            f"【{alias}】{target_module.name}\n"  
            f"{target_config.desc}: {display_val}"  
        )  
        return  
  
    try:  
        candidates = target_config.candidates  
    except Exception:  
        candidates = []  
  
    final_value = None  
  
    if ctype == 'text':  
        final_value = value_str  
  
    elif ctype == 'time':  
        parts = value_str.replace('：', ':').split(':')  
        if len(parts) != 2:  
            parts = value_str.split()  
        if len(parts) != 2:  
            await botev.finish("时间格式错误，请输入 HH:MM，如 05:30")  
        try:  
            h, m = int(parts[0]), int(parts[1])  
            if not (0 <= h < 24 and 0 <= m < 60):  
                await botev.finish("时间范围错误，小时0-23，分钟0-59")  
        except ValueError:  
            await botev.finish("时间格式错误，请输入数字 HH:MM")  
        final_value = parts  
  
    elif ctype == 'bool':  
        true_vals = {'开启', '开', 'true', '是', '1', 'on'}  
        false_vals = {'关闭', '关', 'false', '否', '0', 'off'}  
        if value_str.lower() in true_vals:  
            final_value = True  
        elif value_str.lower() in false_vals:  
            final_value = False  
        else:  
            await botev.finish("请输入: 开启 或 关闭")  
  
    elif ctype in ('multi', 'multi_search'):    
        parts = [p.strip() for p in value_str.replace('，', ',').split(',')]    
        final_value = []    
        for p in parts:    
            matched_c = None    
            for c in candidates:    
                if str(target_config.candidate_display(c)) == p:    
                    matched_c = c    
                    break    
            if matched_c is None:    
                for c in candidates:    
                    if str(c) == p:    
                        matched_c = c    
                        break    
            # NEW: fallback — match by ID prefix (part before ':')  
            if matched_c is None:  
                for c in candidates:  
                    c_str = str(c)  
                    if ':' in c_str and c_str.split(':')[0].strip() == p.strip():  
                        matched_c = c  
                        break  
            if matched_c is not None:    
                final_value.append(matched_c)    
            else:    
                displays = [str(target_config.candidate_display(c)) for c in candidates[:20]]    
                await botev.finish(f"值【{p}】不在候选范围\n可选: {', '.join(displays)}")  
  
    elif ctype == 'int':  
        try:  
            num = int(value_str)  
        except ValueError:  
            await botev.finish(f"请输入整数，可选: {', '.join(str(c) for c in candidates[:30])}")  
        if candidates and num not in candidates:  
            await botev.finish(f"值 {num} 不在可选范围\n可选: {', '.join(str(c) for c in candidates[:30])}")  
        final_value = num  
  
    elif ctype == 'single':  
        # 先按显示名匹配  
        for c in candidates:  
            if str(target_config.candidate_display(c)) == value_str:  
                final_value = c  
                break  
        # 再按原始值字符串匹配  
        if final_value is None:  
            for c in candidates:  
                if str(c) == value_str:  
                    final_value = c  
                    break  
        # 尝试类型转换匹配（如输入 "5000000" 匹配 int 候选值）  
        if final_value is None and candidates:  
            try:  
                converted = type(candidates[0])(value_str)  
                if converted in candidates:  
                    final_value = converted  
            except (ValueError, TypeError):  
                pass  
        if final_value is None:  
            displays = [str(target_config.candidate_display(c)) for c in candidates[:20]]  
            await botev.finish(f"值【{value_str}】不在候选范围\n可选: {', '.join(displays)}")  
  
    else:  
        final_value = value_str  
  
    if final_value is None:  
        await botev.finish("值解析失败")  
  
    acc.data.config[target_config.key] = final_value  
  
    # 显示结果  
    if isinstance(final_value, list):  
        if ctype == 'time':  
            display_val = f"{final_value[0]}:{final_value[1]}"  
        else:  
            display_val = ', '.join(str(target_config.candidate_display(v)) for v in final_value)  
    else:  
        display_val = str(target_config.candidate_display(final_value))  
  
    await botev.send(f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}")

@sv.on_prefix(f"{prefix}日常详情")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def daily_detail(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
  
    if not msg:  
        await botev.finish(  
            f"请指定模块序号或名称\n"  
            f"示例：{prefix}日常详情 6\n"  
            f"发送 {prefix}日常面板 查看模块序号"  
        )  
  
    indexed_modules = _get_daily_modules(acc)  
    module_target = msg[0]  
    success, failed = _match_modules([module_target], indexed_modules)  
    if failed:  
        await botev.finish(f"模块匹配失败: {failed[0]}")  
    mod_idx, target_module = success[0]  
  
    enabled = acc.data.config.get(target_module.key, target_module.default)  
    config_items = list(target_module.config.items())  
  
    header = ["序号", "选项", "当前值", "类型", "可选值"]  
    content = []  
  
    for oidx, (key, cfg) in enumerate(config_items, 1):  
        try:  
            display = target_module.get_config_display(key)  
            ctype = cfg.config_type  
            type_label = {  
                'bool': '布尔', 'int': '整数', 'single': '单选',  
                'multi': '多选', 'multi_search': '多选搜索',  
                'text': '文本', 'time': '时间',  
            }.get(ctype, ctype)  
  
            # 可选值摘要  
            if ctype == 'bool':  
                candidates_str = "开启 / 关闭"  
            elif ctype in ('text', 'time'):  
                candidates_str = "自由输入"  
            else:  
                try:  
                    cands = cfg.candidates  
                    if cands:  
                        displays = [str(cfg.candidate_display(c)) for c in cands]  
                        if len(displays) <= 8:  
                            candidates_str = ', '.join(displays)  
                        else:  
                            candidates_str = ', '.join(displays[:6]) + f'...共{len(cands)}项'  
                    else:  
                        candidates_str = "-"  
                except Exception:  
                    candidates_str = "-"  
  
            content.append([str(oidx), cfg.desc, display, type_label, candidates_str])  
        except Exception:  
            content.append([str(oidx), cfg.desc, "?", "?", "-"])  
  
    if not content:  
        await botev.finish(f"【{target_module.name}】没有子选项，仅支持开关\n使用 {prefix}日常开启/{prefix}日常关闭 {mod_idx}")  
  
    img = await drawer.draw(header, content)  
    status = "#成功" if enabled else "#跳过"  
    desc = f"\n说明: {target_module.description}" if target_module.description else ""  
    await botev.send(  
        f"【{alias}】{mod_idx}.{target_module.name}({target_module.key}) 当前:{'开启' if enabled else '关闭'}{desc}\n"  
        f"设置选项: {prefix}日常设置 {mod_idx} 选项序号 值\n"  
        + outp_b64(img)  
    )  
  

  
  
@sv.on_prefix(f"{prefix}日常面板")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def daily_panel(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    indexed_modules = _get_daily_modules(acc)  
  
    if not indexed_modules:  
        await botev.finish("未找到日常模块")  
  
    # 构建每行数据: [序号, 功能名, 状态]  
    items = []  
    for idx, m in indexed_modules:  
        enabled = acc.data.config.get(m.key, m.default)  
        status = "#成功" if enabled else "#跳过"  
        items.append([str(idx), m.name or m.key, status])  
  
    # 分成 3 列  
    num_cols = 3  
    rows_per_col = math.ceil(len(items) / num_cols)  
  
    header = ["序号", "功能", "状态"]  
    images = []  
    for i in range(num_cols):  
        chunk = items[i * rows_per_col : (i + 1) * rows_per_col]  
        if chunk:  
            img = await drawer.draw(header, chunk)  
            images.append(img)  
  
    # 水平拼接  
    if len(images) == 1:  
        final_img = images[0]  
    else:  
        widths, heights = zip(*(img.size for img in images))  
        max_height = max(heights)  
        total_width = sum(widths)  
        bg = drawer.color().get('bg', '#222529')  
        final_img = Image.new('RGB', (total_width, max_height), bg)  
        x_offset = 0  
        for img in images:  
            final_img.paste(img, (x_offset, 0))  
            x_offset += img.size[0]  
  
    await botev.send(f"【{alias}】日常面板\n" + outp_b64(final_img))  
  
  
@sv.on_prefix(f"{prefix}日常开启")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def daily_enable(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
  
    if not msg:  
        await botev.finish(  
            f"请指定序号或功能名，多个用空格分隔\n"  
            f"示例：{prefix}日常开启 1 3 5\n"  
            f"示例：{prefix}日常开启 免费扭蛋 普通扭蛋\n"  
            f"发送 {prefix}日常面板 查看序号"  
        )  
  
    indexed_modules = _get_daily_modules(acc)  
    success, failed = _match_modules(msg, indexed_modules)  
  
    toggled = []  
    for idx, m in success:  
        current = acc.data.config.get(m.key, m.default)  
        if current:  
            failed.append(f"{idx}.{m.name}(已开启)")  
        else:  
            acc.data.config[m.key] = True  
            toggled.append(f"{idx}.{m.name}")  
  
    lines = []  
    if toggled:  
        lines.append("已开启: " + ", ".join(toggled))  
    if failed:  
        lines.append("跳过: " + ", ".join(failed))  
    await botev.send(f"【{alias}】\n" + "\n".join(lines))  
  
  
@sv.on_prefix(f"{prefix}日常关闭")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def daily_disable(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
  
    if not msg:  
        await botev.finish(  
            f"请指定序号或功能名，多个用空格分隔\n"  
            f"示例：{prefix}日常关闭 2 4 6\n"  
            f"示例：{prefix}日常关闭 免费扭蛋 普通扭蛋\n"  
            f"发送 {prefix}日常面板 查看序号"  
        )  
  
    indexed_modules = _get_daily_modules(acc)  
    success, failed = _match_modules(msg, indexed_modules)  
  
    toggled = []  
    for idx, m in success:  
        current = acc.data.config.get(m.key, m.default)  
        if not current:  
            failed.append(f"{idx}.{m.name}(已关闭)")  
        else:  
            acc.data.config[m.key] = False  
            toggled.append(f"{idx}.{m.name}")  
  
    lines = []  
    if toggled:  
        lines.append("已关闭: " + ", ".join(toggled))  
    if failed:  
        lines.append("跳过: " + ", ".join(failed))  
    await botev.send(f"【{alias}】\n" + "\n".join(lines))

@register_tool("清除编队", "clear_my_party")  
async def clear_my_party_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    msg = await botev.message()  
    clear_tab_start_num = 1  
    clear_party_start_num = 1  
    clear_team_num = 1  
    try:  
        clear_tab_start_num = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        clear_party_start_num = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    try:  
        clear_team_num = int(msg[0])  
        del msg[0]  
    except:  
        pass  
    config = {  
        "clear_tab_start_num": clear_tab_start_num,  
        "clear_party_start_num": clear_party_start_num,  
        "clear_team_num": clear_team_num,  
    }  
    return config
  
@register_tool("保存ex状态", "save_ex_state")  
async def save_ex_state_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    return {}  
  
@register_tool("恢复ex状态", "restore_ex_state")  
async def restore_ex_state_tool(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    return {}  

@sv.on_prefix(f"{prefix}pjjc自动换防")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def pjjc_auto_def_switch(botev: BotEvent, acc):  
    import time as _time  
    import random  
    import itertools  
    from datetime import datetime as dt  
  
    alias = getattr(acc, 'alias', '未知账号')  
    sender_qq = await botev.send_qq()  
  
    # 检查是否已有运行中的任务  
    if sender_qq in _auto_def_stop_events:  
        await botev.finish(f"已有正在运行的自动换防任务，请先发送 {prefix}终止换防")  
  
    shuffle_count = 0  
    check_interval = 2        # 每2秒检查一次被刺  
  
    stop_event = asyncio.Event()  
    _auto_def_stop_events[sender_qq] = stop_event  
  
    try:  
        client = acc.client  
        await client.activate()  
  
        # Login if needed  
        from .autopcr.core.pcrclient import eLoginStatus  
        if client.logged == eLoginStatus.NOT_LOGGED or not client.data.ready:  
            await client.login()  
  
        # 获取初始历史记录基线  
        history_resp = await client.get_grand_arena_history()  
        known_log_ids = set()  
        if history_resp.grand_arena_history_list:  
            for h in history_resp.grand_arena_history_list:  
                known_log_ids.add(h.log_id)  
  
        # --- 换防逻辑提取为内部函数 ---  
        async def do_shuffle():  
            from .autopcr.model.common import DeckListData  
            from .autopcr.model.enums import ePartyType  
  
            # 检查换防次数限制  
            info = await client.get_grand_arena_info()  
            limit_info = info.update_deck_times_limit  
            if limit_info.round_times == limit_info.round_max_limited_times:  
                ok_time = db.format_time(db.parse_time(limit_info.round_end_time))  
                return None, f"已达到换防次数上限{limit_info.round_max_limited_times}，请于{ok_time}后再试，自动换防终止"  
            if limit_info.daily_times == limit_info.daily_max_limited_times:  
                return None, f"已达到每日换防次数上限{limit_info.daily_max_limited_times}，自动换防终止"  
  
            limit_msg = ""  
            if limit_info.round_times:  
                limit_msg = f"{db.format_time(db.parse_time(limit_info.round_end_time))}刷新"  
  
            # 生成错排  
            team_cnt = 3  
            teams = [list(x) for x in itertools.permutations(range(team_cnt))]  
            teams = [x for x in teams if all(x[i] != i for i in range(team_cnt))]  
            ids = random.choice(teams)  
  
            # 构建 deck list  
            deck_list = []  
            for i in range(team_cnt):  
                deck_number_src = getattr(ePartyType, f"GRAND_ARENA_DEF_{i + 1}")  
                units = client.data.deck_list[deck_number_src]  
                units_id = [getattr(units, f"unit_id_{j + 1}") for j in range(5)]  
  
                deck = DeckListData()  
                deck.deck_number = getattr(ePartyType, f"GRAND_ARENA_DEF_{ids[i] + 1}")  
                deck.unit_list = units_id  
                deck_list.append(deck)  
  
            deck_list.sort(key=lambda x: x.deck_number)  
            await client.deck_update_list(deck_list)  
  
            shuffle_msg = '\n'.join([f"队伍{i+1} -> 位置{ids[i]+1}" for i in range(team_cnt)])  
            result_msg = (  
                f"{shuffle_msg}\n"  
                f"本轮换防次数{limit_info.round_times + 1}/{limit_info.round_max_limited_times}，{limit_msg}\n"  
                f"今日换防次数{limit_info.daily_times + 1}/{limit_info.daily_max_limited_times}"  
            )  
            return ids, result_msg  
  
        await botev.send(  
            f"{alias} pjjc自动换防已开启\n"  
            f"每2秒检测被刺记录，被刺立即换防\n"  
            f"未被刺不换防\n"  
            f"发送 {prefix}终止换防 可停止"  
        )  
  
        while True:  
            # 每2秒检查一次  
            try:  
                await asyncio.wait_for(stop_event.wait(), timeout=check_interval)  
                await botev.send(f"{alias} 收到终止信号，自动换防已停止，共执行换防{shuffle_count}次")  
                client.deactivate()  
                return  
            except asyncio.TimeoutError:  
                pass  
  
            # 检查被刺记录  
            try:  
                history_resp = await client.get_grand_arena_history()  
                if history_resp.grand_arena_history_list:  
                    new_attacks = []  
                    for h in history_resp.grand_arena_history_list:  
                        if h.log_id not in known_log_ids:  
                            known_log_ids.add(h.log_id)  
                            if not h.is_challenge:  
                                opponent = h.opponent_user  
                                attack_time = dt.fromtimestamp(h.versus_time)  
                                new_attacks.append(f"{opponent.user_name}({opponent.viewer_id}) {attack_time} 被刺")  
  
                    if new_attacks:  
                        # 被刺了，立即换防  
                        attack_msg = "\n".join(new_attacks)  
                        try:  
                            result = await do_shuffle()  
                            if result[0] is None:  
                                await botev.send(  
                                    f"{alias} 检测到被刺记录：\n{attack_msg}\n"  
                                    f"尝试立即换防但{result[1]}"  
                                )  
                                break  
                            shuffle_count += 1  
  
                            await botev.send(  
                                f"{alias} 检测到被刺记录：\n{attack_msg}\n"  
                                f"已立即执行第{shuffle_count}次换防！\n"  
                                f"{result[1]}\n"  
                                f"正在下线并重新上线..."  
                            )  
                              
                            # 换防后下线  
                            client.deactivate()  
                              
                            # 重新上线  
                            await client.activate()  
                            if client.logged == eLoginStatus.NOT_LOGGED or not client.data.ready:  
                                await client.login()  
                              
                            # 重建历史记录基线（清空旧数据，从服务器重新获取）  
                            known_log_ids.clear()  
                            history_resp2 = await client.get_grand_arena_history()  
                            if history_resp2.grand_arena_history_list:  
                                for h2 in history_resp2.grand_arena_history_list:  
                                    known_log_ids.add(h2.log_id)  
                              
                            await botev.send(  
                                f"{alias} 已重新上线，继续每2秒检测被刺"  
                            ) 
                            
                        except Exception as e:  
                            logger.error(f"pjjc自动换防被刺立即换防出错: {str(e)}")  
                            await botev.send(  
                                f"{alias} 检测到被刺记录：\n{attack_msg}\n"  
                                f"立即换防出错: {str(e)[:200]}\n"  
                                f"尝试下线并重新上线..."  
                            )  
                            try:  
                                client.deactivate()  
                                await client.activate()  
                                if client.logged == eLoginStatus.NOT_LOGGED or not client.data.ready:  
                                    await client.login()  
                                known_log_ids.clear()  
                                history_resp_err = await client.get_grand_arena_history()  
                                if history_resp_err.grand_arena_history_list:  
                                    for h_err in history_resp_err.grand_arena_history_list:  
                                        known_log_ids.add(h_err.log_id)  
                            except:  
                                await botev.send(f"{alias} 重新登录失败，自动换防终止")  
                                break
                                
            except Exception as e:  
                logger.error(f"pjjc自动换防检查被刺出错: {str(e)}")  
                try:  
                    if client.logged == eLoginStatus.NOT_LOGGED:  
                        await client.login()  
                except:  
                    await botev.send(f"{alias} 重新登录失败，自动换防终止")  
                    break  
  
        client.deactivate()  
        await botev.send(f"{alias} pjjc自动换防已结束，共执行换防{shuffle_count}次")  
  
    except Exception as e:  
        try:  
            client.deactivate()  
        except:  
            pass  
        await botev.send(f"{alias} pjjc自动换防异常终止: {str(e)[:300]}")  
    finally:  
        _auto_def_stop_events.pop(sender_qq, None)
  
  
@sv.on_fullmatch(f"{prefix}终止换防")  
@wrap_hoshino_event  
async def pjjc_stop_auto_def(botev: BotEvent):  
    sender_qq = await botev.send_qq()  
    if sender_qq in _auto_def_stop_events:  
        _auto_def_stop_events[sender_qq].set()  
    else:  
        await botev.send("当前没有正在运行的自动换防任务")
        
@register_tool("黎明界刷开局", "labyrinth_start_reroll")
async def labyrinth_start_reroll(botev: BotEvent):
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    guild_id = 0
    msg = await botev.message()
    try:
        for guild in db.labyrinth_enter_guild.values():
            if msg[0] in guild.guild_name.replace(r"\n", ""):
                guild_id = guild.guild_id
                del msg[0]
                break
    except:
        pass
    if guild_id == 0:
        await botev.finish(f"未找到公会，请输入包含以下公会名字：" + "\n".join([guild.guild_name.replace(r"\n", "") for guild in db.labyrinth_enter_guild.values()]))
    return {
            "labyrinth_reroll_guild_id": guild_id,
    }

@register_tool("黎明界积分", "labyrinth_point_query")  
async def labyrinth_point_query(botev: BotEvent):  
    await botev.send("请稍等1-8分钟，过整点需要重新发送")  
    return {}

def _compute_daily_reorder(acc: Account, args: list):  
    """对单个真实账号计算并写入清日常顺序，返回 (是否更新, 提示文本)。不做任何 botev 交互。"""  
    alias = escape(acc.alias)  
    indexed_modules = _get_daily_modules(acc)  
  
    # 重置：清掉自定义顺序，回到默认顺序  
    if len(args) == 1 and args[0] in ("重置", "reset", "默认"):  
        acc.data.config.pop(DAILY_ORDER_KEY, None)  
        return True, f"【{alias}】已恢复默认清日常顺序"  
  
    if len(args) < 2:  
        return False, f"【{alias}】至少需要两个参数：锚点功能 + 要挪到其后的功能"  
  
    # 第一个参数 = 锚点功能  
    anchor_success, anchor_failed = _match_modules([args[0]], indexed_modules)  
    if not anchor_success:  
        return False, f"【{alias}】锚点功能匹配失败: {anchor_failed[0] if anchor_failed else args[0]}"  
    anchor_module = anchor_success[0][1]  
  
    # 其余参数 = 要挪到锚点后面的功能  
    move_success, move_failed = _match_modules(args[1:], indexed_modules)  
  
    move_keys = []  
    for idx, m in move_success:  
        if m.key != anchor_module.key and m.key not in move_keys:  
            move_keys.append(m.key)  
  
    if not move_keys:  
        return False, f"【{alias}】要挪动的功能不能为空，且不能与锚点相同"  
  
    # 基于当前顺序重排：先剔除待挪动项，遍历到锚点后再把它们插进去  
    order = []  
    for idx, m in indexed_modules:  
        if m.key in move_keys:  
            continue  
        order.append(m.key)  
        if m.key == anchor_module.key:  
            order.extend(move_keys)  
  
    acc.data.config[DAILY_ORDER_KEY] = order  
  
    moved_names = ", ".join(acc.modules_list.get_module_from_key(k).name for k in move_keys)  
    lines = [f"已将 [{moved_names}] 挪到 [{anchor_module.name}] 之后"]  
    if move_failed:  
        lines.append("跳过: " + ", ".join(move_failed))  
    return True, f"【{alias}】清日常顺序已更新\n" + "\n".join(lines)  
  
  
@sv.on_prefix(f"{prefix}清日常排序")  
@wrap_hoshino_event  
@wrap_accountmgr  
async def daily_reorder(botev: BotEvent, accmgr: AccountManager):  
    msg = await botev.message()  
  
    # ===== 「所有」分支：逐个真实账号修改，不走 BATCH_RUNNER =====  
    if msg and msg[0] == '所有':  
        del msg[0]  
        if not msg:  
            await botev.finish(  
                f"把指定功能挪到某个功能之后\n"  
                f"第一个是锚点功能，其余是要挪到它后面的功能\n"  
                f"示例：{prefix}清日常排序所有 5 1 3  (把1、3挪到5后面)\n"  
                f"发送 {prefix}清日常排序 重置 可恢复默认顺序"  
            )  
        results = []  
        for alias in accmgr.accounts():  
            async with accmgr.load(alias) as acc:  
                ok, text = _compute_daily_reorder(acc, list(msg))  
                results.append(text)  
        await botev.finish("\n".join(results) if results else "没有可修改的账号")  
  
    # ===== 其余情况：解析出单个账号（复刻原 wrap_account 行为）=====  
    alias = msg[0] if msg else ""  
    if alias == '批量':  
        alias = BATCHINFO  
        del msg[0]  
    elif alias not in accmgr.accounts():  
        alias = accmgr.default_account  
    else:  
        del msg[0]  
  
    if alias != BATCHINFO and len(list(accmgr.accounts())) == 1:  
        alias = list(accmgr.accounts())[0]  
  
    if alias != BATCHINFO and alias not in accmgr.accounts():  
        if alias:  
            await botev.finish(f"未找到昵称为【{alias}】的账号")  
        else:  
            await botev.finish(f"存在多账号且未找到默认账号，请指定昵称")  
  
    if not msg:  
        await botev.finish(  
            f"把指定功能挪到某个功能之后\n"  
            f"第一个是锚点功能，其余是要挪到它后面的功能\n"  
            f"示例：{prefix}清日常排序 5 1 3  (把1、3挪到5后面)\n"  
            f"发送 {prefix}日常面板 查看当前序号\n"  
            f"发送 {prefix}清日常排序 重置 可恢复默认顺序"  
        )  
  
    async with accmgr.load(alias, force_use_all=(alias == BATCHINFO)) as acc:  
        ok, text = _compute_daily_reorder(acc, list(msg))  
    await botev.finish(text)

def _get_cron_modules(acc):  
    """获取定时(cron)模块列表（带序号），返回 [(idx, module), ...]"""  
    modules = acc.modules_list.get_modules_list('cron')  
    return [(i + 1, m) for i, m in enumerate(modules)]

@sv.on_prefix(f"{prefix}定时面板")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def cron_panel(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    indexed_modules = _get_cron_modules(acc)  
    if not indexed_modules:  
        await botev.finish("未找到定时任务")  
  
    lines = [f"【{alias}】定时面板", ""]  
    lines.append(f"{'序号':>4}  {'任务':<12}  {'时间':<7}  状态")  
    lines.append("-" * 40)  
    for idx, m in indexed_modules:  
        enabled = acc.data.config.get(m.key, m.default)  
        status = "开启" if enabled else "关闭"  
        name = m.name or m.key  
        try:  
            time_val = m.get_config_display(f"time_{m.key}")  
        except Exception:  
            time_val = "-"  
        lines.append(f"{idx:>4}  {name:<12}  {time_val:<7}  {status}")  
    lines.append("")  
    lines.append(f"详情: {prefix}定时详情 序号")  
    lines.append(f"开关: {prefix}定时开关 序号")  
    await botev.send("\n".join(lines))  
  
  
@sv.on_prefix(f"{prefix}定时详情")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def cron_detail(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
    if not msg:  
        await botev.finish(  
            f"请指定定时任务序号或名称\n"  
            f"示例：{prefix}定时详情 1\n"  
            f"发送 {prefix}定时面板 查看任务序号"  
        )  
  
    indexed_modules = _get_cron_modules(acc)  
    success, failed = _match_modules([msg[0]], indexed_modules)  
    if failed:  
        await botev.finish(f"任务匹配失败: {failed[0]}")  
    mod_idx, target_module = success[0]  
  
    enabled = acc.data.config.get(target_module.key, target_module.default)  
    config_items = list(target_module.config.items())  
  
    desc = f"\n说明: {target_module.description}" if target_module.description else ""  
    lines = [  
        f"【{alias}】{mod_idx}.{target_module.name}({target_module.key}) "  
        f"当前:{'开启' if enabled else '关闭'}{desc}",  
        ""  
    ]  
    for oidx, (key, cfg) in enumerate(config_items, 1):  
        try:  
            display = target_module.get_config_display(key)  
            ctype = cfg.config_type  
            type_label = {  
                'bool': '布尔', 'int': '整数', 'single': '单选',  
                'multi': '多选', 'multi_search': '多选搜索',  
                'text': '文本', 'time': '时间',  
            }.get(ctype, ctype)  
            if ctype == 'bool':  
                candidates_str = "开启 / 关闭"  
            elif ctype in ('text', 'time'):  
                candidates_str = "自由输入"  
            else:  
                try:  
                    cands = cfg.candidates  
                    if cands:  
                        displays = [str(cfg.candidate_display(c)) for c in cands]  
                        if len(displays) <= 8:  
                            candidates_str = ', '.join(displays)  
                        else:  
                            candidates_str = ', '.join(displays[:6]) + f'...共{len(cands)}项'  
                    else:  
                        candidates_str = "-"  
                except Exception:  
                    candidates_str = "-"  
            lines.append(f"  {oidx}. {cfg.desc}")  
            lines.append(f"     当前: {display}  类型: {type_label}")  
            lines.append(f"     可选: {candidates_str}")  
        except Exception:  
            lines.append(f"  {oidx}. {cfg.desc} (读取失败)")  
    lines.append("")  
    lines.append(f"设置选项: {prefix}定时设置 {mod_idx} 选项序号 值")  
    lines.append(f"开关任务: {prefix}定时开关 {mod_idx}")  
    await botev.send("\n".join(lines))  
  
  
@sv.on_prefix(f"{prefix}定时开关")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def cron_toggle(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
    if not msg:  
        await botev.finish(  
            f"请指定序号或任务名，多个用空格分隔\n"  
            f"示例：{prefix}定时开关 1 3\n"  
            f"发送 {prefix}定时面板 查看序号"  
        )  
  
    indexed_modules = _get_cron_modules(acc)  
    success, failed = _match_modules(msg, indexed_modules)  
  
    enabled_list = []  
    disabled_list = []  
    for idx, m in success:  
        current = acc.data.config.get(m.key, m.default)  
        new_val = not current  
        acc.data.config[m.key] = new_val  
        if new_val:  
            enabled_list.append(f"{idx}.{m.name}")  
        else:  
            disabled_list.append(f"{idx}.{m.name}")  
  
    lines = []  
    if enabled_list:  
        lines.append("已开启: " + ", ".join(enabled_list))  
    if disabled_list:  
        lines.append("已关闭: " + ", ".join(disabled_list))  
    if failed:  
        lines.append("跳过: " + ", ".join(failed))  
    await botev.send(f"【{alias}】\n" + "\n".join(lines))  
  
  
@sv.on_prefix(f"{prefix}定时设置")  
@wrap_hoshino_event  
@wrap_accountmgr  
@wrap_account  
async def cron_set_config(botev: BotEvent, acc: Account):  
    alias = escape(acc.alias)  
    msg = await botev.message()  
  
    if not msg:  
        await botev.finish(  
            f"格式：\n"  
            f"  {prefix}定时设置 任务序号          查看选项\n"  
            f"  {prefix}定时设置 任务序号 选项序号      查看可选值\n"  
            f"  {prefix}定时设置 任务序号 选项序号 值    设置\n"  
            f"发送 {prefix}定时面板 查看任务序号"  
        )  
  
    indexed_modules = _get_cron_modules(acc)  
    success, failed = _match_modules([msg[0]], indexed_modules)  
    if failed:  
        await botev.finish(f"任务匹配失败: {failed[0]}")  
    mod_idx, target_module = success[0]  
  
    config_items = list(target_module.config.items())  
  
    # 只传任务：显示选项列表  
    if len(msg) == 1:  
        enabled = acc.data.config.get(target_module.key, target_module.default)  
        status = "开启" if enabled else "关闭"  
        lines = [f"【{alias}】{mod_idx}.{target_module.name} (当前:{status})", ""]  
        for oidx, (key, cfg) in enumerate(config_items, 1):  
            try:  
                display = target_module.get_config_display(key)  
                type_label = {  
                    'bool': '布尔', 'int': '整数', 'single': '单选',  
                    'multi': '多选', 'multi_search': '多选搜索',  
                    'text': '文本', 'time': '时间',  
                }.get(cfg.config_type, cfg.config_type)  
                lines.append(f"  {oidx}. {cfg.desc}: {display} ({type_label})")  
            except Exception:  
                lines.append(f"  {oidx}. {cfg.desc}: ? (?)")  
        lines.append("")  
        lines.append(f"查看可选值: {prefix}定时设置 {mod_idx} 选项序号")  
        lines.append(f"直接设置: {prefix}定时设置 {mod_idx} 选项序号 值")  
        await botev.finish("\n".join(lines))  
  
    # 匹配选项  
    option_target = msg[1]  
    target_config = None  
    option_idx = None  
    if option_target.isdigit():  
        oidx = int(option_target)  
        if 1 <= oidx <= len(config_items):  
            option_idx = oidx  
            target_config = config_items[oidx - 1][1]  
    if not target_config:  
        for oidx, (key, cfg) in enumerate(config_items, 1):  
            if cfg.desc == option_target or key == option_target:  
                option_idx = oidx  
                target_config = cfg  
                break  
    if not target_config:  
        options = ', '.join(f"{i}.{cfg.desc}" for i, (_, cfg) in enumerate(config_items, 1))  
        await botev.finish(f"未找到选项【{option_target}】\n可用: {options}")  
  
    ctype = target_config.config_type  
    current_display = target_module.get_config_display(target_config.key)  
  
    # 只传任务+选项：显示候选值  
    if len(msg) == 2:  
        try:  
            candidates = target_config.candidates  
        except Exception:  
            candidates = []  
        if ctype == 'text':  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n类型: 文本，直接输入内容\n"  
                f"设置: {prefix}定时设置 {mod_idx} {option_idx} 你的文本"  
            )  
        elif ctype == 'time':  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n类型: 时间，格式 HH:MM\n"  
                f"设置: {prefix}定时设置 {mod_idx} {option_idx} 05:30"  
            )  
        elif ctype == 'bool':  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n可选: 开启 / 关闭\n"  
                f"设置: {prefix}定时设置 {mod_idx} {option_idx} 开启"  
            )  
        if not candidates:  
            await botev.finish(  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n无预设候选值，直接输入值"  
            )  
        current_value = target_config.get_value()  
        lines = [f"【{target_module.name}】{option_idx}.{target_config.desc}",  
                 f"当前: {current_display}", ""]  
        for c in candidates[:50]:  
            display = str(target_config.candidate_display(c))  
            if ctype in ('multi', 'multi_search'):  
                selected = " [已选]" if (isinstance(current_value, list) and c in current_value) else ""  
            else:  
                selected = " [当前]" if c == current_value else ""  
            lines.append(f"  {display}{selected}")  
        if len(candidates) > 50:  
            lines.append(f"  ...共{len(candidates)}项，建议去网页配置")  
        if ctype in ('multi', 'multi_search'):  
            hint = f"多选用逗号分隔: {prefix}定时设置 {mod_idx} {option_idx} 值1,值2"  
        elif ctype == 'int':  
            hint = f"直接输入数字: {prefix}定时设置 {mod_idx} {option_idx} {candidates[0]}"  
        else:  
            hint = f"输入候选值: {prefix}定时设置 {mod_idx} {option_idx} {str(target_config.candidate_display(candidates[0]))}"  
        lines.append("")  
        lines.append(hint)  
        await botev.finish("\n".join(lines))  
  
    # 设置值  
    value_str = ' '.join(msg[2:])  
    if value_str in ('清空', '空', 'clear', 'none', '无'):  
        if ctype in ('multi', 'multi_search'):  
            final_value = []  
        elif ctype == 'text':  
            final_value = ""  
        elif ctype == 'bool':  
            final_value = False  
        else:  
            final_value = target_config.default  
        acc.data.config[target_config.key] = final_value  
        if isinstance(final_value, list):  
            display_val = '(空)' if not final_value else ', '.join(  
                str(target_config.candidate_display(v)) for v in final_value)  
        else:  
            display_val = str(target_config.candidate_display(final_value)) if final_value is not None else '(空)'  
        await botev.finish(f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}")  
  
    try:  
        candidates = target_config.candidates  
    except Exception:  
        candidates = []  
    final_value = None  
  
    if ctype == 'text':  
        final_value = value_str  
    elif ctype == 'time':  
        tp = value_str.replace('：', ':').split(':')  
        if len(tp) != 2:  
            tp = value_str.split()  
        if len(tp) != 2:  
            await botev.finish("时间格式错误，请输入 HH:MM，如 05:30")  
        try:  
            h, m = int(tp[0]), int(tp[1])  
            if not (0 <= h < 24 and 0 <= m < 60):  
                await botev.finish("时间范围错误，小时0-23，分钟0-59")  
        except ValueError:  
            await botev.finish("时间格式错误，请输入数字 HH:MM")  
        final_value = tp  
    elif ctype == 'bool':  
        true_vals = {'开启', '开', 'true', '是', '1', 'on'}  
        false_vals = {'关闭', '关', 'false', '否', '0', 'off'}  
        if value_str.lower() in true_vals:  
            final_value = True  
        elif value_str.lower() in false_vals:  
            final_value = False  
        else:  
            await botev.finish("请输入: 开启 或 关闭")  
    elif ctype in ('multi', 'multi_search'):  
        vals = [p.strip() for p in value_str.replace('，', ',').split(',')]  
        final_value = []  
        for p in vals:  
            matched_c = None  
            for c in candidates:  
                if str(target_config.candidate_display(c)) == p:  
                    matched_c = c  
                    break  
            if matched_c is None:  
                for c in candidates:  
                    if str(c) == p:  
                        matched_c = c  
                        break  
            if matched_c is not None:  
                final_value.append(matched_c)  
            else:  
                displays = [str(target_config.candidate_display(c)) for c in candidates[:20]]  
                await botev.finish(f"值【{p}】不在候选范围\n可选: {', '.join(displays)}")  
    elif ctype == 'int':  
        try:  
            num = int(value_str)  
        except ValueError:  
            await botev.finish(f"请输入整数，可选: {', '.join(str(c) for c in candidates[:30])}")  
        if candidates and num not in candidates:  
            await botev.finish(f"值 {num} 不在可选范围\n可选: {', '.join(str(c) for c in candidates[:30])}")  
        final_value = num  
    elif ctype == 'single':  
        for c in candidates:  
            if str(target_config.candidate_display(c)) == value_str:  
                final_value = c  
                break  
        if final_value is None:  
            for c in candidates:  
                if str(c) == value_str:  
                    final_value = c  
                    break  
        if final_value is None and candidates:  
            try:  
                converted = type(candidates[0])(value_str)  
                if converted in candidates:  
                    final_value = converted  
            except (ValueError, TypeError):  
                pass  
        if final_value is None:  
            displays = [str(target_config.candidate_display(c)) for c in candidates[:20]]  
            await botev.finish(f"值【{value_str}】不在候选范围\n可选: {', '.join(displays)}")  
    else:  
        final_value = value_str  
  
    if final_value is None:  
        await botev.finish("值解析失败")  
  
    acc.data.config[target_config.key] = final_value  
  
    if isinstance(final_value, list):  
        if ctype == 'time':  
            display_val = f"{final_value[0]}:{final_value[1]}"  
        else:  
            display_val = ', '.join(str(target_config.candidate_display(v)) for v in final_value)  
    else:  
        display_val = str(target_config.candidate_display(final_value))  
  
    await botev.send(f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}")    

# @register_tool("获取导入", "get_library_import_data")
# async def get_library_import(botev: BotEvent):
    # return {}