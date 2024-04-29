from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.custom import ItemType
from ...db.models import QuestDatum, ShioriQuest
from typing import List, Dict, Tuple
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from collections import Counter
import datetime

@conditional_execution("normal_sweep_run_time", ["n庆典"])
@singlechoice("normal_sweep_consider_unit", "需求角色", "favorite", ["all", "max_rank", "max_rank-1", "max_rank-2", 'favorite'])
@description('根据【刷图推荐】结果刷n图')
@name('智能刷n图')
@default(False)
@stamina_relative
class smart_normal_sweep(Module):

    async def do_task(self, client: pcrclient):

        if self.get_config('normal_sweep_consider_unit') == 'favorite':
            demand = client.data.get_equip_demand(like_unit_only = True)
        else:
            opt: Dict[Union[int, str], int] = {
                'all': 1,
                'max_rank': db.equip_max_rank,
                'max_rank-1': db.equip_max_rank - 1,
                'max_rank-2': db.equip_max_rank - 2,
            }
            demand = client.data.get_equip_demand(start_rank = opt[self.get_config('normal_sweep_consider_unit')])

        clean_cnt = Counter()
        quest_id = []
        tmp = []
        quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= datetime.datetime.now()]
        stop: bool = False

        try:
            for i in range(10000):

                if i % 3 == 0:

                    gap = client.data.get_demand_gap(demand, lambda x: db.is_equip(x))
                    quest_weight = client.data.get_quest_weght(gap)
                    quest_id = sorted(quest_list, key = lambda x: quest_weight[x], reverse = True)

                target_id = quest_id[0]
                try:
                    resp = await client.quest_skip_aware(target_id, 3)
                    tmp.extend([item for item in resp if db.is_equip((item.type, item.id))]) 
                    clean_cnt[target_id] += 3
                except SkipError:
                    pass
                except AbortError as e:
                    stop = True
                    if str(e).endswith("体力不足"):
                        if not tmp and not self.log: self._log(str(e))
                    else:
                        raise e
                    break
                if stop:
                    break
        except:
            raise 
        finally:
            if clean_cnt:
                msg = '\n'.join((db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}") +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
            if tmp:
                self._log(await client.serlize_reward(tmp))


class simple_demand_sweep_base(Module):

    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]: ...
    def get_need_quest(self, token: ItemType) -> List[QuestDatum]: ...
    def get_max_times(self, client: pcrclient, quest_id: int) -> int: ...

    async def do_task(self, client: pcrclient):

        need_list = await self.get_need_list(client)

        stop = False
        clean_cnt = Counter()
        tmp = []
        try:
            for token, _ in need_list:
                for quest in self.get_need_quest(token):
                    max_times = self.get_max_times(client, quest.quest_id)
                    try:
                        resp = await client.quest_skip_aware(quest.quest_id, max_times, True, True)
                        clean_cnt[quest.quest_id] += max_times
                        tmp.extend([item for item in resp if (item.type, item.id) == token]) 
                    except SkipError as e:
                        pass
                    except AbortError as e:
                        if str(e).endswith("体力不足"):
                            stop = True
                            if not tmp and not self.log: self._log(str(e))
                        elif str(e).endswith("未通关或不存在"):
                            self._log(f"{db.get_inventory_name_san(token)}: {str(e)}")
                        else:
                            raise e
                        break
                if stop:
                    break
        except:
            raise 
        finally:
            if clean_cnt:
                msg = '\n'.join((db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}") +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
            if tmp:
                self._log(await client.serlize_reward(tmp))
            if not self.log:
                raise SkipError("需刷取的图均无次数")


@conditional_execution("hard_sweep_run_time", ["h庆典"])
@singlechoice('hard_sweep_consider_unit_order', "刷取顺序", "缺口少优先", ["缺口少优先", "缺口大优先"])
@booltype('hard_sweep_consider_high_rarity_first', "三星角色优先", False)
@description('根据记忆碎片缺口刷hard图，不包括外传')
@name('智能刷hard图')
@default(False)
@stamina_relative
class smart_hard_sweep(simple_demand_sweep_base):

    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        need_list = client.data.get_memory_demand_gap()
        need_list = [(token, need) for token, need in need_list.items() if need > 0]
        if not need_list:
            raise SkipError("所有记忆碎片均已盈余")
        reverse = -1 if self.get_config('hard_sweep_consider_unit_order') == '缺口大优先' else 1
        high_rarity_first = self.get_config('hard_sweep_consider_high_rarity_first')
        need_list = sorted(need_list, key=lambda x: (
            - db.unit_data[db.memory_to_unit[x[0][1]]].rarity * high_rarity_first, 
            x[1] * reverse))

        return need_list

    def get_need_quest(self, token: ItemType) -> List[QuestDatum]:
        return db.memory_hard_quest.get(token, [])

    def get_max_times(self, client: pcrclient, quest_id: int) -> int:
        return 3

@conditional_execution("shiori_sweep_run_time", ["无庆典"])
@singlechoice('shiori_sweep_consider_unit_order', "刷取顺序", "缺口少优先", ["缺口少优先", "缺口大优先"])
@description('根据记忆碎片缺口刷外传图')
@name('智能刷外传图')
@default(False)
@stamina_relative
class smart_shiori_sweep(simple_demand_sweep_base):

    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        need_list = client.data.get_memory_demand_gap()
        need_list = [(token, need) for token, need in need_list.items() if need > 0]
        if not need_list:
            raise SkipError("所有记忆碎片均已盈余")
        reverse = -1 if self.get_config('shiori_sweep_consider_unit_order') == '缺口大优先' else 1
        need_list = sorted(need_list, key=lambda x: (
            - db.unit_data[db.memory_to_unit[x[0][1]]].rarity, 
            x[1] * reverse))

        return need_list

    def get_need_quest(self, token: ItemType) -> List[ShioriQuest]:
        return db.memory_shiori_quest.get(token, [])

    def get_max_times(self, client: pcrclient, quest_id: int) -> int:
        return 5

unique_equip_2_pure_memory_id = [
        (32025, 1), # 水女仆
        (32046, 1), # 水猫剑
        (32048, 1), # 水子龙
        (32060, 1), # 黑猫
        (32016, 1), # 暴击弓
        (32031, 1), # 万圣忍
        (32050, 1), # 万圣大眼
        (32007, 1), # 万圣布丁
        (32058, 1), # 吃货
        (32033, 1), # 奶牛
        (32023, 1), # 圣锤
        (32042, 1), # 圣千
        (32021, 1), # 圣铃铛
        (32049, 2), # 情姐，姐姐
        (32027, 1), # 情病
        (32011, 1), # 妹弓
        (32045, 1), # 江花
        (32030, 1), # 忍扇
        (32040, 1), # 生菜
        (32013, 1), # 七七香
]
@conditional_execution("very_hard_sweep_run_time", ["vh庆典"])
@description('储备专二需求的150碎片，包括' + ','.join(db.get_item_name(item_id) for item_id, _ in unique_equip_2_pure_memory_id))
@name('专二纯净碎片储备')
@default(False)
@stamina_relative
class mirai_very_hard_sweep(simple_demand_sweep_base):
    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        need_list = client.data.get_pure_memory_demand_gap()
        need_list += Counter({(eInventoryType.Item, pure_memory_id): 150 * cnt for pure_memory_id, cnt in unique_equip_2_pure_memory_id})
        need_list = [(token, need) for token, need in need_list.items() if need > 0]
        if not need_list:
            raise SkipError("所有纯净碎片均已盈余")
        return need_list

    def get_need_quest(self, token: ItemType) -> List[QuestDatum]:
        return db.pure_memory_quest.get(token, [])

    def get_max_times(self, client: pcrclient, quest_id: int) -> int:
        return 5 if db.is_shiori_quest(quest_id) else 3

@singlechoice("vh_sweep_campaign_times", "庆典次数", 3, [0, 3, 6])
@singlechoice("vh_sweep_times", "非庆典次数", 3, [0, 3, 6])
@description('根据纯净碎片缺口智能刷vh图')
@name('智能刷very hard图')
@default(True)
@stamina_relative
class smart_very_hard_sweep(simple_demand_sweep_base):
    times: int = -1

    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        need_list = client.data.get_pure_memory_demand_gap()
        need_list = [(token, need) for token, need in need_list.items() if need > 0]
        if not need_list:
            raise SkipError("所有纯净碎片均已盈余")

        return need_list

    def get_need_quest(self, token: ItemType) -> List[QuestDatum]:
        return db.pure_memory_quest.get(token, [])

    def get_max_times(self, client: pcrclient, quest_id: int) -> int:
        if self.times == -1:
            if not client.data.is_very_hard_quest_campaign():
                self.times = self.get_config('vh_sweep_times')
            else:
                self.times = self.get_config('vh_sweep_campaign_times')
        return self.times

@description('''
首先按次数逐一刷取名字为start的图
然后循环按次数刷取设置为loop的图
当被动体力回复完全消耗后，刷图结束
'''.strip())
@name("自定义刷图")
@conditional_execution("start_run_time", ['h庆典'], desc="start刷取庆典", check=False)
@conditional_execution("loop_run_time", ['n庆典'], desc="loop刷取庆典", check=False)
@default(False)
@stamina_relative
class smart_sweep(Module):
    async def do_task(self, client: pcrclient):
        nloop: List[Tuple[int, int]] = []
        loop: List[Tuple[int, int]] = []
        is_start_run_time, _ = await (self.get_config_instance('start_run_time').do_check(client))
        is_loop_run_time, _ = await (self.get_config_instance('loop_run_time').do_check(client))
        if is_start_run_time: self._log(f"刷取start关卡")
        if is_loop_run_time: self._log(f"刷取loop关卡")

        for tab in client.data.user_my_quest:
            for x in tab.skip_list:
                if tab.tab_name == 'start' and is_start_run_time:
                    nloop.append((x, tab.skip_count))
                elif tab.tab_name == 'loop' and is_loop_run_time:
                    loop.append((x, tab.skip_count))
        have_normal = any(db.is_normal_quest(quest[0]) for quest in loop)
        def _sweep():
            for x in nloop:
                yield x
            if loop:
                while True:
                    for x in loop:
                        yield x
                    if not have_normal:
                        raise AbortError("no normal, stop")

        result = []
        if nloop == [] and loop == []:
            raise SkipError("无刷取关卡")
        clean_cnt = Counter()
        for quest_id, count in _sweep(): 
            try:
                result += await client.quest_skip_aware(quest_id, count, True, True)
                clean_cnt[quest_id] += count
            except SkipError as e:
                pass
            except AbortError as e:
                self._log(str(e))
                break
        
        if clean_cnt:
                msg = '\n'.join((db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}") +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
        if result:
            self._log(await client.serlize_reward(result))
