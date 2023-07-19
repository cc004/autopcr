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

def _wrap_init(cls, setter):
    old = cls.__init__
    def __init__(self, *args, **kwargs):
        old(self, *args, **kwargs)
        setter(self)
    cls.__init__ = __init__
    return cls


def config_option(key:str, desc: str, default, candidates: list = [], config_type='str'):
    from .modulebase import Module
    def wrapper(cls: Module):
        config = Config(key=key, desc=desc, default=default, candidates=candidates, config_type=config_type)
        cls.config[key] = config
        return cls

    return lambda cls: _wrap_init(cls, wrapper)

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

def multichoice(key:str, desc: str, default, candidates: list):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, candidates=candidates, config_type='multi')(cls)
    return decorator

def timetype(key:str, desc: str, default):
    def decorator(cls):
        return config_option(key=key, desc=desc, default=default, config_type='time')(cls)
    return decorator
