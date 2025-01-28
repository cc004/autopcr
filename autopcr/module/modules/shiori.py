from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *


@description("领取已通关外传的任务奖励，对于未通关或未取得三星的关卡会进行提示")
@name("领取外传任务奖励")
@default(True)
class shiori_mission_check(Module):
    async def do_task(self, client: pcrclient):
        shiori_top = await client.get_shiori_top()
        clear_event_list = shiori_top.clear_event_list

        if not clear_event_list:
            raise SkipError("没有已通关的外传活动")

        for event_id in clear_event_list:
            if self.find_cache(f"shiori-check-{event_id}"):
                continue

            event_top = await client.get_shiori_event_top(event_id)
            event_quests = db.shiori_event_quests[event_id]
            top_quests = {q.quest_id: q for q in event_top.quest_list}

            if all(
                m.mission_status == eMissionStatusType.AlreadyReceive
                for m in event_top.missions
            ) and sum(q.clear_flg == 3 for q in event_top.quest_list) == len(
                event_quests
            ):
                self.save_cache(f"shiori-check-{event_id}", 1)
                continue

            self._log(f"{event_id}:{db.event_name[event_id]}：")

            if any(
                m.mission_status == eMissionStatusType.EnableReceive
                for m in event_top.missions
            ):
                resp = await client.shiori_mission_receive(event_id)
                self._log(
                    f"领取了任务奖励，获得了:\n"
                    + await client.serlize_reward(resp.rewards)
                )

            for quest_id in event_quests:
                if quest_id not in top_quests:
                    self._warn(f"关卡 {db.quest_name[quest_id]} 尚未通关")
                elif top_quests[quest_id].clear_flg != 3:
                    self._warn(f"关卡 {db.quest_name[quest_id]} 尚未取得3星")

        if not self.log:
            raise SkipError("所有已通关外传的任务奖励均已领取")
