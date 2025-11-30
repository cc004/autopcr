from collections import Counter
import random
import typing
from typing import List, cast

from ...module.config import booltype, inttype

from ...model.common import CaravanBuddyListInfoData, CaravanDishData, CaravanDishEffectData, CaravanDishSellData, CaravanEventEffectData, CaravanShopBlockLineup, RivalInfo

from ...model.responses import CaravanMoveResponse, CaravanTopResponse

from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from enum import IntEnum

class eFlag(IntEnum):
    DISH_USED = 1
    DICE_USED = 2
    BLOCK_EFFECT = 4
    MINIGAME_ACTIVE = 8
    GOAL_EFFECT = 16
    SELECT_RESULT = 32
    IS_RIVAL_MINIGAME = 64
    IS_RIVAL_TURN_PROGRESS = 128
    IS_PROGRESS_TURN = 256
    BULK_DICE = 512 # unknown
    IS_PARTY_ON = 1024 # unknown 
    IS_SHORTCUT_ON = 2048

class eBlockType(IntEnum):
    NONE = 0
    START_POINT = 1
    MILES = 2
    SHOP = 3
    DISH = 4
    MINI_GAME = 5
    EVENT = 6
    TREASURE = 7
    WARP = 8
    WARP_START_POINT = 9
    WARP_END_POINT = 10
    GACHA = 11
    LOTTERY = 12
    GOAL = 13
    MOVE_ON = 14
    PARTY = 15
    SHORTCUT = 16

class eDishEffectType(IntEnum):
    NONE = 0
    MULTI_DICE = 1
    FIX_DICE_NUMBER = 2
    FIX_DUCE_NUMBER_AND_TURN_NOT_PROGRESS = 3
    RANDOM_EVENT = 4
    MILE_BLOCK_EFFECT = 5
    BLOCK_RANK_UP = 6
    CHANGE_DICE_BY_TURN_ODDS = 7
    OPEN_MILE_SHOP = 8
    BLOCK_SKIP_MOVE_COUNT = 9
    GET_CARAVAN_REWARD = 10
    ADD_MOVE_COUNT = 11
    CHANGE_BLOCK_TYPE = 12

class eEventEffectType(IntEnum):
	NONE = 0
	DISH_GET = 1
	DICE_GET = 2
	TURN_COUNT_SKIP = 3
	MILE_BLOCK_MUL = 4
	MINIGAME_BLOCK_MUL = 5
	SHOP_DISCOUNT = 6

class eGachaType(IntEnum):
	NORMAL = 0
	RARE = 1
	PREMIUM = 2
	MAX = 3

class eMinigameType(IntEnum):
	COIN_CATCH = 1

class eRivalMinigameType(IntEnum):
	NONE = 0
	BS_COIN_CATCH = 1

class eBuddyEffectType(IntEnum):
	NONE = 0
	DISCOUNT_SHOP = 1
	OBTAIN_MILE = 2
	OBTAIN_FOOD = 3
	RETRY = 4
	SELECT_DICE_RESULT = 5
	REPEAT_UNLESS_OVER_TOTAL_VALUE = 6
	FREE_ROLL = 7
	SELECT_FRONT_OR_BACK = 8
	BACK_RIVAL = 9
	SKIP_RIVAL_TURN_BY_ODD_OR_EVEN = 10
	SKIP_RIVAL_TURN_BY_TOTAL_VALUE = 11
	OBTAIN_LOTTERY_TICKET = 12
	GO_FORWARD_BY_ODD_OR_EVEN = 13

class eState(IntEnum):
    INIT = 0
    IDLE = 1
    ROLL_DICE = 2
    MOVE = 3
    CELL_ACTION = 4
    SHOP_BUY = 5
    USE_DISH = 6
    MINI_GAME = 7
    GACHA = 8
    TURN_END = 9
    GOAL = 10
    STOP = 11
    RIVAL_MINI_GAME = 12
    RIVAL_TURN_PROGRESS = 13
    SELECT_RESULT = 14
    SHORTCUT = 15

    _ignore_ = "_zh"
    @property
    def label(self) -> str:
        return _zh.get(self, self.name)

    def __str__(self) -> str:
        return self.label

_zh = {
    eState.INIT:      "开始",
    eState.IDLE:      "空闲",
    eState.ROLL_DICE: "投骰",
    eState.MOVE:      "移动",
    eState.CELL_ACTION: "格子",
    eState.SHOP_BUY:  "商店",
    eState.USE_DISH:  "用食",
    eState.MINI_GAME: "游戏",
    eState.GACHA:     "抽卡",
    eState.TURN_END:  "结算",
    eState.GOAL:      "终点",
    eState.STOP:      "停止",
    eState.RIVAL_MINI_GAME: "对战",
    eState.RIVAL_TURN_PROGRESS: "若菜",
    eState.SELECT_RESULT: "选骰",
    eState.SHORTCUT: "捷径",
}

class CaravanEffectData:
    data: typing.Union[CaravanDishEffectData, CaravanEventEffectData, CaravanBuddyListInfoData]

    _turn_field_map = {
        'CaravanDishEffectData': 'effect_turn',
        'CaravanEventEffectData': 'effect_turn',
        'CaravanBuddyListInfoData': 'turn'
    }

    _count_field_map = {
        'CaravanDishEffectData': 'effect_count',
        'CaravanEventEffectData': 'effect_count',
    }

    def __init__(self, data: typing.Union[CaravanDishEffectData, CaravanEventEffectData, CaravanBuddyListInfoData]):
        if not isinstance(data, (CaravanDishEffectData, CaravanEventEffectData, CaravanBuddyListInfoData)):
            raise TypeError("data must be one of CaravanDishEffectData, CaravanEventEffectData, CaravanBuddyListInfoData")
        self.data = data

    def _get_field(self, field_map: dict) -> Union[int, None]:
        cls_name = type(self.data).__name__
        if cls_name not in field_map:
            return None
        return getattr(self.data, field_map[cls_name])

    def _set_field(self, field_map: dict, value: int):
        cls_name = type(self.data).__name__
        if cls_name not in field_map:
            raise TypeError(f"{cls_name} not supported for this field")
        setattr(self.data, field_map[cls_name], value)

    @property
    def effect_turn(self) -> Union[int, None]:
        return self._get_field(self._turn_field_map)

    @effect_turn.setter
    def effect_turn(self, value: int):
        self._set_field(self._turn_field_map, value)

    @property
    def effect_count(self) -> Union[int, None]:
        return self._get_field(self._count_field_map)

    @effect_count.setter
    def effect_count(self, value: int):
        self._set_field(self._count_field_map, value)

eCaravanEffectType = typing.Union[eDishEffectType, eEventEffectType, eBuddyEffectType]

class EffectManager:
    def __init__(self, game: "CaravanGame", dish_effects: List[CaravanEffectData]):
        self.game = game
        self._effect_list = dish_effects
    def append(self, effect: CaravanEffectData):
        self._effect_list.append(effect)
    def empty(self) -> bool:
        return len(self._effect_list) == 0
    def get_effect_name(self, effect) -> str: ...
    def _get_effect_desc(self, effect) -> str: ...
    def get_effect_category(self, effect) -> eCaravanEffectType: ...
    def get_effect_effect_type(self, effect) -> eCaravanEffectType: ...
    def get_effect_sub_effect_type(self, effect) -> eCaravanEffectType: ...
    def get_effect_influence_value(self, effect_type: eCaravanEffectType) -> Union[int, None]: ...

    def get_effect_lasting_desc(self, effect: CaravanEffectData) -> str:
        if effect.effect_turn is not None and effect.effect_turn > 0:
            return f"持续回合：{effect.effect_turn}"
        elif effect.effect_count is not None and effect.effect_count > 0:
            return f"持续次数：{effect.effect_count}"
        else:
            return "已失效"

    def get_effect_desc(self) -> str:
        return '\n'.join(
            f"  {self.get_effect_name(effect.data)}：{self._get_effect_desc(effect.data)} {self.get_effect_lasting_desc(effect)}"
            for effect in self._effect_list
        )

    def get_effect(self, effect_type: eCaravanEffectType = 0) -> List[CaravanEffectData]:
        return [effect for effect in self._effect_list if not effect_type or self.get_effect_sub_effect_type(effect.data) == effect_type or self.get_effect_effect_type(effect.data) == effect_type]

    def is_category_effect_exist(self, category: int) -> bool:
        return any(effect for effect in self._effect_list if self.get_effect_category(effect.data) == category or self.get_effect_sub_effect_type(effect.data) == category)

    def process_effect(self, effect_type: eCaravanEffectType):
        effects = self.get_effect(effect_type)
        for effect in effects:
            if effect.effect_count is not None:
                effect.effect_count -= 1

    def process_effect_turn(self):
        for effect in self._effect_list:
            if effect.effect_turn is not None:
                effect.effect_turn -= 1
        self.clear_expired_effects()

    def clear_expired_effects(self):
        self._effect_list = [effect for effect in self._effect_list if effect.effect_turn is not None and effect.effect_turn > 0 or effect.effect_count is not None and effect.effect_count > 0]

class DishEffectManager(EffectManager):
    _effect_list: List[CaravanDishEffectData]

    def get_effect(self, effect_type: eDishEffectType = eDishEffectType.NONE) -> List[CaravanDishEffectData]:
        return [cast(CaravanDishEffectData, effect.data) for effect in super().get_effect(effect_type)]

    def get_effect_name(self, effect: CaravanDishEffectData) -> str:
        return db.caravan_dish[effect.id].name

    def _get_effect_desc(self, effect: CaravanDishEffectData) -> str:
        return db.caravan_dish[effect.id].get_effect_desc(lasting=False)

    def get_effect_category(self, effect: CaravanDishEffectData) -> eDishEffectType:
        return db.caravan_dish[effect.id].category

    def get_effect_effect_type(self, effect: CaravanDishEffectData) -> eDishEffectType:
        return db.caravan_dish[effect.id].effect_type

    def get_effect_sub_effect_type(self, effect: CaravanDishEffectData) -> eDishEffectType:
        return db.caravan_dish[effect.id].sub_effect_type

    def get_effect_influence(self, effect: eDishEffectType) -> List[CaravanDishEffectData]:
        dishes = self.get_effect(effect)
        ret = []
        if not dishes:
            return ret
        for dish in dishes:
            if db.caravan_dish[dish.id].effect_type == effect:
                ret.append(dish)
            elif dish.id in self.game.used_dish_id_list: # sub_effect_type
                ret.append(dish)
            if db.caravan_dish[dish.id].disable_category: # 不可覆盖
                break
        return ret

    def get_effect_influence_value(self, effect: eDishEffectType) -> Union[int, None]:
        dishes = self.get_effect_influence(effect)
        hit = False
        val = 0
        for dish in dishes:
            if db.caravan_dish[dish.id].effect_type == effect:
                hit = True
                val += db.caravan_dish[dish.id].effect_value
            elif dish.id in self.game.used_dish_id_list:
                hit = True
                val += db.caravan_dish[dish.id].sub_effect_value
        return val if hit else None

    def is_dice_fix(self) -> bool:
        for effect in [eDishEffectType.FIX_DICE_NUMBER, eDishEffectType.FIX_DUCE_NUMBER_AND_TURN_NOT_PROGRESS, eDishEffectType.CHANGE_DICE_BY_TURN_ODDS]:
            dishes = self.get_effect_influence(effect)
            for dish in dishes:
                if dish and '必定' in db.caravan_dish[dish.id].get_effect_desc(lasting=False): # simple
                    return True
        return False

    def is_dish_forbidden(self) -> int:
        for effect in [eDishEffectType.FIX_DICE_NUMBER, eDishEffectType.FIX_DUCE_NUMBER_AND_TURN_NOT_PROGRESS]:
            val = self.get_effect_influence_value(effect)
            if val is not None and val <= 3:
                return val
        return 0

    def is_disable_effect(self):
        return any(db.caravan_dish[effect.id].disable_category == 1 for effect in self._effect_list)

    def is_block_skip(self, block_type: int) -> bool:
        val = self.get_effect_influence_value(eDishEffectType.BLOCK_SKIP_MOVE_COUNT)
        if val is not None: # only god and pcrer know the rule
            if (val & 1) and block_type == eBlockType.MILES:
                return True
            elif (val & 2) and block_type == eBlockType.TREASURE:
                return True
        return False

class EventEffectManager(EffectManager):
    _effect_list: List[CaravanEventEffectData]

    def get_effect(self, effect_type: eEventEffectType = eEventEffectType.NONE) -> List[CaravanEventEffectData]:
        return [cast(CaravanEventEffectData, effect.data) for effect in super().get_effect(effect_type)]

    def get_effect_name(self, effect: CaravanEventEffectData) -> str:
        return eEventEffectType(db.caravan_event_effect[effect.event_id].effect_type).name

    def _get_effect_desc(self, effect: CaravanEventEffectData) -> str:
        return db.caravan_event_effect[effect.event_id].get_effect_desc(lasting = False)

    def get_effect_category(self, effect: CaravanEventEffectData) -> eEventEffectType:
        return db.caravan_event_effect[effect.event_id].category

    def get_effect_effect_type(self, effect: CaravanEventEffectData) -> eEventEffectType:
        return db.caravan_event_effect[effect.event_id].effect_type

    def get_effect_sub_effect_type(self, effect: CaravanEventEffectData) -> eEventEffectType:
        return eEventEffectType(0)

class BudyEffectManager(EffectManager):
    _effect_list: List[CaravanBuddyListInfoData]

    def get_effect(self, effect_type: eBuddyEffectType = eBuddyEffectType.NONE) -> List[CaravanBuddyListInfoData]:
        ret = [cast(CaravanBuddyListInfoData, effect.data) for effect in super().get_effect(effect_type)]
        assert len(ret) <= 1, "Buddy effects should not have multiple instances"
        return ret

    def get_effect_name(self, effect: CaravanBuddyListInfoData) -> str:
        return db.caravan_buddy[effect.buddy_id].name

    def _get_effect_desc(self, effect: CaravanBuddyListInfoData) -> str:
        return db.caravan_buddy[effect.buddy_id].get_effect_desc(lasting = False)

    def get_effect_effect_type(self, effect: CaravanBuddyListInfoData) -> eBuddyEffectType:
        return eBuddyEffectType(db.caravan_buddy[effect.buddy_id].effect_type)

    def get_effect_sub_effect_type(self, effect: CaravanBuddyListInfoData) -> eBuddyEffectType:
        return eBuddyEffectType(0)

    def get_effect_influence_value(self, effect: eBuddyEffectType) -> Tuple[Union[int, None], Union[int, None]]:
        buddys = self.get_effect(effect)
        ret = None, None
        for buddy in buddys:
            if db.caravan_buddy[buddy.buddy_id].effect_type == effect:
                ret = (db.caravan_buddy[buddy.buddy_id].effect_value_1, db.caravan_buddy[buddy.buddy_id].effect_value_2)
        return ret

    def process_effect_turn(self):
        super().process_effect_turn()
        for effect in self.get_effect():
            effect.exec_count = 0

    def is_dice_retryable(self) -> bool:
        buddys = self.get_effect(eBuddyEffectType.RETRY)
        for buddy in buddys:
            if not buddy.exec_count: 
                buddy.exec_count = 0
            if buddy.exec_count < db.caravan_buddy[buddy.buddy_id].effect_value_1:
                return True
        return False

    def is_effect_exist(self, effect: eBuddyEffectType) -> bool:
        buddys = self.get_effect(effect)
        for buddy in buddys:
            if buddy.turn > 0:
                return True
        return False

    def exec_effect(self, effect: eBuddyEffectType) -> int:
        buddys = self.get_effect(effect)
        for buddy in buddys:
            if not buddy.exec_count: 
                buddy.exec_count = 0
            if buddy.exec_count < db.caravan_buddy[buddy.buddy_id].effect_value_1:
                buddy.exec_count += 1
                return buddy.exec_count
        return 0

    def get_repeat_count(self) -> int:
        val1, val2 = self.get_effect_influence_value(eBuddyEffectType.REPEAT_UNLESS_OVER_TOTAL_VALUE)
        return val1 or 0

class CaravanGame:

    def __init__(self, client: pcrclient, module: Module):
        self.client = client
        self.module = module

        self.state: eState = eState.INIT

        self.season_id: int = 0
        self.current_block_id: int = 0
        self.turn_count: int = 0

        self.spots_list: List[int] = []

        self.dish_effect_manager = DishEffectManager(self, [])
        self.event_effect_manager = EventEffectManager(self, [])
        self.buddy_effect_manager = BudyEffectManager(self, [])

        self.candidate_shop_lineup: List[CaravanShopBlockLineup] = []

    def _log(self, msg):
        self.module._log(f"[回合 {self.turn_count:02d}] [{self.state}] {msg}")

    def _warn(self, msg):
        self.module._warn(msg)

    @property
    def dice_point(self) -> int:
        return self.client.data.get_inventory(db.dice)

    @property
    def licheng_point(self) -> int:
        return self.client.data.get_inventory(db.licheng_point)

    @property
    def candidate_dishes(self) -> typing.Counter[int]:
        return self.client.data.caravan_dishes

    @candidate_dishes.setter
    def candidate_dishes(self, dishes: typing.Counter[int]):
        self.client.data.caravan_dishes = dishes

    @property
    def dish_cnt(self) -> int:
        return sum(dish for dish in self.candidate_dishes.values())

    async def init(self, caravan_play_until_shop_empty: bool = False, caravan_dice_hold_num: int = 0, caravan_play_goal_num: int = 0):
        """
        第一次调用，用于拉取 top 接口，把 season_id、地图初始信息、dice_point 等都初始化好
        """
        resp = await self.client.caravan_top()

        # 从 resp 里提取必要字段
        self.season_id = resp.season_id
        self.current_block_id = resp.block_id
        self.turn_count = resp.turn
        self.block_id_list = []
        self.last_response: Union[CaravanTopResponse, CaravanMoveResponse] = resp
        self.spots = 0
        self.mini_game_id = 0
        self.caravan_play_until_shop_empty = caravan_play_until_shop_empty
        self.caravan_play_dice_hold_num = caravan_dice_hold_num
        self.caravan_play_goal_target = caravan_play_goal_num
        self.caravan_play_goal_num = 0
        self.spots_choices_1 = resp.spots_choices_1
        self.spots_choices_2 = resp.spots_choices_2
        self.rival_info = None
        self.shortcut_block_id = resp.shortcut_block_id or 0
        await self.update_rival_info(resp.rival_info)

        items_list = db.caravan_coin_shop_lineup[resp.season_id]
        have_bought = Counter({item.slot_id: item.purchase_count for item in resp.coin_shop_list or [] if item.season_id == resp.season_id})
        self.coin_token = (eInventoryType.Item, items_list[0].currency_id)

        if self.caravan_play_until_shop_empty:
            self.total_coin = sum((item.stock - have_bought[item.slot_id]) * item.price for item in items_list if item.stock > 0)
            self._log(f"搬空商店需要商店币 {self.total_coin}，当前商店币 {self.client.data.get_inventory(self.coin_token)}")

        if resp.dish_list:
            self.candidate_dishes = Counter({dish.id:dish.stock for dish in resp.dish_list})
        else:
            self.candidate_dishes = Counter()
        self.used_dish_id_list = []
        if resp.used_dish_id_list: # 一般是一次性的
            self.used_dish_id_list = resp.used_dish_id_list

        for dish_effect in resp.dish_effect_list or []:
            self.dish_effect_manager.append(CaravanEffectData(dish_effect))
        for event_effect in resp.event_effect_list or []:
            self.event_effect_manager.append(CaravanEffectData(event_effect))

        if resp.buddy_info:
            self.buddy_effect_manager.append(CaravanEffectData(resp.buddy_info))

        self.state = eState.INIT
        self._log(f"赛季{self.season_id}, 位于格子{self.current_block_id}, 骰子数{self.dice_point}")
        if not self.dish_effect_manager.empty():
            self._log(f"料理效果列表：\n{self.dish_effect_manager.get_effect_desc()}")
        if not self.event_effect_manager.empty():
            self._log(f"事件效果列表：\n{self.event_effect_manager.get_effect_desc()}")
        if not self.buddy_effect_manager.empty():
            self._log(f"伙伴效果列表：\n{self.buddy_effect_manager.get_effect_desc()}")

        self.action_bit_flag = resp.action_bit_flag or 0
        if resp.action_bit_flag:
            self._log(f"处理 action_bit_flag={resp.action_bit_flag}")
            if eFlag.IS_PARTY_ON & resp.action_bit_flag:
                self._log("处理 IS_PARTY_ON")
                self.state = eState.USE_DISH
                await self.step()
            if eFlag.IS_SHORTCUT_ON & resp.action_bit_flag:
                self._log("处理 IS_SHORTCUT_ON")
                self.state = eState.SHORTCUT
                await self.step()
            if eFlag.BLOCK_EFFECT & resp.action_bit_flag:
                self._log("处理 BLOCK_EFFECT")
                self.state = eState.CELL_ACTION
                await self.step()
            if eFlag.MINIGAME_ACTIVE & resp.action_bit_flag and not resp.minigame_retire_reward:
                self._log("处理 MINIGAME_ACTIVE")
                self.state = eState.MINI_GAME
                await self.step()
            if eFlag.GOAL_EFFECT & resp.action_bit_flag:
                self._log("处理 GOAL_EFFECT")
                self.state = eState.GOAL
                await self.step()
            if eFlag.SELECT_RESULT & resp.action_bit_flag:
                self._log("处理 SELECT_RESULT")
                extra_spots = self.dish_effect_manager.get_effect_influence_value(eDishEffectType.ADD_MOVE_COUNT) or 0
                self.spots_list = [resp.spots - extra_spots]
                print(self.spots_list)
                resp.spots = 0
                self.state = eState.SELECT_RESULT
                await self.step()
            if eFlag.IS_RIVAL_MINIGAME & resp.action_bit_flag:
                self._log("处理 IS_RIVAL_MINIGAME")
                self.state = eState.RIVAL_MINI_GAME
                await self.step()
            if eFlag.IS_RIVAL_TURN_PROGRESS & resp.action_bit_flag:
                self._log("处理 IS_RIVAL_TURN_PROGRESS")
                self.state = eState.RIVAL_TURN_PROGRESS
                await self.step()
            if resp.spots:
                self.spots = resp.spots
                self.state = eState.MOVE
                await self.step()
                self.state = eState.CELL_ACTION
                await self.step()
            if eFlag.IS_PROGRESS_TURN & resp.action_bit_flag:
                self._log("处理 IS_PROGRESS_TURN")
                self.state = eState.TURN_END
                await self.step()

        self.state = eState.IDLE

    async def update_rival_info(self, rival_info: RivalInfo):
        if not rival_info or (not rival_info.block_id and not rival_info.after_block_id):
            return
        if (not self.rival_info or not self.rival_info.block_id) and rival_info.block_id:
            self._log(f"若菜出现于{rival_info.block_id}")
            self.rival_info = rival_info
            return

        assert isinstance(self.rival_info, RivalInfo), "rival_info must be an instance of RivalInfo"
        self.rival_info.block_id = rival_info.after_block_id
        self._log(f"若菜掷出了{rival_info.spots_list}，到达格子 {self.rival_info.block_id}")
        if self.current_block_id == self.rival_info.block_id:
            self._log("若菜在当前格子，开始小游戏")
            self.state = eState.RIVAL_MINI_GAME
            self.action_bit_flag |= eFlag.IS_RIVAL_MINIGAME
            await self.step()

    async def check_dishes_full(self, surplus_dish_list: Union[None, List[CaravanDishData]]):
        if surplus_dish_list is None:
            return
        surplus_dishes = Counter({dish.id: dish.stock for dish in surplus_dish_list})
        tot = sum(surplus_dishes.values()) + self.dish_cnt
        if tot > 10: # self.client.data.settings.caravan.limit_caravan_dish_by_type disappear
            self._log(f"料理数量{tot} > 10")
            sell_dishes = []
            sell_surplus_dishes = []
            sell_num = 0
            for dishes, sell_list in [self.candidate_dishes, sell_dishes], [surplus_dishes, sell_surplus_dishes]:
                for dish_id, stock in dishes.items():
                    if stock > 0:
                        if tot <= 10:
                            break
                        sold = min(stock, tot - 10)
                        sell_list.append(CaravanDishSellData(id=dish_id, current_num=stock, sell_num=sold))
                        dishes[dish_id] -= sold
                        tot -= sold
                        sell_num += sold

            self._log(f"卖出料理{sell_num}份")
            await self.client.caravan_dish_sell(
                season_id=self.season_id,
                block_id=self.current_block_id,
                dish_list=sell_dishes,
                surplus_dish_list=sell_surplus_dishes
            )
            surplus_dish_list.clear()

    async def step(self):
        await self.check_dishes_full(self.last_response.surplus_dish_list)

        if self.state == eState.IDLE:

            if self.spots or self.spots_list:
                self.state = eState.MOVE
                return

            if self.action_bit_flag & eFlag.IS_RIVAL_TURN_PROGRESS and self.last_response.rival_info:
                self._log("若菜回合 -> RIVAL_TURN_PROGRESS")
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            if self.candidate_shop_lineup:
                self._log(f"商店开启 -> SHOP_BUY")
                self.state = eState.SHOP_BUY
                return

            if self.action_bit_flag & eFlag.IS_PROGRESS_TURN:
                self.state = eState.TURN_END
                return

            if self.dice_point <= 0:
                self._log("没有骰子了 -> STOP")
                self.state = eState.STOP
                return

            if self.caravan_play_until_shop_empty and self.client.data.get_inventory(self.coin_token) >= self.total_coin:
                self._log(f"商店币{self.client.data.get_inventory(self.coin_token)} > {self.total_coin}，足够搬空商店 -> STOP")
                self.state = eState.STOP
                return

            if self.caravan_play_dice_hold_num >= self.dice_point:
                self._log(f"骰子数{self.dice_point} <= {self.caravan_play_dice_hold_num}，小于阈值 -> STOP")
                self.state = eState.STOP
                return

            if self.caravan_play_goal_target and self.caravan_play_goal_num >= self.caravan_play_goal_target:
                self._log(f"达终点次数{self.caravan_play_goal_num} >= {self.caravan_play_goal_target} -> STOP")
                self.state = eState.STOP
                return

            if not self.action_bit_flag & eFlag.DISH_USED and self.candidate_dishes:
                self.state = eState.USE_DISH
                return

            self.state = eState.ROLL_DICE

        elif self.state == eState.ROLL_DICE:
            if not self.action_bit_flag & eFlag.DICE_USED:
                roll_num = self.dish_effect_manager.get_effect_influence_value(eDishEffectType.MULTI_DICE) or 1

                self._log(f"当前骰子数{self.dice_point}, 掷出骰子{roll_num}个")
                resp = await self.client.caravan_dice_roll(
                    season_id=self.season_id,
                    current_num=self.dice_point,
                    roll_num=roll_num
                )
                self.client.data.set_inventory(db.dice, self.dice_point - 1) # only pcr can do
                self.spots_list = resp.spots_list or []
                extra_spots = self.dish_effect_manager.get_effect_influence_value(eDishEffectType.ADD_MOVE_COUNT) or 0 # feature in spot choice
                self.spots_choices_1 = (resp.spots_choices_1 or 0) - extra_spots
                self.spots_choices_2 = (resp.spots_choices_2 or 0) - extra_spots

                await self.update_rival_info(resp.rival_info) # ? why here update

                self.state = eState.SELECT_RESULT
                await self.step()
                self.state = eState.ROLL_DICE

                self._log(f"骰子结果={self.spots_list}, 剩余骰子={self.dice_point}")
                self.action_bit_flag |= eFlag.DICE_USED
                self.dish_effect_manager.process_effect(eDishEffectType.MULTI_DICE)
                self.dish_effect_manager.process_effect(eDishEffectType.FIX_DICE_NUMBER)
                self.dish_effect_manager.process_effect(eDishEffectType.FIX_DUCE_NUMBER_AND_TURN_NOT_PROGRESS)

                if extra_spots:
                    self._log(f"料理效果增加额外步数：{extra_spots}")
                    self.spots_list.append(extra_spots)

            self.state = eState.MOVE

        elif self.state == eState.MOVE:
            self.block_id_list = [self.current_block_id]
            if not self.spots:
                self.spots = sum(self.spots_list)
                self._log(f"当前格子 {self.current_block_id}，移动 {self.spots} 步")
                self.spots_list = []

            while self.spots > 0:
                next_blocks = db.caravan_map[self.current_block_id].get_next_blocks()
                if self.shortcut_block_id and self.shortcut_block_id == self.current_block_id:
                    next_blocks = list(next_blocks)
                    next_blocks.append(db.caravan_shortcut[self.shortcut_block_id].end_point_block_id)
                    self.shortcut_block_id = 0
                dis = [(nxt, db.caravan_map[nxt].distance_to_goal) for nxt in next_blocks]
                self.current_block_id = min(dis, key=lambda x: x[1])[0]
                self.block_id_list.append(self.current_block_id)
                if db.caravan_map[self.current_block_id].type == eBlockType.GOAL:
                    break
                elif self.dish_effect_manager.is_block_skip(db.caravan_map[self.current_block_id].type):
                    continue
                else:
                    self.spots -= 1

            self._log(f"已落在格子 {self.current_block_id}")
            if len(self.block_id_list) > 1:
                self.last_response = await self.client.caravan_move(
                    season_id=self.season_id,
                    current_block_id=self.block_id_list[0],
                    block_id_list=self.block_id_list[1:]
                )
                self.action_bit_flag = self.last_response.action_bit_flag or 0

            self.state = eState.CELL_ACTION

        elif self.state == eState.CELL_ACTION:

            resp = self.last_response

            block_type = eBlockType(db.caravan_map[self.current_block_id].type)
            self._log(f"当前格子 {self.current_block_id} 的类型 = {block_type.name}")

            if block_type == eBlockType.GOAL:
                self._log("检查点 -> GOAL")
                self.state = eState.GOAL
                return

            elif self.rival_info and self.rival_info.block_id and self.current_block_id == self.rival_info.block_id:
                self._log("抵达若菜格子 -> RIVAL_MINI_GAME")
                self.state = eState.RIVAL_MINI_GAME
                self.action_bit_flag |= eFlag.IS_RIVAL_MINIGAME
                return

            elif block_type == eBlockType.SHOP:
                self._log("商店块 -> 切到 SHOP_BUY")
                self.dish_effect_manager.process_effect(eDishEffectType.BLOCK_RANK_UP)
                self.candidate_shop_lineup = resp.shop_block_lineup_list
                self.state = eState.SHOP_BUY
                return

            elif block_type == eBlockType.DISH:
                self._log("料理块 -> IDLE")
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            elif block_type == eBlockType.MINI_GAME:
                self._log("小游戏块 -> MINI_GAME")
                if isinstance(resp, CaravanMoveResponse):
                    self.mini_game_id = resp.minigame_id or 0
                self.state = eState.MINI_GAME
                return

            elif block_type == eBlockType.GACHA:
                self._log("抽卡块 -> GACHA")
                self.state = eState.GACHA
                return

            elif block_type == eBlockType.TREASURE:
                self._log("宝箱块 -> IDLE")
                self.dish_effect_manager.process_effect(eDishEffectType.BLOCK_RANK_UP)
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            elif block_type == eBlockType.EVENT:
                self._log("事件块 -> IDLE")
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            elif block_type == eBlockType.MILES:
                self._log("里程块 -> IDLE")
                self.dish_effect_manager.process_effect(eDishEffectType.MILE_BLOCK_EFFECT)
                self.dish_effect_manager.process_effect(eDishEffectType.BLOCK_RANK_UP)
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            elif block_type == eBlockType.MOVE_ON:
                self._log("前进块 -> MOVE")
                self.spots_list = [db.caravan_map[self.current_block_id].reference_id]
                self.state = eState.MOVE
                return

            elif block_type == eBlockType.LOTTERY:
                self._log("抽奖块 -> IDLE")
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            elif block_type == eBlockType.SHORTCUT:
                self._log("捷近块 -> SHORTCUT")
                self.state = eState.SHORTCUT

            elif block_type == eBlockType.PARTY:
                self._log("派对块 -> IDLE")
                self.state = eState.RIVAL_TURN_PROGRESS
                return

            else:
                self._log(f"其他类型 {block_type.name} -> TURN_END")
                raise AbortError(f"未处理的格子类型：{block_type.name}")
                self.state = eState.TURN_END
                return

        elif self.state ==  eState.GOAL:
            if self.action_bit_flag & eFlag.GOAL_EFFECT:
                self._log(f"{self.turn_count}回合抵达终点")
                resp = await self.client.caravan_read(
                    season_id=self.season_id,
                    block_id=self.current_block_id
                )
            rewards = []
            if isinstance(self.last_response, CaravanMoveResponse):
                rewards = self.last_response.treasure_reward_list or []
            elif isinstance(self.last_response, CaravanTopResponse):
                rewards = self.last_response.caravan_item_list or []
            if self.rival_info and self.rival_info.block_id:
                if self.rival_info.block_id == self.current_block_id:
                    self._log("与若菜的对决失败了")
                else:
                    self._log("与若菜的对决胜利了")
            self._log(f"获得了 {await self.client.serialize_reward_summary(rewards)}")
            self.turn_count = 0
            self.state = eState.MOVE
            self.rival_info = None
            self.caravan_play_goal_num += 1

        elif self.state == eState.RIVAL_TURN_PROGRESS:
            await self.update_rival_info(self.last_response.rival_info)
            self.last_response.rival_info = None
            self.state = eState.IDLE

        elif self.state == eState.SHORTCUT:
            if self.licheng_point >= db.caravan_shortcut[self.current_block_id].cost:
                self._log(f"花费{db.caravan_shortcut[self.current_block_id].cost}里程币抄近道")
                resp = await self.client.caravan_shortcut_choice(
                    season_id=self.season_id,
                    block_id=self.current_block_id,
                    is_open=1,
                    current_currency_num=self.licheng_point
                )
                self.shortcut_block_id = self.current_block_id
                self.client.data.set_inventory(db.licheng_point, self.licheng_point - db.caravan_shortcut[self.current_block_id].cost)
            else:
                self._log("里程币不足，放弃抄近道")
                resp = await self.client.caravan_shortcut_choice(
                    season_id=self.season_id,
                    block_id=self.current_block_id,
                    is_open=0,
                    current_currency_num=self.licheng_point
                )
            await self.update_rival_info(resp.rival_info)
            self.state = eState.IDLE

        elif self.state == eState.SHOP_BUY:
            treasures = [slot for slot in self.candidate_shop_lineup if slot.type == eInventoryType.CaravanTreasure and not slot.is_sold]
            dishes = [slot for slot in self.candidate_shop_lineup if slot.type == eInventoryType.CaravanDish and not slot.is_sold]
            cost = 0
            slot_ids = []
            for treasure in treasures:
                price = treasure.discounted_price if treasure.discounted_price is not None else treasure.price
                if cost + price > self.licheng_point:
                    break
                cost += price
                slot_ids.append(treasure.slot_id)

            for id, dish in enumerate(dishes):
                if self.dish_cnt + id >= 6: break
                price = dish.discounted_price if dish.discounted_price is not None else dish.price
                if cost + price > self.licheng_point:
                    break
                cost += price
                slot_ids.append(dish.slot_id)
                self.candidate_dishes[dish.item_id] += dish.num

            if slot_ids:
                self._log(f"购买槽位：{slot_ids}")
                shop_resp = await self.client.caravan_shop_block_buy(
                    season_id=self.season_id,
                    block_id=self.current_block_id,
                    slot_id_list=slot_ids,
                    current_currency_num=self.licheng_point
                )
                self._log(f"购买了{await self.client.serialize_reward_summary(shop_resp.purchase_list or [])}")
                self.client.data.set_inventory((eInventoryType.CaravanItem, 99007), self.licheng_point - cost)

            self.candidate_shop_lineup = []
            self.state = eState.RIVAL_TURN_PROGRESS

        elif self.state == eState.USE_DISH:
            if not self.action_bit_flag & eFlag.DISH_USED and self.candidate_dishes:
                for category in [1, 2, 3]:
                    if self.dish_effect_manager.is_category_effect_exist(category):
                        continue
                    if self.dish_effect_manager.is_dish_forbidden() == category:
                        continue
                    dish_to_use = next((dish_id for dish_id, stock in self.candidate_dishes.items() if stock > 0 and db.caravan_dish[dish_id].category == category), None)
                    if dish_to_use is None:
                        continue
                    self.used_dish_id_list.append(dish_to_use)
                    self._log(f"使用料理：{db.caravan_dish[dish_to_use].name}，效果：{db.caravan_dish[dish_to_use].get_effect_desc()}")
                    use_resp = await self.client.caravan_dish_use(
                        season_id=self.season_id,
                        dish_id=dish_to_use
                    )
                    self.candidate_shop_lineup = use_resp.shop_block_lineup_list or []
                    self.dish_effect_manager.append(CaravanEffectData(CaravanDishEffectData(id=dish_to_use, effect_turn=db.caravan_dish[dish_to_use].effect_turn, effect_count=db.caravan_dish[dish_to_use].effect_times)))
                    await self.check_dishes_full(use_resp.surplus_dish_list)
                    if not db.caravan_map[self.current_block_id].type == eBlockType.PARTY:
                        break
                self.action_bit_flag |= eFlag.DISH_USED
                self.state = eState.IDLE

        elif self.state == eState.SELECT_RESULT:
            roll_num = self.dish_effect_manager.get_effect_influence_value(eDishEffectType.MULTI_DICE) or 1
            while not self.dish_effect_manager.is_dice_fix() and self.buddy_effect_manager.is_dice_retryable():
                exec_count = self.buddy_effect_manager.exec_effect(eBuddyEffectType.RETRY)
                if sum(self.spots_list) >= 3 * roll_num:
                    self._log(f"骰子结果 {self.spots_list} >= 3 * {roll_num}, 不低于期望，不重投")
                    await self.client.caravan_spots_choice(
                        season_id=self.season_id,
                        choice=1
                    )
                    break
                else:
                    self._log(f"骰子结果 {self.spots_list} < 3 * {roll_num}, 重投")
                    resp = await self.client.caravan_dice_reroll(
                        season_id=self.season_id,
                        current_count=exec_count,
                        roll_num=roll_num
                    )
                    self.spots_list = resp.spots_list

            repeat_count = self.buddy_effect_manager.get_repeat_count()
            while repeat_count > sum(self.spots_list):
                self._log(f"当前骰子结果 {self.spots_list}, 未达 {self.buddy_effect_manager.get_repeat_count()}，继续投")
                roll_num = self.dish_effect_manager.get_effect_influence_value(eDishEffectType.MULTI_DICE) or 1
                exec_count = self.buddy_effect_manager.exec_effect(eBuddyEffectType.REPEAT_UNLESS_OVER_TOTAL_VALUE)
                resp = await self.client.caravan_dice_reroll(
                    season_id=self.season_id,
                    current_count=exec_count,
                    roll_num=roll_num
                )
                self.spots_list.extend(resp.spots_list) 
            else:
                if repeat_count:
                    self._log(f"当前骰子结果 {self.spots_list}, 达到 {self.buddy_effect_manager.get_repeat_count()}，停止投")

            if self.buddy_effect_manager.is_effect_exist(eBuddyEffectType.SELECT_DICE_RESULT) \
                or self.buddy_effect_manager.is_effect_exist(eBuddyEffectType.SELECT_FRONT_OR_BACK) \
                or self.buddy_effect_manager.is_effect_exist(eBuddyEffectType.GO_FORWARD_BY_ODD_OR_EVEN) and sum(self.spots_list) % 2 == self.buddy_effect_manager.get_effect_influence_value(eBuddyEffectType.GO_FORWARD_BY_ODD_OR_EVEN)[0] % 2: # type: ignore
                choice = 1 + (self.spots_choices_1 < self.spots_choices_2)
                self._log(f"{self.spots_choices_1} vs {self.spots_choices_2}，选择骰子结果 {choice}")
                await self.client.caravan_spots_choice(
                    season_id=self.season_id,
                    choice=choice,
                )
                extra_spots = self.dish_effect_manager.get_effect_influence_value(eDishEffectType.ADD_MOVE_COUNT) or 0
                self.spots_list = [self.spots_choices_1] if choice == 1 else [self.spots_choices_2] # fix

            self.state = eState.IDLE

        elif self.state == eState.RIVAL_MINI_GAME:
            if self.action_bit_flag & eFlag.IS_RIVAL_MINIGAME:
                start_resp = await self.client.caravan_minigame_bs_start(season_id=self.season_id)
                self._log(f"开始小游戏 play_id={start_resp.play_id}")
                items = Counter(ccc.ccc_object_id for ccc in db.ccc_scenario[start_resp.ccc_scenario_id] if db.ccc_object[ccc.ccc_object_id].is_report and (db.ccc_object[ccc.ccc_object_id].ccc_object_type == 2 or random.random() < 0.8))

                finish_resp = await self.client.caravan_minigame_bs_finish(
                    season_id=self.season_id,
                    play_id=start_resp.play_id,
                    items=items
                )
                self._log(f"完成若菜小游戏，总分={finish_resp.total_score_corrected}")
                await self.update_rival_info(finish_resp.rival_info)
            self.state = eState.IDLE

        elif self.state == eState.MINI_GAME:
            if self.action_bit_flag & eFlag.MINIGAME_ACTIVE:
                start_resp = await self.client.caravan_minigame_start()
                self._log(f"开始小游戏 play_id={start_resp.play_id}")
                items = Counter(ccc.ccc_object_id for ccc in db.ccc_scenario[start_resp.ccc_scenario_id] if db.ccc_object[ccc.ccc_object_id].is_report and (db.ccc_object[ccc.ccc_object_id].ccc_object_type == 2 or random.random() < 0.8))

                finish_resp = await self.client.caravan_minigame_finish(
                    play_id=start_resp.play_id,
                    items=items
                )
                self._log(f"完成小游戏，总分={finish_resp.total_score_corrected}")
                await self.update_rival_info(finish_resp.rival_info)
            self.state = eState.IDLE

        elif self.state == eState.GACHA:
            if self.action_bit_flag & eFlag.BLOCK_EFFECT:
                gacha_group_id = db.caravan_map[self.current_block_id].reference_id
                gacha_data = db.caravan_gacha_block_lineup[gacha_group_id]
                rare = eGachaType.NORMAL
                cost = 0
                for rare_type, cost_num in [(eGachaType.PREMIUM, gacha_data.premium_gacha_cost),
                                        (eGachaType.RARE, gacha_data.rare_gacha_cost),
                                        (eGachaType.NORMAL, gacha_data.normal_gacha_cost)]:
                    if self.licheng_point >= cost_num:
                        self._log(f"抽取稀有度{rare_type.name}，费用{cost_num}")
                        rare = rare_type + 1
                        cost = cost_num
                        break

                gacha_resp = await self.client.caravan_gacha_block_exec(
                    season_id=self.season_id,
                    block_id=self.current_block_id,
                    gacha_type=rare,
                    current_currency_num=self.licheng_point
                )
                await self.check_dishes_full(gacha_resp.surplus_dish_list)
                self._log(f"抽卡结果：{await self.client.serialize_reward_summary(gacha_resp.reward_list or [])}")
                self.client.data.set_inventory((eInventoryType.CaravanItem, 99007), self.licheng_point - cost)
            self.state = eState.RIVAL_TURN_PROGRESS

        elif self.state == eState.TURN_END:
            if self.action_bit_flag & eFlag.IS_PROGRESS_TURN:
                progress_resp = await self.client.caravan_progress_turn(
                    season_id=self.season_id,
                    turn=self.turn_count
                )
                self.dish_effect_manager.process_effect_turn()
                self.event_effect_manager.process_effect_turn()
                self.buddy_effect_manager.process_effect_turn()
                self.used_dish_id_list = []

                if progress_resp.buddy_id:
                    self.buddy_effect_manager.append(CaravanEffectData(
                        CaravanBuddyListInfoData(
                            buddy_id=progress_resp.buddy_id,
                            exec_count=0,
                            turn=db.caravan_buddy[progress_resp.buddy_id].effect_turn,
                            is_appear=True
                        )))
                    if progress_resp.shop_block_lineup_list:
                        self.candidate_shop_lineup = progress_resp.shop_block_lineup_list

                await self.check_dishes_full(progress_resp.surplus_dish_list)
                self.candidate_dishes += Counter() # remove zero dishes
                self.action_bit_flag = 0

                self._log(f"回合结算完成")

                self.turn_count = progress_resp.turn
                await self.update_rival_info(progress_resp.rival_info)

                self._log(f"当前格子 {self.current_block_id}, 检查点距离 {db.caravan_map[self.current_block_id].distance_to_goal}, 料理数量 {self.dish_cnt}")
                if not self.dish_effect_manager.empty():
                    self._log(f"料理效果列表\n{self.dish_effect_manager.get_effect_desc()}")
                if not self.event_effect_manager.empty():
                    self._log(f"事件效果列表\n{self.event_effect_manager.get_effect_desc()}")
                if not self.buddy_effect_manager.empty():
                    self._log(f"伙伴效果列表\n{self.buddy_effect_manager.get_effect_desc()}")

            self.state = eState.IDLE

        elif self.state == eState.STOP:
            self._log("循环结束。")

        else:
            raise RuntimeError(f"未识别状态：{self.state}")

    def stop(self) -> bool:
        return self.state == eState.STOP

@name('大富翁')
@default(True)
@description("将运行直至骰子耗尽或可搬空商店或骰子数低于阈值，料理能用则用。可搬空商店停止指商店币可购买所有限定商品后停止，到达终点次数指达到终点的次数满足后停止，骰子保留指当骰子数小于等于该值时停止")
@inttype('caravan_play_goal_num', '到达终点次数', 0, list(range(0, 10)))
@inttype('caravan_play_dice_hold_num', '骰子保留', 0, list(range(0, 100)))
@booltype('caravan_play_until_shop_empty', '可搬空商店停止', True)
class caravan_play(Module):
    async def do_task(self, client: pcrclient):
        game = CaravanGame(client, self)
        caravan_play_until_shop_empty = self.get_config('caravan_play_until_shop_empty')
        caravan_play_dice_hold_num = self.get_config('caravan_play_dice_hold_num')
        caravan_play_goal_num = self.get_config('caravan_play_goal_num')
        await game.init(caravan_play_until_shop_empty, caravan_play_dice_hold_num, caravan_play_goal_num)
        while not game.stop():
            await game.step()


@name('大富翁商店购买')
@default(True)
@description("默认买最新一期商店，按照商品顺序购买，直到商店币用完为止，有次数的无法购买会提示，无次数的不会提示,便于查看是否搬空商店")
@booltype('caravan_shop_last_season', '购买上期商店', False)
class caravan_shop_buy(Module):
    async def do_task(self, client: pcrclient):
        top = await client.caravan_top()
        season_id = top.season_id
        if self.get_config('caravan_shop_last_season'):
            season_id -= 1
        if top.action_bit_flag & eFlag.IS_PROGRESS_TURN:
            raise AbortError("请先执行大富翁进行回合结算")
        if season_id not in db.caravan_schedule:
            raise AbortError(f"赛季 {season_id} 不存在")
        if client.datetime > db.parse_time(db.caravan_schedule[season_id].shop_close_time):
            raise AbortError(f"赛季 {season_id} 商店已关闭")

        items_list = db.caravan_coin_shop_lineup[season_id]
        have_bought = Counter({item.slot_id: item.purchase_count for item in top.coin_shop_list or [] if item.season_id == season_id})
        cost = 0
        rewards = []
        items_list = sorted(items_list, key=lambda x: x.slot_id)
        limit_items_list = [item for item in items_list if item.stock > 0]
        unlimited_items_list = [item for item in items_list if item.stock == 0]

        limit_expend_items = [item for item in limit_items_list for _ in range(item.stock - have_bought[item.slot_id])]

        is_enable_buy_bulk = client.data.settings.caravan.is_enable_caravan_coin_shop_buy_bulk
        to_buy = Counter()
        for item in limit_expend_items[:]:
            coin = client.data.get_inventory((eInventoryType.Item, item.currency_id))
            if coin < cost + item.price:
                if not rewards:
                    self._log(f"商店币不足{coin} < {cost + item.price}，无法购买 {db.get_inventory_name_san((item.reward_type, item.reward_id))}及以后的物品")
                break
            if not is_enable_buy_bulk:
                resp = await client.caravan_coin_shop_buy(
                    season_id=top.season_id,
                    shop_season_id=season_id,
                    slot_id_list=[item.slot_id],
                    current_currency_num=coin
                )
                rewards.extend(resp.purchase_list or [])
            else:
                to_buy[item.slot_id] += 1
            cost += item.price
            limit_expend_items.remove(item)

        if is_enable_buy_bulk and to_buy:
            resp = await client.caravan_coin_shop_buy_bulk(
                season_id=top.season_id,
                shop_season_id=season_id,
                buy_item_dict=to_buy,
                current_currency_num=coin
            )
            rewards.extend(resp.purchase_list or [])

        buy = len(limit_expend_items) == 0
        while buy:
            buy = False
            for item in unlimited_items_list:
                coin = client.data.get_inventory((eInventoryType.Item, item.currency_id))
                if item.price <= coin:
                    if not is_enable_buy_bulk:
                        resp = await client.caravan_coin_shop_buy(
                            season_id=top.season_id,
                            shop_season_id=season_id,
                            slot_id_list=[item.slot_id],
                            current_currency_num=coin
                        )
                    else:
                        resp = await client.caravan_coin_shop_buy_bulk(
                            season_id=top.season_id,
                            shop_season_id=season_id,
                            buy_item_dict=Counter({item.slot_id:1}),
                            current_currency_num=coin
                        )
                    rewards.extend(resp.purchase_list or [])
                    cost += item.price
                    buy = True

        if not rewards:
            self._log("无可购买的物品")
        else:
            self._log(f"花费了商店币 {cost}，购买了\n{await client.serlize_reward(rewards)}")

