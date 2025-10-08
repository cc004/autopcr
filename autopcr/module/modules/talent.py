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
            quest = "未通关" if quest_id == 0 else f"{db.quest_name[quest_id][4:]}"
            msg.append(f"{talent_name}{quest}")
        self._log("/".join(msg))

@description('看看公会深域的通关情况，会登录！')
@name('查公会深域')
class find_clan_talent_quest(Module):
    async def do_task(self, client: pcrclient):
        clan_info = await client.get_clan_info()
        clan_name = clan_info.clan.detail.clan_name
        self._log(f"公会: {clan_name}({len(clan_info.clan.members)}人)")
        for member in clan_info.clan.members:
            profile = await client.get_profile(member.viewer_id)
            msg = []
            for talent_info in profile.quest_info.talent_quest:
                talent_id = talent_info.talent_id
                clear_count = talent_info.clear_count
                quest = f"{(clear_count + 9) // 10}-{(clear_count - 1) % 10 + 1}" if clear_count > 0 else "0-0"
                msg.append(f"{db.talents[talent_id].talent_name}{quest}")
            member_progress = f"({member.viewer_id}){member.name}: " + "/".join(msg)
            self._log(member_progress)
