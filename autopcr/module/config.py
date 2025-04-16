from typing import Callable, Tuple, Union
from types import MethodType
from dataclasses import dataclass
from ..core import pcrclient
from ..model.error import SkipError
from ..db.database import db

@dataclass
class Config():
    key: str
    desc: str
    _default: Union[int, str, list, Callable]
    _candidates: Union[list, Callable]
    config_type: str
    _parent: "Module"

    async def do_check(self, client: Union[None, pcrclient] = None) -> Tuple[bool, str]: ...

    @property
    def candidates(self):
        if isinstance(self._candidates, list):
            return self._candidates
        else:
            return self._candidates()

    @property
    def default(self):
        if isinstance(self._default, Callable):
            return self._default()
        elif isinstance(self._candidates, list):
            return self._default
        else:
            candidates = self._candidates()
            ret = candidates[0] if candidates else ""
            if self.config_type == 'multi':
                ret = [item for item in candidates if item in self._default]
            return ret


    def dict(self) -> dict:
        ret = {
                "key": self.key,
                "desc": self.desc,
                "default": self.default,
                "candidates": self.candidates,
                "config_type": self.config_type,
        }
        return ret

    def get_value(self):
        return self._parent.get_config(self.key)

def _wrap_init(cls, setter):
    old = cls.__init__
    def __init__(self, *args, **kwargs):
        old(self, *args, **kwargs)
        setter(self)
    cls.__init__ = __init__

    return cls

async def _do_check(self, client: pcrclient) -> Tuple[bool, str]:
    return False, ""

def config_option(key:str, desc: str, default, candidates: Union[list, Callable] = [], config_type='str', do_check = _do_check, check: bool = False):
    from .modulebase import Module
    if isinstance(candidates, list):
        assert(not candidates or default in candidates or all(item in candidates for item in default))
    def wrapper(cls: Module):
        config = Config(key=key, desc=desc, _default=default, _candidates=candidates, config_type=config_type, _parent = cls)
        config.do_check = MethodType(do_check, config)
        cls.config[key] = config

        if check:
            old_do_check = cls.do_check
            async def new_do_check(*args, **kwargs):
                ok, msg = await old_do_check(*args, **kwargs)
                if not ok:
                    return False, msg

                ok, msg2 = await config.do_check(*args, **kwargs)
                if not ok:
                    return False, msg + msg2
                return True, msg + msg2

            cls.do_check = new_do_check

        return cls

    return lambda cls: _wrap_init(cls, wrapper)

def booltype(key: str, desc: str, default: bool):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=[True, False], config_type='bool')(cls)
    return decorator

def inttype(key: str, desc: str, default: int, candidates: Union[list, Callable]):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='int')(cls)
    return decorator

def singlechoice(key: str, desc: str, default, candidates: Union[list, Callable]):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='single')(cls)
    return decorator

def multichoice(key:str, desc: str, default, candidates: Union[list, Callable], do_check = _do_check, check: bool = False):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='multi', do_check = do_check, check = check)(cls)
    return decorator

def timetype(key:str, desc: str, default):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, config_type='time')(cls)
    return decorator

def texttype(key:str, desc: str, default):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, config_type='text')(cls)
    return decorator

def unitchoice(key: str, desc: str):
    def decorator(cls):
        return config_option(key=key, desc=desc, default="100101:日和莉", candidates=[f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unlock_unit_condition_candidate()], config_type='single')(cls)
    return decorator

def conditional_execution1(key: str, default, desc: str = "执行条件", check: bool = True): # need login
    async def do_check(self, client: pcrclient) -> Tuple[bool, str]:
        run_time = self.get_value()
        hit = [campaign for campaign in run_time if client.data.is_campaign(campaign)]
        if hit:
            return True, "今日" + ','.join(hit) + "，执行"
        return False, "今日不符合执行条件"

    return multichoice(key=key, desc=desc, default=default, candidates=["无庆典", "n庆典", "h庆典", "vh庆典", "总是执行"], do_check = do_check, check = check)

def conditional_execution2(key: str, default, desc: str = "执行条件", check: bool = True): # not need login
    async def do_check(self) -> Tuple[bool, str]:
        run_time = self.get_value()
        hit = [campaign for campaign in run_time if db.is_campaign(campaign)]
        if hit:
            return True, "今日" + ','.join(hit) + "，执行"
        return False, "今日不符合执行条件"

    return multichoice(key=key, desc=desc, default=default, candidates=['n3以上前夕','n3以上首日午前','h3以上前夕','会战前夕','会战期间','总是执行'], do_check = do_check, check = check)


def conditional_not_execution(key: str, default, desc: str = "不执行条件", check: bool = True):
    async def do_check(self, client: pcrclient) -> Tuple[bool, str]:
        run_time = self.get_value()
        hit = [campaign for campaign in run_time if client.data.is_campaign(campaign)]
        if hit:
            return False, "今日" + ','.join(hit) + "，不执行"
        return True, ""

    return multichoice(key=key, desc=desc, default=default, candidates=["n2", "n3", "n4及以上", "h2", "h3及以上", "vh2", "vh3及以上"], do_check = do_check, check = check)

def unitlist(key: str, desc: str, default=None):
    """
    角色列表选择器，用于选择多个角色
    """
    def decorator(cls):
        all_units = list(db.unlock_unit_condition_candidate())
        # 确保默认值是数组格式
        if default is None:
            default_value = []
        elif isinstance(default, list):
            default_value = default
        else:
            # 如果传入的是字符串，尝试转换为数组
            try:
                default_value = default.split(',') if default else []
            except:
                default_value = []
        
        # 添加获取配置值的包装方法，确保始终返回列表
        old_get_config = cls.get_config
        def new_get_config(self, config_key, *args, **kwargs):
            value = old_get_config(self, config_key, *args, **kwargs)
            # 只处理当前key的值
            if config_key == key:
                # 确保返回的是列表类型
                if value is None:
                    return []
                elif isinstance(value, list):
                    return value
                elif isinstance(value, str) and value:
                    try:
                        # 尝试将字符串转换为列表
                        return value.split(',')
                    except:
                        return [value]
                else:
                    # 其他类型（如整数）转换为单元素列表
                    return [value]
            return value
        
        cls.get_config = new_get_config
        
        return config_option(
            key=key, 
            desc=desc, 
            default=default_value,  # 使用数组格式的默认值
            candidates=[f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unlock_unit_condition_candidate()],
            config_type='unitlist'
        )(cls)
    return decorator

# 添加 tabletype 装饰器
def tabletype(key: str, desc: str, default: list = None):
    """表格类型配置，用于存储和显示表格数据"""
    if default is None:
        default = []
    def decorator(cls):
        # 使用与其他装饰器相同的方式添加配置
        return config_option(key=key, desc=desc, default=default, candidates=[], config_type='table')(cls)
    return decorator