import time
from typing import Set, Dict, Tuple
import typing
from ..model.common import eInventoryType, eCampaignCategory, RoomUserItem, InventoryInfo, ItemType
import datetime
from collections import Counter
from .dbmgr import dbmgr
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

    def update(self, dbmgr: dbmgr):
        
        with dbmgr.session() as db:

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

            self.unit_promotion: Dict[int, Dict[int, typing.Counter[ItemType]]] = (
                UnitPromotion.query(db)
                .group_by(lambda x: x.unit_id)
                .to_dict(lambda x: x.key, lambda x:
                    x.to_dict(lambda y: y.promotion_level, lambda y:
                        Counter(flow(range(1, 7))
                        .select(lambda z: getattr(y, f'equip_slot_{z}'))
                        .where(lambda z: z != 999999)
                        .to_dict(lambda z: (eInventoryType.Equip, z), lambda _: 1)
                    ))
                )
            )

            self.equip_max_rank: int = max(
                max(x.keys()) for x in self.unit_promotion.values()
            )

            self.equip_max_rank_equip_num: int = max(
                len(x.get(self.equip_max_rank, {})) for x in self.unit_promotion.values()
            )

            self.hatsune_schedule: Dict[int, HatsuneSchedule] = (
                HatsuneSchedule.query(db)
                .to_dict(lambda x: x.event_id, lambda x: x)
            )
            
            self.campaign_schedule: Dict[int, CampaignSchedule] = (
                CampaignSchedule.query(db)
                .to_dict(lambda x: x.id, lambda x: x)
            )

            self.memory_quest: Dict[int, List[QuestDatum]] = (
                QuestDatum.query(db)
                .where(lambda x: self.is_hard_quest(x.quest_id))
                .group_by(lambda x: x.reward_image_1)
                .to_dict(lambda x: x.key, lambda x:
                    x.to_list()
                )
            )

            self.unit_unique_equip: Dict[int, UnitUniqueEquip] = (
                UnitUniqueEquip.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x)
            )
            
            self.rarity_up_required: Dict[int, Dict[int, typing.Counter[ItemType]]] = (
                UnitRarity.query(db)
                .select(lambda x: (
                    x.unit_id,
                    x.rarity,
                    x.unit_material_id,
                    x.consume_num
                ))
                .concat(
                    UnlockRarity6.query(db)
                    .group_by(lambda x: (x.unit_id, x.material_id))
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
                        Counter(y.group_by(lambda z: (eInventoryType.Item, z[2]))
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

            self.team_max_stamina: Dict[int, ExperienceTeam] = (
                ExperienceTeam.query(db)
                .to_dict(lambda x: x.team_level, lambda x: x)
            )

            self.event_story: List[EventStoryDetail] = (
                EventStoryDetail.query(db)
                .where(lambda x: x.visible_type == 0)
                #.select(lambda x: (x.story_id, x.pre_story_id, x.title))
                .to_list()
            )

            self.unit_story: List[StoryDetail] = (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 1000000 and x.story_id < 2000000)
                #.select(lambda x: (x.story_id, x.pre_story_id, x.story_group_id, x.love_level, x.title))
                .to_list()
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
                    .select(lambda x: (eInventoryType(x.type), x.emblem_id, x.emblem_name))
                )
                .to_dict(lambda x: (x[0], x[1]), lambda x: x[2])
            )

            self.inventory_name[(eInventoryType.Stamina, 93001)] = "体力"
            self.inventory_name[(eInventoryType.TeamExp, 92001)] = "经验"
            self.inventory_name[(eInventoryType.Jewel, 91002)] = "宝石"
            self.inventory_name[(eInventoryType.Gold, 94002)] = "mana"

            self.room_item: Dict[int, RoomItem] = (
                RoomItem.query(db)
                .to_dict(lambda x: x.id, lambda x: x)
            )
            
            self.daily_mission: Set[int] = (
                DailyMissionDatum.query(db)
                .select(lambda x: x.daily_mission_id)
                .to_set()
            )
            
            self.memory_to_unit: Dict[int, int] = (
                UnitRarity.query(db)
                .group_by(lambda x: x.unit_material_id)
                .to_dict(lambda x: x.key, lambda x: x.first().unit_id)
            )
            

            self.pure_memory_to_unit: Dict[int, int] = (
                UnlockRarity6.query(db)
                .where(lambda x: x.slot_id == 1)
                .to_dict(lambda x: x.material_id, lambda x: x.unit_id)
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
            
            self.gacha_list: Dict[int, List[CampaignFreegachaDatum]] = (
                CampaignFreegachaDatum.query(db)
                .group_by(lambda x: x.campaign_id)
                .to_dict(lambda x: x.key, lambda x: x.to_list())
            )
            
            self.campaign_gacha: Dict[int, CampaignFreegacha] = (
                CampaignFreegacha.query(db)
                .to_dict(lambda x: x.campaign_id, lambda x: CampaignFreegacha)
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

            self.quest_to_event: Dict[int, HatsuneQuest] = (
                HatsuneQuest.query(db)
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x) # 类型不一致，Hatsune和Shiori是否分开？
            )
            
            self.hatsune_item: Dict[int, HatsuneItem] = (
                HatsuneItem.query(db)
                .to_dict(lambda x: x.event_id, lambda x: x)
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

    def is_daily_mission(self, mission_id: int) -> bool:
        return mission_id in self.daily_mission

    def is_exp_upper(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 20000 and item[1] < 21000

    def is_equip_upper(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 22000 and item[1] < 23000

    def is_unit_memory(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 31000 and item[1] < 32000

    def is_unit_pure_memory(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 32000 and item[1] < 33000

    def is_equip(self, item: ItemType) -> bool:
        return item[0] == eInventoryType.Equip and item[1] >= 101000 and item[1] < 140000

    def is_room_item_level_upable(self, team_level: int, item: RoomUserItem) -> bool:
        return item.room_item_level < self.room_item[item.room_item_id].max_level and team_level // 10 >= item.room_item_level and (item.level_up_end_time is None or item.level_up_end_time < time.time())

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

    def is_shiori_quest(self, quest_id: int) -> bool:
        return quest_id // 1000000 == 20

    def is_heart_piece_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_UNIQUE_EQUIP

    def is_star_cup_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_HIGH_RARITY_EQUIP

    def is_normal_quest_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_NORMAL

    def is_hard_quest_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_HARD

    def is_very_hard_quest_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.ITEM_DROP_AMOUNT_VERY_HARD

    def is_dungeon_mana_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id].campaign_category == eCampaignCategory.GOLD_DROP_AMOUNT_DUNGEON

    def get_dungeon_mana_before_day(self) -> int:
        now = datetime.datetime.now()
        dungeon = (
            flow(self.campaign_schedule.values())
            .where(
                lambda x: x.campaign_category == eCampaignCategory.GOLD_DROP_AMOUNT_DUNGEON and 
                db.parse_time(x.start_time) > now
            )
            .min(lambda x: x.start_time)
        )
        today = self.get_today_start_time()
        dungeon = self.get_start_time(db.parse_time(dungeon[2]))
        return (dungeon - today).days

    def get_active_hatsune(self) -> List[HatsuneSchedule]:
        now = datetime.datetime.now()
        return flow(self.hatsune_schedule.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.end_time)) \
                .to_list()

    def get_open_hatsune(self) -> List[HatsuneSchedule]:
        now = datetime.datetime.now()
        return flow(self.hatsune_schedule.values()) \
                .where(lambda x: now >= self.parse_time(x.start_time) and now <= self.parse_time(x.close_time)) \
                .to_list()

    def get_newest_tower_id(self) -> int:
        return max(self.tower, key = lambda x: self.tower[x].start_time)

    def max_total_love(self, rarity: int) -> Tuple[int, int]:
        love_info: Tuple[int, int] = (0, 0)
        for key, value in self.love_char.items():
            if rarity >= key:
                love_info = max(love_info, value)
        return love_info

    def is_clan_battle_time(self) -> bool:
        now = datetime.datetime.now()
        for key, schedule in list(self.clan_battle_period.items()):
            start_time = self.parse_time(schedule.start_time)
            end_time = self.parse_time(schedule.end_time)
            if now > end_time:
                self.clan_battle_period.pop(key)
            elif now >= start_time:
                return True
        return False

    def is_cf_time(self) -> bool:
        now = datetime.datetime.now()
        for key, schedule in list(self.chara_fortune_schedule.items()):
            start_time = self.parse_time(schedule.start_time)
            end_time = self.parse_time(schedule.end_time)
            if now > end_time:
                self.chara_fortune_schedule.pop(key)
            elif now >= start_time:
                return True
        return False

    def parse_time(self, time: str) -> datetime.datetime:
        if time.count(':') == 1: # 怎么以前没有秒的
            time += ":00"
        return datetime.datetime.strptime(time, '%Y/%m/%d %H:%M:%S')

    def format_time(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d %H:%M:%S")

    def get_start_time(self, time: datetime.datetime) -> datetime.datetime:
        shift_time = datetime.timedelta(hours = 5);

        time -= shift_time
        time -= datetime.timedelta(hours = time.hour, minutes = time.minute, seconds = time.second, microseconds = time.microsecond)
        time += shift_time

        return time

    def get_today_start_time(self) -> datetime.datetime:
        return self.get_start_time(datetime.datetime.now())

    def craft_equip(self, source: typing.Counter[ItemType]) -> typing.Counter[ItemType]: # 依赖关系不深，没必要写成拓扑图求解
        result: typing.Counter[ItemType] = Counter()

        queue = SimpleQueue()
        for key, value in source.items():
            queue.put((key, value))
        
        while not queue.empty():
            key, value = queue.get()
            if key in self.equip_craft:
                for token in self.equip_craft[key]:
                    queue.put((token[0], token[1] * value))
            else:
                result[key] += value

        return result


db = database()
