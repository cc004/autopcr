from .pcrclient import pcrclient
from .modulebase import *

import random

@description('在公会中自动随机选择一位成员点赞。')
@booltype
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_clan_info()
        members = [x.viewer_id for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise ValueError("No other members in clan")
        rnd = random.choice(members)
        await client.clan_like(rnd)


def register_all():
    ModuleManager._modules = [
        clan_like
    ]