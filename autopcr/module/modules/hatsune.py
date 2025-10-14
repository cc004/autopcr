from typing import List, Set
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

@conditional_not_execution("hatsune_h_sweep_not_run_time", ["n3", "n4及以上"])
@multichoice("hatsune_h_sweep_quest", "扫荡关卡", [1,2,3,4,5], [1,2,3,4,5])
@ActiveHatsuneListConfig("hatsune_h_sweep_not_event", "不扫荡活动", [])
@description('')
@name('扫荡活动h本')
@default(False)
@tag_stamina_consume
class hatsune_h_sweep(Module):
    async def do_task(self, client: pcrclient):
        area: List[int] = self.get_config('hatsune_h_sweep_quest')
        not_sweep_hatsune_id: Set[int] = set(self.get_config('hatsune_h_sweep_not_event'))
        hard = 200
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
            event_name = db.event_name[event.event_id]
            self._log(f"{event.event_id}:{event_name}：")
            if event.event_id in not_sweep_hatsune_id:
                self._log(f"不扫荡h本")
                continue
            event_active = True
            await client.get_hatsune_top(event.event_id)
            await client.get_hatsune_quest_top(event.event_id)
            for i in area:
                quest_id = event.event_id * 1000 + hard + i
                try: 
                    times = 3 - client.data.hatsune_quest_dict[event.event_id][quest_id].daily_clear_count
                    await client.quest_skip_aware(quest_id, 3, False, True)
                    is_skip = False
                    self._log(f"{quest_id}: 扫荡{times}次")
                except SkipError as e:
                    self._log(f"{quest_id}: {str(e)}")
                except AbortError as e:
                    if not str(e).endswith("体力不足"):
                        is_abort = True
                    self._log(f"{quest_id}: {str(e)}")
                    break
                except Exception as e: 
                    is_error = True
                    self._log(f"{quest_id}: {str(e)}")
                    break
        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@name('扫荡活动vh本boss')
@default(True)
class hatsune_vhboss_sweep(Module):
    async def do_task(self, client: pcrclient):
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
            event_active = True
            event_name = db.event_name[event.event_id]
            self._log(f"{event.event_id}:{event_name}：")

            resp = await client.get_hatsune_top(event.event_id)
            ticket = resp.boss_ticket_info.stock

            vhboss_id = event.event_id * 100 + 3
            times = min(1, ticket // db.hatsune_boss[vhboss_id].use_ticket_num)

            boss_info = {boss.boss_id: boss for boss in resp.boss_battle_info}

            try: 
                if not boss_info[vhboss_id].is_unlocked:
                    raise AbortError(f"vh本boss未解锁")
                if not boss_info[vhboss_id].kill_num:
                    raise AbortError(f"vh本boss未首通")
                if boss_info[vhboss_id].daily_kill_count:
                    raise SkipError(f"今日vh本boss已扫荡")
                if times <= 0:
                    raise AbortError(f"当前{ticket}张，boss券不足")

                if boss_info[vhboss_id].oneblow_kill_count < db.hatsune_boss[vhboss_id].oneblow_count_of_skip_condition:
                    raise AbortError(f"vh本boss一刀击杀次数{boss_info[vhboss_id].oneblow_kill_count}<{db.hatsune_boss[vhboss_id].oneblow_count_of_skip_condition}，无法扫荡")
                resp = await client.hatsune_boss_skip(event.event_id, vhboss_id, times, ticket)
                is_skip = False
                self._log(f"当前{ticket}张，vh本boss扫荡{times}次")
            except SkipError as e:
                self._log(f"{str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{str(e)}")
            except Exception as e: 
                is_error = True
                self._log(f"{str(e)}")
        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@multichoice("hatsune_hboss_strategy", "扫荡策略", ["保留未来vh","保留sp"], ["保留未来vh","保留sp"])
@description('vh保留30，sp保留90，若无通关则会保留')
@name('扫荡活动h本boss')
@default(True)
class hatsune_hboss_sweep(Module):
    async def do_task(self, client: pcrclient):
        strategy: List[str] = self.get_config('hatsune_hboss_strategy')
        future_vh: bool = "保留未来vh" in strategy
        today_sp: bool = "保留sp" in strategy
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
            event_active = True
            event_name = db.event_name[event.event_id]
            self._log(f"{event.event_id}:{event_name}：")

            resp = await client.get_hatsune_top(event.event_id)
            ticket = resp.boss_ticket_info.stock

            hboss_id = event.event_id * 100 + 2
            spboss_id = event.event_id * 100 + 4
            times = ticket // db.hatsune_boss[hboss_id].use_ticket_num

            boss_info = {boss.boss_id: boss for boss in resp.boss_battle_info}

            try: 
                if not boss_info[hboss_id].is_unlocked:
                    raise AbortError(f"h本boss未解锁")
                if not boss_info[hboss_id].kill_num:
                    raise AbortError(f"h本boss未首通")
                if today_sp and not boss_info[spboss_id].kill_num:
                    self._log("sp未通关，保留90张")
                    times -= 3
                if future_vh:
                    left_day = (db.get_start_time(db.parse_time(event.end_time)) - db.get_today_start_time()).days
                    self._log(f"距离活动结束还有{left_day}天，保留{left_day * 30}张")
                    times -= left_day

                if times <= 0:
                    raise SkipError(f"当前{ticket}张，boss券不足")

                if boss_info[hboss_id].oneblow_kill_count < db.hatsune_boss[hboss_id].oneblow_count_of_skip_condition:
                    raise AbortError(f"h本boss一刀击杀次数{boss_info[hboss_id].oneblow_kill_count}<{db.hatsune_boss[hboss_id].oneblow_count_of_skip_condition}，无法扫荡")
                resp = await client.hatsune_boss_skip(event.event_id, hboss_id, times, ticket)
                is_skip = False
                self._log(f"当前{ticket}张，h本boss扫荡{times}次")
            except SkipError as e:
                self._log(f"{str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{str(e)}")
            except Exception as e: 
                is_error = True
                self._log(f"{str(e)}")
        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

# @singlechoice("hatsune_gacha_strategy", "兑换策略", "全部兑换", ["全部兑换"])
@description('自动兑换')
@name('讨伐证交换')
@default(True)
class hatsune_gacha_exchange(Module):
    async def do_task(self, client: pcrclient):
        # early_stop = False if self.get_config('hatsune_gacha_strategy') == "全部兑换" else True
        early_stop = False
        event_active = False

        for event in db.get_open_hatsune():
            event_active = True
            event_name = db.event_name[event.event_id]
            self._log(f"{event.event_id}:{event_name}：")

            res = (await client.get_hatsune_top(event.event_id))
            exchange_ticket_id = db.hatsune_item[event.event_id].gacha_ticket_id
            res = (await client.get_hatsune_gacha_index(event.event_id, event.event_id))
            box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
            ticket = client.data.get_inventory((eInventoryType.Item, exchange_ticket_id))
            while(True):
                if ticket == 0:
                    self._log(f"无讨伐证，停止交换")
                    break
                if res.event_gacha_info.gacha_step >= 6:
                    exchange_times = min(client.data.settings.loop_box_multi_gacha_count, ticket)
                    self._log(f"当前处于第六轮及以上，一键交换{exchange_times}次")
                    await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 1)
                    ticket -= exchange_times
                else:
                    target_done = len([item.reward_id for item in box_item.values() if item.reset_target and item.remain_inbox_count]) == 0
                    remain_cnt = sum(item.remain_inbox_count for item in box_item.values())
                    if remain_cnt == 0 or (target_done and res.event_gacha_info.gacha_step <= 2 and early_stop):
                        self._log(f"已达成重置条件，重置交换轮数")
                        res = await client.reset_hatsune_gacha(event.event_id, event.event_id)
                        box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
                        continue
                    exchange_times = min(100, ticket, remain_cnt)
                    self._log(f"当前处于第{res.event_gacha_info.gacha_step}轮，交换{exchange_times}次")
                    resp = await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 0)
                    ticket -= exchange_times
                    for item in resp.draw_result:
                        box_item[item.box_set_id].remain_inbox_count -= item.hit_reward_count
            self._log(f"已交换至" + (f"第{res.event_gacha_info.gacha_step}轮" if res.event_gacha_info.gacha_step < 6 else "第六轮及以上"))
            client.data.set_inventory((eInventoryType.Item, exchange_ticket_id), ticket)
            
        if not event_active:
            raise SkipError("当前无可进入的活动")

class hatsune_mission_accept_base(Module):
    async def do_task(self, client: pcrclient):
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
            event_active = True
            event_name = db.event_name[event.event_id]
            self._log(f"{event.event_id}:{event_name}：")

            await client.get_hatsune_top(event.event_id)
            resp = await client.hatsune_mission_index(event.event_id)
            types = set(x.mission_id // 10000000 - 5 for x in resp.missions if x.mission_status == eMissionStatusType.EnableReceive)
            try:
                if not types:
                    raise SkipError("没有可领取的任务奖励")
                else:
                    is_skip = False
                    for type in types:
                        res = await client.hatsune_mission_receive(event.event_id, type)
                        reward = await client.serialize_reward_summary(res.rewards)
                        self._log(f"领取了任务奖励，获得了:\n" + reward)
            except SkipError as e:
                self._log(f"{str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{str(e)}")
            except Exception as e:
                is_error = True
                self._log(f"{str(e)}")

        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@description('讨伐证兑换前领取奖励')
@name('领取活动任务奖励1')
@default(True)
class hatsune_mission_accept1(hatsune_mission_accept_base):
    pass

@description('讨伐证兑换后领取奖励')
@name('领取活动任务奖励2')
@default(True)
class hatsune_mission_accept2(hatsune_mission_accept_base):
    pass

@singlechoice("hatsune_normal_sweep_quest", "刷取图", 15, [5, 10, 15])
@ActiveHatsuneChoiceConfig("hatsune_normal_sweep_event", "刷取活动", "")
@description('剩余体力全部刷活动图')
@name('全刷活动普图')
@default(False)
@tag_stamina_consume
class all_in_hatsune(Module):
    async def do_task(self, client: pcrclient):
        quest = 0
        sweep_hatsune_id = self.get_config('hatsune_normal_sweep_event')

        for event in db.get_active_hatsune(): 
            if event.event_id != sweep_hatsune_id:
                continue

            quest = 1000 * event.event_id + 100 + int(self.get_config('hatsune_normal_sweep_quest'))

            await client.get_hatsune_top(event.event_id)
            await client.get_hatsune_quest_top(event.event_id)

            break

        if not quest: raise SkipError("当前无进行中的活动")
        
        event_name = db.event_name[sweep_hatsune_id]
        self._log(f"刷取{event_name}活动")

        count = 0
        while True:
            try:
                await client.quest_skip_aware(quest, 12)
                count += 12
            except SkipError as e:
                pass
            except AbortError as e:
                if not str(e).endswith("体力不足"):
                    self._log(f"{str(e)}")
                    raise AbortError("")
                break

        remain = client.data.stamina // db.quest_info[quest].stamina

        if remain: 
            await client.quest_skip_aware(quest, remain)
            count += remain

        if count:
            self._log(f"已刷{quest}图{count}次")
        else:
            raise SkipError("体力不足")

