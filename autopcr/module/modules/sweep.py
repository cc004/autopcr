from abc import abstractmethod
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

@singlechoice("underground_sweep", "扫荡策略", "always", ["非地下城庆典留一次数", "总是扫荡"])
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
                    if self.get_config('underground_sweep') == "总是执行":
                        rest = await do_sweep(infos.enter_area_id)
                        
        if rest:
            if double_mana or self.get_config('underground_sweep') == "总是执行":
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
            return self.get_config('heart_sweep_times')
        else:
            return self.get_config('heart_sweep_campaign_times')

class starcup_sweep(investigate_sweep):
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_star_cup_double()
    def target_item(self) -> ItemType:
        return db.xingqiubei
    def value(self, campaign: bool):
        if not campaign:
            return self.get_config('starcup_sweep_times')
        else:
            return self.get_config('starcup_sweep_campaign_times')

@singlechoice("heart_sweep_times", "非心碎庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart_sweep_campaign_times", "心碎庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎3')
@default(False)
class xinsui3_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001003

@singlechoice("heart_sweep_times", "非心碎庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart_sweep_campaign_times", "心碎庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎2')
@default(False)
class xinsui2_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001002

@singlechoice("heart_sweep_times", "非心碎庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart_sweep_campaign_times", "心碎庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎1')
@default(False)
class xinsui1_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001001

@singlechoice("starcup_sweep_times", "非星球杯庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("starcup_sweep_campaign_times", "星球杯庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取星球杯2')
@default(False)
class starcup2_sweep(starcup_sweep):
    def quest_id(self) -> int:
        return 19001002

@singlechoice("starcup_sweep_times", "非星球杯庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("starcup_sweep_campaign_times", "星球杯庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取星球杯1')
@default(False)
class starcup1_sweep(starcup_sweep):
    def quest_id(self) -> int:
        return 19001001
