from collections import Counter
from .base import Component, RequestHandler
from .apiclient import apiclient
from ..model.modelbase import *
from typing import Callable, Coroutine, Any, Set, Dict, Tuple, Union
import typing
from ..model.common import *
from ..model.custom import ItemType
import datetime
import json, base64, gzip
from ..db.assetmgr import instance as assetmgr
from ..db.dbmgr import instance as dbmgr
from ..db.database import db
from ..db.models import ItemDatum, TrainingQuestDatum
from ..util.linq import flow
from asyncio import Lock


class datamgr(Component[apiclient]):
    settings: IniSetting = None
    dungeon_avaliable: bool = False
    finishedQuest: Set[int] = None
    jewel: UserJewel = None
    gold: UserGold = None
    uid: int = 0
    clan: int = 0
    cf: RaceLoginBonusInfo = None
    dungeon_area_id: int = 0
    donation_num: int = 0
    team_level: int = 0
    stamina: int = 0
    missions: List[UserMissionInfo] = None
    growth_unit: Dict[int, GrowthInfo] = None
    unit: Dict[int, UnitData] = None
    unit_love_data: Dict[int, UserChara] = None
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
    gacha_point: Dict[int, GachaPointInfo] = None
    dispatch_units: List[UnitDataForClanMember] = None
    event_sub_story: Dict[int, EventSubStory] = None
    user_gold_bank_info: UserBankGoldInfo = None

    def __init__(self):
        self.finishedQuest = set()
        self.hatsune_quest_dict = {}
        self._inventory = {}
        self.deck_list = {}
        self.campaign_list = []

    lck = Lock()

    @staticmethod
    def lock():
        return datamgr.lck

    @staticmethod
    async def try_update_database(ver: int):
        async with datamgr.lock():
            if not assetmgr.ver or assetmgr.ver < ver:
                await assetmgr.init(ver)
            if not dbmgr.ver or dbmgr.ver < assetmgr.ver: 
                await dbmgr.update_db(assetmgr)
                db.update(dbmgr)

    def is_heart_piece_campaign(self) -> bool:
        return any(db.is_heart_piece_campaign(campaign_id) for campaign_id in self.campaign_list)

    def is_star_cup_campaign(self) -> bool:
        return any(db.is_star_cup_campaign(campaign_id) for campaign_id in self.campaign_list)

    def is_quest_campaign(self) -> bool:
        return self.is_normal_quest_campaign() or self.is_hard_quest_campaign() or self.is_very_hard_quest_campaign()

    def is_normal_quest_campaign(self) -> bool:
        return any(db.is_normal_quest_campaign(campaign_id) for campaign_id in self.campaign_list)

    def is_hard_quest_campaign(self) -> bool:
        return any(db.is_hard_quest_campaign(campaign_id) for campaign_id in self.campaign_list)

    def is_very_hard_quest_campaign(self) -> bool:
        return any(db.is_very_hard_quest_campaign(campaign_id) for campaign_id in self.campaign_list)

    def is_dungeon_mana_campaign(self) -> bool:
        return any(db.is_dungeon_mana_campaign(campaign_id) for campaign_id in self.campaign_list)

    def is_campaign(self, campaign: str) -> bool:
        campaign_list = {
            "n2": lambda: self.get_normal_quest_campaign_times() == 2,
            "n3": lambda: self.get_normal_quest_campaign_times() == 3,
            "n4及以上": lambda: self.get_normal_quest_campaign_times() >= 4,
            "h2": lambda: self.get_hard_quest_campaign_times() == 2,
            "h3及以上": lambda: self.get_hard_quest_campaign_times() >= 3,
            "vh2": lambda: self.get_very_hard_quest_campaign_times() == 2,
            "vh3及以上": lambda: self.get_very_hard_quest_campaign_times() >= 3,
        }
        if campaign not in campaign_list:
            raise ValueError(f"不支持的庆典查询：{campaign}")
        return campaign_list[campaign]()

    def get_campaign_times(self, condition_func) -> int:
        times = [db.get_campaign_times(campaign_id) for campaign_id in self.campaign_list if condition_func(campaign_id)]
        if not times:
            return 0
        assert(len(times) == 1)
        return int(times[0] // 1000)

    def get_heart_piece_campaign_times(self) -> int:
        return self.get_campaign_times(db.is_heart_piece_campaign)

    def get_star_cup_campaign_times(self) -> int:
        return self.get_campaign_times(db.is_star_cup_campaign)

    def get_normal_quest_campaign_times(self) -> int:
        return self.get_campaign_times(db.is_normal_quest_campaign)

    def get_hard_quest_campaign_times(self) -> int:
        return self.get_campaign_times(db.is_hard_quest_campaign)

    def get_very_hard_quest_campaign_times(self) -> int:
        return self.get_campaign_times(db.is_very_hard_quest_campaign)

    def get_dungeon_mana_campaign_times(self) -> int:
        return self.get_campaign_times(db.is_dungeon_mana_campaign)

    def clear_inventory(self):
        self._inventory.clear()
        self.hatsune_quest_dict.clear()

    def get_unique_equip_material_demand(self, equip_slot:int, unit_id: int, token: ItemType) -> int:
        if unit_id not in db.unit_unique_equip[equip_slot]:
            return 0
        equip_id = db.unit_unique_equip[equip_slot][unit_id].equip_id
        rank = self.unit[unit_id].unique_equip_slot[0].rank if unit_id in self.unit and self.unit[unit_id].unique_equip_slot else -1
        return (
            flow(db.unique_equip_required[equip_id].items())
            .where(lambda x: x[0] >= rank)
            .select(lambda x: x[1][token])
            .sum()
        )

    def get_unit_eqiup_demand(self, unit_id: int) -> typing.Counter[ItemType]:
        unit = self.unit[unit_id]
        rank = unit.promotion_level

        return db.craft_equip(
            flow(db.unit_promotion_equip_count[unit_id].items())
            .where(lambda x: x[0] >= rank)
            .select(lambda x: x[1])
            .sum(seed=Counter()) - 
            Counter((eInventoryType(eInventoryType.Equip), equip.id) for equip in unit.equip_slot if equip.is_slot)
        )[0]

    def get_exceed_level_unit_demand(self, unit_id: int, token: ItemType) -> int:
        if unit_id in self.unit and self.unit[unit_id].exceed_stage:
            return 0
        if unit_id not in db.exceed_level_unit_required: # 怎么还没有环奈
            return 0
        return db.exceed_level_unit_required[unit_id].consume_num_1 # 1 memory 2 ring

    def get_rarity_memory_demand(self, unit_id: int, token: ItemType, rarity_slot_num: int) -> int:
        rarity = -1
        if unit_id in self.unit:
            unit_data = self.unit[unit_id]
            rarity = unit_data.unit_rarity
            if unit_data.unlock_rarity_6_item and getattr(unit_data.unlock_rarity_6_item, f"slot_{rarity_slot_num}"):
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
        
        return (
            flow(db.normal_quest_rewards.items())
            .to_dict(lambda x: x[0], lambda x:
                flow(x[1].items())
                .select(lambda y: datamgr._weight_mapper(require_equip.get(y[0], 0)) * y[1])
                .sum() + 
                (1000000 if x[1] and flow(x[1].items())
                .select(lambda y: require_equip.get(y[0], 0))
                .max() > 0 else 0)
            )
        )

    def get_equip_demand(self, start_rank: Union[None, int] = None, like_unit_only: bool = False) -> typing.Counter[ItemType]:
        cnt: typing.Counter[ItemType] = Counter()
        for unit_id in self.unit:
            if start_rank and self.unit[unit_id].promotion_level < start_rank:
                continue
            if like_unit_only and not self.unit[unit_id].favorite_flag:
                continue
            need = self.get_unit_eqiup_demand(unit_id)
            if need:
                cnt += need
        return cnt 

    def get_demand_gap(self, required: typing.Counter[ItemType], filter: Callable[[ItemType], bool] = lambda x: True) -> typing.Counter[ItemType]:
        all = set(self._inventory) | set(required)
        demand = Counter({token: required[token] - self.get_inventory(token) for token in all if filter(token)})
        return demand

    def get_equip_demand_gap(self, start_rank: Union[None, int] = None, like_unit_only: bool = False) -> typing.Counter[ItemType]:
        demand = self.get_equip_demand(start_rank, like_unit_only)
        gap = self.get_demand_gap(demand, lambda x: db.is_equip(x, uncraftable_only=True))
        return gap

    def get_memory_demand(self) -> typing.Counter[ItemType]:
        result: typing.Counter[ItemType] = Counter()
        for memory_id, unit_id in db.memory_to_unit.items():
            token = (eInventoryType.Item, memory_id)
            if token not in db.inventory_name: # 未来角色
                continue

            need = self.get_rarity_memory_demand(unit_id, token, 2) + self.get_unique_equip_memory_demand(unit_id, token) + self.get_exceed_level_unit_demand(unit_id, token)
            result[token] += need

        return result

    def get_pure_memory_demand(self) -> typing.Counter[ItemType]:
        result: typing.Counter[ItemType] = Counter()
        for token, unit_id in db.pure_memory_to_unit.items():
            if token not in db.inventory_name: # 未来角色
                continue

            need = self.get_rarity_memory_demand(unit_id, token, 1)
            result[token] += need

        return result

    def get_memory_demand_gap(self) -> typing.Counter[ItemType]: # need -- >0
        demand = self.get_memory_demand()
        gap = self.get_demand_gap(demand, lambda x: db.is_unit_memory(x))
        return gap

    def get_pure_memory_demand_gap(self) -> typing.Counter[ItemType]: # need -- >0
        demand = self.get_pure_memory_demand()
        gap = self.get_demand_gap(demand, lambda x: db.is_unit_pure_memory(x))
        return gap

    def get_suixin_demand(self) -> Tuple[List[Tuple[ItemType, int]], int]:
        cnt = 0
        result: List[Tuple[ItemType, int]] = []
        for unit_id in self.unit:
            token = (eInventoryType.Unit, unit_id)
            need = self.get_unique_equip_material_demand(1, unit_id, db.xinsui)
            if need:
                cnt += need
                result.append((token, need))
        return result, cnt 

    def get_unique_equip_memory_demand(self, unit_id: int, token: ItemType) -> int:
        return self.get_unique_equip_material_demand(1, unit_id, token)

    def get_max_quest(self, quests: Dict[int, TrainingQuestDatum], sweep_available = False) -> int:
        now = datetime.datetime.now()
        return (
            flow(quests.keys())
            .where(lambda x: now >= db.parse_time(quests[x].start_time) and 
                   (not sweep_available or 
                   (quests[x].quest_id in self.quest_dict and self.quest_dict[x].clear_flg == 3)))
            .max()
        )

    def get_max_quest_exp(self, sweep_available = False) -> int:
        return self.get_max_quest(db.training_quest_exp, sweep_available)

    def get_max_quest_mana(self, sweep_available = False) -> int:
        return self.get_max_quest(db.training_quest_mana, sweep_available)

    def get_demand(self, need_point: int, items: List[ItemDatum], need_point_limit: int) -> typing.Counter[ItemType]: # not enough return empty counter
        from ..util.ilp_solver import ilp_solver
        ub = [self.get_inventory((eInventoryType.Item, item.item_id)) for item in items]
        effect = [item.value for item in items]
        ok, ret = ilp_solver(ub, need_point, need_point_limit, effect)
        if not ok:
            return Counter()
        return Counter({(eInventoryType.Item, items[i].item_id): ret[i] for i in range(len(items)) if ret[i]})

    def get_level_up_exp_potion_demand(self, exp_demand: int, exp_demand_limit: int = -1) -> typing.Counter[ItemType]: 
        return self.get_demand(exp_demand, db.exp_potion, exp_demand_limit)

    def get_love_up_cake_demand(self, love_demand: int, love_demand_limit :int = -1) -> typing.Counter[ItemType]:
        return self.get_demand(love_demand, db.love_cake, love_demand_limit)

    def get_equip_enhance_stone_demand(self, enhance_pt: int, enhance_pt_limit: int = -1) -> typing.Counter[ItemType]:
        return self.get_demand(enhance_pt, db.equip_enhance_stone, enhance_pt_limit)

    def get_mana(self, include_bank: bool = False) -> int:
        mana = self.gold.gold_id_free + self.gold.gold_id_pay + (self.user_gold_bank_info.bank_gold if include_bank and self.user_gold_bank_info else 0)
        return mana

    def update_inventory(self, item: InventoryInfo):
        token = (item.type, item.id)
        if token == db.mana:
            self.gold.gold_id_free = item.stock
        elif token == db.jewel:
            self.jewel.free_jewel = item.stock
        elif item.type == eInventoryType.Unit:
            self.unit[item.id] = item.unit_data
            if item.id not in self.unit_love_data:
                unit_id = item.id // 100
                self.unit_love_data[unit_id] = UserChara()
                self.unit_love_data[unit_id].chara_id = unit_id
                self.unit_love_data[unit_id].chara_love = 0
                self.unit_love_data[unit_id].love_level = 0
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

    def is_empty_deck(self, party_type: ePartyType):
        return all(value == 0 for key, value in vars(self.deck_list[party_type]).items() if key.startswith('unit_id'))

    def is_mission_finished(self, system_id: int):
        return len(list(
            flow(self.missions)
            .where(lambda x: 
                   db.is_daily_mission(x.mission_id) and
                   x.mission_status != eMissionStatusType.NoClear and 
                   db.daily_mission_data[x.mission_id].system_id == system_id)
        )) != 0

    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        resp = await next.request(request)
        if resp: await resp.update(self, request)
        return resp

