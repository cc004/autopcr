from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

@name('露娜塔回廊扫荡')
@default(True)
class tower_cloister_sweep(Module):
    async def do_task(self, client: pcrclient):
        now = apiclient.datetime
        tower_id = db.get_newest_tower_id()
        schedule = db.tower_schedule[tower_id]
        start_time = db.parse_time(schedule.start_time)
        end_time = db.parse_time(schedule.end_time)
        if now < start_time:
            raise SkipError("露娜塔未开启")
        if now > end_time:
            raise SkipError("露娜塔已结束")
        top = await client.get_tower_top()
        if top.cloister_first_cleared_flag != 1:
            raise AbortError("回廊未通关")
        if top.cloister_remain_clear_count:
            times = top.cloister_remain_clear_count
            res = await client.tower_cloister_battle_skip(times)
            result = []
            for rewards in res.quest_result_list:
                result.extend(rewards.reward_list)
            result = await client.serialize_reward_summary(result)
            self._log(f"扫荡了{times}次，获得了:\n" + result)
        else:
            raise SkipError("回廊已扫荡")

