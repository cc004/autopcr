# 名字需要斟酌一下

import asyncio
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from ..core.pcrclient import pcrclient
from ..core.sdkclient import account, platform
from .modulemgr import ModuleManager, TaskResult, ModuleResult, eResultStatus
from ..sdk.sdkclients import create
import os, re, shutil
from typing import Any, Dict, Iterator, List, Tuple, Union
from ..constants import CONFIG_PATH, OLD_CONFIG_PATH, RESULT_DIR, BSDK, CHANNEL_OPTION
from asyncio import Lock
import json
from copy import deepcopy
import hashlib
from ..db.database import db
import datetime
import traceback
from .validator import create_validator

class AccountException(Exception):
    pass
class UserException(Exception):
    pass

@dataclass_json
@dataclass
class ResultInfo:
    alias: str = ""
    key: str = ""
    path: str = ""
    time: str = ""
    url: str = ""
    _type: str = ""
    status: eResultStatus = eResultStatus.SKIP

    def save_result(self, result):
        with open(self.path, 'w') as f:
            f.write(result.to_json())
    def delete_result(self):
        if os.path.exists(self.path):
            os.remove(self.path)
    def get_result(self):
        raise NotImplementedError
    def response(self, url_format: str):
        url = url_format.format(self.alias)
        return ResultInfo(alias = self.alias, key = self.key, time = self.time, url = url, status = self.status)

@dataclass_json
@dataclass
class TaskResultInfo(ResultInfo):
    _type: str = "daily_result"
    def get_result(self) -> TaskResult:
        with open(self.path, 'r') as f:
            return TaskResult.from_json(f.read())

@dataclass_json
@dataclass
class ModuleResultInfo(ResultInfo):
    _type: str = "single_result"
    def get_result(self) -> ModuleResult:
        with open(self.path, 'r') as f:
            return ModuleResult.from_json(f.read())

@dataclass_json
@dataclass
class AccountData:
    username: str = ""
    password: str = ""
    channel: str = BSDK
    config: Dict[str, Any] = field(default_factory=dict)
    daily_result: List[TaskResultInfo] = field(default_factory=list)
    single_result: Dict[str, List[ModuleResultInfo]] = field(default_factory=dict)
    batch_accounts: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class UserData:
    password: str = ""
    default_account: str = ""
    clan: bool = False

BATCHINFO = "BATCH_RUNNER"

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
            if account == BATCHINFO:
                with open(self._filename, 'w') as f:
                    f.write(AccountData().to_json())
            else:
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

    async def push_result(self, result_list: List[Any], result: ResultInfo) -> List[Any]:
        while len(result_list) >= 4:
            result_list.pop().delete_result()
        return [result] + result_list

    async def save_daily_result(self, result: TaskResult, status: eResultStatus) -> TaskResultInfo:
        now = datetime.datetime.now()
        time_safe = db.format_time_safe(now)
        file = os.path.join(RESULT_DIR, f"{self.token}_daily_{time_safe}.json")

        item = TaskResultInfo(alias = self.alias, key=time_safe, path = file, time = db.format_time(now), status = status)
        item.save_result(result)
        self.data.daily_result = await self.push_result(self.data.daily_result, item)
        return item

    async def save_single_result(self, module: str, result: ModuleResult) -> ModuleResultInfo:
        now = datetime.datetime.now()
        time_safe = db.format_time_safe(now)
        file = os.path.join(RESULT_DIR, f"{self.token}_{module}_{time_safe}.json")

        item = ModuleResultInfo(alias = self.alias, key = time_safe, path = file, time = db.format_time(now), status = result.status)
        item.save_result(result)
        self.data.single_result[module] = await self.push_result(self.data.single_result.get(module, []), item)
        return item

    async def get_daily_result_from_id(self, id: int = 0) -> Union[None, TaskResult]:
        try:
            return self.data.daily_result[id].get_result()
        except Exception as e:
            traceback.print_exc()
            return None

    async def get_single_result_from_id(self, module, id: int = 0) -> Union[None, ModuleResult]:
        try:
            return self.data.single_result[module][id].get_result()
        except Exception as e:
            traceback.print_exc()
            return None

    async def get_daily_result_from_key(self, key: str) -> Union[None, TaskResult]:
        try: # 为何不用dict？因为先前就用的list，不好更改，以及结果数不多，直接遍历也无所谓
            result = next(filter(lambda x: x.key == key, self.data.daily_result))
            return result.get_result()
        except Exception as e:
            traceback.print_exc()
            return None

    async def get_single_result_from_key(self, module, key: str) -> Union[None, ModuleResult]:
        try:
            result = next(filter(lambda x: x.key == key, self.data.single_result[module]))
            return result.get_result()
        except Exception as e:
            traceback.print_exc()
            return None

    def get_last_daily_clean(self) -> TaskResultInfo:
        daily_result = self.get_daily_result_list()
        if daily_result:
            return daily_result[0]
        else:
            return TaskResultInfo()

    def get_daily_result_list(self) -> List[TaskResultInfo]:
        ret = self.data.daily_result
        return ret

    def get_single_result_list(self, module: str) -> List[ModuleResultInfo]:
        ret = self.data.single_result.get(module, [])
        return ret

    def get_client(self) -> pcrclient:
        return self.get_android_client()

    def get_ios_client(self) -> pcrclient: # Header TODO
        client = pcrclient(create(self.data.channel, account(
            self.data.username,
            self.data.password,
            platform.IOS
        )), captchaVerifier = create_validator(self.qq))
        return client

    def get_android_client(self) -> pcrclient:
        client = pcrclient(create(self.data.channel, account(
            self.data.username,
            self.data.password,
            platform.Android
        )), captchaVerifier = create_validator(self.qq))
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
            'area': super().generate_tab(clan = self._parent.secret.clan)
        }

    def generate_result_info(self):
        ret = {
            'name': self.alias,
            'daily_clean_time': self.get_last_daily_clean().to_dict(),
            }
        return ret

    def generate_modules_info(self, key: str):
        info = super().generate_modules_info(key)
        return info

    def delete(self):
        self._parent.delete(self.alias)

    def is_clan_battle_forbidden(self):
        username = self.data.username.lower()
        return self._parent._parent.is_clan_battle_forbidden(username)

class AccountBatch(Account):
    def __init__(self, parent: 'AccountManager', qid: str, accounts: str = BATCHINFO, readonly: bool = False):
        super().__init__(parent, qid, accounts, readonly)
        # self.enable_account = set([x for x in self.data.batch_accounts]) & set(self._parent.accounts())
        self.enable_account = set(self._parent.accounts())

    def generate_info(self):
        accounts = list(self.enable_account)
        all_accounts = sorted(list(self._parent.accounts()))
        return {
            'alias': self.alias,
            'batch_accounts': accounts,
            'all_accounts': all_accounts,
            'area': super().generate_tab(clan = self._parent.secret.clan, batch = True)
        }

    async def do_from_key(self, config: dict, key: str, isAdminCall: bool = False) -> List[ModuleResultInfo]:
        async def do_from_key_pre(alias: str):
            async with self._parent.load(alias) as acc:
                res = await acc.do_from_key(config, key, isAdminCall)
                return res

        loop = asyncio.get_event_loop()
        alias = []
        task = []
        for acc in self.enable_account:
            alias.append(acc)
            task.append(loop.create_task(do_from_key_pre(acc)))

        resps = await asyncio.gather(*task, return_exceptions=True)
        self.data.single_result[key] = resps
        return resps

    async def do_daily(self):
        raise NotImplementedError
    async def do_task(self):
        raise NotImplementedError

class AccountManager:
    pathsyntax = re.compile(r'[^\\\|?*/#]{1,32}')

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

        self.secret.clan |= self.qid.startswith('g')

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
        if account == BATCHINFO:
            return AccountBatch(self, self.qid, account, readonly = readonly)
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

    def delete_all_accounts(self):
        for account in self.accounts():
            self.delete(account)

    def delete_mgr(self):
        self._parent.delete(self.qid)

    @property
    def default_account(self) -> str:
        return self.secret.default_account

    def accounts(self) -> Iterator[str]:
        account_files = sorted(os.listdir(self.root))
        for fn in account_files:
            if fn.endswith('.json') and not fn.startswith(BATCHINFO):
                yield fn[:-5]

    async def create_accounts_from_tsv(self, tsv: str) -> Tuple[bool, str]:
        acc = []
        ok = True
        exist_accounts = set(self.accounts())
        msg = []
        for line in tsv.splitlines():
            if not line:
                continue
            alias, username, password, *channel = line.split('\t')

            if not AccountManager.pathsyntax.fullmatch(alias):
                ok = False
                msg.append(f'非法昵称{alias}')
            if alias in exist_accounts:
                ok = False
                msg.append(f'昵称重复{alias}')
            channel = channel[0] if channel else BSDK
            if channel not in CHANNEL_OPTION:
                ok = False
                msg.append(f'未知服务器{channel}')

            exist_accounts.add(alias)
            acc.append((alias, username, password, channel))
        if not ok:
            return False, '\n'.join(msg)

        for alias, username, password, channel in acc:
            with open(self.path(alias), 'w') as f:
                f.write(AccountData(username = username, password = password, channel = channel).to_json())
        return True, f'成功导入{len(acc)}个账号'

    async def generate_info(self):
        accounts = []
        for account in self.accounts():
            async with self.load(account, readonly = True) as acc:
                accounts.append(acc.generate_result_info())
        return {
            'qq': self.qid,
            'default_account': self.default_account,
            'accounts': accounts,
            'clan': self.secret.clan
        }

class UserManager:
    pathsyntax = re.compile(r'g?\d{5,12}')

    def __init__(self, root: str):
        self.root = root
        self.user_lock: Dict[str, Lock] = {}
        self.account_lock: Dict[str, Dict[str, Lock]] = {}
        self.clan_battle_forbidden = set()

        # 初始不存在root目录，创建一下
        os.makedirs(self.root, exist_ok=True)

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
            traceback.print_exc()
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
            if os.path.isdir(os.path.join(self.root, fn)):
                yield fn

instance = UserManager(os.path.join(CONFIG_PATH))
