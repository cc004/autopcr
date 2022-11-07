from .pcrclient import pcrclient
from .modulebase import *

import random

@description('在公会中自动随机选择一位成员点赞。')
@booltype
@default(True)
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_clan_info()
        members = [x.viewer_id for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise ValueError("No other members in clan")
        rnd = random.choice(members)
        await client.clan_like(rnd)

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
        for i in range(self.value):
            if client.jewel < 10000: break
            await client.recover_stamina()

@description('收取家园体。')
@booltype
@default(True)
class room_accept_all(Module):
    async def do_task(self, client: pcrclient):
        await client.room_accept_all()

@description('EXP探索和MANA探索。')
@booltype
@default(True)
class explore(Module):
    async def do_task(self, client: pcrclient):
        # 9级
        await client.training_quest_skip(21001009, 2)
        await client.training_quest_skip(21002009, 2)


@description('领取礼物箱')
@booltype
@default(True)
class present_receive_all(Module):
    async def do_task(self, client: pcrclient):
        await client.present_receive_all()

@description('领取双场币')
@booltype
@default(True)
class jjc_reward(Module):
    async def do_task(self, client: pcrclient):
        await client.receive_arena_reward()
        await client.receive_grand_arena_reward()

@description('刷取心碎3')
@booltype
@default(True)
class xinsui3_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001003, 5, 15)

@description('刷取心碎2')
@booltype
@default(True)
class xinsui2_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001002, 5, 15)

@description('刷取心碎1')
@booltype
@default(True)
class xinsui1_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(18001001, 5, 15)

@description('刷取星球杯2')
@booltype
@default(True)
class xingqiubei2_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(19001002, 5, 15)

@description('刷取星球杯1')
@booltype
@default(True)
class xingqiubei1_sweep(Module):
    async def do_task(self, client: pcrclient):
        await client.quest_skip_aware(19001001, 5, 15)

def register_all():
    ModuleManager._modules = {
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
        buy_stamina_active
    }