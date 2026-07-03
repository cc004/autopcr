from typing import Dict, List

from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.requests import (
    LabyrinthTopRequest, LabyrinthEnterRequest,
    LabyrinthRetireRequest,
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

@description('''进入黎明界，检查区域3和区域5的 Boss 是否符合设定。
不符合则放弃重试，直到刷出符合设定的开局。
可多选 Boss，只要实际 Boss 在勾选列表中即视为匹配。''')
@name("黎明界刷开局")
@LabyrinthBossMultiConfig("labyrinth_reset_boss_area5", "区域5 Boss", area=5)
@LabyrinthBossMultiConfig("labyrinth_reset_boss_area3", "区域3 Boss", area=3)
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

        top = await client.request(LabyrinthTopRequest())
        if top.enter_id:
            raise AbortError(
                f"当前有进行中的黎明界 (enter_id={top.enter_id}, "
                f"公会={top.guild_id}, 难度={top.difficulty})。\n"
                f"请先通过网页端【放弃黎明界】或游戏内手动放弃后，再使用刷开局功能。"
            )

        max_attempts = 50
        for attempt in range(1, max_attempts + 1):
            self._log(f"--- 第{attempt}次尝试 ---")

            enter_resp = await client.request(LabyrinthEnterRequest(
                guild_id=guild_id,
                difficulty=difficulty
            ))
            enter_id = enter_resp.enter_id
            self._log(f"进入黎明界 enter_id={enter_id}")

            boss_blocks = [
                b for b in enter_resp.map_list
                if b.block_type == eLabyrinthBlockType.BOSS_QUEST
            ]

            area3_boss_blocks = [b for b in boss_blocks if b.area == 3]
            area5_boss_blocks = [b for b in boss_blocks if b.area == 5]

            area3_ok = False
            area5_ok = False
            actual3_name = "?"
            actual5_name = "?"

            if area3_boss_blocks:
                for b in area3_boss_blocks:
                    boss_unit_id = _get_boss_unit_id(b.quest_id)
                    actual3_name = _get_boss_display_name(boss_unit_id)
                    if boss_unit_id in target_bosses_area3:
                        self._log(f"  ✓ 区域3 Boss匹配: {actual3_name}")
                        area3_ok = True
                    else:
                        self._log(f"  ✗ 区域3 Boss不匹配: {actual3_name}")
            else:
                self._log("  ! 区域3 未找到Boss格")

            if area5_boss_blocks:
                for b in area5_boss_blocks:
                    boss_unit_id = _get_boss_unit_id(b.quest_id)
                    actual5_name = _get_boss_display_name(boss_unit_id)
                    if boss_unit_id in target_bosses_area5:
                        self._log(f"  ✓ 区域5 Boss匹配: {actual5_name}")
                        area5_ok = True
                    else:
                        self._log(f"  ✗ 区域5 Boss不匹配: {actual5_name}")
            else:
                self._log("  ! 区域5 未找到Boss格")

            if area3_ok and area5_ok:
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
