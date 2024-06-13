from abc import abstractmethod
from dataclasses import dataclass
import datetime
from dataclasses_json import dataclass_json
from ..core.pcrclient import pcrclient
from ..model.error import *
from ..model.enums import *
from typing import Dict
import traceback
from ..constants import CACHE_DIR
from .config import Config, _wrap_init

def default(val):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'default', val))

def description(desc: str):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'description', desc))

def name(desc: str):
    return lambda cls:_wrap_init(cls, lambda self: setattr(self, 'name', desc))

def notimplemented(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'implmented', False))

def notrunnable(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'runnable', False))

def stamina_relative(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'stamina_relative', True))

def text_result(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'text_result', True))

@dataclass_json
@dataclass
class ModuleResult:
    name: str = ""
    config: str = ""
    log: str = ""
    status: str = ""

# refers to a schudule to be done
class Module:

    def __init__(self, parent):
        self.key: str = self.__class__.__name__
        self.name: str = ""
        self.default: bool = False
        self.runnable: bool = True
        self.text_result: bool = False
        self.stamina_relative: bool = False
        self.description: str = self.name
        self.config: Dict[str, Config] = {}
        self.implmented = True
        from .modulemgr import ModuleManager
        self._parent: ModuleManager = parent
        self.log = []

        from os.path import join
        self.cache_path: str = join(CACHE_DIR, "modules", self.key, self._parent.parent.id + ".json")
        self.cache_ready = False
        self._cache = {}

    def init_cache(self):
        from os.path import exists
        if not exists(self.cache_path):
            from os import makedirs
            from os.path import dirname
            makedirs(dirname(self.cache_path), exist_ok = True)
            with open(self.cache_path, "w") as f:
                f.write("{}")

        with open(self.cache_path, "r") as f:
            import json
            self._cache = json.load(f)
            self.cache_ready = True

    def find_cache(self, key):
        if not self.cache_ready:
            self.init_cache()

        return self._cache.get(key, None)

    def save_cache(self, key, value):
        if not self.cache_ready:
            self.init_cache()

        self._cache[key] = value
        with open(self.cache_path, "w") as f:
            import json
            json.dump(self._cache, f)

    @abstractmethod
    async def do_task(self, client: pcrclient): ...

    async def do_from(self, client: pcrclient) -> ModuleResult:
        result: ModuleResult = ModuleResult(
                name=self.name,
                config = '\n'.join([f"{self.config[key].desc}: {self.get_config_str(key)}" for key in self.config]),
                status = "",
                log = "",
            )
        try:
            self.log.clear()

            if self.get_config(self.key):
                if self.stamina_relative and client.keys.get('stamina_relative_not_run', False):
                    raise SkipError('体力相关，不执行')

                await self.do_task(client)
            else:
                raise SkipError('功能未启用')


            result.status = "success"
        except SkipError as e:
            result.log = str(e)
            result.status = "skip"
        except AbortError as e:
            result.log = str(e)
            result.status = "abort"
        except Exception as e:
            traceback.print_exc()
            result.log = str(e)
            result.status = "error"
        finally:
            result.log = ('\n'.join(self.log) + "\n" + result.log).strip() or "ok"

        return result

    def cron_hook(self) -> int:
        return None

    def get_config_str(self, key) -> str:
        value = self.get_config(key)
        if isinstance(value, list):
            value = ','.join(map(str, value))
        return str(value)

    def get_config_instance(self, key):
        if key not in self.config:
            raise ValueError(f"config {key} not found")
        return self.config[key]

    def get_config(self, key):
        if key == self.key:
            default = self.default
        else:
            default = self.config[key].default
        value = self._parent.get_config(key, default)
        if key in self.config and self.config[key].config_type == "multi":
            if not isinstance(value, list):
                value = default
            else:
                value = [v for v in value if v in self.config[key].candidates]
        if key != self.key and self.config[key].candidates and (
            not isinstance(value, list) and (
                value not in self.config[key].candidates or 
                self.config[key].config_type == "multi"
                ) or
            isinstance(value, list) and any(item not in self.config[key].candidates for item in value)
            ):
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
                'config_order': list(self.generate_config().keys()),
                'implemented': self.implmented,
                'stamina_relative': self.stamina_relative,
                'runnable': self.runnable,
                'text_result': self.text_result
                }

    def _log(self, msg):
        self.log.append(msg)

