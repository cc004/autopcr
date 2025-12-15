from pydantic.class_validators import make_generic_validator
from pydantic.fields import ModelField
from pydantic.validators import int_validator

from ..model.custom import TalentQuestData
from . import responses, sdkrequests
from .common import *
from .requests import *
from ..core.datamgr import datamgr
from ..db.database import db
from .enums import eEventSubStoryStatus
from typing import Optional

def handles(cls):
    cls.__base__.update = cls.update
    return None

@handles
class SourceIniGetMaintenanceStatusResponse(sdkrequests.SourceIniGetMaintenanceStatusResponse):
    async def update(self, mgr: datamgr, request):
        if self.manifest_ver:
            await mgr.try_update_database(int(self.manifest_ver))

@handles
class CaravanTopResponse(responses.CaravanTopResponse):
    async def update(self, mgr: datamgr, request):
        if self.caravan_item_list:
            for item in self.caravan_item_list:
                mgr.update_inventory(item)
        if self.init_reward_list:
            for item in self.init_reward_list:
                mgr.update_inventory(item)
        if self.buddy_reward_list:
            for item in self.buddy_reward_list:
                mgr.update_inventory(item)
        if self.minigame_retire_reward:
            for item in self.minigame_retire_reward:
                mgr.update_inventory(item)
        if self.reset_reward:
            for item in self.reset_reward:
                mgr.update_inventory(item)

@handles
class TravelResultRoundEventResponse(responses.TravelResultRoundEventResponse):
    async def update(self, mgr: datamgr, request):
        if self.current_round_result and self.current_round_result.reward_list:
            for item in self.current_round_result.reward_list:
                mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.user_jewel:
            mgr.jewel = self.user_jewel

@handles
class CaravanCoinShopBuyBulkResponse(responses.CaravanCoinShopBuyBulkResponse):
    async def update(self, mgr: datamgr, request):
        if self.purchase_list:
            for item in self.purchase_list:
                mgr.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)

@handles
class CaravanCoinShopBuyResponse(responses.CaravanCoinShopBuyResponse):
    async def update(self, mgr: datamgr, request):
        if self.purchase_list:
            for item in self.purchase_list:
                mgr.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)

@handles
class CaravanDishSellResponse(responses.CaravanDishSellResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)

@handles
class CaravanMinigameCccFinishResponse(responses.CaravanMinigameCccFinishResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)

@handles
class CaravanMinigameCccBsFinishResponse(responses.CaravanMinigameCccBsFinishResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)

@handles
class CaravanDishUseResponse(responses.CaravanDishUseResponse):
    async def update(self, mgr: datamgr, request):
        mgr.caravan_dishes[request.dish_id] -= 1
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)
        if self.sub_reward_list:
            for item in self.sub_reward_list:
                mgr.update_inventory(item)

@handles
class CaravanDiceRollResponse(responses.CaravanDiceRollResponse):
    async def update(self, mgr: datamgr, request):
        if self.buddy_reward_list:
            for item in self.buddy_reward_list:
                mgr.update_inventory(item)

@handles
class CaravanProgressTurnResponse(responses.CaravanProgressTurnResponse):
    async def update(self, mgr: datamgr, request):
        if self.buddy_reward_list:
            for item in self.buddy_reward_list:
                mgr.update_inventory(item)

@handles
class CaravanGachaBlockExecResponse(responses.CaravanGachaBlockExecResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)

@handles
class CaravanMoveResponse(responses.CaravanMoveResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)
        if self.goal_bonus_list:
            for item in self.goal_bonus_list:
                mgr.update_inventory(item)
        if self.treasure_reward_list:
            for item in self.treasure_reward_list:
                mgr.update_inventory(item)
        if self.lottery_result_list:
            for item in self.lottery_result_list:
                mgr.update_inventory(item)

@handles
class SkillLevelUpResponse(responses.SkillLevelUpResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)

@handles
class UnitFreeLevelUpResponse(responses.UnitFreeLevelUpResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data

@handles
class UnitFreePromotionResponse(responses.UnitFreePromotionResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data

@handles
class UnitFreeEquipResponse(responses.UnitFreeEquipResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data

@handles
class EquipmentFreeEnhanceResponse(responses.EquipmentFreeEnhanceResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data

@handles
class UnitExceedLevelLimitResponse(responses.UnitExceedLevelLimitResponse):
    async def update(self, mgr: datamgr, request:UnitExceedLevelLimitRequest):
        mgr.unit[request.unit_id].exceed_stage = self.exceed_stage
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.equip_list:
            for item in self.equip_list:
                mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class ShioriQuestSkipResponse(responses.ShioriQuestSkipResponse):
    async def update(self, mgr: datamgr, request):
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.level_info:
            mgr.team_level = self.level_info.team.start_level
        if self.user_info:
            mgr.stamina = self.user_info.user_stamina
            mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        mgr.quest_dict[request.quest_id].daily_clear_count = self.daily_clear_count

@handles
class TrainingQuestSkipResponse(responses.TrainingQuestSkipResponse):
    async def update(self, mgr: datamgr, request: TrainingQuestSkipRequest):
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        mgr.quest_dict[request.quest_id].daily_clear_count = self.daily_clear_count
        mgr.stamina = self.user_info.user_stamina
        mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        if self.quest_challenge_count:
            mgr.training_quest_count = self.quest_challenge_count

@handles
class TrainingQuestFinishResponse(responses.TrainingQuestFinishResponse):
    async def update(self, mgr: datamgr, request):
        mgr.training_quest_count = self.quest_challenge_count

@handles
class StoryViewingResponse(responses.StoryViewingResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for item in self.reward_info:
                mgr.update_inventory(item)


@handles
class ShopResetResponse(responses.ShopResetResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.user_jewel:
            mgr.jewel = self.user_jewel


@handles
class ShopRecoverStaminaResponse(responses.ShopRecoverStaminaResponse):
    async def update(self, mgr: datamgr, request):
        mgr.jewel = self.user_jewel
        mgr.stamina = self.user_info.user_stamina
        mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        mgr.recover_stamina_exec_count = self.recover_stamina.exec_count


@handles
class ShopBuyResponse(responses.ShopBuyResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.purchase_list:
            for item in self.purchase_list:
                mgr.update_inventory(item)
        if self.user_jewel:
            mgr.jewel = self.user_jewel


@handles
class ShopBuyMultipleResponse(responses.ShopBuyMultipleResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.purchase_list:
            for item in self.purchase_list:
                mgr.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)

@handles
class ShopBuyBulkResponse(responses.ShopBuyBulkResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.purchase_list:
            for item in self.purchase_list:
                mgr.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)

@handles
class RoomReceiveItemAllResponse(responses.RoomReceiveItemAllResponse):
    async def update(self, mgr: datamgr, request):
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)


@handles
class RoomMultiGiveGiftResponse(responses.RoomMultiGiveGiftResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gift_item_list:
            for item in self.user_gift_item_list:
                mgr.update_inventory(item)

        if self.level_info:
            for info in self.level_info.love:
                mgr.unit_love_data[info.chara_id].love_level = db.chara_love2love_level(info.total)
                mgr.unit_love_data[info.chara_id].chara_love = info.total


@handles
class RoomLevelUpStartResponse(responses.RoomLevelUpStartResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)


@handles
class QuestSkipResponse(responses.QuestSkipResponse):
    async def update(self, mgr: datamgr, request):
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        mgr.quest_dict[request.quest_id].daily_clear_count = self.daily_clear_count
        if self.user_info:
            mgr.stamina = self.user_info.user_stamina
            mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.level_info:
            mgr.team_level = self.level_info.team.start_level


@handles
class QuestSkipMultipleResponse(responses.QuestSkipMultipleResponse):
    async def update(self, mgr: datamgr, request):

        if self.quest_result_list:
            for result in self.quest_result_list:
                for res in result.quest_result:
                    for item in res.reward_list:
                        mgr.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.user_info:
            mgr.stamina = self.user_info.user_stamina
            mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        if self.user_gold:
            mgr.gold = self.user_gold


@handles
class QuestRecoverChallengeResponse(responses.QuestRecoverChallengeResponse):
    async def update(self, mgr: datamgr, request):
        mgr.jewel = self.user_jewel
        mgr.quest_dict[self.user_quest.quest_id].daily_recovery_count = self.user_quest.daily_recovery_count

@handles
class PresentReceiveAllResponse(responses.PresentReceiveAllResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time

@handles
class PresentReceiveSingleResponse(responses.PresentReceiveSingleResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time

@handles
class MissionIndexResponse(responses.MissionIndexResponse):
    async def update(self, mgr: datamgr, request):
        mgr.missions = self.missions

@handles
class MissionAcceptResponse(responses.MissionAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time
        if self.team_level:
            mgr.team_level = self.team_level


@handles
class LoadIndexResponse(responses.LoadIndexResponse):
    async def update(self, mgr: datamgr, request):
        mgr.uid = self.user_info.viewer_id
        mgr.user_name = self.user_info.user_name
        mgr.team_level = self.user_info.team_level
        mgr.jewel = self.user_jewel
        mgr.gold = self.user_gold
        if self.return_fes_info_list:
            mgr.return_fes_info_list = self.return_fes_info_list
        if self.user_redeem_unit:
            mgr.user_redeem_unit = {unit.unit_id: unit for unit in self.user_redeem_unit}
        if self.resident_info:
            mgr.resident_info = self.resident_info
        if self.bank_bought:
            mgr.user_gold_bank_info = self.user_gold_bank_info
        mgr.user_clan_battle_ex_equip_restriction = {i.serial_id: i for i in self.user_clan_battle_ex_equip_restriction} if self.user_clan_battle_ex_equip_restriction else {}
        mgr.clan_like_count = self.clan_like_count
        mgr.user_my_quest = self.user_my_quest
        mgr.cf = self.cf
        mgr.inventory = {}
        if self.item_list:
            for inv in self.item_list:
                mgr.update_inventory(inv)
        if self.material_list:
            for inv in self.material_list:
                mgr.update_inventory(inv)
        if self.user_equip:
            for inv in self.user_equip:
                mgr.update_inventory(inv)
        if self.user_ex_equip:
            mgr.ex_equips = {equip.serial_id: equip for equip in self.user_ex_equip}
        mgr.unit = {unit.id: unit for unit in self.unit_list} if self.unit_list else {}
        mgr.unit_love_data = {unit.chara_id: unit for unit in self.user_chara_info} if self.user_chara_info else {}
        mgr.growth_unit = {unit.unit_id: unit for unit in self.growth_unit_list} if self.growth_unit_list else {}
        mgr.deck_list = {deck.deck_number:deck for deck in self.deck_list} if self.deck_list else {}
        mgr.gacha_point = {gacha.exchange_id: gacha for gacha in self.gacha_point_info_list} if self.gacha_point_info_list else {}
        mgr.event_sub_story = {sub_story.event_id: sub_story for sub_story in self.event_sub_story} if self.event_sub_story else {}
        mgr.stamina = self.user_info.user_stamina
        mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        mgr.settings = self.ini_setting
        mgr.recover_stamina_exec_count = self.shop.recover_stamina.exec_count
        mgr.read_story_ids = self.read_story_ids
        mgr.unlock_story_ids = self.unlock_story_ids
        mgr.event_statuses = self.event_statuses
        mgr.tower_status = self.tower_status
        mgr.campaign_list = self.campaign_list
        mgr.dispatch_units = self.dispatch_units
        mgr.princess_knight_info = self.princess_knight_info

@handles
class HomeIndexResponse(responses.HomeIndexResponse):
    async def update(self, mgr: datamgr, request):
        mgr.finishedQuest |= set(([q.quest_id for q in self.quest_list if q.result_type > 0 and q.clear_flg == 3] if self.quest_list else []) + ([q.quest_id for q in self.shiori_quest_info.quest_list if q.result_type > 0 and q.clear_flg == 3] if self.shiori_quest_info and self.shiori_quest_info.quest_list else []))
        if self.cleared_byway_quest_id_list:
            mgr.cleared_byway_quest_id_set |= set(self.cleared_byway_quest_id_list)
        if self.user_clan:
            mgr.clan = self.user_clan.clan_id
        if self.user_clan and self.user_clan.donation_num:
            mgr.donation_num = self.user_clan.donation_num
        if self.dungeon_info:
            mgr.dungeon_area_id = self.dungeon_info.enter_area_id
            if self.dungeon_info.rest_challenge_count:
                for count in self.dungeon_info.rest_challenge_count:
                    mgr.dungeon_avaliable = count.count > 0
                    break
        if self.training_quest_count:
            mgr.training_quest_count = self.training_quest_count
        if self.training_quest_max_count:
            mgr.training_quest_max_count = self.training_quest_max_count
        if self.quest_list:
            mgr.quest_dict = {q.quest_id: q for q in self.quest_list}
        if self.missions:
            mgr.missions = self.missions
        shiori_dict = {q.quest_id: q for q in self.shiori_quest_info.quest_list} if self.shiori_quest_info and self.shiori_quest_info.quest_list else {}
        mgr.quest_dict.update(shiori_dict)

        if request.is_first:
            mgr.talent_quest_area_info = {
                v.talent_id: v for v in self.talent_quest_area_info
            }
            mgr.cleared_talent_quest_ids = {db.get_talent_id_from_quest_id(qid): qid for qid in self.cleared_talent_quest_id_list}

        mgr.ready = True


@handles
class HatsuneQuestTopResponse(responses.HatsuneQuestTopResponse):
    async def update(self, mgr: datamgr, request):
        mgr.hatsune_quest_dict[self.quest_list[0].quest_id // 1000] = {q.quest_id: q for q in self.quest_list}


@handles
class HatsuneQuestSkipResponse(responses.HatsuneQuestSkipResponse):
    async def update(self, mgr: datamgr, request: HatsuneQuestSkipRequest):
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        mgr.hatsune_quest_dict[request.event_id][request.quest_id].daily_clear_count = self.daily_clear_count
        mgr.stamina = self.user_info.user_stamina
        mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time

        if self.user_gold:
            mgr.gold = self.user_gold
        if self.level_info:
            mgr.team_level = self.level_info.team.start_level


@handles
class HatsuneMissionAcceptResponse(responses.HatsuneMissionAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)

        if self.team_level:
            mgr.team_level = self.team_level

        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time


@handles
class HatsuneBossBattleSkipResponse(responses.HatsuneBossBattleSkipResponse):
    async def update(self, mgr: datamgr, request):
        if self.crush_reward_list:
            for result in self.crush_reward_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold


@handles
class GrandArenaTimeRewardAcceptResponse(responses.GrandArenaTimeRewardAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            mgr.update_inventory(self.reward_info)


@handles
class GachaExecResponse(responses.GachaExecResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info_list:
            for item in self.reward_info_list:
                mgr.update_inventory(item)

        if self.bonus_reward_info:
            for item in vars(self.bonus_reward_info).values():
                if item is not None:
                    mgr.update_inventory(item)

        if self.prize_reward_info:
            for prize in vars(self.prize_reward_info).values():
                if prize is not None:
                    for item in prize.rewards:
                        mgr.update_inventory(item)

        if self.gacha_point_info:
            mgr.gacha_point[self.gacha_point_info.exchange_id] = self.gacha_point_info


@handles
class EventGachaExecResponse(responses.EventGachaExecResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info_list:
            for item in self.reward_info_list:
                mgr.update_inventory(item)


@handles
class EquipDonateResponse(responses.EquipDonateResponse):
    async def update(self, mgr: datamgr, request):
        mgr.donation_num = self.donation_num
        if self.donate_equip:
            mgr.update_inventory(self.donate_equip)
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)


@handles
class DungeonSkipResponse(responses.DungeonSkipResponse):
    async def update(self, mgr: datamgr, request):
        if self.skip_result_list:
            for result in self.skip_result_list:
                for reward in result.reward_list:
                    mgr.update_inventory(reward)

        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class SpecialDungeonEnterAreaResponse(responses.SpecialDungeonEnterAreaResponse):
    async def update(self, mgr: datamgr, request):
        if self.skip_result_list:
            for result in self.skip_result_list:
                for reward in result.reward_list:
                    mgr.update_inventory(reward)
        if self.total_floor_reward_info:
            for reward in self.total_floor_reward_info:
                mgr.update_inventory(reward)
        if self.mission_reward_info:
            for reward in self.mission_reward_info:
                mgr.update_inventory(reward)
        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class DungeonResetResponse(responses.DungeonResetResponse):
    async def update(self, mgr: datamgr, request):
        mgr.dungeon_area_id = 0
        type = self.dungeon_area[0].dungeon_type
        for count in self.rest_challenge_count:
            if count.dungeon_type == type:
                mgr.dungeon_avaliable = count.count > 0
                break

@handles
class DungeonEnterAreaResponse(responses.DungeonEnterAreaResponse):
    async def update(self, mgr: datamgr, request):
        mgr.dungeon_area_id = self.quest_id // 1000

@handles
class CloisterBattleSkipResponse(responses.CloisterBattleSkipResponse):
    async def update(self, mgr: datamgr, request):
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    mgr.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                mgr.update_inventory(item)
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)

        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class ClanLikeResponse(responses.ClanLikeResponse):
    async def update(self, mgr: datamgr, request):
        mgr.stamina = self.stamina_info.user_stamina
        mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time
        mgr.clan_like_count = 1

@handles
class ClanInfoResponse(responses.ClanInfoResponse):
    async def update(self, mgr: datamgr, request):
        mgr.clan = self.clan.detail.clan_id


@handles
class ClanCreateResponse(responses.ClanCreateResponse):
    async def update(self, mgr: datamgr, request):
        mgr.clan = self.clan_id

@handles
class ArenaTimeRewardAcceptResponse(responses.ArenaTimeRewardAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            mgr.update_inventory(self.reward_info)

@handles
class DeckUpdateResponse(responses.DeckUpdateResponse):
    async def update(self, mgr: datamgr, request: DeckUpdateRequest):
        deck = mgr.deck_list[ePartyType(request.deck_number)]
        deck.unit_id_1 = request.unit_id_1
        deck.unit_id_2 = request.unit_id_2
        deck.unit_id_3 = request.unit_id_3
        deck.unit_id_4 = request.unit_id_4
        deck.unit_id_5 = request.unit_id_5

@handles
class SeasonPassRewardAcceptResponse(responses.SeasonPassRewardAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for reward in self.rewards:
                mgr.update_inventory(reward)

@handles
class SeasonPassMissionAcceptResponse(responses.SeasonPassMissionAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for reward in self.rewards[::-1]:
                mgr.update_inventory(reward)
        if self.exchange_rewards:
            for reward in self.exchange_rewards:
                mgr.update_inventory(reward)

@handles
class SubStoryTprRegisterSuccessResponse(responses.SubStoryTprRegisterSuccessResponse):
    async def update(self, mgr: datamgr, request):
        for reward in self.reward_info or []:
            mgr.update_inventory(reward)
        if self.unlock_sub_story_info_list:
            for sub_story in self.unlock_sub_story_info_list:
                event_id = db.tpr_story_data[sub_story.sub_story_id].original_event_id
                if event_id not in mgr.event_sub_story:
                    mgr.event_sub_story[event_id] = datamgr.EventSubStoryData(event_id=event_id, sub_story_info_list=[])
                find_one = next((s for s in mgr.event_sub_story[event_id].sub_story_info_list if s.sub_story_id == sub_story.sub_story_id), None)
                if find_one:
                    find_one.status = sub_story.status
                else:
                    mgr.event_sub_story[event_id].sub_story_info_list.append(sub_story)

@handles
class SubStoryTprReadStoryResponse(responses.SubStoryTprReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        sub_story_id = request.sub_story_id
        event_id = db.tpr_story_data[sub_story_id].original_event_id
        sub_story_info = next((s for s in mgr.event_sub_story[event_id].sub_story_info_list if s.sub_story_id == sub_story_id), None)
        if sub_story_info:
            sub_story_info.status = eEventSubStoryStatus.READED
        else:
            mgr.event_sub_story[event_id].sub_story_info_list.append(
                datamgr.EventSubStoryInfo(
                    sub_story_id=sub_story_id,
                    status=eEventSubStoryStatus.READED
                )
            )

@handles
class SubStoryApgReadStoryResponse(responses.SubStoryApgReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)
        if self.user_jewel:
            mgr.jewel = self.user_jewel
        if self.special_reward_list:
            for reward in self.special_reward_list:
                mgr.update_inventory(reward)

@handles
class SubStoryAisReadStoryResponse(responses.SubStoryAisReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryNydReadStoryResponse(responses.SubStoryNydReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)
        if self.special_reward_list:
            for reward in self.special_reward_list:
                mgr.update_inventory(reward)

@handles
class SubStoryXacReadStoryResponse(responses.SubStoryXacReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryAsbReadStoryResponse(responses.SubStoryAsbReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryWtmReadStoryResponse(responses.SubStoryWtmReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryWtsReadStoryResponse(responses.SubStoryWtsReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryBmyReadStoryResponse(responses.SubStoryBmyReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryAisConfirmResponse(responses.SubStoryAisConfirmResponse):
    async def update(self, mgr: datamgr, request):
        for sub_story in mgr.event_sub_story[10136].sub_story_info_list:
            if sub_story.status == eEventSubStoryStatus.ADDED:
                sub_story.status = eEventSubStoryStatus.UNREAD
        for sub_story in mgr.event_sub_story[10137].sub_story_info_list:
            if sub_story.status == eEventSubStoryStatus.ADDED:
                sub_story.status = eEventSubStoryStatus.UNREAD

@handles
class SubStorySkeConfirmResponse(responses.SubStorySkeConfirmResponse):
    async def update(self, mgr: datamgr, request):
        for sub_story in mgr.event_sub_story[10058].sub_story_info_list:
            if sub_story.status == eEventSubStoryStatus.ADDED:
                sub_story.status = eEventSubStoryStatus.UNREAD
        for sub_story in mgr.event_sub_story[10059].sub_story_info_list:
            if sub_story.status == eEventSubStoryStatus.ADDED:
                sub_story.status = eEventSubStoryStatus.UNREAD

@handles
class SubStoryXehReadStoryResponse(responses.SubStoryXehReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryDsbReadStoryResponse(responses.SubStoryDsbReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryLtoReadStoryResponse(responses.SubStoryLtoReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryMhpReadStoryResponse(responses.SubStoryMhpReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryMmeReadStoryResponse(responses.SubStoryMmeReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)


class SubStoryWonReadStoryResponse(responses.SubStoryWonReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)
@handles
class SubStoryNopReadStoryResponse(responses.SubStoryNopReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)


@handles
class SubStoryDvsReadStoryResponse(responses.SubStoryDvsReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStoryYsnReadStoryResponse(responses.SubStoryYsnReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.reward_info:
            for reward in self.reward_info:
                mgr.update_inventory(reward)

@handles
class SubStorySvdReadStoryResponse(responses.SubStorySvdReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.special_reward_list:
            for reward in self.special_reward_list:
                mgr.update_inventory(reward)


@handles
class SubStoryLsvReadStoryResponse(responses.SubStoryLsvReadStoryResponse):
    async def update(self, mgr: datamgr, request):
        if self.special_reward_list:
            for reward in self.special_reward_list:
                mgr.update_inventory(reward)

@handles
class UnitCraftEquipResponse(responses.UnitCraftEquipResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.equip_list:
            for equip in self.equip_list:
                mgr.update_inventory(equip)


@handles
class UnitMultiPromotionResponse(responses.UnitMultiPromotionResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.equip_list:
            for equip in self.equip_list:
                mgr.update_inventory(equip)
        if self.refund_items:
            for item in self.refund_items:
                mgr.update_inventory(item)

@handles
class ShopWithdrawGoldFromBankResponse(responses.ShopWithdrawGoldFromBankResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.user_bank_gold_info:
            mgr.user_gold_bank_info = self.user_bank_gold_info

@handles
class UseExpItemResponse(responses.UseExpItemResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        mgr.unit[self.unit_data.id] = self.unit_data

@handles
class EquipEnhanceResponse(responses.EquipEnhanceResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold


@handles
class UniqueEquip2MultiEnhanceRequest(responses.UniqueEquip2MultiEnhanceResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class UniqueEquipEnhanceResponse(responses.UniqueEquipEnhanceResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class UniqueEquipRankupResponse(responses.UniqueEquipRankupResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.equip_list:
            for equip in self.equip_list:
                mgr.update_inventory(equip)

@handles
class EquipmentFreeMultiEnhanceUniqueResponse(responses.EquipmentFreeMultiEnhanceUniqueResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.equip_list:
            for equip in self.equip_list:
                mgr.update_inventory(equip)

@handles
class UniqueEquipCraftResponse(responses.UniqueEquipCraftResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.equip_list:
            for equip in self.equip_list:
                mgr.update_inventory(equip)
        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class UniqueEquipMultiEnhanceResponse(responses.UniqueEquipMultiEnhanceResponse):
    async def update(self, mgr: datamgr, request):
        mgr.unit[self.unit_data.id] = self.unit_data
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.equip_list:
            for equip in self.equip_list:
                mgr.update_inventory(equip)
        if self.user_gold:
            mgr.gold = self.user_gold

@handles
class UnitSetGrowthItemUniqueResponse(responses.UnitSetGrowthItemUniqueResponse):
    async def update(self, mgr: datamgr, request):
        if self.unit_data:
            mgr.unit[self.unit_data.id] = self.unit_data
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.growth_parameter_list:
            mgr.growth_unit.update(
                    {request.unit_id:
                         GrowthInfo(unit_id=request.unit_id, growth_parameter_list=self.growth_parameter_list)
                     })

@handles
class ChangeRarityResponse(responses.ChangeRarityResponse):
    async def update(self, mgr: datamgr, request):
        if self.unit_data_list:
            for unit in self.unit_data_list:
                mgr.unit[unit.id] = unit

@handles
class TravelReceiveAllResponse(responses.TravelReceiveAllResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        for result in self.travel_result:
            for item in result.reward_list:
                mgr.update_inventory(item)

@handles
class TravelReceiveResponse(responses.TravelReceiveResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        for result in self.travel_result:
            for item in result.reward_list:
                mgr.update_inventory(item)

@handles
class TravelRetireResponse(responses.TravelRetireResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.travel_result:
            for result in self.travel_result:
                for item in result.reward_list:
                    mgr.update_inventory(item)

@handles
class TravelDecreaseTimeResponse(responses.TravelDecreaseTimeResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.user_jewel:
            mgr.jewel = self.user_jewel

@handles
class TravelReceiveTopEventRewardResponse(responses.TravelReceiveTopEventRewardResponse):
    async def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.user_jewel:
            mgr.jewel = self.user_jewel
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time
        for item in self.reward_list:
            mgr.update_inventory(item)

@handles
class RedeemUnitRegisterItemResponse(responses.RedeemUnitRegisterItemResponse):
    async def update(self, mgr: datamgr, request):
        for item in request.item_list:
            if item.id == db.zmana[1]:
                mana = min(mgr.gold.gold_id_free, item.count)
                mgr.gold.gold_id_free -= mana
                item.count -= mana
                mgr.gold.gold_id_pay -= item.count
            else:
                mgr.inventory[(eInventoryType.Item, item.id)] -= item.count

@handles
class RedeemUnitUnlockResponse(responses.RedeemUnitUnlockResponse):
    async def update(self, mgr: datamgr, request):
        if self.unit_data:
            mgr.unit[self.unit_data.id] = self.unit_data

@handles
class ItemRecycleExtraEquipResponse(responses.ItemRecycleExtraEquipResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if request.consume_ex_serial_id_list:
            for serial_id in request.consume_ex_serial_id_list:
                mgr.ex_equips.pop(serial_id)

@handles
class SupportUnitChangeSettingResponse(responses.SupportUnitChangeSettingResponse):
    async def update(self, mgr: datamgr, request):
        if self.support_count_bonus:
            for bonus in self.support_count_bonus:
                mgr.update_inventory(bonus)
        if self.support_time_bonus:
            for bonus in self.support_time_bonus:
                mgr.update_inventory(bonus)

@handles
class ShioriMissionAcceptResponse(responses.ShioriMissionAcceptResponse):
    async def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)

        if self.team_level:
            mgr.team_level = self.team_level

        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
            mgr.stamina_full_recovery_time = self.stamina_info.stamina_full_recovery_time

@handles
class GachaExchangePointResponse(responses.GachaExchangePointResponse):
    async def update(self, mgr: datamgr, request):
        if self.gacha_point_info:
            mgr.gacha_point[self.gacha_point_info.exchange_id] = self.gacha_point_info
        if self.reward_info_list:
            for item in self.reward_info_list:
                mgr.update_inventory(item)

@handles
class UnitEquipExResponse(responses.UnitEquipExResponse):
    async def update(self, mgr: datamgr, request):
        for unit_slot_info in request.ex_equip_change_unit_list:
            for ex_equip in unit_slot_info.ex_equip_slot or []:
                mgr.unit[unit_slot_info.unit_id].ex_equip_slot[ex_equip.slot - 1].serial_id = ex_equip.serial_id

            for ex_equip in unit_slot_info.cb_ex_equip_slot or []:
                mgr.unit[unit_slot_info.unit_id].cb_ex_equip_slot[ex_equip.slot - 1].serial_id = ex_equip.serial_id

@handles
class EquipmentRankupExResponse(responses.EquipmentRankupExResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold
        for ex_serial_id in request.consume_ex_serial_id_list:
            mgr.ex_equips.pop(ex_serial_id, None)
        mgr.ex_equips[request.serial_id].rank = request.after_rank

@handles
class EquipmentEnhanceExResponse(responses.EquipmentEnhanceExResponse):
    async def update(self, mgr: datamgr, request):
        if self.item_list:
            for item in self.item_list:
                mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold
        for ex_serial_id in request.consume_ex_serial_id_list:
            mgr.ex_equips.pop(ex_serial_id, None)
        mgr.ex_equips[request.serial_id].enhancement_pt = request.after_enhancement_pt


@handles
class UnitMultiEvolutionResponse(responses.UnitMultiEvolutionResponse):
    async def update(self, mgr: datamgr, request: UnitMultiEvolutionRequest):
        for u in self.unit_data_list or []:
            mgr.unit[u.id] = u
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)


@handles
class TalentQuestSkipResponse(responses.TalentQuestSkipResponse):
    async def update(self, mgr: datamgr, request: TalentQuestSkipRequest):
        for result in self.quest_result_list or []:
            for item in result.reward_list:
                mgr.update_inventory(item)
        for item in self.bonus_reward_list or []:
            mgr.update_inventory(item)
        for item in self.item_list or []:
            mgr.update_inventory(item)
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.level_info:
            mgr.team_level = self.level_info.team.start_level
        if self.user_info:
            mgr.stamina = self.user_info.user_stamina
            mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time
        for info in self.talent_quest_area_info:
            mgr.talent_quest_area_info[info.talent_id] = info
        mgr.stamina = self.user_info.user_stamina
        mgr.stamina_full_recovery_time = self.user_info.stamina_full_recovery_time


@handles
class TalentQuestRecoverChallengeResponse(
    responses.TalentQuestRecoverChallengeResponse
):
    async def update(self, mgr: datamgr, request: TalentQuestRecoverChallengeRequest):
        mgr.jewel = self.user_jewel
        mgr.talent_quest_area_info[
            self.user_talent_quest.talent_id
        ].daily_recovery_count = self.user_talent_quest.daily_recovery_count


# 菜 就别玩
# def custom_dict(self, *args, **kwargs):
#     original_dict = super(TravelStartRequest, self).dict(*args, **kwargs)
#     if self.action_type is not None:
#         original_dict['action_type'] = {"value__": self.action_type.value}
#     return original_dict
# TravelStartRequest.dict = custom_dict

HatsuneTopResponse.__annotations__['event_status'] = HatsuneEventStatus
HatsuneTopResponse.__fields__['event_status'].type_ = Optional[HatsuneEventStatus]
HatsuneTopResponse.__fields__['event_status'].outer_type_ = Optional[HatsuneEventStatus]
HatsuneTopResponse.__fields__['event_status'].annotation = HatsuneEventStatus
HatsuneTopResponse.__fields__['event_status'].shape = 1 # singleton

DungeonUnit.__annotations__['skill_limit_counter'] = int
DungeonUnit.__fields__['skill_limit_counter'].type_ = Optional[int]
DungeonUnit.__fields__['skill_limit_counter'].outer_type_ = Optional[int]
DungeonUnit.__fields__['skill_limit_counter'].validators = [make_generic_validator(int_validator)] # singleton
DungeonUnit.__fields__['skill_limit_counter'].annotation = int
DungeonUnit.__fields__['skill_limit_counter'].sub_fields = None 
DungeonUnit.__fields__['skill_limit_counter'].shape = 1 # singleton

CaravanCoinShopData.__annotations__['season_id'] = Optional[int]
field = ModelField.infer(
    name='season_id',
    value=None,
    annotation=int,
    class_validators=None,
    config=CaravanCoinShopData.__config__,
)
CaravanCoinShopData.__fields__['season_id'] = field
setattr(CaravanCoinShopData, 'season_id', None)

ExtraEquipSlot.__annotations__['slot'] = Optional[int]
field = ModelField.infer(
    name='slot',
    value=None,
    annotation=int,
    class_validators=None,
    config=ExtraEquipSlot.__config__,
)
ExtraEquipSlot.__fields__['slot'] = field
setattr(ExtraEquipSlot, 'slot', None)

ProfileQuestInfo.__annotations__['talent_quest'] = Optional[List[TalentQuestData]]
field = ModelField.infer(
    name='talent_quest',
    value=None,
    annotation=List[TalentQuestData],
    class_validators=None,
    config=ProfileQuestInfo.__config__,
)
ProfileQuestInfo.__fields__['talent_quest'] = field
setattr(ProfileQuestInfo, 'talent_quest', None)
