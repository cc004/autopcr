from abc import abstractmethod
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from ..core.pcrclient import eLoginStatus, pcrclient
from ..model.error import *
from ..model.enums import *
from typing import Dict, List, Tuple, Union
from ..constants import CACHE_DIR
from .config import Config, _wrap_init
from enum import Enum
from datetime import datetime
from ..db.database import db
from ..util.logger import instance as logger

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

def notlogin(check_data = False):
    def setter(self):
        self.tags.append("不登录")
        self.need_login = False
        old_do_check = self.do_check
        async def new_do_check(client: pcrclient) -> Tuple[bool, str]:
            ok, msg = await old_do_check(client)
            if not ok: 
                return ok, msg
            if check_data and not client.data.ready:
                return False, '无缓存，请登录'
            return True, ''
        self.do_check = new_do_check
        if check_data:
            old_do_task = self.do_task
            async def new_do_task(client: pcrclient):
                self._log(f"[{db.format_time(datetime.fromtimestamp(client.data.data_time))}]")
                await old_do_task(client)
            self.do_task = new_do_task


    return lambda cls: _wrap_init(cls, setter)

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

HeaderItem = Union[str, Dict[str, List['HeaderItem']]]
DataItem = Union[str, int, Dict[str, 'DataItem']]

@dataclass_json
@dataclass
class ResultTable:
    header: List[HeaderItem] = field(default_factory=list)
    data: List[Dict[str, DataItem]] = field(default_factory=list)

    def __bool__(self):
        return bool(self.data)

@dataclass_json
@dataclass
class ModuleResult:
    name: str = ""
    config: str = ""
    log: str = ""
    table: ResultTable = field(default_factory=ResultTable)
    status: eResultStatus = eResultStatus.SUCCESS

# refers to a schudule to be done
class Module:

    def __init__(self, parent):
        self.key: str = self.__class__.__name__
        self.name: str = ""
        self.default: bool = False
        self.runnable: bool = True
        self.tags: List[str] = []
        self.stamina_relative: bool = False
        self.description: str = self.name
        self.config: Dict[str, Config] = {}
        self.implmented = True
        self.need_login = True
        from .modulemgr import ModuleManager
        self._parent: ModuleManager = parent
        self.log = []
        self.warn = []
        self.is_warn = False
        self.table: ResultTable = ResultTable()

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
                config = '\n'.join([f"{self.config[key].desc}: {self.get_config_display(key)}" for key in self.config]),
            )
        try:
            self.log.clear()
            self.warn.clear()

            if self.need_login:
                if client.logged == eLoginStatus.NOT_LOGGED or not client.data.ready:
                    await client.login()
                elif client.logged == eLoginStatus.NEED_REFRESH:
                    client.data.update_stamina_recover()
                    await client.refresh()

            ok, msg = await self.do_check(client)
            if not ok:
                raise SkipError(msg)
            elif msg:
                self._log(msg)

            await self.do_task(client)

            if self.is_warn:
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
            logger.exception(e)
            result.log = str(e)
            result.status = eResultStatus.ERROR
        finally:
            result.log = ('\n'.join(self.log) + "\n" + result.log).strip() or "ok"
            result.table = self.table

        return result

    def cron_hook(self) -> int:
        return None

    def _get_raw_config(self, key, default = None):
        return self._parent.get_config(key, default)

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
            return self._get_raw_config(key, self.default)
        elif key in self.config:
            return self.config[key].get_value()
        else:
            raise ValueError(f"config {key} not found")

    def get_config_display(self, key):
        return self.get_config_instance(key).get_display()

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
                }

    def _table_header(self, header: List):
        self.table.header = header

    def _table(self, table: Dict):
        self.table.data.append(table)

    def _log(self, msg: str):
        self.log.append(msg)

    def _warn(self, msg: str):
        self.is_warn = True
        self.log.append("! " + msg)

    def _abort(self, msg: str = ""):
        raise AbortError(msg)
