from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *
import random
import datetime
from ...db.database import db

@description('在公会中自动随机选择一位成员点赞。')
@name("公会点赞")
@default(True)
class clan_like(Module):
    async def do_task(self, client: pcrclient):
        if client.data.clan_like_count:
            raise SkipError('今日点赞次数已用完。')
        clan = await client.get_clan_info()
        if not clan:
            raise AbortError("未加入公会")
        info = clan.clan
        members = [(x.viewer_id, x.name) for x in info.members if x.viewer_id != client.viewer_id]
        if len(members) == 0: raise AbortError("No other members in clan")
        rnd = random.choice(members)
        await client.clan_like(rnd[0])
        self._log(f"为【{rnd[1]}】点赞")

@description('对某颜色缺口数量最多的装备发起请求')
@name("装备请求")
@singlechoice("clan_equip_request_color", "装备颜色", "all", ["all", "Silver", "Gold", "Purple", 'Red', 'Green'])
@singlechoice("clan_equip_request_consider_unit", "需求角色", "all", ["all", 'favorite'])
@default(False)
class clan_equip_request(Module):
    async def do_task(self, client: pcrclient):
        clan = await client.get_clan_info()
        if not clan:
            raise AbortError("未加入公会")

        if datetime.datetime.now().timestamp() > clan.latest_request_time + client.data.settings.clan.equipment_request_interval:
            res = await client.equip_get_request(clan.clan.detail.clan_id, 0)
            msg = f"收到{db.get_inventory_name_san((eInventoryType.Equip, res.request.equip_id))}x{res.request.donation_num}：" + ' '.join(f"{user.name}x{user.num}" for user in res.request.history)
            self._log(msg.strip("："))
        else:
            raise SkipError("当前请求尚未结束")

        fav = (self.get_config('clan_equip_request_consider_unit') == 'favorite')
        demand = client.data.get_equip_demand_gap(like_unit_only=fav)
        config_color: str = self.get_config('clan_equip_request_color')
        target_level = set(level for color, level in vars(ePromotionLevel).items() if color.startswith(config_color))

        consider_equip = [(equip_id, num) for (item_type, equip_id), num in demand.items() if db.equip_data[equip_id].enable_donation and (db.equip_data[equip_id].promotion_level in target_level or config_color == 'all')]
        consider_equip = sorted(consider_equip, key=lambda x: x[1], reverse=True)

        if consider_equip:
            (equip_id, num) = consider_equip[0]
            await client.request_equip(equip_id, clan.clan.detail.clan_id)
            self._log(f"请求【{db.get_inventory_name_san((eInventoryType.Equip, equip_id))}】装备，缺口数量为{num}")
        else:
            raise AbortError("没有可请求的装备")
