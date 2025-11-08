from typing import Set
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *
from datetime import datetime

@description('刷新角色练度')
@name("刷新box")
@default(True)
class refresh_box(Module):
    async def do_task(self, client: pcrclient):
        self._log("刷新成功，当前box时间：" + db.format_time(datetime.fromtimestamp(client.data.data_time)))

@description('从缓存中查询角色练度，不会登录！任意登录或者刷新box可以更新缓存')
@name("查角色")
@default(True)
@notlogin(check_data=True)
@unitchoice("search_unit_id", "角色")
class search_unit(Module):
    async def do_task(self, client: pcrclient):
        unit_id = self.get_config('search_unit_id')
        unit = int(unit_id)
        unit_name = db.get_unit_name(unit)

        read_story = set(client.data.read_story_ids)
        info = [unit_id, unit_name]
        if unit not in client.data.unit:
            info += ['无'] * 7
        else:
            unitinfo = client.data.unit[unit]
            info.append(unitinfo.unit_rarity)
            info.append(unitinfo.unit_level)
            rank = f"r{unitinfo.promotion_level}"
            equip = ""
            for solt in unitinfo.equip_slot:
                equip += "-" if not solt.is_slot else str(solt.enhancement_level)
            info.append(f"{rank}({equip})")

            level = []
            level.append(unitinfo.union_burst[0].skill_level if unitinfo.union_burst else 0)
            level.append(unitinfo.main_skill[0].skill_level if unitinfo.main_skill else 0)
            level.append(unitinfo.main_skill[1].skill_level if len(unitinfo.main_skill) > 1 else 0)
            level.append(unitinfo.ex_skill[0].skill_level if unitinfo.ex_skill else 0)
            level = [str(i) for i in level]
            info.append('/'.join(level))

            read_storys = len([str(story.story_id) for story in db.unit_story if story.story_group_id == unit // 100 and story.story_id in read_story])
            not_read_storys = len([str(story.story_id) for story in db.unit_story if story.story_group_id == unit // 100 and story.story_id not in read_story])
            info.append("未实装" if not unitinfo.unique_equip_slot else "无" if not unitinfo.unique_equip_slot[0].is_slot else unitinfo.unique_equip_slot[0].enhancement_level)
            if len(unitinfo.unique_equip_slot) > 1:
                info.append("无" if not unitinfo.unique_equip_slot[1].is_slot else f"{unitinfo.unique_equip_slot[1].enhancement_level}星") 

            ex_equip = []
            for cb_ex in unitinfo.cb_ex_equip_slot:
                if not cb_ex.serial_id:
                    ex_equip.append("-")
                else:
                    ex = client.data.ex_equips[cb_ex.serial_id]
                    rarity = db.get_ex_equip_rarity_name(ex.ex_equipment_id)
                    star = db.get_ex_equip_star_from_pt(ex.ex_equipment_id, ex.enhancement_pt)
                    ex_equip.append(f"{rarity}{star}")
            info.append("/".join(i for i in ex_equip))

            kizuna_unit = set()
            for story in db.chara2story[unit]:
                if story.story_id in db.story_detail:
                    kizuna_unit.add(db.story_detail[story.story_id].requirement_id)

            love = []
            for other in kizuna_unit:
                if other not in db.unlock_unit_condition: continue
                kizuna_name = db.get_unit_name(other)
                unit_id = other // 100
                love_level = client.data.unit_love_data[unit_id].love_level if unit_id in client.data.unit_love_data else 0
                unit_story = [story.story_id for story in db.unit_story if story.story_group_id == unit_id]
                total_storys = len(unit_story)
                read_storys = len([story for story in unit_story if story in read_story])
                love.append(f"{kizuna_name}好感{love_level}({read_storys}/{total_storys})")
            info.append("\n" + ";".join(i for i in love))

        self._log(" ".join(str(i) for i in info))

        data = client.unit_info_to_dict(unit)
        header = ['姓名'] + list(data.keys())
        data.update({"姓名": unit_name})
        self._table_header(header)
        self._table(data)

@description('从缓存中查询角色练度，不会登录！任意登录或者刷新box可以更新缓存')
@name('查box')
@notlogin(check_data=True)
@default(True)
@unitlist("box_unit", "查询角色")
@booltype("box_all_unit", "附加所有角色", False)
@multichoice("box_unit_info", "角色信息", ['星级', '等级', '品级', '装备', 'UB', 'S1', 'S2', 'EX', '剧情', '专武1', '专武2', '普碎数', '金碎数'], ['星级', '等级', '品级', '装备', 'UB', 'S1', 'S2', 'EX', '剧情', '专武1', '专武2', '普碎数', '金碎数'])
@multichoice("box_user_info", "用户信息", ['名字', '钻石', '母猪石', '星球杯', '心碎', 'mana'], ['名字', '钻石', '母猪石', '星球杯', '心碎', 'mana'])
@multichoice("box_talent_info", "属性信息", ['火深域', '水深域', '风深域', '光深域', '暗深域', '火属性', '水属性', '风属性', '光属性', '暗属性', '属性技能', '大师技能'], ['火深域', '水深域', '风深域', '光深域', '暗深域', '火属性', '水属性', '风属性', '光属性', '暗属性', '属性技能', '大师技能'])
class get_box_table(Module):
    async def _prepare_user_data(self, client: pcrclient, user_info: Set[str]) -> Dict:
        """准备用户基本信息"""
        ret = {
            "名字": client.data.user_name,
            "钻石": client.data.jewel.free_jewel,
            "母猪石": client.data.get_inventory((eInventoryType.Item, 90005)),
            "星球杯": client.data.get_inventory(db.xingqiubei),
            "心碎": client.data.get_inventory(db.xinsui),
            "mana": client.data.gold.gold_id_pay + client.data.gold.gold_id_free + client.data.user_gold_bank_info.bank_gold if client.data.user_gold_bank_info else 0,
        }
        ret.update({
            f"{db.talents[talent_id].talent_name}深域": client.data.get_talent_quest_single(talent_id) for talent_id in sorted([area.talent_id for area in db.talent_quest_area_data.values()])
        })
        ret.update({
            f"{db.talents[talent_info.talent_id].talent_name}属性": client.data.get_talent_level_single(talent_info) for talent_info in client.data.princess_knight_info.talent_level_info_list
        })
        ret.update({
            "属性技能": client.data.get_talent_skill_info(),
            "大师技能": client.data.get_master_skill_info(),
        })
        ret = {key : ret[key] for key in ret if key in user_info}
        return ret
    
    def _get_filtered_units(self, client: pcrclient, unit_list):
        """获取过滤后的角色列表"""
        filtered_units = []
        if unit_list:
            filtered_units = unit_list.copy()
        if self.get_config('box_all_unit') or not filtered_units:
            filtered_units.extend(db.unlock_unit_condition_candidate())
        return filtered_units
    
    def _get_unit_data(self, client: pcrclient, unit_id: int, box_unit_info: Set[str]) -> Dict:
        unit_data = client.unit_info_to_dict(unit_id)
        unit_data = {key: unit_data[key] for key in unit_data if key in box_unit_info}
        return unit_data

    async def do_task(self, client: pcrclient):
        box_unit = self.get_config('box_unit')
        
        filtered_units = self._get_filtered_units(client, box_unit)
        
        if not filtered_units:
            raise AbortError("没有找到符合条件的角色")

        user_info = set(self.get_config('box_user_info')) | set(self.get_config('box_talent_info'))
        box_unit_info = set(self.get_config('box_unit_info'))
        
        header = []
        data = {}

        user_data = await self._prepare_user_data(client, user_info)
        data.update(user_data)
        header.extend(list(user_data.keys()))

        for unit_id in filtered_units:
            unit_data = self._get_unit_data(client, unit_id, box_unit_info)
            unit_name = db.get_unit_name(unit_id)
            header.append({unit_name: list(unit_data.keys())})
            data[unit_name] = unit_data

        self._table_header(header)
        self._table(data)
