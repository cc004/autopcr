# 名字需要斟酌一下

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from ..core.pcrclient import pcrclient
from ..core.sdkclient import account, platform
from .modulemgr import ModuleManager, TaskResult, ModuleResult
from ..sdk.sdkclients import create
import os, re, shutil
from typing import Any, Dict, Iterator, List, Union
from ..constants import CONFIG_PATH, OLD_CONFIG_PATH, RESULT_DIR, BSDK, CHANNEL_OPTION
from asyncio import Lock
import json
from copy import deepcopy
import hashlib
from ..db.database import db
import datetime
import traceback

class AccountException(Exception):
    pass
class UserException(Exception):
    pass

@dataclass_json
@dataclass
class DailyResult:
    path: str = ""
    time: str = "无"
    time_safe: str = "无"
    status: str = "skip"

    def safe_info(self) -> "DailyResult":
        return DailyResult(path = "", time = self.time, time_safe = self.time_safe, status = self.status)

@dataclass_json
@dataclass
class AccountData:
    username: str = ""
    password: str = ""
    channel: str = BSDK
    config: Dict[str, Any] = field(default_factory=dict)
    daily_result: List[DailyResult] = field(default_factory=list)

@dataclass_json
@dataclass
class UserData:
    password: str = ""
    default_account: str = ""

class Account(ModuleManager):
    def __init__(self, parent: 'AccountManager', qid: str, account: str, readonly: bool = False):
        if not account in parent.account_lock:
            parent.account_lock[account] = Lock()
        self._lck = parent.account_lock[account]
        self._filename = parent.path(account)
        self._parent = parent
        self.readonly = readonly
        self.id = hashlib.md5(account.encode('utf-8')).hexdigest()

        if not os.path.exists(self._filename):
            raise AccountException("账号不存在")

        with open(self._filename, 'r') as f:
            self.data: AccountData = AccountData.from_json(f.read())
            self.old_data: AccountData = deepcopy(self.data)

        self.qq = qid
        self.alias = account
        self.token = f"{self.qq}_{self.alias}"
        super().__init__(self.data.config, self)
    
    async def __aenter__(self):
        if not self.readonly:
            await self._lck.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.readonly:
            if self.data != self.old_data:
                await self.save_data()
            self._lck.release()

    async def save_data(self):
        with open(self._filename, 'w') as f:
            f.write(self.data.to_json())

    async def save_daily_result(self, result: TaskResult, status: str):
        now = datetime.datetime.now()
        time_safe = db.format_time_safe(now)
        file = os.path.join(RESULT_DIR, f"{self.token}_daily_{time_safe}.json")
        with open(file, 'w') as f:
            f.write(result.to_json())

        old_list = self.data.daily_result
        while len(old_list) >= 4:
            if os.path.exists(old_list[-1].path):
                os.remove(old_list[-1].path)
            old_list.pop()
        item = DailyResult(path = file, time = db.format_time(now), time_safe=time_safe, status = status)
        self.data.daily_result = [item] + old_list

    async def save_single_result(self, module: str, result: ModuleResult):
        file = os.path.join(RESULT_DIR, f"{self.token}_{module}.json")
        with open(file, 'w') as f:
            f.write(result.to_json())

    async def get_daily_result_from_id(self, id: int = 0) -> Union[None, TaskResult]:
        if len(self.data.daily_result) > id:
            try:
                with open(self.data.daily_result[id].path, 'r') as f:
                    return TaskResult.from_json(f.read())
            except Exception as e:
                traceback.print_exc()
                return None
        else:
            return None

    async def get_daily_result_from_time(self, safe_time: str) -> Union[None, TaskResult]:
        ret = [daily_result.path for daily_result in self.data.daily_result if safe_time == daily_result.time_safe]
        if ret:
            with open(ret[0], 'r') as f:
                return TaskResult.from_json(f.read())
        else:
            return None

    async def get_single_result(self, module) -> Union[None, ModuleResult]:
        file = os.path.join(RESULT_DIR, f"{self.token}_{module}.json")
        if os.path.exists(file):
            with open(file, 'r') as f:
                return ModuleResult.from_json(f.read())
        else:
            return None

    def get_last_daily_clean(self) -> DailyResult:
        if self.data.daily_result:
            return self.data.daily_result[0].safe_info()
        else:
            return DailyResult()

    def get_client(self) -> pcrclient:
        return self.get_android_client()

    def get_ios_client(self) -> pcrclient: # Header TODO
        client = pcrclient(create(self.data.channel, account(
            self.data.username,
            self.data.password,
            platform.IOS
        )))
        return client

    def get_android_client(self) -> pcrclient:
        client = pcrclient(create(self.data.channel, account(
            self.data.username,
            self.data.password,
            platform.Android
        )))
        return client

    def generate_info(self):
        def _mask_str(mask_str: str) -> str:
            if not isinstance(mask_str, str):
                raise ValueError("Input must be a string")
            elif not mask_str:
                return ""
            else:
                return "*" * 7 + mask_str[-1]
        return {
            'alias': self.alias,
            'username': self.data.username,
            'password': 8 * "*" if self.data.password else "",
            'channel': self.data.channel,
            'channel_option': CHANNEL_OPTION,
            'area': [{"key": 'daily', "name":"日常"}, {"key": 'tools', "name":"工具"}]
        }

    def generate_result_info(self):
        ret = {
            'name': self.alias,
            'daily_clean_time': self.get_last_daily_clean().to_dict(),
            'daily_clean_time_list': [daily_result.safe_info().to_dict() for daily_result in self.data.daily_result],
            }
        return ret

    def generate_daily_info(self):
        info = super().generate_daily_config()
        return info

    def generate_tools_info(self):
        info = super().generate_tools_config()
        return info

    def delete(self):
        self._parent.delete(self.alias)

    def is_clan_battle_forbidden(self):
        username = self.data.username.lower()
        return self._parent._parent.is_clan_battle_forbidden(username)

class AccountManager:
    pathsyntax = re.compile(r'[^\\\|?*/]{1,32}')

    def __init__(self, parent: 'UserManager', qid: str, readonly: bool = False):
        if not qid in parent.user_lock:
            parent.user_lock[qid] = Lock()
        self._lck = parent.user_lock[qid]
        self.qid = qid
        self.root = parent.qid_path(qid);
        self._parent = parent
        self.readonly = readonly
        
        with open(self.root + '/secret', 'r') as f:
            self.secret: UserData = UserData.from_json(f.read())
            self.old_secret = deepcopy(self.secret)

    async def __aenter__(self):
        if not self.readonly:
            await self._lck.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.readonly:
            if self.secret != self.old_secret:
                self.save_secret()
            self._lck.release()

    @property
    def account_lock(self) -> Dict[str, Lock]:
        if not self.qid in self._parent.account_lock:
            self._parent.account_lock[self.qid] = {}
        return self._parent.account_lock[self.qid]

    def create_account(self, account: str) -> Account:
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException(f'非法账户名{account}')
        if account in self.accounts():
            raise AccountException('账号已存在')
        with open(self.path(account), 'w') as f:
            f.write(AccountData().to_json())
        return self.load(account)

    def save_secret(self):
        with open(self.root + '/secret', 'w') as f:
            f.write(self.secret.to_json())

    def set_default_account(self, account: str):
        if account not in self.accounts():
            raise AccountException('账号不存在')
        self.secret.default_account = account

    def validate_password(self, password: str) -> bool:
        return self.secret.password == password

    def load(self, account: str = "", readonly = False) -> Account:
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException(f'非法账户名{account}')
        if not account:
            account = self.secret.default_account
        if not account and len(list(self.accounts())) == 1:
            account = list(self.accounts())[0]
        if not account:
            raise AccountException('No default account')
        return Account(self, self.qid, account, readonly)

    def path(self, account: str) -> str:
        return os.path.join(self.root, account + '.json')

    def delete(self, account: str): 
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException(f'非法账户名{account}')
        os.remove(self.path(account))

    @property
    def default_account(self) -> str:
        return self.secret.default_account

    def accounts(self) -> Iterator[str]:
        for fn in os.listdir(self.root):
            if fn.endswith('.json'):
                yield fn[:-5]

    async def generate_info(self):
        accounts = []
        for account in self.accounts():
            async with self.load(account, readonly = True) as acc:
                accounts.append(acc.generate_result_info())
        return {
            'qq': self.qid,
            'default_account': self.default_account,
            'accounts': sorted(accounts, key=lambda x: x['name'], reverse=False)
        }

class UserManager:
    pathsyntax = re.compile(r'\d{5,12}')

    def __init__(self, root: str):
        self.root = root
        self.user_lock: Dict[str, Lock] = {}
        self.account_lock: Dict[str, Dict[str, Lock]] = {}
        self.clan_battle_forbidden = set()

    def is_clan_battle_forbidden(self, username: str) -> bool:
        if os.path.exists(os.path.join(CONFIG_PATH, 'clan_battle_forbidden.txt')):
            with open(os.path.join(CONFIG_PATH, 'clan_battle_forbidden.txt'), 'r') as f:
                data = f.read().splitlines()
                self.clan_battle_forbidden = set([x.strip().lower() for x in data])
            return username in self.clan_battle_forbidden
        else:
            return False

    def validate_password(self, qid: str, password: str) -> bool:
        try:
            if qid not in self.qids():
                return False
            return self.load(qid).validate_password(password)
        except Exception as e:
            print(e)
            return False

    def qid_path(self, qid: str) -> str:
        return os.path.join(self.root, qid)

    def create(self, qid: str, password: str) -> AccountManager:
        if not UserManager.pathsyntax.fullmatch(qid):
            raise UserException('无效的QQ号')
        if qid in self.qids():
            raise UserException('QQ号已存在')
        os.makedirs(self.qid_path(qid))
        with open(self.qid_path(qid) + '/secret', 'w') as f:
            f.write(UserData(password=password).to_json())
        self.shift_old_accounts(qid)
        return AccountManager(self, qid)

    def shift_old_accounts(self, qid: str):
        import glob
        for config in glob.glob(os.path.join(OLD_CONFIG_PATH, "*.json")):
            ok = False
            with open(config, 'r') as f:
                data = json.load(f)
                if str(data.get('qq', '')) == qid:
                    ok = True
            if ok:
                os.rename(config, os.path.join(self.qid_path(qid), data['alian'] + '.json'))

    def load(self, qid: str, readonly: bool = False) -> AccountManager:
        if not UserManager.pathsyntax.fullmatch(qid):
            raise UserException('无效的QQ号')
        return AccountManager(self, qid, readonly)

    def delete(self, qid: str, account: str = ""):
        if not UserManager.pathsyntax.fullmatch(qid):
            raise AccountException('无效的QQ号')
        if account:
            self.load(qid).delete(account)
        else:
            shutil.rmtree(self.qid_path(qid))

    def qids(self) -> Iterator[str]:
        for fn in os.listdir(self.root):
            if fn.isdigit() and os.path.isdir(os.path.join(self.root, fn)):
                yield fn

instance = UserManager(os.path.join(CONFIG_PATH))
