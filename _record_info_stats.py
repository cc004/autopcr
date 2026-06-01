#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator


DEFAULT_EX_EQUIP_PATH = "cache/modules/ex_equip_rainbow_enchance"
DEFAULT_TRAVEL_PATH = "cache/modules/travel_quest_sweep"

ROUND_SELECT_RE = re.compile(r"^(\d+)-select-([12])-(success|fail|end)(-biling)?$")
ROUND_SIDE_RE = re.compile(r"^(\d+)-biling-(left|right)$")
ROUND_SIMPLE_RE = re.compile(r"^(\d+)-(enter|get|lose)$")
STATUS_STEP_RE = re.compile(r"^(\d+)-(\d+)$")
PLAY_MAX_STEP_RE = re.compile(r"^(\d+)-max_step-(\d+)$")

STATUS_NAME = {
    1: "HP",
    2: "物攻",
    3: "物防",
    4: "魔攻",
    5: "魔防",
    6: "物爆",
    7: "法爆",
    8: "闪避",
    9: "吸血",
    10: "HP回复",
    11: "TP回复",
    12: "物贯",
    13: "法贯",
    14: "物爆提升",
    15: "回复量上升",
    16: "法爆提升",
    17: "命中",
}

STATUS_IS_PERCENT = {
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
    6: True,
    7: True,
    8: False,
    9: False,
    10: False,
    11: False,
    12: False,
    13: False,
    14: False,
    15: False,
    16: False,
    17: False,
}

RARITY_NAME = {
    1: "铜",
    2: "银",
    3: "金",
    4: "粉",
    5: "彩",
}


@dataclass
class EquipMeta:
    name: str | None = None
    rarity: int | None = None
    group_id: int | None = None
    step_values: dict[tuple[int, int], int] = field(default_factory=dict)


@dataclass
class EquipAttrStats:
    attr_counts: Counter[str] = field(default_factory=Counter)
    legacy_total: int = 0
    source_files: set[str] = field(default_factory=set)

    @property
    def total(self) -> int:
        return sum(self.attr_counts.values())


@dataclass
class PlayEffectStats:
    explicit_total: int = 0
    effect_counts: Counter[int] = field(default_factory=Counter)
    max_step_by_effect: dict[int, Counter[int]] = field(default_factory=lambda: defaultdict(Counter))
    source_files: set[str] = field(default_factory=set)

    @property
    def effect_total(self) -> int:
        return sum(self.effect_counts.values())


@dataclass
class ExEquipStats:
    attr_by_equip: dict[str, EquipAttrStats] = field(default_factory=lambda: defaultdict(EquipAttrStats))
    play_by_equip: dict[str, PlayEffectStats] = field(default_factory=lambda: defaultdict(PlayEffectStats))
    files: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class AccountTravelStats:
    account_id: str
    path: Path
    counter: Counter[str] = field(default_factory=Counter)


@dataclass
class TravelStats:
    counter: Counter[str] = field(default_factory=Counter)
    accounts: list[AccountTravelStats] = field(default_factory=list)
    files: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="汇总 9dea451df3ef 新增的记录信息：宝箱殿、彩装词条、play_effect_id。"
    )
    parser.add_argument("--travel-path", default=DEFAULT_TRAVEL_PATH, help=f"travel 缓存目录，默认 {DEFAULT_TRAVEL_PATH}")
    parser.add_argument("--ex-equip-path", default=DEFAULT_EX_EQUIP_PATH, help=f"彩装缓存目录，默认 {DEFAULT_EX_EQUIP_PATH}")
    parser.add_argument("--db", default="", help="指定本地 db 文件；不传则自动取 cache/db 下最新的 .db")
    parser.add_argument("--section", choices=("all", "travel", "exequip"), default="all", help="只输出指定统计块")
    parser.add_argument("--top-status", type=int, default=0, help="每件装备最多展示多少个属性，0 表示全部")
    parser.add_argument("--top-equip", type=int, default=0, help="最多展示多少件装备明细，0 表示全部")
    parser.add_argument("--travel-account-min-enter", type=int, default=5, help="账号间比较时，每层至少进入多少次才纳入")
    parser.add_argument("--travel-account-top", type=int, default=20, help="账号间比较时每层最多展示偏差最大的多少个账号，0 表示全部")
    parser.add_argument("--output", default="", help="把报告写入指定文件；不传则只打印到 stdout")
    return parser.parse_args()


def iter_json_files(root: Path) -> Iterator[Path]:
    if root.is_file() and root.suffix.lower() == ".json":
        yield root
        return
    if not root.exists():
        return
    for path in sorted(root.rglob("*.json")):
        if path.is_file():
            yield path


def safe_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def load_json(path: Path, warnings: list[str]) -> dict[str, object] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        warnings.append(f"{path}: JSON 解析失败: {exc}")
        return None
    if not isinstance(data, dict):
        warnings.append(f"{path}: 顶层不是 object，已跳过")
        return None
    return data


def load_travel_stats(root: Path) -> TravelStats:
    stats = TravelStats(files=list(iter_json_files(root)))
    if not root.exists():
        stats.warnings.append(f"{root}: 路径不存在")
        return stats

    for path in stats.files:
        data = load_json(path, stats.warnings)
        if data is None:
            continue
        raw_round_event = data.get("round_event")
        if raw_round_event is None:
            continue
        if not isinstance(raw_round_event, dict):
            stats.warnings.append(f"{path}: round_event 不是 object，已跳过")
            continue

        account_counter: Counter[str] = Counter()
        for raw_key, raw_count in raw_round_event.items():
            count = safe_int(raw_count)
            if count is None or count <= 0:
                continue
            key = str(raw_key)
            stats.counter[key] += count
            account_counter[key] += count
        if account_counter:
            stats.accounts.append(AccountTravelStats(path.stem, path, account_counter))

    return stats


def load_ex_equip_stats(root: Path) -> ExEquipStats:
    stats = ExEquipStats(files=list(iter_json_files(root)))
    if not root.exists():
        stats.warnings.append(f"{root}: 路径不存在")
        return stats

    for path in stats.files:
        data = load_json(path, stats.warnings)
        if data is None:
            continue

        for raw_key, raw_payload in data.items():
            key = str(raw_key)
            if key == "round_event":
                continue
            if not isinstance(raw_payload, dict):
                stats.warnings.append(f"{path}: {key} 的值不是 object，已跳过")
                continue

            if key.startswith("play-effect-"):
                equip_id = key.removeprefix("play-effect-")
                item_stats = stats.play_by_equip[equip_id]
                item_stats.source_files.add(str(path))
                for raw_item_key, raw_count in raw_payload.items():
                    item_key = str(raw_item_key)
                    count = safe_int(raw_count)
                    if count is None or count <= 0:
                        continue
                    if item_key == "count":
                        item_stats.explicit_total += count
                    elif item_key.isdigit():
                        item_stats.effect_counts[int(item_key)] += count
                    else:
                        match = PLAY_MAX_STEP_RE.match(item_key)
                        if match:
                            item_stats.max_step_by_effect[int(match.group(1))][int(match.group(2))] += count
                        else:
                            stats.warnings.append(f"{path}: 未识别 play-effect key {item_key!r}")
                continue

            if not key.isdigit():
                stats.warnings.append(f"{path}: 未识别装备 key {key!r}")
                continue

            item_stats = stats.attr_by_equip[key]
            item_stats.source_files.add(str(path))
            for raw_item_key, raw_count in raw_payload.items():
                item_key = str(raw_item_key)
                count = safe_int(raw_count)
                if count is None or count <= 0:
                    continue
                if item_key == "total":
                    item_stats.legacy_total += count
                elif STATUS_STEP_RE.match(item_key):
                    item_stats.attr_counts[item_key] += count
                else:
                    stats.warnings.append(f"{path}: 未识别词条 key {item_key!r}")

    return stats


def find_db_path(user_input: str) -> Path | None:
    if user_input:
        path = Path(user_input)
        return path if path.exists() else None
    candidates = sorted(Path("cache/db").glob("*.db"))
    return candidates[-1] if candidates else None


def load_equip_meta(db_path: Path | None) -> tuple[dict[str, EquipMeta], list[str]]:
    if db_path is None:
        return {}, ["未找到本地 db，装备名和词条数值将只显示 ID/step"]

    warnings: list[str] = []
    result: dict[str, EquipMeta] = {}
    try:
        conn = sqlite3.connect(db_path)
    except Exception as exc:
        return {}, [f"打开 db 失败: {db_path}: {exc}"]

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT d.ex_equipment_id, d.name, d.rarity, g.group_id
            FROM ex_equipment_data AS d
            LEFT JOIN ex_equipment_sub_status_group AS g
                ON g.ex_equipment_id = d.ex_equipment_id
            """
        )
        for equip_id, name, rarity, group_id in cur.fetchall():
            result[str(equip_id)] = EquipMeta(name=name, rarity=rarity, group_id=group_id)

        cur.execute(
            """
            SELECT group_id, status, value_1, value_2, value_3, value_4, value_5
            FROM ex_equipment_sub_status
            """
        )
        group_values: dict[int, dict[tuple[int, int], int]] = defaultdict(dict)
        for group_id, status, value_1, value_2, value_3, value_4, value_5 in cur.fetchall():
            group_values[group_id][(status, 1)] = value_1
            group_values[group_id][(status, 2)] = value_2
            group_values[group_id][(status, 3)] = value_3
            group_values[group_id][(status, 4)] = value_4
            group_values[group_id][(status, 5)] = value_5
        for meta in result.values():
            if meta.group_id is not None:
                meta.step_values = group_values.get(meta.group_id, {})
    except Exception as exc:
        warnings.append(f"读取 db 失败: {db_path}: {exc}")
        return {}, warnings
    finally:
        conn.close()

    return result, warnings


def pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "N/A"
    return f"{numerator / denominator * 100:.2f}%"


def ratio(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator} = {pct(numerator, denominator)}"


def status_name(status_id: int) -> str:
    return STATUS_NAME.get(status_id, f"未知属性({status_id})")


def step_value(raw_value: int | None, status_id: int) -> str:
    if raw_value is None:
        return "?"
    if STATUS_IS_PERCENT.get(status_id, False):
        return f"{raw_value / 100:.2f}%"
    return str(raw_value)


def equip_name(equip_id: str, meta_map: dict[str, EquipMeta]) -> str:
    meta = meta_map.get(equip_id)
    if not meta or not meta.name:
        return equip_id
    rarity = RARITY_NAME.get(meta.rarity, "")
    return f"{rarity}-{meta.name}" if rarity else meta.name


def append_warnings(lines: list[str], warnings: list[str]) -> None:
    if not warnings:
        return
    lines.append("")
    lines.append("告警:")
    for warning in warnings:
        lines.append(f"  - {warning}")


def parse_round_event_counter(
    counter: Counter[str],
) -> tuple[
    set[int],
    dict[int, Counter[tuple[int, str, bool]]],
    dict[int, Counter[str]],
    dict[int, Counter[str]],
]:
    rounds: set[int] = set()
    select_counts: dict[int, Counter[tuple[int, str, bool]]] = defaultdict(Counter)
    side_counts: dict[int, Counter[str]] = defaultdict(Counter)
    simple_counts: dict[int, Counter[str]] = defaultdict(Counter)

    for key, count in counter.items():
        if key == "count":
            continue
        match = ROUND_SELECT_RE.match(key)
        if match:
            round_id = int(match.group(1))
            door_id = int(match.group(2))
            result = match.group(3)
            selected_biling = bool(match.group(4))
            rounds.add(round_id)
            select_counts[round_id][(door_id, result, selected_biling)] += count
            continue

        match = ROUND_SIDE_RE.match(key)
        if match:
            round_id = int(match.group(1))
            rounds.add(round_id)
            side_counts[round_id][match.group(2)] += count
            continue

        match = ROUND_SIMPLE_RE.match(key)
        if match:
            round_id = int(match.group(1))
            rounds.add(round_id)
            simple_counts[round_id][match.group(2)] += count

    return rounds, select_counts, side_counts, simple_counts


def get_round_result_counts(counter: Counter[str], round_id: int) -> Counter[str]:
    ret: Counter[str] = Counter()
    for key, count in counter.items():
        match = ROUND_SELECT_RE.match(key)
        if match and int(match.group(1)) == round_id:
            ret[match.group(3)] += count
    return ret


def probability_triplet(counts: Counter[str], denominator: int) -> str:
    return (
        f"success {ratio(counts.get('success', 0), denominator)}，"
        f"fail {ratio(counts.get('fail', 0), denominator)}，"
        f"end {ratio(counts.get('end', 0), denominator)}"
    )


def norm_cdf(x: float) -> float:
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def chi_square_sf_approx(chi_square: float, degrees_of_freedom: int) -> float | None:
    if degrees_of_freedom <= 0:
        return None
    if chi_square <= 0:
        return 1.0
    k = degrees_of_freedom
    z = ((chi_square / k) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * k))) / math.sqrt(2.0 / (9.0 * k))
    return max(0.0, min(1.0, 1.0 - norm_cdf(z)))


def p_value_text(p_value: float | None) -> str:
    if p_value is None:
        return "N/A"
    if p_value < 0.0001:
        return "<0.0001"
    return f"{p_value:.4f}"


def account_compare_judgement(p_value: float | None, expected_lt_5: int, expected_total: int) -> str:
    small_expected_ratio = expected_lt_5 / expected_total if expected_total else 0.0
    sample_note = "，但小期望格较多，结论只作参考" if small_expected_ratio > 0.2 else ""
    if p_value is None:
        return "有效结果种类不足，无法检验"
    if p_value >= 0.05:
        return f"未发现显著账号差异{sample_note}"
    if p_value >= 0.01:
        return f"账号间可能存在差异{sample_note}"
    return f"账号间差异明显{sample_note}"


def append_travel_account_compare(lines: list[str], stats: TravelStats, rounds: set[int], min_enter: int, top_accounts: int) -> None:
    if not stats.accounts:
        return

    lines.append("")
    lines.append("账号间一致性:")
    lines.append(f"  口径: 每层按账号的 success/fail/end 做同分布检验；该层进入次数 < {min_enter} 的账号不纳入。")
    lines.append("  检验: Pearson chi-square 同质性检验，p 值为 Wilson-Hilferty 近似。")

    for round_id in sorted(rounds):
        account_rows: list[tuple[AccountTravelStats, int, Counter[str]]] = []
        pooled_counts: Counter[str] = Counter()
        for account in stats.accounts:
            entered = account.counter.get(f"{round_id}-enter", 0)
            if entered < min_enter:
                continue
            result_counts = get_round_result_counts(account.counter, round_id)
            total = sum(result_counts.values()) or entered
            if total <= 0:
                continue
            account_rows.append((account, total, result_counts))
            pooled_counts.update(result_counts)

        pooled_total = sum(pooled_counts.values())
        active_outcomes = [outcome for outcome in ("success", "fail", "end") if pooled_counts.get(outcome, 0) > 0]

        lines.append(f"  第 {round_id} 层:")
        lines.append(
            f"    纳入账号: {len(account_rows)}/{len(stats.accounts)}，样本数: {pooled_total}，总体分布: {probability_triplet(pooled_counts, pooled_total)}"
        )
        if len(account_rows) < 2 or len(active_outcomes) < 2 or pooled_total <= 0:
            lines.append("    有效账号或结果种类不足，无法判断账号间是否一致。")
            continue

        chi_square = 0.0
        expected_lt_5 = 0
        expected_total = 0
        deviations: list[tuple[float, AccountTravelStats, int, Counter[str], str, float]] = []
        for account, total, result_counts in account_rows:
            max_abs_residual = 0.0
            max_label = ""
            max_residual = 0.0
            for outcome in active_outcomes:
                expected = total * pooled_counts[outcome] / pooled_total
                observed = result_counts.get(outcome, 0)
                if expected <= 0:
                    continue
                residual = (observed - expected) / math.sqrt(expected)
                chi_square += residual * residual
                expected_total += 1
                if expected < 5:
                    expected_lt_5 += 1
                if abs(residual) > max_abs_residual:
                    max_abs_residual = abs(residual)
                    max_label = outcome
                    max_residual = residual
            deviations.append((max_abs_residual, account, total, result_counts, max_label, max_residual))

        degrees_of_freedom = (len(account_rows) - 1) * (len(active_outcomes) - 1)
        p_value = chi_square_sf_approx(chi_square, degrees_of_freedom)
        lines.append(
            f"    chi-square={chi_square:.2f}, df={degrees_of_freedom}, p≈{p_value_text(p_value)}，"
            f"{account_compare_judgement(p_value, expected_lt_5, expected_total)}"
        )
        if expected_total:
            lines.append(f"    期望值 < 5 的格子: {expected_lt_5}/{expected_total}")

        ranked = sorted(deviations, key=lambda item: (-item[0], item[1].account_id))
        if top_accounts > 0:
            ranked = ranked[:top_accounts]
        lines.append(f"    偏差最大的账号{'(全部)' if top_accounts == 0 else f'(前 {top_accounts})'}:")
        for _, account, total, result_counts, max_label, max_residual in ranked:
            direction = "+" if max_residual >= 0 else ""
            lines.append(
                f"      {account.account_id}: n={total}，{probability_triplet(result_counts, total)}，"
                f"最大残差 {max_label} {direction}{max_residual:.2f}"
            )


def build_travel_report(root: Path, stats: TravelStats, account_min_enter: int, account_top: int) -> list[str]:
    lines = [
        "[travel_quest_sweep / 宝箱殿]",
        f"扫描路径: {root.resolve()}",
        f"JSON 文件数: {len(stats.files)}",
        "口径: 只统计已触发 round_event 的宝箱殿；未记录没有出现宝箱殿的探险次数。",
    ]
    append_warnings(lines, stats.warnings)

    counter = stats.counter
    if not counter:
        lines.append("")
        lines.append("无 round_event 统计数据")
        return lines

    event_count = counter.get("count", 0)
    rounds, select_counts, side_counts, simple_counts = parse_round_event_counter(counter)
    total_get = sum(simple_counts[round_id].get("get", 0) for round_id in rounds)
    total_lose = sum(simple_counts[round_id].get("lose", 0) for round_id in rounds)

    total_non_biling_door: Counter[int] = Counter()
    total_non_biling_success: Counter[int] = Counter()
    for round_select_counts in select_counts.values():
        for (door_id, result, selected_biling), count in round_select_counts.items():
            if selected_biling:
                continue
            total_non_biling_door[door_id] += count
            if result == "success":
                total_non_biling_success[door_id] += count

    lines.append("")
    lines.append("总体:")
    lines.append(f"  宝箱殿记录次数: {event_count}")
    lines.append(f"  最终拿到宝箱: {ratio(total_get, event_count)}")
    lines.append(f"  最终未拿到宝箱: {ratio(total_lose, event_count)}")
    lines.append(
        "  选中非闪光门成功率: "
        f"左门 {ratio(total_non_biling_success.get(1, 0), total_non_biling_door.get(1, 0))}，"
        f"右门 {ratio(total_non_biling_success.get(2, 0), total_non_biling_door.get(2, 0))}"
    )

    lines.append("")
    lines.append("到达层数:")
    for round_id in sorted(rounds):
        entered = simple_counts[round_id].get("enter", 0)
        lines.append(f"  第 {round_id} 层: {ratio(entered, event_count)}")

    lines.append("")
    lines.append("最终停层:")
    for round_id in sorted(rounds):
        got = simple_counts[round_id].get("get", 0)
        lost = simple_counts[round_id].get("lose", 0)
        if got or lost:
            lines.append(f"  第 {round_id} 层: 拿箱 {ratio(got, event_count)}，失败 {ratio(lost, event_count)}")

    lines.append("")
    lines.append("逐层选择结果:")
    for round_id in sorted(rounds):
        entered = simple_counts[round_id].get("enter", 0)
        left_biling = side_counts[round_id].get("left", 0)
        right_biling = side_counts[round_id].get("right", 0)

        result_counter: Counter[str] = Counter()
        door_counter: Counter[int] = Counter()
        non_biling_door: Counter[int] = Counter()
        non_biling_success: Counter[int] = Counter()
        selected_biling_count = 0
        for (door_id, result, selected_biling), count in select_counts[round_id].items():
            result_counter[result] += count
            door_counter[door_id] += count
            if selected_biling:
                selected_biling_count += count
            else:
                non_biling_door[door_id] += count
                if result == "success":
                    non_biling_success[door_id] += count

        lines.append(f"  第 {round_id} 层，进入 {entered} 次")
        lines.append(
            "    闪光门: "
            f"左 {ratio(left_biling, entered)}，"
            f"右 {ratio(right_biling, entered)}，"
            f"门计数合计 {ratio(left_biling + right_biling, entered)}"
        )
        lines.append(
            "    选门: "
            f"左 {ratio(door_counter.get(1, 0), entered)}，"
            f"右 {ratio(door_counter.get(2, 0), entered)}，"
            f"选中闪光门 {ratio(selected_biling_count, entered)}"
        )
        lines.append(f"    结果: {probability_triplet(result_counter, entered)}")
        lines.append(
            "    选中非闪光门成功率: "
            f"左门 {ratio(non_biling_success.get(1, 0), non_biling_door.get(1, 0))}，"
            f"右门 {ratio(non_biling_success.get(2, 0), non_biling_door.get(2, 0))}"
        )
        if selected_biling_count:
            selected_biling_results: Counter[str] = Counter()
            for (_, result, selected_biling), count in select_counts[round_id].items():
                if selected_biling:
                    selected_biling_results[result] += count
            lines.append(f"    选中闪光门后的结果: {probability_triplet(selected_biling_results, selected_biling_count)}")

    append_travel_account_compare(lines, stats, rounds, account_min_enter, account_top)
    return lines


def parse_status_step(key: str) -> tuple[int, int] | None:
    match = STATUS_STEP_RE.match(key)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def attr_groups(attr_counts: Counter[str]) -> dict[int, Counter[int]]:
    groups: dict[int, Counter[int]] = defaultdict(Counter)
    for key, count in attr_counts.items():
        parsed = parse_status_step(key)
        if parsed is None:
            continue
        status_id, step = parsed
        groups[status_id][step] += count
    return groups


def merge_play_stats(items: Iterable[PlayEffectStats]) -> PlayEffectStats:
    merged = PlayEffectStats()
    for item in items:
        merged.explicit_total += item.explicit_total
        merged.effect_counts.update(item.effect_counts)
        for effect_id, counter in item.max_step_by_effect.items():
            merged.max_step_by_effect[effect_id].update(counter)
        merged.source_files.update(item.source_files)
    return merged


def append_play_report(lines: list[str], title: str, stats: PlayEffectStats) -> None:
    prefix = title[: len(title) - len(title.lstrip())]
    child = prefix + "  "
    denominator = stats.explicit_total if stats.explicit_total > 0 else stats.effect_total
    lines.append(title)
    lines.append(f"{child}alces_exec count: {stats.explicit_total}")
    lines.append(f"{child}play_effect_id 计数和: {stats.effect_total}")
    if denominator <= 0:
        lines.append(f"{child}无 play_effect_id 统计数据")
        return
    if stats.explicit_total and stats.effect_total and stats.explicit_total != stats.effect_total:
        lines.append(f"{child}注意: count 与 play_effect_id 计数和不一致，本段概率仍以 count={denominator} 为分母。")

    for effect_id, count in sorted(stats.effect_counts.items()):
        max_step_counter = stats.max_step_by_effect.get(effect_id, Counter())
        max_step_text = " / ".join(
            f"{max_step}满词条: {ratio(max_step_count, count)}"
            for max_step, max_step_count in sorted(max_step_counter.items())
        )
        suffix = f"，max_step 分布: {max_step_text}" if max_step_text else ""
        lines.append(f"{child}play_effect_id={effect_id}: {ratio(count, denominator)}{suffix}")

    all_max_step: Counter[int] = Counter()
    for counter in stats.max_step_by_effect.values():
        all_max_step.update(counter)
    if all_max_step:
        total = sum(all_max_step.values())
        avg = sum(max_step * count for max_step, count in all_max_step.items()) / total
        text = " / ".join(
            f"{max_step}满词条: {ratio(count, total)}"
            for max_step, count in sorted(all_max_step.items())
        )
        lines.append(f"{child}全部演出 max_step 分布: {text}")
        lines.append(f"{child}平均每次出现满词条数: {avg:.4f}")


def build_ex_equip_report(
    root: Path,
    stats: ExEquipStats,
    meta_map: dict[str, EquipMeta],
    db_path: Path | None,
    top_status: int,
    top_equip: int,
    db_warnings: list[str],
) -> list[str]:
    lines = [
        "[ex_equip_rainbow_enchance / 彩装究极炼成]",
        f"扫描路径: {root.resolve()}",
        f"JSON 文件数: {len(stats.files)}",
        f"本地 DB: {db_path.resolve() if db_path else '未找到'}",
        "口径: 词条概率按非锁定词条记录计数统计；play_effect_id 概率按 alces_exec 次数统计。",
    ]
    append_warnings(lines, stats.warnings + db_warnings)
    if not stats.attr_by_equip and not stats.play_by_equip:
        lines.append("")
        lines.append("无彩装统计数据")
        return lines

    all_attr_counts: Counter[str] = Counter()
    legacy_total = 0
    for item in stats.attr_by_equip.values():
        all_attr_counts.update(item.attr_counts)
        legacy_total += item.legacy_total
    denominator = sum(all_attr_counts.values())

    lines.append("")
    lines.append("词条池总体:")
    lines.append(f"  装备数: {len(stats.attr_by_equip)}")
    lines.append(f"  非锁定词条记录数: {denominator}")
    if legacy_total:
        lines.append(f"  legacy total 字段合计: {legacy_total} (旧缓存遗留，不作为概率分母)")
    for status_id, steps in sorted(attr_groups(all_attr_counts).items(), key=lambda item: (-sum(item[1].values()), item[0])):
        status_total = sum(steps.values())
        step_text = " / ".join(f"step{step}: {ratio(count, denominator)}" for step, count in sorted(steps.items()))
        lines.append(f"  {status_name(status_id)}: {ratio(status_total, denominator)}")
        lines.append(f"    {step_text}")

    lines.append("")
    append_play_report(lines, "play_effect_id 总体:", merge_play_stats(stats.play_by_equip.values()))

    equip_ids = sorted(set(stats.attr_by_equip) | set(stats.play_by_equip), key=lambda item: int(item) if item.isdigit() else item)
    if top_equip > 0:
        equip_ids = equip_ids[:top_equip]
    for equip_id in equip_ids:
        attr_stats = stats.attr_by_equip.get(equip_id, EquipAttrStats())
        play_stats = stats.play_by_equip.get(equip_id, PlayEffectStats())
        meta = meta_map.get(equip_id)
        denominator = attr_stats.total
        lines.append("")
        lines.append(f"装备 {equip_id} {equip_name(equip_id, meta_map)}:")
        lines.append(f"  来源文件: {len(attr_stats.source_files | play_stats.source_files)}")
        lines.append(f"  非锁定词条记录数: {denominator}")
        if attr_stats.legacy_total:
            lines.append(f"  legacy total: {attr_stats.legacy_total} (不作为概率分母)")

        if denominator > 0:
            ranked_groups = sorted(attr_groups(attr_stats.attr_counts).items(), key=lambda item: (-sum(item[1].values()), item[0]))
            if top_status > 0:
                ranked_groups = ranked_groups[:top_status]
            for status_id, steps in ranked_groups:
                status_total = sum(steps.values())
                step_text = " / ".join(
                    (
                        f"step{step}"
                        f"({step_value(meta.step_values.get((status_id, step)) if meta else None, status_id)})"
                        f": {ratio(count, denominator)}"
                    )
                    for step, count in sorted(steps.items())
                )
                lines.append(f"  {status_name(status_id)}: {ratio(status_total, denominator)}")
                lines.append(f"    {step_text}")
        else:
            lines.append("  无词条池统计数据")

        if play_stats.explicit_total or play_stats.effect_counts:
            append_play_report(lines, "  play_effect_id:", play_stats)

    return lines


def main() -> int:
    args = parse_args()
    db_path = find_db_path(args.db)
    meta_map, db_warnings = load_equip_meta(db_path)
    lines: list[str] = []

    if args.section in ("all", "travel"):
        travel_root = Path(args.travel_path)
        travel_stats = load_travel_stats(travel_root)
        lines.extend(build_travel_report(travel_root, travel_stats, args.travel_account_min_enter, args.travel_account_top))

    if args.section == "all":
        lines.append("")
        lines.append("=" * 80)
        lines.append("")

    if args.section in ("all", "exequip"):
        ex_root = Path(args.ex_equip_path)
        ex_stats = load_ex_equip_stats(ex_root)
        lines.extend(build_ex_equip_report(ex_root, ex_stats, meta_map, db_path, args.top_status, args.top_equip, db_warnings))

    report = "\n".join(lines)
    print(report)
    if args.output:
        Path(args.output).write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
