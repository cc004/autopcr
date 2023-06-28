import time
from typing import Set, Dict, Tuple
import typing
from ..model.common import *
import datetime
from collections import Counter
from functools import reduce
from .dbmgr import dbmgr
from .models import *
from ..util.linq import flow

'''
db_path = os.path.join(os.path.dirname(__file__), "../../", "redive_cn.db")
def rec_intdict(deep: int) -> Union[int, DefaultDict]:
    if not deep:
        return 0
    else:
        return defaultdict(lambda: rec_intdict(deep - 1))

def rec_counter(deep: int) -> Union[typing.Counter, DefaultDict]:
    if deep == 1:
        return Counter()
    else:
        return defaultdict(lambda: rec_counter(deep - 1))
'''

class database():
    heart: Tuple[eInventoryType, int] = (eInventoryType.Equip, 140000)
    xinsui: Tuple[eInventoryType, int] = (eInventoryType.Equip, 140001)
    xingqiubei: Tuple[eInventoryType, int] = (eInventoryType.Item, 25001)
    mana: Tuple[eInventoryType, int] = (eInventoryType.Gold, 94002)
    jewel: Tuple[eInventoryType, int] = (eInventoryType.Jewel, 91002)
    '''
    six_area: Dict[int, Tuple[int, int]] = {}
    inventory_name: Dict[Tuple[eInventoryType, int], str] = {}
    tower: Dict[int, Tuple[str, str]] = {}
    daily_mission: Set[int] = set()
    main_story: List[Tuple[int, int, int, str]] = []
    floor2clositer: Dict[int, int] = {}
    tower_story: List[Tuple[int, int, int, str, str]] = []
    tower2floor: Dict[int, int] = {}
    event_story: List[Tuple[int, int, str]] = []
    unit_story: List[Tuple[int, int, int, int, str]] = []
    dungeon_name: Dict[int, str] = {}
    team_max_stamina: Dict[int, int] = {}
    room_item_max_level: Dict[int, int] = {}
    campaign_gacha: Dict[int, Tuple[str, str, List[int]]] = {}
    love_cake: List[Tuple[int, int]] = []
    love_char: Dict[int, Tuple[int, int]] = {}
    quest_info: Dict[int, Tuple[int, int]] = {}
    clan_battle_period: Dict[int, Tuple[str, str]] = {}
    chara_fortune_schedule: Dict[int, Tuple[str, str]] = {}
    hatsune_item: Dict[int, Tuple[int, int]] = {}
    quest_to_event_id: Dict[int, int] = {}
    quest_name: Dict[int, str] = {}
    training_quest_exp: Dict[int, str] = {}
    training_quest_mana: Dict[int, str] = {}
    unit_unique_equip_id: Dict[int, int] = {}
    unique_equip_required: Dict[int, Dict[int, typing.Counter[Tuple[eInventoryType, int]]]] = rec_counter(3)
    unique_equip_rank_max_level: Dict[int, int] = rec_intdict(1)
    rarity_up_required: Dict[int, Dict[int, typing.Counter[Tuple[eInventoryType, int]]]] = rec_counter(3)
    pure_memory_to_unit: Dict[int, int] = {}
    memory_to_unit: Dict[int, int] = {}
    memory_quest: Dict[int, List[int]] = {}
    campaign_schedule: Dict[int, Tuple[int, int, str, str]] = {}
    hatsune_schedule: Dict[int, Tuple[str, str]] = {}
    unit_promotion: Dict[int, Dict[int, typing.Counter[Tuple[eInventoryType, int]]]] = rec_counter(3)
    equip_craft: Dict[Tuple[eInventoryType, int], List[Tuple[Tuple[eInventoryType, int], int]]] = {}
    equip_max_rank: int = 0
    equip_max_rank_equip_num: int = 0
    '''

    def update(self, dbmgr: dbmgr):
        
        with dbmgr.session() as db:
            self.unique_equip_rank_max_level: Dict[int, int] = (
                UniqueEquipmentEnhanceDatum.query(db)
                .group_by(lambda x: x.rank)
                .to_dict(lambda x: x.key, lambda x: x.max(lambda y: y.enhance_level))
            )

            self.equip_craft: Dict[Tuple[eInventoryType, int], List[Tuple[Tuple[eInventoryType, int], int]]] = (
                EquipmentCraft.query(db)
                .to_dict(lambda x: (eInventoryType.Equip, x.equipment_id), lambda x: [
                    ((eInventoryType.Equip, getattr(x, f'condition_equipment_id_{i}')),
                        getattr(x, f'consume_num_{i}')) for i in range(1, 11)
                ])
            )

            self.unit_promotion: Dict[int, Dict[int, typing.Counter[Tuple[eInventoryType, int]]]] = (
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

            for unit_id in self.unit_promotion:
                for rank in range(max(self.unit_promotion[unit_id].keys()) - 1, 0, -1):
                    self.unit_promotion[unit_id][rank] += self.unit_promotion[unit_id][rank + 1]

            self.hatsune_schedule: Dict[int, Tuple[str, str]] = (
                HatsuneSchedule.query(db)
                .to_dict(lambda x: x.event_id, lambda x: (x.start_time, x.end_time))
            )
            
            self.campaign_schedule: Dict[int, Tuple[int, int, str, str]] = (
                CampaignSchedule.query(db)
                .to_dict(lambda x: x.id, lambda x: (x.campaign_category, x.value, x.start_time, x.end_time))
            )

            self.memory_questmemory_quest: Dict[int, List[int]] = (
                QuestDatum.query(db)
                .where(lambda x: x.quest_id >= 12000000 and x.quest_id < 13000000)
                .group_by(lambda x: x.quest_id)
                .to_dict(lambda x: x.key, lambda x:
                    x.select(lambda y: y.reward_image_1).to_list()
                )
            )

            self.unit_unique_equip_id: Dict[int, int] = (
                UnitUniqueEquip.query(db)
                .to_dict(lambda x: x.unit_id, lambda x: x.equip_id)
            )
            
            self.rarity_up_required: Dict[int, Dict[int, typing.Counter[Tuple[eInventoryType, int]]]] = (
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

            for unit_id in self.rarity_up_required:
                for rarity in range(max(self.rarity_up_required[unit_id].keys()) - 1, 0, -1):
                    self.rarity_up_required[unit_id][rarity] += self.rarity_up_required[unit_id][rarity + 1]
                self.rarity_up_required[unit_id][0] = self.rarity_up_required[unit_id][1]

            self.unique_equip_required: Dict[int, Dict[int, typing.Counter[Tuple[eInventoryType, int]]]] = (
                UniqueEquipmentCraft.query(db)
                .select_many(lambda x: [(
                    x.equip_id,
                    0,
                    x.reward_type_1,
                    x.item_id_1,
                    x.consume_num_1
                ), (
                    x.equip_id,
                    0,
                    x.reward_type_2,
                    x.item_id_2,
                    x.consume_num_2
                )])
                .concat(
                    UniqueEquipmentRankup.query(db)
                    .select_many(lambda x: [(
                        x.equip_id,
                        x.unique_equip_rank,
                        x.reward_type_1,
                        x.item_id_1,
                        x.consume_num_1
                    ), (
                        x.equip_id,
                        x.unique_equip_rank,
                        x.reward_type_2,
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

            for equip_id in self.unique_equip_required:
                for rank in range(max(self.unique_equip_required[equip_id].keys()) - 1, -1, -1):
                    self.unique_equip_required[equip_id][rank] += self.unique_equip_required[equip_id][rank + 1]

            self.training_quest_exp: Dict[int, str] = (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21002)
                .to_dict(lambda x: x.quest_id, lambda x: x.start_time)
            )

            self.training_quest_mana: Dict[int, str] = (
                TrainingQuestDatum.query(db)
                .where(lambda x: x.area_id == 21001)
                .to_dict(lambda x: x.quest_id, lambda x: x.start_time)
            )
            
            self.chara_fortune_schedule: Dict[int, Tuple[str, str]] = (
                CharaFortuneSchedule.query(db)
                .to_dict(lambda x: x.fortune_id, lambda x: (x.start_time, x.end_time))
            )

            self.clan_battle_period: Dict[int, Tuple[str, str]] = (
                ClanBattlePeriod.query(db)
                .to_dict(lambda x: x.clan_battle_id, lambda x: (x.start_time, x.end_time))
            )

            self.quest_info: Dict[int, Tuple[int, int]] = (
                QuestDatum.query(db)
                .concat(HatsuneQuest.query(db))
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: (x.daily_limit, x.stamina))
            )

            self.quest_name: Dict[int, str] = (
                QuestDatum.query(db)
                .concat(HatsuneQuest.query(db))
                .concat(ShioriQuest.query(db))
                .concat(TrainingQuestDatum.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x.quest_name)
            )

            self.main_story: List[Tuple[int, int, int, str]] = (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 2000000 and x.story_id < 3000000)
                .select(lambda x: (x.story_id, x.pre_story_id, x.unlock_quest_id, x.title))
                .to_list()
            )

            self.tower_story: List[Tuple[int, int, int, str, str]] = (
                TowerStoryDetail.query(db)
                .select(lambda x: (x.story_id, x.pre_story_id, x.unlock_quest_id, x.title, x.start_time))
                .to_list()
            )

            self.floor2clositer: Dict[int, int] = (
                TowerAreaDatum.query(db)
                .to_dict(lambda x: x.max_floor_num, lambda x: x.cloister_quest_id)
            )

            self.tower2floor: Dict[int, int] = (
                TowerQuestDatum.query(db)
                .to_dict(lambda x: x.tower_quest_id, lambda x: x.floor_num)
            )

            self.team_max_stamina: Dict[int, int] = (
                ExperienceTeam.query(db)
                .to_dict(lambda x: x.team_level, lambda x: x.max_stamina)
            )

            self.event_story: List[Tuple[int, int, str]] = (
                EventStoryDetail.query(db)
                .where(lambda x: x.visible_type == 0)
                .select(lambda x: (x.story_id, x.pre_story_id, x.title))
                .to_list()
            )

            self.unit_story: List[Tuple[int, int, int, int, str]] = (
                StoryDetail.query(db)
                .where(lambda x: x.story_id >= 1000000 and x.story_id < 2000000)
                .select(lambda x: (x.story_id, x.pre_story_id, x.story_group_id, x.love_level, x.title))
                .to_list()
            )

            self.inventory_name: Dict[Tuple[eInventoryType, int], str] = (
                EquipmentDatum.query(db)
                .select(lambda x: (eInventoryType.Equip, x.equipment_id, x.equipment_name))
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
                .to_dict(lambda x: (x[0], x[1]), lambda x: x[2])
            )

            self.inventory_name[(eInventoryType.Stamina, 93001)] = "体力"
            self.inventory_name[(eInventoryType.TeamExp, 92001)] = "经验"
            self.inventory_name[(eInventoryType.Jewel, 91002)] = "宝石"
            self.inventory_name[(eInventoryType.Gold, 94002)] = "mana"

            self.room_item_max_level: Dict[int, int] = (
                RoomItem.query(db)
                .to_dict(lambda x: x.id, lambda x: x.max_level)
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
            
            self.six_area: Dict[int, Tuple[int, int]] = (
                QuestDatum.query(db)
                .where(lambda x: x.quest_id >= 13000000 and x.quest_id < 14000000)
                .to_dict(lambda x: x.quest_id, lambda x: (x.reward_image_1, self.pure_memory_to_unit[x.reward_image_1]))
            )

            self.tower: Dict[int, Tuple[int, int]] = (
                TowerSchedule.query(db)
                .to_dict(lambda x: x.tower_schedule_id, lambda x: (x.start_time, x.end_time))
            )
            
            self.dungeon_name: Dict[int, str] = (
                DungeonArea.query(db)
                .to_dict(lambda x: x.dungeon_area_id, lambda x: x.dungeon_name)
            )
            
            gacha_list = (
                CampaignFreegachaDatum.query(db)
                .group_by(lambda x: x.campaign_id)
                .to_dict(lambda x: x.key, lambda x: [i.gacha_id for i in x])
            )
            
            self.campaign_gacha: Dict[int, Tuple[int, int, List[int]]] = (
                CampaignFreegacha.query(db)
                .to_dict(lambda x: x.campaign_id, lambda x: (x.start_time, x.end_time, gacha_list[x.campaign_id]))
            )
            
            self.love_char: Dict[int, Tuple[int, int]] = (
                LoveChara.query(db)
                .group_by(lambda x: x.rarity)
                .to_dict(lambda x: x.key, lambda x:
                    x.select(lambda i: (i.love_level, i.total_love)).max()
                )
            )

            self.love_cake: List[Tuple[int, int]] = (
                ItemDatum.query(db)
                .where(lambda x: x.item_id >= 50000 and x.item_id < 51000)
                .select(lambda x: (x.item_id, x.value))
                .to_list()
            )

            self.love_cake = self.love_cake[::-1]

            self.quest_to_event_id: Dict[int, int] = (
                HatsuneQuest.query(db)
                .concat(ShioriQuest.query(db))
                .to_dict(lambda x: x.quest_id, lambda x: x.event_id)
            )
            
            self.hatsune_item: Dict[int, Tuple[int, int]] = (
                HatsuneItem.query(db)
                .to_dict(lambda x: x.event_id, lambda x: (x.boss_ticket_id, x.gacha_ticket_id))
            )

    def get_inventory_name(self, item: InventoryInfo) -> str:
        try:
            return self.inventory_name[(item.type, item.id)]
        except:
            return f"未知物品({item.id})"

    def get_inventory_name_san(self, item: Tuple[eInventoryType, int]) -> str:
        try:
            return self.inventory_name[(item[0], item[1])]
        except:
            return f"未知物品({item[1]})"

    def is_daily_mission(self, mission_id: int) -> bool:
        return mission_id in self.daily_mission

    def is_exp_upper(self, item: Tuple[eInventoryType, int]) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 20000 and item[1] < 21000

    def is_equip_upper(self, item: Tuple[eInventoryType, int]) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 22000 and item[1] < 23000

    def is_unit_memory(self, item: Tuple[eInventoryType, int]) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 31000 and item[1] < 32000

    def is_unit_pure_memory(self, item: Tuple[eInventoryType, int]) -> bool:
        return item[0] == eInventoryType.Item and item[1] >= 32000 and item[1] < 33000

    def is_equip(self, item: Tuple[eInventoryType, int]) -> bool:
        return item[0] == eInventoryType.Equip and item[1] >= 101000 and item[1] < 140000

    def is_room_item_level_upable(self, team_level: int, item: RoomUserItem) -> bool:
        return item.room_item_level < self.room_item_max_level[item.room_item_id] and team_level // 10 >= item.room_item_level and (item.level_up_end_time is None or item.level_up_end_time < time.time())

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

    def campaign_info(self, campaign_id: int) -> Tuple[str, str, List[int]]:
        return self.campaign_gacha[campaign_id]

    def is_heart_piece_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id][0] == eCampaignCategory.ITEM_DROP_AMOUNT_UNIQUE_EQUIP

    def is_star_cup_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id][0] == eCampaignCategory.ITEM_DROP_AMOUNT_HIGH_RARITY_EQUIP

    def is_normal_quest_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id][0] == eCampaignCategory.ITEM_DROP_AMOUNT_NORMAL

    def is_hard_quest_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id][0] == eCampaignCategory.ITEM_DROP_AMOUNT_HARD

    def is_very_hard_quest_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id][0] == eCampaignCategory.ITEM_DROP_AMOUNT_VERY_HARD

    def is_dungeon_mana_double(self, campaign_id: int) -> bool:
        return self.campaign_schedule[campaign_id][0] == eCampaignCategory.GOLD_DROP_AMOUNT_DUNGEON

    def get_dungeon_mana_before_day(self) -> int:
        dungeon = min([schedule for schedule in self.campaign_schedule.values() if schedule[0] == eCampaignCategory.GOLD_DROP_AMOUNT_DUNGEON and db.parse_time(schedule[2]) > datetime.datetime.now()], lambda x: x[2])
        today = self.get_today_start_time()
        dungeon = self.get_start_time(db.parse_time(dungeon[2]))
        return (dungeon - today).days

    def get_newest_tower_id(self):
        return max(self.tower, key = lambda x: self.tower[x][0])

    def max_total_love(self, rarity: int):
        love_info: Tuple[int, int] = (0, 0)
        for key, value in self.love_char.items():
            if rarity >= key:
                love_info = max(love_info, value)
        return love_info

    def is_clan_battle_time(self) -> bool:
        now = datetime.datetime.now()
        for key, (start_time, end_time) in list(self.clan_battle_period.items()):
            start_time = self.parse_time(start_time)
            end_time = self.parse_time(end_time)
            if now > end_time:
                self.clan_battle_period.pop(key)
            elif now >= start_time:
                return True
        return False

    def is_cf_time(self) -> bool:
        now = datetime.datetime.now()
        for key, (start_time, end_time) in list(self.chara_fortune_schedule.items()):
            start_time = self.parse_time(start_time)
            end_time = self.parse_time(end_time)
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

    def craft_equip(self, equip: Tuple[eInventoryType, int], num: int) -> typing.Counter[Tuple[eInventoryType, int]]: # 依赖关系不深，没必要写成拓扑图求解
        if equip not in self.equip_craft:
            return Counter({equip: num})
        sub_results = map(lambda token: self.craft_equip(token[0], token[1] * num), self.equip_craft[equip])
        res = reduce(lambda x, y: x + y, sub_results, Counter())
        return res

db = database()