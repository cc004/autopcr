from ...util.linq import flow
from ...util.ilp_solver import ex_equip_power_max_cost_flow
from ...model.common import ExtraEquipChangeSlot, ExtraEquipChangeUnit, InventoryInfoPost, AlcesSubStatusResult, ExtraEquipSubStatus
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from collections import Counter

ALCES_AUTO_EXEC_COUNT = 100

@name('彩装究极炼成')
@default(True)
@inttype('ex_equip_rainbow_enhance_pt_hold', '保留pt数(w)', 10, list(range(0, 10001)))
@ExEquipSubStatusRankConfig('ex_equip_rainbow_enhance_rank', '属性优先级')
@inttype('ex_equip_rainbow_enhance_no_max_num', '不需要满属性的词条个数', 1, [0, 1, 2, 3, 4])
@inttype('ex_equip_rainbow_enchance_target_sum', '需求的属性总值', 0, range(0, 21))
@ExEquipSubStatusConfig('ex_equip_rainbow_enchance_sub_status_4', '炼成属性4')
@ExEquipSubStatusConfig('ex_equip_rainbow_enchance_sub_status_3', '炼成属性3')
@ExEquipSubStatusConfig('ex_equip_rainbow_enchance_sub_status_2', '炼成属性2')
@ExEquipSubStatusConfig('ex_equip_rainbow_enchance_sub_status_1', '炼成属性1')
@singlechoice('ex_equip_rainbow_enchance_action', '做什么', '看属性', ['看属性', '炼成', '看概率'])
@texttype('ex_equip_rainbow_enchance_id', '彩装id（记得按回车顺便刷新）', 0)
@description('看属性指获取彩装id和炼成属性,炼成则进行究极炼成,看概率指根据炼成记录统计各属性概率,非满属性指属性值不必最大,以便手动用光球强化.属性优先级指目标属性值一样时,比较其他属性决定保留或放弃,优先级是按顺序从高到低,目标属性的优先级最高,不受属性优先级影响.满强目标属性会自动锁住.')
class ex_equip_rainbow_enchance(Module):

    async def do_task(self, client: pcrclient):
        ex_equip_rainbow_enchance_action = self.get_config('ex_equip_rainbow_enchance_action')
        if ex_equip_rainbow_enchance_action == '看属性':
            msg = flow(client.data.ex_equips.values()) \
                .where(lambda ex: db.get_ex_equip_rarity(ex.ex_equipment_id) == 5) \
                .select(lambda ex: f"{ex.serial_id}: {db.get_ex_equip_name(ex.ex_equipment_id)} "
                                  f"{db.get_ex_equip_sub_status_str(ex.ex_equipment_id, ex.sub_status or [])}") \
                .to_list()
            cnt = len(msg)
            if not cnt:
                raise SkipError("无彩装")
            msg = '\n'.join(msg)
            self._log(f"{cnt}件彩装:\n{msg}")
        elif ex_equip_rainbow_enchance_action == '看概率':
            for equip, data in self.iter_cache():
                total = sum(data.values())
                if total == 0:
                    continue
                equip = int(equip)
                self._log(f"{db.get_ex_equip_name(equip)}({total}次词条刷新)")
                info = flow(data.items()) \
                    .where(lambda kv: kv[0] != 'total') \
                    .select(lambda kv: (list(map(int, kv[0].split('-'))), kv[1])) \
                    .group_by(lambda kv: kv[0][0]) \
                    .to_dict(lambda g: g.key, lambda g: g.to_list())
                for status in sorted(info):
                    status_info = info[status]
                    status_info.sort(key=lambda x: x[0][1])
                    msg = '/'.join([f"{db.get_ex_equip_sub_status_str(equip, [ExtraEquipSubStatus(status=k, step=s)])}: {v/total * 100:.2f}%" for (k, s), v in status_info])
                    self._log(f"  {msg}")
                self._log("")

        elif ex_equip_rainbow_enchance_action == '炼成':
            serial_id = self.get_config('ex_equip_rainbow_enchance_id')
            if not serial_id.isdigit():
                raise AbortError("彩装id非法")
            serial_id = int(serial_id)
            if serial_id not in client.data.ex_equips or db.get_ex_equip_rarity(client.data.ex_equips[serial_id].ex_equipment_id) != 5:
                raise AbortError("彩装id不存在")
            
            group = db.ex_equipment_sub_status_group[client.data.ex_equips[serial_id].ex_equipment_id]
            sub_status_data = db.ex_equipment_sub_status[group.group_id]
            target_sub_status = Counter()
            for i in range(1, 5):
                val = self.get_config(f'ex_equip_rainbow_enchance_sub_status_{i}')
                if val:
                    target_sub_status[val] += 1
            
            invalid_status = [status for status in target_sub_status if status not in sub_status_data]
            if invalid_status:
                raise AbortError(f"炼成属性包含该装备不支持的属性: {', '.join(UnitAttribute.index2ch[eParamType(s)] for s in invalid_status)}")

            self.cache_info = self.find_cache(str(client.data.ex_equips[serial_id].ex_equipment_id))
            if not self.cache_info:
                self.cache_info = Counter()
            else:
                self.cache_info = Counter(self.cache_info)


            target_sum = self.get_config('ex_equip_rainbow_enchance_target_sum')
            if target_sum > 0:
                self._log(f"属性总值阈值: {target_sum}")

            base = 1
            self.weight = Counter()
            rank_order = self.get_config('ex_equip_rainbow_enhance_rank')
            for key in rank_order[::-1]:
                if key not in target_sub_status:
                    self.weight[key] += base
                    base *= 30
            for key in target_sub_status:
                self.weight[key] += base
                
            top = await client.alces_top()
            if top.pending_alces_data:
                if top.pending_alces_data.serial_id != serial_id:
                    raise AbortError(f"{top.pending_alces_data.serial_id}炼成属性待决定,请先自行决定")
                _, pending_target_step = self.get_alces_auto_target(
                    client, serial_id, target_sub_status, no_max_num
                )
                await self.decide_alces(
                    client,
                    top.pending_alces_data,
                    target_sub_status,
                    target_step=pending_target_step,
                )

            no_max_num = self.get_config('ex_equip_rainbow_enhance_no_max_num')
            target_cnt = sum(target_sub_status.values())

            if no_max_num > target_cnt:
                raise AbortError(f"非满属性个数{no_max_num}不能大于非任意的目标属性个数{target_cnt}")

            consume_cnt = Counter()
            alces_exec_cnt = 0
            last_lock_cnt = 0
            stop = False
            


            # self._log(f"各属性加权值: " + ', '.join(f"{UnitAttribute.index2ch[eParamType(k)]}: {v}" for k, v in self.weight.items()))

            self._log(f"当前彩装属性 " +
                      f"{serial_id}: {db.get_ex_equip_name(client.data.ex_equips[serial_id].ex_equipment_id)} "
                      f"{db.get_ex_equip_sub_status_str(client.data.ex_equips[serial_id].ex_equipment_id, client.data.ex_equips[serial_id].sub_status or [])}")

            pt_hold = self.get_config('ex_equip_rainbow_enhance_pt_hold')
                
            while not stop:
                if target_sum > 0:
                    current_total = await self.get_current_target_value(client, serial_id, target_sub_status)
                    self._log(f"当前目标属性值: {current_total}")
                    if current_total >= target_sum:
                        self._log(f"当前目标属性值{current_total} ≥ 阈值{target_sum}，停止洗练")
                        break
                
                achived_max_cnt, achived_cnt = await self.get_achived_sub_status_cnt(client, serial_id, target_sub_status)
                if achived_max_cnt >= target_cnt - no_max_num and achived_cnt >= target_cnt:
                    self._log("彩装炼成属性已达成目标")
                    break

                lock_cnt = await self.do_lock(client, serial_id, target_sub_status)

                if last_lock_cnt != lock_cnt:
                    self._log(f"L 锁定属性个数{last_lock_cnt} -> {lock_cnt}")
                    last_lock_cnt = lock_cnt

                if client.data.get_inventory(db.ex_rainbow_enhance_pt) <= pt_hold * 10000:
                    self._warn(f"彩装究极炼成PT{client.data.get_inventory(db.ex_rainbow_enhance_pt)}<={pt_hold * 10000}，停止炼成")
                    break

                per_exec_consume = Counter()
                exec_count = ALCES_AUTO_EXEC_COUNT
                for consume, item in db.alces_cost.items():
                    cost = item.count
                    cur = client.data.get_inventory(consume)
                    cost *= lock_cnt + 1
                    per_exec_consume[consume] = cost
                    if cur < cost:
                        self._warn(f"E {db.get_inventory_name_san(consume)}数量{cur}<{cost}，无法进行究极炼成")
                        stop = True
                        continue

                    affordable_count = cur // cost
                    if consume == db.ex_rainbow_enhance_pt:
                        reserve = pt_hold * 10000
                        # 与原单次逻辑一致：只要开始执行时高于保留值，至少允许本轮执行一次。
                        affordable_count = max(1, (cur - reserve) // cost)
                    exec_count = min(exec_count, affordable_count)

                if stop:
                    break
                auto_target_status, auto_target_step = self.get_alces_auto_target(
                    client, serial_id, target_sub_status, no_max_num
                )
                resp = await client.alces_exec_auto(
                    serial_id,
                    exec_count,
                    auto_target_status,
                    auto_target_step,
                )
                result_list = resp.sub_status_result_list or []
                if not result_list:
                    raise AbortError("批量究极炼成未返回属性结果")

                for result_index, alces_data in enumerate(result_list, start=1):
                    self.record_alces_result(alces_data)
                    if result_index < len(result_list):
                        self._log(f"批量炼成的第{result_index}次炼成属性: {db.get_ex_equip_sub_status_str(client.data.ex_equips[serial_id].ex_equipment_id, alces_data.sub_status or [])}")

                pending_alces_data = result_list[-1]
                accept = await self.decide_alces(
                    client,
                    pending_alces_data,
                    target_sub_status,
                    record_result=False,
                    target_step=auto_target_step,
                )
                actual_exec_count = len(result_list)
                alces_exec_cnt += actual_exec_count
                for consume, cost in per_exec_consume.items():
                    consume_cnt[consume] += cost * actual_exec_count

                # self._log(f"{'A 接受' if accept else 'R 放弃'}批量炼成的第{len(result_list)}次炼成属性: {db.get_ex_equip_sub_status_str(client.data.ex_equips[serial_id].ex_equipment_id, pending_alces_data.sub_status or [])}")

            if alces_exec_cnt:
                self._log(f"共进行了{alces_exec_cnt}次究极炼成，消耗了：")
                for consume in consume_cnt:
                    self._log(f"  {db.get_inventory_name_san(consume)} x {consume_cnt[consume]}")
            
            if target_sum > 0:
                final_total = await self.get_current_target_value(client, serial_id, target_sub_status)
                self._log(f"最终目标属性值: {final_total}")
            
            self.save_cache(str(client.data.ex_equips[serial_id].ex_equipment_id), self.cache_info)
            self._log(f"最终彩装属性 " +
                      f"{serial_id}: {db.get_ex_equip_name(client.data.ex_equips[serial_id].ex_equipment_id)} "
                      f"{db.get_ex_equip_sub_status_str(client.data.ex_equips[serial_id].ex_equipment_id, client.data.ex_equips[serial_id].sub_status or [])}")
        else:
            raise AbortError(f"未知操作{ex_equip_rainbow_enchance_action}")
    
    async def do_lock(self, client: pcrclient, serial_id: int, target_sub_status: Counter):
        current_max_sub_status = Counter()
        lock_cnt = 0
        for status in client.data.ex_equips[serial_id].sub_status or []:
            to_lock = False
            if current_max_sub_status[status.status] < target_sub_status[status.status] and status.step == 5:
                current_max_sub_status[status.status] += 1
                to_lock = True
                lock_cnt += 1
            if to_lock != status.is_lock:
                await client.alces_lock_slot(serial_id, status.slot_number, to_lock)
        return lock_cnt

    def get_alces_auto_target(self, client: pcrclient, serial_id: int, target_sub_status: Counter, no_max_num: int) -> Tuple[List[int], int]:
        current_sub_status = Counter(
            status.status
            for status in client.data.ex_equips[serial_id].sub_status or []
        )
        current_max_sub_status = Counter(
            status.status
            for status in client.data.ex_equips[serial_id].sub_status or []
            if status.step == 5
        )

        required_max_cnt = sum(target_sub_status.values()) - no_max_num
        achieved_max_cnt = sum((current_max_sub_status & target_sub_status).values())
        if achieved_max_cnt < required_max_cnt:
            current_target_sub_status = current_max_sub_status
            target_step = 5
        else:
            current_target_sub_status = current_sub_status
            target_step = 1

        target_status = [
            status
            for status, count in target_sub_status.items()
            if current_target_sub_status[status] < count
        ]
        return target_status, target_step

    def record_alces_result(self, alces_data: AlcesSubStatusResult):
        for status in alces_data.sub_status:
            if not status.is_lock:
                self.cache_info[f"{status.status}-{status.step}"] += 1

    async def decide_alces(self, client: pcrclient, alces_data: AlcesSubStatusResult, target_sub_status: Counter, record_result: bool = True, target_step: int = 5):
        accept = False
        current_max_sub_status = Counter()

        if record_result:
            self.record_alces_result(alces_data)

        for status in alces_data.sub_status:
            if status.is_lock:
                current_max_sub_status[status.status] += 1
                continue
            if current_max_sub_status[status.status] < target_sub_status[status.status] and status.step >= target_step:
                current_max_sub_status[status.status] += 1
                accept = True
        
        if not accept:
            current_score = sum(status.step * self.weight[status.status] for status in client.data.ex_equips[alces_data.serial_id].sub_status or [])
            nxt_score = sum(status.step * self.weight[status.status] for status in alces_data.sub_status)
            # self._log(f"当前目标属性加权值{current_score}，新属性加权值{nxt_score}")

            if nxt_score > current_score:
                accept = True

        if accept:
            await client.alces_fix_result(alces_data.serial_id)
        else:
            await client.alces_cancel_result(alces_data.serial_id)
        return accept

    async def get_achived_sub_status_cnt(self, client: pcrclient, serial_id: int, target_sub_status: Counter) -> Tuple[int, int]:
        ex_equip = client.data.ex_equips[serial_id]
        current_sub_status = Counter(status.status for status in ex_equip.sub_status or [])
        max_sub_status = Counter(status.status for status in ex_equip.sub_status or [] if status.step == 5)

        achived_cnt = current_sub_status & target_sub_status
        achived_cnt = sum(achived_cnt.values())
        achived_max_cnt = max_sub_status & target_sub_status
        achived_max_cnt = sum(achived_max_cnt.values())
        return achived_max_cnt, achived_cnt
    
    async def get_current_target_value(self, client: pcrclient, serial_id: int, target_sub_status: Counter) -> int:
        ex_equip = client.data.ex_equips[serial_id]
        attr_str = db.get_ex_equip_sub_status_str(ex_equip.ex_equipment_id, ex_equip.sub_status or [])
        
        target_value = 0
        target_keys = target_sub_status.keys()
        
        for target_key in target_keys:
            attr_name = UnitAttribute.index2ch[eParamType(target_key)] if hasattr(UnitAttribute, 'index2ch') else str(target_key)
            
            if attr_name in attr_str:
                import re
                pattern = rf'{attr_name}[×x](\d+(?:\.\d+)?)'
                match = re.search(pattern, attr_str)
                if match:
                    try:
                        value = float(match.group(1))
                        target_value += value
                    except:
                        pass
        
        return int(target_value) if target_value == int(target_value) else target_value

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

@name('撤下普通EX装')
@default(True)
@description('')
class remove_normal_ex_equip(Module):
    async def do_task(self, client: pcrclient):
        ex_cnt = 0
        unit_cnt = 0
        for unit_id in client.data.unit:
            unit = client.data.unit[unit_id]
            exchange_list = []
            for ex_equip in unit.ex_equip_slot:
                if ex_equip.serial_id != 0:
                    exchange_list.append(ExtraEquipChangeSlot(slot=ex_equip.slot, serial_id=0))
                    ex_cnt += 1

            if exchange_list:
                unit_cnt += 1
                await client.unit_equip_ex([ExtraEquipChangeUnit(
                        unit_id=unit_id, 
                        ex_equip_slot=exchange_list,
                        cb_ex_equip_slot=None)])
        if ex_cnt:
            self._log(f"撤下了{unit_cnt}个角色的{ex_cnt}个普通EX装备")
        else:
            raise SkipError("所有普通EX装备均已撤下")

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

            unit_attr = db.calc_unit_attribute(client.data.unit[unit_id], read_story, client.data.ex_equips, exclude_ex_equip = True)

            slot_data = db.unit_ex_equipment_slot[unit_id]
            for slot_id, ex_category in enumerate([slot_data.slot_category_1, slot_data.slot_category_2, slot_data.slot_category_3], start=1):
                unit_slot_node = f"{unit_node}k{slot_id}"
                edges.append((unit_node, unit_slot_node, 1, 0))
                ex_equip_group_by_star = flow(client.data.ex_equips.values()) \
                        .where(lambda ex: ex_category == db.ex_equipment_data[ex.ex_equipment_id].category) \
                        .group_by(lambda ex: db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)) \
                        .to_dict(lambda ex: ex.key, lambda ex: ex.to_list())
                for star in ex_equip_group_by_star:
                    consider_ex = set()
                    for ex in ex_equip_group_by_star[star]:
                        if db.get_ex_equip_rarity(ex.ex_equipment_id) == 5:
                            ex_node = f"r{ex.serial_id}"
                        else:
                            if ex.ex_equipment_id in consider_ex:
                                continue
                            consider_ex.add(ex.ex_equipment_id)
                            ex_node = f"e{ex.ex_equipment_id}s{star}"

                        attr = db.ex_equipment_data[ex.ex_equipment_id].get_unit_attribute(star, ex.sub_status)
                        bonus = unit_attr.ex_equipment_mul(attr).ceil()
                        power = int(bonus.get_power(coefficient) + 0.5)
                        edges.append((unit_slot_node, ex_node, 1, -power))

        rainbow_serial_ids = set()
        for ex in client.data.ex_equips.values():
            if db.get_ex_equip_rarity(ex.ex_equipment_id) == 5:
                ex_node = f"r{ex.serial_id}"
                edges.append((ex_node, ed, 1, 0))
                rainbow_serial_ids.add(ex.serial_id)

        ex_equips_group_by_id_star = flow(client.data.ex_equips.values()) \
                .where(lambda ex: db.get_ex_equip_rarity(ex.ex_equipment_id) != 5) \
                .group_by(lambda ex: (ex.ex_equipment_id, db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt))) \
                .to_dict(lambda ex: ex.key, lambda ex: ex.count())
        for (ex_id, star) in ex_equips_group_by_id_star:
            ex_node = f"e{ex_id}s{star}"
            edges.append((ex_node, ed, ex_equips_group_by_id_star[(ex_id, star)], 0))
        min_cost, strategy = ex_equip_power_max_cost_flow(edges, st, ed)
        self._log(f"最大战力提升：{-min_cost}")

        slot_strategy = []
        for u, v, flow_num in strategy:
            if u == st or v == ed or flow_num == 0 or u.startswith("u") and v.startswith("u"):
                continue
            unit_id = int(u[1:u.index('k')])
            slot_id = int(u[u.index('k') + 1:])

            if v.startswith("r"):
                serial_id = int(v[1:])
                ex_equip = client.data.ex_equips[serial_id]
                ex_equipment_id = ex_equip.ex_equipment_id
                star = db.get_ex_equip_star_from_pt(ex_equipment_id, ex_equip.enhancement_pt)
                slot_strategy.append((unit_id, slot_id, ex_equipment_id, star, serial_id))
            else:
                ex_equipment_id = int(v[1:v.index('s')])
                star = int(v[v.index('s') + 1:])
                slot_strategy.append((unit_id, slot_id, ex_equipment_id, star, None))

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
                for (_, slot, ex_equipment_id, star, serial_id) in slot_strategy[unit_id]:
                    if serial_id is not None:
                        if serial_id in use_series_set:
                            self._warn(f"彩装{db.get_ex_equip_name(ex_equipment_id)}(serial:{serial_id})已被使用")
                            continue
                        use_series_set.add(serial_id)
                        exchange_list.append(ExtraEquipChangeSlot(slot=slot, serial_id=serial_id))
                    else:
                        ex_candidates = flow(client.data.ex_equips.values()) \
                                .where(lambda ex: ex.ex_equipment_id == ex_equipment_id and db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt) == star) \
                                .where(lambda ex: ex.serial_id not in use_series_set) \
                                .to_list()
                        if not ex_candidates:
                            self._warn(f"无{db.get_ex_equip_name(ex_equipment_id)}★{star}，无法装备")
                            continue
                        ex_to_equip = ex_candidates[0]
                        use_series_set.add(ex_to_equip.serial_id)
                        exchange_list.append(ExtraEquipChangeSlot(slot=slot, serial_id=ex_to_equip.serial_id))
                if exchange_list:
                    await client.unit_equip_ex([ExtraEquipChangeUnit(
                            unit_id=unit_id, 
                            ex_equip_slot=exchange_list,
                            cb_ex_equip_slot=None)])

        for unit_id in slot_strategy:
            msg = []
            for (_, slot, ex_equipment_id, star, serial_id) in slot_strategy[unit_id]:
                name = db.get_ex_equip_name(ex_equipment_id)
                if serial_id is not None:
                    sub_str = db.get_ex_equip_sub_status_str(ex_equipment_id, client.data.ex_equips[serial_id].sub_status or [])
                    msg.append(f"{name}★{star}({sub_str})")
                else:
                    msg.append(f"{name}★{star}")
            msg = ','.join(msg)
            self._log(f"{db.get_unit_name(unit_id)} 装备 {msg}")
           
# ---- 通用穿EX装备辅助函数 ----  
async def _equip_ex_by_serial(module: Module, client: pcrclient,   
                               config_unit_key: str, config_serial_key: str,  
                               target_rarity: int, rarity_name: str):  
    """通用穿EX装备逻辑，供彩/粉/金装共用"""  
    unit_id = int(module.get_config(config_unit_key))  
    serial_id_str = module.get_config(config_serial_key)  
  
    if not serial_id_str or not str(serial_id_str).strip().isdigit():  
        raise AbortError(f"请输入有效的{rarity_name}装ID（数字）")  
    serial_id = int(serial_id_str)  
  
    if unit_id not in client.data.unit:  
        raise AbortError(f"未拥有角色{db.get_unit_name(unit_id)}")  
  
    if serial_id not in client.data.ex_equips:  
        raise AbortError(f"{rarity_name}装ID {serial_id} 不存在")  
  
    ex_equip = client.data.ex_equips[serial_id]  
    actual_rarity = db.get_ex_equip_rarity(ex_equip.ex_equipment_id)  
    if actual_rarity != target_rarity:  
        raise AbortError(f"ID {serial_id} 不是{rarity_name}装（实际稀有度: {db.ex_rarity_name.get(actual_rarity, actual_rarity)}）")  
  
    equip_category = db.ex_equipment_data[ex_equip.ex_equipment_id].category  
    equip_name = db.get_ex_equip_name(ex_equip.ex_equipment_id)  
    unit_name = db.get_unit_name(unit_id)  
  
    # 检查装备是否已被其他角色装备，先撤下  
    for uid, u in client.data.unit.items():  
        for slot_idx, ex_slot in enumerate(u.ex_equip_slot):  
            if ex_slot.serial_id == serial_id and uid != unit_id:  
                module._log(f"{equip_name}当前装备在{db.get_unit_name(uid)}的槽{slot_idx + 1}上，将先撤下")  
                await client.unit_equip_ex([ExtraEquipChangeUnit(  
                    unit_id=uid,  
                    ex_equip_slot=[ExtraEquipChangeSlot(slot=slot_idx + 1, serial_id=0)],  
                    cb_ex_equip_slot=None  
                )])  
                break  
  
    # 根据装备类别找到角色匹配的槽位  
    slot_data = db.unit_ex_equipment_slot[unit_id]  
    target_slot = None  
    for slot_id, cat in enumerate(  
        [slot_data.slot_category_1, slot_data.slot_category_2, slot_data.slot_category_3], start=1  
    ):  
        if cat == equip_category:  
            target_slot = slot_id  
            break  
  
    if target_slot is None:  
        raise AbortError(f"{unit_name}没有匹配{equip_name}类别的EX装备槽")  
  
    # 检查是否已装备  
    unit = client.data.unit[unit_id]  
    current_slot = unit.ex_equip_slot[target_slot - 1]  
    if current_slot.serial_id == serial_id:  
        raise SkipError(f"{unit_name}的槽{target_slot}已装备该{rarity_name}装")  
  
    # 装备  
    exchange_list = [ExtraEquipChangeSlot(slot=target_slot, serial_id=serial_id)]  
    await client.unit_equip_ex([ExtraEquipChangeUnit(  
        unit_id=unit_id,  
        ex_equip_slot=exchange_list,  
        cb_ex_equip_slot=None  
    )])  
  
    module._log(f"已为{unit_name}装备{equip_name}（槽{target_slot}）")  
  
@name('穿ex彩装')  
@default(True)  
@texttype('equip_rainbow_serial_id', '彩装ID', '')  
@unitchoice('equip_rainbow_unit_id', '角色')  
@description('将指定彩装(serial_id)穿到指定角色的普通EX装备栏')  
class equip_rainbow_ex(Module):  
    async def do_task(self, client: pcrclient):  
        await _equip_ex_by_serial(self, client, 'equip_rainbow_unit_id', 'equip_rainbow_serial_id', 5, '彩')
        
@name('穿ex粉装')  
@default(True)  
@texttype('equip_pink_serial_id', '粉装ID', '')  
@unitchoice('equip_pink_unit_id', '角色')  
@description('将指定粉装(serial_id)穿到指定角色的普通EX装备栏')  
class equip_pink_ex(Module):  
    async def do_task(self, client: pcrclient):  
        await _equip_ex_by_serial(self, client, 'equip_pink_unit_id', 'equip_pink_serial_id', 4, '粉')  
  
  
@name('穿ex金装')  
@default(True)  
@texttype('equip_gold_serial_id', '金装ID', '')  
@unitchoice('equip_gold_unit_id', '角色')  
@description('将指定金装(serial_id)穿到指定角色的普通EX装备栏')  
class equip_gold_ex(Module):  
    async def do_task(self, client: pcrclient):  
        await _equip_ex_by_serial(self, client, 'equip_gold_unit_id', 'equip_gold_serial_id', 3, '金')   
        
# ---- 保存/恢复EX装备状态 ----  
  
@name('保存ex状态')  
@default(True)  
@description('保存所有角色当前穿戴的普通EX装备状态，供恢复ex状态使用。数据保存在cache/modules/目录下，不影响账号配置。')  
class save_ex_state(Module):  
    async def do_task(self, client: pcrclient):  
        state = {}  
        total_ex = 0  
        for unit_id in client.data.unit:  
            unit = client.data.unit[unit_id]  
            slots = []  
            for ex_slot in unit.ex_equip_slot:  
                slots.append(ex_slot.serial_id)  
            if any(s != 0 for s in slots):  
                state[str(unit_id)] = slots  
                # 记录日志  
                unit_name = db.get_unit_name(unit_id)  
                slot_info = []  
                for i, sid in enumerate(slots):  
                    if sid != 0:  
                        total_ex += 1  
                        if sid in client.data.ex_equips:  
                            ex = client.data.ex_equips[sid]  
                            slot_info.append(f"槽{i+1}: {db.get_ex_equip_name(ex.ex_equipment_id)}(id:{sid})")  
                        else:  
                            slot_info.append(f"槽{i+1}: 未知装备(id:{sid})")  
                self._log(f"{unit_name}: {', '.join(slot_info)}")  
  
        if not state:  
            raise SkipError("没有角色穿戴普通EX装备，无需保存")  
  
        self.save_cache("ex_state", state)  
        self._log(f"共保存了{len(state)}个角色的{total_ex}件普通EX装备状态")  
  
  
@name('恢复ex状态')  
@default(True)  
@description('恢复之前保存的普通EX装备穿戴状态，需先执行保存ex状态。只处理有差异的部分，不会全部卸载。')  
class restore_ex_state(Module):  
    async def do_task(self, client: pcrclient):  
        from os.path import join, exists  
        import json  
        save_cache_path = join(CACHE_DIR, "modules", "save_ex_state", self._parent.id + ".json")  
        if not exists(save_cache_path):  
            raise AbortError("未找到保存的EX状态，请先执行「#保存ex状态」")  
        with open(save_cache_path, "r") as f:  
            cache = json.load(f)  
        state = cache.get("ex_state", None)  
        if not state:  
            raise AbortError("保存的EX状态数据为空，请重新执行「#保存ex状态」")  
  
        # 1. 构建当前 serial_id -> (unit_id, slot) 映射  
        current_owner = {}  
        for unit_id in client.data.unit:  
            unit = client.data.unit[unit_id]  
            for ex_slot in unit.ex_equip_slot:  
                if ex_slot.serial_id != 0:  
                    current_owner[ex_slot.serial_id] = (unit_id, ex_slot.slot)  
  
        # 2. 找出所有需要变更的 (unit_id, slot_num, target_serial_id)  
        changes = []  
        skip_cnt = 0  
        for unit_id_str, slots in state.items():  
            unit_id = int(unit_id_str)  
            if unit_id not in client.data.unit:  
                self._warn(f"角色{unit_id}已不存在，跳过")  
                skip_cnt += 1  
                continue  
            unit = client.data.unit[unit_id]  
            for i, saved_serial_id in enumerate(slots):  
                if i >= len(unit.ex_equip_slot):  
                    continue  
                current_serial = unit.ex_equip_slot[i].serial_id  
                if current_serial == saved_serial_id:  
                    continue  # 已经一致，跳过  
                # 检查目标装备是否还存在  
                if saved_serial_id != 0 and saved_serial_id not in client.data.ex_equips:  
                    unit_name = db.get_unit_name(unit_id)  
                    self._warn(f"{unit_name} 槽{i+1}: 装备(id:{saved_serial_id})已不存在，跳过")  
                    skip_cnt += 1  
                    continue  
                slot_num = unit.ex_equip_slot[i].slot  
                changes.append((unit_id, slot_num, saved_serial_id))  
  
        if not changes:  
            if skip_cnt:  
                self._warn(f"所有保存的装备均无法恢复（{skip_cnt}项跳过）")  
                return  
            raise SkipError("当前EX装备状态与保存的一致，无需恢复")  
  
        # 3. 找出需要先释放的 serial_id（目标装备当前在别的角色身上）  
        need_free = {}  # serial_id -> (owner_uid, owner_slot)  
        for (unit_id, slot_num, target_serial) in changes:  
            if target_serial != 0 and target_serial in current_owner:  
                owner_uid, owner_slot = current_owner[target_serial]  
                if owner_uid != unit_id or owner_slot != slot_num:  
                    need_free[target_serial] = (owner_uid, owner_slot)  
  
        # 4. 按角色分组，卸载需要释放的槽位（合并同角色多槽位到一次请求）  
        unequip_by_unit = {}  
        for serial_id, (owner_uid, owner_slot) in need_free.items():  
            unequip_by_unit.setdefault(owner_uid, []).append(  
                ExtraEquipChangeSlot(slot=owner_slot, serial_id=0))  
          
        unequip_cnt = 0  
        for uid, exchange_list in unequip_by_unit.items():  
            await client.unit_equip_ex([ExtraEquipChangeUnit(  
                unit_id=uid, ex_equip_slot=exchange_list, cb_ex_equip_slot=None)])  
            unequip_cnt += len(exchange_list)  
        if unequip_cnt:  
            self._log(f"释放了{len(unequip_by_unit)}个角色的{unequip_cnt}件装备")  
  
        # 5. 按角色分组，穿戴有差异的槽位（合并同角色多槽位到一次请求）  
        equip_by_unit = {}  
        for (unit_id, slot_num, target_serial) in changes:  
            equip_by_unit.setdefault(unit_id, []).append(  
                ExtraEquipChangeSlot(slot=slot_num, serial_id=target_serial))  
  
        equip_unit_cnt = 0  
        equip_ex_cnt = 0  
        for uid, exchange_list in equip_by_unit.items():  
            await client.unit_equip_ex([ExtraEquipChangeUnit(  
                unit_id=uid, ex_equip_slot=exchange_list, cb_ex_equip_slot=None)])  
            unit_name = db.get_unit_name(uid)  
            slot_info = []  
            for slot_change in exchange_list:  
                if slot_change.serial_id != 0:  
                    ex = client.data.ex_equips[slot_change.serial_id]  
                    slot_info.append(f"槽{slot_change.slot}: {db.get_ex_equip_name(ex.ex_equipment_id)}")  
                    equip_ex_cnt += 1  
                else:  
                    slot_info.append(f"槽{slot_change.slot}: 卸下")  
            equip_unit_cnt += 1  
            self._log(f"{unit_name}: {', '.join(slot_info)}")  
  
        msg = f"共变更了{equip_unit_cnt}个角色的装备"  
        if skip_cnt:  
            msg += f"（{skip_cnt}项因角色或装备不存在而跳过）"  
        self._log(msg)       
       