from ...util.linq import flow
from ...util.ilp_solver import ex_equip_power_max_cost_flow
from ...model.common import ExtraEquipChangeSlot, ExtraEquipChangeUnit, InventoryInfoPost
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from collections import Counter

@name('强化EX装')
@default(True)
@booltype('ex_equip_enhance_view', '看消耗', True)
@inttype('ex_equip_enhance_max_num', '满强化个数', 5, list(range(-1, 51)))
@MultiChoiceConfig('ex_equip_enhance_up_kind', '强化种类', [], ['粉', '会战金', '普通金', '会战银'])
@description('仅使用强化PT强化至当前突破满星，不考虑突破。强化个数指同类满强化EX装超过阈值则不强化，-1表示不限制，看消耗指观察消耗资源情况，实际不执行强化')
class ex_equip_enhance_up(Module):
    async def do_task(self, client: pcrclient):
        use_ex_equip = {ex_slot.serial_id: [unit.id, frame, ex_slot.slot]
                        for unit in client.data.unit.values() 
                        for frame, ex_slots in enumerate([unit.ex_equip_slot, unit.cb_ex_equip_slot], start=1)
                        for ex_slot in ex_slots if ex_slot.serial_id != 0}

        ex_equip_enhance_up_kind = self.get_config('ex_equip_enhance_up_kind')
        ex_equip_enhance_max_nun = self.get_config('ex_equip_enhance_max_num')
        ex_equip_enhance_view = self.get_config('ex_equip_enhance_view')

        consider_ex_equips = flow(client.data.ex_equips.values()) \
                .where(lambda ex: 
                       '粉' in ex_equip_enhance_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 4 \
                or '会战金' in ex_equip_enhance_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 3 and db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id)) \
                or '普通金' in ex_equip_enhance_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 3 and not db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id)) \
                or '会战银' in ex_equip_enhance_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 2 and db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id))) \
                .to_list()

        consider_ex_equips.sort(key=lambda ex: (ex.rank, ex.ex_equipment_id), reverse=True)

        ex_equips_max_star_cnt = Counter()

        enhanceup_equip_cnt = 0
        consume_equip_pt = 0
        cost_mana = 0
        for equip in consider_ex_equips:
            max_star = db.get_ex_equip_max_star(equip.ex_equipment_id, equip.rank)
            cur_star = db.get_ex_equip_star_from_pt(equip.ex_equipment_id, equip.enhancement_pt)
            if cur_star >= max_star:
                ex_equips_max_star_cnt[equip.ex_equipment_id] += 1
                continue
            if ex_equip_enhance_max_nun != -1 and ex_equips_max_star_cnt[equip.ex_equipment_id] >= ex_equip_enhance_max_nun:
                continue
            demand_pt = db.get_ex_equip_enhance_pt(equip.ex_equipment_id, equip.enhancement_pt, max_star)
            if not ex_equip_enhance_view and client.data.get_inventory(db.ex_pt) < demand_pt:
                self._log(f"强化PT不足{demand_pt}，无法强化EX装")
                break

            demand_mana = db.get_ex_equip_enhance_mana(equip.ex_equipment_id, equip.enhancement_pt, max_star)
            if not ex_equip_enhance_view and not await client.prepare_mana(demand_mana):
                self._log(f"mana数不足{demand_mana}，无法强化EX装")
                break

            enhanceup_equip_cnt += 1
            consume_equip_pt += demand_pt
            cost_mana += demand_mana

            ex_equips_max_star_cnt[equip.ex_equipment_id] += 1

            unit_id, frame, slot = use_ex_equip.get(equip.serial_id, [0, 0, 0])
            if ex_equip_enhance_view:
                continue
            await client.equipment_enhance_ex(
                unit_id=unit_id,
                serial_id=equip.serial_id,
                frame=frame,
                slot=slot,
                before_enhancement_pt=equip.enhancement_pt,
                after_enhancement_pt=equip.enhancement_pt + demand_pt,
                consume_gold=demand_mana,
                from_view=2,
                item_list=[
                    InventoryInfoPost(type = db.ex_pt[0], id = db.ex_pt[1], count = demand_pt)
                ],
                consume_ex_serial_id_list=[],
            )

        if enhanceup_equip_cnt:
            if ex_equip_enhance_view:
                self._log(f"需消耗{consume_equip_pt}强化PT和{cost_mana} mana来强化{enhanceup_equip_cnt}个EX装")
                self._log(f"当前强化PT {client.data.get_inventory(db.ex_pt)}, mana {client.data.get_inventory(db.mana)}")
            else:
                self._log(f"消耗了{consume_equip_pt}强化PT和{cost_mana}mana，强化了{enhanceup_equip_cnt}个EX装")
        else:
            raise SkipError("没有可强化的EX装")

@name('合成EX装')
@default(True)
@inttype('ex_equip_rank_max_num', '满突破个数', 5, list(range(-1, 51)))
@MultiChoiceConfig('ex_equip_rank_up_kind', '合成种类', [], ['粉', '会战金', '普通金', '会战银'])
@description('合成忽略已装备和锁定的EX装，满突破个数指同类满突破EX装超过阈值则不突破，-1表示不限制')
class ex_equip_rank_up(Module):
    async def do_task(self, client: pcrclient):
        use_ex_equip = {ex_slot.serial_id: [unit.id, frame, ex_slot.slot]
                        for unit in client.data.unit.values() 
                        for frame, ex_slots in enumerate([unit.ex_equip_slot, unit.cb_ex_equip_slot], start=1)
                        for ex_slot in ex_slots if ex_slot.serial_id != 0}

        ex_equip_rank_up_kind = self.get_config('ex_equip_rank_up_kind')
        ex_equip_rank_max_num = self.get_config('ex_equip_rank_max_num')

        consider_ex_equips = flow(client.data.ex_equips.values()) \
                .where(lambda ex: ex.protection_flag != 2) \
                .where(lambda ex: 
                       '粉' in ex_equip_rank_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 4 \
                or '会战金' in ex_equip_rank_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 3 and db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id)) \
                or '普通金' in ex_equip_rank_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 3 and not db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id)) \
                or '会战银' in ex_equip_rank_up_kind and db.get_ex_equip_rarity(ex.ex_equipment_id) == 2 and db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id))) \
                .to_list()

        zero_rank_ex = flow(consider_ex_equips) \
                    .where(lambda ex: ex.serial_id not in use_ex_equip and ex.rank == 0) \
                    .group_by(lambda ex: ex.ex_equipment_id) \
                    .to_dict(lambda ex: ex.key, lambda ex: ex.to_list())

        ex_equips_max_rank_cnt = Counter(flow(client.data.ex_equips.values()) \
                .where(lambda ex: ex.rank == db.get_ex_equip_max_rank(ex.ex_equipment_id)) \
                .group_by(lambda ex: ex.ex_equipment_id) \
                .to_dict(lambda ex: ex.key, lambda ex: ex.count()))

        rankup_equip_cnt = 0
        consume_equip_cnt = 0
        cost_mana = 0
        for equip in consider_ex_equips:
            if equip.serial_id not in client.data.ex_equips:
                continue
            max_rank = db.get_ex_equip_max_rank(equip.ex_equipment_id)
            if equip.rank >= max_rank:
                continue
            if ex_equip_rank_max_num != -1 and ex_equips_max_rank_cnt[equip.ex_equipment_id] >= ex_equip_rank_max_num:
                continue
            demand = max_rank - equip.rank
            use_series = flow(zero_rank_ex.get(equip.ex_equipment_id, [])) \
                .where(lambda ex: ex.serial_id != equip.serial_id 
                       and ex.serial_id in client.data.ex_equips 
                       and client.data.ex_equips[ex.serial_id].rank == 0) \
                .take(demand) \
                .select(lambda ex: ex.serial_id) \
                .to_list()

            if use_series:
                rankup_equip_cnt += 1
                consume_equip_cnt += len(use_series)
                final_rank = equip.rank + len(use_series)
                mana = db.get_ex_equip_rankup_cost(equip.ex_equipment_id, equip.rank, final_rank)
                cost_mana += mana
                if not await client.prepare_mana(mana):
                    self._log(f"mana数不足{mana}，无法合成EX装")
                    break
                unit_id, frame, slot = use_ex_equip.get(equip.serial_id, [0, 0, 0])
                await client.equipment_rankup_ex(
                    serial_id=equip.serial_id,
                    unit_id=unit_id,
                    frame=frame,
                    slot=slot,
                    before_rank=equip.rank,
                    after_rank=final_rank,
                    consume_gold=mana,
                    from_view=2,
                    item_list=[],
                    consume_ex_serial_id_list=use_series
                )
                if final_rank == max_rank:
                    ex_equips_max_rank_cnt[equip.ex_equipment_id] += 1


        if rankup_equip_cnt:
            self._log(f"消耗了{consume_equip_cnt}个零星EX装和{cost_mana}mana，合成了{rankup_equip_cnt}个EX装")
        else:
            raise SkipError("没有可合成的EX装")


@name('撤下会战EX装')
@default(True)
@description('')
class remove_cb_ex_equip(Module):
    async def do_task(self, client: pcrclient):
        ex_cnt = 0
        unit_cnt = 0
        forbidden = set(client.data.user_clan_battle_ex_equip_restriction.keys())
        no_remove_for_forbidden = 0
        for unit_id in client.data.unit:
            unit = client.data.unit[unit_id]
            exchange_list = []
            for ex_equip in unit.cb_ex_equip_slot:
                if ex_equip.serial_id != 0 and ex_equip.serial_id not in forbidden:
                    exchange_list.append(ExtraEquipChangeSlot(slot=ex_equip.slot, serial_id=0))
                    ex_cnt += 1
                elif ex_equip.serial_id in forbidden:
                    no_remove_for_forbidden += 1

            if exchange_list:
                unit_cnt += 1
                await client.unit_equip_ex([ExtraEquipChangeUnit(
                        unit_id=unit_id, 
                        ex_equip_slot = None,
                        cb_ex_equip_slot=exchange_list)])
        if ex_cnt:
            msg = f"（{no_remove_for_forbidden}个因会战CD未撤下）" if no_remove_for_forbidden else ""
            self._log(f"撤下了{unit_cnt}个角色的{ex_cnt}个会战EX装备{msg}")
        else:
            raise SkipError("所有会战EX装备均已撤下")


@name('EX装战力最高搭配')
@default(True)
@description('理论最优，执行装备将撤下所有EX装备，然后再进行最优搭配')
@booltype('ex_equip_power_maximun_do', '执行装备', False)
class ex_equip_power_maximun(Module):
    async def do_task(self, client: pcrclient):
        st = "st"
        ed = "ed"
        edges = []
        read_story = set(client.data.read_story_ids)
        coefficient = db.unit_status_coefficient[1]
        for unit_id in client.data.unit:
            unit_node = f"u{unit_id}"
            edges.append((st, unit_node, 3, 0))

            unit_attr = db.calc_unit_attribute(client.data.unit[unit_id], read_story, client.data.ex_equips)

            slot_data = db.unit_ex_equipment_slot[unit_id]
            for ex_category in [slot_data.slot_category_1, slot_data.slot_category_2, slot_data.slot_category_3]:
                ex_equip_group_by_star = flow(client.data.ex_equips.values()) \
                        .where(lambda ex: ex_category == db.ex_equipment_data[ex.ex_equipment_id].category) \
                        .group_by(lambda ex: db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)) \
                        .to_dict(lambda ex: ex.key, lambda ex: ex.to_list())
                for star in ex_equip_group_by_star:
                    consider_ex = set()
                    for ex in ex_equip_group_by_star[star]:
                        if ex.ex_equipment_id in consider_ex:
                            continue
                        consider_ex.add(ex.ex_equipment_id)
                        ex_node = f"e{ex.ex_equipment_id}s{star}"
                        attr = db.ex_equipment_data[ex.ex_equipment_id].get_unit_attribute(star)
                        bonus = unit_attr.ex_equipment_mul(attr).ceil()
                        power = int(bonus.get_power(coefficient) + 0.5)
                        edges.append((unit_node, ex_node, 1, -power))

        ex_equips_group_by_id_star = flow(client.data.ex_equips.values()) \
                .group_by(lambda ex: (ex.ex_equipment_id, db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt))) \
                .to_dict(lambda ex: ex.key, lambda ex: ex.count())
        for (ex_id, star) in ex_equips_group_by_id_star:
            ex_node = f"e{ex_id}s{star}"
            edges.append((ex_node, ed, ex_equips_group_by_id_star[(ex_id, star)], 0))
        min_cost, strategy = ex_equip_power_max_cost_flow(edges, st, ed)
        self._log(f"最大战力提升：{-min_cost}")

        slot_strategy = []
        for u, v, flow_num in strategy:
            if u == st or v == ed or flow_num == 0:
                continue
            unit_id = int(u[1:])
            ex_equipment_id = int(v[1:v.index('s')])
            star = int(v[v.index('s') + 1:])

            slot_strategy.append((unit_id, ex_equipment_id, star))

        slot_strategy = flow(slot_strategy) \
                .group_by(lambda x: x[0]) \
                .to_dict(lambda x: x.key, lambda x: x.to_list())
        do_equip = self.get_config('ex_equip_power_maximun_do')
        if do_equip:
            cnt = 0
            for unit_id in client.data.unit:
                unit = client.data.unit[unit_id]
                exchange_list = []
                for ex_slot in unit.ex_equip_slot:
                    if ex_slot.serial_id != 0:
                        exchange_list.append(ExtraEquipChangeSlot(slot=ex_slot.slot, serial_id=0))
                if exchange_list:
                    cnt += 1
                    await client.unit_equip_ex([ExtraEquipChangeUnit(
                            unit_id=unit_id, 
                            ex_equip_slot=exchange_list[:len(unit.ex_equip_slot)],
                            cb_ex_equip_slot=None)])
            if cnt:
                self._log(f"撤下了{cnt}个角色的EX装备")

            use_series_set = set()
            for unit_id in slot_strategy:
                unit = client.data.unit[unit_id]
                exchange_list = []
                for (_, ex_equipment_id, star) in slot_strategy[unit_id]:
                    ex_candidates = flow(client.data.ex_equips.values()) \
                            .where(lambda ex: ex.ex_equipment_id == ex_equipment_id and db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt) == star) \
                            .where(lambda ex: ex.serial_id not in use_series_set) \
                            .to_list()
                    if not ex_candidates:
                        continue
                    ex_to_equip = ex_candidates[0]
                    use_series_set.add(ex_to_equip.serial_id)
                    slot_data = db.unit_ex_equipment_slot[unit_id]
                    if db.ex_equipment_data[ex_equipment_id].category == slot_data.slot_category_1:
                        slot = 1
                    elif db.ex_equipment_data[ex_equipment_id].category == slot_data.slot_category_2:
                        slot = 2
                    else:
                        slot = 3
                    exchange_list.append(ExtraEquipChangeSlot(slot=slot, serial_id=ex_to_equip.serial_id))
                if exchange_list:
                    await client.unit_equip_ex([ExtraEquipChangeUnit(
                            unit_id=unit_id, 
                            ex_equip_slot=exchange_list,
                            cb_ex_equip_slot=None)])

        for unit_id in slot_strategy:
            msg = []
            for (_, ex_equipment_id, star) in slot_strategy[unit_id]:
                msg.append(f"{db.get_ex_equip_name(ex_equipment_id)}★{star}")
            msg = ','.join(msg)
            self._log(f"{db.get_unit_name(unit_id)} 装备 {msg}")

