from typing import List

from ...model.common import InventoryInfo
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.questutils import *
import asyncio
import datetime

@description('仅开启时生效，氪体数优先级n4>n3>h3>vh3>n2>h2>vh2，禅模式指不执行体力相关的功能，仅在清日常生效，单项执行将忽略。庆典包括其倍数')
@name("全局配置")
@default(True)
@inttype('sweep_recover_stamina_times', "平时氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_n2', "n2氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_n3', "n3氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_n4', "n4以上氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_h2', "h2氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_h3', "h3以上氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_vh2', "vh2氪体数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_vh3', "vh3以上氪体数", 0, [i for i in range(41)])
@conditional_not_execution("force_stop_heart_sweep", [], desc="不刷心碎庆典", check=False)
@conditional_not_execution("force_stop_star_cup_sweep", [], desc="不刷星球杯庆典", check=False)
@conditional_execution2('stamina_relative_not_run_campaign_before_one_day', [], desc='禅模式', check=False)
@notrunnable
class global_config(Module):
    async def do_task(self, client: pcrclient): # stamina TODO
        if client.is_cron_run():
            self._log("执行定时任务")

        stamina_check = [('sweep_recover_stamina_times_n4', 
                          lambda: client.data.is_normal_quest_campaign() and client.data.get_normal_quest_campaign_times() >= 4),
                         ('sweep_recover_stamina_times_n3',
                          lambda: client.data.is_normal_quest_campaign() and client.data.get_normal_quest_campaign_times() == 3),
                         ('sweep_recover_stamina_times_h3',
                          lambda: client.data.is_hard_quest_campaign() and client.data.get_hard_quest_campaign_times() >= 3),
                         ('sweep_recover_stamina_times_vh3',
                          lambda: client.data.is_very_hard_quest_campaign() and client.data.get_very_hard_quest_campaign_times() >= 3),
                         ('sweep_recover_stamina_times_n2',
                          lambda: client.data.is_normal_quest_campaign() and client.data.get_normal_quest_campaign_times() == 2),
                         ('sweep_recover_stamina_times_h2',
                          lambda: client.data.is_hard_quest_campaign() and client.data.get_hard_quest_campaign_times() == 2),
                         ('sweep_recover_stamina_times_vh2',
                          lambda: client.data.is_very_hard_quest_campaign() and client.data.get_very_hard_quest_campaign_times() == 2),
                         ('sweep_recover_stamina_times',
                          lambda: True)
        ]
        for key, check in stamina_check:
            if check():
                stamina: int = self.get_config(key)
                campaign = key.split('_')[-1]
                campaign = '无庆典' if campaign == 'times' else campaign
                client.set_stamina_recover_cnt(stamina)
                self._log(f"今日{campaign}，氪体数{stamina}")
                break

        force_stop_star_cup_sweep = self.get_config_instance('force_stop_star_cup_sweep')
        ok, msg = await force_stop_star_cup_sweep.do_check(client)
        if not ok:
            client.set_star_cup_sweep_not_run()
            self._log(msg + "星球杯扫荡")

        force_stop_heart_sweep = self.get_config_instance('force_stop_heart_sweep')
        ok, msg = await force_stop_heart_sweep.do_check(client)
        if not ok:
            client.set_heart_sweep_not_run()
            self._log(msg + "心碎扫荡")

        if client.is_stamina_get_not_run():
            self._log("体力获取不执行")
        elif client.is_stamina_consume_not_run():
            self._log("体力消耗不执行")
        else:
            stamina_relative_not_run_campaign_before_one_day = self.get_config_instance('stamina_relative_not_run_campaign_before_one_day')
            ok, msg = await stamina_relative_not_run_campaign_before_one_day.do_check()
            if ok:
                client.set_stamina_get_not_run()
                client.set_stamina_consume_not_run()
                self._log(msg + "禅模式")


@description('选谁其实排名都一样的')
@name("赛马")
@default(True)
class chara_fortune(Module):
    async def do_task(self, client: pcrclient):
        if not db.is_cf_time():
            raise SkipError("今日无赛马")
        if client.data.cf is None:
            raise SkipError("今日已赛马")
        res = await client.draw_chara_fortune()
        self._log(f"赛马第{client.data.cf.rank}名，获得了宝石x{res.reward_list[0].received}")

@description('开始时领取任务奖励')
@name("领取每日任务奖励1")
@default(True)
@tag_stamina_get
class mission_receive_first(Module):
    async def do_task(self, client: pcrclient):
        resp = await client.mission_index()
        for mission in resp.missions:
            if db.is_daily_mission(mission.mission_id) and mission.mission_status == eMissionStatusType.EnableReceive:
                resp = await client.mission_receive()
                reward = await client.serlize_reward(resp.rewards)
                self._log("领取了任务奖励，获得了:\n" + reward)
                return
        raise SkipError("没有可领取的任务奖励")

@description('结束时领取任务奖励')
@name("领取每日任务奖励2")
@default(True)
@tag_stamina_get
class mission_receive_last(Module):
    async def do_task(self, client: pcrclient):
        resp = await client.mission_index()
        for mission in resp.missions:
            if db.is_daily_mission(mission.mission_id) and mission.mission_status == eMissionStatusType.EnableReceive:
                resp = await client.mission_receive()
                reward = await client.serlize_reward(resp.rewards)
                self._log("领取了任务奖励，获得了:\n" + reward)
                return
        raise SkipError("没有可领取的任务奖励")

@description('')
@name("领取女神祭任务")
@default(True)
class seasonpass_accept(Module):
    async def do_task(self, client: pcrclient):
        seasonpasses = db.get_active_seasonpass()
        if not seasonpasses:
            raise SkipError("目前无进行中的女神祭")
        for seasonpass in seasonpasses: # it should be 1
            seasonpass_id = seasonpass.season_id 
            resp = await client.season_ticket_new_index(seasonpass_id)
            if any(mission.mission_status == eMissionStatusType.EnableReceive for mission in resp.missions):
                resp = await client.season_ticket_new_accept(seasonpass_id, 0)
                reward = await client.serlize_reward(resp.rewards)
                self._log(f"领取了女神祭任务，获得了{reward}")
                self._log(f"当前女神祭等级：{resp.seasonpass_level}")
            else:
                raise SkipError("没有可领取的女神祭任务")

@description('')
@booltype('seasonpass_reward_stamina_exclude', "不领取体力", True)
@name("领取女神祭奖励")
@default(True)
@tag_stamina_get
class seasonpass_reward(Module):

    class Reward:
        level: int
        status: List[int]

    def to_key(self, reward: int) -> Reward:
        level = reward // 10
        status = reward % 10
        ret = self.Reward()
        ret.level = level
        ret.status = [((status >> i) & 1) for i in range(3)]
        return ret

    async def do_task(self, client: pcrclient):
        receive_all = not self.get_config('seasonpass_reward_stamina_exclude')
        seasonpasses = db.get_open_seasonpass()
        if not seasonpasses:
            raise SkipError("目前无女神祭庆典")
        for seasonpass in seasonpasses: # it len should be 1
            seasonpass_id = seasonpass.season_id 
            resp = await client.season_ticket_new_index(seasonpass_id)
            VIP = resp.is_buy
            if VIP: self._log("拥有神秘请柬的骑士君")
            unreceive_reward = [self.to_key(reward) for reward in resp.received_rewards if reward != db.seasonpass_level_reward_full_sign(reward // 10, VIP)]
            rewards = []
            if unreceive_reward:
                if receive_all: 
                    resp = await client.season_ticket_new_reward(seasonpass_id, 0, 0)
                    rewards = resp.rewards
                else:
                    async def check_reward(reward: seasonpass_reward.Reward, full_reward: seasonpass_reward.Reward, reward_type: int, index: int) -> List[InventoryInfo]: 
                        if full_reward.status[index] and \
                        not reward.status[index] and \
                        not db.is_stamina_type(reward_type):
                            resp = await client.season_ticket_new_reward(seasonpass_id, reward.level, index)
                            return resp.rewards
                        else:
                            return []
                        

                    for reward in unreceive_reward:
                        rewards += await check_reward(reward, 
                                           self.to_key(db.seasonpass_level_reward_full_sign(reward.level, VIP)), 
                                           db.seasonpass_level_reward[reward.level].free_reward_type,
                                           0)
                        rewards += await check_reward(reward, 
                                           self.to_key(db.seasonpass_level_reward_full_sign(reward.level, VIP)), 
                                           db.seasonpass_level_reward[reward.level].charge_reward_type_1,
                                           1)
                        rewards += await check_reward(reward, 
                                           self.to_key(db.seasonpass_level_reward_full_sign(reward.level, VIP)), 
                                           db.seasonpass_level_reward[reward.level].charge_reward_type_2,
                                           2)
                        
            if rewards:
                reward = await client.serlize_reward(rewards)
                self._log(f"领取了女神祭奖励，获得了:\n{reward}")
            else:
                raise SkipError("没有可领取的女神祭奖励")

@singlechoice("present_receive_strategy", "领取策略", "非体力", ["非体力", "全部"])
@description('领取符合条件的所有礼物箱奖励')
@name('领取礼物箱')
@default(True)
@tag_stamina_get
class present_receive(Module):
    async def do_task(self, client: pcrclient):
        if self.get_config('present_receive_strategy') == "非体力":
            is_exclude_stamina = True
            op = "领取了非体力物品：\n"
        else:
            is_exclude_stamina = False
            op = "领取了所有物品：\n"
        received = False
        result = []
        stop = False
        while not stop:
            present = await client.present_index()
            for present in present.present_info_list:
                if not is_exclude_stamina or not (present.reward_type == eInventoryType.Stamina and present.reward_id == 93001):
                    print(present.reward_type, present.reward_id)
                    res = await client.present_receive_all(is_exclude_stamina)
                    if not res.rewards:
                        stop = True
                    else:
                        result += res.rewards
                        received = True
                    break
            else:
                stop = True

        if not received:
            raise SkipError(f"不存在未领取{'的非体力的' if is_exclude_stamina == True else '的'}礼物")
        msg = await client.serlize_reward(result)
        self._log(op + msg)


@description('领取jjc和pjjc的币')
@name('领取双场币')
@default(True)
class jjc_reward(Module):
    async def do_task(self, client: pcrclient):
        info = await client.get_arena_info()
        if info.reward_info.count:
            await client.receive_arena_reward()
        self._log(f"jjc币x{info.reward_info.count}")
        info = await client.get_grand_arena_info()
        if info.reward_info.count:
            await client.receive_grand_arena_reward()
        self._log(f"pjjc币x{info.reward_info.count}")

@description('仅进攻，不结算，会消耗次数')
@name('完成每日jjc任务')
@default(False)
class jjc_daily(Module):
    async def do_task(self, client: pcrclient):
        if client.data.is_empty_deck(ePartyType.ARENA):
            raise AbortError("未设置进攻队伍，请设置") # AUTO SET TODO

        info = await client.get_arena_info()
        if info.arena_info.battle_number != info.arena_info.max_battle_number:
            raise SkipError("今日jjc任务已完成")

        for _ in range(3):
            if info.search_opponent: break
            await asyncio.sleep(2)
            info = await client.get_arena_info()

        if not info.search_opponent:
            raise AbortError("无法搜到可攻击对手，请稍后再试")
        opponent = info.search_opponent[0]
        await client.arena_apply(opponent.viewer_id, opponent.rank)
        token = create_battle_start_token()
        await client.arena_start(token, opponent.viewer_id, info.arena_info.battle_number, 1)
        await client.logout()
        await asyncio.sleep(2)
        self._log(f"当前排名{info.arena_info.rank}，进攻第{opponent.rank}名的【{opponent.user_name}】")

@description('仅进攻，不结算，会消耗次数')
@name('完成每日pjjc任务')
@default(False)
class pjjc_daily(Module):
    async def do_task(self, client: pcrclient):
        if client.data.is_empty_deck(ePartyType.GRAND_ARENA_1) or \
        client.data.is_empty_deck(ePartyType.GRAND_ARENA_2) or \
        client.data.is_empty_deck(ePartyType.GRAND_ARENA_3):
            raise AbortError("未设置进攻队伍，请设置") # AUTO SET TODO

        info = await client.get_grand_arena_info()
        if info.grand_arena_info.battle_number != info.grand_arena_info.max_battle_number:
            raise SkipError("今日pjjc任务已完成")

        for _ in range(3):
            if info.search_opponent: break
            await asyncio.sleep(2)
            info = await client.get_grand_arena_info()

        if not info.search_opponent:
            raise AbortError("无法搜到可攻击对手，请稍后再试")
        opponent = info.search_opponent[0]
        await client.grand_arena_apply(opponent.viewer_id, opponent.rank)
        token = create_battle_start_token()
        await client.grand_arena_start(token, opponent.viewer_id, info.grand_arena_info.battle_number, 1)
        await client.logout()
        await asyncio.sleep(2)
        self._log(f"当前排名{info.grand_arena_info.rank}，进攻第{opponent.rank}名的【{opponent.user_name}】")

@description('展示基本信息')
@name('基本信息')
@default(True)
class user_info(Module):
    async def do_task(self, client: pcrclient):
        now = db.format_time(datetime.datetime.now())
        name = client.data.name
        level = client.data.team_level
        stamina = client.data.stamina
        max_stamina = db.team_info[client.data.team_level].max_stamina
        jewel = client.data.jewel.free_jewel
        mana = client.data.gold.gold_id_free
        sweep_ticket = client.data.get_inventory((eInventoryType.Item, 23001))
        pig = client.data.get_inventory((eInventoryType.Item, 90005))
        tot_power = sum([client.data.get_unit_power(unit) for unit in client.data.unit])

        if stamina >= max_stamina:
            self._warn(f"体力爆了！")
        self._log(f"{name} 体力{stamina}({max_stamina}) 等级{level} 钻石{jewel}")
        self._log(f"玛那{mana} 扫荡券{sweep_ticket} 母猪石{pig}")
        self._log(f"全角色战力：{tot_power}")
        self._log(f"已氪体数：{client.data.recover_stamina_exec_count}")
        self._log(f"清日常时间：{now}")

