from typing import List

from ...model.common import ChangeRarityUnit

from ...db.models import GachaExchangeLineup
from ...model.custom import GachaReward, ArenaQueryResponse
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
import datetime

@description('来发十连，或者直到出货')
@name('抽卡')
@singlechoice("pool_id", "池子", db.get_cur_gacha()[0], db.get_cur_gacha())
@booltype("cc_until_get", "抽到出", False)
@default(True)
class gacha_start(Module):
    def can_stop(self, new, exchange: List[GachaExchangeLineup]):
        r = set(item.unit_id for item in exchange)
        return any(item.id in r for item in new)

    async def do_task(self, client: pcrclient):
        if ':' not in self.get_config('pool_id'):
            raise ValueError("配置格式不正确")
        gacha_id = int(self.get_config('pool_id').split(':')[0])
        resp = await client.get_gacha_index()
        for gacha in resp.gacha_info:
            if gacha.id == gacha_id:
                target_gacha = gacha
                break
        else:
            raise AbortError(f"未找到卡池{gacha_id}")
        if target_gacha.type != eGachaType.Payment:
            raise AbortError("非宝石抽卡池")

        reward = GachaReward()
        always = self.get_config('cc_until_get')
        cnt = 0
        try:
            while True:
                reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Payment, client.data.jewel.free_jewel + client.data.jewel.jewel, 0)
                cnt += 1
                if not always or self.can_stop(reward.new_unit, db.gacha_exchange_chara[target_gacha.exchange_id]) :
                    break
        except:
            raise 
        finally:
            self._log(f"抽取了{cnt}次十连")
            self._log(await client.serlize_gacha_reward(reward))
            self._log(f"当前pt为{client.data.gacha_point[target_gacha.exchange_id].current_point}")

@description('查看会战支援角色的详细数据，拒绝内鬼！')
@name('会战支援数据')
@default(True)
class get_clan_support_unit(Module):
    async def do_task(self, client: pcrclient):
        await client.get_clan_battle_top(client.data.clan, 1, client.data.get_shop_gold(eSystemId.CLAN_BATTLE_SHOP))
        unit_list = await client.get_clan_battle_support_unit_list(client.data.clan)
        msg = []
        for unit in unit_list.support_unit_list:
            strongest, info = await client.serialize_unit_info(unit.unit_data)
            msg.append((unit.unit_data.id, strongest, unit.owner_name, info))

        for unit in client.data.dispatch_units:
            if unit.position == eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_1 or unit.position == eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_2:
                strongest, info = await client.serialize_unit_info(client.data.unit[unit.unit_id])
                msg.append((unit.unit_id, strongest, client.name, info))

        msg = sorted(msg, key=lambda x:(x[0], -x[1]))
        for unit_id, strongest, owner_name, unit_info in msg:
            unit_name = db.get_unit_name(unit_id)
            info = f'{unit_name}({owner_name}): {"满中满" if strongest else "非满警告！"}\n{unit_info}\n'
            self._log(info)

@description('查询jjc回刺阵容，并自动设置进攻队伍')
@name('jjc回刺查询')
@default(True)
class jjc_back(Module):
    async def rank_team(self, team: List[ArenaQueryResponse]):
        def score(x):
            good = team[x].up
            bad = team[x].down
            total = good + bad
            bad_ratio = bad / total if total else 0
            return (bad_ratio, x)

        id = list(range(len(team)))
        return sorted(id, key=lambda x: score(x))

    async def choose_best_team(self, team: List[ArenaQueryResponse], rank_id: List[int], client: pcrclient):
        all_have = [id for id in rank_id if all(unit.id in client.data.unit and client.data.unit[unit.id].promotion_level > db.equip_max_rank - 3 for unit in team[id].atk)]
        return None if not all_have else all_have[0]

    async def update_deck(self, units: List[int], client: pcrclient):
        star_change_unit = [unit for unit in units if client.data.unit[unit].unit_rarity == 5 and client.data.unit[unit].battle_rarity != 0]
        if star_change_unit:
            res = [ChangeRarityUnit(unit_id=unit_id, battle_rarity=5) for unit_id in star_change_unit]
            self._log(f"将{'|'.join([db.get_unit_name(unit_id) for unit_id in star_change_unit])}调至5星")
            await client.unit_change_rarity(res)
        await client.deck_update(ePartyType.ARENA, units)

    async def get_opponent_info(self, client: pcrclient, viewer_id: int):
        for page in range(1, 6):
            ranking = {info.viewer_id: info for info in (await client.arena_rank(20, page)).ranking}
            if viewer_id in ranking:
                return ranking[viewer_id]
        raise AbortError("对手不在前100名，无法查询")

    async def do_task(self, client: pcrclient):
        try:
            from hoshino.modules.priconne.arena.arena import do_query
            from hoshino.modules.priconne.arena import render_atk_def_teams
        except Exception as e:
            print(e)
            raise AbortError("仅支持插件端")

        rank = (await client.get_arena_info()).arena_info.rank
        history = await client.get_arena_history()
        if not history.versus_result_list:
            raise SkipError("没有被刺记录")
        history = history.versus_result_list[0]
        timestamp = history.versus_time
        target = history.opponent_user
        self._log(f"{target.user_name}: {datetime.datetime.fromtimestamp(timestamp)}")
        target_info = await self.get_opponent_info(client, target.viewer_id)
        self._log(f"对方排名：{target_info.rank}, 您当前排名：{rank}")
        if rank < target_info.rank:
            raise SkipError(f"对方排名位于您排名之后")
        deck_info = [unit.id for unit in target_info.arena_deck]
        short_info = [unit.id // 100 for unit in target_info.arena_deck]

        res = await do_query(short_info, 2)

        defen = [db.get_unit_name(x) for x in deck_info]
        defen = f"防守方【{' '.join(defen)}】"
        if res is None:
            raise AbortError(f'{defen}\n数据库未返回数据，请再次尝试查询或前往pcrdfans.com')
        if res == []:
            raise AbortError(f'{defen}\n抱歉没有查询到解法\n※没有作业说明随便拆 发挥你的想象力～★\n作业上传请前往pcrdfans.com')

        res = res[:min(8, len(res))] 
        teams = await render_atk_def_teams(res)
        # [
        #   atk: List[Chara(id, star, equip)]
        #   up: int,
        #   down: int,
        # ]

        obj = [{ **re,
                 **{ 'atk': [{
                    'id': unit.id * 100 + 1,
                    'star': unit.star,
                    'equip': unit.equip } for unit in re['atk']]
                   }
                } for re in res]
        obj = [ArenaQueryResponse.parse_obj(o) for o in obj]

        rank_id = await self.rank_team(obj)
        best_team_id = await self.choose_best_team(obj, rank_id, client)
        if best_team_id is not None:
            self._log(f"选择第{best_team_id + 1}支队伍作为进攻方队伍")
            team = [unit.id for unit in obj[best_team_id].atk][::-1]
            await self.update_deck(team, client)
        else:
            self._log("未找到合适队伍，请自行选择")

        from io import BytesIO
        import base64
        img_byte_array = BytesIO()
        teams = teams.convert("RGB")
        teams.save(img_byte_array, format="JPEG")
        teams = base64.b64encode(img_byte_array.getvalue()).decode()
        pic = f'<img src="data:image/jpeg;base64,{teams}" alt="Image">'
        msg = [defen, pic]
        self._log('\n'.join(msg))

@description('获得可导入到兰德索尔图书馆的账号数据')
@name('兰德索尔图书馆导入数据')
@default(True)
class get_library_import_data(Module):
    async def do_task(self, client: pcrclient):
        msg = client.data.get_library_import_data()
        self._log(msg)

@description('根据每个角色拉满星级、开专、升级至当前最高专所需的记忆碎片减去库存的结果')
@booltype("sweep_get_able_unit_memory", "地图可刷取角色", False)
@name('获取记忆碎片缺口')
@default(True)
class get_need_memory(Module):
    async def do_task(self, client: pcrclient):
        demand = list(client.data.get_memory_demand_gap().items())
        demand = sorted(demand, key=lambda x: x[1], reverse=True)
        if self.get_config("sweep_get_able_unit_memory"):
            demand = [i for i in demand if i[0] in db.memory_quest]

        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in demand])
        self._log(msg)

@description('根据每个角色开专、升级至当前最高专所需的心碎减去库存的结果，大心转换成10心碎')
@name('获取心碎缺口')
@default(True)
class get_need_xinsui(Module):
    async def do_task(self, client: pcrclient):
        result, need = client.data.get_suixin_demand()
        result = sorted(result, key=lambda x: x[1])
        msg = [f"{db.get_inventory_name_san(item[0])}: 需要{item[1]}片" for item in result]

        store = client.data.get_inventory(db.xinsui) + client.data.get_inventory(db.heart) * 10
        cnt = need - store
        tot = f"当前心碎数量为{store}(大心自动转换成10心碎)，需要{need}，"
        if cnt > 0:
            tot += f"缺口数量为:{cnt}"
        elif cnt < 0:
            tot += f"盈余数量为:{-cnt}"
        else:
            tot += "当前心碎储备刚刚好！"
        msg = [tot] + msg
        msg = '\n'.join(msg)
        self._log(msg)

@inttype("start_rank", "起始品级", 1, [i for i in range(1, 99)])
@booltype("like_unit_only", "收藏角色", False)
@description('统计指定角色拉满品级所需的装备减去库存的结果，不考虑仓库中的大件装备')
@name('获取装备缺口')
@default(True)
class get_need_equip(Module):
    async def do_task(self, client: pcrclient):
        start_rank: int = self.get_config("start_rank")
        like_unit_only: bool = self.get_config("like_unit_only")

        demand = list(client.data.get_equip_demand_gap(start_rank=start_rank, like_unit_only=like_unit_only).items())

        demand = sorted(demand, key=lambda x: x[1], reverse=True)

        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in demand])
        self._log(msg)

@inttype("start_rank", "起始品级", 1, [i for i in range(1, 99)])
@booltype("like_unit_only", "收藏角色", False)
@description('根据装备缺口计算刷图优先级，越前的优先度越高')
@name('刷图推荐')
@default(True)
class get_normal_quest_recommand(Module):
    async def do_task(self, client: pcrclient):
        start_rank: int = self.get_config("start_rank")
        like_unit_only: bool = self.get_config("like_unit_only")

        quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= datetime.datetime.now()]
        require_equip = client.data.get_equip_demand_gap(start_rank = start_rank, like_unit_only = like_unit_only)
        quest_weight = client.data.get_quest_weght(require_equip)
        quest_id = sorted(quest_list, key = lambda x: quest_weight[x], reverse = True)
        tot = []
        for i in range(10):
            id = quest_id[i]
            name = db.quest_name[id]
            tokens: List[ItemType] = [i for i in db.normal_quest_rewards[id]]
            msg = f"{name}:\n" + '\n'.join([
                (f'{db.get_inventory_name_san(token)}: {"缺少" if require_equip[token] > 0 else "盈余"}{abs(require_equip[token])}片')
                for token in tokens])
            tot.append(msg.strip())

        msg = '\n--------\n'.join(tot)
        self._log(msg)
