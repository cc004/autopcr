from typing import Dict, List

from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.requests import (
    LabyrinthTopRequest, LabyrinthEnterRequest,
    LabyrinthRetireRequest, LabyrinthResumeRequest,
)
from ...model.enums import eLabyrinthBlockType, eInventoryType
from ...db.database import db
from ...db.models import (
    LabyrinthQuestDatum, LabyrinthWaveGroupDatum,
    LabyrinthEnemyParameter,
)

# Cache: quest_id -> main boss unit_id (highest HP enemy in the wave)
_boss_unit_cache: Dict[int, int] = {}
# Cache: unit_id -> boss display name
_boss_name_cache: Dict[int, str] = {}


def _get_session():
    return db.dbmgr.session()


def _get_boss_unit_id(quest_id: int) -> int:
    """Get the main boss unit_id (highest HP enemy) for a given boss quest_id."""
    if quest_id in _boss_unit_cache:
        return _boss_unit_cache[quest_id]

    session = _get_session()
    try:
        quest = session.query(LabyrinthQuestDatum).filter(
            LabyrinthQuestDatum.quest_id == quest_id
        ).first()
        if not quest:
            _boss_unit_cache[quest_id] = 0
            return 0

        wave = session.query(LabyrinthWaveGroupDatum).filter(
            LabyrinthWaveGroupDatum.wave_group_id == quest.wave_group_id
        ).first()
        if not wave:
            _boss_unit_cache[quest_id] = 0
            return 0

        enemy_ids = [
            wave.enemy_id_1, wave.enemy_id_2, wave.enemy_id_3,
            wave.enemy_id_4, wave.enemy_id_5
        ]
        best_unit_id = 0
        best_hp = 0
        for eid in enemy_ids:
            if not eid:
                continue
            ep = session.query(LabyrinthEnemyParameter).filter(
                LabyrinthEnemyParameter.enemy_id == eid
            ).first()
            if ep and ep.hp > best_hp:
                best_hp = ep.hp
                best_unit_id = ep.unit_id

        _boss_unit_cache[quest_id] = best_unit_id
    finally:
        session.close()
    return _boss_unit_cache[quest_id]


def _get_boss_display_name(unit_id: int) -> str:
    """Get display name for a boss unit_id."""
    if not unit_id:
        return "未知"
    if unit_id in _boss_name_cache:
        return _boss_name_cache[unit_id]

    session = _get_session()
    try:
        ep = session.query(LabyrinthEnemyParameter).filter(
            LabyrinthEnemyParameter.unit_id == unit_id
        ).first()
        if ep:
            _boss_name_cache[unit_id] = ep.name
        else:
            _boss_name_cache[unit_id] = f"unit_{unit_id}"
    finally:
        session.close()
    return _boss_name_cache[unit_id]


# --- Static data: guilds and bosses ---

_GUILD_LIST: List[Tuple[int, str]] = []  # loaded lazily from DB


def _load_guild_list() -> List[Tuple[int, str]]:
    global _GUILD_LIST
    if not _GUILD_LIST:
        session = _get_session()
        try:
            from ...db.models import LabyrinthEnterGuild
            guilds = session.query(LabyrinthEnterGuild).all()
            _GUILD_LIST = [(g.guild_id, g.guild_name.replace('\\n', ' ')) for g in guilds]
        finally:
            session.close()
    return _GUILD_LIST


# Area 3: 77033 series bosses (1=厄勒克特拉夫人, 2=冰霜魔狼, 3=暗黑滴水嘴兽, 4=巨型魔像, 5=毒液沙罗曼蛇)
_AREA3_BOSS_DATA: List[Tuple[int, str, str]] = [
    (312505, "厄勒克特拉夫人", "简单"),
    (319604, "冰霜魔狼", "简单"),
    (303306, "暗黑滴水嘴兽", "普通"),
    (301206, "巨型魔像", "普通"),
    (306604, "毒液沙罗曼蛇", "困难"),
]
_AREA3_UNIT_IDS = [uid for uid, _, _ in _AREA3_BOSS_DATA]

# Area 5: 77053 series bosses (1=愤怒巨龙, 2=炸脖龙, 3=究极守护者, 4=领主哥布林, 5=奇美拉)
_AREA5_BOSS_DATA: List[Tuple[int, str, str]] = [
    (310103, "愤怒巨龙", "简单"),
    (301701, "炸脖龙", "普通"),
    (319401, "究极守护者", "普通"),
    (315004, "领主哥布林", "困难"),
    (302501, "奇美拉", "困难"),
]
_AREA5_UNIT_IDS = [uid for uid, _, _ in _AREA5_BOSS_DATA]

_BOSS_META: Dict[int, Tuple[str, str]] = {}
for uid, bname, btag in _AREA3_BOSS_DATA + _AREA5_BOSS_DATA:
    _BOSS_META[uid] = (bname, btag)


# --- Config classes ---

class LabyrinthDifficultyConfig(SingleChoiceConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, 1, [1, 2, 3, 4, 5])

    def candidate_display(self, candidate: int) -> str:
        return f"难度{candidate}"


class LabyrinthGuildConfig(SingleChoiceConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, 1, lambda: [gid for gid, _ in _load_guild_list()])

    def candidate_display(self, candidate: int) -> str:
        for gid, gname in _load_guild_list():
            if gid == candidate:
                return gname
        return str(candidate)

    def process_value(self, value):
        """Handle stored formats: int, '3,咲恋救济院', tuple/list, plain string."""
        if isinstance(value, (tuple, list)):
            return int(value[0])
        if isinstance(value, str):
            return int(value.split(',')[0].strip())
        return int(value)

    def validate_value(self, value):
        valid_ids = {gid for gid, _ in _load_guild_list()}
        return value if value in valid_ids else None


class LabyrinthBossMultiConfig(MultiChoiceConfig):
    def __init__(self, key: str, desc: str, area: int):
        self._area = area
        self._ids = _AREA3_UNIT_IDS if area == 3 else _AREA5_UNIT_IDS
        super().__init__(key, desc, [], lambda: list(self._ids), short_display=True)

    def candidate_display(self, candidate: int) -> str:
        meta = _BOSS_META.get(candidate)
        if meta:
            return f"{meta[0]} [{meta[1]}]"
        return str(candidate)

    def candidate_tag(self, candidate: int) -> List[str]:
        meta = _BOSS_META.get(candidate)
        return [meta[1]] if meta else []

    def process_value(self, value):
        """Handle stored formats: [int, int, None], [tuple, ...], single int, None."""
        if not value:
            return []
        if not isinstance(value, list):
            value = [value]
        result = []
        for v in value:
            if v is None:
                continue
            if isinstance(v, (tuple, list)):
                result.append(int(v[0]))
            else:
                result.append(int(v))
        return result

    def validate_value(self, value: List):
        if not value:
            return []
        valid = [v for v in value if v in self._ids]
        return valid if valid else None


# --- Modules ---

def _check_ex_path(map_list, area: int) -> bool:
    """Check if all EX (HARD_QUEST) blocks in an area can be reached via a single path.
    Returns True if OK, False if map needs reroll."""
    area_blocks = [b for b in map_list if b.area == area]
    ex_blocks = [b for b in area_blocks if b.block_type == eLabyrinthBlockType.HARD_QUEST]
    if len(ex_blocks) <= 1:
        return True  # 0 or 1 EX block is trivially OK

    block_map = {b.block_id: b for b in area_blocks}
    ex_ids = [b.block_id for b in ex_blocks]

    # BFS from first EX block to find all reachable blocks
    reachable = set()
    queue = [ex_ids[0]]
    while queue:
        bid = queue.pop(0)
        if bid in reachable:
            continue
        reachable.add(bid)
        block = block_map.get(bid)
        if block and block.next_block_id_list:
            for nid in block.next_block_id_list:
                if nid not in reachable:
                    queue.append(nid)

    # All other EX blocks must be reachable from the first one
    for ex_id in ex_ids[1:]:
        if ex_id not in reachable:
            return False
    return True


def _check_relic_path(map_list, area: int, allowed_types: set) -> bool:
    """Check if the block immediately before the first EX in area 2/5 is of an allowed type.
    Returns True if OK, False if map needs reroll."""
    area_blocks = [b for b in map_list if b.area == area]
    if not area_blocks:
        return True

    block_map = {b.block_id: b for b in area_blocks}

    # Find all EX blocks in this area
    ex_ids = {b.block_id for b in area_blocks if b.block_type == eLabyrinthBlockType.HARD_QUEST}
    if not ex_ids:
        return True

    # Find blocks that point directly to an EX block (predecessors of EX)
    for b in area_blocks:
        if b.next_block_id_list:
            for nid in b.next_block_id_list:
                if nid in ex_ids:
                    # b is the block immediately before an EX
                    if b.block_type not in allowed_types:
                        return False
    return True


@description('''进入黎明界，检查区域3和区域5的 Boss 是否符合设定，
不符合则放弃重试，直到刷出符合设定的开局。
可多选 Boss。开启「刷EX路径」后检查极难战斗是否在一条可达路径上。
「刷遗物」可设置区域2/5第一个EX格前只允许的格子类型。''')
@name("黎明界刷开局")
@LabyrinthBossMultiConfig("labyrinth_reset_boss_area5", "区域5 Boss", area=5)
@LabyrinthBossMultiConfig("labyrinth_reset_boss_area3", "区域3 Boss", area=3)
@singlechoice("labyrinth_reset_relic", "刷遗物", "关闭", ["关闭", "遗物", "事件", "任意"])
@booltype("labyrinth_reset_ex_path", "刷EX路径", False)
@LabyrinthGuildConfig("labyrinth_reset_guild", "公会")
@LabyrinthDifficultyConfig("labyrinth_reset_difficulty", "难度")
class labyrinth_reset(Module):
    async def do_task(self, client: pcrclient):
        difficulty = self.get_config("labyrinth_reset_difficulty")
        guild_id = self.get_config("labyrinth_reset_guild")
        target_bosses_area3: List[int] = self.get_config("labyrinth_reset_boss_area3")
        target_bosses_area5: List[int] = self.get_config("labyrinth_reset_boss_area5")

        if not target_bosses_area3:
            raise AbortError("请至少选择一个区域3 Boss")
        if not target_bosses_area5:
            raise AbortError("请至少选择一个区域5 Boss")

        # Check labyrinth ticket count
        ticket_cnt = client.data.get_inventory((eInventoryType.Item, 99013))
        self._log(f"迷宫通行证: {ticket_cnt} 张")
        if ticket_cnt <= 0:
            raise AbortError("迷宫通行证不足，无法进入黎明界")

        names3 = ', '.join(_get_boss_display_name(uid) for uid in target_bosses_area3)
        names5 = ', '.join(_get_boss_display_name(uid) for uid in target_bosses_area5)

        self._log(f"目标: 难度{difficulty}, 公会{guild_id}")
        self._log(f"  区域3 Boss: {names3}")
        self._log(f"  区域5 Boss: {names5}")

        # Build checker for map conditions
        def _check_map(map_list):
            boss_blocks = [b for b in map_list if b.block_type == eLabyrinthBlockType.BOSS_QUEST]
            area3_boss = [b for b in boss_blocks if b.area == 3]
            area5_boss = [b for b in boss_blocks if b.area == 5]
            if not area3_boss or not area5_boss:
                return False, None, None
            a3_uid = _get_boss_unit_id(area3_boss[0].quest_id)
            a5_uid = _get_boss_unit_id(area5_boss[0].quest_id)
            if a3_uid not in target_bosses_area3 or a5_uid not in target_bosses_area5:
                return False, a3_uid, a5_uid
            if self.get_config("labyrinth_reset_ex_path"):
                for area in set(b.area for b in map_list):
                    ex_cnt = sum(1 for b in map_list if b.area == area and b.block_type == eLabyrinthBlockType.HARD_QUEST)
                    if ex_cnt > 1 and not _check_ex_path(map_list, area):
                        return False, a3_uid, a5_uid
            relic_mode = self.get_config("labyrinth_reset_relic")
            if relic_mode != "关闭":
                allowed_map = {
                    "遗物": {eLabyrinthBlockType.NONE, eLabyrinthBlockType.RELIC},
                    "事件": {eLabyrinthBlockType.NONE, eLabyrinthBlockType.EVENT},
                    "任意": {eLabyrinthBlockType.NONE, eLabyrinthBlockType.RELIC, eLabyrinthBlockType.EVENT},
                }
                allowed = allowed_map[relic_mode]
                for area in (2, 5):
                    if not _check_relic_path(map_list, area, allowed):
                        return False, a3_uid, a5_uid
            return True, a3_uid, a5_uid

        top = await client.request(LabyrinthTopRequest())
        if top.enter_id:
            # Resume to check if we're at the first block
            resume = await client.request(LabyrinthResumeRequest(enter_id=top.enter_id))
            entry_block = None
            all_ids = {b.block_id for b in resume.map_list}
            nexted = set()
            for b in resume.map_list:
                if b.next_block_id_list:
                    for nid in b.next_block_id_list:
                        nexted.add(nid)
            entry_ids = all_ids - nexted
            entry_block = next((b for b in resume.map_list if b.block_id in entry_ids and b.area == 1), None)

            if entry_block and resume.block_id == entry_block.block_id:
                self._log(f"检测到进行中的黎明界 (enter_id={top.enter_id})，当前在第一格")
                ok, a3, a5 = _check_map(resume.map_list)
                if ok:
                    self._log(f"  当前开局符合条件，无需重刷")
                    self._log(f"  enter_id: {top.enter_id}")
                    self._log(f"  难度: {top.difficulty}")
                    self._log(f"  公会: {top.guild_id}")
                    self._log(f"  区域3 Boss: {_get_boss_display_name(a3)} ✓")
                    self._log(f"  区域5 Boss: {_get_boss_display_name(a5)} ✓")
                    self._table({
                        "结果": "成功（复用已有）",
                        "enter_id": str(top.enter_id),
                        "难度": str(top.difficulty),
                        "公会": str(top.guild_id),
                        "区域3 Boss": _get_boss_display_name(a3),
                        "区域5 Boss": _get_boss_display_name(a5),
                    })
                    return
                else:
                    self._log(f"  当前开局不符合条件，放弃重来...")
                    await client.request(LabyrinthRetireRequest(enter_id=top.enter_id))
            else:
                raise AbortError(
                    f"当前有进行中的黎明界 (enter_id={top.enter_id})，且不在第一格。\n"
                    f"请先通过网页端【放弃黎明界】或游戏内手动放弃后，再使用刷开局功能。"
                )

        max_attempts = 100
        for attempt in range(1, max_attempts + 1):
            self._log(f"--- 第{attempt}次尝试 ---")

            enter_resp = await client.request(LabyrinthEnterRequest(
                guild_id=guild_id,
                difficulty=difficulty
            ))
            enter_id = enter_resp.enter_id
            self._log(f"进入黎明界 enter_id={enter_id}")

            map_ok, a3_uid, a5_uid = _check_map(enter_resp.map_list)
            if map_ok:
                actual3_name = _get_boss_display_name(a3_uid)
                actual5_name = _get_boss_display_name(a5_uid)
                self._log("")
                self._log(f"🎉 在第{attempt}次尝试后刷到符合设定的开局！")
                self._log(f"  enter_id: {enter_id}")
                self._log(f"  难度: {difficulty}")
                self._log(f"  公会: {guild_id}")
                self._log(f"  区域3 Boss: {actual3_name} ✓")
                self._log(f"  区域5 Boss: {actual5_name} ✓")

                self._table({
                    "结果": "成功",
                    "尝试次数": str(attempt),
                    "enter_id": str(enter_id),
                    "难度": str(difficulty),
                    "公会": str(guild_id),
                    "区域3 Boss": actual3_name,
                    "区域5 Boss": actual5_name,
                })
                return

            self._log("  不符合设定，放弃本次探索...")
            await client.request(LabyrinthRetireRequest(enter_id=enter_id))

        raise AbortError(f"已达到最大尝试次数({max_attempts})，仍未刷到符合设定的开局")


@description('放弃当前进行中的黎明界探索，不进行结算。')
@name("放弃黎明界")
@default(True)
class labyrinth_retire(Module):
    async def do_task(self, client: pcrclient):
        top = await client.request(LabyrinthTopRequest())
        if not top.enter_id:
            self._log("当前没有进行中的黎明界，无需放弃")
            return

        self._log(f"检测到进行中的黎明界:")
        self._log(f"  enter_id: {top.enter_id}")
        self._log(f"  公会: {top.guild_id}")
        self._log(f"  难度: {top.difficulty}")

        await client.request(LabyrinthRetireRequest(enter_id=top.enter_id))
        self._log("已放弃本次探索")

        self._table({
            "结果": "已放弃",
            "enter_id": str(top.enter_id),
            "公会": str(top.guild_id),
            "难度": str(top.difficulty),
        })
