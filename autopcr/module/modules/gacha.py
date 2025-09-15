from ...model.custom import GachaReward
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...model.common import GachaParameter
import datetime

@description('进行装备扭蛋')
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
            msg = await client.serialize_reward_summary(memory) + f"\n{10 - len(memory)}件装备"
        self._log(msg)

@description('每日免费一抽')
@name('凭证扭蛋')
@default(True)
class monthly_gacha(Module):
    async def do_task(self, client: pcrclient):
        if not client.data.resident_info or apiclient.datetime > db.parse_time(client.data.resident_info.end_time):
            raise SkipError("未购买凭证月卡")
        resp = await client.get_gacha_resident_index()
        if len(resp.gacha_info) != 1:
            raise ValueError("怎么有多个凭证扭蛋可以同时抽取？")
        end_time = db.parse_time(client.data.resident_info.end_time)
        if db.is_today(end_time):
            self._warn("今日凭证扭蛋最后一天")
        point_info = client.data.resident_info.gacha_point_info
        if point_info.current_point >= point_info.max_point:
            raise AbortError(f"已达到天井{point_info.current_point}pt，请上号兑换角色")
        gacha = resp.gacha_info[0]
        gacha_reward: GachaReward = GachaReward()
        if not resp.free_gacha_info.fg1_exec_cnt:
            self._log("今日单抽已使用")
        else:
            self._log("使用单抽")
            gacha_reward += await client.exec_gacha_aware(gacha, 1, eGachaDrawType.Monthly_Free_Single, 1, 0)

        if not resp.free_gacha_info.fg10_exec_cnt and resp.free_gacha_info.fg10_last_exec_time:
            self._log("十连已使用")
        elif resp.free_gacha_info.fg10_exec_cnt:
            self._log("使用十连")
            gacha_reward += await client.exec_gacha_aware(gacha, 10, eGachaDrawType.Monthly_Free_Multi, 1, 0)

        reward = await client.serlize_gacha_reward(gacha_reward, gacha.id)
        if reward != "无":
            self._log(reward)
            point = client.data.gacha_point[gacha.exchange_id].current_point if gacha.exchange_id in client.data.gacha_point else 0
            self._log(f"当前pt为{point}")


@description('有免费十连时自动抽取，附奖池自动选择缺口最多的碎片，多卡池可抽取则选择编号大的。卡池编号名字可于“危险”栏查看。智能pickup指当抽出pickup角色后自动切换未拥有的pickup角色，有多个则选角色编号大的。未选够pickup角色会自动选。')
@name('免费十连')
@booltype('today_end_gacha_no_do', "当日切卡池前不抽取", True)
@booltype('free_gacha_start_auto_select_pickup_min_first', "PickUp编号小优先", False)
@booltype('free_gacha_auto_select_pickup', "智能pickup", True)
@multichoice('free_gacha_select_ids', "抽取卡池", db.free_gacha_ids_candidate, db.free_gacha_ids_candidate)
@default(False)
class free_gacha(Module):
    async def do_task(self, client: pcrclient):
        res = await client.get_gacha_index()
        if res.campaign_info is None:
            raise SkipError("免费十连已结束")
        free_gacha_select_ids: List[str] = self.get_config("free_gacha_select_ids")
        free_gacha_auto_select_pickup: bool = self.get_config("free_gacha_auto_select_pickup")
        pickup_min_first: bool = self.get_config("free_gacha_start_auto_select_pickup_min_first")
        schedule = db.campaign_gacha[res.campaign_info.campaign_id]
        gacha_list = db.campaign_free_gacha_data[schedule.campaign_id]
        start_time = db.parse_time(schedule.start_time)
        end_time = db.parse_time(schedule.end_time)
        if apiclient.datetime >= end_time:
            raise SkipError("免费十连已结束")
        if apiclient.datetime < start_time:
            raise SkipError("免费十连尚未开始")
        if res.campaign_info.fg10_exec_cnt == 0:
            raise SkipError("今日份免费十连已使用")
        cnt = res.campaign_info.fg10_exec_cnt
        free_gacha_ids = set(gacha.gacha_id for gacha in gacha_list) & set(db.gacha_data)
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

        select_open_free_gacha_ids = open_free_gacha_ids & set(int(i) for i in free_gacha_select_ids)
        if not select_open_free_gacha_ids:
            raise AbortError(f"没有可抽取的卡池，请重新配置")
        target_gacha_id = max(select_open_free_gacha_ids)
        
        for gacha_info in res.gacha_info:
            if gacha_info.id == target_gacha_id:
                target_gacha = gacha_info
                break
        else:
            raise ValueError("target gacha not found")

        gacha_reward: GachaReward = GachaReward()

        self._log(f"抽取卡池：{db.gacha_data[target_gacha.id].gacha_name}")

        while cnt > 0:
            gacha_reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Campaign10Shot, cnt, res.campaign_info.campaign_id, free_gacha_auto_select_pickup, pickup_min_first)
            cnt -= 1

        self._log(await client.serlize_gacha_reward(gacha_reward, target_gacha.id))
