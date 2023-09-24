from __future__ import annotations
from .enums import eInventoryType
from typing import List, Tuple, Counter as CounterType
from collections import Counter
from pydantic import BaseModel

ItemType = Tuple[eInventoryType, int]


class GachaReward():
    reward_list: List = None
    new_unit: List = None
    unit_rarity: CounterType = None
    prize_rarity: CounterType = None

    def __init__(self, resp=None):
        self.reward_list = []
        self.new_unit = []
        self.unit_rarity = Counter()
        self.prize_rarity = Counter()

        if resp: self.load_reward(resp)

    def load_reward(self, resp):
        self.new_unit += [item for item in resp.reward_info_list if item.type == eInventoryType.Unit]
        self.reward_list += [item for item in resp.reward_info_list if item.type != eInventoryType.Unit]

        self.unit_rarity += Counter(
            item.unit_data.unit_rarity for item in resp.reward_info_list if item.type == eInventoryType.Unit)
        self.unit_rarity += Counter(
            item.exchange_data.rarity for item in resp.reward_info_list if item.type != eInventoryType.Unit)

        if resp.prize_reward_info:
            self.prize_rarity += Counter(
                prize.rarity for prize in vars(resp.prize_reward_info).values() if prize is not None)
            self.reward_list += [item for prize in vars(resp.prize_reward_info).values() if prize is not None for item
                                 in prize.rewards]
        if resp.bonus_reward_info:
            self.reward_list += [item for item in vars(resp.bonus_reward_info).values() if item is not None]

    def __iadd__(self, oth: GachaReward):
        self.reward_list.extend(oth.reward_list)
        self.new_unit.extend(oth.new_unit)
        self.unit_rarity += oth.unit_rarity
        self.prize_rarity += oth.prize_rarity

        return self
