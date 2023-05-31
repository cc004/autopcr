from ..model.models import *
from .apiclient import apiclient
from .sessionmgr import sessionmgr
from .misc import errorhandler
from .datamgr import datamgr
from .database import db
from typing import Tuple

class pcrclient(apiclient):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.keys = {}
        self.data = datamgr()
        self.session = sessionmgr(*args, **kwargs)
        self.register(errorhandler())
        self.register(self.data)
        self.register(self.session)
    
    @property
    def name(self) -> str:
        return self.data.name

    async def login(self):
        await self.request(None)

    async def multi_give_gift(self, unit_id: int, cakes: List[SendGiftData]):
        req = RoomMultiGiveGiftRequest()
        req.unit_id = unit_id
        req.item_info = cakes
        return await self.request(req)

    async def get_gacha_index(self):
        req = GachaIndexRequest()
        return await self.request(req)

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

    async def read_story(self, story_id: int):
        req = StoryMaintenanceCheckRequest()
        req.story_id = story_id
        await self.request(req)
        req = StoryViewingRequest()
        req.story_id = story_id
        return await self.request(req)

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
        req.quest_id = db.floor2clositer[self.data.tower_status.cleared_floor_num] # TODO
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

    async def get_clan_info(self) -> ClanData:
        if self.data.clan == 0: return None
        req = ClanInfoRequest()
        req.clan_id = self.data.clan
        req.get_user_equip = 0
        return (await self.request(req)).clan
    
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
    
    async def recover_stamina(self):
        req = ShopRecoverStaminaRequest()
        req.current_currency_num = self.data.jewel.free_jewel + self.data.jewel.jewel
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
    
    async def serlize_reward(self, reward_list: List[InventoryInfo], target: Tuple[eInventoryType, int] = None):
        result = []
        rewards = {}
        for reward in reward_list:
            if target is None or (reward.type == target[0] and reward.id == target[1]):
                if (reward.id, reward.type) not in rewards:
                    rewards[(reward.id, reward.type)] = [reward.count, reward.stock, reward]
                else:
                    rewards[(reward.id, reward.type)][0] += reward.count
                    rewards[(reward.id, reward.type)][1] = max(reward.stock, rewards[(reward.id, reward.type)][1])
        for _, value in rewards.items():
            try:
                result.append(f"{db.get_inventory_name(value[2])}x{value[0]}({value[1]})")
            except:
                result.append(f"未知物品({value[2],type},{value[2].id})x{value[0]}({value[1]})")
        if target is not None and len(result) == 0:
            result.append(f"{db.get_inventory_name_san(target)}x0({self.data.get_inventory(target)})")
        return '\n'.join(result)

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
        return (quest in self.data.quest_dict and self.data.quest_dict[quest].clear_flg > 0) or (quest in db.tower2floor and self.data.tower_status.cleared_floor_num >= db.tower2floor[quest])

    async def quest_skip_aware(self, quest: int, times: int, recover: bool = False, is_total: bool = False):
        name = db.quest_name[quest] if quest in db.quest_name else f"未知关卡{quest}"
        if db.is_hatsune_quest(quest):
            event = db.quest_to_event_id[quest]
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
            if self.data.stamina < info[1] * times:
                if self.keys.get('buy_stamina_passive', 0) > self.data.recover_stamina_exec_count:
                    await self.recover_stamina()
                else:
                    raise SkipError(f"任务{name}体力不足")
            if db.is_shiori_quest(quest):
                event = db.quest_to_event_id[quest]
                return await self.shiori_quest_skip(event, quest, times)
            elif db.is_hatsune_quest(quest):
                event = db.quest_to_event_id[quest]
                return await self.hatsune_quest_skip(event, quest, times)
            else:
                return await self.quest_skip(quest, times)
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
