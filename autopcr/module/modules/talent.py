from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.custom import ItemType
from ...db.models import QuestDatum, ShioriQuest
from typing import List, Dict, Tuple
import typing
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from collections import Counter
from ...core.apiclient import apiclient
'''@description('看看你的通关情况')
@notlogin(check_data=True)
@name('查深域')
class find_talent_quest(Module):
    async def do_task(self, client: pcrclient):
        result = []
        for area in db.talent_quest_area_data.values():
            talent_id = area.talent_id
            max_quest_id = client.data.cleared_talent_quest_ids.get(talent_id, 0)
            result.append((area.talent_id, max_quest_id))
        result.sort(key = lambda x: x[0])

        msg = []
        for talent_id, quest_id in result:
            talent_name = db.talents[talent_id].talent_name 
            quest = "未通关" if quest_id == 0 else f"{db.quest_name[quest_id][4:]}"
            msg.append(f"{talent_name}{quest}")
        self._log("/".join(msg))'''

@description('看看你的通关情况')
@notlogin(check_data=True)
@name('查深域')
class find_talent_quest(Module):
    async def do_task(self, client: pcrclient):
        result = []
        for area in db.talent_quest_area_data.values():
            talent_id = area.talent_id
            max_quest_id = client.data.cleared_talent_quest_ids.get(talent_id, 0)
            result.append((area.talent_id, max_quest_id))
        result.sort(key = lambda x: x[0])

        msg = []
        clear_info = []
        for talent_id, quest_id in result:
            talent_name = db.talents[talent_id].talent_name 
            quest = "未通关" if quest_id == 0 else f"{db.quest_name[quest_id][4:]}"
            clear_info.append(f"{talent_name}{quest}")
        msg.append("通关情况：\n" + "/".join(clear_info)) 

        # 添加属性等级和技能信息
        princess_knight_info = client.data.princess_knight_info
        if princess_knight_info:
            # 属性等级信息
            talent_names = {1:"火",2:"水",3:"风",4:"光",5:"暗"}
            talent_levels = {}
            level_info = []
            for talent_info in princess_knight_info.talent_level_info_list:
                talent_levels[talent_info.talent_id] = db.get_talent_level(talent_info.total_point)
            
            for tid, name in talent_names.items():
                level_info.append(f"{name}{talent_levels.get(tid, 0)}")
            msg.append("属性等级：\n" + "/".join(level_info))

            # 属性技能信息
            skill_tree_text = "无"
            if princess_knight_info.talent_skill_last_enhanced_page_node_list:
                talent_skill_list = [
                    {"node_id": node.node_id, "enhance_level": node.enhance_level} 
                    for node in princess_knight_info.talent_skill_last_enhanced_page_node_list
                ]
                
                if talent_skill_list:
                    import bisect
                    talent_skill_list.sort(key=lambda x: x["node_id"])
                    
                    INTERSECTIONS = [1,26,54,82,110,138,166,194,222,235,248,261,274,287,300,313,326,
                                    339,352,365,378,391,404,417,430,443,456,469,482,495,508,521,534,
                                    547,560,573,586,599,612,625,638]
                    PAGE_BOUNDARIES = [4, 8, 16, 24, 32, 40]
                    
                    max_node_id = talent_skill_list[-1]["node_id"]
                    current_index = bisect.bisect_right(INTERSECTIONS, max_node_id) - 1
                    current_index = max(current_index, 0)
                    
                    current_level_value = INTERSECTIONS[current_index]
                    current_level_enhance = talent_skill_list[current_level_value-1]["enhance_level"] if current_level_value-1 < len(talent_skill_list) else 0
                    current_page = bisect.bisect_left(PAGE_BOUNDARIES, current_index) + 1

                    node_ids = [n['node_id'] for n in talent_skill_list]
                    start_idx = bisect.bisect_right(node_ids, current_level_value)

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
                        f"第{current_page}页 合{current_index}[{current_level_enhance}] "
                        f"左{columns['left']['count']}[{columns['left']['last_level']}] "
                        f"中{columns['middle']['count']}[{columns['middle']['last_level']}] "
                        f"右{columns['right']['count']}[{columns['right']['last_level']}]"
                    )
            msg.append("属性技能：\n" + skill_tree_text + f"\n星幽碎片：{client.data.get_inventory(db.xinyou)}")

            # 添加大师技能和碎片信息
            team_skill_id = princess_knight_info.team_skill_latest_node.node_id if princess_knight_info.team_skill_latest_node else 0
            master_info = [
                f"大师技能{team_skill_id}",
                f"大师碎片{client.data.get_inventory(db.master_fragment)}"
            ]
            msg.append("/".join(master_info))

        self._log("\n".join(msg))



@description('看看公会深域的通关情况，会登录！')
@name('查公会深域')
class find_clan_talent_quest(Module):
    def _format_quest_stage(self, count: int) -> str:
        if count <= 0:
            return "0-0"
        return f"{(count + 9) // 10}-{(count - 1) % 10 + 1}"

    async def do_task(self, client: pcrclient):
        clan_info = await client.get_clan_info()
        clan_name = clan_info.clan.detail.clan_name
        self._log(f"公会: {clan_name}({len(clan_info.clan.members)}人)")
        for member in clan_info.clan.members:
            profile = await client.get_profile(member.viewer_id)
            rank_exp = profile.user_info.princess_knight_rank_total_exp
            kight_rank=db.query_knight_exp_rank(rank_exp)
            msg = []
            flag = False
            max_stage = 0
            for talent_info in profile.quest_info.talent_quest:
                talent_id = talent_info.talent_id
                clear_count = talent_info.clear_count
                talent_name = db.talents[talent_id].talent_name

                #获取对应area_id
                area_id = next((a_id for a_id in db.talent_quest_area_data 
                              if db.talent_quest_area_data[a_id].talent_id == talent_id), None)
                if not area_id:
                    continue

                # 获取该区域最高关卡ID
                quest_ids = db.talent_quests_data.get(area_id, [])
                if not quest_ids:
                    continue
                max_count = len(quest_ids)
                if clear_count < max_count:
                    flag = True
                    max_stage = max(max_stage, max_count)
                quest = self._format_quest_stage(clear_count) 
                msg.append(f"{talent_name}{quest}")
            max_stage = self._format_quest_stage(max_stage)
            warn = f"(未通关最高关卡：{max_stage}！！！)" if flag else "" 
            member_progress = f"({member.viewer_id}){member.name}: " + "/".join(msg) + f" rank等级:{kight_rank}{warn}"
            self._log(member_progress)
