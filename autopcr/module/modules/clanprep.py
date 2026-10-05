'''会战准备：踩蘑菇作业对照名单的配套一键操作

目标角色配置留空时，自动使用"本期会战作业用到的角色 ∩ 已拥有角色"。
作业数据来自 autopcr/util/caimogu.py（带磁盘缓存，注意接口限流）。
'''
import re
from typing import Dict, List

from ...core.pcrclient import pcrclient
from ...db.database import db
from ...model.common import ExtraEquipChangeSlot, ExtraEquipChangeUnit, InventoryInfoPost
from ...model.enums import eInventoryType
from ...model.error import SkipError
from ...util.caimogu import fetch_latest, parse_battle
from ...util.ilp_solver import ex_equip_power_max_cost_flow
from ...util.linq import flow
from ..modulebase import *
from ..config import *
from .unit import UnitController


async def _load_battle() -> Dict:
    return parse_battle(await fetch_latest())


def _owned_unit(client: pcrclient, base_id: int) -> int:
    '''踩蘑菇4位基础id -> 已拥有的6位游戏unit_id(含换装变体)，未拥有返回0'''
    for game_id in client.data.unit:
        if game_id // 100 == base_id:
            return game_id
    return 0


def _default_targets(battle: Dict, client: pcrclient) -> List[int]:
    '''本期会战作业用到的角色 ∩ 已拥有，按使用次数降序，返回6位unit_id'''
    usage = battle["unit_usage"]
    result = []
    for base_id in sorted(usage, key=lambda k: (-usage[k], k)):
        game_id = _owned_unit(client, int(base_id))
        if game_id:
            result.append(game_id)
    return result


async def _resolve_targets(client: pcrclient, config_units: List) -> List[int]:
    '''目标角色：配置非空走手动指定(过滤空白项)，留空才拉作业数据取"本期名单∩已拥有"'''
    units = [u for u in config_units if str(u).strip()]
    if units:
        result = []
        for u in units:
            if not str(u).strip().isdigit():
                raise ValueError(f'目标角色id含非数字项: {u}')
            u = int(u)
            if u in client.data.unit:
                result.append(u)
            else:
                game_id = _owned_unit(client, u)
                if game_id:
                    result.append(game_id)
        return result
    battle = await _load_battle()
    return _default_targets(battle, client)


@description('为"本期会战作业用到的已拥有角色"购买记忆碎片并升至5星'
             '\n购买顺序：先商店与大师币商店，再母猪石商店'
             '\n目标角色留空 = 已拥有的本期会战名单'
             '\n注意：可能会消耗大师币/母猪石。如希望手动操作，请不要勾选主页处的自动一键拉5星')
@name('会战准备·一键拉5星')
@unitlist('clan_prep_star5_units', '目标角色(留空=本期会战名单)')
@booltype('clan_prep_star5_do_buy', '碎片不足时购买', True)
@booltype('clan_prep_star5_do_evolve', '执行升星', True)
@default(False)
class clan_prep_star5(UnitController):

    async def do_task(self, client: pcrclient):
        self.client = client
        targets = await _resolve_targets(client, self.get_config('clan_prep_star5_units'))
        do_buy = self.get_config('clan_prep_star5_do_buy')
        do_evolve = self.get_config('clan_prep_star5_do_evolve')
        if not targets:
            raise SkipError('没有目标角色(本期会战名单为空或名单内角色均未拥有)')
        self._table_header(['角色', '星级', '碎片缺口', '购买', '结果'])
        for game_id in targets:
            self.unit_id = game_id
            try:
                if self.unit_id not in client.data.unit:
                    self._warn(f'未解锁角色{self.unit_name}')
                    continue
                unit = client.data.unit[self.unit_id]
                if unit.unit_rarity >= 5:
                    continue
                token = (eInventoryType.Item, self.memory_id)
                cur = unit.unit_rarity
                required = db.rarity_up_required[self.unit_id]
                need = sum(required[r][token] for r in range(cur + 1, 6))
                have = client.data.get_inventory(token)
                gap = max(0, need - have)
                bought_desc = '-'
                if gap > 0 and do_buy:
                    before = gap
                    gap = await self.buy_memory(gap)
                    bought_desc = f'购买{before - gap}片'
                if gap > 0:
                    self._warn(f'{self.unit_name}升至5星还缺{gap}片记忆碎片')
                    self._table({'角色': self.unit_name, '星级': f'{cur}星', '碎片缺口': str(gap), '购买': bought_desc, '结果': '碎片不足'})
                    continue
                mana = sum(10_000 * i for i in range(cur + 1, 6))
                if do_evolve:
                    if not await client.prepare_mana(mana):
                        self._warn(f'{self.unit_name}升星需{mana}玛娜，玛娜不足')
                        continue
                    await client.unit_multi_evolution(
                        unit_id=self.unit_id,
                        current_rarity=cur,
                        after_rarity=5,
                        current_gold_num=client.data.get_mana(),
                        current_memory_piece_num=client.data.get_inventory(token),
                    )
                    self._table({'角色': self.unit_name, '星级': f'{cur}星', '碎片缺口': '0', '购买': bought_desc, '结果': f'升至5星(花费{mana}玛娜)'})
                else:
                    self._table({'角色': self.unit_name, '星级': f'{cur}星', '碎片缺口': '0', '购买': bought_desc, '结果': '碎片已齐，未执行升星'})
            except Exception as e:
                self._warn(f'{self.unit_name}处理失败: {e}')
                continue


@description('把"本期会战作业用到的已拥有角色"的等级/品级/装备/技能/专武拉至当前上限'
             '\n目标角色留空 = 已拥有的本期会战名单'
             '\n星级请用"一键拉5星"处理，会战EX装备请用"一键穿会战EX装"'
             '\n注意，买碎拉满专武同一键拉5星，会先商店再大师商店购买，最后母猪石商店。如希望手动操作，请不要勾选主页处的自动一键最高练度')
@name('会战准备·一键最高练度')
@unitlist('clan_prep_promote_units', '目标角色(留空=本期会战名单)')
@booltype('clan_prep_promote_use_raw_ore', '装备不足时用原矿补充', True)
@booltype('clan_prep_promote_unique', '拉满专武', True)
@booltype('clan_prep_promote_buy_shards', '买碎拉满专武', False)
@default(False)
class clan_prep_max_promote(UnitController):

    async def do_task(self, client: pcrclient):
        self.client = client
        self.use_raw_ore = self.get_config('clan_prep_promote_use_raw_ore')
        targets = await _resolve_targets(client, self.get_config('clan_prep_promote_units'))
        if not targets:
            raise SkipError('没有目标角色(本期会战名单为空或名单内角色均未拥有)')
        pull_unique = self.get_config('clan_prep_promote_unique')
        buy_shards = self.get_config('clan_prep_promote_buy_shards')
        max_rank = max(db.unit_rank_candidate())
        max_unique = {slot: max(db.unit_unique_equip_level_candidate(slot)) for slot in (1, 2)}
        for game_id in targets:
            self.unit_id = game_id
            try:
                if self.unit_id not in client.data.unit:
                    self._warn(f'未解锁角色{self.unit_name}')
                    continue
                # 等级上限按角色突破阶段算(与"队伍拉满"同口径)：未突破到team_max、已突破+10，
                # 避免给已到顶的未突破角色打出"目标超上限"警告
                max_level = db.team_max_level + 10 * self.unit.exceed_stage
                target_unique1 = max_unique[1] if 1 in db.unit_unique_equip and self.unit_id in db.unit_unique_equip[1] else 0
                target_unique2 = max_unique[2] if pull_unique and 2 in db.unit_unique_equip and self.unit_id in db.unit_unique_equip[2] else -1
                promote_kwargs = dict(
                    target_level=max_level,
                    target_star=self.unit.unit_rarity,
                    target_dear=1,
                    target_promote_rank=max_rank,
                    target_equip_star=[5] * 6,
                    target_skill_ub_level=max_level,
                    target_skill_s1_level=max_level,
                    target_skill_s2_level=max_level,
                    target_skill_ex_level=max_level,
                    target_unique1_level=target_unique1,
                    target_unique2_level=target_unique2,
                )
                warn_before = len(self.warn)
                await self.promote(**promote_kwargs)
                # 买碎拉满专武：promote 内部专武突破缺角色碎片时会转为警告（不中断），
                # 按警告里的缺口补购记忆碎片后重试一次
                if buy_shards:
                    gap = 0
                    for w in self.warn[warn_before:]:
                        m = re.search(r'缺少(\d+)片', str(w))
                        if m:
                            gap = max(gap, int(m.group(1)))
                    if gap > 0:
                        lack = await self.buy_memory(gap)
                        self._log(f'{self.unit_name}补购记忆碎片{gap - lack}片，重新拉满专武')
                        await self.promote(**promote_kwargs)
                self._log(f'{self.unit_name} 练度已拉至当前上限')
            except Exception as e:
                self._warn(f'{self.unit_name}练度提升失败: {e}')
                continue


@description('为"本期会战作业用到的已拥有角色"按排序尽可能穿上会战专用装备'
             '\n会先全员脱下会战栏装备，再为名单内角色统一穿上，并强化至最高等级'
             '\n目标角色留空 = 已拥有的本期会战名单'
             '\n关闭执行装备时只展示角色名单。如需要突破装备，请使用 合成EX装 功能')
@name('会战准备·一键穿会战EX装')
@unitlist('clan_prep_cb_ex_units', '目标角色(留空=本期会战名单)')
@booltype('clan_prep_cb_ex_do', '执行装备', True)
@booltype('clan_prep_cb_ex_enhance', '强化到满星', True)
@default(False)
class clan_prep_cb_ex(Module):

    async def do_task(self, client: pcrclient):
        targets = await _resolve_targets(client, self.get_config('clan_prep_cb_ex_units') or [])
        if not targets:
            raise SkipError('没有目标角色(本期会战名单为空或名单内角色均未拥有)')
        do_equip = self.get_config('clan_prep_cb_ex_do')
        do_enhance = self.get_config('clan_prep_cb_ex_enhance')
        if not do_equip:
            names = '、'.join(db.get_unit_name(uid) for uid in targets)
            self._log(f'执行装备未开启，仅展示角色名单({len(targets)}人)：{names}')
            return

        # 会战EX装备池：只排除CD锁定的（锁定装备不能动）。
        # 名单外角色已穿的不再视为"占用"——执行时会先全员脱下回收进池，全部会战装备统一参与分配
        locked = set(client.data.user_clan_battle_ex_equip_restriction.keys())
        pool = flow(client.data.ex_equips.values()) \
            .where(lambda ex: db.is_clan_ex_equip((eInventoryType.ExtraEquip, ex.ex_equipment_id))) \
            .where(lambda ex: ex.serial_id not in locked) \
            .to_list()

        st, ed = 'st', 'ed'
        edges = []
        read_story = set(client.data.read_story_ids)
        coefficient = db.unit_status_coefficient[1]
        for unit_id in targets:
            slot_data = db.unit_ex_equipment_slot.get(unit_id)
            if not slot_data:
                self._warn(f'{db.get_unit_name(unit_id)}无EX装备槽位数据，跳过')
                continue
            unit_node = f'u{unit_id}'
            edges.append((st, unit_node, 3, 0))
            unit_attr = db.calc_unit_attribute(client.data.unit[unit_id], read_story, client.data.ex_equips, exclude_ex_equip=True)
            for slot_id, ex_category in enumerate([slot_data.slot_category_1, slot_data.slot_category_2, slot_data.slot_category_3], start=1):
                unit_slot_node = f'{unit_node}k{slot_id}'
                edges.append((unit_node, unit_slot_node, 1, 0))
                by_star = flow(pool) \
                    .where(lambda ex: ex_category == db.ex_equipment_data[ex.ex_equipment_id].category) \
                    .group_by(lambda ex: db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)) \
                    .to_dict(lambda ex: ex.key, lambda ex: ex.to_list())
                for star, group in by_star.items():
                    consider = set()
                    for ex in group:
                        if db.get_ex_equip_rarity(ex.ex_equipment_id) == 5:
                            edges.append((unit_slot_node, f'r{ex.serial_id}', 1, 0))
                            continue
                        if ex.ex_equipment_id in consider:
                            continue
                        consider.add(ex.ex_equipment_id)
                        attr = db.ex_equipment_data[ex.ex_equipment_id].get_unit_attribute(star, ex.sub_status)
                        bonus = unit_attr.ex_equipment_mul(attr).ceil()
                        power = int(bonus.get_power(coefficient) + 0.5)
                        edges.append((unit_slot_node, f'e{ex.ex_equipment_id}s{star}', 1, -power))

        pool_by_key = {}
        for ex in pool:
            if db.get_ex_equip_rarity(ex.ex_equipment_id) == 5:
                edges.append((f'r{ex.serial_id}', ed, 1, 0))
            else:
                key = (ex.ex_equipment_id, db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt))
                pool_by_key[key] = pool_by_key.get(key, 0) + 1
        for (ex_id, star), cnt in pool_by_key.items():
            edges.append((f'e{ex_id}s{star}', ed, cnt, 0))

        if not any(u.startswith('u') for u, _, _, _ in edges):
            raise SkipError('没有可搭配的目标角色')
        min_cost, strategy = ex_equip_power_max_cost_flow(edges, st, ed)
        self._log(f'理论最大战力提升：{-min_cost}')

        slot_strategy: Dict[int, Dict[int, tuple]] = {}
        for u, v, flow_num in strategy:
            if flow_num == 0 or u == st or v == ed:
                continue
            if not (u.startswith('u') and 'k' in u):
                continue
            unit_id = int(u[1:u.index('k')])
            slot_id = int(u[u.index('k') + 1:])
            if v.startswith('r'):
                serial_id = int(v[1:])
                equip = client.data.ex_equips[serial_id]
                star = db.get_ex_equip_star_from_pt(equip.ex_equipment_id, equip.enhancement_pt)
                slot_strategy.setdefault(unit_id, {})[slot_id] = (equip.ex_equipment_id, star, serial_id)
            else:
                ex_id = int(v[1:v.index('s')])
                star = int(v[v.index('s') + 1:])
                slot_strategy.setdefault(unit_id, {})[slot_id] = (ex_id, star, None)

        used_serials = set()
        enhance_plan = []  # (unit_id, slot, serial_id, cur_pt, target_star)
        if do_equip:
            # 第一步：全员脱下会战栏装备（CD锁定中的保留原位），把全部会战装备回收进池——
            # 装备散在名单外角色身上时，名单内角色未必凑得齐
            stripped = 0
            locked_kept: Dict[int, Dict[int, int]] = {}  # unit_id -> {slot: serial}，CD锁定保留的槽
            for unit in client.data.unit.values():
                kept = {s.slot: s.serial_id for s in (unit.cb_ex_equip_slot or [])
                        if s.serial_id != 0 and s.serial_id in locked}
                to_strip = [s for s in (unit.cb_ex_equip_slot or [])
                            if s.serial_id != 0 and s.serial_id not in locked]
                if kept:
                    locked_kept[unit.id] = kept
                if not to_strip:
                    continue
                await client.unit_equip_ex([ExtraEquipChangeUnit(
                    unit_id=unit.id,
                    ex_equip_slot=None,
                    cb_ex_equip_slot=[ExtraEquipChangeSlot(slot=s.slot, serial_id=0) for s in to_strip],
                )])
                stripped += len(to_strip)
            if stripped:
                self._log(f'已全员脱下会战EX装备{stripped}件，统一重新分配')

        for unit_id in targets:
            unit = client.data.unit[unit_id]
            slots_map = slot_strategy.get(unit_id, {})
            kept = locked_kept.get(unit_id, {}) if do_equip else {}
            exchange_list = []
            # 全脱流程下槽位号固定(1~3)，硬遍历，不依赖脱下请求后 client.data 是否已同步
            for slot_no in (1, 2, 3):
                if slot_no in kept:
                    # CD锁定的装备保留原位，不参与重新分配
                    serial_id = kept[slot_no]
                    used_serials.add(serial_id)
                    exchange_list.append(ExtraEquipChangeSlot(slot=slot_no, serial_id=serial_id))
                    continue
                target = slots_map.get(slot_no)
                serial_id = 0
                if target:
                    ex_id, star, serial = target
                    if serial is not None:
                        serial_id = serial
                    else:
                        cand = flow(client.data.ex_equips.values()) \
                            .where(lambda ex: ex.ex_equipment_id == ex_id and db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt) == star) \
                            .where(lambda ex: ex.serial_id not in used_serials and ex.serial_id not in locked) \
                            .to_list()
                        if cand:
                            serial_id = cand[0].serial_id
                        else:
                            self._warn(f'{db.get_unit_name(unit_id)}无{db.get_ex_equip_name(ex_id)}★{star}可穿')
                if serial_id:
                    equip = client.data.ex_equips[serial_id]
                    max_star = db.get_ex_equip_max_star(equip.ex_equipment_id, equip.rank)
                    enhance_plan.append((unit_id, slot_no, serial_id, equip.enhancement_pt, max_star))
                    sub = db.get_ex_equip_sub_status_str(equip.ex_equipment_id, equip.sub_status or []) if equip.sub_status else ''
                    self._log(f'{db.get_unit_name(unit_id)} 会战栏{slot_no}号位 → {db.get_ex_equip_name(equip.ex_equipment_id)}★{star}{("(" + sub + ")") if sub else ""}')
                    used_serials.add(serial_id)
                exchange_list.append(ExtraEquipChangeSlot(slot=slot_no, serial_id=serial_id))
            if do_equip and any(s.serial_id != e.serial_id for s, e in zip(exchange_list, (unit.cb_ex_equip_slot or []))):
                await client.unit_equip_ex([ExtraEquipChangeUnit(
                    unit_id=unit_id,
                    ex_equip_slot=None,
                    cb_ex_equip_slot=exchange_list,
                )])

        enhanced = 0
        if do_enhance:
            for unit_id, slot, serial_id, cur_pt, max_star in enhance_plan:
                equip = client.data.ex_equips[serial_id]
                cur_star = db.get_ex_equip_star_from_pt(equip.ex_equipment_id, equip.enhancement_pt)
                if cur_star >= max_star:
                    continue
                demand_pt = db.get_ex_equip_enhance_pt(equip.ex_equipment_id, equip.enhancement_pt, max_star)
                demand_mana = db.get_ex_equip_enhance_mana(equip.ex_equipment_id, equip.enhancement_pt, max_star)
                if client.data.get_inventory(db.ex_pt) < demand_pt:
                    self._warn(f'强化PT不足(需{demand_pt})，{db.get_unit_name(unit_id)}的{db.get_ex_equip_name(equip.ex_equipment_id)}未强化')
                    continue
                if not await client.prepare_mana(demand_mana):
                    self._warn(f'玛娜不足(需{demand_mana})，{db.get_unit_name(unit_id)}的{db.get_ex_equip_name(equip.ex_equipment_id)}未强化')
                    continue
                await client.equipment_enhance_ex(
                    unit_id=unit_id,
                    serial_id=serial_id,
                    frame=2,
                    slot=slot,
                    before_enhancement_pt=cur_pt,
                    after_enhancement_pt=cur_pt + demand_pt,
                    consume_gold=demand_mana,
                    from_view=2,
                    item_list=[InventoryInfoPost(type=db.ex_pt[0], id=db.ex_pt[1], count=demand_pt)],
                    consume_ex_serial_id_list=[],
                )
                enhanced += 1
                self._log(f'{db.get_unit_name(unit_id)} 会战栏{slot}号位 {db.get_ex_equip_name(equip.ex_equipment_id)} 强化至★{max_star}')
            if enhanced:
                self._log(f'共强化{enhanced}个会战EX装备')

        if not do_equip and not do_enhance:
            self._log('未开启执行装备/强化，仅展示方案')
