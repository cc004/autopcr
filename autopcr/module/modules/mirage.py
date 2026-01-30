from ...core.apiclient import apiclient
from ...model.common import QuestSkipInfo
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db

@description("每天收取")
@name('追忆战礼物收取')
@default(True)
class mirage_floor_receive(Module):
    async def do_task(self, client: pcrclient):
        top = await client.mirage_top()
        if top.reward_full_time == -1:
            raise AbortError(f"追忆战未通关")
        # max_floor = max(db.mirage_floor_setting.keys())
        # if top.max_cleared_floor_num < max_floor:
            # self._warn(f"最高层{db.get_quest_name(db.mirage_floor_setting[max_floor].quest_id)}未通关")
        setting = db.get_mirage_setting()
        if top.reward_full_time - apiclient.time < (setting.pool_reward_accumulate_day_num_max - 1) * 24 * 60 * 60:
            resp = await client.mirage_receive_reward(eSystemId.MIRAGE)
            rewards = resp.reward_info or []

            self._log("领取了礼物箱，获得了:")
            self._log(await client.serialize_reward_summary(rewards))
        else:
            raise SkipError("礼物箱无奖励")

@booltype("mirage_nemesis_sweep_not_max_stop", "非最高不扫荡", True)
@description("每周扫荡")
@name('追忆战・霸扫荡')
@default(True)
class mirage_nemesis_sweep(Module):
    async def do_task(self, client: pcrclient):
        not_max_stop = self.get_config("mirage_nemesis_sweep_not_max_stop")
        top = await client.mirage_top()
        to_skip = []
        setting = db.get_mirage_setting()
        for nemesis_id in db.mirage_nemesis_quest:
            if nemesis_id not in db.mirage_nemesis_area:
                continue
            boss = next((b for b in top.nemesis_progress or [] if b.nemesis_id == nemesis_id), None)
            if db.mirage_nemesis_area[nemesis_id].condition_story_id not in client.data.read_story_ids:
                self._warn(f"未阅读剧情{db.story_detail[db.mirage_nemesis_area[nemesis_id].condition_story_id].title}，无法进入{db.mirage_nemesis_area[nemesis_id].nemesis_area_name}")
                continue
            if not boss:
                self._warn(f"未首通{db.mirage_nemesis_area[nemesis_id].nemesis_area_name}，无法扫荡")
                continue

            boss_info = db.mirage_nemesis_quest[nemesis_id]
            max_level = max(boss_info.keys())
            if boss.area_level < max_level and not_max_stop:
                self._warn(f"最高等级{db.get_quest_name(boss_info[max_level].quest_id)}未通关，不扫荡\n如欲扫荡已通关的，请关闭「非最高不扫荡」")
                continue
            if boss.periodic_clear_count < setting.challenge_count_max:
                to_skip.append((boss_info[boss.area_level].quest_id, setting.challenge_count_max - boss.periodic_clear_count))
        if not to_skip:
            if not self.log:
                raise SkipError("本周追忆战・霸已扫荡")
            return

        skip_info = [QuestSkipInfo(quest_id=qid, skip_count=count) for qid, count in to_skip]
        resp = await client.mirage_nemesis_skip_multiple(skip_info)

        self._log(f"扫荡了\n" + '\n'.join(f"{db.get_quest_name(qid)} x{count}" for qid, count in to_skip))

        rewards = []
        rewards.extend(resp.drop_reward_list or [])

        self._log("获得了:")
        self._log(await client.serialize_reward_summary(rewards))
