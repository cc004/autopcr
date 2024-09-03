from typing import List, Set, Tuple
import json, asyncio, time
from os.path import join, exists
from random import choice, sample, choices

from ..model.custom import PLACEHOLDER, ArenaQueryType, ArenaQueryUnit, ArenaRegion, ArenaQueryResult, ArenaQueryResponse
from . import aiorequests, pcrdapi

try:
    from hoshino.modules.priconne.arena.arena import curpath as CACHE_DIR
except:
    from ..constants import CACHE_DIR

RECENTTIME = 3600 * 24 * 5

class ArenaQuery:
    bufferpath = join(CACHE_DIR, 'buffer')
    timepath = join(bufferpath, 'buffer.json')
    buffer = {}
    querylock = asyncio.Lock()

    def __init__(self):
        print(f"using cache {self.timepath}")
        if not exists(self.timepath):
            from os import makedirs
            from os.path import dirname
            makedirs(dirname(self.timepath), exist_ok = True)
            with open(self.timepath, 'w', encoding="utf-8") as fp:
                fp.write("{}")

        with open(self.timepath, 'r', encoding="utf-8") as fp:
            self.buffer = json.load(fp)

    _endpoint = 'https://api.pcrdfans.com/x/v1/search'
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Referer": "https://pcrdfans.com/",
        "Origin": "https://pcrdfans.com",
        "Accept": "*/*",
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "",
        "Host": "api.pcrdfans.com",
    }
    
    @staticmethod
    def _getNonce():
        return ''.join(choices("0123456789abcdefghijklmnopqrstuvwxyz", k=16))

    @staticmethod
    def _getTs():
        return int(time.time())

    @staticmethod
    def _get_query_payload(units, region):
        return {
            "def": units,
            "language": 0,
            "nonce": ArenaQuery._getNonce(),
            "page": 1,
            "region": region,
            "sort": 1,
            "ts": ArenaQuery._getTs()
        }

    @staticmethod
    def _dumps(x):
        return json.dumps(x, ensure_ascii=False).replace(' ', '')

    def save_buffer(self):
        with open(self.timepath, 'w', encoding="utf-8") as fp:
            json.dump(self.buffer, fp, ensure_ascii=False, indent=4)

    def result_path(self, key: str) -> str:
        return join(self.bufferpath, f'{key}.json') 

    def is_exist_result(self, key: str) -> bool:
        return exists(self.result_path(key))  

    def load_result(self, key: str) -> List[ArenaQueryResult]:
        with open(self.result_path(key), 'r', encoding="utf-8") as fp:
            ret = json.load(fp)
        return [ArenaQueryResult.parse_obj(o) for o in ret]

    def save_result(self, key: str, result: List[ArenaQueryResult]):
        timestamp = int(time.time())
        self.buffer[key] = timestamp
        self.save_buffer()

        with open(self.result_path(key), 'w', encoding="utf-8") as fp:
            json.dump([json.loads(ret.json(by_alias=True)) for ret in result], fp, indent=4, ensure_ascii=False)

    def is_recent_time(self, timestamp: int) -> bool:
        return int(time.time()) - timestamp < RECENTTIME

    def is_recent_buffer(self, key: str) -> bool:
        return self.is_recent_time(self.buffer.get(key, 0)) and self.is_exist_result(key)

    def key(self, defend: List[int], region: ArenaRegion) -> str:
        return ''.join([str(x // 100) for x in sorted(defend)]) + str(int(region))

    def anti_key(self, key: str) -> Tuple[List[int], ArenaRegion]:
        region = ArenaRegion(int(key[-1]))
        key = key[:-1]
        from textwrap import wrap
        units = list(map(lambda x: int(x) * 100 + 1, wrap(key, 4)))
        return (units, region)

    def save(self, defend: List[int], region: ArenaRegion, result: List[ArenaQueryResult]):
        key = self.key(defend, region)
        self.save_result(key, result)

    async def query(self, units: List[int], region: ArenaRegion) -> List[ArenaQueryResult]:
        result = await self.do_query(units, region)
        if result:
            self.save(units, region, result)
        return result

    async def do_query(self, units: List[int], region: ArenaRegion) -> List[ArenaQueryResult]:
        async with self.querylock:
            await asyncio.sleep(1)
            try:
                data = ArenaQuery._get_query_payload(units, region)
                data['_sign'] = pcrdapi.sign(ArenaQuery._dumps(data), data['nonce'])
                resp = await aiorequests.post(
                    ArenaQuery._endpoint,
                    headers=ArenaQuery._headers,
                    data=ArenaQuery._dumps(data).encode('utf8'),
                    timeout=5,
                )
                res = await resp.json()
                res = ArenaQueryResponse.parse_obj(res)
                if res.code:
                    raise ValueError(f'服务器报错：返回值{res.code}')
                return res.data.result if res.data else []
            except aiorequests.requests.ConnectionError as e:
                return []
            except aiorequests.requests.ReadTimeout as e:
                return []
            except Exception as e:
                raise e

    def is_approximate_team(self, lunits: List[int], lregion: ArenaRegion, units: List[int], region: ArenaRegion) -> bool:
        if lregion != region and lregion != ArenaRegion.ALL:
            return False
        return len(set(lunits) & set(units)) >= 4

    async def get_approximate_attack(self, units: List[int], region: ArenaRegion) -> List[ArenaQueryResult]:
        if len(units) > 5 or len(units) < 4:
            raise ValueError("仅支持4或5人的近似解查询")
        candidate: List[str] = [key for key in self.buffer if self.is_approximate_team(*self.anti_key(key), units, region)]
        result: List[ArenaQueryResult] = [ret.__setattr__('query_type', ArenaQueryType.APPROXIMATION) or ret for key in candidate for ret in self.load_result(key)]

        result = sorted(result, key=lambda x: self.attack_score(x), reverse=True)
        return result

    def attack_score(self, record: ArenaQueryResult) -> float: # the bigger, the better
        up_vote = record.up
        down_vote = record.down

        total_vote = up_vote + down_vote
        if total_vote == 0:
            return 0

        def mean(x) -> float:
            return (x[0] + x[1]) / 2

        from .statistics import wilson_score_interval as proportion_confint
        positive_rate_ci = proportion_confint(up_vote, total_vote)
        negative_rate_ci = proportion_confint(down_vote, total_vote)
        composite_score = mean(positive_rate_ci) - mean(negative_rate_ci)
        return composite_score 

    async def get_other_region_result(self, defen: List[int], region: ArenaRegion) -> List[ArenaQueryResult]:
        query_seq = {
            ArenaRegion.ALL: [ArenaRegion.CN, ArenaRegion.JP, ArenaRegion.TW],  
            ArenaRegion.CN: [ArenaRegion.ALL, ArenaRegion.TW, ArenaRegion.JP], 
            ArenaRegion.TW: [ArenaRegion.ALL, ArenaRegion.CN, ArenaRegion.JP],
            ArenaRegion.JP: [ArenaRegion.ALL, ArenaRegion.TW, ArenaRegion.CN]
        }

        query_seq = query_seq.get(region, [])
        result = []
        for other_region in query_seq:
            other_key = self.key(defen, other_region)
            if self.is_exist_result(other_key):
                print(f'存在它服({other_region})缓存，作为降级备用')
                result = self.load_result(other_key)
                break
        else:
            print(f'不存在它服缓存')
        return result

    async def get_attack(self, available_unit: Set[int], defen: List[int], region : ArenaRegion = ArenaRegion.CN) -> List[ArenaQueryResult]:
        result = []

        if len(defen) < 4:
            raise ValueError("暂不支持少于4人的搜索")
        elif len(defen) > 5:
            raise ValueError("不支持大于5人的搜索")
        elif len(defen) == 4:
            result = await self.get_approximate_attack(defen, region)
        else:
            key = self.key(defen, region)

            if self.is_recent_buffer(key):
                print(f'存在本服({region})近缓存，直接使用')
                result = self.load_result(key)
            else:
                degrade_result = self.load_result(key) if self.is_exist_result(key) else await self.get_other_region_result(defen, region)
                result = await self.query(defen, region)
                if not result:
                    if degrade_result:
                        print(f'使用缓存')
                        result = degrade_result
                    else:
                        print(f'查询近似解')
                        result = await self.get_approximate_attack(defen, region)

        result = [team for team in result if all(unit.id in available_unit for unit in team.atk)]
        result = sorted(result, key=lambda x: self.attack_score(x), reverse=True)
        return result

    def build_placeholder_result(self, units: List[int]) -> ArenaQueryResult:
        ret = ArenaQueryResult(down=10)
        ret.atk = [ArenaQueryUnit(id=unit, equip=False,star=5) for unit in units]
        ret.query_type = ArenaQueryType.PLACEHOLDER
        return ret

    def replace_placeholder(self, available_unit: Set[int], teams: List[ArenaQueryResult]) -> List[ArenaQueryResult]:
        placeholder = [index for index, value in enumerate(teams) if value == PLACEHOLDER]
        if len(placeholder) != 1:
            raise ValueError("仅支持替换一个占位符")
        placeholder = placeholder[0]

        candidate_unit = available_unit - set(unit.id for team in teams for unit in team.atk)
        candidates = [key for key in self.buffer if all(unit_id in candidate_unit for unit_id in self.anti_key(key)[0])]
        if candidates:
            candidates = self.anti_key(choice((candidates)))[0]
        else:
            candidates = sample(list(available_unit), 5)
        teams[placeholder] = self.build_placeholder_result(candidates)
        return teams

    def have_placeholder(self, teams: List[ArenaQueryResult]) -> bool:
        return PLACEHOLDER in teams

    async def get_multi_attack(self, available_unit: Set[int], defens: List[List[int]], region : ArenaRegion = ArenaRegion.CN) -> List[List[ArenaQueryResult]]:
        attacks = [await self.get_attack(available_unit, defen, region) + [PLACEHOLDER] for defen in defens]
        from itertools import product
        cartesian = product(*attacks)
        candidates: List[List[ArenaQueryResult]] = list(
                map(lambda x: list(x), 
                    filter(lambda x: len(set(unit.id for attack in x for unit in attack.atk)) == 
                           sum(1 for attack in x for unit in attack.atk), 
                           cartesian))) # only allow one placeholder

        candidates = [team if not self.have_placeholder(team) else self.replace_placeholder(available_unit, team) for team in candidates]
        candidates = sorted(candidates, key=lambda x: sum(self.attack_score(attack) for attack in x), reverse=True)
        return candidates

    def str_result(self, result: List[ArenaQueryResult]):
        msg = ""
        from ..db.database import db
        for id, ret in enumerate(result):
            head = f"{id + 1}. {db.format_date(db.parse_time(ret.updated)) if ret.updated else ''}:"
            tail = f"{ret.up}/{ret.down}"
            if ret.query_type == ArenaQueryType.APPROXIMATION:
                tail += f"(近似解)"
            elif ret.query_type == ArenaQueryType.PLACEHOLDER:
                tail = f"凑解"
            comment = '\n'.join([f"  | {db.format_date(db.parse_time(c.date)) if c.date else ''}: {c.msg.strip()}" for c in ret.comment[:3] if c.msg.strip()]) if ret.comment else "  | 无评论"
            msg += f'''{head}【{" ".join([db.get_unit_name(unit.id) for unit in ret.atk])}】 {tail}
{comment}
'''

        return msg

instance = ArenaQuery()
