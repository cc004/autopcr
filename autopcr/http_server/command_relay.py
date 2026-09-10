"""  
指令中继辅助类及特殊指令处理器。  
提供 FinishSignal 异常、RelayBotEvent 伪造事件、以及不在 register_tool 中的特殊指令处理函数。  
供 httpserver.py 中的 /account/<acc>/command 路由使用。  
  
注意：本文件不注册任何路由，路由统一在 httpserver.py 的 configure_routes() 中定义。  
"""  
  
from __future__ import annotations  
import asyncio  
import datetime  
import math  
import os  
from typing import Awaitable, Callable, Dict, List  
import base64  
import io
from ..constants import DAILY_ORDER_KEY 
  
# ==================== 辅助类 ====================  
  
class FinishSignal(Exception):  
    """模拟 BotEvent.finish() 的提前返回信号"""  
    def __init__(self, msg: str):  
        self.msg = msg  
  
  
class RelayBotEvent:  
    """  
    伪造的 BotEvent 实现，供 register_tool 的 config_parser 调用。  
    只实现 config_parser 实际会用到的方法。  
    """  
  
    def __init__(self, qq: str, parts: List[str], raw: str):  
        self._qq = qq  
        self._parts = list(parts)  
        self._raw = raw  
        self._sent: List[str] = []  
  
    async def finish(self, msg: str = ""):  
        raise FinishSignal(msg)  
  
    async def send(self, msg: str = ""):  
        self._sent.append(msg)  
  
    async def target_qq(self) -> str:  
        return self._qq  
  
    async def send_qq(self) -> str:  
        return self._qq  
  
    async def group_id(self) -> str:  
        return ""  
  
    async def message(self) -> List[str]:  
        return self._parts  
  
    async def message_raw(self) -> str:  
        return self._raw  
  
    async def image(self) -> List[str]:  
        return []  
  
    async def is_admin(self) -> bool:  
        return False  
  
    async def is_super_admin(self) -> bool:  
        return False  
  
    async def get_group_member_list(self) -> List:  
        return []  
  
    async def call_action(self, *args, **kwargs) -> Dict:  
        return {}  
  
  
# ==================== 辅助函数 ====================  
def _get_cron_modules(acc):  
    """获取定时(cron)模块列表（带序号），返回 [(idx, module), ...]"""  
    modules = acc.modules_list.get_modules_list('cron')  
    return [(i + 1, m) for i, m in enumerate(modules)]  
  
  
async def handle_cron_panel(mgr, parts: List[str]) -> str:  
    """定时面板 — 返回文本版定时任务列表"""  
    indexed_modules = _get_cron_modules(mgr)  
  
    if not indexed_modules:  
        return "未找到定时任务"  
  
    lines = [f"【{mgr.alias}】定时面板", ""]  
    lines.append(f"{'序号':>4}  {'任务':<12}  {'时间':<7}  状态")  
    lines.append("-" * 40)  
    for idx, m in indexed_modules:  
        enabled = mgr.data.config.get(m.key, m.default)  
        status = "开启" if enabled else "关闭"  
        name = m.name or m.key  
        try:  
            time_val = m.get_config_display(f"time_{m.key}")  
        except Exception:  
            time_val = "-"  
        lines.append(f"{idx:>4}  {name:<12}  {time_val:<7}  {status}")  
  
    lines.append("")  
    lines.append("详情: #定时详情 序号")  
    lines.append("开关: #定时开关 序号")  
    return "\n".join(lines)

async def handle_cron_detail(mgr, parts: List[str]) -> str:  
    """定时详情 序号/名称 — 返回定时任务详细配置"""  
    if not parts:  
        return (  
            "请指定定时任务序号或名称\n"  
            "示例：#定时详情 1\n"  
            "发送 #定时面板 查看任务序号"  
        )  
  
    indexed_modules = _get_cron_modules(mgr)  
    module_target = parts[0]  
    success, failed = _match_modules([module_target], indexed_modules)  
    if failed:  
        return f"任务匹配失败: {failed[0]}"  
    mod_idx, target_module = success[0]  
  
    enabled = mgr.data.config.get(target_module.key, target_module.default)  
    config_items = list(target_module.config.items())  
  
    desc = f"\n说明: {target_module.description}" if target_module.description else ""  
    lines = [  
        f"【{mgr.alias}】{mod_idx}.{target_module.name}({target_module.key}) "  
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
    lines.append(f"设置选项: #定时设置 {mod_idx} 选项序号 值")  
    lines.append(f"开关任务: #定时开关 {mod_idx}")  
  
    return "\n".join(lines)    

async def handle_cron_toggle(mgr, parts: List[str]) -> str:  
    """定时开关 序号/名称 — 切换定时任务开启/关闭状态（可多个）"""  
    if not parts:  
        return (  
            "请指定序号或任务名，多个用空格分隔\n"  
            "示例：#定时开关 1 3\n"  
            "发送 #定时面板 查看序号"  
        )  
  
    indexed_modules = _get_cron_modules(mgr)  
    success, failed = _match_modules(parts, indexed_modules)  
  
    enabled_list = []  
    disabled_list = []  
    for idx, m in success:  
        current = mgr.data.config.get(m.key, m.default)  
        new_val = not current  
        mgr.data.config[m.key] = new_val  
        if new_val:  
            enabled_list.append(f"{idx}.{m.name}")  
        else:  
            disabled_list.append(f"{idx}.{m.name}")  
  
    lines = [f"【{mgr.alias}】"]  
    if enabled_list:  
        lines.append("已开启: " + ", ".join(enabled_list))  
    if disabled_list:  
        lines.append("已关闭: " + ", ".join(disabled_list))  
    if failed:  
        lines.append("跳过: " + ", ".join(failed))  
    return "\n".join(lines)
    
async def handle_cron_set_config(mgr, parts: List[str]) -> str:  
    """定时设置 任务序号 [选项序号] [值]"""  
    alias = mgr.alias  
  
    if not parts:  
        return (  
            "格式：\n"  
            "  #定时设置 任务序号          查看选项\n"  
            "  #定时设置 任务序号 选项序号      查看可选值\n"  
            "  #定时设置 任务序号 选项序号 值    设置\n"  
            "发送 #定时面板 查看任务序号"  
        )  
  
    indexed_modules = _get_cron_modules(mgr)  
  
    # 匹配任务  
    module_target = parts[0]  
    success, failed = _match_modules([module_target], indexed_modules)  
    if failed:  
        return f"任务匹配失败: {failed[0]}"  
    mod_idx, target_module = success[0]  
  
    config_items = list(target_module.config.items())  
  
    # 只传任务：显示选项列表  
    if len(parts) == 1:  
        if not config_items:  
            return (  
                f"【{target_module.name}】没有子选项，仅支持开关\n"  
                f"使用 #定时开关 {mod_idx}"  
            )  
  
        enabled = mgr.data.config.get(target_module.key, target_module.default)  
        status = "开启" if enabled else "关闭"  
        lines = [  
            f"【{alias}】{mod_idx}.{target_module.name} (当前:{status})",  
            ""  
        ]  
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
        lines.append(f"查看可选值: #定时设置 {mod_idx} 选项序号")  
        lines.append(f"直接设置: #定时设置 {mod_idx} 选项序号 值")  
        return "\n".join(lines)  
  
    # 匹配选项  
    option_target = parts[1]  
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
        return f"未找到选项【{option_target}】\n可用: {options}"  
  
    ctype = target_config.config_type  
    current_display = target_module.get_config_display(target_config.key)  
  
    # 只传任务+选项：显示候选值  
    if len(parts) == 2:  
        try:  
            candidates = target_config.candidates  
        except Exception:  
            candidates = []  
  
        if ctype == 'text':  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"类型: 文本，直接输入内容\n"  
                f"设置: #定时设置 {mod_idx} {option_idx} 你的文本"  
            )  
        elif ctype == 'time':  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"类型: 时间，格式 HH:MM\n"  
                f"设置: #定时设置 {mod_idx} {option_idx} 05:30"  
            )  
        elif ctype == 'bool':  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"可选: 开启 / 关闭\n"  
                f"设置: #定时设置 {mod_idx} {option_idx} 开启"  
            )  
  
        if not candidates:  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"无预设候选值，直接输入值"  
            )  
  
        # 构建候选值列表  
        current_value = target_config.get_value()  
        lines = [  
            f"【{target_module.name}】{option_idx}.{target_config.desc}",  
            f"当前: {current_display}",  
            ""  
        ]  
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
            hint = f"多选用逗号分隔: #定时设置 {mod_idx} {option_idx} 值1,值2"  
        elif ctype == 'int':  
            hint = f"直接输入数字: #定时设置 {mod_idx} {option_idx} {candidates[0]}"  
        else:  
            hint = f"输入候选值: #定时设置 {mod_idx} {option_idx} {str(target_config.candidate_display(candidates[0]))}"  
  
        lines.append("")  
        lines.append(hint)  
        return "\n".join(lines)  
  
    # 设置值  
    value_str = ' '.join(parts[2:])  
  
    # 特殊关键词：清空  
    if value_str in ('清空', '空', 'clear', 'none', '无'):  
        if ctype in ('multi', 'multi_search'):  
            final_value = []  
        elif ctype == 'text':  
            final_value = ""  
        elif ctype == 'bool':  
            final_value = False  
        else:  
            final_value = target_config.default  
  
        mgr.data.config[target_config.key] = final_value  
  
        if isinstance(final_value, list):  
            display_val = '(空)' if not final_value else ', '.join(  
                str(target_config.candidate_display(v)) for v in final_value  
            )  
        else:  
            display_val = str(target_config.candidate_display(final_value)) if final_value is not None else '(空)'  
  
        return f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}"  
  
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
            return "时间格式错误，请输入 HH:MM，如 05:30"  
        try:  
            h, m = int(tp[0]), int(tp[1])  
            if not (0 <= h < 24 and 0 <= m < 60):  
                return "时间范围错误，小时0-23，分钟0-59"  
        except ValueError:  
            return "时间格式错误，请输入数字 HH:MM"  
        final_value = tp  
  
    elif ctype == 'bool':  
        true_vals = {'开启', '开', 'true', '是', '1', 'on'}  
        false_vals = {'关闭', '关', 'false', '否', '0', 'off'}  
        if value_str.lower() in true_vals:  
            final_value = True  
        elif value_str.lower() in false_vals:  
            final_value = False  
        else:  
            return "请输入: 开启 或 关闭"  
  
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
                return f"值【{p}】不在候选范围\n可选: {', '.join(displays)}"  
  
    elif ctype == 'int':  
        try:  
            num = int(value_str)  
        except ValueError:  
            return f"请输入整数，可选: {', '.join(str(c) for c in candidates[:30])}"  
        if candidates and num not in candidates:  
            return f"值 {num} 不在可选范围\n可选: {', '.join(str(c) for c in candidates[:30])}"  
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
            return f"值【{value_str}】不在候选范围\n可选: {', '.join(displays)}"  
  
    else:  
        final_value = value_str  
  
    if final_value is None:  
        return "值解析失败"  
  
    mgr.data.config[target_config.key] = final_value  
  
    if isinstance(final_value, list):  
        if ctype == 'time':  
            display_val = f"{final_value[0]}:{final_value[1]}"  
        else:  
            display_val = ', '.join(str(target_config.candidate_display(v)) for v in final_value)  
    else:  
        display_val = str(target_config.candidate_display(final_value))  
  
    return f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}"    
  
def _get_daily_modules(acc):  
    """获取已实现的日常模块列表（带序号），返回 [(idx, module), ...]"""  
    modules = acc.modules_list.get_modules_list('daily')  
    return [(i + 1, m) for i, m in enumerate(m for m in modules if m.implmented)]  
  
  
def _match_modules(targets: list, indexed_modules: list):  
    """  
    根据用户输入匹配模块，支持序号、精确name、精确key、模糊name。  
    返回 (success_list, failed_list)  
    """  
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
  
        if target.isdigit():  
            num = int(target)  
            if num in idx_map:  
                matched = (num, idx_map[num])  
            else:  
                failed.append(f"{target}(序号不存在)")  
                continue  
        elif target in key_map:  
            matched = key_map[target]  
        elif target in name_map:  
            matched = name_map[target]  
        else:  
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

async def handle_daily_reorder(mgr, parts: List[str]) -> str:  
    """清日常排序 — 把指定功能挪到锚点功能之后"""  
    alias = mgr.alias  
    indexed_modules = _get_daily_modules(mgr)  
  
    if not parts:  
        return (  
            "把指定功能挪到某个功能之后\n"  
            "第一个是锚点功能，其余是要挪到它后面的功能\n"  
            "示例：#清日常排序 5 1 3  (把1、3挪到5后面)\n"  
            "发送 #日常面板 查看当前序号\n"  
            "发送 #清日常排序 重置 可恢复默认顺序"  
        )  
  
    # 重置  
    if len(parts) == 1 and parts[0] in ("重置", "reset", "默认"):  
        mgr.data.config.pop(DAILY_ORDER_KEY, None)  
        return f"【{alias}】已恢复默认清日常顺序"  
  
    if len(parts) < 2:  
        return "至少需要两个参数：锚点功能 + 要挪到其后的功能"  
  
    # 锚点  
    anchor_success, anchor_failed = _match_modules([parts[0]], indexed_modules)  
    if not anchor_success:  
        return f"锚点功能匹配失败: {anchor_failed[0] if anchor_failed else parts[0]}"  
    anchor_module = anchor_success[0][1]  
  
    # 要挪动的功能  
    move_success, move_failed = _match_modules(parts[1:], indexed_modules)  
    move_keys = []  
    for idx, m in move_success:  
        if m.key != anchor_module.key and m.key not in move_keys:  
            move_keys.append(m.key)  
  
    if not move_keys:  
        return "要挪动的功能不能为空，且不能与锚点相同"  
  
    # 重排  
    order = []  
    for idx, m in indexed_modules:  
        if m.key in move_keys:  
            continue  
        order.append(m.key)  
        if m.key == anchor_module.key:  
            order.extend(move_keys)  
  
    mgr.data.config[DAILY_ORDER_KEY] = order  
  
    moved_names = ", ".join(mgr.modules_list.get_module_from_key(k).name for k in move_keys)  
    lines = [f"已将 [{moved_names}] 挪到 [{anchor_module.name}] 之后"]  
    if move_failed:  
        lines.append("跳过: " + ", ".join(move_failed))  
    return f"【{alias}】清日常顺序已更新\n" + "\n".join(lines)  
  
# ==================== 特殊指令处理函数 ====================  
# 签名统一为: async def handler(mgr: Account, parts: List[str]) -> str  
# mgr 是已加载的 Account 对象（通过 wrapaccount 装饰器注入）  
# parts 是指令名之后的参数列表  
  
  
async def handle_daily_panel(mgr, parts: List[str]) -> str:  
    """日常面板 — 返回文本版模块列表"""  
    indexed_modules = _get_daily_modules(mgr)  
  
    if not indexed_modules:  
        return "未找到日常模块"  
  
    lines = [f"【{mgr.alias}】日常面板", ""]  
    lines.append(f"{'序号':>4}  {'功能':<20}  状态")  
    lines.append("-" * 40)  
    for idx, m in indexed_modules:  
        enabled = mgr.data.config.get(m.key, m.default)  
        status = "开启" if enabled else "关闭"  
        name = m.name or m.key  
        lines.append(f"{idx:>4}  {name:<20}  {status}")  
  
    return "\n".join(lines)  
  
  
async def handle_daily_detail(mgr, parts: List[str]) -> str:  
    """日常详情 模块名/序号 — 返回模块详细配置"""  
    if not parts:  
        return (  
            "请指定模块序号或名称\n"  
            "示例：#日常详情 6\n"  
            "发送 #日常面板 查看模块序号"  
        )  
  
    indexed_modules = _get_daily_modules(mgr)  
    module_target = parts[0]  
    success, failed = _match_modules([module_target], indexed_modules)  
    if failed:  
        return f"模块匹配失败: {failed[0]}"  
    mod_idx, target_module = success[0]  
  
    enabled = mgr.data.config.get(target_module.key, target_module.default)  
    config_items = list(target_module.config.items())  
  
    if not config_items:  
        return (  
            f"【{target_module.name}】没有子选项，仅支持开关\n"  
            f"使用 #日常开启/#日常关闭 {mod_idx}"  
        )  
  
    desc = f"\n说明: {target_module.description}" if target_module.description else ""  
    lines = [  
        f"【{mgr.alias}】{mod_idx}.{target_module.name}({target_module.key}) "  
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
    lines.append(f"设置选项: #日常设置 {mod_idx} 选项序号 值")  
  
    return "\n".join(lines)  
  
  
async def handle_daily_enable(mgr, parts: List[str]) -> str:  
    """日常开启 模块名/序号"""  
    if not parts:  
        return (  
            "请指定序号或功能名，多个用空格分隔\n"  
            "示例：#日常开启 1 3 5\n"  
            "示例：#日常开启 免费扭蛋 普通扭蛋\n"  
            "发送 #日常面板 查看序号"  
        )  
  
    indexed_modules = _get_daily_modules(mgr)  
    success, failed = _match_modules(parts, indexed_modules)  
  
    toggled = []  
    for idx, m in success:  
        current = mgr.data.config.get(m.key, m.default)  
        if current:  
            failed.append(f"{idx}.{m.name}(已开启)")  
        else:  
            mgr.data.config[m.key] = True  
            toggled.append(f"{idx}.{m.name}")  
  
    lines = [f"【{mgr.alias}】"]  
    if toggled:  
        lines.append("已开启: " + ", ".join(toggled))  
    if failed:  
        lines.append("跳过: " + ", ".join(failed))  
    return "\n".join(lines)  
  
  
async def handle_daily_disable(mgr, parts: List[str]) -> str:  
    """日常关闭 模块名/序号"""  
    if not parts:  
        return (  
            "请指定序号或功能名，多个用空格分隔\n"  
            "示例：#日常关闭 2 4 6\n"  
            "示例：#日常关闭 免费扭蛋 普通扭蛋\n"  
            "发送 #日常面板 查看序号"  
        )  
  
    indexed_modules = _get_daily_modules(mgr)  
    success, failed = _match_modules(parts, indexed_modules)  
  
    toggled = []  
    for idx, m in success:  
        current = mgr.data.config.get(m.key, m.default)  
        if not current:  
            failed.append(f"{idx}.{m.name}(已关闭)")  
        else:  
            mgr.data.config[m.key] = False  
            toggled.append(f"{idx}.{m.name}")  
  
    lines = [f"【{mgr.alias}】"]  
    if toggled:  
        lines.append("已关闭: " + ", ".join(toggled))  
    if failed:  
        lines.append("跳过: " + ", ".join(failed))  
    return "\n".join(lines)  
  
  
async def handle_daily_set_config(mgr, parts: List[str]) -> str:  
    """日常设置 模块序号 [选项序号] [值]"""  
    alias = mgr.alias  
  
    if not parts:  
        return (  
            "格式：\n"  
            "  #日常设置 模块序号          查看选项\n"  
            "  #日常设置 模块序号 选项序号      查看可选值\n"  
            "  #日常设置 模块序号 选项序号 值    设置\n"  
            "发送 #日常面板 查看模块序号"  
        )  
  
    indexed_modules = _get_daily_modules(mgr)  
  
    # 匹配模块  
    module_target = parts[0]  
    success, failed = _match_modules([module_target], indexed_modules)  
    if failed:  
        return f"模块匹配失败: {failed[0]}"  
    mod_idx, target_module = success[0]  
  
    config_items = list(target_module.config.items())  
  
    # 只传模块：显示选项列表  
    if len(parts) == 1:  
        if not config_items:  
            return (  
                f"【{target_module.name}】没有子选项，仅支持开关\n"  
                f"使用 #日常开启/#日常关闭 {mod_idx}"  
            )  
  
        enabled = mgr.data.config.get(target_module.key, target_module.default)  
        status = "开启" if enabled else "关闭"  
        lines = [  
            f"【{alias}】{mod_idx}.{target_module.name} (当前:{status})",  
            ""  
        ]  
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
        lines.append(f"查看可选值: #日常设置 {mod_idx} 选项序号")  
        lines.append(f"直接设置: #日常设置 {mod_idx} 选项序号 值")  
        return "\n".join(lines)  
  
    # 匹配选项  
    option_target = parts[1]  
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
        return f"未找到选项【{option_target}】\n可用: {options}"  
  
    ctype = target_config.config_type  
    current_display = target_module.get_config_display(target_config.key)  
  
    # 只传模块+选项：显示候选值  
    if len(parts) == 2:  
        try:  
            candidates = target_config.candidates  
        except Exception:  
            candidates = []  
  
        if ctype == 'text':  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"类型: 文本，直接输入内容\n"  
                f"设置: #日常设置 {mod_idx} {option_idx} 你的文本"  
            )  
        elif ctype == 'time':  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"类型: 时间，格式 HH:MM\n"  
                f"设置: #日常设置 {mod_idx} {option_idx} 05:30"  
            )  
        elif ctype == 'bool':  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"可选: 开启 / 关闭\n"  
                f"设置: #日常设置 {mod_idx} {option_idx} 开启"  
            )  
  
        if not candidates:  
            return (  
                f"【{target_module.name}】{option_idx}.{target_config.desc}\n"  
                f"当前: {current_display}\n"  
                f"无预设候选值，直接输入值"  
            )  
  
        # 构建候选值列表  
        current_value = target_config.get_value()  
        lines = [  
            f"【{target_module.name}】{option_idx}.{target_config.desc}",  
            f"当前: {current_display}",  
            ""  
        ]  
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
            hint = f"多选用逗号分隔: #日常设置 {mod_idx} {option_idx} 值1,值2"  
        elif ctype == 'int':  
            hint = f"直接输入数字: #日常设置 {mod_idx} {option_idx} {candidates[0]}"  
        else:  
            hint = f"输入候选值: #日常设置 {mod_idx} {option_idx} {str(target_config.candidate_display(candidates[0]))}"  
  
        lines.append("")  
        lines.append(hint)  
        return "\n".join(lines)  
  
    # 设置值  
    value_str = ' '.join(parts[2:])  
  
    # 特殊关键词：清空  
    if value_str in ('清空', '空', 'clear', 'none', '无'):  
        if ctype in ('multi', 'multi_search'):  
            final_value = []  
        elif ctype == 'text':  
            final_value = ""  
        elif ctype == 'bool':  
            final_value = False  
        else:  
            final_value = target_config.default  
  
        mgr.data.config[target_config.key] = final_value  
  
        if isinstance(final_value, list):  
            display_val = '(空)' if not final_value else ', '.join(  
                str(target_config.candidate_display(v)) for v in final_value  
            )  
        else:  
            display_val = str(target_config.candidate_display(final_value)) if final_value is not None else '(空)'  
  
        return f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}"  
  
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
            return "时间格式错误，请输入 HH:MM，如 05:30"  
        try:  
            h, m = int(tp[0]), int(tp[1])  
            if not (0 <= h < 24 and 0 <= m < 60):  
                return "时间范围错误，小时0-23，分钟0-59"  
        except ValueError:  
            return "时间格式错误，请输入数字 HH:MM"  
        final_value = tp  
  
    elif ctype == 'bool':  
        true_vals = {'开启', '开', 'true', '是', '1', 'on'}  
        false_vals = {'关闭', '关', 'false', '否', '0', 'off'}  
        if value_str.lower() in true_vals:  
            final_value = True  
        elif value_str.lower() in false_vals:  
            final_value = False  
        else:  
            return "请输入: 开启 或 关闭"  
  
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
                return f"值【{p}】不在候选范围\n可选: {', '.join(displays)}"  
  
    elif ctype == 'int':  
        try:  
            num = int(value_str)  
        except ValueError:  
            return f"请输入整数，可选: {', '.join(str(c) for c in candidates[:30])}"  
        if candidates and num not in candidates:  
            return f"值 {num} 不在可选范围\n可选: {', '.join(str(c) for c in candidates[:30])}"  
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
            return f"值【{value_str}】不在候选范围\n可选: {', '.join(displays)}"  
  
    else:  
        final_value = value_str  
  
    if final_value is None:  
        return "值解析失败"  
  
    mgr.data.config[target_config.key] = final_value  
  
    if isinstance(final_value, list):  
        if ctype == 'time':  
            display_val = f"{final_value[0]}:{final_value[1]}"  
        else:  
            display_val = ', '.join(str(target_config.candidate_display(v)) for v in final_value)  
    else:  
        display_val = str(target_config.candidate_display(final_value))  
  
    return f"【{alias}】{target_module.name}\n{target_config.desc}: {display_val}"  
  
  
async def handle_daily_report(mgr, parts: List[str]) -> dict:  
    """日常报告 [0|1|2|3] — 查看最近清日常报告"""  
    result_id = 0  
    if parts:  
        try:  
            result_id = int(parts[0])  
        except Exception:  
            pass  
  
    resp = await mgr.get_daily_result_from_id(result_id)  
    if not resp:  
        return "未找到日常报告"  
  
    from ..util.draw import instance as drawer  
    img = await drawer.draw_tasks_result(resp, skip_skipped=True)
    buf = io.BytesIO()  
    img.save(buf, format='PNG')  
    image_b64 = base64.b64encode(buf.getvalue()).decode()  
    return {"text": f"【{mgr.alias}】日常报告 #{result_id}", "image": image_b64} 
  
  
async def handle_daily_record(mgr, parts: List[str]) -> str:  
    """日常记录 — 查看清日常时间记录（需要遍历所有账号，但这里只能看当前账号）"""  
    daily_results = mgr.get_daily_result_list()  
    if not daily_results:  
        return f"【{mgr.alias}】暂无日常记录"  
  
    lines = [f"【{mgr.alias}】日常记录", ""]  
    lines.append(f"{'昵称':<12}  {'清日常时间':<20}  状态")  
    lines.append("-" * 50)  
    for dr in daily_results:  
        status = dr.status.value if hasattr(dr.status, 'value') else str(dr.status)  
        lines.append(f"{mgr.alias:<12}  {dr.time:<20}  {status}")  
  
    return "\n".join(lines)  
  
  
async def handle_cron_log(mgr, parts: List[str]) -> str:  
    """定时日志 — 查看定时运行状态"""  
    try:  
        from ..module.crons import CRONLOG_PATH, CronLog  
        from ..module.modulebase import eResultStatus  
    except ImportError:  
        return "无法加载定时日志模块"  
  
    if not os.path.exists(CRONLOG_PATH):  
        return "暂无定时日志"  
  
    try:  
        with open(CRONLOG_PATH, 'r') as f:  
            logs = [CronLog.from_json(line.strip()) for line in f.readlines() if line.strip()]  
    except Exception as e:  
        return f"读取定时日志失败: {e}"  
  
    cur = datetime.datetime.now()  
  
    # 支持过滤参数  
    if '错误' in parts:  
        logs = [log for log in logs if log.status == eResultStatus.ERROR]  
    if '警告' in parts:  
        logs = [log for log in logs if log.status == eResultStatus.WARNING]  
    if '成功' in parts:  
        logs = [log for log in logs if log.status == eResultStatus.SUCCESS]  
    if '昨日' in parts:  
        cur -= datetime.timedelta(days=1)  
        logs = [log for log in logs if log.time.date() == cur.date()]  
    if '今日' in parts:  
        logs = [log for log in logs if log.time.date() == cur.date()]  
  
    logs = logs[-40:]  
    logs = logs[::-1]  
  
    if not logs:  
        return "暂无定时日志"  
  
    lines = ["定时日志（最近40条）", ""]  
    for log in logs:  
        lines.append(str(log))  
  
    return "\n".join(lines)  
  
  
async def handle_clean_daily(mgr, parts: List[str]) -> dict:  
    """清日常 — 执行清日常"""  
    try:  
        clan = mgr._parent.secret.clan  
        res = await asyncio.wait_for(  
            mgr.do_daily(clan),  
            timeout=600  
        )  
        resp = res.get_result()  
  
        from ..util.draw import instance as drawer  
        img = await drawer.draw_tasks_result(resp)  
        buf = io.BytesIO()  
        img.save(buf, format='PNG')  
        image_b64 = base64.b64encode(buf.getvalue()).decode()  
        return {"text": f"【{mgr.alias}】清日常完成", "image": image_b64}  
    except asyncio.TimeoutError:  
        return "清日常超时（10分钟），请稍后重试"  
    except Exception as e:  
        return f"清日常失败: {e}"
  
  
async def handle_gacha_current(mgr, parts: List[str]) -> str:  
    """卡池 — 查看当前卡池"""  
    try:  
        from ..db.database import db  
        gacha_list = db.get_mirai_gacha()  
        if not gacha_list:  
            return "当前没有可用卡池"  
        return "\n".join(gacha_list)  
    except Exception as e:  
        return f"获取卡池失败: {e}"  
  
  
# ==================== 特殊指令注册表 ====================  
# key = 指令前缀（不含#），value = handler 函数  
# handler 签名: async def handler(mgr: Account, parts: List[str]) -> str  
  
SPECIAL_HANDLERS: Dict[str, Callable[..., Awaitable[str]]] = {  
    "日常面板": handle_daily_panel,  
    "日常详情": handle_daily_detail,  
    "日常开启": handle_daily_enable,  
    "日常关闭": handle_daily_disable,  
    "日常设置": handle_daily_set_config,  
    "日常报告": handle_daily_report,  
    "日常记录": handle_daily_record,  
    "定时日志": handle_cron_log,  
    "清日常排序": handle_daily_reorder,  
    "清日常": handle_clean_daily,  
    "卡池": handle_gacha_current,  
    "定时面板": handle_cron_panel,  
    "定时详情": handle_cron_detail,  
    "定时开关": handle_cron_toggle,  
    "定时设置": handle_cron_set_config,
}