from .base import Component
from .apiclient import apiclient
from ..model.modelbase import *
from typing import Callable, Coroutine, Any, Set, Dict, Tuple
from ..model.common import *

class datamgr(Component[apiclient]):
    settings: IniSetting = None
    dungeon_avaliable: bool = False
    finishedQuest: Set[int] = set()
    jewel: UserJewel = None
    clan: int = 0
    dungeon_area_id: int = 0
    donation_num: int = 0
    team_level: int = 0
    stamina: int = 0
    recover_stamina_exec_count: int = 0
    training_quest_count: TrainingQuestCount = None
    quest_dict: Dict[int, UserQuestInfo] = None
    name: str = None
    clan_like_count: int = 0
    user_my_quest: List[UserMyQuest] = None
    _inventory: Dict[Tuple[eInventoryType, int], int] = {}

    def clear_inventory(self):
        self._inventory.clear()

    def update_inventory(self, item: InventoryInfo):
        self._inventory[(item.type, item.id)] = item.stock

    def get_inventory(self, item: Tuple[eInventoryType, int]):
        return self._inventory.get(item, 0)

    def set_inventory(self, item: Tuple[eInventoryType, int], value: int):
        self._inventory[item] = value

    async def request(self, request: Request[TResponse], next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        resp = await next(request)
        if resp: resp.update(self, request)
        return resp
