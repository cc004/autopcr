from abc import abstractmethod
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.common import InventoryInfo
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...model.custom import ItemType
from ...util.linq import flow

from typing import cast

TALENT_TARGET_NAMES: list[str] = list(db.talents.keys())


@MultiChoiceConfig(
    "talent_sweep_target_recovery_areas", "需要重置的属性图", [], TALENT_TARGET_NAMES
)
@MultiChoiceConfig(
    "talent_sweep_targets", "需要扫荡的属性图", TALENT_TARGET_NAMES, TALENT_TARGET_NAMES
)
@name("深域扫荡")
@default(False)
@tag_stamina_consume
class talent_sweep(Module):
    def get_daily_recovery_count(self, client: pcrclient, talent_id: int) -> int:
        area_info = client.data.talent_quest_area_info.get(talent_id)
        return area_info.daily_recovery_count if area_info else 0

    def get_daily_clear_count(self, client: pcrclient, talent_id: int) -> int:
        area_info = client.data.talent_quest_area_info.get(talent_id)
        return area_info.daily_clear_count if area_info else 0

    async def do_task(self, client: pcrclient):
        targets = self.get_config("talent_sweep_targets")
        target_recovery_areas: list[str] = self.get_config(
            "talent_sweep_target_recovery_areas"
        )

        clear_limit_count = client.data.settings.talent_quest.daily_clear_limit_count
        recovery_max_count = client.data.settings.talent_quest.recovery_max_count

        cleared_talent_quest_id_set = client.data.cleared_talent_quest_id_set

        if not targets:
            raise SkipError("没有需要扫荡的深域图")

        for talent_name in targets:
            talent_id = db.talents[talent_name].talent_id
            area = db.talent_areas[talent_id]
            area_info = client.data.talent_quest_area_info.get(talent_id)

            daily_clear_count = self.get_daily_clear_count(client, talent_id)

            quest_id: int | None = next(
                filter(
                    lambda i: i in db.talent_quests_by_area[area.area_id],
                    cleared_talent_quest_id_set,
                ),
                None,
            )
            if not quest_id:
                self._log(f"深域属性图[{talent_name}]尚未通关")
                continue
            quest_info = db.talent_quests_by_area[area.area_id][quest_id]

            need_reset = talent_name in target_recovery_areas
            total_times = clear_limit_count * (
                1 + (recovery_max_count if need_reset else 0)
            )
            if daily_clear_count >= total_times:
                self._log(
                    f"深域属性图[{talent_name}]今日已经扫荡{daily_clear_count}次，无需扫荡"
                )
                continue

            res: list[InventoryInfo] = []
            while self.get_daily_clear_count(client, talent_id) < total_times:
                times_in_this_round = clear_limit_count * (
                    self.get_daily_recovery_count(client, talent_id) + 1
                ) - self.get_daily_clear_count(client, talent_id)

                if times_in_this_round <= 0:
                    await client.talent_quest_recovery_challenge(talent_id)
                    continue

                stamina = client.data.stamina
                stamina_times_round = min(
                    times_in_this_round, stamina // quest_info.stamina
                )

                if stamina_times_round <= 0:
                    self._warn("体力不足")
                    break

                r = await client.talent_quest_skip(quest_id, stamina_times_round)
                res.extend(r.item_list)
                for q in r.quest_result_list:
                    res.extend(q.reward_list)
                res.extend(r.bonus_reward_list)
            if res:
                self._log(
                    f"扫荡[{db.quest_name[quest_id]}]共{total_times - daily_clear_count}次，获得："
                    "\n" + await client.serialize_reward_summary(res)
                )
