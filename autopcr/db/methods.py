from typing import Iterator, Tuple, List
from ..model.common import eInventoryType
from ..model.custom import ItemType, UnitAttribute
from . import models

class Reward:
    def __init__(self, reward_type: int, reward_id: int, reward_num: int, odds: int):
        self.reward_item: ItemType = (eInventoryType(reward_type), reward_id)
        self.reward_num = reward_num
        self.odds = odds

def method(cls):
    base_cls = next(base_cls for base_cls in cls.__bases__ if cls.__name__ in base_cls.__name__)
    for method_name, method_obj in cls.__dict__.items():
        if method_name != "__init__" and callable(method_obj):
            setattr(base_cls, method_name, method_obj)
    return cls

@method
class PromotionBonus(models.PromotionBonus):
    def get_unit_attribute(self) -> UnitAttribute:
        return UnitAttribute.load(self)

@method
class UnitPromotionStatus(models.UnitPromotionStatus):
    def get_unit_attribute(self) -> UnitAttribute:
        return UnitAttribute.load(self)

@method
class UnitRarity(models.UnitRarity):
    def get_unit_attribute(self) -> UnitAttribute:
        return UnitAttribute.load(self)

    def get_unit_attribute_growth(self, level: int) -> UnitAttribute:
        return UnitAttribute.load(self, suf='_growth') * level

@method
class EquipmentDatum(models.EquipmentDatum):
    def get_unit_attribute(self) -> UnitAttribute:
        return UnitAttribute.load(self)

@method
class EquipmentEnhanceRate(models.EquipmentEnhanceRate):
    def get_unit_attribute(self, level: int) -> UnitAttribute:
        return UnitAttribute.load(self) * level

@method
class UniqueEquipmentDatum(models.UniqueEquipmentDatum):
    def get_unit_attribute(self) -> UnitAttribute:
        return UnitAttribute.load(self)

@method
class UniqueEquipEnhanceRate(models.UniqueEquipEnhanceRate):
    def get_unit_attribute(self, level: int) -> UnitAttribute:
        rate = UnitAttribute.load(self)
        if level < self.min_lv:
            return rate * 0
        elif self.max_lv == -1:
            return rate * (level - self.min_lv + 1)
        else:
            return rate * (min(self.max_lv, level) - self.min_lv + 1)

@method
class CharaStoryStatus(models.CharaStoryStatus):
    def get_unit_attribute(self) -> UnitAttribute:
        ret = UnitAttribute()
        for i in range(1, 5 + 1):
            type = getattr(self, f"status_type_{i}")
            value = getattr(self, f"status_rate_{i}")
            ret.set_value(type, value)
        return ret

    def get_effect_unit_ids(self) -> Iterator[int]:
        for i in range(1, 20 + 1):
            effect_unit_id = getattr(self, f"chara_id_{i}")
            if effect_unit_id != 0:
                yield effect_unit_id * 100 + 1

@method
class PrizegachaDatum(models.PrizegachaDatum):
    def get_prize_memory_id(self) -> Iterator[ItemType]:
        prize_memory_id_keys: List[str] = [i for i in self.__dict__.keys() if i.startswith("prize_memory_id_")]
        for prize_memory_id_key in prize_memory_id_keys: # fes池 20列 还会更多列
            prize_memory_id = getattr(self, prize_memory_id_key)
            if prize_memory_id != 0:
                yield (eInventoryType.Item, prize_memory_id)

@method
class EnemyRewardDatum(models.EnemyRewardDatum):
    def get_rewards(self) -> Iterator[Reward]:
        yield Reward(self.reward_type_1, self.reward_id_1, self.reward_num_1, self.odds_1)
        yield Reward(self.reward_type_2, self.reward_id_2, self.reward_num_2, self.odds_2)
        yield Reward(self.reward_type_3, self.reward_id_3, self.reward_num_3, self.odds_3)
        yield Reward(self.reward_type_4, self.reward_id_4, self.reward_num_4, self.odds_4)
        yield Reward(self.reward_type_5, self.reward_id_5, self.reward_num_5, self.odds_5)


@method
class EquipmentCraft(models.EquipmentCraft):
    def get_materials(self) -> Iterator[Tuple[ItemType, int]]:
        yield ((eInventoryType.Equip, self.condition_equipment_id_1), self.consume_num_1)
        yield ((eInventoryType.Equip, self.condition_equipment_id_2), self.consume_num_2)
        yield ((eInventoryType.Equip, self.condition_equipment_id_3), self.consume_num_3)
        yield ((eInventoryType.Equip, self.condition_equipment_id_4), self.consume_num_4)
        yield ((eInventoryType.Equip, self.condition_equipment_id_5), self.consume_num_5)
        yield ((eInventoryType.Equip, self.condition_equipment_id_6), self.consume_num_6)
        yield ((eInventoryType.Equip, self.condition_equipment_id_7), self.consume_num_7)
        yield ((eInventoryType.Equip, self.condition_equipment_id_8), self.consume_num_8)
        yield ((eInventoryType.Equip, self.condition_equipment_id_9), self.consume_num_9)
        yield ((eInventoryType.Equip, self.condition_equipment_id_10), self.consume_num_10)

@method
class QuestDatum(models.QuestDatum):
    def get_wave_group_ids(self) -> Iterator[int]:
        yield self.wave_group_id_1
        yield self.wave_group_id_2
        yield self.wave_group_id_3

@method
class WaveGroupDatum(models.WaveGroupDatum):
    def get_drop_reward_ids(self) -> Iterator[int]:
        yield self.drop_reward_id_1
        yield self.drop_reward_id_2
        yield self.drop_reward_id_3
        yield self.drop_reward_id_4
        yield self.drop_reward_id_5

@method
class TravelQuestDatum(models.TravelQuestDatum):
    def get_rewards(self) -> Iterator[Reward]:
        yield Reward(eInventoryType.ExtraEquip, self.main_reward_1, 1, 1)
        yield Reward(eInventoryType.ExtraEquip, self.main_reward_2, 1, 1)
        yield Reward(eInventoryType.ExtraEquip, self.main_reward_3, 1, 1)
        yield Reward(eInventoryType.ExtraEquip, self.main_reward_4, 1, 1)
        yield Reward(eInventoryType.ExtraEquip, self.main_reward_5, 1, 1)
