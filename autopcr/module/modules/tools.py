from typing import List, Set
 
from ...util.ilp_solver import memory_use_average
import time
from ...model.common import ChangeRarityUnit, DeckListData, ExtraEquipChangeSlot, ExtraEquipChangeUnit, GachaPointInfo, GrandArenaHistoryDetailInfo, GrandArenaHistoryInfo, GrandArenaSearchOpponent, ProfileUserInfo, RankingSearchOpponent, RedeemUnitInfo, RedeemUnitSlotInfo, UnitData, UnitDataLight, VersusResult, VersusResultDetail
from ...model.responses import GachaIndexResponse, PsyTopResponse
from ...db.models import GachaExchangeLineup
from ...model.custom import ArenaQueryResult, ArenaQueryType, GachaReward, ItemType, eRedeemUnitUnlockCondition
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.arena import instance as ArenaQuery
from ...constants import DAILY_ORDER_KEY  

import random
import itertools
from collections import Counter
import datetime
import time
from datetime import datetime
@texttype("target_viewer_id", "玩家ID", "")
@description('通过玩家ID查询玩家公开信息')
@name('查询玩家资料')
@default(False)
class query_player_profile(Module):
    # 新增深域进度格式化方法
    def format_talent_quest(self, progress_value: int) -> str:
        """将深域进度值转换为a-b格式的字符串"""
        if progress_value > 0:
            big_stage = (progress_value - 1) // 10 + 1
            small_stage = (progress_value - 1) % 10 + 1
            return f"{big_stage}-{small_stage}"
        else:
            return "0-0"
            
    async def do_task(self, client: pcrclient):
        viewer_id_str: str = self.get_config("target_viewer_id").strip()

        if not viewer_id_str:
            raise AbortError("请输入玩家ID")

        # 验证是否为全数字
        if not viewer_id_str.isdigit():
            raise AbortError("玩家ID必须是数字")

        viewer_id: int = int(viewer_id_str)

        if viewer_id <= 0:
            raise AbortError("请输入有效的玩家ID")

        self._log(f"正在查询玩家ID: {viewer_id}")

        try:
            # 调用get_profile接口
            profile_data = await client.get_profile(viewer_id)
            # 直接打印原始数据
            # self._log(f"查询成功！玩家数据:")
            # self._log(f"原始响应数据: {profile_data}")

            # 如果有user_info，显示基础信息
            if hasattr(profile_data, 'user_info') and profile_data.user_info:
                user_info = profile_data.user_info
                self._log(f"玩家名称: {user_info.user_name}")
                self._log(f"个人签名: {user_info.user_comment}")
                self._log(f"竞技场排名: {user_info.arena_rank}")
                self._log(f"竞技场分组: {user_info.arena_group}")
                self._log(f"公主竞技场排名: {user_info.grand_arena_rank}")
                self._log(f"公主竞技场分组: {user_info.grand_arena_group}")
                self._log(f"已解锁剧情数: {user_info.open_story_num}")
                self._log(f"持有角色数: {user_info.unit_num}")
                self._log(f"已通关塔层数: {user_info.tower_cleared_floor_num}")
                self._log(f"已通关塔额外关卡数: {user_info.tower_cleared_ex_quest_count}")
                if hasattr(user_info, 'last_login_time') and user_info.last_login_time > 0:
                    timestamp = user_info.last_login_time
                    if timestamp > 10**12:  
                        timestamp = timestamp // 1000
                    login_time = time.localtime(timestamp)
                    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", login_time)
                    self._log(f"上次登录时间: {formatted_time}")
                else:
                    self._log(f"上次登录时间: 未知")
                self._log(f"好友数: {user_info.friend_num}")
                normal_quest = profile_data.quest_info.normal_quest
                self._log(f"普通关卡进度: {normal_quest[-1] if isinstance(normal_quest, (list, tuple)) else normal_quest}")
                hard_quest = profile_data.quest_info.hard_quest
                self._log(f"困难关卡进度: {hard_quest[-1] if isinstance(hard_quest, (list, tuple)) else hard_quest}")
                very_hard_quest = profile_data.quest_info.very_hard_quest
                self._log(f"Very Hard关卡进度: {very_hard_quest[-1] if isinstance(very_hard_quest, (list, tuple)) else very_hard_quest}")
                self._log(f"支线关卡进度: {profile_data.quest_info.byway_quest}")
                self._log(f"深域火属性进度: {self.format_talent_quest(profile_data.quest_info.talent_quest[0].clear_count)}")
                self._log(f"深域水属性进度: {self.format_talent_quest(profile_data.quest_info.talent_quest[1].clear_count)}")
                self._log(f"深域风属性进度: {self.format_talent_quest(profile_data.quest_info.talent_quest[2].clear_count)}")
                self._log(f"深域光属性进度: {self.format_talent_quest(profile_data.quest_info.talent_quest[3].clear_count)}")
                self._log(f"深域暗属性进度: {self.format_talent_quest(profile_data.quest_info.talent_quest[4].clear_count)}")
                self._log(f"团队等级: {user_info.team_level}")
                self._log(f"总战力: {user_info.total_power}")
                if hasattr(profile_data, 'clan_name') and profile_data.clan_name:
                    self._log(f"公会: {profile_data.clan_name}")

        except Exception as e:
            self._log(f"查询失败: {e}")
            raise AbortError(f"无法获取玩家 {viewer_id} 的资料")


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
                msg = '\n'.join(f"{ex.serial_id}: {db.get_ex_equip_name(ex.ex_equipment_id)}: {db.get_ex_equip_sub_status_str(ex.ex_equipment_id, ex.sub_status or [])}" for ex in rainbow)
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
                        reward += await client.exec_gacha_aware(target_gacha, 10, eGachaDrawType.Ticket, num, 0, client.time, gacha_start_auto_select_pickup, pickup_min_first) # real ticket ?
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

            self._log(f"{target.user_name}({target.viewer_id})\n{datetime.fromtimestamp(history.versus_time)} {'刺' if history_detail.is_challenge else '被刺'}")
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
     
        display_count = max(10, best_team_id + 1)  
        attack_str = self.present_attack(attack[:display_count])  
        msg = [f"#一键编队 5 1", defend_str, attack_str]  
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
        msg = f"防守方 {' '.join(msg)}"  
        return msg

    def present_attack(self, attack: List[ArenaQueryResult]) -> str:  
        lines = []  
        for id, ret in enumerate(attack):  
            unit_names = ' '.join([db.get_unit_name(unit.id) for unit in ret.atk])  
            suffix = ""  
            if ret.query_type == ArenaQueryType.APPROXIMATION:  
                suffix = "(近似解)"  
            elif ret.query_type == ArenaQueryType.PLACEHOLDER:  
                suffix = "(凑解)"  
            lines.append(f"第{id + 1}解.{ret.up}/{ret.down} {unit_names}{suffix}")  
        return '\n'.join(lines)

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
        msg = '\n防守队伍\t'.join(msg)
        msg = f"防守方\n防守队伍\t{msg}"
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
        time = db.format_time(apiclient.datetime)
        self._log(f"时间：{time}")
        for page in range(1, 4):
            ranking = await self.get_rank_info(client, 20, page)
            for info in ranking:
                if info.rank > 51:
                    break
                user_name = await self.get_user_info(client, info.viewer_id)
                you = " <--- 你" if info.viewer_id == client.data.uid else ""
                self._log(f"{info.rank:02}: {user_name}{you}\n bd{info.viewer_id}")

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

class ShuffleTeam(Module):
    def team_cnt(self) -> int: ...
    def deck_num(self, num: int) -> ePartyType: ...
    async def check_limit(self, client: pcrclient): 
        pass

    def shuffle_candidate(self) -> List[List[int]]:
        teams = [list(x) for x in itertools.permutations(range(self.team_cnt()))]
        teams = [x for x in teams if all(x[i] != i for i in range(self.team_cnt()))]
        return teams

    async def do_task(self, client: pcrclient):
        ids = random.choice(self.shuffle_candidate())
        deck_list: List[DeckListData] = []
        for i in range(self.team_cnt()):
            deck_number = self.deck_num(i)
            units = client.data.deck_list[deck_number]
            units_id = [getattr(units, f"unit_id_{i + 1}") for i in range(5)]

            deck = DeckListData()
            deck_number = self.deck_num(ids[i])
            deck.deck_number = deck_number
            deck.unit_list = units_id
            deck_list.append(deck)

        await self.check_limit(client)
        deck_list.sort(key=lambda x: x.deck_number)
        self._log('\n'.join([f"{i} -> {j}" for i, j in enumerate(ids)]))
        await client.deck_update_list(deck_list)

class PJJCShuffleTeam(ShuffleTeam):
    def team_cnt(self) -> int: return 3

@description('将pjjc进攻阵容随机错排')
@name('pjjc换攻')
class pjjc_atk_shuffle_team(PJJCShuffleTeam):
    def deck_num(self, num: int) -> ePartyType: return getattr(ePartyType, f"GRAND_ARENA_{num + 1}")

@description('将pjjc防守阵容随机错排')
@name('pjjc换防')
class pjjc_def_shuffle_team(PJJCShuffleTeam):
    def deck_num(self, num: int) -> ePartyType: return getattr(ePartyType, f"GRAND_ARENA_DEF_{num + 1}")
    async def check_limit(self, client: pcrclient):
        info = await client.get_grand_arena_info()
        limit_info = info.update_deck_times_limit
        if limit_info.round_times == limit_info.round_max_limited_times:
            ok_time = db.format_time(db.parse_time(limit_info.round_end_time))
            raise AbortError(f"已达到换防次数上限{limit_info.round_max_limited_times}，请于{ok_time}后再试")
        if limit_info.daily_times == limit_info.daily_max_limited_times:
            raise AbortError(f"已达到换防次数上限{limit_info.daily_max_limited_times}，请于明日再试")
        msg = f"{db.format_time(db.parse_time(limit_info.round_end_time))}刷新" if limit_info.round_times else ""
        self._log(f'''本轮换防次数{limit_info.round_times + 1}/{limit_info.round_max_limited_times}，{msg}
今日换防次数{limit_info.daily_times + 1}/{limit_info.daily_max_limited_times}''')

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
        demand = list(client.data.get_memory_demand_gap().items())#限制显示  添加这条就行
        demand = [d for d in demand if d[1] > -0] #限制显示  添加这条就行 
        demand = sorted(demand, key=lambda x: x[1], reverse=True)
        consider = self.get_config("memory_demand_consider_unit")
        msg = {}
        if consider == "地图可刷取":
            demand = [i for i in demand if i[0] in db.memory_hard_quest or i[0] in db.memory_shiori_quest]#限制显示  添加这条就行
            demand = [d for d in demand if d[1] > -0] #限制显示  添加这条就行 
        elif consider == "大师币商店":
            shop_content = await client.get_shop_item_list()
            master_shops = [shop for shop in shop_content.shop_list if shop.system_id == eSystemId.COUNTER_STOP_SHOP]
            if not master_shops:
                raise AbortError("大师币商店未开启")
            master_shop = master_shops[0]
            master_shop_item = set((item.type, item.item_id) for item in master_shop.item_list)
            msg = {(item.type, item.item_id): "已买" for item in master_shop.item_list if item.sold}
            demand = [i for i in demand if i[0] in master_shop_item]#限制显示  添加这条就行
            demand = [d for d in demand if d[1] > -0] #限制显示  添加这条就行
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
        for unit in unique_equip_2_pure_memory_id:
            kana = db.unit_data[unit].kana
            target[kana] += 150 if unit not in client.data.unit or len(client.data.unit[unit].unique_equip_slot) < 2 or not client.data.unit[unit].unique_equip_slot[1].is_slot else 0
            own = -sum(pure_gap[db.unit_to_pure_memory[unit]] if unit in db.unit_to_pure_memory else 0 for unit in db.unit_kana_ids[kana])
            need_list.append(((eInventoryType.Unit, unit), target[kana] - own))

        msg = {}
        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: 缺少{abs(item[1])}片' for item in need_list if item[1] > 0])#修改了这里
        self._log(msg)

@description('去除六星需求后，专二所需纯净碎片减去库存的结果')
@name('获取纯净碎片缺口(表格版)')
@notlogin(check_data = True)
@default(True)
class get_need_pure_memory_box(Module):
    async def do_task(self, client: pcrclient):
        from .autosweep import unique_equip_2_pure_memory_id
        pure_gap = client.data.get_pure_memory_demand_gap()
        target = Counter()
        need_list = []
        header = []
        data = {}
        for unit in unique_equip_2_pure_memory_id:
            kana = db.unit_data[unit].kana
            target[kana] += 150 if unit not in client.data.unit or len(client.data.unit[unit].unique_equip_slot) < 2 or not client.data.unit[unit].unique_equip_slot[1].is_slot else 150 - client.data.unit[unit].unique_equip_slot[1].enhancement_pt
            own = -sum(pure_gap[db.unit_to_pure_memory[unit]] if unit in db.unit_to_pure_memory else 0 for unit in db.unit_kana_ids[kana])
            need_list.append((unit, target[kana] - own))
            unit_name = db.get_unit_name(unit)
            header.append(unit_name)
            data[unit_name] = target[kana] - own

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
                target[token] += 320
                need_list.append((token, target[token] + memory_gap[token]))

                token_name = f"{db.get_inventory_name_san(token)}({type_desc})"
                header.append(token_name)
                data[token_name] = target[token] + memory_gap[token]

            shortage_list = [item for item in need_list if item[1] > 0]  
            msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: 缺少{item[1]}片' for item in shortage_list])
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

@description('从指定面板的指定队开始清除指定数量的编队')
@inttype("clear_team_num", "队伍数", 1, [i for i in range(1, 21)])
@inttype("clear_party_start_num", "初始队伍", 1, [i for i in range(1, 21)])
@inttype("clear_tab_start_num", "初始面板", 1, [i for i in range(1, 6)])
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
       
@description('根据EX装备名称查询对应的serial_id')  
@name('查ID')  
@texttype('search_ex_equip_name', '装备名称', '')  
@notlogin(check_data=True)  
@default(True)  
class search_ex_equip_id(Module):  
    async def do_task(self, client: pcrclient):  
        search_name = str(self.get_config('search_ex_equip_name')).strip()  
        if not search_name:  
            raise AbortError("请输入装备名称")  
  
        # 建立 serial_id -> 装备所在角色 的映射  
        equip_on_unit = {}  
        for uid, u in client.data.unit.items():  
            unit_name = db.get_unit_name(uid)  
            for slot_idx, ex_slot in enumerate(u.ex_equip_slot):  
                if ex_slot.serial_id != 0:  
                    equip_on_unit[ex_slot.serial_id] = f"{unit_name}(普通槽{slot_idx + 1})"  
            for slot_idx, ex_slot in enumerate(u.cb_ex_equip_slot):  
                if ex_slot.serial_id != 0:  
                    equip_on_unit[ex_slot.serial_id] = f"{unit_name}(会战槽{slot_idx + 1})"  
  
        # 搜索匹配的装备（模糊匹配）  
        results = []  
        for ex in client.data.ex_equips.values():  
            raw_name = db.inventory_name.get((eInventoryType.ExtraEquip, ex.ex_equipment_id), '')  
            if search_name in raw_name:  
                rarity = db.get_ex_equip_rarity(ex.ex_equipment_id)  
                display_name = db.get_ex_equip_name(ex.ex_equipment_id, ex.rank)  
                owner = equip_on_unit.get(ex.serial_id, '未装备')  
                results.append((rarity, ex.rank, ex.enhancement_pt, ex.serial_id, display_name, owner, ex))  
  
        if not results:  
            raise AbortError(f"未找到名称包含「{search_name}」的EX装备")  
  
        # 按稀有度降序、突破降序、强化降序排列  
        results.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)  
  
        lines = [f"找到 {len(results)} 件匹配「{search_name}」的EX装备："]  
        for rarity, rank, enhancement_pt, serial_id, display_name, owner, ex in results:  
            line = f"{serial_id}: {display_name} [{owner}]"  
            # 彩装额外显示 sub_status  
            if rarity == 5:  
                sub_str = db.get_ex_equip_sub_status_str(ex.ex_equipment_id, ex.sub_status or [])  
                line = f"{serial_id}: {display_name} ({sub_str}) [{owner}]"  
            lines.append(line)  
  
        self._log('\n'.join(lines))       

@name('一键穿ex')  
@default(True)  
@texttype('one_click_ex_selection', '选择(试穿/数字如 1 1 2)', '试穿')  
@unitchoice('one_click_ex_unit_id', '角色')  
@description('试穿模式：显示每个槽位可选的EX装备及属性。数字模式(如 1 1 2)：选择每个槽位的第N个装备并穿上，0表示不改动。多件在他人身上时可用字母后缀指定从谁换(如 1A 1 2)。从其他角色拿装备时会互换而非卸下。')  
class one_click_ex_equip(Module):  
    async def do_task(self, client: pcrclient):  
        unit_id = int(self.get_config('one_click_ex_unit_id'))  
        selection = str(self.get_config('one_click_ex_selection')).strip()  
  
        if unit_id not in client.data.unit:  
            raise AbortError(f"未拥有角色{db.get_unit_name(unit_id)}")  
  
        unit = client.data.unit[unit_id]  
        unit_name = db.get_unit_name(unit_id)  
        slot_data = db.unit_ex_equipment_slot[unit_id]  
  
        read_story = set(client.data.read_story_ids)  
        unit_attr = db.calc_unit_attribute(unit, read_story, client.data.ex_equips, exclude_ex_equip=True)  
        coefficient = db.unit_status_coefficient[1]  
  
        # Build mapping: serial_id -> (owner_unit_id, slot_index_1based)  
        equip_on_unit = {}  
        for uid, u in client.data.unit.items():  
            for slot_idx, ex_slot in enumerate(u.ex_equip_slot):  
                if ex_slot.serial_id != 0:  
                    equip_on_unit[ex_slot.serial_id] = (uid, slot_idx + 1)  
  
        # Build candidates per slot  
        from collections import defaultdict  
        slot_candidates = {}  
  
        for slot_id, ex_category in enumerate(  
            [slot_data.slot_category_1, slot_data.slot_category_2, slot_data.slot_category_3], start=1  
        ):  
            candidates = []  
            equip_groups = defaultdict(list)  
            for ex in client.data.ex_equips.values():  
                if db.ex_equipment_data[ex.ex_equipment_id].category != ex_category:  
                    continue  
                star = db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)  
                equip_groups[(ex.ex_equipment_id, star)].append(ex)  
  
            for (ex_id, star), ex_list in sorted(  
                equip_groups.items(),  
                key=lambda kv: (  
                    db.ex_equipment_data[kv[0][0]].rarity,  
                    kv[0][1],  
                    kv[0][0],  
                ),  
                reverse=True,  
            ):  
                rarity = db.ex_equipment_data[ex_id].rarity  
                attr = db.ex_equipment_data[ex_id].get_unit_attribute(star)  
                bonus = unit_attr.ex_equipment_mul(attr).ceil()  
                power = int(bonus.get_power(coefficient) + 0.5)  
  
                attr_parts = []  
                for param_type, ch_name in UnitAttribute.index2ch.items():  
                    en_name = UnitAttribute.index2name.get(param_type)  
                    if en_name:  
                        val = getattr(bonus, en_name, 0)  
                        if val and val != 0:  
                            attr_parts.append(f"{ch_name}{int(val)}")  
                attr_str = "/".join(attr_parts) if attr_parts else "无属性"  
  
                equip_name = db.get_ex_equip_name(ex_id)  
  
                if rarity == 5:  
                    # 彩装：每件单独列出，附带词条  
                    for ex in sorted(ex_list, key=lambda e: e.serial_id in equip_on_unit):  
                        sub_str = db.get_ex_equip_sub_status_str(ex.ex_equipment_id, ex.sub_status or [])  
                        sid = ex.serial_id  
                        on_others = [  
                            (equip_on_unit[sid], sid)  
                            for sid in [sid]  
                            if sid in equip_on_unit and equip_on_unit[sid][0] != unit_id  
                        ]  
                        candidates.append((ex_id, star, equip_name, attr_str, power, [sid], on_others, sub_str))  
                else:  
                    # 非彩装：保持原有分组逻辑  
                    serial_ids = sorted(  
                        [e.serial_id for e in ex_list],  
                        key=lambda sid: sid in equip_on_unit,  
                    )  
                    on_others = [(equip_on_unit[sid], sid) for sid in serial_ids if sid in equip_on_unit and equip_on_unit[sid][0] != unit_id]  
                    candidates.append((ex_id, star, equip_name, attr_str, power, serial_ids, on_others, ""))  
  
            slot_candidates[slot_id] = candidates  
  
        is_preview = selection == '试穿'  
  
        if is_preview:  
            self._log(f"=== {unit_name} EX装备试穿 ===")  
  
            # 显示当前3个槽位的EX装备  
            self._log(f"\n【当前装备】")  
            for slot_id in [1, 2, 3]:  
                ex_slot = unit.ex_equip_slot[slot_id - 1]  
                if not ex_slot.serial_id:  
                    self._log(f"  槽位{slot_id}: -")  
                else:  
                    ex = client.data.ex_equips[ex_slot.serial_id]  
                    star = db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)  
                    name = db.get_ex_equip_name(ex.ex_equipment_id)  
                    # 计算当前装备的战力加成  
                    cur_attr = db.ex_equipment_data[ex.ex_equipment_id].get_unit_attribute(star)  
                    cur_bonus = unit_attr.ex_equipment_mul(cur_attr).ceil()  
                    cur_power = int(cur_bonus.get_power(coefficient) + 0.5)  
                    cur_attr_parts = []  
                    for param_type, ch_name in UnitAttribute.index2ch.items():  
                        en_name = UnitAttribute.index2name.get(param_type)  
                        if en_name:  
                            val = getattr(cur_bonus, en_name, 0)  
                            if val and val != 0:  
                                cur_attr_parts.append(f"{ch_name}{int(val)}")  
                    cur_attr_str = "/".join(cur_attr_parts) if cur_attr_parts else "无属性"  
                    # 彩装额外显示词条  
                    if db.ex_equipment_data[ex.ex_equipment_id].rarity == 5:  
                        sub_str = db.get_ex_equip_sub_status_str(ex.ex_equipment_id, ex.sub_status or [])  
                        self._log(f"[ex:{ex.ex_equipment_id}]  槽位{slot_id}: {name}★{star} 战力+{cur_power} ({cur_attr_str}) 词条:{sub_str}") 
                    else:  
                        self._log(f"[ex:{ex.ex_equipment_id}]  槽位{slot_id}: {name}★{star} 战力+{cur_power} ({cur_attr_str})") 
  
            for slot_id in [1, 2, 3]:  
                cands = slot_candidates[slot_id]  
                self._log(f"\n【槽位{slot_id}】共{len(cands)}种穿法：")  
                for idx, (ex_id, star, name, attr_str, power, serial_ids, on_others, sub_str) in enumerate(cands, start=1):  
                    owner_info = ""  
                    if on_others:    
                        # 给每个在他人身上的装备加字母标记    
                        MAX_OWNER_DISPLAY = 7  
                        owner_parts = []    
                        for letter_idx, ((oid, oslot), _sid) in enumerate(on_others):    
                            letter = chr(ord('A') + letter_idx)    
                            owner_parts.append(f"{letter}:{db.get_unit_name(oid)}槽{oslot}")    
                        on_self_cnt = sum(1 for sid in serial_ids if sid in equip_on_unit and equip_on_unit[sid][0] == unit_id)    
                        free_cnt = len(serial_ids) - len(on_others) - on_self_cnt    
                        owner_info = f" [共{len(serial_ids)}件"    
                        if on_self_cnt > 0:    
                            owner_info += f", {on_self_cnt}件已穿戴"    
                        if free_cnt > 0:    
                            owner_info += f", {free_cnt}件空闲"  
                        if len(owner_parts) > MAX_OWNER_DISPLAY:  
                            displayed = ', '.join(owner_parts[:MAX_OWNER_DISPLAY])  
                            owner_info += f", {displayed}, ...等{len(owner_parts)}人穿戴]"  
                        else:  
                            owner_info += f", {', '.join(owner_parts)}]" 
                    sub_info = f" 词条:{sub_str}" if sub_str else ""  
                    self._log(f"[ex:{ex_id}]  {idx}. {name}★{star} 战力+{power} ({attr_str}){sub_info}{owner_info}") 
                if not cands:  
                    self._log(f"  无可用装备")  
        else:  
            # Equip mode: parse space-separated selection like "1 1 2" or "1A 1 2"  
            import re as _re  
            parts = selection.split()  
            if len(parts) != 3:  
                raise AbortError(f"选择格式错误：请输入3个空格分隔的数字(如 1 1 2)或'试穿'，当前输入: {selection}")  
  
            used_serial_ids = set()  
            selected = []  # list of (slot_id, serial_id, name, star, power)  
  
            for slot_id, part in enumerate(parts, start=1):  
                cands = slot_candidates[slot_id]  
  
                if part == '0':  
                    continue  
  
                # 解析数字和可选字母后缀  
                m = _re.match(r'^(\d+)([A-Za-z]?)$', part)  
                if not m:  
                    raise AbortError(f"槽位{slot_id}选择格式错误: {part}，请输入数字或数字+字母(如 1A)")  
  
                choice = int(m.group(1))  
                letter = m.group(2).upper()  # '' or 'A'-'Z'  
  
                if choice < 1 or choice > len(cands):  
                    raise AbortError(f"槽位{slot_id}只有{len(cands)}种装备，无法选择第{choice}个")  
  
                ex_id, star, name, attr_str, power, serial_ids, on_others, sub_str = cands[choice - 1]  
  
                target_serial = None  
  
                if letter:  
                    # 用户指定了字母，从 on_others 中按字母索引选择  
                    letter_index = ord(letter) - ord('A')  
                    if letter_index < 0 or letter_index >= len(on_others):  
                        available = [chr(ord('A') + i) + ':' + db.get_unit_name(oid) for i, ((oid, oslot), _sid) in enumerate(on_others)]  
                        if not available:  
                            raise AbortError(f"槽位{slot_id}编号{choice}没有在他人身上的装备，不需要字母后缀")  
                        raise AbortError(f"槽位{slot_id}编号{choice}字母{letter}超出范围，可选: {', '.join(available)}")  
                    (owner_uid, owner_slot), target_serial = on_others[letter_index]  
                    if target_serial in used_serial_ids:  
                        raise AbortError(f"槽位{slot_id}: {name}★{star} 的{letter}号装备已被其他槽位选用")  
                else:  
                    # 无字母，按原逻辑选第一个可用的  
                    for sid in serial_ids:  
                        if sid not in used_serial_ids:  
                            target_serial = sid  
                            break  
  
                if target_serial is None:  
                    raise AbortError(f"槽位{slot_id}: {name}★{star} 无可用装备(已被其他槽位选用)")  
  
                used_serial_ids.add(target_serial)  
                selected.append((slot_id, target_serial, name, star, power))  
                self._log(f"槽位{slot_id}: {name}★{star} 战力+{power}")  
  
            if not selected:  
                raise SkipError("无需操作")  
  
            # Collect swap pairs: (other_uid, other_slot, old_serial_id_from_target)  
            # When we take equip_X from another character, we give them the target's current equip in return  
            swap_pairs = []  # list of (owner_uid, owner_slot, target_old_serial_id)  
            slots_to_change = set(s[0] for s in selected)  
  
            for slot_id, sid, name, star, power in selected:  
                if sid in equip_on_unit:  
                    owner_uid, owner_slot = equip_on_unit[sid]  
                    if owner_uid != unit_id:  
                        # Get what the target character currently has in this slot  
                        target_old_serial = unit.ex_equip_slot[slot_id - 1].serial_id  
                        if target_old_serial != 0:  
                            swap_pairs.append((owner_uid, owner_slot, target_old_serial))  
                            self._log(f"与{db.get_unit_name(owner_uid)}槽{owner_slot}互换装备")  
                        else:  
                            swap_pairs.append((owner_uid, owner_slot, 0))  
                            self._log(f"从{db.get_unit_name(owner_uid)}的槽{owner_slot}取下{name}")  
  
            # Step 1: Unequip selected serial_ids from OTHER characters  
            for slot_id, sid, name, star, power in selected:  
                if sid in equip_on_unit:  
                    owner_uid, owner_slot = equip_on_unit[sid]  
                    if owner_uid != unit_id:  
                        await client.unit_equip_ex([ExtraEquipChangeUnit(  
                            unit_id=owner_uid,  
                            ex_equip_slot=[ExtraEquipChangeSlot(slot=owner_slot, serial_id=0)],  
                            cb_ex_equip_slot=None  
                        )])  
  
            # Step 2: Clear target character's slots that will be changed  
            clear_list = []  
            for ex_slot in unit.ex_equip_slot:  
                if ex_slot.serial_id != 0 and (ex_slot.slot in slots_to_change or ex_slot.serial_id in used_serial_ids):  
                    clear_list.append(ExtraEquipChangeSlot(slot=ex_slot.slot, serial_id=0))  
            if clear_list:  
                await client.unit_equip_ex([ExtraEquipChangeUnit(  
                    unit_id=unit_id,  
                    ex_equip_slot=clear_list,  
                    cb_ex_equip_slot=None  
                )])  
  
            # Step 3: Equip the new selections on target character  
            exchange_list = [ExtraEquipChangeSlot(slot=slot_id, serial_id=sid) for slot_id, sid, _, _, _ in selected]  
            await client.unit_equip_ex([ExtraEquipChangeUnit(  
                unit_id=unit_id,  
                ex_equip_slot=exchange_list,  
                cb_ex_equip_slot=None  
            )])  
  
            # Step 4: Swap — equip the target's old equipment onto the other characters  
            for owner_uid, owner_slot, old_serial in swap_pairs:  
                if old_serial != 0:  
                    await client.unit_equip_ex([ExtraEquipChangeUnit(  
                        unit_id=owner_uid,  
                        ex_equip_slot=[ExtraEquipChangeSlot(slot=owner_slot, serial_id=old_serial)],  
                        cb_ex_equip_slot=None  
                    )])  
  
            self._log(f"已为{unit_name}装备完成！")
           
@texttype("add_friend_viewer_id", "玩家UID", "")  
@description('通过玩家UID发送好友申请')  
@name('添加好友')  
@default(False)  
class add_friend(Module):  
    async def do_task(self, client: pcrclient):  
        viewer_id_str: str = self.get_config("add_friend_viewer_id").strip()  
  
        if not viewer_id_str:  
            raise AbortError("请输入玩家UID")  
  
        if not viewer_id_str.isdigit():  
            raise AbortError("玩家UID必须是数字")  
  
        viewer_id: int = int(viewer_id_str)  
  
        if viewer_id <= 0:  
            raise AbortError("请输入有效的玩家UID")  
  
        self._log(f"正在向玩家UID: {viewer_id} 发送好友申请...")  
  
        try:  
            from ...model.requests import FriendRequestRequest  
            req = FriendRequestRequest()  
            req.target_viewer_id = viewer_id  
            resp = await client.request(req)  
            self._log(f"已成功向玩家 {viewer_id} 发送好友申请！")  
        except Exception as e:  
            error_msg = str(e)  
            if "已经是好友" in error_msg or "ALREADY_FRIEND" in error_msg.upper():  
                raise AbortError(f"玩家 {viewer_id} 已经是你的好友")  
            elif "申请已发送" in error_msg or "PENDING" in error_msg.upper():  
                raise AbortError(f"已经向玩家 {viewer_id} 发送过好友申请，请等待对方处理")  
            elif "好友已满" in error_msg or "LIMIT" in error_msg.upper():  
                raise AbortError(f"好友数量已达上限，无法发送申请")  
            else:  
                self._log(f"发送好友申请失败: {e}")  
                raise AbortError(f"无法向玩家 {viewer_id} 发送好友申请: {e}")    


  
@texttype("daily_order_move", "要挪到其后的功能(名称/序号，空格分隔)", "")  
@texttype("daily_order_anchor", "锚点功能(名称/序号，留空或填『重置』可恢复默认)", "")  
@description('调整【日常】清日常顺序：把指定功能挪到锚点功能之后。与 #清日常排序 共用同一份配置。填“重置”可恢复默认。')  
@name('调整日常顺序')  
@notlogin()  
@default(False)  
class daily_order_edit(Module):  
    def _match(self, targets, indexed):  
        idx_map = {i: m for i, m in indexed}  
        name_map = {m.name: m for _, m in indexed if m.name}  
        key_map = {m.key: m for _, m in indexed}  
        out = []  
        for t in targets:  
            t = t.strip()  
            if not t:  
                continue  
            if t.isdigit() and int(t) in idx_map:  
                out.append(idx_map[int(t)])  
            elif t in key_map:  
                out.append(key_map[t])  
            elif t in name_map:  
                out.append(name_map[t])  
            else:  
                fuzzy = [m for _, m in indexed if m.name and t in m.name]  
                if len(fuzzy) == 1:  
                    out.append(fuzzy[0])  
                else:  
                    self._warn(f"{t}（未匹配到唯一功能，已跳过）")  
        return out  
  
    async def do_task(self, client: pcrclient):  
        acc = self._parent                     
        anchor_raw = self.get_config("daily_order_anchor").strip()  
        moves_raw = self.get_config("daily_order_move").strip()  
  
        modules = acc.modules_list.get_modules_list('daily')  
        indexed = [(i + 1, m) for i, m in enumerate(m for m in modules if m.implmented)]  
  
        # 重置  
        if anchor_raw in ("重置", "reset", "默认") or (not anchor_raw and not moves_raw):  
            acc.data.config.pop(DAILY_ORDER_KEY, None)  
            self._log("已恢复默认清日常顺序")  
            return  
  
        anchor = self._match([anchor_raw], indexed)  
        if not anchor:  
            raise AbortError(f"锚点功能匹配失败: {anchor_raw}")  
        anchor = anchor[0]  
  
        moves = self._match(moves_raw.split(), indexed)  
        move_keys = []  
        for m in moves:  
            if m.key != anchor.key and m.key not in move_keys:  
                move_keys.append(m.key)  
        if not move_keys:  
            raise AbortError("要挪动的功能不能为空，且不能与锚点相同")  
  
        order = []  
        for _, m in indexed:  
            if m.key in move_keys:  
                continue  
            order.append(m.key)  
            if m.key == anchor.key:  
                order.extend(move_keys)  
  
        acc.data.config[DAILY_ORDER_KEY] = order   
  
        moved = ", ".join(acc.modules_list.get_module_from_key(k).name for k in move_keys)  
        self._log(f"已将 [{moved}] 挪到 [{anchor.name}] 之后，清日常顺序已更新")          

@name('我的支援')  
@default(True)  
@description('显示地下城/会战/好友三类支援位当前挂载的角色及其穿戴的EX装备')  
class get_my_support(Module):  
    def _log_ex(self, client: pcrclient, slots):  
        has_any = False  
        for ex_slot in (slots or []):  
            if not ex_slot.serial_id:  
                continue  
            ex = client.data.ex_equips[ex_slot.serial_id]  
            star = db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)  
            name = db.get_ex_equip_name(ex.ex_equipment_id)  
            self._log(f"[ex:{ex.ex_equipment_id}]{name}★{star}")  
            has_any = True  
        if not has_any:  
            self._log("无EX装备")  
  
    def _log_unit(self, client: pcrclient, unit_id, cb=False):  
        self._log(f"[unit:{unit_id}]")   # 只带ID，draw.py自行转头像与取名  
        if unit_id not in client.data.unit:  
            return  
        unit = client.data.unit[unit_id]  
        slots = unit.cb_ex_equip_slot if cb else unit.ex_equip_slot  
        self._log_ex(client, slots)  
  
    async def do_task(self, client: pcrclient):  
        support_info = await client.support_unit_get_setting()  
  
        dungeon_positions = {eClanSupportMemberType.DUNGEON_SUPPORT_UNIT_1,  
                             eClanSupportMemberType.DUNGEON_SUPPORT_UNIT_2}  
        cb_positions = {eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_1,  
                        eClanSupportMemberType.CLAN_BATTLE_SUPPORT_UNIT_2}  
        friend_positions = {1, 2}  
  
        dungeon_list, cb_list, friend_list = [], [], []  
  
        for support in (support_info.clan_support_units or []):  
            if support.unit_id and support.unit_id != 0:  
                if support.position in dungeon_positions:  
                    dungeon_list.append(support)  
                elif support.position in cb_positions:  
                    cb_list.append(support)  
  
        for support in (support_info.friend_support_units or []):  
            if support.unit_id and support.unit_id != 0 and support.position in friend_positions:  
                friend_list.append(support)  
  
        self._log("【地下城·追忆的战场】")  
        if not dungeon_list:  
            self._log("无")  
        for support in dungeon_list:  
            self._log_unit(client, support.unit_id, cb=False)  
  
        self._log("【团队战·露娜塔】")  
        if not cb_list:  
            self._log("无")  
        for support in cb_list:  
            self._log_unit(client, support.unit_id, cb=True)  
  
        self._log("【关卡·活动(好友)】")  
        if not friend_list:  
            self._log("无")  
        for support in friend_list:  
            self._log_unit(client, support.unit_id, cb=False)