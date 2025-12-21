from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from typing import List, Tuple
from ...model.error import *
from ...model.custom import eDifficulty
from ...db.database import db
from ...model.enums import *
from .autosweep import DIY_sweep

@description('''
不扫等于15天不上线
'''.strip())
@name("深渊前哨战扫荡")
@default(True)
@tag_stamina_consume
class abyss_quest_sweep(DIY_sweep):
    warn = True

    async def get_start_quest(self, client: pcrclient) -> List[Tuple[int, int]]: 
        ret = []
        for abyss in db.get_active_abyss():
            abyss_id = abyss.abyss_id
            await client.abyss_top(abyss_id)
            for quest in db.abyss_quest_info[abyss_id]:
                ret.append((quest.quest_id, client.data.settings.abyss.daily_clear_limit_count))
        if not ret:
            raise AbortError("当前无进行中的深渊讨伐战")
        return ret

@description('''
将选择分数最高的战斗扫荡\n全通才扫荡指通关所有指定难度的Boss才扫荡，否则不扫荡。
'''.strip())
@name("深渊Boss战扫荡")
@AbyssBossConfig("abyss_boss_sweep_when_all_difficulty_clear", "全通才扫荡", eDifficulty.EXTREME)
@default(True)
class abyss_boss_sweep(Module):
    async def do_task(self, client: pcrclient):
        abyss_difficulty = self.get_config("abyss_boss_sweep_when_all_difficulty_clear")
        do_sweep = False
        rewards = []
        for abyss in db.get_active_abyss():
            self._log(f"=={abyss.title}==")
            abyss_id = abyss.abyss_id
            top = await client.abyss_top(abyss_id)
            boss_info = {boss.boss_id : boss for boss in top.user_boss_list}
            boss_ticket_cnt = client.data.get_inventory((eInventoryType.Item, abyss.boss_ticket_id))

            if boss_ticket_cnt:
                self._log(f"当前持有深渊讨伐券x{boss_ticket_cnt}")
            else:
                self._log("没有深渊讨伐券，跳过扫荡")
                continue

            to_sweep = True

            for boss in db.get_abyss_bosses(abyss_id):
                if boss.difficulty != abyss_difficulty or abyss_difficulty == eDifficulty.NONE:
                    continue
                boss_status = boss_info.get(boss.boss_id, None)
                if not boss_status or boss_status.enemy_index == 1:
                    self._warn(f"未通关{eDifficulty(abyss_difficulty).name} {boss.boss_id // 100 % 10}，跳过扫荡")
                    to_sweep = False

            if to_sweep:
                target_boss = max(
                    (boss for boss in boss_info.values() if boss.enemy_index > 1),
                    key=lambda b: b.best_damage * db.abyss_boss_data[b.boss_id].score_rate,
                    default=None
                )
                if not target_boss:
                    raise AbortError("没有可扫荡的Boss")
                if not boss_ticket_cnt:
                    raise SkipError("没有深渊讨伐券")
                boss_name = f"{eDifficulty(db.abyss_boss_data[target_boss.boss_id].difficulty).name}{target_boss.boss_id // 100 % 10}"
                self._log(f"扫荡{boss_name}x{boss_ticket_cnt}")
                do_sweep = True
                resp = await client.abyss_boss_skip(abyss_id, target_boss.boss_id, target_boss.enemy_index, boss_ticket_cnt, boss_ticket_cnt)
                rewards.extend(resp.reward_list or [])
                rewards.extend(resp.challenge_reward_list or [])

        if rewards:
            self._log("------")
            self._log(await client.serialize_reward_summary(rewards))

        if not self.log:
            self._log("当前无进行中的深渊讨伐战")

        if not do_sweep and not self.is_warn:
            raise SkipError()
