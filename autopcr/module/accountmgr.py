# 名字需要斟酌一下

import asyncio
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from werkzeug.exceptions import Forbidden
from copy import copy
from contextlib import contextmanager

from ..core.sdkclient import account, platform
from .modulemgr import ModuleManager, TaskResult, ModuleResult, eResultStatus, TaskResultInfo, ModuleResultInfo, ResultInfo
import os, re, shutil
from typing import Any, Dict, Generator, Iterator, List, Optional, Tuple, Union
from ..constants import CACHE_DIR, CLAN_BATTLE_FORBID_PATH, CONFIG_PATH, OLD_CONFIG_PATH, RESULT_DIR, BSDK, CHANNEL_OPTION, SUPERUSER
from asyncio import Lock
import json
from copy import deepcopy
import hashlib
import hmac
import secrets
import sqlite3
from ..db.database import db
import datetime
import traceback
from ..core.clientpool import instance as clientpool, PoolClientWrapper
from ..sdk.sdkclients import create
from ..util.logger import instance as logger
from ..openbao import instance as openbao, OpenBaoError
from ..openbao_audit import OpenBaoAuditContext

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

    def __init__(
        self,
        parent: 'AccountManager',
        qid: str,
        account: str,
        readonly: bool = False,
        load_credentials: bool = True,
    ):
        self._filename = parent.path(account)
        self._lck = Account._account_locks.setdefault(self._filename, Lock())
        self._parent = parent
        self.readonly = readonly
        self.load_credentials = load_credentials
        self._id = hashlib.md5(account.encode('utf-8')).hexdigest()

        if account == BATCHINFO:
            self.data = parent._parent.load_batch_runner_data(qid)
        else:
            if not os.path.exists(self._filename):
                raise AccountException("账号不存在")
            with open(self._filename, 'r') as f:
                self.data: AccountData = AccountData.from_json(f.read())
        self.old_data: AccountData = deepcopy(self.data)

        self.qq = qid
        self.alias = account
        self.token = f"{self.qq}_{self.alias}"
        super().__init__(deepcopy(self.data.config))

    @property
    def batch_accounts(self) -> List[str]:
        if self.alias != BATCHINFO:
            return []
        return self._parent._parent.get_batch_accounts(self.qq)

    @batch_accounts.setter
    def batch_accounts(self, accounts: List[str]):
        if self.alias != BATCHINFO:
            raise AccountException("只有批量账号可以设置批量账号列表")
        self._parent._parent.save_batch_accounts(self.qq, accounts)

    async def _do_aenter(self):
        if not self.readonly:
            logger.debug(f"Acquire lock {self._filename}")
            await self._lck.acquire()
        try:
            if self.alias != BATCHINFO and self.load_credentials:
                credentials = await openbao.read_game_credentials(self.qq, self.alias)
                if credentials is not None:
                    username = credentials.get("username", "")
                    password = credentials.get("password", "")
                    if not isinstance(username, str) or not isinstance(password, str):
                        raise OpenBaoError("OpenBao returned invalid game credentials")
                    self.data.username = username
                    self.data.password = password
            self.old_data = deepcopy(self.data)
            if not self.readonly:
                await super().__aenter__()
        except Exception:
            if not self.readonly:
                self._lck.release()
            raise
        return self

    async def __aenter__(self):
        return await self._do_aenter()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.readonly:
            try:
                await super().__aexit__(exc_type, exc_val, exc_tb)
                if self.data != self.old_data:
                    await self.save_data()
            finally:
                self._lck.release()
            logger.debug(f"Release lock {self._filename}")

    async def save_data(self):
        if self.alias == BATCHINFO:
            self._write_data_file()
            self.old_data = deepcopy(self.data)
            return

        if self.alias != BATCHINFO and not self._parent._parent.has_account(self.qq, self.alias):
            raise AccountException("账号不存在")
        credentials_changed = (
            self.data.username != self.old_data.username
            or self.data.password != self.old_data.password
        )
        if not isinstance(self.data.username, str) or not isinstance(self.data.password, str):
            raise AccountException("账号凭据必须是字符串")
        if credentials_changed:
            if self.data.username or self.data.password:
                await openbao.write_game_credentials(
                    self.qq,
                    self.alias,
                    self.data.username,
                    self.data.password,
                )
            else:
                await openbao.delete_game_credentials(self.qq, self.alias)

        stored_data = deepcopy(self.data)
        stored_data.username = ""
        stored_data.password = ""
        self._write_data_file(stored_data)
        self.old_data = deepcopy(self.data)

    def _write_data_file(self, data: Optional[AccountData] = None):
        stored_data = deepcopy(data if data is not None else self.data)
        stored_data.username = ""
        stored_data.password = ""
        temporary = self._filename + ".tmp"
        with open(temporary, 'w') as f:
            f.write(stored_data.to_json())
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, self._filename)

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
        await self._ensure_credentials()
        client = await clientpool.get_client(
            create(
                self.data.channel,
                account(
                    self.data.username,
                    self.data.password,
                    platform.IOS,
                    self._parent.farmer,
                ),
            ),
            audit_context=OpenBaoAuditContext(self.qq, self.alias),
        )
        return client

    async def _ensure_credentials(self):
        if self.data.username or self.data.password:
            return
        credentials = await openbao.read_game_credentials(self.qq, self.alias)
        if credentials is not None:
            self.data.username = credentials.get("username", "")
            self.data.password = credentials.get("password", "")

    async def get_android_client(self) -> PoolClientWrapper:
        await self._ensure_credentials()
        client = await clientpool.get_client(
            create(
                self.data.channel,
                account(
                    self.data.username,
                    self.data.password,
                    platform.Android,
                    self._parent.farmer,
                ),
            ),
            audit_context=OpenBaoAuditContext(self.qq, self.alias),
        )
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

    async def delete(self):
        await self._parent.delete(self.alias)

    def is_clan_battle_forbidden(self):
        username = self.data.username.lower()
        return self._parent._parent.is_clan_battle_forbidden(username)

class AccountBatch(Account):
    def __init__(self, parent: 'AccountManager', qid: str, accounts: str = BATCHINFO, readonly: bool = False, force_use_all: bool = False):
        super().__init__(parent, qid, accounts, readonly)
        if force_use_all:
            self.enable_account = sorted(list(self._parent.accounts()))
        else:
            self.enable_account = sorted(
                set(self.batch_accounts) & set(self._parent.accounts())
            )

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
            ret.status = eResultStatus.ERROR if any(x.status == eResultStatus.ERROR for x in ret_list) else eResultStatus.WARNING if any(x.status == eResultStatus.WARNING for x in ret_list) else eResultStatus.SUCCESS
            if any(r.table.header for r in ret_list):
                ret.table.header = next(r.table.header for r in ret_list)
                ret.table.header = ["昵称", '状态'] + ret.table.header
                ret.table.data = [
                    {**d, '昵称': name, '状态': f"#{x.status.value}"}
                    for name, x in zip(alias, ret_list)
                    if x.table
                    for d in x.table.data
                ]
            else:
                ret.table.header = ["昵称", "状态", "结果"]
                ret.table.data = [
                    {
                     '昵称': name, 
                     '状态': f"#{x.status.value}",
                     '结果': x.log
                    }
                    for name, x in zip(alias, ret_list)
                ]
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
        
        self.secret = parent.get_user_data(qid)
        self.old_secret = deepcopy(self.secret)

        self.secret.clan |= self.qid.startswith('g')

    async def __aenter__(self):
        if not self.readonly:
            await self._lck.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.readonly:
            try:
                if self.secret != self.old_secret:
                    self.save_secret()
            finally:
                self._lck.release()

    @property
    def farmer(self) -> bool:
        return not self.secret.clan and self.account_count() > 10

    def create_account(self, account: str) -> Account:
        if not AccountManager.pathsyntax.fullmatch(account) or account.startswith(BATCHINFO):
            raise AccountException(f'非法账户名{account}')
        try:
            with open(self.path(account), 'x') as f:
                f.write(AccountData().to_json())
            self._parent.register_accounts(self.qid, [account])
        except FileExistsError as error:
            raise AccountException('账号已存在') from error
        except Exception:
            if os.path.exists(self.path(account)):
                os.remove(self.path(account))
            raise
        return self.load(account)

    def save_secret(self):
        self._parent.save_user_data(self.qid, self.secret)

    def set_default_account(self, account: str):
        if account not in self.accounts():
            raise AccountException('账号不存在')
        self.secret.default_account = account

    def set_password(self, password: str):
        self._parent.set_password(self.qid, password)

    def validate_password(self, password: str) -> bool:
        return self._parent.validate_password(self.qid, password)

    def load(
        self,
        account: str = "",
        readonly=False,
        force_use_all: bool = False,
        load_credentials: bool = True,
    ) -> Account:
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException(f'非法账户名{account}')
        if account == BATCHINFO:
            return AccountBatch(self, self.qid, account, readonly = readonly, force_use_all = force_use_all)
        if not account:
            account = self.secret.default_account
        if not account and len(list(self.accounts())) == 1:
            account = list(self.accounts())[0]
        if not account:
            raise AccountException('No default account')
        if account not in self.accounts():
            raise AccountException("账号不存在")
        return Account(
            self,
            self.qid,
            account,
            readonly,
            load_credentials=load_credentials,
        )

    def path(self, account: str) -> str:
        return os.path.join(self.root, account + '.json')

    async def delete(self, account: str):
        if not AccountManager.pathsyntax.fullmatch(account):
            raise AccountException(f'非法账户名{account}')
        filename = self.path(account)
        if not self._parent.has_account(self.qid, account) or not os.path.isfile(filename):
            raise AccountException("账号不存在")
        await openbao.delete_game_credentials(self.qid, account)
        os.remove(filename)
        self._parent.unregister_account(self.qid, account)
        if self.secret.default_account == account:
            self.secret.default_account = ""
            self.save_secret()

    async def delete_all_accounts(self):
        for account in self.accounts():
            await self.delete(account)

    async def delete_mgr(self):
        await self._parent.delete(self.qid)
        self.old_secret = deepcopy(self.secret)

    @property
    def default_account(self) -> str:
        return self.secret.default_account

    def accounts(self) -> Iterator[str]:
        yield from self._parent.account_names(self.qid)

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

            if not AccountManager.pathsyntax.fullmatch(alias) or alias.startswith(BATCHINFO):
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

        created_files = []
        written_credentials = []
        current_alias = ""
        try:
            for alias, username, password, channel in acc:
                current_alias = alias
                with open(self.path(alias), 'x') as f:
                    created_files.append(self.path(alias))
                    f.write(AccountData(channel = channel).to_json())
            for alias, username, password, _ in acc:
                current_alias = alias
                if username or password:
                    existing = await openbao.read_game_credentials(self.qid, alias)
                    if existing is not None:
                        raise AccountException(f'账号凭据已存在: {alias}')
                    await openbao.write_game_credentials(self.qid, alias, username, password)
                    written_credentials.append(alias)
            self._parent.register_accounts(self.qid, [alias for alias, *_ in acc])
        except FileExistsError:
            for filename in created_files:
                os.remove(filename)
            return False, f'昵称对应的JSON文件已存在: {current_alias}'
        except Exception:
            for alias in written_credentials:
                await openbao.delete_game_credentials(self.qid, alias)
            for filename in created_files:
                if os.path.exists(filename):
                    os.remove(filename)
            raise
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
    PASSWORD_ITERATIONS = 600_000
    PASSWORD_SALT_BYTES = 16

    def __init__(self, root: str):
        self.root = root
        self.auth_db_path = os.path.join(root, 'users.db')
        self.clan_battle_forbidden = set()

        os.makedirs(self.root, exist_ok=True)
        self._initialize_auth_db()
        self._migrate_legacy_users()
        for description, migration in (
            ("account mappings", self._initialize_account_mapping),
            ("batch-runner data", self._migrate_batch_runner_data),
        ):
            try:
                migration()
            except Exception:
                logger.exception("Startup migration failed for %s", description)
                raise
        self.load_clan_battle_forbidden()

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        connection = sqlite3.connect(self.auth_db_path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 30000")
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize_auth_db(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    qid TEXT PRIMARY KEY,
                    password_hash BLOB NOT NULL,
                    password_salt BLOB NOT NULL,
                    password_iterations INTEGER NOT NULL,
                    default_account TEXT NOT NULL DEFAULT '',
                    clan INTEGER NOT NULL DEFAULT 0,
                    admin INTEGER NOT NULL DEFAULT 0,
                    disabled INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            columns = {
                row['name']
                for row in connection.execute("PRAGMA table_info(users)").fetchall()
            }
            if 'batch_account' not in columns:
                connection.execute(
                    "ALTER TABLE users ADD COLUMN batch_account TEXT NOT NULL DEFAULT '[]'"
                )

    @classmethod
    def _hash_password(cls, password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        salt = salt or secrets.token_bytes(cls.PASSWORD_SALT_BYTES)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            cls.PASSWORD_ITERATIONS,
        )
        return salt, password_hash

    def _migrate_legacy_users(self):
        legacy_users = [
            qid for qid in os.listdir(self.root)
            if os.path.isdir(self.qid_path(qid))
            and os.path.isfile(os.path.join(self.qid_path(qid), 'secret'))
        ]
        if not legacy_users:
            return

        logger.info(
            "Found %d legacy plaintext user credential files; migrating to SQLite",
            len(legacy_users),
        )
        migrated_users = 0
        removed_legacy_files = 0
        for qid in legacy_users:
            legacy_path = os.path.join(self.qid_path(qid), 'secret')

            try:
                migrated = False
                with self._connect() as connection:
                    connection.execute("BEGIN IMMEDIATE")
                    existing = connection.execute(
                        "SELECT 1 FROM users WHERE qid = ?", (qid,)
                    ).fetchone()
                    if existing is None:
                        with open(legacy_path, 'r') as legacy_file:
                            legacy_data = UserData.from_json(legacy_file.read())
                        salt, password_hash = self._hash_password(legacy_data.password)
                        connection.execute(
                            """
                            INSERT INTO users (
                                qid, password_hash, password_salt, password_iterations,
                                default_account, clan, admin, disabled
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                qid,
                                password_hash,
                                salt,
                                self.PASSWORD_ITERATIONS,
                                legacy_data.default_account,
                                int(legacy_data.clan or qid.startswith('g')),
                                int(legacy_data.admin),
                                int(legacy_data.disabled),
                            ),
                        )
                        migrated = True

                if migrated:
                    migrated_users += 1
                    logger.info(
                        "Migrated legacy user credentials to SQLite for user %s",
                        qid,
                    )
                else:
                    logger.info(
                        "SQLite credentials already exist for user %s; "
                        "removing the legacy plaintext file",
                        qid,
                    )

                os.remove(legacy_path)
                removed_legacy_files += 1
            except FileNotFoundError:
                # Another server process may have completed this migration.
                pass
            except Exception:
                logger.exception(
                    "Failed to migrate legacy user credentials for user %s",
                    qid,
                )
                raise

        logger.info(
            "Finished legacy user credential migration: %d users imported, "
            "%d plaintext files removed",
            migrated_users,
            removed_legacy_files,
        )

    def _initialize_account_mapping(self):
        migrated_accounts = 0
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            table_exists = connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type = 'table' AND name = 'user_accounts'
                """
            ).fetchone() is not None
            if table_exists:
                columns = {
                    row['name']
                    for row in connection.execute(
                        "PRAGMA table_info(user_accounts)"
                    ).fetchall()
                }
                if columns == {'qid', 'filename', 'display_name'}:
                    rows = connection.execute(
                        """
                        SELECT qid, filename, display_name
                        FROM user_accounts
                        """
                    ).fetchall()
                    for row in rows:
                        if (
                            row['filename'] != f"{row['display_name']}.json"
                            or not AccountManager.pathsyntax.fullmatch(
                                row['display_name']
                            )
                        ):
                            raise UserException(
                                "账号映射无法安全迁移: "
                                f"{row['qid']}/{row['display_name']}"
                            )
                    connection.execute(
                        """
                        CREATE TABLE user_accounts_new (
                            qid TEXT NOT NULL REFERENCES users(qid) ON DELETE CASCADE,
                            display_name TEXT NOT NULL,
                            PRIMARY KEY (qid, display_name)
                        )
                        """
                    )
                    connection.executemany(
                        """
                        INSERT INTO user_accounts_new (qid, display_name)
                        VALUES (?, ?)
                        """,
                        [(row['qid'], row['display_name']) for row in rows],
                    )
                    connection.execute("DROP TABLE user_accounts")
                    connection.execute(
                        "ALTER TABLE user_accounts_new RENAME TO user_accounts"
                    )
                    logger.info(
                        "Migrated the legacy user_accounts schema to SQLite "
                        "for %d accounts",
                        len(rows),
                    )
                    return
                if columns != {'qid', 'display_name'}:
                    raise UserException(
                        "user_accounts 表结构不受支持，无法自动迁移"
                    )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS user_accounts (
                    qid TEXT NOT NULL REFERENCES users(qid) ON DELETE CASCADE,
                    display_name TEXT NOT NULL,
                    PRIMARY KEY (qid, display_name)
                )
                """
            )
            if table_exists:
                return

            for qid_row in connection.execute("SELECT qid FROM users").fetchall():
                qid = qid_row['qid']
                user_root = self.qid_path(qid)
                if not os.path.isdir(user_root):
                    continue
                filenames = sorted(
                    filename for filename in os.listdir(user_root)
                    if filename.endswith('.json') and not filename.startswith(BATCHINFO)
                )
                display_names = set()
                for filename in filenames:
                    display_name = filename[:-5]
                    if not AccountManager.pathsyntax.fullmatch(display_name):
                        raise UserException(f'非法账户名{display_name}')
                    if display_name in display_names:
                        raise UserException(f'用户{qid}下存在重复账号名{display_name}')
                    display_names.add(display_name)
                    connection.execute(
                        """
                        INSERT INTO user_accounts (qid, display_name)
                        VALUES (?, ?)
                        """,
                        (qid, display_name),
                    )
                    migrated_accounts += 1

        if migrated_accounts:
            logger.info(
                "Migrated %d account mappings from existing account JSON files to SQLite",
                migrated_accounts,
            )

    @staticmethod
    def _parse_batch_accounts(value) -> List[str]:
        try:
            accounts = json.loads(value) if isinstance(value, str) else value
        except json.JSONDecodeError as error:
            raise AccountException("批量账号列表格式错误") from error
        if not isinstance(accounts, list) or any(
            not isinstance(account, str) for account in accounts
        ):
            raise AccountException("批量账号列表格式错误")
        return accounts

    @classmethod
    def _parse_batch_runner_data(cls, payload: str):
        try:
            raw_data = json.loads(payload)
        except json.JSONDecodeError as error:
            raise AccountException(f'{BATCHINFO}.json 格式错误') from error
        if not isinstance(raw_data, dict):
            raise AccountException(f'{BATCHINFO}.json 格式错误')
        batch_accounts = cls._parse_batch_accounts(
            raw_data.pop('batch_accounts', [])
        )
        return AccountData.from_json(json.dumps(raw_data)), batch_accounts

    def _migrate_batch_runner_data(self):
        staged_files = []
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            for row in connection.execute(
                "SELECT qid, batch_account FROM users"
            ).fetchall():
                path = os.path.join(self.qid_path(row['qid']), f"{BATCHINFO}.json")
                if os.path.isfile(path):
                    with open(path, 'r', encoding='utf-8') as batch_file:
                        data, file_accounts = self._parse_batch_runner_data(
                            batch_file.read()
                        )
                        if not self._parse_batch_accounts(row['batch_account']):
                            connection.execute(
                                "UPDATE users SET batch_account = ? WHERE qid = ?",
                                (
                                    json.dumps(file_accounts, ensure_ascii=False),
                                    row['qid'],
                                ),
                            )

                    data.username = ""
                    data.password = ""
                    temporary = path + ".tmp"
                    with open(temporary, 'w', encoding='utf-8') as batch_file:
                        batch_file.write(data.to_json())
                        batch_file.flush()
                        os.fsync(batch_file.fileno())
                    staged_files.append((temporary, path))

        for temporary, path in staged_files:
            os.replace(temporary, path)
        if staged_files:
            logger.info(
                "Migrated batch-runner settings for %d users; removed legacy "
                "credentials from the JSON files",
                len(staged_files),
            )

    def load_batch_runner_data(self, qid: str) -> AccountData:
        path = os.path.join(self.qid_path(qid), f"{BATCHINFO}.json")
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as batch_file:
                data, _ = self._parse_batch_runner_data(batch_file.read())
        else:
            data = AccountData()
        data.username = ""
        data.password = ""
        return data

    def get_batch_accounts(self, qid: str) -> List[str]:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT batch_account FROM users WHERE qid = ?",
                (qid,),
            ).fetchone()
        if row is None:
            raise UserException('用户不存在')
        return self._parse_batch_accounts(row['batch_account'])

    def save_batch_accounts(self, qid: str, accounts: List[str]):
        if not isinstance(accounts, list) or any(
            not isinstance(account, str) for account in accounts
        ):
            raise AccountException("批量账号列表格式错误")
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE users SET batch_account = ?
                WHERE qid = ?
                """,
                (json.dumps(accounts, ensure_ascii=False), qid),
            )
        if cursor.rowcount == 0:
            raise UserException('用户不存在')

    async def migrate_game_credentials(self, qid: Optional[str] = None):
        try:
            await self._migrate_game_credentials(qid)
        except Exception:
            logger.exception("Failed to migrate legacy game credentials and sessions")
            raise

    async def _migrate_game_credentials(self, qid: Optional[str] = None):
        user_ids = [qid] if qid is not None else list(self.qids())
        migrated_credentials = 0
        existing_credentials = 0
        cleaned_configs = 0
        for user_id in user_ids:
            for account in self.account_names(user_id):
                account_path = os.path.join(
                    self.qid_path(user_id),
                    f"{account}.json",
                )
                with open(account_path, 'r') as account_file:
                    raw_data = json.load(account_file)
                if not isinstance(raw_data, dict):
                    raise AccountException(f'账号配置格式错误: {user_id}/{account}')
                obsolete_batch_field = 'batch_accounts' in raw_data
                raw_data.pop('batch_accounts', None)
                data = AccountData.from_json(json.dumps(raw_data))
                if not isinstance(data.username, str) or not isinstance(data.password, str):
                    raise AccountException(f'账号凭据格式错误: {user_id}/{account}')
                credentials_present = bool(data.username or data.password)
                if not credentials_present and not obsolete_batch_field:
                    continue

                if credentials_present:
                    existing = await openbao.read_game_credentials(user_id, account)
                    if existing != {"username": data.username, "password": data.password}:
                        await openbao.write_game_credentials(user_id, account, data.username, data.password)
                        migrated_credentials += 1
                    else:
                        existing_credentials += 1
                data.username = ""
                data.password = ""
                temporary = account_path + ".tmp"
                with open(temporary, 'w') as account_file:
                    account_file.write(data.to_json())
                    account_file.flush()
                    os.fsync(account_file.fileno())
                os.replace(temporary, account_path)
                cleaned_configs += 1
                if credentials_present:
                    logger.info(
                        "Migrated legacy game credentials to OpenBao for account %s/%s",
                        user_id,
                        account,
                    )
                elif obsolete_batch_field:
                    logger.info(
                        "Removed obsolete batch_accounts field from account config %s/%s",
                        user_id,
                        account,
                    )
        await self.migrate_game_sessions()
        if cleaned_configs:
            logger.info(
                "Finished legacy game credential migration: %d credentials copied "
                "to OpenBao, %d already present, %d account configs cleaned",
                migrated_credentials,
                existing_credentials,
                cleaned_configs,
            )

    async def migrate_game_sessions(self):
        token_dir = os.path.join(CACHE_DIR, "token")
        if not os.path.isdir(token_dir):
            return

        migrated_sessions = 0
        existing_sessions = 0
        for entry in os.scandir(token_dir):
            if (
                not entry.is_file(follow_symlinks=False)
                or not re.fullmatch(r"[a-f0-9]{32}", entry.name)
            ):
                continue
            with open(entry.path, "r") as session_file:
                try:
                    session = json.load(session_file)
                except json.JSONDecodeError as error:
                    raise AccountException(
                        f'游戏登录缓存格式错误: {entry.name}'
                    ) from error
            if not isinstance(session, dict):
                raise AccountException(f'游戏登录缓存格式错误: {entry.name}')
            uid = session.get("uid")
            access_key = session.get("access_key")
            if (
                not isinstance(uid, (str, int))
                or isinstance(uid, bool)
                or not isinstance(access_key, str)
            ):
                raise AccountException(f'游戏登录缓存格式错误: {entry.name}')

            existing = await openbao.read_game_session(entry.name)
            if existing is None:
                await openbao.write_game_session(entry.name, str(uid), access_key)
                migrated_sessions += 1
            else:
                existing_sessions += 1
            os.remove(entry.path)
        if migrated_sessions or existing_sessions:
            logger.info(
                "Migrated legacy game login sessions to OpenBao: %d copied, "
                "%d already present; removed local cache files",
                migrated_sessions,
                existing_sessions,
            )

    def account_names(self, qid: str) -> List[str]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT display_name FROM user_accounts
                WHERE qid = ? ORDER BY display_name
                """,
                (qid,),
            ).fetchall()
        return [row['display_name'] for row in rows]

    def has_account(self, qid: str, display_name: str) -> bool:
        with self._connect() as connection:
            return connection.execute(
                """
                SELECT 1 FROM user_accounts
                WHERE qid = ? AND display_name = ?
                """,
                (qid, display_name),
            ).fetchone() is not None

    def register_accounts(self, qid: str, display_names: List[str]):
        try:
            with self._connect() as connection:
                connection.executemany(
                    """
                    INSERT INTO user_accounts (qid, display_name)
                    VALUES (?, ?)
                    """,
                    [
                        (qid, display_name) for display_name in display_names
                    ],
                )
        except sqlite3.IntegrityError as error:
            raise AccountException('账号名重复或用户不存在') from error

    def unregister_account(self, qid: str, display_name: str):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                DELETE FROM user_accounts
                WHERE qid = ? AND display_name = ?
                """,
                (qid, display_name),
            )
        if cursor.rowcount == 0:
            raise AccountException("账号不存在")

    def get_user_data(self, qid: str) -> UserData:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT default_account, clan, admin, disabled
                FROM users WHERE qid = ?
                """,
                (qid,),
            ).fetchone()
        if row is None:
            raise UserException('用户不存在')
        return UserData(
            default_account=row['default_account'],
            clan=bool(row['clan']),
            admin=bool(row['admin']),
            disabled=bool(row['disabled']),
        )

    def save_user_data(self, qid: str, user_data: UserData):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE users
                SET default_account = ?, clan = ?, admin = ?, disabled = ?
                WHERE qid = ?
                """,
                (
                    user_data.default_account,
                    int(user_data.clan),
                    int(user_data.admin),
                    int(user_data.disabled),
                    qid,
                ),
            )
        if cursor.rowcount == 0:
            raise UserException('用户不存在')

    def set_password(self, qid: str, password: str):
        salt, password_hash = self._hash_password(password)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE users
                SET password_hash = ?, password_salt = ?, password_iterations = ?
                WHERE qid = ?
                """,
                (password_hash, salt, self.PASSWORD_ITERATIONS, qid),
            )
        if cursor.rowcount == 0:
            raise UserException('用户不存在')

    @staticmethod
    def _verify_password(row: sqlite3.Row, password: str) -> bool:
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            row['password_salt'],
            row['password_iterations'],
        )
        return hmac.compare_digest(password_hash, row['password_hash'])

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
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT password_hash, password_salt, password_iterations
                FROM users WHERE qid = ?
                """,
                (qid,),
            ).fetchone()
        return row is not None and self._verify_password(row, password)

    def check_enabled(self, qid: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT disabled FROM users WHERE qid = ?", (qid,)
            ).fetchone()
        return row is not None and not bool(row['disabled'])

    def qid_path(self, qid: str) -> str:
        return os.path.join(self.root, qid)

    def create(self, qid: str, password: str) -> AccountManager:
        if not UserManager.pathsyntax.fullmatch(qid):
            raise UserException('无效的QQ号')
        user_root = self.qid_path(qid)
        try:
            os.mkdir(user_root)
        except FileExistsError as error:
            raise UserException('QQ号已存在') from error

        salt, password_hash = self._hash_password(password)
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO users (
                        qid, password_hash, password_salt, password_iterations
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (qid, password_hash, salt, self.PASSWORD_ITERATIONS),
                )
        except sqlite3.IntegrityError as error:
            os.rmdir(user_root)
            raise UserException('QQ号已存在') from error
        except Exception:
            os.rmdir(user_root)
            raise

        try:
            self.shift_old_accounts(qid)
        except Exception:
            shutil.rmtree(user_root)
            with self._connect() as connection:
                connection.execute("DELETE FROM users WHERE qid = ?", (qid,))
            raise
        logger.info(f"Create user {qid}")
        return AccountManager(self, qid)

    def shift_old_accounts(self, qid: str):
        import glob
        migrations = []
        aliases = set()
        for config in glob.glob(os.path.join(OLD_CONFIG_PATH, "*.json")):
            with open(config, 'r') as f:
                data = json.load(f)
            if str(data.get('qq', '')) != qid:
                continue
            alias = data['alian']
            if not AccountManager.pathsyntax.fullmatch(alias) or alias.startswith(BATCHINFO):
                raise UserException(f'非法账户名{alias}')
            if alias in aliases or os.path.exists(os.path.join(self.qid_path(qid), alias + '.json')):
                raise AccountException(f'账号已存在: {alias}')
            aliases.add(alias)
            migrations.append((config, os.path.join(self.qid_path(qid), alias + '.json'), alias))

        moved = []
        try:
            for source, destination, _ in migrations:
                os.rename(source, destination)
                moved.append((source, destination))
            if migrations:
                self.register_accounts(qid, [alias for _, _, alias in migrations])
                logger.info(
                    "Migrated %d legacy account configs for user %s",
                    len(migrations),
                    qid,
                )
        except Exception:
            logger.exception("Failed to migrate legacy account configs for user %s", qid)
            for source, destination in reversed(moved):
                os.rename(destination, source)
            raise

    def load(self, qid: str, readonly: bool = False) -> AccountManager:
        if not UserManager.pathsyntax.fullmatch(qid):
            raise UserException('无效的QQ号')
        return AccountManager(self, qid, readonly)

    async def delete(self, qid: str, account: str = ""):
        if not UserManager.pathsyntax.fullmatch(qid):
            raise AccountException('无效的QQ号')
        if account:
            await self.load(qid).delete(account)
        else:
            for account_name in self.account_names(qid):
                await openbao.delete_game_credentials(qid, account_name)
            shutil.rmtree(self.qid_path(qid))
            with self._connect() as connection:
                connection.execute("DELETE FROM users WHERE qid = ?", (qid,))

    def qids(self) -> Iterator[str]:
        with self._connect() as connection:
            rows = connection.execute("SELECT qid FROM users ORDER BY qid").fetchall()
        yield from (row['qid'] for row in rows)

instance = UserManager(os.path.join(CONFIG_PATH))
