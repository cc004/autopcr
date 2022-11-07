from .clientbase import *

class pcrclient(dataclient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = {}
    
    async def login(self):
        await self._request(None)

    async def get_profile(self, user: int):
        req = ProfileGetRequest()
        req.target_viewer_id = user
        return await self._request(req)
    
    async def present_receive_all(self):
        req = PresentReceiveAllRequest()
        req.time_filter = -1
        return await self._request(req)

    async def accept_clan_invitation(self, clan: int, page: 0):
        req = UserInviteClanListRequest()
        req.page = page
        for inv in (await self._request(req)).list:
            if inv.clan_id == clan:
                req = ClanJoinRequest()
                req.clan_id = clan
                req.from_invite = inv.invite_id
                result = await self._request(req)
                req = ClanInfoRequest()
                req.clan_id = clan
                await self._request(req)
                return result
        else:
            return None

    async def remove_member(self, user: int):
        req = ClanRemoveRequest()
        req.clan_id = self.clan
        req.remove_viewer_id = user
        return await self._request(req)
    
    async def invite_to_clan(self, user: int, msg: str = ''):
        req = ClanInviteRequest()
        req.invite_message = msg
        req.invited_viewer_id = user
        return await self._request(req)
    
    async def invite_to_clan2(self, other: "pcrclient"):
        await self.invite_to_clan(other.viewer_id)
        for page in range(5):
            if await other.accept_clan_invitation(self.clan, page):
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
        await self._request(req)

    async def get_clan_info(self) -> ClanData:
        if self.clan == 0: return None
        req = ClanInfoRequest()
        req.clan_id = self.clan
        req.get_user_equip = 0
        return (await self._request(req)).clan
    
    async def donate_equip(self, request: EquipRequests, times: int):
        req = EquipDonateRequest()
        req.clan_id = self.clan
        req.current_equip_num = self.get_inventory((eInventoryType.Equip, request.equip_id))
        req.donation_num = times
        req.message_id = request.message_id
        return await self._request(req)
    
    async def quest_skip(self, quest: int, times: int):
        req = QuestSkipRequest()
        req.current_ticket_num = self.get_inventory((eInventoryType.Item, 23001))
        req.quest_id = quest
        req.random_count = times
        return await self._request(req)
    
    async def training_quest_skip(self, quest: int, times: int):
        req = TrainingQuestSkipRequest()
        req.current_ticket_num = self.get_inventory((eInventoryType.Item, 23001))
        req.quest_id = quest
        req.random_count = times
        return await self._request(req)
    
    async def get_requests(self):
        req = ClanChatInfoListRequest()
        req.clan_id = self.clan
        req.count = 100
        req.direction = 1 # RequestDirection.UP
        req.search_date = "2099-12-31"
        req.start_message_id = 0
        req.update_message_ids = []
        req.wait_interval = 3
        resp = await self._request(req)
        times = {msg.message_id : msg.create_time for msg in resp.clan_chat_message if msg.message_type == eClanChatMessageType.DONATION}
        return (equip for equip in resp.equip_requests if times[equip.message_id] > self.server_time - 28800)
    
    async def recover_stamina(self):
        req = ShopRecoverStaminaRequest()
        req.current_currency_num = self.jewel
        return await self._request(req)
    
    async def receive_arena_reward(self):
        req = ArenaTimeRewardAcceptRequest()
        return await self._request(req)
    
    async def receive_grand_arena_reward(self):
        req = GrandArenaTimeRewardAcceptRequest()
        return await self._request(req)
    
    async def receive_all(self):
        await self._request(RoomReceiveItemAllRequest())
        req = PresentReceiveAllRequest()
        req.time_filter = -1
        await self._request(req)
        req = MissionAcceptRequest()
        req.type = 1
        await self._request(req)
    
    async def quest_skip_aware(self, quest: int, times: int, cost: int):
        if self.stamina < cost * times and self.keys.get('buy_stamina_passive', 0) > self.recover_stamina_exec_count:
            await self.recover_stamina()
        await self.quest_skip(quest, times)
    
    async def refresh(self):
        req = HomeIndexRequest()
        req.message_id = 1
        req.gold_history = 0
        req.is_first = 1
        req.tips_id_list = []
        await self._request(req)
    
    async def reset_dungeon(self):
        req = DungeonResetRequest()
        req.dungeon_area_id = self.dungeon_area_id
        return await self._request(req)

    async def enter_dungeon(self, area: int):
        req = DungeonEnterAreaRequest()
        req.dungeon_area_id = area
        return await self._request(req)

    async def get_dungeon_unit(self):
        req = DungeonDispatchUnitList2Request()
        req.dungeon_area_id = self.dungeon_area_id
        return (await self._request(req)).dispatch_unit_list

    async def clan_like(self, viewer_id):
        req = ClanLikeRequest()
        req.viewer_id = viewer_id
        req.clan_id = self.clan
        return await self._request(req)

    async def room_accept_all(self):
        req = RoomReceiveItemAllRequest()
        return await self._request(req)

    async def borrow_dungeon_member(self, viewer_id):
        if not self.dungeon_avaliable: return
        if self.dungeon_area_id != 0:
            await self.reset_dungeon()
        area = await self.enter_dungeon(31001) # 云海的山脉
        for unit in await self.get_dungeon_unit():
            if unit.owner_viewer_id == viewer_id:
                if unit.unit_data.unit_level > self.team_level + self.settings.dungeon.support_lv_band:
                    continue
                req = DeckUpdateRequest()
                req.deck_number = 4
                req.unit_id_1 = 1
                req.unit_id_2 = 0
                req.unit_id_3 = 0
                req.unit_id_4 = 0
                req.unit_id_5 = 0
                await self._request(req)
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
                await self._request(req)
                req = DungeonBattleRetireRequest()
                req.quest_id = 31001001
                await self._request(req)
                break
        await self.reset_dungeon()