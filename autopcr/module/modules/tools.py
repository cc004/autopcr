from typing import List, Set

from ...model.common import ChangeRarityUnit, DeckListData, GrandArenaHistoryDetailInfo, GrandArenaHistoryInfo, GrandArenaSearchOpponent, ProfileUserInfo, RankingSearchOpponent, VersusResult, VersusResultDetail
from ...model.responses import PsyTopResponse
from ...db.models import GachaExchangeLineup
from ...model.custom import ArenaQueryResult, ArenaRegion, GachaReward, ItemType
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.arena import instance as ArenaQuery
import datetime

@name('【活动限时】一键做布丁')
@default(True)
@description('一键做+吃布丁，直到清空你的材料库存。<br/>顺便还能把剧情也看了。')
class cook_pudding(Module):
    async def do_task(self, client: pcrclient):
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
            if event.event_id != 10080:
                continue
            else:
                is_skip = False
                event_active = True
            resp = await client.get_hatsune_top(event.event_id)

            nboss_id = event.event_id * 100 + 1
            boss_info = {boss.boss_id: boss for boss in resp.boss_battle_info}

            async def read_drama(psy_top_resp: PsyTopResponse):
                drama_list = [item.drama_id for item in psy_top_resp.drama_list if item.read_status == 0]
                if len(drama_list) != 0:
                    for did in drama_list:
                        await client.psy_read_drama(did)
                return len(drama_list)

            try:
                if not boss_info[nboss_id].is_unlocked:
                    raise AbortError(f"n本boss未解锁")
                if not boss_info[nboss_id].kill_num:
                    raise AbortError(f"n本boss未首通")

                resp = await client.psy_top()
                stock = client.data.get_inventory((eInventoryType.Item, int(resp.psy_setting.material_item_id)))
                if stock < 1:
                    read_cnt = await read_drama(resp)
                    raise AbortError(f"材料不足。\n阅读了{read_cnt}个剧情。")

                cooking_frame = []
                for item in resp.cooking_status:
                    cooking_frame.append(item.frame_id)
                if len(cooking_frame) != 0:
                    await client.get_pudding(cooking_frame)

                times = (stock // int(resp.psy_setting.use_material_count)) // 24
                over = (stock // int(resp.psy_setting.use_material_count)) % 24

                if times > 0:
                    for i in range(times):
                        frame_list = [x for x in range(1, 25)]
                        await client.start_cooking(frame_list)
                        await client.get_pudding(frame_list)

                if over > 0:
                    frame_list = [x for x in range(1, over + 1)]
                    await client.start_cooking(frame_list)
                    await client.get_pudding(frame_list)

                resp = await client.psy_top()
                read_cnt = await read_drama(resp)

                self._log(f"做了{times * 24 + over}个布丁。\n阅读了{read_cnt}个剧情。")

            except SkipError as e:
                self._log(f"{event.event_id}: {str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{event.event_id}: {str(e)}")
            except Exception as e:
                is_error = True
                self._log(f"{event.event_id}: {str(e)}")

        if not event_active: raise SkipError("当前无进行中的活动。")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")


@description('来进行赛博抽卡')
@name('抽卡')
@booltype("single_ticket", "用单抽券", False)
@singlechoice("pool_id", "池子", "", db.get_cur_gacha)
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
        single_ticket = self.get_config('single_ticket')
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
                if single_ticket:
                    reward += await client.exec_gacha_aware(target_gacha, 1, eGachaDrawType.Ticket, client.data.get_inventory(db.gacha_single_ticket), 0)
                else:
                    if resp.campaign_info and resp.campaign_info.fg10_exec_cnt:
                        raise AbortError("当前可免费十连，请先自行抽取")
                    reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Payment, client.data.jewel.free_jewel + client.data.jewel.jewel, 0)
                cnt += 1
                if not always or self.can_stop(reward.new_unit, db.gacha_exchange_chara[target_gacha.exchange_id]) :
                    break
        except:
            raise 
        finally:
            self._log(f"抽取了{cnt}次{'十连' if not single_ticket else '单抽'}")
            self._log(await client.serlize_gacha_reward(reward))
            point = client.data.gacha_point[target_gacha.exchange_id].current_point if target_gacha.exchange_id in client.data.gacha_point else 0
            self._log(f"当前pt为{point}")

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

class Arena(Module):

    def target_rank(self) -> int: ...

    def present_defend(self, defen: Union[List[List[int]], List[int]]) -> str: ...

    def present_attack(self, attack: Union[List[List[ArenaQueryResult]], List[ArenaQueryResult]]) -> str: ...

    def get_rank_from_user_info(self, user_info: ProfileUserInfo) -> int: ...

    async def self_rank(self, client: pcrclient) -> int: ...

    async def choose_best_team(self, team: Union[List[ArenaQueryResult], List[List[ArenaQueryResult]]], rank_id: List[int], client: pcrclient) -> int: ...

    async def update_deck(self, units: Union[List[ArenaQueryResult], ArenaQueryResult], client: pcrclient): ...

    async def get_rank_info(self, client: pcrclient, rank: int) -> Union[RankingSearchOpponent, GrandArenaSearchOpponent]: ...

    async def get_opponent_info(self, client: pcrclient, viewer_id: int) -> Union[RankingSearchOpponent, GrandArenaSearchOpponent]: ...

    async def get_arena_history(self, client: pcrclient) -> Union[List[VersusResult], List[GrandArenaHistoryInfo]]: ...

    async def get_history_detail(self, log_id: int, client: pcrclient) -> Union[VersusResultDetail, GrandArenaHistoryDetailInfo]: ...

    async def get_defend_from_info(self, info: Union[RankingSearchOpponent, GrandArenaSearchOpponent]) -> Union[List[List[int]], List[int]]: ...

    async def get_defend_from_histroy_detail(self, history_detail: Union[VersusResultDetail, GrandArenaHistoryDetailInfo]) -> Union[List[List[int]], List[int]]: ...


    async def get_attack_team(self, defen: Union[List[List[int]], List[int]]) -> Union[List[List[ArenaQueryResult]], List[ArenaQueryResult]]: ...

    async def get_defend(self, client: pcrclient) -> Union[List[List[int]], List[int]]:
        target_rank: int = self.target_rank()
        self_rank = await self.self_rank(client)

        if target_rank:
            target = await self.get_rank_info(client, target_rank)
            target_info = (await client.get_profile(target.viewer_id)).user_info
            self._log(f"{target_info.user_name}({target.viewer_id})")
            self._log(f"{self_rank} -> {target_rank}({target_info.user_name})")
            defend = await self.get_defend_from_info(target)
        else:
            history = await self.get_arena_history(client)
            if not history:
                raise SkipError("没有被刺记录")
            history = history[0]
            history_detail = await self.get_history_detail(history.log_id, client)
            target = history.opponent_user

            target_info = (await client.get_profile(target.viewer_id)).user_info
            target_rank = self.get_rank_from_user_info(target_info)

            self._log(f"{target.user_name}({target.viewer_id})\n{datetime.datetime.fromtimestamp(history.versus_time)} {'刺' if history_detail.is_challenge else '被刺'}")
            self._log(f"{self_rank} -> {target_rank}({target_info.user_name})")

            if history_detail.is_challenge:
                defend = await self.get_defend_from_histroy_detail(history_detail)
            else:
                target = await self.get_opponent_info(client, target.viewer_id)
                defend = await self.get_defend_from_info(target)


        if isinstance(defend[0], list):
            defend = [d[-5:] for d in defend]
        else:
            defend = defend[-5:]

        return defend


    async def do_task(self, client: pcrclient):
        self.available_unit: Set[int] = set(unit_id for unit_id in client.data.unit if client.data.unit[unit_id].promotion_level >= 7)

        defend = await self.get_defend(client)
        attack = await self.get_attack_team(defend)

        defend_str = self.present_defend(defend)

        if attack == []:
            raise AbortError(f'{defend_str}\n抱歉没有查询到解法\n※没有作业说明随便拆 发挥你的想象力～★\n')

        rank_id = list(range(len(attack)))
        best_team_id = await self.choose_best_team(attack, rank_id, client)
        if best_team_id >= 0: # it always be the first one now
            self._log(f"选择第{best_team_id + 1}支队伍作为进攻方队伍")
            await self.update_deck(attack[best_team_id], client)
        else:
            self._log("未找到合适队伍，请自行选择")

        attack_str = self.present_attack(attack[:max(8, best_team_id + 1)])
        msg = [defend_str, "-------", attack_str]
        self._log('\n'.join(msg))

@description('查询jjc回刺阵容，并自动设置进攻队伍，对手排名0则查找对战纪录第一条')
@name('jjc回刺查询')
@default(True)
@inttype("opponent_jjc_rank", "对手排名", 0, [i for i in range(0, 101)])
class jjc_back(Arena):

    def target_rank(self) -> int:
        return self.get_config("opponent_jjc_rank")

    async def self_rank(self, client: pcrclient) -> int: 
        return (await client.get_arena_info()).arena_info.rank

    def get_rank_from_user_info(self, user_info: ProfileUserInfo) -> int:
        return user_info.arena_rank 

    def present_defend(self, defen: List[int]) -> str:
        msg = [db.get_unit_name(x) for x in defen]
        msg = f"防守方【{' '.join(msg)}】"
        return msg

    def present_attack(self, attack: List[ArenaQueryResult]) -> str:
        msg = ArenaQuery.str_result(attack)
        return msg

    async def choose_best_team(self, team: List[ArenaQueryResult], rank_id: List[int], client: pcrclient) -> int: 
        all_have = [id for id in rank_id if all(
            unit.id in client.data.unit and 
            client.data.unit[unit.id].promotion_level > 7 
            for unit in team[id].atk)]
        return -1 if not all_have else all_have[0]

    async def update_deck(self, units: ArenaQueryResult, client: pcrclient):
        units_id = [unit.id for unit in units.atk]
        star_change_unit = [unit for unit in units_id if client.data.unit[unit].unit_rarity == 5 and client.data.unit[unit].battle_rarity != 0]
        if star_change_unit:
            res = [ChangeRarityUnit(unit_id=unit_id, battle_rarity=5) for unit_id in star_change_unit]
            self._log(f"将{'|'.join([db.get_unit_name(unit_id) for unit_id in star_change_unit])}调至5星")
            await client.unit_change_rarity(res)
        await client.deck_update(ePartyType.ARENA, units_id)

    async def get_rank_info(self, client: pcrclient, rank: int) -> RankingSearchOpponent: 
        for page in range(1, 6):
            ranking = {info.rank: info for info in (await client.arena_rank(20, page)).ranking}
            if rank in ranking:
                return ranking[rank]
        raise AbortError("对手不在前100名，无法查询")

    async def get_opponent_info(self, client: pcrclient, viewer_id: int) -> RankingSearchOpponent: 
        for page in range(1, 6):
            ranking = {info.viewer_id: info for info in (await client.arena_rank(20, page)).ranking}
            if viewer_id in ranking:
                return ranking[viewer_id]
        raise AbortError("对手不在前100名，无法查询")

    async def get_arena_history(self, client: pcrclient) -> List[VersusResult]:
        return (await client.get_arena_history()).versus_result_list

    async def get_history_detail(self, log_id: int, client: pcrclient) -> VersusResultDetail:
        return (await client.get_arena_history_detail(log_id)).versus_result_detail

    async def get_defend_from_info(self, info: RankingSearchOpponent) -> List[int]:
        return [unit.id for unit in info.arena_deck]

    async def get_defend_from_histroy_detail(self, history_detail: VersusResultDetail) -> List[int]:
        return [unit.id for unit in history_detail.vs_user_arena_deck]

    async def get_attack_team(self, defen: List[int]) -> List[ArenaQueryResult]:
        return await ArenaQuery.get_attack(self.available_unit, defen)

@description('查询pjjc回刺阵容，并自动设置进攻队伍，对手排名0则查找对战纪录第一条')
@name('pjjc回刺查询')
@default(True)
@inttype("opponent_pjjc_rank", "对手排名", 0, [i for i in range(0, 101)])
class pjjc_back(Arena):
    def target_rank(self) -> int:
        return self.get_config("opponent_pjjc_rank")

    def present_defend(self, defen: List[List[int]]) -> str:
        msg = [' '.join([db.get_unit_name(y) for y in x]) for x in defen]
        msg = '\n'.join(msg)
        msg = f"防守方\n{msg}"
        return msg

    def present_attack(self, attack: List[List[ArenaQueryResult]]) -> str:
        msg = [ArenaQuery.str_result(x) for x in attack]
        msg = '\n\n'.join(msg)
        return msg

    def get_rank_from_user_info(self, user_info: ProfileUserInfo) -> int:
        return user_info.grand_arena_rank 

    async def self_rank(self, client: pcrclient) -> int:
        return (await client.get_grand_arena_info()).grand_arena_info.rank

    async def choose_best_team(self, team: List[List[ArenaQueryResult]], rank_id: List[int], client: pcrclient) -> int:
        all_have = [id for id in rank_id if all(
            unit.id in client.data.unit and 
            client.data.unit[unit.id].promotion_level > 7
            for units in team[id] 
                for unit in units.atk)]
        return -1 if not all_have else all_have[0]

    async def update_deck(self, units: List[ArenaQueryResult], client: pcrclient):
        units_id = [[uni.id for uni in unit.atk] for unit in units]
        star_change_unit = [uni_id for unit_id in units_id for uni_id in unit_id if 
                            client.data.unit[uni_id].unit_rarity == 5 and 
                            client.data.unit[uni_id].battle_rarity != 0]
        if star_change_unit:
            res = [ChangeRarityUnit(unit_id=unit_id, battle_rarity=5) for unit_id in star_change_unit]
            self._log(f"将{'|'.join([db.get_unit_name(unit_id) for unit_id in star_change_unit])}调至5星")
            await client.unit_change_rarity(res)

        deck_list = []
        for i, unit_id in enumerate(units_id):
            deck_number = getattr(ePartyType, f"GRAND_ARENA_{i + 1}")
            sorted_unit_id = db.deck_sort_unit(unit_id)

            deck = DeckListData()
            deck.deck_number = deck_number
            deck.unit_list = sorted_unit_id
            deck_list.append(deck)

        await client.deck_update_list(deck_list)

    async def get_rank_info(self, client: pcrclient, rank: int) -> GrandArenaSearchOpponent:
        for page in range(1, 6):
            ranking = {info.rank: info for info in (await client.grand_arena_rank(20, page)).ranking}
            if rank in ranking:
                return ranking[rank]
        raise AbortError("对手不在前100名，无法查询")

    async def get_opponent_info(self, client: pcrclient, viewer_id: int) -> GrandArenaSearchOpponent:
        for page in range(1, 6):
            ranking = {info.viewer_id: info for info in (await client.grand_arena_rank(20, page)).ranking}
            if viewer_id in ranking:
                return ranking[viewer_id]
        # raise AbortError("对手不在前100名，无法查询")
        ret = GrandArenaSearchOpponent(viewer_id=viewer_id)
        return ret

    async def get_arena_history(self, client: pcrclient) -> List[GrandArenaHistoryInfo]:
        return (await client.get_grand_arena_history()).grand_arena_history_list

    async def get_history_detail(self, log_id: int, client: pcrclient) -> GrandArenaHistoryDetailInfo:
        return (await client.get_grand_arena_history_detail(log_id)).grand_arena_history_detail

    async def get_defend_from_info(self, info: GrandArenaSearchOpponent) -> List[List[int]]:
        ret = []
        if info.grand_arena_deck:
            if info.grand_arena_deck.first and info.grand_arena_deck.first[0].id != 2:
                ret.append([unit.id for unit in info.grand_arena_deck.first])
            if info.grand_arena_deck.second and info.grand_arena_deck.second[0].id != 2:
                ret.append([unit.id for unit in info.grand_arena_deck.second])
            if info.grand_arena_deck.third and info.grand_arena_deck.third[0].id != 2:
                ret.append([unit.id for unit in info.grand_arena_deck.third])
        
        if len(ret) < 2:
            ret = self.find_cache(str(info.viewer_id))
            if ret is None:
                raise AbortError("未知的对手防守，请尝试进攻一次")
            print("读取缓存队伍阵容")
        return ret

    async def get_defend_from_histroy_detail(self, history_detail: GrandArenaHistoryDetailInfo) -> List[List[int]]:
        ret = []
        if history_detail.vs_user_grand_arena_deck.first[0].id != 2:
            ret.append([unit.id for unit in history_detail.vs_user_grand_arena_deck.first])
        if history_detail.vs_user_grand_arena_deck.second[0].id != 2:
            ret.append([unit.id for unit in history_detail.vs_user_grand_arena_deck.second])
        if history_detail.vs_user_grand_arena_deck.third[0].id != 2:
            ret.append([unit.id for unit in history_detail.vs_user_grand_arena_deck.third])
        self.save_cache(str(history_detail.vs_user_viewer_id), ret)
        return ret

    async def get_attack_team(self, defen: List[List[int]]) -> List[List[ArenaQueryResult]]:
        return await ArenaQuery.get_multi_attack(self.available_unit, defen)

class ArenaInfo(Module):

    @property
    def use_cache(self) -> bool: ...
    
    async def get_rank_info(self, client: pcrclient, num: int, page: int) -> List[Union[GrandArenaSearchOpponent, RankingSearchOpponent]]: ...
    
    async def get_user_info(self, client: pcrclient, viewer_id: int) -> str: 
        user_name = self.find_cache(str(viewer_id))
        if user_name is None or not self.use_cache:
            user_name = (await client.get_profile(viewer_id)).user_info.user_name
            self.save_cache(str(viewer_id), user_name)
        return user_name

    async def do_task(self, client: pcrclient):
        time = db.format_time(datetime.datetime.now())
        self._log(f"时间：{time}")
        for page in range(1, 4):
            ranking = await self.get_rank_info(client, 20, page)
            for info in ranking:
                if info.rank > 51:
                    break
                user_name = await self.get_user_info(client, info.viewer_id)
                you = " <--- 你" if info.viewer_id == client.data.uid else ""
                self._log(f"{info.rank:02}: ({info.viewer_id}){user_name}{you}")

@booltype("jjc_info_cache", "使用缓存信息", True)
@description('jjc透视前51名玩家的名字')
@name('jjc透视')
@default(True)
class jjc_info(ArenaInfo):
    @property
    def use_cache(self) -> bool: return self.get_config("jjc_info_cache")

    async def get_rank_info(self, client: pcrclient, num: int, page: int) -> List[RankingSearchOpponent]:
        return (await client.arena_rank(num, page)).ranking

@booltype("pjjc_info_cache", "使用缓存信息", True)
@description('pjjc透视前51名玩家的名字')
@name('pjjc透视')
@default(True)
class pjjc_info(ArenaInfo):
    @property
    def use_cache(self) -> bool: return self.get_config("pjjc_info_cache")

    async def get_rank_info(self, client: pcrclient, num: int, page: int) -> List[GrandArenaSearchOpponent]:
        return (await client.grand_arena_rank(num, page)).ranking


@description('获得可导入到兰德索尔图书馆的账号数据')
@name('兰德索尔图书馆导入数据')
@default(True)
@text_result
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
            demand = [i for i in demand if i[0] in db.memory_hard_quest or i[0] in db.memory_shiori_quest]

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
