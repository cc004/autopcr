from collections import Counter

from ...model.custom import ItemType
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...db.models import GrowthParameter, GrowthParameterUnique
from ...model.enums import *
from ...model.common import SkillLevelInfo, SkillLevelUpDetail, UnitData

class UnitController(Module):

    unit_id: int
    client: pcrclient
    auto_level_up : bool = True
    auto_rank_up : bool = True
    use_raw_ore : bool = True

    skill_name = {
        eSkillLocationCategory.UNION_BURST_SKILL: "UB",
        eSkillLocationCategory.MAIN_SKILL_1: "S1",
        eSkillLocationCategory.MAIN_SKILL_2: "S2",
        eSkillLocationCategory.EX_SKILL_1: "EX",
    }

    @property
    def unit(self) -> UnitData:
        return self.client.data.unit[self.unit_id]

    @property
    def memory_id(self) -> int:
        return db.unit_to_memory[self.unit_id]

    @property
    def unit_name(self) -> str:
        return db.get_unit_name(self.unit_id)

    async def set_unique_growth_unit(self):
        ball = self.client.data.filter_inventory(db.is_unique_equip_glow_ball)
        if not ball:
            raise AbortError(f"没有专武球")
        if not self.unit.unique_equip_slot:
            raise AbortError(f"{self.unit_name}专武未实装")
        if self.unit.unique_equip_slot[0].is_slot:
            raise AbortError(f"{self.unit_name}专武已装备")
        if await self.is_unique_growth_unit():
            raise AbortError(f"{self.unit_name}已装备专武球")
        ball = ball[0]
        self._log(f"{self.unit_name}装备专武球")
        await self.client.set_growth_item_unique(self.unit_id, ball[1])

    async def is_growth_unit(self) -> Union[GrowthParameter, None]:
        if self.unit_id not in self.client.data.unit:
            raise AbortError(f"未解锁角色{self.unit_name}")
        if self.unit_id not in self.client.data.growth_unit:
            return None
        growth_id = list(set(self.client.data.growth_unit[self.unit_id].growth_parameter_list.growth_id_list) & set(db.growth_parameter.keys())) 
        if not growth_id:
            return None
        if len(growth_id) > 1:
            raise ValueError(f"{self.unit_name}怎么装了多个辉光球？" + ','.join(map(str, growth_id)))
        growth_limit = db.growth_parameter[growth_id[0]]
        return growth_limit

    async def is_unique_growth_unit(self) -> Union[GrowthParameterUnique, None]:
        if self.unit_id not in self.client.data.unit:
            raise AbortError(f"未解锁角色{self.unit_name}")
        if self.unit_id not in self.client.data.growth_unit:
            return None
        growth_id = list(set(self.client.data.growth_unit[self.unit_id].growth_parameter_list.growth_id_list) & set(db.growth_parameter_unique.keys())) 
        if not growth_id:
            return None
        if len(growth_id) > 1:
            raise ValueError(f"{self.unit_name}怎么装了多个专武辉光球？" + ','.join(map(str, growth_id)))
        growth_limit = db.growth_parameter_unique[growth_id[0]]
        return growth_limit

    async def unit_skill_up(self, location: eSkillLocationCategory, target_level: int, current_level: int, free: bool):
        step = target_level - current_level
        if free:
            self._log(f"{self.unit_name}技能{self.skill_name[location]}升至{current_level + step}级")
            skill_level_up_detail = SkillLevelUpDetail()
            skill_level_up_detail.location = location
            skill_level_up_detail.step = step
            skill_level_up_detail.current_level = current_level
            await self.client.skill_level_up(self.unit.id, [skill_level_up_detail])
        else:
            mana = db.get_skill_up_cost(current_level, target_level)
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{self.unit_name}技能{self.skill_name[location]}升至{target_level}级需要{mana}玛娜，当前玛娜不足")

            skill_levelup_list = [SkillLevelUpDetail(location=location, step=target_level-current_level, current_level=current_level)]
            self._log(f"{self.unit_name}技能{self.skill_name[location]}升至{current_level + step}级")
            await self.client.skill_level_up(self.unit.id,  skill_levelup_list)

    # md python 没有引用
    async def unit_skill_up_aware(self, location: eSkillLocationCategory, skill: Callable[[], SkillLevelInfo], target_skill_level: int, limit: Union[None, GrowthParameter] = None):
        if limit and limit.skill_level < target_skill_level and skill().skill_level < limit.skill_level:
            self._log(f"{self.unit_name}技能{self.skill_name[location]}超过了免费可提升等级{limit.skill_level},先提升至等级{limit.skill_level}")
            await self.unit_skill_up_aware(location, skill, limit.skill_level, limit)

        if target_skill_level > self.unit.unit_level:
            self._log(f"{self.unit_name}技能{self.skill_name[location]}升至{target_skill_level}级需要角色等级升至{target_skill_level}级")
            if not self.auto_level_up:
                raise AbortError(f"当前设置不自动拉角色等级，无法升级")
            await self.unit_level_up_aware(target_skill_level, limit)

        await self.unit_skill_up(location, target_skill_level, skill().skill_level, limit is not None and target_skill_level <= limit.skill_level)

    async def unit_promotion_up(self, target_promotion_level: int, free: bool):
        if free:
            self._log(f"{self.unit_name}升至品级{target_promotion_level}")
            await self.client.unit_free_promotion(self.unit.id, target_promotion_level)
        else:
            now_equip_slot = [equip.is_slot for equip in self.unit.equip_slot]
            equips = db.get_rank_promote_equip_demand(self.unit.id, self.unit.promotion_level, now_equip_slot, target_promotion_level, [False] * 6)
            cost_equip, mana = db.craft_equip(equips)
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{self.unit_name}升至品级{target_promotion_level}需要{mana}玛娜，当前玛娜不足")

            bad = self.client.data.get_not_enough_item(cost_equip)
            if bad and self.use_raw_ore:
                raw_ore = db.get_raw_ore_of_equip(bad)
                cost_equip += raw_ore
                cost_equip -= bad
                bad = self.client.data.get_not_enough_item(raw_ore)
            if bad:
                bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad.items()])
                raise AbortError(f"{self.unit_name}升至品级{target_promotion_level}所需材料不足:\n{bad_list}")

            for promotion in range(self.unit.promotion_level, target_promotion_level):
                equip = db.unit_promotion_equip_count[self.unit.id][promotion]
                if promotion == self.unit.promotion_level:
                    equip = equip - Counter((eInventoryType(eInventoryType.Equip), equip.id) for equip in self.unit.equip_slot if equip.is_slot)
                equip = db.craft_equip(equip)[0]
                bad = self.client.data.get_not_enough_item(equip)
                if bad:
                    raw_ore = db.get_raw_ore_of_equip(bad)
                    equip += raw_ore
                    equip -= bad
                equip_recipe_list = [equip]

                self._log(f"{self.unit_name}升至品级{promotion + 1}")
                await self.client.multi_promotion(self.unit.id, promotion + 1, equip_recipe_list)

    async def unit_promotion_up_aware(self, target_promotion_level: int, limit: Union[None, GrowthParameter]):
        if limit and target_promotion_level > limit.promotion_level and self.unit.promotion_level < limit.promotion_level:
            self._log(f"目标品级{target_promotion_level}超过了免费可提升品级{limit.promotion_level},先提升至品级{limit.promotion_level}")
            await self.unit_promotion_up_aware(limit.promotion_level, limit)

        demand_level = db.get_promotion_demand_level(self.unit.id, target_promotion_level)
        if self.unit.unit_level < demand_level:
            self._log(f"{self.unit_name}升至品级{target_promotion_level}需要升至{demand_level}级")
            await self.unit_level_up_aware(demand_level, limit)

        await self.unit_promotion_up(target_promotion_level, 
                                     limit is not None and target_promotion_level <= limit.promotion_level, 
                                     )

    async def unit_level_up(self, target_level: int, free: bool):
        if free:
            self._log(f"{self.unit_name}升至{target_level}级")
            await self.client.unit_free_level_up(self.unit.id, target_level)
        else:
            exp_demand = db.get_level_up_total_exp(target_level) - self.unit.unit_exp
            exp_demand_limit = db.get_level_up_total_exp(target_level + 1) - self.unit.unit_exp
            cost_potion = self.client.data.get_level_up_exp_potion_demand(exp_demand, exp_demand_limit)
            if not cost_potion:
                raise AbortError(f"{self.unit_name}升至{target_level}级所需经验药水不足，或无法达到其要求")

            self._log(f"{self.unit_name}升至{target_level}级")
            await self.client.unit_level_up(self.unit.id, cost_potion)

    async def unit_level_up_aware(self, target_level: int, limit: Union[GrowthParameter, None] = None):
        if limit and target_level > limit.unit_level and self.unit.unit_level < limit.unit_level:
                self._log(f"{self.unit_name}目标等级{target_level}超过了免费可提升等级{limit.unit_level},先提升至等级{limit.unit_level}")
                await self.unit_level_up_aware(limit.unit_level, limit)

        level_limit = self.client.data.team_level + (10 if self.unit.exceed_stage else 0)
        if target_level > level_limit:
            raise AbortError(f"{self.unit_name}目标等级{target_level}超过了可提升的最高等级{level_limit}，无法升级")

        await self.unit_level_up(target_level, limit is not None and target_level <= limit.unit_level)

    async def unit_equip_slot(self, equip_id: int, slot_num: int, free: bool):
        if free:
            self._log(f"{self.unit_name}装备{db.get_equip_name(equip_id)}")
            await self.client.unit_free_equip(self.unit_id, [slot_num])
        else:
            item: ItemType = (eInventoryType.Equip, equip_id)
            cost_equip, mana = db.craft_equip(Counter({item: 1}))
            if (not await self.client.prepare_mana(mana)):
                raise AbortError(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}需要{mana}玛娜，当前玛娜不足")

            bad = self.client.data.get_not_enough_item(cost_equip)
            if bad and self.use_raw_ore:
                raw_ore = db.get_raw_ore_of_equip(bad)
                cost_equip += raw_ore
                cost_equip -= bad
                bad = self.client.data.get_not_enough_item(raw_ore)
            if bad:
                bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad.items()])
                raise AbortError(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}所需材料不足:\n{bad_list}")

            self._log(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}")
            await self.client.unit_craft_equip(self.unit.id, slot_num, cost_equip)

    async def unit_equip_slot_aware(self, equip_id: int, slot_num: int, limit: Union[None, GrowthParameter] = None):
        if db.equip_data[equip_id].require_level > self.unit.unit_level:
            self._log(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}需要角色升至{db.equip_data[equip_id].require_level}级")
            if not self.auto_level_up:
                raise AbortError(f"当前设置不自动拉角色等级，无法装备")
            await self.unit_level_up_aware(db.equip_data[equip_id].require_level, limit)

        await self.unit_equip_slot(equip_id, slot_num, limit is not None and (
                                   limit.promotion_level > self.unit.promotion_level or \
                                   limit.promotion_level == self.unit.promotion_level and getattr(limit, f"equipment_{slot_num}") != -1))

    async def unit_equip_enhance(self, equip_id: int, slot_num: int, enhancement_level: int, free: bool):

        if free:
            self._log(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级")
            await self.client.equipment_free_enhance(self.unit.id, slot_num, enhancement_level)
        else:
            current_enhancement_pt = self.unit.equip_slot[slot_num - 1].enhancement_pt
            pt = db.get_equip_star_pt(equip_id, enhancement_level) - current_enhancement_pt
            pt_limit = -1 if enhancement_level == db.get_equip_max_star(equip_id) else db.get_equip_star_pt(equip_id, enhancement_level + 1) - current_enhancement_pt
            cost_stone = self.client.data.get_equip_enhance_stone_demand(pt, pt_limit)
            if not cost_stone:
                raise AbortError(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级所需强化石不足，或无法达到其要求")

            mana = pt * 200 # guess
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级需要{mana}玛娜，当前玛娜不足")

            self._log(f"{self.unit_name}{slot_num}位装备{db.get_equip_name(equip_id)}强化至{enhancement_level}星级")
            await self.client.equipment_enhance(self.unit.id, slot_num, current_enhancement_pt, cost_stone)

    async def unit_unique_slot_aware(self, limit: Union[GrowthParameterUnique, None] = None):
        if self.unit.promotion_level < 7:
            self._log(f"{self.unit_name}专武需要角色升至品级7")
            if not self.auto_rank_up:
                raise AbortError(f"当前设置不自动拉品级，无法装备")
            await self.unit_promotion_up_aware(7, await self.is_growth_unit())

        if limit:
            pass
        else:
            await self.unit_unique_slot(False)

    async def unit_unique_slot(self, free: bool):
        if free: # impossible
            pass
        else:
            equip_id = db.unit_unique_equip[1][self.unit_id].equip_id
            if self.client.data.get_inventory((eInventoryType.Equip, equip_id)) == 0:
                demand = db.get_unique_equip_material_demand(self.unit_id, 1, 0, 1)
                bad = self.client.data.get_not_enough_item(demand)
                if bad:
                    bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad.items()])
                    raise AbortError(f"制作{self.unit_name}专武所需材料不足:\n{bad_list}")
                self._log(f"{self.unit_name}制作专武")
                equip_recipe_dict = Counter({item: cnt for item, cnt in demand.items() if db.is_equip(item) or item == db.xinsui})
                item_recipe_dict = demand - equip_recipe_dict
                await self.client.equipment_craft_unique(equip_id, equip_recipe_dict, item_recipe_dict, 0)
            mana = self.client.data.get_mana()
            self._log(f"{self.unit_name}装备专武")
            await self.client.equipment_multi_enhance_unique(self.unit_id, 1, mana, [], [], [], [], [], 0, 1, [], 0)

    async def unit_unique_equip_rank_up_aware(self, target_rank: int, limit: Union[GrowthParameterUnique, None] = None):
        require_level = db.get_unique_equip_rank_required_level(1, self.unit_id, target_rank)
        if require_level > self.unit.unit_level:
            self._log(f"{self.unit_name}专武突破至{target_rank}品级需要角色升至{require_level}级")
            if not self.auto_level_up:
                raise AbortError(f"当前设置不自动拉角色等级，无法升级")
            await self.unit_level_up_aware(require_level, await self.is_growth_unit())

        # 先判断整个突破过程是否可行
        start_rank = self.unit.unique_equip_slot[0].rank if not limit else max(self.unit.unique_equip_slot[0].rank, limit.unique_equip_rank_1)
        demand = db.get_unique_equip_material_demand(self.unit_id, 1, start_rank, target_rank)
        bad = self.client.data.get_not_enough_item(demand)
        if bad:
            bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad.items()])
            raise AbortError(f"{self.unit_name}专武突破至{target_rank}品级所需材料不足:\n{bad_list}")

        if not self.unit.unique_equip_slot:
            raise AbortError(f"{self.unit_name}专武未实装")

        if self.unit.unique_equip_slot[0].is_slot == 0:
            self._log(f"{self.unit_name}专武突破至{target_rank}品级需要先装备专武")
            await self.unit_unique_slot_aware(limit)

        if limit and self.unit.unique_equip_slot[0].enhancement_pt < limit.unique_equip_strength_point_1:
            pass
        else:
            await self.unit_unique_equip_rank_up(target_rank, False)

    async def unit_unique_equip_rank_up(self, target_rank: int, free: bool):
        if free: # impossible
            pass
        else:
            current_rank = self.unit.unique_equip_slot[0].rank
            demand = db.get_unique_equip_material_demand(self.unit_id, 1, current_rank, target_rank)
            bad = self.client.data.get_not_enough_item(demand)
            if bad:
                bad_list = '\n'.join([f"{db.get_inventory_name_san(item)}缺少{cnt}片" for item, cnt in bad.items()])
                raise AbortError(f"{self.unit_name}专武突破至{target_rank}品级所需材料不足:\n{bad_list}")

            mana = (target_rank - current_rank) * 1000000 # TODO 随便设的
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{self.unit_name}专武突破至{target_rank}品级需要{mana}玛娜，当前玛娜不足")

            for cur_rank in range(current_rank, target_rank):
                self._log(f"{self.unit_name}专武突破至{cur_rank + 1}品级")
                demand = db.get_unique_equip_material_demand(self.unit_id, 1, cur_rank, cur_rank + 1)
                equip_recipe_dict = Counter({item: cnt for item, cnt in demand.items() if db.is_equip(item) or item == db.xinsui})
                item_recipe_dict = demand - equip_recipe_dict
                await self.client.equipment_rankup_unique(self.unit.id, 1, equip_recipe_dict, item_recipe_dict, cur_rank)

    async def unit_unique_equip_enhance_aware(self, target_level: int, limit: Union[GrowthParameterUnique, None] = None):
        target_pt = db.get_unique_equip_pt_from_level(1, target_level)
        if limit and target_pt > limit.unique_equip_strength_point_1 and self.unit.unique_equip_slot[0].enhancement_pt < limit.unique_equip_strength_point_1:
            level = db.get_unique_equip_level_from_pt(1, limit.unique_equip_strength_point_1)
            self._log(f"目标专武等级{target_level}超过了免费可提升等级{level},先提升至等级{level}")
            await self.unit_unique_equip_enhance_aware(level, limit)

        target_rank = db.get_unique_equip_rank_from_level(1, target_level)

        if target_rank > self.unit.unique_equip_slot[0].rank:
            self._log(f"{self.unit_name}专武升至{target_level}级需要先突破至{target_rank}品级")
            await self.unit_unique_equip_rank_up_aware(target_rank, limit)

        if self.unit.unique_equip_slot[0].enhancement_level < target_level:
            await self.unit_unique_equip_enhance(target_level, limit is not None and target_level <= db.get_unique_equip_level_from_pt(1, limit.unique_equip_strength_point_1))

    async def unit_unique_equip_enhance(self, target_level: int, free: bool):
        if free:
            self._log(f"{self.unit_name}专武升至{target_level}级")
            start_pt = self.unit.unique_equip_slot[0].enhancement_pt
            target_pt = db.get_unique_equip_pt_from_level(1, target_level)
            await self.client.unique_equip_free_enhance(self.unit.id, 1, start_pt, target_pt)
        else:
            current_enhancement_pt: int = self.unit.unique_equip_slot[0].enhancement_pt
            target_pt = db.get_unique_equip_pt_from_level(1, target_level)
            pt = target_pt - current_enhancement_pt

            pt_limit = -1 if target_level == db.get_unique_equip_max_level_from_rank(1, self.unit.unique_equip_slot[0].rank) else db.get_unique_equip_pt_from_level(1, target_level + 1) - current_enhancement_pt
            cost_stone = self.client.data.get_equip_enhance_stone_demand(pt, pt_limit)
            if not cost_stone:
                raise AbortError(f"{self.unit_name}专武升至{target_level}级所需强化石不足，或无法达到其要求")

            mana = pt * 680 # guess
            if not (await self.client.prepare_mana(mana)):
                raise AbortError(f"{self.unit_name}专武升至{target_level}级需要{mana}玛娜，当前玛娜不足")

            self._log(f"{self.unit_name}专武升至{target_level}级")
            await self.client.equipment_enhance_unique(self.unit.id, 1, cost_stone, current_enhancement_pt)

    async def get_memory_gap(self, star: int, unique_level: int, exceed_state: bool) -> int:
        client = self.client
        unique_rank = db.get_unique_equip_rank_from_level(1, unique_level)

        token = (eInventoryType.Item, self.memory_id)
        demand = client.data.get_unit_memory_demand(self.unit_id, star, unique_rank, exceed_state)

        gap = demand - client.data.get_inventory(token)
        self._log(f"{db.get_inventory_name_san(token)}需求{demand}，库存{client.data.get_inventory(token)}，将购买{max(0, gap)}")

        return gap

    async def buy_master_shop(self, gap: int) -> int:
        client = self.client
        shop_id = eSystemId.COUNTER_STOP_SHOP
        shops = {shop.system_id: shop for shop in (await client.get_shop_item_list()).shop_list}

        master_shop = shops.get(shop_id, None)
        if not master_shop:
            self._log("大师店未开启")
            return gap

        items = [item for item in master_shop.item_list if item.item_id == self.memory_id and not item.sold]
        buy = Counter()
        cost = 0
        for item in items:
            cnt = min((gap + item.num - 1) // item.num, item.stock_count - item.purchase_count)
            if cnt:
                buy[item.slot_id] += cnt
                cost += cnt * item.price.currency_num
                gap -= cnt * item.num

        golds = client.data.get_shop_gold(shop_id)
        if cost > golds:
            self._log(f"大师店代币{golds}<{cost}")
            return gap

        if buy:
            ret = await client.shop_buy_bulk(shop_id, buy)
            msg = await client.serlize_reward(ret.purchase_list)
            self._log(f"花费{cost}大师币购买了{msg}")
        return gap

    async def buy_nvshen_shop(self, gap: int) -> int:
        client = self.client
        shop_id = eSystemId.MEMORY_PIECE_SHOP
        shops = {shop.system_id: shop for shop in (await client.get_shop_item_list()).shop_list}
        
        shop = shops.get(shop_id, None)
        if not shop:
            self._log("女神店未开启")
            return gap

        items = [item for item in shop.item_list if item.item_id == self.memory_id and not item.sold]

        cost = 0
        golds = client.data.get_shop_gold(shop_id)
        for item in items: # it should be one
            total_price = db.get_shop_item_buy_total_price(item.price_group, item.exchange_count, gap)
            if golds < total_price:
                self._log(f"女神币{golds}<{total_price}, 无法购买")
                return gap
            while gap > 0:
                info = db.get_shop_item_price_info(item.price_group, item.exchange_count)
                cnt = gap if info.buy_count_to == -1 else min(gap, info.buy_count_to - item.exchange_count)
                assert cnt > 0, '怎么会出现0个的情况呢？'
                cost = cnt * info.count
                ret = await client.shop_buy(shop_id, item.slot_id, cnt, cost)
                msg = await client.serlize_reward(ret.purchase_list)
                self._log(f"花费{cost}母猪石购买了{msg}")
                gap -= cnt
                item.exchange_count += cnt
                golds -= cost
        return gap

    async def buy_memory(self, gap: int):
        for buy_shop in [self.buy_master_shop, self.buy_nvshen_shop]:
            if gap > 0:
                gap = await buy_shop(gap)
        return gap

    async def promote(self, target_level: int = 1, target_star: int = 1, target_dear: int = 1, target_promote_rank: int = 1, target_equip_star: List[int] = [-1, -1, -1, -1, -1, -1], target_skill_ub_level: int = 1, target_skill_s1_level: int = 1, target_skill_s2_level: int = 1, target_skill_ex_level: int = 1, target_unique1_level: int = 0):
        growth_limit = await self.is_growth_unit()

        if self.unit.unit_level < target_level:
            await self.unit_level_up_aware(target_level, growth_limit)

        if self.unit.promotion_level < target_promote_rank:
            await self.unit_promotion_up_aware(target_promote_rank, growth_limit)

        for i in range(6):
            equip = self.unit.equip_slot[i]
            if equip.id == 999999:
                continue

            star = target_equip_star[i]

            if star != -1:
                if not equip.is_slot:
                    await self.unit_equip_slot_aware(equip.id, i + 1, growth_limit)

                promotion_limit = db.get_equip_max_star(equip.id)
                if star > promotion_limit:
                    self._log(f"{i+1}号位装备预设{star}星级超过了最大星级{promotion_limit}，提升至最大星级{promotion_limit}")
                    star = promotion_limit

                if equip.enhancement_level < star:
                    await self.unit_equip_enhance(equip.id, i + 1, star, growth_limit is not None and (
                        self.unit.promotion_level < growth_limit.promotion_level or \
                        self.unit.promotion_level == growth_limit.promotion_level and getattr(growth_limit, f"equipment_{i}") > star))

        if self.unit.union_burst and self.unit.union_burst[0].skill_level < target_skill_ub_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.UNION_BURST_SKILL, lambda: self.unit.union_burst[0], target_skill_ub_level, growth_limit)

        if self.unit.main_skill and self.unit.main_skill[0].skill_level < target_skill_s1_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.MAIN_SKILL_1, lambda: self.unit.main_skill[0], target_skill_s1_level, growth_limit)

        if len(self.unit.main_skill) > 1 and self.unit.main_skill[1].skill_level < target_skill_s2_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.MAIN_SKILL_2, lambda: self.unit.main_skill[1], target_skill_s2_level, growth_limit)

        if self.unit.ex_skill and self.unit.ex_skill[0].skill_level < target_skill_ex_level:
            await self.unit_skill_up_aware(eSkillLocationCategory.EX_SKILL_1, lambda: self.unit.ex_skill[0], target_skill_ex_level, growth_limit)

        growth_limit_unique = await self.is_unique_growth_unit()
        if self.unit.unique_equip_slot and self.unit.unique_equip_slot[0].enhancement_level < target_unique1_level:
            await self.unit_unique_equip_enhance_aware(target_unique1_level, growth_limit_unique)


@description('支持全部角色')
@name('完成装备强化任务')
@unitchoice("equip_enhance_up_unit", "强化角色")
@default(False)
class unit_equip_enhance_up(UnitController):
    async def do_task(self, client: pcrclient):
        if client.data.is_mission_finished(eSystemId.UNIT_EQUIP_ENHANCE):
            raise SkipError("今日已完成装备强化任务")

        self.client = client
        unit_id, unit_name = self.get_config('equip_enhance_up_unit').split(':')
        self.unit_id = int(unit_id)

        growth_limit = await self.is_growth_unit()

        equip_slot_list = [1, 3, 5, 4, 2, 0]

        stop = False
        while not stop:
            for id in equip_slot_list: 
                equip = self.unit.equip_slot[id]
                
                if equip.id == 999999: # 未实装
                    raise AbortError("装备已强化至最高级，请更换角色")

                slot_num = id + 1
                if not equip.is_slot:
                    await self.unit_equip_slot_aware(equip.id, slot_num, growth_limit)

                if equip.enhancement_level < db.get_equip_max_star(equip.id):
                    await self.unit_equip_enhance(equip.id, slot_num, equip.enhancement_level + 1, growth_limit is not None)
                    stop = True
                    break
            else:
                self._log(f"所有装备均已满强化，需提升角色品级")
                await self.unit_promotion_up_aware(self.unit.promotion_level + 1, growth_limit)

@description('支持全部角色')
@name('完成技能升级任务')
@unitchoice("level_up_unit", "强化角色")
@default(False)
class unit_skill_level_up(UnitController):
    async def do_task(self, client: pcrclient):
        if client.data.is_mission_finished(eSystemId.UNIT_SKILL_LVUP):
            raise SkipError("今日已完成技能升级任务")

        self.client = client
        unit_id, unit_name = self.get_config('level_up_unit').split(':')
        self.unit_id = int(unit_id)

        growth_limit = await self.is_growth_unit()

        stop = False

        while not stop:
            skills = [(eSkillLocationCategory(eSkillLocationCategory.UNION_BURST_SKILL + id), lambda id=id: self.unit.union_burst[id]) for id, skill in enumerate(self.unit.union_burst)] +  \
                    [(eSkillLocationCategory(eSkillLocationCategory.MAIN_SKILL_1 + id), lambda id=id: self.unit.main_skill[id]) for id, skill in enumerate(self.unit.main_skill)] +  \
                    [(eSkillLocationCategory(eSkillLocationCategory.EX_SKILL_1 + id), lambda id=id: self.unit.ex_skill[id]) for id, skill in enumerate(self.unit.ex_skill)]

            for pos, skill in skills:
                try:
                    if skill().skill_level < self.unit.unit_level:
                        await self.unit_skill_up_aware(pos, skill, skill().skill_level + 1, growth_limit)
                        stop = True
                        break
                except AbortError as e:
                    continue
            else:
                self._log(f"所有技能均等于角色等级{self.unit.unit_level}级，需提升角色等级")
                await self.unit_level_up_aware(self.unit.unit_level + 1, growth_limit)

@description('仅支持设置未装备专武的角色，优先使用低专武球')
@name('设置专武球')
@unitchoice("unit_set_unique_equip_growth_id", "装备角色")
@default(False)
class unit_set_unique_equip_growth(UnitController):

    async def do_task(self, client: pcrclient):
        self.client = client
        unit_id, unit_name = self.get_config('unit_set_unique_equip_growth_id').split(':')
        self.unit_id = int(unit_id)
        await self.set_unique_growth_unit()

@description('支持全部角色，装备星级-1表示不穿装备，自动拉等级指当前等级不足以穿装备或提升技能等级，将会提升角色等级，自动拉品级指当前品级不足以装备专武时，会提升角色品级，使用原矿指装备不足时用原矿补充')
@name('拉角色练度')
@booltype("unit_promote_rank_when_fail_to_unique_equip", "自动拉品级", False)
@booltype("unit_promote_level_when_fail_to_equip_or_skill", "自动拉等级", False)
@booltype("unit_promote_rank_use_raw_ore", "使用原矿", False)
@singlechoice("unit_promote_unique_equip1_level", "专武等级", 0, lambda : db.unit_unique_equip_level_candidate(1))
@singlechoice("unit_promote_equip_5", "右下装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_4", "左下装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_3", "右中装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_2", "左中装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_1", "右上装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_equip_0", "左上装备星级", -1, [-1,0,1,2,3,4,5])
@singlechoice("unit_promote_skill_ex", "ex等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_skill_s2", "s2等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_skill_s1", "s1等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_skill_ub", "ub等级", 1, db.unit_level_candidate)
@singlechoice("unit_promote_rank", "品级", 1, db.unit_rank_candidate)
@singlechoice("unit_promote_level", "等级", 1, db.unit_level_candidate)
@unitchoice("unit_promote_unit", "拉取角色")
@default(False)
class unit_promote(UnitController):

    async def do_task(self, client: pcrclient):
        self.client = client
        unit_id, unit_name = self.get_config('unit_promote_unit').split(':')
        self.unit_id = int(unit_id)

        self.auto_level_up = bool(self.get_config('unit_promote_level_when_fail_to_equip_or_skill'))
        self.auto_rank_up = bool(self.get_config('unit_promote_rank_when_fail_to_unique_equip'))
        self.use_raw_ore = bool(self.get_config('unit_promote_rank_use_raw_ore'))

        target_level = int(self.get_config('unit_promote_level'))
        target_promotion_rank = int(self.get_config('unit_promote_rank'))
        target_equip_star = [int(self.get_config(f'unit_promote_equip_{i}')) for i in range(6)]
        target_skill_ub_level = int(self.get_config('unit_promote_skill_ub'))
        target_skill_s1_level = int(self.get_config('unit_promote_skill_s1'))
        target_skill_s2_level = int(self.get_config('unit_promote_skill_s2'))
        target_skill_ex_level = int(self.get_config('unit_promote_skill_ex'))
        target_unique1_level = int(self.get_config('unit_promote_unique_equip1_level'))

        await self.promote(target_level = target_level, 
                           target_promote_rank = target_promotion_rank, 
                           target_equip_star = target_equip_star, 
                           target_skill_ub_level = target_skill_ub_level, 
                           target_skill_s1_level = target_skill_s1_level, 
                           target_skill_s2_level = target_skill_s2_level, 
                           target_skill_ex_level = target_skill_ex_level, 
                           target_unique1_level = target_unique1_level)

@description('''角色ID	角色名字	角色等级	角色星级	角色好感度	角色Rank	装备等级(左上)	装备等级(右上)	装备等级(左中)	装备等级(右中)	装备等级(左下)	装备等级(右下)	UB技能等级	技能1等级	技能2等级	EX技能等级	专武等级	EX武器	EX武器等级	EX防具	EX防具等级	EX首饰	EX首饰等级	高级设置
不会使用专武球，专武升级请认真考虑！
不考虑星级、好感度、EX武器、高级设置''')
@name('批量拉角色练度')
@texttype("unit_promote_text", "目标练度", "")
@booltype("unit_promote_batch_use_raw_ore", "使用原矿", False)
@default(False)
class unit_promote_batch(UnitController):

    async def do_task(self, client: pcrclient):

        self.client = client
        unit_promote_texts = self.get_config('unit_promote_text').strip().split('\n')
        self.use_raw_ore = bool(self.get_config('unit_promote_batch_use_raw_ore'))

        for unit_text in unit_promote_texts:
            try:
                unit_id, unit_name, target_level, target_star, target_dear, target_rank, \
                    equip_0, equip_1, equip_2, equip_3, equip_4, equip_5, \
                    ub, s1, s2, ex, unique1_level, \
                    ex1_id, ex1_star, ex2_id, ex2_star, ex3_id, ex3_star, \
                    dear_info = unit_text.split()

                equip_star = [equip_0, equip_1, equip_2, equip_3, equip_4, equip_5]

                self.unit_id = int(unit_id)

                self.auto_level_up = False
                self.auto_rank_up = False

                target_level = int(target_level)
                target_star = int(target_star)
                target_dear = int(target_dear)
                target_promotion_rank = int(target_rank)
                target_equip_star = [int(equip_star[i]) if equip_star[i].isdigit() else -1 for i in range(6)]
                target_skill_ub_level = int(ub)
                target_skill_s1_level = int(s1)
                target_skill_s2_level = int(s2)
                target_skill_ex_level = int(ex)
                target_unique1_level = int(unique1_level) if unique1_level.isdigit() else 0
                target_ex1_id = int(ex1_id)
                target_ex1_star = int(ex1_star)
                target_ex2_id = int(ex2_id)
                target_ex2_star = int(ex2_star)
                target_ex3_id = int(ex3_id)
                target_ex3_star = int(ex3_star)

                await self.promote(target_level = target_level,
                                   target_star = target_star,
                                   target_dear = target_dear,
                                   target_promote_rank = target_promotion_rank,
                                   target_equip_star = target_equip_star,
                                   target_skill_ub_level = target_skill_ub_level,
                                   target_skill_s1_level = target_skill_s1_level,
                                   target_skill_s2_level = target_skill_s2_level,
                                   target_skill_ex_level = target_skill_ex_level,
                                   target_unique1_level = target_unique1_level)

            except Exception as e:
                self._warn(str(e))
                continue

@name('购买记忆碎片')
@booltype("unit_memory_do_buy", "开买", False)
@booltype("unit_memory_unit_exceed_state", "界限突破", False)
@singlechoice("unit_memory_unique_equip_level", "专武等级", 0, lambda : db.unit_unique_equip_level_candidate(1))
@singlechoice("unit_memory_unit_star", "星级", 1, [1,2,3,4,5,6])
@unitchoice("unit_memory_buy_unit", "角色")
@default(False)
@description('购买目标练度所缺的记忆碎片，先考虑大师店，再考虑女神店，其余商店请用对应的商店模块购买！')
class unit_memory_buy(UnitController):
    async def do_task(self, client: pcrclient):
        self.client = client
        self.unit_id = int(self.get_config('unit_memory_buy_unit').split(':')[0])
        do_buy = bool(self.get_config('unit_memory_do_buy'))
        star = int(self.get_config('unit_memory_unit_star'))
        exceed_state = bool(self.get_config('unit_memory_unit_exceed_state'))
        unique_level = int(self.get_config('unit_memory_unique_equip_level'))

        gap = await self.get_memory_gap(star, unique_level, exceed_state)
        if do_buy:
            await self.buy_memory(gap)

@name('批量购买记忆碎片')
@booltype("unit_memory_batch_do_buy", "开买", False)
@description('''角色ID	角色名字	角色等级	角色星级	角色好感度	角色Rank	装备等级(左上)	装备等级(右上)	装备等级(左中)	装备等级(右中)	装备等级(左下)	装备等级(右下)	UB技能等级	技能1等级	技能2等级	EX技能等级	专武等级	EX武器	EX武器等级	EX防具	EX防具等级	EX首饰	EX首饰等级	高级设置
购买目标练度所缺的记忆碎片，先考虑大师店，再考虑女神店，其余商店请用对应的商店模块购买！
仅考虑星级、专武，不考虑界限突破''')
@default(False)
@texttype("unit_memory_buy_batch_text", "目标练度", "")
class unit_memory_buy_batch(UnitController):
    async def do_task(self, client: pcrclient):
        self.client = client
        unit_memory_buy_text = self.get_config('unit_memory_buy_batch_text').strip().split('\n')
        do_buy = bool(self.get_config('unit_memory_batch_do_buy'))

        summary = []

        for unit_text in unit_memory_buy_text:
            try:
                unit_id, unit_name, target_level, target_star, target_dear, target_rank, \
                    equip_0, equip_1, equip_2, equip_3, equip_4, equip_5, \
                    ub, s1, s2, ex, unique1_level, \
                    ex1_id, ex1_star, ex2_id, ex2_star, ex3_id, ex3_star, \
                    dear_info = unit_text.split()

                self.unit_id = int(unit_id)
                star = int(target_star)
                exceed_state = False
                try:
                    unique_level = int(unique1_level)
                except:
                    unique_level = 0

                gap = await self.get_memory_gap(star, unique_level, exceed_state)
                if do_buy:
                    gap = await self.buy_memory(gap)
                    if gap > 0:
                        self._log(f"剩余{gap}个记忆碎片未购买")
                else:
                    if gap > 0:
                        summary.append(f"{gap}片{unit_name}记忆碎片")

            except Exception as e:
                self._warn(str(e))
                continue

        if summary:
            self._warn(f"将购买记忆碎片:\n" + '\n'.join(summary))
