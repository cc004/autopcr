from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
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
        resp = await client.exec_gacha(normal_gacha.id, 10, 0, 1, -1, 0)
        memory = [i for i in resp.reward_info_list if db.is_unit_memory((i.type, i.id))]
        msg = "10件装备"
        if memory:
            msg = await client.serlize_reward(memory) + f"\n{10 - len(memory)}件装备"
        self._log(msg)

@description('有免费十连时自动抽取')
@name('免费十连')
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
        gacha_list = set(gacha.gacha_id for gacha in gacha_list)
        for gacha_info in res.gacha_info:
            if gacha_info.id in gacha_list:
                target_gacha = gacha_info
                break
        else:
            raise ValueError("target gacha not found")
        reward_list = []
        new_unit = []
        unit_rarity = Counter()
        prize_rarity = Counter()
        if target_gacha.selected_item_id == 0:
            self._log("未选择奖励碎片")
            prizegacha_id = db.gacha_data[target_gacha.id].prizegacha_id
            if db.prizegacha_data[prizegacha_id].prize_memory_id_2 != 0:
                raise AbortError("可选碎片大于一种，请自行手动选择")
            item_id = db.prizegacha_data[prizegacha_id].prize_memory_id_1
            await client.gacha_select_prize(prizegacha_id, item_id)
            self._log(f"选择了{db.get_inventory_name_san((eInventoryType.Item, item_id))}")

        while cnt > 0:
            resp = await client.exec_gacha(target_gacha.id, 10, target_gacha.exchange_id, 6, cnt, res.campaign_info.campaign_id)
            cnt -= 1

            new_unit += [item for item in resp.reward_info_list if item.type == eInventoryType.Unit]
            reward_list += [item for item in resp.reward_info_list if item.type != eInventoryType.Unit]

            unit_rarity += Counter(item.unit_data.unit_rarity for item in resp.reward_info_list if item.type == eInventoryType.Unit)
            unit_rarity += Counter(item.exchange_data.rarity for item in resp.reward_info_list if item.type != eInventoryType.Unit)

            if resp.prize_reward_info:
                prize_rarity += Counter(prize.rarity for prize in vars(resp.prize_reward_info).values() if prize is not None)
                reward_list += [item for prize in vars(resp.prize_reward_info).values() if prize is not None for item in prize.rewards]
            if resp.bonus_reward_info:
                reward_list += [item for item in vars(resp.bonus_reward_info).values() if item is not None]

        if new_unit:
            self._log(f"NEW: \n" + '\n'.join([db.get_inventory_name(item) for item in new_unit]) + '\n')
        if unit_rarity:
            self._log(' '.join(["★"*i + f"x{cnt}" for i, cnt in unit_rarity.items()]))
        if prize_rarity:
            self._log(' '.join([f"{i}等" + f"x{cnt}" for i, cnt in prize_rarity.items()]))
        self._log(await client.serlize_reward(reward_list))
