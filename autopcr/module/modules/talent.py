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
        if client.data.princess_knight_info:
            self._log(f"属性等级: {client.data.get_talent_level_info()}")
            self._log(f"属性技能: {client.data.get_talent_skill_info()}")
            self._log(f"大师技能: {client.data.get_master_skill_info()}")
        roles = client.data.unit_role_list
        role_ticket_num = client.data.unit_role_gacha_exec_count + client.data.get_inventory(db.unit_role_gach_ticket)
        role_logs = [f"职能练度({role_ticket_num}):", client.data.get_role_level_info()]
        self._log("\n".join(role_logs))
        self._log(f"黎明界票: {client.data.get_inventory(db.labyrinth_ticket)}")
        data = {}
        data.update({
            f"{db.talents[talent_id].talent_name}深域": client.data.get_talent_quest_single(talent_id)
            for talent_id in sorted([area.talent_id for area in db.talent_quest_area_data.values()])
        })
        if client.data.princess_knight_info:
            data.update({
                f"{db.talents[talent_info.talent_id].talent_name}属性": client.data.get_talent_level_single(talent_info)
                for talent_info in client.data.princess_knight_info.talent_level_info_list
            })
            data.update({
                "属性技能": client.data.get_talent_skill_info(),
                "大师技能": client.data.get_master_skill_info(),
            }) 
        if roles:
            data["职能券"] = f"{role_ticket_num}"
            data.update({
                    f"{db.unit_role_type[role.unit_role_id].unit_role_name}": client.data.get_role_level_single(role)
                    for role in roles
                })
        data['黎明界票'] = client.data.get_inventory(db.labyrinth_ticket)

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

@description('查看并导出各职能精通槽位的完整库存数据和最高可达等级，不会进行强化')
@notlogin(check_data=True)
@name('查职能精通')
class find_unit_role_mastery(Module):
    EXPORT_SCHEMA_VERSION = 1
    HEADERS = [
        '格式版本',
        '玩家ID',
        '玩家名',
        '公会ID',
        '主数据库版本',
        '数据完整',
        '职能ID',
        '职能名称',
        '槽位ID',
        '精通ID',
        '精通名称',
        '是否解锁',
        '状态',
        '当前阶段',
        '当前强化等级',
        '当前等级',
        '普通T1',
        '普通T2',
        '普通T3',
        '普通T4',
        '普通T5',
        '万能T1',
        '万能T2',
        '万能T3',
        '万能T4',
        '万能T5',
        '仅普通可达',
        '含万能单项可达',
    ]

    def _build_row(
        self,
        client: pcrclient,
        detail: Dict,
        universal_stocks: Dict[int, int],
        complete: bool,
    ) -> Dict:
        unlocked = (
            detail['current_enhance_level'] is not None
            and detail['current_enhance_level'] >= 0
        )
        return {
            '格式版本': self.EXPORT_SCHEMA_VERSION,
            '玩家ID': str(client.data.uid),
            '玩家名': client.data.user_name or '',
            '公会ID': str(client.data.clan) if client.data.clan else '',
            '主数据库版本': getattr(getattr(db, 'dbmgr', None), 'ver', '') or '',
            '数据完整': '是' if complete else '否',
            '职能ID': detail['unit_role_id'],
            '职能名称': detail['role_name'],
            '槽位ID': detail['slot_id'],
            '精通ID': detail['mastery_id'],
            '精通名称': detail['name'],
            '是否解锁': '是' if unlocked else '否',
            '状态': detail['status'],
            '当前阶段': detail['current_slot_level'] if unlocked else None,
            '当前强化等级': detail['current_enhance_level'] if unlocked else None,
            '当前等级': detail['current_level'],
            **{
                f'普通T{level}': detail['ordinary_stocks'][level]
                for level in range(1, 6)
            },
            **{
                f'万能T{level}': universal_stocks[level]
                for level in range(1, 6)
            },
            '仅普通可达': detail['reachable_without_universal'],
            '含万能单项可达': detail['reachable_with_universal'],
        }

    async def do_task(self, client: pcrclient):
        details = client.data.get_unit_role_mastery_details()
        self._table_header(self.HEADERS.copy())

        if not details:
            self._warn('未找到职能精通数据，请登录刷新缓存或更新主数据库')
            return

        if not (getattr(client.data, 'unit_role_list', None) or []):
            self._log('缓存中暂无已解锁职能；以下槽位按未解锁展示')
        complete = not any(
            detail['status'] in ('数据不可用', '数据缺失')
            for detail in details
        )
        if not complete:
            self._warn('部分职能精通主数据不可用，请更新主数据库后重试')
        self._log('普通与万能碎片按 T1-T5 分列；含万能可达为各槽位独立投入的单项上限')

        universal_stocks = client.data.get_unit_role_mastery_universal_stocks()
        for detail in details:
            self._table(self._build_row(
                client,
                detail,
                universal_stocks,
                complete,
            ))
