from typing import List, Dict, Set, Tuple, Union
import typing
from ..model.enums import eCampaignCategory
from ..model.common import UnitData, eInventoryType, RoomUserItem, InventoryInfo
from ..model.custom import ItemType
import datetime
from collections import Counter, defaultdict
from .dbmgr import dbmgr
from .methods import *
from .models import *
from ..util.linq import flow
from queue import SimpleQueue
from .constdata import extra_drops
from ..core.apiclient import apiclient
from typing import TypeVar, Generic

T = TypeVar("T")

class lazy_property(Generic[T]):
    def __init__(self, func):
        self.func = func
        self.attr_name = f"__cached_{func.__name__}"
        self.version_attr = f"__cached_version_{func.__name__}"
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self # type: ignore

        dbmgr = getattr(instance, "dbmgr", None)
        if dbmgr is None:
            raise ValueError("数据库未初始化完成，请稍等片刻")
        current_version = dbmgr.ver
        cached = getattr(instance, self.attr_name, None)
        cached_version = getattr(instance, self.version_attr, None)

        if cached is None or current_version != cached_version:
            value = self.func(instance)  # 现在函数里自己处理 db
            setattr(instance, self.attr_name, value)
            setattr(instance, self.version_attr, current_version)
            return value

        return cached

class database():
    heart: ItemType = (eInventoryType.Equip, 140000)
    xinsui: ItemType = (eInventoryType.Equip, 140001)
    xingqiubei: ItemType = (eInventoryType.Item, 25001)
    zmana: ItemType = (eInventoryType.Gold, 94000)
    mana: ItemType = (eInventoryType.Gold, 94002)
    jewel: ItemType = (eInventoryType.Jewel, 91002)
    travel_speed_up_paper: ItemType = (eInventoryType.Item, 23002)
    gacha_single_ticket: ItemType = (eInventoryType.Item, 24001)

    def update(self, dbmgr):
        self.dbmgr = dbmgr

    @lazy_property
    def redeem_unit(self) -> Dict[int, Dict[int, RedeemUnit]]:
        with self.dbmgr.session() as db:
            return (
                RedeemUnit.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(lambda x: x.slot_id, lambda x: x))
            )

    @lazy_property
    def dear_story_data(self) -> Dict[int, DearStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                DearStoryDatum.query(db)
                .to_dict(lambda x: x.value, lambda x: x)
            )

    @lazy_property
    def dear_story_detail(self) -> Dict[int, Dict[int, DearStoryDetail]]:
        with self.dbmgr.session() as db:
            return (
                DearStoryDetail.query(db)
                .group_by(lambda x: x.story_group_id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(
                            lambda x: x.story_id, lambda x: x))
            )

    @lazy_property
    def seasonpass_level_reward(self) -> Dict[int, SeasonpassLevelReward]:
        with self.dbmgr.session() as db:
            return (
                SeasonpassLevelReward.query(db)
                .to_dict(lambda x: x.level_id, lambda x: x)
            )

    @lazy_property
    def seasonpass_foundation(self) -> Dict[int, SeasonpassFoundation]:
        with self.dbmgr.session() as db:
            return (
                SeasonpassFoundation.query(db)
                .to_dict(lambda x: x.season_id, lambda x: x)
            )

    @lazy_property
    def guild_data(self) -> Dict[int, Guild]:
        with self.dbmgr.session() as db:
            return (
                Guild.query(db)
                .to_dict(lambda x: x.guild_id, lambda x: x)
            )

    @lazy_property
    def normal_quest_data(self) -> Dict[int, QuestDatum]:
        with self.dbmgr.session() as db:
            return (
                QuestDatum.query(db)
                .where(lambda x: self.is_normal_quest(x.quest_id)) 
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

    @lazy_property
    def wave_groups(self) -> Dict[int, WaveGroupDatum]:
        with self.dbmgr.session() as db:
            return (
                WaveGroupDatum.query(db)
                .to_dict(lambda x: x.wave_group_id, lambda x: x)
            )

    @lazy_property
    def reward_groups(self) -> Dict[int, EnemyRewardDatum]:
        with self.dbmgr.session() as db:
            return (
                EnemyRewardDatum.query(db)
                .to_dict(lambda x: x.drop_reward_id, lambda x: x)
            )

    @lazy_property
    def normal_quest_rewards(self) -> Dict[int, typing.Counter[ItemType]]:
        return (
                flow(self.normal_quest_data.values())
            .to_dict(lambda x: x.quest_id, lambda x:
                flow(x.get_wave_group_ids())
                .where(lambda y: y != 0)
                .select_many(lambda y: self.wave_groups[y].get_drop_reward_ids() if y in self.wave_groups else [])
                .where(lambda y: y != 0)
                .select_many(lambda y: self.reward_groups[y].get_rewards() if y in self.reward_groups else [])
                .where(lambda y: y != 0 and y.reward_item[0] == eInventoryType.Equip)
                .select(lambda y: Counter({y.reward_item: y.reward_num * y.odds / 100.0}))
                .sum(seed=Counter()) + 
                extra_drops.get(x.quest_id // 1000, Counter())
            )
        )

    @lazy_property
    def unique_equipment_data(self) -> Dict[int, UniqueEquipmentDatum]:
        with self.dbmgr.session() as db:
            return (
                UniqueEquipmentDatum.query(db)
                .to_dict(lambda x: x.equipment_id, lambda x: x)
            )

    @lazy_property
    def unique_equip_enhance_rate(self) -> Dict[int, List[UniqueEquipEnhanceRate]]:
        with self.dbmgr.session() as db:
            return (
                UniqueEquipEnhanceRate.query(db)
                .group_by(lambda x: x.equipment_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )
        
    @lazy_property
    def unique_equip_rank(self) -> Dict[int, Dict[int, UniqueEquipmentEnhanceDatum]]:
            with self.dbmgr.session() as db:
                return ( 
                UniqueEquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.equip_slot)
                .to_dict(lambda x: x.key, lambda x: x
                .group_by(lambda x: x.rank)
                .to_dict(lambda x: x.key, lambda x: x.max(lambda y: y.enhance_level)))
        )

    @lazy_property
    def equip_craft(self) -> Dict[ItemType, List[Tuple[ItemType, int]]]:
        with self.dbmgr.session() as db:
            return (
                EquipmentCraft.query(db)
                .to_dict(lambda x: (eInventoryType.Equip, x.equipment_id), lambda x: 
                    flow(x.get_materials())
                    .where(lambda y: y[0][1] != 0 and y[1] != 0)
                    .to_list()
                )
            )

    @lazy_property
    def equip_craft_mana(self) -> Dict[ItemType, int]:
        with self.dbmgr.session() as db:
            return (
                EquipmentCraft.query(db)
                .to_dict(lambda x: (eInventoryType.Equip, x.equipment_id), lambda x: x.crafted_cost
                )
            )

    @lazy_property
    def unit_status_coefficient(self) -> Dict[int, UnitStatusCoefficient]:
        with self.dbmgr.session() as db:
            return (
                UnitStatusCoefficient.query(db)
                .to_dict(lambda x: x.coefficient_id, lambda x: x)
            )

    @lazy_property
    def promote_bonus(self) -> Dict[int, Dict[int, PromotionBonus]]:
        with self.dbmgr.session() as db:
            return (
                PromotionBonus.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x: 
                    x.to_dict(lambda x: x.promotion_level, lambda x: x))
            )

    @lazy_property
    def unit_promotion(self) -> Dict[int, Dict[int, UnitPromotion]]:
        with self.dbmgr.session() as db:
            return (
                UnitPromotion.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x:
                    x.to_dict(lambda y: y.promotion_level, lambda y: y
                    )
                )
            )

    @lazy_property
    def unit_promotion_status(self) -> Dict[int, Dict[int, UnitPromotionStatus]]:
        with self.dbmgr.session() as db:
            return (
                UnitPromotionStatus.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x:
                    x.to_dict(lambda y: y.promotion_level, lambda y: y
                     )
                 )
            )

    @lazy_property
    def unit_promotion_equip_count(self) -> Dict[int, Dict[int, typing.Counter[ItemType]]]:
        with self.dbmgr.session() as db:
            return (
                UnitPromotion.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x:
                    x.to_dict(lambda y: y.promotion_level, lambda y:
                        Counter(flow(range(1, 7))
                        .select(lambda z: (eInventoryType.Equip, getattr(y, f'equip_slot_{z}')))
                        .where(lambda z: z[1] != 999999)
                        .to_list()
                    ))
                )
            )

    @lazy_property
    def equip_max_rank(self) -> int:
        return max(
            max(x.keys()) for x in self.unit_promotion.values()
        )

    @lazy_property
    def equip_max_rank_equip_num(self) -> int:
        return max(
            len(x.get(self.equip_max_rank, {})) for x in self.unit_promotion_equip_count.values()
        )

    @lazy_property
    def equip_max_rank_equip_slot(self) -> List[bool]:
        return [ # 简洁
                [False, True, False, True, False, True],
                [False, True, False, True, True, True],
                [False, True, True, True, True, True],
        ][self.equip_max_rank_equip_num - 3]

    @lazy_property
    def unique_equipment_max_rank(self) -> Dict[int, int]:
        return {
                equip_slot: max(self.unique_equip_rank[equip_slot].keys()) for equip_slot in self.unique_equip_rank
            }

    @lazy_property
    def hatsune_boss(self) -> Dict[int, HatsuneBoss]:
        with self.dbmgr.session() as db:
            return (
                HatsuneBoss.query(db)
                .to_dict(lambda x: x.boss_id, lambda x: x)
            )

    @lazy_property
    def hatsune_schedule(self) -> Dict[int, HatsuneSchedule]:
        with self.dbmgr.session() as db:
            return (
                HatsuneSchedule.query(db)
                .to_dict(lambda x: x.event_id, lambda x: x)
            )

    @lazy_property
    def campaign_beginner_data(self) -> Dict[int, CampaignBeginnerDatum]:
        with self.dbmgr.session() as db:
            return (
                CampaignBeginnerDatum.query(db)
                .to_dict(lambda x: x.beginner_id, lambda x: x)
            )

    @lazy_property
    def campaign_schedule(self) -> Dict[int, CampaignSchedule]:
        with self.dbmgr.session() as db:
            return (
                CampaignSchedule.query(db)
                .to_dict(lambda x: x.id, lambda x: x)
            )

    @lazy_property
    def pure_memory_quest(self) -> Dict[ItemType, List[QuestDatum]]:
        with self.dbmgr.session() as db:
            return (
                QuestDatum.query(db)
                .where(lambda x: self.is_very_hard_quest(x.quest_id))
                .group_by(lambda x: x.reward_image_1)
                .to_dict(lambda x: (eInventoryType.Item, x.key), lambda x:
                         x.to_list()[::-1]
                )
            )

    @lazy_property
    def memory_hard_quest(self) -> Dict[ItemType, List[QuestDatum]]:
        with self.dbmgr.session() as db:
            return (
                QuestDatum.query(db)
                .where(lambda x: self.is_hard_quest(x.quest_id))
                .group_by(lambda x: x.reward_image_1)
                .to_dict(lambda x: (eInventoryType.Item, x.key), lambda x:
                         x.to_list()[::-1]
                )
            )

    @lazy_property
    def memory_shiori_quest(self) -> Dict[ItemType, List[ShioriQuest]]:
        with self.dbmgr.session() as db:
            return (
                ShioriQuest.query(db)
                .where(lambda x: self.is_shiori_hard_quest(x.quest_id))
                .group_by(lambda x: x.drop_reward_id)
                .to_dict(lambda x: (eInventoryType.Item, x.key), lambda x:
                         x.to_list()[::-1]
                )
            )

    @lazy_property
    def team_info(self) -> Dict[int, ExperienceTeam]:
        with self.dbmgr.session() as db:
            return (
                ExperienceTeam.query(db)
                .to_dict(lambda x: x.team_level, lambda x: x)
            )

    @lazy_property
    def team_max_level(self) -> int:
        return max(self.team_info.keys()) - 1

    @lazy_property
    def unit_unique_equip(self) -> Dict[int, Dict[int, UnitUniqueEquipment]]:
        with self.dbmgr.session() as db:
            return (
                    UnitUniqueEquipment.query(db)
                    .group_by(lambda x: x.equip_slot)
                    .to_dict(lambda x: x.key, lambda x: 
                        x.to_dict(lambda x: x.unit_id, lambda x: x))
                )

    @lazy_property
    def unique_equipment_enhance_data(self) -> Dict[int, Dict[int, UniqueEquipmentEnhanceDatum]]:
        with self.dbmgr.session() as db:
            return (
                UniqueEquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.equip_slot)
                .to_dict(lambda x: x.key, lambda x: 
                     x.to_dict(lambda x: x.enhance_level, lambda x: x))
            )

    @lazy_property
    def unique_equipment_rank_up(self) -> Dict[int, Dict[int, UniqueEquipmentRankup]]:
        with self.dbmgr.session() as db:
            return (
                UniqueEquipmentRankup.query(db)
                .group_by(lambda x: x.equip_id)
                .to_dict(lambda x: x.key, lambda x: x
                    .to_dict(lambda x: x.unique_equip_rank, lambda x: x))
            )

    @lazy_property
    def unique_equipment_max_level(self) -> Dict[int, int]:
        ret = {
            equip_slot: max(self.unique_equipment_enhance_data[equip_slot].keys()) for equip_slot in self.unique_equipment_enhance_data
        }
        ret[1] = (self.team_max_level + 9) // 10 * 10 # 手动修正
        return ret

    @lazy_property
    def exceed_level_unit_required(self) -> Dict[int, ExceedLevelUnit]:
        with self.dbmgr.session() as db:
            return (
                ExceedLevelUnit.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

    @lazy_property
    def unit_rarity(self) -> Dict[int, Dict[int, UnitRarity]]:
        with self.dbmgr.session() as db:
            return (
                UnitRarity.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x: x
                    .to_dict(lambda x: x.rarity, lambda x: x))
                )
        
    @lazy_property
    def rarity_up_required(self) -> Dict[int, Dict[int, typing.Counter[ItemType]]]:
        with self.dbmgr.session() as db:
            return (
                UnitRarity.query(db)
                .select(lambda x: (
                    x.unit_id,
                    x.rarity,
                    (eInventoryType(eInventoryType.Item), x.unit_material_id),
                    x.consume_num
                ))
                .concat(
                    UnlockRarity6.query(db)
                    .group_by(lambda x: (x.unit_id, (eInventoryType(eInventoryType.Item), x.material_id))) # 感觉有点奇怪，别问，问就是Itemtype != MaterialType
                    .select(lambda x: (
                        x.key[0],
                        6,
                        x.key[1],
                        x.sum(lambda y: y.material_count)
                    )
                ))
                .group_by(lambda x: x[0])
                .to_dict(lambda x: x.key, lambda x:
                    x.group_by(lambda y: y[1])
                    .to_dict(lambda y: y.key, lambda y:
                        Counter(y.group_by(lambda z: z[2])
                        .to_dict(lambda z: z.key, lambda z: z.sum(lambda w: w[3]))
                        )
                    )
                )
            )

    @lazy_property
    def unique_equip_required(self) -> Dict[int, Dict[int, typing.Counter[ItemType]]]:
        with self.dbmgr.session() as db:
            return (
                UniqueEquipmentCraft.query(db)
                .select_many(lambda x: [(
                    x.equip_id,
                    int(0),
                    eInventoryType(x.reward_type_1),
                    x.item_id_1,
                    x.consume_num_1
                ), (
                    x.equip_id,
                    0,
                    eInventoryType(x.reward_type_2),
                    x.item_id_2,
                    x.consume_num_2
                )])
                .concat(
                    UniqueEquipmentRankup.query(db)
                    .select_many(lambda x: [(
                        x.equip_id,
                        x.unique_equip_rank,
                        eInventoryType(x.reward_type_1),
                        x.item_id_1,
                        x.consume_num_1
                    ), (
                        x.equip_id,
                        x.unique_equip_rank,
                        eInventoryType(x.reward_type_2),
                        x.item_id_2,
                        x.consume_num_2
                    )])
                )
                .select(lambda x: (
                    x[0],
                    x[1],
                    self.xinsui[0],
                    self.xinsui[1],
                    x[4] * 10
                ) if (x[2], x[3]) == self.heart else x)
                .group_by(lambda x: x[0])
                .to_dict(lambda x: x.key, lambda x:
                    x.group_by(lambda y: y[1])
                    .to_dict(lambda y: y.key, lambda y:
                        Counter(y.group_by(lambda z: (z[2], z[3]))
                        .to_dict(lambda z: z.key, lambda z: z.sum(lambda w: w[4]))
                        )
                    )
                )
            )

    @lazy_property
    def dungeon_area(self) -> Dict[int, DungeonArea]:
        with self.dbmgr.session() as db:
            return (
                DungeonArea.query(db)
                .where(lambda x: self.is_dungeon_id(x.dungeon_area_id))
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x)
            )

    @lazy_property
    def secret_dungeon_area(self) -> Dict[int, DungeonArea]:
        with self.dbmgr.session() as db:
            return (
                DungeonArea.query(db)
                .where(lambda x: self.is_secret_dungeon_id(x.dungeon_area_id))
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x)
            )

    @lazy_property
    def secret_dungeon_schedule(self) -> Dict[int, SecretDungeonSchedule]:
        with self.dbmgr.session() as db:
            return (
                SecretDungeonSchedule.query(db)
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x)
            )

    @lazy_property
    def training_quest_exp(self) -> Dict[int, TrainingQuestDatum]:
        with self.dbmgr.session() as db:
            return (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21002)
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

    @lazy_property
    def training_quest_mana(self) -> Dict[int, TrainingQuestDatum]:
        with self.dbmgr.session() as db:
            return (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21001)
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )
        
    @lazy_property
    def chara_fortune_schedule(self) -> Dict[int, CharaFortuneSchedule]:
        with self.dbmgr.session() as db:
            return (
                CharaFortuneSchedule.query(db)
                .to_dict(lambda x: x.fortune_id, lambda x: x)
            )

    @lazy_property
    def clan_battle_period(self) -> Dict[int, ClanBattlePeriod]:
        with self.dbmgr.session() as db:
            return (
                ClanBattlePeriod.query(db)
                .to_dict(lambda x: x.clan_battle_id, lambda x: x)
            )

    @lazy_property
    def quest_info(self) -> Dict[int, QuestDatum]:
        with self.dbmgr.session() as db:
            return (
                QuestDatum.query(db)
                .concat(HatsuneQuest.query(db))
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

    @lazy_property
    def chara_story_status(self) -> Dict[int, CharaStoryStatus]:
        with self.dbmgr.session() as db:
            return (
                CharaStoryStatus.query(db)
                .to_dict(lambda x: x.story_id, lambda x: x)
            )

    @lazy_property
    def chara2story(self) -> Dict[int, List[CharaStoryStatus]]:
        ret = defaultdict(list)
        for story in self.chara_story_status.values():
            for unit_id in story.get_effect_unit_ids():
                ret[unit_id].append(story)
        return ret
        
    @lazy_property
    def guild_story(self) -> List[StoryDetail]:
        with self.dbmgr.session() as db:
            return (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 3000000 and x.story_id < 4000000)
                .to_list()
            )

    @lazy_property
    def birthday_story(self) -> List[StoryDetail]:
        with self.dbmgr.session() as db:
            return (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 4010000 and x.story_id < 4020000)
                .to_list()
            )

    @lazy_property
    def main_story(self) -> List[StoryDetail]:
        with self.dbmgr.session() as db:
            return (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 2000000 and x.story_id < 3000000)
                .concat(
                    BywayStoryDetail.query(db)
                )
                .to_list()
            )

    @lazy_property
    def tower_story(self) -> List[TowerStoryDetail]:
        with self.dbmgr.session() as db:
            return (
                TowerStoryDetail.query(db)
                .to_list()
            )

    @lazy_property
    def tower_area(self) -> Dict[int, TowerAreaDatum]:
        with self.dbmgr.session() as db:
            return (
                TowerAreaDatum.query(db)
                .to_dict(lambda x: x.max_floor_num, lambda x: x)
            )

    @lazy_property
    def tower_quest(self) -> Dict[int, TowerQuestDatum]:
        with self.dbmgr.session() as db:
            return (
                TowerQuestDatum.query(db)
                .to_dict(lambda x: x.tower_quest_id, lambda x: x)
            )

    @lazy_property
    def tdf_schedule(self) -> Dict[int, TdfSchedule]:
        with self.dbmgr.session() as db:
            return (
                TdfSchedule.query(db)
                .to_dict(lambda x: x.schedule_id, lambda x: x)
            )

    @lazy_property
    def event_story_data(self) -> Dict[int, EventStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                EventStoryDatum.query(db)
                .to_dict(lambda x: x.story_group_id, lambda x: x)
            )

    @lazy_property
    def event_name(self) -> Dict[int, str]:
        with self.dbmgr.session() as db:
            return (
                EventStoryDatum.query(db)
                .select(lambda x: (x.story_group_id + 5000, x.title))
                .concat(
                    EventStoryDatum.query(db)
                    .select(lambda x: (x.value, x.title))
                ).to_dict(lambda x: x[0], lambda x: x[1])
            )

    @lazy_property
    def event_story_detail(self) -> List[EventStoryDetail]:
        with self.dbmgr.session() as db:
            return (
                EventStoryDetail.query(db)
                .to_list()
            )

    @lazy_property
    def unit_story(self) -> List[StoryDetail]:
        with self.dbmgr.session() as db:
            return (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 1000000 and x.story_id < 2000000)
                #.select(lambda x: (x.story_id, x.pre_story_id, x.story_group_id, x.love_level, x.title))
                .to_list()
            )

    @lazy_property
    def equip_data(self) -> Dict[int, EquipmentDatum]:
        with self.dbmgr.session() as db:
            return (
                EquipmentDatum.query(db)
                .to_dict(lambda x: x.equipment_id, lambda x: x)
            )

    @lazy_property
    def equip_promotion_to_raw_ore(self) -> Dict[int, ItemType]:
        with self.dbmgr.session() as db:
            return (
                EquipmentDatum.query(db)
                .where(lambda x: self.is_equip_raw_ore((eInventoryType.Equip, x.equipment_id)))
                .to_dict(lambda x: x.promotion_level, lambda x: (eInventoryType.Equip, x.equipment_id))
            )

    @lazy_property
    def skill_cost(self) -> Dict[int, int]:
        with self.dbmgr.session() as db:
            return (
                SkillCost.query(db)
                .to_dict(lambda x: x.target_level, lambda x: x.cost)
            )

    @lazy_property
    def skill_action(self) -> Dict[int, SkillAction]:
        with self.dbmgr.session() as db:
            return (
                SkillAction.query(db)
                .to_dict(lambda x: x.action_id, lambda x: x)
            )

    @lazy_property
    def skill_data(self) -> Dict[int, SkillDatum]:
        with self.dbmgr.session() as db:
            return (
                SkillDatum.query(db)
                .to_dict(lambda x: x.skill_id, lambda x: x)
            )

    @lazy_property
    def unit_skill_data(self) -> Dict[int, UnitSkillDatum]:
        with self.dbmgr.session() as db:
            return (
                UnitSkillDatum.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

    @lazy_property
    def experience_unit(self) -> Dict[int, int]:
        with self.dbmgr.session() as db:
            return (
                ExperienceUnit.query(db)
                .to_dict(lambda x: x.unit_level, lambda x: x.total_exp)
            )

    @lazy_property
    def equipment_enhance_data(self) -> Dict[int, Dict[int, EquipmentEnhanceDatum]]:
        with self.dbmgr.session() as db:
            return (
                EquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.promotion_level)
                .to_dict(lambda x: x.key, lambda x: 
                     x.to_dict(lambda x: x.equipment_enhance_level, lambda x: x))
            )

    @lazy_property
    def equipment_enhance_rate(self) -> Dict[int, EquipmentEnhanceRate]:
        with self.dbmgr.session() as db:
            return (
                EquipmentEnhanceRate.query(db)
                .to_dict(lambda x: x.equipment_id, lambda x: x)
            )

    @lazy_property
    def inventory_name(self) -> Dict[ItemType, str]:
        ret = {}
        with self.dbmgr.session() as db:
            ret = (
                EquipmentDatum.query(db)
                .select(lambda x: (eInventoryType(eInventoryType.Equip), x.equipment_id, x.equipment_name))
                .concat(
                    ItemDatum.query(db)
                    .select(lambda x: (eInventoryType.Item, x.item_id, x.item_name))
                )
                .concat(
                    UnitDatum.query(db)
                    .select(lambda x: (eInventoryType.Unit, x.unit_id, x.unit_name))
                )
                .concat(
                    RoomItem.query(db)
                    .select(lambda x: (eInventoryType.RoomItem, x.id, x.name))
                )
                .concat(
                    EmblemDatum.query(db)
                    .select(lambda x: (eInventoryType.Emblem, x.emblem_id, x.emblem_name))
                )
                .concat(
                    CustomMypage.query(db)
                    .select(lambda x: (eInventoryType.CustomMypage, x.still_id, x.still_name))
                )
                .concat(
                    ExEquipmentDatum.query(db)
                    .select(lambda x: (eInventoryType.ExtraEquip, x.ex_equipment_id, x.name))
                )
                .to_dict(lambda x: (x[0], x[1]), lambda x: x[2])
            )

        ret[(eInventoryType.Stamina, 93001)] = "体力"
        ret[(eInventoryType.TeamExp, 92001)] = "经验"
        ret[(eInventoryType.Jewel, 91002)] = "宝石"
        ret[(eInventoryType.Gold, 94002)] = "mana"
        ret[(eInventoryType.SeasonPassPoint, 98002)] = "祝福经验值"
        ret[(eInventoryType.SeasonPassStamina, 93002)] = "星尘体力药剂"
        return ret

    @lazy_property
    def room_item(self) -> Dict[int, RoomItem]:
        with self.dbmgr.session() as db:
            return (
                RoomItem.query(db)
                .to_dict(lambda x: x.id, lambda x: x)
            )

    @lazy_property
    def room_item_detail(self) -> Dict[int, Dict[int, RoomItemDetail]]:
            with self.dbmgr.session() as db:
                return ( # id, level
                RoomItemDetail.query(db)
                .group_by(lambda x: x.room_item_id)
                .to_dict(lambda x: x.key, lambda x: 
                    x.to_dict(lambda x: x.level, lambda x: x))
        )
        
    @lazy_property
    def daily_mission_data(self) -> Dict[int, DailyMissionDatum]:
        with self.dbmgr.session() as db:
            return (
                DailyMissionDatum.query(db)
                .to_dict(lambda x: x.daily_mission_id, lambda x: x)
            )

    @lazy_property
    def season_pack(self) -> Dict[int, SeasonPack]:
        with self.dbmgr.session() as db:
            return (
                SeasonPack.query(db)
                .where(lambda x: x.mission_id != 0)
                .to_dict(lambda x: x.mission_id, lambda x: x)
            )

    @lazy_property
    def stationary_mission_data(self) -> Dict[int, StationaryMissionDatum]:
        with self.dbmgr.session() as db:
            return (
                StationaryMissionDatum.query(db)
                .to_dict(lambda x: x.stationary_mission_id, lambda x: x)
            )

    @lazy_property
    def emblem_mission_data(self) -> Dict[int, EmblemMissionDatum]:
        with self.dbmgr.session() as db:
            return (
                EmblemMissionDatum.query(db)
                .to_dict(lambda x: x.mission_id, lambda x: x)
            )

    @lazy_property
    def memory_to_unit(self) -> Dict[int, int]:
        with self.dbmgr.session() as db:
            return (
                UnitRarity.query(db)
                .group_by(lambda x: x.unit_material_id)
                .to_dict(lambda x: x.key, lambda x: x.first().unit_id)
            )
    @lazy_property
    def unit_to_memory(self) -> Dict[int, int]:
        return {
            value: key for key, value in self.memory_to_unit.items()
        }

    @lazy_property
    def growth_parameter(self) -> Dict[int, GrowthParameter]:
        with self.dbmgr.session() as db:
            return (
                GrowthParameter.query(db)
                .to_dict(lambda x: x.growth_id, lambda x: x)
            )

    @lazy_property
    def growth_parameter_unique(self) -> Dict[int, GrowthParameterUnique]:
        with self.dbmgr.session() as db:
            return (
                GrowthParameterUnique.query(db)
                .to_dict(lambda x: x.growth_id, lambda x: x)
            )

    @lazy_property
    def unit_data(self) -> Dict[int, UnitDatum]:
        with self.dbmgr.session() as db:
            return (
                UnitDatum.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

    @lazy_property
    def unlock_unit_condition(self) -> Dict[int, UnlockUnitCondition]:
        with self.dbmgr.session() as db:
            return (
                UnlockUnitCondition.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

    @lazy_property
    def unit_kana_ids(self) -> Dict[str, List[int]]:
        with self.dbmgr.session() as db:
            return (
                UnitDatum.query(db)
                .where(lambda x: x.unit_id in self.unlock_unit_condition)
                .group_by(lambda x: x.kana)
                .to_dict(lambda x: x.key, lambda x: x.select(lambda y: y.unit_id).to_list())
            )

    @lazy_property
    def pure_memory_to_unit(self) -> Dict[ItemType, int]:
        with self.dbmgr.session() as db:
            return (
                UnlockRarity6.query(db)
                .where(lambda x: x.slot_id == 1)
                .to_dict(lambda x: (eInventoryType.Item, x.material_id), lambda x: x.unit_id)
            )
    @lazy_property
    def unit_to_pure_memory(self) -> Dict[int, ItemType]:
        return {
            value: key for key, value in self.pure_memory_to_unit.items()
        }

    @lazy_property
    def six_area(self) -> Dict[int, QuestDatum]:
        with self.dbmgr.session() as db:
            return (
                QuestDatum.query(db)
                .where(lambda x: self.is_very_hard_quest(x.quest_id))
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

    @lazy_property
    def login_bonus_data(self) -> Dict[int, LoginBonusDatum]:
        with self.dbmgr.session() as db:
            return (
                LoginBonusDatum.query(db)
                .to_dict(lambda x: x.login_bonus_id, lambda x: x)
            )

    @lazy_property
    def tower_schedule(self) -> Dict[int, TowerSchedule]:
        with self.dbmgr.session() as db:
            return (
                TowerSchedule.query(db)
                .to_dict(lambda x: x.tower_schedule_id, lambda x: x)
            )
        
    @lazy_property
    def dungeon_name(self) -> Dict[int, str]:
        with self.dbmgr.session() as db:
            return (
                DungeonArea.query(db)
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x.dungeon_name)
            )

    @lazy_property
    def gacha_exchange_chara(self) -> Dict[int, List[GachaExchangeLineup]]:
        with self.dbmgr.session() as db:
            return (
                GachaExchangeLineup.query(db)
                .group_by(lambda x: x.exchange_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )

    @lazy_property
    def campaign_free_gacha(self) -> Dict[int, CampaignFreegacha]:
        with self.dbmgr.session() as db:
            return (
                CampaignFreegacha.query(db)
                .to_dict(lambda x: x.campaign_id, lambda x: x)
            )
        
    @lazy_property
    def campaign_free_gacha_data(self) -> Dict[int, List[CampaignFreegachaDatum]]:
        with self.dbmgr.session() as db:
            return (
                CampaignFreegachaDatum.query(db)
                .group_by(lambda x: x.campaign_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )

    @lazy_property
    def gacha_data(self) -> Dict[int, GachaDatum]:
        with self.dbmgr.session() as db:
            return (
                GachaDatum.query(db)
                .to_dict(lambda x: x.gacha_id, lambda x: x)
            )

    @lazy_property
    def gacha_pickup(self) -> Dict[int, Dict[int, GachaPickup]]:
        with self.dbmgr.session() as db:
            return (
                GachaPickup.query(db)
                .group_by(lambda x: x.id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(
                    lambda x: x.priority, lambda x: x
                ))
            )

    @lazy_property
    def prizegacha_data(self) -> Dict[int, PrizegachaDatum]:
        with self.dbmgr.session() as db:
            return (
                PrizegachaDatum.query(db)
                .to_dict(lambda x: x.prizegacha_id, lambda x: x)
            )

    @lazy_property
    def prizegacha_sp_data(self) -> Dict[int, Dict[int, PrizegachaSpDatum]]:
        with self.dbmgr.session() as db:
            return (
                PrizegachaSpDatum.query(db)
                .group_by(lambda x: x.gacha_id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(lambda x: x.rarity, lambda x: x))
            )

    @lazy_property
    def prizegacha_sp_detail(self) -> Dict[int, PrizegachaSpDetail]:
        with self.dbmgr.session() as db:
            return (
                PrizegachaSpDetail.query(db)
                .to_dict(lambda x: x.disp_rarity, lambda x: x)
            )

    @lazy_property
    def campaign_gacha(self) -> Dict[int, CampaignFreegacha]:
        with self.dbmgr.session() as db:
            return (
                CampaignFreegacha.query(db)
                .to_dict(lambda x: x.campaign_id, lambda x: x)
            )

    @lazy_property
    def love_char(self) -> Dict[int, Tuple[int, int]]:
        with self.dbmgr.session() as db:
            return (
                LoveChara.query(db)
                .group_by(lambda x: x.rarity)
                .to_dict(lambda x: x.key, lambda x:
                    x.select(lambda i: (i.love_level, i.total_love)).max()
                )
            )

    @lazy_property
    def love_cake(self) -> List[ItemDatum]:
        with self.dbmgr.session() as db:
            return (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 50000 and x.item_id < 51000)
                .to_list()
            )

    @lazy_property
    def exp_potion(self) -> List[ItemDatum]:
        with self.dbmgr.session() as db:
            return (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 20001 and x.item_id < 21000)
                .to_list()
            )

    @lazy_property
    def equip_enhance_stone(self) -> List[ItemDatum]:
        with self.dbmgr.session() as db:
            return (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 22001 and x.item_id < 23000)
                .to_list()
            )

    @lazy_property
    def gacha_temp_ticket(self) -> List[ItemDatum]:
        with self.dbmgr.session() as db:
            return (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 1024000 and x.item_id < 1025000)
                .to_list()
            )

    @lazy_property
    def quest_to_event(self) -> Dict[int, HatsuneQuest]:
        with self.dbmgr.session() as db:
            return (
                HatsuneQuest.query(db)
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x) # 类型不一致，Hatsune和Shiori是否分开？
            )
        
    @lazy_property
    def hatsune_item(self) -> Dict[int, HatsuneItem]:
        with self.dbmgr.session() as db:
            return (
                HatsuneItem.query(db)
                .to_dict(lambda x: x.event_id, lambda x: x)
            )

    @lazy_property
    def bmy_story_data(self) -> Dict[int, BmyStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                BmyStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def won_story_data(self) -> Dict[int, WonStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                WonStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def mme_story_data(self) -> Dict[int, MmeStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                MmeStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def dsb_story_data(self) -> Dict[int, DsbStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                DsbStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def xeh_story_data(self) -> Dict[int, XehStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                XehStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def dvs_story_data(self) -> Dict[int, DvsStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                DvsStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def lsv_story_data(self) -> Dict[int, LsvStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                LsvStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def ysn_story_data(self) -> Dict[int, YsnStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                YsnStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def nop_story_data(self) -> Dict[int, NopDramaDatum]:
        with self.dbmgr.session() as db:
            return (
                NopDramaDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def mhp_story_data(self) -> Dict[int, MhpStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                MhpStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def svd_story_data(self) -> Dict[int, SvdStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                SvdStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def ssp_story_data(self) -> Dict[int, SspStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                SspStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def ske_story_data(self) -> Dict[int, SkeStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                SkeStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def lto_story_data(self) -> Dict[int, LtoStoryDatum]:
        with self.dbmgr.session() as db:
            return (
                LtoStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    @lazy_property
    def ex_equipment_data(self) -> Dict[int, ExEquipmentDatum]:
        with self.dbmgr.session() as db:
            return (
                ExEquipmentDatum.query(db)
                .to_dict(lambda x: x.ex_equipment_id, lambda x: x)
            )

    @lazy_property
    def unit_ex_equipment_slot(self) -> Dict[int, UnitExEquipmentSlot]:
        with self.dbmgr.session() as db:
            return (
                UnitExEquipmentSlot.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

    @lazy_property
    def ex_equipment_type_to_clan_battle_ex(self) -> Dict[int, int]:
        return { # 只有每个类别的会战装备
            ex.category: ex.ex_equipment_id for ex in self.ex_equipment_data.values() if ex.clan_battle_equip_flag == 1 and ex.rarity == 3
        }

    @lazy_property
    def ex_equipment_enhance_data(self) -> Dict[int, Dict[int, ExEquipmentEnhanceDatum]]:
        with self.dbmgr.session() as db:
            return (
                ExEquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.rarity)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(lambda x: x.enhance_level, lambda x: x))
            )

    @lazy_property
    def ex_event_data(self) -> Dict[int, TravelExEventDatum]:
        with self.dbmgr.session() as db:
            return (
                TravelExEventDatum.query(db)
                .to_dict(lambda x: x.still_id, lambda x: x)
            )

    @lazy_property
    def travel_area_data(self) -> Dict[int, TravelAreaDatum]:
        with self.dbmgr.session() as db:
            return (
                TravelAreaDatum.query(db)
                .to_dict(lambda x: x.travel_area_id, lambda x: x)
            )

    @lazy_property
    def travel_quest_data(self) -> Dict[int, TravelQuestDatum]:
        with self.dbmgr.session() as db:
            return (
                TravelQuestDatum.query(db)
                .to_dict(lambda x: x.travel_quest_id, lambda x: x)
            )

    @lazy_property
    def quest_name(self) -> Dict[int, str]:
        ret = {}
        with self.dbmgr.session() as db:
            ret = (
                QuestDatum.query(db)
                .concat(HatsuneQuest.query(db))
                .concat(ShioriQuest.query(db))
                .concat(TrainingQuestDatum.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x.quest_name)
            )
        ret.update(
            {x.travel_quest_id :x.travel_quest_name for x in self.travel_quest_data.values()}
        )
        return ret

    @lazy_property
    def shop_static_price_group(self) -> Dict[int, List[ShopStaticPriceGroup]]:
        with self.dbmgr.session() as db:
            return (
                ShopStaticPriceGroup.query(db)
                .group_by(lambda x: x.price_group_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )

    ex_rarity_name = {
        1: '铜',
        2: '银',
        3: '金',
        4: '粉'
    }

    @lazy_property
    def shiori_event_quests(self) -> Dict[int, Dict[int, ShioriQuest]]:
        with self.dbmgr.session() as db:
            return (
                ShioriQuest.query(db)
                .group_by(lambda x: x.event_id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(lambda x: x.quest_id, lambda x: x))
            )

    def get_ex_equip_star_from_pt(self, id: int, pt: int) -> int:
        rarity = self.get_ex_equip_rarity(id)
        history_star = [star for star, enhancement_data in self.ex_equipment_enhance_data[rarity].items() if enhancement_data.total_point <= pt]
        star = max([0] + history_star)
        return star

    def get_ex_equip_rarity(self, id: int) -> int:
        return self.ex_equipment_data[id].rarity

    def get_ex_equip_rarity_name(self, id: int) -> str:
        return self.ex_rarity_name[self.get_ex_equip_rarity(id)]

    def get_inventory_name(self, item: InventoryInfo) -> str:
        try:
            if item.type == eInventoryType.ExtraEquip:
                return f"{self.get_ex_equip_rarity_name(item.id)}{item.ex_equip.rank}-" + self.inventory_name[(item.type, item.id)] 
            return self.inventory_name[(item.type, item.id)]
        except:
            return f"未知物品({item.id})"

    def get_inventory_name_san(self, item: ItemType) -> str:
        try:
            return self.inventory_name[(item[0], item[1])]
        except:
            return f"未知物品({item[1]})"

    def get_ex_equip_name(self, item: int, rank: int = 0) -> str:
        try:
            return f"{self.ex_rarity_name[self.ex_equipment_data[item].rarity]}{rank}-" + self.inventory_name[(eInventoryType.ExtraEquip, item)] 
        except:
            return f"未知ex装备({item})"

    def get_unit_name(self, unit_id: int) -> str:
        try:
            return self.inventory_name[(eInventoryType.Unit, unit_id)]
        except:
            return f"未知角色({unit_id})"

    def get_equip_name(self, equip_id: int) -> str:
        try:
            return self.inventory_name[(eInventoryType.Equip, equip_id)]
        except:
            return f"未知装备({equip_id})"

    def get_item_name(self, item_id: int) -> str:
        try:
            return self.inventory_name[(eInventoryType.Item, item_id)]
        except:
            return f"未知物品({item_id})"

    def get_room_item_name(self, item_id: int) -> str:
        try:
            return self.inventory_name[(eInventoryType.RoomItem, item_id)]
        except:
            return f"未知房间物品({item_id})"

    def get_quest_name(self, quest_id: int) -> str:
        try:
            if quest_id in self.travel_quest_data:
                area = self.travel_quest_data[quest_id].travel_area_id % 10
                quest = self.travel_quest_data[quest_id].travel_quest_id % 10
                return f"{area}-{quest}图"
            else:
                return self.quest_name[quest_id]
        except:
            return f"未知关卡({quest_id})"

    def is_daily_mission(self, mission_id: int) -> bool:
        return mission_id in self.daily_mission_data or mission_id in self.season_pack

    def is_stationary_mission(self, mission_id: int) -> bool:
        return mission_id in self.stationary_mission_data

    def is_emblem_mission(self, mission_id: int) -> bool:
        return mission_id in self.emblem_mission_data

    def is_ex_equip(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.ExtraEquip

    def is_clan_ex_equip(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.ExtraEquip and self.ex_equipment_data[item[1]].clan_battle_equip_flag == 1

    def is_exp_upper(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 20000 and item[1] < 21000

    def is_equip_upper(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 22000 and item[1] < 23000

    def is_unit_memory(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 31000 and item[1] < 32000

    def is_unit_pure_memory(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 32000 and item[1] < 33000

    def is_equip(self, item: ItemType, uncraftable_only: bool = False) -> bool:
        return item[0] == eInventoryType.Equip and item[1] >= 101000 and item[1] < 140000 and (not uncraftable_only or not self.is_equip_craftable(item))

    def is_equip_raw_ore(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Equip and item[1] >= 150001 and item[1] < 160000

    def is_equip_craftable(self, item: ItemType) -> bool:
        return item in self.equip_craft

    def is_equip_glow_ball(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 21900 and item[1] < 21950

    def is_unique_equip_glow_ball(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 21950 and item[1] < 22000

    def is_room_item_level_upable(self, team_level: int, item: RoomUserItem, now: int) -> bool:
        return (item.room_item_level < self.room_item[item.room_item_id].max_level and 
                item.room_item_level in self.room_item_detail[item.room_item_id] and
                team_level >= self.room_item_detail[item.room_item_id][item.room_item_level].lvup_trigger_value and 
                (item.level_up_end_time is None or item.level_up_end_time < now))

    def is_normal_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 11

    def is_hard_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 12

    def is_very_hard_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 13

    def is_heart_piece_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 18

    def is_star_cup_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 19

    def is_hatsune_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 10

    def is_hatsune_normal_quest(self, quest_id: int) -> bool:
        return self.is_hatsune_quest(quest_id) and (quest_id // 100) % 10 == 1

    def is_hatsune_hard_quest(self, quest_id: int) -> bool:
        return self.is_hatsune_quest(quest_id) and (quest_id // 100) % 10 == 2

    def is_shiori_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 20

    def is_shiori_normal_quest(self, quest_id: int) -> bool:
        return self.is_shiori_quest(quest_id) and (quest_id // 100) % 10 == 1

    def is_shiori_hard_quest(self, quest_id: int) -> bool:
        return self.is_shiori_quest(quest_id) and (quest_id // 100) % 10 == 2

    def is_heart_piece_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_UNIQUE_EQUIP

    def is_star_cup_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_HIGH_RARITY_EQUIP

    def is_normal_quest_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_NORMAL

    def is_hard_quest_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_HARD

    def is_very_hard_quest_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_VERY_HARD

    def is_normal_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_NORMAL \
                or self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_BOTH

    def is_hard_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_HARD \
                or self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_BOTH

    def is_very_hard_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_VERY_HARD

    def is_heart_piece_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_UNIQUE_EQUIP

    def is_star_cup_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_HIGH_RARITY_EQUIP

    def is_hatsune_normal_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_HATSUNE_NORMAL \
                or self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_HATSUNE_BOTH

    def is_hatsune_hard_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_HATSUNE_HARD \
                or self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_HATSUNE_BOTH

    def is_shiori_normal_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_SHIORI_NORMAL

    def is_shiori_hard_quest_stamina_half_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.HALF_STAMINA_SHIORI_HARD

    def is_dungeon_mana_campaign(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.GOLD_DROP_AMOUNT_DUNGEON

    def get_campaign_times(self, campaign_id: int) -> float:
        return self.campaign_schedule[campaign_id].value

    def get_active_hatsune(self) -> List[HatsuneSchedule]:
        now = apiclient.datetime
        return flow(self.hatsune_schedule.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.end_time)) \
                .to_list()

    def get_active_hatsune_name(self) -> List[str]:
        active_hatsune = self.get_active_hatsune()
        return [f"{event.event_id}:{db.event_name[event.event_id]}" for event in active_hatsune]

    def get_open_hatsune(self) -> List[HatsuneSchedule]:
        now = apiclient.datetime
        return flow(self.hatsune_schedule.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.close_time)) \
                .to_list()

    def get_active_seasonpass(self) -> List[SeasonpassFoundation]:
        now = apiclient.datetime
        return flow(self.seasonpass_foundation.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.limit_time)) \
                .to_list()

    def get_open_seasonpass(self) -> List[SeasonpassFoundation]:
        now = apiclient.datetime
        return flow(self.seasonpass_foundation.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.end_time)) \
                .to_list()

    def seasonpass_level_reward_full_sign(self, level: int, VIP: int) -> int:
        ret = 0
        if self.seasonpass_level_reward[level].free_reward_num:
            ret |= 1
        if VIP and self.seasonpass_level_reward[level].charge_reward_num_1:
            ret |= 2
        if VIP and self.seasonpass_level_reward[level].charge_reward_num_2:
            ret |= 4
        ret = ret + level * 10
        return ret

    def get_newest_tower_id(self) -> int:
        return max(self.tower_schedule, key = lambda x: self.tower_schedule[x].start_time)

    def max_total_love(self, rarity: int) -> Tuple[int, int]:
        love_info: Tuple[int, int] = (0, 0)
        for key, value in self.love_char.items():
            if rarity >= key:
                love_info = max(love_info, value)
        return love_info

    def is_target_time(self, schedule: List[Tuple[datetime.datetime, datetime.datetime]], now: Union[None, datetime.datetime] = None) -> bool:
        if now is None:
            now = apiclient.datetime
        for start_time, end_time in schedule:
            if now >= start_time and now <= end_time:
                return True
        return False

    def is_campaign(self, campaign: str, now: Union[None, datetime.datetime] = None, level: int = 999) -> bool:
        now = apiclient.datetime if now is None else now
        tomorrow = now + datetime.timedelta(days = 1)
        half_day = datetime.timedelta(hours = 7)
        n3 = (flow(self.campaign_schedule.values())
                .where(lambda x: self.is_normal_quest_campaign(x.id) and x.value >= 6000 and self.is_level_effective_scope_in_campaign(level, x.id)) # TODO change 3000 when stop speed up
                .select(lambda x: (db.parse_time(x.start_time), db.parse_time(x.end_time)))
                .to_list()
              )
        h3 = (flow(self.campaign_schedule.values())
                .where(lambda x: self.is_hard_quest_campaign(x.id) and x.value >= 6000) # TODO change 3000 when stop speed up
                .select(lambda x: (db.parse_time(x.start_time), db.parse_time(x.end_time)))
                .to_list()
             )
        campaign_list = {
            "n3以上前夕": lambda: not self.is_target_time(n3, now) and self.is_target_time(n3, tomorrow),
            "n3以上首日午前": lambda: self.is_target_time(n3, now) and not self.is_target_time(n3, now - half_day),
            "h3以上前夕": lambda: not self.is_target_time(h3, now) and self.is_target_time(h3, tomorrow),
            "会战前夕": lambda: not self.is_clan_battle_time(now) and self.is_clan_battle_time(tomorrow),
            "会战期间": lambda: self.is_clan_battle_time(now),
            "总是执行": lambda: True,
        }
        if campaign not in campaign_list:
            raise ValueError(f"不支持的庆典查询：{campaign}")
        return campaign_list[campaign]()

    def is_level_effective_scope_in_campaign(self, level: int, campaign_id: int) -> bool:
        lv_from = self.campaign_schedule[campaign_id].lv_from
        lv_to = self.campaign_schedule[campaign_id].lv_to
        return lv_from <= level and \
                (lv_to == -1 or level <= lv_to)

    def is_quest_effective_scope_in_campaign(self, quest_id: int, campaign_id: int) -> bool:
        beginner_id = self.campaign_schedule[campaign_id].beginner_id
        if beginner_id == 0: return True
        id_from = self.campaign_beginner_data[beginner_id].id_from
        id_to = self.campaign_beginner_data[beginner_id].id_to
        return id_from <= quest_id and quest_id <= id_to

    def is_clan_battle_time(self, now: Union[None, datetime.datetime] = None) -> bool:
        schedule = [(db.parse_time(schedule.start_time), db.parse_time(schedule.end_time)) 
                    for schedule in self.clan_battle_period.values()]
        return self.is_target_time(schedule, now)

    def is_cf_time(self, now: Union[None, datetime.datetime] = None) -> bool:
        schedule = [(db.parse_time(schedule.start_time), db.parse_time(schedule.end_time)) 
                    for schedule in self.chara_fortune_schedule.values()]
        return self.is_target_time(schedule, now)

    def is_secret_dungeon_time(self) -> bool:
        schedule = [(db.parse_time(schedule.start_time), db.parse_time(schedule.end_time)) 
                    for schedule in self.secret_dungeon_schedule.values()]
        return self.is_target_time(schedule)

    def get_open_secret_dungeon_area(self) -> int:
        schedule = [schedule.dungeon_area_id 
                    for schedule in self.secret_dungeon_schedule.values() if self.is_target_time([(db.parse_time(schedule.start_time), db.parse_time(schedule.end_time))])]
        assert len(schedule) == 1
        return schedule[0]

    def parse_time(self, time: Union[int, str]) -> datetime.datetime:
        try:
            return datetime.datetime.fromtimestamp(int(time))
        except:
            pass

        for timeformat in ['%Y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M', '%Y/%m/%d', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%Y%m%d%H%M%S']:
            try:
                return datetime.datetime.strptime(str(time), timeformat)
            except:
                pass
        raise ValueError(f"无法解析时间：{time}")

    def format_time(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d %H:%M:%S")

    def format_date(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d")

    def format_time_safe(self, time: datetime.datetime) -> str:
        return time.strftime("%Y%m%d%H%M%S")

    def format_second(self, total_seconds: int) -> str:
        time_delta = datetime.timedelta(seconds=total_seconds)
        hours, remainder = divmod(time_delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def get_start_time(self, time: datetime.datetime) -> datetime.datetime:
        shift_time = datetime.timedelta(hours = 5);

        time -= shift_time
        time -= datetime.timedelta(hours = time.hour, minutes = time.minute, seconds = time.second, microseconds = time.microsecond)
        time += shift_time

        return time

    def is_today(self, time: datetime.datetime) -> bool:
        now = apiclient.datetime
        today = self.get_start_time(time)
        tomorrow = today + datetime.timedelta(days = 1)
        return today <= now and now < tomorrow

    def get_today_start_time(self) -> datetime.datetime:
        return self.get_start_time(apiclient.datetime)

    def get_rarity_memory_demand(self, unit_id: int, start_rarity: int, target_rarity: int, token: ItemType) -> int:
        return (
            flow(self.rarity_up_required[unit_id].items())
            .where(lambda x: x[0] > start_rarity and x[0] <= target_rarity)
            .select(lambda x: x[1][token])
            .sum()
        )

    def get_unique_equip_material_demand(self, unit_id: int, slot_id:int, start_rank:int, target_rank: int) -> typing.Counter[ItemType]: 
        if unit_id not in db.unit_unique_equip[slot_id]:
            return Counter() 
        equip_id = db.unit_unique_equip[slot_id][unit_id].equip_id
        return (
            flow(db.unique_equip_required[equip_id].items())
            .where(lambda x: x[0] >= start_rank and x[0] < target_rank)
            .select(lambda x: x[1])
            .sum(seed = Counter())
        )

    def get_rank_promote_equip_demand(self, unit_id: int, start_rank: int, start_rank_equip_slot: List[bool], target_rank, target_rank_equip_slot: List[bool]) -> typing.Counter[ItemType]: # 都是整装
        ret = (
            (flow(self.unit_promotion_equip_count[unit_id].items())
            .where(lambda x: x[0] >= start_rank and x[0] < target_rank)
            .select(lambda x: x[1])
            .sum(seed=Counter())) +
            Counter((eInventoryType(eInventoryType.Equip), int(getattr(self.unit_promotion[unit_id][target_rank], f"equip_slot_{i}"))) for i in range(1, 7) if target_rank_equip_slot[i - 1]) -
            Counter((eInventoryType(eInventoryType.Equip), int(getattr(self.unit_promotion[unit_id][start_rank], f"equip_slot_{i}"))) for i in range(1, 7) if start_rank_equip_slot[i - 1])
            )
        return ret

    def craft_equip(self, source: typing.Counter[ItemType]) -> Tuple[typing.Counter[ItemType], int]: # 返回剩余的材料和消耗的mana
        result: typing.Counter[ItemType] = Counter()
        mana = 0

        queue = SimpleQueue()
        for key, value in source.items():
            queue.put((key, value)) # ItemType, count
        
        while not queue.empty():
            key, value = queue.get()
            if key in self.equip_craft:
                for token in self.equip_craft[key]:
                    queue.put((token[0], token[1] * value))
                mana += self.equip_craft_mana[key] * value
            else:
                result[key] += value

        return result, mana

    def get_redeem_unit_slot_info(self, unit_id: int, slot_id: int) -> RedeemUnit:
        return self.redeem_unit[unit_id][slot_id]

    def get_promotion_demand_level(self, unit_id: int, traget_rank: int) -> int:
        equips = self.get_rank_promote_equip_demand(unit_id, 1, [False] * 6, traget_rank, [False] * 6)
        return max(self.equip_data[id].require_level for (_, id) in equips.keys())

    def get_skill_up_cost(self, start_level: int, target_level: int) -> int:
        return sum(self.skill_cost[i] for i in range(start_level + 1, target_level + 1))

    def get_level_up_total_exp(self, target_level: int) -> int:
        return self.experience_unit[target_level]

    def get_gacha_temp_ticket(self) -> List[int]:
        now = apiclient.datetime
        return flow(self.gacha_temp_ticket) \
            .where(lambda x: self.parse_time(x.start_time) <= now and now <= self.parse_time(x.end_time)) \
            .select(lambda x: x.item_id) \
            .to_list()

    def get_cur_gacha(self) -> List[str]:
        now = apiclient.datetime
        return flow(self.gacha_data.values()) \
        .where(lambda x: self.parse_time(x.start_time) <= now and now <= self.parse_time(x.end_time)) \
        .select(lambda x: f"{x.gacha_id}: {x.gacha_name}-{x.pick_up_chara_text}") \
        .to_list()

    def get_mirai_gacha(self) -> List[str]:
        now = apiclient.datetime
        return flow(self.gacha_data.values()) \
        .where(lambda x: now <= self.parse_time(x.end_time)) \
        .select(lambda x: f"{x.gacha_id}: {x.gacha_name}-{x.pick_up_chara_text}") \
        .to_list()

    def get_raw_ore_of_equip(self, equip: typing.Counter[ItemType]) -> typing.Counter[ItemType]:
        ore_cnt = Counter()
        for e, cnt in equip.items():
            raw_ore = self.get_equip_raw_ore(e[1])
            ore_cnt[raw_ore] += cnt
        return ore_cnt

    def get_equip_raw_ore(self, equip_id: int) -> ItemType:
        promote_level = self.get_equip_promotion(equip_id)
        return self.equip_promotion_to_raw_ore[promote_level] if promote_level in self.equip_promotion_to_raw_ore else (eInventoryType.Equip, equip_id)

    def get_equip_promotion(self, equip_id: int) -> int:
        return self.equip_data[equip_id].promotion_level

    def get_equip_max_star(self, equip_id: int) -> int:
        return max(self.equipment_enhance_data[self.equip_data[equip_id].promotion_level].keys()) if self.equip_data[equip_id].promotion_level in self.equipment_enhance_data else 0

    def get_equip_star_pt(self, equip_id: int, star: int) -> int:
        equip = self.equip_data[equip_id]
        return self.equipment_enhance_data[equip.promotion_level][star].total_point

    def get_equip_star_from_pt(self, equip_id: int, enhancement_pt: int) -> int:
        equip = self.equip_data[equip_id]
        history_star = [star for star, enhancement_data in self.equipment_enhance_data[equip.promotion_level].items() if enhancement_data.total_point <= enhancement_pt]
        star = max([0] + history_star)
        return star

    def get_unique_equip_level_from_pt(self, equip_slot: int, enhancement_pt: int) -> int:
        histort_level = [star for star, enhancement_data in self.unique_equipment_enhance_data[equip_slot].items() if enhancement_data.total_point <= enhancement_pt]
        level = max([1] + histort_level)
        return level

    def get_unique_equip_max_level_from_rank(self, equip_slot: int, rank: int) -> int:
        return self.unique_equip_rank[equip_slot][rank].enhance_level

    def get_unique_equip_rank_from_level(self, equip_slot: int, level: int) -> int:
        rank = self.unique_equipment_enhance_data[equip_slot][level].rank if level in self.unique_equipment_enhance_data[equip_slot] else 1
        return rank

    def get_unique_equip_rank_required_level(self, slot_id: int, unit_id: int, rank: int) -> int:
        rank -= 1 # db是从当前rank升下一级的花费限制，因此升到rank的限制来自于rank-1
        equip_id = db.unit_unique_equip[slot_id][unit_id].equip_id
        level = self.unique_equipment_rank_up[equip_id][rank].unit_level if rank > 0 else 1
        return level

    def get_unique_equip_pt_from_level(self, equip_slot: int, level: int) -> int:
        pt = self.unique_equipment_enhance_data[equip_slot][level].total_point if level in self.unique_equipment_enhance_data[equip_slot] else 0
        return pt

    def get_open_travel_area(self) -> List[int]:
        return (flow(self.travel_area_data.values())
                .where(lambda x: self.is_target_time([(db.parse_time(x.start_time), db.parse_time(x.end_time))]))
                .select(lambda x: x.travel_area_id)
                .to_list()
        )

    def get_shop_item_buy_total_price(self, price_group_id: int, bought_cnt: int, buy_cnt: int) -> int:
        cost = 0
        while buy_cnt > 0:
            info = self.get_shop_item_price_info(price_group_id, bought_cnt)
            cnt = buy_cnt if info.buy_count_to == -1 else min(buy_cnt, info.buy_count_to - bought_cnt)
            cost += cnt * info.count
            buy_cnt -= cnt
        return cost

    def get_shop_item_price_info(self, price_group_id: int, bought_cnt: int) -> ShopStaticPriceGroup:
        buy_cnt = bought_cnt + 1
        item = flow(self.shop_static_price_group[price_group_id]) \
            .first(lambda x: x.buy_count_from <= buy_cnt and (buy_cnt <= x.buy_count_to or x.buy_count_to == -1)) 
        return item


    def deck_sort_unit(self, units: List[int]) -> List[int]:
        return sorted(units, key=lambda x: self.unit_data[x].search_area_width if x in self.unit_data else 9999)

    def is_stamina_type(self, type_id: int) -> bool:
        return type_id in [eInventoryType.Stamina, eInventoryType.SeasonPassStamina]

    def chara_love2love_level(self, chara_love: int):
        return max([0] + [love[0] for love in self.love_char.values() if love[1] <= chara_love])

    def is_gacha_today_end(self, gacha_id: int) -> bool:
        gacha_data = self.gacha_data[gacha_id]
        end_time = self.parse_time(gacha_data.end_time)
        return self.is_today(end_time)

    def is_gacha_today_start(self, gacha_id: int) -> bool:
        gacha_data = self.gacha_data[gacha_id]
        start_time = self.parse_time(gacha_data.start_time)
        return self.is_today(start_time)

    def is_dungeon_id(self, dungeon_id: int) -> bool:
        return dungeon_id // 1000 == 31

    def is_secret_dungeon_id(self, dungeon_id: int) -> bool:
        return dungeon_id // 1000 == 32

    def unit_rank_candidate(self) -> List[int]:
        return list(range(1, self.equip_max_rank + 1))

    def unit_level_candidate(self) -> List[int]:
        return list(range(1, self.team_max_level + 1 + 10))

    def unit_unique_equip_level_candidate(self, equip_slot: int) -> List[int]:
        return list(range(0, self.unique_equipment_max_level[equip_slot] + 1))

    def last_normal_quest(self) -> List[int]:
        last_start_time = flow(self.normal_quest_data.values()) \
                .where(lambda x: db.parse_time(x.start_time) <= apiclient.datetime) \
                .max(lambda x: x.start_time).start_time
        return flow(self.normal_quest_data.values()) \
                .where(lambda x: x.start_time == last_start_time) \
                .select(lambda x: x.quest_id) \
                .to_list()

    def last_normal_quest_candidate(self) -> List[str]:
        quest = self.last_normal_quest()
        return [f"{x}: {self.quest_name[x].split(' ')[1]}" for x in quest]

    def travel_quest_candidate(self) -> List[str]:
        return flow(self.travel_quest_data.values()) \
                .select(lambda x: f"{x.travel_area_id % 10}-{x.travel_quest_id % 10}") \
                .to_list()

    def get_travel_quest_id_from_candidate(self, candidate: str) -> int:
        area, quest = candidate.split('-')
        ret = next(x.travel_quest_id for x in self.travel_quest_data.values() if x.travel_area_id % 10 == int(area) and x.travel_quest_id % 10 == int(quest))
        return ret

    def get_gacha_prize_name(self, gacha_id: int, prize_rarity: int) -> str:
        if gacha_id in self.prizegacha_sp_data:
            prize_rarity = self.prizegacha_sp_data[gacha_id][prize_rarity].disp_rarity
            if prize_rarity in self.prizegacha_sp_detail:
                return self.prizegacha_sp_detail[prize_rarity].name 
        return f"{prize_rarity}等奖"

    def is_unit_rank_bonus(self, unit_id: int, promotion_level: int) -> bool:
        return unit_id in self.promote_bonus and promotion_level in self.promote_bonus[unit_id]

    def calc_unit_attribute(self, unit_data: UnitData, read_story: Set[int]) -> UnitAttribute:
        unit_id = unit_data.id
        promotion_level = unit_data.promotion_level.value
        rarity = unit_data.battle_rarity if unit_data.battle_rarity else unit_data.unit_rarity

        base_attribute = UnitAttribute()
        # 基础属性
        base_attribute += self.unit_rarity[unit_id][rarity].get_unit_attribute()

        # 等级属性
        base_attribute += self.unit_rarity[unit_id][rarity].get_unit_attribute_growth(unit_data.unit_level + promotion_level)

        #品级属性
        if promotion_level > 1:
            base_attribute += self.unit_promotion_status[unit_id][promotion_level].get_unit_attribute()

        rb_attribute = UnitAttribute()
        if self.is_unit_rank_bonus(unit_id, promotion_level):
            rb_attribute += self.promote_bonus[unit_id][promotion_level].get_unit_attribute()

        equip_attribute = UnitAttribute()
        # 装备属性
        for equip in unit_data.equip_slot:
            if equip.is_slot:
                equip_attribute += (self.equip_data[equip.id].get_unit_attribute() + self.equipment_enhance_rate[equip.id].get_unit_attribute(equip.enhancement_level)).ceil()

        unique_equip_attribute = UnitAttribute()
        # 专武属性
        for unique_equip in unit_data.unique_equip_slot:
            if unique_equip.is_slot:
                unique_equip_attribute += self.unique_equipment_data[unique_equip.id].get_unit_attribute()
                for enhance_rate in self.unique_equip_enhance_rate[unique_equip.id]:
                    unique_equip_attribute += enhance_rate.get_unit_attribute(unique_equip.enhancement_level)

        kizuna_attribute = UnitAttribute()
        # 羁绊属性
        for story in self.chara2story[unit_id]:
            if story.story_id in read_story:
                kizuna_attribute += story.get_unit_attribute()

        unit_attribute = base_attribute.round() + rb_attribute.round() + equip_attribute.round() + unique_equip_attribute.ceil() + kizuna_attribute.round()
        return unit_attribute

    def calc_unit_attribute_power(self, unit_data: UnitData, read_story: Set[int], coefficient: UnitStatusCoefficient) -> float:
        unit_attribute = self.calc_unit_attribute(unit_data, read_story)
        return unit_attribute.get_power(coefficient)

    def calc_skill_power(self, unit_data: UnitData, coefficient: UnitStatusCoefficient) -> float:
        unit_rarity = unit_data.unit_rarity if not unit_data.battle_rarity else unit_data.battle_rarity
        skill_power = 0
        for ub in unit_data.union_burst:
            evolution = unit_rarity >= 6
            base = ub.skill_level
            coef = coefficient.ub_evolution_slv_coefficient if evolution else 1
            extra = coefficient.ub_evolution_coefficient if evolution else 0
            skill_power += base * coef + extra

        for id, skill in enumerate(unit_data.main_skill):
            evolution = len(unit_data.unique_equip_slot) > id and unit_data.unique_equip_slot[id].is_slot
            base = skill.skill_level
            coef = getattr(coefficient, f"skill{id+1}_evolution_slv_coefficient") if evolution else 1
            extra = getattr(coefficient, f"skill{id+1}_evolution_coefficient") if evolution else 0
            skill_power += base * coef + extra

        for ex in unit_data.ex_skill:
            evolution = unit_rarity >= 5
            base = ex.skill_level
            coef = 1
            extra = coefficient.exskill_evolution_coefficient if evolution else 0
            skill_power += base * coef + extra

        return skill_power * coefficient.skill_lv_coefficient

    def calc_unit_power(self, unit_data: UnitData, read_story: Set[int]) -> float:
        coefficient = self.unit_status_coefficient[1]
        attribute_power = self.calc_unit_attribute_power(unit_data, read_story, coefficient)
        skill_power = self.calc_skill_power(unit_data, coefficient)
        return attribute_power + skill_power

    def calc_travel_once_time(self, quest_id: int, power: int, coeff: float = 0.015) -> int:
        quest = self.travel_quest_data[quest_id]
        return quest.travel_time - min(
            quest.travel_time_decrease_limit,
            int(max(0, power - quest.need_power) * coeff)
        )

    def unlock_unit_condition_candidate(self):
        return self.unlock_unit_condition

    def free_gacha_ids_candidate(self):
        free_gacha_campaigns = flow(self.campaign_free_gacha.values()) \
            .where(lambda x: apiclient.datetime < self.parse_time(x.end_time)) \
            .select(lambda x: x.campaign_id) \
            .to_list()
        if not free_gacha_campaigns:
            return []
        free_gacha_campaign = min(free_gacha_campaigns)
        return [gacha.gacha_id for gacha in self.campaign_free_gacha_data[free_gacha_campaign]]


db = database()
