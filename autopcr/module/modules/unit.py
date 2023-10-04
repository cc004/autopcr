from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...db.models import GrowthParameter
from ...model.enums import *
from ...model.common import SkillLevelInfo, SkillLevelUpDetail, UnitData

class unit_controller(Module):

    async def is_growth_unit(self, unit_id: int, client: pcrclient) -> Union[GrowthParameter, None]:
        unit_name = db.get_unit_name(unit_id)
        if unit_id not in client.data.unit:
            raise AbortError(f"未解锁角色{unit_name}")
        if unit_id not in client.data.growth_unit:
            return None
        growth_id = list(set(client.data.growth_unit[unit_id].growth_parameter_list.growth_id_list) & set(db.growth_parameter.keys())) # len should 1
        if len(growth_id) != 1:
            raise ValueError("未知的光辉球类型" + ','.join(map(str, growth_id)))
        growth_limit = db.growth_parameter[growth_id[0]]
        return growth_limit

    async def unit_skill_up(self, unit_id: int, location: int, step: int, current_level: int, free: bool, client: pcrclient):
        if free:
            self._log(f"角色【{db.get_unit_name(unit_id)}】技能{location}升至{current_level + step}级")
            skill_level_up_detail = SkillLevelUpDetail()
            skill_level_up_detail.location = location
            skill_level_up_detail.step = step
            skill_level_up_detail.current_level = current_level
            await client.skill_level_up(unit_id, [skill_level_up_detail])
        else:
            raise ValueError("暂不支持非免费品级提升")

    async def unit_skill_up_aware(self, unit: UnitData, location: int, skill: SkillLevelInfo, target_skill_level: int, client: pcrclient, limit: GrowthParameter = None):
        if limit:
            if limit.skill_level < target_skill_level:
                raise AbortError(f"{db.get_unit_name(unit.id)}技能{location}不支持免费强化至{target_skill_level}级(至多{limit.skill_level})")

        if target_skill_level > unit.unit_level:
            await self.unit_level_up_aware(unit, target_skill_level, client, limit)

        await self.unit_skill_up(unit.id, location, target_skill_level - skill.skill_level, skill.skill_level, limit is not None, client)

    async def unit_promotion_up(self, unit_id: int, target_promotion_level: int, free: bool, client: pcrclient):
        if free:
            self._log(f"角色【{db.get_unit_name(unit_id)}】升至品级{target_promotion_level}")
            await client.unit_free_promotion(unit_id, target_promotion_level)
        else:
            raise ValueError("暂不支持非免费品级提升")

    async def unit_promotion_up_aware(self, unit: UnitData, target_promotion_level: int, client: pcrclient, limit: GrowthParameter):
        if limit:
            if target_promotion_level > limit.promotion_level:
                raise AbortError(f"目标品级{target_promotion_level}超过了免费可提升品级{limit.promotion_level}")
        await self.unit_promotion_up(unit.id, target_promotion_level, limit is not None, client)

    async def unit_level_up(self, unit_id: int, target_level: int, free: bool, client: pcrclient):
        if free:
            self._log(f"角色【{db.get_unit_name(unit_id)}】升至{target_level}级")
            await client.unit_free_level_up(unit_id, target_level)
        else:
            raise ValueError("暂不支持非免费等级提升")

    async def unit_level_up_aware(self, unit: UnitData, target_level: int, client: pcrclient, limit: GrowthParameter = None):
        if limit:
            if target_level > limit.unit_level:
                raise AbortError(f"角色{db.get_unit_name(unit.id)}的目标等级{target_level}超过了免费可提升等级{limit.unit_level}")
        await self.unit_level_up(unit.id, target_level, limit is not None, client)

    async def unit_equip_slot(self, unit_id: int, equip_id: int, slot_num: int, free: bool, client: pcrclient):
        if free:
            self._log(f"为角色【{db.get_unit_name(unit_id)}】装备{db.get_equip_name(equip_id)}")
            await client.unit_free_equip(unit_id, [slot_num])
        else:
            raise ValueError("暂不支持非免费装备装备")

    async def unit_equip_slot_aware(self, unit: UnitData, equip_id: int, slot_num: int, client: pcrclient, limit: GrowthParameter = None):
        if limit:
            if limit.promotion_level <= unit.promotion_level and getattr(limit, f"equipment_{slot_num}") == -1:
                raise AbortError(f"{db.get_unit_name(unit.id)}品级{unit.promotion_level}的{slot_num}位装备{db.get_equip_name(equip_id)}不支持免费装备")

        if db.equip_data[equip_id].require_level > unit.unit_level:
            self._log(f"为角色{db.get_unit_name(unit.id)}装备{db.get_equip_name(equip_id)}需要升至{db.equip_data[equip_id].require_level}级")
            await self.unit_level_up_aware(unit, db.equip_data[equip_id].require_level, client, limit)

        await self.unit_equip_slot(unit.id, equip_id, slot_num, limit is not None, client)

    async def unit_equip_enhance(self, unit: UnitData, equip_id: int, slot_num: int, enhancement_level: int, free: bool, client: pcrclient):
        if free:
            self._log(f"角色【{db.get_unit_name(unit.id)}】{slot_num}位上装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级")
            await client.equipment_free_enhance(unit.id, slot_num, enhancement_level)
        else:
            raise ValueError("暂不支持非免费装备强化")

@description('仅支持光辉球角色')
@name('完成装备强化任务')
@singlechoice("equip_enhance_up_unit", "强化角色", "100101:日和莉", [f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unit_data])
@default(False)
class unit_equip_enhance_up(unit_controller):
    async def do_task(self, client: pcrclient):
        if client.data.is_mission_finished(eSystemId.UNIT_EQUIP_ENHANCE):
            raise SkipError("今日已完成装备强化任务")

        unit_id, unit_name = self.get_config('equip_enhance_up_unit').split(':')
        unit_id = int(unit_id)
        growth_limit = await self.is_growth_unit(unit_id, client)
        if not growth_limit:
            raise AbortError(f"非光辉球使用角色【{unit_name}】")

        stop = False
        while not stop:
            for id, equip in enumerate(client.data.unit[unit_id].equip_slot):
                slot_num = id + 1
                if not equip.is_slot:
                    await self.unit_equip_slot_aware(client.data.unit[unit_id], equip.id, slot_num, client, growth_limit)

                equip_promotion_level = db.equip_data[equip.id].promotion_level
                if equip_promotion_level in db.equipment_enhance_data and equip.enhancement_level < max(db.equipment_enhance_data[equip_promotion_level].keys()):
                    await self.unit_equip_enhance(client.data.unit[unit_id], equip.id, slot_num, equip.enhancement_level + 1, growth_limit is not None, client)
                    stop = True
                    break
            else:
                self._log(f"所有装备均已满强化，需提升角色品级")
                await self.unit_promotion_up_aware(client.data.unit[unit_id], client.data.unit[unit_id].promotion_level + 1, client, growth_limit)

@description('仅支持光辉球角色')
@name('完成技能升级任务')
@singlechoice("level_up_unit", "强化角色", "100101:日和莉", [f"{unit}:{db.unit_data[unit].unit_name}" for unit in db.unit_data])
@default(False)
class unit_skill_level_up(unit_controller):
    async def do_task(self, client: pcrclient):
        if client.data.is_mission_finished(eSystemId.UNIT_SKILL_LVUP):
            raise SkipError("今日已完成技能升级任务")

        unit_id, unit_name = self.get_config('level_up_unit').split(':')
        unit_id = int(unit_id)
        growth_limit = await self.is_growth_unit(unit_id, client)
        if not growth_limit:
            raise AbortError(f"非光辉球使用角色【{unit_name}】")

        stop = False

        while not stop:
            skills = [(eSkillLocationCategory.UNION_BURST_SKILL + id, skill) for id, skill in enumerate(client.data.unit[unit_id].union_burst)] +  \
                    [(eSkillLocationCategory.MAIN_SKILL_1 + id, skill) for id, skill in enumerate(client.data.unit[unit_id].main_skill)] +  \
                    [(eSkillLocationCategory.EX_SKILL_1 + id, skill) for id, skill in enumerate(client.data.unit[unit_id].ex_skill)]

            for pos, skill in skills:
                if skill.skill_level < client.data.unit[unit_id].unit_level and skill.skill_level < growth_limit.skill_level:
                    await self.unit_skill_up_aware(client.data.unit[unit_id], pos, skill, skill.skill_level + 1, client, growth_limit)
                    stop = True
                    break
            else:
                self._log(f"所有技能均等于角色等级{client.data.unit[unit_id].unit_level}级，需提升角色等级")
                await self.unit_level_up_aware(client.data.unit[unit_id], client.data.unit[unit_id].unit_level + 1, client, growth_limit)
