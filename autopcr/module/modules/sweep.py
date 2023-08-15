from abc import abstractmethod
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

class explore_sweep(Module):
    @abstractmethod
    def remain_cnt(self, client: pcrclient) -> int: ...
    @abstractmethod
    def get_max_quest(self, client: pcrclient, sweep_available: bool = False) -> int: ...
    @abstractmethod
    def not_max_stop(self): ...

    async def do_task(self, client: pcrclient):
        remain_cnt = self.remain_cnt(client)
        if remain_cnt:
            quest_id = self.get_max_quest(client, sweep_available = True)
            if not quest_id:
                raise AbortError("不存在可扫荡的探索")
            if self.not_max_stop() and self.get_max_quest(client) != quest_id:
                raise AbortError(f"最高级探索{self.get_max_quest}未通关，不扫荡")
            name = db.quest_name[quest_id]
            await client.training_quest_skip(quest_id, remain_cnt)
            self._log(f"{name}扫荡{remain_cnt}次")
        else:
            raise SkipError("今日已扫荡")

@description('自动扫荡可扫荡的最高等级的EXP探索')
@name('EXP探索')
@booltype("exp_not_max_stop", "非最高不扫荡", True)
@default(True)
class explore_exp(explore_sweep):
    def remain_cnt(self, client: pcrclient) -> int: 
        return client.data.training_quest_max_count.exp_quest - client.data.training_quest_count.exp_quest
    def get_max_quest(self, client: pcrclient, sweep_available: bool = False) -> int:
        return client.data.get_max_quest_exp(sweep_available)
    def not_max_stop(self): 
        return self.get_config("exp_not_max_stop")

@description('自动扫荡可扫荡的最高等级的Mana探索')
@name('Mana探索')
@booltype("mana_not_max_stop", "非最高不扫荡", True)
@default(True)
class explore_mana(explore_sweep):
    def remain_cnt(self, client: pcrclient) -> int: 
        return client.data.training_quest_max_count.gold_quest - client.data.training_quest_count.gold_quest
    def get_max_quest(self, client: pcrclient, sweep_available: bool = False) -> int:
        return client.data.get_max_quest_mana(sweep_available)
    def not_max_stop(self): 
        return self.get_config("mana_not_max_stop")

@singlechoice("underground_sweep", "扫荡策略", "总是扫荡", ["非庆典留一次数", "总是扫荡"])
@description('会选择最高级地下城扫荡，非mana庆典时会自动保留一个次数，但第一次时需手动打一关以完成每日任务')
@name('地下城扫荡')
@default(True)
class underground_skip(Module):
    async def do_task(self, client: pcrclient):
        infos = await client.get_dungeon_info()

        async def do_enter(now_id = None):
            id = max([0] + infos.dungeon_cleared_area_id_list) if not now_id else now_id
            if id > 0:
                await client.enter_dungeon(id)
                dungeon_name = db.dungeon_name[id]
                self._log(f"已进入【{dungeon_name}】")
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        async def do_sweep(now_id = None):
            id = max([0] + infos.dungeon_cleared_area_id_list) if not now_id else now_id
            dungeon_name = db.dungeon_name[id]
            if id > 0:
                if id not in infos.dungeon_cleared_area_id_list:
                    raise AbortError(f"{dungeon_name}未讨伐，无法扫荡")
                reward_list = await client.skip_dungeon(id)
                rewards = [reward for reward_item in reward_list.skip_result_list for reward in reward_item.reward_list 
                           if db.is_unit_memory((reward.type, reward.id)) 
                           or db.xinsui == (reward.type, reward.id)
                           or db.xingqiubei == (reward.type, reward.id)]
                result = await client.serlize_reward(rewards)
                self._log(f"扫荡了【{dungeon_name}】,获得了:\n{result}")
                return reward_list.rest_challenge_count[0].count
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        double_mana = client.data.is_dungeon_mana_double()
        rest = infos.rest_challenge_count[0].count
        if infos.enter_area_id != 0:
            dungeon_name = db.dungeon_name[infos.enter_area_id]
            self._log(f"当前位于【{dungeon_name}】")
            if double_mana:
                self._log(f"今日地下城双倍mana")
                rest = await do_sweep(infos.enter_area_id)
            else:
                self._log(f"今日地下城非双倍mana")
                if rest:
                    self._log(f"还有{rest}次挑战次数，进行扫荡")
                    rest = await do_sweep(infos.enter_area_id)
                else:
                    if self.get_config('underground_sweep') == "总是扫荡":
                        rest = await do_sweep(infos.enter_area_id)
                        
        if rest:
            if double_mana or self.get_config('underground_sweep') == "总是扫荡":
                await do_sweep()
            else:
                await do_enter()
        else:
            raise SkipError("今日已扫荡地下城")


class investigate_sweep(Module):
    @abstractmethod
    def quest_id(self) -> int: ...
    @abstractmethod
    def is_double_drop(self, client: pcrclient) -> bool: ...
    @abstractmethod
    def target_item(self) -> ItemType: ...
    @abstractmethod
    def value(self, campaign: bool) -> int: ...

    async def do_task(self, client: pcrclient):
        times = self.value(self.is_double_drop(client))
        result = await client.quest_skip_aware(self.quest_id(), times, True, True)
        msg = await client.serlize_reward(result, self.target_item())
        self._log(f"重置{times // 5 - 1}次，获得了{msg}")

class xinsui_sweep(investigate_sweep):
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_heart_piece_double()
    def target_item(self) -> ItemType:
        return db.xinsui
    def value(self, campaign: bool):
        if not campaign:
            return self.get_config(f'heart{self.quest_id() % 10}_sweep_times')
        else:
            return self.get_config(f'heart{self.quest_id() % 10}_sweep_campaign_times')

class starcup_sweep(investigate_sweep):
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_star_cup_double()
    def target_item(self) -> ItemType:
        return db.xingqiubei
    def value(self, campaign: bool):
        if not campaign:
            return self.get_config(f'starcup{self.quest_id() % 10}_sweep_times')
        else:
            return self.get_config(f'starcup{self.quest_id() % 10}_sweep_campaign_times')

@singlechoice("heart4_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart4_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎4')
@default(False)
class xinsui4_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001004

@singlechoice("heart3_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart3_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎3')
@default(False)
class xinsui3_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001003

@singlechoice("heart2_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart2_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎2')
@default(False)
class xinsui2_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001002

@singlechoice("heart1_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart1_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎1')
@default(False)
class xinsui1_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001001

@singlechoice("starcup2_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("starcup2_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取星球杯2')
@default(False)
class starcup2_sweep(starcup_sweep):
    def quest_id(self) -> int:
        return 19001002

@singlechoice("starcup1_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("starcup1_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取星球杯1')
@default(False)
class starcup1_sweep(starcup_sweep):
    def quest_id(self) -> int:
        return 19001001
