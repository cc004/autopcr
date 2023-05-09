from ..util.sqlite3 import RecordDAO
import time
from typing import Set, Dict, Tuple
from ..model.common import *
from .base import Container
import os

db_path = os.path.join(os.path.dirname(__file__), "../../", "redive_cn.db")

class database(Container["database"]):
    six_area: Dict[int, Tuple[int, int]] = {}
    inventory_name: Dict[Tuple[eInventoryType, int], str] = {}
    tower: Dict[int, Tuple[str, str]] = {}
    daily_mission: Set[int] = set()
    main_story: List[Tuple[int, int, int, str]] = []
    tower_story: List[Tuple[int, int, int, str]] = []
    tower2floor: Dict[int, int] = {}
    event_story: List[Tuple[int, int, str]] = []
    unit_story: List[Tuple[int, int, int, int, str]] = []
    dungeon_name: Dict[int, str] = {}
    team_max_stamina: Dict[int, int] = {}
    xinsui: Tuple[eInventoryType, int] = (eInventoryType.Equip, 140001)
    xingqiubei: Tuple[eInventoryType, int] = (eInventoryType.Item, 25001)
    mana: Tuple[eInventoryType, int] = (eInventoryType.Gold, 94002)
    jewel: Tuple[eInventoryType, int] = (eInventoryType.Jewel, 91002)
    room_item_max_level: Dict[int, int] = {}
    campaign: Dict[int, Tuple[str, str, List[int]]] = {}
    love_cake: List[Tuple[int, int]] = []
    love_char: Dict[int, Tuple[int, int]] = {}

    def __init__(self, path):
        db = RecordDAO(path)
        self.inventory_name[(eInventoryType.Stamina, 93001)] = "体力"
        self.inventory_name[(eInventoryType.TeamExp, 92001)] = "经验"
        self.inventory_name[(eInventoryType.Jewel, 91002)] = "宝石"
        self.inventory_name[(eInventoryType.Gold, 94002)] = "mana"

        for story in db.get_main_story_detail():
            id = story[0]
            pre_id = story[1]
            unlock_quest_id = story[2]
            title = story[3]
            self.main_story.append((id, pre_id, unlock_quest_id, title))

        for story in db.get_tower_story_detail():
            id = story[0]
            pre_id = story[1]
            unlock_quest_id = story[2]
            title = story[3]
            self.tower_story.append((id, pre_id, unlock_quest_id, title))

        for quest in db.get_tower_quest_detail():
            quest_id = quest[0]
            floor_num = quest[1]
            self.tower2floor[quest_id] = floor_num

        for team_info in db.get_team_max_stamina():
            team_level = team_info[0]
            max_stamina = team_info[1]
            self.team_max_stamina[team_level] = max_stamina

        for story in db.get_event_story_detail():
            id = story[0]
            pre_id = story[1]
            title = story[2]
            self.event_story.append((id, pre_id, title))

        for story in db.get_unit_story_detail():
            id = story[0]
            pre_id = story[1]
            story_group_id = story[2]
            love_level = story[3]
            title = story[4]
            self.unit_story.append((id, pre_id, story_group_id, love_level, title))

        for equitement in db.get_equitement_data():
            id = equitement[0]
            name = equitement[1]
            self.inventory_name[(eInventoryType.Equip, id)] = name
        for item in db.get_item_data():
            id = item[0]
            name = item[1]
            self.inventory_name[(eInventoryType.Item, id)] = name
        for unit in db.get_unit_data():
            id = unit[0]
            name = unit[1]
            self.inventory_name[(eInventoryType.Unit, id)] = name
        for unit in db.get_room_data():
            id = unit[0]
            name = unit[1]
            max_level = unit[2]
            self.inventory_name[(eInventoryType.RoomItem, id)] = name
            self.room_item_max_level[id] = max_level

        for daily_mission in db.get_daily_mission():
            mission_id = daily_mission[0]
            self.daily_mission.add(mission_id)

        memory2unit = {}
        for material in db.get_unlock_rarity_six():
            unitid = material[0]
            pure_memory = material[1]
            memory2unit[pure_memory] = unitid
        for area in db.get_six_area_data():
            id = area[0]
            pure_memory = area[1]
            self.six_area[id] = (pure_memory, memory2unit[pure_memory])

        for tower in db.get_tower_schedule():
            tower_id = tower[0]
            start_time = tower[1]
            end_time = tower[2]
            self.tower[tower_id] = (start_time, end_time)

        for dungeon in db.get_dungeon_name():
            dungeon_id = dungeon[0]
            dungeon_name = dungeon[1]
            self.dungeon_name[dungeon_id] = dungeon_name

        for campaign in db.get_campaign():
            campaign_id = campaign[0]
            start_time = campaign[1]
            end_time = campaign[2]
            gacha_list = [i[0] for i in db.get_campaign_gacha(campaign_id)]
            self.campaign[campaign_id] = (start_time, end_time, gacha_list)

        for love_chara in db.get_love_chara():
            love_level = love_chara[0]
            totle_love = love_chara[1]
            rarity = love_chara[2]
            if rarity not in self.love_char:
                self.love_char[rarity] = (love_level, totle_love)
            else:
                self.love_char[rarity] = max(self.love_char[rarity], (love_level, totle_love))

        for love_cake in db.get_love_cake():
            cake_id = love_cake[0]
            cake_value = love_cake[1]
            self.love_cake.append((cake_id, cake_value))
        self.love_cake = self.love_cake[::-1]

    def get_inventory_name(self, item: InventoryInfo):
        try:
            return self.inventory_name[(item.type, item.id)]
        except:
            return f"未知物品({item.id})"

    def get_inventory_name_san(self, item: Tuple[eInventoryType, int]):
        try:
            return self.inventory_name[(item[0], item[1])]
        except:
            return f"未知物品({item[1]})"

    def is_daily_mission(self, mission_id: int):
        return mission_id in self.daily_mission

    def is_exp_upper(self, item: Tuple[eInventoryType, int]):
        return item[0] == eInventoryType.Item and item[1] >= 20000 and item[1] < 21000

    def is_equip_upper(self, item: Tuple[eInventoryType, int]):
        return item[0] == eInventoryType.Item and item[1] >= 22000 and item[1] < 23000

    def is_unit_memory(self, item: Tuple[eInventoryType, int]):
        return item[0] == eInventoryType.Item and item[1] >= 31000 and item[1] < 32000

    def is_unit_pure_memory(self, item: Tuple[eInventoryType, int]):
        return item[0] == eInventoryType.Item and item[1] >= 32000 and item[1] < 33000

    def is_equip(self, item: Tuple[eInventoryType, int]):
        return item[0] == eInventoryType.Equip and item[1] >= 101000 and item[1] < 140000

    def is_room_item_level_upable(self, team_level: int, item: RoomUserItem):
        return item.room_item_level < self.room_item_max_level[item.room_item_id] and team_level // 10 >= item.room_item_level and (item.level_up_end_time is None or item.level_up_end_time < time.time())

    def campaign_info(self, campaign_id: int):
        return self.campaign[campaign_id]

    def max_total_love(self, rarity: int):
        love_info: Tuple[int, int] = (0, 0)
        for key, value in self.love_char.items():
            if rarity >= key:
                love_info = max(love_info, value)
        return love_info

db = database(db_path)

def init_db():
    global db
    db = database(db_path)

