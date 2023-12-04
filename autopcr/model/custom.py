from __future__ import annotations
from .enums import eInventoryType
from typing import List, Optional, Tuple, Counter as CounterType
from collections import Counter
from pydantic import BaseModel, Field

ItemType = Tuple[eInventoryType, int]

class GachaReward():
    reward_list: List = None
    new_unit: List = None
    unit_rarity: CounterType = None
    prize_rarity: CounterType = None

    def __init__(self, resp = None):
        self.reward_list = []
        self.new_unit = []
        self.unit_rarity = Counter()
        self.prize_rarity = Counter()

        if resp: self.load_reward(resp)

    def load_reward(self, resp):
        self.new_unit += [item for item in resp.reward_info_list if item.type == eInventoryType.Unit]
        self.reward_list += [item for item in resp.reward_info_list if item.type != eInventoryType.Unit]

        self.unit_rarity += Counter(item.unit_data.unit_rarity for item in resp.reward_info_list if item.type == eInventoryType.Unit)
        self.unit_rarity += Counter(item.exchange_data.rarity for item in resp.reward_info_list if item.type != eInventoryType.Unit)

        if resp.prize_reward_info:
            self.prize_rarity += Counter(prize.rarity for prize in vars(resp.prize_reward_info).values() if prize is not None)
            self.reward_list += [item for prize in vars(resp.prize_reward_info).values() if prize is not None for item in prize.rewards]
        if resp.bonus_reward_info:
            self.reward_list += [item for item in vars(resp.bonus_reward_info).values() if item is not None]

    def __iadd__(self, oth: GachaReward):
        self.reward_list.extend(oth.reward_list)
        self.new_unit.extend(oth.new_unit)
        self.unit_rarity += oth.unit_rarity
        self.prize_rarity += oth.prize_rarity

        return self

from enum import IntEnum as Enum
class ArenaRegion(Enum):
    ALL = 1
    CN = 2
    TW = 3
    JP = 4
class ArenaQueryType(Enum):
    NORMAL = 0
    APPROXIMATION = 1
    PLACEHOLDER = 2

class ArenaQueryUnit(BaseModel):
    equip: bool 
    id: int 
    star: int 

class ArenaQueryComment(BaseModel):
    id: str
    date: str
    msg: str
    avatar: int

class ArenaQueryResult(BaseModel):
    id: str = ""
    atk: List[ArenaQueryUnit] = []
    up: int = 0
    down: int = 0
    iseditor: bool = False
    private: bool = False
    group: bool = False
    updated: str = ""
    # comment: List[ArenaQueryComment] = []
    liked: bool = False
    disliked: bool = False
    query_type: ArenaQueryType = ArenaQueryType.NORMAL

PLACEHOLDER = ArenaQueryResult(down=99999,atk=[ArenaQueryUnit(id=0, equip=False, star=0)])

class ArenaQueryPage(BaseModel):
    page: int 
    hasMore: bool

class ArenaQueryData(BaseModel):
    result: List[ArenaQueryResult]
    page: ArenaQueryPage

class ArenaQueryResponse(BaseModel):
    code: int 
    message: str
    data: Optional[ArenaQueryData]
    version: str

