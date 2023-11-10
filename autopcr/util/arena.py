from typing import List, Tuple
import json, asyncio, time
from os.path import join, exists
from random import random
from math import log

from ..model.custom import PLACEHOLDER, ArenaRegion, ArenaQueryResult, ArenaQueryResponse
from . import aiorequests 

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

    def __get_query_ip(self):
        return "https://api.pcrdfans.com/x/v1/search"

    def __get_query_header(self):
        return {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
        "authorization": self.__get_auth_key(),
    }

    def __get_auth_key(self):
        key = ""
        try: 
            from hoshino.config.priconne import arena
            key = arena.AUTH_KEY
        except:
            from ..constants import AUTH_KEY
            key = AUTH_KEY
        if not key:
            raise ValueError("请配置key")
        return key

    def __get_query_payload(self, units, region):
        timestamp = int(time.time())
        return {
            "_sign": "a",
            "def": units,
            "nonce": "a",
            "page": 1,
            "sort": 1,
            "ts": timestamp,
            "region": region,
        }

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
                resp = await aiorequests.post(
                    self.__get_query_ip(),
                    headers=self.__get_query_header(),
                    json=self.__get_query_payload(units, region),
                    timeout=5,
                )
                res = await resp.json()
                res = ArenaQueryResponse.parse_obj(res)
                if res.code:
                    raise ValueError(f'服务器报错：返回值{res.code}')
                return res.data.result
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
        result: List[ArenaQueryResult] = [ret for key in candidate for ret in self.load_result(key)]

        result = sorted(result, key=lambda x: self.attack_score(x), reverse=True)
        return result

    def attack_score(self, record: ArenaQueryResult) -> float: # the bigger, the better
        up_vote = int(record.up)
        down_vote = int(record.down)
        val_1 = up_vote / (down_vote + up_vote + 0.0001) * 2 - 1  # 赞踩比占比 [-1, 1]
        val_2 = log(up_vote + down_vote + 0.01, 100)  # 置信度占比（log(100)）[-1,+inf]
        return val_1 + val_2 + random() / 1000  # 阵容推荐度权值

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

    async def get_attack(self, defen: List[int], region : ArenaRegion = ArenaRegion.CN) -> List[ArenaQueryResult]:
        if len(defen) < 4:
            raise ValueError("暂不支持少于4人的搜索")
        elif len(defen) > 5:
            raise ValueError("不支持大于5人的搜索")
        elif len(defen) == 4:
            return await self.get_approximate_attack(defen, region)

        key = self.key(defen, region)

        result = []
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
                    return await self.get_approximate_attack(defen, region)

        result = sorted(result, key=lambda x: self.attack_score(x), reverse=True)
        return result

    async def get_multi_attack(self, defens: List[List[int]], region : ArenaRegion = ArenaRegion.CN) -> List[List[ArenaQueryResult]]:
        attacks = [await self.get_attack(defen, region) + [PLACEHOLDER] for defen in defens]
        from itertools import product
        cartesian = product(*attacks)
        candidates: List[Tuple[ArenaQueryResult]] = list(filter(lambda x: len(set(unit.id for attack in x for unit in attack.atk)) == sum(1 for attack in x for unit in attack.atk) , cartesian)) # only allow one placeholder

        candidates = sorted(candidates, key=lambda x: sum(self.attack_score(attack) for attack in x), reverse=True)
        attacks = [list(attack) for attack in candidates]
        return attacks

    def str_result(self, result: List[ArenaQueryResult]):
        msg = ""
        from ..db.database import db
        for ret in result:
            msg += f'''【{" ".join([db.get_unit_name(unit.id) for unit in ret.atk])}】 {ret.up}/{ret.down}\n'''

        return msg

instance = ArenaQuery()
