from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
from xml.sax.saxutils import escape


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = ROOT_DIR / "cache" / "modules" / "user_info"
DEFAULT_OUTPUT = ROOT_DIR / "result" / "user_info_trend.svg"

COLORS = [
    "#2563eb",
    "#dc2626",
    "#16a34a",
    "#9333ea",
    "#ea580c",
    "#0891b2",
]

SERIES_LABELS = {
    "jewel": "钻石",
    "pig": "母猪石",
}


@dataclass(frozen=True)
class Point:
    ts: float
    value: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="根据 cache/modules/user_info 中的 JSON 绘制数量变化折线图。"
    )
    parser.add_argument(
        "json_file",
        nargs="?",
        type=Path,
        help="要绘制的 user_info JSON；不传则使用目录中最新的非空 JSON。",
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"未指定 JSON 时扫描的目录，默认：{DEFAULT_INPUT_DIR}",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"输出 SVG 路径，默认：{DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "-s",
        "--series",
        nargs="+",
        help="只绘制指定指标；默认优先绘制 jewel，例如：--series pig",
    )
    parser.add_argument("--title", default="数量变化趋势", help="图表标题。")
    parser.add_argument("--width", type=int, default=960, help="图片宽度。")
    parser.add_argument("--height", type=int, default=540, help="图片高度。")
    parser.add_argument(
        "--no-markers",
        action="store_true",
        help="不绘制每个数据点的小圆点，数据很多时可使用。",
    )
    return parser.parse_args()


def newest_json(input_dir: Path) -> Path:
    candidates = [
        path
        for path in input_dir.glob("*.json")
        if path.is_file() and path.stat().st_size > 0
    ]
    if not candidates:
        raise FileNotFoundError(f"未找到非空 JSON 文件：{input_dir}")
    import random
    return random.choice(candidates)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_timestamp(value: object) -> Optional[float]:
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return None

    # 支持常见的秒、毫秒、微秒时间戳。
    while abs(ts) > 10_000_000_000:
        ts /= 1000
    return ts


def parse_number(value: object) -> Optional[float]:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_timestamp_mapping(data: object) -> Optional[List[Point]]:
    if not isinstance(data, Mapping):
        return None

    points: List[Point] = []
    for raw_ts, raw_value in data.items():
        ts = parse_timestamp(raw_ts)
        value = parse_number(raw_value)
        if ts is None or value is None:
            return None
        points.append(Point(ts, value))

    if not points:
        return None
    points.sort(key=lambda point: point.ts)
    return points


def extract_series(data: object) -> Dict[str, List[Point]]:
    single_series = parse_timestamp_mapping(data)
    if single_series:
        return {"数量": single_series}

    if not isinstance(data, Mapping):
        raise ValueError("JSON 顶层应为 {时间戳: 数量} 或 {指标名: {时间戳: 数量}}。")

    series: Dict[str, List[Point]] = {}
    for name, values in data.items():
        points = parse_timestamp_mapping(values)
        if points:
            series[str(name)] = points

    if not series:
        raise ValueError("JSON 中没有找到可绘制的 {时间戳: 数量} 数据。")
    return series


def choose_series(
    all_series: Mapping[str, List[Point]], requested: Optional[Sequence[str]]
) -> Dict[str, List[Point]]:
    if not requested:
        if "jewel" in all_series:
            return {"jewel": all_series["jewel"]}
        return dict(all_series)

    missing = [name for name in requested if name not in all_series]
    if missing:
        available = ", ".join(all_series.keys())
        raise KeyError(f"找不到指标：{', '.join(missing)}；可用指标：{available}")
    return {name: all_series[name] for name in requested}


def nice_value(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 100_000_000:
        return f"{value / 100_000_000:.1f}亿"
    if abs_value >= 10_000:
        return f"{value / 10_000:.1f}万"
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}"


def display_name(name: object) -> str:
    text = str(name)
    return SERIES_LABELS.get(text, text)


def timestamp_label(ts: float, span: float) -> Tuple[str, str]:
    dt = datetime.fromtimestamp(ts)
    if span >= 365 * 24 * 3600:
        return dt.strftime("%Y"), dt.strftime("%m-%d")
    if span >= 2 * 24 * 3600:
        return dt.strftime("%m-%d"), ""
    return dt.strftime("%m-%d"), dt.strftime("%H:%M")


def make_ticks(start: float, end: float, count: int) -> List[float]:
    if count <= 1 or start == end:
        return [start]
    step = (end - start) / (count - 1)
    return [start + step * idx for idx in range(count)]


def clamp_dimension(value: int, minimum: int) -> int:
    return max(minimum, int(value))


def svg_text(
    x: float,
    y: float,
    text: str,
    *,
    size: int = 14,
    fill: str = "#334155",
    anchor: str = "start",
    weight: str = "400",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f"{escape(text)}</text>"
    )


def polyline(points: Iterable[Tuple[float, float]], color: str) -> str:
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="3" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{coords}" />'
    )


def text_width(text: str, size: int = 13) -> int:
    units = sum(2 if ord(char) > 127 else 1 for char in text)
    return int(units * size * 0.52) + 22


def clamp(value: float, low: float, high: float) -> float:
    return min(max(value, low), high)


def extrema(points: Sequence[Point]) -> List[Tuple[str, Point]]:
    high = max(points, key=lambda point: point.value)
    low = min(points, key=lambda point: point.value)
    if high.ts == low.ts and high.value == low.value:
        return [("最高/最低", high)]
    return [("最高", high), ("最低", low)]


def extreme_label(
    label: str,
    point: Point,
    x: float,
    y: float,
    *,
    color: str,
    chart_left: float,
    chart_right: float,
    chart_top: float,
    chart_bottom: float,
) -> str:
    text = f"{label} {nice_value(point.value)}"
    width = text_width(text)
    height = 24
    label_x = clamp(x - width / 2, chart_left, chart_right - width)

    if label == "最低":
        label_y = y + 16 if y + 16 + height <= chart_bottom else y - 16 - height
    else:
        label_y = y - 16 - height if y - 16 - height >= chart_top else y + 16

    line_end_y = label_y if label_y > y else label_y + height
    return "\n".join(
        [
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{line_end_y:.1f}" stroke="{color}" stroke-width="1.5" />',
            f'<rect x="{label_x:.1f}" y="{label_y:.1f}" width="{width}" height="{height}" rx="4" fill="#ffffff" stroke="{color}" stroke-width="1.5" />',
            svg_text(label_x + width / 2, label_y + 17, text, size=13, fill="#0f172a", anchor="middle", weight="700"),
        ]
    )


def render_chart(
    series: Mapping[str, List[Point]],
    *,
    title: str,
    width: int,
    height: int,
    show_markers: bool,
) -> str:
    width = clamp_dimension(width, 640)
    height = clamp_dimension(height, 400)

    all_points = [point for points in series.values() for point in points]
    x_min = min(point.ts for point in all_points)
    x_max = max(point.ts for point in all_points)
    y_min = min(point.value for point in all_points)
    y_max = max(point.value for point in all_points)

    y_span = y_max - y_min
    if y_span == 0:
        padding = max(abs(y_max) * 0.1, 1)
    else:
        padding = y_span * 0.08
    y_min = max(0, y_min - padding) if y_min >= 0 else y_min - padding
    y_max += padding

    left = 84
    right = 36
    top = 78
    bottom = 76
    chart_w = width - left - right
    chart_h = height - top - bottom

    def scale_x(ts: float) -> float:
        if x_max == x_min:
            return left + chart_w / 2
        return left + (ts - x_min) / (x_max - x_min) * chart_w

    def scale_y(value: float) -> float:
        if y_max == y_min:
            return top + chart_h / 2
        return top + (y_max - value) / (y_max - y_min) * chart_h

    elements: List[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text { font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', Arial, sans-serif; }",
        "</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff" />',
        svg_text(width / 2, 34, title, size=24, fill="#0f172a", anchor="middle", weight="700"),
    ]

    legend_x = left
    legend_y = 58
    for idx, name in enumerate(series.keys()):
        color = COLORS[idx % len(COLORS)]
        x = legend_x + idx * 110
        elements.append(f'<circle cx="{x:.1f}" cy="{legend_y:.1f}" r="5" fill="{color}" />')
        elements.append(svg_text(x + 10, legend_y + 5, display_name(name), size=13, fill="#475569"))

    y_ticks = make_ticks(y_min, y_max, 5)
    for tick in y_ticks:
        y = scale_y(tick)
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + chart_w}" y2="{y:.1f}" stroke="#e2e8f0" stroke-width="1" />'
        )
        elements.append(svg_text(left - 12, y + 5, nice_value(tick), size=12, fill="#64748b", anchor="end"))

    x_tick_count = 6 if x_max != x_min else 1
    for tick in make_ticks(x_min, x_max, x_tick_count):
        x = scale_x(tick)
        label1, label2 = timestamp_label(tick, x_max - x_min)
        elements.append(
            f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + chart_h}" stroke="#f1f5f9" stroke-width="1" />'
        )
        elements.append(svg_text(x, top + chart_h + 28, label1, size=12, fill="#64748b", anchor="middle"))
        if label2:
            elements.append(svg_text(x, top + chart_h + 45, label2, size=12, fill="#94a3b8", anchor="middle"))

    elements.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#94a3b8" stroke-width="1.5" />',
            f'<line x1="{left}" y1="{top + chart_h}" x2="{left + chart_w}" y2="{top + chart_h}" stroke="#94a3b8" stroke-width="1.5" />',
            svg_text(left + chart_w / 2, height - 16, "时间", size=13, fill="#475569", anchor="middle"),
            svg_text(22, top + chart_h / 2, "数量", size=13, fill="#475569", anchor="middle"),
        ]
    )

    total_points = sum(len(points) for points in series.values())
    draw_markers = show_markers and total_points <= 500
    for idx, (name, points) in enumerate(series.items()):
        color = COLORS[idx % len(COLORS)]
        scaled = [(scale_x(point.ts), scale_y(point.value)) for point in points]
        elements.append(polyline(scaled, color))
        if draw_markers:
            for point, (x, y) in zip(points, scaled):
                value_label = nice_value(point.value)
                date_label = datetime.fromtimestamp(point.ts).strftime("%Y-%m-%d %H:%M")
                elements.append(
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#ffffff" stroke="{color}" stroke-width="2">'
                    f"<title>{escape(display_name(name))} {escape(date_label)}：{escape(value_label)}</title>"
                    "</circle>"
                )
        scaled_by_point = {point: scaled_point for point, scaled_point in zip(points, scaled)}
        for label, point in extrema(points):
            x, y = scaled_by_point[point]
            elements.append(
                extreme_label(
                    label,
                    point,
                    x,
                    y,
                    color=color,
                    chart_left=left,
                    chart_right=left + chart_w,
                    chart_top=top,
                    chart_bottom=top + chart_h,
                )
            )

    elements.append("</svg>")
    return "\n".join(elements)


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def main() -> int:
    args = parse_args()
    source = resolve_path(args.json_file) if args.json_file else newest_json(resolve_path(args.input_dir))
    output = resolve_path(args.output)

    data = load_json(source)
    all_series = extract_series(data)
    series = choose_series(all_series, args.series)

    svg = render_chart(
        series,
        title=args.title,
        width=args.width,
        height=args.height,
        show_markers=not args.no_markers,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")

    summary = ", ".join(
        f"{display_name(name)}[{name}]({len(points)}点)" for name, points in series.items()
    )
    print(f"source: {source}")
    print(f"output: {output}")
    print(f"series: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
