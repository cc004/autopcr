"""Wire-format models required by the JJC simulator transport."""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class UnitData(BaseModel):
    """单位数据"""
    enemyid: int = 0
    unitId: int = 0
    level: int = 1
    rarity: int = 1
    love: int = 0                          # 好感度
    rank: int = 1
    equipLevel: List[int] = Field(default_factory=lambda: [-1, -1, -1, -1, -1, -1])  # 装备等级，-1-未装备，0~5表示强化等级
    skillLevel: List[int] = Field(default_factory=lambda: [1, 1, 1, 1])  # 技能等级，0123对应UB/技能1/技能2/EX技能
    playLoveDic: Dict[int, int] = Field(default_factory=dict)
    uniqueEqLv: int = 0                  # 专武等级
    uniqueEq2Lv: int = -1                # 专武2等级
    exEquip: List[int] = Field(default_factory=lambda: [0, 0, 0])
    exEquipLevel: List[int] = Field(default_factory=lambda: [0, 0, 0])
    exEquipSubs: Dict[int, List[int]] = Field(default_factory=dict)
    name: Optional[str] = Field(default="", exclude=True)  # JSON序列化时忽略
    PrefabId: int = 0
    love2: int = 0

class GuildRandomSpecialData(BaseModel):
    """公会战随机特殊数据"""
    class UnitType(Enum):
        """单位类型"""
        BOSS = "BOSS"
        PLAYER1 = "PLAYER1"
        PLAYER2 = "PLAYER2"
        PLAYER3 = "PLAYER3"
        PLAYER4 = "PLAYER4"
        PLAYER5 = "PLAYER5"
        ALLPLAYER = "ALLPLAYER"

    fixTimeExec: bool = False
    startFream: int = 0
    endFream: int = 0
    fixCountExec: bool = False
    countEcexNum: int = 0
    sourceNum: UnitType = UnitType.BOSS

class GuildRandomData(BaseModel):
    """公会战随机数数据"""
    class LogBarrierType(Enum):
        """日志屏障类型"""
        NO_BARRIER = "NoBarrier"           # 无盾
        TP_ONLY = "TpOnly"                 # 无盾有tp
        FULL_BARRIER = "FullBarrier"       # 有盾

    DataName: str = "默认世界线"
    UseFixedRandomSeed: bool = False
    RandomSeed: int = 666
    ForceNoCritical_player: bool = False
    ForceNoCritical_enemy: bool = False
    ForceIgnoreDodge_player: bool = False
    ForceIgnoreDodge_enemy: bool = False
    ForceCritical_player: bool = False
    randomSpecialDatas: List[GuildRandomSpecialData] = Field(default_factory=list)
