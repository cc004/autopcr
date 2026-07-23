import os, json, re
from typing import Dict, Pattern, Tuple
from ..constants import CACHE_DIR, DATA_DIR
from .assetmgr import assetmgr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..util.logger import instance as logger

# rainbow 表项中指向真实表名的特殊键
TABLE_NAME_KEY = "--table_name"

# 哈希名的形态：表名 = 'v1_' + sha256 十六进制，列名 = sha256 十六进制
HASHED_NAME = re.compile(r"(?:v1_)?[0-9a-f]{64}")

class dbmgr:
    def __init__(self):
        self.ver = None
        self._dbpath = None
        self._engine = None

    async def update_db(self, mgr: assetmgr):
        ver = mgr.ver
        self._dbpath = os.path.join(CACHE_DIR, 'db', f'{ver}.db')
        if not os.path.exists(self._dbpath):
            data = await mgr.db()
            with open(self._dbpath, 'wb') as f:
                f.write(data)
            logger.info(f'db version {ver} updated')
        self._engine = create_engine(f'sqlite:///{self._dbpath}')
        self.ver = ver
        self.unhash()

    def session(self) -> Session:
        return Session(self._engine)

    @staticmethod
    def _build_replacer(rainbow: dict) -> Tuple[Dict[str, str], Pattern]:
        # 表名与列名可以合并进同一个映射：哈希名全局唯一
        mapping: Dict[str, str] = {}
        for hashed_table, cols in rainbow.items():
            intact_table = cols.get(TABLE_NAME_KEY)
            if intact_table:
                mapping[hashed_table] = intact_table
            for hashed_col, intact_col in cols.items():
                if hashed_col != TABLE_NAME_KEY:
                    mapping[hashed_col] = intact_col
        mapping = {hashed: intact for hashed, intact in mapping.items() if hashed != intact}

        # 定长正则扫描 + 查表比上万个字面量拼成的 alternation 快两个数量级，形态不符则退回后者
        if all(HASHED_NAME.fullmatch(hashed) for hashed in mapping):
            return mapping, HASHED_NAME
        pattern = "|".join(sorted((re.escape(hashed) for hashed in mapping), key=len, reverse=True))
        return mapping, re.compile(pattern)

    def unhash(self):
        rainbow_json = os.path.join(DATA_DIR, 'rainbow.json')
        if not os.path.exists(rainbow_json):
            logger.error("Rainbow table not found, unhashing skipped.")
            return

        with open(rainbow_json, 'r') as f:
            mapping, pattern = self._build_replacer(json.load(f))

        def restore(text):
            if not text:
                return text
            return pattern.sub(lambda m: mapping.get(m.group(0), m.group(0)), text)

        logger.info("Start Unhashing DB.")
        with self._engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            schema_version = conn.exec_driver_sql("PRAGMA schema_version").scalar()
            rows = conn.exec_driver_sql(
                "SELECT rowid, type, name, tbl_name, sql FROM sqlite_master"
            ).fetchall()

            # 只改 schema 文本，不搬运数据行，故索引、触发器、视图原样保留；
            # rainbow 未覆盖的表/列不在映射里，自然保持原名
            updates = []
            renamed_tables = 0
            unresolved_tables = 0
            for rowid, type_, name, tbl_name, sql in rows:
                restored = (restore(name), restore(tbl_name), restore(sql))
                if type_ == 'table' and HASHED_NAME.fullmatch(restored[0]):
                    unresolved_tables += 1
                if restored == (name, tbl_name, sql):
                    continue
                updates.append((*restored, rowid))
                if type_ == 'table' and restored[0] != name:
                    renamed_tables += 1

            if unresolved_tables:
                logger.warning(f"{unresolved_tables} tables missing from rainbow table, left hashed.")

            if not updates:
                logger.info("DB is already unhashed, nothing to do.")
                return

            try:
                conn.exec_driver_sql("PRAGMA writable_schema=ON")
                conn.exec_driver_sql("BEGIN")
                conn.exec_driver_sql(
                    "UPDATE sqlite_master SET name=?, tbl_name=?, sql=? WHERE rowid=?", updates
                )
                conn.exec_driver_sql("COMMIT")
                # 直改 sqlite_master 不会更新库头的 schema cookie，手动 +1 让后续连接重载 schema
                conn.exec_driver_sql(f"PRAGMA schema_version={schema_version + 1}")
                # RESET 让当前连接立刻重载，需要 SQLite >= 3.32，老版本报错也无妨
                try:
                    conn.exec_driver_sql("PRAGMA writable_schema=RESET")
                except Exception:
                    pass
            finally:
                conn.exec_driver_sql("PRAGMA writable_schema=OFF")

            # sqlite_stat1 里记的还是旧哈希名，统计已失效，按真实名重建
            conn.exec_driver_sql("ANALYZE")

        # 连接池里可能还留着 schema 已过期的连接
        self._engine.dispose()
        logger.info(f"Unhashing complete, {renamed_tables} tables restored.")


instance = dbmgr()
