import asyncio
import os
from itertools import combinations
from io import BytesIO
from typing import List, Optional, Tuple

from PIL import Image

from hoshino import Service, priv

# Initialize the core package before importing db; database imports apiclient
# during module setup and otherwise enters a core <-> db initialization cycle.
from .autopcr.core import apiclient as _apiclient
from .autopcr.db.database import db
from .autopcr.jjc_server.jjc import (
    JJCHotTeam,
    JJCRecord,
    eJJCStatus,
    format_matrix_text,
    format_pjjc_blind_groups_text,
    format_team_name,
    instance as jjc_server,
)
from .autopcr.util import aiorequests
from .autopcr.util.draw import instance as drawer
from .autopcr.util.draw_table import outp_b64
from .autopcr.util.roster import roster
from .server import BotEvent, wrap_hoshino_event

jjc_server.configure_simulator(
    os.getenv("AUTOPCR_JJC_SIMULATOR_URL", "http://localhost:8080")
)

prefix = '#'
BLIND_MAX_DEFEND_TEAMS = 8

sv_help = f"""
- {prefix}jjc模拟 角色1 角色2 vs 角色A 角色B
- {prefix}jjc建议 角色1 角色2 角色3 ...
- {prefix}jjc盲打 角色1 角色2 ...（每5个角色一队）
- {prefix}jjc矩阵 角色... vs 角色...（左右各每5个角色一队）
- {prefix}pjjc盲打 角色1 角色2 ...（每5个角色一队，至少3队）
- {prefix}jjc热门防守
- {prefix}jjc热门进攻
- {prefix}pjjc热门防守
- {prefix}pjjc热门进攻
""".strip()

sv = Service(
    name="jjc模拟",
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=False,  # False隐藏
    enable_on_default=False,  # 是否默认启用
    bundle='pcr工具',  # 属于哪一类
    help_=sv_help  # 帮助文本
)

async def _parse_defend_teams(
    botev: BotEvent,
) -> List[List[int]]:
    """Resolve defend teams from either images or plain text."""
    defends: List[List[int]] = []
    img_urls = await botev.image()
    if img_urls:
        from .autopcr.util.unit_recognizer import instance as unit_recognizer

        for idx, img_url in enumerate(img_urls):
            try:
                response = await aiorequests.get(img_url, timeout=30)
                response.raise_for_status()
                image = Image.open(BytesIO(await response.content))
            except Exception as e:
                await botev.send(f"图片{idx+1}下载失败: {e}")
                continue
            try:
                box, summary = await unit_recognizer.recognize(image)
            finally:
                image.close()
            await botev.send(f"图片{idx+1}识别结果: {summary}")
            if not box:
                await botev.finish(f"图片{idx+1}未识别到任何队伍！")
            defends += box
    else:
        msg = ''.join(await botev.message())
        enemy_ids, unknown_units = roster.parse_team(msg)

        if unknown_units:
            await botev.finish(f"未知昵称{unknown_units}")

        defends = [enemy_ids[i:i+5] for i in range(0, len(enemy_ids), 5)]

    if not defends:
        await botev.finish("未识别到任何队伍！")

    return [[unit_id if unit_id > 100000 else unit_id * 100 + 1 for unit_id in defend] for defend in defends]

async def _format_pjjc_candidates(candidate: List[List[JJCRecord]], limit: int = 5) -> Tuple[List[str], Optional[Image.Image]]:
    """Convert already-ranked PJJC recommendation groups to Bot output."""
    top = candidate[:limit]
    if not top:
        return [], None
    formatted = []
    for result_tuple in top:
        desc_parts = [res.description(include_attack=True, include_defend=False) for res in result_tuple]
        formatted.append("\n".join(desc_parts))

    img = await drawer.draw_pjjc_suggestion(top)
    return formatted, img


def _format_hot_teams(title: str, teams: List[JJCHotTeam], limit: int = 8) -> str:
    if not teams:
        return f"{title}\n暂无数据"
    lines = [title]
    for idx, item in enumerate(teams[:limit], 1):
        lines.append(f"{idx}. ({item.count}次) {format_team_name(item.team)}")
    return '\n'.join(lines)


def _build_pjjc_hot_combinations(teams: List[JJCHotTeam], limit: int = 8) -> List[Tuple[int, Tuple[JJCHotTeam, JJCHotTeam, JJCHotTeam]]]:
    candidates: List[Tuple[int, Tuple[JJCHotTeam, JJCHotTeam, JJCHotTeam]]] = []
    for combo in combinations(teams, 3):
        team_a, team_b, team_c = combo
        units = set(team_a.team)
        if units & set(team_b.team):
            continue
        units |= set(team_b.team)
        if units & set(team_c.team):
            continue
        score = team_a.count + team_b.count + team_c.count
        candidates.append((score, combo))

    candidates.sort(
        key=lambda item: (
            -item[0],
            -item[1][0].count,
            -item[1][1].count,
            -item[1][2].count,
        )
    )
    return candidates[:limit]


def _format_pjjc_hot_combinations(title: str, combos: List[Tuple[int, Tuple[JJCHotTeam, JJCHotTeam, JJCHotTeam]]]) -> str:
    if not combos:
        return f"{title}\n暂无可用组合"
    lines = [title]
    for idx, (score, combo) in enumerate(combos, 1):
        lines.append(f"{idx}. 总查询{score}次")
        for i, item in enumerate(combo, 1):
            lines.append(f"  {i}队({item.count}次): {format_team_name(item.team)}")
    return '\n'.join(lines)

@sv.on_fullmatch(f"{prefix}jjc热门防守")
@wrap_hoshino_event
async def jjc_hot_defend(botev: BotEvent):
    teams = await jjc_server.get_hot_defend_teams(days=7, limit=8)
    await botev.send(_format_hot_teams("近7天JJC热门防守 Top 8", teams, limit=8))


@sv.on_fullmatch(f"{prefix}jjc热门进攻")
@wrap_hoshino_event
async def jjc_hot_attack(botev: BotEvent):
    teams = await jjc_server.get_hot_attack_teams(days=7, limit=8)
    await botev.send(_format_hot_teams("近7天JJC热门进攻 Top 8", teams, limit=8))


@sv.on_fullmatch(f"{prefix}pjjc热门防守")
@wrap_hoshino_event
async def pjjc_hot_defend(botev: BotEvent):
    teams = await jjc_server.get_hot_defend_teams(days=7, limit=32)
    combos = _build_pjjc_hot_combinations(teams, limit=8)
    await botev.send(_format_pjjc_hot_combinations("近7天PJJC热门防守组合 Top 8", combos))


@sv.on_fullmatch(f"{prefix}pjjc热门进攻")
@wrap_hoshino_event
async def pjjc_hot_attack(botev: BotEvent):
    teams = await jjc_server.get_hot_attack_teams(days=7, limit=32)
    combos = _build_pjjc_hot_combinations(teams, limit=8)
    await botev.send(_format_pjjc_hot_combinations("近7天PJJC热门进攻组合 Top 8", combos))


@sv.on_prefix(f"{prefix}jjc盲打")
@wrap_hoshino_event
async def jjc_blind_fight(botev: BotEvent):
    defends = await _parse_defend_teams(botev)
    attacks = await asyncio.gather(*[
        jjc_server.pick_confidence_attack_team(defend)
        for defend in defends
    ])
    teams = await jjc_server.get_hot_attack_teams(days=7, limit=8)
    attacks.append([t.team for t in teams])
    if attacks or teams:
        await botev.send(f"防守方「" + '\n'.join(format_team_name(deck) for deck in defends) + f"」\n根据历史数据分析，筛选了{'+'.join([str(len(team)) for team in attacks])}支进攻队伍，正在组合中...")
    attacks = [list(team) for team in dict.fromkeys(tuple(team) for teams in attacks for team in teams)]
    if not attacks:
        await botev.finish("未筛到可用的进攻队伍")

    result = await jjc_server.build_jjc_matrix(
        attacks=attacks,
        defends=defends,
    )

    result = result.truncate(8)

    msg = format_matrix_text(
        results=result,
    )
    await botev.send(msg)
    matrix_img = await drawer.draw_jjc_blind_matrix(
        result=result
    )
    await botev.send(outp_b64(matrix_img))


@sv.on_prefix(f"{prefix}jjc矩阵")
@wrap_hoshino_event
async def jjc_direct_matrix(botev: BotEvent):
    msg = ''.join(await botev.message()).split('vs')
    if len(msg) != 2:
        await botev.finish("请指定双方角色，格式如：角色1 角色2 vs 角色A 角色B")
    attacks, unknown_units = roster.parse_team(msg[0])
    defends, unknown_units_enemy = roster.parse_team(msg[1])

    attacks = [attacks[i:i+5] for i in range(0, len(attacks), 5)]
    defends = [defends[i:i+5] for i in range(0, len(defends), 5)]

    unknown_units += unknown_units_enemy
    if unknown_units:
        await botev.finish(f"未知昵称{unknown_units}")

    if not attacks or not defends:
        await botev.finish("请指定双方角色，格式如：角色1 角色2 vs 角色A 角色B")

    if len(attacks) > BLIND_MAX_DEFEND_TEAMS or len(defends) > BLIND_MAX_DEFEND_TEAMS:
        await botev.finish(f"jjc矩阵进攻和防守阵容数量都不能超过{BLIND_MAX_DEFEND_TEAMS}队")
    pair_count = len(attacks) * len(defends)
    await botev.send(
        f"识别到进攻{len(attacks)}队、防守{len(defends)}队，开始计算矩阵，共{pair_count}组对阵..."
    )
    result = await jjc_server.build_jjc_matrix(
        attacks=attacks,
        defends=defends,
    )
    msg = format_matrix_text(
        results=result,
    )
    await botev.send(msg)
    matrix_img = await drawer.draw_jjc_blind_matrix(
        result=result
    )
    await botev.send(outp_b64(matrix_img))


@sv.on_prefix(f"{prefix}pjjc盲打")
@wrap_hoshino_event
async def pjjc_blind_fight(botev: BotEvent):
    defends = await _parse_defend_teams(botev)
    attacks = await asyncio.gather(*[
        jjc_server.pick_confidence_attack_team(defend)
        for defend in defends
    ])
    teams = await jjc_server.get_hot_attack_teams(days=7, limit=8)
    attacks.append([t.team for t in teams])
    if attacks:
        await botev.send(f"防守方「" + '\n'.join(format_team_name(deck) for deck in defends) + f"」\n根据历史数据分析，筛选了{'+'.join([str(len(team)) for team in attacks])}支进攻队伍，正在组合中...")
    attacks = [list(team) for team in dict.fromkeys(tuple(team) for teams in attacks for team in teams)]
    if not attacks:
        await botev.finish("未筛到可用的进攻队伍")

    result = await jjc_server.build_pjjc_matrix(
        attacks=attacks,
        defends=defends,
    )
    if not result.attacks:
        await botev.finish("未找到角色无冲突的三队组合")

    result = result.truncate(8)

    await botev.send(
        format_pjjc_blind_groups_text(
            result=result,
        )
    )
    pjjc_img = await drawer.draw_pjjc_blind_matrix(
        result=result
    )
    await botev.send(outp_b64(pjjc_img))

@sv.on_prefix(f"{prefix}jjc建议")
@wrap_hoshino_event
async def jjc_suggestion(botev: BotEvent):
    defends = await _parse_defend_teams(botev)
    if len(defends) > 3:
        await botev.finish("JJC/PJJC建议最多支持3队防守阵容")
        return
    if any(len(team) != 5 or len(set(team)) != 5 for team in defends):
        await botev.finish("每队请选择5位不同的角色")
        return

    if len(defends) == 1:
        enemy_ids = defends[0]

        await botev.send(f"防守方「" + format_team_name(enemy_ids) + "」\n正在获取建议...")
        try:
            results = await jjc_server.get_attack_recommendations(enemy_ids)
        except Exception as exc:
            await botev.finish(f"获取JJC建议失败: {exc}")
            return

        if not results:
            await botev.finish("未找到可行的拆法")
        msg = "推荐拆法:\n" + '\n'.join(result.description(include_attack=True, include_defend=False) for result in results[:10])
        await botev.send(msg)
        img = await drawer.draw_jjc_suggestion(results[:10])
        await botev.send(outp_b64(img))
    else:
        await botev.send(f"防守方「" + '\n'.join(format_team_name(deck) for deck in defends) + "」\n正在获取建议...")
        try:
            candidates = await jjc_server.get_pjjc_recommendations(defends)
        except Exception as exc:
            await botev.finish(f"获取PJJC建议失败: {exc}")
            return
        msg, img = await _format_pjjc_candidates(candidates)
        if not msg:
            await botev.finish("未找到可行的拆法")
        await botev.send("\n\n".join(msg))
        await botev.send(outp_b64(img))

@sv.on_prefix(f"{prefix}jjc模拟")
@wrap_hoshino_event
async def jjc_simulator(botev: BotEvent):
    msg = ''.join(await botev.message()).split('vs')
    if len(msg) != 2:
        await botev.finish("请指定双方角色，格式如：角色1 角色2 vs 角色A 角色B")
    player_ids, unknown_units = roster.parse_team(msg[0])
    enemy_ids, unknown_units_enemy = roster.parse_team(msg[1])

    unknown_units += unknown_units_enemy
    if unknown_units:
        await botev.finish(f"未知昵称{unknown_units}")

    if not player_ids or not enemy_ids:
        await botev.finish("请指定双方角色，格式如：角色1 角色2 vs 角色A 角色B")

    player_ids = [i * 100 + 1 for i in player_ids]
    enemy_ids = [i * 100 + 1 for i in enemy_ids]

    results = await jjc_server.simulate_battle_multiple(player_ids, enemy_ids, use_cache=False)

    attack_names = ' '.join([db.get_unit_name(uid) for uid in player_ids])
    defense_names = ' '.join([db.get_unit_name(uid) for uid in enemy_ids])

    summary = f"{attack_names} vs {defense_names}\n" + '\n'.join(
            [f"耗时 {result.duration:.1f}s | 结果 {eJJCStatus(result.result).name}" for result in results.results])
    await botev.send(summary)

    img = await drawer.draw_jjc_vs(results.results)
    await botev.send(outp_b64(img))
