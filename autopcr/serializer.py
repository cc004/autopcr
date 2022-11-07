from typing import _GenericAlias, Generic
from enum import Enum

def _get_annotations(cls):
    typing = {}
    if isinstance(cls, _GenericAlias): # if class is generic type with params
        for base in cls.__origin__.__orig_bases__:
            if isinstance(base, _GenericAlias):
                generic = base
                break
        else:
            raise Exception
        for typevar, type in zip(generic.__args__, cls.__args__):
            typing[typevar] = type
        cls = cls.__origin__
    if hasattr(cls, '__annotations__'):
        for name, type in cls.__annotations__.items():
            yield name, (typing[type] if type in typing else type)
    orig = (cls.__orig_bases__ if hasattr(cls, '__orig_bases__') else cls.__bases__)
    if not orig: return
    orig = orig[0]
    if cls.__bases__[0] is Generic:
        return
    yield from _get_annotations(orig)

def dump(obj, cls = None):
    if cls is None: cls = obj.__orig_class__ if hasattr(obj, '__orig_class__') else obj.__class__
    if obj is None:
        if cls is int or cls is float or isinstance(cls, type) and issubclass(cls, Enum): return 0
        return None
    if isinstance(cls, _GenericAlias) and cls.__origin__ is list:
        return [dump(i) for i in obj]
    elif cls is str or cls is int or cls is float:
        return cls(obj)
    elif isinstance(cls, type) and issubclass(cls, Enum):
        return obj.value
    else:
        return {key: val for key, val in ((name, dump(getattr(obj, name), cls1)) for name, cls1 in _get_annotations(cls)) if val is not None}

def load(obj, cls):
    if obj is None: return None
    if cls is int or cls is float or cls is str or isinstance(cls, type) and issubclass(cls, Enum):
        return cls(obj)
    elif isinstance(cls, _GenericAlias) and cls.__origin__ is list:    
        t = cls.__args__[0]
        if not isinstance(obj, list): return obj
        return [load(i, t) for i in obj]
    else:
        inst = cls()
        for name, cls in _get_annotations(cls):
            if name in obj:
                setattr(inst, name, load(obj[name], cls))
        return inst
