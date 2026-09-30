from ..modulebase import *
from ..config import ConditionalExecutionWrapper, ConditionalNotExecutionClient
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import eMissionStatusType
from .hatsune import hatsune_h_sweep, all_in_hatsune
from .autosweep import (
    lazy_normal_sweep, smart_hard_sweep, smart_shiori_sweep,
    mirai_very_hard_sweep, mirai_sp1_h_sweep, mirai_sp1_shiori_sweep,
    smart_very_hard_sweep, smart_sweep, last_normal_quest_sweep, oldest_normal_quest_sweep,
)


@description('先按既有配置执行扫荡，次数不足时再强制启用任务并忽略执行时间条件，仍完不成则刷1-1。执行期间忽略禅模式，补足职能券任务次数后停止。')
@name('完成职能券任务')
@default(True)
@tag_stamina_consume(do_check=False)
class role_mission_get(Module):

    first_order = [
        smart_very_hard_sweep,
        hatsune_h_sweep,
        smart_sweep,
        mirai_very_hard_sweep,
        smart_hard_sweep,
        smart_shiori_sweep,
        mirai_sp1_h_sweep,
        mirai_sp1_shiori_sweep,
        last_normal_quest_sweep,
        lazy_normal_sweep,
        all_in_hatsune,
    ]

    second_order = [
        smart_very_hard_sweep,
        hatsune_h_sweep,
        smart_sweep,
        mirai_very_hard_sweep,
        smart_hard_sweep,
        smart_shiori_sweep,
        mirai_sp1_h_sweep,
        mirai_sp1_shiori_sweep,
        all_in_hatsune,
        oldest_normal_quest_sweep,
    ]

    async def do_task(self, client: pcrclient):
        mission_data = db.VIP_mission
        if mission_data is None:
            raise ValueError("未找到职能券任务！")
        top = await client.mission_index()
        missions = [m for m in top.missions if m.mission_id == mission_data.daily_mission_id]
        if len(missions) == 0:
            mission = None
        elif len(missions) > 1:
            raise ValueError("职能券任务不唯一！")
        else:
            mission = missions[0]
        remain = (mission_data.condition_num - mission.clear_num) if mission else mission_data.condition_num
        if mission and (mission.mission_status != eMissionStatusType.NoClear or remain <= 0):
            raise SkipError("职能券任务已完成")

        with client.override_config({
            'stamina_consume_not_run': False,
            'quest_skip_remaining': remain,
        }):
            for force, order in [(False, self.first_order), (True, self.second_order)]:
                if client.quest_skip_remaining <= 0:
                    break
                for module in order:
                    if client.quest_skip_remaining <= 0:
                        break
                    sweep = module(self._parent)
                    if force:
                        sweep.config_overrides[sweep.key] = True
                        for key, config in sweep.config.items():
                            if isinstance(config, ConditionalNotExecutionClient):
                                sweep.config_overrides[key] = []
                            elif isinstance(config, ConditionalExecutionWrapper):
                                sweep.config_overrides[key] = ['总是执行']
                    before = client.quest_skip_remaining
                    with client.override_config({'quest_skip_no_stamina': False}):
                        result = await sweep.do_from(client)
                        count = before - client.quest_skip_remaining
                        if count or client.quest_skip_no_stamina:
                            msg = f"{sweep.name}: 扫荡{count}次"
                            if client.quest_skip_no_stamina:
                                msg += "，体力不足"
                            self._log(msg)
                    if result.status == eResultStatus.PANIC:
                        raise PanicError(f"{sweep.name}执行失败: {result.log}")
                    if result.status == eResultStatus.ERROR:
                        raise ValueError(f"{sweep.name}执行失败: {result.log}")

            if client.quest_skip_remaining > 0:
                self._warn(f"职能券任务还需扫荡{client.quest_skip_remaining}次")
