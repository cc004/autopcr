from typing import List
from . import responses
from ..core.datamgr import datamgr

def handles(cls):
    cls.__base__.update = cls.update
    return None

@handles
class ClanCreateResponse(responses.ClanCreateResponse):
    def update(self, mgr: datamgr, request):
        mgr.clan = self.clan_id

@handles
class ClanInfoResponse(responses.ClanInfoResponse):
    def update(self, mgr: datamgr, request):
        mgr.clan = self.clan.detail.clan_id

@handles
class ClanLikeResponse(responses.ClanLikeResponse):
    def update(self, mgr: datamgr, request):
        mgr.stamina = self.stamina_info.user_stamina
        mgr.clan_like_count = 0

@handles
class DungeonEnterAreaResponse(responses.DungeonEnterAreaResponse):
    def update(self, mgr: datamgr, request):
        mgr.dungeon_area_id = self.quest_id / 1000

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
class EquipDonateResponse(responses.EquipDonateResponse):
    def update(self, mgr: datamgr, request):
        mgr.donation_num = self.donation_num
        if self.donate_equip:
            mgr.update_inventory(self.donate_equip)
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)

@handles
class HomeIndexResponse(responses.HomeIndexResponse):
    def update(self, mgr: datamgr, request):
        mgr.finishedQuest = [q.quest_id for q in self.quest_list if q.result_type > 0]
        mgr.clan = self.user_clan.clan_id
        mgr.donation_num = self.user_clan.donation_num
        mgr.dungeon_area_id = self.dungeon_info.enter_area_id
        mgr.training_quest_count = self.training_quest_count
        mgr.quest_dict = {q.quest_id: q for q in self.quest_list}
        if self.dungeon_info.dungeon_area:
            type = self.dungeon_info.dungeon_area[0].dungeon_type
            for count in self.dungeon_info.rest_challenge_count:
                if count.dungeon_type == type:
                    mgr.dungeon_avaliable = count.count > 0
                    break

@handles
class LoadIndexResponse(responses.LoadIndexResponse):
    def update(self, mgr: datamgr, request):
        mgr.name = self.user_info.user_name
        mgr.team_level = self.user_info.team_level
        mgr.jewel = self.user_jewel
        mgr.clan_like_count = self.clan_like_count
        mgr.user_my_quest = self.user_my_quest
        mgr.clear_inventory()
        if self.item_list:
            for inv in self.item_list:
                mgr.update_inventory(inv)
        if self.material_list:
            for inv in self.material_list:
                mgr.update_inventory(inv)
        if self.user_equip:
            for inv in self.user_equip:
                mgr.update_inventory(inv)
        mgr.stamina = self.user_info.user_stamina
        mgr.settings = self.ini_setting
        mgr.recover_stamina_exec_count = self.shop.recover_stamina.exec_count

@handles
class MissionAcceptResponse(responses.MissionAcceptResponse):
    def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        mgr.stamina = self.stamina_info.user_stamina

@handles
class PresentReceiveAllResponse(responses.PresentReceiveAllResponse):
    def update(self, mgr: datamgr, request):
        if self.rewards:
            for item in self.rewards:
                mgr.update_inventory(item)
        mgr.stamina = self.stamina_info.user_stamina

@handles
class QuestRecoverChallengeResponse(responses.QuestRecoverChallengeResponse):
    def update(self, mgr: datamgr, request):
        mgr.jewel = self.user_jewel
        mgr.quest_dict[self.user_quest.quest_id].daily_recovery_count = self.user_quest.daily_recovery_count

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
        mgr.stamina = self.user_info.user_stamina

@handles
class RoomReceiveItemAllResponse(responses.RoomReceiveItemAllResponse):
    def update(self, mgr: datamgr, request):
        if self.stamina_info:
            mgr.stamina = self.stamina_info.user_stamina

@handles
class ShopRecoverStaminaResponse(responses.ShopRecoverStaminaResponse):
    def update(self, mgr: datamgr, request):
        mgr.jewel = self.user_jewel
        mgr.stamina = self.user_info.user_stamina
        mgr.recover_stamina_exec_count = self.recover_stamina.exec_count

@handles
class TrainingQuestFinishResponse(responses.TrainingQuestFinishResponse):
    def update(self, mgr: datamgr, request):
        mgr.training_quest_count = self.quest_challenge_count
