from ...model.common import TalentSkillNodeInfo
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
from ...util.linq import flow

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
        for talent_id, quest_id in result:
            talent_name = db.talents[talent_id].talent_name 
            quest = "0-0" if quest_id == 0 else f"{db.quest_name[quest_id][4:]}"
            msg.append(f"{talent_name}{quest}")
        self._log("深域通关:" + "/".join(msg))

        princess_knight_info = client.data.princess_knight_info
        if princess_knight_info:
            msg = []
            for talent_info in princess_knight_info.talent_level_info_list:
                msg.append(f"{db.talents[talent_info.talent_id].talent_name}{db.get_talent_level(talent_info.total_point)}")
            self._log("属性等级:" + "/".join(msg))

            page = 0 if not princess_knight_info.talent_skill_last_enhanced_page_node_list else db.talent_skill_node[princess_knight_info.talent_skill_last_enhanced_page_node_list[0].node_id].page_num
            joined_nodes = flow(princess_knight_info.talent_skill_last_enhanced_page_node_list) \
                            .where(lambda x: db.talent_skill_node[x.node_id].is_joined_node()) \
                            .to_list()
            max_joined_node = max(joined_nodes, key=lambda x: x.node_id, default=TalentSkillNodeInfo(node_id=1))
            joined_node_after = flow(princess_knight_info.talent_skill_last_enhanced_page_node_list) \
                                .where(lambda x: x.node_id > max_joined_node.node_id) \
                                .group_by(lambda x: db.talent_skill_node[x.node_id].pos_x) \
                                .to_dict(lambda g: g.key, lambda g: g.to_list())
            joined_node_after_max = {pos: max(nodes, key=lambda x: x.node_id) for pos, nodes in joined_node_after.items()}

            prefix = f"第{page}页 第{len(joined_nodes)}合流"
            msg = []
            if not joined_node_after and joined_nodes:
                prefix += f"[{max_joined_node.enhance_level}级]"
            elif joined_node_after:
                for pos, nodes in joined_node_after.items():
                    msg.append(f"{db.talent_skill_node[nodes[0].node_id].pos()}{len(nodes)}[{joined_node_after_max[pos].enhance_level}级]")
            self._log("属性技能:" + prefix + " " + "/".join(msg))

            self._log(f"大师技能: MP{princess_knight_info.team_skill_latest_node.node_id}")

            for item in [db.fire_ball, db.water_ball, db.wind_ball, db.sun_ball, db.dark_ball, db.xinyou, db.master_fragment, db.master_ffragment]: # temp display, future replace with effect
                self._log(f"{db.get_inventory_name_san(item)}: {client.data.get_inventory(item)}")

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
