from typing import List

from ...model.common import InventoryInfo
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.questutils import *
from ...util.format_number import format_number

@description('仅开启时生效，氪体数将取满足条件的最大值，禅模式指不执行体力相关的功能，仅在清日常生效，单项执行将忽略。庆典包括其倍数，加速期间的所有倍数判断均x2')
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
class global_config(Module):
    async def do_task(self, client: pcrclient): # stamina TODO
        if client.is_cron_run():
            self._log("执行定时任务")

        stamina_check = [('sweep_recover_stamina_times_n4', 
                          lambda: client.data.is_normal_quest_campaign() and client.data.get_normal_quest_campaign_times() >= 4, "n4及以上"),
                         ('sweep_recover_stamina_times_n3',
                          lambda: client.data.is_normal_quest_campaign() and client.data.get_normal_quest_campaign_times() == 3, "n3"),
                         ('sweep_recover_stamina_times_h3',
                          lambda: client.data.is_hard_quest_campaign() and client.data.get_hard_quest_campaign_times() >= 3, "h3及以上"),
                         ('sweep_recover_stamina_times_vh3',
                          lambda: client.data.is_very_hard_quest_campaign() and client.data.get_very_hard_quest_campaign_times() >= 3, "vh3及以上"),
                         ('sweep_recover_stamina_times_n2',
                          lambda: client.data.is_normal_quest_campaign() and client.data.get_normal_quest_campaign_times() == 2, "n2"),
                         ('sweep_recover_stamina_times_h2',
                          lambda: client.data.is_hard_quest_campaign() and client.data.get_hard_quest_campaign_times() == 2, "h2"),
                         ('sweep_recover_stamina_times_vh2',
                          lambda: client.data.is_very_hard_quest_campaign() and client.data.get_very_hard_quest_campaign_times() == 2, "vh2"),
                         ('sweep_recover_stamina_times',
                          lambda: True, "")
        ]
        stamina_hit = [(self.get_config(key), desc) for key, check, desc in stamina_check if check()]
        today_recover_stamina = max([stamina for stamina, _ in stamina_hit], default=0)
        self._log(f"今日" + '，'.join([desc for _, desc in stamina_hit]) + f"氪体数{today_recover_stamina}")
        client.set_stamina_recover_cnt(today_recover_stamina)

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
        client.data.cf = None

class mission_receive(Module):
    async def do_task(self, client: pcrclient):
        missions = await client.mission_index()
        for type_id, condifion in zip([1, 2, 4], [db.is_daily_mission, db.is_stationary_mission, db.is_emblem_mission]): # 我也不知道为什么是1 2 4
            if any(1 for mission in missions.missions if condifion(mission.mission_id) and mission.mission_status == eMissionStatusType.EnableReceive) or any(1 for mission in missions.season_pack or [] if condifion(mission.mission_id) and not mission.received):
                resp = await client.mission_receive(type_id)
                reward = await client.serialize_reward_summary(resp.rewards)
                self._log("领取了任务奖励，获得了:\n" + reward)
        if not self.log:
            raise SkipError("没有可领取的任务奖励")

@description('开始时领取任务奖励')
@name("领取任务奖励1")
@default(True)
@tag_stamina_get
class mission_receive_first(mission_receive):
    pass

@description('结束时领取任务奖励')
@name("领取任务奖励2")
@default(True)
@tag_stamina_get
class mission_receive_last(mission_receive):
    pass

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
                reward = await client.serialize_reward_summary(resp.rewards)
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
                reward = await client.serialize_reward_summary(rewards)
                self._log(f"领取了女神祭奖励，获得了:\n{reward}")
            else:
                raise SkipError("没有可领取的女神祭奖励")

@ConditionalExecution3Config('present_receive_unlimit_stamina_strategy', "无限期体力", [], check = False)
@ConditionalExecution3Config('present_receive_limit_stamina_strategy', "有限期体力", ["n3", "n4及以上"], check = False)
@ConditionalExecution3Config('present_receive_one_day_limit_stamina_strategy', "一天到期体力", ["总是执行"], check = False)
@description('领取非体力的所有东西以及符合条件的体力')
@name('领取礼物箱')
@default(True)
@tag_stamina_get
class present_receive(Module):
    async def do_task(self, client: pcrclient):
        received = False
        result = []
        stop = False
        gets = []
        for conf in ['present_receive_unlimit_stamina_strategy', 'present_receive_limit_stamina_strategy', 'present_receive_one_day_limit_stamina_strategy']:
            config = self.get_config_instance(conf)
            get, msg = await config.do_check(client)
            gets.append(get)
            if get:
                self._log(msg + config.desc + "领取")
        unlimit_stamina_get, limit_stamina_get, one_day_limit_stamina_get = gets
        while not stop:
            is_exclude_stamina = False if unlimit_stamina_get and limit_stamina_get else True
            present_index = await client.present_index()
            for present in present_index.present_info_list:
                if not is_exclude_stamina or not (present.reward_type == eInventoryType.Stamina and present.reward_id == 93001):
                    res = await client.present_receive_all(is_exclude_stamina)
                    if not res.rewards:
                        if not is_exclude_stamina and any(present.reward_type == eInventoryType.Stamina and present.reward_id == 93001 for present in present_index.present_info_list):
                            self._warn("体力满了，无法领取礼物箱的体力")
                        if any(db.is_ex_equip((present.reward_type, present.reward_id)) for present in present_index.present_info_list):
                            self._warn("EX装备满了，无法领取礼物箱的EX装备")
                        if any((present.reward_type, present.reward_id) == db.dice for present in present_index.present_info_list):
                            self._warn("骰子满了，无法领取礼物箱的骰子")
                        stop = True
                    else:
                        result += res.rewards
                        received = True
                    break
            else:
                stop = True

        if unlimit_stamina_get or limit_stamina_get or one_day_limit_stamina_get:
            stop = False
            while not stop:
                present = await client.present_index()
                for present in present.present_info_list:
                    if present.reward_type == eInventoryType.Stamina and present.reward_id == 93001 \
                    and ((not present.reward_limit_flag and unlimit_stamina_get) or
                        (present.reward_limit_flag and limit_stamina_get) or
                        (present.reward_limit_flag and one_day_limit_stamina_get and present.reward_limit_time <= apiclient.time + 24 * 3600)):
                        res = await client.present_receive(present.present_id)
                        if not res.rewards:
                            self._warn("体力满了，无法继续领取礼物箱的体力")
                            stop = True
                            break
                        else:
                            result += res.rewards
                            stop = False
                else:
                    stop = True

        if not received:
            raise SkipError(f"不存在未领取礼物")
        msg = await client.serialize_reward_summary(result)
        self._log(f"领取了礼物箱，获得了:\n{msg}")

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

_USER_INFO_DISPLAY_ORDER = (
    '玛娜', '心碎', '星球杯', '星幽碎片', '属性球', '大师碎片', '炼金点数',
    '香水', '扫荡券', '加速券', '大师币', '连结币',
)

@description('展示基本信息，固定显示玩家名、体力、等级、钻石、母猪石、全角色战力，可自定义显示其他信息')
@name('基本信息')
@default(True)
@multichoice(
    "user_info_display", "显示信息",
    ['心碎', '星幽碎片', '炼金点数', '香水'],
    ['玛娜', '心碎', '星球杯', '星幽碎片', '属性球', '大师碎片', '炼金点数', '香水', '扫荡券', '加速券', '大师币', '连结币']
)
class user_info(Module):
    def _collect_optional_info(self, client: pcrclient, display_items: set[str]) -> dict[str, str]:
        data = client.data
        inv = data.get_inventory

        def fmt(n: int, **kwargs) -> str:
            return format_number(n, **kwargs)

        def fmt_heart() -> str:
            heart = inv(db.heart)
            xinsui = inv(db.xinsui)
            if heart > 0:
                return f"{fmt(xinsui)}(大心 {fmt(heart)})"
            return fmt(xinsui)

        def fmt_balls() -> str:
            items = [
                db.fire_ball,
                db.water_ball,
                db.wind_ball,
                db.sun_ball,
                db.dark_ball,
            ]
            return '/'.join(fmt(inv(item)) for item in items)

        def fmt_master_fragment() -> str:
            master = inv(db.master_fragment)
            master_f = inv(db.master_ffragment)
            if master_f > 0:
                return f"{master}(残片 {master_f})"
            return str(master)

        handlers = {
            '玛娜': lambda: fmt(
                data.gold.gold_id_free + data.gold.gold_id_pay,
                scale='亿',
                decimals=1,
                separator='no',
            ),
            '心碎': fmt_heart,
            '星球杯': lambda: fmt(inv(db.xingqiubei)),
            '星幽碎片': lambda: fmt(inv(db.xinyou)),
            '母猪石': lambda: fmt(inv((eInventoryType.Item, 90005))),
            '属性球': fmt_balls,
            '大师碎片': fmt_master_fragment,
            '炼金点数': lambda: fmt(
                inv(db.ex_rainbow_enhance_pt),
                scale='万',
                decimals=0,
                separator='no',
            ),
            '香水': lambda: str(inv(db.ex_rainbow_enhance_ball)),
            '扫荡券': lambda: fmt(inv((eInventoryType.Item, 23001))),
            '加速券': lambda: str(inv(db.travel_speed_up_paper)),
            '大师币': lambda: fmt(
                inv((eInventoryType.Item, 90008)),
                scale='万',
                decimals=1,
                separator='no',
            ),
            '连结币': lambda: str(inv((eInventoryType.Item, 90012))),
        }

        return {
            key: handlers[key]()
            for key in _USER_INFO_DISPLAY_ORDER
            if key in display_items and key in handlers
        }

    def _log_optional_info(self, optional_info: dict[str, str], pig: int) -> None:
        keys = [k for k in _USER_INFO_DISPLAY_ORDER if k in optional_info]

        line2_items = [
            f"{key}{optional_info[key]}"
            for key in keys[:2]
        ]
        line2_items.append(f"母猪石{format_number(pig)}")
        self._log(' '.join(line2_items))

        for i in range(2, len(keys), 3):
            line_items = [
                f"{key}{optional_info[key]}"
                for key in keys[i:i + 3]
            ]
            self._log(' '.join(line_items))

    async def do_task(self, client: pcrclient):
        data = client.data
        now = db.format_time(apiclient.datetime)
        display_items = set(self.get_config('user_info_display'))

        name = data.user_name
        level = data.team_level
        stamina = data.stamina
        max_stamina = db.team_info[level].max_stamina
        jewel = data.jewel.free_jewel + data.jewel.jewel
        pig = data.get_inventory((eInventoryType.Item, 90005))
        total_power = sum(data.get_unit_power(unit) for unit in data.unit)

        if stamina >= max_stamina:
            self._warn("体力爆了！")

        optional_info = self._collect_optional_info(client, display_items)

        self._log(
            f"{name} 体力{stamina}({max_stamina}) "
            f"等级{level} 钻石{format_number(jewel)}"
        )
        self._log_optional_info(optional_info, pig)

        self._log(f"全角色战力：{format_number(total_power)}")
        self._log(f"已氪体数：{data.recover_stamina_exec_count}")
        self._log(f"清日常时间：{now}")

