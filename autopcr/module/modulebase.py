from abc import abstractmethod
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from ..core.pcrclient import pcrclient
from ..model.error import *
from ..model.enums import *
from typing import Dict, List, Tuple
import traceback
from ..constants import CACHE_DIR
from .config import Config, _wrap_init
from enum import Enum

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

def tag_stamina_consume(cls):
    def setter(self):
        self.tags.append("体力消耗")
        self.stamina_relative = True
        old_do_check = self.do_check
        async def new_do_check(client: pcrclient) -> Tuple[bool, str]:
            ok, msg = await old_do_check(client)
            if not ok: 
                return ok, msg
            if client.is_stamina_consume_not_run():
                return False, '体力消耗，不执行'
            return True, ''
        self.do_check = new_do_check

    return _wrap_init(cls, setter)

def tag_stamina_get(cls):
    def setter(self):
        self.tags.append("体力获取")
        self.stamina_relative = True
        old_do_check = self.do_check
        async def new_do_check(client: pcrclient) -> Tuple[bool, str]:
            ok, msg = await old_do_check(client)
            if not ok: 
                return ok, msg
            if client.is_stamina_get_not_run():
                return False, '体力获取，不执行'
            return True, ''
        self.do_check = new_do_check
    return _wrap_init(cls, setter)

def text_result(cls):
    return _wrap_init(cls, lambda self: setattr(self, 'text_result', True))

class eResultStatus(str, Enum):
    SUCCESS = "成功"
    SKIP = "跳过"
    WARNING = "警告"
    ABORT = "中止"
    ERROR = "错误"
    PANIC = "致命"
    @classmethod
    def _missing_(cls, value):
        old = {
            'success': cls.SUCCESS,
            'skip': cls.SKIP,
            'warning': cls.WARNING,
            'abort': cls.ABORT,
            'error': cls.ERROR,
            'panic': cls.PANIC
        }
        if value in old:
            return old[value]
        return ValueError(f"{value} not found in eResultStatus")

@dataclass_json
@dataclass
class ModuleResult:
    name: str = ""
    config: str = ""
    log: str = ""
    status: eResultStatus = eResultStatus.SUCCESS

# refers to a schudule to be done
class Module:

    def __init__(self, parent):
        self.key: str = self.__class__.__name__
        self.name: str = ""
        self.default: bool = False
        self.runnable: bool = True
        self.text_result: bool = False
        self.tags: List[str] = []
        self.stamina_relative: bool = False
        self.description: str = self.name
        self.config: Dict[str, Config] = {}
        self.implmented = True
        from .modulemgr import ModuleManager
        self._parent: ModuleManager = parent
        self.log = []
        self.warn = []

        from os.path import join
        self.cache_path: str = join(CACHE_DIR, "modules", self.key, self._parent.id + ".json")
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

    async def do_check(self, client: pcrclient) -> Tuple[bool, str]:
        enable = self.get_config(self.key)
        if not enable:
            return False, "功能未启用"
        else:
            return True, ""

    async def do_from(self, client: pcrclient) -> ModuleResult:
        result: ModuleResult = ModuleResult(
                name=self.name,
                config = '\n'.join([f"{self.config[key].desc}: {self.get_config_str(key)}" for key in self.config]),
            )
        try:
            self.log.clear()
            self.warn.clear()

            if not client.logged:
                await client.login()

            ok, msg = await self.do_check(client)
            if not ok:
                raise SkipError(msg)
            elif msg:
                self._log(msg)

            await self.do_task(client)

            if self.warn:
                result.status = eResultStatus.WARNING
            else:
                result.status = eResultStatus.SUCCESS
        except SkipError as e:
            result.log = str(e)
            result.status = eResultStatus.SKIP
        except AbortError as e:
            result.log = str(e)
            result.status = eResultStatus.ABORT
        except PanicError as e:
            result.log = str(e)
            result.status = eResultStatus.PANIC
        except Exception as e:
            traceback.print_exc()
            result.log = str(e)
            result.status = eResultStatus.ERROR
        finally:
            result.log = ('\n'.join(self.warn + 
                                    (['----'] if self.warn and self.log else []) +
                                    self.log) + "\n" + result.log).strip() or "ok"

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

    def generate_config(self) -> dict:
        return {key: self.config[key].dict() for key in self.config}

    def generate_info(self) -> dict:
        return {
                'key': self.key,
                'name': self.name,
                'description': self.description,
                'config': self.generate_config(),
                'config_order': list(self.generate_config().keys()),
                'implemented': self.implmented,
                'stamina_relative': self.stamina_relative,
                'tags': self.tags,
                'runnable': self.runnable,
                'text_result': self.text_result
                }

    def _log(self, msg: str):
        self.log.append(msg)

    def _warn(self, msg: str):
        self.log.append(msg)
        self.warn.append(msg)

    def _abort(self, msg: str = ""):
        raise AbortError(msg)
