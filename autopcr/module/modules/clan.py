from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...model.enums import *
import random
import datetime
from ...db.database import db

@description('在公会中自动随机选择一位成员点赞。')
@name("公会点赞")
@default(True)
@tag_stamina_get
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        if client.data.clan_like_count:
            raise SkipError('今日点赞次数已用完。')
        clan = await client.get_clan_info()
        if not clan:
            raise AbortError("未加入公会")
        info = clan.clan
        members = [(x.viewer_id, x.name) for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise AbortError("nobody's home?")
        rnd = random.choice(members)
        await client.clan_like(rnd[0])
        self._log(f"为【{rnd[1]}】点赞")

@description('对某颜色缺口数量最多的装备发起请求')
@name("装备请求")
@singlechoice("clan_equip_request_color", "装备颜色", "all", ["all", "Silver", "Gold", "Purple", 'Red', 'Green'])
@singlechoice("clan_equip_request_consider_unit_rank", "起始品级", "所有", ["所有", '最高', '次高', '次次高'])
@booltype("clan_equip_request_consider_unit_fav", "收藏角色", False)
@default(False)
class clan_equip_request(Module):
    color_to_promotion = {
            'all': 0,
            "Brozen": 2,
            "Silver": 3,
            "Gold": 4,
            "Purple": 5,
            "Red": 6,
            "Green": 7,
    }
    async def do_task(self, client: pcrclient):
        clan = await client.get_clan_info()
        if not clan:
            raise AbortError("未加入公会")

        if clan.latest_request_time and apiclient.time <= clan.latest_request_time + client.data.settings.clan.equipment_request_interval:
            raise SkipError("当前请求尚未结束")
        elif clan.latest_request_time:
            res = await client.equip_get_request(clan.clan.detail.clan_id, 0)
            msg = f"收到{db.get_equip_name(res.request.equip_id)}x{res.request.donation_num}：" + ' '.join(f"{user.name}x{user.num}" for user in res.request.history)
            self._log(msg.strip("："))

        opt: Dict[Union[int, str], int] = {
            '所有': 1,
            '最高': db.equip_max_rank,
            '次高': db.equip_max_rank - 1,
            '次次高': db.equip_max_rank - 2,
        }

        fav: bool = self.get_config('clan_equip_request_consider_unit_fav')
        start_rank: int = opt[self.get_config('clan_equip_request_consider_unit_rank')]
        demand = client.data.get_equip_demand_gap(like_unit_only=fav, start_rank=start_rank)
        config_color: str = self.get_config('clan_equip_request_color')
        target_level = self.color_to_promotion[config_color]

        consider_equip = [(equip_id, num) for (item_type, equip_id), num in demand.items() if 
                          db.equip_data[equip_id].enable_donation and 
                          db.equip_data[equip_id].require_level <= client.data.team_level and
                          (db.equip_data[equip_id].promotion_level == target_level or config_color == 'all')]
        consider_equip = sorted(consider_equip, key=lambda x: x[1], reverse=True)

        if consider_equip:
            (equip_id, num) = consider_equip[0]
            await client.request_equip(equip_id, clan.clan.detail.clan_id)
            self._log(f"请求【{db.get_equip_name(equip_id)}】装备，缺口数量为{num}")
        else:
            raise AbortError("没有可请求的装备")
