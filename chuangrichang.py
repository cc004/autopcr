import os
import re
import json  
import random          # 新增  
import string          # 新增
import shutil
import traceback
import requests
from hoshino import Service, priv, get_bot
from hoshino.typing import CQEvent
from nonebot import on_command, CommandSession

sv = Service(
    '清日常创建', 
    enable_on_default=False,
    help_='发送"清日常创建"初始化日常配置（自动导入桌面账号文件）\n'  
          '或发送"清日常创建 账号 密码 用户名"设置账号密码及文件名\n'  
          '发送"清日常禁用 文件夹名1 [文件夹名2...]"禁用指定文件夹的日常任务\n'  
          '发送"清日常解禁 文件夹名1 [文件夹名2...]"解禁指定文件夹的日常任务\n'  
          '发送"清日常重置密码"将登录密码重置为随机密码'
)

def get_public_ip():
    try:
        services = [
            'https://api.ipify.org',
            'https://ident.me',
            'https://ifconfig.me/ip'
        ]
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue
        return None
    except Exception:
        return None

def update_json_file(file_path, username, password):
    """严格只更新username和password字段，其他内容原封不动"""
    try:
        # 1. 读取原始文件内容（完全保留所有字符）
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 2. 备份原始内容
        original_content = content
        
        # 3. 处理username字段
        if '"username"' in content:
            # 如果已有username字段，只替换值部分
            content = re.sub(
                r'("username"\s*:\s*")[^"]*(")',
                f'\\g<1>{username}\\g<2>',
                content
            )
        else:
            # 如果没有username字段，在第一个{后添加
            content = content.replace('{', f'{{\n    "username": "{username}",', 1)
        
        # 4. 处理password字段
        if '"password"' in content:
            content = re.sub(
                r'("password"\s*:\s*")[^"]*(")',
                f'\\g<1>{password}\\g<2>',
                content
            )
        else:
            # 如果没有password字段，在第一个{后添加
            content = content.replace('{', f'{{\n    "password": "{password}",', 1)
        
        # 5. 验证JSON格式是否有效
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            # 如果格式错误，恢复原始内容
            content = original_content
            raise Exception(f"更新后JSON格式无效，已恢复原文件: {str(e)}")
        
        # 6. 写入文件（完全保留原始编码和换行符）
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
            
    except Exception as e:
        raise Exception(f"更新JSON文件失败: {str(e)}")

def update_secret_status(user_dirs, enable: bool):  
    """  
    批量更新secret文件的clan和disabled状态，并在禁用/解禁时备份或恢复 cron1~cron10 的开关状态。  
    :param user_dirs: 文件夹名列表（对应user_id）  
    :param enable: True=解禁（clan/disabled=False，并恢复cron备份），False=禁用（clan/disabled=True，并备份cron状态）  
    :return: 操作结果字典  
    """  
    result = {"success": [], "failed": []}  
  
    target_clan = "false" if enable else "true"  
    target_disabled = "false" if enable else "true"  
  
    hoshino_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  
    base_dir = os.path.join(hoshino_dir, 'modules', 'autopcr', 'cache', 'http_server')  
    cron_keys = [f'cron{i}' for i in range(1, 11)]  
  
    def replace_bool_field(content: str, key: str, value: str) -> str:  
        pattern = r'(\"%s\"\s*:\s*)(true|false)(?=\s*[,}\n])' % re.escape(key)  
        return re.sub(pattern, lambda m: m.group(1) + value, content)  
  
    for user_dir in user_dirs:  
        try:  
            secret_file = os.path.join(base_dir, user_dir, 'secret')  
            if not os.path.exists(secret_file):  
                result["failed"].append(f"{user_dir}: secret文件不存在")  
                continue  
  
            # 先处理 secret 文件  
            with open(secret_file, 'r', encoding='utf-8') as f:  
                content = f.read()  
  
            content = replace_bool_field(content, 'clan', target_clan)  
            content = replace_bool_field(content, 'disabled', target_disabled)  
  
            with open(secret_file, 'w', encoding='utf-8', newline='') as f:  
                f.write(content)  
  
            # 再处理该目录下所有账号 .json  
            user_path = os.path.join(base_dir, user_dir)  
            if os.path.isdir(user_path):  
                for fn in os.listdir(user_path):  
                    if not fn.endswith('.json') or fn.endswith('.cron_backup.json'):  
                        continue  
  
                    account_file = os.path.join(user_path, fn)  
                    backup_file = account_file + '.cron_backup.json'  
  
                    try:  
                        with open(account_file, 'r', encoding='utf-8') as af:  
                            acontent = af.read()  
  
                        if not enable:  
                            # 禁用：首次生成 cron 备份，保存真实布尔值  
                            if not os.path.exists(backup_file):  
                                cron_state = {}  
                                for key in cron_keys:  
                                    m = re.search(  
                                        r'(\"%s\"\s*:\s*)(true|false)(?=\s*[,}\n])' % re.escape(key),  
                                        acontent  
                                    )  
                                    if m:  
                                        cron_state[key] = (m.group(2) == 'true')  
  
                                with open(backup_file, 'w', encoding='utf-8') as bf:  
                                    json.dump(cron_state, bf, ensure_ascii=False, separators=(',', ':'))  
  
                            # 禁用时把 cron1~cron10 置为 false  
                            for key in cron_keys:  
                                acontent = re.sub(  
                                    r'(\"%s\"\s*:\s*)(true|false)(?=\s*[,}\n])' % re.escape(key),  
                                    lambda m: m.group(1) + 'false',  
                                    acontent  
                                )  
  
                        else:  
                            # 解禁：必须有备份，恢复后删除备份文件  
                            if not os.path.exists(backup_file):  
                                raise FileNotFoundError(f"{backup_file} 不存在，无法恢复 cron 状态")  
  
                            try:  
                                with open(backup_file, 'r', encoding='utf-8') as bf:  
                                    cron_state = json.load(bf)  
  
                                for key in cron_keys:  
                                    if key in cron_state:  
                                        raw = cron_state[key]  
                                        if isinstance(raw, str):  
                                            value = 'true' if raw.lower() == 'true' else 'false'  
                                        else:  
                                            value = 'true' if raw else 'false'  
  
                                        acontent = re.sub(  
                                            r'(\"%s\"\s*:\s*)(true|false)(?=\s*[,}\n])' % re.escape(key),  
                                            lambda m, v=value: m.group(1) + v,  
                                            acontent  
                                        )  
                            finally:  
                                if os.path.exists(backup_file):  
                                    os.remove(backup_file)  
  
                        with open(account_file, 'w', encoding='utf-8', newline='') as af:  
                            af.write(acontent)  
  
                    except Exception as ce:  
                        result["failed"].append(f"{user_dir}/{fn}: {str(ce)}")  
  
            result["success"].append(user_dir)  
  
        except Exception as e:  
            result["failed"].append(f"{user_dir}: {str(e)}")  
  
    return result

def reset_secret_password(secret_file):
    """重置secret文件中的password字段为123456789，default_account字段为空字符串，保留其他字段不变"""
    try:
        # 读取原始内容
        with open(secret_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析JSON（保留原有结构）
        secret_data = json.loads(content)
        # 重置密码
        secret_data['password'] = '123456789'
        # 新增：重置default_account为空字符串
        secret_data['default_account'] = ""
        
        # 单行紧凑格式写入（保持原有格式）
        with open(secret_file, 'w', encoding='utf-8') as f:
            json.dump(secret_data, f, ensure_ascii=False, separators=(',', ':'))
        
        return True
    except Exception as e:
        raise Exception(f"重置secret密码和默认账号清空失败: {str(e)}")

def generate_random_password(length=12):  
    chars = string.ascii_letters + string.digits  
    return ''.join(random.choices(chars, k=length))  

def reset_secret_password_random(secret_file):  
    try:  
        with open(secret_file, 'r', encoding='utf-8') as f:  
            content = f.read()  
        secret_data = json.loads(content)  
        new_password = generate_random_password()  
        secret_data['password'] = new_password  
        with open(secret_file, 'w', encoding='utf-8') as f:  
            json.dump(secret_data, f, ensure_ascii=True, separators=(',', ':'))  # 改这里  
        return new_password  
    except Exception as e:  
        raise Exception(f"重置secret随机密码失败: {str(e)}")

async def create_daily_config(user_id, username=None, password=None, filename=None):
    try:
        hoshino_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        base_dir = os.path.join(hoshino_dir, 'modules', 'autopcr', 'cache', 'http_server')
        user_dir = os.path.join(base_dir, user_id)
        secret_file = os.path.join(user_dir, 'secret')
        
        # ========== 修复1：兼容多系统的桌面路径获取 ==========
        if os.name == 'nt':  # Windows系统
            import winreg
            try:
                # 从注册表获取真实桌面路径（避免中文/自定义桌面路径问题）
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
                desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
                winreg.CloseKey(key)
            except:
                # 兜底方案
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        else:  # macOS/Linux
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        src_json = os.path.join(desktop_path, '我的账号.json')
        # 确定JSON文件名，有提供则使用，否则用默认
        json_filename = filename if filename else '我的账号.json'
        # ========== 修复2：提前定义目标文件路径 ==========
        dst_json = os.path.join(user_dir, json_filename)
        
        # 确保文件夹存在（仅创建文件夹，不影响后续判断）
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(user_dir, exist_ok=True)
        
        file_msg = ""
        # 检查secret文件是否存在
        if not os.path.exists(secret_file):
            # 文件不存在时创建默认配置（单行格式）
            default_config = {
                "password": "123456789",
                "default_account": "",  # 确保初始值为空字符串
                "clan": False,
                "admin": False,
                "disabled": False
            }
            # 单行紧凑格式输出
            with open(secret_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, separators=(',', ':'))
            file_msg = "✅ 初始secret配置已创建（单行格式），密码已重置为123456789，默认账号已置空"
        else:  
            # 文件已存在（重复发送者）：不重置密码，只返回地址和修改密码提示  
            public_ip = get_public_ip()  
            login_url = f"http://{public_ip}:8040/daily/login" if public_ip else "无法获取公网IP，请手动配置"  
            return f'''【清日常配置已存在】  
🌐 清日常地址: {login_url}  
🔑 如需修改密码，请发送：清日常重置密码'''
        
        # ========== 修复3：移除错误的文件夹创建判断，直接处理文件复制 ==========
        # 1. 检查桌面是否有账号文件
        if os.path.exists(src_json):
            try:
                # 复制文件（无论是否首次创建，只要源文件存在就复制，避免覆盖已存在的文件）
                if not os.path.exists(dst_json):
                    shutil.copy2(src_json, dst_json)  # 保留文件元数据
                    file_msg += "，✅ 桌面账号文件已复制"
                else:
                    file_msg += "，ℹ️ 目标文件夹已存在账号文件，未覆盖"
                
                # 如果传入了账号密码，更新文件
                if username and password:
                    try:
                        update_json_file(dst_json, username, password)
                        file_msg += "，账号密码已设置"
                    except Exception as e:
                        backup_json = f"{dst_json}.bak"
                        if os.path.exists(backup_json):
                            shutil.move(backup_json, dst_json)
                        file_msg += f"，⚠️ 账号文件更新失败: {str(e)}"
            except Exception as e:
                file_msg += f"，⚠️ 账号文件复制失败: {str(e)}"
        else:
            # 桌面无账号文件，但传入了账号密码，创建新文件
            if username and password:
                account_data = {
                    "username": username,
                    "password": password
                }
                # 单行格式创建账号文件
                with open(dst_json, 'w', encoding='utf-8') as f:
                    json.dump(account_data, f, ensure_ascii=False, separators=(',', ':'))
                file_msg += "，✅ 账号密码已创建"
            else:
                # 无文件且无账号密码，提示手动放入
                file_msg += f"，⚠️ 未找到桌面上的账号文件，请手动放入：\n{user_dir}"
        
        public_ip = get_public_ip()
        login_url = f"http://{public_ip}:8040/daily/login" if public_ip else "无法获取公网IP，请手动配置"
        
        return f'''【清日常配置创建完成】
{file_msg}
🔧🔧 使用说明：
1. 登录网站的账号为QQ号，初始密码为123456789，请及时修改[CQ:image,file=https://docimg7.docs.qq.com/image/AgAACIUgb5q_Vr3vGG5NIJHWpiWpcnHA.png?w=596&h=704]
2. 上去按指示点击圆点[CQ:image,file=https://docimg4.docs.qq.com/image/AgAACIUgb5qLsZ3QKA9Ntb683ojPeN-P.png?w=323&h=251]再点击配置填账号密码，[CQ:image,file=https://docimg5.docs.qq.com/image/AgAACIUgb5rXOV9adwdE6ai5YP1EccG_.png?w=667&h=554]再进入【日常】页面修改需求
3. [CQ:image,file=https://docimg3.docs.qq.com/image/AgAACIUgb5q18BAEbbFKL72SgBXRIu_R.png?w=452&h=174]平时可使用【#配置日常】召唤网站
🌐🌐 访问地址: {login_url}
安卓教程：https://docs.qq.com/aio/DYUt2WHRFdGFZbEZR?p=fPQSBKKVHAkZcAzvFUdq7d
'''
        
    except Exception as e:
        error_msg = f'❌❌ 创建失败：{str(e)}\n{traceback.format_exc()}'
        sv.logger.error(error_msg)
        return f'❌❌ 创建失败：{str(e)}'

# 群聊 - 清日常创建
@sv.on_prefix('清日常创建')
async def create_daily_file(bot, ev: CQEvent):
    user_id = str(ev.user_id)
    args = ev.message.extract_plain_text().strip().split()
    
    filename = None
    
    # 处理文件名参数（如果提供）
    if len(args) >= 1:
        # 确保文件名以.json结尾
        filename = args[0] + '.json' if not args[0].endswith('.json') else args[0]
    
    # 调用创建配置的函数，不传递账号和密码
    result = await create_daily_config(user_id, username=None, password=None, filename=filename)
    await bot.send(ev, result)

# 群聊 - 清日常重置密码  
@sv.on_prefix('清日常重置密码')  
async def reset_daily_password(bot, ev: CQEvent):  
    user_id = str(ev.user_id)  
    hoshino_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  
    base_dir = os.path.join(hoshino_dir, 'modules', 'autopcr', 'cache', 'http_server')  
    user_dir = os.path.join(base_dir, user_id)  
    secret_file = os.path.join(user_dir, 'secret')  
  
    if not os.path.exists(secret_file):  
        await bot.send(ev, "❌ 未找到你的清日常配置，请先发送“清日常创建”")  
        return  
    try:  
        new_pwd = reset_secret_password_random(secret_file)  
        await bot.send(ev, f"✅ 密码已重置为随机密码：{new_pwd}\n请尽快用它登录网站并修改。")  
    except Exception as e:  
        await bot.send(ev, f"❌ 重置失败：{str(e)}")

# 群聊 - 清日常禁用
@sv.on_prefix('清日常禁用')
async def disable_daily(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().strip().split()
    if not args:
        await bot.send(ev, "❌ 请指定要禁用的文件夹名，支持批量：\n格式：清日常禁用 文件夹名1 [文件夹名2...]")
        return
    
    # 执行禁用操作
    result = update_secret_status(args, enable=False)
    
    # 构造回复消息
    msg = "【清日常禁用结果】\n"
    if result["success"]:
        msg += f"✅ 成功禁用：{', '.join(result['success'])}\n"
    if result["failed"]:
        msg += f"❌ 禁用失败：\n" + "\n".join([f"  - {item}" for item in result["failed"]])
    
    await bot.send(ev, msg)

# 群聊 - 清日常解禁
@sv.on_prefix('清日常解禁')
async def enable_daily(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().strip().split()
    if not args:
        await bot.send(ev, "❌ 请指定要解禁的文件夹名，支持批量：\n格式：清日常解禁 文件夹名1 [文件夹名2...]")
        return
    
    # 执行解禁操作
    result = update_secret_status(args, enable=True)
    
    # 构造回复消息
    msg = "【清日常解禁结果】\n"
    if result["success"]:
        msg += f"✅ 成功解禁：{', '.join(result['success'])}\n"
    if result["failed"]:
        msg += f"❌ 解禁失败：\n" + "\n".join([f"  - {item}" for item in result["failed"]])
    
    await bot.send(ev, msg)

# 私聊 - 清日常创建
# @on_command('清日常创建', aliases=('创建清日常', '初始化清日常'), permission=priv.NORMAL)
async def private_create_daily(session: CommandSession):
    user_id = str(session.event.user_id)
    args = session.current_arg_text.strip().split()
    
    username = None
    password = None
    filename = None
    
    if len(args) >= 3:
        username = args[0]
        password = args[1]
        filename = args[2] + '.json' if not args[2].endswith('.json') else args[2]
    elif len(args) == 2:
        username = args[0]
        password = args[1]
    elif len(args) == 1:
        await session.send('请输入完整的账号和密码，格式：清日常创建 账号 密码 [用户名]')
        return
    
    result = await create_daily_config(user_id, username, password, filename)
    await session.send(result)

# 私聊 - 清日常禁用
@on_command('清日常禁用', aliases=('禁用清日常',), permission=priv.NORMAL)
async def private_disable_daily(session: CommandSession):
    args = session.current_arg_text.strip().split()
    if not args:
        await session.send("❌ 请指定要禁用的文件夹名，支持批量：\n格式：清日常禁用 文件夹名1 [文件夹名2...]")
        return
    
    # 执行禁用操作
    result = update_secret_status(args, enable=False)
    
    # 构造回复消息
    msg = "【清日常禁用结果】\n"
    if result["success"]:
        msg += f"✅ 成功禁用：{', '.join(result['success'])}\n"
    if result["failed"]:
        msg += f"❌ 禁用失败：\n" + "\n".join([f"  - {item}" for item in result["failed"]])
    
    await session.send(msg)

# 私聊 - 清日常解禁
@on_command('清日常解禁', aliases=('解禁清日常',), permission=priv.NORMAL)
async def private_enable_daily(session: CommandSession):
    args = session.current_arg_text.strip().split()
    if not args:
        await session.send("❌ 请指定要解禁的文件夹名，支持批量：\n格式：清日常解禁 文件夹名1 [文件夹名2...]")
        return
    
    # 执行解禁操作
    result = update_secret_status(args, enable=True)
    
    # 构造回复消息
    msg = "【清日常解禁结果】\n"
    if result["success"]:
        msg += f"✅ 成功解禁：{', '.join(result['success'])}\n"
    if result["failed"]:
        msg += f"❌ 解禁失败：\n" + "\n".join([f"  - {item}" for item in result["failed"]])
    
    await session.send(msg)
    
# 私聊 - 清日常重置密码  
@on_command('清日常重置密码', aliases=('重置清日常密码',), permission=priv.NORMAL)  
async def private_reset_daily_password(session: CommandSession):  
    user_id = str(session.event.user_id)  
    hoshino_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  
    base_dir = os.path.join(hoshino_dir, 'modules', 'autopcr', 'cache', 'http_server')  
    user_dir = os.path.join(base_dir, user_id)  
    secret_file = os.path.join(user_dir, 'secret')  
  
    if not os.path.exists(secret_file):  
        await session.send("❌ 未找到你的清日常配置，请先发送“清日常创建”")  
        return  
    try:  
        new_pwd = reset_secret_password_random(secret_file)  
        await session.send(f"✅ 密码已重置为随机密码：{new_pwd}\n请尽快用它登录网站并修改。")  
    except Exception as e:  
        await session.send(f"❌ 重置失败：{str(e)}")    