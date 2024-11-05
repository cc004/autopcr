from typing import List, Set

from ...util.ilp_solver import dispatch_solver

from ...model.common import ChangeRarityUnit, DeckListData, GrandArenaHistoryDetailInfo, GrandArenaHistoryInfo, GrandArenaSearchOpponent, ProfileUserInfo, RankingSearchOpponent, TravelDecreaseItem, TravelStartInfo, VersusResult, VersusResultDetail
from ...model.responses import PsyTopResponse
from ...db.models import GachaExchangeLineup
from ...model.custom import ArenaQueryResult, GachaReward, ItemType
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.arena import instance as ArenaQuery
import datetime
import random
from collections import Counter

@name('计算探险编队')
@default(True)
@booltype('travel_team_view_go', '探险出发', False)
@multichoice('travel_team_view_quest_id', '探险任务', [], db.travel_quest_candidate)
@booltype('travel_team_view_auto_memory', '自动设置记忆碎片', True)
@description('根据设定的记忆碎片优先级，从剩余可派遣角色中自动计算战力平衡编队，自动设置记忆碎片指记忆碎片优先度不足够派出队伍时，根据盈亏情况补充，探险出发指以计算出的编队出发')
class travel_team_view(Module):
    async def do_task(self, client: pcrclient):
        travel_team_auto_memory = self.get_config('travel_team_view_auto_memory')
        travel_team_go = self.get_config('travel_team_view_go')
        travel_quest_id_raw: List[str] = self.get_config('travel_team_view_quest_id')
        travel_quest_id = [db.get_travel_quest_id_from_candidate(x) for x in travel_quest_id_raw]

        top = await client.travel_top(max(db.get_open_travel_area()), 1)
        unit_list = top.priority_unit_list

        memory_gap = client.data.get_memory_demand_gap()
        if unit_list:
            memory_need = []
            for unit in unit_list:
                token = (eInventoryType.Item, db.unit_to_memory[unit])
                memory_need.append((token, memory_gap[token]))
            msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in memory_need])
            self._log(f"记忆碎片优先级的盈缺情况：\n{msg}")
            self._log("----")

        if top.travel_quest_list:
            self._log('当前派遣区域：')
            for quest in top.travel_quest_list:
                import time
                now = int(time.time())
                leave_time = int(quest.travel_end_time - quest.decrease_time - now)
                self._log(f"{db.get_quest_name(quest.travel_quest_id)} -{db.format_second(leave_time)}")
                if quest.travel_quest_id in travel_quest_id: travel_quest_id.remove(quest.travel_quest_id)

        teams_go = 3 - len(top.travel_quest_list)
        if not teams_go:
            raise AbortError("已经派遣了3支队伍")
        if teams_go < len(travel_quest_id):
            raise AbortError(f"可派队伍数量{teams_go}<需派图数{travel_quest_id}")
        teams_go = len(travel_quest_id)

        memory_unit = 3 * teams_go

        forbid_unit = []
        for quest in top.travel_quest_list:
            forbid_unit.extend(quest.travel_deck)
        forbid_unit = set(forbid_unit)

        unit_list = [unit for unit in unit_list if unit not in forbid_unit][:memory_unit]
        if len(unit_list) != memory_unit:
            if not travel_team_auto_memory:
                raise AbortError(f"设置的未派遣的记忆碎片优先级的角色不足{memory_unit}个，请前往游戏里设置更多角色")
            else:
                leave = memory_unit - len(unit_list)
                new_unit = sorted(
                        [unit_id for unit_id in client.data.unit if unit_id not in unit_list and unit_id not in forbid_unit], 
                        key=lambda x: memory_gap[(eInventoryType.Item, db.unit_to_memory[x])], 
                        reverse=True)[:leave]
                msg = f"设置的未派遣的记忆碎片优先级的角色不足{memory_unit}个，将根据盈亏情况补充以下角色：\n"
                msg += ' '.join(f"{db.get_unit_name(unit)}" for unit in new_unit)
                self._log(msg)
                unit_list.extend(new_unit)
                await client.travel_update_priority_unit_list(unit_list)

        unit_power = {unit: client.data.get_unit_power(unit) for unit in client.data.unit}
        unit_list.sort(key=lambda x: unit_power[x], reverse=True)

        teams = [
            unit_list[st::3] for st in range(teams_go)
        ]

        start_power = [sum(unit_power[unit] for unit in teams[i]) for i in range(teams_go)]
        candidate_unit_id = sorted([unit_id for unit_id in unit_power if unit_id not in unit_list and unit_id not in forbid_unit], key=lambda x: unit_power[x], reverse=True)[:teams_go * 7]
        candidate_unit_power = [unit_power[unit] for unit in candidate_unit_id]

        lb = [db.travel_quest_data[quest].need_power for quest in travel_quest_id]
        ret, sol = dispatch_solver(start_power, candidate_unit_power, lb, 7)
        if not ret:
            raise AbortError(f"无法凑出战力满足最低要求的{teams_go}支队伍！")
        for pos, unit in zip(sol, candidate_unit_id):
            teams[pos].append(unit)

        teams_power = [sum(unit_power[unit] for unit in teams[i]) for i in range(teams_go)]

        for id, (team, power) in enumerate(zip(teams, teams_power), start=1):
            time = db.format_second(db.calc_travel_once_time(power))
            self._log(f"第{id}队({time})总战力{power}=" + '+'.join(f"{unit_power[unit]}" for unit in team))
            self._log(' '.join(f"{db.get_unit_name(unit)}" for unit in team))

        if travel_team_go:
            self._log('----')

            start_travel_quest_list: List[TravelStartInfo] = []
            for id, (team, quest) in enumerate(zip(teams, travel_quest_id), start = 1):
                start_item = TravelStartInfo(
                        travel_quest_id = quest,
                        travel_deck = team,
                        decrease_time_item = TravelDecreaseItem(jewel = 0, item = 0),
                        total_lap_count = client.data.settings.travel.travel_quest_max_repeat_count,
                 )
                start_travel_quest_list.append(start_item)

            action_type = eTravelStartType.NORMAL
            msg = '\n'.join(f"派遣第{id}队到{db.get_quest_name(quest.travel_quest_id)}x{quest.total_lap_count}" for id, quest in enumerate(start_travel_quest_list, start = 1))
            self._log(msg)
            await client.travel_start(start_travel_quest_list, [], [], action_type)


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

@description('看看你缺了什么角色')
@name('查缺角色')
@default(True)
class missing_unit(Module):
    async def do_task(self, client: pcrclient):
        missing_unit = set(db.unlock_unit_condition.keys()) - set(client.data.unit.keys())
        if not missing_unit:
            self._log("全图鉴玩家！你竟然没有缺少的角色！")
        else:
            limit_unit = set(id for id in missing_unit if db.unit_data[id].is_limited)
            resident_unit = missing_unit - limit_unit
            self._log(f"缺少{len(missing_unit)}个角色，其中{len(limit_unit)}个限定角色，{len(resident_unit)}个常驻角色")
            if limit_unit:
                self._log(f"==限定角色==" )
                self._log('\n'.join(db.get_unit_name(id) for id in limit_unit))
                self._log('')
            if resident_unit:
                self._log(f"==常驻角色==" )
                self._log('\n'.join(db.get_unit_name(id) for id in resident_unit))

@description('警告！真抽！抽到出指NEW出保底角色，或达天井停下来，如果已有保底角色，就不会NEW！意味着就是一井！')
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
            self._log(await client.serlize_gacha_reward(reward, target_gacha.id))
            point = client.data.gacha_point[target_gacha.exchange_id].current_point if target_gacha.exchange_id in client.data.gacha_point else 0
            self._log(f"当前pt为{point}")

@description('查看会战支援角色的详细数据，拒绝内鬼！')
@name('会战支援数据')
@default(True)
class get_clan_support_unit(Module):
    async def do_task(self, client: pcrclient):
        await client.get_clan_battle_top(1, client.data.get_shop_gold(eSystemId.CLAN_BATTLE_SHOP))
        unit_list = await client.get_clan_battle_support_unit_list()
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

        if target_rank > 0:
            target = await self.get_rank_info(client, target_rank)
            target_info = (await client.get_profile(target.viewer_id)).user_info
            self._log(f"{target_info.user_name}({target.viewer_id})")
            self._log(f"{self_rank} -> {target_rank}({target_info.user_name})")
            defend = await self.get_defend_from_info(target)
        else:
            historys = await self.get_arena_history(client)
            if not historys:
                raise AbortError("没有被刺记录")
            id = -target_rank
            if id == 0:
                for i, h in enumerate(historys):
                    h_detail = await self.get_history_detail(h.log_id, client)
                    if h_detail.is_challenge:
                        self._log(f"查找第{i + 1}条记录")
                        history = h
                        history_detail = h_detail
                        break
                else:
                    raise AbortError("没有刺人记录")
            else:
                self._log(f"查找第{id}条记录")
                if len(historys) < id:
                    raise AbortError(f"只有{len(historys)}条被刺记录")
                history = historys[id - 1]
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
        if best_team_id >= 0 and best_team_id < len(attack):
            self._log(f"选择第{best_team_id + 1}支队伍作为进攻方队伍")
            await self.update_deck(attack[best_team_id], client)
        else:
            self._warn(f"队伍只有{len(attack)}支，无法选择第{best_team_id + 1}支队伍作为进攻方队伍")

        attack_str = self.present_attack(attack[:max(8, best_team_id + 1)])
        msg = [defend_str, "-------", attack_str]
        self._log('\n'.join(msg))

@description('查询jjc回刺阵容，并自动设置进攻队伍，对手排名=0则查找对战纪录第一条刺人的，<0则查找对战纪录，-1表示第一条，-2表示第二条，以此类推')
@name('jjc回刺查询')
@default(True)
@inttype("opponent_jjc_attack_team_id", "选择阵容", 1, [i for i in range(1, 10)])
@inttype("opponent_jjc_rank", "对手排名", -1, [i for i in range(-20, 101)])
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
        id = int(self.get_config("opponent_jjc_attack_team_id")) - 1
        return id

    async def update_deck(self, units: ArenaQueryResult, client: pcrclient):
        units_id = [unit.id for unit in units.atk]
        star_change_unit = [unit_id for unit_id in units_id if client.data.unit[unit_id].unit_rarity == 5 and client.data.unit[unit_id].battle_rarity != 0]
        if star_change_unit:
            res = [ChangeRarityUnit(unit_id=unit_id, battle_rarity=5) for unit_id in star_change_unit]
            self._log(f"将{'|'.join([db.get_unit_name(unit_id) for unit_id in star_change_unit])}调至5星")
            await client.unit_change_rarity(res)

        under_rank_bonus_unit = [unit for unit in units_id if client.data.unit[unit].promotion_level < db.equip_max_rank - 1]
        if under_rank_bonus_unit:
            self._warn(f"无品级加成：{'，'.join([db.get_unit_name(unit_id) for unit_id in under_rank_bonus_unit])}")

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

@description('查询pjjc回刺阵容，并自动设置进攻队伍，对手排名=0则查找对战纪录第一条刺人的，<0则查找对战纪录，-1表示第一条，-2表示第二条，以此类推')
@name('pjjc回刺查询')
@default(True)
@inttype("opponent_pjjc_attack_team_id", "选择阵容", 1, [i for i in range(1, 10)])
@inttype("opponent_pjjc_rank", "对手排名", -1, [i for i in range(-20, 101)])
class pjjc_back(Arena):
    def target_rank(self) -> int:
        return self.get_config("opponent_pjjc_rank")

    def present_defend(self, defen: List[List[int]]) -> str:
        msg = [' '.join([db.get_unit_name(y) for y in x]) for x in defen]
        msg = '\n'.join(msg)
        msg = f"防守方\n{msg}"
        return msg

    def present_attack(self, attack: List[List[ArenaQueryResult]]) -> str:
        msg = [f"第{id + 1}对策\n{ArenaQuery.str_result(x)}" for id, x in enumerate(attack)]
        msg = '\n\n'.join(msg)
        return msg

    def get_rank_from_user_info(self, user_info: ProfileUserInfo) -> int:
        return user_info.grand_arena_rank 

    async def self_rank(self, client: pcrclient) -> int:
        return (await client.get_grand_arena_info()).grand_arena_info.rank

    async def choose_best_team(self, team: List[List[ArenaQueryResult]], rank_id: List[int], client: pcrclient) -> int:
        id = int(self.get_config("opponent_pjjc_attack_team_id")) - 1
        return id

    async def update_deck(self, units: List[ArenaQueryResult], client: pcrclient):
        units_id = [[uni.id for uni in unit.atk] for unit in units]
        star_change_unit = [uni_id for unit_id in units_id for uni_id in unit_id if 
                            client.data.unit[uni_id].unit_rarity == 5 and 
                            client.data.unit[uni_id].battle_rarity != 0]
        if star_change_unit:
            res = [ChangeRarityUnit(unit_id=unit_id, battle_rarity=5) for unit_id in star_change_unit]
            self._log(f"将{'|'.join([db.get_unit_name(unit_id) for unit_id in star_change_unit])}调至5星")
            await client.unit_change_rarity(res)

        under_rank_bonus_unit = [uni_id for unit_id in units_id for uni_id in unit_id if 
                                 client.data.unit[uni_id].promotion_level < db.equip_max_rank - 1]
        if under_rank_bonus_unit:
            self._warn(f"无品级加成：{'，'.join([db.get_unit_name(unit_id) for unit_id in under_rank_bonus_unit])}")

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

@description('将pjjc防守阵容随机错排')
@name('pjjc换防')
class pjjc_shuffle_team(Module):
    async def do_task(self, client: pcrclient):
        ids = random.choice([ [1, 2, 0], [2, 0, 1] ])
        deck_list: List[DeckListData] = []
        cnt = 3
        for i in range(cnt):
            deck_number = getattr(ePartyType, f"GRAND_ARENA_DEF_{i + 1}")
            units = client.data.deck_list[deck_number]
            units_id = [getattr(units, f"unit_id_{i + 1}") for i in range(5)]

            deck = DeckListData()
            deck_number = getattr(ePartyType, f"GRAND_ARENA_DEF_{ids[i] + 1}")
            deck.deck_number = deck_number
            deck.unit_list = units_id
            deck_list.append(deck)

        deck_list.sort(key=lambda x: x.deck_number)
        self._log('\n'.join([f"{i} -> {j}" for i, j in enumerate(ids)]))
        await client.deck_update_list(deck_list)


@description('获得可导入到兰德索尔图书馆的账号数据')
@name('兰德索尔图书馆导入数据')
@default(True)
@text_result
class get_library_import_data(Module):
    async def do_task(self, client: pcrclient):
        msg = client.data.get_library_import_data()
        self._log(msg)

@description('根据每个角色拉满星级、开专、升级至当前最高专所需的记忆碎片减去库存的结果')
@singlechoice('memory_demand_consider_unit', '考虑角色', '所有', ['所有', '地图可刷取', '大师币商店'])
@name('获取记忆碎片缺口')
@default(True)
class get_need_memory(Module):
    async def do_task(self, client: pcrclient):
        demand = list(client.data.get_memory_demand_gap().items())
        demand = sorted(demand, key=lambda x: x[1], reverse=True)
        consider = self.get_config("memory_demand_consider_unit")
        msg = {}
        if consider == "地图可刷取":
            demand = [i for i in demand if i[0] in db.memory_hard_quest or i[0] in db.memory_shiori_quest]
        elif consider == "大师币商店":
            shop_content = await client.get_shop_item_list()
            master_shops = [shop for shop in shop_content.shop_list if shop.system_id == eSystemId.COUNTER_STOP_SHOP]
            if not master_shops:
                raise AbortError("大师币商店未开启")
            master_shop = master_shops[0]
            master_shop_item = set((item.type, item.item_id) for item in master_shop.item_list)
            msg = {(item.type, item.item_id): "已买" for item in master_shop.item_list if item.sold}
            demand = [i for i in demand if i[0] in master_shop_item]

        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片{("(" + msg[item[0]] + ")") if item[0] in msg else ""}' for item in demand])
        self._log(msg)

@description('根据每个角色升六星（国服当前）、满二专（日服当前）所需的纯净碎片减去库存的结果')
@name('获取纯净碎片缺口')
@default(True)
class get_need_pure_memory(Module):
    async def do_task(self, client: pcrclient):
        from .autosweep import unique_equip_2_pure_memory_id
        need_list = client.data.get_pure_memory_demand_gap()
        need_list.update(Counter({(eInventoryType.Item, pure_memory_id): 150 * cnt for pure_memory_id, cnt in unique_equip_2_pure_memory_id}))
        demand = list(need_list.items())
        demand = sorted(demand, key=lambda x: x[1], reverse=True)
        msg = {}
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

        piece = client.data.get_inventory(db.xinsui)
        heart = client.data.get_inventory(db.heart)
        store = piece + heart * 10
        cnt = need - store
        tot = f"当前心碎数量为{store}={piece}+{heart}*10，需要{need}，"
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
            name = db.get_quest_name(id)
            tokens: List[ItemType] = [i for i in db.normal_quest_rewards[id]]
            msg = f"{name}:\n" + '\n'.join([
                (f'{db.get_inventory_name_san(token)}: {"缺少" if require_equip[token] > 0 else "盈余"}{abs(require_equip[token])}片')
                for token in tokens])
            tot.append(msg.strip())

        msg = '\n--------\n'.join(tot)
        self._log(msg)


@description('从指定面板的指定队开始设置。6行重复，标题+5行角色ID	角色名字	角色等级	角色星级')
@texttype("set_my_party_text", "队伍阵容", "")
@inttype("party_start_num", "初始队伍", 1, [i for i in range(1, 11)])
@inttype("tab_start_num", "初始面板", 1, [i for i in range(1, 7)])
@name('设置编队')
class set_my_party(Module):
    async def do_task(self, client: pcrclient):
        set_my_party_text: str = self.get_config('set_my_party_text')
        tab_number: int = self.get_config('tab_start_num')
        party_number: int = self.get_config('party_start_num') - 1
        party = set_my_party_text.splitlines()
        for i in range(0, len(party), 6):

            party_number += 1
            if party_number == 11:
                tab_number += 1
                party_number = 1
                if tab_number >= 6:
                    raise AbortError("队伍数量超过上限")

            title = party[i] + "记得借人"
            unit_list = [u.split('\t') for u in party[i + 1 : i + 1 + 5]]

            own_unit = [u for u in unit_list if int(u[0]) in client.data.unit]
            not_own_unit = [u for u in unit_list if int(u[0]) not in client.data.unit]
            if not_own_unit:
                self._warn(f"{title}未持有：{', '.join([u[1] for u in not_own_unit])}")

            change_rarity_list = []
            unit_list = []
            for unit in own_unit:
                id = int(unit[0])
                star = int(unit[3])
                unit_data = client.data.unit[id]
                can_change_star = unit_data.unit_rarity == 5
                now_star = unit_data.battle_rarity if unit_data.battle_rarity else unit_data.unit_rarity
                if can_change_star and star != now_star:
                    if star >= 3 and star <= 5 and now_star >= 3 and now_star <= 5:
                        change_rarity = ChangeRarityUnit(unit_id=id, battle_rarity=star)
                        change_rarity_list.append(change_rarity)
                    else:
                        self._warn(f"{title}：{unit[1]}星级无法{now_star} -> {star}")
                unit_list.append(id)

            if change_rarity_list:
                await client.unit_change_rarity(change_rarity_list)
            if not unit_list:
                self._warn(f"{title}没有可用的角色")
            else:
                await client.set_my_party(tab_number, party_number, 4, title, unit_list, change_rarity_list)
                self._log(f"设置了{title}")
