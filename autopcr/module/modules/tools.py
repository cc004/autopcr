from typing import List, Set

from ...util.ilp_solver import memory_use_average

from ...model.common import ChangeRarityUnit, DeckListData, GachaPointInfo, GrandArenaHistoryDetailInfo, GrandArenaHistoryInfo, GrandArenaSearchOpponent, ProfileUserInfo, RankingSearchOpponent, RedeemUnitInfo, RedeemUnitSlotInfo, VersusResult, VersusResultDetail
from ...model.responses import GachaIndexResponse, PsyTopResponse
from ...db.models import GachaExchangeLineup
from ...model.custom import ArenaQueryResult, GachaReward, ItemType
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
import random
import itertools
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
                if slot_info.slot_id == 1:
                    self._log(f"已使用{slot_info.register_num}碎片")
                    use_piece = int(db_info.consume_num) - slot_info.register_num
                elif slot_info.slot_id == 2:
                    self._log(f"已使用{slot_info.register_num}玛那")
                elif slot_info.slot_id == 3:
                    if db_info.condition_id not in client.data.unit:
                        raise AbortError(f"未解锁{db.get_unit_name(db_info.condition_id)}，无法兑换{db.get_unit_name(unit_id)}")
                elif slot_info.slot_id == 4:
                    if db_info.condition_id not in client.data.read_story_ids:
                        raise AbortError(f"未阅读{db_info.condition_id}，无法兑换{db.get_unit_name(unit_id)}")
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
                    if slot_info.slot_id == 1:
                        memory_use = Counter({item[i]: res[i] for i in id if res[i] > 0})
                        if memory_use:
                            self._log(f"使用了角色碎片")
                            ret = await client.unit_register_item(unit_id, slot_info.slot_id, memory_use, slot_info.register_num)
                            slot_info.register_num = ret.register_num
                    elif slot_info.slot_id == 2:
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
        pink_cnt = sum(1 * c for (id, rank), c in cnt if db.ex_equipment_data[id].rarity == 4)
        history_pink_cnt = sum((rank + 1) * c for (id, rank), c in cnt if db.ex_equipment_data[id].rarity == 4)
        self._log(f"粉装数量：{pink_cnt}/{history_pink_cnt}")
        msg = '\n'.join(f"{db.get_ex_equip_name(id, rank)}x{c}" for (id, rank), c in cnt)
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
        for unit in unique_equip_2_pure_memory_id:
            kana = db.unit_data[unit].kana
            target[kana] += 150 if unit not in client.data.unit or len(client.data.unit[unit].unique_equip_slot) < 2 or not client.data.unit[unit].unique_equip_slot[1].is_slot else 0
            own = -sum(pure_gap[db.unit_to_pure_memory[unit]] if unit in db.unit_to_pure_memory else 0 for unit in db.unit_kana_ids[kana])
            need_list.append(((eInventoryType.Unit, unit), target[kana] - own))
        msg = {}
        msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in need_list])
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
@inttype("clear_team_num", "队伍数", 1, [i for i in range(1, 11)])
@inttype("clear_party_start_num", "初始队伍", 1, [i for i in range(1, 11)])
@inttype("clear_tab_start_num", "初始面板", 1, [i for i in range(1, 7)])
@name('清除编队')
class clear_my_party(Module):
    async def do_task(self, client: pcrclient):
        number: int = self.get_config('clear_team_num')
        tab_number: int = self.get_config('clear_tab_start_num')
        party_number: int = self.get_config('clear_party_start_num') - 1
        for _ in range(number):

            party_number += 1
            if party_number == 11:
                tab_number += 1
                party_number = 1
                if tab_number >= 6:
                    raise AbortError("队伍数量超过上限")

            self._log(f"清除了{tab_number}面板{party_number}队伍")
            await client.clear_my_party(tab_number, party_number)



@description('从指定面板的指定队开始设置，并调整星级。若干行重复，标题+若干行角色ID	角色名字	角色等级	角色星级\n忽略角色名字和角色等级')
@texttype("set_my_party_text", "队伍阵容", "")
@inttype("party_start_num", "初始队伍", 1, [i for i in range(1, 21)])
@inttype("tab_start_num", "初始面板", 1, [i for i in range(1, 7)])
@name('设置编队')
class set_my_party(Module):
    async def do_task(self, client: pcrclient):
        set_my_party_text: str = self.get_config('set_my_party_text')
        tab_number: int = self.get_config('tab_start_num')
        party_number: int = self.get_config('party_start_num')
        party = set_my_party_text.splitlines()
        title_id = [i for i, text in enumerate(party) if len(text.strip().split()) == 1]
        title_id.append(len(party))
        for i in range(len(title_id) - 1):

            if tab_number >= 6:
                raise AbortError("队伍数量超过上限")

            st = title_id[i]
            ed = title_id[i + 1]

            title = party[st].strip()
            unit_list = [u.split() for u in party[st + 1 : ed]]
            if len(unit_list) > 5:
                self._warn(f"{title}角色数超过5个，忽略该队伍")
                continue
            if len(unit_list) < 1:
                self._warn(f"{title}角色数小于1个，忽略该队伍")
                continue
            if len(set(u[0] for u in unit_list)) != len(unit_list):
                self._warn(f"{title}角色重复，忽略该队伍")
                continue

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

            party_number += 1
            if party_number == 21:
                tab_number += 1
                party_number = 1

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
