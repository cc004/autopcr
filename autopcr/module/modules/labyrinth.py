from typing import Dict, List, Optional, Set, Tuple

from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import eLabyrinthBlockType

LABYRINTH_BLOCK_TYPE_NAME = {
    eLabyrinthBlockType.NONE: "起点",
    eLabyrinthBlockType.NORMAL_QUEST: "普通怪物",
    eLabyrinthBlockType.HARD_QUEST: "EX怪物",
    eLabyrinthBlockType.TICKET: "角色",
    eLabyrinthBlockType.EVENT: "事件",
    eLabyrinthBlockType.RELIC: "遗物",
    eLabyrinthBlockType.SHOP: "商店",
    eLabyrinthBlockType.BOSS_QUEST: "Boss",
}


@description('刷分用。若已进入黎明界，会立刻撤退。\n完美开局指一层双角色、二层双角色+遗物+EX+遗物/商店，三层角色+遗物+遗物/事件，四层双角色+双EX，五层遗物/事件+双EX。遗物固定分，事件分可高可低。')
@name('黎明界刷开局')
@LabyrinthBossConfig('labyrinth_reroll_area5_boss', '区域5Boss', 5, [301701, 310103, 319401, 315004])
@LabyrinthBossConfig('labyrinth_reroll_area3_boss', '区域3Boss', 3, [301206, 312505, 319604])
@singlechoice('labyrinth_reroll_third_block_type', '区域3/5第3格', '事件', ['遗物', '事件', '任意'])
@singlechoice('labyrinth_reroll_second_block_type', '区域2第4格', '遗物', ['遗物', '商店', '任意'])
@singlechoice('labyrinth_reroll_max_count', '重开上限', 100, [100, 500, 1000, 2000])
@booltype('labyrinth_reroll_perfect_start', '完美开局', False)
@LabyrinthGuildConfig('labyrinth_reroll_guild_id', '公会', 5)
@singlechoice('labyrinth_reroll_difficulty', '难度', 5, [1, 2, 3, 4, 5])
class labyrinth_start_reroll(Module):
    AREA_REQUIREMENTS: Dict[int, Dict[int, Set[eLabyrinthBlockType]]] = {
        1: {
            1: {eLabyrinthBlockType.NONE},
            2: {eLabyrinthBlockType.NORMAL_QUEST},
            3: {eLabyrinthBlockType.TICKET},
            4: {eLabyrinthBlockType.NORMAL_QUEST},
            5: {eLabyrinthBlockType.TICKET},
            6: {eLabyrinthBlockType.RELIC},
        },
        2: {
            1: {eLabyrinthBlockType.NONE},
            2: {eLabyrinthBlockType.TICKET},
            3: {eLabyrinthBlockType.NORMAL_QUEST},
            4: {eLabyrinthBlockType.RELIC, eLabyrinthBlockType.SHOP},
            5: {eLabyrinthBlockType.HARD_QUEST},
            6: {eLabyrinthBlockType.TICKET},
            7: {eLabyrinthBlockType.RELIC},
        },
        3: {
            1: {eLabyrinthBlockType.NONE},
            2: {eLabyrinthBlockType.NORMAL_QUEST},
            3: {eLabyrinthBlockType.EVENT, eLabyrinthBlockType.RELIC},
            4: {eLabyrinthBlockType.TICKET},
            5: {eLabyrinthBlockType.HARD_QUEST},
            6: {eLabyrinthBlockType.SHOP},
            7: {eLabyrinthBlockType.BOSS_QUEST},
        },
        4: {
            1: {eLabyrinthBlockType.NONE},
            2: {eLabyrinthBlockType.TICKET},
            3: {eLabyrinthBlockType.HARD_QUEST},
            4: {eLabyrinthBlockType.EVENT},
            5: {eLabyrinthBlockType.HARD_QUEST},
            6: {eLabyrinthBlockType.NORMAL_QUEST},
            7: {eLabyrinthBlockType.TICKET},
            8: {eLabyrinthBlockType.SHOP},
        },
        5: {
            1: {eLabyrinthBlockType.NONE},
            2: {eLabyrinthBlockType.NORMAL_QUEST},
            3: {eLabyrinthBlockType.EVENT, eLabyrinthBlockType.RELIC},
            4: {eLabyrinthBlockType.HARD_QUEST},
            5: {eLabyrinthBlockType.RELIC},
            6: {eLabyrinthBlockType.HARD_QUEST},
            7: {eLabyrinthBlockType.SHOP},
            8: {eLabyrinthBlockType.BOSS_QUEST},
        },
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
            if info.difficulty is not None
        ]
        if not cleared:
            return 1
        return min(max(cleared) + 1, 5)

    def _build_expected_block_types(self, third_block_type: str, second_block_type: str) -> Dict[int, Dict[int, Set[eLabyrinthBlockType]]]:
        expected = {
            area: {
                column: set(block_types)
                for column, block_types in requirements.items()
            }
            for area, requirements in self.AREA_REQUIREMENTS.items()
        }

        third_types = {
            '遗物': {eLabyrinthBlockType.RELIC},
            '事件': {eLabyrinthBlockType.EVENT},
            '任意': {eLabyrinthBlockType.EVENT, eLabyrinthBlockType.RELIC},
        }.get(third_block_type, {eLabyrinthBlockType.RELIC})
        expected[3][3] = set(third_types)
        expected[5][3] = set(third_types)

        second_types = {
            '遗物': {eLabyrinthBlockType.RELIC},
            '商店': {eLabyrinthBlockType.SHOP},
            '任意': {eLabyrinthBlockType.RELIC, eLabyrinthBlockType.SHOP},
        }.get(second_block_type, {eLabyrinthBlockType.RELIC})
        expected[2][4] = set(second_types)
        return expected

    def _find_area_route(self, area: int, map_list: List, area3_bosses: Set[int], area5_bosses: Set[int], perfect_start: bool, expected_block_types: Dict[int, Dict[int, Set[eLabyrinthBlockType]]]) -> Tuple[Optional[List], str]:
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
                if perfect_start and self._block_type(block) not in expected_block_types[area][column]:
                    return None

            if column == last_column:
                if eLabyrinthBlockType.BOSS_QUEST in expected[column] and not self._boss_matches(area, block, area3_bosses, area5_bosses):
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

    def _find_routes(self, map_list: List, difficulty: int, area3_bosses: Set[int], area5_bosses: Set[int], perfect_start: bool, expected_block_types: Dict[int, Dict[int, Set[eLabyrinthBlockType]]]) -> Tuple[Optional[Dict[int, List]], str]:
        routes: Dict[int, List] = {}
        failures = []
        for area in self._target_areas(difficulty):
            route, reason = self._find_area_route(area, map_list, area3_bosses, area5_bosses, perfect_start, expected_block_types)
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
            block_type = self._block_type(block)
            block_type_name = LABYRINTH_BLOCK_TYPE_NAME.get(block_type, str(block_type))
            extra = ""
            if block_type == eLabyrinthBlockType.BOSS_QUEST:
                boss_units = self._boss_unit_ids(block)
                if boss_units:
                    selected = area3_bosses if area == 3 else area5_bosses if area == 5 else set()
                    boss_info = db.labyrinth_boss_info.get(area, {})
                    candidates = selected or set(boss_info)
                    boss_names = [
                        boss_info[unit_id]
                        for unit_id in sorted(boss_units & candidates)
                        if unit_id in boss_info
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
        second_block_type: str = self.get_config('labyrinth_reroll_second_block_type')
        perfect_start: bool = self.get_config('labyrinth_reroll_perfect_start')
        max_count: int = self.get_config('labyrinth_reroll_max_count')
        expected_block_types = self._build_expected_block_types(third_block_type, second_block_type)

        top = await client.labyrinth_top()
        max_unlocked_difficulty = self._max_unlocked_difficulty(top)
        if difficulty > max_unlocked_difficulty:
            self._warn(f"黎明界难度{difficulty}尚未解锁，当前最大可挑战难度为{max_unlocked_difficulty}，跳过执行。")
            raise AbortError("未解锁所选黎明界难度")

        if top.enter_id:
            self._log("检测到已有黎明界开局，先撤退。")
            await client.labyrinth_retire(top.enter_id)

        for attempt in range(1, max_count + 1):
            enter = await client.labyrinth_enter(guild_id, difficulty)
            routes, _ = self._find_routes(enter.map_list or [], difficulty, area3_bosses, area5_bosses, perfect_start, expected_block_types)
            if routes:
                self._log(f"刷到{'完美' if perfect_start else ''}路线，总尝试次数：{attempt}")
                for area in sorted(routes):
                    self._log(self._format_route(area, routes[area], enter.map_list or [], area3_bosses, area5_bosses))
                return

            if enter.enter_id:
                await client.labyrinth_retire(enter.enter_id)
            await client.labyrinth_top()

        raise AbortError(f"重开{max_count}次仍未刷到目标路线")


@description('当黎明界通行证超过保留数量时，使用超出的通行证扫荡。难度自动使用所选公会已通关的最高难度。')
@name('黎明界扫荡')
@inttype('labyrinth_sweep_ticket_hold', '保留黎明界票数', 96, list(range(100)))
@LabyrinthGuildConfig('labyrinth_sweep_guild_id', '公会', 5)
@default(True)
class labyrinth_sweep(Module):
    def _max_cleared_difficulty(self, top, guild_id: int) -> Optional[int]:
        cleared = [
            info.difficulty
            for info in (top.guild_cleared_difficulty_list or [])
            if info.guild_id == guild_id and info.difficulty is not None
        ]
        return max(cleared) if cleared else None

    async def do_task(self, client: pcrclient):
        ticket_hold: int = self.get_config('labyrinth_sweep_ticket_hold')
        guild_id: int = self.get_config('labyrinth_sweep_guild_id')
        ticket_count = client.data.get_inventory(db.labyrinth_ticket)
        skip_count = ticket_count - ticket_hold
        if skip_count <= 0:
            raise SkipError(f'当前黎明界票数为{ticket_count}，不超过保留数量{ticket_hold}')

        top = await client.labyrinth_top()
        difficulty = self._max_cleared_difficulty(top, guild_id)
        if difficulty is None:
            raise AbortError(f'公会{guild_id}尚未通关黎明界，无法扫荡！')

        self._log(f'公会{guild_id}，难度{difficulty}，当前票数{ticket_count}，扫荡{skip_count}次')
        response = await client.labyrinth_skip(guild_id, skip_count)
        rewards = []
        for reward_list in (
            response.skip_reward_list,
            response.treasure_box_reward_list,
            response.item_list,
        ):
            rewards.extend(reward_list or [])
        if rewards:
            self._log(await client.serialize_reward_summary(rewards))
