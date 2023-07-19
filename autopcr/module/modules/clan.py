from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *
import random

@description('在公会中自动随机选择一位成员点赞。')
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

