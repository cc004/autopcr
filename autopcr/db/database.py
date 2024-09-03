import time
from typing import List, Dict, Tuple, Union
import typing
from ..model.enums import eCampaignCategory
from ..model.common import eInventoryType, RoomUserItem, InventoryInfo
from ..model.custom import ItemType
import datetime
from collections import Counter
from .dbmgr import dbmgr
from .methods import *
from .models import *
from ..util.linq import flow
from queue import SimpleQueue
from .constdata import extra_drops

class database():
    heart: ItemType = (eInventoryType.Equip, 140000)
    xinsui: ItemType = (eInventoryType.Equip, 140001)
    xingqiubei: ItemType = (eInventoryType.Item, 25001)
    mana: ItemType = (eInventoryType.Gold, 94002)
    jewel: ItemType = (eInventoryType.Jewel, 91002)
    gacha_single_ticket: ItemType = (eInventoryType.Item, 24001)

    def update(self, dbmgr: dbmgr):
        
        with dbmgr.session() as db:

            self.dear_story_data: Dict[int, DearStoryDatum] = (
                DearStoryDatum.query(db)
                .to_dict(lambda x: x.value, lambda x: x)
            )

            self.dear_story_detail: Dict[int, Dict[int, DearStoryDetail]] = (
                DearStoryDetail.query(db)
                .group_by(lambda x: x.story_group_id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(
                            lambda x: x.story_id, lambda x: x))
            )

            self.seasonpass_level_reward: Dict[int, SeasonpassLevelReward] = (
                SeasonpassLevelReward.query(db)
                .to_dict(lambda x: x.level_id, lambda x: x)
            )

            self.seasonpass_foundation: Dict[int, SeasonpassFoundation] = (
                SeasonpassFoundation.query(db)
                .to_dict(lambda x: x.season_id, lambda x: x)
            )

            self.guild_data: Dict[int, Guild] = (
                Guild.query(db)
                .to_dict(lambda x: x.guild_id, lambda x: x)
            )

            self.normal_quest_data: Dict[int, QuestDatum] = (
                QuestDatum.query(db)
                .where(lambda x: self.is_normal_quest(x.quest_id)) 
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

            self.wave_groups: Dict[int, WaveGroupDatum] = (
                WaveGroupDatum.query(db)
                .to_dict(lambda x: x.wave_group_id, lambda x: x)
            )

            self.reward_groups: Dict[int, EnemyRewardDatum] = (
                EnemyRewardDatum.query(db)
                .to_dict(lambda x: x.drop_reward_id, lambda x: x)
            )

            self.normal_quest_rewards: Dict[int, typing.Counter[ItemType]] = (
                flow(self.normal_quest_data.values())
                .to_dict(lambda x: x.quest_id, lambda x:
                    flow(x.get_wave_group_ids())
                    .where(lambda y: y != 0)
                    .select_many(lambda y: self.wave_groups[y].get_drop_reward_ids())
                    .where(lambda y: y != 0)
                    .select_many(lambda y: self.reward_groups[y].get_rewards())
                    .where(lambda y: y != 0 and y.reward_item[0] == eInventoryType.Equip)
                    .select(lambda y: Counter({y.reward_item: y.reward_num * y.odds / 100.0}))
                    .sum(seed=Counter()) + 
                    extra_drops.get(x.quest_id // 1000, Counter())
                )
            )
            
            self.unique_equip_rank: Dict[int, UniqueEquipmentEnhanceDatum] = ( # 第二维是int？
                UniqueEquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.rank)
                .to_dict(lambda x: x.key, lambda x: x.max(lambda y: y.enhance_level))
            )

            self.equip_craft: Dict[ItemType, List[Tuple[ItemType, int]]] = (
                EquipmentCraft.query(db)
                .to_dict(lambda x: (eInventoryType.Equip, x.equipment_id), lambda x: 
                    flow(x.get_materials())
                    .where(lambda y: y[0][1] != 0 and y[1] != 0)
                    .to_list()
                )
            )

            self.equip_craft_mana: Dict[ItemType, int] = (
                EquipmentCraft.query(db)
                .to_dict(lambda x: (eInventoryType.Equip, x.equipment_id), lambda x: x.crafted_cost
                )
            )

            self.unit_promotion: Dict[int, Dict[int, UnitPromotion]] = (
                UnitPromotion.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x:
                    x.to_dict(lambda y: y.promotion_level, lambda y: y
                    )
                )
            )

            self.unit_promotion_equip_count: Dict[int, Dict[int, typing.Counter[ItemType]]] = (
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

            self.equip_max_rank: int = max(
                max(x.keys()) for x in self.unit_promotion.values()
            )

            self.equip_max_rank_equip_num: int = max(
                len(x.get(self.equip_max_rank, {})) for x in self.unit_promotion_equip_count.values()
            )

            self.hatsune_schedule: Dict[int, HatsuneSchedule] = (
                HatsuneSchedule.query(db)
                .to_dict(lambda x: x.event_id, lambda x: x)
            )

            self.campaign_beginner_data: Dict[int, CampaignBeginnerDatum] = (
                CampaignBeginnerDatum.query(db)
                .to_dict(lambda x: x.beginner_id, lambda x: x)
            )

            self.campaign_schedule: Dict[int, CampaignSchedule] = (
                CampaignSchedule.query(db)
                .to_dict(lambda x: x.id, lambda x: x)
            )

            self.pure_memory_quest: Dict[ItemType, List[QuestDatum]] = (
                QuestDatum.query(db)
                .where(lambda x: self.is_very_hard_quest(x.quest_id))
                .group_by(lambda x: x.reward_image_1)
                .to_dict(lambda x: (eInventoryType.Item, x.key), lambda x:
                         x.to_list()[::-1]
                )
            )

            self.memory_hard_quest: Dict[ItemType, List[QuestDatum]] = (
                QuestDatum.query(db)
                .where(lambda x: self.is_hard_quest(x.quest_id))
                .group_by(lambda x: x.reward_image_1)
                .to_dict(lambda x: (eInventoryType.Item, x.key), lambda x:
                         x.to_list()[::-1]
                )
            )

            self.memory_shiori_quest: Dict[ItemType, List[ShioriQuest]] = (
                ShioriQuest.query(db)
                .where(lambda x: self.is_shiori_hard_quest(x.quest_id))
                .group_by(lambda x: x.drop_reward_id)
                .to_dict(lambda x: (eInventoryType.Item, x.key), lambda x:
                         x.to_list()[::-1]
                )
            )

            self.team_info: Dict[int, ExperienceTeam] = (
                ExperienceTeam.query(db)
                .to_dict(lambda x: x.team_level, lambda x: x)
            )

            self.team_max_level: int = max(self.team_info.keys()) - 1

            self.unit_unique_equip: Dict[int, Dict[int, UnitUniqueEquipment]] = (
                UnitUniqueEquipment.query(db)
                .group_by(lambda x: x.equip_slot)
                .to_dict(lambda x: x.key, lambda x: 
                    x.to_dict(lambda x: x.unit_id, lambda x: x))
            )

            self.unique_equipment_enhance_data: Dict[int, Dict[int, UniqueEquipmentEnhanceDatum]] = (
                UniqueEquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.equip_slot)
                .to_dict(lambda x: x.key, lambda x: 
                     x.to_dict(lambda x: x.enhance_level, lambda x: x))
            )

            self.unique_equipment_max_level: Dict[int, int] = {
                equip_slot: max(self.unique_equipment_enhance_data[equip_slot].keys()) for equip_slot in self.unique_equipment_enhance_data
            }
            self.unique_equipment_max_level[1] = (self.team_max_level + 9) // 10 * 10 # 手动修正

            self.exceed_level_unit_required: Dict[int, ExceedLevelUnit] = (
                ExceedLevelUnit.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )
            
            self.rarity_up_required: Dict[int, Dict[int, typing.Counter[ItemType]]] = (
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

            self.unique_equip_required: Dict[int, Dict[int, typing.Counter[ItemType]]] = (
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

            self.dungeon_area: Dict[int, DungeonArea] = (
                DungeonArea.query(db)
                .where(lambda x: self.is_dungeon_id(x.dungeon_area_id))
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x)
            )

            self.secret_dungeon_area: Dict[int, DungeonArea] = (
                DungeonArea.query(db)
                .where(lambda x: self.is_secret_dungeon_id(x.dungeon_area_id))
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x)
            )

            self.secret_dungeon_schedule: Dict[int, SecretDungeonSchedule] = (
                SecretDungeonSchedule.query(db)
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x)
            )

            self.training_quest_exp: Dict[int, TrainingQuestDatum] = (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21002)
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

            self.training_quest_exp: Dict[int, TrainingQuestDatum] = (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21002)
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

            self.training_quest_mana: Dict[int, TrainingQuestDatum] = (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21001)
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )
            
            self.chara_fortune_schedule: Dict[int, CharaFortuneSchedule] = (
                CharaFortuneSchedule.query(db)
                .to_dict(lambda x: x.fortune_id, lambda x: x)
            )

            self.clan_battle_period: Dict[int, ClanBattlePeriod] = (
                ClanBattlePeriod.query(db)
                .to_dict(lambda x: x.clan_battle_id, lambda x: x)
            )

            self.quest_info: Dict[int, QuestDatum] = (
                QuestDatum.query(db)
                .concat(HatsuneQuest.query(db))
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

            self.quest_name: Dict[int, str] = (
                QuestDatum.query(db)
                .concat(HatsuneQuest.query(db))
                .concat(ShioriQuest.query(db))
                .concat(TrainingQuestDatum.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x.quest_name)
            )
            
            self.guild_story: List[StoryDetail] = (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 3000000 and x.story_id < 4000000)
                .to_list()
            )

            self.main_story: List[StoryDetail] = (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 2000000 and x.story_id < 3000000)
                .to_list()
            )

            self.tower_story: List[TowerStoryDetail] = (
                TowerStoryDetail.query(db)
                .to_list()
            )

            self.tower_area: Dict[int, TowerAreaDatum] = (
                TowerAreaDatum.query(db)
                .to_dict(lambda x: x.max_floor_num, lambda x: x)
            )

            self.tower_quest: Dict[int, TowerQuestDatum] = (
                TowerQuestDatum.query(db)
                .to_dict(lambda x: x.tower_quest_id, lambda x: x)
            )

            self.event_story_data: Dict[int, EventStoryDatum] = (
                EventStoryDatum.query(db)
                .to_dict(lambda x: x.story_group_id, lambda x: x)
            )

            self.event_name: Dict[int, str] = (
                EventStoryDatum.query(db)
                .select(lambda x: (x.story_group_id + 5000, x.title))
                .concat(
                    EventStoryDatum.query(db)
                    .select(lambda x: (x.value, x.title))
                ).to_dict(lambda x: x[0], lambda x: x[1])
            )

            self.event_story_detail: List[EventStoryDetail] = (
                EventStoryDetail.query(db)
                .to_list()
            )

            self.unit_story: List[StoryDetail] = (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 1000000 and x.story_id < 2000000)
                #.select(lambda x: (x.story_id, x.pre_story_id, x.story_group_id, x.love_level, x.title))
                .to_list()
            )

            self.equip_data: Dict[int, EquipmentDatum] = (
                EquipmentDatum.query(db)
                .to_dict(lambda x: x.equipment_id, lambda x: x)
            )

            self.skill_cost: Dict[int, int] = (
                SkillCost.query(db)
                .to_dict(lambda x: x.target_level, lambda x: x.cost)
            )

            self.experience_unit: Dict[int, int] = (
                ExperienceUnit.query(db)
                .to_dict(lambda x: x.unit_level, lambda x: x.total_exp)
            )

            self.equipment_enhance_data: Dict[int, Dict[int, EquipmentEnhanceDatum]] = (
                EquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.promotion_level)
                .to_dict(lambda x: x.key, lambda x: 
                     x.to_dict(lambda x: x.equipment_enhance_level, lambda x: x))
            )

            self.inventory_name: Dict[ItemType, str] = (
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
                .to_dict(lambda x: (x[0], x[1]), lambda x: x[2])
            )

            self.inventory_name[(eInventoryType.Stamina, 93001)] = "体力"
            self.inventory_name[(eInventoryType.TeamExp, 92001)] = "经验"
            self.inventory_name[(eInventoryType.Jewel, 91002)] = "宝石"
            self.inventory_name[(eInventoryType.Gold, 94002)] = "mana"
            self.inventory_name[(eInventoryType.SeasonPassPoint, 98002)] = "祝福经验值"
            self.inventory_name[(eInventoryType.SeasonPassStamina, 93002)] = "星尘体力药剂"

            self.room_item: Dict[int, RoomItem] = (
                RoomItem.query(db)
                .to_dict(lambda x: x.id, lambda x: x)
            )

            self.room_item_detail: Dict[int, Dict[int, RoomItemDetail]] = ( # id, level
                RoomItemDetail.query(db)
                .group_by(lambda x: x.room_item_id)
                .to_dict(lambda x: x.key, lambda x: 
                    x.to_dict(lambda x: x.level, lambda x: x))
            )
            
            self.daily_mission_data: Dict[int, DailyMissionDatum] = (
                DailyMissionDatum.query(db)
                .to_dict(lambda x: x.daily_mission_id, lambda x: x)
            )

            self.memory_to_unit: Dict[int, int] = (
                UnitRarity.query(db)
                .group_by(lambda x: x.unit_material_id)
                .to_dict(lambda x: x.key, lambda x: x.first().unit_id)
            )

            self.growth_parameter: Dict[int, GrowthParameter] = (
                GrowthParameter.query(db)
                .to_dict(lambda x: x.growth_id, lambda x: x)
            )

            self.unit_data: Dict[int, UnitDatum] = (
                UnitDatum.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

            self.unlock_unit_condition: Dict[int, UnlockUnitCondition] = (
                UnlockUnitCondition.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )

            self.pure_memory_to_unit: Dict[ItemType, int] = (
                UnlockRarity6.query(db)
                .where(lambda x: x.slot_id == 1)
                .to_dict(lambda x: (eInventoryType.Item, x.material_id), lambda x: x.unit_id)
            )
            
            self.six_area: Dict[int, QuestDatum] = (
                QuestDatum.query(db)
                .where(lambda x: self.is_very_hard_quest(x.quest_id))
                .to_dict(lambda x: x.quest_id, lambda x: x)
            )

            self.tower: Dict[int, TowerSchedule] = (
                TowerSchedule.query(db)
                .to_dict(lambda x: x.tower_schedule_id, lambda x: x)
            )
            
            self.dungeon_name: Dict[int, str] = (
                DungeonArea.query(db)
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x.dungeon_name)
            )

            self.gacha_exchange_chara: Dict[int, List[GachaExchangeLineup]] = (
                GachaExchangeLineup.query(db)
                .group_by(lambda x: x.exchange_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )
            
            self.free_gacha_list: Dict[int, List[CampaignFreegachaDatum]] = (
                CampaignFreegachaDatum.query(db)
                .group_by(lambda x: x.campaign_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )

            self.gacha_data: Dict[int, GachaDatum] = (
                GachaDatum.query(db)
                .to_dict(lambda x: x.gacha_id, lambda x: x)
            )

            self.prizegacha_data: Dict[int, PrizegachaDatum] = (
                PrizegachaDatum.query(db)
                .to_dict(lambda x: x.prizegacha_id, lambda x: x)
            )

            self.prizegacha_sp_data: Dict[int, Dict[int, PrizegachaSpDatum]] = (
                PrizegachaSpDatum.query(db)
                .group_by(lambda x: x.gacha_id)
                .to_dict(lambda x: x.key, lambda x: x.to_dict(lambda x: x.rarity, lambda x: x))
            )

            self.prizegacha_sp_detail: Dict[int, PrizegachaSpDetail] = (
                PrizegachaSpDetail.query(db)
                .to_dict(lambda x: x.disp_rarity, lambda x: x)
            )

            self.campaign_gacha: Dict[int, CampaignFreegacha] = (
                CampaignFreegacha.query(db)
                .to_dict(lambda x: x.campaign_id, lambda x: x)
            )

            self.love_char: Dict[int, Tuple[int, int]] = (
                LoveChara.query(db)
                .group_by(lambda x: x.rarity)
                .to_dict(lambda x: x.key, lambda x:
                    x.select(lambda i: (i.love_level, i.total_love)).max()
                )
            )

            self.love_cake: List[ItemDatum] = (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 50000 and x.item_id < 51000)
                #.select(lambda x: (x.item_id, x.value))
                .to_list()
            )

            self.love_cake = self.love_cake[::-1]

            self.exp_potion: List[ItemDatum] = (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 20001 and x.item_id < 21000)
                .to_list()
            )

            # self.exp_potion = self.exp_potion[::-1]

            self.equip_enhance_stone: List[ItemDatum] = (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 22001 and x.item_id < 23000)
                .to_list()
            )

            # self.equip_enhance_stone = self.equip_enhance_stone[::-1]

            self.quest_to_event: Dict[int, HatsuneQuest] = (
                HatsuneQuest.query(db)
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x) # 类型不一致，Hatsune和Shiori是否分开？
            )
            
            self.hatsune_item: Dict[int, HatsuneItem] = (
                HatsuneItem.query(db)
                .to_dict(lambda x: x.event_id, lambda x: x)
            )

            self.lsv_story_data: Dict[int, LsvStoryDatum] = (
                LsvStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.ysn_story_data: Dict[int, YsnStoryDatum] = (
                YsnStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.nop_story_data: Dict[int, NopDramaDatum] = (
                NopDramaDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.mhp_story_data: Dict[int, MhpStoryDatum] = (
                MhpStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.svd_story_data: Dict[int, SvdStoryDatum] = (
                SvdStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.ssp_story_data: Dict[int, SspStoryDatum] = (
                SspStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.ske_story_data: Dict[int, SkeStoryDatum] = (
                SkeStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

            self.lto_story_data: Dict[int, LtoStoryDatum] = (
                LtoStoryDatum.query(db)
                .to_dict(lambda x: x.sub_story_id, lambda x: x)
            )

    def get_inventory_name(self, item: InventoryInfo) -> str:
        try:
            return self.inventory_name[(item.type, item.id)]
        except:
            return f"未知物品({item.id})"

    def get_inventory_name_san(self, item: ItemType) -> str:
        try:
            return self.inventory_name[(item[0], item[1])]
        except:
            return f"未知物品({item[1]})"

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

    def is_daily_mission(self, mission_id: int) -> bool:
        return mission_id in self.daily_mission_data

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

    def is_equip_craftable(self, item: ItemType) -> bool:
        return item in self.equip_craft

    def is_room_item_level_upable(self, team_level: int, item: RoomUserItem) -> bool:
        return (item.room_item_level < self.room_item[item.room_item_id].max_level and 
                item.room_item_level in self.room_item_detail[item.room_item_id] and
                team_level >= self.room_item_detail[item.room_item_id][item.room_item_level].lvup_trigger_value and 
                (item.level_up_end_time is None or item.level_up_end_time < time.time()))

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
        now = datetime.datetime.now()
        return flow(self.hatsune_schedule.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.end_time)) \
                .to_list()

    def get_active_hatsune_name(self) -> List[str]:
        active_hatsune = self.get_active_hatsune()
        return [f"{event.event_id}:{db.event_name[event.event_id]}" for event in active_hatsune]

    def get_open_hatsune(self) -> List[HatsuneSchedule]:
        now = datetime.datetime.now()
        return flow(self.hatsune_schedule.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.close_time)) \
                .to_list()

    def get_active_seasonpass(self) -> List[SeasonpassFoundation]:
        now = datetime.datetime.now()
        return flow(self.seasonpass_foundation.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.limit_time)) \
                .to_list()

    def get_open_seasonpass(self) -> List[SeasonpassFoundation]:
        now = datetime.datetime.now()
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
        return max(self.tower, key = lambda x: self.tower[x].start_time)

    def max_total_love(self, rarity: int) -> Tuple[int, int]:
        love_info: Tuple[int, int] = (0, 0)
        for key, value in self.love_char.items():
            if rarity >= key:
                love_info = max(love_info, value)
        return love_info

    def is_target_time(self, schedule: List[Tuple[datetime.datetime, datetime.datetime]], now: Union[None, datetime.datetime] = None) -> bool:
        if now is None:
            now = datetime.datetime.now()
        for start_time, end_time in schedule:
            if now >= start_time and now <= end_time:
                return True
        return False

    def is_campaign(self, campaign: str, now: Union[None, datetime.datetime] = None) -> bool:
        now = datetime.datetime.now() if now is None else now
        tomorrow = now + datetime.timedelta(days = 1)
        half_day = datetime.timedelta(hours = 7)
        n3 = (flow(self.campaign_schedule.values())
                .where(lambda x: self.is_normal_quest_campaign(x.id) and x.value >= 3000)
                .select(lambda x: (db.parse_time(x.start_time), db.parse_time(x.end_time)))
                .to_list()
              )
        h3 = (flow(self.campaign_schedule.values())
                .where(lambda x: self.is_hard_quest_campaign(x.id) and x.value >= 3000)
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

    def is_effective_scope_in_campaign(self, quest_id: int, campaign_id: int) -> bool:
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

    def parse_time(self, time: str) -> datetime.datetime:
        for timeformat in ['%Y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']:
            try:
                return datetime.datetime.strptime(time, timeformat)
            except:
                pass
        raise ValueError(f"无法解析时间：{time}")

    def parse_time_safe(self, time: str) -> datetime.datetime:
        return datetime.datetime.strptime(time, '%Y%m%d%H%M%S')

    def format_time(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d %H:%M:%S")

    def format_date(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d")

    def format_time_safe(self, time: datetime.datetime) -> str:
        return time.strftime("%Y%m%d%H%M%S")

    def get_start_time(self, time: datetime.datetime) -> datetime.datetime:
        shift_time = datetime.timedelta(hours = 5);

        time -= shift_time
        time -= datetime.timedelta(hours = time.hour, minutes = time.minute, seconds = time.second, microseconds = time.microsecond)
        time += shift_time

        return time

    def is_today(self, time: datetime.datetime) -> bool:
        now = datetime.datetime.now()
        today = self.get_start_time(time)
        tomorrow = today + datetime.timedelta(days = 1)
        return today <= now and now < tomorrow

    def get_today_start_time(self) -> datetime.datetime:
        return self.get_start_time(datetime.datetime.now())

    def get_rank_promote_equip_demand(self, unit_id: int, start_rank: int, start_rank_equip_slot: List[bool], target_rank, target_rank_equip_slot: List[bool]) -> typing.Counter[ItemType]: # 都是整装
        ret = (
            (flow(self.unit_promotion_equip_count[unit_id].items())
            .where(lambda x: x[0] >= start_rank and x[0] < target_rank)
            .select(lambda x: x[1])
            .sum(seed=Counter())) - 
            Counter((eInventoryType(eInventoryType.Equip), int(getattr(self.unit_promotion[unit_id][start_rank], f"equip_slot_{i}"))) for i in range(1, 7) if start_rank_equip_slot[i - 1]) +
            Counter((eInventoryType(eInventoryType.Equip), int(getattr(self.unit_promotion[unit_id][target_rank], f"equip_slot_{i}"))) for i in range(1, 7) if target_rank_equip_slot[i - 1])
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

    def get_promotion_demand_level(self, unit_id: int, traget_rank: int) -> int:
        equips = self.get_rank_promote_equip_demand(unit_id, 1, [False] * 6, traget_rank, [False] * 6)
        return max(self.equip_data[id].require_level for (_, id) in equips.keys())

    def get_skill_up_cost(self, start_level: int, target_level: int) -> int:
        return sum(self.skill_cost[i] for i in range(start_level + 1, target_level + 1))

    def get_level_up_total_exp(self, target_level: int) -> int:
        return self.experience_unit[target_level]

    def get_cur_gacha(self):
        now = datetime.datetime.now()
        return flow(self.gacha_data.values()) \
        .where(lambda x: self.parse_time(x.start_time) <= now and now <= self.parse_time(x.end_time)) \
        .select(lambda x: f"{x.gacha_id}: {x.gacha_name}-{x.pick_up_chara_text}") \
        .to_list()

    def get_equip_max_star(self, equip_id: int):
        return max(self.equipment_enhance_data[self.equip_data[equip_id].promotion_level].keys()) if self.equip_data[equip_id].promotion_level in self.equipment_enhance_data else 0

    def get_equip_star_pt(self, equip_id: int, star: int):
        equip = self.equip_data[equip_id]
        return self.equipment_enhance_data[equip.promotion_level][star].total_point

    def get_equip_star_from_pt(self, equip_id: int, enhancement_pt: int):
        equip = self.equip_data[equip_id]
        history_star = [star for star, enhancement_data in self.equipment_enhance_data[equip.promotion_level].items() if enhancement_data.total_point <= enhancement_pt]
        star = max([0] + history_star)
        return star

    def get_unique_equip_level_from_pt(self, equip_slot: int, enhancement_pt: int):
        histort_level = [star for star, enhancement_data in self.unique_equipment_enhance_data[equip_slot].items() if enhancement_data.total_point <= enhancement_pt]
        level = max([1] + histort_level)
        return level

    def deck_sort_unit(self, units: List[int]):
        return sorted(units, key=lambda x: self.unit_data[x].search_area_width)

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

    def unit_rank_candidate(self):
        return list(range(1, self.equip_max_rank + 1))

    def unit_level_candidate(self):
        return list(range(1, self.team_max_level + 1 + 10))

    def last_normal_quest_candidate(self):
        last_start_time = flow(self.normal_quest_data.values()) \
                .where(lambda x: db.parse_time(x.start_time) <= datetime.datetime.now()) \
                .max(lambda x: x.start_time).start_time
        return flow(self.normal_quest_data.values()) \
                .where(lambda x: x.start_time == last_start_time) \
                .select(lambda x: f"{x.quest_id}: {x.quest_name.split(' ')[1]}") \
                .to_list()

    def get_gacha_prize_name(self, gacha_id: int, prize_rarity: int) -> str:
        if gacha_id in self.prizegacha_sp_data:
            prize_rarity = self.prizegacha_sp_data[gacha_id][prize_rarity].disp_rarity
            if prize_rarity in self.prizegacha_sp_detail:
                return self.prizegacha_sp_detail[prize_rarity].name 
        return f"{prize_rarity}等奖"

db = database()
