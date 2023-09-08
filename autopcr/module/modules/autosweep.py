from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from typing import List, Dict
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from collections import Counter
import datetime

@multichoice("normal_sweep_run_time", "执行条件", ["n庆典"], ["n庆典", "h庆典", "vh庆典", "总是执行"])
@singlechoice("normal_sweep_consider_unit", "需求角色", "favorite", ["all", "max_rank", "max_rank-1", "max_rank-2", 'favorite'])
@description('根据装备缺口刷n图')
@name('智能刷n图')
@default(False)
class smart_normal_sweep(Module):

    async def do_task(self, client: pcrclient):
        run_time = set(self.get_config('normal_sweep_run_time'))
        if not (
        "n庆典" in run_time and client.data.is_normal_quest_campaign()
        or  "h庆典" in run_time and client.data.is_hard_quest_campaign()
        or  "vh庆典" in run_time and client.data.is_very_hard_quest_campaign()
        or "总是执行" in run_time):
            raise SkipError("今日不符合执行条件，不刷取")

        if self.get_config('normal_sweep_consider_unit') == 'favorite':
            require_equip = client.data.get_equip_demand(like_unit_only = True)
        else:
            opt: Dict[Union[int, str], int] = {
                'all': 1,
                'max_rank': db.equip_max_rank,
                'max_rank-1': db.equip_max_rank - 1,
                'max_rank-2': db.equip_max_rank - 2,
            }
            require_equip = client.data.get_equip_demand(start_rank = opt[self.get_config('normal_sweep_consider_unit')])

        clean_cnt = Counter()
        quest_id = []
        tmp = []
        quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= datetime.datetime.now()]
        stop: bool = False

        try:
            for i in range(10000):

                if i % 3 == 0:

                    demand = Counter({token: require_equip[token] - client.data.get_inventory(token) for token in client.data._inventory if db.is_equip(token)})
                    quest_weight = client.data.get_quest_weght(demand)
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


@singlechoice('hard_sweep_consider_unit_order', "刷取顺序", "缺口少优先", ["缺口少优先", "缺口大优先"])
@booltype('hard_sweep_consider_high_rarity_first', "三星角色优先", False)
@singlechoice("hard_sweep_run_time", "执行条件", "h庆典", ["h庆典", "非n庆典", "总是执行"])
@description('根据记忆碎片缺口刷hard图')
@name('智能刷hard图')
@default(False)
class smart_hard_sweep(Module):
    async def do_task(self, client: pcrclient):
        if self.get_config('hard_sweep_run_time') == "h庆典" and not client.data.is_hard_quest_campaign():
            raise SkipError("今日非hard庆典，不刷取")
        if self.get_config('hard_sweep_run_time') == "非n庆典" and client.data.is_normal_quest_campaign():
            raise SkipError("今日normal庆典，不刷取")

        need_list = client.data.get_memory_demand_gap()
        need_list = [(token, need) for token, need in need_list.items() if need > 0]

        if not need_list:
            raise SkipError("不存在缺乏的记忆碎片")

        reverse = -1 if self.get_config('hard_sweep_consider_unit_order') == '缺口大优先' else 1
        high_rarity_first = self.get_config('hard_sweep_consider_high_rarity_first')
        need_list = sorted(need_list, key=lambda x: (
            - db.unit_data[db.memory_to_unit[x[0][1]]].rarity * high_rarity_first, 
            x[1] * reverse))

        stop = False
        clean_cnt = Counter()
        tmp = []
        try:
            for token, _ in need_list:
                for quest in db.memory_quest.get(token, []):
                    max_times = 5 if db.is_shiori_quest(quest.quest_id) else 3
                    try:
                        resp = await client.quest_skip_aware(quest.quest_id, max_times)
                        clean_cnt[quest.quest_id] += max_times
                        tmp.extend([item for item in resp if (item.type, item.id) == token]) 
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

@singlechoice("vh_sweep_campaign_times", "庆典次数", 3, [0, 3, 6])
@singlechoice("vh_sweep_times", "非庆典次数", 3, [0, 3, 6])
@description('根据纯净碎片缺口智能刷vh图')
@name('智能刷very hard图')
@default(True)
class smart_very_hard_sweep(Module):
    async def do_task(self, client: pcrclient):
        times = 3
        if not client.data.is_very_hard_quest_campaign():
            times = self.get_config('vh_sweep_times')
        else:
            times = self.get_config('vh_sweep_campaign_times')

        is_skip = True
        for quest_id, quest in db.six_area.items():
            pure_memory = quest.reward_image_1
            unit_id = db.pure_memory_to_unit[pure_memory]
            data = client.data.unit.get(unit_id, None) # unlock unit
            if (not data or data.unit_rarity != 6) and \
            (not data or 
             not data.unlock_rarity_6_item or 
             not data.unlock_rarity_6_item.slot_1) and \
            client.data.get_inventory((eInventoryType.Item, pure_memory)) < 50:
                try:
                    rewards = await client.quest_skip_aware(quest_id, times, True, True)
                    msg = await client.serlize_reward(rewards, (eInventoryType.Item, pure_memory))
                    is_skip = False
                    self._log(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {msg}")
                except SkipError as e:
                    self._log(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                except AbortError as e:
                    raise AbortError(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
                except Exception as e:
                    raise ValueError(f"{db.inventory_name[(eInventoryType.Unit, unit_id)]}六星本: {str(e)}")
            else:
                pass
                # result.append(f"{quest_id}: 材料已够，无需刷取")
        if is_skip: raise SkipError("")
        if not self.log:
            raise SkipError("六星碎片均已足够，无需刷取")

@description('''
首先按次数逐一刷取名字为start的图
然后循环按次数刷取设置为loop的图
当被动体力回复完全消耗后，刷图结束
'''.strip())
@name("自定义刷图")
@default(False)
class smart_sweep(Module):
    async def do_task(self, client: pcrclient):
        nloop: List[Tuple[int, int]] = []
        loop: List[Tuple[int, int]] = []
        for tab in client.data.user_my_quest:
            for x in tab.skip_list:
                if tab.tab_name == 'start':
                    nloop.append((x, tab.skip_count))
                elif tab.tab_name == 'loop':
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
            raise AbortError("未找到start和loop")
        clean_cnt = Counter()
        for quest_id, count in _sweep(): 
            try:
                result += await client.quest_skip_aware(quest_id, count, True, True)
                clean_cnt[quest_id] += count
            except SkipError as e:
                pass
            except AbortError as e:
                if not self.log and not str(e).endswith("体力不足"):
                    self._log(str(e))
                break
        
        if clean_cnt:
                msg = '\n'.join((db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}") +
                f": 刷取{cnt}次" for quest, cnt in clean_cnt.items())
                self._log(msg)
                self._log("---------")
        if result:
            self._log(await client.serlize_reward(result))
