import asyncio
import json
import threading
import time
import uuid
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from ..util import aiorequests
from ..util.logger import instance as perf_logging, logging
from .models import UnitData as UnitDTO, GuildRandomData as GuildBattleSettingData

class BattleRequestDTO(BaseModel):
    CalcStats: int = 0
    PlayerList: List[UnitDTO]
    EnemyList: List[UnitDTO] = Field(default_factory=list)
    GuildEnemyList: List[int] = Field(default_factory=list)
    UBExecTimeList: List[List[float]] = Field(default_factory=list)
    SemanUBExecTimeList: List[List[int]] = Field(default_factory=list)
    Settings: GuildBattleSettingData = Field(default_factory=GuildBattleSettingData)
    TalentSkillLevels: Optional[dict] = Field(default_factory=dict)
    TalentSkillNodeLevels: Optional[dict] = Field(default_factory=dict)
    MasterSkillNodeLevels: Optional[dict] = Field(default_factory=dict)
    RoleMastery: Dict[int, Dict[str, int]] = Field(default_factory=dict)
    LabyrinthEnhancedNodeIds: List[int] = Field(default_factory=list)
    LabyrinthRelicIds: List[int] = Field(default_factory=list)
    LabyrinthOwnedUnitIds: List[int] = Field(default_factory=list)
    LabyrinthAlphaRupee: int = 0
    LabyrinthQuestId: int = 0
    LabyrinthDifficulty: int = 0
    BattleTime: int = 0
    TalentFullInfo: bool = False
    IsTalentQuest: bool = False
    ToMaxUnitAttr: bool = False
    IsAutoMode: bool = True
    IsSetMode: bool = False
    IsSemanMode: bool = False
    IsGuildBattle: bool = True
    IsSkipping: bool = True
    TimeLineData: Optional[GuildBattleSettingData] = None
    WaveGroupId: int = 0
    SetToggles: List[bool] = Field(default_factory=list)
    NeedOnceResult: bool = False
    RepeatCount: int = 1

class eBattleResult(IntEnum):
    Win = 0
    Lost = 1
    Timeout = 2
    Unknown = 3

class BattleStatsData(BaseModel):
    TotalDamage: int = 0
    TotalMagicBuff: int = 0
    TotalPhysicsBuff: int = 0
    TotalMagicDebuff: int = 0
    TotalPhysicsDebuff: int = 0
    ScorePhysicsExpectation: float = 0.0
    ScoreMagicExpectation: float = 0.0
    PlayerTpGained: List[int] = Field(default_factory=list)
    PlayerNonUbDamageList: List[int] = Field(default_factory=list)
    PlayerDamageList: List[int] = Field(default_factory=list)
    UBToleranceFrames: List[List[int]] = Field(default_factory=list)
    UBTime: List[List[float]] = Field(default_factory=list)

class BattleSimulationResultDTO(BaseModel):
    PlayerList: List[UnitDTO] = Field(default_factory=list)
    EnemyList: List[UnitDTO] = Field(default_factory=list)
    Success: bool = False
    Message: Optional[str] = None

    Stats: Optional[BattleStatsData] = None

    TalentLevel: str = ""
    TalentSkill: str = ""
    TeamSkill: str = ""
    BattleFrames: int = 0
    CurrentSeed: int = 0
    SemanUBNum: Optional[List[int]] = Field(default_factory=list)
    Result: eBattleResult = eBattleResult.Unknown
    ResultList: Optional[List[eBattleResult]] = Field(default_factory=list)
    BattleFramesList: Optional[List[int]] = Field(default_factory=list)
    CurrentSeedList: Optional[List[int]] = Field(default_factory=list)


def _serialize_role_mastery(
    role_mastery: Optional[Dict[int, Tuple[int, int]]],
) -> Dict[int, Dict[str, int]]:
    if not role_mastery:
        return {}

    result: Dict[int, Dict[str, int]] = {}
    for mastery_id, value in role_mastery.items():
        slot_level = 0
        enhance_level = 0

        if isinstance(value, dict):
            slot_level = value.get("Item1", value.get("slotLevel", 0))
            enhance_level = value.get("Item2", value.get("enhanceLevel", 0))
        elif isinstance(value, (list, tuple)):
            if len(value) > 0:
                slot_level = value[0]
            if len(value) > 1:
                enhance_level = value[1]

        result[int(mastery_id)] = {
            "Item1": int(slot_level),
            "Item2": int(enhance_level),
        }

    return result

@dataclass
class _PendingRequest:
    payload: dict
    future: asyncio.Future
    trace_id: Optional[str] = None
    enqueued_at: float = field(default_factory=time.perf_counter)


def _batch_trace_ids(batch: List[_PendingRequest]) -> str:
    return ",".join(dict.fromkeys(item.trace_id for item in batch if item.trace_id)) or "-"


simulation_trace_id: ContextVar[Optional[str]] = ContextVar(
    "mzq_simulation_trace_id", default=None
)


class MzqDebugExchangeStore:
    """Append raw MZQ simulation request/response exchanges to a text file."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._lock = threading.Lock()

    def append(
        self,
        *,
        url: str,
        request_body: str,
        response_status: Optional[int],
        response_body: Optional[str],
        error: Optional[str] = None,
        exchange_id: Optional[str] = None,
        request_items: Optional[List[dict]] = None,
    ) -> None:
        record = {
            "exchange_id": exchange_id or uuid.uuid4().hex,
            "trace_ids": list(
                dict.fromkeys(
                    item["trace_id"]
                    for item in (request_items or [])
                    if item.get("trace_id")
                )
            ),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "url": str(url),
            "request_items": request_items or [],
            "request_body": str(request_body),
            "response_status": (
                int(response_status) if response_status is not None else None
            ),
            "response_body": (
                str(response_body) if response_body is not None else None
            ),
            "error": str(error) if error else None,
        }
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(line)
                stream.write("\n")


class MzqServer:
    url: str = "http://localhost:8080"
    simulate_url: str = f"{url}/simulate"

    def __init__(
        self,
        max_workers: int = 3,
        batch_size: int = 100,
        batch_wait_seconds: float = 0.5,
        request_timeout: int = 100,
        debug_mode: bool = False,
        debug_exchange_store: Optional[MzqDebugExchangeStore] = None,
        compact_result: bool = False,
    ) -> None:
        self.max_workers = max_workers
        self.batch_size = max(batch_size, 1)
        self.batch_wait_seconds = max(batch_wait_seconds, 0.0)
        self.request_timeout = max(request_timeout, 1)
        self.debug_mode = bool(debug_mode)
        self.debug_exchange_store = debug_exchange_store
        self.compact_result = bool(compact_result)
        self._task_queue: Optional[asyncio.Queue] = None
        self._workers: List[asyncio.Task] = []
        self._enqueued_count = 0
        self._resolved_count = 0
        self._failed_count = 0
        self._dispatched_batch_count = 0
        self._dispatched_request_count = 0
        self._inflight_request_count = 0
        self._last_batch_size = 0
        self._last_batch_cost_ms = 0.0
        self._last_batch_avg_wait_ms = 0.0

    def get_runtime_metrics(self) -> Dict[str, Any]:
        queue_size = self._task_queue.qsize() if self._task_queue else 0
        alive_workers = sum(1 for w in self._workers if not w.done())
        try:
            loop_tasks = len(asyncio.all_tasks())
        except RuntimeError:
            loop_tasks = -1
        return {
            "queue_size": queue_size,
            "alive_workers": alive_workers,
            "max_workers": self.max_workers,
            "enqueued": self._enqueued_count,
            "resolved": self._resolved_count,
            "failed": self._failed_count,
            "dispatched_batches": self._dispatched_batch_count,
            "dispatched_requests": self._dispatched_request_count,
            "inflight": self._inflight_request_count,
            "last_batch_size": self._last_batch_size,
            "last_batch_cost_ms": self._last_batch_cost_ms,
            "last_batch_avg_wait_ms": self._last_batch_avg_wait_ms,
            "loop_tasks": loop_tasks,
        }

    def _ensure_workers(self) -> None:
        loop = asyncio.get_running_loop()
        if self._task_queue is None:
            self._task_queue = asyncio.Queue()

        # Drop finished workers so we can respawn if needed.
        alive_workers: List[asyncio.Task] = []
        for worker in self._workers:
            if not worker.done():
                alive_workers.append(worker)
        self._workers = alive_workers

        missing = self.max_workers - len(self._workers)
        for _ in range(max(0, missing)):
            self._workers.append(loop.create_task(self._batch_worker_loop()))

    async def close(self) -> None:
        """Cancel idle batch workers and release this instance's event-loop state."""
        workers = list(self._workers)
        for worker in workers:
            worker.cancel()
        if workers:
            await asyncio.gather(*workers, return_exceptions=True)

        if self._task_queue is not None:
            while True:
                try:
                    pending = self._task_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                if not pending.future.done():
                    pending.future.cancel()
                self._task_queue.task_done()
        self._workers = []
        self._task_queue = None

    async def _save_debug_exchange(
        self,
        *,
        request_body: str,
        response_status: Optional[int],
        response_body: Optional[str],
        error: Optional[str] = None,
        exchange_id: Optional[str] = None,
        request_items: Optional[List[dict]] = None,
    ) -> None:
        if not self.debug_mode or self.debug_exchange_store is None:
            return
        try:
            await asyncio.to_thread(
                self.debug_exchange_store.append,
                url=self.simulate_url,
                request_body=request_body,
                response_status=response_status,
                response_body=response_body,
                error=error,
                exchange_id=exchange_id,
                request_items=request_items,
            )
        except Exception:
            logging.error("保存 MZQ debug 请求/响应失败", exc_info=True)

    async def _enqueue_request(self, payload: dict) -> BattleSimulationResultDTO:
        self._ensure_workers()
        assert self._task_queue is not None

        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        await self._task_queue.put(
            _PendingRequest(
                payload=payload,
                future=future,
                trace_id=simulation_trace_id.get(),
            )
        )
        self._enqueued_count += 1
        try:
            return await future
        except Exception as exc:
            payload_json = json.dumps(payload, ensure_ascii=False)
            if len(payload_json) > 2000:
                payload_json = payload_json[:2000] + f"...(truncated, {len(payload_json)} chars)"
            logging.error(f"战斗模拟请求失败: {exc}，请求数据: {payload_json}")
            raise

    async def _batch_worker_loop(self) -> None:
        assert self._task_queue is not None
        while True:
            try:
                first_task = await self._task_queue.get()
                batch = [first_task]
                batch_deadline = time.monotonic() + self.batch_wait_seconds

                while len(batch) < self.batch_size:
                    timeout = batch_deadline - time.monotonic()
                    if timeout <= 0:
                        logging.info(f"Batch wait time exceeded, dispatching batch of {len(batch)} times battle requests")
                        break
                    try:
                        next_task = await asyncio.wait_for(self._task_queue.get(), timeout=timeout)
                        batch.append(next_task)
                    except asyncio.TimeoutError:
                        break

                now = time.perf_counter()
                avg_wait_ms = sum((now - item.enqueued_at) for item in batch) * 1000 / len(batch)
                max_wait_ms = max(now - item.enqueued_at for item in batch) * 1000
                self._last_batch_avg_wait_ms = avg_wait_ms
                queue_size = self._task_queue.qsize() if self._task_queue else 0
                loop_tasks = len(asyncio.all_tasks())
                perf_logging.info(
                    f"[MZQ] batch ready traces={_batch_trace_ids(batch)} size={len(batch)} "
                    f"avg_wait={avg_wait_ms:.1f}ms max_wait={max_wait_ms:.1f}ms "
                    f"queue={queue_size} inflight={self._inflight_request_count} "
                    f"workers={sum(1 for w in self._workers if not w.done())}/{self.max_workers} "
                    f"loop_tasks={loop_tasks}"
                )

                try:
                    await self._dispatch_batch(batch)
                    logging.info(f"Batch of {len(batch)} times battle requests dispatched")
                finally:
                    if self.debug_mode:
                        logging.debug(
                            "Batch worker finished processing batch of %s battle requests",
                            len(batch),
                        )
                    for _ in batch:
                        self._task_queue.task_done()
            except Exception as exc:
                logging.error(f"Batch worker loop error: {exc}", exc_info=True)
                await asyncio.sleep(1)

    async def _dispatch_batch(self, batch: List[_PendingRequest]) -> None:
        if not batch:
            return

        trace_ids = _batch_trace_ids(batch)
        payload = [item.payload for item in batch]
        payload_json = (
            json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            if self.debug_mode else ""
        )
        exchange_id = uuid.uuid4().hex
        request_items = (
            [
                {
                    "trace_id": item.trace_id,
                    "unit_ids": [
                        unit["unitId"]
                        for unit in item.payload.get("PlayerList", [])
                        if isinstance(unit, dict) and "unitId" in unit
                    ],
                }
                for item in batch
            ]
            if self.debug_mode else []
        )
        batch_begin = time.perf_counter()
        self._inflight_request_count += len(batch)
        response_status: Optional[int] = None
        response_text: Optional[str] = None
        exchange_saved = False
        try:
            logging.debug(f"Dispatching batch of {len(batch)} battle requests to /simulate")
            if self.debug_mode:
                logging.info(
                    "[MZQ DEBUG] -> exchange_id=%s %s body=%s",
                    exchange_id,
                    self.simulate_url,
                    payload_json,
                )
            t0 = time.perf_counter()
            response = await aiorequests.post(self.simulate_url, json=payload, timeout=self.request_timeout)
            post_ms = (time.perf_counter() - t0) * 1000
            response_status = response.status_code

            t1 = time.perf_counter()
            response_text = await response.text
            text_ms = (time.perf_counter() - t1) * 1000
            if self.debug_mode:
                logging.info(
                    "[MZQ DEBUG] <- exchange_id=%s %s status=%s body=%s",
                    exchange_id,
                    self.simulate_url,
                    response_status,
                    response_text,
                )
            response.raise_for_status()
            await self._save_debug_exchange(
                request_body=payload_json,
                response_status=response_status,
                response_body=response_text,
                exchange_id=exchange_id,
                request_items=request_items,
            )
            exchange_saved = True
            try:
                t2 = time.perf_counter()
                parsed = json.loads(response_text)
                json_ms = (time.perf_counter() - t2) * 1000
            except json.JSONDecodeError as exc:
                raise ValueError(f"无法解析模拟结果: {exc}") from exc

            if not isinstance(parsed, list):
                raise ValueError("模拟结果格式错误，应当是数组")

            if len(parsed) != len(batch):
                raise ValueError(f"返回结果数量不匹配: {len(parsed)} != {len(batch)}")

            t3 = time.perf_counter()
            ok_count = 0
            fail_count = 0
            for item, pending in zip(parsed, batch):
                try:
                    if self.compact_result:
                        if not isinstance(item, dict):
                            raise ValueError("模拟结果格式错误，应当是对象")
                        compact = {
                            key: item[key]
                            for key in (
                                "Success", "Message", "Result", "BattleFrames",
                                "CurrentSeed", "ResultList", "BattleFramesList",
                                "CurrentSeedList",
                            )
                            if key in item
                        }
                        stats = item.get("Stats")
                        if isinstance(stats, dict) and "TotalDamage" in stats:
                            compact["Stats"] = {"TotalDamage": stats["TotalDamage"]}
                        result = BattleSimulationResultDTO.parse_obj(compact)
                    else:
                        result = BattleSimulationResultDTO.parse_obj(item)
                    if not pending.future.done():
                        pending.future.set_result(result)
                    ok_count += 1
                except Exception as exc:
                    if not pending.future.done():
                        pending.future.set_exception(exc)
                    fail_count += 1
            parse_obj_ms = (time.perf_counter() - t3) * 1000
            total_ms = (time.perf_counter() - batch_begin) * 1000
            self._dispatched_batch_count += 1
            self._dispatched_request_count += len(batch)
            self._resolved_count += ok_count
            self._failed_count += fail_count
            self._last_batch_size = len(batch)
            self._last_batch_cost_ms = total_ms
            queue_size = self._task_queue.qsize() if self._task_queue else 0
            loop_tasks = len(asyncio.all_tasks())
            perf_logging.info(
                f"[MZQ] batch done traces={trace_ids} exchange_id={exchange_id} size={len(batch)} "
                f"ok={ok_count} fail={fail_count} "
                f"post={post_ms:.1f}ms body={text_ms:.1f}ms json={json_ms:.1f}ms "
                f"map={parse_obj_ms:.1f}ms total={total_ms:.1f}ms bytes={len(response_text)} "
                f"queue={queue_size} inflight={self._inflight_request_count} loop_tasks={loop_tasks}"
            )
        except Exception as exc:
            if not exchange_saved:
                await self._save_debug_exchange(
                    request_body=payload_json,
                    response_status=response_status,
                    response_body=response_text,
                    error=str(exc),
                    exchange_id=exchange_id,
                    request_items=request_items,
                )
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            if status_code == 413 and len(batch) > 1:
                mid = len(batch) // 2
                left = batch[:mid]
                right = batch[mid:]
                perf_logging.warning(
                    f"[MZQ] batch split traces={trace_ids} exchange_id={exchange_id} "
                    f"/simulate 返回 413，批次过大，"
                    f"自动拆分重试: {len(batch)} -> {len(left)} + {len(right)}"
                )
                await self._dispatch_batch(left)
                await self._dispatch_batch(right)
                return

            failed = 0
            for pending in batch:
                if not pending.future.done():
                    pending.future.set_exception(exc)
                    failed += 1
            self._failed_count += failed
            queue_size = self._task_queue.qsize() if self._task_queue else 0
            perf_logging.error(
                f"[MZQ] batch failed traces={trace_ids} exchange_id={exchange_id} "
                f"size={len(batch)} failed={failed} "
                f"queue={queue_size} inflight={self._inflight_request_count} error={exc}"
            )
        finally:
            self._inflight_request_count = max(0, self._inflight_request_count - len(batch))

    async def _submit_battle(
        self,
        player_units: List[UnitDTO],
        enemy_units: List[UnitDTO],
        guild_enemy_units: List[int],
        ub_exec_times: List[List[float]],
        seman_ub_exec_times: List[List[int]],
        talent_skill_levels: Optional[dict] = None,
        talent_skill_node_levels: Optional[dict] = None,
        master_skill_node_levels: Optional[dict] = None,
        role_mastery: Optional[Dict[int, Tuple[int, int]]] = None,
        talent_full_info: bool = False,
        is_talent_quest: bool = False,
        to_max_unit_attr: bool = False,
        is_auto_mode: bool = True,
        is_set_mode: bool = False,
        is_seman_mode: bool = False,
        is_guild_battle: bool = False,
        battle_time: int = 0,
        settings: GuildBattleSettingData = GuildBattleSettingData(),
        wave_group_id: int = 0,
        repeat_count: int = 1,
        set_toggles: List[bool] = [False, False, False, False, False],
        labyrinth_enhanced_node_ids: Optional[List[int]] = None,
        labyrinth_relic_ids: Optional[List[int]] = None,
        labyrinth_owned_unit_ids: Optional[List[int]] = None,
        labyrinth_alpha_rupee: int = 0,
        labyrinth_quest_id: int = 0,
        labyrinth_difficulty: int = 0,
        is_skipping: bool = True,
        need_once_result: bool = False,
        calc_stats: int = 0,
    ) -> BattleSimulationResultDTO:

        req_dto = BattleRequestDTO(
            CalcStats=calc_stats,
            PlayerList=player_units,
            EnemyList=enemy_units,
            GuildEnemyList=guild_enemy_units,
            UBExecTimeList=ub_exec_times,
            SemanUBExecTimeList=seman_ub_exec_times,
            TalentSkillLevels=talent_skill_levels,
            TalentSkillNodeLevels=talent_skill_node_levels,
            MasterSkillNodeLevels=master_skill_node_levels,
            RoleMastery=_serialize_role_mastery(role_mastery),
            TalentFullInfo=talent_full_info,
            IsTalentQuest=is_talent_quest,
            ToMaxUnitAttr=to_max_unit_attr,
            IsAutoMode=is_auto_mode,
            IsSetMode=is_set_mode,
            IsSemanMode=is_seman_mode,
            IsGuildBattle=is_guild_battle,
            IsSkipping=is_skipping,
            BattleTime=battle_time,
            Settings=settings,
            LabyrinthEnhancedNodeIds=labyrinth_enhanced_node_ids or [],
            LabyrinthRelicIds=labyrinth_relic_ids or [],
            LabyrinthOwnedUnitIds=labyrinth_owned_unit_ids or [],
            LabyrinthAlphaRupee=labyrinth_alpha_rupee,
            LabyrinthQuestId=labyrinth_quest_id,
            LabyrinthDifficulty=labyrinth_difficulty,
            WaveGroupId=wave_group_id,
            SetToggles=set_toggles,
            NeedOnceResult=need_once_result,
            RepeatCount=repeat_count,
        )

        data = req_dto.dict()
        if self.debug_mode:
            logging.debug("Request: %s", data)
        result = await self._enqueue_request(data)
        if self.debug_mode:
            logging.debug("Response: %s", result)
        return result

    async def _simulate_battle(
        self,
        player_units: List[UnitDTO],
        enemy_units: Optional[List[UnitDTO]] = None,
        guild_enemy_units: Optional[List[int]] = None,
        ub_exec_times: Optional[List[List[float]]] = None,
        seman_ub_exec_times: Optional[List[List[int]]] = None,
        talent_skill_levels: Optional[dict] = None,
        talent_skill_node_levels: Optional[dict] = None,
        master_skill_node_levels: Optional[dict] = None,
        role_mastery: Optional[Dict[int, Tuple[int, int]]] = None,
        talent_full_info: bool = False,
        is_talent_quest: bool = False,
        to_max_unit_attr: bool = False,
        is_auto_mode: bool = True,
        is_set_mode: bool = False,
        is_seman_mode: bool = False,
        is_guild_battle: bool = False,
        battle_time: int = 90,
        settings: GuildBattleSettingData = GuildBattleSettingData(),
        wave_group_id: int = 0,
        repeat_count: int = 1,
        set_toggles: List[bool] = [False, False, False, False, False],
        labyrinth_enhanced_node_ids: Optional[List[int]] = None,
        labyrinth_relic_ids: Optional[List[int]] = None,
        labyrinth_owned_unit_ids: Optional[List[int]] = None,
        labyrinth_alpha_rupee: int = 0,
        labyrinth_quest_id: int = 0,
        labyrinth_difficulty: int = 0,
        is_skipping: bool = True,
        need_once_result: bool = False,
        calc_stats: int = 0,
    ) -> BattleSimulationResultDTO:
        if enemy_units is None:
            enemy_units = []
        if guild_enemy_units is None:
            guild_enemy_units = []
        if ub_exec_times is None:
            ub_exec_times = []
        if seman_ub_exec_times is None:
            seman_ub_exec_times = []

        result = await self._submit_battle(
            player_units=player_units,
            enemy_units=enemy_units,
            guild_enemy_units=guild_enemy_units,
            ub_exec_times=ub_exec_times,
            seman_ub_exec_times=seman_ub_exec_times,
            talent_skill_levels=talent_skill_levels,
            talent_skill_node_levels=talent_skill_node_levels,
            master_skill_node_levels=master_skill_node_levels,
            role_mastery=role_mastery,
            talent_full_info=talent_full_info,
            is_talent_quest=is_talent_quest,
            to_max_unit_attr=to_max_unit_attr,
            is_auto_mode=is_auto_mode,
            is_set_mode=is_set_mode,
            is_seman_mode=is_seman_mode,
            is_guild_battle=is_guild_battle,
            battle_time=battle_time,
            settings=settings,
            wave_group_id=wave_group_id,
            repeat_count=repeat_count,
            set_toggles=set_toggles,
            labyrinth_enhanced_node_ids=labyrinth_enhanced_node_ids,
            labyrinth_relic_ids=labyrinth_relic_ids,
            labyrinth_owned_unit_ids=labyrinth_owned_unit_ids,
            labyrinth_alpha_rupee=labyrinth_alpha_rupee,
            labyrinth_quest_id=labyrinth_quest_id,
            labyrinth_difficulty=labyrinth_difficulty,
            is_skipping=is_skipping,
            need_once_result=need_once_result,
            calc_stats=calc_stats,
        )
        return result

    async def simulate_battle(self,
        player_ids: List[int],
        enemy_ids: List[int],
        guild_enemy_units: Optional[List[int]] = None,
        ub_exec_times: Optional[List[List[float]]] = None,
        seman_ub_exec_times: Optional[List[List[int]]] = None,
        talent_skill_levels: Optional[dict] = None,
        talent_skill_node_levels: Optional[dict] = None,
        master_skill_node_levels: Optional[dict] = None,
        role_mastery: Optional[Dict[int, Tuple[int, int]]] = None,
        talent_full_info: bool = False,
        is_talent_quest: bool = False,
        to_max_unit_attr: bool = False,
        is_auto_mode: bool = True,
        is_set_mode: bool = False,
        is_seman_mode: bool = False,
        is_guild_battle: bool = False,
        battle_time: int = 90,
        settings: GuildBattleSettingData = GuildBattleSettingData(),
        repeat_count: int = 1,
        labyrinth_enhanced_node_ids: Optional[List[int]] = None,
        labyrinth_relic_ids: Optional[List[int]] = None,
        labyrinth_owned_unit_ids: Optional[List[int]] = None,
        labyrinth_alpha_rupee: int = 0,
        labyrinth_quest_id: int = 0,
        labyrinth_difficulty: int = 0,
        is_skipping: bool = True,
        need_once_result: bool = False,
        calc_stats: int = 0,
      ) -> BattleSimulationResultDTO:
        if is_guild_battle:
            raise NotImplementedError("Guild battle caching not implemented yet.")
        else:
            from ..db.database import db
            player_ids = db.deck_sort_unit(player_ids)
            enemy_ids = db.deck_sort_unit(enemy_ids)

            player_units = [UnitDTO(unitId=uid) for uid in player_ids]
            enemy_units = [UnitDTO(unitId=uid) for uid in enemy_ids]
            return await self._simulate_battle(
                player_units=player_units,
                enemy_units=enemy_units,
                guild_enemy_units=guild_enemy_units,
                ub_exec_times=ub_exec_times,
                seman_ub_exec_times=seman_ub_exec_times,
                talent_skill_levels=talent_skill_levels,
                talent_skill_node_levels=talent_skill_node_levels,
                master_skill_node_levels=master_skill_node_levels,
                role_mastery=role_mastery,
                talent_full_info=talent_full_info,
                is_talent_quest=is_talent_quest,
                to_max_unit_attr=to_max_unit_attr,
                is_auto_mode=is_auto_mode,
                is_set_mode=is_set_mode,
                is_seman_mode=is_seman_mode,
                is_guild_battle=is_guild_battle,
                battle_time=battle_time,
                settings=settings,
                repeat_count=repeat_count,
                labyrinth_enhanced_node_ids=labyrinth_enhanced_node_ids,
                labyrinth_relic_ids=labyrinth_relic_ids,
                labyrinth_owned_unit_ids=labyrinth_owned_unit_ids,
                labyrinth_alpha_rupee=labyrinth_alpha_rupee,
                labyrinth_quest_id=labyrinth_quest_id,
                labyrinth_difficulty=labyrinth_difficulty,
                is_skipping=is_skipping,
                need_once_result=need_once_result,
                calc_stats=calc_stats,
            )

instance = MzqServer()
