from collections import Counter

from ...model.custom import ItemType
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...db.models import GrowthParameter
from ...model.enums import *
from ...model.common import SkillLevelInfo, SkillLevelUpDetail, UnitData

class UnitController(Module):

    unit_id: int
    client: pcrclient
    auto_level_up : bool = True

    skill_name = {
        eSkillLocationCategory.UNION_BURST_SKILL: "UB",
        eSkillLocationCategory.MAIN_SKILL_1: "S1",
        eSkillLocationCategory.MAIN_SKILL_2: "S2",
        eSkillLocationCategory.EX_SKILL_1: "EX",
    }

    @property
    def unit(self) -> UnitData:
        return self.client.data.unit[self.unit_id]

    async def is_growth_unit(self) -> Union[GrowthParameter, None]:
        unit_name = db.get_unit_name(self.unit_id)
        if self.unit_id not in self.client.data.unit:
            raise AbortError(f"未解锁角色{unit_name}")
        if self.unit_id not in self.client.data.growth_unit:
            return None
        growth_id = list(set(self.client.data.growth_unit[self.unit_id].growth_parameter_list.growth_id_list) & set(db.growth_parameter.keys())) # 专武球后应该需要修改
        if len(growth_id) != 1:
            raise ValueError("未知的光辉球类型" + ','.join(map(str, growth_id)))
        growth_limit = db.growth_parameter[growth_id[0]]
        return growth_limit

    async def unit_skill_up(self, location: eSkillLocationCategory, target_level: int, current_level: int, free: bool):
        step = target_level - current_level
        if free:
            self._log(f"{db.get_unit_name(self.unit.id)}技能{self.skill_name[location]}升至{current_level + step}级")
            skill_level_up_detail = SkillLevelUpDetail()
            skill_level_up_detail.location = location
            skill_level_up_detail.step = step
            skill_level_up_detail.current_level = current_level
            await self.client.skill_level_up(self.unit.id, [skill_level_up_detail])
        else:
            mana = db.get_skill_up_cost(current_level, target_level)
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{db.get_unit_name(self.unit.id)}技能{self.skill_name[location]}升至{target_level}级需要{mana}玛娜，当前玛娜不足")

            skill_levelup_list = [SkillLevelUpDetail(location=location, step=target_level-current_level, current_level=current_level)]
            self._log(f"{db.get_unit_name(self.unit.id)}技能{self.skill_name[location]}升至{current_level + step}级")
            await self.client.skill_level_up(self.unit.id,  skill_levelup_list)

    # md python 没有引用
    async def unit_skill_up_aware(self, location: eSkillLocationCategory, skill: Callable[[], SkillLevelInfo], target_skill_level: int, limit: Union[None, GrowthParameter] = None):
        if limit and limit.skill_level < target_skill_level:
            raise AbortError(f"{db.get_unit_name(self.unit.id)}技能{self.skill_name[location]}超过了免费可提升等级{limit.skill_level}，请自行完成免费可提升的所有内容")
            self._log(f"{db.get_unit_name(self.unit.id)}技能{self.skill_name[location]}超过了免费可提升等级{limit.skill_level},先提升至等级{limit.skill_level}")
            await self.unit_skill_up_aware(location, skill, limit.skill_level, limit)

        if target_skill_level > self.unit.unit_level:
            self._log(f"{db.get_unit_name(self.unit.id)}技能{self.skill_name[location]}升至{target_skill_level}级需要角色等级升至{target_skill_level}级")
            if not self.auto_level_up:
                raise AbortError(f"当前设置不自动拉角色等级，无法升级")
            await self.unit_level_up_aware(target_skill_level, limit)

        await self.unit_skill_up(location, target_skill_level, skill().skill_level, limit is not None and target_skill_level <= limit.skill_level)

    async def unit_promotion_up(self, target_promotion_level: int, free: bool):
        if free:
            self._log(f"{db.get_unit_name(self.unit.id)}升至品级{target_promotion_level}")
            await self.client.unit_free_promotion(self.unit.id, target_promotion_level)
        else:
            now_equip_slot = [equip.is_slot for equip in self.unit.equip_slot]
            equips = db.get_rank_promote_equip_demand(self.unit.id, self.unit.promotion_level, now_equip_slot, target_promotion_level, [False] * 6)
            cost_equip, mana = db.craft_equip(equips)
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{db.get_unit_name(self.unit.id)}升至品级{target_promotion_level}需要{mana}玛娜，当前玛娜不足")

            bad = [(item, cnt - self.client.data.get_inventory(item)) for item, cnt in cost_equip.items() if cnt > self.client.data.get_inventory(item)]
            if bad:
                bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad])
                raise AbortError(f"{db.get_unit_name(self.unit.id)}升至品级{target_promotion_level}所需材料不足:\n{bad_list}")

            equip_recipe_list = [db.craft_equip(
                    db.unit_promotion_equip_count[self.unit.id][self.unit.promotion_level] - 
                    Counter((eInventoryType(eInventoryType.Equip), equip.id) for equip in self.unit.equip_slot if equip.is_slot)
                    )[0]
                    ] + [db.craft_equip(
                        db.unit_promotion_equip_count[self.unit.id][rank]
                        )[0] for rank in range(self.unit.promotion_level + 1, target_promotion_level)]
            self._log(f"{db.get_unit_name(self.unit.id)}升至品级{target_promotion_level}")
            await self.client.multi_promotion(self.unit.id, target_promotion_level, equip_recipe_list)

    async def unit_promotion_up_aware(self, target_promotion_level: int, limit: Union[None, GrowthParameter]):
        if limit and target_promotion_level > limit.promotion_level:
            raise AbortError(f"目标品级{target_promotion_level}超过了免费可提升品级{limit.promotion_level}，请自行完成免费可提升的所有内容")
            self._log(f"目标品级{target_promotion_level}超过了免费可提升品级{limit.promotion_level},先提升至品级{limit.promotion_level}")
            await self.unit_promotion_up_aware(limit.promotion_level, limit)

        demand_level = db.get_promotion_demand_level(self.unit.id, target_promotion_level)
        if self.unit.unit_level < demand_level:
            self._log(f"{db.get_unit_name(self.unit.id)}升至品级{target_promotion_level}需要升至{demand_level}级")
            await self.unit_level_up_aware(demand_level, limit)

        await self.unit_promotion_up(target_promotion_level, 
                                     limit is not None and target_promotion_level <= limit.promotion_level, 
                                     )

    async def unit_level_up(self, target_level: int, free: bool):
        if free:
            self._log(f"{db.get_unit_name(self.unit.id)}升至{target_level}级")
            await self.client.unit_free_level_up(self.unit.id, target_level)
        else:
            exp_demand = db.get_level_up_total_exp(target_level) - self.unit.unit_exp
            exp_demand_limit = db.get_level_up_total_exp(target_level + 1) - self.unit.unit_exp
            cost_potion = self.client.data.get_level_up_exp_potion_demand(exp_demand, exp_demand_limit)
            if not cost_potion:
                raise AbortError(f"{db.get_unit_name(self.unit.id)}升至{target_level}级所需经验药水不足，或无法达到其要求")

            self._log(f"{db.get_unit_name(self.unit.id)}升至{target_level}级")
            await self.client.unit_level_up(self.unit.id, cost_potion)

    async def unit_level_up_aware(self, target_level: int, limit: Union[GrowthParameter, None] = None):
        if limit and target_level > limit.unit_level:
                raise AbortError(f"目标等级{target_level}超过了免费可提升等级{limit.unit_level}，请自行完成免费可提升的所有内容")
                self._log(f"目标等级{target_level}超过了免费可提升等级{limit.unit_level},先提升至等级{limit.unit_level}")
                await self.unit_level_up_aware(limit.unit_level, limit)

        level_limit = self.client.data.team_level + (10 if self.unit.exceed_stage else 0)
        if target_level > level_limit:
            raise AbortError(f"{db.get_unit_name(self.unit.id)}的目标等级{target_level}超过了可提升的最高等级{level_limit}，无法升级")

        await self.unit_level_up(target_level, limit is not None and target_level <= limit.unit_level)

    async def unit_equip_slot(self, equip_id: int, slot_num: int, free: bool):
        if free:
            self._log(f"{db.get_unit_name(self.unit.id)}装备{db.get_equip_name(equip_id)}")
            await self.client.unit_free_equip(self.unit_id, [slot_num])
        else:
            item: ItemType = (eInventoryType.Equip, equip_id)
            cost_equip, mana = db.craft_equip(Counter({item: 1}))
            if (not await self.client.prepare_mana(mana)):
                raise AbortError(f"{db.get_unit_name(self.unit_id)}装备{db.get_equip_name(equip_id)}需要{mana}玛娜，当前玛娜不足")

            bad = [(item, cnt - self.client.data.get_inventory(item)) for item, cnt in cost_equip.items() if cnt > self.client.data.get_inventory(item)]
            if bad:
                bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad])
                raise AbortError(f"{db.get_unit_name(self.unit.id)}装备{db.get_equip_name(equip_id)}所需材料不足:\n{bad_list}")

            self._log(f"{db.get_unit_name(self.unit.id)}装备{db.get_equip_name(equip_id)}")
            await self.client.unit_craft_equip(self.unit.id, slot_num, cost_equip)

    async def unit_equip_slot_aware(self, equip_id: int, slot_num: int, limit: Union[None, GrowthParameter] = None):
        if db.equip_data[equip_id].require_level > self.unit.unit_level:
            self._log(f"{db.get_unit_name(self.unit.id)}装备{db.get_equip_name(equip_id)}需要角色升至{db.equip_data[equip_id].require_level}级")
            if not self.auto_level_up:
                raise AbortError(f"当前设置不自动拉角色等级，无法装备")
            await self.unit_level_up_aware(db.equip_data[equip_id].require_level, limit)

        if limit and limit.promotion_level <= self.unit.promotion_level and getattr(limit, f"equipment_{slot_num}") == -1: # 不知何用
                raise AbortError(f"{db.get_unit_name(self.unit.id)}品级{self.unit.promotion_level}的{slot_num}位装备{db.get_equip_name(equip_id)}不支持免费装备")

        await self.unit_equip_slot(equip_id, slot_num, limit is not None)

    async def unit_equip_enhance(self, equip_id: int, slot_num: int, enhancement_level: int, free: bool):

        if free:
            self._log(f"{db.get_unit_name(self.unit.id)}{slot_num}位装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级")
            await self.client.equipment_free_enhance(self.unit.id, slot_num, enhancement_level)
        else:
            current_enhancement_pt = self.unit.equip_slot[slot_num - 1].enhancement_pt
            pt = db.get_equip_star_pt(equip_id, enhancement_level) - current_enhancement_pt
            pt_limit = -1 if enhancement_level == 5 else db.get_equip_star_pt(equip_id, enhancement_level + 1) - current_enhancement_pt
            cost_stone = self.client.data.get_equip_enhance_stone_demand(pt, pt_limit)
            if not cost_stone:
                raise AbortError(f"{db.get_unit_name(self.unit.id)}{slot_num}位上装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级所需强化石不足，或无法达到其要求")

            mana = pt * 200 # guess
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{db.get_unit_name(self.unit.id)}{slot_num}位上装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级需要{mana}玛娜，当前玛娜不足")

            self._log(f"{db.get_unit_name(self.unit.id)}{slot_num}位上装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级")
            await self.client.equipment_enhance(self.unit.id, slot_num, current_enhancement_pt, cost_stone)

@description('支持全部角色')
@name('完成装备强化任务')
@singlechoice("equip_enhance_up_unit", "强化角色", "100101:日和莉", [f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unlock_unit_condition])
@default(False)
class unit_equip_enhance_up(UnitController):
    async def do_task(self, client: pcrclient):
        if client.data.is_mission_finished(eSystemId.UNIT_EQUIP_ENHANCE):
            raise SkipError("今日已完成装备强化任务")

        self.client = client
        unit_id, unit_name = self.get_config('equip_enhance_up_unit').split(':')
        self.unit_id = int(unit_id)

        growth_limit = await self.is_growth_unit()

        equip_slot_list = [1, 3, 5, 4, 2, 0]

        stop = False
        while not stop:
            for id in equip_slot_list: 
                equip = self.unit.equip_slot[id]
                
                if equip.id == 999999: # 未实装
                    continue

                slot_num = id + 1
                if not equip.is_slot:
                    await self.unit_equip_slot_aware(equip.id, slot_num, growth_limit)

                if equip.enhancement_level < db.get_equip_max_star(equip.id):
                    await self.unit_equip_enhance(equip.id, slot_num, equip.enhancement_level + 1, growth_limit is not None)
                    stop = True
                    break
            else:
                self._log(f"所有装备均已满强化，需提升角色品级")
                await self.unit_promotion_up_aware(self.unit.promotion_level + 1, growth_limit)

@description('支持全部角色')
@name('完成技能升级任务')
@singlechoice("level_up_unit", "强化角色", "100101:日和莉", [f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unlock_unit_condition])
@default(False)
class unit_skill_level_up(UnitController):
    async def do_task(self, client: pcrclient):
        if client.data.is_mission_finished(eSystemId.UNIT_SKILL_LVUP):
            raise SkipError("今日已完成技能升级任务")

        self.client = client
        unit_id, unit_name = self.get_config('level_up_unit').split(':')
        self.unit_id = int(unit_id)

        growth_limit = await self.is_growth_unit()

        stop = False

        while not stop:
            skills = [(eSkillLocationCategory(eSkillLocationCategory.UNION_BURST_SKILL + id), lambda id=id: self.unit.union_burst[id]) for id, skill in enumerate(self.unit.union_burst)] +  \
                    [(eSkillLocationCategory(eSkillLocationCategory.MAIN_SKILL_1 + id), lambda id=id: self.unit.main_skill[id]) for id, skill in enumerate(self.unit.main_skill)] +  \
                    [(eSkillLocationCategory(eSkillLocationCategory.EX_SKILL_1 + id), lambda id=id: self.unit.ex_skill[id]) for id, skill in enumerate(self.unit.ex_skill)]

            for pos, skill in skills:
                try:
                    if skill().skill_level < self.unit.unit_level:
                        await self.unit_skill_up_aware(pos, skill, skill().skill_level + 1, growth_limit)
                        stop = True
                        break
                except AbortError as e:
                    print(e)
                    continue
            else:
                self._log(f"所有技能均等于角色等级{self.unit.unit_level}级，需提升角色等级")
                await self.unit_level_up_aware(self.unit.unit_level + 1, growth_limit)


@description('支持全部角色，装备星级-1表示不穿装备，自动拉等级指当前等级不足以穿装备或提升技能等级，将会提升角色等级')
@name('拉角色练度')
@booltype("unit_promote_level_when_fail_to_equip_or_skill", "自动拉等级", False)
@singlechoice("unit_promote_equip_5", "右下装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_4", "左下装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_3", "右中装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_2", "左中装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_1", "右上装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_0", "左上装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_skill_ex", "ex等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_skill_s2", "s2等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_skill_s1", "s1等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_skill_ub", "ub等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_rank", "品级", 1, db.unit_rank_candidate)
@singlechoice("unit_promote_level", "等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_unit", "拉取角色", "100101:日和莉", [f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unlock_unit_condition])
@default(False)
class unit_promote(UnitController):

    async def do_task(self, client: pcrclient):

        self.client = client
        unit_id, unit_name = self.get_config('unit_promote_unit').split(':')
        self.unit_id = int(unit_id)

        growth_limit = await self.is_growth_unit()
        self.auto_level_up = bool(self.get_config('unit_promote_level_when_fail_to_equip_or_skill'))

        # 拉等级
        target_level = int(self.get_config('unit_promote_level'))
        if self.unit.unit_level < target_level:
            await self.unit_level_up_aware(target_level, growth_limit)

        # 拉品级
        target_promotion_rank = int(self.get_config('unit_promote_rank'))
        if self.unit.promotion_level < target_promotion_rank:
            await self.unit_promotion_up_aware(target_promotion_rank, growth_limit)

        # 拉装备
        for i in range(6):
            equip = self.unit.equip_slot[i]
            if equip.id == 999999:
                continue

            star = int(self.get_config(f'unit_promote_equip_{i}'))
            if star != -1:
                if not equip.is_slot:
                    await self.unit_equip_slot_aware(equip.id, i + 1, growth_limit)
                
                promotion_limit = db.get_equip_max_star(equip.id)
                if star > promotion_limit:
                    self._log(f"{i+1}号位装备预设{star}星级超过了最大星级{promotion_limit}，提升至最大星级{promotion_limit}")
                    star = promotion_limit

                if equip.enhancement_level < star:
                    await self.unit_equip_enhance(equip.id, i + 1, star, growth_limit is not None)
        
        # 拉技能
        target_skill_ub_level = int(self.get_config('unit_promote_skill_ub'))
        if self.unit.union_burst and self.unit.union_burst[0].skill_level < target_skill_ub_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.UNION_BURST_SKILL, lambda: self.unit.union_burst[0], target_skill_ub_level, growth_limit)

        target_skill_s1_level = int(self.get_config('unit_promote_skill_s1'))
        if self.unit.main_skill and self.unit.main_skill[0].skill_level < target_skill_s1_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.MAIN_SKILL_1, lambda: self.unit.main_skill[0], target_skill_s1_level, growth_limit)

        target_skill_s2_level = int(self.get_config('unit_promote_skill_s2'))
        if len(self.unit.main_skill) > 1 and self.unit.main_skill[1].skill_level < target_skill_s2_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.MAIN_SKILL_2, lambda: self.unit.main_skill[1], target_skill_s2_level, growth_limit)

        target_skill_ex_level = int(self.get_config('unit_promote_skill_ex'))
        if self.unit.ex_skill and self.unit.ex_skill[0].skill_level < target_skill_ex_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.EX_SKILL_1, lambda: self.unit.ex_skill[0], target_skill_ex_level, growth_limit)
