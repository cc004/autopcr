from ..core.pcrclient import pcrclient
from typing import DefaultDict, List, Dict, Tuple, Iterator
from collections import defaultdict
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
        else: raise SkipError('功能未启用')
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
        self.result = ""
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
            raise AbortError(f"Invalid value for module {self.name}")

    @abstractmethod
    async def do_task(self, client: pcrclient): ...

    def cron_hook(self) -> int:
        return None

    def get_config(self, name):
        return self._parent.get_config(name)
    def set_result(self, msg):
        self.result = msg
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
        self._crons = []
        self._load_config()
    
    def _load_config(self):
        try:
            with open(self._filename, 'r') as f:
                self.data = json.load(f)
            self._load_from(self.data)
        except:
            traceback.print_exc()
            self.data = {'username': '', 'password': '', 'alian': ''}
    
    def _load_from(self, data):
        self._crons.clear()
        for name, module in self.modules.items():
            if name in data:
                module.value = data[name]
                self.data[name] = data[name]
            cron = module.cron_hook()
            if cron: self._crons.append(cron)
        # 这里对time1和time2进行兼容
        if data.get('time1open', False): self._crons.append(int(data['time1'].split(':')[0]))
        if data.get('time2open', False): self._crons.append(int(data['time2'].split(':')[0]))
    
    def _save_config(self):
        data = {m.name: m.value for m in self.modules.values()}
        for k, v in data.items():
            self.data[k] = v
        with open(self._filename, 'w') as f:
            json.dump(self.data, f)
    
    def get_config(self, name):
        return self.modules[name].value
    
    def update_config(self, data):
        self._load_from(data)
        self._save_config()

    def generate_config(self):
        return {
            # 'username': self.data['username'],
            # 'password': self.data['password'],
            'alian': self.data['alian'],
            'qq': "",
            'username': "",
            'password': "",
            'time1': self.data['time1'] if 'time1' in self.data else None,
            'time2': self.data['time2'] if 'time2' in self.data else None,
            'time1open': self.data['time1open'] if 'time1open' in self.data else None,
            'time2open': self.data['time2open'] if 'time2open' in self.data else None,
            'data': [{'name': m.name, 'value': m.generate_config()} for m in self.modules.values()],
            'last_result': self.data.get('_last_result', None)
        }
    
    async def do_cron(self, hour):
        if hour in self._crons:
            await self.do_task()

    async def do_task(self):
        result: Dict[int, Dict[str, str]] = {}
        try:
            client = pcrclient({
                'account': self.data['username'],
                'password': self.data['password'],
                'channel': 1,
                'platform': 2
                # 'channel': 1000,
                # 'platform': 1
            })
            await client.login()
            cnt = 0
            for name in (x.__name__ for x in ModuleManager._modules):
                module = self.modules[name]
                result[cnt] = {"name": name, "value": module.value if module.type != "bool" else "", "desc": module.description, "msg": "", "status": ""}
                try:
                    module.log.clear()
                    await module.do_task(client)
                    result[cnt]["msg"] = module.result or '\n'.join(module.log) or "ok" # 哈哈，这下屎山了
                    result[cnt]["status"] = "success"
                except SkipError as e:
                    result[cnt]["msg"] = str(e)
                    result[cnt]["status"] = "skip"
                except AbortError as e:
                    result[cnt]["msg"] = str(e)
                    result[cnt]["status"] = "abort"
                except Exception as e:
                    traceback.print_exc()
                    result[cnt]["msg"] = str(e)
                    result[cnt]["status"] = "error"
                cnt += 1
        except Exception as e:
            traceback.print_exc()
            raise(e)
        finally:
            self.data['_last_result'] = result
            self._save_config()
        return result
