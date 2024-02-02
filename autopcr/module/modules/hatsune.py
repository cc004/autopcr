from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

@conditional_not_execution("hatsune_h_sweep_not_run_time", ["n3", "n4及以上"])
@multichoice("hatsune_h_sweep_quest", "扫荡关卡", [1,2,3,4,5], [1,2,3,4,5])
@description('')
@name('扫荡活动h本')
@default(False)
class hatsune_h_sweep(Module):
    async def do_task(self, client: pcrclient):
        area = self.get_config('hatsune_h_sweep_quest')
        hard = 200
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
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

@singlechoice("hatsune_hboss_strategy", "扫荡策略", "保留当日vh份", ["保留当日vh份", "保留当日及未来vh份"])
@description('未打今日vh保留30+未打sp保留90')
@name('自动扫荡活动h本boss')
@default("none")
class hatsune_hboss_sweep(Module):
    async def do_task(self, client: pcrclient):
        is_error = False
        is_abort = False
        is_skip = True
        event_active = False
        for event in db.get_active_hatsune():
            event_active = True
            resp = await client.get_hatsune_top(event.event_id)
            ticket = resp.boss_ticket_info.stock
            event_name = db.event_name[event.event_id]

            times = ticket // 30
            hboss_id = event.event_id * 100 + 2
            vhboss_id = event.event_id * 100 + 3
            spboss_id = event.event_id * 100 + 4

            boss_info = {boss.boss_id: boss for boss in resp.boss_battle_info}

            try: 
                if not boss_info[hboss_id].is_unlocked:
                    raise AbortError(f"h本boss未解锁")
                if not boss_info[hboss_id].kill_num:
                    raise AbortError(f"h本boss未首通")
                if not boss_info[spboss_id].kill_num:
                    self._log("sp未通关，保留90张")
                    times -= 3
                if not boss_info[vhboss_id].daily_kill_count:
                    self._log("今日vh未通关，保留30张")
                    times -= 1
                if self.get_config('hatsune_hboss_strategy') == "保留当日及未来vh份":
                    left_day = (db.get_start_time(db.parse_time(event.end_time)) - db.get_today_start_time()).days 
                    self._log(f"距离活动结束还有{left_day}天，保留{left_day * 30}张")
                    times -= left_day

                if times <= 0:
                    raise SkipError(f"boss券不足")
                resp = await client.hatsune_boss_skip(event.event_id, hboss_id, times, ticket)
                is_skip = False
                self._log(f"{event_name} h boss: 扫荡{times}次")
            except SkipError as e:
                self._log(f"{event_name}: {str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{event_name}: {str(e)}")
            except Exception as e: 
                is_error = True
                self._log(f"{event_name}: {str(e)}")
        if not event_active: raise SkipError("当前无进行中的活动")
        if is_error: raise ValueError("")
        if is_abort: raise AbortError("")
        if is_skip: raise SkipError("")

@singlechoice("hatsune_gacha_strategy", "兑换策略", "全部兑换", ["前两轮尽早重置", "全部兑换"])
@description('自动兑换，前两轮兑换处目标物品可选择重置')
@name('讨伐证交换')
@default(True)
class hatsune_gacha_exchange(Module):
    async def do_task(self, client: pcrclient):
        early_stop = False if self.get_config('hatsune_gacha_strategy') == "全部兑换" else True
        event_active = False

        for event in db.get_open_hatsune():
            event_active = True
            event_name = db.event_name[event.event_id]
            res = (await client.get_hatsune_top(event.event_id))
            exchange_ticket_id = db.hatsune_item[event.event_id].gacha_ticket_id
            res = (await client.get_hatsune_gacha_index(event.event_id, event.event_id))
            box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
            ticket = client.data.get_inventory((eInventoryType.Item, exchange_ticket_id))
            while(True):
                if ticket == 0:
                    self._log(f"{event_name}: 无讨伐证，停止交换")
                    break
                if res.event_gacha_info.gacha_step >= 6:
                    exchange_times = min(client.data.settings.loop_box_multi_gacha_count, ticket)
                    self._log(f"{event_name}: 当前处于第六轮及以上，一键交换{exchange_times}次")
                    await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 1)
                    ticket -= exchange_times
                else:
                    target_done = len([item.reward_id for item in box_item.values() if item.reset_target and item.remain_inbox_count]) == 0
                    remain_cnt = sum(item.remain_inbox_count for item in box_item.values())
                    if remain_cnt == 0 or (target_done and res.event_gacha_info.gacha_step <= 2 and early_stop):
                        self._log(f"{event_name}: 已达成重置条件，重置交换轮数")
                        res = await client.reset_hatsune_gacha(event.event_id, event.event_id)
                        box_item = {item.box_set_id: item for item in res.event_gacha_info.box_set_list}
                        continue
                    exchange_times = min(100, ticket, remain_cnt)
                    self._log(f"{event_name}: 当前处于第{res.event_gacha_info.gacha_step}轮，交换{exchange_times}次")
                    resp = await client.exec_hatsune_gacha(event.event_id, event.event_id, exchange_times, ticket, 0)
                    ticket -= exchange_times
                    for item in resp.draw_result:
                        box_item[item.box_set_id].remain_inbox_count -= item.hit_reward_count
            self._log(f"{event_name}: 已交换至" + (f"第{res.event_gacha_info.gacha_step}轮" if res.event_gacha_info.gacha_step < 6 else "第六轮及以上"))
            
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
                        reward = await client.serlize_reward(res.rewards)
                        self._log(f"{event_name}: 领取了任务奖励，获得了:\n" + reward)
            except SkipError as e:
                self._log(f"{event_name}: {str(e)}")
            except AbortError as e:
                is_abort = True
                self._log(f"{event_name}: {str(e)}")
            except Exception as e:
                is_error = True
                self._log(f"{event_name}: {str(e)}")

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
@description('剩余体力全部刷活动图')
@name('全刷活动普图')
@default(False)
class all_in_hatsune(Module):
    async def do_task(self, client: pcrclient):
        quest = 0
        for event in db.get_active_hatsune(): # 复刻和正常一起开的话会刷先开的那个
            quest = 1000 * event.event_id + 100 + self.get_config('hatsune_normal_sweep_quest')
            
            await client.get_hatsune_top(event.event_id)
            await client.get_hatsune_quest_top(event.event_id)

            break
        
        if not quest: raise SkipError("当前无进行中的活动")
        

        count = client.data.stamina // db.quest_info[quest].stamina

        if count == 0: raise AbortError("体力不足")
        await client.quest_skip_aware(quest, count)
        self._log(f"已刷{quest}图{count}次")

