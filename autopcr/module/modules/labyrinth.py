from typing import Dict, List, Set, Tuple

from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.enums import eLabyrinthBlockType, eInventoryType
from ...db.database import db


# --- Boss definitions ---

LABYRINTH_AREA3_BOSSES: List[Tuple[int, str, str]] = [
    (312505, "厄勒克特拉夫人", "简单"),
    (319604, "冰霜魔狼", "简单"),
    (303306, "暗黑滴水嘴兽", "普通"),
    (301206, "巨型魔像", "普通"),
    (306604, "毒液沙罗曼蛇", "困难"),
]

LABYRINTH_AREA5_BOSSES: List[Tuple[int, str, str]] = [
    (310103, "愤怒巨龙", "简单"),
    (301701, "炸脖龙", "普通"),
    (319401, "究极守护者", "普通"),
    (315004, "领主哥布林", "困难"),
    (302501, "奇美拉", "困难"),
]

LABYRINTH_BOSS_NAME_BY_UNIT: Dict[int, str] = {
    unit_id: name
    for unit_id, name, _ in LABYRINTH_AREA3_BOSSES + LABYRINTH_AREA5_BOSSES
}


class LabyrinthBossConfig(MultiChoiceConfig):
    """Multi-select for labyrinth boss, with difficulty shown inline."""

    def __init__(self, key: str, desc: str, boss_list: List[Tuple[int, str, str]]):
        simple_bosses = [unit_id for unit_id, _, difficulty in boss_list if difficulty == "简单"]
        super().__init__(key, desc, simple_bosses, [unit_id for unit_id, _, _ in boss_list])
        self.boss_info = {unit_id: (name, difficulty) for unit_id, name, difficulty in boss_list}

    def candidate_display(self, unit_id: int):
        name, difficulty = self.boss_info.get(unit_id, (str(unit_id), "未知"))
        return f"【{difficulty}】{name}"


def _get_boss_unit_ids(quest_id: int) -> Set[int]:
    """Get all unit_ids for enemies in a boss quest's wave group."""
    quest = db.labyrinth_quest_data.get(quest_id)
    if not quest:
        return set()
    wave = db.labyrinth_wave_group_data.get(quest.wave_group_id)
    if not wave:
        return set()
    return {ep.unit_id for eid in wave.get_enemy_ids() if eid
            and (ep := db.labyrinth_enemy_parameter.get(eid))}


# --- Map check helpers ---

def _check_ex_path(map_list, area: int) -> bool:
    area_blocks = [b for b in map_list if b.area == area]
    ex_blocks = [b for b in area_blocks if b.block_type == eLabyrinthBlockType.HARD_QUEST]
    if len(ex_blocks) <= 1:
        return True

    block_map = {b.block_id: b for b in area_blocks}
    ex_ids = [b.block_id for b in ex_blocks]

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

    for ex_id in ex_ids[1:]:
        if ex_id not in reachable:
            return False
    return True


def _check_relic_path(map_list, area: int, allowed_types: set) -> bool:
    area_blocks = [b for b in map_list if b.area == area]
    if not area_blocks:
        return True

    block_map = {b.block_id: b for b in area_blocks}
    ex_ids = {b.block_id for b in area_blocks if b.block_type == eLabyrinthBlockType.HARD_QUEST}
    if not ex_ids:
        return True

    for b in area_blocks:
        if b.next_block_id_list:
            for nid in b.next_block_id_list:
                if nid in ex_ids and b.block_type not in allowed_types:
                    return False
    return True


def _check_ticket_path(map_list) -> bool:
    area1_blocks = [b for b in map_list if b.area == 1]
    ticket_blocks = [b for b in area1_blocks if b.block_type == eLabyrinthBlockType.TICKET]
    if len(ticket_blocks) < 2:
        return True

    block_map = {b.block_id: b for b in area1_blocks}
    ticket_ids = [b.block_id for b in ticket_blocks]

    reachable = set()
    queue = [ticket_ids[0]]
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

    # All ticket blocks must be on the same path
    for tid in ticket_ids[1:]:
        if tid not in reachable:
            return False

    # At least one EX block must be reachable from the ticket blocks
    ex_blocks = [b for b in area1_blocks if b.block_type == eLabyrinthBlockType.HARD_QUEST]
    if ex_blocks and not any(b.block_id in reachable for b in ex_blocks):
        return False
    return True


class LabyrinthDifficultyConfig(SingleChoiceConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, 1, [1, 2, 3, 4, 5])

    def candidate_display(self, candidate: int) -> str:
        return f"难度{candidate}"


# --- Modules ---

@description('''进入黎明界，检查区域3和区域5的 Boss 是否符合设定，
不符合则放弃重试，直到刷出符合设定的开局。
可多选 Boss。开启「刷EX路径」后检查极难战斗是否在一条可达路径上，
「刷角色」检查区域1两个角色格是否可达，
「刷遗物」设置区域2/5第一个EX格前只允许的格子类型（仅难度≥4生效）。''')
@name("黎明界刷开局")
@LabyrinthBossConfig("labyrinth_reset_boss_area5", "区域5 Boss", LABYRINTH_AREA5_BOSSES)
@LabyrinthBossConfig("labyrinth_reset_boss_area3", "区域3 Boss", LABYRINTH_AREA3_BOSSES)
@singlechoice("labyrinth_reset_relic", "刷遗物", "关闭", ["关闭", "遗物", "事件", "任意"])
@booltype("labyrinth_reset_ticket", "刷角色", False)
@booltype("labyrinth_reset_ex_path", "刷EX路径", False)
@LabyrinthGuildConfig("labyrinth_reset_guild", "公会", 1)
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

        ticket_cnt = client.data.get_inventory((eInventoryType.Item, 99013))
        self._log(f"迷宫通行证: {ticket_cnt} 张")
        if ticket_cnt <= 0:
            raise AbortError("迷宫通行证不足，无法进入黎明界")

        top = await client.labyrinth_top()
        cleared = [info.difficulty for info in (top.guild_cleared_difficulty_list or []) if getattr(info, "difficulty", None)]
        max_unlocked = min(max(cleared) + 1, 5) if cleared else 1
        if difficulty > max_unlocked:
            self._warn(f"黎明界难度{difficulty}尚未解锁，当前最大可挑战难度为{max_unlocked}，跳过执行。")
            raise AbortError("未解锁所选黎明界难度")

        names3 = ', '.join(LABYRINTH_BOSS_NAME_BY_UNIT.get(uid, str(uid)) for uid in target_bosses_area3)
        names5 = ', '.join(LABYRINTH_BOSS_NAME_BY_UNIT.get(uid, str(uid)) for uid in target_bosses_area5)

        self._log(f"目标: 难度{difficulty}, 公会{guild_id}")
        self._log(f"  区域3 Boss: {names3}")
        self._log(f"  区域5 Boss: {names5}")

        def _check_map(map_list):
            boss_blocks = [b for b in map_list if b.block_type == eLabyrinthBlockType.BOSS_QUEST]
            area3_boss = [b for b in boss_blocks if b.area == 3]
            area5_boss = [b for b in boss_blocks if b.area == 5]
            if not area3_boss or not area5_boss:
                return False, None, None
            a3_unit_ids = _get_boss_unit_ids(area3_boss[0].quest_id)
            a5_unit_ids = _get_boss_unit_ids(area5_boss[0].quest_id)
            a3_matched = bool(a3_unit_ids & set(target_bosses_area3))
            a5_matched = bool(a5_unit_ids & set(target_bosses_area5))
            if not a3_matched or not a5_matched:
                return False, a3_unit_ids, a5_unit_ids
            if self.get_config("labyrinth_reset_ex_path"):
                for area in set(b.area for b in map_list):
                    ex_cnt = sum(1 for b in map_list if b.area == area and b.block_type == eLabyrinthBlockType.HARD_QUEST)
                    if ex_cnt > 1 and not _check_ex_path(map_list, area):
                        return False, a3_unit_ids, a5_unit_ids
            if self.get_config("labyrinth_reset_ticket"):
                if not _check_ticket_path(map_list):
                    return False, a3_unit_ids, a5_unit_ids
            relic_mode = self.get_config("labyrinth_reset_relic")
            if relic_mode != "关闭" and difficulty >= 4:
                allowed_map = {
                    "遗物": {eLabyrinthBlockType.NONE, eLabyrinthBlockType.RELIC},
                    "事件": {eLabyrinthBlockType.NONE, eLabyrinthBlockType.EVENT},
                    "任意": {eLabyrinthBlockType.NONE, eLabyrinthBlockType.RELIC, eLabyrinthBlockType.EVENT},
                }
                allowed = allowed_map[relic_mode]
                for area in (2, 5):
                    if not _check_relic_path(map_list, area, allowed):
                        return False, a3_unit_ids, a5_unit_ids
            return True, a3_unit_ids, a5_unit_ids

        if top.enter_id:
            resume = await client.labyrinth_resume(enter_id=top.enter_id)
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
                    matched3 = a3 & set(target_bosses_area3)
                    matched5 = a5 & set(target_bosses_area5)
                    a3_name = ', '.join(LABYRINTH_BOSS_NAME_BY_UNIT.get(uid, str(uid)) for uid in matched3) or "?"
                    a5_name = ', '.join(LABYRINTH_BOSS_NAME_BY_UNIT.get(uid, str(uid)) for uid in matched5) or "?"
                    self._log(f"  区域3 Boss: {a3_name} ✓")
                    self._log(f"  区域5 Boss: {a5_name} ✓")
                    self._table({
                        "结果": "成功（复用已有）",
                        "enter_id": str(top.enter_id),
                        "难度": str(top.difficulty),
                        "公会": str(top.guild_id),
                        "区域3 Boss": a3_name,
                        "区域5 Boss": a5_name,
                    })
                    return
                else:
                    self._log(f"  当前开局不符合条件，放弃重来...")
                    await client.labyrinth_retire(enter_id=top.enter_id)
            else:
                raise AbortError(
                    f"当前有进行中的黎明界 (enter_id={top.enter_id})，且不在第一格。\n"
                    f"请先通过网页端【放弃黎明界】或游戏内手动放弃后，再使用刷开局功能。"
                )

        max_attempts = 100
        for attempt in range(1, max_attempts + 1):
            self._log(f"--- 第{attempt}次尝试 ---")

            enter_resp = await client.labyrinth_enter(guild_id=guild_id, difficulty=difficulty)
            enter_id = enter_resp.enter_id
            self._log(f"进入黎明界 enter_id={enter_id}")

            map_ok, a3_uid, a5_uid = _check_map(enter_resp.map_list)
            if map_ok:
                matched3 = a3_uid & set(target_bosses_area3)
                matched5 = a5_uid & set(target_bosses_area5)
                actual3_name = ', '.join(LABYRINTH_BOSS_NAME_BY_UNIT.get(uid, str(uid)) for uid in matched3) or "?"
                actual5_name = ', '.join(LABYRINTH_BOSS_NAME_BY_UNIT.get(uid, str(uid)) for uid in matched5) or "?"
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
            await client.labyrinth_retire(enter_id=enter_id)

        raise AbortError(f"已达到最大尝试次数({max_attempts})，仍未刷到符合设定的开局")


@description('放弃当前进行中的黎明界探索，不进行结算。')
@name("放弃黎明界")
@default(True)
class labyrinth_retire(Module):
    async def do_task(self, client: pcrclient):
        top = await client.labyrinth_top()
        if not top.enter_id:
            self._log("当前没有进行中的黎明界，无需放弃")
            return

        self._log(f"检测到进行中的黎明界:")
        self._log(f"  enter_id: {top.enter_id}")
        self._log(f"  公会: {top.guild_id}")
        self._log(f"  难度: {top.difficulty}")

        await client.labyrinth_retire(enter_id=top.enter_id)
        self._log("已放弃本次探索")

        self._table({
            "结果": "已放弃",
            "enter_id": str(top.enter_id),
            "公会": str(top.guild_id),
            "难度": str(top.difficulty),
        })
