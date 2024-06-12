from abc import abstractmethod
from typing import List
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *

class shop_buyer(Module):
    def _get_count(self, name: str, key: str) -> int:
        if name not in self.buy_kind():
            return -999999
        return self.get_config(key)
    def _exp_count(self):
        return self._get_count('经验药水', 'shop_buy_exp_count_limit')
    def _equip_count(self):
        return self._get_count('装备', 'shop_buy_equip_count_limit')
    def _equip_upper_count(self):
        return self._get_count('强化石', 'shop_buy_equip_upper_count_limit')
    def _unit_memory_count(self):
        return self._get_count('记忆碎片', 'shop_buy_memory_count_limit')

    @abstractmethod
    def coin_limit(self) -> int: ...
    @abstractmethod
    def system_id(self) -> eSystemId: ...
    @abstractmethod
    def reset_count(self) -> int: ...
    @abstractmethod
    def buy_kind(self) -> List[str]: ...

    def require_equip_units_fav(self) -> bool:
        return False

    def require_equip_units_rank(self) -> str:
        return '所有'

    async def _get_shop(self, client: pcrclient):
        res = await client.get_shop_item_list()
        for shop in res.shop_list:
            if shop.system_id == self.system_id().value:
                return shop
        raise SkipError("商店未开启")

    async def do_task(self, client: pcrclient):
        lmt = self.coin_limit()
        reset_cnt = self.reset_count()

        shop_content = await self._get_shop(client)

        prev = client.data.get_shop_gold(shop_content.system_id)
        old_reset_cnt = shop_content.reset_count
        result = []

        while True:
            opt: Dict[Union[int, str], int] = {
                '所有': 1,
                '最高': db.equip_max_rank,
                '次高': db.equip_max_rank - 1,
                '次次高': db.equip_max_rank - 2,
            }
            equip_demand_gap = client.data.get_equip_demand_gap(like_unit_only=self.require_equip_units_fav(), start_rank=opt[self.require_equip_units_rank()])

            memory_demand_gap = client.data.get_memory_demand_gap()

            gold = client.data.get_shop_gold(shop_content.system_id)
            if gold < lmt:
                raise SkipError(f"商店货币{gold}不足{lmt}，将不进行购买")

            target = [
                (item.slot_id, item.price.currency_num) for item in shop_content.item_list if not item.sold and
                    (
                        (db.is_exp_upper((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._exp_count()) or
                        (db.is_equip_upper((item.type, item.item_id)) and client.data.get_inventory((item.type, item.item_id)) < self._equip_upper_count()) or
                        (db.is_equip((item.type, item.item_id)) and -equip_demand_gap[(item.type, item.item_id)] < self._equip_count()) or
                        (db.is_unit_memory((item.type, item.item_id)) and -memory_demand_gap[(item.type, item.item_id)] < self._unit_memory_count())
                    )
            ]

            slots_to_buy = [item[0] for item in target]
            cost_gold = sum([item[1] for item in target])

            if cost_gold > gold: # 货币不足
                self._log(f"商店货币{gold}不足购买需求的{cost_gold}，停止购买")
                break
            
            if slots_to_buy:
                res = await client.shop_buy_item(shop_content.system_id, slots_to_buy)
                result.extend(res.purchase_list)
            # else: # 无商品购买还需要重置吗
            #     break

            if shop_content.reset_count >= reset_cnt:
                self._log(f"商店已重置{shop_content.reset_count}次，停止购买")
                break
            
            await client.shop_reset(shop_content.system_id)
            shop_content = await self._get_shop(client)

        cost_gold = prev - client.data.get_shop_gold(shop_content.system_id)
        if cost_gold == 0:
            raise SkipError("无对应商品购买")
        else:
            self._log(f"花费了{cost_gold}货币，重置了{shop_content.reset_count - old_reset_cnt}次，购买了:")
            msg = await client.serlize_reward(result)
            self._log(msg)

@singlechoice('shop_buy_exp_count_limit', "经验药水储备", 99000, [100, 1000, 5000, 10000, 50000, 99000])
@singlechoice('shop_buy_equip_upper_count_limit', "强化石储备", 99000, [100, 1000, 5000, 10000, 50000, 99000])
@singlechoice('normal_shop_buy_coin_limit', "货币阈值", 5000000, [0, 5000000, 10000000, 20000000])
@inttype('normal_shop_reset_count', "重置次数(<=20)", 0, [i for i in range(21)])
@multichoice("normal_shop_buy_kind", "购买种类", ['经验药水', '强化石'], ['经验药水', '强化石'])
@description('')
@name('通用商店购买')
@default(False)
class normal_shop(shop_buyer):
    def coin_limit(self) -> int: return self.get_config('normal_shop_buy_coin_limit')
    def system_id(self) -> eSystemId: return eSystemId.NORMAL_SHOP
    def reset_count(self) -> int: return self.get_config('normal_shop_reset_count')
    def buy_kind(self) -> List[str]: return self.get_config('normal_shop_buy_kind')

@singlechoice('limit_shop_buy_coin_limit', "货币阈值", 5000000, [0, 5000000, 10000000, 20000000])
@multichoice("limit_shop_buy_kind", "购买种类", ['经验药水', '装备'], ['经验药水', '装备'])
@description('此项购买不使用最大值')
@name('限定商店购买')
@default(False)
class limit_shop(shop_buyer):
    def _exp_count(self): return 99000 if "经验药水" in self.get_config('limit_shop_buy_kind') else 0
    def _equip_count(self): return 9900 if "装备" in self.get_config('limit_shop_buy_kind') else 0
    def coin_limit(self) -> int: return self.get_config('limit_shop_buy_coin_limit')
    def system_id(self) -> eSystemId: return eSystemId.LIMITED_SHOP
    def reset_count(self) -> int: return 0
    def buy_kind(self) -> List[str]: return self.get_config('limit_shop_buy_kind')

@singlechoice('underground_shop_buy_memory_count_limit', "记忆碎片盈余值", 0, [0, 10, 20, 120, 270, 9900])
@singlechoice('underground_shop_buy_equip_count_limit', "装备盈余值", 0, [0, 20, 50, 100, 200, 500, 9900])
@singlechoice('underground_shop_buy_coin_limit', "货币阈值", 10000, [0, 10000, 50000, 100000, 200000])
@singlechoice("underground_shop_buy_equip_consider_unit_rank", "角色起始品级", "所有", ["所有", "最高", "次高", "次次高"])
@booltype("underground_shop_buy_equip_consider_unit_fav", "收藏角色", False) 
@inttype('underground_shop_reset_count', "重置次数(<=200)", 0, [i for i in range(201)])
@multichoice("underground_shop_buy_kind", "购买种类", ['记忆碎片', '装备'], ['记忆碎片', '装备'])
@name('地下城商店购买')
@description('根据需求购买装备和记忆碎片，可设置需求角色的品级和收藏角色')
@default(False)
class underground_shop(shop_buyer):
    def _equip_count(self):
        return self._get_count('装备', 'underground_shop_buy_equip_count_limit')
    def _unit_memory_count(self):
        return self._get_count('记忆碎片', 'underground_shop_buy_memory_count_limit')
    def coin_limit(self) -> int: return self.get_config('underground_shop_buy_coin_limit')
    def system_id(self) -> eSystemId: return eSystemId.EXPEDITION_SHOP
    def reset_count(self) -> int: return self.get_config('underground_shop_reset_count')
    def buy_kind(self) -> List[str]: return self.get_config('underground_shop_buy_kind')
    def require_equip_units_fav(self) -> bool: return self.get_config('underground_shop_buy_equip_consider_unit_fav')
    def require_equip_units_rank(self) -> str: return self.get_config('underground_shop_buy_equip_consider_unit_rank')

@singlechoice('jjc_shop_buy_memory_count_limit', "记忆碎片盈余值", 0, [0, 10, 20, 120, 270, 9900])
@singlechoice('jjc_shop_buy_equip_count_limit', "装备盈余值", 0, [0, 20, 50, 100, 200, 500, 9900])
@singlechoice('jjc_shop_buy_coin_limit', "货币阈值", 10000, [0, 10000, 50000, 100000, 200000])
@singlechoice("jjc_shop_buy_equip_consider_unit_rank", "角色起始品级", "所有", ["所有", "最高", "次高", "次次高"])
@booltype("jjc_shop_buy_equip_consider_unit_fav", "收藏角色", False) 
@inttype('jjc_shop_reset_count', "重置次数(<=20)", 0, [i for i in range(21)])
@multichoice("jjc_shop_buy_kind", "购买种类", ['记忆碎片', '装备'], ['记忆碎片', '装备'])
@name('jjc商店购买')
@description('根据需求购买装备和记忆碎片，可设置需求角色的品级和收藏角色')
@default(False)
class jjc_shop(shop_buyer):
    def _equip_count(self):
        return self._get_count('装备', 'jjc_shop_buy_equip_count_limit')
    def _unit_memory_count(self):
        return self._get_count('记忆碎片', 'jjc_shop_buy_memory_count_limit')
    def coin_limit(self) -> int: return self.get_config('jjc_shop_buy_coin_limit')
    def system_id(self) -> eSystemId: return eSystemId.ARENA_SHOP
    def reset_count(self) -> int: return self.get_config('jjc_shop_reset_count')
    def buy_kind(self) -> List[str]: return self.get_config('jjc_shop_buy_kind')
    def require_equip_units_fav(self) -> bool: return self.get_config('jjc_shop_buy_equip_consider_unit_fav')
    def require_equip_units_rank(self) -> str: return self.get_config('jjc_shop_buy_equip_consider_unit_rank')

@singlechoice('pjjc_shop_buy_memory_count_limit', "记忆碎片盈余值", 0, [0, 10, 20, 120, 270, 9900])
@singlechoice('pjjc_shop_buy_equip_count_limit', "装备盈余值", 0, [0, 20, 50, 100, 200, 500, 9900])
@singlechoice('pjjc_shop_buy_coin_limit', "货币阈值", 10000, [0, 10000, 50000, 100000, 200000])
@singlechoice("pjjc_shop_buy_equip_consider_unit_rank", "角色起始品级", "所有", ["所有", "最高", "次高", "次次高"])
@booltype("pjjc_shop_buy_equip_consider_unit_fav", "收藏角色", False) 
@inttype('pjjc_shop_reset_count', "重置次数(<=20)", 0, [i for i in range(21)])
@multichoice("pjjc_shop_buy_kind", "购买种类", ['记忆碎片', '装备'], ['记忆碎片', '装备'])
@name('pjjc商店购买')
@description('根据需求购买装备和记忆碎片，可设置需求角色的品级和收藏角色')
@default(False)
class pjjc_shop(shop_buyer):
    def _equip_count(self):
        return self._get_count('装备', 'pjjc_shop_buy_equip_count_limit')
    def _unit_memory_count(self):
        return self._get_count('记忆碎片', 'pjjc_shop_buy_memory_count_limit')
    def coin_limit(self) -> int: return self.get_config('pjjc_shop_buy_coin_limit')
    def system_id(self) -> eSystemId: return eSystemId.GRAND_ARENA_SHOP
    def reset_count(self) -> int: return self.get_config('pjjc_shop_reset_count')
    def buy_kind(self) -> List[str]: return self.get_config('pjjc_shop_buy_kind')
    def require_equip_units_fav(self) -> bool: return self.get_config('pjjc_shop_buy_equip_consider_unit_fav')
    def require_equip_units_rank(self) -> str: return self.get_config('pjjc_shop_buy_equip_consider_unit_rank')


@singlechoice('clanbattle_shop_buy_memory_count_limit', "记忆碎片盈余值", 0, [0, 10, 20, 120, 270, 9900])
@singlechoice('clanbattle_shop_buy_equip_count_limit', "装备盈余值", 0, [0, 20, 50, 100, 200, 500, 9900])
@singlechoice('clanbattle_shop_buy_coin_limit', "货币阈值", 10000, [0, 10000, 50000, 100000, 200000])
@singlechoice("clanbattle_shop_buy_equip_consider_unit_rank", "角色起始品级", "所有", ["所有", "最高", "次高", "次次高"])
@booltype("clanbattle_shop_buy_equip_consider_unit_fav", "收藏角色", False) 
@inttype('clanbattle_shop_reset_count', "重置次数(<=20)", 0, [i for i in range(21)])
@multichoice("clanbattle_shop_buy_kind", "购买种类", ['记忆碎片'], ['记忆碎片', '装备'])
@name('会战商店购买')
@description('根据需求购买装备和记忆碎片，可设置需求角色的品级和收藏角色')
@default(False)
class clanbattle_shop(shop_buyer):
    def _equip_count(self):
        return self._get_count('装备', 'clanbattle_shop_buy_equip_count_limit')
    def _unit_memory_count(self):
        return self._get_count('记忆碎片', 'clanbattle_shop_buy_memory_count_limit')
    def coin_limit(self) -> int: return self.get_config('clanbattle_shop_buy_coin_limit')
    def system_id(self) -> eSystemId: return eSystemId.CLAN_BATTLE_SHOP
    def reset_count(self) -> int: return self.get_config('clanbattle_shop_reset_count')
    def buy_kind(self) -> List[str]: return self.get_config('clanbattle_shop_buy_kind')
    def require_equip_units_fav(self) -> bool: return self.get_config('clanbattle_shop_buy_equip_consider_unit_fav')
    def require_equip_units_rank(self) -> str: return self.get_config('clanbattle_shop_buy_equip_consider_unit_rank')

