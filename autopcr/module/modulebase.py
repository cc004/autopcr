from abc import abstractmethod
from ..core.pcrclient import pcrclient
from ..model.error import *
from ..model.enums import *
from typing import Dict
from .config import Config, _wrap_init
import traceback

def default(val):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'default', val))

def description(desc: str):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'description', desc))

def name(desc: str):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'name', desc))

def booltype(cls):
    old = cls.do_task
    async def do_task(self, client: pcrclient):
        if self.get_config(cls.key):
            return await old(self, client)
        else:
            raise SkipError('功能未启用')
    cls.do_task = do_task
    return cls

def notimplemented(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'implmented', False))

# refers to a schudule to be done
class Module:

    def __init__(self, parent):
        self.key: str = self.__class__.__name__
        self.name: str = ""
        self.default: bool = False
        self.description: str = self.name
        self.config: Dict[str, Config] = {}
        self.implmented = True
        from .modulemgr import ModuleManager
        self._parent: ModuleManager = parent
        self.log = []

    @abstractmethod
    async def do_task(self, client: pcrclient): ...

    async def do_from(self, client: pcrclient):
        result = {
                "name": self.name,
                "status": "",
                "log" : "",
                }
        try:
            self.log.clear()
            await self.do_task(client)
            result["status"] = "success"
        except SkipError as e:
            result["log"] = str(e)
            result["status"] = "skip"
        except AbortError as e:
            result["log"] = str(e)
            result["status"] = "abort"
        except Exception as e:
            traceback.print_exc()
            result["log"] = str(e)
            result["status"] = "error"
        finally:
            result['log'] = ('\n'.join(self.log) + "\n" + result['log']).strip() or "ok"

        return result

    def cron_hook(self) -> int:
        return None

    def get_config(self, key):
        if key == self.key:
            default = self.default
        else:
            default = self.config[key].default
        value = self._parent.get_config(key, default)
        if key != self.key and self.config[key].candidates and value not in self.config[key].candidates:
            value = default
        return value

    def generate_config(self):
        return {key: self.config[key].dict() for key in self.config}

    def generate_info(self):
        return {
                'key': self.key,
                'name': self.name,
                'description': self.description,
                'config': self.generate_config(),
                'implemented': self.implmented
                }

    def _log(self, msg):
        self.log.append(msg)

