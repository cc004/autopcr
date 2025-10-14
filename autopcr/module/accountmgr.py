# 名字需要斟酌一下

import asyncio
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from werkzeug.exceptions import Forbidden
from copy import copy

from ..core.sdkclient import account, platform
from .modulemgr import ModuleManager, TaskResult, ModuleResult, eResultStatus, TaskResultInfo, ModuleResultInfo, ResultInfo
import os, re, shutil
from typing import Any, Dict, Iterator, List, Tuple, Union
from ..constants import CLAN_BATTLE_FORBID_PATH, CONFIG_PATH, OLD_CONFIG_PATH, RESULT_DIR, BSDK, CHANNEL_OPTION, SUPERUSER
from asyncio import Lock
import json
from copy import deepcopy
import hashlib
from ..db.database import db
import datetime
import traceback
from ..core.clientpool import instance as clientpool, PoolClientWrapper
from ..sdk.sdkclients import create
from ..util.logger import instance as logger

class AccountException(Exception):
    pass
class UserException(Exception):
    pass
class PermissionLimitedException(Forbidden):
    pass
class UserDisabledException(Forbidden):
    pass

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
    admin: bool = False
    disabled: bool = False

BATCHINFO = "BATCH_RUNNER"

class Account(ModuleManager):
    _account_locks: Dict[str, Lock] = dict()

    def __init__(self, parent: 'AccountManager', qid: str, account: str, readonly: bool = False):
        self._filename = parent.path(account)
        self._lck = Account._account_locks.setdefault(self._filename, Lock())
        self._parent = parent
        self.readonly = readonly
        self._id = hashlib.md5(account.encode('utf-8')).hexdigest()

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
        super().__init__(deepcopy(self.data.config))

    async def _do_aenter(self):
        if not self.readonly:
            logger.debug(f"Acquire lock {self._filename}")
            await self._lck.acquire()
            await super().__aenter__()
        return self

    async def __aenter__(self):
        return await self._do_aenter()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.readonly:
            await super().__aexit__(exc_type, exc_val, exc_tb)
            if self.data != self.old_data:
                await self.save_data()
            self._lck.release()
            logger.debug(f"Release lock {self._filename}")

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
            logger.exception(e)
            return None

    async def get_single_result_from_id(self, module, id: int = 0) -> Union[None, ModuleResult]:
        try:
            return self.data.single_result[module][id].get_result()
        except Exception as e:
            logger.exception(e)
            return None

    async def get_daily_result_from_key(self, key: str) -> Union[None, TaskResult]:
        try: # 为何不用dict？因为先前就用的list，不好更改，以及结果数不多，直接遍历也无所谓
            result = next(filter(lambda x: x.key == key, self.data.daily_result))
            return result.get_result()
        except Exception as e:
            logger.exception(e)
            return None

    async def get_single_result_from_key(self, module, key: str) -> Union[None, ModuleResult]:
        try:
            result = next(filter(lambda x: x.key == key, self.data.single_result[module]))
            return result.get_result()
        except Exception as e:
            logger.exception(e)
            return None

    @property
    def id(self) -> str:
        return self._id

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

    async def get_client(self) -> PoolClientWrapper:
        return await self.get_android_client()

    async def get_ios_client(self) -> PoolClientWrapper: # Header TODO
        client = await clientpool.get_client(create(self.data.channel, account(
            self.data.username,
            self.data.password,
            platform.IOS
        )))
        return client

    async def get_android_client(self) -> PoolClientWrapper:
        client = await clientpool.get_client(create(self.data.channel, account(
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
            'area': super().generate_tab(clan = self._parent.secret.clan)
        }

    def generate_result_info(self):
        ret = {
            'name': self.alias,
            'daily_clean_time': self.get_last_daily_clean().to_dict(),
            'clan_forbid': self.is_clan_battle_forbidden() and not self._parent.secret.clan and not self._parent.is_admin()
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
        self.enable_account = sorted(set([x for x in self.data.batch_accounts]) & set(self._parent.accounts()))

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

        if resps:
            ret_list = [x.get_result() for x in resps]
            ret = copy(ret_list[0])
            ret.log = '\n'.join(f"==={name}===\n{x.log}" for name, x in zip(alias, ret_list) if x.log)
            if any(r.table.header for r in ret_list):
                ret.table.header = next(r.table.header for r in ret_list)
                ret.table.header = ["昵称"] + ret.table.header
                ret.table.data = [
                    {**d, '昵称': name}
                    for name, x in zip(alias, ret_list)
                    if x.table
                    for d in x.table.data
                ]
            else:
                ret.table.header = ["昵称", "结果"]
                ret.table.data = [
                    {'昵称': name, '结果': x.log}
                    for name, x in zip(alias, ret_list)
                ]
            ret.status = eResultStatus.ERROR if any(x.status == eResultStatus.ERROR for x in ret_list) else eResultStatus.WARNING if any(x.status == eResultStatus.WARNING for x in ret_list) else eResultStatus.SUCCESS
            all = await self.save_single_result(key, ret)
            resps = [all] + resps
        self.data.single_result[key] = resps
        return resps

    async def do_daily(self):
        raise NotImplementedError
    async def do_task(self):
        raise NotImplementedError

class AccountManager:
    pathsyntax = re.compile(r'[^\\\|?*/#]{1,32}')
    _user_locks: Dict[str, Lock] = dict()

    def __init__(self, parent: 'UserManager', qid: str, readonly: bool = False):
        self.qid = qid
        self.root = parent.qid_path(qid)
        self._parent = parent
        self.readonly = readonly
        self._lck = AccountManager._user_locks.setdefault(self.root, Lock())
        
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

    def set_password(self, password: str):
        self.secret.password = password

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

    def account_count(self) -> int:
        return sum(1 for _ in self.accounts())

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

    async def generate_role(self):
        return {
            'admin': self.is_admin(),
            'super_user': self.is_super_user()
        }

    def is_admin(self):
        return self.secret.admin or self.is_super_user()

    def is_super_user(self):
        return SUPERUSER == self.qid


class UserManager:
    pathsyntax = re.compile(r'g?\d{5,12}')

    def __init__(self, root: str):
        self.root = root
        self.clan_battle_forbidden = set()

        # 初始不存在root目录，创建一下
        os.makedirs(self.root, exist_ok=True)
        self.load_clan_battle_forbidden()

    def load_clan_battle_forbidden(self):
        if os.path.exists(CLAN_BATTLE_FORBID_PATH):
            with open(CLAN_BATTLE_FORBID_PATH, "r") as f:
                data = f.read().splitlines()
                self.clan_battle_forbidden = set([x.strip().lower() for x in data])

    def is_clan_battle_forbidden(self, username: str) -> bool:
        return username in self.clan_battle_forbidden

    def get_clan_battle_forbidden(self) -> List[str]:
        return list(self.clan_battle_forbidden)

    def set_clan_battle_forbidden(self, accs: List[str]):
        with open(CLAN_BATTLE_FORBID_PATH, "w") as f:
            f.write('\n'.join(accs))
        self.load_clan_battle_forbidden()

    def validate_password(self, qid: str, password: str) -> bool:
        try:
            if qid not in self.qids():
                return False
            return self.load(qid).validate_password(password)
        except Exception as e:
            logger.exception(e)
            return False

    def check_enabled(self, qid: str) -> bool:
        try:
            if qid not in self.qids():
                return False
            return not self.load(qid, readonly=True).secret.disabled
        except Exception as e:
            logger.exception(e)
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
        logger.info(f"Create user {qid}")
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
