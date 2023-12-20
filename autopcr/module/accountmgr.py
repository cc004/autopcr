# 名字需要斟酌一下

from ..core.pcrclient import pcrclient
from .modulemgr import ModuleManager
import os, re
from typing import Dict, Iterator, Tuple
from ..constants import CONFIG_PATH
from asyncio import Lock
import json
from copy import deepcopy
import hashlib
from ..db.database import db
import datetime

class AccountException(Exception):
    pass

class Account(ModuleManager):
    def __init__(self, parent: 'AccountManager', qid: str, account: str, readonly: bool = False, create_when_no_exist: bool = False):
        if not account in parent.account_lock:
            parent.account_lock[account] = Lock()
        self._lck = parent.account_lock[account]
        self._account = account
        self._filename = parent.path(qid, account)
        self._parent = parent
        self.readonly = readonly
        self.id = hashlib.md5(account.encode('utf-8')).hexdigest()

        if not os.path.exists(self._filename):
            if create_when_no_exist:
                with open(self._filename, 'w') as f:
                    f.write('{"username": "", "password": "", "alian": ""}')
            else:
                raise AccountException("account no exist")

        with open(self._filename, 'r') as f:
            self.data = json.load(f)
            self.old_data = deepcopy(self.data)

        self.qq = qid
        self.alian = self.data.get("alian", "未知")
        self.username = self.data.get("username", "")
        super().__init__(self.data.get("config", {}), self)
    
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
            json.dump(self.data, f)

    async def set_result(self, result):
        self.data.setdefault('_last_result', {}).update(result)
        self.data['_last_clean_time'] = db.format_time(datetime.datetime.now())

    def get_client(self) -> pcrclient:
        return self.get_android_client()

    def get_ios_client(self) -> pcrclient: # Header TODO
        client = pcrclient({
            'account': self.data['username'],
            'password': self.data['password'],
            'channel': 1000,
            'platform': 1
        })
        return client

    def get_android_client(self) -> pcrclient:
        client = pcrclient({
            'account': self.data['username'],
            'password': self.data['password'],
            'channel': 1,
            'platform': 2
        })
        return client

    def generate_info(self):
        def _mask_str(mask_str: str) -> str:
            if not isinstance(mask_str, str):
                raise ValueError("Input must be a string")
            elif not mask_str:
                return ""
            else:
                return "*" * 7 + mask_str[-1]
        last_clean_time = self.data.setdefault('_last_result', {}).get("_last_clean_time", "")
        return {
            'file': self._account,
            'alian': self.alian,
            'qq': self.qq,
            'username': _mask_str(self.username),
            'last_clean_time': last_clean_time,
            'password': 8 * "*",
        }

    def generate_daily_info(self):
        info = { 'last_result': self.data.get('_last_result', {}) }
        info.update(super().generate_daily_config())
        return info

    def generate_tools_info(self):
        info = { 'last_result': self.data.get('_last_result', {}) }
        info.update(super().generate_tools_config())
        return info

    def delete(self):
        self._parent.delete(self.qq, self._account)

class AccountManager:
    pathsyntax = re.compile(r'[^\\\|?*/]{1,32}')

    def __init__(self, root: str):
        self.root = root
        self.account_lock: Dict[str, Lock] = {}

    def qid_path(self, qid: str) -> str:
        return os.path.join(self.root, qid)

    def path(self, qid: str, account: str) -> str:
        return os.path.join(self.qid_path(qid), account + '.json')

    def load(self, qid: str, account: str, readonly: bool = False, create_when_no_exist: bool = False) -> Account:
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException('Invalid account name')
        return Account(self, qid, account, readonly, create_when_no_exist)

    def delete(self, qid: str, account: str = ""):
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException('Invalid account name')
        if account:
            os.remove(self.path(qid, account))
        else: 
            os.removedirs(self.qid_path(qid))

    def accounts(self, qid: str) -> Iterator[str]:
        for fn in os.listdir(self.qid_path(qid)):
            if fn.endswith('.json'):
                yield fn[:-5]

    def qids(self) -> Iterator[str]:
        for fn in os.listdir(self.root):
            if fn.isdigit() and os.path.isdir(fn):
                yield fn

    def all_accounts(self) -> Iterator[Tuple[str, str]]:
        for qid in self.qids():
            for account in self.accounts(qid):
                yield (qid, account)


instance = AccountManager(os.path.join(CONFIG_PATH))
