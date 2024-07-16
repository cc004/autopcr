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
    _default: Union[int, str, list]
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
        if isinstance(self._candidates, list):
            return self._default
        else:
            candidates = self._candidates()
            ret = candidates[0] if candidates else ""
            return ret if self.config_type != "multi" else []

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

                ok, msg = await config.do_check(*args, **kwargs)
                if not ok:
                    return False, msg
                return True, ""

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

