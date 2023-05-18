from .base import Component
from .apiclient import apiclient
from ..model.modelbase import *
from typing import Callable, Coroutine, Any, Set, Dict, Tuple
from ..model.common import *
from .database import db

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
    event_statuses: List[EventStatus] = None
    tower_status: TowerStatus = None
    deck_list: Dict[ePartyType, LoadDeckData] = []

    def clear_inventory(self):
        self._inventory.clear()
        self.hatsune_quest_dict.clear()

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

    def get_inventory(self, item: Tuple[eInventoryType, int]) -> int:
        return self._inventory.get(item, 0)

    def set_inventory(self, item: Tuple[eInventoryType, int], value: int):
        self._inventory[item] = value

    def get_shop_gold(self, shop_id: int) -> int:
        if shop_id == 201: # 正常商店
            return self.gold.gold_id_free
        if shop_id == 212: # 限定商店
            return self.gold.gold_id_free
        elif shop_id == 202: # jjc店
            return self.get_inventory((eInventoryType.Item, 90003))
        elif shop_id == 203: # pjjc店
            return self.get_inventory((eInventoryType.Item, 90004))
        elif shop_id == 204: # 地下城店
            return self.get_inventory((eInventoryType.Item, 90002))
        elif shop_id == 205: # 会战店
            return self.get_inventory((eInventoryType.Item, 90006))
        elif shop_id == 207: # 女神店
            return self.get_inventory((eInventoryType.Item, 90005))
        elif shop_id == 210: # 大师店
            return self.get_inventory((eInventoryType.Item, 90008))
        else:
            raise ValueError(f"未知的商店{shop_id}")

    async def request(self, request: Request[TResponse], next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        resp = await next(request)
        if resp: resp.update(self, request)
        return resp
