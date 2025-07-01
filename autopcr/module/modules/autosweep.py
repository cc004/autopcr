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

@conditional_execution1("normal_sweep_run_time", ["n庆典"])
@singlechoice("normal_sweep_strategy", "刷取策略", "刷最缺", ["刷最缺", "均匀刷"])
@singlechoice("normal_sweep_quest_scope", "刷取图", "全部", ["全部", "可扫荡", "新开图"])
@booltype("normal_sweep_full_ok_stop", "刷完所有角色停止", False)
@booltype("normal_sweep_equip_ok_to_full", "刷满则考虑所有角色", False)
@singlechoice("normal_sweep_consider_unit", "起始品级", "所有", ["所有", "最高", "次高", "次次高"])
@booltype("normal_sweep_consider_unit_fav", "收藏角色", True)
@description('根据【刷图推荐】结果刷n图，均匀刷指每次刷取的图覆盖所缺的需求装备，若无缺装备则刷取推荐的第一张图，仅可扫荡指忽略未三星通关地图')
@name('智能刷n图')
@default(False)
@tag_stamina_consume
class smart_normal_sweep(Module):

    async def get_quests(self, quest_list: List[int], strategy: str, gap: typing.Counter[ItemType]) -> List[int]:
        ret = []
        lack = set(item for item, need in gap.items() if need > 0)
        if (not lack or strategy == "刷最缺") and quest_list:
            ret.append(quest_list[0])
        elif strategy == "均匀刷":
            uncover = lack
            ret = []
            for quest in quest_list:
                if any(item in uncover for item in db.normal_quest_rewards[quest]):
                    ret.append(quest)
                    uncover -= set(db.normal_quest_rewards[quest])
                    if not uncover:
                        break
        else:
            raise ValueError(f"未知策略{strategy}")

        if not ret and quest_list:
            ret.append(quest_list[0])
        if not ret:
            self._log("无需刷取的图！")
        return ret

    async def do_task(self, client: pcrclient):

        like_unit_only: bool = self.get_config('normal_sweep_consider_unit_fav')
        rank: str = self.get_config('normal_sweep_consider_unit')
        strategy: str = self.get_config('normal_sweep_strategy')
        full2all: bool = self.get_config('normal_sweep_equip_ok_to_full')
        quest_scope: str = self.get_config('normal_sweep_quest_scope')
        full2stop: bool = self.get_config('normal_sweep_full_ok_stop')
        opt: Dict[Union[int, str], int] = {
            '所有': 1,
            '最高': db.equip_max_rank,
            '次高': db.equip_max_rank - 1,
            '次次高': db.equip_max_rank - 2,
        }
        demand = client.data.get_equip_demand(like_unit_only=like_unit_only, start_rank = opt[rank])
        all_demand = client.data.get_equip_demand()

        clean_cnt = Counter()
        quest_id = []
        tmp = []
        quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= apiclient.datetime]
        if quest_scope == "可扫荡":
            quest_list = [id for id in quest_list if client.data.is_quest_sweepable(id)]
        elif quest_scope == "新开图":
            last_normal = set(db.last_normal_quest())
            quest_list = [id for id in quest_list if id in last_normal]
        elif quest_scope != "全部":
            raise ValueError(f"未知刷取图范围{quest_scope}")
            
        stop: bool = False
        first: bool = True

        try:
            target_quest = []
            for i in range(10000):

                if i % 3 == 0:

                    gap = client.data.get_demand_gap(demand, lambda x: db.is_equip(x))
                    if all(gap[item] <= 0 for item in gap):
                        if first:
                            first = False
                            self._log("需求装备均已盈余")
                            if full2all:
                                demand = all_demand
                                gap = client.data.get_demand_gap(demand, lambda x: db.is_equip(x))
                                self._log("考虑所有角色的需求装备")

                                if all(gap[item] <= 0 for item in gap):
                                    self._log("所有角色的需求装备均已盈余")
                                    if full2stop:
                                        self._log("停止刷图")
                                        break

                    quest_weight = client.data.get_quest_weght(gap)
                    quest_id = sorted(quest_list, key = lambda x: quest_weight[x], reverse = True)
                    target_quest = await self.get_quests(quest_id, strategy, gap)
                    if not target_quest: break

                for target_id in target_quest:
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
                msg = '\n'.join(db.get_quest_name(quest) +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
            if tmp:
                self._log(await client.serialize_reward_summary(tmp))


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
                        tmp.extend(resp) 
                    except SkipError as e:
                        pass
                    except AbortError as e:
                        if str(e).endswith("体力不足"):
                            stop = True
                            if not tmp and not self.log: self._log(str(e))
                        elif str(e).endswith("未通关或不存在") or str(e).endswith("未三星"):
                            self._warn(f"{db.get_inventory_name_san(token)}: {str(e)}")
                        else:
                            self._log(str(e))
                            raise AbortError()
                        break
                if stop:
                    break
        except:
            raise 
        finally:
            if clean_cnt:
                msg = '\n'.join(db.get_quest_name(quest) +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
            if tmp:
                self._log(await client.serialize_reward_summary(tmp))
            if not self.log:
                self._log("需刷取的图均无次数")
                raise SkipError()


@singlechoice('hard_sweep_gap_limit', "盈余阈值", 10, [0, 5, 10])
@conditional_execution1("hard_sweep_run_time", ["h庆典"])
@singlechoice('hard_sweep_consider_unit_order', "刷取顺序", "缺口少优先", ["缺口少优先", "缺口大优先"])
@booltype('hard_sweep_consider_high_rarity_first', "三星角色优先", False)
@description('根据记忆碎片缺口刷hard图，不包括外传，直到盈余超过阈值')
@name('智能刷hard图')
@default(False)
@tag_stamina_consume
class smart_hard_sweep(simple_demand_sweep_base):

    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        gap_limit = self.get_config('hard_sweep_gap_limit')
        need_list = client.data.get_memory_demand_gap()
        need_list = [(token, need) for token, need in need_list.items() if need > -gap_limit]
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

@singlechoice('shiori_sweep_gap_limit', "盈余阈值", 10, [0, 5, 10])
@conditional_execution1("shiori_sweep_run_time", ["无庆典"])
@singlechoice('shiori_sweep_consider_unit_order', "刷取顺序", "缺口少优先", ["缺口少优先", "缺口大优先"])
@description('根据记忆碎片缺口刷外传图，直到盈余超过阈值')
@name('智能刷外传图')
@default(False)
@tag_stamina_consume
class smart_shiori_sweep(simple_demand_sweep_base):

    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        gap_limit = self.get_config('shiori_sweep_gap_limit')
        need_list = client.data.get_memory_demand_gap()
        need_list = [(token, need) for token, need in need_list.items() if need > -gap_limit]
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
        107701, # 水女仆
        107901, # 水猫剑
        108001, # 水子龙
        106001, # 黑猫
        101601, # 暴击弓
        108101, # 万圣忍
        108201, # 万圣布丁
        108301, # 万圣大眼
        103301, # 奶牛
        105801, # 吃货
        108401, # 圣千
        108501, # 圣铃铛
        108601, # 圣锤
        109001, # 情病
        109101, # 情姐
        104901, # 姐姐
        101101, # 妹弓
        109501, # 江花
        109601, # 忍扇
        101301, # 七七香
        110701, # 生菜
        110001, # 水暴
        110101, # 水老师
        110301, # 水电
        110401, # 水狼
        110501, # 水狗
        110601, # 水壶
        102501, # 女仆
        111101, # mcw
        111301, # 瓜兔
        111201, # 瓜炸
        105901, # 妈
        112201, # 魔驴
        112301, # 魔栞
        100301, # 剑圣
        112101, # 春女仆
        111501, # 圣克
        111701, # 圣yly
        111601, # 圣诞望
        107501, # 水吃
        113101, # 水流夏
        113301, # 水七七香
]
@conditional_execution1("very_hard_sweep_run_time", ["vh庆典"])
@description('储备专二需求的150碎片，包括' + ','.join(db.get_unit_name(unit_id) for unit_id in unique_equip_2_pure_memory_id))
@name('专二纯净碎片储备')
@default(False)
@tag_stamina_consume
class mirai_very_hard_sweep(simple_demand_sweep_base):
    async def get_need_list(self, client: pcrclient) -> List[Tuple[ItemType, int]]:
        pure_gap = client.data.get_pure_memory_demand_gap()
        target = Counter()
        need_list = []
        for unit in unique_equip_2_pure_memory_id:
            kana = db.unit_data[unit].kana
            target[kana] += 150 if unit not in client.data.unit or len(client.data.unit[unit].unique_equip_slot) < 2 or not client.data.unit[unit].unique_equip_slot[1].is_slot else 0
            own = -sum(pure_gap[db.unit_to_pure_memory[unit]] if unit in db.unit_to_pure_memory else 0 for unit in db.unit_kana_ids[kana])
            if own < target[kana]:
                need_list.append(((0, kana), target[kana] - own))
        if not need_list:
            raise SkipError("所有纯净碎片均已盈余")
        return need_list

    def get_need_quest(self, token: ItemType) -> List[QuestDatum]:
        kana = str(token[1])
        ret = []
        for unit in db.unit_kana_ids[kana]:
            if unit in db.unit_to_pure_memory:
                ret += db.pure_memory_quest.get(db.unit_to_pure_memory[unit], [])
        return ret

    def get_max_times(self, client: pcrclient, quest_id: int) -> int:
        return 5 if db.is_shiori_quest(quest_id) else 3

@singlechoice("vh_sweep_campaign_times", "庆典次数", 3, [0, 3, 6])
@singlechoice("vh_sweep_times", "非庆典次数", 3, [0, 3, 6])
@description('根据纯净碎片缺口智能刷vh图')
@name('智能刷very hard图')
@default(True)
@tag_stamina_consume
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

class DIY_sweep(Module):

    async def get_start_quest(self, client: pcrclient) -> List[Tuple[int, int]]:
        return []
    async def get_loop_quest(self, client: pcrclient) -> List[Tuple[int, int]]:
        return []

    async def do_task(self, client: pcrclient):
        nloop: List[Tuple[int, int]] = await self.get_start_quest(client)
        loop: List[Tuple[int, int]] = await self.get_loop_quest(client)

        have_normal = any(db.is_normal_quest(quest[0]) for quest in loop)
        def _sweep():
            for x in nloop:
                yield x
            if loop:
                while True:
                    for x in loop:
                        yield x
                    if not have_normal:
                        raise AbortError("为什么loop里没n关卡？")

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
                msg = '\n'.join(db.get_quest_name(quest) +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
        else:
            self._log("需刷取的图均无次数")
        if result:
            self._log(await client.serialize_reward_summary(result))

@description('''
首先按次数逐一刷取名字为start和start2的图
然后循环按次数刷取设置为loop的图
当被动体力回复完全消耗后，刷图结束
'''.strip())
@name("自定义刷图")
@conditional_execution1("start2_run_time", ['vh庆典'], desc="start2刷取庆典", check=False)
@conditional_execution1("start_run_time", ['h庆典'], desc="start刷取庆典", check=False)
@conditional_execution1("loop_run_time", ['n庆典'], desc="loop刷取庆典", check=False)
@default(False)
@tag_stamina_consume
class smart_sweep(DIY_sweep):
    async def get_start_quest(self, client: pcrclient) -> List[Tuple[int, int]]: 
        quest: List[Tuple[int, int]] = []
        for name, value in zip(['start', 'start2'], ['start_run_time', 'start2_run_time']):
            is_run_time, _ = await (self.get_config_instance(value).do_check(client))
            if is_run_time:
                self._log(f"刷取{name}关卡")
                for tab in client.data.user_my_quest:
                    if tab.tab_name == name:
                        for x in tab.skip_list:
                            quest.append((x, tab.skip_count))
        return quest

    async def get_loop_quest(self, client: pcrclient) -> List[Tuple[int, int]]:
        is_loop_run_time, _ = await (self.get_config_instance('loop_run_time').do_check(client))
        quest: List[Tuple[int, int]] = []
        if is_loop_run_time: 
            self._log(f"刷取loop关卡")
            for tab in client.data.user_my_quest:
                if tab.tab_name == 'loop':
                    for x in tab.skip_list:
                        quest.append((x, tab.skip_count))
        return quest

@description('''
开新图时的便捷设置，将循环刷取所选关卡
'''.strip())
@name("刷最新n图")
@conditional_execution1("last_normal_quest_run_time", ['n庆典'])
@LastNormalQuestConfig("last_normal_quests_sweep", "刷取关卡", [])
@default(False)
@tag_stamina_consume
class last_normal_quest_sweep(DIY_sweep):
    async def get_loop_quest(self, client: pcrclient) -> List[Tuple[int, int]]:
        last_sweep_quests: List[int] = self.get_config('last_normal_quests_sweep')
        last_sweep_quests_count: int = 3
        quest: List[Tuple[int, int]] = [(id, last_sweep_quests_count) for id in last_sweep_quests]
        return quest
