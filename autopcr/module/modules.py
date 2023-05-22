from ..core import pcrclient
from ..model.models import *
from .modulebase import *

import datetime
from ..model.error import *
from ..core.database import db
from ..model.models import *
import random
import itertools
from abc import abstractmethod

@enumtype([x for x in range(-1, 24)])
@default(-1)
class cron(Module):
    def cron_hook(self) -> int:
        return self.value

@description('定时清日常1')
class cron1(cron): ...

@description('定时清日常2')
class cron2(cron): ...

@description('定时清日常3')
class cron3(cron): ...

@description('定时清日常4')
class cron4(cron): ...

@description('赛马')
@booltype
@default(True)
class chara_fortune(Module):
    async def do_task(self, client: pcrclient):
        if client.data.cf is None:
            raise SkipError("今日无赛马或已赛马")
        res = await client.draw_chara_fortune()
        result = f"赛马第{client.data.cf.rank}名，获得了宝石x{res.reward_list[0].received}" 
        self.set_result(result)

@description('喂蛋糕')
@booltype
@default(True)
class love_up(Module):
    async def do_task(self, client: pcrclient):
        result = []
        for unit in client.data.unit_love.values():
            unit_id = unit.chara_id * 100 + 1
            unit_name = db.get_inventory_name_san((eInventoryType.Unit, unit_id))
            love_level, total_love = db.max_total_love(client.data.unit[unit_id].unit_rarity)
            if unit.chara_love < total_love:
                dis = total_love - unit.chara_love
                cakes: List[SendGiftData] = []
                for cake_id, cake_value in db.love_cake:
                    current_num = client.data.get_inventory((eInventoryType.Item, cake_id))
                    item_num = min(current_num, (dis + cake_value - 1) // cake_value)
                    dis -= item_num * cake_value
                    use_cake = SendGiftData()
                    use_cake.item_id = cake_id
                    use_cake.item_num = item_num
                    use_cake.current_item_num = current_num
                    cakes.append(use_cake)
                    if dis <= 0: 
                        break
                if dis > 0:
                    result.append(f"{unit_name}: 蛋糕数量不足")
                    break
                await client.multi_give_gift(unit_id, cakes)
                result.append(f"{unit_name}: 亲密度升至{love_level}级")

        if len(result) == 0:
            raise SkipError("所有角色均已亲密度满级")
        msg = '\n'.join(result)
        self.set_result(msg)

@description('免费十连')
@booltype
@default(True)
class free_gacha(Module):
    async def do_task(self, client: pcrclient):
        res = await client.get_gacha_index()
        if res.campaign_info is None:
            raise SkipError("免费十连已结束")
        start_time, end_time, gacha_list = db.campaign_info(res.campaign_info.campaign_id)
        start_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y/%m/%d %H:%M:%S')
        if datetime.datetime.now() >= end_time:
            raise SkipError("免费十连已结束")
        if datetime.datetime.now() < start_time:
            raise SkipError("免费十连尚未开始")
        if res.campaign_info.fg10_exec_cnt == 0:
            raise SkipError("今日份免费十连已使用")
        cnt = res.campaign_info.fg10_exec_cnt
        gacha_id = 0
        exchange_id = 0
        gacha_list = set(gacha_list)
        for gacha_info in res.gacha_info:
            if gacha_info.id in gacha_list:
                gacha_id = gacha_info.id
                exchange_id = gacha_info.exchange_id
                break
        else:
            assert(1==0, f"gacha not found!")
        reward_list = []
        new_unit = []
        while cnt > 0:
            resp = await client.exec_gacha(gacha_id, 10, exchange_id, 6, cnt, res.campaign_info.campaign_id)
            cnt -= 1
            new_unit += [item for item in resp.reward_info_list if item.type == eInventoryType.Unit]
            reward_list += [item for item in resp.reward_info_list if item.type != eInventoryType.Unit]
            # bonues reward TODO
        result = ""
        if len(new_unit) != 0:
            result += f"NEW: \n" + '\n'.join([db.get_inventory_name(item) for item in new_unit]) + '\n'
        result += await client.serlize_reward(reward_list)
        self.set_result(result)

@description('商店购买最大经验药水量')
@enumtype([0, 100, 300, 600, 900, 99999])
@default(0)
class shop_buy_exp_count_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['exp_count_limit'] = self.value

@description('商店购买最大装备量')
@enumtype([0, 100, 300, 600, 900, 9999])
@default(300)
class shop_buy_equip_count_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['equip_count_limit'] = self.value

@description('商店购买最大强化石量')
@enumtype([0, 100, 300, 600, 900, 99999])
@default(0)
class shop_buy_equip_upper_count_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['equip_upper_count_limit'] = self.value

@description('商店购买最大记忆碎片量')
@enumtype([0, 15, 50, 120, 150, 270, 9999])
@default(15)
class shop_buy_unit_memory_count_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['unit_memory_count_limit'] = self.value

class shop_buyer(Module):
    def _get_count(self, client: pcrclient, name: str, key: str):
        if self.value != name and self.value != 'all':
            return 0
        return client.keys.get(key, 0)
    def _exp_count(self, client: pcrclient):
        return self._get_count(client, '经验药水', 'exp_count_limit')
    def _equip_count(self, client: pcrclient):
        return self._get_count(client, '装备', 'equip_count_limit')
    def _equip_upper_count(self, client: pcrclient):
        return self._get_count(client, '强化石', 'equip_upper_count_limit')
    def _unit_memory_count(self, client: pcrclient):
        return self._get_count(client, '记忆碎片', 'unit_memory_count_limit')

    @abstractmethod
    def coin_limit(self) -> int: ...
    @abstractmethod
    def system_id(self) -> eSystemId: ...
    @abstractmethod
    def reset_count_key(self) -> str: ...

    async def _get_shop(self, client: pcrclient):
        res = await client.get_shop_item_list()
        for shop in res.shop_list:
            if shop.system_id == self.system_id().value:
                return shop
        return None

    async def do_task(self, client: pcrclient):
        if self.value == "none":
            raise SkipError('功能未启用')
        lmt = self.coin_limit()
        reset_cnt = client.keys.get(self.reset_count_key(), 0)
        
        shop_content = await self._get_shop(client)

        while True:
            gold = client.data.get_shop_gold(shop_content.system_id)
            if gold < lmt:
                raise SkipError(f"商店货币{gold}不足{lmt}，将不进行购买")

            slots_to_buy = [
                item.slot_id for item in shop_content.item_list if not item.sold and
                    (
                        db.is_exp_upper((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._exp_count(client) or
                        db.is_equip((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._equip_count(client) or
                        db.is_equip_upper((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._equip_upper_count(client) or
                        db.is_unit_memory((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._unit_memory_count(client)
                    )
            ]
            
            if slots_to_buy:
                res = await client.shop_buy_item(shop_content.system_id, slots_to_buy)
                result = await client.serlize_reward(res.purchase_list)
                self._log(result)

            if shop_content.reset_count >= reset_cnt:
                break
            
            await client.shop_reset(shop_content.system_id)
            shop_content = await self._get_shop(client)

@description('通用商店重置次数')
@enumtype([0, 1, 2, 3, 4, 7, 11, 20])
@default(0)
class normal_shop_reset_count(Module):
    async def do_task(self, client: pcrclient):
        client.keys['normal_shop_reset_count'] = self.value

@description('通用商店购买')
@enumtype(["none", "经验药水", "强化石", "all"])
@default("none")
class normal_shop(shop_buyer):
    def coin_limit(self) -> int: return 5000000
    def system_id(self) -> eSystemId: return eSystemId.NORMAL_SHOP
    def reset_count_key(self) -> str: return 'normal_shop_reset_count'

@description('限定商店购买（此项购买不使用最大值）')
@enumtype(["none", "经验药水", "装备", "all"])
@default("none")
class limit_shop(shop_buyer):
    def _exp_count(self, client: pcrclient): return 99999
    def _equip_count(self, client: pcrclient): return 9999
    def coin_limit(self) -> int: return 5000000
    def system_id(self) -> eSystemId: return eSystemId.LIMITED_SHOP
    def reset_count_key(self) -> str: return 'limited_shop_reset_count'
    async def do_task(self, client: pcrclient):
        client.keys['limited_shop_reset_count'] = 0
        await super().do_task(client)

@description('地下城商店重置次数')
@enumtype([0, 1, 2, 3, 4, 7, 11, 20])
@default(0)
class underground_shop_reset_count(Module):
    async def do_task(self, client: pcrclient):
        client.keys['expedition_shop_reset_count'] = self.value

@description('地下城商店购买，记忆碎片+装备')
@enumtype(["none", "记忆碎片", "装备", "all"])
@default("none")
class underground_shop(shop_buyer):
    def coin_limit(self) -> int: return 20000
    def system_id(self) -> eSystemId: return eSystemId.EXPEDITION_SHOP
    def reset_count_key(self) -> str: return 'expedition_shop_reset_count'

@description('jjc商店重置次数')
@enumtype([0, 1, 2, 3, 4, 7, 11, 20])
@default(0)
class jjc_shop_reset_count(Module):
    async def do_task(self, client: pcrclient):
        client.keys['arena_shop_reset_count'] = self.value

@description('jjc商店购买，记忆碎片+装备')
@enumtype(["none", "记忆碎片", "装备", "all"])
@default("none")
class jjc_shop(shop_buyer):
    def coin_limit(self) -> int: return 20000
    def system_id(self) -> eSystemId: return eSystemId.ARENA_SHOP
    def reset_count_key(self) -> str: return 'arena_shop_reset_count'

@description('pjjc商店重置次数')
@enumtype([0, 1, 2, 3, 4, 7, 11, 20])
@default(0)
class pjjc_shop_reset_count(Module):
    async def do_task(self, client: pcrclient):
        client.keys['grand_arena_shop_reset_count'] = self.value

@description('pjjc商店购买，记忆碎片+装备')
@enumtype(["none", "记忆碎片", "装备", "all"])
@default("none")
class pjjc_shop(shop_buyer):
    def coin_limit(self) -> int: return 20000
    def system_id(self) -> eSystemId: return eSystemId.GRAND_ARENA_SHOP
    def reset_count_key(self) -> str: return 'grand_arena_shop_reset_count'

@description('领取任务奖励')
@booltype
@default(True)
class mission_receive(Module):
    async def do_task(self, client: pcrclient):
        resp = await client.mission_index()
        for mission in resp.missions:
            if db.is_daily_mission(mission.mission_id) and mission.mission_status == eMissionStatusType.EnableReceive:
                resp = await client.mission_receive()
                reward = await client.serlize_reward(resp.rewards)
                self.set_result("领取了任务奖励，获得了:\n" + reward)
                return
        raise SkipError("没有可领取的任务奖励")

@description('六星碎片')
@enumtype([0, 3, 6])
@default(3)
class six_star(Module):
    async def do_task(self, client: pcrclient):
        result: List[str] = []
        is_error = False
        is_abort = False
        times = int(self.value)
        for quest_id, (pure_memory, unit_id) in db.six_area.items():
            data = client.data.unit[unit_id]
            if data.unit_rarity != 6 and data.unlock_rarity6_item and not data.unlock_rarity6_item.status1 and client.data.get_inventory((eInventoryType.Item, pure_memory)) < 50:
                # unlock_rarity6_item有时候明明有数据，但服务端返回了null
                try:
                    rewards = await client.quest_skip_aware(quest_id, times, True, True)
                    msg = await client.serlize_reward(rewards, (eInventoryType.Item, pure_memory))
                    result.append(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {msg}")
                except SkipError as e:
                    result.append(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                except AbortError as e:
                    is_abort = True
                    result.append(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                    break
                except Exception as e:
                    is_error = True
                    result.append(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                    break
            else:
                pass
                # result.append(f"{quest_id}: 材料已够，无需刷取")
        msg = '\n'.join(result)
        if is_error: raise ValueError(msg)
        if is_abort: raise AbortError(msg)
        if len(result) == 0:
            raise SkipError("六星碎片均已足够，无需刷取")
        self.set_result(msg)

@description('最高级地下城扫荡')
@booltype
@default(True)
class underground_skip(Module):
    async def do_task(self, client: pcrclient):
        infos = await client.get_dungeon_info()
        result = ""
        rest = infos.rest_challenge_count[0].count
        if infos.enter_area_id != 0:
            dungeon_name = db.dungeon_name[infos.enter_area_id]
            raise AbortError(f"当前以位于{dungeon_name}，将不进行扫荡")
        
        if rest:
            id = max([0] + infos.dungeon_cleared_area_id_list)
            if id > 0:
                reward_list = await client.skip_dungeon(id)
                # rewards = []
                # for reward in reward_list.skip_result_list:
                #     rewards += reward.reward_list
                # result = await client.serlize_reward(rewards)
                dungeon_name = db.dungeon_name[id]
                self.set_result(f"扫荡了【{dungeon_name}】")
                # self.set_result(f"扫荡了{dungeon_name}，获得了：\n{result}")
            else:
                raise AbortError("不存在已完成讨伐的地下城")
        else:
            raise SkipError("今日已扫荡地下城")

@description('基本信息')
@booltype
@default(True)
class user_info(Module):
    async def do_task(self, client: pcrclient):
        now = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        result = f"{client.data.name} 体力{client.data.stamina}({db.team_max_stamina[client.data.team_level]}) 等级{client.data.team_level} 钻石{client.data.jewel.free_jewel} mana{client.data.gold.gold_id_free} 扫荡券{client.data.get_inventory((eInventoryType.Item, 23001))} 母猪石{client.data.get_inventory((eInventoryType.Item, 90005))}\n清日常时间:{now}"
        self.set_result(result)

@description('阅读角色剧情')
@enumtype(["none", "除ue普妈圣千普千真步", "all"])
@default("none")
class unit_story_reading(Module):
    async def do_task(self, client: pcrclient):
        if self.value is None or self.value == "none":
            raise SkipError("功能未启用")
        ignore = True if self.value != "all" else False
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        result = []
        ignore_chara_id = set([
            1002, # ue
            1010, # 真步
            1042, # 千歌
            1059, # 普妈
            1084, # 圣千
        ])
        for story_id, pre_story_id, chara_id, love_level, title in db.unit_story:
            if ignore and chara_id in ignore_chara_id:
                continue
            if story_id not in read_story and pre_story_id in read_story and chara_id in client.data.unit_love and client.data.unit_love[chara_id].love_level >= love_level:
                await client.read_story(story_id)
                result.append(title)
                read_story.add(story_id)
        if len(result) == 0:
            raise SkipError("不存在未阅读的角色剧情")
        client.data.read_story_ids = list(read_story)
        msg = f"阅读了{len(result)}篇：" + '|'.join(result) 
        self.set_result(msg)

@description('阅读主线剧情')
@booltype
@default(True)
class main_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        result = []
        msg = ""
        for story_id, pre_story_id, unlock_quest_id, title in db.main_story:
            if story_id not in read_story and pre_story_id in read_story:
                if not await client.unlock_quest_id(unlock_quest_id):
                    msg = f"区域{str(unlock_quest_id)}未通关，无法观看{title}\n"
                    break
                await client.read_story(story_id)
                result.append(title)
                read_story.add(story_id)
        client.data.read_story_ids = list(read_story)
        if msg != "":
            if len(result) != 0:
                raise AbortError("已阅读" + '|'.join(result) + "，但" + msg)
            else:
                raise AbortError(msg)
        if len(result) == 0:
            raise SkipError("不存在未阅读的主线剧情")
        msg = f"阅读了{len(result)}篇：" + '|'.join(result) 
        self.set_result(msg)

@description('阅读露娜塔剧情')
@booltype
@default(True)
class tower_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        result = []
        msg = ""
        for story_id, pre_story_id, unlock_quest_id, title, start_time in db.tower_story:
            now = datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
            if now < start_time:
                continue
            if story_id not in read_story and pre_story_id in read_story:
                if not await client.unlock_quest_id(unlock_quest_id):
                    msg = f"层数{db.tower2floor[unlock_quest_id]}未通关，无法观看{title}\n"
                    break
                await client.read_story(story_id)
                result.append(title)
                read_story.add(story_id)
        client.data.read_story_ids = list(read_story)
        if msg != "":
            if len(result) != 0:
                raise AbortError("已阅读" + '|'.join(result) + "，但" + msg)
            else:
                raise AbortError(msg)
        if len(result) == 0:
            raise SkipError("不存在未阅读的露娜塔剧情")
        msg = f"阅读了{len(result)}篇：" + '|'.join(result) 
        self.set_result(msg)

@description('阅读活动剧情')
@booltype
@default(True)
class hatsune_story_reading(Module):
    async def do_task(self, client: pcrclient):
        result = []
        read_story = set(client.data.read_story_ids)
        for story_id, pre_story_id, title in db.event_story:
            if story_id not in read_story and pre_story_id in read_story:
                await client.read_story(story_id)
                result.append(title)
                read_story.add(story_id)
        if len(result) == 0:
            raise SkipError("不存在未阅读的活动剧情")
        client.data.read_story_ids = list(read_story)
        msg = f"阅读了{len(result)}篇：" + '|'.join(result) 
        self.set_result(msg)

@description('阅读活动信赖度')
@booltype
@default(True)
class hatsune_dear_reading(Module):
    async def do_task(self, client: pcrclient):
        result = []
        event_active = False
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            event_active = True
            resp = (await client.get_hatsune_top(event.event_id))
            if resp.unchoiced_dear_story_id_list == None:
                continue
            resp = (await client.get_hatsune_dear_top(event.event_id))
            for story in resp.unlock_dear_story_info_list:
                if not story.is_choiced:
                    result.append(f"{story.story_id}")
                    await client.read_dear(event.event_id, story.story_id)
        if not event_active:
            raise SkipError("当前无进行中的活动")
        if len(result) == 0:
            raise SkipError("不存在未阅读的活动信赖度剧情")
        msg = "阅读了" + ' '.join(result) 
        self.set_result(msg)

@description('讨伐证交换')
@enumtype(["none", "前两轮重置", "all"])
@default("none")
class hatsune_gacha_exchange(Module):
    async def do_task(self, client: pcrclient):
        if self.value is None or self.value == "none":
            raise SkipError("功能未启用")
        early_stop = False if self.value == "all" else True
        event_active = False
        result = []
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            event_active = True
            res = (await client.get_hatsune_top(event.event_id))
            exchange_ticket_id = db.hatsune_item[event.event_id][1]
            res = (await client.get_hatsune_gacha_index(event.event_id, event.event_id))
            box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
            ticket = client.data.get_inventory((eInventoryType.Item, exchange_ticket_id))
            while(True):
                if ticket == 0:
                    break
                if res.event_gacha_info.gacha_step >= 6:
                    exchange_times = min(client.data.settings.loop_box_multi_gacha_count, ticket)
                    await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 1)
                    ticket -= exchange_times
                else:
                    target_done = len([item.reward_id for item in box_item.values() if item.reset_target and item.remain_inbox_count]) == 0
                    remain_cnt = sum(item.remain_inbox_count for item in box_item.values())
                    if remain_cnt == 0 or (target_done and res.event_gacha_info.gacha_step <= 2 and early_stop):
                        res = await client.reset_hatsune_gacha(event.event_id, event.event_id)
                        box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
                        continue
                    exchange_times = min(100, ticket, remain_cnt)
                    resp = await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 0)
                    ticket -= exchange_times
                    for item in resp.draw_result:
                        box_item[item.box_set_id].remain_inbox_count -= item.hit_reward_count
            result.append(f"{event.event_id}: 已交换至第{res.event_gacha_info.gacha_step}轮")
            
        if not event_active:
            raise SkipError("当前无进行中的活动")
        msg = '\n'.join(result)
        self.set_result(msg)

@description('在公会中自动随机选择一位成员点赞。')
@booltype
@default(True)
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        if client.data.clan_like_count:
            raise SkipError('今日点赞次数已用完。')
        info = await client.get_clan_info()
        members = [(x.viewer_id, x.name) for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise AbortError("No other members in clan")
        rnd = random.choice(members)
        await client.clan_like(rnd[0])
        self.set_result(f"为【{rnd[1]}】点赞")

@description('活动h本')
@enumtype(["none", "odd", "even", "all"])
@default("none")
class hatsune_h_sweep(Module):
    async def do_task(self, client: pcrclient):
        result: List[str] = []
        area = []
        hard = 200
        is_error = False
        is_abort = False
        is_skip = True
        if self.value == "none":
            raise SkipError("功能未启用")
        if self.value == "odd":
            area = [1, 3, 5]
        elif self.value == "even":
            area = [2, 4]
        elif self.value == "all":
            area = [1, 2, 3, 4, 5]
        event_active = False
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2: # 不知道其他类型的是什么
                continue
            event_active = True
            await client.get_hatsune_top(event.event_id)
            await client.get_hatsune_quest_top(event.event_id)
            for i in area:
                quest_id = event.event_id * 1000 + hard + i
                try: 
                    times = 3 - client.data.hatsune_quest_dict[event.event_id][quest_id].daily_clear_count
                    await client.hatsune_quest_skip_aware(event.event_id, quest_id, 3, False, True)
                    is_skip = False
                    result.append(f"{quest_id}: 扫荡{times}次")
                except SkipError as e:
                    result.append(f"{quest_id}: {str(e)}")
                except AbortError as e:
                    is_abort = True
                    result.append(f"{quest_id}: {str(e)}")
                    break
                except Exception as e: 
                    is_error = True
                    result.append(f"{quest_id}: {str(e)}")
                    break
        if not event_active: raise SkipError("当前无进行中的活动")
        msg = '\n'.join(result)
        if is_error: raise ValueError(msg)
        if is_abort: raise AbortError(msg)
        if is_skip: raise SkipError(msg)
        self.set_result(msg)

@description('领取活动任务奖励')
@booltype
@default(True)
class hatsune_mission_accept(Module):
    async def do_task(self, client: pcrclient):
        result: List[str] = []
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            event_active = True
            await client.get_hatsune_top(event.event_id)
            resp = await client.hatsune_mission_index(event.event_id)
            types = set(x.mission_id // 10000000 - 5 for x in resp.missions if x.mission_status == eMissionStatusType.EnableReceive)
            try:
                if not types:
                    raise SkipError("没有可领取的任务奖励")
                else:
                    is_skip = False
                    for type in types:
                        res = await client.hatsune_mission_receive(event.event_id, type)
                        reward = await client.serlize_reward(res.rewards)
                        result.append(f"{event.event_id}: 领取了任务奖励，获得了:\n" + reward)
            except SkipError as e:
                result.append(f"{event.event_id}: {str(e)}")
            except AbortError as e:
                is_abort = True
                result.append(f"{event.event_id}: {str(e)}")
            except Exception as e:
                is_error = True
                result.append(f"{event.event_id}: {str(e)}")

        if not event_active: raise SkipError("当前无进行中的活动")
        msg = '\n'.join(result)
        if is_error: raise ValueError(msg)
        if is_abort: raise AbortError(msg)
        if is_skip: raise SkipError(msg)
        self.set_result(msg)

@description('活动h本boss')
@enumtype(["none", "max", "max - 1"])
@default("none")
class hatsune_hboss_sweep(Module):
    async def do_task(self, client: pcrclient):
        result: List[str] = []
        is_error = False
        is_abort = False
        is_skip = True
        if self.value == "none":
            raise SkipError("功能未启用")
        event_active = False
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            event_active = True
            resp = await client.get_hatsune_top(event.event_id)
            ticket = resp.boss_ticket_info.stock
            if self.value == "max":
                times = ticket // 30
            elif self.value == "max - 1":
                times = ticket // 30 - 1
            else:
                raise ValueError(f"Unknown option: {self.value}")
            boss_id = event.event_id * 100 + 2
            try: 
                for boss_battle_info in resp.boss_battle_info:
                    if boss_battle_info.boss_id == boss_id and not boss_battle_info.is_unlocked:
                        raise AbortError(f"h本boss未解锁")
                if times <= 0:
                    raise SkipError(f"boss券不足 {ticket}")
                is_skip = False
                resp = await client.hatsune_boss_skip(event.event_id, boss_id, times, ticket)
                result.append(f"{event.event_id} h boss: 扫荡{times}次")
            except SkipError as e:
                result.append(f"{event.event_id}: {str(e)}")
            except AbortError as e:
                is_abort = True
                result.append(f"{event.event_id}: {str(e)}")
            except Exception as e: 
                is_error = True
                result.append(f"{event.event_id}: {str(e)}")
        if not event_active:
            raise SkipError("当前无进行中的活动")
        msg = '\n'.join(result)
        if is_error: raise ValueError(msg)
        if is_abort: raise AbortError(msg)
        if is_skip: raise SkipError(msg)
        self.set_result(msg)

@description('使用体力时，若体力不足，最多允许购买的体力管数。')
@enumtype([0, 1, 2, 3, 6, 9, 12])
@default(0)
class buy_stamina_passive(Module):
    async def do_task(self, client: pcrclient):
        client.keys['buy_stamina_passive'] = self.value
     
@description('每天主动购买的体力管数。钻石数量<1w强制不触发。')
@enumtype([0, 1, 2, 3, 6, 9, 12])
@default(0)
class buy_stamina_active(Module):
    async def do_task(self, client: pcrclient):
        cnt = 0
        for _ in range(self.value):
            if client.data.jewel.free_jewel < 10000:
                raise AbortError('钻石数量不足。中止购买体力。')
            if client.data.stamina + 120 > 999:
                raise AbortError('体力恢复将超过999。中止购买体力')
            await client.recover_stamina()
            cnt += 1
        self.set_result(f"购买了{str(cnt)}次体力")

@description('收取家园体')
@booltype
@default(True)
class room_accept_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        t = client.data.stamina
        for x in room.user_room_item_list:
            if x.item_count:
                res = await client.room_accept_all()
                result = await client.serlize_reward(res.reward_list)
                self.set_result(result)
                return
        self._log(f'收取家园体力：{t} => {client.data.stamina}')
        raise SkipError('没有可收取的家园物品。')

@description('升级家园家具')
@booltype
@default(True)
class room_upper_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        floors = {}
        cnt = 0
        for layout in room.room_layout.floor_layout:
            cnt += 1
            for item in layout.floor:
                floors[item.serial_id] = cnt

        result = []
        for x in room.user_room_item_list:
            if db.is_room_item_level_upable(client.data.team_level, x):
                await client.room_level_up_item(floors[x.serial_id], x)
                result.append(f"升级{db.get_inventory_name_san((eInventoryType.RoomItem, x.room_item_id))}至{x.room_item_level + 1}级")

        if len(result) == 0:
            raise SkipError('没有可升级的家园物品。')
        result = '\n'.join(result)
        self.set_result(result)

@description('公会小屋点赞，先回赞，再随机点赞')
@booltype
@default(True)
class room_like_back(Module):
    async def do_task(self, client: pcrclient):
        await client.room_start()
        result = []
        like_user = []
        like_history = await client.room_like_history()
        cnt = like_history.today_like_count
        pos = 0
        if cnt >= 10:
            raise SkipError(f"今日已点赞{cnt}次")
        while pos < like_history.today_be_liked_count or cnt < 10:
            viewer_id = 0
            if pos < like_history.today_be_liked_count:
                viewer_id = like_history.like_history[pos].viewer_id
            user = await client.room_visit(viewer_id)
            pos += 1
            if user.room_user_info.today_like_flag:
                continue
            resp = await client.room_like(user.room_user_info.viewer_id)
            result += resp.reward_list
            like_user.append(user.room_user_info.name)
            cnt += 1

        result = await client.serlize_reward(result)
        msg = f"为【{'|'.join(like_user)}】点赞，获得了:\n" + result
        self.set_result(msg)

@description('EXP探索')
@booltype
@default(True)
class explore_exp(Module):
    async def do_task(self, client: pcrclient):
        # 11级探索
        exp_quest_remain = client.data.training_quest_max_count.exp_quest - client.data.training_quest_count.exp_quest
        result: str = ""
        if exp_quest_remain:
            await client.training_quest_skip(21002011, exp_quest_remain)
            result = f"11级exp探索扫荡{exp_quest_remain}次"
        else:
            raise SkipError("11级exp探索已扫荡")
        self.set_result(result)

@description('普通扭蛋')
@booltype
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
        result = "全是装备"
        if memory:
            result = await client.serlize_reward(memory)
        self.set_result(result)

@description('MANA探索')
@booltype
@default(True)
class explore_mana(Module):
    async def do_task(self, client: pcrclient):
        # 11级探索
        gold_quest_remain = client.data.training_quest_max_count.gold_quest - client.data.training_quest_count.gold_quest
        result: List[str] = []
        if gold_quest_remain:
            await client.training_quest_skip(21001011, gold_quest_remain)
            result.append(f"11级mana探索扫荡{gold_quest_remain}次")
        else:
            raise SkipError("11级mana探索已扫荡")
        msg = ' '.join(result)
        self.set_result(msg)

@description('露娜塔回廊扫荡')
@booltype
@default(True)
class tower_cloister_sweep(Module):
    async def do_task(self, client: pcrclient):
        now = datetime.datetime.now()
        tower_id = client.data.tower_status.last_login_schedule_id
        start_time, end_time = db.tower[tower_id]
        start_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y/%m/%d %H:%M:%S')
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
            msg = await client.serlize_reward(result, db.xinsui)
            self.set_result(f"扫荡了{times}次，获得了:\n" + msg)
        else:
            raise SkipError("回廊已扫荡")

@description('领取礼物箱')
@enumtype(["none", "非体力", "all"])
@default("非体力")
class present_receive(Module):
    async def do_task(self, client: pcrclient):
        if self.value == "none":
            raise SkipError("功能未启用")
        elif self.value == "非体力":
            is_exclude_stamina = True
            op = "领取了非体力物品：\n"
        elif self.value == "all":
            is_exclude_stamina = False
            op = "领取了所有物品：\n"
        else:
            raise ValueError(f"Unknown option: {self.value}")
        received = False
        result = []
        while True:
            present = await client.present_index()
            for present in present.present_info_list:
                if not (present.reward_type == eInventoryType.Stamina and present.reward_id == 93001):
                    res = await client.present_receive_all(is_exclude_stamina)
                    result += res.rewards
                    received = True
                    break
            else:
                break

        if not received:
            raise SkipError(f"不存在未领取{'的非体力的' if is_exclude_stamina == True else '的'}礼物")
        msg = await client.serlize_reward(result)
        self.set_result(op + msg)
        self._log('礼物已领取完成')

@description('领取双场币')
@booltype
@default(True)
class jjc_reward(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_arena_info()
        result: List[str] = []
        if info.reward_info.count:
            await client.receive_arena_reward()
        result.append(f"jjc币x{info.reward_info.count}")
        info = await client.get_grand_arena_info()
        if info.reward_info.count:
            await client.receive_grand_arena_reward()
        result.append(f"pjjc币x{info.reward_info.count}")
        msg = ' '.join(result)
        self.set_result(msg)

@description('刷取心碎3')
@booltype
@default(True)
class xinsui3_sweep(Module):
    async def do_task(self, client: pcrclient):
        result = await client.quest_skip_aware(18001003, 5)
        msg = await client.serlize_reward(result, db.xinsui)
        self.set_result(msg)
        self._log('心碎3已刷取完成')

@description('刷取心碎2')
@booltype
@default(True)
class xinsui2_sweep(Module):
    async def do_task(self, client: pcrclient):
        result = await client.quest_skip_aware(18001002, 5)
        msg = await client.serlize_reward(result, db.xinsui)
        self.set_result(msg)
        self._log('心碎2已刷取完成')

@description('刷取心碎1')
@booltype
@default(True)
class xinsui1_sweep(Module):
    async def do_task(self, client: pcrclient):
        result = await client.quest_skip_aware(18001001, 5)
        msg = await client.serlize_reward(result, db.xinsui)
        self.set_result(msg)
        self._log('心碎1已刷取完成')

@description('刷取星球杯2')
@booltype
@default(True)
class xingqiubei2_sweep(Module):
    async def do_task(self, client: pcrclient):
        result = await client.quest_skip_aware(19001002, 5)
        msg = await client.serlize_reward(result, db.xingqiubei)
        self.set_result(msg)
        self._log('星球杯2已刷取完成')

@description('刷取星球杯1')
@booltype
@default(True)
class xingqiubei1_sweep(Module):
    async def do_task(self, client: pcrclient):
        result = await client.quest_skip_aware(19001001, 5)
        msg = await client.serlize_reward(result, db.xingqiubei)
        self.set_result(msg)
        self._log('星球杯1已刷取完成')

@description('''
首先按次数逐一刷取名字为start的图
然后循环按次数刷取设置为loop的图
当被动体力回复完全消耗后，刷图结束
'''.strip())
@booltype
@default(True)
class smart_sweep(Module):
    async def do_task(self, client: pcrclient):
        nloop = []
        loop = []
        for tab in client.data.user_my_quest:
            for x in tab.skip_list:
                if tab.tab_name == 'start':
                    nloop.append((x, tab.skip_count))
                elif tab.tab_name == 'loop':
                    loop.append((x, tab.skip_count))
        def _sweep():
            for x in nloop:
                yield x
            if loop:
                while True:
                    for x in loop:
                        yield x

        msg = []
        result = []
        if nloop == [] and loop == []:
            raise AbortError("未找到start和loop")
        for quest_id, count in _sweep(): # loop 全是hard very hard时会死循环
            try:
                result += await client.quest_skip_aware(quest_id, count, True, True)
            except SkipError as e:
                m = str(e)
                if m.endswith('体力不足'): 
                    break
            except AbortError as e:
                m = str(e)
                msg.append(m)
                if not m.endswith("已达最大次数"):
                    raise AbortError('\n'.join(msg))
        
        msg = await client.serlize_reward(result)
        self.set_result(msg)

'''
class shop_buy(Module):
    @abstractmethod
    def system_id(self) -> int: ...
    @abstractmethod
    def coin_limit(self) -> int: ...

    async def _get_shop_content(self, client: pcrclient):
        for shop in (await client.get_shop_item_list()).shop_list:
            if shop.system_id == self.system_id():
                return shop
        raise AbortError("商店未开启")

    async def do_task(self, client: pcrclient):
        shop_content = await self._get_shop_content(client)

        prev = client.data.get_shop_gold(self.system_id())
        
        buy_limit = client.keys.get('shop_buy_limit', 300)

        while shop_content.reset_count <= self.value:
            
            if client.data.get_shop_gold(self.system_id()) < self.coin_limit():
                raise AbortError(f"商店金币小于{self.coin_limit()}，无法继续购买")

            slots_to_buy = [
                item.slot_id for item in shop_content.item_list if 
                    item.available_num and 
                    client.data.get_inventory((item.type, item.item_id)) < buy_limit and 
                    not item.sold
            ]
            
            if slots_to_buy:
                await client.shop_buy_item(shop_content.system_id, slots_to_buy)

            if shop_content.reset_count == self.value:
                break
            
            await client.shop_reset(shop_content.system_id)
            shop_content = await self._get_shop_content(client)

        self._log(f"已花费{prev - client.data.get_shop_gold(self.system_id())}代币购买装备")

@description('购买地下城币刷新次数, -1为不购买')
@enumtype([-1, 0, 1, 2, 3, 4, 7, 10])
@default(0)
class dungeon_shop(shop_buy):
    def system_id(self) -> int:
        return 204
    def coin_limit(self) -> int:
        return 100000

@description('购买jjc币刷新次数, -1为不购买')
@enumtype([-1, 0, 1, 2, 3, 4, 7, 10])
@default(0)
class new_jjc_shop(shop_buy):
    def system_id(self) -> int:
        return 202
    def coin_limit(self) -> int:
        return 30000

@description('购买pjjc币刷新次数, -1为不购买')
@enumtype([-1, 0, 1, 2, 3, 4, 7, 10])
@default(0)
class new_pjjc_shop(shop_buy):
    def system_id(self) -> int:
        return 203
    def coin_limit(self) -> int:
        return 30000

@description('购买限时商店')
@booltype
@default(True)
class new_daily_shop(Module):
    async def do_task(self, client: pcrclient):
        items_to_buy = [x.slot_id for x in client.data.daily_shop.item_list if x.available_num]
        if not items_to_buy:
            raise SkipError(f"限时商店已购买")
        await client.shop_buy_item(client.data.daily_shop.system_id, items_to_buy)
        self._log(f"已购买限时商店")
'''

@description('剩余体力全部刷活动图')
@enumtype(['disabled', 'n-5', 'n-10', 'n-15'])
@default('disabled')
class all_in_hatsune(Module):
    async def do_task(self, client: pcrclient):
        if self.value == 'disabled':
            return
        quest = event_id = 0
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            if self.value == 'n-5':
                quest = 1000 * event.event_id + 105
            elif self.value == 'n-10':
                quest = 1000 * event.event_id + 110
            elif self.value == 'n-15':
                quest = 1000 * event.event_id + 115
            event_id = event.event_id
            
            break
        
        if not quest: raise AbortError("未找到活动")

        count = client.data.stamina // 10

        if count == 0: raise AbortError("体力不足")
        await client.hatsune_quest_skip_aware(event_id, quest, count)
        self._log(f"已刷{quest}图{count}次")

def register_test():
    ModuleManager._modules = [
        buy_stamina_passive,
        smart_sweep
    ]

def register_all():
    ModuleManager._modules = [
        chara_fortune,
        mission_receive,
        buy_stamina_passive,
        clan_like,
        room_like_back,
        free_gacha,
        normal_gacha,
        room_accept_all,
        explore_exp,
        explore_mana,
        underground_skip,
        tower_cloister_sweep,
        six_star,
        jjc_reward,
        xinsui3_sweep,
        xinsui2_sweep,
        xinsui1_sweep,
        xingqiubei2_sweep,
        xingqiubei1_sweep, 
        hatsune_dear_reading,
        hatsune_h_sweep,
        present_receive,
        hatsune_hboss_sweep,
        hatsune_mission_accept,
        hatsune_gacha_exchange,
        hatsune_mission_accept,
        smart_sweep,

        buy_stamina_active,
        all_in_hatsune,

        mission_receive,

        shop_buy_exp_count_limit,
        shop_buy_equip_count_limit,
        shop_buy_equip_upper_count_limit,
        shop_buy_unit_memory_count_limit,

        normal_shop_reset_count,
        normal_shop,
        limit_shop,
        underground_shop_reset_count,
        underground_shop,
        jjc_shop_reset_count,
        jjc_shop,
        pjjc_shop_reset_count,
        pjjc_shop,
        
        love_up,
        main_story_reading,
        tower_story_reading,
        hatsune_story_reading,
        unit_story_reading,
        room_upper_all,
        user_info,
    ]
