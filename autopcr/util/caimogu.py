'''踩蘑菇公会战作业网(gzlj)数据客户端

数据来源 https://www.caimogu.cc/gzlj.html ，接口无需登录但有按IP的频率限制
(超频时返回HTTP 200 + 空body)，因此所有请求必须走磁盘缓存，TTL内不发请求。
'''
import asyncio
import datetime
import json
import re
from collections import Counter, defaultdict
from os.path import dirname, exists, join
from time import time
from typing import Any, Dict, List

from ..constants import CACHE_DIR
from .aiorequests import get as _get
from .logger import instance as logger

BASE_URL = "https://www.caimogu.cc"
CACHE_PATH = join(CACHE_DIR, "caimogu", "latest.json")
REQUEST_INTERVAL = 5
HEADERS = {
    "Referer": f"{BASE_URL}/gzlj.html",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

# 刀型分类：手动以接口auto=2为准；auto=1的作业没有更细的可靠描述，统一按自动处理
SEMI_PATTERN = re.compile(r"单操作|开关|半自动|半手动", re.IGNORECASE)

_last_request_time = 0.0
# 上游按IP限流，并发协程必须串行排队：check-then-sleep竞争或请求在途时时间戳未更新都会超频
_request_lock = asyncio.Lock()


def classify_knife(homework: Dict[str, Any]) -> str:
    if homework.get("auto") == 2:
        return "手动"
    text = "".join(v.get("text") or "" for v in homework.get("video") or [])
    if SEMI_PATTERN.search(text):
        return "半自动"
    # auto=1的作业在作业网归为AUTO/半AUTO类，没有细分描述时按自动处理
    return "自动"


def load_cache() -> Dict[str, Any]:
    if not exists(CACHE_PATH):
        return None
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        logger.exception("读取踩蘑菇缓存失败")
        return None


def save_cache(payload: Dict[str, Any]):
    from os import makedirs
    makedirs(dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


async def _request_json(path: str, params: Dict[str, str]) -> Any:
    global _last_request_time
    async with _request_lock:
        interval = time() - _last_request_time
        if interval < REQUEST_INTERVAL:
            await asyncio.sleep(REQUEST_INTERVAL - interval)
        _last_request_time = time()  # 发出前先占位，请求在途时其他协程不会插入
        resp = await _get(f"{BASE_URL}{path}", params=params, headers=HEADERS, timeout=20)
    text = await resp.text  # AsyncResponse.text是异步属性
    if not text or not text.strip():
        raise RuntimeError("踩蘑菇接口返回空(可能触发限流)")
    return json.loads(text)


async def fetch_latest(force: bool = False) -> Dict[str, Any]:
    '''获取最新一期会战作业数据(磁盘缓存)。

    缓存无过期时间：只有 force(前端"重新拉作业数据"按钮，或会战开始日按通知时刻的自动更新)
    才重新抓取；force 失败回落旧缓存。 '''
    cached = load_cache()
    if cached and not force:
        return {**cached, "stale": False}
    try:
        data = await _request_json("/gzlj/data", {"date": "", "lang": "cn"})
        if data.get("status") != 1:
            raise RuntimeError(f"踩蘑菇接口status异常: {data.get('status')}")
        icons = None
        try:
            icons = await _request_json("/gzlj/data/icon", {"date": "", "lang": "cn"})
        except Exception:
            logger.exception("拉取踩蘑菇头像表失败，跳过")
        payload = {"fetched_at": int(time()), "data": data.get("data"), "icons": icons.get("data") if icons else None}
        save_cache(payload)
        return {**payload, "stale": False}
    except Exception as e:
        if cached:
            logger.exception("拉取踩蘑菇数据失败，使用过期缓存")
            return {**cached, "stale": True, "error": str(e)}
        raise


# 会战阶段口径：sn首字母=周目(B=2,C=3,D=4,E=5)；本会战仅B/C/DE三阶段，4~5周目合并为DE
STAGE_OF = {"B": "B", "C": "C", "D": "DE", "E": "DE"}


def parse_battle(payload: Dict[str, Any]) -> Dict[str, Any]:
    '''把缓存payload解析为结构化会战数据(纯计算，不发请求)'''
    boss_names: Dict[int, str] = {}
    unit_names: Dict[int, str] = {}
    icons = payload.get("icons")
    if icons and len(icons) >= 4:
        try:
            for icon in icons[3]:
                name = (icon.get("iconValue") or "").strip()
                if name:
                    boss_names[int(icon["id"])] = name
            for group in icons[:3]:
                for icon in group:
                    name = (icon.get("iconValue") or "").strip()
                    if name:
                        unit_names[int(icon["id"])] = name
        except Exception:
            logger.exception("解析踩蘑菇头像表失败")

    bosses: List[Dict[str, Any]] = []
    boss_order: Dict[str, int] = {}
    comps: List[Dict[str, Any]] = []
    unit_usage: Counter = Counter()
    unit_best: Dict[int, int] = {}
    unit_bosses: Dict[int, set] = defaultdict(set)

    for boss in payload.get("data") or []:
        try:
            bid = int(boss["id"])
            stage = int(boss.get("stage", 0))
            name = boss_names.get(bid, f"BOSS{bid}")
            # 分数倍率：伤害×rate=分数；接口用-1表示无倍率的阶段(如1/4周目)，归一成None
            rate = float(boss.get("rate") or 0)
            rate = rate if rate > 0 else None
        except Exception:
            logger.exception(f"解析踩蘑菇boss条目失败: {boss}")
            continue
        homework = boss.get("homework") or []
        if name not in boss_order:
            boss_order[name] = len(bosses)
            bosses.append({"name": name, "boss_id": bid, "stages": [], "count": 0})
        entry = bosses[boss_order[name]]
        entry["stages"].append(stage)
        entry["count"] += len(homework)
        # try收窄到单条作业：一条脏数据不能丢掉该boss剩余全部作业
        for hw in homework:
            try:
                units = [int(u) for u in hw.get("unit") or []]
                damage = int(hw.get("damage") or 0)
                videos = [{"text": (v.get("text") or "").replace("\n", " ").strip(), "url": (v.get("url") or "").strip()}
                          for v in hw.get("video") or [] if (v.get("text") or "").strip() or (v.get("url") or "").strip()]
                text = videos[0]["text"] if videos else ""
                url = videos[0]["url"] if videos else ""
                sn = hw.get("sn", "")
                # boss位数字（sn=面别字母+可选T/W+boss位+序号），供倍率表等按boss聚合
                m = re.match(r"^[A-E][TW]?(\d)\d+$", sn)
                comps.append({
                    "boss": name,
                    "stage": stage,
                    # 尾刀口径在数据建模处一次定死：remain非空即尾刀
                    "knife": "尾刀" if hw.get("remain") else classify_knife(hw),
                    "sn": sn,
                    "stage_key": STAGE_OF.get(sn[:1]),
                    "boss_idx": int(m.group(1)) if m else None,
                    "unit": units,
                    "damage": damage,
                    "rate": rate,
                    "text": text,
                    "url": url,
                    "videos": videos,
                })
                for uid in units:
                    unit_usage[uid] += 1
                    unit_bosses[uid].add(name)
                    if damage > unit_best.get(uid, 0):
                        unit_best[uid] = damage
            except Exception:
                logger.exception(f"解析踩蘑菇作业条目失败: {hw.get('sn')}")

    # 半月刊启发式：月初5天内拉取的会战属于上月第2期；月中拉取按当月第1/2期
    fetched = payload.get("fetched_at", 0)
    d = datetime.datetime.fromtimestamp(fetched) if fetched else None
    if d is None:
        period = ""
    elif d.day <= 5:
        prev_month = d.month - 1 or 12
        period = f"{prev_month}月会战"
    else:
        period = f"{d.month}月会战"

    return {
        "fetched_at": payload.get("fetched_at", 0),
        "stale": payload.get("stale", False),
        "period": period,
        "bosses": bosses,
        "comps": comps,
        "unit_names": unit_names,
        "boss_names": boss_names,
        "unit_usage": dict(unit_usage),
        "unit_best": unit_best,
        "unit_bosses": {k: sorted(v) for k, v in unit_bosses.items()},
    }


def load_cached_battle() -> Dict[str, Any]:
    '''只读缓存的解析结果，不发网络请求(供模块配置候选项使用)'''
    payload = load_cache()
    if not payload:
        raise RuntimeError("踩蘑菇数据尚未拉取")
    return parse_battle(payload)
