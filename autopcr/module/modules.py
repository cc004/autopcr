from ..core import pcrclient
from .modulebase import *

import random

@description('在公会中自动随机选择一位成员点赞。')
@booltype
@default(True)
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        if client.data.clan_like_count != 0:
            raise ValueError('今日点赞次数已用完。')
        info = await client.get_clan_info()
        members = [x.viewer_id for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise ValueError("No other members in clan")
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
            if client.jewel.free_jewel < 10000: break
            await client.recover_stamina()

@description('收取家园体。')
@booltype
@default(True)
class room_accept_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        for x in room.user_room_item_list:
            if x.item_count:
                await client.room_accept_all()
                return
        raise ValueError('没有可收取的家园物品。')

@description('EXP探索和MANA探索。')
@booltype
@default(True)
class explore(Module):
    async def do_task(self, client: pcrclient):
        # 11级探索
        if 2 - client.data.training_quest_count.gold_quest:
            await client.training_quest_skip(21001011, 2 - client.data.training_quest_count.gold_quest)
        if 2 - client.data.training_quest_count.exp_quest:
            await client.training_quest_skip(21002011, 2 - client.data.training_quest_count.exp_quest)


@description('领取礼物箱')
@booltype
@default(True)
class present_receive_all(Module):
    async def do_task(self, client: pcrclient):
        present = await client.present_index()
        if not present.present_count:
            raise ValueError("No present to receive")
        await client.present_receive_all()

@description('领取双场币')
@booltype
@default(True)
class jjc_reward(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_arena_info()
        if info.reward_info.count:
            await client.receive_arena_reward()
        info = await client.get_grand_arena_info()
        if info.reward_info.count:
            await client.receive_grand_arena_reward()

@description('刷取心碎3')
@booltype
@default(True)
class xinsui3_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001003, 5)

@description('刷取心碎2')
@booltype
@default(True)
class xinsui2_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001002, 5)

@description('刷取心碎1')
@booltype
@default(True)
class xinsui1_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001001, 5)

@description('刷取星球杯2')
@booltype
@default(True)
class xingqiubei2_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(19001002, 5)

@description('刷取星球杯1')
@booltype
@default(True)
class xingqiubei1_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(19001001, 5)

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

        msg = []
        for quest_id, count in _sweep():
            try:
                await client.quest_skip_aware(quest_id, count, True, True)
            except ValueError as e:
                m = str(e)
                if m == '体力不足': break
                else:
                    msg.append(m)
                    if not m.endswith("已达最大次数"):
                        raise ValueError(';'.join(msg))
        
        if msg: raise ValueError(';'.join(msg))

def register_test():
    ModuleManager._modules = [
        buy_stamina_passive,
        smart_sweep
    ]

def register_all():
    ModuleManager._modules = [
        buy_stamina_passive,
        room_accept_all,
        explore,
        present_receive_all,
        jjc_reward,
        xinsui3_sweep,
        xinsui2_sweep,
        xingqiubei2_sweep,
        xinsui1_sweep,
        xingqiubei1_sweep, 
        clan_like,
        buy_stamina_active,
        smart_sweep
    ]
