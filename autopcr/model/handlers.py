from . import responses
from .common import *
from ..core.datamgr import datamgr

def handles(cls):
    cls.__base__.update = cls.update
    return None

@handles
class ShioriQuestSkipResponse(responses.ShioriQuestSkipResponse):
    def update(self, mgr: datamgr, request):
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
        mgr.quest_dict[request.quest_id].daily_clear_count = self.daily_clear_count

@handles
class TrainingQuestSkipResponse(responses.TrainingQuestSkipResponse):
    def update(self, mgr: datamgr, request):
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


@handles
class TrainingQuestFinishResponse(responses.TrainingQuestFinishResponse):
    def update(self, mgr: datamgr, request):
        mgr.training_quest_count = self.quest_challenge_count

@handles
class StoryViewingResponse(responses.StoryViewingResponse):
    def update(self, mgr: datamgr, request):
        if self.reward_info:
            for item in self.reward_info:
                mgr.update_inventory(item)


@handles
class ShopResetResponse(responses.ShopResetResponse):
    def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.user_jewel:
            mgr.jewel = self.user_jewel


@handles
class ShopRecoverStaminaResponse(responses.ShopRecoverStaminaResponse):
    def update(self, mgr: datamgr, request):
        mgr.jewel = self.user_jewel
        mgr.stamina = self.user_info.user_stamina
        mgr.recover_stamina_exec_count = self.recover_stamina.exec_count


@handles
class ShopBuyResponse(responses.ShopBuyResponse):
    def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)
        if self.user_jewel:
            mgr.jewel = self.user_jewel


@handles
class ShopBuyMultipleResponse(responses.ShopBuyMultipleResponse):
    def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)


@handles
class RoomReceiveItemAllResponse(responses.RoomReceiveItemAllResponse):
    def update(self, mgr: datamgr, request):
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina
        if self.reward_list:
            for item in self.reward_list:
                mgr.update_inventory(item)


@handles
class RoomMultiGiveGiftResponse(responses.RoomMultiGiveGiftResponse):
    def update(self, mgr: datamgr, request):
        if self.user_gift_item_list:
            for item in self.user_gift_item_list:
                mgr.update_inventory(item)

        if self.level_info:
            for info in self.level_info.love:
                mgr.unit_love[info.chara_id].love_level = info.current_level
                mgr.unit_love[info.chara_id].chara_love = info.total


@handles
class RoomLevelUpStartResponse(responses.RoomLevelUpStartResponse):
    def update(self, mgr: datamgr, request):
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.item_data:
            for item in self.item_data:
                mgr.update_inventory(item)


@handles
class QuestSkipResponse(responses.QuestSkipResponse):
    def update(self, mgr: datamgr, request):
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
        if self.user_gold:
            mgr.gold = self.user_gold
        if self.level_info:
            mgr.team_level = self.level_info.team.start_level


@handles
class QuestSkipMultipleResponse(responses.QuestSkipMultipleResponse):
    def update(self, mgr: datamgr, request):

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
        if self.user_info:
            mgr.stamina = self.user_info.user_stamina
        if self.user_gold:
            mgr.gold = self.user_gold


@handles
class QuestRecoverChallengeResponse(responses.QuestRecoverChallengeResponse):
    def update(self, mgr: datamgr, request):
        mgr.jewel = self.user_jewel
        mgr.quest_dict[self.user_quest.quest_id].daily_recovery_count = self.user_quest.daily_recovery_count

@handles
class PresentReceiveAllResponse(responses.PresentReceiveAllResponse):
    def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina


@handles
class MissionAcceptResponse(responses.MissionAcceptResponse):
    def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina


@handles
class LoadIndexResponse(responses.LoadIndexResponse):
    def update(self, mgr: datamgr, request):
        mgr.name = self.user_info.user_name
        mgr.team_level = self.user_info.team_level
        mgr.jewel = self.user_jewel
        mgr.gold = self.user_gold
        mgr.clan_like_count = self.clan_like_count
        mgr.user_my_quest = self.user_my_quest
        mgr.clear_inventory()
        mgr.cf = self.cf
        if self.item_list:
            for inv in self.item_list:
                mgr.update_inventory(inv)
        if self.material_list:
            for inv in self.material_list:
                mgr.update_inventory(inv)
        if self.user_equip:
            for inv in self.user_equip:
                mgr.update_inventory(inv)
        if self.unit_list:
            mgr.unit = {unit.id: unit for unit in self.unit_list}
        if self.user_chara_info:
            mgr.unit_love = {unit.chara_id: unit for unit in self.user_chara_info}
        mgr.stamina = self.user_info.user_stamina
        mgr.settings = self.ini_setting
        mgr.recover_stamina_exec_count = self.shop.recover_stamina.exec_count
        mgr.read_story_ids = self.read_story_ids
        mgr.unlock_story_ids = self.unlock_story_ids
        mgr.event_statuses = self.event_statuses
        mgr.tower_status = self.tower_status
        mgr.deck_list = {deck.deck_number:deck for deck in self.deck_list}
        mgr.campaign_list = self.campaign_list


@handles
class HomeIndexResponse(responses.HomeIndexResponse):
    def update(self, mgr: datamgr, request):
        mgr.finishedQuest = set([q.quest_id for q in self.quest_list if q.result_type > 0] + [q.quest_id for q in self.shiori_quest_info.quest_list if q.result_type > 0] if self.shiori_quest_info else [])
        mgr.clan = self.user_clan.clan_id
        mgr.donation_num = self.user_clan.donation_num
        mgr.dungeon_area_id = self.dungeon_info.enter_area_id
        mgr.training_quest_count = self.training_quest_count
        mgr.training_quest_max_count = self.training_quest_max_count
        mgr.quest_dict = {q.quest_id: q for q in self.quest_list}
        shiori_dict = {q.quest_id: q for q in self.shiori_quest_info.quest_list} if self.shiori_quest_info else {}
        mgr.quest_dict.update(shiori_dict)

        if self.dungeon_info.dungeon_area:
            type = self.dungeon_info.dungeon_area[0].dungeon_type
            for count in self.dungeon_info.rest_challenge_count:
                if count.dungeon_type == type:
                    mgr.dungeon_avaliable = count.count > 0
                    break


@handles
class HatsuneQuestTopResponse(responses.HatsuneQuestTopResponse):
    def update(self, mgr: datamgr, request):
        mgr.hatsune_quest_dict[self.quest_list[0].quest_id // 1000] = {q.quest_id: q for q in self.quest_list}


@handles
class HatsuneQuestSkipResponse(responses.HatsuneQuestSkipResponse):
    def update(self, mgr: datamgr, request):
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

        if self.user_gold:
            mgr.gold = self.user_gold
        if self.level_info:
            mgr.team_level = self.level_info.team.start_level


@handles
class HatsuneMissionAcceptResponse(responses.HatsuneMissionAcceptResponse):
    def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)

        if self.team_level:
            mgr.team_level = self.team_level

        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina


@handles
class HatsuneBossBattleSkipResponse(responses.HatsuneBossBattleSkipResponse):
    def update(self, mgr: datamgr, request):
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
    def update(self, mgr: datamgr, request):
        if self.reward_info:
            mgr.update_inventory(self.reward_info)


@handles
class GachaExecResponse(responses.GachaExecResponse):
    def update(self, mgr: datamgr, request):
        if self.reward_info_list:
            for item in self.reward_info_list:
                mgr.update_inventory(item)

        if self.bonus_reward_info:
            if self.bonus_reward_info.bonus1:
                mgr.update_inventory(self.bonus_reward_info.bonus1)
            if self.bonus_reward_info.bonus2:
                mgr.update_inventory(self.bonus_reward_info.bonus2)
            if self.bonus_reward_info.bonus3:
                mgr.update_inventory(self.bonus_reward_info.bonus3)
            if self.bonus_reward_info.bonus4:
                mgr.update_inventory(self.bonus_reward_info.bonus4)
            if self.bonus_reward_info.bonus5:
                mgr.update_inventory(self.bonus_reward_info.bonus5)
            if self.bonus_reward_info.bonus6:
                mgr.update_inventory(self.bonus_reward_info.bonus6)
            if self.bonus_reward_info.bonus7:
                mgr.update_inventory(self.bonus_reward_info.bonus7)
            if self.bonus_reward_info.bonus8:
                mgr.update_inventory(self.bonus_reward_info.bonus8)
            if self.bonus_reward_info.bonus9:
                mgr.update_inventory(self.bonus_reward_info.bonus9)
            if self.bonus_reward_info.bonus10:
                mgr.update_inventory(self.bonus_reward_info.bonus10)

        # if self.user_gold:
        #     mgr.gold = self.user_gold
        # bonus not set


@handles
class EventGachaExecResponse(responses.EventGachaExecResponse):
    def update(self, mgr: datamgr, request):
        if self.reward_info_list:
            for item in self.reward_info_list:
                mgr.update_inventory(item)


@handles
class EquipDonateResponse(responses.EquipDonateResponse):
    def update(self, mgr: datamgr, request):
        mgr.donation_num = self.donation_num
        if self.donate_equip:
            mgr.update_inventory(self.donate_equip)
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)


@handles
class DungeonSkipResponse(responses.DungeonSkipResponse):
    def update(self, mgr: datamgr, request):
        if self.skip_result_list:
            for result in self.skip_result_list:
                for reward in result.reward_list:
                    mgr.update_inventory(reward)

        if self.user_gold:
            mgr.gold = self.user_gold


@handles
class DungeonResetResponse(responses.DungeonResetResponse):
    def update(self, mgr: datamgr, request):
        mgr.dungeon_area_id = 0
        type = self.dungeon_area[0].dungeon_type
        for count in self.rest_challenge_count:
            if count.dungeon_type == type:
                mgr.dungeon_avaliable = count.count > 0
                break


@handles
class DungeonEnterAreaResponse(responses.DungeonEnterAreaResponse):
    def update(self, mgr: datamgr, request):
        mgr.dungeon_area_id = self.quest_id // 1000


@handles
class CloisterBattleSkipResponse(responses.CloisterBattleSkipResponse):
    def update(self, mgr: datamgr, request):
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
    def update(self, mgr: datamgr, request):
        mgr.stamina = self.stamina_info.user_stamina
        mgr.clan_like_count = 1

@handles
class ClanInfoResponse(responses.ClanInfoResponse):
    def update(self, mgr: datamgr, request):
        mgr.clan = self.clan.detail.clan_id


@handles
class ClanCreateResponse(responses.ClanCreateResponse):
    def update(self, mgr: datamgr, request):
        mgr.clan = self.clan_id


@handles
class ArenaTimeRewardAcceptResponse(responses.ArenaTimeRewardAcceptResponse):
    def update(self, mgr: datamgr, request):
        if self.reward_info:
            mgr.update_inventory(self.reward_info)

@handles
class DeckUpdateResponse(responses.DeckUpdateResponse):
    def update(self, mgr: datamgr, request):
        deck = mgr.deck_list[ePartyType(request.deck_number)]
        deck.unit_id1 = request.unit_id_1
        deck.unit_id2 = request.unit_id_2
        deck.unit_id3 = request.unit_id_3
        deck.unit_id4 = request.unit_id_4
        deck.unit_id5 = request.unit_id_5
