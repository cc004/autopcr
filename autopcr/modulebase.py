from .pcrclient import pcrclient
from typing import List

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
def enumtype(candidates: List[str]):
    return lambda cls:_wrap_init(cls, lambda self: (setattr(self, 'type', 'enum'), setattr(self, 'candidates', candidates)))
def booltype(cls):
    cls = _wrap_init(cls, lambda self: (setattr(self, 'type', 'bool'), setattr(self, 'candidates', [True, False])))
    old = cls.do_task
    async def do_task(self, client: pcrclient):
        if self.value: await old(self, client)
        else: raise ValueError('not enabled')
    cls.do_task = do_task
    return cls
def notimplemented(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'implmented', False))

# refers to a schudule to be done
class Module:
    def __init__(self, parent: "ModuleManager"):
        self.val = None
        self.candidates: list = []
        self.name: str = self.__class__.__name__
        self.description: str = self.name
        self.type = 'invalid'
        self.implmented = True
        self._parent = parent
    @property
    def value(self):
        return self.val
    @value.setter
    def set_value(self, val):
        if val in self.candidates:
            msg = f'{self.name()}: {self.val} => {val}'
            self.val = val
            return msg
        else:
            raise ValueError(f"Invalid value for module {self.name()}")
    async def do_task(self, client: pcrclient):
        pass
    def get_config(self, name):
        return self._parent.get_config(name)
    def generate_config(self):
        return {
            'value': self.val,
            'description': self.description,
            'candidates': self.candidates,
            'type': self.type,
            'candidate_value': self.candidates,
            'implemented': self.implmented
        }

import json
from .validator import autoValidator

class ModuleManager:
    _modules: List[type] = []

    def __init__(self, filename):
        self._filename = filename
        self.modules: List[Module] = {clazz.__name__: clazz(self) for clazz in self._modules}
        self._load_config()
    
    def _load_config(self):
        try:
            with open(self._filename, 'r') as f:
                data = json.load(f)
            self._load_from(data)
        except:
            data = {}
    
    def _load_from(self, data):
        for name, module in self.modules.items():
            if name in data:
                module.val = data[name]
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
        return {m.name(): m.generate_config() for m in self.modules}
    
    async def do_task(self):
        result = {}
        try:
            client = pcrclient({
                'account': self.data['username'],
                'password': self.data['password'],
                'channel': 1,
                'platform': 2
            }, autoValidator)
            await client.login()
            for name, module in self.modules.items():
                try:
                    await module.do_task(client)
                    result[name] = 'success'
                except Exception as e:
                    result[name] = str(e)
            result['main'] = 'success'
        except Exception as e:
            result['main'] = str(e)
        return result

