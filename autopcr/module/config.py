from typing import Union
from dataclasses import dataclass


@dataclass
class Config():
    key: str
    desc: str
    default: Union[int, str, list]
    candidates: list
    config_type: str

    def dict(self) -> dict:
        return vars(self)

def _wrap_init(cls, setter, do_check = None):
    old = cls.__init__
    def __init__(self, *args, **kwargs):
        old(self, *args, **kwargs)
        setter(self)
    cls.__init__ = __init__

    if do_check:
        old_do_task = cls.do_task
        async def do_task(self, *args, **kwargs):
            await do_check(self, *args, **kwargs)
            await old_do_task(self, *args, **kwargs)
        cls.do_task = do_task

    return cls


def config_option(key:str, desc: str, default, candidates: list = [], config_type='str', do_check = None):
    from .modulebase import Module
    assert(not candidates or default in candidates or all(item in candidates for item in default))
    def wrapper(cls: Module):
        config = Config(key=key, desc=desc, default=default, candidates=candidates, config_type=config_type)
        cls.config[key] = config
        return cls

    return lambda cls: _wrap_init(cls, wrapper, do_check)

def booltype(key: str, desc: str, default: bool):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=[True, False], config_type='bool')(cls)
    return decorator

def inttype(key: str, desc: str, default: int, candidates: list):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='int')(cls)
    return decorator

def singlechoice(key: str, desc: str, default, candidates: list):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='single')(cls)
    return decorator

def multichoice(key:str, desc: str, default, candidates: list, do_check = None):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='multi', do_check = do_check)(cls)
    return decorator

def timetype(key:str, desc: str, default):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, config_type='time')(cls)
    return decorator

def conditional_execution(key: str, default, desc: str = "执行条件", check: bool = True):
    from ..core import pcrclient
    from ..model.error import SkipError
    async def do_check(self, client: pcrclient):
        run_time = set(self.get_config(key))
        if check and not (
        "无庆典" in run_time and not client.data.is_quest_campaign()
        or "n庆典" in run_time and client.data.is_normal_quest_campaign()
        or  "h庆典" in run_time and client.data.is_hard_quest_campaign()
        or  "vh庆典" in run_time and client.data.is_very_hard_quest_campaign()
        or "总是执行" in run_time):
            raise SkipError("今日不符合执行条件，不刷取")

    return multichoice(key=key, desc=desc, default=default, candidates=["无庆典", "n庆典", "h庆典", "vh庆典", "总是执行"], do_check = do_check)

