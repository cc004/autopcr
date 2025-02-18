from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

@description('包括mana体力等等哦')
@name('收取家园产物')
@default(True)
@tag_stamina_get
class room_accept_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        for x in room.user_room_item_list:
            if x.item_count:
                res = await client.room_accept_all()
                msg = await client.serialize_reward_summary(res.reward_list)
                self._log(msg)
                return
        raise SkipError('没有可收取的家园物品。')

@description('等级提升时可自动升级')
@name('升级家园家具')
@default(True)
@tag_stamina_get
class room_upper_all(Module):
    async def do_task(self, client: pcrclient):
        room = await client.room_start()
        floors = {item.serial_id: floor + 1 for floor, floor_layout in enumerate(room.room_layout.floor_layout) for item in floor_layout.floor}

        for x in room.user_room_item_list:
            if db.is_room_item_level_upable(client.data.team_level, x, apiclient.time):
                if x.serial_id not in floors:
                    self._warn(f"{db.get_room_item_name(x.room_item_id)}未放置，无法升级")
                else:
                    gold = client.data.get_shop_gold(eSystemId.GOLD_SHOP)
                    cost = db.room_item_detail[x.room_item_id][x.room_item_level].lvup_item1_num
                    if gold < cost:
                        self._warn(f"金币{gold} < {cost}，无法升级{db.get_room_item_name(x.room_item_id)}至{x.room_item_level + 1}级")
                    else:
                        self._log(f"开始升级{db.get_room_item_name(x.room_item_id)}至{x.room_item_level + 1}级")
                        await client.room_level_up_item(floors[x.serial_id], x)

        if not self.log:
            raise SkipError('没有可升级的家园物品。')

@description('先回赞，再随机点赞')
@name('公会小屋点赞')
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
                viewer_id = like_history.be_liked_history[pos].viewer_id
            user = await client.room_visit(viewer_id)
            pos += 1
            if user.room_user_info.today_like_flag:
                continue
            try:
                resp = await client.room_like(user.room_user_info.viewer_id)
                result += resp.reward_list
                like_user.append(user.room_user_info.name)
                cnt += 1
            except Exception as e:
                if str(e).startswith("此玩家未读取的点赞数"):
                    continue
                else:
                    raise(e)

        result = await client.serialize_reward_summary(result)
        self._log(f"为【{'|'.join(like_user)}】点赞，获得了:\n" + result)

@description('一键发情所有角色')
@name('喂蛋糕')
@default(True)
class love_up(Module):
    async def do_task(self, client: pcrclient):
        for unit in client.data.unit_love_data.values():
            unit_id = unit.chara_id * 100 + 1
            unit_name = db.get_unit_name(unit_id)
            love_level, total_love = db.max_total_love(client.data.unit[unit_id].unit_rarity)
            if unit.chara_love < total_love:
                dis = total_love - unit.chara_love
                cakes = client.data.get_love_up_cake_demand(dis)
                if not cakes:
                    self._log(f"{unit_name}: 蛋糕数量不足")
                    break
                self._log(f"{unit_name}: 亲密度升至{love_level}级")
                await client.multi_give_gift(unit_id, cakes)

        if not self.log:
            raise SkipError("所有角色均已亲密度满级")
