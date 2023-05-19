from ..core.pcrclient import pcrclient
from typing import List, Dict, Iterator
from abc import abstractmethod
from ..model.error import *

def _wrap_init(cls, setter):
    old = cls.__init__
    def __init__(self, *args, **kwargs):
        old(self, *args, **kwargs)
        setter(self)
    cls.__init__ = __init__
    return cls

def default(val):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'val', val))
def description(desc: str):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'description', desc))
def enumtype(candidates: list):
    return lambda cls:_wrap_init(cls, lambda self: (setattr(self, 'type', 'enum'), setattr(self, 'candidates', candidates)))
def booltype(cls):
    cls = _wrap_init(cls, lambda self: (setattr(self, 'type', 'bool'), setattr(self, 'candidates', [True, False])))
    old = cls.do_task
    async def do_task(self, client: pcrclient):
        if self.value: await old(self, client)
        else: raise SkipError('not enabled')
    cls.do_task = do_task
    return cls
def notimplemented(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'implmented', False))

# refers to a schudule to be done
class Module:
    def __init__(self, parent: "ModuleManager"):
        self._val = None
        self.candidates: list = []
        self.name: str = self.__class__.__name__
        self.description: str = self.name
        self.type = 'invalid'
        self.implmented = True
        self._parent = parent
        self.log = []
    @property
    def value(self):
        return self._val
    @value.setter
    def value(self, val):
        try:
            iv = int(val)
            if iv in self.candidates: val = iv
        except:
            pass
        if val in self.candidates:
            msg = f'{self.name}: {self._val} => {val}'
            self._val = val
            return msg
        else:
            raise AbortError(f"Invalid value for module {self.name()}")

    @abstractmethod
    async def do_task(self, client: pcrclient): ...

    def get_config(self, name):
        return self._parent.get_config(name)
    def generate_config(self):
        return {
            'value': self.value,
            'description': self.description,
            'candidates': self.candidates,
            'type': self.type,
            'candidate_value': self.candidates,
            'implemented': self.implmented
        }

    def _log(self, msg):
        self.log.append(msg)

import json
import traceback
class ModuleManager:
    _modules: List[type] = []

    def __init__(self, filename):
        self._filename = filename
        self.modules: Dict[str, Module] = {clazz.__name__: clazz(self) for clazz in self._modules}
        self._load_config()
    
    def _load_config(self):
        try:
            with open(self._filename, 'r') as f:
                data = json.load(f)
            self._load_from(data)
        except:
            traceback.print_exc()
            self.data = {'username': '', 'password': ''}
    
    def _load_from(self, data):
        for name, module in self.modules.items():
            if name in data:
                module.value = data[name]
        self.data = data
    
    def _save_config(self):
        data = {m.name(): m.value for m in self.modules.values()}
        with open(self._filename, 'w') as f:
            json.dump(data, f)
    
    def get_config(self, name):
        return self.modules[name].value
    
    def update_config(self, data):
        self._load_from(data)
        self._save_config()

    def generate_config(self):
        return {
            'username': self.data['username'],
            'password': self.data['password'],
            'data': {m.name: m.generate_config() for m in self.modules.values()}
        }
    
    async def do_task(self):
        result = {}
        try:
            client = pcrclient({
                'account': self.data['username'],
                'password': self.data['password'],
                'channel': 1,
                'platform': 2
            })
            await client.login()
            for name in (x.__name__ for x in ModuleManager._modules):
                module = self.modules[name]
                try:
                    module.log.clear()
                    await module.do_task(client)
                    result[name] = {
                        'status': 'success',
                        'log': module.log
                    }
                except Exception as e:
                    result[name] = {
                        'status': 'failed',
                        'log': module.log,
                        'error': str(e)
                    }
            result['main'] = {
                'status': 'success'
            }
        except Exception as e:
            result['main'] = {
                'status': 'failed',
                'error': str(e)
            }
        print(json.dumps(result, indent=4))
        return result

