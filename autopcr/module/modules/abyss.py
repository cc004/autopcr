from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from typing import List, Tuple
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from .autosweep import DIY_sweep

class eDifficulty(IntEnum):
    NORMAL = 1
    HARD = 2
    VERY_HARD = 3
    EXTREME = 4

@description('''
深域讨伐战的前哨战扫荡！
'''.strip())
@name("前哨战扫荡")
@default(True)
@tag_stamina_consume
class abyss_quest_sweep(DIY_sweep):
    async def get_start_quest(self, client: pcrclient) -> List[Tuple[int, int]]: 
        ret = []
        for abyss in db.get_active_abyss():
            abyss_id = abyss.abyss_id
            await client.abyss_top(abyss_id)
            for quest in db.abyss_quest_info[abyss_id]:
                ret.append((quest.quest_id, client.data.settings.abyss.daily_clear_limit_count))
        return ret

@description('''
深域讨伐战的Boss战扫荡！将选择分数最高的战斗扫荡\n全通才扫荡指通关所有Boss的EX难度才扫荡，否则不扫荡。
'''.strip())
@name("讨伐Boss战扫荡")
@booltype("abyss_boss_sweep_when_all_clear", "全通才扫荡", True)
@default(True)
@tag_stamina_consume
class abyss_boss_sweep(Module):
    async def do_task(self, client: pcrclient):
        do_sweep_when_all_clear = self.get_config("abyss_boss_sweep_when_all_clear")
        for abyss in db.get_active_abyss():
            self._log(f"=={abyss.title}==")
            abyss_id = abyss.abyss_id
            top = await client.abyss_top(abyss_id)
            boss_info = {boss.boss_id : boss for boss in top.user_boss_list}

            do_sweep = True

            for boss in db.get_abyss_bosses(abyss_id):
                if boss.difficulty != eDifficulty.EXTREME:
                    continue
                boss_status = boss_info.get(boss.boss_id, None)
                if not boss_status or boss_status.enemy_index == 0:
                    if do_sweep_when_all_clear:
                        self._warn(f"未通关{boss.boss_id // 100 % 10}号Boss，跳过扫荡")
                        do_sweep = False

            if do_sweep:
                target_boss = max(
                    (boss for boss in boss_info.values() if boss.enemy_index != 0),
                    key=lambda b: b.best_damage * db.abyss_boss_data[b.boss_id].score_rate,
                )
                boss_ticket_cnt = client.data.get_inventory((eInventoryType.Item, abyss.boss_ticket_id))
                await client.abyss_boss_skip(abyss_id, target_boss.boss_id, target_boss.enemy_index, boss_ticket_cnt, boss_ticket_cnt)
                self._log(f"扫荡{target_boss.boss_id // 100 % 10}号Boss{boss_ticket_cnt}次")

