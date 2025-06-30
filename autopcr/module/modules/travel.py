from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...model.common import InventoryInfo, TravelAppearEventData, TravelDecreaseItem, TravelQuestAddLap, TravelQuestInfo, TravelStartInfo
from typing import Set
from collections import Counter
from ...util.ilp_solver import dispatch_solver
import math
import random
import time

@description('''
分解对应的EX装备，不分解已锁或已装备的EX装备
'''.strip())
@multichoice("ex_equip_recycle_category", "稀有度", ['普通铜', '普通银'], ['普通铜', '普通银', '会战银'])
@name("EX装备分解")
@default(True)
class ex_equip_recycle(Module):
    task = {
        '普通铜': lambda ex_id: db.ex_equipment_data[ex_id].rarity == 1 and db.ex_equipment_data[ex_id].clan_battle_equip_flag == 0,
        '普通银': lambda ex_id: db.ex_equipment_data[ex_id].rarity == 2 and db.ex_equipment_data[ex_id].clan_battle_equip_flag == 0,
        '会战银': lambda ex_id: db.ex_equipment_data[ex_id].rarity == 2 and db.ex_equipment_data[ex_id].clan_battle_equip_flag == 1,
    }

    async def do_task(self, client: pcrclient):
        ex_equip_resolve_category: List[str] = self.get_config("ex_equip_recycle_category")
        cnt = Counter()
        rewards = []

        slot_ex = set(ex.serial_id for unit in client.data.unit.values() for ex in unit.ex_equip_slot if ex.serial_id) | set(ex.serial_id for unit in client.data.unit.values() for ex in unit.cb_ex_equip_slot if ex.serial_id)

        async def resolve(filter: Callable[[int], bool]):
            serial_ids = [ex.serial_id for ex in client.data.ex_equips.values() if 
                          filter(ex.ex_equipment_id) and 
                          ex.protection_flag != 2 and 
                          ex.serial_id not in slot_ex]
            if serial_ids:
                gap = client.data.settings.ex_equip.ex_equip_limit_consume_num
                cnt[category] = len(serial_ids)
                for i in range(0, len(serial_ids), gap):
                    ret = await client.item_recycle_ex(serial_ids[i:i+gap])
                    rewards.extend(ret.item_list)

        for category in ex_equip_resolve_category:
            if category not in self.task:
                self._warn(f"未知的稀有度{category}")
            else:
                await resolve(self.task[category])

        if cnt:
            msg = "分解了" + ' '.join(f"{category}x{cnt}" for category, cnt in cnt.items())
            self._log(msg)
            msg = "获得了:\n" + (await client.serialize_reward_summary(rewards)).strip('无')
            self._log(msg)
        else:
            raise SkipError("没有可分解的装备")

class eEventReward(IntEnum):
    Unknown = 0
    Coin = 1
    Cake = 2
    EquipStone = 3
    ExpItem = 4
    Mana = 5
    HeartPiece = 6
    Muzhu = 7
    SingleTicket = 8

ManaTravelEventReward = {
    2001: eEventReward.Cake, # 佩可莉姆,凯露
    2002: eEventReward.HeartPiece, # 优衣,日和莉
    2003: eEventReward.ExpItem, # 未奏希,美美
    2004: eEventReward.HeartPiece, # 莫妮卡,空花
    2005: eEventReward.Mana, # 杏奈,流夏
    2006: eEventReward.Mana, # 千爱瑠,克罗依
    2007: eEventReward.ExpItem, # 望,纺希
    2008: eEventReward.SingleTicket, # 纯,克莉丝提娜
    2009: eEventReward.ExpItem, # 碧,美里
    2010: eEventReward.Cake, # 铃,真阳
    2011: eEventReward.HeartPiece, # 静流,璃乃
    2012: eEventReward.HeartPiece, # 真步,香织
    2013: eEventReward.Mana, # 伊莉亚,宫子
    2014: eEventReward.EquipStone, # 铃莓,咲恋
    2015: eEventReward.ExpItem, # 秋乃,由加莉
    2016: eEventReward.ExpItem, # 铃奈,伊绪
    2017: eEventReward.ExpItem, # 嘉夜,祈梨
    2018: eEventReward.Coin, # 克蕾琪塔
    2019: eEventReward.SingleTicket, # 矛依未,似似花
    2020: eEventReward.HeartPiece, # 花凛
    2021: eEventReward.Cake, # 香澄,真琴
    2022: eEventReward.Coin, # 胡桃,绫音
    2023: eEventReward.Coin, # 美冬,珠希
    2024: eEventReward.EquipStone, # 惠理子,深月
    2025: eEventReward.EquipStone, # 茉莉,智
    2026: eEventReward.HeartPiece, # 可可萝
    2027: eEventReward.HeartPiece, # 爱梅斯
    2028: eEventReward.SingleTicket, # 菈比莉斯塔,霸瞳皇帝
}

ManaTravelEventRemain = set({eEventReward.Coin, eEventReward.EquipStone, eEventReward.Cake, eEventReward.ExpItem, eEventReward.Mana})

@description('''
仅支持阅读特殊事件+续派遣次数到最大派遣数。
加速券大于保留值则会加速，建议与探险轮转的加速阈值保持一致。
装备事件为 60%三金装40%一金装 或 100%二金装 选项
代币事件为 30%1000代币70%200代币 或 100%400代币 选项
赌狗策略为前者，保守策略为后者
蓝色事件保留指不收取金币、蛋糕、强化石、经验药水、Mana事件，以期提高出现其他事件的概率，当保留事件超过阈值时会自动收取一个。
'''.strip())
@inttype('travel_top_blue_event_remain_cnt', '蓝色事件保留', 1, [0, 1, 2])
@TravelQuestConfig("travel_speed_up_target", "加速地图", [11002001, 11002004])
@singlechoice('travel_quest_gold_event_strategy', "代币事件策略", '赌狗', ['保守','赌狗','随机'])
@singlechoice('travel_quest_equip_event_strategy', "装备事件策略", '赌狗', ['保守','赌狗','随机'])
@inttype('travel_quest_speed_up_paper_hold', "加速券保留", 12, list(range(3001)))
@name("探险续航")
@default(True)
class travel_quest_sweep(Module):
    def can_receive_count(self, quest: TravelQuestInfo, now: int) -> int:
        st = quest.travel_start_time
        ed = quest.travel_end_time
        decrease_time = quest.decrease_time
        once_time = (ed - st) // quest.total_lap_count
        now = int(time.time())
        received_count = quest.received_count
        cnt = (min(now, ed) - st + decrease_time) // once_time - received_count
        return cnt

    def quest_still_round(self, quest: TravelQuestInfo) -> int:
        return quest.total_lap_count - quest.received_count

    def quest_left_time(self, quest: TravelQuestInfo, now: int) -> int:
        return max(0, quest.travel_end_time - quest.decrease_time - now)

    def get_choice(self, strategy: str) -> int:
        choice = 0
        if strategy == '赌狗':
            choice =  1
        elif strategy == '保守':
            choice =  2
        else:
            choice = random.randint(1, 2)
        self._log(f"选择{'赌狗' if choice == 1 else '保守'}策略")
        return choice

    async def do_task(self, client: pcrclient):
        travel_quest_equip_event_strategy: str = self.get_config("travel_quest_equip_event_strategy")
        travel_quest_gold_event_strategy: str = self.get_config("travel_quest_gold_event_strategy")
        travel_quest_speed_up_paper_hold: int = self.get_config("travel_quest_speed_up_paper_hold")
        travel_top_blue_event_remain_cnt: int = self.get_config("travel_top_blue_event_remain_cnt")
        travel_speed_up_target: Set[int] = set(self.get_config("travel_speed_up_target"))
        reward: List[InventoryInfo] = []

        def get_strategy(event_id: int) -> str:
            if event_id == 4007:
                self._log("遇到装备事件")
                return travel_quest_equip_event_strategy
            elif event_id == 4009:
                self._log("遇到代币事件")
                return travel_quest_gold_event_strategy
            else:
                raise ValueError(f"未知可选项事件{event_id}")

        top = await client.travel_top(max(db.get_open_travel_area()), 1)

        team_count = len(top.travel_quest_list)

        if team_count < 3:
            self._warn(f"正在探险的小队数为{team_count}<3，请上号开始新的探险！")

        if top.round_event_data:
            self._log("发现宝箱殿")
            round_event_data = top.round_event_data
            result = None
            round_id = round_event_data.round
            while round_event_data is not None:
                round_id = round_event_data.round
                select_door_id = 1
                if round_event_data.right_door_effect_id != 900000:
                    select_door_id = 2
                resp = await client.travel_result_round_event(round_event_data.round, select_door_id)
                reward.extend(resp.current_round_result.reward_list or [])
                round_event_data = resp.next_round_event_data
                result = resp.current_round_result.result

            if result == eRoundEventResultType.SUCCESS:
                self._log(f"通关宝箱殿，获得了{round_id}层宝箱")
            else:
                suffix = "但获得了该层宝箱" if result == eRoundEventResultType.END else "且未获得该层宝箱"
                self._log(f"止步于第{round_id}层，{suffix}")

        if top.top_event_list:
            blue_events = sorted([
                event for event in top.top_event_list if event.top_event_id in ManaTravelEventReward
                ], key=lambda x: ManaTravelEventReward[x.top_event_id]) 
            remain_blue_event_cnt = 0
            for top_event in top.top_event_list:
                try:
                    chooice = 0
                    if top_event.top_event_choice_flag:
                        strategy = get_strategy(top_event.top_event_id)
                        chooice = self.get_choice(strategy)
                    if top_event in blue_events and \
                    ManaTravelEventReward.get(top_event.top_event_id, eEventReward.Unknown) in ManaTravelEventRemain and \
                    blue_events.index(top_event) < travel_top_blue_event_remain_cnt:
                        remain_blue_event_cnt += 1
                    else:
                        result = await client.travel_receive_top_event_reward(top_event.top_event_appear_id, chooice)
                        reward.extend(result.reward_list)
                except Exception as e:
                    self._warn(f"处理特殊事件{top_event.top_event_id}失败:{e}")
            if remain_blue_event_cnt:
                self._log(f"保留{remain_blue_event_cnt}个蓝色事件")
            self._log(f"阅读{len(top.top_event_list) - remain_blue_event_cnt}个特殊事件")

        check_next = True
        result_count = {}
        while check_next:
            check_next = False
            if any(self.can_receive_count(quest, apiclient.time) for quest in top.travel_quest_list):
                result = await client.travel_receive_all()
                secret_travel: List[TravelAppearEventData] = []
                for quest in result.travel_result:
                    reward.extend(quest.reward_list)
                    for event in quest.appear_event_list or []:
                        reward.extend(event.reward_list)
                        secret_travel.append(event)

                result_count = Counter([quest.travel_quest_id for quest in result.travel_result])
                msg = '探索了' + ' '.join(f"{db.get_quest_name(quest)}{cnt}次" for quest, cnt in result_count.items())
                self._log(msg)
                if secret_travel:
                    msg = '触发了秘密探险：' + ' '.join(db.ex_event_data[event.still_id].title for event in secret_travel)
                    self._log(msg)

            if reward:
                self._log(f"获得了:")
                msg = (await client.serialize_reward_summary(reward)).strip('无')
                if msg: self._log(msg)
                self._log("")

            add_lap_travel_quest_list: List[TravelQuestAddLap] = []
            add_lap_travel_quest_id: List[int] = []
            start_travel_quest_list: List[TravelStartInfo] = []
            new_quest_list: List[TravelQuestInfo] = [] 
            for quest in top.travel_quest_list:
                quest.received_count += result_count.get(quest.travel_quest_id, 0)
                quest_still_round = self.quest_still_round(quest)
                if not quest_still_round: # restart
                    start_item = TravelStartInfo(
                            travel_quest_id = quest.travel_quest_id,
                            travel_deck = quest.travel_deck,
                            decrease_time_item = TravelDecreaseItem(jewel = 0, item = 0),
                            total_lap_count = client.data.settings.travel.travel_quest_max_repeat_count,
                     )
                    start_travel_quest_list.append(start_item)
                else:
                    append_round = client.data.settings.travel.travel_quest_max_repeat_count - quest_still_round
                    if append_round > 0:
                        add_item = TravelQuestAddLap(travel_id = quest.travel_id, add_lap_count = append_round)
                        add_lap_travel_quest_list.append(add_item)
                        add_lap_travel_quest_id.append(quest.travel_quest_id)
                    else:
                        new_quest_list.append(quest)

            if start_travel_quest_list or add_lap_travel_quest_list:
                msg = '\n'.join(f"继续派遣{db.get_quest_name(quest_id)} x{quest.add_lap_count}" for quest_id, quest in zip(add_lap_travel_quest_id, add_lap_travel_quest_list))
                self._log(msg)
                msg = '\n'.join(f"重新派遣{db.get_quest_name(quest.travel_quest_id)} x{quest.total_lap_count}" for quest in start_travel_quest_list)
                self._log(msg)
                action_type = eTravelStartType.ADD_LAP if add_lap_travel_quest_list else eTravelStartType.RESTART
                if start_travel_quest_list and add_lap_travel_quest_list:
                    action_type = eTravelStartType.RESTART_AND_ADD
                ret = await client.travel_start(start_travel_quest_list, add_lap_travel_quest_list, [], action_type)
                new_quest_list.extend(ret.travel_quest_list)

            total_use = max(
                min(
                    top.remain_daily_decrease_count_ticket,
                    client.data.get_inventory(db.travel_speed_up_paper)
                    - travel_quest_speed_up_paper_hold,
                ),
                0,
            )
            speed_up_quest = [quest for quest in new_quest_list if quest.travel_quest_id in travel_speed_up_target]
            team_count = len(speed_up_quest)
            if team_count and total_use: # avoid divide by zero
                self._log(f"可使用加速券{total_use}张")
                quest_use = [total_use // team_count + (1 if i < total_use % team_count else 0) for i in range(team_count)]
                speed_up_quest.sort(key=lambda x: self.quest_left_time(x, apiclient.time), reverse=True) # large left time first
                for quest, use in zip(speed_up_quest, quest_use):
                    time_left_use = int(math.ceil(self.quest_left_time(quest, apiclient.time) / client.data.settings.travel.decrease_time_by_ticket))
                    use = min(use, time_left_use)
                    if use:
                        self._log(f"{db.get_quest_name(quest.travel_quest_id)}使用加速券x{use}")
                        ret = await client.travel_decrease_time(quest.travel_quest_id, quest.travel_id, TravelDecreaseItem(jewel = 0, item = use))
                        top.remain_daily_decrease_count_ticket = ret.remain_daily_decrease_count_ticket
                        quest.decrease_time += use * client.data.settings.travel.decrease_time_by_ticket
                        check_next = True
            if check_next:
                top = await client.travel_top(max(db.get_open_travel_area()), 1)
                reward = []
                result_count.clear()

        if not self.log:
            raise SkipError("探险仍在继续...")

@inttype("travel_speed_up_paper_threshold", "加速阈值", 12, list(range(13)))
@inttype("travel_target_day", "轮转天数", 7, list(range(1, 31)))
@TravelQuestConfig("travel_target_quest3", "轮转目标3", [11002002, 11002003, 11002005])
@TravelQuestConfig("travel_target_quest2", "轮转目标2", [11002004])
@TravelQuestConfig("travel_target_quest1", "轮转目标1", [11002001])
@name('探险轮转')
@description('''
自动根据轮转进行探险，按轮转时间进行目标切换，需保持三支队探险。
切换时若一轮剩余时间小于阈值且可加速时则加速，否则直接撤退。
'''.strip())
@default(True)
class travel_round(Module):
    def is_finish_quest(self, quest: TravelQuestInfo, now: int) -> bool:
        return now >= quest.travel_end_time - quest.decrease_time

    def today_targets(self) -> List[int]:
        target_quest1: List[str] = self.get_config("travel_target_quest1")
        target_quest2: List[str] = self.get_config("travel_target_quest2")
        target_quest3: List[str] = self.get_config("travel_target_quest3")
        if not target_quest1 or not target_quest2 or not target_quest3:
            raise AbortError("三个轮转目标未全设置！")
        if set(target_quest1) & set(target_quest2) or set(target_quest1) & set(target_quest3) or set(target_quest2) & set(target_quest3):
            raise AbortError("三个轮转目标有重叠！请修改！")

        n = db.get_today_start_time().timetuple().tm_yday // int(self.get_config("travel_target_day"))
        def get_quest_id(lst: List, n): return lst[n % len(lst)]
        return [
            get_quest_id(target_quest1, n),
            get_quest_id(target_quest2, n),
            get_quest_id(target_quest3, n)
        ]
    async def do_task(self, client: pcrclient):
        top = await client.travel_top(max(db.get_open_travel_area()), 1)
        now_quest = {
            quest.travel_quest_id: quest for quest in top.travel_quest_list
        }
        if len(now_quest) != 3:
            raise AbortError(f"当前探险队数为{len(now_quest)}<3，不支持轮换！")

        travel_speed_up_paper_threshold = int(self.get_config("travel_speed_up_paper_threshold"))
        target_quest = set(self.today_targets())
        self._log(f"当前探险为{', '.join(db.get_quest_name(quest) for quest in now_quest)}")
        self._log(f"今日目标为{', '.join(db.get_quest_name(quest) for quest in target_quest)}")

        to_delete = {k: v for k, v in now_quest.items() if k not in target_quest}
        to_add = target_quest - set(now_quest.keys())

        start_infos = []
        reward = []
        for add_quest_id, (remove_quest_id, remove_quest) in zip(to_add, to_delete.items()):
            self._log(f"{db.get_quest_name(remove_quest_id)}->{db.get_quest_name(add_quest_id)}")
            quest_interval = (remove_quest.travel_end_time - remove_quest.travel_start_time) / remove_quest.total_lap_count
            next_loop = next(i for i in range(remove_quest.received_count, remove_quest.total_lap_count + 1) 
                             if i == remove_quest.total_lap_count 
                             or remove_quest.travel_start_time + i * quest_interval - remove_quest.decrease_time > apiclient.time)

            if next_loop < remove_quest.total_lap_count:
                delta_time = int(remove_quest.travel_start_time + next_loop * quest_interval - remove_quest.decrease_time - apiclient.time)
                ticket_to_use = int(math.ceil(delta_time / client.data.settings.travel.decrease_time_by_ticket))
                if ticket_to_use <= travel_speed_up_paper_threshold:
                    self._log(f"一轮剩余时间{db.format_second(delta_time)}小于使用阈值{travel_speed_up_paper_threshold}小时，加速一轮")
                    ticket_can_use = client.data.get_inventory(db.travel_speed_up_paper)
                    if ticket_to_use > ticket_can_use:
                        self._warn(f"已有加速券{ticket_can_use}<{ticket_to_use}，无法加速")
                        ticket_to_use = 0
                    if ticket_to_use > top.remain_daily_decrease_count_ticket:
                        self._warn(f"本日可使用加速券次数{top.remain_daily_decrease_count_ticket}<{ticket_to_use}，无法加速")
                        ticket_to_use = 0
                else:
                    ticket_to_use = 0
                    self._log(f"一轮剩余{db.format_second(delta_time)}大于阈值{travel_speed_up_paper_threshold}小时，直接撤退")

                if top.remain_daily_retire_count <= 0:
                    self._warn(f"本日已无撤退次数，无法{db.get_quest_name(remove_quest_id)}->{db.get_quest_name(add_quest_id)}")
                    continue

                if ticket_to_use:
                    self._log(f"{db.get_quest_name(remove_quest_id)}使用加速券x{ticket_to_use}")
                    ret = await client.travel_decrease_time(remove_quest.travel_quest_id, remove_quest.travel_id, TravelDecreaseItem(jewel = 0, item = ticket_to_use))
                    top.remain_daily_decrease_count_ticket = ret.remain_daily_decrease_count_ticket
                    remove_quest.decrease_time += ticket_to_use * client.data.settings.travel.decrease_time_by_ticket

            if self.is_finish_quest(remove_quest, apiclient.time):
                self._log(f"{db.get_quest_name(remove_quest_id)}完成")
                ret = await client.travel_receive(remove_quest.travel_id)
                for result in ret.travel_result:
                    reward.extend(result.reward_list)
            else:
                self._log(f"{db.get_quest_name(remove_quest_id)}撤退")
                ret = await client.travel_retire(remove_quest.travel_quest_id, remove_quest.travel_id)
                top.remain_daily_retire_count = ret.remain_daily_retire_count
                if ret.travel_result:
                    for result in ret.travel_result:
                        reward.extend(result.reward_list)

            start_infos.append(
                TravelStartInfo(
                    travel_quest_id = add_quest_id,
                    travel_deck = remove_quest.travel_deck,
                    decrease_time_item = TravelDecreaseItem(jewel = 0, item = 0),
                    total_lap_count = client.data.settings.travel.travel_quest_max_repeat_count
                )
            )

        if reward:
            self._log(f"获得了:")
            msg = (await client.serialize_reward_summary(reward))
            if msg: self._log(msg)
            self._log("")

        if start_infos:
            msg = '\n'.join(f"派遣{db.get_quest_name(quest.travel_quest_id)} x{quest.total_lap_count}" for quest in start_infos)
            self._log(msg)
            await client.travel_start(start_infos, [], [], eTravelStartType.NORMAL)


@name('计算探险编队')
@default(True)
@booltype('travel_team_view_go', '探险出发', False)
@TravelQuestConfig('travel_team_view_quest_id', '探险任务', [])
@booltype('travel_team_view_auto_memory', '自动设置记忆碎片', True)
@description('根据设定的记忆碎片优先级，从剩余可派遣角色中自动计算战力平衡编队，自动设置记忆碎片指记忆碎片优先度不足够派出队伍时，根据盈亏情况补充，探险出发指以计算出的编队出发')
class travel_team_view(Module):
    async def do_task(self, client: pcrclient):
        travel_team_auto_memory = self.get_config('travel_team_view_auto_memory')
        travel_team_go = self.get_config('travel_team_view_go')
        travel_quest_id: List[int] = self.get_config('travel_team_view_quest_id')
        top = await client.travel_top(max(db.get_open_travel_area()), 1)
        unit_list = top.priority_unit_list

        memory_gap = client.data.get_memory_demand_gap()
        if unit_list:
            memory_need = []
            for unit in unit_list:
                token = (eInventoryType.Item, db.unit_to_memory[unit])
                memory_need.append((token, memory_gap[token]))
            msg = '\n'.join([f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in memory_need])
            self._log(f"记忆碎片优先级的盈缺情况：\n{msg}")
            self._log("----")

        if top.travel_quest_list:
            self._log('当前派遣区域：')
            for quest in top.travel_quest_list:
                leave_time = int(quest.travel_end_time - quest.decrease_time - apiclient.time)
                self._log(f"{db.get_quest_name(quest.travel_quest_id)} -{db.format_second(leave_time)}")
                if quest.travel_quest_id in travel_quest_id: travel_quest_id.remove(quest.travel_quest_id)

        teams_go = client.data.settings.travel.travel_start_max_deck_count - len(top.travel_quest_list)
        if not teams_go:
            raise AbortError("已经派遣了3支队伍")
        if teams_go < len(travel_quest_id):
            raise AbortError(f"可派队伍数量{teams_go}<需派图数{travel_quest_id}")
        teams_go = len(travel_quest_id)

        memory_unit = 3 * teams_go

        forbid_unit = []
        for quest in top.travel_quest_list:
            forbid_unit.extend(quest.travel_deck)
        forbid_unit = set(forbid_unit)

        unit_list = [unit for unit in unit_list if unit not in forbid_unit][:memory_unit]
        if len(unit_list) != memory_unit:
            if not travel_team_auto_memory:
                raise AbortError(f"设置的未派遣的记忆碎片优先级的角色不足{memory_unit}个，请前往游戏里设置更多角色")
            else:
                leave = memory_unit - len(unit_list)
                new_unit = sorted(
                        [unit_id for unit_id in client.data.unit if unit_id not in unit_list and unit_id not in forbid_unit], 
                        key=lambda x: memory_gap[(eInventoryType.Item, db.unit_to_memory[x])], 
                        reverse=True)[:leave]
                msg = f"设置的未派遣的记忆碎片优先级的角色不足{memory_unit}个，将根据盈亏情况补充以下角色：\n"
                msg += ' '.join(f"{db.get_unit_name(unit)}" for unit in new_unit)
                self._log(msg)
                unit_list.extend(new_unit)
                await client.travel_update_priority_unit_list(unit_list)

        unit_power = {unit: client.data.get_unit_power(unit) for unit in client.data.unit}
        unit_list.sort(key=lambda x: unit_power[x], reverse=True)

        teams = [
            unit_list[st::3] for st in range(teams_go)
        ]

        start_power = [sum(unit_power[unit] for unit in teams[i]) for i in range(teams_go)]
        candidate_unit_id = sorted([unit_id for unit_id in unit_power if unit_id not in unit_list and unit_id not in forbid_unit], key=lambda x: unit_power[x], reverse=True)[:teams_go * 7]
        candidate_unit_power = [unit_power[unit] for unit in candidate_unit_id]

        lb = [db.travel_quest_data[quest].need_power for quest in travel_quest_id]
        ret, sol = dispatch_solver(start_power, candidate_unit_power, lb, 7)
        if not ret:
            raise AbortError(f"无法凑出战力满足最低要求的{teams_go}支队伍！")
        for pos, unit in zip(sol, candidate_unit_id):
            teams[pos].append(unit)

        teams_power = [sum(unit_power[unit] for unit in teams[i]) for i in range(teams_go)]

        for id, (team, power) in enumerate(zip(teams, teams_power), start=1):
            time = db.format_second(db.calc_travel_once_time(travel_quest_id[id - 1], power, client.data.settings.travel.over_power_decrease_time_coefficient))
            self._log(f"第{id}队({time})总战力{power}=" + '+'.join(f"{unit_power[unit]}" for unit in team))
            self._log(' '.join(f"{db.get_unit_name(unit)}" for unit in team))

        if travel_team_go:
            self._log('----')

            start_travel_quest_list: List[TravelStartInfo] = []
            for id, (team, quest) in enumerate(zip(teams, travel_quest_id), start = 1):
                start_item = TravelStartInfo(
                        travel_quest_id = quest,
                        travel_deck = team,
                        decrease_time_item = TravelDecreaseItem(jewel = 0, item = 0),
                        total_lap_count = client.data.settings.travel.travel_quest_max_repeat_count,
                 )
                start_travel_quest_list.append(start_item)

            action_type = eTravelStartType.NORMAL
            msg = '\n'.join(f"派遣第{id}队到{db.get_quest_name(quest.travel_quest_id)}x{quest.total_lap_count}" for id, quest in enumerate(start_travel_quest_list, start = 1))
            self._log(msg)
            await client.travel_start(start_travel_quest_list, [], [], action_type)
