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
        self._log(f"深域通关: {client.data.get_talent_quest_info()}")
        princess_knight_info = client.data.princess_knight_info
        if princess_knight_info:
            self._log(f"属性等级: {client.data.get_talent_level_info()}")
            self._log(f"属性技能: {client.data.get_talent_skill_info()}")
            self._log(f"大师技能: {client.data.get_master_skill_info()}")

        data = {}
        data.update({
            f"{db.talents[talent_id].talent_name}深域": client.data.get_talent_quest_single(talent_id) for talent_id in sorted([area.talent_id for area in db.talent_quest_area_data.values()])
        })
        data.update({
            f"{db.talents[talent_info.talent_id].talent_name}属性": client.data.get_talent_level_single(talent_info) for talent_info in client.data.princess_knight_info.talent_level_info_list
        })
        data.update({
            "属性技能": client.data.get_talent_skill_info(),
            "大师技能": client.data.get_master_skill_info(),
        })
        header = list(data.keys())
        self._table_header(header)
        self._table(data)

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
        header = ['uid', '名字', 'Rank等级', '火深域', '水深域', '风深域', '光深域', '暗深域', '顶关未通']
        self._table_header(header)
        for member in clan_info.clan.members:
            profile = await client.get_profile(member.viewer_id)
            rank_exp = profile.user_info.princess_knight_rank_total_exp
            kight_rank=db.query_knight_exp_rank(rank_exp)
            msg = []
            flag = False
            max_stage = 0
            data = {
                'uid': member.viewer_id,
                '名字': member.name,
                'Rank等级': kight_rank
            }
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
                data[f'{talent_name}深域'] = quest
            max_stage = self._format_quest_stage(max_stage)
            warn = f"(未通关最高关卡：{max_stage}！！！)" if flag else "" 
            member_progress = f"({member.viewer_id}){member.name}: " + "/".join(msg) + f" rank等级:{kight_rank}{warn}"

            data['顶关未通'] = "√" if flag else ""
            self._log(member_progress)
            self._table(data)
