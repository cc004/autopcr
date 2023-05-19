from ..core import pcrclient
from .modulebase import *
from ..model.error import *
from ..core.database import db
from ..model.models import *
import random
import itertools
from abc import abstractmethod

@description('在公会中自动随机选择一位成员点赞。')
@booltype
@default(True)
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        if not client.data.clan_like_count:
            raise SkipError('今日点赞次数已用完。')
        info = await client.get_clan_info()
        members = [x.viewer_id for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise AbortError("No other members in clan")
        rnd = random.choice(members)
        await client.clan_like(rnd)

@description('使用体力时，若体力不足，最多允许购买的体力管数。')
@enumtype([0, 1, 2, 3, 6, 9, 12])
@default(6)
class buy_stamina_passive(Module):
    async def do_task(self, client: pcrclient):
        client.keys['buy_stamina_passive'] = self.value
     
@description('每天主动购买的体力管数。钻石数量<1w强制不触发。')
@enumtype([0, 1, 2, 3, 6, 9, 12])
@default(0)
class buy_stamina_active(Module):
    async def do_task(self, client: pcrclient):
        for i in range(self.value):
            if client.jewel.free_jewel < 10000:
                raise AbortError('钻石数量不足。中止购买体力。')
            await client.recover_stamina()

@description('收取家园体。')
@booltype
@default(True)
class room_accept_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        t = client.data.stamina
        for x in room.user_room_item_list:
            if x.item_count:
                await client.room_accept_all()
                return
        self._log(f'收取家园体力：{t} => {client.data.stamina}')
        raise SkipError('没有可收取的家园物品。')

@description('EXP探索和MANA探索。')
@booltype
@default(True)
class explore(Module):
    async def do_task(self, client: pcrclient):
        # 11级探索
        if client.data.training_quest_count.gold_quest != 2:
            self._log(f'Mana探索: {2 - client.data.training_quest_count.gold_quest}次')
            await client.training_quest_skip(21001011, 2 - client.data.training_quest_count.gold_quest)
        else:
            self._log(f'Mana探索：已完成')
        if client.data.training_quest_count.exp_quest != 2:
            self._log(f'Exp探索: {2 - client.data.training_quest_count.exp_quest}次')
            await client.training_quest_skip(21002011, 2 - client.data.training_quest_count.exp_quest)
        else:
            self._log(f'Exp探索：已完成')


@description('领取礼物箱')
@booltype
@default(True)
class present_receive_all(Module):
    async def do_task(self, client: pcrclient):
        present = await client.present_index()
        if not present.present_count:
            raise SkipError("No present to receive")
        await client.present_receive_all(False)
        self._log('礼物已领取完成')

@description('领取双场币')
@booltype
@default(True)
class jjc_reward(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_arena_info()
        if info.reward_info.count:
            await client.receive_arena_reward()
            self._log(f'领取jjc币x{info.reward_info.count}')
        else:
            self._log('jjc币已领取完成')
        info = await client.get_grand_arena_info()
        if info.reward_info.count:
            await client.receive_grand_arena_reward()
            self._log(f'领取pjjc币x{info.reward_info.count}')
        else:
            self._log('pjjc币已领取完成')

@description('刷取心碎3')
@booltype
@default(True)
class xinsui3_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001003, 5)
        self._log('心碎3已刷取完成')

@description('刷取心碎2')
@booltype
@default(True)
class xinsui2_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001002, 5)
        self._log('心碎2已刷取完成')

@description('刷取心碎1')
@booltype
@default(True)
class xinsui1_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001001, 5)
        self._log('心碎1已刷取完成')

@description('刷取星球杯2')
@booltype
@default(True)
class xingqiubei2_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(19001002, 5)
        self._log('星球杯2已刷取完成')

@description('刷取星球杯1')
@booltype
@default(True)
class xingqiubei1_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(19001001, 5)
        self._log('星球杯1已刷取完成')

@description('''
根据一键扫荡设置自动刷图，具体次数由标签页名字和设置的使用扫荡张数决定
刷图逻辑：首先按次数逐一刷取名字为start的图，然后循环按次数刷取设置为loop的图
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
            while True:
                for x in loop:
                    yield x

        for quest_id, count in _sweep():
            try:
                await client.quest_skip_aware(quest_id, count, True, True)
            except SkipError as e:
                m = str(e)
                if m == '体力不足': break
                else:
                    self._log(m)
                    if not m.endswith("已达最大次数"):
                        raise

@description('开始时领取任务奖励')
@booltype
@default(True)
class receive_mission_reward(Module):
    async def do_task(self, client: pcrclient):
        index = await client.mission_index()
        if not [x for x in index.missions if x.mission_status == eMissionStatusType.EnableReceive]:
            raise SkipError("没有要领取的任务奖励")
        await client.mission_receive()
        self._log('任务奖励已领取完成')

@description('结束时领取任务奖励')
class receive_mission_reward2(receive_mission_reward):
    pass

@description('探索露娜塔回廊')
@booltype
@default(True)
class tower_explore(Module):
    async def do_task(self, client: pcrclient):
        top = await client.get_tower_top()
        if not top.cloister_first_cleared_flag:
            raise AbortError("露娜塔回廊未开启")
        if not top.cloister_remain_clear_count:
            raise SkipError("露娜塔回廊已探索完成")
        await client.tower_cloister_battle_skip(top.cloister_remain_clear_count)
        self._log(f'露娜塔回廊探索完成{top.cloister_remain_clear_count}次')

@description('普通扭蛋')
@booltype
@default(True)
class gacha_normal(Module):
    async def do_task(self, client: pcrclient):
        await client.normal_gacha()
        self._log('普通扭蛋已完成')


@description('商店购买最大碎片量')
@enumtype([0, 100, 300, 600, 900, 99999])
@default(300)
class shop_buy_limit(Module):
    async def do_task(self, client: pcrclient):
        client.keys['shop_buy_limit'] = self.value

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
class jjc_shop(shop_buy):
    def system_id(self) -> int:
        return 202
    def coin_limit(self) -> int:
        return 30000

@description('购买pjjc币刷新次数, -1为不购买')
@enumtype([-1, 0, 1, 2, 3, 4, 7, 10])
@default(0)
class pjjc_shop(shop_buy):
    def system_id(self) -> int:
        return 203
    def coin_limit(self) -> int:
        return 30000

@description('地下城扫荡')
@booltype
@default(True)
class dungeon_sweep(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_dungeon_info()
        if info.enter_area_id:
            if info.enter_area_id in info.dungeon_cleared_area_id_list:
                await client.skip_dungeon(info.enter_area_id)
                self._log(f"地下城{db.dungeon_name[info.enter_area_id]}已扫荡完成")
                return
            raise AbortError("地下城进入了不可扫荡的区域")
        if not [
            x for x in info.rest_challenge_count if x.dungeon_type == 1 and x.count > 0
        ]:
            raise AbortError("地下城挑战次数不足")
        
        await client.skip_dungeon(max(info.dungeon_cleared_area_id_list))
        self._log(f'地下城{db.dungeon_name[max(info.dungeon_cleared_area_id_list)]}扫荡已完成')

@description('活动任务领取')
@booltype
@default(True)
class hatsune_mission_receive_all(Module):
    async def do_task(self, client: pcrclient):
        for event in client.data.event_statuses:
            index = await client.hatsune_mission_index(event.event_id)
            types = set(x // 10000000 + 5 for x in index.missions if x.mission_status == eMissionStatusType.EnableReceive)
            if not types:
                self._log(f"活动{event.event_id}任务已领取")
            else:
                for type in types:
                    await client.hatsune_mission_receive(event.event_id, type)
                self._log(f'活动{event.event_id}任务领取完成')

@description('活动Boss扫荡')
@enumtype(['0', 'max - 1', 'max'])
@default('max - 1')
class hatsune_boss_sweep(Module):
    async def do_task(self, client: pcrclient):
        for event in client.data.event_statuses:
            index = await client.get_hatsune_top(event.event_id)
            item_count = client.data.get_inventory((eInventoryType.Item, db.hatsune_item[event.event_id][0]))
            times_to_sweep = max(0, item_count // 30 if self.value == 'max' else item_count // 30 - 1 if self.value == 'max - 1' else 0)
            if not times_to_sweep:
                self._log(f"活动{event.event_id}Boss券不足")
                continue
            boss_id = [x.boss_id for x in index.boss_battle_info if x.boss_id % 100 == 2]
            if not boss_id:
                self._log(f"活动{event.event_id}Boss未解锁")
                continue
            await client.hatsune_boss_skip(event.event_id, boss_id[0], times_to_sweep, item_count)
            self._log(f"活动{event.event_id}Boss扫荡{times_to_sweep}次")

@description('活动一键兑换')
@booltype
@default(True)
class hatsune_exchange(Module):
    async def do_task(self, client: pcrclient):
        for event in client.data.event_statuses:
            top = await client.get_hatsune_top(event.event_id)
            index = await client.get_hatsune_gacha_index(event.event_id, event.event_id)
            if len([x for x in index.event_gacha_info.box_set_list if x.remain_inbox_count]) > 1:
                self._log(f"活动{event.event_id}尚未进入循环兑换")
                continue
            await client.exec_hatsune_gacha_all(event.event_id, event.event_id)

class hatsune_sweep(Module):
    @abstractmethod
    def quest_tails(self) -> List[int]: ...
    @abstractmethod
    def kwargs(self) -> dict: ...

    async def do_task(self, client: pcrclient):
        for (tail, event) in itertools.product(self.quest_tails(), client.data.event_statuses):
            await client.get_hatsune_quest_top(event.event_id) # refresh hatsune quest cache
            try:
                await client.hatsune_quest_skip_aware(event.event_id, (1000 * event.event_id + tail), **self.kwargs())
                self._log(f"活动{event.event_id}扫荡{tail}图")
            except SkipError as e:
                self._log(f"活动{event.event_id}扫荡{tail}图失败: {e}")
                break
            except AbortError as e:
                self._log(f"活动{event.event_id}扫荡{tail}图失败: {e}")
                continue

@description('活动扫荡h135图')
@booltype
@default(True)
class hatsune135_sweep(hatsune_sweep):
    def quest_tails(self) -> List[int]:
        return [205, 203, 201]
    def kwargs(self) -> dict:
        return {'times': 3, 'is_total': True}

@description('活动扫荡h24图')
@booltype
@default(True)
class hatsune24_sweep(hatsune_sweep):
    def quest_tails(self) -> List[int]:
        return [204, 202]
    def kwargs(self) -> dict:
        return {'times': 3, 'is_total': True}

@description('扫荡六星碎片')
@enumtype([0, 3, 6])
@default(3)
class vh_sweep(Module):
    async def do_task(self, client: pcrclient):
        for quest, (item, unit) in db.six_area.items():
            data = client.data.unit[unit]
            if data.unit_rarity == 6 or data.unlock_rarity6_item and data.unlock_rarity6_item.status1 or client.data.get_inventory(
                (eInventoryType.Piece, item)) >= 50:
                continue
            await client.quest_skip_aware(quest, self.value, True, True)
            self._log(f"为角色{unit}扫荡六星碎片图")


@description('购买限时商店')
@booltype
@default(True)
class daily_shop(Module):
    async def do_task(self, client: pcrclient):
        items_to_buy = [x.slot_id for x in client.data.daily_shop.item_list if x.available_num]
        if not items_to_buy:
            raise SkipError(f"限时商店已购买")
        await client.shop_buy_item(client.data.daily_shop.system_id, items_to_buy)
        self._log(f"已购买限时商店")

def register_test():
    ModuleManager._modules = [
        buy_stamina_passive,
        smart_sweep
    ]

def register_all():
    ModuleManager._modules = [
        buy_stamina_passive,
        receive_mission_reward,
        clan_like,
        room_accept_all,
        explore,
        gacha_normal,
        shop_buy_limit,
        dungeon_shop,
        jjc_shop,
        pjjc_shop,
        dungeon_sweep,
        vh_sweep,
        hatsune135_sweep,
        hatsune24_sweep,
        jjc_reward,
        tower_explore,
        xinsui3_sweep,
        xinsui2_sweep,
        xingqiubei2_sweep,
        xinsui1_sweep,
        xingqiubei1_sweep,
        hatsune_boss_sweep,
        hatsune_mission_receive_all,
        hatsune_exchange,
        daily_shop,
        buy_stamina_active,
        present_receive_all,
        smart_sweep,
        receive_mission_reward2,
    ]