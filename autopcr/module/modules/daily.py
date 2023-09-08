from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
import datetime

@description('全局生效，优先级n4>n3>h3>n2>h2')
@name("全局配置")
@default(True)
@inttype('sweep_recover_stamina_times', "平时被动恢复体力数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_n2', "n2被动恢复体力数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_n3', "n3被动恢复体力数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_n4', "n4及以上被动恢复体力数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_h2', "h2被动恢复体力数", 0, [i for i in range(41)])
@inttype('sweep_recover_stamina_times_h3', "h3及以上被动恢复体力数", 0, [i for i in range(41)])
@multichoice("force_stop_heart_sweep", "强制不刷心碎庆典", [], ["n2", "n3", "n4及以上", "h2", "h3及以上"])
@multichoice("force_stop_star_cup_sweep", "强制不刷星球杯庆典", [], ["n2", "n3", "n4及以上", "h2", "h3及以上"])
@notrunnable
class global_config(Module):
    async def do_task(self, client: pcrclient):
        pass

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

@singlechoice("present_receive_strategy", "领取策略", "非体力", ["非体力", "全部"])
@description('领取符合条件的所有礼物箱奖励')
@name('领取礼物箱')
@default(True)
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

@description('展示基本信息')
@name('基本信息')
@default(True)
class user_info(Module):
    async def do_task(self, client: pcrclient):
        now = db.format_time(datetime.datetime.now())
        self._log(f"{client.data.name} 体力{client.data.stamina}({db.team_max_stamina[client.data.team_level].max_stamina}) 等级{client.data.team_level} 钻石{client.data.jewel.free_jewel} mana{client.data.gold.gold_id_free} 扫荡券{client.data.get_inventory((eInventoryType.Item, 23001))} 母猪石{client.data.get_inventory((eInventoryType.Item, 90005))}")
        self._log(f"已购买体力数：{client.data.recover_stamina_exec_count}")
        self._log(f"清日常时间:{now}")


