from .base import Component
from .apiclient import apiclient
from ..model.modelbase import *
from typing import Callable, Coroutine, Any, Set, Dict, Tuple
from ..model.common import *
from .database import db
import datetime

class datamgr(Component[apiclient]):
    settings: IniSetting = None
    dungeon_avaliable: bool = False
    finishedQuest: Set[int] = set()
    jewel: UserJewel = None
    gold: UserGold = None
    clan: int = 0
    cf: RaceLoginBonusInfo = None
    dungeon_area_id: int = 0
    donation_num: int = 0
    team_level: int = 0
    stamina: int = 0
    unit: Dict[int, UnitData] = None
    unit_love: Dict[int, UserChara] = None
    recover_stamina_exec_count: int = 0
    training_quest_count: TrainingQuestCount = None
    training_quest_max_count: TrainingQuestCount = None
    quest_dict: Dict[int, UserQuestInfo] = None
    hatsune_quest_dict: Dict[int, Dict[int, HatsuneUserEventQuest]] = {}
    name: str = None
    clan_like_count: int = 0
    user_my_quest: List[UserMyQuest] = None
    _inventory: Dict[Tuple[eInventoryType, int], int] = {}
    read_story_ids: List[int] = None
    unlock_story_ids: List[int] = None
    event_statuses: List[EventStatus] = None
    tower_status: TowerStatus = None
    deck_list: Dict[ePartyType, LoadDeckData] = {}

    def clear_inventory(self):
        self._inventory.clear()
        self.hatsune_quest_dict.clear()

    def get_max_avaliable_quest(self, quests: Dict[int, str]):
        now = datetime.datetime.now()
        result = 0
        for quest_id, start_time in quests.items():
            start_time = db.parse_time(start_time)
            if now < start_time:
                continue
            if quest_id in self.quest_dict and self.quest_dict[quest_id].clear_flg == 3:
                result = max(result, quest_id)
        return result

    def get_max_avaliable_quest_exp(self):
        return self.get_max_avaliable_quest(db.training_quest_exp)

    def get_max_avaliable_quest_mana(self):
        return self.get_max_avaliable_quest(db.training_quest_mana)

    def update_inventory(self, item: InventoryInfo):
        token = (item.type, item.id)
        if token == db.mana:
            self.gold.gold_id_free = item.stock
        elif token == db.jewel:
            self.jewel.free_jewel = item.stock
        elif item.type == eInventoryType.Unit:
            self.unit[item.id] = item.unit_data
        else:
            self._inventory[token] = item.stock

    def recover_max_time(self, quest: int):
        if db.is_normal_quest(quest):
            return 0
        elif db.is_hard_quest(quest):
            return self.settings.recover_challenge_count.recovery_max_count
        elif db.is_very_hard_quest(quest):
            return self.settings.very_hard_recover_challenge_count.recovery_max_count
        elif db.is_heart_piece_quest(quest):
            return self.settings.equip_recover_challenge_count.recovery_max_count
        elif db.is_star_cup_quest(quest):
            return self.settings.high_rarity_equip_recover_challenge_count.recovery_max_count
        else: # hatsune, shiori 0
            return self.settings.hatsune_recover_challenge_count.recovery_max_count

    def get_inventory(self, item: Tuple[eInventoryType, int]) -> int:
        return self._inventory.get(item, 0)

    def set_inventory(self, item: Tuple[eInventoryType, int], value: int):
        self._inventory[item] = value

    def get_shop_gold(self, shop_id: int) -> int:
        if shop_id == eSystemId.NORMAL_SHOP: # 正常商店
            return self.gold.gold_id_free
        if shop_id == eSystemId.LIMITED_SHOP: # 限定商店
            return self.gold.gold_id_free
        elif shop_id == eSystemId.ARENA_SHOP: # jjc店
            return self.get_inventory((eInventoryType.Item, 90003))
        elif shop_id == eSystemId.GRAND_ARENA_SHOP: # pjjc店
            return self.get_inventory((eInventoryType.Item, 90004))
        elif shop_id == eSystemId.EXPEDITION_SHOP: # 地下城店
            return self.get_inventory((eInventoryType.Item, 90002))
        elif shop_id == eSystemId.CLAN_BATTLE_SHOP: # 会战店
            return self.get_inventory((eInventoryType.Item, 90006))
        elif shop_id == eSystemId.MEMORY_PIECE_SHOP: # 女神店
            return self.get_inventory((eInventoryType.Item, 90005))
        elif shop_id == eSystemId.COUNTER_STOP_SHOP: # 大师店
            return self.get_inventory((eInventoryType.Item, 90008))
        else:
            raise ValueError(f"未知的商店{shop_id}")

    async def request(self, request: Request[TResponse], next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        resp = await next(request)
        if resp: resp.update(self, request)
        return resp
