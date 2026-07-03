from typing import List, Set

from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

LABYRINTH_AREA3_BOSSES = [
    (312505, "厄勒克特拉夫人", "简单"),
    (319604, "冰霜魔狼", "简单"),
    (303306, "暗黑滴水嘴兽", "普通"),
    (301206, "巨型魔像", "普通"),
    (306604, "毒液沙鳗蛇", "困难"),
]

LABYRINTH_AREA5_BOSSES = [
    (310103, "愤怒巨龙", "简单"),
    (301701, "炸脖龙", "普通"),
    (319401, "究极守护者", "普通"),
    (315004, "领主哥布林", "困难"),
    (302501, "奇美拉", "困难"),
]

LABYRINTH_BOSS_NAME_BY_UNIT = {
    unit_id: name
    for unit_id, name, _ in LABYRINTH_AREA3_BOSSES + LABYRINTH_AREA5_BOSSES
}

LABYRINTH_BLOCK_TYPE_NAME = {
    1: "起点",
    2: "普通怪物",
    3: "EX怪物",
    4: "角色",
    5: "事件",
    6: "遗物",
    7: "商店",
    8: "Boss",
}

class LabyrinthBossConfig(MultiChoiceConfig):
    def __init__(self, key: str, desc: str, boss_list: List[Tuple[int, str, str]]):
        simple_bosses = [unit_id for unit_id, _, difficulty in boss_list if difficulty == "简单"]
        super().__init__(key, desc, simple_bosses, [unit_id for unit_id, _, _ in boss_list])
        self.boss_info = {unit_id: (name, difficulty) for unit_id, name, difficulty in boss_list}

    def candidate_display(self, unit_id: int):
        name, difficulty = self.boss_info.get(unit_id, (str(unit_id), "未知"))
        return f"【{difficulty}】{name}"


@description('刷黎明界开局，直到符合要求为准。若已进入黎明界，会无条件撤退，再刷取。完美开局指路线不会错过任何EX关卡和必要的遗物，适合凹高分。区域3/5第3格有遗物和事件两种，遗物固定200分，事件可高可低，求稳or赌狗。')
@name('黎明界刷开局')
@LabyrinthBossConfig('labyrinth_reroll_area5_boss', '区域5Boss', LABYRINTH_AREA5_BOSSES)
@LabyrinthBossConfig('labyrinth_reroll_area3_boss', '区域3Boss', LABYRINTH_AREA3_BOSSES)
@singlechoice('labyrinth_reroll_third_block_type', '区域3/5第3格', '两者都行', ['必须遗物', '必须事件', '两者都行'])
@booltype('labyrinth_reroll_perfect_start', '完美开局', False)
@LabyrinthGuildConfig('labyrinth_reroll_guild_id', '公会', 5)
@singlechoice('labyrinth_reroll_difficulty', '难度', 5, [1, 2, 3, 4, 5])
class labyrinth_start_reroll(Module):
    AREA_REQUIREMENTS: Dict[int, Dict[int, int]] = {
        1: {1: 1, 2: 2, 3: 4, 4: 2, 5: 4, 6: 6},
        2: {1: 1, 2: 4, 3: 2, 4: 6, 5: 3, 6: 4, 7: 6},
        3: {1: 1, 2: 2, 3: 6, 4: 4, 5: 3, 6: 7, 7: 8},
        4: {1: 1, 2: 4, 3: 3, 4: 5, 5: 3, 6: 2, 7: 4, 8: 7},
        5: {1: 1, 2: 2, 3: 6, 4: 3, 5: 6, 6: 3, 7: 7, 8: 8},
    }

    def _block_type(self, block) -> int:
        return int(block.block_type) if block.block_type is not None else 0

    def _position_name(self, block, area_columns: Dict[int, List]) -> str:
        rows = [b.row for b in area_columns.get(block.column, [])]
        max_row = max(rows) if rows else block.row
        if max_row <= 1:
            return "合流"
        if max_row == 2:
            return {1: "下", 2: "上"}.get(block.row, str(block.row))
        if max_row == 3:
            return {1: "下", 2: "中", 3: "上"}.get(block.row, str(block.row))
        return str(block.row)

    def _boss_unit_ids(self, block) -> Set[int]:
        quest_id = getattr(block, "quest_id", None)
        if not quest_id:
            return set()
        quest = db.labyrinth_quest_data.get(quest_id)
        if not quest:
            return set()
        wave_group = db.labyrinth_wave_group_data.get(quest.wave_group_id)
        if not wave_group:
            return set()
        unit_ids: Set[int] = set()
        for enemy_id in wave_group.get_enemy_ids():
            enemy = db.labyrinth_enemy_parameter.get(enemy_id)
            if enemy:
                unit_ids.add(enemy.unit_id)
        return unit_ids

    def _boss_matches(self, area: int, block, area3_bosses: Set[int], area5_bosses: Set[int]) -> bool:
        selected = area3_bosses if area == 3 else area5_bosses if area == 5 else set()
        if not selected:
            return True
        return bool(self._boss_unit_ids(block) & selected)

    def _target_areas(self, difficulty: int) -> List[int]:
        if difficulty == 1:
            return [1, 2, 3]
        return sorted(self.AREA_REQUIREMENTS)

    def _max_unlocked_difficulty(self, top) -> int:
        cleared = [
            info.difficulty
            for info in (top.guild_cleared_difficulty_list or [])
            if getattr(info, "difficulty", None)
        ]
        if not cleared:
            return 1
        return min(max(cleared) + 1, 5)

    def _expected_block_types(self, area: int, column: int, third_block_type: str) -> Set[int]:
        if area in {3, 5} and column == 3:
            if third_block_type == '必须事件':
                return {5}
            if third_block_type == '两者都行':
                return {5, 6}
            return {6}
        return {self.AREA_REQUIREMENTS[area][column]}

    def _find_area_route(self, area: int, map_list: List, area3_bosses: Set[int], area5_bosses: Set[int], third_block_type: str, perfect_start: bool) -> Tuple[Optional[List], str]:
        expected = self.AREA_REQUIREMENTS[area]
        blocks = [block for block in map_list if block.area == area]
        if not blocks:
            return None, f"区域{area}没有地图数据"

        by_id = {block.block_id: block for block in blocks}
        by_column: Dict[int, List] = {}
        for block in blocks:
            by_column.setdefault(block.column, []).append(block)
        for column_blocks in by_column.values():
            column_blocks.sort(key=lambda block: block.row)

        missing_columns = [column for column in expected if column not in by_column]
        if missing_columns:
            return None, f"区域{area}缺少列{missing_columns}"

        last_column = max(expected)

        def dfs(block, path: List, seen: Set[int]) -> Optional[List]:
            column = block.column
            if column in expected:
                if perfect_start and self._block_type(block) not in self._expected_block_types(area, column, third_block_type):
                    return None

            if column == last_column:
                if expected[column] == 8 and not self._boss_matches(area, block, area3_bosses, area5_bosses):
                    return None
                return path + [block]

            for next_block_id in block.next_block_id_list or []:
                if next_block_id in seen:
                    continue
                next_block = by_id.get(next_block_id)
                if not next_block:
                    continue
                route = dfs(next_block, path + [block], seen | {next_block_id})
                if route:
                    return route
            return None

        for start in by_column[1]:
            route = dfs(start, [], {start.block_id})
            if route:
                return route, ""

        return None, f"区域{area}没有满足条件的可达路线"

    def _find_routes(self, map_list: List, difficulty: int, area3_bosses: Set[int], area5_bosses: Set[int], third_block_type: str, perfect_start: bool) -> Tuple[Optional[Dict[int, List]], str]:
        routes: Dict[int, List] = {}
        failures = []
        for area in self._target_areas(difficulty):
            route, reason = self._find_area_route(area, map_list, area3_bosses, area5_bosses, third_block_type, perfect_start)
            if not route:
                failures.append(reason)
            else:
                routes[area] = route
        if failures:
            return None, "；".join(failures)
        return routes, ""

    def _format_route(self, area: int, route: List, map_list: List, area3_bosses: Set[int], area5_bosses: Set[int]) -> str:
        area_columns: Dict[int, List] = {}
        for block in map_list:
            if block.area == area:
                area_columns.setdefault(block.column, []).append(block)

        parts = []
        for block in route:
            position = self._position_name(block, area_columns)
            block_type_name = LABYRINTH_BLOCK_TYPE_NAME.get(self._block_type(block), str(self._block_type(block)))
            extra = ""
            if self._block_type(block) == 8:
                boss_units = self._boss_unit_ids(block)
                if boss_units:
                    selected = area3_bosses if area == 3 else area5_bosses if area == 5 else set()
                    candidates = selected or set(LABYRINTH_BOSS_NAME_BY_UNIT)
                    boss_names = [
                        LABYRINTH_BOSS_NAME_BY_UNIT[unit_id]
                        for unit_id in sorted(boss_units & candidates)
                        if unit_id in LABYRINTH_BOSS_NAME_BY_UNIT
                    ]
                    if boss_names:
                        extra = f"({'/'.join(boss_names)})"
            parts.append(f"{block.column}{position}【{block_type_name}{extra}】")
        return f"区域{area}：" + "-".join(parts)

    async def do_task(self, client: pcrclient):
        guild_id: int = self.get_config('labyrinth_reroll_guild_id')
        difficulty: int = self.get_config('labyrinth_reroll_difficulty')
        area3_bosses: Set[int] = set(self.get_config('labyrinth_reroll_area3_boss'))
        area5_bosses: Set[int] = set(self.get_config('labyrinth_reroll_area5_boss'))
        third_block_type: str = self.get_config('labyrinth_reroll_third_block_type')
        perfect_start: bool = self.get_config('labyrinth_reroll_perfect_start')
        max_count: int = 100

        top = await client.labyrinth_top()
        max_unlocked_difficulty = self._max_unlocked_difficulty(top)
        if difficulty > max_unlocked_difficulty:
            self._warn(f"黎明界难度{difficulty}尚未解锁，当前最大可挑战难度为{max_unlocked_difficulty}，跳过执行。")
            raise AbortError("未解锁所选黎明界难度")

        if top.enter_id:
            self._log("检测到已有黎明界开局，先撤退。")
            await client.labyrinth_retire(top.enter_id)

        last_reason = ""
        for attempt in range(1, max_count + 1):
            enter = await client.labyrinth_enter(guild_id, difficulty)
            routes, reason = self._find_routes(enter.map_list or [], difficulty, area3_bosses, area5_bosses, third_block_type, perfect_start)
            if routes:
                self._log(f"刷到{'完美' if perfect_start else ''}路线，总尝试次数：{attempt}")
                for area in sorted(routes):
                    self._log(self._format_route(area, routes[area], enter.map_list or [], area3_bosses, area5_bosses))
                return

            last_reason = reason
            if enter.enter_id:
                await client.labyrinth_retire(enter.enter_id)
            await client.labyrinth_top()

        raise AbortError(f"重开{max_count}次仍未刷到目标路线，最后失败原因：{last_reason}")
