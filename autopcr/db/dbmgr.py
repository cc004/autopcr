import json
import os
import re
from typing import Iterable, List, Optional
from ..constants import CACHE_DIR, DATA_DIR
from .assetmgr import assetmgr
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from ..util.logger import instance as logger

class dbmgr:
    _identifier = re.compile(r'^[A-Za-z0-9_]+$')

    def __init__(self, region: str = 'cn'):
        self.region = region
        self.ver = None
        self.generation = 0
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
        self.dispose()
        self._engine = create_engine(f'sqlite:///{self._dbpath}')
        self.ver = ver
        self.unhash()
        self.generation += 1

    def load_db(self, path: str, ver: int):
        """Load an already decoded database (used by regional DB mirrors)."""
        self.dispose()
        self._dbpath = path
        self._engine = create_engine(f'sqlite:///{self._dbpath}')
        self.ver = int(ver)
        self.generation += 1

    def dispose(self):
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

    def session(self) -> Session:
        return Session(self._engine)

    @staticmethod
    def get_create_table(session: Session, table_name: str):
        result = session.execute(
            text(
                "SELECT sql FROM sqlite_master "
                "WHERE type='table' AND name=:table_name"
            ),
            {'table_name': table_name},
        ).fetchone()
        return result[0] if result else None

    @staticmethod
    def get_table_columns(session: Session, table_name: str):
        if not dbmgr._identifier.fullmatch(table_name):
            raise ValueError(f'Invalid database identifier: {table_name!r}')
        result = session.execute(
            text(f"PRAGMA table_info(`{table_name}`)")
        ).fetchall()
        return [row[1] for row in result]

    @staticmethod
    def exec_transaction(session: Session, commands: List[str]) -> bool:
        try:
            for cmd in commands:
                session.execute(text(cmd))
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            session.rollback()
            return False

    def unhash(
        self,
        rainbow_json: Optional[str] = None,
        *,
        strict: bool = False,
        required_tables: Iterable[str] = (),
    ) -> int:
        """Decode hashed table/column names using a regional rainbow table.

        ``strict`` is used while building the TW cache: a stale rainbow table
        must never produce a partially decoded database that looks usable.
        Existing CN behaviour remains best-effort for backwards compatibility.
        """
        rainbow_json = rainbow_json or os.path.join(DATA_DIR, 'rainbow.json')
        if not os.path.exists(rainbow_json):
            message = f"Rainbow table not found: {rainbow_json}"
            if strict:
                raise FileNotFoundError(message)
            logger.error("%s; unhashing skipped.", message)
            return 0

        with open(rainbow_json, 'r', encoding='utf-8') as fp:
            json_object = json.load(fp)
        for hashed_table_name, cols_dict in json_object.items():
            if not isinstance(cols_dict, dict):
                raise ValueError(
                    f'Invalid rainbow entry for {hashed_table_name!r}'
                )
            identifiers = [
                hashed_table_name,
                *(
                    name for name in cols_dict
                    if name != '--table_name'
                ),
                *cols_dict.values(),
            ]
            if any(
                not isinstance(name, str)
                or not self._identifier.fullmatch(name)
                for name in identifiers
            ):
                raise ValueError(
                    f'Invalid identifier in rainbow entry {hashed_table_name!r}'
                )
        logger.info("Start Unhashing DB with %s.", rainbow_json)

        decoded_count = 0
        with self.session() as session:
            # Validate all present hashed tables before mutating any of them.
            # This turns a mismatched TW map into an atomic build failure.
            for hashed_table_name, cols_dict in json_object.items():
                if self.get_create_table(session, hashed_table_name) is None:
                    continue
                actual_columns = set(
                    self.get_table_columns(session, hashed_table_name)
                )
                mapped_columns = set(cols_dict) - {"--table_name"}
                missing = mapped_columns - actual_columns
                if missing:
                    message = (
                        f"Rainbow table mismatch for {hashed_table_name}: "
                        f"missing {len(missing)} mapped columns"
                    )
                    if strict:
                        raise ValueError(message)
                    logger.error(message)

            for hashed_table_name, cols_dict in json_object.items():
                intact_table_name = cols_dict.get("--table_name")
                if not intact_table_name:
                    if strict:
                        raise ValueError(
                            f"Rainbow entry {hashed_table_name} has no table name"
                        )
                    continue

                create_table_statement = self.get_create_table(
                    session, hashed_table_name
                )
                decoded_table_statement = self.get_create_table(
                    session, intact_table_name
                )
                if create_table_statement is None:
                    if strict and decoded_table_statement is None:
                        # A regional map may contain a few tables absent from a
                        # particular version, so absence alone is not fatal.
                        logger.debug(
                            "Mapped table %s (%s) is absent",
                            intact_table_name,
                            hashed_table_name,
                        )
                    continue

                hashed_cols = []
                intact_cols = []
                create_table_statement = create_table_statement.replace(
                    hashed_table_name, intact_table_name
                )
                for hashed_col_name, intact_col_name in cols_dict.items():
                    if hashed_col_name == "--table_name":
                        continue
                    hashed_cols.append(hashed_col_name)
                    intact_cols.append(intact_col_name)
                    create_table_statement = create_table_statement.replace(
                        hashed_col_name, intact_col_name
                    )

                for hashed_col_name in self.get_table_columns(
                    session, hashed_table_name
                ):
                    if hashed_col_name not in hashed_cols:
                        hashed_cols.append(hashed_col_name)
                        intact_cols.append(hashed_col_name)

                insert_statement = (
                    f"INSERT INTO `{intact_table_name}` "
                    f"(`{'`, `'.join(intact_cols)}`) "
                    f"SELECT `{'`, `'.join(hashed_cols)}` "
                    f"FROM `{hashed_table_name}`"
                )
                drop_table_statement = f"DROP TABLE `{hashed_table_name}`"
                transaction_cmd = [
                    create_table_statement,
                    insert_statement,
                    drop_table_statement,
                ]
                if not self.exec_transaction(session, transaction_cmd):
                    message = (
                        f"Failed to decode {intact_table_name} "
                        f"({hashed_table_name})"
                    )
                    if strict:
                        raise ValueError(message)
                    logger.error(message)
                    continue
                decoded_count += 1

            missing_required = [
                table
                for table in required_tables
                if self.get_create_table(session, table) is None
            ]
            minimum_coverage = max(1, len(json_object) * 4 // 5)
            if strict and decoded_count < minimum_coverage:
                raise ValueError(
                    "Rainbow table coverage is too low: "
                    f"decoded {decoded_count}/{len(json_object)} tables"
                )
            if missing_required:
                raise ValueError(
                    "Decoded database is missing required tables: "
                    + ", ".join(missing_required)
                )

        logger.info("Unhashing complete: %s tables decoded.", decoded_count)
        return decoded_count


_instances = {'cn': dbmgr('cn')}


def get_dbmgr(region: str = 'cn') -> dbmgr:
    if region not in _instances:
        _instances[region] = dbmgr(region)
    return _instances[region]


instance = get_dbmgr('cn')
