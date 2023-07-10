from collections import Counter
from .base import Component
from .apiclient import apiclient
from ..model.modelbase import *
from typing import Callable, Coroutine, Any, Set, Dict, Tuple, Union
import typing
from ..model.common import *
import datetime
from functools import reduce
import json, base64, gzip
from ..db.assetmgr import instance as assetmgr
from ..db.dbmgr import instance as dbmgr
from ..db.database import db
from ..db.models import TrainingQuestDatum
from ..util.linq import flow

class datamgr(Component[apiclient]):
    settings: IniSetting = None
    dungeon_avaliable: bool = False
    finishedQuest: Set[int] = None
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
    hatsune_quest_dict: Dict[int, Dict[int, HatsuneUserEventQuest]] = None
    name: str = None
    clan_like_count: int = 0
    user_my_quest: List[UserMyQuest] = None
    _inventory: Dict[ItemType, int] = None
    read_story_ids: List[int] = None
    unlock_story_ids: List[int] = None
    event_statuses: List[EventStatus] = None
    tower_status: TowerStatus = None
    deck_list: Dict[ePartyType, LoadDeckData] = None
    campaign_list: List[int] = None

    def __init__(self):
        self.finishedQuest = set()
        self.hatsune_quest_dict = {}
        self._inventory = {}
        self.deck_list = {}
        self.campaign_list = []


    async def try_update_database(self, ver: int):
        if not assetmgr.ver or assetmgr.ver < ver:
            await assetmgr.init(ver)
            await dbmgr.update_db(assetmgr)
            db.update(dbmgr)

    def is_heart_piece_double(self) -> bool:
        return any(db.is_heart_piece_double(campaign_id) for campaign_id in self.campaign_list)

    def is_star_cup_double(self) -> bool:
        return any(db.is_star_cup_double(campaign_id) for campaign_id in self.campaign_list)

    def is_normal_quest_double(self) -> bool:
        return any(db.is_normal_quest_double(campaign_id) for campaign_id in self.campaign_list)

    def is_hard_quest_double(self) -> bool:
        return any(db.is_hard_quest_double(campaign_id) for campaign_id in self.campaign_list)

    def is_very_hard_quest_double(self) -> bool:
        return any(db.is_very_hard_quest_double(campaign_id) for campaign_id in self.campaign_list)

    def is_dungeon_mana_double(self) -> bool:
        return any(db.is_dungeon_mana_double(campaign_id) for campaign_id in self.campaign_list)

    def clear_inventory(self):
        self._inventory.clear()
        self.hatsune_quest_dict.clear()

    def get_need_unique_equip_material(self, unit_id: int, token: ItemType) -> int:
        if unit_id not in db.unit_unique_equip:
            return 0
        equip_id = db.unit_unique_equip[unit_id].equip_id
        rank = self.unit[unit_id].unique_equip_slot[0].rank if unit_id in self.unit and self.unit[unit_id].unique_equip_slot else -1
        return (
            flow(db.unique_equip_required[equip_id].items())
            .where(lambda x: x[0] > rank)
            .select(lambda x: x[1][token])
            .sum()
        )

    def get_need_unit_need_eqiup(self, unit_id: int) -> typing.Counter[ItemType]:
        unit = self.unit[unit_id]
        rank = unit.promotion_level

        return db.craft_equip(
            flow(db.unit_promotion[unit_id].items())
            .where(lambda x: x[0] >= rank)
            .select(lambda x: x[1])
            .sum(seed=Counter()) - 
            Counter((eInventoryType.Equip, equip.id) for equip in unit.equip_slot if equip.is_slot)
        )

    def get_need_rarity_memory(self, unit_id: int, token: ItemType) -> int:
        rarity = -1
        if unit_id in self.unit:
            unit_data = self.unit[unit_id]
            rarity = unit_data.unit_rarity
            if unit_data.unlock_rarity_6_item and unit_data.unlock_rarity_6_item.slot_2:
                rarity = 6
        return (
            flow(db.rarity_up_required[unit_id].items())
            .where(lambda x: x[0] > rarity)
            .select(lambda x: x[1][token])
            .sum()
        )

    def get_library_unit_data(self) -> List:
        result = []
        for unit in self.unit.values():
            if unit.id == 170101 or unit.id == 170201: # 竟然没有春环
                continue
            equip_slot = ""
            for equip in unit.equip_slot:
                equip_slot += "1" if equip.is_slot else "0"
            result.append({ 
                "e": equip_slot,
                "p": unit.promotion_level,
                "r": str(unit.unit_rarity),
                "u": hex(unit.id // 100)[2:],
                "t": f"{db.equip_max_rank}.{db.equip_max_rank_equip_num}",
                "q": str(db.unique_equip_rank[unit.unique_equip_slot[0].rank].enhance_level) if unit.unique_equip_slot and unit.unique_equip_slot[0].rank > 0 else "0",
                "b": "true" if unit.exceed_stage else "false",
                "f": False
            })
        return result

    def get_library_equip_data(self) -> List:
        result = []
        candidate = [item for item in db.inventory_name if db.is_equip(item) and item not in db.equip_craft] + [db.xinsui]
        for equip in candidate:
            result.append({
                "c": hex(self.get_inventory(equip))[2:],
                "e": hex(equip[1])[2:],
                "a": "1",
            })
        return result

    def get_library_memory_data(self) -> List:
        result = []
        for memory_id, unit_id in db.memory_to_unit.items():
            if unit_id == 170101 or unit_id == 170201:
                continue
            result.append({
                "c": hex(self.get_inventory((eInventoryType.Item, memory_id)))[2:],
                "u": hex(unit_id)[2:],
            })

        return result

    def get_library_import_data(self) -> str:
        result = []
        result.append(self.get_library_unit_data()) 
        result.append(self.get_library_equip_data())
        result.append(self.get_library_memory_data())
        json_str = json.dumps(result)
        compressed_data = gzip.compress(json_str.encode('utf-8'))
        encoded_data = base64.b64encode(compressed_data).decode('utf-8')
        return encoded_data

    @staticmethod
    def _weight_mapper(cnt: int) -> float:
        return max(0, cnt) + max(0, cnt + 300) * .1 + max(0, cnt + 600) * .01 + max(0, cnt + 900) * .001

    def get_quest_weght(self, require_equip: typing.Counter[ItemType]) -> Dict[int, float]: # weight demand
        
        need = {token: num - self.get_inventory(token) for token, num in require_equip.items()}

        return (
            flow(db.normal_quest_rewards.items())
            .to_dict(lambda x: x[0], lambda x:
                flow(x[1].items())
                .select(lambda y: datamgr._weight_mapper(need.get(y[0], 0)) * y[1])
                .sum()
            )
        )
        '''
        def f(x: int, pos: int):
            wei = [0, 0.4, 0.4, 0.2]
            return x * wei[pos]

        need = {token: num - self.get_inventory(token) 
                for token, num in require_equip.items() 
                if num - self.get_inventory(token) > 0}

        quest_weight: Dict[int, Tuple[int, int]] = {
                quest.quest_id: 
                    (
                    sum(f(
                        need.get((eInventoryType.Equip, getattr(quest, f'reward_image_{i}')), 0), i
                    ) for i in range(1,4)),
                    max(f(
                        need.get((eInventoryType.Equip, getattr(quest, f'reward_image_{i}')), 0), i
                    ) for i in range(1,4)),
                     )
                for quest in db.normal_quest_data.values()
                }
        return quest_weight
        '''

    def get_need_equip(self, start_rank: Union[None, int] = None, like_unit_only: bool = False) -> Tuple[List[Tuple[ItemType, List[Tuple[ItemType, int]]]], typing.Counter[ItemType]]:
        cnt: typing.Counter[ItemType] = Counter()
        result: List[Tuple[ItemType, List[Tuple[ItemType, int]]]] = []
        for unit_id in self.unit:
            if start_rank and self.unit[unit_id].promotion_level < start_rank:
                continue
            if like_unit_only and not self.unit[unit_id].favorite_flag:
                continue
            token = (eInventoryType.Unit, unit_id)
            need = self.get_need_unit_need_eqiup(unit_id)
            if need:
                cnt += need
                result.append((token, list(need.items())))
        return result, cnt 

    def get_need_suixin(self) -> Tuple[List[Tuple[ItemType, int]], int]:
        cnt = 0
        result: List[Tuple[ItemType, int]] = []
        for unit_id in self.unit:
            token = (eInventoryType.Unit, unit_id)
            need = self.get_need_unique_equip_material(unit_id, db.xinsui)
            if need:
                cnt += need
                result.append((token, need))
        return result, cnt 

    def get_need_unique_equip_memory(self, unit_id: int, token: ItemType) -> int:
        return self.get_need_unique_equip_material(unit_id, token)

    def get_need_memory(self) -> Tuple[List[Tuple[ItemType, int]], int]:
        cnt = 0
        result: List[Tuple[ItemType, int]] = []
        for memory_id, unit_id in db.memory_to_unit.items():
            token = (eInventoryType.Item, memory_id)
            if token not in db.inventory_name: # 未来角色
                continue

            need = self.get_need_rarity_memory(unit_id, token) + self.get_need_unique_equip_memory(unit_id, token)
            cnt += need
            result.append((token, need))

        return result, cnt 

    def get_max_avaliable_quest(self, quests: Dict[int, TrainingQuestDatum]) -> int:
        now = datetime.datetime.now()
        result = 0
        for quest_id, quest in quests.items():
            start_time = db.parse_time(quest.start_time)
            if now < start_time:
                continue
            if quest_id in self.quest_dict and self.quest_dict[quest_id].clear_flg == 3:
                result = max(result, quest_id)
        return result

    def get_max_avaliable_quest_exp(self) -> int:
        return self.get_max_avaliable_quest(db.training_quest_exp)

    def get_max_avaliable_quest_mana(self) -> int:
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

    def recover_max_time(self, quest: int) -> int:
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

    def get_inventory(self, item: ItemType) -> int:
        return self._inventory.get(item, 0)

    def set_inventory(self, item: ItemType, value: int):
        self._inventory[item] = value

    def get_shop_gold(self, shop_id: int) -> int:
        if shop_id == eSystemId.NORMAL_SHOP: # 正常商店
            return self.gold.gold_id_free + self.gold.gold_id_pay
        if shop_id == eSystemId.LIMITED_SHOP: # 限定商店
            return self.gold.gold_id_free + self.gold.gold_id_pay
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
        if resp: await resp.update(self, request)
        return resp
