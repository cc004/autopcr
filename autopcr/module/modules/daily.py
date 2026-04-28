from decimal import ROUND_HALF_UP, Decimal
from typing import List, Literal, Optional, Tuple

from ...model.common import InventoryInfo
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.questutils import *

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

_CN_SCALE: Tuple[Tuple[str, int], ...] = (('亿', 10 ** 8), ('万', 10 ** 4))
_EN_SCALE: Tuple[Tuple[str, int], ...] = (('b', 10 ** 9), ('m', 10 ** 6), ('k', 10 ** 3))


def _resolve_scale_unit(val: int, scale: Literal['k', 'm', 'b', '万', '亿']) -> Tuple[int, str]:
    ladder = _CN_SCALE if scale in ('万', '亿') else _EN_SCALE
    start = next(i for i, (s, _) in enumerate(ladder) if s == scale)
    av = abs(val)
    for i in range(start, len(ladder)):
        suf, div = ladder[i]
        if av >= div:
            return div, suf
    return 1, ''


def _round_scaled_quotient(quotient: Decimal, decimals: int) -> str:
    if decimals <= 0:
        n = quotient.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return str(int(n))
    step = Decimal('1').scaleb(-decimals)
    n = quotient.quantize(step, rounding=ROUND_HALF_UP)
    s = format(n, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def _group_int_string(int_part: str, use_grouping: bool) -> str:
    if not use_grouping or not int_part:
        return int_part
    sign = ''
    if int_part[0] == '-':
        sign = '-'
        int_part = int_part[1:]
    elif int_part[0] == '+':
        sign = '+'
        int_part = int_part[1:]
    rev = int_part[::-1]
    pieces = [rev[i:i + 3][::-1] for i in range(0, len(rev), 3)]
    return sign + ','.join(reversed(pieces))


def _apply_numeric_separator(num_str: str, mode: Literal['auto', 'no', 'yes'], original_val: int) -> str:
    if mode == 'no':
        use = False
    elif mode == 'yes':
        use = True
    else:
        use = abs(original_val) >= 100_000
    if '.' in num_str:
        a, b = num_str.split('.', 1)
        return _group_int_string(a, use) + '.' + b
    return _group_int_string(num_str, use)


def format_number(
    val: int,
    scale: Optional[Literal['k', 'm', 'b', '万', '亿']] = None,
    decimals: Optional[int] = None,
    separator: Literal['auto', 'no', 'yes'] = 'auto',
) -> str:
    if scale is None:
        s = str(int(val))
        return _apply_numeric_separator(s, separator, val)
    dec = 2 if decimals is None else decimals
    div, suffix = _resolve_scale_unit(val, scale)
    if not suffix:
        s = str(int(val))
        return _apply_numeric_separator(s, separator, val)
    q = Decimal(val) / Decimal(div)
    coeff = _round_scaled_quotient(q, dec)
    return _apply_numeric_separator(coeff, separator, val) + suffix


@description('展示基本信息，固定显示玩家名、体力、等级、钻石、母猪石、全角色战力，可自定义显示其他信息')
@name('基本信息')
@default(True)
@multichoice("user_info_display", "显示信息",
    ['心碎', '星幽碎片', '炼金点数', '香水'],
    ['玛娜', '心碎', '星球杯', '星幽碎片', '属性球', '大师碎片', '炼金点数', '香水', '扫荡券', '加速券', '大师币', '连结币'])
class user_info(Module):
    async def do_task(self, client: pcrclient):
        now = db.format_time(apiclient.datetime)
        display_items = set(self.get_config('user_info_display'))

        # 固定信息
        name = client.data.user_name
        level = client.data.team_level
        stamina = client.data.stamina
        max_stamina = db.team_info[client.data.team_level].max_stamina
        jewel = client.data.jewel.free_jewel + client.data.jewel.jewel
        pig = client.data.get_inventory((eInventoryType.Item, 90005))
        tot_power = sum([client.data.get_unit_power(unit) for unit in client.data.unit])

        # 可选信息
        optional_info = {}

        if '玛娜' in display_items:
            mana = client.data.gold.gold_id_free + client.data.gold.gold_id_pay
            optional_info['玛娜'] = format_number(mana, scale='亿', decimals=1, separator='no')

        if '心碎' in display_items:
            heart = client.data.get_inventory(db.heart)
            xinsui = client.data.get_inventory(db.xinsui)
            if heart > 0:
                optional_info['心碎'] = f"{format_number(xinsui)}(大心 {format_number(heart)})"
            else:
                optional_info['心碎'] = format_number(xinsui)

        if '星球杯' in display_items:
            star_cup = client.data.get_inventory(db.xingqiubei)
            optional_info['星球杯'] = format_number(star_cup)

        if '星幽碎片' in display_items:
            xinyou = client.data.get_inventory(db.xinyou)
            optional_info['星幽碎片'] = format_number(xinyou)

        if '属性球' in display_items:
            fire = client.data.get_inventory(db.fire_ball)
            water = client.data.get_inventory(db.water_ball)
            wind = client.data.get_inventory(db.wind_ball)
            sun = client.data.get_inventory(db.sun_ball)
            dark = client.data.get_inventory(db.dark_ball)
            optional_info['属性球'] = f"{format_number(fire)}/{format_number(water)}/{format_number(wind)}/{format_number(sun)}/{format_number(dark)}"

        if '大师碎片' in display_items:
            master = client.data.get_inventory(db.master_fragment)
            master_f = client.data.get_inventory(db.master_ffragment)
            if master_f > 0:
                optional_info['大师碎片'] = f"{master}(残片 {master_f})"
            else:
                optional_info['大师碎片'] = str(master)

        if '炼金点数' in display_items:
            alces_pt = client.data.get_inventory(db.ex_rainbow_enhance_pt)
            optional_info['炼金点数'] = format_number(alces_pt, scale='万', decimals=0, separator='no')

        if '香水' in display_items:
            perfume = client.data.get_inventory((eInventoryType.Item, 26203))
            optional_info['香水'] = str(perfume)

        if '扫荡券' in display_items:
            sweep_ticket = client.data.get_inventory((eInventoryType.Item, 23001))
            optional_info['扫荡券'] = format_number(sweep_ticket)

        if '加速券' in display_items:
            speed_ticket = client.data.get_inventory(db.travel_speed_up_paper)
            optional_info['加速券'] = str(speed_ticket)

        if '大师币' in display_items:
            master_coin = client.data.get_inventory((eInventoryType.Item, 90008))
            optional_info['大师币'] = format_number(master_coin, scale='万', decimals=1, separator='no')

        if '连结币' in display_items:
            link_coin = client.data.get_inventory((eInventoryType.Item, 99007))
            optional_info['连结币'] = str(link_coin)

        # 注释掉的琐碎物品（方便后续启用）
        # if 'EX装备币' in display_items:
        #     ex_weapon = client.data.get_inventory((eInventoryType.Item, 90009))
        #     ex_armor = client.data.get_inventory((eInventoryType.Item, 90010))
        #     ex_accessory = client.data.get_inventory((eInventoryType.Item, 90011))
        #     fmt_coin = lambda n: format_number(n, scale='万', decimals=2, separator='no')
        #     optional_info['EX装备币'] = f"{fmt_coin(ex_weapon)}/{fmt_coin(ex_armor)}/{fmt_coin(ex_accessory)}"

        # if '商店币' in display_items:
        #     dungeon_coin = client.data.get_inventory((eInventoryType.Item, 90002))
        #     arena_coin = client.data.get_inventory((eInventoryType.Item, 90003))
        #     grand_arena_coin = client.data.get_inventory((eInventoryType.Item, 90004))
        #     clan_coin = client.data.get_inventory((eInventoryType.Item, 90006))
        #     fmt_coin = lambda n: format_number(n, scale='万', decimals=2, separator='no')
        #     optional_info['商店币'] = f"{fmt_coin(dungeon_coin)}/{fmt_coin(arena_coin)}/{fmt_coin(grand_arena_coin)}/{fmt_coin(clan_coin)}"

        # if '原矿' in display_items:
        #     # 原矿 ID 范围通常是 35000-35999，按ID倒序
        #     ores = [(item_id, client.data.get_inventory((eInventoryType.Item, item_id)))
        #             for item_id in range(35999, 34999, -1)
        #             if client.data.get_inventory((eInventoryType.Item, item_id)) > 0]
        #     if ores:
        #         optional_info['原矿'] = '/'.join(str(cnt) for _, cnt in ores)

        # if '经验药剂' in display_items:
        #     # 经验药剂 ID: 20001-20004，按ID倒序
        #     exp_potions = [client.data.get_inventory((eInventoryType.Item, item_id))
        #                    for item_id in range(20004, 20000, -1)]
        #     optional_info['经验药剂'] = '/'.join(
        #         format_number(cnt, scale='万', decimals=2, separator='auto') for cnt in exp_potions)

        # if '精炼石' in display_items:
        #     # 精炼石 ID: 22001-22006，按ID倒序
        #     refine_stones = [client.data.get_inventory((eInventoryType.Item, item_id))
        #                      for item_id in range(22006, 22000, -1)]
        #     optional_info['精炼石'] = '/'.join(
        #         format_number(cnt, scale='万', decimals=2, separator='auto') for cnt in refine_stones)

        # if '好感礼物' in display_items:
        #     # 蛋糕类 ID: 50001-50003，按ID倒序
        #     cakes = [client.data.get_inventory((eInventoryType.Item, item_id))
        #              for item_id in range(50003, 50000, -1)]
        #     optional_info['好感礼物'] = '/'.join(
        #         format_number(cnt, scale='万', decimals=2, separator='auto') for cnt in cakes)

        # 输出格式
        if stamina >= max_stamina:
            self._warn(f"体力爆了！")

        # 第一行：固定信息
        self._log(f"{name} 体力{stamina}({max_stamina}) 等级{level} 钻石{format_number(jewel)}")

        # 第二行：可选信息（前两项）+ 母猪石（顺序与配置候选项一致，避免 set 迭代无序）
        line2_items = []
        keys = [k for k in _USER_INFO_DISPLAY_ORDER if k in optional_info]
        for i in range(min(2, len(keys))):
            line2_items.append(f"{keys[i]}{optional_info[keys[i]]}")
        line2_items.append(f"母猪石{format_number(pig)}")
        self._log(' '.join(line2_items))

        # 第三行及以后：每行3个属性
        remaining_keys = keys[2:]
        for i in range(0, len(remaining_keys), 3):
            line_items = []
            for j in range(3):
                if i + j < len(remaining_keys):
                    key = remaining_keys[i + j]
                    line_items.append(f"{key}{optional_info[key]}")
            self._log(' '.join(line_items))

        # 最后一行：全角色战力
        self._log(f"全角色战力：{format_number(tot_power)}")
        self._log(f"已氪体数：{client.data.recover_stamina_exec_count}")
        self._log(f"清日常时间：{now}")

