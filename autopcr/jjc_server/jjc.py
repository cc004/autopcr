from __future__ import annotations

import asyncio
import enum
import json
import random
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from itertools import combinations, permutations, product
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

import numpy as np
from dataclasses_json import dataclass_json

from ..constants import CACHE_DIR, DATA_DIR
from ..mzq.mzq import UnitDTO, instance as mzq_server, simulation_trace_id
from ..util.logger import instance as logging
from .onnx_model_manager import JJCModelManager
from .simulation_config import progression_kwargs
from .timing import current_trace_id, log_stage, timed_suggestion


AUTOPCR_CACHE_DIR = Path(CACHE_DIR).expanduser().resolve()
JJC_CACHE_DIR = AUTOPCR_CACHE_DIR / "jjc_server"
JJC_RECORD_DATABASE = JJC_CACHE_DIR / "jjc_record.sqlite3"
JJC_MODEL_DIR = Path(DATA_DIR).expanduser().resolve() / "jjc"
TRANSFORMER_CHECKPOINT = JJC_MODEL_DIR / "generator.onnx"
CRITIC_CHECKPOINT = JJC_MODEL_DIR / "critic.onnx"


TEAM_SIZE = 5
TEAM_TABLE = "jjc_teams"
MAIN_RESULT_TABLE = "jjc_results"
BUFFER_RESULT_TABLES = {
    "b": "jjc_results_buffer_b",
    "c": "jjc_results_buffer_c",
}
RESULT_TABLES = (MAIN_RESULT_TABLE, *BUFFER_RESULT_TABLES.values())
OUTCOME_COLUMNS = (
    "win_0_15",
    "win_15_30",
    "win_30_60",
    "win_60_90",
    "losses",
    "timeouts",
)
DEFAULT_PICK_PER_LEVELS = (10, 2, 2, 2, 1)
SUGGESTION_HISTORY_PICK_PER_LEVELS = (10, 0, 0, 0, 0)
DEFAULT_SUGGESTION_LIMIT = 64
HISTORICAL_SUGGESTION_CACHE_SIZE = 128
SUGGESTION_CACHE_TABLE = "jjc_suggestion_cache"
SUGGESTION_CACHE_READY_COUNT = 16
SUGGESTION_CRITIC_LIMIT = 54
SUGGESTION_TRANSFORMER_RECALL = 256
SUGGESTION_HOT_TEAM_LIMIT = 10
SUGGESTION_REPEAT_COUNT = 10
SUGGESTION_MIN_WINS = 8


class eJJCStatus(enum.IntEnum):
    WIN = 0
    LOSS = 1
    TIMEOUT = 2
    UNKNOWN = 3


@dataclass_json
@dataclass
class JJCResult:
    duration: float = 0.0
    result: eJJCStatus = eJJCStatus.UNKNOWN
    seed: int = 666
    timestamp: float = field(default_factory=time.time)
    player_info: List[UnitDTO] = field(default_factory=list)
    enemy_info: List[UnitDTO] = field(default_factory=list)
    talent_level: str = ""
    talent_skill: str = ""
    team_skill: str = ""


@dataclass_json
@dataclass
class JJCRecord:
    attacks: List[int] = field(default_factory=list)
    defends: List[int] = field(default_factory=list)
    results: List[JJCResult] = field(default_factory=list)

    def is_cache_expired(self, max_age_seconds: float = 15 * 24 * 3600) -> bool:
        if not self.results:
            return True
        self.results = [
            result
            for result in self.results
            if time.time() - result.timestamp <= max_age_seconds
        ]
        return not self.results

    def description(self, include_attack: bool = True, include_defend: bool = True) -> str:
        from ..db.database import db

        def names(units: Sequence[int]) -> str:
            return " ".join(db.get_unit_name(uid) for uid in db.deck_sort_unit(units))

        grouped = {status: [] for status in eJJCStatus}
        for result in self.results:
            grouped[result.result].append(result.duration)

        def average(values: Sequence[float]) -> float:
            return sum(values) / len(values) if values else 0.0

        parts: List[str] = []
        if include_attack:
            parts.append(names(self.attacks))
        if include_defend:
            parts.append(names(self.defends))
        summary = []
        if grouped[eJJCStatus.WIN]:
            summary.append(
                f"{len(grouped[eJJCStatus.WIN])}胜"
                f"({average(grouped[eJJCStatus.WIN]):.1f}s)"
            )
        if grouped[eJJCStatus.LOSS]:
            summary.append(
                f"{len(grouped[eJJCStatus.LOSS])}负"
                f"({average(grouped[eJJCStatus.LOSS]):.1f}s)"
            )
        if grouped[eJJCStatus.TIMEOUT]:
            summary.append(f"{len(grouped[eJJCStatus.TIMEOUT])}超时")
        if grouped[eJJCStatus.UNKNOWN]:
            summary.append(f"{len(grouped[eJJCStatus.UNKNOWN])}未知")
        return " vs ".join(parts) + " | " + " ".join(summary)

    @property
    def win_rate(self) -> float:
        if not self.results:
            return 0.0
        return sum(result.result == eJJCStatus.WIN for result in self.results) / len(
            self.results
        )

    @property
    def sort_key(self) -> float:
        wins = [
            result.duration
            for result in self.results
            if result.result == eJJCStatus.WIN
        ]
        average = sum(wins) / len(wins) if wins else float("inf")
        return -((self.win_rate * 10_000_000) - average)

    @property
    def defend_sort_key(self) -> float:
        wins = [
            result.duration
            for result in self.results
            if result.result == eJJCStatus.WIN
        ]
        average = sum(wins) / len(wins) if wins else float("-inf")
        return -((self.win_rate * 10_000_000) + average)

    def __str__(self) -> str:
        return self.description()


def record_to_payload(record: JJCRecord) -> Dict[str, Any]:
    """Serialize one record compactly for the persistent cache and HTTP API."""
    sample = record.results[0] if record.results else None
    return {
        "attacks": [int(value) for value in record.attacks],
        "defends": [int(value) for value in record.defends],
        "results": [
            {
                "duration": float(result.duration),
                "result": int(result.result),
                "seed": int(result.seed),
                "timestamp": float(result.timestamp),
            }
            for result in record.results
        ],
        "player_info": [unit.dict() for unit in (sample.player_info if sample else [])],
        "enemy_info": [unit.dict() for unit in (sample.enemy_info if sample else [])],
        "talent_level": sample.talent_level if sample else "",
        "talent_skill": sample.talent_skill if sample else "",
        "team_skill": sample.team_skill if sample else "",
    }


def record_from_payload(payload: Dict[str, Any]) -> JJCRecord:
    """Restore the compact cache/API representation into the shared domain type."""
    player_info = [UnitDTO.parse_obj(value) for value in payload.get("player_info", [])]
    enemy_info = [UnitDTO.parse_obj(value) for value in payload.get("enemy_info", [])]
    results = [
        JJCResult(
            duration=float(value.get("duration", 0.0)),
            result=eJJCStatus(int(value.get("result", eJJCStatus.UNKNOWN))),
            seed=int(value.get("seed", 666)),
            timestamp=float(value.get("timestamp", 0.0)),
            player_info=player_info,
            enemy_info=enemy_info,
            talent_level=str(payload.get("talent_level", "")),
            talent_skill=str(payload.get("talent_skill", "")),
            team_skill=str(payload.get("team_skill", "")),
        )
        for value in payload.get("results", [])
    ]
    return JJCRecord(
        attacks=[int(value) for value in payload.get("attacks", [])],
        defends=[int(value) for value in payload.get("defends", [])],
        results=results,
    )


def recommendation_rank_key(record: JJCRecord) -> tuple[float, float]:
    results = list(record.results)
    win_durations = [
        float(result.duration)
        for result in results
        if result.result == eJJCStatus.WIN
    ]
    return (
        -(len(win_durations) / len(results) if results else 0.0),
        sum(win_durations) / len(win_durations)
        if win_durations
        else float("inf"),
    )


def recommendation_group_rank_key(
    group: Sequence[JJCRecord],
) -> tuple[float, float]:
    results = [result for record in group for result in record.results]
    win_durations = [
        float(result.duration)
        for result in results
        if result.result == eJJCStatus.WIN
    ]
    return (
        -(len(win_durations) / len(results) if results else 0.0),
        sum(win_durations) / len(win_durations)
        if win_durations
        else float("inf"),
    )


@dataclass
class JJCHotTeam:
    team: List[int]
    count: int


JJCBlindPairKey = Tuple[str, str]


@dataclass
class JJCMatrixResult:
    matrix: List[List[float]] = field(default_factory=list)
    attacks: List[List[UnitDTO]] = field(default_factory=list)
    defends: List[List[UnitDTO]] = field(default_factory=list)
    header_result: Optional[JJCResult] = None
    raw_result: Dict[JJCBlindPairKey, JJCRecord] = field(default_factory=dict)

    def truncate(self, limit: int) -> "JJCMatrixResult":
        return JJCMatrixResult(
            matrix=self.matrix[:limit],
            attacks=self.attacks[:limit],
            defends=self.defends,
            header_result=self.header_result,
            raw_result=self.raw_result,
        )


@dataclass
class PJJCMatrixResult:
    matrix: List[List[List[float]]] = field(default_factory=list)
    attacks: List[List[List[UnitDTO]]] = field(default_factory=list)
    defends: List[List[UnitDTO]] = field(default_factory=list)
    win_rate: List[float] = field(default_factory=list)
    header_result: Optional[JJCResult] = None
    raw_result: Dict[JJCBlindPairKey, JJCRecord] = field(default_factory=dict)

    def truncate(self, limit: int) -> "PJJCMatrixResult":
        return PJJCMatrixResult(
            matrix=self.matrix[:limit],
            attacks=self.attacks[:limit],
            defends=self.defends,
            win_rate=self.win_rate[:limit],
            header_result=self.header_result,
            raw_result=self.raw_result,
        )


def format_team_name(team: Sequence[int]) -> str:
    """Format a team for Bot/text presentation without coupling it to storage."""
    from ..db.database import db

    return " ".join(db.get_unit_name(uid) for uid in team)


def format_matrix_text(result: JJCMatrixResult) -> str:
    """Render a JJC matrix as plain text for Bot and diagnostic callers."""
    lines = [" | ".join(["攻\\防", *[f"D{i + 1}" for i in range(len(result.defends))]])]
    for index, row in enumerate(result.matrix):
        lines.append(
            " | ".join(
                [
                    f"A{index + 1}",
                    *["N/A" if rate == -1 else f"{rate * 100:0f}%" for rate in row],
                ]
            )
        )
    lines.extend(["", "防守队伍："])
    for index, defend in enumerate(result.defends, 1):
        lines.append(f"D{index}: {format_team_name([unit.unitId for unit in defend])}")
    lines.extend(["", "进攻队伍："])
    for index, attack in enumerate(result.attacks, 1):
        lines.append(f"A{index}: {format_team_name([unit.unitId for unit in attack])}")
    return "\n".join(lines)


def format_pjjc_blind_groups_text(
    result: PJJCMatrixResult,
    limit: int = 8,
) -> str:
    """Render PJJC blind-attack groups as plain text."""
    lines: List[str] = []
    for index, group in enumerate(result.attacks[:limit], 1):
        needed = (len(group) + 1) // 2
        lines.append(
            f"{index}. {len(group)}局{needed}胜率{result.win_rate[index - 1] * 100:.1f}%"
        )
        for team_index, attack in enumerate(group, 1):
            lines.append(
                f"  A{team_index}: {format_team_name([unit.unitId for unit in attack])}"
            )
    return "\n".join(lines)


def combine_pjjc_attack(
    attacks: Sequence[Sequence[JJCRecord]],
    defend: bool = False,
) -> List[List[JJCRecord]]:
    """Combine non-overlapping PJJC teams without involving persistence."""
    candidates = [
        list(combo)
        for combo in product(*attacks)
        if len({uid for record in combo for uid in record.attacks})
        == sum(len(record.attacks) for record in combo)
    ]
    key = (
        (lambda combo: sum(record.defend_sort_key for record in combo))
        if defend
        else (lambda combo: sum(record.sort_key for record in combo))
    )
    candidates.sort(key=key)
    return candidates


@dataclass(frozen=True)
class MatchupObservation:
    attack: tuple[int, ...]
    defend: tuple[int, ...]
    counts: tuple[int, int, int, int, int, int]
    observed_at: float


@dataclass(frozen=True)
class ModelState:
    active_buffer: str
    transformer_checkpoint: str | None
    critic_checkpoint: str | None


class JJCRecordManager:
    """JJC battle records, cached ONNX recommendations, and simulator transport."""

    def __init__(
        self,
        db_path: str | Path | None = None,
        transformer_checkpoint: str | Path = TRANSFORMER_CHECKPOINT,
        critic_checkpoint: str | Path = CRITIC_CHECKPOINT,
        device: str = "auto",
    ) -> None:
        resolved = Path(db_path or JJC_RECORD_DATABASE).expanduser().resolve()
        resolved.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = str(resolved)
        self.model_manager = JJCModelManager(
            transformer_checkpoint,
            critic_checkpoint,
            device,
        )
        self._lock = asyncio.Lock()
        self._model_inference_lock = Lock()
        self._team_id_cache: Dict[tuple[int, ...], int] = {}
        self._team_units_cache: Dict[int, tuple[int, ...]] = {}
        self._historical_suggestion_cache: Dict[
            tuple[tuple[int, ...], tuple[int, ...]],
            Dict[int, tuple[int, ...]],
        ] = {}
        self._historical_suggestion_cache_lock = Lock()
        self._suggestion_build_locks: Dict[tuple[int, ...], asyncio.Lock] = {}
        self.conn = self._open_connection(setup_wal=True)
        self._init_db()
        state = self.model_state()
        transformer_path, critic_path = self._active_checkpoint_paths(state)
        self.model_manager.set_checkpoints(transformer_path, critic_path)
        self._store_active_checkpoint_references(transformer_path, critic_path)

    def close(self) -> None:
        self.conn.close()

    def _open_connection(self, setup_wal: bool = False) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=60.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=60000")
        if setup_wal:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    @staticmethod
    def _checkpoint_reference(path: str | Path) -> str:
        """Store portable references to data assets and cache-local checkpoints."""
        resolved = Path(path).expanduser().resolve()
        try:
            return "data/" + resolved.relative_to(Path(DATA_DIR).resolve()).as_posix()
        except ValueError:
            pass
        try:
            return resolved.relative_to(AUTOPCR_CACHE_DIR).as_posix()
        except ValueError:
            return str(resolved)

    @staticmethod
    def _resolve_checkpoint_reference(
        reference: str | None,
        fallback: str | Path,
    ) -> Path:
        """Resolve portable state and rebase stale cache paths from another host."""
        fallback_path = Path(fallback).expanduser().resolve()
        if not reference:
            return fallback_path
        raw_path = Path(reference).expanduser()
        # Old SQLite state may still point at readable .pt checkpoints. Never
        # select those for inference after switching to the bundled ONNX files.
        if raw_path.suffix != ".onnx":
            return fallback_path
        if not raw_path.is_absolute() and raw_path.parts[:1] == ("data",):
            return Path(DATA_DIR).resolve().parent.joinpath(raw_path)
        if raw_path.is_absolute() and "data" in raw_path.parts:
            index = len(raw_path.parts) - 1 - raw_path.parts[::-1].index("data")
            if raw_path.parts[index + 1:index + 2] == ("jjc",):
                rebased = Path(DATA_DIR).resolve().joinpath(*raw_path.parts[index + 1:])
                if not raw_path.is_file():
                    return rebased
        candidate = (
            raw_path.resolve()
            if raw_path.is_absolute()
            else (AUTOPCR_CACHE_DIR / raw_path).resolve()
        )
        if candidate.is_file() or not raw_path.is_absolute():
            return candidate

        parts = raw_path.parts
        for index in range(len(parts) - 1):
            if parts[index : index + 2] != ("cache", "jjc_server"):
                continue
            rebased = (AUTOPCR_CACHE_DIR.joinpath(*parts[index + 1 :])).resolve()
            if rebased.is_file():
                return rebased
            return fallback_path if fallback_path.is_file() else rebased
        return candidate

    def _active_checkpoint_paths(
        self,
        state: ModelState | None = None,
    ) -> tuple[Path, Path]:
        current = state or self.model_state()
        return (
            self._resolve_checkpoint_reference(
                current.transformer_checkpoint,
                self.model_manager.transformer_output_path,
            ),
            self._resolve_checkpoint_reference(
                current.critic_checkpoint,
                self.model_manager.critic_output_path,
            ),
        )

    def _store_active_checkpoint_references(
        self,
        transformer_checkpoint: str | Path,
        critic_checkpoint: str | Path,
    ) -> None:
        transformer_reference = self._checkpoint_reference(transformer_checkpoint)
        critic_reference = self._checkpoint_reference(critic_checkpoint)
        row = self.conn.execute(
            "SELECT transformer_checkpoint,critic_checkpoint FROM jjc_state WHERE singleton=1"
        ).fetchone()
        if row is not None and (
            row["transformer_checkpoint"] != transformer_reference
            or row["critic_checkpoint"] != critic_reference
        ):
            with self._immediate_transaction():
                self.conn.execute(
                    "UPDATE jjc_state SET transformer_checkpoint=?,critic_checkpoint=? "
                    "WHERE singleton=1",
                    (transformer_reference, critic_reference),
                )

    @contextmanager
    def _immediate_transaction(self) -> Iterator[None]:
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    @staticmethod
    def _outcome_schema() -> str:
        return """
            bucket_start INTEGER NOT NULL,
            attack_team_id INTEGER NOT NULL REFERENCES jjc_teams(team_id),
            defend_team_id INTEGER NOT NULL REFERENCES jjc_teams(team_id),
            win_0_15 INTEGER NOT NULL,
            win_15_30 INTEGER NOT NULL,
            win_30_60 INTEGER NOT NULL,
            win_60_90 INTEGER NOT NULL,
            losses INTEGER NOT NULL,
            timeouts INTEGER NOT NULL,
            first_battle_ts REAL NOT NULL,
            last_battle_ts REAL NOT NULL,
            PRIMARY KEY(bucket_start, attack_team_id, defend_team_id)
        """

    def _init_db(self) -> None:
        outcome_schema = self._outcome_schema()
        self.conn.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS jjc_teams (
                team_id INTEGER PRIMARY KEY,
                unit_1 INTEGER NOT NULL,
                unit_2 INTEGER NOT NULL,
                unit_3 INTEGER NOT NULL,
                unit_4 INTEGER NOT NULL,
                unit_5 INTEGER NOT NULL,
                UNIQUE(unit_1, unit_2, unit_3, unit_4, unit_5)
            );
            CREATE TABLE IF NOT EXISTS {MAIN_RESULT_TABLE} ({outcome_schema}) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS {BUFFER_RESULT_TABLES['b']} ({outcome_schema}) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS {BUFFER_RESULT_TABLES['c']} ({outcome_schema}) WITHOUT ROWID;
            CREATE TABLE IF NOT EXISTS jjc_state (
                singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
                active_buffer TEXT NOT NULL CHECK(active_buffer IN ('b', 'c')),
                transformer_checkpoint TEXT,
                critic_checkpoint TEXT
            );
            INSERT OR IGNORE INTO jjc_state(
                singleton, active_buffer, transformer_checkpoint, critic_checkpoint
            ) VALUES (
                1, 'b',
                {json.dumps(self._checkpoint_reference(self.model_manager.transformer_output_path))},
                {json.dumps(self._checkpoint_reference(self.model_manager.critic_output_path))}
            );
            CREATE TABLE IF NOT EXISTS {SUGGESTION_CACHE_TABLE} (
                defend_team_id INTEGER NOT NULL REFERENCES jjc_teams(team_id),
                attack_team_id INTEGER NOT NULL REFERENCES jjc_teams(team_id),
                record_json TEXT NOT NULL,
                cached_at REAL NOT NULL,
                PRIMARY KEY(defend_team_id, attack_team_id)
            ) WITHOUT ROWID;
            CREATE INDEX IF NOT EXISTS idx_jjc_results_defend
                ON {MAIN_RESULT_TABLE}(defend_team_id, attack_team_id);
            CREATE INDEX IF NOT EXISTS idx_jjc_suggestion_cache_defend
                ON {SUGGESTION_CACHE_TABLE}(defend_team_id, cached_at DESC);
            CREATE INDEX IF NOT EXISTS idx_jjc_results_recent
                ON {MAIN_RESULT_TABLE}(last_battle_ts DESC);
            """
        )
        self.conn.commit()
        columns = {
            str(row[1]) for row in self.conn.execute("PRAGMA table_info(jjc_teams)")
        }
        required = {"team_id", "unit_1", "unit_2", "unit_3", "unit_4", "unit_5"}
        if not required <= columns or "team_key" in columns:
            raise RuntimeError(
                "jjc_record.sqlite3 uses the retired schema; archive it before starting "
                "the single-manager database"
            )

    @staticmethod
    def _normalize_unit_id(unit_id: int) -> int:
        value = int(unit_id)
        return value * 100 + 1 if 1000 <= value < 10000 else value

    @classmethod
    def _canonical_team(
        cls,
        values: Sequence[int],
        *,
        require_full: bool = True,
    ) -> tuple[int, ...]:
        team = tuple(sorted({cls._normalize_unit_id(value) for value in values}))
        if require_full and len(team) != TEAM_SIZE:
            raise ValueError("team must contain five distinct unit IDs")
        return team

    @classmethod
    def _normalize_team(cls, values: Sequence[int]) -> List[int]:
        return list(cls._canonical_team(values, require_full=False))

    @classmethod
    def _to_team_key(cls, values: Sequence[int]) -> str:
        return ",".join(str(value) for value in cls._normalize_team(values))

    def _find_team_id_unlocked(
        self,
        cursor: sqlite3.Cursor,
        team: Sequence[int],
    ) -> Optional[int]:
        canonical = self._canonical_team(team)
        cached = self._team_id_cache.get(canonical)
        if cached is not None:
            return cached
        row = cursor.execute(
            """
            SELECT team_id FROM jjc_teams
            WHERE unit_1=? AND unit_2=? AND unit_3=? AND unit_4=? AND unit_5=?
            """,
            canonical,
        ).fetchone()
        if row is None:
            return None
        team_id = int(row[0])
        self._team_id_cache[canonical] = team_id
        self._team_units_cache[team_id] = canonical
        return team_id

    def _ensure_team_unlocked(
        self,
        cursor: sqlite3.Cursor,
        team: Sequence[int],
    ) -> tuple[int, tuple[int, ...]]:
        canonical = self._canonical_team(team)
        team_id = self._find_team_id_unlocked(cursor, canonical)
        if team_id is None:
            cursor.execute(
                """
                INSERT OR IGNORE INTO jjc_teams(
                    unit_1, unit_2, unit_3, unit_4, unit_5
                ) VALUES (?, ?, ?, ?, ?)
                """,
                canonical,
            )
            team_id = self._find_team_id_unlocked(cursor, canonical)
        if team_id is None:
            raise RuntimeError("failed to resolve JJC team")
        return team_id, canonical

    def _load_team_units_unlocked(
        self,
        cursor: sqlite3.Cursor,
        team_id: int,
    ) -> List[int]:
        cached = self._team_units_cache.get(int(team_id))
        if cached is not None:
            return list(cached)
        row = cursor.execute(
            """
            SELECT unit_1, unit_2, unit_3, unit_4, unit_5
            FROM jjc_teams WHERE team_id=?
            """,
            (int(team_id),),
        ).fetchone()
        if row is None:
            return []
        team = tuple(int(value) for value in row)
        self._team_units_cache[int(team_id)] = team
        self._team_id_cache[team] = int(team_id)
        return list(team)

    @staticmethod
    def _result_table(buffer: str) -> str:
        try:
            return BUFFER_RESULT_TABLES[str(buffer).lower()]
        except KeyError as exc:
            raise ValueError(f"unknown JJC result buffer: {buffer}") from exc

    @staticmethod
    def _result_counts(result: JJCResult) -> tuple[int, int, int, int, int, int]:
        if result.result == eJJCStatus.WIN:
            duration = float(result.duration)
            index = 0 if duration <= 15 else 1 if duration <= 30 else 2 if duration <= 60 else 3
            counts = [0] * 6
            counts[index] = 1
            return tuple(counts)  # type: ignore[return-value]
        if result.result == eJJCStatus.LOSS:
            return (0, 0, 0, 0, 1, 0)
        if result.result == eJJCStatus.TIMEOUT:
            return (0, 0, 0, 0, 0, 1)
        return (0, 0, 0, 0, 0, 0)

    def record_matchups(self, observations: Iterable[MatchupObservation]) -> str:
        rows = list(observations)
        if not rows:
            return self.model_state().active_buffer
        buffer = ""
        with self._immediate_transaction():
            state = self.conn.execute(
                "SELECT active_buffer FROM jjc_state WHERE singleton=1"
            ).fetchone()
            if state is None:
                raise RuntimeError("JJC state row is missing")
            buffer = str(state[0])
            table = self._result_table(buffer)
            cursor = self.conn.cursor()
            for observation in rows:
                counts = tuple(int(value) for value in observation.counts)
                if len(counts) != 6 or any(value < 0 for value in counts):
                    raise ValueError("outcome counts must contain six non-negative integers")
                if not sum(counts):
                    continue
                attack_id, _ = self._ensure_team_unlocked(cursor, observation.attack)
                defend_id, _ = self._ensure_team_unlocked(cursor, observation.defend)
                observed_at = float(observation.observed_at)
                bucket_start = int(observed_at // 3600) * 3600
                self.conn.execute(
                    f"""
                    INSERT INTO {table}(
                        bucket_start, attack_team_id, defend_team_id,
                        win_0_15, win_15_30, win_30_60, win_60_90,
                        losses, timeouts, first_battle_ts, last_battle_ts
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(bucket_start, attack_team_id, defend_team_id)
                    DO UPDATE SET
                        win_0_15=win_0_15+excluded.win_0_15,
                        win_15_30=win_15_30+excluded.win_15_30,
                        win_30_60=win_30_60+excluded.win_30_60,
                        win_60_90=win_60_90+excluded.win_60_90,
                        losses=losses+excluded.losses,
                        timeouts=timeouts+excluded.timeouts,
                        first_battle_ts=MIN(first_battle_ts, excluded.first_battle_ts),
                        last_battle_ts=MAX(last_battle_ts, excluded.last_battle_ts)
                    """,
                    (bucket_start, attack_id, defend_id, *counts, observed_at, observed_at),
                )
        if rows:
            self._clear_historical_suggestion_cache()
        return buffer

    async def save_record(self, record: JJCRecord) -> None:
        observations = [
            MatchupObservation(
                attack=self._canonical_team(record.attacks),
                defend=self._canonical_team(record.defends),
                counts=self._result_counts(result),
                observed_at=float(result.timestamp),
            )
            for result in record.results
            if sum(self._result_counts(result))
        ]
        async with self._lock:
            self.record_matchups(observations)

    def batch_import(self, records: List[JJCRecord]) -> None:
        observations = [
            MatchupObservation(
                self._canonical_team(record.attacks),
                self._canonical_team(record.defends),
                self._result_counts(result),
                float(result.timestamp),
            )
            for record in records
            for result in record.results
            if sum(self._result_counts(result))
        ]
        self.record_matchups(observations)

    def _aggregate_pair_unlocked(
        self,
        cursor: sqlite3.Cursor,
        attack_id: int,
        defend_id: int,
        limit_buckets: int = 100,
    ) -> List[sqlite3.Row]:
        union = " UNION ALL ".join(
            f"""
            SELECT bucket_start, win_0_15, win_15_30, win_30_60, win_60_90,
                   losses, timeouts, first_battle_ts, last_battle_ts
            FROM {table} WHERE attack_team_id=? AND defend_team_id=?
            """
            for table in RESULT_TABLES
        )
        parameters = tuple(
            value
            for _table in RESULT_TABLES
            for value in (int(attack_id), int(defend_id))
        )
        return cursor.execute(
            f"""
            SELECT bucket_start,
                   SUM(win_0_15) AS win_0_15,
                   SUM(win_15_30) AS win_15_30,
                   SUM(win_30_60) AS win_30_60,
                   SUM(win_60_90) AS win_60_90,
                   SUM(losses) AS losses,
                   SUM(timeouts) AS timeouts,
                   MIN(first_battle_ts) AS first_battle_ts,
                   MAX(last_battle_ts) AS last_battle_ts
            FROM ({union})
            GROUP BY bucket_start
            ORDER BY bucket_start DESC
            LIMIT ?
            """,
            (*parameters, max(1, int(limit_buckets))),
        ).fetchall()

    @staticmethod
    def _representative_results(rows: Sequence[sqlite3.Row]) -> List[JJCResult]:
        durations = (10.0, 22.5, 45.0, 75.0)
        results: List[JJCResult] = []
        for row in reversed(rows):
            timestamp = float(row["last_battle_ts"])
            for index, duration in enumerate(durations):
                results.extend(
                    JJCResult(duration, eJJCStatus.WIN, 0, timestamp)
                    for _ in range(int(row[OUTCOME_COLUMNS[index]] or 0))
                )
            results.extend(
                JJCResult(90.0, eJJCStatus.LOSS, 0, timestamp)
                for _ in range(int(row["losses"] or 0))
            )
            results.extend(
                JJCResult(90.0, eJJCStatus.TIMEOUT, 0, timestamp)
                for _ in range(int(row["timeouts"] or 0))
            )
        return results

    async def get_record(self, attacks: List[int], defends: List[int]) -> JJCRecord:
        conn = self._open_connection()
        try:
            cursor = conn.cursor()
            attack_id = self._find_team_id_unlocked(cursor, attacks)
            defend_id = self._find_team_id_unlocked(cursor, defends)
            if attack_id is None or defend_id is None:
                return JJCRecord(list(attacks), list(defends), [])
            rows = self._aggregate_pair_unlocked(cursor, attack_id, defend_id)
            return JJCRecord(
                list(attacks),
                list(defends),
                self._representative_results(rows),
            )
        finally:
            conn.close()

    def _historical_attack_ids(
        self,
        cursor: sqlite3.Cursor,
        defend_id: int,
        limit: int,
    ) -> List[int]:
        union = " UNION ALL ".join(
            f"""
            SELECT attack_team_id, win_0_15, win_15_30, win_30_60, win_60_90,
                   losses, timeouts
            FROM {table} WHERE defend_team_id=?
            """
            for table in RESULT_TABLES
        )
        return [
            int(row[0])
            for row in cursor.execute(
                f"""
                SELECT attack_team_id,
                       SUM(win_0_15+win_15_30+win_30_60+win_60_90) AS wins,
                       SUM(win_0_15+win_15_30+win_30_60+win_60_90+losses+timeouts) AS runs
                FROM ({union})
                GROUP BY attack_team_id
                HAVING wins > 0
                ORDER BY CAST(wins AS REAL)/runs DESC, wins DESC, runs DESC
                LIMIT ?
                """,
                (*([int(defend_id)] * len(RESULT_TABLES)), max(1, int(limit))),
            )
        ]

    def _historical_attack_ids_by_overlap(
        self,
        cursor: sqlite3.Cursor,
        opponent: Sequence[int],
        pick_per_levels: Sequence[int],
    ) -> Dict[int, List[int]]:
        """Return winning attacks grouped by exact 5/4/3/2/1-role overlap."""
        canonical = self._canonical_team(opponent)
        limits = tuple(
            max(0, int(pick_per_levels[index]))
            if index < len(pick_per_levels)
            else 0
            for index in range(TEAM_SIZE)
        )
        cache_key = (canonical, limits)
        with self._historical_suggestion_cache_lock:
            cached = self._historical_suggestion_cache.get(cache_key)
        if cached is not None:
            return {overlap: list(team_ids) for overlap, team_ids in cached.items()}

        result = {overlap: [] for overlap in range(TEAM_SIZE, 0, -1)}
        active_overlaps = [
            TEAM_SIZE - index for index, limit in enumerate(limits) if limit > 0
        ]
        if not active_overlaps:
            return result

        if active_overlaps == [TEAM_SIZE]:
            defend_id = self._find_team_id_unlocked(cursor, canonical)
            if defend_id is not None:
                result[TEAM_SIZE] = self._historical_attack_ids(
                    cursor,
                    defend_id,
                    limits[0],
                )
        else:
            outcome_union = " UNION ALL ".join(
                f"""
                SELECT attack_team_id, defend_team_id,
                       win_0_15, win_15_30, win_30_60, win_60_90,
                       losses, timeouts
                FROM {table}
                """
                for table in RESULT_TABLES
            )
            placeholders = ",".join("?" for _ in canonical)
            overlap_terms = " + ".join(
                f"(unit_{position} IN ({placeholders}))"
                for position in range(1, TEAM_SIZE + 1)
            )
            active_placeholders = ",".join("?" for _ in active_overlaps)
            rows = cursor.execute(
                f"""
                WITH outcomes AS ({outcome_union}),
                defense_overlap AS (
                    SELECT team_id, ({overlap_terms}) AS overlap
                    FROM {TEAM_TABLE}
                ),
                aggregates AS (
                    SELECT defense_overlap.overlap, outcomes.attack_team_id,
                           SUM(
                               outcomes.win_0_15 + outcomes.win_15_30 +
                               outcomes.win_30_60 + outcomes.win_60_90
                           ) AS wins,
                           SUM(
                               outcomes.win_0_15 + outcomes.win_15_30 +
                               outcomes.win_30_60 + outcomes.win_60_90 +
                               outcomes.losses + outcomes.timeouts
                           ) AS runs
                    FROM outcomes
                    JOIN defense_overlap
                      ON defense_overlap.team_id = outcomes.defend_team_id
                    WHERE defense_overlap.overlap IN ({active_placeholders})
                    GROUP BY defense_overlap.overlap, outcomes.attack_team_id
                    HAVING wins > 0
                ),
                ranked AS (
                    SELECT overlap, attack_team_id, wins, runs,
                           ROW_NUMBER() OVER (
                               PARTITION BY overlap
                               ORDER BY CAST(wins AS REAL) / runs DESC,
                                        wins DESC, runs DESC, attack_team_id
                           ) AS rank
                    FROM aggregates
                )
                SELECT overlap, attack_team_id
                FROM ranked
                WHERE rank <= CASE overlap
                    WHEN 5 THEN ? WHEN 4 THEN ? WHEN 3 THEN ?
                    WHEN 2 THEN ? WHEN 1 THEN ? ELSE 0 END
                ORDER BY overlap DESC, rank
                """,
                (
                    *(value for _position in range(TEAM_SIZE) for value in canonical),
                    *active_overlaps,
                    *limits,
                ),
            ).fetchall()
            for row in rows:
                result[int(row["overlap"])].append(int(row["attack_team_id"]))

        with self._historical_suggestion_cache_lock:
            if len(self._historical_suggestion_cache) >= HISTORICAL_SUGGESTION_CACHE_SIZE:
                self._historical_suggestion_cache.pop(
                    next(iter(self._historical_suggestion_cache))
                )
            self._historical_suggestion_cache[cache_key] = {
                overlap: tuple(team_ids) for overlap, team_ids in result.items()
            }
        return result

    def _clear_historical_suggestion_cache(self) -> None:
        with self._historical_suggestion_cache_lock:
            self._historical_suggestion_cache.clear()

    def _load_historical_suggestion_candidates(
        self,
        opponent: Sequence[int],
        levels: Sequence[int],
    ) -> tuple[List[tuple[int, ...]], List[tuple[int, ...]]]:
        conn = self._open_connection()
        try:
            cursor = conn.cursor()
            historical_ids = self._historical_attack_ids_by_overlap(
                cursor,
                opponent,
                levels,
            )
            exact_candidates = [
                tuple(self._load_team_units_unlocked(cursor, team_id))
                for team_id in historical_ids[TEAM_SIZE]
            ]
            ranked_candidates = [
                tuple(self._load_team_units_unlocked(cursor, team_id))
                for overlap in range(TEAM_SIZE - 1, 0, -1)
                for team_id in historical_ids[overlap]
            ]
            return exact_candidates, ranked_candidates
        finally:
            conn.close()

    async def pick_attack_suggestions(
        self,
        team: List[int],
        pick_per_levels: Sequence[int] = DEFAULT_PICK_PER_LEVELS,
        include_hot_team: bool = False,
        suggestion_limit: int | None = None,
    ) -> List[List[int]]:
        """Recall tiered history plus model teams, preserving exact-match winners."""
        opponent = self._canonical_team(team)
        levels = tuple(max(0, int(value)) for value in pick_per_levels)
        wanted = max(
            1,
            int(
                DEFAULT_SUGGESTION_LIMIT
                if suggestion_limit is None and levels == DEFAULT_PICK_PER_LEVELS
                else (
                    sum(levels)
                    if suggestion_limit is None
                    else suggestion_limit
                )
            ),
        )
        exact_candidates, ranked_candidates = await asyncio.to_thread(
            self._load_historical_suggestion_candidates,
            opponent,
            levels,
        )
        if include_hot_team:
            ranked_candidates.extend(
                tuple(item.team)
                for item in await self.get_hot_attack_teams(days=7, limit=10)
            )

        critic_ranked = await asyncio.to_thread(
            self._suggest_model_attacks, opponent, ranked_candidates, wanted
        )
        distinct = list(
            dict.fromkeys(
                candidate
                for candidate in [*exact_candidates, *critic_ranked]
                if len(candidate) == TEAM_SIZE
            )
        )
        return [list(candidate) for candidate in distinct[:wanted]]

    def _suggest_model_attacks(
        self,
        opponent: tuple[int, ...],
        candidates: Sequence[tuple[int, ...]],
        wanted: int,
    ) -> List[tuple[int, ...]]:
        with self._model_inference_lock:
            if self.model_manager.load_if_available():
                return self.model_manager.suggest(opponent, candidates, wanted=wanted)
            return list(candidates)

    @timed_suggestion("suggest", "recall_total")
    async def _recall_recommendation_candidates(
        self,
        defend: Sequence[int],
    ) -> List[List[int]]:
        """Build suggestions from exact-defense history and generated candidates."""
        opponent = self._canonical_team(defend)
        defense_key = ",".join(map(str, opponent))
        started = time.perf_counter()
        exact, _ = await asyncio.to_thread(
            self._load_historical_suggestion_candidates,
            opponent,
            SUGGESTION_HISTORY_PICK_PER_LEVELS,
        )
        log_stage("history", started, defense=defense_key, exact_count=len(exact))
        started = time.perf_counter()
        hot = await self.get_hot_attack_teams(days=7, limit=SUGGESTION_HOT_TEAM_LIMIT)
        log_stage("hot_teams", started, defense=defense_key, count=len(hot))
        return await asyncio.to_thread(self._recall_and_rank, opponent, exact, hot)

    def _recall_and_rank(
        self,
        opponent: tuple[int, ...],
        exact: Sequence[tuple[int, ...]],
        hot: Sequence[JJCHotTeam],
    ) -> List[List[int]]:
        # Keep CPU inference off the Bot event loop. A thread lock also protects
        # loading/generation when requests overlap or an awaiting task is cancelled.
        with self._model_inference_lock:
            defense_key = ",".join(map(str, opponent))
            exact_set = set(exact)
            non_exact = [tuple(item.team) for item in hot]
            started = time.perf_counter()
            model_loaded = self.model_manager.load_if_available()
            if model_loaded and not self.model_manager.supports_team(opponent):
                model_loaded = False
            log_stage("model_load", started, defense=defense_key, available=int(model_loaded))
            if model_loaded:
                started = time.perf_counter()
                generated = self.model_manager.recall(
                    opponent,
                    "fast_attack",
                    candidate_count=SUGGESTION_TRANSFORMER_RECALL,
                    generation_batch_size=64,
                )
                log_stage("model_recall", started, defense=defense_key, count=len(generated))
                non_exact.extend(tuple(team) for team in generated)
            else:
                non_exact = []

            started = time.perf_counter()
            normalized_non_exact: List[tuple[int, ...]] = []
            for team in non_exact:
                try:
                    candidate = self._canonical_team(team)
                except (TypeError, ValueError):
                    continue
                if candidate not in exact_set and self.model_manager.supports_team(candidate):
                    normalized_non_exact.append(candidate)
            distinct = list(dict.fromkeys(normalized_non_exact))
            log_stage("candidate_normalize", started, defense=defense_key, count=len(distinct))
            if distinct and model_loaded:
                started = time.perf_counter()
                _probabilities, scores = self.model_manager.rank(
                    distinct,
                    opponent,
                    "fast_attack",
                )
                order = np.argsort(-np.asarray(scores)).tolist()
                distinct = [distinct[index] for index in order]
                log_stage("critic_rank", started, defense=defense_key, count=len(distinct))

            started = time.perf_counter()
            candidates = list(
                dict.fromkeys([*exact, *distinct[:SUGGESTION_CRITIC_LIMIT]])
            )[:DEFAULT_SUGGESTION_LIMIT]
            log_stage("candidate_pool", started, defense=defense_key, count=len(candidates))
            return [list(team) for team in candidates]

    def _load_suggestion_cache(self, defend: Sequence[int]) -> List[JJCRecord]:
        cursor = self.conn.cursor()
        defend_id = self._find_team_id_unlocked(cursor, defend)
        if defend_id is None:
            return []
        rows = cursor.execute(
            f"SELECT record_json FROM {SUGGESTION_CACHE_TABLE} "
            "WHERE defend_team_id=?",
            (defend_id,),
        ).fetchall()
        records: List[JJCRecord] = []
        for row in rows:
            try:
                records.append(record_from_payload(json.loads(str(row[0]))))
            except (TypeError, ValueError, KeyError, json.JSONDecodeError):
                logging.exception("Ignoring malformed JJC suggestion cache row")
        records.sort(key=recommendation_rank_key)
        return records

    def _store_suggestion_cache(self, records: Sequence[JJCRecord]) -> None:
        if not records:
            return
        with self._immediate_transaction():
            cursor = self.conn.cursor()
            now = time.time()
            for record in records:
                attack_id, _ = self._ensure_team_unlocked(cursor, record.attacks)
                defend_id, _ = self._ensure_team_unlocked(cursor, record.defends)
                self.conn.execute(
                    f"""
                    INSERT INTO {SUGGESTION_CACHE_TABLE}(
                        defend_team_id, attack_team_id, record_json, cached_at
                    ) VALUES (?, ?, ?, ?)
                    ON CONFLICT(defend_team_id, attack_team_id) DO UPDATE SET
                        record_json=excluded.record_json,
                        cached_at=excluded.cached_at
                    """,
                    (
                        defend_id,
                        attack_id,
                        json.dumps(record_to_payload(record), ensure_ascii=False),
                        now,
                    ),
                )

    async def clear_suggestion_cache(
        self,
        defend: Sequence[int] | None = None,
    ) -> int:
        """Clear all cached suggestions, or only the normalized defense requested."""
        async with self._lock:
            if defend is None:
                with self._immediate_transaction():
                    cursor = self.conn.execute(f"DELETE FROM {SUGGESTION_CACHE_TABLE}")
                return max(0, int(cursor.rowcount))
            cursor = self.conn.cursor()
            defend_id = self._find_team_id_unlocked(cursor, defend)
            if defend_id is None:
                return 0
            with self._immediate_transaction():
                deleted = self.conn.execute(
                    f"DELETE FROM {SUGGESTION_CACHE_TABLE} WHERE defend_team_id=?",
                    (defend_id,),
                )
            return max(0, int(deleted.rowcount))

    @timed_suggestion("suggest", "recommendation_total")
    async def get_attack_recommendations(
        self,
        defend: Sequence[int],
    ) -> List[JJCRecord]:
        """Return cached qualified attacks or run the shared recall/simulation flow."""
        opponent = self._canonical_team(defend)
        defense_key = ",".join(map(str, opponent))
        started = time.perf_counter()
        cached = self._load_suggestion_cache(opponent)
        log_stage("cache_read", started, defense=defense_key, count=len(cached),
                  ready=int(len(cached) >= SUGGESTION_CACHE_READY_COUNT))
        if len(cached) >= SUGGESTION_CACHE_READY_COUNT:
            return cached

        lock = self._suggestion_build_locks.setdefault(opponent, asyncio.Lock())
        started = time.perf_counter()
        async with lock:
            log_stage("build_lock_wait", started, defense=defense_key)
            started = time.perf_counter()
            cached = self._load_suggestion_cache(opponent)
            log_stage("cache_recheck", started, defense=defense_key, count=len(cached),
                      ready=int(len(cached) >= SUGGESTION_CACHE_READY_COUNT))
            if len(cached) >= SUGGESTION_CACHE_READY_COUNT:
                return cached
            candidates = await self._recall_recommendation_candidates(opponent)
            if not candidates:
                return cached
            started = time.perf_counter()
            trace_token = simulation_trace_id.set(current_trace_id())
            records: List[JJCRecord] | None = None
            try:
                records = await self.simulate_battle_batch_single_enemy(
                    candidates,
                    list(opponent),
                    to_max_unit_attr=True,
                    repeat_count=SUGGESTION_REPEAT_COUNT,
                    use_cache=False,
                )
            finally:
                simulation_trace_id.reset(trace_token)
                log_stage("simulate", started, defense=defense_key,
                          candidates=len(candidates), repeats=SUGGESTION_REPEAT_COUNT,
                          returned=len(records) if records is not None else 0,
                          status="ok" if records is not None else "error")
            started = time.perf_counter()
            qualified: List[JJCRecord] = []
            for record in records:
                record.results = [
                    result
                    for result in record.results
                    if result.result != eJJCStatus.UNKNOWN
                ]
                wins = sum(
                    result.result == eJJCStatus.WIN for result in record.results
                )
                if wins >= SUGGESTION_MIN_WINS:
                    qualified.append(record)
            log_stage("qualify", started, defense=defense_key, count=len(qualified))
            started = time.perf_counter()
            async with self._lock:
                self._store_suggestion_cache(qualified)
            log_stage("cache_write", started, defense=defense_key, count=len(qualified))
            started = time.perf_counter()
            result = self._load_suggestion_cache(opponent)
            log_stage("cache_final_read", started, defense=defense_key, count=len(result))
            return result

    @timed_suggestion("pjjc_suggest", "pjjc_total")
    async def get_pjjc_recommendations(
        self,
        defends: Sequence[Sequence[int]],
        *,
        defend_mode: bool = False,
        limit: int | None = 10,
    ) -> List[List[JJCRecord]]:
        """Combine cached per-defense results without caching final PJJC groups."""
        started = time.perf_counter()
        records = await asyncio.gather(
            *(self.get_attack_recommendations(defend) for defend in defends)
        )
        log_stage("pjjc_defenses", started, teams=len(defends),
                  counts=",".join(str(len(group)) for group in records))
        started = time.perf_counter()
        groups = combine_pjjc_attack(
            [group[:DEFAULT_SUGGESTION_LIMIT] for group in records],
            defend=defend_mode,
        )
        log_stage("pjjc_combine", started, groups=len(groups))
        if not defend_mode:
            started = time.perf_counter()
            groups.sort(key=recommendation_group_rank_key)
            log_stage("pjjc_rank", started, groups=len(groups))
        started = time.perf_counter()
        selected = groups if limit is None else groups[: max(0, int(limit))]
        log_stage("pjjc_limit", started, returned=len(selected))
        return selected

    @staticmethod
    def _calc_at_least_k_win_prob(probs: List[float], need_wins: int) -> float:
        count = len(probs)
        if count <= 0:
            return 0.0
        needed = max(0, min(int(need_wins), count))
        distribution = [0.0] * (count + 1)
        distribution[0] = 1.0
        for probability in probs:
            probability = max(0.0, min(1.0, float(probability)))
            updated = [0.0] * (count + 1)
            for wins in range(count):
                updated[wins] += distribution[wins] * (1.0 - probability)
                updated[wins + 1] += distribution[wins] * probability
            distribution = updated
        return sum(distribution[needed:])

    async def _ensure_record_valid(self, records: List[JJCRecord]) -> List[JJCRecord]:
        valid = [record for record in records if record and not record.is_cache_expired()]
        valid_ids = {id(record) for record in valid}
        expired = [record for record in records if id(record) not in valid_ids]
        if valid:
            await asyncio.gather(
                *[
                    self.simulate_battle_multiple(
                        record.attacks,
                        record.defends,
                        repeat_count=2,
                        use_cache=True,
                    )
                    for record in valid
                ],
                return_exceptions=True,
            )
        if expired:
            await asyncio.gather(
                *[
                    self.simulate_battle_multiple(
                        record.attacks,
                        record.defends,
                        repeat_count=10,
                        use_cache=False,
                    )
                    for record in expired
                ],
                return_exceptions=True,
            )
        return [await self.get_record(record.attacks, record.defends) for record in records]

    async def pick_confidence_attack_team(
        self,
        defend: List[int],
        pick_per_levels: List[int] = [18, 10, 5, 4, 4],
        keep_rate_threshold: int = 80,
        limit: int = 20,
    ) -> List[List[int]]:
        suggestions = await self.pick_attack_suggestions(defend, pick_per_levels)
        records = [await self.get_record(attack, defend) for attack in suggestions]
        records = await self._ensure_record_valid(records)
        records = [record for record in records if record.win_rate * 100 >= keep_rate_threshold]
        records.sort(key=lambda record: record.sort_key)
        return [record.attacks for record in records[:limit]]

    async def build_jjc_matrix(
        self,
        attacks: List[List[int]],
        defends: List[List[int]],
    ) -> JJCMatrixResult:
        records = [
            await self.get_record(attack, defend)
            for attack in attacks
            for defend in defends
        ]
        records = await self._ensure_record_valid(records)
        mapped = {
            (self._to_team_key(record.attacks), self._to_team_key(record.defends)): record
            for record in records
        }
        return await self.build_jjc_matrix_result(attacks, defends, mapped)

    async def build_jjc_matrix_result(
        self,
        attacks: List[List[int]],
        defends: List[List[int]],
        results: Dict[JJCBlindPairKey, JJCRecord],
    ) -> JJCMatrixResult:
        unit_info = {
            unit.unitId: unit
            for record in results.values()
            for result in record.results[-1:]
            for team in (result.player_info or [], result.enemy_info or [])
            for unit in team
        }
        attacks.sort(
            key=lambda attack: sum(
                results[key].win_rate
                for defend in defends
                for key in [(self._to_team_key(attack), self._to_team_key(defend))]
                if key in results
            ),
            reverse=True,
        )
        from ..db.database import db

        header = next(
            (
                record.results[-1]
                for record in results.values()
                if record.results
            ),
            JJCResult(),
        )
        return JJCMatrixResult(
            attacks=[
                [unit_info.get(int(uid), UnitDTO(unitId=uid)) for uid in db.deck_sort_unit(attack)]
                for attack in attacks
            ],
            defends=[
                [unit_info.get(int(uid), UnitDTO(unitId=uid)) for uid in db.deck_sort_unit(defend)]
                for defend in defends
            ],
            matrix=[
                [
                    results[key].win_rate if key in results else -1.0
                    for defend in defends
                    for key in [(self._to_team_key(attack), self._to_team_key(defend))]
                ]
                for attack in attacks
            ],
            header_result=header,
            raw_result=results,
        )

    async def build_pjjc_matrix(
        self,
        attacks: List[List[int]],
        defends: List[List[int]],
    ) -> PJJCMatrixResult:
        result = await self.build_jjc_matrix(attacks, defends)
        group_size = min(3, len(defends))
        if group_size <= 0:
            return PJJCMatrixResult()
        needed = group_size // 2 + 1
        team_sets = [set(int(unit) for unit in team) for team in attacks]
        defend_scenarios = [
            permutation
            for defend_combo in combinations(range(len(defends)), group_size)
            for permutation in permutations(defend_combo)
        ]
        attack_scenarios = [
            combo
            for combo in combinations(range(len(attacks)), group_size)
            if len(set().union(*(team_sets[index] for index in combo)))
            == sum(len(team_sets[index]) for index in combo)
        ]

        def score(combo: tuple[int, ...]) -> float:
            return sum(
                self._calc_at_least_k_win_prob(
                    [result.matrix[combo[row]][defend] for row, defend in enumerate(scenario)],
                    needed,
                )
                for scenario in defend_scenarios
            ) / len(defend_scenarios)

        scored = sorted(((score(combo), combo) for combo in attack_scenarios), reverse=True)
        return PJJCMatrixResult(
            attacks=[[result.attacks[index] for index in combo] for _score, combo in scored],
            defends=result.defends,
            matrix=[
                [[result.matrix[attack][defend] for defend in range(len(defends))] for attack in combo]
                for _score, combo in scored
            ],
            win_rate=[value for value, _combo in scored],
            header_result=result.header_result,
            raw_result=result.raw_result,
        )

    async def _get_hot_teams(
        self,
        column: str,
        days: int,
        limit: int,
    ) -> List[JJCHotTeam]:
        if column not in {"attack_team_id", "defend_team_id"}:
            raise ValueError("invalid hot-team column")
        since = time.time() - max(1, int(days)) * 86400
        union = " UNION ALL ".join(
            f"""
            SELECT {column} AS team_id,
                   win_0_15+win_15_30+win_30_60+win_60_90+losses+timeouts AS runs
            FROM {table} WHERE last_battle_ts>=?
            """
            for table in RESULT_TABLES
        )
        conn = self._open_connection()
        try:
            cursor = conn.cursor()
            rows = cursor.execute(
                f"""
                SELECT team_id, SUM(runs) AS run_count
                FROM ({union}) GROUP BY team_id
                ORDER BY run_count DESC LIMIT ?
                """,
                (*([since] * len(RESULT_TABLES)), max(1, int(limit))),
            ).fetchall()
            return [
                JJCHotTeam(self._load_team_units_unlocked(cursor, int(row[0])), int(row[1]))
                for row in rows
            ]
        finally:
            conn.close()

    async def get_hot_attack_teams(self, days: int = 7, limit: int = 20) -> List[JJCHotTeam]:
        return await self._get_hot_teams("attack_team_id", days, limit)

    async def get_hot_defend_teams(self, days: int = 7, limit: int = 20) -> List[JJCHotTeam]:
        return await self._get_hot_teams("defend_team_id", days, limit)

    async def simulate_battle_batch_single_enemy(
        self,
        player_ids_list: List[List[int]],
        enemy_ids: List[int],
        to_max_unit_attr: bool = True,
        repeat_count: int = 10,
        use_cache: bool = False,
    ) -> List[JJCRecord]:
        return await asyncio.gather(
            *[
                self.simulate_battle_multiple(
                    player_ids,
                    enemy_ids,
                    to_max_unit_attr,
                    use_cache,
                    repeat_count,
                )
                for player_ids in player_ids_list
            ]
        )

    async def simulate_battle_multiple(
        self,
        player_ids: List[int],
        enemy_ids: List[int],
        to_max_unit_attr: bool = True,
        use_cache: bool = False,
        repeat_count: int = 10,
    ) -> JJCRecord:
        results = await self.simulate_battle(
            player_ids,
            enemy_ids,
            to_max_unit_attr,
            repeat_count,
            use_cache,
        )
        return JJCRecord(
            player_ids,
            enemy_ids,
            [result for result in results if not isinstance(result, BaseException)],
        )

    async def simulate_battle_batch(
        self,
        player_ids_list: List[List[int]],
        enemy_ids_list: List[List[int]],
        to_max_unit_attr: bool = True,
        repeat_count: int = 10,
        use_cache: bool = False,
    ) -> List[Union[List[JJCResult], BaseException]]:
        return await asyncio.gather(
            *[
                self.simulate_battle(
                    player_ids,
                    enemy_ids,
                    to_max_unit_attr,
                    repeat_count,
                    use_cache,
                )
                for player_ids, enemy_ids in zip(player_ids_list, enemy_ids_list)
            ],
            return_exceptions=True,
        )

    async def simulate_battle(
        self,
        player_ids: List[int],
        enemy_ids: List[int],
        to_max_unit_attr: bool = True,
        repeat_count: int = 10,
        use_cache: bool = False,
        persist_result: bool = True,
    ) -> List[JJCResult]:
        player_ids = list(self._canonical_team(player_ids))
        enemy_ids = list(self._canonical_team(enemy_ids))
        results: List[JJCResult] = []
        if use_cache:
            cached = await self.get_record(player_ids, enemy_ids)
            if cached and not cached.is_cache_expired():
                results.extend(cached.results[-repeat_count:])
        remaining = int(repeat_count) - len(results)
        if remaining <= 0:
            return results
        raw = await mzq_server.simulate_battle(
            player_ids=player_ids,
            enemy_ids=enemy_ids,
            guild_enemy_units=[],
            ub_exec_times=[],
            seman_ub_exec_times=[],
            to_max_unit_attr=to_max_unit_attr,
            is_auto_mode=True,
            is_set_mode=False,
            is_seman_mode=False,
            is_guild_battle=False,
            repeat_count=remaining,
            **progression_kwargs(),
        )
        if not raw.Success:
            raise RuntimeError(raw.Message or "战斗模拟失败")
        if remaining == 1:
            raw_rows = [(raw.Result, raw.BattleFrames, raw.CurrentSeed)]
        else:
            raw_rows = zip(raw.ResultList, raw.BattleFramesList, raw.CurrentSeedList)
        now = time.time()
        fresh = [
            JJCResult(
                duration=float(frames) / 60.0,
                result=eJJCStatus(int(status)),
                seed=int(seed),
                timestamp=now,
                player_info=raw.PlayerList,
                enemy_info=raw.EnemyList,
                talent_level=raw.TalentLevel,
                talent_skill=raw.TalentSkill,
                team_skill=raw.TeamSkill,
            )
            for status, frames, seed in raw_rows
        ]
        results.extend(fresh)
        if persist_result and fresh:
            await self.save_record(JJCRecord(player_ids, enemy_ids, fresh))
        return results

    def configure_simulator(
        self,
        simulator_url: str,
        *,
        batch_size: int | None = None,
        timeout: int | None = None,
    ) -> str:
        """Configure the shared MZQ transport behind the manager boundary."""
        endpoint = str(simulator_url).rstrip("/")
        if not endpoint.endswith("/simulate"):
            endpoint += "/simulate"
        mzq_server.url = endpoint[: -len("/simulate")]
        mzq_server.simulate_url = endpoint
        if batch_size is not None:
            mzq_server.batch_size = max(1, int(batch_size))
        if timeout is not None:
            mzq_server.request_timeout = max(1, int(timeout))
        return endpoint

    async def close_simulator(self) -> None:
        await mzq_server.close()

    def model_state(self) -> ModelState:
        row = self.conn.execute("SELECT * FROM jjc_state WHERE singleton=1").fetchone()
        if row is None:
            raise RuntimeError("JJC state row is missing")
        return ModelState(
            active_buffer=str(row["active_buffer"]),
            transformer_checkpoint=row["transformer_checkpoint"],
            critic_checkpoint=row["critic_checkpoint"],
        )

    def table_summary(self) -> Dict[str, Dict[str, int]]:
        summary: Dict[str, Dict[str, int]] = {}
        for name, table in (
            ("a", MAIN_RESULT_TABLE),
            ("b", BUFFER_RESULT_TABLES["b"]),
            ("c", BUFFER_RESULT_TABLES["c"]),
        ):
            row = self.conn.execute(
                f"""
                SELECT COUNT(*), COALESCE(SUM(
                    win_0_15+win_15_30+win_30_60+win_60_90+losses+timeouts
                ), 0) FROM {table}
                """
            ).fetchone()
            summary[name] = {"rows": int(row[0]), "runs": int(row[1])}
        return summary

    def status(self) -> Dict[str, Any]:
        return {
            **vars(self.model_state()),
            "tables": self.table_summary(),
            "database": self.db_path,
        }


instance = JJCRecordManager()
