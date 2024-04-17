from ...model.custom import GachaReward
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...model.common import GachaParameter
import datetime
from collections import Counter

@description('扭曲装备扭蛋')
@name('普通扭蛋')
@default(True)
class normal_gacha(Module):
    async def do_task(self, client: pcrclient):
        resp = await client.get_gacha_index()
        normal_gacha: GachaParameter = None
        for gacha in resp.gacha_info:
            if gacha.type == eGachaType.FreeOnly and gacha.cost_num_single == 0:
                normal_gacha = gacha 
                break
        if normal_gacha.free_exec_times != 0:
            raise SkipError("已进行过普通扭蛋")
        resp = await client.exec_gacha(normal_gacha.id, 10, 0, eGachaDrawType.Free, -1, 0)
        memory = [i for i in resp.reward_info_list if db.is_unit_memory((i.type, i.id))]
        msg = "10件装备"
        if memory:
            msg = await client.serlize_reward(memory) + f"\n{10 - len(memory)}件装备"
        self._log(msg)

@description('有免费十连时自动抽取')
@name('免费十连')
@booltype('today_end_gacha_no_do', "当日切卡池前不抽取", True)
@default(False)
class free_gacha(Module):
    async def do_task(self, client: pcrclient):
        res = await client.get_gacha_index()
        if res.campaign_info is None:
            raise SkipError("免费十连已结束")
        schedule = db.campaign_gacha[res.campaign_info.campaign_id]
        gacha_list = db.free_gacha_list[schedule.campaign_id]
        start_time = db.parse_time(schedule.start_time)
        end_time = db.parse_time(schedule.end_time)
        if datetime.datetime.now() >= end_time:
            raise SkipError("免费十连已结束")
        if datetime.datetime.now() < start_time:
            raise SkipError("免费十连尚未开始")
        if res.campaign_info.fg10_exec_cnt == 0:
            raise SkipError("今日份免费十连已使用")
        cnt = res.campaign_info.fg10_exec_cnt
        free_gacha_ids = set(gacha.gacha_id for gacha in gacha_list)
        open_gacha_ids = set(gacha.id for gacha in res.gacha_info)
        open_free_gacha_ids = free_gacha_ids & open_gacha_ids
        close_free_gacha_ids = free_gacha_ids - open_gacha_ids

        switch_no_do = self.get_config("today_end_gacha_no_do")
        today_end_gacha = [id for id in open_free_gacha_ids if db.is_gacha_today_end(id)]
        today_open_gacha = [id for id in close_free_gacha_ids if db.is_gacha_today_start(id)]
        if switch_no_do and (today_end_gacha or today_open_gacha):
            msg = ""
            if today_end_gacha: msg += "卡池【" + "、".join(db.gacha_data[id].pick_up_chara_text for id in today_end_gacha) + "】于今日结束，"
            if today_open_gacha: msg += "卡池【" + "、".join(db.gacha_data[id].pick_up_chara_text for id in today_open_gacha) + "】于今日开始，"
            msg += "不自动抽取\n请自行决定是否抽取"
            raise SkipError(msg)

        target_gacha_id = max(open_free_gacha_ids)
        
        for gacha_info in res.gacha_info:
            if gacha_info.id == target_gacha_id:
                target_gacha = gacha_info
                break
        else:
            raise ValueError("target gacha not found")

        gacha_reward: GachaReward = GachaReward()

        while cnt > 0:
            gacha_reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Campaign10Shot, cnt, res.campaign_info.campaign_id)
            cnt -= 1

        self._log(await client.serlize_gacha_reward(gacha_reward))
