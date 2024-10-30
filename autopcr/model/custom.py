from __future__ import annotations

from ..db.models import UnitStatusCoefficient
from .enums import eInventoryType, eParamType
from typing import List, Optional, Tuple, Counter as CounterType, Union
from collections import Counter
from pydantic import BaseModel, Field
from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal, ROUND_HALF_UP

ItemType = Tuple[eInventoryType, int]

@dataclass
class UnitAttribute:
    # 浮点误差
    hp: Decimal = Decimal(0)
    atk: Decimal = Decimal(0)
    magic_str: Decimal = Decimal(0)
    def_: Decimal = Decimal(0)
    magic_def: Decimal = Decimal(0)
    physical_critical: Decimal = Decimal(0)
    magic_critical: Decimal = Decimal(0)
    wave_hp_recovery: Decimal = Decimal(0)
    wave_energy_recovery: Decimal = Decimal(0)
    dodge: Decimal = Decimal(0)
    physical_penetrate: Decimal = Decimal(0)
    magic_penetrate: Decimal = Decimal(0)
    life_steal: Decimal = Decimal(0)
    hp_recovery_rate: Decimal = Decimal(0)
    energy_recovery_rate: Decimal = Decimal(0)
    energy_reduce_rate: Decimal = Decimal(0)
    accuracy: Decimal = Decimal(0)

    index2name = {
        eParamType.HP: "hp",
        eParamType.ATK: "atk",
        eParamType.MAGIC_ATK: "magic_str",
        eParamType.DEF: "def_",
        eParamType.MAGIC_DEF: "magic_def",
        eParamType.PHYSICAL_CRITICAL: "physical_critical",
        eParamType.MAGIC_CRITICAL: "magic_critical",
        eParamType.WAVE_HP_RECOVERY: "wave_hp_recovery",
        eParamType.WAVE_ENERGY_RECOVERY: "wave_energy_recovery",
        eParamType.DODGE: "dodge",
        eParamType.PHYSICAL_PENETRATE: "physical_penetrate",
        eParamType.MAGIC_PENETRATE: "magic_penetrate",
        eParamType.LIFE_STEAL: "life_steal",
        eParamType.HP_RECOVERY_RATE: "hp_recovery_rate",
        eParamType.ENERGY_RECOVERY_RATE: "energy_recovery_rate",
        eParamType.ENERGY_REDUCE_RATE: "energy_reduce_rate",
        eParamType.ACCURACY: "accuracy"
    }

    def __add__(self, oth: UnitAttribute):
        return UnitAttribute(**{key: getattr(self, key) + getattr(oth, key) for key in self.__annotations__})

    def __iadd__(self, oth: UnitAttribute):
        for key in self.__annotations__:
            setattr(self, key, getattr(self, key) + getattr(oth, key))
        return self

    def __mul__(self, oth: Union[int, float, Decimal]):
        if not isinstance(oth, Decimal):
            oth = Decimal(str(oth))
        return UnitAttribute(**{key: getattr(self, key) * oth for key in self.__annotations__})

    def round(self):
        ret = UnitAttribute()
        for key in self.__annotations__:
            setattr(ret, key, getattr(self, key).quantize(Decimal(1), rounding=ROUND_HALF_UP))
        return ret

    def ceil(self):
        ret = UnitAttribute()
        for key in self.__annotations__:
            setattr(ret, key, getattr(self, key).quantize(Decimal(1), rounding=ROUND_CEILING))
        return ret

    @staticmethod
    def load(data: object, pre: str = '', suf: str = '') -> UnitAttribute:
        ret = UnitAttribute()
        for key in ret.__annotations__:
            target = (pre + key.strip('_') + suf) if suf else key
            setattr(ret, key, Decimal(str(getattr(data, target, 0))))
        return ret

    def set_value(self, type: int, value: Union[int, float, Decimal]):
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        if type in self.index2name:
            setattr(self, self.index2name[type], value)

    def get_power(self, coefficient: UnitStatusCoefficient) -> float:
        pow = self.hp.quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(coefficient.hp_coefficient)
        pow += self.atk.quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(coefficient.atk_coefficient)
        pow += self.magic_str.quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(coefficient.magic_str_coefficient)
        pow += self.def_.quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(coefficient.def_coefficient)
        pow += self.magic_def.quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(coefficient.magic_def_coefficient)
        pow += self.physical_critical * Decimal(coefficient.physical_critical_coefficient)
        pow += self.magic_critical * Decimal(coefficient.magic_critical_coefficient)
        pow += self.dodge * Decimal(coefficient.dodge_coefficient)
        pow += self.physical_penetrate * Decimal(coefficient.physical_penetrate_coefficient)
        pow += self.magic_penetrate * Decimal(coefficient.magic_penetrate_coefficient)
        pow += self.wave_hp_recovery * Decimal(coefficient.wave_hp_recovery_coefficient)
        pow += self.wave_energy_recovery * Decimal(coefficient.wave_energy_recovery_coefficient)
        pow += self.life_steal * Decimal(coefficient.life_steal_coefficient)
        pow += self.hp_recovery_rate * Decimal(coefficient.hp_recovery_rate_coefficient)
        pow += self.energy_recovery_rate * Decimal(coefficient.energy_recovery_rate_coefficient)
        pow += self.energy_reduce_rate * Decimal(coefficient.energy_reduce_rate_coefficient)
        pow += self.accuracy * Decimal(coefficient.accuracy_coefficient)
        return float(pow)

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
    deff: List[ArenaQueryUnit] = Field(default = [], alias="def")
    up: int = 0
    down: int = 0
    iseditor: bool = False
    private: bool = False
    group: bool = False
    updated: str = ""
    comment: Optional[List[ArenaQueryComment]] = []
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

