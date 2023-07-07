from ..core import pcrclient
from ..model.models import *
from .modulebase import *

import datetime
from ..model.error import *
from ..db.database import db
from ..db.models import *
from ..model.models import *
import random
from abc import abstractmethod
from collections import Counter

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


@description('智能刷n图考虑的角色')
@enumtype(['all', 'max_rank', 'max_rank-1', 'max_rank-2', 'favorite'])
@default('all')
class smart_normal_sweep_unit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['smart_normal_sweep_unit'] = self.value

@description('智能刷n图')
@enumtype(["none", "n庆典", "always"])
@default("none")
class smart_normal_sweep(Module):

    async def do_task(self, client: pcrclient):
        if self.value == "n庆典" and not client.data.is_normal_quest_double():
            raise SkipError("今日非normal庆典，不刷取")

        if client.keys['smart_normal_sweep_unit'] == 'favorite':
            _, require_equip = client.data.get_need_equip(like_unit_only = True)
        else:
            opt = {
                'all': 1,
                'max_rank': db.equip_max_rank,
                'max_rank-1': db.equip_max_rank - 1,
                'max_rank-2': db.equip_max_rank - 2,
            }
            _, require_equip = client.data.get_need_equip(start_rank = opt[client.keys['smart_normal_sweep_unit']])

        clean_cnt = Counter()
        quest_id = []
        tmp = []
        quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= datetime.datetime.now()]
        stop: bool = False

        try:
            for i in range(10000):

                if i % 3 == 0:
                    quest_weight = client.data.get_quest_weght(require_equip)
                    quest_id = sorted(quest_list, key = lambda x: quest_weight[x][0], reverse = True)

                target_id = quest_id[0]
                try:
                    tmp.extend(await client.quest_skip_aware(target_id, 3))
                    clean_cnt[target_id] += 3
                except SkipError:
                    pass
                except AbortError as e:
                    stop = True
                    if str(e).endswith("体力不足"):
                        if not tmp and not self.log: self._log(str(e))
                    else:
                        raise e
                    break
                if stop:
                    break
        except:
            raise 
        finally:
            if tmp:
                self._log(await client.serlize_reward(tmp))
            if clean_cnt:
                msg = '\n'.join((db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}") +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)


@description('智能刷hard图')
@enumtype(["none", "h庆典", "非n庆典", "always"])
@default("none")
class smart_hard_sweep(Module):
    async def do_task(self, client: pcrclient):
        if self.value == "h庆典" and not client.data.is_hard_quest_double():
            raise SkipError("今日非hard庆典，不刷取")
        if self.value == "非n庆典" and client.data.is_normal_quest_double():
            raise SkipError("今日normal庆典，不刷取")

        need_list, _ = client.data.get_need_memory()
        need_list = [(token, need - client.data.get_inventory(token)) for token, need in need_list if need > client.data.get_inventory(token)]

        if not need_list:
            raise SkipError("不存在缺乏的记忆碎片")

        need_list = sorted(need_list, key=lambda x: x[1])
        stop = False
        for token, _ in need_list:
            if token[1] not in db.memory_quest:
                continue
            tmp = []
            for quest in db.memory_quest[token[1]]:
                max_times = 5 if db.is_shiori_quest(quest.quest_id) else 3
                try:
                    resp = await client.quest_skip_aware(quest.quest_id, max_times)
                    tmp += resp
                except SkipError:
                    pass
                except AbortError as e:
                    stop = True
                    if str(e).endswith("体力不足"):
                        if not tmp and not self.log: self._log(str(e))
                    else:
                        if tmp: self._log(await client.serlize_reward(tmp, token))
                        raise e
                    break
            if tmp:
                self._log(await client.serlize_reward(tmp, token))
            if stop:
                break

@description('赛马')
@booltype
@default(True)
class chara_fortune(Module):
    async def do_task(self, client: pcrclient):
        if not db.is_cf_time():
            raise SkipError("今日无赛马")
        if client.data.cf is None:
            raise SkipError("今日已赛马")
        res = await client.draw_chara_fortune()
        self._log(f"赛马第{client.data.cf.rank}名，获得了宝石x{res.reward_list[0].received}")

@description('喂蛋糕')
@booltype
@default(True)
class love_up(Module):
    async def do_task(self, client: pcrclient):
        for unit in client.data.unit_love.values():
            unit_id = unit.chara_id * 100 + 1
            unit_name = db.get_inventory_name_san((eInventoryType.Unit, unit_id))
            love_level, total_love = db.max_total_love(client.data.unit[unit_id].unit_rarity)
            if unit.chara_love < total_love:
                dis = total_love - unit.chara_love
                cakes: List[SendGiftData] = []
                for cake in db.love_cake:
                    current_num = client.data.get_inventory((eInventoryType.Item, cake.item_id))
                    if not current_num:
                        continue
                    item_num = min(current_num, (dis + cake.value - 1) // cake.value)
                    dis -= item_num * cake.value
                    use_cake = SendGiftData()
                    use_cake.item_id = cake.item_id
                    use_cake.item_num = item_num
                    use_cake.current_item_num = current_num
                    cakes.append(use_cake)
                    if dis <= 0: 
                        break
                if dis > 0:
                    self._log(f"{unit_name}: 蛋糕数量不足")
                    break
                await client.multi_give_gift(unit_id, cakes)
                self._log(f"{unit_name}: 亲密度升至{love_level}级")

        if not self.log:
            raise SkipError("所有角色均已亲密度满级")

@description('免费十连')
@booltype
@default(True)
class free_gacha(Module):
    async def do_task(self, client: pcrclient):
        res = await client.get_gacha_index()
        if res.campaign_info is None:
            raise SkipError("免费十连已结束")
        schedule = db.campaign_gacha[res.campaign_info.campaign_id]
        gacha_list = db.gacha_list[schedule.campaign_id]
        start_time = db.parse_time(schedule.start_time)
        end_time = db.parse_time(schedule.end_time)
        if datetime.datetime.now() >= end_time:
            raise SkipError("免费十连已结束")
        if datetime.datetime.now() < start_time:
            raise SkipError("免费十连尚未开始")
        if res.campaign_info.fg10_exec_cnt == 0:
            raise SkipError("今日份免费十连已使用")
        cnt = res.campaign_info.fg10_exec_cnt
        gacha_id = 0
        exchange_id = 0
        gacha_list = set(gacha.gacha_id for gacha in gacha_list)
        for gacha_info in res.gacha_info:
            if gacha_info.id in gacha_list:
                gacha_id = gacha_info.id
                exchange_id = gacha_info.exchange_id
                break
        else:
            raise ValueError("target gacha not found")
        reward_list = []
        new_unit = []
        while cnt > 0:
            resp = await client.exec_gacha(gacha_id, 10, exchange_id, 6, cnt, res.campaign_info.campaign_id)
            cnt -= 1
            new_unit += [item for item in resp.reward_info_list if item.type == eInventoryType.Unit]
            reward_list += [item for item in resp.reward_info_list if item.type != eInventoryType.Unit]
            # bonues reward TODO
        if new_unit:
            self._log(f"NEW: \n" + '\n'.join([db.get_inventory_name(item) for item in new_unit]) + '\n')
        self._log(await client.serlize_reward(reward_list))

@description('商店购买最大经验药水量')
@enumtype([0, 1000, 5000, 20000, 50000, 99999])
@default(0)
class shop_buy_exp_count_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['exp_count_limit'] = self.value

@description('商店购买最大装备量')
@enumtype([0, 100, 300, 600, 1000, 9999])
@default(300)
class shop_buy_equip_count_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['equip_count_limit'] = self.value

@description('商店购买最大强化石量')
@enumtype([0, 100, 500, 2000, 5000, 99999])
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
        raise SkipError("商店未开启")

    async def do_task(self, client: pcrclient):
        lmt = self.coin_limit()
        reset_cnt = client.keys.get(self.reset_count_key(), 0)

        shop_content = await self._get_shop(client)

        prev = client.data.get_shop_gold(shop_content.system_id)
        old_reset_cnt = shop_content.reset_count
        result = []

        while True:
            gold = client.data.get_shop_gold(shop_content.system_id)
            if gold < lmt:
                raise SkipError(f"商店货币{gold}不足{lmt}，将不进行购买")

            target = [
                (item.slot_id, item.price.currency_num) for item in shop_content.item_list if not item.sold and
                    (
                        db.is_exp_upper((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._exp_count(client) or
                        db.is_equip((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._equip_count(client) or
                        db.is_equip_upper((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._equip_upper_count(client) or
                        db.is_unit_memory((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._unit_memory_count(client)
                    )
            ]

            slots_to_buy = [item[0] for item in target]
            cost_gold = sum([item[1] for item in target])

            if cost_gold > gold: # 货币不足
                break
            
            if slots_to_buy:
                res = await client.shop_buy_item(shop_content.system_id, slots_to_buy)
                result.extend(res.purchase_list)

            if shop_content.reset_count >= reset_cnt:
                break
            
            await client.shop_reset(shop_content.system_id)
            shop_content = await self._get_shop(client)

        cost_gold = prev - client.data.get_shop_gold(shop_content.system_id)
        if cost_gold == 0:
            raise SkipError("无对应商品购买")
        else:
            self._log(f"花费了{cost_gold}货币，重置了{shop_content.reset_count - old_reset_cnt}次，购买了:")
            msg = await client.serlize_reward(result)
            self._log(msg)

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
    def _exp_count(self, client: pcrclient): return 99999 if self.value == "经验药水" or self.value == "all" else 0
    def _equip_count(self, client: pcrclient): return 9999 if self.value == "装备" or self.value == "all" else 0
    def coin_limit(self) -> int: return 5000000
    def system_id(self) -> eSystemId: return eSystemId.LIMITED_SHOP
    def reset_count_key(self) -> str: return 'limited_shop_reset_count'
    async def do_task(self, client: pcrclient):
        client.keys['limited_shop_reset_count'] = 0
        return await super().do_task(client)

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

@description('开始时领取任务奖励')
@booltype
@default(True)
class mission_receive_first(Module):
    async def do_task(self, client: pcrclient):
        resp = await client.mission_index()
        for mission in resp.missions:
            if db.is_daily_mission(mission.mission_id) and mission.mission_status == eMissionStatusType.EnableReceive:
                resp = await client.mission_receive()
                reward = await client.serlize_reward(resp.rewards)
                self._log("领取了任务奖励，获得了:\n" + reward)
                return
        raise SkipError("没有可领取的任务奖励")

@description('结束时领取任务奖励')
@booltype
@default(True)
class mission_receive_last(Module):
    async def do_task(self, client: pcrclient):
        resp = await client.mission_index()
        for mission in resp.missions:
            if db.is_daily_mission(mission.mission_id) and mission.mission_status == eMissionStatusType.EnableReceive:
                resp = await client.mission_receive()
                reward = await client.serlize_reward(resp.rewards)
                self._log("领取了任务奖励，获得了:\n" + reward)
                return
        raise SkipError("没有可领取的任务奖励")

@description('六星碎片，平时次数:庆典次数')
@enumtype(["none"] + [f"{i}:{j}" for i in range(0, 9, 3) for j in range(i, 9, 3) if i or j])
@default("3:3")
class six_star(Module):
    async def do_task(self, client: pcrclient):
        times = int(self.value.split(':')[client.data.is_very_hard_quest_double()])
        is_skip = True
        for quest_id, quest in db.six_area.items():
            pure_memory = quest.reward_image_1
            unit_id = db.pure_memory_to_unit[pure_memory]
            data = client.data.unit[unit_id]
            if data.unit_rarity != 6 and \
            (not data.unlock_rarity_6_item or 
             data.unlock_rarity_6_item and not data.unlock_rarity_6_item.slot_1) and \
            client.data.get_inventory((eInventoryType.Item, pure_memory)) < 50:
                try:
                    rewards = await client.quest_skip_aware(quest_id, times, True, True)
                    msg = await client.serlize_reward(rewards, (eInventoryType.Item, pure_memory))
                    is_skip = False
                    self._log(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {msg}")
                except SkipError as e:
                    self._log(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                except AbortError as e:
                    raise AbortError(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                except Exception as e:
                    raise ValueError(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
            else:
                pass
                # result.append(f"{quest_id}: 材料已够，无需刷取")
        if is_skip: raise SkipError("")
        if not self.log:
            raise SkipError("六星碎片均已足够，无需刷取")

@description('最高级地下城扫荡')
@enumtype(["none", "非双倍留一次数", "always"])
@default("always")
class underground_skip(Module):
    async def do_task(self, client: pcrclient):
        infos = await client.get_dungeon_info()

        async def do_enter(now_id = None):
            id = max([0] + infos.dungeon_cleared_area_id_list) if not now_id else now_id
            if id > 0:
                await client.enter_dungeon(id)
                dungeon_name = db.dungeon_name[id]
                self._log(f"已进入【{dungeon_name}】")
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        async def do_sweep(now_id = None):
            id = max([0] + infos.dungeon_cleared_area_id_list) if not now_id else now_id
            dungeon_name = db.dungeon_name[id]
            if id > 0:
                if id not in infos.dungeon_cleared_area_id_list:
                    raise AbortError(f"{dungeon_name}未讨伐，无法扫荡")
                reward_list = await client.skip_dungeon(id)
                rewards = [reward for reward_item in reward_list.skip_result_list for reward in reward_item.reward_list 
                           if db.is_unit_memory((reward.type, reward.id)) 
                           or db.xinsui == (reward.type, reward.id)
                           or db.xingqiubei == (reward.type, reward.id)]
                result = await client.serlize_reward(rewards)
                self._log(f"扫荡了【{dungeon_name}】,获得了:\n{result}")
                return reward_list.rest_challenge_count[0].count
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        double_mana = client.data.is_dungeon_mana_double()
        rest = infos.rest_challenge_count[0].count
        if infos.enter_area_id != 0:
            dungeon_name = db.dungeon_name[infos.enter_area_id]
            self._log(f"当前位于【{dungeon_name}】")
            if double_mana:
                self._log(f"今日地下城双倍mana")
                rest = await do_sweep(infos.enter_area_id)
            else:
                self._log(f"今日地下城非双倍mana")
                if rest:
                    self._log(f"还有{rest}次挑战次数，进行扫荡")
                    rest = await do_sweep(infos.enter_area_id)
                else:
                    if self.value == "always":
                        rest = await do_sweep(infos.enter_area_id)
                        
        if rest:
            if double_mana or self.value == "always":
                await do_sweep()
            else:
                await do_enter()
        else:
            raise SkipError("今日已扫荡地下城")

@description('基本信息')
@booltype
@default(True)
class user_info(Module):
    async def do_task(self, client: pcrclient):
        now = db.format_time(datetime.datetime.now())
        self._log(f"{client.data.name} 体力{client.data.stamina}({db.team_max_stamina[client.data.team_level].max_stamina}) 等级{client.data.team_level} 钻石{client.data.jewel.free_jewel} mana{client.data.gold.gold_id_free} 扫荡券{client.data.get_inventory((eInventoryType.Item, 23001))} 母猪石{client.data.get_inventory((eInventoryType.Item, 90005))}\n清日常时间:{now}")

@description('阅读角色剧情')
@enumtype(["none", "除ue普妈圣千普千真步", "all"])
@default("none")
class unit_story_reading(Module):
    async def do_task(self, client: pcrclient):
        ignore = True if self.value != "all" else False
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        ignore_chara_id = set([
            1002, # ue
            1010, # 真步
            1042, # 千歌
            1059, # 普妈
            1084, # 圣千
        ])
        for story in db.unit_story:
            if ignore and story.story_group_id in ignore_chara_id:
                continue
            if (
                story.story_id not in read_story and
                story.pre_story_id in read_story and
                story.story_group_id in client.data.unit_love and 
                client.data.unit_love[story.story_group_id].love_level >= story.love_level
                ):
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        if not self.log:
            raise SkipError("不存在未阅读的角色剧情")
        client.data.read_story_ids = list(read_story)
        self._log(f"共{len(self.log)}篇")

@description('阅读主线剧情')
@booltype
@default(True)
class main_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        for story in db.main_story:
            if story.story_id not in read_story and story.pre_story_id in read_story:
                if not await client.unlock_quest_id(story.unlock_quest_id):
                    raise AbortError(f"区域{story.unlock_quest_id}未通关，无法观看{story.title}\n")
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        client.data.read_story_ids = list(read_story)
        if not self.log:
            raise SkipError("不存在未阅读的主线剧情")
        self._log(f"共{len(self.log)}篇")

@description('阅读露娜塔剧情')
@booltype
@default(True)
class tower_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        for story in db.tower_story:
            now = datetime.datetime.now()
            start_time = db.parse_time(story.start_time)
            if now < start_time:
                continue
            if story.story_id not in read_story and story.pre_story_id in read_story:
                if not await client.unlock_quest_id(story.unlock_quest_id):
                    raise AbortError(f"层数{db.tower_quest[story.unlock_quest_id].floor_num}未通关，无法观看{story.title}\n")
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        client.data.read_story_ids = list(read_story)
        if not self.log:
            raise SkipError("不存在未阅读的露娜塔剧情")
        self._log(f"共{len(self.log)}篇")

@description('阅读活动剧情')
@booltype
@default(True)
class hatsune_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        unlock_story = set(client.data.unlock_story_ids)
        for story in db.event_story:
            if story.story_id not in read_story and story.pre_story_id in read_story and story.story_id in unlock_story:
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        if not self.log:
            raise SkipError("不存在未阅读的活动剧情")
        client.data.read_story_ids = list(read_story)
        self._log(f"共{len(self.log)}篇")

@description('阅读活动信赖度')
@booltype
@default(True)
class hatsune_dear_reading(Module):
    async def do_task(self, client: pcrclient):
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
                    await client.read_dear(event.event_id, story.story_id)
                    self._log(f"阅读了{story.story_id}")

        if not event_active:
            raise SkipError("当前无进行中的活动")
        if not self.log:
            raise SkipError("不存在未阅读的活动信赖度剧情")
        self._log(f"共{len(self.log)}篇")

@description('讨伐证交换')
@enumtype(["none", "前两轮重置", "all"])
@default("none")
class hatsune_gacha_exchange(Module):
    async def do_task(self, client: pcrclient):
        early_stop = False if self.value == "all" else True
        event_active = False

        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            event_active = True
            res = (await client.get_hatsune_top(event.event_id))
            exchange_ticket_id = db.hatsune_item[event.event_id].gacha_ticket_id
            res = (await client.get_hatsune_gacha_index(event.event_id, event.event_id))
            box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
            ticket = client.data.get_inventory((eInventoryType.Item, exchange_ticket_id))
            while(True):
                if ticket == 0:
                    self._log(f"{event.event_id}: 无讨伐证，停止交换")
                    break
                if res.event_gacha_info.gacha_step >= 6:
                    exchange_times = min(client.data.settings.loop_box_multi_gacha_count, ticket)
                    self._log(f"{event.event_id}: 当前处于第六轮及以上，一键交换{exchange_times}次")
                    await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 1)
                    ticket -= exchange_times
                else:
                    target_done = len([item.reward_id for item in box_item.values() if item.reset_target and item.remain_inbox_count]) == 0
                    remain_cnt = sum(item.remain_inbox_count for item in box_item.values())
                    if remain_cnt == 0 or (target_done and res.event_gacha_info.gacha_step <= 2 and early_stop):
                        self._log(f"{event.event_id}: 已达成重置条件，重置交换轮数")
                        res = await client.reset_hatsune_gacha(event.event_id, event.event_id)
                        box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
                        continue
                    exchange_times = min(100, ticket, remain_cnt)
                    self._log(f"{event.event_id}: 当前处于第{res.event_gacha_info.gacha_step}轮，交换{exchange_times}次")
                    resp = await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 0)
                    ticket -= exchange_times
                    for item in resp.draw_result:
                        box_item[item.box_set_id].remain_inbox_count -= item.hit_reward_count
            self._log(f"{event.event_id}: 已交换至" + (f"第{res.event_gacha_info.gacha_step}轮" if res.event_gacha_info.gacha_step < 6 else "第六轮及以上"))
            
        if not event_active:
            raise SkipError("当前无进行中的活动")

@description('在公会中自动随机选择一位成员点赞。')
@booltype
@default(True)
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        if client.data.clan_like_count:
            raise SkipError('今日点赞次数已用完。')
        info = await client.get_clan_info()
        if not info:
            raise AbortError("未加入公会")
        members = [(x.viewer_id, x.name) for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise AbortError("No other members in clan")
        rnd = random.choice(members)
        await client.clan_like(rnd[0])
        self._log(f"为【{rnd[1]}】点赞")

@description('活动h本')
@enumtype(["none", "odd", "even", "all"])
@default("none")
class hatsune_h_sweep(Module):
    async def do_task(self, client: pcrclient):
        area = []
        hard = 200
        is_error = False
        is_abort = False
        is_skip = True
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
                    await client.quest_skip_aware(quest_id, 3, False, True)
                    is_skip = False
                    self._log(f"{quest_id}: 扫荡{times}次")
                except SkipError as e:
                    self._log(f"{quest_id}: {str(e)}")
                except AbortError as e:
                    is_abort = True
                    self._log(f"{quest_id}: {str(e)}")
                    break
                except Exception as e: 
                    is_error = True
                    self._log(f"{quest_id}: {str(e)}")
                    break
        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@description('领取活动任务奖励')
@booltype
@default(True)
class hatsune_mission_accept(Module):
    async def do_task(self, client: pcrclient):
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
                        self._log(f"{event.event_id}: 领取了任务奖励，获得了:\n" + reward)
            except SkipError as e:
                self._log(f"{event.event_id}: {str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{event.event_id}: {str(e)}")
            except Exception as e:
                is_error = True
                self._log(f"{event.event_id}: {str(e)}")

        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@description('活动h本boss，未打vh保留30+未打sp保留90')
@enumtype(["none", "保留当日vh份", "保留当日及未来vh份"])
@default("none")
class hatsune_hboss_sweep(Module):
    async def do_task(self, client: pcrclient):
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in client.data.event_statuses:
            if event.event_type != 1 or event.period != 2:
                continue
            event_active = True
            resp = await client.get_hatsune_top(event.event_id)
            ticket = resp.boss_ticket_info.stock

            times = ticket // 30
            hboss_id = event.event_id * 100 + 2
            vhboss_id = event.event_id * 100 + 3
            spboss_id = event.event_id * 100 + 4

            boss_info = {boss.boss_id: boss for boss in resp.boss_battle_info}

            try: 
                if not boss_info[hboss_id].is_unlocked:
                    raise AbortError(f"h本boss未解锁")
                if not boss_info[spboss_id].kill_num:
                    self._log("sp未通关，保留90张")
                    times -= 3
                if not boss_info[vhboss_id].daily_kill_count:
                    self._log("今日vh未通关，保留30张")
                    times -= 1
                if self.value == "保留当日及未来vh份":
                    left_day = (db.get_start_time(db.parse_time(db.hatsune_schedule[event.event_id].end_time)) - db.get_today_start_time()).days 
                    self._log(f"距离活动结束还有{left_day}天，保留{left_day * 30}张")
                    times -= left_day

                if times <= 0:
                    raise SkipError(f"boss券不足")
                resp = await client.hatsune_boss_skip(event.event_id, hboss_id, times, ticket)
                is_skip = False
                self._log(f"{event.event_id} h boss: 扫荡{times}次")
            except SkipError as e:
                self._log(f"{event.event_id}: {str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{event.event_id}: {str(e)}")
            except Exception as e: 
                is_error = True
                self._log(f"{event.event_id}: {str(e)}")
        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@description('使用体力时，若体力不足，最多允许购买的体力管数。')
@enumtype([0, 1, 2, 3, 6, 9, 12])
@default(0)
class buy_stamina_passive(Module):
    async def do_task(self, client: pcrclient):
        client.keys['buy_stamina_passive'] = self.value
     
@description('每天主动购买的体力管数。仅一天第一次清日常触发。钻石数量<1w强制不触发。')
@enumtype(["none", 1, 2, 3, 6, 9, 12])
@default("none")
class buy_stamina_active(Module):
    async def do_task(self, client: pcrclient):
        cnt = 0
        last_clean_time = db.parse_time(client.keys['_last_clean_time']) if client.keys['_last_clean_time'] else None
        today = db.get_today_start_time()
        self._log(f"上一次清日常时间:{last_clean_time}，今日起始时间:{db.format_time(today)}")
        if last_clean_time and last_clean_time >= today:
            raise SkipError("非今天首次清日常，不主动购买体力")
        for _ in range(self.value):
            if client.data.jewel.free_jewel < 10000:
                self._log(f"今天首次清日常，购买了{str(cnt)}次体力")
                raise AbortError('钻石数量不足。中止购买体力。')
            if client.data.stamina + 120 > 999:
                self._log(f"今天首次清日常，购买了{str(cnt)}次体力")
                raise AbortError('体力恢复将超过999。中止购买体力')
            await client.recover_stamina()
            cnt += 1
        self._log(f"今天首次清日常，购买了{str(cnt)}次体力")

@description('收取家园体')
@booltype
@default(True)
class room_accept_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        for x in room.user_room_item_list:
            if x.item_count:
                res = await client.room_accept_all()
                msg = await client.serlize_reward(res.reward_list)
                self._log(msg)
                return
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

        for x in room.user_room_item_list:
            if db.is_room_item_level_upable(client.data.team_level, x):
                await client.room_level_up_item(floors[x.serial_id], x)
                self._log(f"开始升级{db.get_inventory_name_san((eInventoryType.RoomItem, x.room_item_id))}至{x.room_item_level + 1}级")

        if not self.log:
            raise SkipError('没有可升级的家园物品。')

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
            try:
                resp = await client.room_like(user.room_user_info.viewer_id)
            except Exception as e:
                if str(e).startswith("此玩家未读取的点赞数"):
                    continue
                else:
                    raise(e)
            result += resp.reward_list
            like_user.append(user.room_user_info.name)
            cnt += 1

        result = await client.serlize_reward(result)
        self._log(f"为【{'|'.join(like_user)}】点赞，获得了:\n" + result)

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
        msg = "10件装备"
        if memory:
            msg = await client.serlize_reward(memory) + f"\n{10 - len(memory)}件装备"
        self._log(msg)

@description('EXP探索')
@booltype
@default(True)
class explore_exp(Module):
    async def do_task(self, client: pcrclient):
        exp_quest_remain = client.data.training_quest_max_count.exp_quest - client.data.training_quest_count.exp_quest
        if exp_quest_remain:
            quest_id = client.data.get_max_avaliable_quest_exp()
            if not quest_id:
                raise AbortError("不存在可扫荡的exp探索")
            name = db.quest_name[quest_id]
            await client.training_quest_skip(quest_id, exp_quest_remain)
            self._log(f"{name}扫荡{exp_quest_remain}次")
        else:
            raise SkipError("exp已扫荡")

@description('MANA探索')
@booltype
@default(True)
class explore_mana(Module):
    async def do_task(self, client: pcrclient):
        gold_quest_remain = client.data.training_quest_max_count.gold_quest - client.data.training_quest_count.gold_quest
        if gold_quest_remain:
            quest_id = client.data.get_max_avaliable_quest_mana()
            if not quest_id:
                raise AbortError("不存在可扫荡的mana探索")
            name = db.quest_name[quest_id]
            await client.training_quest_skip(quest_id, gold_quest_remain)
            self._log(f"{name}扫荡{gold_quest_remain}次")
        else:
            raise SkipError("mana已扫荡")

@description('露娜塔回廊扫荡')
@booltype
@default(True)
class tower_cloister_sweep(Module):
    async def do_task(self, client: pcrclient):
        now = datetime.datetime.now()
        tower_id = db.get_newest_tower_id()
        schedule = db.tower[tower_id]
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
            result = await client.serlize_reward(result, db.xinsui)
            self._log(f"扫荡了{times}次，获得了:\n" + result)
        else:
            raise SkipError("回廊已扫荡")

@description('领取礼物箱')
@enumtype(["none", "非体力", "all"])
@default("非体力")
class present_receive(Module):
    async def do_task(self, client: pcrclient):
        if self.value == "非体力":
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
                if not is_exclude_stamina or not (present.reward_type == eInventoryType.Stamina and present.reward_id == 93001):
                    print(present.reward_type, present.reward_id)
                    res = await client.present_receive_all(is_exclude_stamina)
                    result += res.rewards
                    received = True
                    break
            else:
                break

        if not received:
            raise SkipError(f"不存在未领取{'的非体力的' if is_exclude_stamina == True else '的'}礼物")
        msg = await client.serlize_reward(result)
        self._log(op + msg)

@description('领取双场币')
@booltype
@default(True)
class jjc_reward(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_arena_info()
        if info.reward_info.count:
            await client.receive_arena_reward()
        self._log(f"jjc币x{info.reward_info.count}")
        info = await client.get_grand_arena_info()
        if info.reward_info.count:
            await client.receive_grand_arena_reward()
        self._log(f"pjjc币x{info.reward_info.count}")

class investigate_sweep(Module):
    @abstractmethod
    def quest_id(self) -> int: ...
    @abstractmethod
    def is_double_drop(self, client: pcrclient) -> bool: ...
    @abstractmethod
    def target_item(self) -> Tuple[eInventoryType, int]: ...

    async def do_task(self, client: pcrclient):
        times = int(self.value.split(':')[self.is_double_drop(client)])
        result = await client.quest_skip_aware(self.quest_id(), times, True, True)
        msg = await client.serlize_reward(result, self.target_item())
        self._log(f"重置{times // 5 - 1}次，获得了{msg}")

@description('刷取心碎3，平时次数:庆典次数')
@enumtype(["none"] + [f"{i}:{j}" for i in range(0, 25, 5) for j in range(i, 25, 5) if i or j])
@default("none")
class xinsui3_sweep(investigate_sweep):
    def quest_id(self) -> int:
        return 18001003
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_heart_piece_double()
    def target_item(self) -> Tuple[eInventoryType, int]:
        return db.xinsui

@description('刷取心碎2，平时次数:庆典次数')
@enumtype(["none"] + [f"{i}:{j}" for i in range(0, 25, 5) for j in range(i, 25, 5) if i or j])
@default("none")
class xinsui2_sweep(investigate_sweep):
    def quest_id(self) -> int:
        return 18001002
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_heart_piece_double()
    def target_item(self) -> Tuple[eInventoryType, int]:
        return db.xinsui

@description('刷取心碎1，平时次数:庆典次数')
@enumtype(["none"] + [f"{i}:{j}" for i in range(0, 25, 5) for j in range(i, 25, 5) if i or j])
@default("none")
class xinsui1_sweep(investigate_sweep):
    def quest_id(self) -> int:
        return 18001001
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_heart_piece_double()
    def target_item(self) -> Tuple[eInventoryType, int]:
        return db.xinsui

@description('刷取星球杯2，平时次数:庆典次数')
@enumtype(["none"] + [f"{i}:{j}" for i in range(0, 25, 5) for j in range(i, 25, 5) if i or j])
@default("none")
class xingqiubei2_sweep(investigate_sweep):
    def quest_id(self) -> int:
        return 19001002
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_star_cup_double()
    def target_item(self) -> Tuple[eInventoryType, int]:
        return db.xingqiubei

@description('刷取星球杯1，平时次数:庆典次数')
@enumtype(["none"] + [f"{i}:{j}" for i in range(0, 25, 5) for j in range(i, 25, 5) if i or j])
@default("none")
class xingqiubei1_sweep(investigate_sweep):
    def quest_id(self) -> int:
        return 19001001
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_star_cup_double()
    def target_item(self) -> Tuple[eInventoryType, int]:
        return db.xingqiubei

@description('''
首先按次数逐一刷取名字为start的图
然后循环按次数刷取设置为loop的图
当被动体力回复完全消耗后，刷图结束
'''.strip())
@booltype
@default(True)
class smart_sweep(Module):
    async def do_task(self, client: pcrclient):
        nloop: List[Tuple[int, int]] = []
        loop: List[Tuple[int, int]] = []
        for tab in client.data.user_my_quest:
            for x in tab.skip_list:
                if tab.tab_name == 'start':
                    nloop.append((x, tab.skip_count))
                elif tab.tab_name == 'loop':
                    loop.append((x, tab.skip_count))
        have_normal = any(db.is_normal_quest(quest[0]) for quest in loop)
        def _sweep():
            for x in nloop:
                yield x
            if loop:
                while True:
                    for x in loop:
                        yield x
                    if not have_normal:
                        raise AbortError("no normal, stop")

        result = []
        if nloop == [] and loop == []:
            raise AbortError("未找到start和loop")
        for quest_id, count in _sweep(): 
            try:
                result += await client.quest_skip_aware(quest_id, count, True, True)
            except SkipError as e:
                pass
            except AbortError as e:
                self._log(str(e))
                break
        
        self._log(await client.serlize_reward(result))

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
@enumtype(['none', 'n-5', 'n-10', 'n-15'])
@default('none')
class all_in_hatsune(Module):
    async def do_task(self, client: pcrclient):
        quest = 0
        for event in client.data.event_statuses: # 复刻和正常一起开的话会刷哪个？
            if event.event_type != 1 or event.period != 2:
                continue
            if self.value == 'n-5':
                quest = 1000 * event.event_id + 105
            elif self.value == 'n-10':
                quest = 1000 * event.event_id + 110
            elif self.value == 'n-15':
                quest = 1000 * event.event_id + 115
            
            await client.get_hatsune_top(event.event_id)
            await client.get_hatsune_quest_top(event.event_id)

            break
        
        if not quest: raise SkipError("当前无进行中的活动")
        

        count = client.data.stamina // db.quest_info[quest].stamina

        if count == 0: raise AbortError("体力不足")
        await client.quest_skip_aware(quest, count)
        self._log(f"已刷{quest}图{count}次")

def register_test():
    ModuleManager._modules = [
        buy_stamina_passive,
        smart_sweep
    ]

def register_all():
    ModuleManager._modules = [
        chara_fortune,
        mission_receive_first,
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
        hatsune_h_sweep,
        hatsune_dear_reading,
        present_receive,
        smart_sweep,
        smart_hard_sweep,
        smart_normal_sweep_unit,
        smart_normal_sweep,

        buy_stamina_active,
        all_in_hatsune,

        hatsune_hboss_sweep,
        hatsune_mission_accept,
        hatsune_gacha_exchange,
        hatsune_mission_accept,

        mission_receive_last,

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
