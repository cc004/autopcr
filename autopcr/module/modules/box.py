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
                kizuna_unit |= set(story.get_effect_unit_ids())

            love = []
            for other in kizuna_unit:
                if other not in db.unlock_unit_condition: continue
                unit_name = db.get_unit_name(other)
                unit_id = other // 100
                love_level = client.data.unit_love_data[unit_id].love_level if unit_id in client.data.unit_love_data else 0
                unit_story = [story.story_id for story in db.unit_story if story.story_group_id == unit_id]
                total_storys = len(unit_story)
                read_storys = len([story for story in unit_story if story in read_story])
                love.append(f"{unit_name}好感{love_level}({read_storys}/{total_storys})")
            info.append("\n" + ";".join(i for i in love))

        self._log(" ".join(str(i) for i in info))

@description('从缓存中查询角色练度，不会登录！任意登录或者刷新box可以更新缓存')
@name('查box')
@notlogin(check_data=True)
@default(True)
@unitlist("box_unit", "查询角色")
@multichoice("box_unit_info", "角色信息", ['星级', '等级', '品级', '装备', 'UB', 'S1', 'S2', 'EX', '剧情', '专武1', '专武2', '普碎数', '金碎数'], ['星级', '等级', '品级', '装备', 'UB', 'S1', 'S2', 'EX', '剧情', '专武1', '专武2', '普碎数', '金碎数'])
@multichoice("box_user_info", "用户信息", ['名字', '数据时间', '钻石', '母猪石', '星球杯', '心碎', 'mana'], ['名字', '数据时间', '钻石', '母猪石', '星球杯', '心碎', 'mana'])
class get_box_table(Module):
    async def _prepare_user_data(self, client: pcrclient, box_user_info: Set[str]) -> Dict:
        """准备用户基本信息"""
        ret = {
            "名字": client.data.user_name,
            "数据时间": db.format_time(db.parse_time(client.data.data_time)),
            "钻石": client.data.jewel.free_jewel,
            "母猪石": client.data.get_inventory((eInventoryType.Item, 90005)),
            "星球杯": client.data.get_inventory(db.xingqiubei),
            "心碎": client.data.get_inventory(db.xinsui),
            "mana": client.data.gold.gold_id_pay + client.data.gold.gold_id_free + client.data.user_gold_bank_info.bank_gold if client.data.user_gold_bank_info else 0
        }
        ret = {key : ret[key] for key in ret if key in box_user_info}
        return ret
    
    def _get_filtered_units(self, client: pcrclient, unit_list):
        """获取过滤后的角色列表"""
        if unit_list:
            filtered_units = unit_list.copy()
        else:
            filtered_units = list(client.data.unit.keys())
        return filtered_units
    
    def _get_unit_data(self, client: pcrclient, unit_id: int, box_unit_info: Set[str]) -> Dict:
        """获取单个角色的详细数据"""
        unit_data = {
            "星级": "无",
            "等级": "无",
            "品级": "无",
            "装备": "无",
            "UB": 0,
            "S1": 0,
            "S2": 0,
            "EX": 0,
            "剧情": "无",
            "专武1": "无",
            "专武2": "无",
            "普碎数": "无",
            "金碎数": "无",
        }
        
        read_story = set(client.data.read_story_ids)
        if unit_id in client.data.unit:
            unitinfo = client.data.unit[unit_id]
            rank = f"R{unitinfo.promotion_level}"
            equip = ''.join('-' if not solt.is_slot else str(solt.enhancement_level) for solt in unitinfo.equip_slot)
            total_storys = [story.story_id for story in db.unit_story if story.story_group_id == unit_id // 100]
            read_storys_num = len([id for id in total_storys if id in read_story])
            total_storys_num = len(total_storys)

            unit_data.update({
                "星级": f"{unitinfo.unit_rarity}★",
                "等级": unitinfo.unit_level,
                "品级": rank,
                "装备": equip,
                "UB": unitinfo.union_burst[0].skill_level if unitinfo.union_burst else "无",
                "S1": unitinfo.main_skill[0].skill_level if unitinfo.main_skill else "无",
                "S2": unitinfo.main_skill[1].skill_level if len(unitinfo.main_skill) > 1 else "无",
                "EX": unitinfo.ex_skill[0].skill_level if unitinfo.ex_skill else "无",
                "剧情": f"{read_storys_num}/{total_storys_num}",
                "专武1": "未实装" if not unitinfo.unique_equip_slot else "无" if not unitinfo.unique_equip_slot[0].is_slot else unitinfo.unique_equip_slot[0].enhancement_level,
                "专武2": "未实装" if len(unitinfo.unique_equip_slot) < 2 else "无" if not unitinfo.unique_equip_slot[1].is_slot else unitinfo.unique_equip_slot[1].enhancement_level,
                "普碎数": client.data.get_inventory((eInventoryType.Item, db.unit_to_memory[unit_id])) if unit_id in db.unit_to_memory else "无",
                "金碎数": client.data.get_inventory((eInventoryType.Item, db.unit_to_pure_memory[unit_id])) if unit_id in db.unit_to_pure_memory else "无",
            })
        
        unit_data = {key: unit_data[key] for key in unit_data if key in box_unit_info}
        return unit_data

    async def do_task(self, client: pcrclient):
        box_unit = self.get_config('box_unit')
        
        filtered_units = self._get_filtered_units(client, box_unit)
        
        if not filtered_units:
            raise AbortError("没有找到符合条件的角色")

        box_user_info = set(self.get_config('box_user_info'))
        box_unit_info = set(self.get_config('box_unit_info'))
        
        header = []
        data = {}

        user_data = await self._prepare_user_data(client, box_user_info)
        data.update(user_data)
        header.extend(list(user_data.keys()))

        for unit_id in filtered_units:
            unit_data = self._get_unit_data(client, unit_id, box_unit_info)
            unit_name = db.get_unit_name(unit_id)
            header.append({unit_name: list(unit_data.keys())})
            data[unit_name] = unit_data
        
        self._table_header(header)
        self._table(data)

'''@description('从缓存中查询属性练度，不会登录！任意登录或者刷新box可以更新缓存')
@name('查属性练度')
@notlogin(check_data=True)
@default(True)
class get_talent_info(Module):
    async def do_task(self, client: pcrclient):
        princess_knight_info = client.data.princess_knight_info
        
        if not princess_knight_info:
            self._log("未找到公主骑士信息")
            return
            
        # 属性映射
        talent_names = {
            1: "火属性",
            2: "水属性", 
            3: "风属性",
            4: "光属性",
            5: "暗属性"
        }

        # 显示属性等级信息
        talent_levels = {}
        for talent_info in princess_knight_info.talent_level_info_list:
            # talent_name = talent_names.get(talent_info.talent_id, f"属性{talent_info.talent_id}")
            talent_levels[talent_info.talent_id] = db.get_talent_level(talent_info.total_point)


        # 显示属性技能节点信息
        if princess_knight_info.talent_skill_last_enhanced_page_node_list:
            talent_skill_list = [
                {"node_id": node_info.node_id, "enhance_level": node_info.enhance_level} 
                for node_info in princess_knight_info.talent_skill_last_enhanced_page_node_list
            ]
            
            if talent_skill_list:
                # 按node_id排序
                talent_skill_list.sort(key=lambda x: x["node_id"])
                
                # 定义交点和页面边界
                INTERSECTIONS = [1,26,54,82,110,138,166,194,222,235,248,261,274,287,300,313,326,
                                339,352,365,378,391,404,417,430,443,456,469,482,495,508,521,534,
                                547,560,573,586,599,612,625,638]
                PAGE_BOUNDARIES = [4, 8, 16, 24, 32, 40]
                
                import bisect
                import json
                
                max_node_id = talent_skill_list[-1]["node_id"] if talent_skill_list else 0

                current_index = bisect.bisect_right(INTERSECTIONS, max_node_id) - 1
                if current_index < 0:
                    current_index = 0
                
                current_level_value = INTERSECTIONS[current_index] if current_index < len(INTERSECTIONS) else 1
                current_level_enhance = 0
                if current_index < len(talent_skill_list) and current_level_value <= len(talent_skill_list):
                    current_level_enhance = talent_skill_list[current_level_value-1]["enhance_level"] if current_level_value-1 < len(talent_skill_list) else 0
                current_page = bisect.bisect_left(PAGE_BOUNDARIES, current_index) + 1

                node_ids = [n['node_id'] for n in talent_skill_list]
                start_idx = bisect.bisect_right(node_ids, current_level_value) if node_ids else 0

                columns = {
                    "left": {"count": 0, "last_level": 0},
                    "middle": {"count": 0, "last_level": 0},
                    "right": {"count": 0, "last_level": 0}
                }

                for node in talent_skill_list[start_idx:]:
                    offset = (node["node_id"] - current_level_value) % 3
                    if offset == 1:
                        columns["left"]["count"] += 1
                        columns["left"]["last_level"] = node["enhance_level"]
                    elif offset == 2:
                        columns["middle"]["count"] += 1
                        columns["middle"]["last_level"] = node["enhance_level"]
                    else:
                        columns["right"]["count"] += 1
                        columns["right"]["last_level"] = node["enhance_level"]

                skill_tree_text = (
                    f"第{current_page}页 "
                    f"合{current_index}[{current_level_enhance}] "
                    f"左{columns['left']['count']}[{columns['left']['last_level']}] "
                    f"中{columns['middle']['count']}[{columns['middle']['last_level']}] "
                    f"右{columns['right']['count']}[{columns['right']['last_level']}] "
                )

        # 显示大师技能节点信息
        if princess_knight_info.team_skill_latest_node:
            team_node = princess_knight_info.team_skill_latest_node

        # 构造JSON格式的数据
        talent_enhance_info = {
            "talent_levels": talent_levels,
            "skill_tree": skill_tree_text,
            "team_skill":team_node.node_id,
        }
        self._log(json.dumps(talent_enhance_info, ensure_ascii=False))'''
        
@description('从缓存中查询属性练度，不会登录！任意登录或者刷新box可以更新缓存')
@name('查属性练度')
@notlogin(check_data=True)
@default(True)
class get_talent_info(Module):
    async def do_task(self, client: pcrclient):
        princess_knight_info = client.data.princess_knight_info
        
        if not princess_knight_info:
            self._log("未找到公主骑士信息")
            return
            
        # 属性映射
        talent_names = {
            1: "火属性",
            2: "水属性", 
            3: "风属性",
            4: "光属性",
            5: "暗属性"
        }

        # 准备用户信息
        user_info = {
            "名字": client.data.user_name,
            "数据时间": db.format_time(db.parse_time(client.data.data_time))
        }

        # 构建header和data结构
        header = []
        data = {}
        
        # 添加用户信息
        header.extend(list(user_info.keys()))
        data.update(user_info)

        # 属性等级信息
        talent_levels = {}
        for talent_info in princess_knight_info.talent_level_info_list:
            talent_levels[talent_info.talent_id] = db.get_talent_level(talent_info.total_point)
        
        # 转换属性名称并添加到表格
        attr_headers = []
        for tid, name in talent_names.items():
            attr_headers.append(f"{name}等级")
            data[f"{name}等级"] = talent_levels.get(tid, 0)
        header.extend(attr_headers)

        # 属性技能信息
        skill_tree_text = "无"
        if princess_knight_info.talent_skill_last_enhanced_page_node_list:
            talent_skill_list = [
                {"node_id": node_info.node_id, "enhance_level": node_info.enhance_level} 
                for node_info in princess_knight_info.talent_skill_last_enhanced_page_node_list
            ]
            
            if talent_skill_list:
                # 按node_id排序
                talent_skill_list.sort(key=lambda x: x["node_id"])
                
                # 定义交点和页面边界
                INTERSECTIONS = [1,26,54,82,110,138,166,194,222,235,248,261,274,287,300,313,326,
                                339,352,365,378,391,404,417,430,443,456,469,482,495,508,521,534,
                                547,560,573,586,599,612,625,638]
                PAGE_BOUNDARIES = [4, 8, 16, 24, 32, 40]
                
                import bisect
                
                max_node_id = talent_skill_list[-1]["node_id"] if talent_skill_list else 0
                current_index = bisect.bisect_right(INTERSECTIONS, max_node_id) - 1
                current_index = max(current_index, 0)
                
                current_level_value = INTERSECTIONS[current_index] if current_index < len(INTERSECTIONS) else 1
                current_level_enhance = 0
                if current_index < len(talent_skill_list) and current_level_value <= len(talent_skill_list):
                    current_level_enhance = talent_skill_list[current_level_value-1]["enhance_level"] if current_level_value-1 < len(talent_skill_list) else 0
                current_page = bisect.bisect_left(PAGE_BOUNDARIES, current_index) + 1

                node_ids = [n['node_id'] for n in talent_skill_list]
                start_idx = bisect.bisect_right(node_ids, current_level_value) if node_ids else 0

                columns = {
                    "left": {"count": 0, "last_level": 0},
                    "middle": {"count": 0, "last_level": 0},
                    "right": {"count": 0, "last_level": 0}
                }

                for node in talent_skill_list[start_idx:]:
                    offset = (node["node_id"] - current_level_value) % 3
                    if offset == 1:
                        columns["left"]["count"] += 1
                        columns["left"]["last_level"] = node["enhance_level"]
                    elif offset == 2:
                        columns["middle"]["count"] += 1
                        columns["middle"]["last_level"] = node["enhance_level"]
                    else:
                        columns["right"]["count"] += 1
                        columns["right"]["last_level"] = node["enhance_level"]

                skill_tree_text = (
                    f"第{current_page}页 "
                    f"合{current_index}[{current_level_enhance}] "
                    f"左{columns['left']['count']}[{columns['left']['last_level']}] "
                    f"中{columns['middle']['count']}[{columns['middle']['last_level']}] "
                    f"右{columns['right']['count']}[{columns['right']['last_level']}] "
                )
            
            header.append("属性技能")
            data["属性技能"] = skill_tree_text

        #星幽碎片
        xinyou_count = client.data.get_inventory(db.xinyou)
        header.append("星幽碎片")
        data["星幽碎片"] = xinyou_count
        
        # 大师技能信息
        team_skill_id = 0
        if princess_knight_info.team_skill_latest_node:
            team_skill_id = princess_knight_info.team_skill_latest_node.node_id
        header.append("大师技能")
        data["大师技能"] = team_skill_id

       #大师碎片
        master_fragment_count = client.data.get_inventory(db.master_fragment)
        header.append("大师碎片")
        data["大师碎片"] = master_fragment_count
        
        self._table_header(header)
        self._table(data)