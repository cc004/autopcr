from abc import abstractmethod
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...model.custom import ItemType
from ...util.linq import flow
from ...model.common import InventoryInfo, TravelAppearEventData, TravelCurrentCurrencyNum, TravelDecreaseItem, TravelExtraEquipAutoRecycleOptionData, TravelQuestAddLap, TravelQuestInfo, TravelStartInfo
import time
import random
from collections import Counter
import math


@description('''
仅支持阅读特殊事件+续派遣次数到最大派遣数。
装备事件为 60%三金装40%一金装 或 100%二金装 选项
代币事件为 30%1000代币70%200代币 或 100%400代币 选项
赌狗策略为前者，保守策略为后者
'''.strip())
@singlechoice('travel_quest_gold_event_strategy', "代币事件策略", ['随机'], ['保守','赌狗','随机'])
@singlechoice('travel_quest_equip_event_strategy', "装备事件策略", ['随机'], ['保守','赌狗','随机'])
@inttype('travel_quest_max_round', "最大派遣数", 3, [2,3,4,5])
@name("探险")
@default(True)
class travel_quest_sweep(Module):
    def can_receive_count(self, quest: TravelQuestInfo) -> int:
        st = quest.travel_start_time
        ed = quest.travel_end_time
        decrease_time = quest.decrease_time
        once_time = db.calc_travel_once_time(quest.total_power)
        now = int(time.time())
        received_count = quest.received_count
        cnt = (min(now, ed) - st + decrease_time) // once_time - received_count
        return cnt

    def quest_still_round(self, quest: TravelQuestInfo) -> int:
        return quest.total_lap_count - quest.received_count

    def get_choice(self, strategy: str) -> int:
        if strategy == '赌狗':
            return 1
        elif strategy == '保守':
            return 2
        else:
            return random.randint(1, 2)

    async def do_task(self, client: pcrclient):
        travel_quest_max_round: int = int(self.get_config("travel_quest_max_round"))
        travel_quest_equip_event_strategy: str = self.get_config("travel_quest_equip_event_strategy")
        travel_quest_gold_event_strategy: str = self.get_config("travel_quest_gold_event_strategy")
        reward: List[InventoryInfo] = []

        def get_strategy(event_id: int) -> str:
            if event_id == 4007:
                return travel_quest_equip_event_strategy
            elif event_id == 4009:
                return travel_quest_gold_event_strategy
            else:
                raise ValueError(f"未知可选项事件{event_id}")

        top = await client.travel_top(max(db.get_open_travel_area()), 1)

        if len(top.travel_quest_list) < 3:
            self._warn(f"正在探险的小队数为{len(top.travel_quest_list)}<3，请上号开始新的探险！")

        if top.top_event_list:
            for top_event in top.top_event_list:
                try:
                    chooice = 0
                    if top_event.top_event_choice_flag:
                        strategy = get_strategy(top_event.top_event_id)
                        chooice = self.get_choice(strategy)
                    result = await client.travel_receive_top_event_reward(top_event.top_event_appear_id, chooice)
                    reward.extend(result.reward_list)
                except Exception as e:
                    self._warn(f"处理特殊事件{top_event.top_event_id}失败:{e}")
            self._log(f"阅读{len(top.top_event_list)}个特殊事件")
        result_count = {}
        reward2: List[InventoryInfo] = []
        if any(self.can_receive_count(quest) for quest in top.travel_quest_list):
            option = TravelExtraEquipAutoRecycleOptionData(rarity=[], frame=[], category=[])
            result = await client.travel_receive_all(option)
            secret_travel: List[TravelAppearEventData] = []
            for quest in result.travel_result:
                reward2.extend(quest.reward_list)
                for event in quest.appear_event_list or []:
                    reward2.extend(event.reward_list)
                    secret_travel.append(event)

            result_count = Counter([quest.travel_quest_id for quest in result.travel_result])
            msg = '探索了:' + ' '.join(f"{db.get_quest_name(quest)} x{cnt}" for quest, cnt in result_count.items())
            self._log(msg)
            if secret_travel:
                msg = '触发了秘密探险：' + ' '.join(db.ex_event_data[event.still_id].title for event in secret_travel)
                self._log(msg)

        if reward or reward2:
            self._log(f"获得了:")
            msg = (await client.serlize_reward(reward)).strip('无')
            if msg: self._log(msg)
            msg = (await client.serlize_reward(reward2, filter=lambda x: db.is_ex_equip(x) or db.is_unit_memory(x))).strip('无')
            if msg: self._log(msg)
            self._log("")

        add_lap_travel_quest_list: List[TravelQuestAddLap] = []
        add_lap_travel_quest_id: List[int] = []
        start_travel_quest_list: List[TravelStartInfo] = []
        for quest in top.travel_quest_list:
            quest.received_count += result_count.get(quest.travel_quest_id, 0)
            quest_still_round = self.quest_still_round(quest)
            if not quest_still_round: # restart
                start_item = TravelStartInfo(
                        travel_quest_id = quest.travel_quest_id,
                        travel_deck = quest.travel_deck,
                        decrease_time_item = TravelDecreaseItem(jewel = 0, item = 0),
                        total_lap_count = travel_quest_max_round,
                 )
                start_travel_quest_list.append(start_item)
            else:
                append_round = travel_quest_max_round - quest_still_round
                if append_round > 0:
                    add_item = TravelQuestAddLap(travel_id = quest.travel_id, add_lap_count = append_round)
                    add_lap_travel_quest_list.append(add_item)
                    add_lap_travel_quest_id.append(quest.travel_quest_id)

        if start_travel_quest_list or add_lap_travel_quest_list:
            jewel = client.data.jewel.free_jewel + client.data.jewel.jewel
            speed_up_paper = client.data.get_inventory(db.travel_speed_up_paper)
            msg = '\n'.join(f"继续派遣{db.get_quest_name(quest_id)} x{quest.add_lap_count}" for quest_id, quest in zip(add_lap_travel_quest_id, add_lap_travel_quest_list))
            msg += '\n'.join(f"重新派遣{db.get_quest_name(quest.travel_quest_id)} x{quest.total_lap_count}" for quest in start_travel_quest_list)
            self._log(msg)
            action_type = eTravelStartType.ADD_LAP if add_lap_travel_quest_list else eTravelStartType.RESTART
            if start_travel_quest_list and add_lap_travel_quest_list:
                action_type = eTravelStartType.RESTART_AND_ADD
            await client.travel_start(start_travel_quest_list, add_lap_travel_quest_list, [], action_type, TravelCurrentCurrencyNum(jewel = jewel, item=speed_up_paper))

        if not self.log and not reward:
            raise SkipError("探险仍在继续...")

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
                raise SkipError("不存在可扫荡的探索")
            max_quest = self.get_max_quest(client)
            if self.not_max_stop() and max_quest != quest_id:
                raise AbortError(f"最高级探索{max_quest}未通关，不扫荡\n如欲扫荡已通关的，请关闭【非最高不扫荡】")
            name = db.get_quest_name(quest_id)
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
@booltype("underground_not_max_stop", "非最高不扫荡", True)
@booltype("secret_dungeon_stop", "特别地下城期间不扫荡", True)
@description('会选择最高级地下城扫荡，非庆典留一次数指非mana庆典时会位于地下城内不扫荡，以期庆典当天能扫荡两次，获得更多的mana，但第一次时需手动打一关以完成每日任务')
@name('地下城扫荡')
@default(True)
class underground_skip(Module):
    async def do_task(self, client: pcrclient):
        infos = await client.get_dungeon_info()
        if not infos.dungeon_cleared_area_id_list:
            infos.dungeon_cleared_area_id_list = []
        not_max_stop = self.get_config("underground_not_max_stop")
        always_sweep = self.get_config("underground_sweep") == "总是扫荡"
        secret_dungeon_stop = self.get_config("secret_dungeon_stop")

        def dungeon_name(id: int):
            return db.dungeon_area[id].dungeon_name

        def get_cleared_max_dungeon_id():
            return max([0] + [id for id in infos.dungeon_cleared_area_id_list if db.is_dungeon_id(id)])

        def get_max_dungeon_id():
            return (flow(db.dungeon_area.values())
                    .select(lambda x: x.dungeon_area_id)
                    .max()
                   )

        async def do_enter(now_id = None):
            id = get_cleared_max_dungeon_id() if not now_id else now_id
            if id > 0:
                await client.enter_dungeon(id)
                self._log(f"已进入【{dungeon_name(id)}】")
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        async def do_sweep(now_id = None):
            id = get_cleared_max_dungeon_id() if not now_id else now_id
            if id > 0:
                if id not in infos.dungeon_cleared_area_id_list:
                    raise AbortError(f"【{dungeon_name(id)}】未讨伐，无法扫荡")
                reward_list = await client.skip_dungeon(id)
                rewards = [reward for reward_item in reward_list.skip_result_list for reward in reward_item.reward_list 
                           if db.is_unit_memory((reward.type, reward.id)) 
                           or db.xinsui == (reward.type, reward.id)
                           or db.xingqiubei == (reward.type, reward.id)]
                result = await client.serlize_reward(rewards)
                self._log(f"扫荡了【{dungeon_name(id)}】,获得了:\n{result}")
                return reward_list.rest_challenge_count[0].count
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        double_mana = client.data.is_dungeon_mana_campaign()
        rest = infos.rest_challenge_count[0].count
        if infos.enter_area_id != 0:
            if db.is_secret_dungeon_id(infos.enter_area_id):
                raise SkipError("当前位于里地下城")

            self._log(f"当前位于【{dungeon_name(infos.enter_area_id)}】")
            if double_mana:
                self._log(f"今日地下城双倍mana")
                rest = await do_sweep(infos.enter_area_id)
            else:
                self._log(f"今日地下城非双倍mana")
                if rest:
                    self._log(f"还有{rest}次挑战次数，进行扫荡")
                    rest = await do_sweep(infos.enter_area_id)
                else:
                    if always_sweep:
                        rest = await do_sweep(infos.enter_area_id)

        if secret_dungeon_stop and db.is_secret_dungeon_time():
            raise SkipError("今日里地下城活动，不扫荡普通地下城")
                        
        if rest:
            if not_max_stop and get_max_dungeon_id() != get_cleared_max_dungeon_id():
                raise AbortError(f"最高级地下城【{dungeon_name(get_max_dungeon_id())}】未通关，不扫荡\n如欲扫荡已通关的，请关闭【非最高不扫荡】")
            if double_mana or always_sweep:
                await do_sweep()
            else:
                await do_enter()
        else:
            raise SkipError("今日已扫荡地下城")

@booltype("secret_dungeon_retreat", "自动撤退", False)
@description('只进入特别地下城，以期扫荡前5层。需首通一次。自动撤退指首通后，当前位于特别地下城，且还有挑战次数，则会撤退后再次进入，以扫荡前5层，用于只打30层。')
@name('特别地下城扫荡')
@default(True)
class special_underground_skip(Module):
    async def do_task(self, client: pcrclient):
        if not db.is_secret_dungeon_time():
            raise SkipError("当前无特别地下城")

        infos = await client.get_dungeon_info()

        special_dungeon_area = db.get_open_secret_dungeon_area()
        _special_info = None
        secret_dungeon_retreat = self.get_config("secret_dungeon_retreat")
        async def special_dungeon_info(refresh: bool = False):
            nonlocal _special_info
            if refresh or not _special_info:
                _special_info = await client.get_special_dungeon_info(special_dungeon_area)
            return _special_info

        def dungeon_name(id: int):
            if id in db.dungeon_area:
                return db.dungeon_area[id].dungeon_name
            elif id in db.secret_dungeon_area:
                return db.secret_dungeon_area[id].dungeon_name
            else:
                return f"未知地下城{id}"

        async def do_retreat(id: int):
            await client.reset_special_dungeon(id)
            self._log(f"从【{dungeon_name(id)}】撤退")

        async def do_enter(id):
            if db.secret_dungeon_area[id].open_area_id not in infos.dungeon_cleared_area_id_list:
                raise AbortError(f"【{dungeon_name(id)}】未讨伐，无法进入特别地下城")

            await special_dungeon_info(refresh=True)
            await client.deck_update(ePartyType.DUNGEON, [0, 0, 0, 0, 0])

            req = await client.enter_special_dungeon(id)
            reward_list = req.skip_result_list if req.skip_result_list else []
            rewards = [reward for reward_item in reward_list for reward in reward_item.reward_list 
                       if db.is_unit_memory((reward.type, reward.id)) 
                       or db.xinsui == (reward.type, reward.id)
                       or db.xingqiubei == (reward.type, reward.id)]
            result = await client.serlize_reward(rewards)
            self._log(f"进入了【{dungeon_name(id)}】,获得了:\n{result}")

        rest = infos.rest_challenge_count[0].count

        if infos.enter_area_id != 0:
            if not db.is_secret_dungeon_id(infos.enter_area_id):
                raise AbortError("当前位于普通地下城，不支持扫荡")

            self._log(f"当前位于【{dungeon_name(infos.enter_area_id)}】")
            if rest:
                if secret_dungeon_retreat:
                    if (await special_dungeon_info()).clear_num == 0:
                        raise AbortError("特别地下城未通关，将不撤退")
                    await do_retreat(infos.enter_area_id)
                else:
                    raise AbortError("今天仍有挑战次数，但设置不撤退")

                        
        if rest:
            await do_enter(special_dungeon_area)

        if (await special_dungeon_info()).clear_num == 0:
            raise AbortError("特别地下城尚未首通，请记得通关")

        if not rest:
            raise SkipError("今日已扫荡特别地下城")


@tag_stamina_consume
class investigate_sweep(Module):
    @abstractmethod
    def quest_id(self) -> int: ...
    @abstractmethod
    def is_double_drop(self, client: pcrclient) -> bool: ...
    @abstractmethod
    def target_item(self) -> ItemType: ...
    @abstractmethod
    def value(self, campaign: bool) -> int: ...
    @abstractmethod
    def force_stop(self, client: pcrclient) -> bool: ...

    async def do_task(self, client: pcrclient):
        if self.force_stop(client):
            raise SkipError("今日强制不刷取")
        times = self.value(self.is_double_drop(client))
        try:
            result = await client.quest_skip_aware(self.quest_id(), times, True, True)
        except AbortError as e:
            if str(e).endswith("体力不足"):
                raise SkipError(str(e))
            raise e
        msg = await client.serlize_reward(result, self.target_item())
        self._log(f"重置{times // 5 - 1}次，获得了{msg}")

class xinsui_sweep(investigate_sweep):
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_heart_piece_campaign()
    def target_item(self) -> ItemType:
        return db.xinsui
    def force_stop(self, client: pcrclient) -> bool:
        return client.is_heart_sweep_not_run()
    def value(self, campaign: bool):
        if not campaign:
            return self.get_config(f'heart{self.quest_id() % 10}_sweep_times')
        else:
            return self.get_config(f'heart{self.quest_id() % 10}_sweep_campaign_times')

class starcup_sweep(investigate_sweep):
    def is_double_drop(self, client: pcrclient) -> bool:
        return client.data.is_star_cup_campaign()
    def target_item(self) -> ItemType:
        return db.xingqiubei
    def force_stop(self, client: pcrclient) -> bool:
        return client.is_star_cup_sweep_not_run()
    def value(self, campaign: bool):
        if not campaign:
            return self.get_config(f'starcup{self.quest_id() % 10}_sweep_times')
        else:
            return self.get_config(f'starcup{self.quest_id() % 10}_sweep_campaign_times')

@singlechoice("heart5_sweep_campaign_times", "庆典次数", 5, [0, 5, 10, 15, 20])
@singlechoice("heart5_sweep_times", "非庆典次数", 5, [0, 5, 10, 15, 20])
@name('刷取心碎5')
@default(False)
class xinsui5_sweep(xinsui_sweep):
    def quest_id(self) -> int:
        return 18001005

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

@multichoice("travel_target_quest1", "轮转目标1", [1], [1, 2, 3, 4, 5])
@multichoice("travel_target_quest2", "轮转目标2", [4], [1, 2, 3, 4, 5])
@multichoice("travel_target_quest3", "轮转目标3", [2, 3, 5], [1, 2, 3, 4, 5])
@inttype("travel_target_day", "轮转时间", 7, [2, 3, 5, 7, 10])
@name('自动探险')
@description('''
自动根据轮转进行探险，按轮转时间进行目标切换，切换时自动用券进行尾轮加速。
'''.strip())
@default(False)
class auto_travel(Module):
    def today_targets(self) -> List[int]:
        n = time.localtime().tm_yday // int(self.get_config("travel_target_day"))
        def get_team(lst, n): return lst[n % len(lst)]
        return [
            get_team(self.get_config("travel_target_quest1"), n),
            get_team(self.get_config("travel_target_quest2"), n),
            get_team(self.get_config("travel_target_quest3"), n)
        ]
    async def do_task(self, client: pcrclient):
        area_id = max(db.get_open_travel_area())
        top = await client.travel_top(area_id, 1)
        targets = set(
            area_id * 1000 + x for x in self.today_targets()
        )

        now_targets = {
            quest.travel_quest_id: quest for quest in top.travel_quest_list
        }

        to_delete = {k: v for k, v in now_targets.items() if k not in targets}
        to_add = targets - set(now_targets.keys())
        
        start_infos = []

        for add_quest_id, (remove_quest_id, remove_quest) in zip(to_add, to_delete.items()):
            quest_interval = (remove_quest.travel_end_time - remove_quest.travel_start_time) / remove_quest.total_lap_count
            for i in range(remove_quest.total_lap_count):
                if remove_quest.travel_start_time + i * quest_interval > client.server_time:
                    break
            
            delta_time = remove_quest.travel_start_time + i * quest_interval - client.server_time
            ticket_to_use = math.ceil(delta_time / client.data.settings.travel.decrease_time_by_ticket)
            if ticket_to_use > client.data.get_inventory(db.travel_speed_up_paper):
                raise AbortError(f"没有足够的加速券，无法切换目标")
            if ticket_to_use > top.remain_daily_decrease_count_ticket:
                raise AbortError(f"本日剩余加速券不足，无法切换目标")
            if top.remain_daily_retire_count <= 0:
                raise AbortError("本日剩余撤退次数不足，无法切换目标")
            
            if remove_quest:
                self._log(f"结束探险{remove_quest_id}")

            await client.travel_decrease_time(remove_quest.travel_quest_id, remove_quest.travel_id, TravelDecreaseItem(jewel = 0, item = ticket_to_use))
            await client.travel_retire(remove_quest)

            top.remain_daily_decrease_count_ticket -= ticket_to_use
            top.remain_daily_retire_count -= 1

            start_infos.append(
                TravelStartInfo(
                    travel_quest_id = add_quest_id,
                    travel_deck = remove_quest.travel_deck,
                    decrease_time_item = TravelDecreaseItem(jewel = 0, item = 0),
                    total_lap_count = client.data.settings.travel.travel_quest_max_repeat_count
                )
            )
        
        await client.travel_start(
            start_infos,
            [],
            [],
            eTravelStartType.RESTART,
            TravelCurrentCurrencyNum(jewel = client.data.jewel.free_jewel + client.data.jewel.jewel, item = client.data.get_inventory(db.travel_speed_up_paper))
        )