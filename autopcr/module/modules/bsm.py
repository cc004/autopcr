import asyncio
import uuid
import time
from typing import List
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import ApiException
from ...model.error import *
from ...model.common import InventoryInfo
from ...model.enums import eMissionStatusType

def generate_token() -> str:
    """生成16位随机token"""
    return uuid.uuid4().hex[:16]

@description('自动完成战车小游戏，每赢5次领取一次奖励')
@name("战车小游戏")
@default(False)
@inttype('run_times', "运行次数", 1, [i for i in range(1, 201)])
class bsm_auto(Module):
    async def do_task(self, client: pcrclient):
        target_runs = self.get_config('run_times')
        self._log(f"目标: {target_runs}轮 (每轮=赢5场+领奖励)")
        start_time = time.time()

        # 警告：大量次数可能被服务器限流
        if target_runs > 100:
            self._log(f"警告: 次数较多({target_runs})，建议先测试100次确认正常")

        # BSM 活动 ID
        event_id = 10156

        # 先进入活动页面
        try:
            await client.get_hatsune_top(event_id)
        except Exception as e:
            self._log(f"进入活动页面失败: {e}")
            return

        # 获取BSM活动信息
        try:
            top = await client.bsm_top()
        except Exception as e:
            self._log(f"获取BSM信息失败: {e}")
            return

        if not top or top.battle_point is None:
            self._log("活动未开启")
            return

        initial_point = top.battle_point
        current_point = initial_point
        machine_id = top.machines[0].machine_id if top.machines else 1

        self._log(f"初始积分: {initial_point}, 机器: {machine_id}")

        # 先领取已有奖励
        if top.missions:
            for mission in top.missions:
                if mission.mission_status == eMissionStatusType.EnableReceive:
                    try:
                        reward = await client.bsm_mission_accept(mission.mission_id)
                        self._log(f"领取奖励: {len(reward.rewards) if reward.rewards else 0} 个物品")
                    except:
                        pass

        completed_runs = 0
        total_wins = 0
        consecutive_fails = 0
        report_interval = 50 if target_runs > 100 else 10  # 大次数时减少日志

        while completed_runs < target_runs:
            # 每50轮刷新一次活动页面，防止会话过期
            if completed_runs > 0 and completed_runs % 50 == 0:
                try:
                    await client.get_hatsune_top(event_id)
                    top = await client.bsm_top()
                    if top:
                        current_point = top.battle_point
                except Exception as e:
                    self._log(f"刷新会话失败: {e}")
                    return

            # 每轮报告进度
            if completed_runs > 0 and completed_runs % report_interval == 0:
                self._log(f"进度: {completed_runs}/{target_runs} 轮, 积分: {current_point} (+{current_point - initial_point})")

            # 赢5场
            wins_this_round = 0
            attempts = 0
            max_attempts = 20  # 每轮最多尝试20次，防止无限循环

            while wins_this_round < 5 and attempts < max_attempts:
                attempts += 1

                # 准备对手
                try:
                    prepare = await client.bsm_rival_battle_prepare()
                    if not prepare.npcs:
                        continue
                except:
                    consecutive_fails += 1
                    if consecutive_fails >= 5:
                        self._log(f"连续失败5次，停止。当前积分: {current_point}")
                        return
                    await asyncio.sleep(1)
                    continue

                # 生成token并对战
                token = generate_token()
                try:
                    await client.bsm_battle_start(type=21, enemy_viewer_id=0, machine_id=machine_id, token=token)
                    await asyncio.sleep(0.1)  # start和finish之间小延迟
                    await client.bsm_battle_finish(battle_result=3, token=token)
                except Exception as e:
                    consecutive_fails += 1
                    if '限流' in str(e) or '频繁' in str(e) or 'too many' in str(e).lower():
                        self._log(f"触发服务器限流，暂停5秒...")
                        await asyncio.sleep(5)
                    continue

                # 检查积分变化（每5场检查一次，减少请求）
                should_check = (wins_this_round % 5 == 4) or (wins_this_round == 0 and attempts > 1)
                if should_check:
                    try:
                        top = await client.bsm_top()
                        new_point = top.battle_point if top else current_point
                        if new_point > current_point:
                            wins_this_round += 1
                            total_wins += 1
                            consecutive_fails = 0
                            current_point = new_point
                            self._log(f"  确认胜利，当前积分: {current_point}")
                        else:
                            consecutive_fails += 1
                            self._log(f"  积分未增加，可能失败")
                    except Exception as e:
                        consecutive_fails += 1
                        self._log(f"  查询积分失败: {e}")
                else:
                    # 不检查时假设成功，减少请求
                    wins_this_round += 1
                    total_wins += 1
                    consecutive_fails = 0

                # 大量请求时延迟
                if total_wins % 20 == 0:
                    await asyncio.sleep(0.3)

            if wins_this_round < 5:
                self._log(f"警告: 第{completed_runs+1}轮只赢了{wins_this_round}场")

            # 刷新并领取奖励
            try:
                top = await client.bsm_top()
                if top and top.missions:
                    for mission in top.missions:
                        if mission.mission_status == eMissionStatusType.EnableReceive:
                            try:
                                await client.bsm_mission_accept(mission.mission_id)
                            except:
                                pass
                if top:
                    current_point = top.battle_point
            except:
                pass

            completed_runs += 1

            # 每100轮后暂停一段时间，模拟正常玩家行为
            if completed_runs % 100 == 0:
                self._log(f"已完成{completed_runs}轮，暂停3秒...")
                await asyncio.sleep(3)

        # 最终报告
        elapsed = time.time() - start_time
        self._log(f"完成! {completed_runs}轮, 总胜场{total_wins}, 耗时{elapsed:.1f}秒")
        self._log(f"积分: {initial_point} -> {current_point} (+{current_point - initial_point})")
