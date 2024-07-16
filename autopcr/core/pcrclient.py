from ..model.models import *
from .apiclient import apiclient
from .sessionmgr import sessionmgr
from .misc import errorhandler
from .datamgr import datamgr
from ..db.database import db
from typing import Tuple, Union
import typing

class pcrclient(apiclient):
    def __init__(self, platform, *args, **kwargs):
        super().__init__(platform)
        self.keys = {}
        self.data = datamgr()
        self.session = sessionmgr(platform, *args, **kwargs)
        self.register(errorhandler())
        self.register(self.data)
        self.register(self.session)
    
    @property
    def name(self) -> str:
        return self.data.name

    @property
    def logged(self):
        return self.session._logged

    async def login(self):
        await self.request(None)

    async def logout(self):
        await self.session.clear_session()

    async def season_ticket_new_index(self, season_id: int):
        req = SeasonPassIndexRequest()
        req.season_id = season_id
        return await self.request(req)

    async def season_ticket_new_reward(self, season_id: int, level: int, index: int):
        req = SeasonPassRewardAcceptRequest()
        req.season_id = season_id
        req.level = level
        req.index = index
        return await self.request(req)

    async def season_ticket_new_accept(self, season_id: int, mission_id: int):
        req = SeasonPassMissionAcceptRequest()
        req.season_id = season_id
        req.mission_id = mission_id
        return await self.request(req)

    async def deck_update(self, deck_number: int, units: List[int], sorted: bool = False):
        req = DeckUpdateRequest()
        req.deck_number = deck_number
        cnt = len(units)
        if not sorted:
            units = db.deck_sort_unit(units)
        for i in range(1, 6):
            setattr(req, f"unit_id_{i}",units[i - 1] if i <= cnt else 0) 
        return await self.request(req)

    async def deck_update_list(self, deck_list: List):
        req = DeckUpdateListRequest()
        req.deck_list = deck_list
        return await self.request(req)

    async def unit_change_rarity(self, change_rarity_unit_list: List[ChangeRarityUnit]):
        req = ChangeRarityRequest()
        req.change_rarity_unit_list = change_rarity_unit_list
        return await self.request(req)

    async def skill_level_up(self, unit_id: int, skill_levelup_list: List[SkillLevelUpDetail]):
        req = SkillLevelUpRequest()
        req.unit_id = unit_id
        req.skill_levelup_list = skill_levelup_list
        return await self.request(req)

    async def unit_free_level_up(self, unit_id: int, after_level: int):
        req = UnitFreeLevelUpRequest()
        req.unit_id = unit_id
        req.after_level = after_level
        return await self.request(req)

    async def multi_promotion(self, unit_id: int, target_promotion_level: int, equip_recipe_list: List[typing.Counter[ItemType]]):
        req = UnitMultiPromotionRequest()
        req.unit_id = unit_id
        req.item_list = []
        req.target_promotion_level = target_promotion_level
        req.equip_recipe_list = [RequiredMaterialList(
                equip_list=[UserEquipParameterIdCount(id=item[1], count=count) for item, count in equips.items()]
            ) for equips in equip_recipe_list]
        return await self.request(req)

    async def unit_free_promotion(self, unit_id: int, target_promotion_level: int):
        req = UnitFreePromotionRequest()
        req.unit_id = unit_id
        req.target_promotion_level = target_promotion_level
        return await self.request(req)

    async def unit_free_equip(self, unit_id: int, equip_slot_num_list: List[int]):
        req = UnitFreeEquipRequest()
        req.unit_id = unit_id
        req.equip_slot_num_list = equip_slot_num_list
        return await self.request(req)

    async def unit_craft_equip(self, unit_id: int, equip_slot_num: int, equip_recipe_dict: typing.Counter[ItemType]):
        req = UnitCraftEquipRequest()
        req.unit_id = unit_id
        req.equip_slot_num = equip_slot_num
        req.equip_recipe_list = [UserEquipParameterIdCount(id=item[1], count=count) for item, count in equip_recipe_dict.items()]
        req.item_list = []
        return await self.request(req)

    async def unit_level_up(self, unit_id: int, item: typing.Counter[ItemType]):
        req = UseExpItemRequest()
        req.unit_id = unit_id
        req.item_list = [ItemInfo(item_id=item[1], item_num=count, current_num=self.data.get_inventory(item)) for item, count in item.items()]
        return await self.request(req)

    async def equipment_enhance(self, unit_id: int, equip_slot_num: int, current_enhancement_pt: int, items: typing.Counter[ItemType]):
        req = EquipEnhanceRequest()
        req.unit_id = unit_id
        req.equip_slot_num = equip_slot_num
        req.current_enhancement_pt = current_enhancement_pt
        req.item_list = [InventoryInfoPost(id=item[1], type=eInventoryType.Item, count=count) for item, count in items.items()]
        return await self.request(req)

    async def equipment_free_enhance(self, unit_id: int, equip_slot_num: int, after_equip_level: int):
        req = EquipmentFreeEnhanceRequest()
        req.unit_id = unit_id
        req.equip_slot_num = equip_slot_num
        req.after_equip_level = after_equip_level
        return await self.request(req)

    async def get_clan_battle_top(self, clan_id: int, is_first: int, current_clan_battle_coin: int):
        req = ClanBattleTopRequest()
        req.clan_id = clan_id
        req.is_first = is_first
        req.current_clan_battle_coin = current_clan_battle_coin
        return await self.request(req)

    async def get_clan_battle_support_unit_list(self, clan_id: int):
        req = ClanBattleSupportUnitList2Request()
        req.clan_id = clan_id
        return await self.request(req)

    async def grand_arena_rank(self, limit: int, page: int):
        req = GrandArenaRankingRequest()
        req.limit = limit
        req.page = page
        return await self.request(req)

    async def arena_rank(self, limit: int, page: int):
        req = ArenaRankingRequest()
        req.limit = limit
        req.page = page
        return await self.request(req)

    async def arena_apply(self, battle_viewer_id: int, opponent_rank: int):
        req = ArenaApplyRequest()
        req.battle_viewer_id = battle_viewer_id
        req.opponent_rank = opponent_rank
        return await self.request(req)

    async def arena_start(self, token: str, battle_viewer_id: int, remain_battle_number: int, disable_skin: int):
        req = ArenaStartRequest()
        req.token = token
        req.battle_viewer_id = battle_viewer_id
        req.remain_battle_number = remain_battle_number
        req.disable_skin = disable_skin
        return await self.request(req)

    async def grand_arena_apply(self, battle_viewer_id: int, opponent_rank: int):
        req = GrandArenaApplyRequest()
        req.battle_viewer_id = battle_viewer_id
        req.opponent_rank = opponent_rank
        return await self.request(req)

    async def grand_arena_start(self, token: str, battle_viewer_id: int, remain_battle_number: int, disable_skin: int):
        req = GrandArenaStartRequest()
        req.token = token
        req.battle_viewer_id = battle_viewer_id
        req.remain_battle_number = remain_battle_number
        req.disable_skin = disable_skin
        return await self.request(req)

    async def multi_give_gift(self, unit_id: int, cakes: typing.Counter[ItemType]):
        req = RoomMultiGiveGiftRequest()
        req.unit_id = unit_id
        req.item_info = [SendGiftData(item_id=item[1], item_num=cnt, current_item_num=self.data.get_inventory(item)) for item, cnt in cakes.items()]
        return await self.request(req)

    async def get_gacha_index(self):
        req = GachaIndexRequest()
        return await self.request(req)

    async def get_gacha_resident_index(self):
        req = GachaMonthlyIndexRequest()
        return await self.request(req)

    async def gacha_select_prize(self, prizegacha_id: int, item_id: int):
        req = GachaSelectPrizeRequest()
        req.prizegacha_id = prizegacha_id
        req.item_id = item_id
        return await self.request(req)

    async def draw_from_bank(self, current_bank_gold: int, draw_gold: int):
        req = ShopWithdrawGoldFromBankRequest()
        req.current_bank_gold = current_bank_gold
        req.draw_gold = draw_gold
        return await self.request(req)

    async def prepare_mana(self, mana: int):
        if self.data.get_mana() >= mana:
            return True
        elif self.data.get_mana(include_bank = True) >= mana:
            await self.draw_from_bank(mana, mana - self.data.get_mana())
            return True
        else:
            return False

    async def exec_gacha_aware(self, target_gacha: GachaParameter, gacha_times: int, draw_type: eGachaDrawType, current_cost_num: int, campaign_id: int) -> GachaReward:

        if draw_type == eGachaDrawType.Payment and current_cost_num < 1500:
            raise AbortError(f"宝石{current_cost_num}不足1500")

        if draw_type == eGachaDrawType.Ticket and current_cost_num < 1:
            raise AbortError(f"单抽券{current_cost_num}不足")

        if target_gacha.selected_item_id == 0:
            prizegacha_id = db.gacha_data[target_gacha.id].prizegacha_id
            if db.prizegacha_data[prizegacha_id].prize_memory_id_2 != 0:
                raise AbortError("可选碎片大于一种，请自行手动选择")
            item_id = db.prizegacha_data[prizegacha_id].prize_memory_id_1
            await self.gacha_select_prize(prizegacha_id, item_id)

        if target_gacha.exchange_id in self.data.gacha_point and  \
        self.data.gacha_point[target_gacha.exchange_id].current_point >= self.data.gacha_point[target_gacha.exchange_id].max_point:
            raise AbortError(f"已达到天井{self.data.gacha_point[target_gacha.exchange_id].current_point}pt，请上号兑换角色") 
            # auto exchange TODO

        if draw_type == eGachaDrawType.Payment: # 怎么回传没有宝石数
            tot = 1500
            mine = min(tot, self.data.jewel.free_jewel)

            tot -= mine
            self.data.jewel.free_jewel -= mine
            if tot:
                self.data.jewel.jewel -= tot
        elif draw_type == eGachaDrawType.Ticket:
            self.data.set_inventory(db.gacha_single_ticket, current_cost_num - 1)

        resp = await self.exec_gacha(target_gacha.id, gacha_times, target_gacha.exchange_id, draw_type, current_cost_num, campaign_id)

        reward: GachaReward = GachaReward(resp)

        return reward

    async def exec_gacha(self, gacha_id: int, gacha_times: int, exchange_id: int, draw_type: int, current_cost_num: int, campaign_id: int):
        req = GachaExecRequest()
        req.gacha_id = gacha_id
        req.gacha_times = gacha_times
        req.exchange_id = exchange_id
        req.draw_type = draw_type
        req.current_cost_num = current_cost_num
        req.campaign_id = campaign_id
        return await self.request(req)

    async def exec_hatsune_gacha(self, event_id: int, gacha_id: int, gacha_times: int, current_cost_num: int, loop_box_multi_gacha_flag: int):
        req = EventGachaExecRequest()
        req.event_id = event_id
        req.gacha_id = gacha_id
        req.gacha_times = gacha_times
        req.current_cost_num = current_cost_num
        req.loop_box_multi_gacha_flag = loop_box_multi_gacha_flag
        return await self.request(req)

    async def reset_hatsune_gacha(self, event_id: int, gacha_id: int):
        req = EventGachaResetRequest()
        req.event_id = event_id
        req.gacha_id = gacha_id
        return await self.request(req)

    async def story_check(self, story_id: int):
        req = StoryMaintenanceCheckRequest()
        req.story_id = story_id
        return await self.request(req)

    async def story_view(self, story_id: int):
        req = StoryViewingRequest()
        req.story_id = story_id
        return await self.request(req)

    async def read_story(self, story_id: int):
        await self.story_check(story_id)
        return await self.story_view(story_id)

    async def read_ysn_story(self, sub_story_id: int):
        req = SubStoryYsnReadStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def read_nop_story(self, sub_story_id: int):
        req = SubStoryNopReadStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def read_mhp_story(self, sub_story_id: int):
        req = SubStoryMhpReadStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def read_svd_story(self, sub_story_id: int):
        req = SubStorySvdReadStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def read_ssp_story(self, sub_story_id: int):
        req = SubStorySspReadSspStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def read_ske_story(self, sub_story_id: int):
        req = SubStorySkeReadStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def confirm_ske_story(self):
        req = SubStorySkeConfirmRequest()
        await self.request(req)

    async def read_lto_story(self, sub_story_id: int):
        req = SubStoryLtoReadStoryRequest()
        req.sub_story_id = sub_story_id
        await self.request(req)

    async def read_dear(self, event_id: int, story_id: int):
        req = HatsuneDearFinishRequest()
        req.event_id = event_id
        req.story_id = story_id
        req.choice = 1
        return await self.request(req)

    async def mission_index(self):
        req = MissionIndexRequest()
        request_flag = MissionRequestFlag()
        request_flag.quest_clear_rank = 0
        req.request_flag = request_flag
        return await self.request(req)

    async def room_level_up_item(self, floor_number: int, item: RoomUserItem):
        req = RoomLevelUpStartRequest()
        req.floor_number = floor_number
        req.serial_id = item.serial_id
        return await self.request(req)

    async def draw_chara_fortune(self):
        req = RaceLoginBonusCharaSelectDataRequest()
        req.fortune_id = self.data.cf.fortune_id
        req.unit_id = self.data.cf.unit_list[0]
        return await self.request(req)

    async def get_shop_item_list(self):
        req = ShopItemListRequest()
        return await self.request(req)

    async def shop_buy_item(self, shop_id, bought_list):
        req = ShopBuyMultipleRequest()
        req.system_id = shop_id
        req.slot_ids = bought_list
        req.current_currency_num = self.data.get_shop_gold(shop_id)
        return await self.request(req)

    async def shop_reset(self, shop_id):
        req = ShopResetRequest()
        req.system_id = shop_id
        req.current_currency_num = self.data.get_shop_gold(shop_id)
        return await self.request(req)

    async def mission_receive(self):
        req = MissionAcceptRequest()
        req.type = 1
        req.buy_id = 0
        req.id = 0
        return await self.request(req)

    async def get_tower_top(self):
        req = TowerTopRequest()
        req.is_first = 1
        req.return_cleared_ex_quest = 0
        return await self.request(req)

    async def tower_cloister_battle_skip(self, times: int):
        req = CloisterBattleSkipRequest()
        req.skip_count = times
        req.quest_id = db.tower_area[self.data.tower_status.cleared_floor_num].cloister_quest_id # TODO
        req.current_ticket_num = self.data.get_inventory((eInventoryType.Item, 23001))
        return await self.request(req)

    async def hatsune_mission_index(self, event_id: int):
        req = HatsuneMissionIndexRequest()
        req.event_id = event_id
        return await self.request(req)

    async def hatsune_mission_receive(self, event_id: int, type: int):
        req = HatsuneMissionAcceptRequest()
        req.event_id = event_id
        req.type = type 
        req.buy_id = 0
        req.id = 0
        return await self.request(req)

    async def get_hatsune_dear_top(self, event_id: int):
        req = HatsuneDearTopRequest()
        req.event_id = event_id
        return await self.request(req)

    async def get_hatsune_gacha_index(self, event_id: int, gacha_id: int):
        req = EventGachaIndexRequest()
        req.event_id = event_id
        req.gacha_id = gacha_id
        return await self.request(req)

    async def hatsune_boss_skip(self, event_id: int, boss_id: int, times: int, ticket: int):
        req = HatsuneBossBattleSkipRequest()
        req.event_id = event_id
        req.boss_id = boss_id
        req.exec_skip_num = times
        req.current_boss_ticket_num = ticket
        req.current_skip_ticket_num = self.data.get_inventory((eInventoryType.Item, 23001))
        return await self.request(req)

    async def get_profile(self, user: int):
        req = ProfileGetRequest()
        req.target_viewer_id = user
        return await self.request(req)

    async def get_hatsune_top(self, event: int):
        req = HatsuneTopRequest()
        req.event_id = event
        return await self.request(req)

    async def get_hatsune_quest_top(self, event: int):
        req = HatsuneQuestTopRequest()
        req.event_id = event
        return await self.request(req)
    
    async def present_receive_all(self, is_exclude_stamina: bool):
        req = PresentReceiveAllRequest()
        req.time_filter = -1
        req.type_filter = 0
        req.desc_flag = True
        req.is_exclude_stamina = is_exclude_stamina
        return await self.request(req)

    async def accept_clan_invitation(self, clan: int, page: int = 0):
        req = UserInviteClanListRequest()
        req.page = page
        for inv in (await self.request(req)).list:
            if inv.clan_id == clan:
                req = ClanJoinRequest()
                req.clan_id = clan
                req.from_invite = inv.invite_id
                result = await self.request(req)
                req = ClanInfoRequest()
                req.clan_id = clan
                await self.request(req)
                return result
        else:
            return None

    async def remove_member(self, user: int):
        req = ClanRemoveRequest()
        req.clan_id = self.data.clan
        req.remove_viewer_id = user
        return await self.request(req)
    
    async def invite_to_clan(self, user: int, msg: str = ''):
        req = ClanInviteRequest()
        req.invite_message = msg
        req.invited_viewer_id = user
        return await self.request(req)
    
    async def invite_to_clan2(self, other: "pcrclient"):
        await self.invite_to_clan(other.viewer_id)
        for page in range(5):
            if await other.accept_clan_invitation(self.data.clan, page):
                return
    
    async def create_clan(self, name: str = "默认名字", description: str = "默认描述", 
        cond: eClanJoinCondition = eClanJoinCondition.ONLY_INVITATION,
        guildLine: eClanActivityGuideline = eClanActivityGuideline.GUIDELINE_1):
        req = ClanCreateRequest()
        req.activity = guildLine
        req.clan_battle_mode = 0
        req.clan_name = name
        req.description = description
        req.join_condition = cond
        await self.request(req)

    async def get_clan_info(self):
        if self.data.clan == 0: return None
        req = ClanInfoRequest()
        req.clan_id = self.data.clan
        req.get_user_equip = 0
        return (await self.request(req))

    async def request_equip(self, equip_id: int, clan_id: int):
        req = EquipRequestRequest()
        req.equip_id = equip_id
        req.clan_id = clan_id
        return await self.request(req)
    
    async def donate_equip(self, request: EquipRequests, times: int):
        req = EquipDonateRequest()
        req.clan_id = self.data.clan
        req.current_equip_num = self.data.get_inventory((eInventoryType.Equip, request.equip_id))
        req.donation_num = times
        req.message_id = request.message_id
        return await self.request(req)
    
    async def quest_skip(self, quest: int, times: int):
        req = QuestSkipRequest()
        req.current_ticket_num = self.data.get_inventory((eInventoryType.Item, 23001))
        req.quest_id = quest
        req.random_count = times
        return await self.request(req)

    async def shiori_quest_skip(self, event: int, quest: int, times: int):
        req = ShioriQuestSkipRequest()
        req.event_id = event
        req.quest_id = quest
        req.use_ticket_num = times
        req.current_ticket_num = self.data.get_inventory((eInventoryType.Item, 23001))
        return await self.request(req)

    async def hatsune_quest_skip(self, event: int, quest: int, times: int):
        req = HatsuneQuestSkipRequest()
        req.event_id = event
        req.quest_id = quest
        req.use_ticket_num = times
        req.current_ticket_num = self.data.get_inventory((eInventoryType.Item, 23001))
        return await self.request(req)
    
    async def training_quest_skip(self, quest: int, times: int):
        req = TrainingQuestSkipRequest()
        req.current_ticket_num = self.data.get_inventory((eInventoryType.Item, 23001))
        req.quest_id = quest
        req.random_count = times
        return await self.request(req)

    async def equip_get_request(self, clan_id: int, message_id: int):
        req = EquipGetRequestRequest()
        req.clan_id = clan_id
        req.message_id = message_id
        return await self.request(req)
    
    async def getrequests(self):
        req = ClanChatInfoListRequest()
        req.clan_id = self.data.clan
        req.count = 100
        req.direction = 1 # RequestDirection.UP
        req.search_date = "2099-12-31"
        req.start_message_id = 0
        req.update_message_ids = []
        req.wait_interval = 3
        resp = await self.request(req)
        times = {msg.message_id : msg.create_time for msg in resp.clan_chat_message if msg.message_type == eClanChatMessageType.DONATION}
        return (equip for equip in resp.equip_requests if times[equip.message_id] > self.server_time - 28800)
    
    async def recover_stamina(self, recover_count: int = 1):
        req = ShopRecoverStaminaRequest()
        req.current_currency_num = self.data.jewel.free_jewel + self.data.jewel.jewel
        req.recover_count = recover_count
        return await self.request(req)

    async def get_arena_history(self):
        req = ArenaHistoryRequest()
        return await self.request(req)

    async def get_grand_arena_history(self):
        req = GrandArenaHistoryRequest()
        return await self.request(req)

    async def get_arena_history_detail(self, log_id: int):
        req = ArenaHistoryDetailRequest()
        req.log_id = log_id
        return await self.request(req)

    async def get_grand_arena_history_detail(self, log_id: int):
        req = GrandArenaHistoryDetailRequest()
        req.log_id = log_id
        return await self.request(req)
    
    async def get_arena_info(self):
        req = ArenaInfoRequest()
        return await self.request(req)
    
    async def get_grand_arena_info(self):
        req = GrandArenaInfoRequest()
        return await self.request(req)
    
    async def receive_arena_reward(self):
        req = ArenaTimeRewardAcceptRequest()
        return await self.request(req)

    async def get_dungeon_info(self):
        req = DungeonInfoRequest()
        return await self.request(req)

    async def get_special_dungeon_info(self ,dungeon_area_id: int):
        req = SpecialDungeonTopRequest()
        req.dungeon_area_id = dungeon_area_id
        return await self.request(req)

    async def skip_dungeon(self, dungeon_area_id: int):
        req = DungeonSkipRequest()
        req.dungeon_area_id = dungeon_area_id
        return await self.request(req)
    
    async def receive_grand_arena_reward(self):
        req = GrandArenaTimeRewardAcceptRequest()
        return await self.request(req)
    
    async def receive_all(self):
        await self.request(RoomReceiveItemAllRequest())
        req = PresentReceiveAllRequest()
        req.time_filter = -1
        await self.request(req)
        req = MissionAcceptRequest()
        req.type = 1
        await self.request(req)

    async def serlize_gacha_reward(self, gacha: GachaReward):
        res = ""
        if gacha.new_unit:
            res += f"NEW: \n" + '\n'.join([db.get_inventory_name(item) for item in gacha.new_unit]) + '\n'
        if gacha.unit_rarity:
            res += ' '.join(["★"*i + f"x{cnt}" for i, cnt in gacha.unit_rarity.items()]) + '\n'
        if gacha.prize_rarity:
            res += ' '.join([f"{i}等" + f"x{cnt}" for i, cnt in gacha.prize_rarity.items()]) + '\n'

        res += await self.serlize_reward(gacha.reward_list)

        return res
    
    async def serlize_reward(self, reward_list: List[InventoryInfo], target: Union[ItemType, None] = None):
        result = []
        rewards = {}
        for reward in reward_list:
            if target is None or (reward.type == target[0] and reward.id == target[1]):
                if (reward.id, reward.type) not in rewards:
                    rewards[(reward.id, reward.type)] = [reward.count, reward.stock, reward]
                else:
                    rewards[(reward.id, reward.type)][0] += reward.count
                    rewards[(reward.id, reward.type)][1] = max(reward.stock, rewards[(reward.id, reward.type)][1])
        reward_item = list(rewards.values())
        reward_item = sorted(reward_item, key = lambda x: x[0], reverse = True)
        for value in reward_item:
            try:
                result.append(f"{db.get_inventory_name(value[2])}x{value[0]}({value[1]})")
            except:
                result.append(f"未知物品({value[2],type},{value[2].id})x{value[0]}({value[1]})")
        if target is not None and len(result) == 0:
            result.append(f"{db.get_inventory_name_san(target)}x0({self.data.get_inventory(target)})")
        return '\n'.join(result) if result else "无"

    async def serialize_unit_info(self, unit_data: Union[UnitData, UnitDataLight]) -> Tuple[bool, str]:
        info = []
        ok = True
        def add_info(prefix, cur, expect = None):
            if expect:
                nonlocal ok
                info.append(f'{prefix}:{cur}/{expect}')
                ok &= (cur == expect)
            else:
                info.append(f'{prefix}:{cur}')
        unit_id = unit_data.id
        add_info("等级", unit_data.unit_level, db.team_max_level)
        if unit_data.battle_rarity:
            add_info("星级", f"{unit_data.battle_rarity}-{unit_data.unit_rarity}")
        else:
            add_info("星级", f"{unit_data.unit_rarity}")
        add_info("品级", unit_data.promotion_level, db.equip_max_rank)
        for id, union_burst in enumerate(unit_data.union_burst):
            if union_burst.skill_level:
                add_info(f"ub{id}", union_burst.skill_level, unit_data.unit_level)
        for id, skill in enumerate(unit_data.main_skill):
            if skill.skill_level:
                add_info(f"skill{id}", skill.skill_level, unit_data.unit_level)
        for id, skill in enumerate(unit_data.ex_skill):
            if skill.skill_level:
                add_info(f"ex{id}", skill.skill_level, unit_data.unit_level)
        equip_info = []
        for id, equip in enumerate(unit_data.equip_slot):
            equip_id = getattr(db.unit_promotion[unit_id][unit_data.promotion_level], f'equip_slot_{id + 1}')
            if not equip.is_slot:
                if equip_id != 999999:
                    equip_info.append('-')
                    ok = False
                else:
                    equip_info.append('*')
            else:
                star = db.get_equip_star_from_pt(equip_id, equip.enhancement_pt)
                ok &= (star == 5)
                equip_info.append(str(star))
        equip_info = '/'.join(equip_info)
        add_info("装备", equip_info)

        for id, equip in enumerate(unit_data.unique_equip_slot):
            equip_slot = id + 1
            have_unique = (equip_slot in db.unit_unique_equip and unit_id in db.unit_unique_equip[equip_slot])
            max_level = 0 if not have_unique else db.unique_equipment_max_level[equip_slot]
            if have_unique:
                if not equip.is_slot:
                    add_info(f"专武{id}", '-', max_level)
                else:
                    add_info(f"专武{id}", db.get_unique_equip_level_from_pt(equip_slot, equip.enhancement_pt), max_level)
        
        return ok, ' '.join(info)

    async def recover_challenge(self, quest: int):
        req = QuestRecoverChallengeRequest()
        req.quest_id = quest
        req.current_currency_num = self.data.jewel.free_jewel + self.data.jewel.jewel
        return await self.request(req)
    
    async def present_index(self) -> PresentIndexResponse:
        req = PresentIndexRequest()
        req.time_filter = -1
        req.type_filter = 0
        req.desc_flag = True
        req.offset = 0
        return await self.request(req)

    async def unlock_quest_id(self, quest: int):
        return (
            (quest in self.data.quest_dict and self.data.quest_dict[quest].clear_flg > 0) or 
            (quest in db.tower_quest and self.data.tower_status.cleared_floor_num >= db.tower_quest[quest].floor_num)
        )

    @property
    def stamina_recover_cnt(self) -> int:
        return self.keys.get('stamina_recover_times', 0)

    def set_stamina_recover_cnt(self, value: int):
        self.keys['stamina_recover_times'] = value

    async def quest_skip_aware(self, quest: int, times: int, recover: bool = False, is_total: bool = False):
        name = db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}"
        if db.is_hatsune_quest(quest):
            event = db.quest_to_event[quest].event_id
            if not quest in self.data.hatsune_quest_dict[event]:
                raise AbortError(f"任务{name}未通关或不存在")

            qinfo = self.data.hatsune_quest_dict[event][quest]

            if qinfo.clear_flag != 3:
                raise AbortError(f"任务{name}未三星")

        else:
            if not quest in self.data.quest_dict:
                raise AbortError(f"任务{name}未通关或不存在")
            qinfo = self.data.quest_dict[quest]

            if qinfo.clear_flg != 3: # 怎么会少一个a
                raise AbortError(f"任务{name}未三星")


        info = db.quest_info[quest]
        result: List[InventoryInfo] = []
        async def skip(times):
            while self.data.stamina < info.stamina * times:
                if self.stamina_recover_cnt > self.data.recover_stamina_exec_count:
                    await self.recover_stamina()
                else:
                    raise AbortError(f"任务{name}体力不足")
            if db.is_shiori_quest(quest):
                event = db.quest_to_event[quest].event_id
                return await self.shiori_quest_skip(event, quest, times)
            elif db.is_hatsune_quest(quest):
                event = db.quest_to_event[quest].event_id
                return await self.hatsune_quest_skip(event, quest, times)
            else:
                return await self.quest_skip(quest, times)
        if info.daily_limit:
            if is_total:
                times -= qinfo.daily_clear_count
            max_times = ((self.data.recover_max_time(quest) if recover else 0) + 1) * info.daily_limit - qinfo.daily_clear_count
            times = min(times, max_times)
            if times <= 0:
                raise SkipError(f"任务{name}已达最大次数")
            remain = info.daily_limit * (qinfo.daily_recovery_count + 1) - qinfo.daily_clear_count
            while times > 0:
                if remain == 0:
                    await self.recover_challenge(quest)
                    remain = info.daily_limit
                t = min(times, remain)
                resp = await skip(t)
                if resp.quest_result_list:
                    for result_list in resp.quest_result_list:
                        result = result + result_list.reward_list
                if resp.bonus_reward_list:
                    result = result + resp.bonus_reward_list
                    
                times -= t
                remain -= t
        else:
            resp = await skip(times)
            if resp.quest_result_list:
                for result_list in resp.quest_result_list:
                    result = result + result_list.reward_list
            if resp.bonus_reward_list:
                result = result + resp.bonus_reward_list

        return result

    '''
    async def hatsune_quest_skip_aware(self, event: int, quest: int, times: int, recover: bool = False, is_total: bool = False):
        name = db.quest_name[quest]
        if not quest in self.data.hatsune_quest_dict[event]:
            raise AbortError(f"任务{name}未通关或不存在")
        qinfo = self.data.hatsune_quest_dict[event][quest]
        if qinfo.clear_flag != 3:
            raise AbortError(f"任务{name}未三星")
        info = db.quest_info[quest]
        async def skip(times):
            if self.data.stamina < info[1] * times:
                if self.keys.get('buy_stamina_passive', 0) > self.data.recover_stamina_exec_count:
                    await self.recover_stamina()
                else:
                    raise SkipError(f"任务{name}体力不足")
            return await self.hatsune_quest_skip(event, quest, times)
        result: List[InventoryInfo] = []
        if info[0]:
            if is_total:
                times -= qinfo.daily_clear_count
            max_times = ((self.data.recover_max_time(quest) if recover else 0) + 1) * info[0] - qinfo.daily_clear_count
            times = min(times, max_times)
            if times <= 0:
                raise SkipError(f"任务{name}已达最大次数")
            remain = info[0] * (qinfo.daily_recovery_count + 1) - qinfo.daily_clear_count
            while times > 0:
                if remain == 0:
                    await self.recover_challenge(quest)
                    remain = info[0]
                t = min(times, remain)
                resp = await skip(t)
                if resp.quest_result_list:
                    for result_list in resp.quest_result_list:
                        result = result + result_list.reward_list
                if resp.bonus_reward_list:
                    result = result + resp.bonus_reward_list
                times -= t
                remain -= t
        else:
            resp = await skip(times)
            if resp.quest_result_list:
                for result_list in resp.quest_result_list:
                    result = result + result_list.reward_list
            if resp.bonus_reward_list:
                result = result + resp.bonus_reward_list

        return result
    '''
    
    async def refresh(self):
        req = HomeIndexRequest()
        req.message_id = 1
        req.gold_history = 0
        req.is_first = 1
        req.tips_id_list = []
        await self.request(req)
    
    async def reset_dungeon(self):
        req = DungeonResetRequest()
        req.dungeon_area_id = self.data.dungeon_area_id
        return await self.request(req)

    async def enter_dungeon(self, area: int):
        req = DungeonEnterAreaRequest()
        req.dungeon_area_id = area
        return await self.request(req)

    async def enter_special_dungeon(self, area: int):
        req = SpecialDungeonEnterAreaRequest()
        req.dungeon_area_id = area
        return await self.request(req)

    async def reset_special_dungeon(self, area: int):
        req = SpecialDungeonResetRequest()
        req.dungeon_area_id = area
        return await self.request(req)

    async def get_dungeon_unit(self):
        req = DungeonDispatchUnitList2Request()
        req.dungeon_area_id = self.data.dungeon_area_id
        return (await self.request(req)).dispatch_unit_list

    async def clan_like(self, viewer_id):
        req = ClanLikeRequest()
        req.target_viewer_id = viewer_id
        req.clan_id = self.data.clan
        return await self.request(req)

    async def room_like(self, viewer_id: int):
        req = RoomLikeRequest()
        req.target_viewer_id = viewer_id
        return await self.request(req)

    async def room_visit(self, viewer_id: int):
        req = RoomVisitRequest()
        req.target_viewer_id = viewer_id
        return await self.request(req)

    async def room_like_history(self):
        req = RoomLikeHistoryRequest()
        return await self.request(req)

    async def room_accept_all(self):
        req = RoomReceiveItemAllRequest()
        return await self.request(req)

    async def room_start(self) -> RoomStartResponse:
        req = RoomStartRequest()
        req.wac_auto_option_flag = 1
        return await self.request(req)

    async def borrow_dungeon_member(self, viewer_id):
        if not self.data.dungeon_avaliable: return
        if self.data.dungeon_area_id != 0:
            await self.reset_dungeon()
        area = await self.enter_dungeon(31001) # 云海的山脉
        for unit in await self.get_dungeon_unit():
            if unit.owner_viewer_id == viewer_id:
                if unit.unit_data.unit_level > self.data.team_level + self.data.settings.dungeon.support_lv_band:
                    continue
                req = DeckUpdateRequest()
                req.deck_number = 4
                req.unit_id_1 = 1
                req.unit_id_2 = 0
                req.unit_id_3 = 0
                req.unit_id_4 = 0
                req.unit_id_5 = 0
                await self.request(req)
                req = DungeonBattleStartRequest()
                req.quest_id = 31001001 # 云海的山脉第一层
                dispatch_unit = DungeonBattleStartUnit()
                dispatch_unit.owner_viewer_id = unit.owner_viewer_id
                dispatch_unit.unit_id = unit.unit_data.id
                empty_unit = DungeonBattleStartUnit()
                empty_unit.owner_viewer_id = self.viewer_id
                empty_unit.unit_id = 0
                req.unit_list = [
                    dispatch_unit,
                    empty_unit,
                    empty_unit,
                    empty_unit,
                    empty_unit
                ]
                req.disable_skin = 1
                req.support_battle_rarity = 0
                await self.request(req)
                req = DungeonBattleRetireRequest()
                req.quest_id = 31001001
                await self.request(req)
                break
        await self.reset_dungeon()

    async def psy_top(self, from_system_id: eSystemId = eSystemId.HATSUNE_TOP):
        req = PsyTopRequest()
        req.from_system_id = from_system_id
        return await self.request(req)

    async def start_cooking(self, frame_list: List[int], from_system_id: eSystemId = eSystemId.HATSUNE_TOP):
        req = PsyStartCookingRequest()
        req.start_cooking_frame_id_list = frame_list
        req.get_pudding_frame_id_list = []
        req.from_system_id = from_system_id
        return await self.request(req)

    async def get_pudding(self, frame_list: List[int], from_system_id: eSystemId = eSystemId.HATSUNE_TOP):
        req = PsyGetPuddingRequest()
        req.frame_id_list = frame_list
        req.from_system_id = from_system_id
        return await self.request(req)

    async def psy_read_drama(self, drama_id: int, from_system_id: eSystemId = eSystemId.HATSUNE_TOP):
        req = PsyReadDramaRequest()
        req.drama_id = drama_id
        req.from_system_id = from_system_id
        return await self.request(req)

    def set_stamina_consume_not_run(self):
        self.keys['stamina_consume_not_run'] = True

    def is_stamina_consume_not_run(self):
        return self.keys.get('stamina_consume_not_run', False)

    def set_stamina_get_not_run(self):
        self.keys['stamina_get_not_run'] = True

    def is_stamina_get_not_run(self):
        return self.keys.get('stamina_get_not_run', False)

    def set_star_cup_sweep_not_run(self):
        self.keys['star_cup_sweep_not_run'] = True

    def is_star_cup_sweep_not_run(self):
        return self.keys.get('star_cup_sweep_not_run', False)

    def set_heart_sweep_not_run(self):
        self.keys['heart_sweep_not_run'] = True

    def is_heart_sweep_not_run(self):
        return self.keys.get('heart_sweep_not_run', False)

    def set_cron_run(self):
        self.keys['cron_run'] = True

    def is_cron_run(self):
        return self.keys.get('cron_run', False)
