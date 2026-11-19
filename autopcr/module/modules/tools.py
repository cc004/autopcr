from typing import Dict, List, Set

from ...util.ilp_solver import memory_use_average

from ...model.common import ChangeRarityUnit, DeckListData, GachaPointInfo, GrandArenaHistoryDetailInfo, GrandArenaHistoryInfo, GrandArenaSearchOpponent, ProfileUserInfo, RankingSearchOpponent, RedeemUnitInfo, RedeemUnitSlotInfo, UnitData, UnitDataLight, VersusResult, VersusResultDetail
from ...model.responses import GachaIndexResponse, PsyTopResponse
from ...db.models import GachaExchangeLineup
from ...model.custom import ArenaQueryResult, GachaReward, ItemType, eRedeemUnitUnlockCondition
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
import random
import itertools
import re
from collections import Counter

@name('撤下会战助战')
@default(True)
@description('拒绝内鬼练度')
class remove_cb_support(Module):
    async def do_task(self, client: pcrclient):
        support_info = await client.support_unit_get_setting()
        remove = False
        for support in support_info.clan_support_units:
            if support.position in [eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_1, eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_2]:
                remove = True
                self._log(f"移除{db.get_unit_name(support.unit_id)}，已被借{support.clan_support_count}次")
                await client.support_unit_change_setting(1, support.position, 2, support.unit_id)
        if not remove:
            raise SkipError("没有会战助战")

@name('计算兑换角色碎片')
@default(True)
@booltype('redeem_unit_swap_do', '开换', False)
@description('计算兑换对应角色所需的3000碎片的最优使用方案，使得剩余碎片的盈余值的最大值最小')
class redeem_unit_swap(Module):

    async def do_task(self, client: pcrclient):
        do = self.get_config('redeem_unit_swap_do')

        for unit_id in db.redeem_unit:
            if unit_id in client.data.unit:
                continue
            gap = client.data.get_memory_demand_gap()
            item = [k for k, v in gap.items() if v < 0] 
            self._log(f"{db.get_unit_name(unit_id)}")
            use_piece = 0
            info = client.data.user_redeem_unit.get(unit_id, 
                                                    RedeemUnitInfo(unit_id = unit_id, 
                                                                   slot_info = [RedeemUnitSlotInfo(slot_id = i, register_num = 0) for i in db.redeem_unit[unit_id]]))

            for slot_id in db.redeem_unit[unit_id]:
                if all(slot_info.slot_id != slot_id for slot_info in info.slot_info):
                    info.slot_info.append(RedeemUnitSlotInfo(slot_id = slot_id, register_num = 0))

            for slot_info in info.slot_info:
                db_info = db.get_redeem_unit_slot_info(unit_id,slot_info.slot_id)
                if db_info.condition_category == eRedeemUnitUnlockCondition.UNLOCK_UNIT:
                    if db_info.condition_id not in client.data.unit:
                        raise AbortError(f"未解锁{db.get_unit_name(db_info.condition_id)}，无法兑换{db.get_unit_name(unit_id)}")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.VIEWED_STORY:
                    if db_info.condition_id not in client.data.read_story_ids:
                        raise AbortError(f"未阅读{db_info.condition_id}，无法兑换{db.get_unit_name(unit_id)}")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.GOLD:
                    self._log(f"已使用{slot_info.register_num}玛那")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.CURRENCY:
                    self._log(f"已使用{slot_info.register_num}??")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.MEMORY_PIECE:
                    self._log(f"已使用{slot_info.register_num}碎片")
                    use_piece = int(db_info.consume_num) - slot_info.register_num
                elif db_info.condition_category == eRedeemUnitUnlockCondition.SUPER_MEMORY_PIECE:
                    self._log(f"已使用{slot_info.register_num}纯净碎片")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.JEWEL:
                    self._log(f"已使用{slot_info.register_num}宝石")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.EQUIP:
                    self._log(f"已使用{slot_info.register_num}装备")
                elif db_info.condition_category == eRedeemUnitUnlockCondition.EQUIP_MATERIAL:
                    self._log(f"已使用{slot_info.register_num}装备碎片")
                else:
                    raise ValueError(f"未知的兑换条件{slot_info.slot_id}")


            ok, res = memory_use_average([-gap[i] for i in item], use_piece)
            if not ok:
                raise AbortError(f"盈余碎片不足{use_piece}片")
            id: List[int] = list(range(len(item)))
            id.sort(key=lambda x: (res[x], -gap[item[x]] - res[x]), reverse=True)
            msg = '\n'.join(f"{db.get_inventory_name_san(item[i])}使用{res[i]}片, 剩余盈余{-gap[item[i]] - res[i]}片" for i in id)
            self._log(msg)

            unsatisfied = [db.memory_to_unit[item[i][1]] for i in id if 
                           res[i] > 0 and 
                           (db.memory_to_unit[item[i][1]] not in client.data.unit or
                           client.data.unit[db.memory_to_unit[item[i][1]]].unit_rarity < 5)]
            if unsatisfied:
                msg = '以下角色未5星，无法用于兑换：\n' + '\n'.join(db.get_unit_name(i) for i in unsatisfied)
                raise AbortError(msg)

            if do:
                for slot_info in info.slot_info:
                    db_info = db.get_redeem_unit_slot_info(unit_id,slot_info.slot_id)
                    if db_info.condition_category == eRedeemUnitUnlockCondition.MEMORY_PIECE:
                        memory_use = Counter({item[i]: res[i] for i in id if res[i] > 0})
                        if memory_use:
                            self._log(f"使用了角色碎片")
                            ret = await client.unit_register_item(unit_id, slot_info.slot_id, memory_use, slot_info.register_num)
                            slot_info.register_num = ret.register_num
                    elif db_info.condition_category == eRedeemUnitUnlockCondition.GOLD:
                        info = db.get_redeem_unit_slot_info(unit_id,slot_info.slot_id)
                        total_mana = int(info.consume_num) - slot_info.register_num
                        if not (await client.prepare_mana(total_mana)):
                            raise AbortError("玛那不足")
                        while total_mana > 0:
                            mana = min(total_mana, client.data.settings.max_once_consume_gold.redeem_unit)
                            self._log(f"使用了{mana}玛那")
                            ret = await client.unit_register_item(unit_id, slot_info.slot_id, Counter({(eInventoryType.Gold, info.condition_id): mana}), slot_info.register_num)
                            slot_info.register_num = ret.register_num
                            total_mana -= mana
                    else:
                        if db_info.condition_category in [eRedeemUnitUnlockCondition.UNLOCK_UNIT,
                                                        eRedeemUnitUnlockCondition.VIEWED_STORY]:
                            continue
                        raise AbortError(f"未实现的兑换条件{db_info.condition_category}")

                self._log(f"兑换{db.get_unit_name(unit_id)}")
                await client.unit_unlock_redeem_unit(unit_id)

        if not self.log:
            raise SkipError("没有可兑换的角色")

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

@description('看看你的特别装备数量')
@name('查ex装备')
@booltype('ex_equip_info_cb_only', '会战', False)
@notlogin(check_data = True)
@default(True)
class ex_equip_info(Module):
    async def do_task(self, client: pcrclient):
        cb_only = self.get_config('ex_equip_info_cb_only')
        cnt = sorted( 
                list(Counter(
                (ex.ex_equipment_id, ex.rank) for ex in client.data.ex_equips.values() 
                if not cb_only or db.ex_equipment_data[ex.ex_equipment_id].clan_battle_equip_flag).items()),
                key=lambda x: (db.ex_equipment_data[x[0][0]].rarity, db.ex_equipment_data[x[0][0]].clan_battle_equip_flag, x[0][0], x[0][1]), reverse=True
                )
        rainbow_cnt = sum(1 * c for (id, rank), c in cnt if db.ex_equipment_data[id].rarity == 5)
        pink_cnt = sum(1 * c for (id, rank), c in cnt if db.ex_equipment_data[id].rarity == 4)
        history_pink_cnt = sum((rank + 1) * c for (id, rank), c in cnt if db.ex_equipment_data[id].rarity == 4)
        if not cb_only:
            self._log(f"彩装数量：{rainbow_cnt}")
            self._log(f"粉装数量：{pink_cnt}/{history_pink_cnt}")
            if rainbow_cnt:
                rainbow = [ex for ex in client.data.ex_equips.values() if db.ex_equipment_data[ex.ex_equipment_id].rarity == 5]
                msg = '\n'.join(f"{db.get_ex_equip_name(ex.ex_equipment_id)}: {db.get_ex_equip_sub_status_str(ex.ex_equipment_id, ex.sub_status or [])}" for ex in rainbow)
                self._log(msg)

        no_rainbow = [ ((id, rank), c) for (id, rank), c in cnt if db.ex_equipment_data[id].rarity < 5 ]
        if no_rainbow:
            msg = '\n'.join(f"{db.get_ex_equip_name(id, rank)}x{c}" for (id, rank), c in no_rainbow)
            self._log(msg)


@description('看看你缺了什么称号')
@name('查缺称号')
@default(True)
class missing_emblem(Module):
    async def do_task(self, client: pcrclient):
        emblem_top = await client.emblem_top()
        missing_emblem = set(db.emblem_data.keys()) - set(emblem.emblem_id for emblem in emblem_top.user_emblem_list)
        if not missing_emblem:
            self._log("全称号玩家！你竟然没有缺少的称号！")
        else:
            self._log(f"缺少{len(missing_emblem)}个称号")
            self._log('\n'.join(f"{db.emblem_data[id].emblem_name}-{db.emblem_mission_data[db.emblem_data[id].description_mission_id].description if db.emblem_data[id].description_mission_id in db.emblem_mission_data else ''}" for id in missing_emblem))

@description('看看你缺了什么角色')
@name('查缺角色')
@notlogin(check_data = True)
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

@description('警告！真抽！\n抽到出指NEW出保底角色，或达天井停下来，如果已有保底角色，就不会NEW！意味着就是一井！\n智能pickup指当前pickup角色为已拥有角色时会自动切换成未拥有的角色。\n附奖池自动选择缺口最多的碎片，pickup池未选满角色自动选择未拥有角色，有多个则按角色编号大到小或小到大选取\n先免费十连->限定十连券->钻石')
@name('抽卡')
@singlechoice("gacha_method", "抽取方式", '十连', ['十连', '单抽', '单抽券'])
@singlechoice("pool_id", "池子", "", db.get_cur_gacha)
@booltype('gacha_start_auto_select_pickup_min_first', "PickUp编号小优先", False)
@booltype('gacha_start_auto_select_pickup', "智能PickUp", True)
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
        gacha_method = self.get_config('gacha_method')
        pickup_min_first = self.get_config('gacha_start_auto_select_pickup_min_first')
        real_exchange_id = 0
        if gacha_id == 120001:
            if not client.data.return_fes_info_list or all(item.end_time <= client.time for item in client.data.return_fes_info_list):
                raise AbortError("没有回归池开放")
            resp = await client.gacha_special_fes()
            real_exchange_id = db.gacha_data[client.data.return_fes_info_list[0].original_gacha_id].exchange_id
        else:
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
        temp_tickets = [(eInventoryType.Item, id) for id in db.get_gacha_temp_ticket()]
        gacha_start_auto_select_pickup: bool = self.get_config('gacha_start_auto_select_pickup')
        try:
            while True:
                if gacha_method == '单抽券':
                    reward += await client.exec_gacha_aware(target_gacha, 1, eGachaDrawType.Ticket, client.data.get_inventory(db.gacha_single_ticket), 0, client.time, gacha_start_auto_select_pickup, pickup_min_first)
                elif gacha_method == '单抽':
                    reward += await client.exec_gacha_aware(target_gacha, 1, eGachaDrawType.Payment, client.data.jewel.free_jewel + client.data.jewel.jewel, 0, client.time, gacha_start_auto_select_pickup, pickup_min_first)
                elif gacha_method == '十连':
                    if isinstance(resp, GachaIndexResponse) and resp.campaign_info and resp.campaign_info.fg10_exec_cnt and target_gacha.id in db.campaign_free_gacha_data[resp.campaign_info.campaign_id]:
                        reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Campaign10Shot, cnt, resp.campaign_info.campaign_id, client.time, gacha_start_auto_select_pickup, pickup_min_first)
                        resp.campaign_info.campaign_id -= 1
                    elif any(client.data.get_inventory(temp_ticket) > 0 for temp_ticket in temp_tickets):
                        # find first ticket
                        ticket = next((temp_ticket for temp_ticket in temp_tickets if client.data.get_inventory(temp_ticket)))
                        num = client.data.get_inventory(ticket)
                        reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Temp_Ticket_10, num, 0, client.time, gacha_start_auto_select_pickup, pickup_min_first)
                    elif any(client.data.get_inventory(gacha_ten_ticket) > 0 for gacha_ten_ticket in db.gacha_ten_tickets):
                        ticket = next((gacha_ten_ticket for gacha_ten_ticket in db.gacha_ten_tickets if client.data.get_inventory(gacha_ten_ticket)))
                        num = client.data.get_inventory(ticket)
                        reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.TicketMultiPull10, num, 0, client.time, gacha_start_auto_select_pickup, pickup_min_first, ticket_item=ticket)
                    else:
                        reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Payment, client.data.jewel.free_jewel + client.data.jewel.jewel, 0, client.time, gacha_start_auto_select_pickup, pickup_min_first)
                else:
                    raise ValueError("未知的抽卡方式")

                cnt += 1
                if not always or self.can_stop(reward.new_unit, db.gacha_exchange_chara[target_gacha.exchange_id if not real_exchange_id else real_exchange_id]):
                    break

        except:
            raise 
        finally:
            self._log(f"抽取了{cnt}次{gacha_method}")
            self._log(await client.serlize_gacha_reward(reward, target_gacha.id))
            point = client.data.gacha_point[target_gacha.exchange_id].current_point if target_gacha.exchange_id in client.data.gacha_point else 0
            self._log(f"当前pt为{point}")

@description('天井兑换角色')
@name('兑天井')
@unitchoice("gacha_exchange_unit_id", "兑换角色")
@singlechoice("gacha_exchange_pool_id", "池子", "", db.get_cur_gacha)
@default(True)
class gacha_exchange_chara(Module):
    async def do_task(self, client: pcrclient):
        if ':' not in self.get_config('gacha_exchange_pool_id'):
            raise ValueError("配置格式不正确")
        gacha_id = int(self.get_config('gacha_exchange_pool_id').split(':')[0])
        gacha_exchange_unit_id = int(self.get_config('gacha_exchange_unit_id'))
        real_exchange_id = 0
        if gacha_id == 120001:
            if not client.data.return_fes_info_list or all(item.end_time <= client.time for item in client.data.return_fes_info_list):
                raise AbortError("没有回归池开放")
            resp = await client.gacha_special_fes()
            real_exchange_id = db.gacha_data[client.data.return_fes_info_list[0].original_gacha_id].exchange_id
        else:
            resp = await client.get_gacha_index()
        for gacha in resp.gacha_info:
            if gacha.id == gacha_id:
                target_gacha = gacha
                break
        else:
            raise AbortError(f"未找到卡池{gacha_id}")
        if target_gacha.type != eGachaType.Payment:
            raise AbortError("非宝石抽卡池")

        exchange_id = target_gacha.exchange_id if not real_exchange_id else real_exchange_id

        exchange_unit_ids = [d.unit_id for d in db.gacha_exchange_chara[exchange_id]]
        if gacha_exchange_unit_id not in exchange_unit_ids:
            raise AbortError(f"天井池里未找到{db.get_unit_name(gacha_exchange_unit_id)}")

        gacha_point = client.data.gacha_point.get(exchange_id, None)
        if not gacha_point:
            raise AbortError(f"当前pt为0，未到达天井")
        elif gacha_point.current_point < gacha_point.max_point:
            raise AbortError(f"当前pt为{gacha_point.current_point}<{gacha_point.max_point}，未到达天井")

        resp = await client.gacha_exchange_point(exchange_id, gacha_exchange_unit_id, gacha_point.current_point)
        msg = await client.serialize_reward_summary(resp.reward_info_list)
        self._log(f"兑换了{db.get_unit_name(gacha_exchange_unit_id)}，获得了:\n{msg}")


@description('查看会战支援角色的详细数据，拒绝内鬼！')
@name('会战支援数据')
@default(True)
class get_clan_support_unit(Module):
    async def serialize_unit_info(self, unit_data: Union[UnitData, UnitDataLight]) -> Tuple[bool, str]:
        info = []
        ok = True
        def add_info(prefix, cur, expect = None):
            if expect:
                nonlocal ok
                info.append(f'{prefix}:{cur}/{expect}')
                ok &= (cur == expect)
            else:
                info.append(f'{prefix}:{cur}')
        unit_id = unit_data.id
        add_info("等级", unit_data.unit_level, max(unit_data.unit_level, db.team_max_level))
        if unit_data.battle_rarity:
            add_info("星级", f"{unit_data.battle_rarity}-{unit_data.unit_rarity}")
        else:
            add_info("星级", f"{unit_data.unit_rarity}")
        add_info("品级", unit_data.promotion_level, db.equip_max_rank)
        for id, union_burst in enumerate(unit_data.union_burst):
            if union_burst.skill_level:
                add_info(f"ub{id}", union_burst.skill_level, unit_data.unit_level)
        for id, skill in enumerate(unit_data.main_skill):
            if skill.skill_level:
                add_info(f"skill{id}", skill.skill_level, unit_data.unit_level)
        for id, skill in enumerate(unit_data.ex_skill):
            if skill.skill_level:
                add_info(f"ex{id}", skill.skill_level, unit_data.unit_level)
        equip_info = []
        for id, equip in enumerate(unit_data.equip_slot):
            equip_id = getattr(db.unit_promotion[unit_id][unit_data.promotion_level], f'equip_slot_{id + 1}')
            if not equip.is_slot:
                if equip_id != 999999:
                    equip_info.append('-')
                    ok = False
                else:
                    equip_info.append('*')
            else:
                star = db.get_equip_star_from_pt(equip_id, equip.enhancement_pt)
                ok &= (star == 5)
                equip_info.append(str(star))
        equip_info = '/'.join(equip_info)
        add_info("装备", equip_info)

        for id, equip in enumerate(unit_data.unique_equip_slot):
            equip_slot = id + 1
            have_unique = (equip_slot in db.unit_unique_equip and unit_id in db.unit_unique_equip[equip_slot])
            max_level = 0 if not have_unique else db.unique_equipment_max_level[equip_slot]
            if have_unique:
                if not equip.is_slot:
                    add_info(f"专武{id}", '-', max_level)
                else:
                    add_info(f"专武{id}", db.get_unique_equip_level_from_pt(equip_slot, equip.enhancement_pt), max_level)

        return ok, ' '.join(info)

    async def do_task(self, client: pcrclient):
        await client.get_clan_battle_top(1, client.data.get_shop_gold(eSystemId.CLAN_BATTLE_SHOP))
        unit_list = await client.get_clan_battle_support_unit_list()
        msg = []
        for unit in unit_list.support_unit_list:
            strongest, info = await self.serialize_unit_info(unit.unit_data)
            msg.append((unit.unit_data.id, strongest, unit.owner_name, info))

        for unit in client.data.dispatch_units:
            if unit.position == eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_1 or unit.position == eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_2:
                strongest, info = await self.serialize_unit_info(client.data.unit[unit.unit_id])
                msg.append((unit.unit_id, strongest, client.user_name, info))

        msg = sorted(msg, key=lambda x:(x[0], -x[1]))
        for unit_id, strongest, owner_name, unit_info in msg:
            unit_name = db.get_unit_name(unit_id)
            info = f'{unit_name}({owner_name}): {"满中满" if strongest else "非满警告！"}\n{unit_info}\n'
            self._log(info)

@description('获得可导入到兰德索尔图书馆的账号数据')
@name('兰德索尔图书馆导入数据')
@default(True)
@notlogin(check_data = True)
class get_library_import_data(Module):
    async def do_task(self, client: pcrclient):
        msg = client.data.get_library_import_data()
        self._log(msg)

@description('注意！大师币会顶号！根据每个角色拉满星级、开专、升级至当前最高专所需的记忆碎片减去库存的结果')
@singlechoice('memory_demand_consider_unit', '考虑角色', '所有', ['所有', '地图可刷取', '大师币商店'])
@name('获取记忆碎片缺口')
@notlogin(check_data = True)
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

@description('去除六星需求后，专二所需纯净碎片减去库存的结果')
@name('获取纯净碎片缺口')
@notlogin(check_data = True)
@default(True)
class get_need_pure_memory(Module):
    async def do_task(self, client: pcrclient):
        from .autosweep import unique_equip_2_pure_memory_id
        pure_gap = client.data.get_pure_memory_demand_gap()
        target = Counter()
        need_list = []
        header = []
        data = {}
        for unit in unique_equip_2_pure_memory_id:
            kana = db.unit_data[unit].kana
            target[kana] += 150 if unit not in client.data.unit or len(client.data.unit[unit].unique_equip_slot) < 2 or not client.data.unit[unit].unique_equip_slot[1].is_slot else 0
            own = -sum(pure_gap[db.unit_to_pure_memory[unit]] if unit in db.unit_to_pure_memory else 0 for unit in db.unit_kana_ids[kana])
            need_list.append(((eInventoryType.Unit, unit), target[kana] - own))
            unit_name = db.get_unit_name(unit)
            header.append(unit_name)
            data[unit_name] = target[kana] - own

        msg = {}
        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in need_list])
        self._log(msg)

        self._table_header(header)
        self._table(data)

@description('去除升级突破满专需求后，专一SP所需纯净碎片减去库存的结果')
@name('获取SP碎片缺口')
@notlogin(check_data = True)
@default(True)
class get_need_sp_memory(Module):
    async def do_task(self, client: pcrclient):
        from .autosweep import UniqueEquip1SPMemory
        memory_gap = client.data.get_memory_demand_gap()
        target = Counter()
        header = []
        data = {}
        for _type in UniqueEquip1SPMemory.Type:
            if _type == 0: continue
            need_list = []
            type_desc = UniqueEquip1SPMemory.typeName[_type]
            for unit in UniqueEquip1SPMemory.get_unit_demand(_type):
                token = (eInventoryType.Item, db.unit_to_memory[unit])
                target[token] += 300
                need_list.append((token, target[token] + memory_gap[token]))

                token_name = f"{db.get_inventory_name_san(token)}({type_desc})"
                header.append(token_name)
                data[token_name] = target[token] + memory_gap[token]

            msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in need_list])
            self._log(f"=={type_desc}==")
            self._log(msg)

        self._table_header(header)
        self._table(data)

@description('根据每个角色开专、升级至当前最高专所需的心碎减去库存的结果，大心转换成10心碎')
@name('获取心碎缺口')
@notlogin(check_data = True)
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

@description(
    "按顺序计算职能节点强化目标是否可由当前专用材料和全能精通材料满足。"
    "格式：攻击型-4-4.2 治疗型-所有-4.2"
)
@name("职阶计算")
@texttype("role_mastery_targets", "强化目标", "")
@notlogin(check_data=True)
@default(True)
class role_mastery_calculation(Module):
    @staticmethod
    def parse_role_mastery_targets(text: str, catalog: Dict) -> List[Dict]:
        tokens = str(text or "").split()
        if not tokens:
            raise ValueError("请提供职阶要求，例如：攻击型-4-4.2 治疗型-所有-4.2")

        targets = []
        for token in tokens:
            parts = token.split("-")
            if len(parts) != 3:
                raise ValueError(f"要求【{token}】格式错误，应为：职能-节点-等级.星级")

            role_name, slot_text, state_text = parts
            if role_name not in catalog["role_ids_by_name"]:
                available = "、".join(
                    catalog["role_names"][role_id]
                    for role_id in sorted(catalog["role_names"])
                )
                raise ValueError(f"未知职能【{role_name}】，可用职能：{available}")

            role_id = catalog["role_ids_by_name"][role_name]
            available_slots = catalog["role_slots"][role_id]
            if slot_text == "所有":
                slot_ids = available_slots
            else:
                try:
                    slot_ids = (int(slot_text),)
                except ValueError as exc:
                    raise ValueError(
                        f"未知节点【{slot_text}】，节点应为数字或“所有”"
                    ) from exc

            if not slot_ids or any(
                slot_id not in available_slots
                for slot_id in slot_ids
            ):
                available = "、".join(map(str, available_slots))
                raise ValueError(
                    f"{role_name}不存在节点【{slot_text}】，可用节点：{available}"
                )

            state_match = re.fullmatch(r"(\d+)\.(\d+)", state_text)
            if not state_match:
                raise ValueError(
                    f"目标【{state_text}】格式错误，应为：等级.星级，例如 4.2"
                )
            state = tuple(map(int, state_match.groups()))

            for slot_id in slot_ids:
                node = catalog["nodes"][(role_id, slot_id)]
                if state not in node["state_costs"]:
                    states = sorted(node["state_costs"])
                    min_state = states[0]
                    max_state = states[-1]
                    raise ValueError(
                        f"{role_name}{slot_id}号节点不支持目标{state_text}，"
                        f"可用范围为{min_state[0]}.{min_state[1]}"
                        f"至{max_state[0]}.{max_state[1]}"
                    )

            targets.append({
                "source": token,
                "role_id": role_id,
                "role_name": role_name,
                "slot_ids": slot_ids,
                "state": state,
            })
        return targets

    @staticmethod
    def format_role_mastery_shortage(missing: Dict[int, int]) -> str:
        return " ".join(
            f"万能{tier}级x{count}"
            for tier, count in sorted(missing.items())
            if count > 0
        )

    async def do_task(self, client: pcrclient):
        try:
            catalog = db.unit_role_mastery_catalog
            targets = self.parse_role_mastery_targets(
                self.get_config("role_mastery_targets"),
                catalog,
            )
            results = client.data.calculate_role_mastery_requirements(
                targets,
                catalog=catalog,
            )
        except ValueError as exc:
            raise AbortError(str(exc)) from exc

        first_shortage_found = False
        headers = []
        row = {}
        for result in results:
            target = result["target"]
            if result["satisfied"]:
                status = "满足"
                line = f"{target['source']}：满足"
            else:
                shortage = self.format_role_mastery_shortage(
                    result["cumulative_missing"],
                )
                prefix = "累计缺" if first_shortage_found else "缺"
                status = f"缺{shortage}"
                line = f"{target['source']}：{prefix}{shortage}"
                first_shortage_found = True
            self._log(line)
            headers.append(target["source"])
            row[target["source"]] = status
        self._table_header(headers)
        self._table(row)

@description('统计考虑角色拉满品级所需的装备减去库存的结果，不考虑仓库中的大件装备')
@name('获取装备缺口')
@UnitListConfig('get_need_equip_consider_units', "考虑角色")
@notlogin(check_data = True)
@default(True)
class get_need_equip(Module):
    async def do_task(self, client: pcrclient):
        consider_units: List[int] = self.get_config("get_need_equip_consider_units")

        grow_parameter_list = client.data.get_synchro_parameter()
        demand = list(client.data.get_equip_demand2_gap(consider_units, grow_parameter_list = grow_parameter_list).items())

        demand = sorted(demand, key=lambda x: x[1], reverse=True)

        demand = filter(lambda item: item[1] > -100, demand)

        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in demand])
        self._log(msg)

# @inttype("start_rank", "起始品级", 1, [i for i in range(1, 99)])
# @booltype("like_unit_only", "收藏角色", False)
# @description('统计指定角色拉满品级所需的装备减去库存的结果，不考虑仓库中的大件装备')
# @name('获取装备缺口(弃用)')
# @notlogin(check_data = True)
# @default(True)
# class get_need_equip(Module):
#     async def do_task(self, client: pcrclient):
#         start_rank: int = self.get_config("start_rank")
#         like_unit_only: bool = self.get_config("like_unit_only")
#
#         demand = list(client.data.get_equip_demand_gap(start_rank=start_rank, like_unit_only=like_unit_only).items())
#
#         demand = sorted(demand, key=lambda x: x[1], reverse=True)
#
#         demand = filter(lambda item: item[1] > -100, demand)
#
#         msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in demand])
#         self._log(msg)

@description('根据考虑角色的装备缺口计算刷图优先级，越前的优先度越高')
@name('刷图推荐')
@UnitListConfig('get_normal_quest_recommand_consider_units', "考虑角色")
@notlogin(check_data = True)
@default(True)
class get_normal_quest_recommand(Module):
    async def do_task(self, client: pcrclient):
        consider_units: List[int] = self.get_config("get_normal_quest_recommand_consider_units")

        quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= apiclient.datetime]
        grow_parameter_list = client.data.get_synchro_parameter()
        require_equip = client.data.get_equip_demand2_gap(consider_units, grow_parameter_list = grow_parameter_list)
        quest_weight = client.data.get_quest_weght(require_equip)
        quest_id = sorted(quest_list, key = lambda x: quest_weight[x], reverse = True)
        tot = []
        for i in range(5):
            id = quest_id[i]
            name = db.get_quest_name(id)
            tokens: List[ItemType] = [i for i in db.normal_quest_rewards[id]]
            msg = f"{name}:\n" + '\n'.join([
                (f'{db.get_inventory_name_san(token)}: {"缺少" if require_equip[token] > 0 else "盈余"}{abs(require_equip[token])}片')
                for token in tokens
                if require_equip[token] > -100
                ])
            tot.append(msg.strip())

        msg = '\n--------\n'.join(tot)
        self._log(msg)

# @inttype("start_rank", "起始品级", 1, [i for i in range(1, 99)])
# @booltype("like_unit_only", "收藏角色", False)
# @description('根据装备缺口计算刷图优先级，越前的优先度越高')
# @name('刷图推荐(弃用)')
# @notlogin(check_data = True)
# @default(True)
# class get_normal_quest_recommand(Module):
#     async def do_task(self, client: pcrclient):
#         start_rank: int = self.get_config("start_rank")
#         like_unit_only: bool = self.get_config("like_unit_only")
#
#         quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= apiclient.datetime]
#         require_equip = client.data.get_equip_demand_gap(start_rank = start_rank, like_unit_only = like_unit_only)
#         quest_weight = client.data.get_quest_weght(require_equip)
#         quest_id = sorted(quest_list, key = lambda x: quest_weight[x], reverse = True)
#         tot = []
#         for i in range(5):
#             id = quest_id[i]
#             name = db.get_quest_name(id)
#             tokens: List[ItemType] = [i for i in db.normal_quest_rewards[id]]
#             msg = f"{name}:\n" + '\n'.join([
#                 (f'{db.get_inventory_name_san(token)}: {"缺少" if require_equip[token] > 0 else "盈余"}{abs(require_equip[token])}片')
#                 for token in tokens
#                 if require_equip[token] > -100
#                 ])
#             tot.append(msg.strip())
#
#         msg = '\n--------\n'.join(tot)
#         self._log(msg)

@description('从指定面板的指定队开始清除指定数量的编队')
@inttype("clear_team_num", "队伍数", 1, [i for i in range(1, 21)])
@inttype("clear_party_start_num", "初始队伍", 1, [i for i in range(1, 21)])
@inttype("clear_tab_start_num", "初始面板", 1, [i for i in range(1, 7)])
@name('清除编队')
class clear_my_party(Module):
    async def do_task(self, client: pcrclient):
        number: int = self.get_config('clear_team_num')
        tab_number: int = self.get_config('clear_tab_start_num')
        party_number: int = self.get_config('clear_party_start_num') - 1
        for _ in range(number):

            party_number += 1
            if party_number == 21:
                tab_number += 1
                party_number = 1
                if tab_number >= 6:
                    raise AbortError("队伍数量超过上限")

            self._log(f"清除了{tab_number}面板{party_number}队伍")
            await client.clear_my_party(tab_number, party_number)

@description('计算等级同步返钻数量')
@name('返钻计算')
@notlogin(check_data = True)
@default(True)
class return_jewel(Module):
    async def do_task(self, client: pcrclient):
        import math
        max_unit_rarity, max_promotion_level = 31, 305
        return_jewel_count = 0
        
        units = list(client.data.unit.values())
        count_unit = len(units)
        
        promo_levels = sorted([u.promotion_level for u in units], reverse=True)
        unit_levels = sorted([u.unit_level for u in units], reverse=True)

        value1 = sum(promo_levels[20:]) - len(promo_levels[20:])
        value2 = sum(unit_levels[20:]) - len(unit_levels[20:])

        return_jewel_count = 1500 + (value1 + value2 / 10) / 2
        return_jewel_count_10 = math.ceil(return_jewel_count / 10) * 10
        
        count_max_rarity = count_max_level = 0
        for unit in units:
            count_max_rarity += unit.promotion_level == max_unit_rarity
            count_max_level += unit.unit_level == max_promotion_level
        
        max_return_jewel_count = math.ceil((1500 + (count_unit - 20) * (max_unit_rarity - 1 + (max_promotion_level - 1) / 10) / 2) / 10) * 10

        self._log(f"当前角色数: {count_unit}")
        self._log(f"当前处于最大品级角色数: {count_max_rarity}")
        self._log(f"当前处于最大突破等级角色数: {count_max_level}")
        self._log(f"返钻数量: {return_jewel_count} (向上取整实际获得: {return_jewel_count_10})")
        self._log(f"当前box最多返钻数量: {max_return_jewel_count}")

async def _remove_unit_from_other_supports(client: pcrclient, support_info, unit_ids, target_support_type, target_positions, now, log_func, warn_func):  
    """  
    检查 unit_ids 中的角色是否在其他类型的支援位中，如果在则先撤下。  
    返回因冷却无法移除的 unit_id 集合。  
  
    支援位分类：  
    - 地下城: clan_support_units 中 position 1/2, API support_type=1  
    - 会战:   clan_support_units 中 position 3/4, API support_type=1  
    - 好友:   friend_support_units 中 position 1/2, API support_type=2  
    """  
    SUPPORT_COOLDOWN = 1800  
    blocked_units = set()  
  
    dungeon_positions = {eClanSupportMemberType.DUNGEON_SUPPORT_UNIT_1,  
                         eClanSupportMemberType.DUNGEON_SUPPORT_UNIT_2}  
    cb_positions = {eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_1,  
                    eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_2}  
    friend_positions = {1, 2}  
  
    # 构建"其他类型"的支援列表: (support_setting, api_support_type, type_name)  
    other_supports = []  
  
    for support in (support_info.clan_support_units or []):  
        if support.unit_id and support.unit_id != 0:  
            # 判断是否属于当前目标类型（目标类型不算"其他"）  
            is_target = (target_support_type == 1 and support.position in target_positions)  
            if not is_target:  
                if support.position in dungeon_positions:  
                    other_supports.append((support, 1, "地下城"))  
                elif support.position in cb_positions:  
                    other_supports.append((support, 1, "会战"))  
  
    for support in (support_info.friend_support_units or []):  
        if support.unit_id and support.unit_id != 0:  
            is_target = (target_support_type == 2 and support.position in target_positions)  
            if not is_target:  
                other_supports.append((support, 2, "好友"))  
  
    # 检查目标角色是否在其他类型中  
    for uid in unit_ids:  
        for support, api_type, type_name in other_supports:  
            if support.unit_id == uid:  
                unit_name = db.get_unit_name(uid)  
                if support.support_start_time and now - support.support_start_time < SUPPORT_COOLDOWN:  
                    remaining = SUPPORT_COOLDOWN - (now - support.support_start_time)  
                    warn_func(f"{unit_name}当前在{type_name}支援中，且挂上不足30分钟（剩余{remaining // 60}分{remaining % 60}秒），跳过该角色")  
                    blocked_units.add(uid)  
                else:  
                    log_func(f"{unit_name}当前在{type_name}支援中，正在移除...")  
                    await client.support_unit_change_setting(api_type, support.position, 2, support.unit_id)  
                    log_func(f"已将{unit_name}从{type_name}支援中移除")  
  
    return blocked_units

@name('挂会战支援')    
@default(True)    
@inttype("set_cb_support_star_2", "角色2星级", 0, [0, 3, 4, 5])  
@inttype("set_cb_support_star_1", "角色1星级", 0, [0, 3, 4, 5])  
@unitchoice("set_cb_support_unit_id_2", "角色2（选填）")    
@unitchoice("set_cb_support_unit_id_1", "角色1")    
@description('设置指定角色为会战支援（最多2个），并自动穿满会战EX装备，支持调星级')    
class set_cb_support(Module):  
    async def do_task(self, client: pcrclient):  
        SUPPORT_COOLDOWN = 1800  
  
        unit_id_1 = int(self.get_config('set_cb_support_unit_id_1'))  
        unit_id_2 = int(self.get_config('set_cb_support_unit_id_2'))  
  
        unit_ids = []  
        if unit_id_1 and unit_id_1 in client.data.unit:  
            unit_ids.append(unit_id_1)  
        if unit_id_2 and unit_id_2 in client.data.unit and unit_id_2 != unit_id_1:  
            unit_ids.append(unit_id_2)  
  
        if not unit_ids:  
            raise AbortError("请指定至少一个角色")  
  
        positions = [eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_1,  
                     eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_2]  
  
        support_info = await client.support_unit_get_setting()  
        now = apiclient.time  
  
        # 跨类型冲突检测：从其他支援类型中移除目标角色  
        blocked = await _remove_unit_from_other_supports(  
            client, support_info, unit_ids,  
            target_support_type=1,  
            target_positions=set(positions),  
            now=now, log_func=self._log, warn_func=self._warn  
        )  
        unit_ids = [uid for uid in unit_ids if uid not in blocked]  
  
        if not unit_ids:  
            if not self.log:  
                raise SkipError("无操作")  
            return  
  
        # 重新获取支援信息  
        support_info = await client.support_unit_get_setting()  
  
        # 识别冷却中的槽位  
        cooldown_positions = set()  
        for support in support_info.clan_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                if support.support_start_time and now - support.support_start_time < SUPPORT_COOLDOWN:  
                    cooldown_positions.add(support.position)  
  
        # 统计当前状态  
        already_placed = set()  
        non_target_supports = []  
        occupied_positions = set()  
        for support in support_info.clan_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                occupied_positions.add(support.position)  
                if support.unit_id in unit_ids:  
                    already_placed.add(support.unit_id)  
                else:  
                    non_target_supports.append(support)  
  
        empty_positions = [pos for pos in positions if pos not in occupied_positions and pos not in cooldown_positions]  
        need_placement = [uid for uid in unit_ids if uid not in already_placed]  
        slots_to_free = max(0, len(need_placement) - len(empty_positions))  
  
        removed = 0  
        for support in non_target_supports:  
            if removed >= slots_to_free:  
                break  
            if support.position in cooldown_positions:  
                remaining = SUPPORT_COOLDOWN - (now - support.support_start_time)  
                self._warn(f"支援位{support.position - 2}的{db.get_unit_name(support.unit_id)}在冷却中（剩余{remaining // 60}分{remaining % 60}秒），无法移除")  
            else:  
                self._log(f"移除旧支援{db.get_unit_name(support.unit_id)}")  
                await client.support_unit_change_setting(1, support.position, 2, support.unit_id)  
                removed += 1  
  
        support_info = await client.support_unit_get_setting()  
  
        already_set = {}  
        occupied_positions = set()  
        for support in support_info.clan_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                already_set[support.unit_id] = support.position  
                occupied_positions.add(support.position)  
  
        for uid in unit_ids:  
            unit_name = db.get_unit_name(uid)  
            if uid in already_set:  
                self._log(f"{unit_name}已经是会战支援位{already_set[uid] - 2}")  
                continue  
  
            target_pos = None  
            for pos in positions:  
                if pos not in occupied_positions and pos not in cooldown_positions:  
                    target_pos = pos  
                    break  
  
            if target_pos is None:  
                self._warn(f"没有可用的支援位给{unit_name}（槽位被占用或在冷却中）")  
                continue  
  
            await client.support_unit_change_setting(1, target_pos, 1, uid)  
            already_set[uid] = target_pos  
            occupied_positions.add(target_pos)  
            self._log(f"已设置{unit_name}为会战支援位{target_pos - 2}")  
  
        # Step 2: Equip CB EX equipment for all set units  
        use_ex_equip = set(  
            ex_slot.serial_id  
            for u in client.data.unit.values()  
            for ex_slot in u.cb_ex_equip_slot  
            if ex_slot.serial_id != 0  
        ) | client.data.user_clan_battle_ex_equip_restriction.keys()  
  
        for uid in unit_ids:  
            try:  
                unit_name = db.get_unit_name(uid)  
                unit = client.data.unit[uid]  
                slot_data = db.unit_ex_equipment_slot[uid]  
                exchange_list = []  
                equipped_names = []  
  
                for slot_id, ex_category in enumerate(  
                    [slot_data.slot_category_1, slot_data.slot_category_2, slot_data.slot_category_3], start=1  
                ):  
                    cb_slot = unit.cb_ex_equip_slot[slot_id - 1]  
  
                    if cb_slot.serial_id != 0:  
                        equipped_names.append(f"槽{slot_id}: 已装备")  
                        continue  
  
                    candidates = sorted(  
                        [ex for ex in client.data.ex_equips.values()  
                         if db.ex_equipment_data[ex.ex_equipment_id].category == ex_category  
                         and ex.serial_id not in use_ex_equip],  
                        key=lambda ex: (  
                            db.ex_equipment_data[ex.ex_equipment_id].clan_battle_equip_flag,  
                            db.ex_equipment_data[ex.ex_equipment_id].rarity,  
                            ex.enhancement_pt,  
                        ),  
                        reverse=True  
                    )  
  
                    if candidates:  
                        best = candidates[0]  
                        use_ex_equip.add(best.serial_id)  
                        exchange_list.append(ExtraEquipChangeSlot(slot=slot_id, serial_id=best.serial_id))  
                        equipped_names.append(f"槽{slot_id}: {db.get_ex_equip_name(best.ex_equipment_id)}")  
                    else:  
                        equipped_names.append(f"槽{slot_id}: 无可用装备")  
  
                if exchange_list:  
                    await client.unit_equip_ex([ExtraEquipChangeUnit(  
                        unit_id=uid,  
                        ex_equip_slot=None,  
                        cb_ex_equip_slot=exchange_list  
                    )])  
                    self._log(f"已为{unit_name}装备会战EX装:\n" + "\n".join(equipped_names))  
                elif equipped_names:  
                    self._log(f"{unit_name}会战EX装状态:\n" + "\n".join(equipped_names))  
            except Exception as e:  
                self._warn(f"{db.get_unit_name(uid)} EX装备失败: {e}")  
  
        # 调整星级  
        star_map = {}  
        if unit_id_1 and unit_id_1 in client.data.unit:  
            star_map[unit_id_1] = int(self.get_config('set_cb_support_star_1'))  
        if unit_id_2 and unit_id_2 in client.data.unit and unit_id_2 != unit_id_1:  
            star_map[unit_id_2] = int(self.get_config('set_cb_support_star_2'))  
          
        change_rarity_list = []  
        for uid in unit_ids:  
            target_star = star_map.get(uid, 0)  
            if target_star == 0:  
                continue  
            if uid not in client.data.unit:  
                continue  
            unit_data = client.data.unit[uid]  
            if unit_data.unit_rarity != 5:  
                self._warn(f"{db.get_unit_name(uid)}不是5星角色，无法调星")  
                continue  
            now_star = unit_data.battle_rarity if unit_data.battle_rarity else unit_data.unit_rarity  
            if target_star == now_star:  
                continue  
            if 3 <= target_star <= 5 and 3 <= now_star <= 5:  
                change_rarity_list.append(ChangeRarityUnit(unit_id=uid, battle_rarity=target_star))  
                self._log(f"将{db.get_unit_name(uid)}星级从{now_star}调至{target_star}")  
            else:  
                self._warn(f"{db.get_unit_name(uid)}星级无法从{now_star}调至{target_star}")  
        if change_rarity_list:  
            await client.unit_change_rarity(change_rarity_list)
            
        if not self.log:  
            raise SkipError("无操作")
       
@name('挂地下城支援')    
@default(True)    
@inttype("set_dungeon_support_star_2", "角色2星级", 0, [0, 3, 4, 5])  
@inttype("set_dungeon_support_star_1", "角色1星级", 0, [0, 3, 4, 5])  
@unitchoice("set_dungeon_support_unit_id_2", "角色2（选填）")    
@unitchoice("set_dungeon_support_unit_id_1", "角色1")    
@description('设置指定角色为地下城支援（最多2个），支持调星级') 
class set_dungeon_support(Module):  
    async def do_task(self, client: pcrclient):  
        SUPPORT_COOLDOWN = 1800  
  
        unit_id_1 = int(self.get_config('set_dungeon_support_unit_id_1'))  
        unit_id_2 = int(self.get_config('set_dungeon_support_unit_id_2'))  
  
        unit_ids = []  
        if unit_id_1 and unit_id_1 in client.data.unit:  
            unit_ids.append(unit_id_1)  
        if unit_id_2 and unit_id_2 in client.data.unit and unit_id_2 != unit_id_1:  
            unit_ids.append(unit_id_2)  
  
        if not unit_ids:  
            raise AbortError("请指定至少一个角色")  
  
        positions = [eClanSupportMemberType.DUNGEON_SUPPORT_UNIT_1,  
                     eClanSupportMemberType.DUNGEON_SUPPORT_UNIT_2]  
  
        support_info = await client.support_unit_get_setting()  
        now = apiclient.time  
  
        # 跨类型冲突检测：从其他支援类型中移除目标角色  
        blocked = await _remove_unit_from_other_supports(  
            client, support_info, unit_ids,  
            target_support_type=1,  
            target_positions=set(positions),  
            now=now, log_func=self._log, warn_func=self._warn  
        )  
        unit_ids = [uid for uid in unit_ids if uid not in blocked]  
  
        if not unit_ids:  
            if not self.log:  
                raise SkipError("无操作")  
            return  
  
        support_info = await client.support_unit_get_setting()  
  
        cooldown_positions = set()  
        for support in support_info.clan_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                if support.support_start_time and now - support.support_start_time < SUPPORT_COOLDOWN:  
                    cooldown_positions.add(support.position)  
  
        already_placed = set()  
        non_target_supports = []  
        occupied_positions = set()  
        for support in support_info.clan_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                occupied_positions.add(support.position)  
                if support.unit_id in unit_ids:  
                    already_placed.add(support.unit_id)  
                else:  
                    non_target_supports.append(support)  
  
        empty_positions = [pos for pos in positions if pos not in occupied_positions and pos not in cooldown_positions]  
        need_placement = [uid for uid in unit_ids if uid not in already_placed]  
        slots_to_free = max(0, len(need_placement) - len(empty_positions))  
  
        removed = 0  
        for support in non_target_supports:  
            if removed >= slots_to_free:  
                break  
            if support.position in cooldown_positions:  
                remaining = SUPPORT_COOLDOWN - (now - support.support_start_time)  
                self._warn(f"支援位{support.position}的{db.get_unit_name(support.unit_id)}在冷却中（剩余{remaining // 60}分{remaining % 60}秒），无法移除")  
            else:  
                self._log(f"移除旧支援{db.get_unit_name(support.unit_id)}")  
                await client.support_unit_change_setting(1, support.position, 2, support.unit_id)  
                removed += 1  
  
        support_info = await client.support_unit_get_setting()  
  
        already_set = {}  
        occupied_positions = set()  
        for support in support_info.clan_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                already_set[support.unit_id] = support.position  
                occupied_positions.add(support.position)  
  
        for uid in unit_ids:  
            unit_name = db.get_unit_name(uid)  
            if uid in already_set:  
                self._log(f"{unit_name}已经是地下城支援位{already_set[uid]}")  
                continue  
  
            target_pos = None  
            for pos in positions:  
                if pos not in occupied_positions and pos not in cooldown_positions:  
                    target_pos = pos  
                    break  
  
            if target_pos is None:  
                self._warn(f"没有可用的支援位给{unit_name}（槽位被占用或在冷却中）")  
                continue  
  
            await client.support_unit_change_setting(1, target_pos, 1, uid)  
            already_set[uid] = target_pos  
            occupied_positions.add(target_pos)  
            self._log(f"已设置{unit_name}为地下城支援位{target_pos}")             
  
        # 调整星级  
        star_configs = {  
            unit_id_1: int(self.get_config('set_dungeon_support_star_1')),  
            unit_id_2: int(self.get_config('set_dungeon_support_star_2')),  
        }  
        change_rarity_list = []  
        for uid in unit_ids:  
            target_star = star_configs.get(uid, 0)  
            if target_star == 0:  
                continue  
            if uid not in client.data.unit:  
                continue  
            unit_data = client.data.unit[uid]  
            if unit_data.unit_rarity != 5:  
                self._warn(f"{db.get_unit_name(uid)}不是5星角色，无法调星")  
                continue  
            now_star = unit_data.battle_rarity if unit_data.battle_rarity else unit_data.unit_rarity  
            if target_star == now_star:  
                continue  
            if 3 <= target_star <= 5 and 3 <= now_star <= 5:  
                change_rarity_list.append(ChangeRarityUnit(unit_id=uid, battle_rarity=target_star))  
                self._log(f"将{db.get_unit_name(uid)}星级从{now_star}调至{target_star}")  
            else:  
                self._warn(f"{db.get_unit_name(uid)}星级无法从{now_star}调至{target_star}")  
        if change_rarity_list:  
            await client.unit_change_rarity(change_rarity_list)
            
        if not self.log:  
            raise SkipError("无操作")
            
            
@name('挂好友支援')    
@default(True)    
@inttype("set_friend_support_star_2", "角色2星级", 0, [0, 3, 4, 5])  
@inttype("set_friend_support_star_1", "角色1星级", 0, [0, 3, 4, 5])  
@unitchoice("set_friend_support_unit_id_2", "角色2（选填）")    
@unitchoice("set_friend_support_unit_id_1", "角色1")    
@description('设置指定角色为好友支援（最多2个），好友可在关卡中借用，支持调星级')
class set_friend_support(Module):  
    async def do_task(self, client: pcrclient):  
        SUPPORT_COOLDOWN = 1800  
  
        unit_id_1 = int(self.get_config('set_friend_support_unit_id_1'))  
        unit_id_2 = int(self.get_config('set_friend_support_unit_id_2'))  
  
        unit_ids = []  
        if unit_id_1 and unit_id_1 in client.data.unit:  
            unit_ids.append(unit_id_1)  
        if unit_id_2 and unit_id_2 in client.data.unit and unit_id_2 != unit_id_1:  
            unit_ids.append(unit_id_2)  
  
        if not unit_ids:  
            raise AbortError("请指定至少一个角色")  
  
        positions = [1, 2]  # friend_support_units 的 position  
  
        support_info = await client.support_unit_get_setting()  
        now = apiclient.time  
  
        # 跨类型冲突检测：从其他支援类型中移除目标角色  
        blocked = await _remove_unit_from_other_supports(  
            client, support_info, unit_ids,  
            target_support_type=2,  
            target_positions=set(positions),  
            now=now, log_func=self._log, warn_func=self._warn  
        )  
        unit_ids = [uid for uid in unit_ids if uid not in blocked]  
  
        if not unit_ids:  
            if not self.log:  
                raise SkipError("无操作")  
            return  
  
        support_info = await client.support_unit_get_setting()  
  
        cooldown_positions = set()  
        for support in support_info.friend_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                if support.support_start_time and now - support.support_start_time < SUPPORT_COOLDOWN:  
                    cooldown_positions.add(support.position)  
  
        already_placed = set()  
        non_target_supports = []  
        occupied_positions = set()  
        for support in support_info.friend_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                occupied_positions.add(support.position)  
                if support.unit_id in unit_ids:  
                    already_placed.add(support.unit_id)  
                else:  
                    non_target_supports.append(support)  
  
        empty_positions = [pos for pos in positions if pos not in occupied_positions and pos not in cooldown_positions]  
        need_placement = [uid for uid in unit_ids if uid not in already_placed]  
        slots_to_free = max(0, len(need_placement) - len(empty_positions))  
  
        removed = 0  
        for support in non_target_supports:  
            if removed >= slots_to_free:  
                break  
            if support.position in cooldown_positions:  
                remaining = SUPPORT_COOLDOWN - (now - support.support_start_time)  
                self._warn(f"支援位{support.position}的{db.get_unit_name(support.unit_id)}在冷却中（剩余{remaining // 60}分{remaining % 60}秒），无法移除")  
            else:  
                self._log(f"移除旧支援{db.get_unit_name(support.unit_id)}")  
                await client.support_unit_change_setting(2, support.position, 2, support.unit_id)  
                removed += 1  
  
        support_info = await client.support_unit_get_setting()  
  
        already_set = {}  
        occupied_positions = set()  
        for support in support_info.friend_support_units:  
            if support.position in positions and support.unit_id and support.unit_id != 0:  
                already_set[support.unit_id] = support.position  
                occupied_positions.add(support.position)  
  
        for uid in unit_ids:  
            unit_name = db.get_unit_name(uid)  
            if uid in already_set:  
                self._log(f"{unit_name}已经是好友支援位{already_set[uid]}")  
                continue  
  
            target_pos = None  
            for pos in positions:  
                if pos not in occupied_positions and pos not in cooldown_positions:  
                    target_pos = pos  
                    break  
  
            if target_pos is None:  
                self._warn(f"没有可用的支援位给{unit_name}（槽位被占用或在冷却中）")  
                continue  
  
            await client.support_unit_change_setting(2, target_pos, 1, uid)  
            already_set[uid] = target_pos  
            occupied_positions.add(target_pos)  
            self._log(f"已设置{unit_name}为好友支援位{target_pos}")  
  
        # 调整星级  
        star_configs = {  
            unit_id_1: int(self.get_config('set_friend_support_star_1')),  
            unit_id_2: int(self.get_config('set_friend_support_star_2')),  
        }  
        change_rarity_list = []  
        for uid in unit_ids:  
            target_star = star_configs.get(uid, 0)  
            if target_star == 0:  
                continue  
            if uid not in client.data.unit:  
                continue  
            unit_data = client.data.unit[uid]  
            if unit_data.unit_rarity != 5:  
                self._warn(f"{db.get_unit_name(uid)}不是5星角色，无法调星")  
                continue  
            now_star = unit_data.battle_rarity if unit_data.battle_rarity else unit_data.unit_rarity  
            if target_star == now_star:  
                continue  
            if 3 <= target_star <= 5 and 3 <= now_star <= 5:  
                change_rarity_list.append(ChangeRarityUnit(unit_id=uid, battle_rarity=target_star))  
                self._log(f"将{db.get_unit_name(uid)}星级从{now_star}调至{target_star}")  
            else:  
                self._warn(f"{db.get_unit_name(uid)}星级无法从{now_star}调至{target_star}")  
        if change_rarity_list:  
            await client.unit_change_rarity(change_rarity_list)
            
        if not self.log:  
            raise SkipError("无操作")          
          
