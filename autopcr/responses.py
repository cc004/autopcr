from typing import List
from .modelbase import ResponseBase
from .common import *
from .enums import *

class AcceptAgreementResponse(ResponseBase):
    pass
class AddUserTipsResponse(ResponseBase):
    pass
class ArcadeBuyResponse(ResponseBase):
    item_data: List[InventoryInfo] = None
class ArcadeReadStoryResponse(ResponseBase):
    pass
class ArcadeStoryListResponse(ResponseBase):
    story_id_list: List[int] = None
class ArcadeSyncStoryListResponse(ResponseBase):
    story_id_list: List[int] = None
class ArcadeTopResponse(ResponseBase):
    arcade_id_list: List[int] = None
class ArenaApplyResponse(ResponseBase):
    battle_viewer_id: int = None
    true_rank: int = None
class ArenaCancelResponse(ResponseBase):
    search_opponent: List[SearchOpponent] = None
class ArenaFinishResponse(ResponseBase):
    old_record: int = None
    new_record: int = None
    arena_info: ArenaInfo = None
    highest_rank_reward: InventoryInfo = None
class ArenaHistoryDamageRankingResponse(ResponseBase):
    user_unit_list: List[UnitDataForView] = None
    opponent_unit_list: List[UnitDataForView] = None
    damage_list: List[UnitDamageInfo] = None
class ArenaHistoryDetailResponse(ResponseBase):
    versus_result_detail: VersusResultDetail = None
class ArenaHistoryResponse(ResponseBase):
    versus_result_list: List[VersusResult] = None
class ArenaInfoResponse(ResponseBase):
    arena_info: ArenaInfo = None
    attack_deck: DeckData = None
    defend_deck: DeckData = None
    search_opponent: List[SearchOpponent] = None
    reward_info: InventoryInfo = None
    reward_hour_num: int = None
    is_time_reward_max: bool = None
class ArenaIntervalCancelResponse(ResponseBase):
    arena_info: ArenaInfo = None
    user_jewel: UserJewel = None
class ArenaMoveGroupResponse(ResponseBase):
    arena_info: ArenaInfo = None
class ArenaRankingResponse(ResponseBase):
    ranking: List[RankingSearchOpponent] = None
class ArenaReplayResponse(ResponseBase):
    seed: int = None
    is_challenge: int = None
    user_unit_list: List[UnitData] = None
    opponent_unit_list: List[UnitData] = None
class ArenaResetBattleNumberResponse(ResponseBase):
    arena_info: ArenaInfo = None
    user_jewel: UserJewel = None
class ArenaSearchResponse(ResponseBase):
    search_opponent: List[SearchOpponent] = None
class ArenaStartResponse(ResponseBase):
    my_viewer_id: int = None
    battle_viewer_id: int = None
    battle_id: int = None
    battle_speed: int = None
    wave_info_list: List[ArenaWaveInfo] = None
class ArenaTimeRewardAcceptResponse(ResponseBase):
    reward_info: InventoryInfo = None
    add_present_count: int = None
class AutomaticEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    equip_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
class AutomaticEquipEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    item_list: List[InventoryInfo] = None
    user_gold: UserGold = None
class AutomaticEquipEnhanceUniqueResponse(ResponseBase):
    unit_data: UnitData = None
    item_list: List[InventoryInfo] = None
    user_gold: UserGold = None
class BaseResponse(ResponseBase):
    notification: Notification = None
class ChangeRarityResponse(ResponseBase):
    unit_data_list: List[UnitData] = None
class ChangeRoleResponse(ResponseBase):
    members: List[ClanMemberInfo] = None
class ChangeSkinResponse(ResponseBase):
    pass
class CharaETicketExchangeResponse(ResponseBase):
    reward_info_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
class CharaETicketRewardsResponse(ResponseBase):
    rewards: List[CharaExchangeTicketReward] = None
class CheckAgreementResponse(ResponseBase):
    agreement: AgreementStatus = None
    policy: AgreementStatus = None
class CheckExistClanResponse(ResponseBase):
    pass
class ClanBattleBossHistoryResponse(ResponseBase):
    boss_history: List[BossHistory] = None
class ClanBattleBossInfoResponse(ResponseBase):
    damage_history: List[DamageHistory] = None
    current_hp: int = None
    attack_count: int = None
    fighter_num: int = None
class ClanBattleBossRankingInClanResponse(ResponseBase):
    bosses: List[BossRankingInClan] = None
    summary: BossRankingInClanSummary = None
class ClanBattleConfirmRehearsalMyLogResponse(ResponseBase):
    is_full: int = None
    mylogs: List[MyLog] = None
class ClanBattleConfirmTrainingMyLogResponse(ResponseBase):
    is_full: int = None
    mylogs: List[MyLog] = None
class ClanBattleDamageReportResponse(ResponseBase):
    damage_report: List[DamageReport] = None
    max_hp: int = None
class ClanBattleDeleteRehearsalMyLogResponse(ResponseBase):
    mylog_count: int = None
class ClanBattleDeleteTrainingMyLogResponse(ResponseBase):
    mylog_count: int = None
class ClanBattleFinishResponse(ResponseBase):
    acquired_gold: int = None
    user_gold: UserGold = None
    damage_result: int = None
    dead: int = None
    carry_over_time: int = None
    is_over_kill: int = None
    attack_count: int = None
    challenge_reward: List[InventoryInfo] = None
    add_present_count: int = None
class ClanBattleHistoryReportResponse(ResponseBase):
    history_report: List[HistoryReport] = None
    lap_num: int = None
    order_num: int = None
class ClanBattleMissionIndexResponse(ResponseBase):
    missions: List[UserMissionInfo] = None
    daily_reset_time: int = None
class ClanBattleMyLogDetailResponse(ResponseBase):
    lap_num: int = None
    order_num: int = None
class ClanBattleMyLogResponse(ResponseBase):
    actual_logs: List[MyLog] = None
    rehearsal_logs: List[MyLog] = None
    training_logs: List[MyLog] = None
class ClanBattlePeriodRankingResponse(ResponseBase):
    period_ranking: List[PeriodRanking] = None
    my_clan_data: PeriodRanking = None
    clan_battle_id: int = None
    period: int = None
    clan_battle_mode: int = None
class ClanBattleRehearsalFinishResponse(ResponseBase):
    damage_result: int = None
    carry_over_time: int = None
class ClanBattleRehearsalStartResponse(ResponseBase):
    limit_time: int = None
    enemy_data: UnitData = None
    battle_log_id: int = None
    skin_data_for_request: List[SkinDataForRequest] = None
    seed: int = None
    current_hp: int = None
class ClanBattleReloadDetailInfoResponse(ResponseBase):
    fighter_num: int = None
    current_hp: int = None
class ClanBattleResetHpResponse(ResponseBase):
    user_jewel: UserJewel = None
    used_unit: List[int] = None
class ClanBattleSaveRehearsalMyLogResponse(ResponseBase):
    mylog_count: int = None
class ClanBattleSaveTrainingMyLogResponse(ResponseBase):
    mylog_count: int = None
class ClanBattleStartResponse(ResponseBase):
    limit_time: int = None
    enemy_data: UnitData = None
    battle_log_id: int = None
    current_hp: int = None
    user_gold: UserGold = None
    skin_data_for_request: List[SkinDataForRequest] = None
    seed: int = None
class ClanBattleSuggestDeckListResponse(ResponseBase):
    suggest_deck_list: List[ClanBattleSuggestDeck] = None
class ClanBattleSuggestDeckReplayResponse(ResponseBase):
    limit_time: int = None
    user_unit_list: List[UnitData] = None
    enemy_data: UnitData = None
    current_hp: int = None
    seed: int = None
    report_key: str = None
class ClanBattleSuggestDeckReplayReportResponse(ResponseBase):
    pass
class ClanBattleSupportUnitList2Response(ResponseBase):
    support_unit_list: List[ClanBattleSupportUnitLight] = None
class ClanBattleSupportUnitListResponse(ResponseBase):
    support_unit_list: List[ClanBattleSupportUnit] = None
class ClanBattleTopResponse(ResponseBase):
    clan_battle_id: int = None
    period: int = None
    lap_num: int = None
    boss_info: List[BossInfo] = None
    damage_history: List[DamageHistory] = None
    period_rank: int = None
    remaining_count: int = None
    used_unit: List[int] = None
    using_unit: List[int] = None
    point: int = None
    hp_reset_count: int = None
    boss_reward: List[BossReward] = None
    last_rank_result: List[RankResult] = None
    change_period: int = None
    change_season: int = None
    add_present_count: int = None
    carry_over_time: int = None
    clan_battle_mode: int = None
    next_clan_battle_mode: int = None
    user_clan: ClanBattleTopUserClanInformation = None
    missions: List[UserMissionInfo] = None
    challenge_reward: List[ClanBattleExtraBattleChallengeRewardInfo] = None
class ClanBattleTrainingFinishResponse(ResponseBase):
    damage_result: int = None
    carry_over_time: int = None
class ClanBattleTrainingStartResponse(ResponseBase):
    limit_time: int = None
    enemy_data: UnitData = None
    battle_log_id: int = None
    skin_data_for_request: List[SkinDataForRequest] = None
    seed: int = None
    current_hp: int = None
class ClanBlockListResponse(ResponseBase):
    list: List[BlockUserDetail] = None
class ClanBreakUpResponse(ResponseBase):
    add_present_count: int = None
class ClanChatInfoListResponse(ResponseBase):
    clan_chat_message: List[ChatMessageInfo] = None
    users: List[ChatMemberInfo] = None
    equip_requests: List[EquipRequests] = None
    user_equip_data: List[UserEquipParameter] = None
    latest_comment_id: int = None
    expired_message_ids: List[int] = None
    next_search_date: str = None
    wait_interval: int = None
class ClanChatResponse(ResponseBase):
    pass
class ClanCreateResponse(ResponseBase):
    clan_id: int = None
    clan_status: eUserClanJoinStatus = None

    def update(self, client: "dataclient"):
        client.clan = self.clan_id

class ClanDamageReportResponse(ResponseBase):
    damage_report: List[HistoryReport] = None
class ClanDetailResponse(ResponseBase):
    member: List[ClanMemberInfo] = None
    owner_viewer_id: int = None
    invite_id: int = None
    block_id: int = None
class ClanInfoResponse(ResponseBase):
    clan: ClanData = None
    clan_status: eUserClanJoinStatus = None
    user_equip: List[InventoryInfoShort] = None
    have_join_request: int = None
    unread_liked_count: int = None
    is_equip_request_finish_checked: int = None
    add_present_count: int = None
    user_gold: UserGold = None
    latest_request_time: int = None
    current_period_ranking: int = None
    last_total_ranking: int = None
    current_clan_battle_mode: int = None
    current_battle_joined: int = None
    last_clan_battle_mode: int = None
    last_battle_joined: int = None
    grade_rank: int = None
    clan_point: int = None
    remaining_count: int = None

    def update(self, client: "dataclient"):
        client.clan = self.clan.detail.clan_id

class ClanInviteBlockResponse(ResponseBase):
    pass
class ClanInviteCancelResponse(ResponseBase):
    pass
class ClanInvitedUserListResponse(ResponseBase):
    list: List[InvitedUserDetail] = None
    oldest_time: int = None
class ClanInvitePermissionResponse(ResponseBase):
    pass
class ClanInviteResponse(ResponseBase):
    pass
class ClanInviteRejectResponse(ResponseBase):
    pass
class ClanInviteUnblockResponse(ResponseBase):
    pass
class ClanJoinResponse(ResponseBase):
    clan_status: eUserClanJoinStatus = None
class ClanJoinRequestAcceptResponse(ResponseBase):
    pass
class ClanJoinRequestCancelResponse(ResponseBase):
    pass
class ClanJoinRequestListResponse(ResponseBase):
    list: List[JoinRequestUserInfo] = None
    oldest_time: int = None
class ClanJoinRequestRejectResponse(ResponseBase):
    pass
class ClanLeaveResponse(ResponseBase):
    add_present_count: int = None
class ClanLikeResponse(ResponseBase):
    stamina_info: UserStaminaInfo = None
class ClanMemberBattleFinishResponse(ResponseBase):
    pass
class ClanMemberBattleStartResponse(ResponseBase):
    battle_id: int = None
    wave_info_list: List[PracticeWaveInfo] = None
class ClanRemoveResponse(ResponseBase):
    pass
class ClanSearchResponse(ResponseBase):
    list: List[ClanInfo] = None
class ClanSearchUserResponse(ResponseBase):
    search_user_list: List[ClanMemberInfo] = None
class ClanSetDispatchStatusResponse(ResponseBase):
    dispatch_units: List[UnitDataForClanMember] = None
    dispatch_time_bonus: InventoryInfo = None
    dispatch_count_bonus: InventoryInfo = None
    add_present_count: int = None
class ClanUpdateResponse(ResponseBase):
    clan: ClanInfo = None
class CloisterBattleSkipResponse(ResponseBase):
    quest_result_list: List[QuestResult] = None
    bonus_reward_list: List[InventoryInfo] = None
    user_gold: UserGold = None
    item_list: List[InventoryInfo] = None
    cloister_remain_clear_count: int = None
    add_present_count: int = None
class DeckUpdateListResponse(ResponseBase):
    pass
class DeckUpdateResponse(ResponseBase):
    pass
class DungeonBattleFinishResponse(ResponseBase):
    quest_id: int = None
    complete: bool = None
    area_quest_list: List[DungeonQuest] = None
    rest_challenge_count: List[RestChallengeInfo] = None
    reward_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
    add_present_count: int = None
    first_area_clear_flag: int = None
    current_battle_mission_list: List[DungeonBattleMission] = None
class DungeonBattleRetireResponse(ResponseBase):
    pass
class DungeonBattleStartResponse(ResponseBase):
    user_unit: List[UnitData] = None
    versus_user_unit: List[UnitData] = None
    battle_log_id: int = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
    seed: int = None
    support_unit_hp: int = None
class DungeonClanDispatchUnitListResponse(ResponseBase):
    dispatch_unit_list: List[ClanDispatchUnit] = None
class DungeonDispatchUnitList2Response(ResponseBase):
    dispatch_unit_list: List[ClanDispatchUnitLight] = None
class DungeonEnterAreaResponse(ResponseBase):
    quest_id: int = None
    complete: bool = None
    area_quest_list: List[DungeonQuest] = None
    dungeon_unit: List[DungeonUnit] = None
    rest_challenge_count: List[RestChallengeInfo] = None
    dungeon_cleared_area_id_list: List[int] = None
    season_pack_rate: int = None
    current_battle_mission_list: List[DungeonBattleMission] = None
    enter_reset_time: int = None

    def update(self, client: "dataclient"):
        client.dungeon_area_id = self.quest_id / 1000

class DungeonInfoResponse(ResponseBase):
    enter_area_id: int = None
    rest_challenge_count: List[RestChallengeInfo] = None
    dungeon_area: List[DungeonArea] = None
    dungeon_cleared_area_id_list: List[int] = None
    season_pack_rate: int = None
class DungeonResetResponse(ResponseBase):
    rest_challenge_count: List[RestChallengeInfo] = None
    dungeon_area: List[DungeonArea] = None
    season_pack_rate: int = None

    def update(self, client: "dataclient"):
        client.dungeon_area_id = 0
        type = self.dungeon_area[0].dungeon_type
        for count in self.rest_challenge_count:
            if count.dungeon_type == type:
                client.dungeon_avaliable = count.count > 0
                break

class DungeonSkipResponse(ResponseBase):
    start_quest_id: int = None
    rest_challenge_count: List[RestChallengeInfo] = None
    season_pack_rate: int = None
    skip_result_list: List[QuestResult] = None
    user_gold: UserGold = None
    add_present_count: int = None
    upper_limit_flag: bool = None
class EmblemChangeResponse(ResponseBase):
    pass
class EmblemTopResponse(ResponseBase):
    user_emblem_list: List[UserEmblem] = None
class EquipCraftResponse(ResponseBase):
    equip_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
class EquipDonateResponse(ResponseBase):
    donation_num: int = None
    donate_equip: InventoryInfo = None
    rewards: List[InventoryInfo] = None
    add_present_count: int = None

    def update(self, client: "dataclient"):
        client.donation_num = self.donation_num
        if self.donate_equip:
            client.update_inventory(self.donate_equip)
        if self.rewards:
            for item in self.rewards:
                client.update_inventory(item)

class EquipEnhanceMaxResponse(ResponseBase):
    unit_data: UnitData = None
    user_jewel: UserJewel = None
class EquipEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
    item_list: List[InventoryInfo] = None
class EquipGetRequestResponse(ResponseBase):
    request: EquipRequests = None
    equip_list: List[InventoryInfo] = None
    receive_donation_sum: int = None
    add_present_count: int = None
class EquipmentFreeEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
class EquipRequestResponse(ResponseBase):
    latest_request_time: int = None
class EventGachaExecResponse(ResponseBase):
    draw_result: List[EventBoxGachaHitRewardInfo] = None
    reward_info_list: List[InventoryInfo] = None
    add_present_count: int = None
    unlock_bosses: List[HatsuneEventBossStatus] = None
class EventGachaIndexResponse(ResponseBase):
    event_gacha_info: EventGachaInfo = None
class EventGachaLineupResponse(ResponseBase):
    event_gacha_lineup: List[EventBoxGachaSet] = None
class EventGachaResetResponse(ResponseBase):
    event_gacha_info: EventGachaInfo = None
class FkeFinishResponse(ResponseBase):
    total_fke_point: int = None
    add_present_count: int = None
class FkeStartResponse(ResponseBase):
    fke_play_id: int = None
class FkeSyncTopResponse(ResponseBase):
    total_fke_point: int = None
    best_fke_point: int = None
    happening_id_list: List[int] = None
class FkeTopResponse(ResponseBase):
    total_fke_point: int = None
    best_fke_point: int = None
    happening_id_list: List[int] = None
class FriendAcceptResponse(ResponseBase):
    pass
class FriendBattleFinishResponse(ResponseBase):
    pass
class FriendBattleStartResponse(ResponseBase):
    battle_id: int = None
    wave_info_list: List[PracticeWaveInfo] = None
class FriendBattleTopResponse(ResponseBase):
    my_deck_list: List[PracticeDeckData] = None
    friend: List[FriendBattleInfo] = None
class FriendBattleUpdateDeckResponse(ResponseBase):
    pass
class FriendCancelResponse(ResponseBase):
    pass
class FriendFriendListResponse(ResponseBase):
    friend_list: List[FriendInfo] = None
    campaign_target_list: List[CampaignTarget] = None
class FriendGetMissionTargetFriendCountResponse(ResponseBase):
    target_friend_count: int = None
class FriendMissionAcceptResponse(ResponseBase):
    team_level: int = None
    team_exp: int = None
    stamina_info: UserStaminaInfo = None
    rewards: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
class FriendMissionIndexResponse(ResponseBase):
    missions: List[UserMissionInfo] = None
    campaign_target_flag: bool = None
class FriendPendingListResponse(ResponseBase):
    pending_list: List[FriendInfo] = None
    friend_num: int = None
    campaign_target_list: List[CampaignTarget] = None
class FriendRejectResponse(ResponseBase):
    pass
class FriendRemoveResponse(ResponseBase):
    pass
class FriendRequestListResponse(ResponseBase):
    request_list: List[FriendInfo] = None
    friend_num: int = None
    campaign_target_list: List[CampaignTarget] = None
class FriendRequestResponse(ResponseBase):
    favorite_unit: UnitDataForView = None
class FriendSearchResponse(ResponseBase):
    search_list: List[FriendInfo] = None
    friend_num: int = None
    campaign_target_list: List[CampaignTarget] = None
class GachaExchangePointResponse(ResponseBase):
    reward_info_list: List[InventoryInfo] = None
    gacha_point_info: GachaPointInfo = None
    sdfes_gacha_point_info: GachaPointInfo = None
    bonus_reward_info: GachaBonusResult = None
    growth_unit_info: GachaGrowthUnitInfo = None
class GachaExecResponse(ResponseBase):
    reward_info_list: List[InventoryInfo] = None
    user_gold: UserGold = None
    prize_reward_info: PrizeRewardInfo = None
    gacha_point_info: GachaPointInfo = None
    sdfes_gacha_point_info: GachaPointInfo = None
    add_present_count: int = None
    bonus_reward_info: GachaBonusResult = None
    growth_unit_info: GachaGrowthUnitInfo = None
class GachaIndexResponse(ResponseBase):
    gacha_info: List[GachaParameter] = None
    nngtime: int = None
    campaign_info: CampaignGachaInfo = None
    sdg_url_param: str = None
    gacha_point_reset_list: List[GachaPointReset] = None
    gacha_point_reset: GachaPointReset = None
    sdfes_gacha_point_reset: GachaPointReset = None
    return_fes_gacha_point_reset: GachaPointReset = None
    current_gacha_point: int = None
    ticket_gacha_info: List[TicketGachaParameter] = None
class GachaPrizeHistoryResponse(ResponseBase):
    gacha_prize_history_list: List[GachaPrizeHistoryList] = None
class GachaPrizeRewardResponse(ResponseBase):
    gacha_prize_reward_list: List[GachaPrizeItemDetail] = None
class GachaSelectPrizeResponse(ResponseBase):
    pass
class GachaSpecialFesIndexResponse(ResponseBase):
    gacha_info: List[GachaParameter] = None
    ticket_gacha_info: List[TicketGachaParameter] = None
class GetFriendSupportUnitListResponse(ResponseBase):
    friend_support_unit_list: List[SupportUnitStatus] = None
    general_support_unit_list: List[SupportUnitStatus] = None
class GetTipsListResponse(ResponseBase):
    tips_id_list: List[int] = None
class GrandArenaApplyResponse(ResponseBase):
    battle_viewer_id: int = None
    true_rank: int = None
class GrandArenaCancelIntervalResponse(ResponseBase):
    grand_arena_info: GrandArenaInfo = None
    user_jewel: UserJewel = None
class GrandArenaCancelResponse(ResponseBase):
    search_opponent: List[GrandArenaSearchOpponent] = None
class GrandArenaFinishResponse(ResponseBase):
    old_record: int = None
    new_record: int = None
    grand_arena_info: GrandArenaInfo = None
    highest_rank_reward: InventoryInfo = None
class GrandArenaGetDestinationGroupResponse(ResponseBase):
    group_list: List[RankingGroupInfo] = None
class GrandArenaHistoryDetailResponse(ResponseBase):
    grand_arena_history_detail: GrandArenaHistoryDetailInfo = None
class GrandArenaHistoryResponse(ResponseBase):
    grand_arena_history_list: List[GrandArenaHistoryInfo] = None
class GrandArenaInfoResponse(ResponseBase):
    grand_arena_info: GrandArenaInfo = None
    attack_deck_list: List[DeckData] = None
    defend_deck_list: List[DeckData] = None
    search_opponent: List[GrandArenaSearchOpponent] = None
    reward_info: InventoryInfo = None
    reward_hour_num: int = None
    is_time_reward_max: bool = None
class GrandArenaMoveGroupResponse(ResponseBase):
    grand_arena_info: GrandArenaInfo = None
class GrandArenaRankingResponse(ResponseBase):
    ranking: List[GrandArenaSearchOpponent] = None
class GrandArenaReplayResponse(ResponseBase):
    seed: int = None
    is_challenge: int = None
    user_unit_list: List[UnitData] = None
    vs_user_unit_list: List[UnitData] = None
class GrandArenaResetBattleNumberResponse(ResponseBase):
    grand_arena_info: GrandArenaInfo = None
    user_jewel: UserJewel = None
class GrandArenaSearchResponse(ResponseBase):
    search_opponent: List[GrandArenaSearchOpponent] = None
class GrandArenaStartResponse(ResponseBase):
    battle_id: int = None
    my_viewer_id: int = None
    battle_viewer_id: int = None
    battle_speed: int = None
    wave_info_list: List[ArenaWaveInfo] = None
class GrandArenaTimeRewardAcceptResponse(ResponseBase):
    reward_info: InventoryInfo = None
    add_present_count: int = None
class HatsuneBossBattleFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    result_type: int = None
    unlock_quest_list: List[int] = None
    unlock_story_id: int = None
    unlock_story_id_list: List[int] = None
    quest_rewards: List[InventoryInfo] = None
    first_clear_rewards: List[InventoryInfo] = None
    acquired_gold: int = None
    user_gold: UserGold = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    treasure_rewards: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    unlock_unit: UnitData = None
    event_present_list: List[int] = None
    unlock_dear_story_id: int = None
    release_diary_ids: List[int] = None
    new_omp_story_ids: List[int] = None
    release_nyx_story_ids: List[int] = None
    new_sub_story_info_list: List[EventSubStoryInfo] = None
    next_boss: HatsuneEventBossStatus = None
    damage_result: int = None
    unlock_bosses: List[HatsuneEventBossStatus] = None
    unlock_boss_id_list: List[int] = None
class HatsuneBossBattleSkipResponse(ResponseBase):
    quest_result_list: List[QuestResult] = None
    crush_reward_list: List[QuestResult] = None
    user_gold: UserGold = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    item_list: List[InventoryInfo] = None
    unlock_dear_story_id: int = None
    release_diary_ids: List[int] = None
    release_nyx_story_ids: List[int] = None
class HatsuneBossBattleStartResponse(ResponseBase):
    limit_time: int = None
    battle_log_id: int = None
    seed: int = None
    boss_unit_data: UnitData = None
    hit_treasure_nums: List[int] = None
    hit_treasure_list: List[EventHitTreasureInfo] = None
class HatsuneChangeNyxItemColorResponse(ResponseBase):
    pass
class HatsuneDearFinishResponse(ResponseBase):
    before_dear_point_info: DearPointInfo = None
    after_dear_point_info: DearPointInfo = None
    add_present_count: int = None
class HatsuneDearTopResponse(ResponseBase):
    unlock_dear_story_info_list: List[DearStoryInfo] = None
    dear_point_info_list: List[DearPointInfo] = None
class HatsuneMissionAcceptResponse(ResponseBase):
    team_level: int = None
    team_exp: int = None
    stamina_info: UserStaminaInfo = None
    rewards: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
    release_contents: List[ReleaseContentData] = None
class HatsuneMissionIndexResponse(ResponseBase):
    missions: List[UserMissionInfo] = None
    season_pack: List[UserSeasonPackInfo] = None
    daily_reset_time: int = None
    series_info_list: List[HatsuneSeriesInfo] = None
class HatsuneQuestFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    reward_list: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    unlock_quest_list: List[int] = None
    unlock_story_id: int = None
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    daily_clear_count: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    has_drop: int = None
    clan_point: ClanPoint = None
    drop_rewards: List[InventoryInfo] = None
    event_present_list: List[int] = None
    unlock_quiz: List[int] = None
    state_exchange_stamina: eExchangeStaminaState = None
    unlock_dear_story_id: int = None
    release_diary_ids: List[int] = None
    new_relay_story_ids: List[int] = None
    new_omp_story_ids: List[int] = None
    release_nyx_story_ids: List[int] = None
    user_gold: UserGold = None
    new_sub_story_info_list: List[EventSubStoryInfo] = None
    unlock_bosses: List[HatsuneEventBossStatus] = None
    unlock_boss_id_list: List[int] = None
class HatsuneQuestRetireResponse(ResponseBase):
    pass
class HatsuneQuestSkipResponse(ResponseBase):
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    flag_exchange_team_exp: bool = None
    quest_result_list: List[QuestResult] = None
    bonus_reward_list: List[InventoryInfo] = None
    user_gold: UserGold = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    item_list: List[InventoryInfo] = None
    daily_clear_count: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    clan_point: ClanPoint = None
    state_exchange_stamina: eExchangeStaminaState = None
    unlock_dear_story_id: int = None
    release_diary_ids: List[int] = None
    release_nyx_story_ids: List[int] = None
class HatsuneQuestStartResponse(ResponseBase):
    quest_wave_info: List[WaveEnemyInfoList] = None
    user_info: UserStaminaInfo = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    battle_log_id: int = None
    seed: int = None
    user_gold: UserGold = None
    support_position: int = None
class HatsuneQuestTopResponse(ResponseBase):
    quest_list: List[HatsuneUserEventQuest] = None
    quiz: List[EventQuizInfo] = None
    release_diary_ids: List[int] = None
    bosses: List[HatsuneEventBossStatus] = None
    boss_battle_info: List[HatsuneEventBossStatus] = None
    boss_enemy_info: List[HatsuneEventBossEnemyInfo] = None
class HatsuneQuizAnswerResponse(ResponseBase):
    is_correct: int = None
    unlock_quest_list: List[int] = None
    unlock_quiz: List[int] = None
    add_present_count: int = None
class HatsuneReadDiaryResponse(ResponseBase):
    pass
class HatsuneReadNyxStoryResponse(ResponseBase):
    pass
class HatsuneReadOmpStoryResponse(ResponseBase):
    add_present_count: int = None
class HatsuneReadRelayStoryResponse(ResponseBase):
    pass
class HatsuneRecoverChallengeResponse(ResponseBase):
    user_jewel: UserJewel = None
    user_quest: QuestRecoverInfo = None
class HatsuneSpecialBattleExFinishResponse(ResponseBase):
    result_type: int = None
    chat_battle_log_flag: int = None
    damage_result: int = None
class HatsuneSpecialBattleExHistoryResponse(ResponseBase):
    total_attack_count: int = None
    clear_time: int = None
    history: List[EventSpecialBattleExHistory] = None
class HatsuneSpecialBattleExResetResponse(ResponseBase):
    special_battle_info: SpecialBattleInfo = None
class HatsuneSpecialBattleExRetireResponse(ResponseBase):
    pass
class HatsuneSpecialBattleExStartResponse(ResponseBase):
    limit_time: int = None
    battle_log_id: int = None
    enemy_info: List[EventEnemyInfo] = None
class HatsuneSpecialBattleFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    result_type: int = None
    unlock_story_id: int = None
    first_clear_rewards: List[InventoryInfo] = None
    quest_rewards: List[InventoryInfo] = None
    acquired_gold: int = None
    user_gold: UserGold = None
    item_list: List[InventoryInfo] = None
    treasure_rewards: List[InventoryInfo] = None
    unlock_unit: UnitData = None
    add_present_count: int = None
    chat_battle_log_flag: int = None
    unlock_dear_story_id: int = None
    release_nyx_story_ids: List[int] = None
    damage_result: int = None
class HatsuneSpecialBattleRetireResponse(ResponseBase):
    pass
class HatsuneSpecialBattleStartResponse(ResponseBase):
    limit_time: int = None
    battle_log_id: int = None
    enemy_info: List[EventEnemyInfo] = None
    hit_treasure_nums: List[int] = None
    hit_treasure_list: List[EventHitTreasureInfo] = None
class HatsuneTopResponse(ResponseBase):
    event_status: List[HatsuneEventStatus] = None
    additional_stories: List[HatsuneEventStoryState] = None
    boss_ticket_info: InventoryInfo = None
    event_decks: List[DeckData] = None
    login_bonus: HatsuneLoginBonusData = None
    add_present_count: int = None
    missions: List[UserMissionInfo] = None
    is_hard_quest_unlocked: bool = None
    special_battle_info: SpecialBattleInfo = None
    quiz: List[EventQuizInfo] = None
    unchoiced_dear_story_id_list: List[int] = None
    ex_mode_ranking: List[EventSpecialBattleExRankingInfo] = None
    release_minigame: List[int] = None
    release_diary_ids: List[int] = None
    series_info_list: List[HatsuneSeriesInfo] = None
    uek_mission_acceptable_flg: bool = None
    new_omp_story_ids: List[int] = None
    bosses: List[HatsuneEventBossStatus] = None
    boss_battle_info: List[HatsuneEventBossStatus] = None
    boss_enemy_info: List[HatsuneEventBossEnemyInfo] = None
class HomeIndexResponse(ResponseBase):
    unread_message_list: UnreadMessageList = None
    missions: List[UserMissionInfo] = None
    season_pack: List[UserSeasonPackInfo] = None
    daily_reset_time: int = None
    limited_shop: List[LimitedShop] = None
    daily_shop: DailyShop = None
    user_clan: UserClan = None
    have_clan_invitation: int = None
    new_equip_donation: EquipRequests = None
    have_join_request: int = None
    quest_list: List[UserQuestInfo] = None
    dungeon_info: DungeonInfo = None
    training_quest_count: TrainingQuestCount = None
    training_quest_max_count: TrainingQuestCount = None
    training_quest_pack_end_time: int = None
    have_clan_battle_reward: int = None
    gold: List[int] = None
    paid_jewel: int = None
    free_jewel: int = None
    alchemy_reward_list: List[AlchemyReward] = None
    alchemy_reward_time: int = None
    season_pack_alert: int = None
    season_pack_end_time: int = None
    daily_jewel_pack_end: int = None
    last_friend_time: LastFriendTime = None
    clan_battle_remaining_count: int = None
    campaign_target_flag: bool = None
    everyday_jewel_pack_buy: bool = None
    chara_e_ticket_purchased_times: List[CharaExchangeTicketProductData] = None
    purchased_arcade_id_list: List[int] = None
    shiori_quest_info: ShioriQuestInfo = None
    srt_story_id_list: List[int] = None
    season_ticket: SeasonPassData = None
    custom_season_pack_alert: List[int] = None
    custom_season_pack_end_time: List[int] = None

    def update(self, client: "dataclient"):
        client.finishedQuest = [q.quest_id for q in self.quest_list if q.result_type > 0]
        client.clan = self.user_clan.clan_id
        client.donation_num = self.user_clan.donation_num
        client.dungeon_area_id = self.dungeon_info.enter_area_id
        type = self.dungeon_info.dungeon_area[0].dungeon_type
        for count in self.dungeon_info.rest_challenge_count:
            if count.dungeon_type == type:
                client.dungeon_avaliable = count.count > 0
                break

class ItemETicketExchangeResponse(ResponseBase):
    reward_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    add_present_count: int = None
    upper_limit_flag: bool = None
class KaiserBattleGetMainBossInfoResponse(ResponseBase):
    main_boss_info: KaiserBossInfo = None
    deck_list: List[DeckData] = None
class KaiserBattleMainFinishResponse(ResponseBase):
    damage_result: int = None
    acquired_gold: int = None
    user_gold: UserGold = None
    boss_rewards: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    add_present_count: int = None
    attack_count: int = None
class KaiserBattleMainRetireResponse(ResponseBase):
    pass
class KaiserBattleMainStartResponse(ResponseBase):
    battle_log_id: int = None
    enemy_info: List[EventEnemyInfo] = None
    support_unit_info: List[UnitData] = None
    skin_data_for_request: List[SkinDataForRequest] = None
class KaiserBattleMySupportListResponse(ResponseBase):
    my_support_list: List[SupportUnitSetting] = None
class KaiserBattleSetSupportUnitResponse(ResponseBase):
    rewards: List[InventoryInfo] = None
    add_present_count: int = None
    my_support_info: SupportUnitSetting = None
class KaiserBattleSubFinishResponse(ResponseBase):
    damage_result: int = None
    acquired_gold: int = None
    user_gold: UserGold = None
    boss_rewards: List[InventoryInfo] = None
    add_present_count: int = None
class KaiserBattleSubStartResponse(ResponseBase):
    battle_log_id: int = None
    seed: int = None
    support_unit_info: List[UnitData] = None
    skin_data_for_request: List[SkinDataForRequest] = None
class KaiserBattleSupportListResponse(ResponseBase):
    friend_support_unit_list: List[SupportUnitStatus] = None
    general_support_unit_list: List[SupportUnitStatus] = None
class KaiserBattleTopResponse(ResponseBase):
    remaining_count: int = None
    sub_boss_list: List[KaiserBossInfo] = None
    sub_boss_reward: List[InventoryInfo] = None
    add_present_count: int = None
    extermination_boss_id_list: List[int] = None
    main_boss_info: KaiserBossInfo = None
    deck_list: List[DeckData] = None
    my_support_list: List[SupportUnitSetting] = None
class KaiserBattleUpdateDeckResponse(ResponseBase):
    pass
class KmkFinishResponse(ResponseBase):
    current_score: int = None
    total_score_all: int = None
    is_opened_extra_first: int = None
    special_reward_list: InventoryInfo = None
    kill_list: KmkKillList = None
    max_combo_count_score: int = None
    after_hp_score: int = None
    fever_score: int = None
    add_present_count: int = None
class KmkStartResponse(ResponseBase):
    play_id: int = None
    seed: int = None
class KmkTopResponse(ResponseBase):
    total_score_all: int = None
    normal_high_score: int = None
    hard_high_score: int = None
    extra_high_score: int = None
class LoadIndexResponse(ResponseBase):
    user_info: UserInfo = None
    user_jewel: UserJewel = None
    user_gold: UserGold = None
    unit_list: List[UnitData] = None
    user_chara_info: List[UserChara] = None
    deck_list: List[LoadDeckData] = None
    material_list: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    user_equip: List[InventoryInfo] = None
    today_start_level: int = None
    shop: Shop = None
    tips_id_list: List[int] = None
    ini_setting: IniSetting = None
    daily_reset_time: int = None
    present_count: int = None
    login_bonus_list: LoginBonusList = None
    max_storage_num: int = None
    can_free_gacha: int = None
    can_receive_clan_battle_reward: int = None
    campaign_list: List[int] = None
    read_story_ids: List[int] = None
    clan_like_count: int = None
    dispatch_units: List[UnitDataForClanMember] = None
    clan_battle: ClanBattleData = None
    event_statuses: List[EventStatus] = None
    tower_status: TowerStatus = None
    bgm: List[MusicIdData] = None
    unlock_story_ids: List[int] = None
    can_campaign_gacha: int = None
    can_guarantee_gacha: int = None
    can_limited_guarantee_gacha: int = None
    start_dash_fes_info_list: List[StartDashFesInfo] = None
    return_fes_info_list: List[ReturnFesInfo] = None
    growth_unit_list: List[GrowthInfo] = None
    pa: int = None
    sdg_start: int = None
    sdg_end: int = None
    cf: RaceLoginBonusInfo = None
    drj: CampaignDate = None
    gacha_point_info_list: List[GachaPointInfo] = None
    gacha_point_info: GachaPointInfo = None
    voice: UserBirthDayVoice = None
    maintenance_status: MaintenanceStatus = None
    user_my_party: List[UserMyParty] = None
    user_my_party_tab: List[UserMyPartyTab] = None
    user_my_quest: List[UserMyQuest] = None
    csc: CounterStopCoinExchange = None
    tt: int = None
    cgl: int = None
    ab: int = None
    ebm: int = None
    lsm: int = None
    last_login_bonus_time: int = None
    friend_support_units: List[SupportUnitSetting] = None
    my_page_exists: bool = None
    my_page: List[MyPage] = None
    limit_still_ids: List[int] = None
    read_diary_ids: List[int] = None
    unlock_diary_ids: List[int] = None
    read_relay_story_ids: List[int] = None
    unlock_relay_story_ids: List[int] = None
    read_omp_story_ids: List[int] = None
    unlock_omp_story_ids: List[int] = None
    read_nyx_story_ids: List[int] = None
    unlock_nyx_story_ids: List[int] = None
    nyx_color_id: int = None
    cbm: int = None
    csm: int = None
    cbs: int = None
    tbm: int = None
    dbm: int = None
    fst: int = None
    force_release_chapter: int = None
    cr: int = None
    fsr: int = None
    sfr: int = None
    pff: int = None
    een_n: int = None
    een_r: int = None
    serialcode_restrict_release_time: int = None
    chr: int = None
    nls: int = None
    event_sub_story: List[EventSubStory] = None
    evmb: int = None
    gi: int = None
    erdr: int = None
    lbme: int = None

    def update(self, client: "dataclient"):
        client.name = self.user_info.user_name
        client.team_level = self.user_info.team_level
        client.jewel = self.user_jewel.free_jewel
        client.clear_inventory()
        if self.item_list:
            for inv in self.item_list:
                client.update_inventory(inv)
        if self.material_list:
            for inv in self.material_list:
                client.update_inventory(inv)
        if self.user_equip:
            for inv in self.user_equip:
                client.update_inventory(inv)
        client.stamina = self.user_info.user_stamina
        client.settings = self.ini_setting


class LoadNextDayIndexResponse(ResponseBase):
    daily_reset_time: int = None
    login_bonus_list: LoginBonusList = None
    can_free_gacha: int = None
    can_receive_clan_battle_reward: int = None
    campaign_list: List[int] = None
    present_count: int = None
    shop: Shop = None
    event_statuses: List[EventStatus] = None
    can_campaign_gacha: int = None
    dispatch_units: List[UnitDataForClanMember] = None
    cf: RaceLoginBonusInfo = None
    maintenance_status: MaintenanceStatus = None
    csc: CounterStopCoinExchange = None
    friend_support_units: List[SupportUnitSetting] = None
    start_dash_fes_info_list: List[StartDashFesInfo] = None
    return_fes_info_list: List[ReturnFesInfo] = None
    unlock_story_ids: List[int] = None
class MissionAcceptResponse(ResponseBase):
    team_level: int = None
    team_exp: int = None
    stamina_info: UserStaminaInfo = None
    rewards: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
    release_contents: List[ReleaseContentData] = None
    room_item_level_mission: List[int] = None

    def update(self, client: "dataclient"):
        if self.rewards:
            for item in self.rewards:
                client.update_inventory(item)
        client.stamina = self.stamina_info.user_stamina

class MissionIndexResponse(ResponseBase):
    missions: List[UserMissionInfo] = None
    season_pack: List[UserSeasonPackInfo] = None
    daily_reset_time: int = None
class MultiUnlockRaritySixSlotResponse(ResponseBase):
    unit_data: UnitData = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class MusicBuyResponse(ResponseBase):
    music_id: int = None
    purchased_time: int = None
    item_data: List[InventoryInfo] = None
class MusicSetResponse(ResponseBase):
    pass
class MusicTopResponse(ResponseBase):
    bgm_keys: List[int] = None
    music_list_purchased: List[MusicPurchasedData] = None
class MyPageSetMyPageResponse(ResponseBase):
    pass
class OtherClanInfoResponse(ResponseBase):
    clan: OtherClanData = None
    current_clan_battle_mode: int = None
    current_battle_joined: int = None
class PctFinishResponse(ResponseBase):
    bonus_list: List[PctBonusInfo] = None
    final_pct_point: int = None
    after_pct_point: int = None
    after_pct_unit_point: PctUnitPointInfo = None
    add_present_count: int = None
class PctStartResponse(ResponseBase):
    seed: int = None
    pct_play_id: int = None
class PctTopResponse(ResponseBase):
    pct_point: int = None
    unit_pct_point_list: List[PctUnitPointInfo] = None
    cacao_list: List[PctCacaoInfo] = None
class PictureBookResponse(ResponseBase):
    item_list: List[InventoryInfoShort] = None
    user_equip: List[InventoryInfoShort] = None
class PkbFinishSoloResponse(ResponseBase):
    current_score: int = None
    total_score: int = None
    special_reward_list: List[InventoryInfo] = None
    add_present_count: int = None
class PkbFinishVsResponse(ResponseBase):
    current_score: int = None
    total_score: int = None
    special_reward_list: List[InventoryInfo] = None
    add_present_count: int = None
class PkbReadCatalogResponse(ResponseBase):
    pass
class PkbReadRankingResponse(ResponseBase):
    pass
class PkbStartSoloResponse(ResponseBase):
    play_id: int = None
    seed: int = None
class PkbStartVsResponse(ResponseBase):
    play_id: int = None
    seed: int = None
class PkbTopResponse(ResponseBase):
    total_score: int = None
    total_score_solo: int = None
    total_score_vs: int = None
    solo_high_score_info: PkbHighScoreInfo = None
    vs_high_score_info: PkbHighScoreInfo = None
    simple_solo_high_score_info: PkbHighScoreInfo = None
    simple_vs_high_score_info: PkbHighScoreInfo = None
    catalog_info: PkbCatalogInfo = None
    ranking_info: PkbRankingInfo = None
    simple_ranking_info: PkbRankingInfo = None
class PresentHistoryResponse(ResponseBase):
    present_history: List[PresentHistoryInfo] = None
class PresentIndexResponse(ResponseBase):
    present_info_list: List[PresentParameter] = None
    present_count: int = None
class PresentReceiveAllResponse(ResponseBase):
    rewards: List[InventoryInfo] = None
    stamina_info: UserStaminaInfo = None
    flag_over_limit: int = None
    flag_expiration: int = None
    present_info_list: List[PresentParameter] = None
    arena_count_info: ArenaCountInfo = None
    grand_arena_count_info: GrandArenaCountInfo = None

    def update(self, client: "dataclient"):
        if self.rewards:
            for item in self.rewards:
                client.update_inventory(item)
        client.stamina = self.stamina_info.user_stamina

class PresentReceiveSingleResponse(ResponseBase):
    rewards: List[InventoryInfo] = None
    stamina_info: UserStaminaInfo = None
    flag_over_limit: int = None
    flag_expiration: int = None
    arena_count_info: ArenaCountInfo = None
    grand_arena_count_info: GrandArenaCountInfo = None
class ProfileFavoriteUnitResponse(ResponseBase):
    pass
class ProfileGetResponse(ResponseBase):
    user_info: ProfileUserInfo = None
    quest_info: ProfileQuestInfo = None
    favorite_unit: UnitDataForView = None
    clan_name: str = None
    own_clan_role: int = None
    clan_invite_result_code: int = None
    invite_enable_time: int = None
    friend_support_units: List[SupportUnitForProfile] = None
    clan_support_units: List[SupportUnitForProfile] = None
    campaign_target_list: List[CampaignTarget] = None
class ProfileMakerGetClanProfileResponse(ResponseBase):
    profile: ClanProfileCardSetting = None
    clan: ClanProfileCardClanInfo = None
class ProfileMakerGetMyProfileResponse(ResponseBase):
    profile: MyProfileCardSetting = None
    score: MyProfileCardScore = None
class ProfileMakerSetClanProfileResponse(ResponseBase):
    pass
class ProfileMakerSetMyProfileResponse(ResponseBase):
    pass
class ProfileRenameResponse(ResponseBase):
    pass
class ProfileSetBirthDayResponse(ResponseBase):
    birthday: int = None
    birthday_period: int = None
class ProfileUpdateCommentResponse(ResponseBase):
    pass
class QuestFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    reward_list: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    unlock_quest_list: List[int] = None
    unlock_dungeon_area_id: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    open_story_ids: List[UserStory] = None
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    daily_clear_count: int = None
    add_present_count: int = None
    release_contents: List[ReleaseContentData] = None
    clan_point: ClanPoint = None
    state_exchange_stamina: eExchangeStaminaState = None
    user_gold: UserGold = None
class QuestRecoverChallengeMultipleResponse(ResponseBase):
    user_jewel: UserJewel = None
    user_quest: List[QuestRecoverInfo] = None
class QuestRecoverChallengeResponse(ResponseBase):
    user_jewel: UserJewel = None
    user_quest: QuestRecoverInfo = None
class QuestReplayListResponse(ResponseBase):
    replay_list: List[QuestReplayData] = None
class QuestReplayResponse(ResponseBase):
    user_unit_list: List[UnitData] = None
    quest_wave_info: List[WaveEnemyInfoList] = None
    enemy_list: List[UnitData] = None
class QuestReplayReportResponse(ResponseBase):
    pass
class QuestRetireResponse(ResponseBase):
    pass
class QuestSkipMultipleResponse(ResponseBase):
    quest_result_list: List[QuestResultList] = None
    bonus_reward_list: List[InventoryInfo] = None
    level_info: LevelInfo = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    user_info: UserStaminaInfo = None
    daily_clear_count: int = None
    daily_challenge_count: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
    clan_point: ClanPoint = None
    state_exchange_stamina: eExchangeStaminaState = None
class QuestSkipResponse(ResponseBase):
    quest_result_list: List[QuestResult] = None
    bonus_reward_list: List[InventoryInfo] = None
    level_info: LevelInfo = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    user_info: UserStaminaInfo = None
    daily_clear_count: int = None
    daily_challenge_count: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
    clan_point: ClanPoint = None
    state_exchange_stamina: eExchangeStaminaState = None

    def update(self, client: "dataclient"):
        if self.item_list:
            for item in self.item_list:
                client.update_inventory(item)
        if self.bonus_reward_list:
            for item in self.bonus_reward_list:
                client.update_inventory(item)
        if self.item_data:
            for item in self.item_data:
                client.update_inventory(item)
        if self.quest_result_list:
            for result in self.quest_result_list:
                for item in result.reward_list:
                    client.update_inventory(item)
        client.stamina = self.user_info.user_stamina

class QuestStartResponse(ResponseBase):
    quest_wave_info: List[WaveEnemyInfoList] = None
    limit_time: int = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    user_info: UserStaminaInfo = None
    battle_log_id: int = None
    seed: int = None
    skin_data_for_request: List[SkinDataForRequest] = None
    user_gold: UserGold = None
    support_position: int = None
    sub_drop: List[InventoryInfo] = None
class RaceLoginBonusCharaSelectDataResponse(ResponseBase):
    reward_list: List[InventoryInfo] = None
    add_present_count: int = None
class RaritySixQuestFinishResponse(ResponseBase):
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    add_present_count: int = None
class RaritySixQuestStartResponse(ResponseBase):
    limit_time: int = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    battle_log_id: int = None
    seed: int = None
    skin_data_for_request: List[SkinDataForRequest] = None
class RoomClanMemberResponse(ResponseBase):
    clan_members: List[RoomUserInfo] = None
class RoomExtendStorageResponse(ResponseBase):
    max_storage_num: int = None
    user_jewel: UserJewel = None
class RoomFreeGiftResponse(ResponseBase):
    level_info: LevelInfo = None
class RoomGiveGiftResponse(ResponseBase):
    level_info: LevelInfo = None
    user_gift_item_list: List[InventoryInfo] = None
class RoomItemBuyResponse(ResponseBase):
    user_room_item_list: List[RoomUserItem] = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class RoomItemSellResponse(ResponseBase):
    user_room_item_list: List[RoomUserItem] = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
    add_present_count: int = None
class RoomLevelUpEndResponse(ResponseBase):
    user_room_item: RoomUserItem = None
    max_exec_num_list: MaxExecNumList = None
class RoomLevelUpShorteningResponse(ResponseBase):
    user_room_item: RoomUserItem = None
    user_jewel: UserJewel = None
    max_exec_num_list: MaxExecNumList = None
class RoomLevelUpStartResponse(ResponseBase):
    user_room_item: RoomUserItem = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class RoomLevelUpStopResponse(ResponseBase):
    user_room_item: RoomUserItem = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
    add_present_count: int = None
class RoomLikeHistoryResponse(ResponseBase):
    total_like: int = None
    total_be_liked: int = None
    today_like_count: int = None
    today_be_liked_count: int = None
    like_history: List[RoomUserInfo] = None
    unread_count: int = None
    be_liked_history: List[RoomUserInfo] = None
    reward_list: List[InventoryInfo] = None
class RoomLikeResponse(ResponseBase):
    total_like: int = None
    daily_like: int = None
    like_history: List[RoomUserInfo] = None
    reward_list: List[InventoryInfo] = None
    room_user_info: RoomUserInfo = None
class RoomMultiGiveGiftResponse(ResponseBase):
    level_info: LevelInfo = None
    user_gift_item_list: List[InventoryInfo] = None
class RoomMultiLevelUpEndResponse(ResponseBase):
    user_room_item_list: List[RoomUserItem] = None
class RoomMysetDeleteResponse(ResponseBase):
    pass
class RoomMysetListResponse(ResponseBase):
    myset_list: List[RoomMysetElement] = None
class RoomMysetRenameResponse(ResponseBase):
    pass
class RoomMysetSaveResponse(ResponseBase):
    myset_update_time: str = None
class RoomReceiveItemAllResponse(ResponseBase):
    user_room_item_list: List[RoomUserItem] = None
    reward_list: List[InventoryInfo] = None
    stamina_info: UserStaminaInfo = None
    add_present_count: int = None

    def update(self, client: "dataclient"):
        client.stamina = self.stamina_info.user_stamina

class RoomReceiveItemResponse(ResponseBase):
    user_room_item: RoomUserItem = None
    reward_list: List[InventoryInfo] = None
    stamina_info: UserStaminaInfo = None
    add_present_count: int = None
class RoomStartResponse(ResponseBase):
    room_layout: RoomWholeLayout = None
    max_storage_num: int = None
    unread_count: int = None
    user_room_item_list: List[RoomUserItem] = None
    event_room_item_get_time_list: List[RoomItemGetTime] = None
class RoomUpdateResponse(ResponseBase):
    user_room_item_list: List[RoomUserItem] = None
class RoomVisitResponse(ResponseBase):
    room_layout: RoomWholeLayout = None
    user_room_item_list: List[RoomUserItem] = None
    room_user_info: RoomUserInfo = None
    deck_list: List[DeckListDataForView] = None
    unread_count: int = None
    extension_key: RoomExtensionItem = None
class SeasonPassBuyLevelResponse(ResponseBase):
    user_jewel: UserJewel = None
    seasonpass_level: int = None
    user_point: int = None
    point_limit_flag: int = None
    exchange_rewards: List[ExchangeRewards] = None
class SeasonPassIndexResponse(ResponseBase):
    is_buy: int = None
    seasonpass_level: int = None
    user_point: int = None
    weekly_point: int = None
    missions: List[UserMissionInfo] = None
    received_rewards: List[int] = None
    daily_reset_time: int = None
    weekly_reset_time: int = None
class SeasonPassMissionAcceptResponse(ResponseBase):
    seasonpass_level: int = None
    user_point: int = None
    weekly_point: int = None
    point_limit_flag: int = None
    exchange_rewards: List[ExchangeRewards] = None
    rewards: List[InventoryInfo] = None
    add_present_count: int = None
    release_contents: List[ReleaseContentData] = None
    room_item_level_mission: List[int] = None
class SeasonPassRewardAcceptResponse(ResponseBase):
    stamina_info: UserStaminaInfo = None
    rewards: List[InventoryInfo] = None
    add_present_count: int = None
    received_rewards: List[int] = None
class SekaiBossInfoResponse(ResponseBase):
    damage_history: DamageHistory = None
    current_hp: int = None
class SekaiFinishResponse(ResponseBase):
    pass
class SekaiHistoryReportResponse(ResponseBase):
    history_report: List[HistoryReport] = None
class SekaiRankingInClanResponse(ResponseBase):
    sekai_id: int = None
    my_rank: int = None
    my_damage: int = None
    ranking: List[SekaiRanking] = None
class SekaiRankingResponse(ResponseBase):
    sekai_id: int = None
    my_rank: int = None
    my_damage: int = None
    ranking: List[SekaiRanking] = None
class SekaiRetireResponse(ResponseBase):
    sekai_id: int = None
    my_rank: int = None
    my_damage: int = None
    ranking: List[SekaiRanking] = None
class SekaiStartResponse(ResponseBase):
    enemy_data: UnitData = None
    battle_log_id: int = None
    current_hp: int = None
    user_unit: List[UnitData] = None
    seed: int = None
class SekaiSupportUnitList2Response(ResponseBase):
    support_unit_list: List[ClanBattleSupportUnitLight] = None
class SekaiTopResponse(ResponseBase):
    sekai_id: int = None
    current_hp: int = None
    damage_history: List[DamageHistory] = None
    rank: int = None
    remaining_count: int = None
class SellItemResponse(ResponseBase):
    item_list: List[InventoryInfo] = None
    material_list: List[InventoryInfo] = None
    user_equip: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
    add_present_count: int = None
class SendBattleLogCsvResponse(ResponseBase):
    pass
class SerialCodeRegisterResponse(ResponseBase):
    reward_list: List[InventoryInfo] = None
    serial_campaign_id: int = None
    group_reward_list: List[InventoryInfo] = None
    serial_group_id: int = None
    add_present_count: int = None
class SetMyPartyResponse(ResponseBase):
    pass
class SetMyPartyTabResponse(ResponseBase):
    pass
class ShioriBossBattleFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    result_type: int = None
    unlock_quest_list: List[int] = None
    unlock_bosses: List[HatsuneEventBossStatus] = None
    unlock_story_id: int = None
    unlock_story_id_list: List[int] = None
    quest_rewards: List[InventoryInfo] = None
    first_clear_rewards: List[InventoryInfo] = None
    acquired_gold: int = None
    user_gold: UserGold = None
    damage_result: int = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    treasure_rewards: List[InventoryInfo] = None
    next_boss: HatsuneEventBossStatus = None
    item_list: List[InventoryInfo] = None
    unlock_unit: UnitData = None
    event_present_list: List[int] = None
    new_dear_story_id_list: List[int] = None
    release_diary_ids: List[int] = None
    new_omp_story_ids: List[int] = None
class ShioriBossBattleRetireResponse(ResponseBase):
    pass
class ShioriBossBattleStartResponse(ResponseBase):
    boss_unit_data: UnitData = None
    limit_time: int = None
    hit_treasure_nums: List[int] = None
    battle_log_id: int = None
    seed: int = None
class ShioriDearFinishResponse(ResponseBase):
    before_dear_point_info: DearPointInfo = None
    after_dear_point_info: DearPointInfo = None
    add_present_count: int = None
class ShioriDearTopResponse(ResponseBase):
    unlock_dear_story_info_list: List[DearStoryInfo] = None
    dear_point_info_list: List[DearPointInfo] = None
class ShioriEventTopResponse(ResponseBase):
    bosses: List[HatsuneEventBossStatus] = None
    event_decks: List[DeckData] = None
    login_count: int = None
    missions: List[UserMissionInfo] = None
    quest_list: List[UserQuestInfo] = None
    quiz: List[EventQuizInfo] = None
    unchoiced_dear_story_id_list: List[int] = None
    release_diary_ids: List[int] = None
    series_info_list: List[HatsuneSeriesInfo] = None
class ShioriFavoriteResponse(ResponseBase):
    pass
class ShioriMissionAcceptResponse(ResponseBase):
    team_level: int = None
    team_exp: int = None
    stamina_info: UserStaminaInfo = None
    rewards: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
    release_contents: List[ReleaseContentData] = None
class ShioriMissionIndexResponse(ResponseBase):
    missions: List[UserMissionInfo] = None
    season_pack: List[UserSeasonPackInfo] = None
    daily_reset_time: int = None
class ShioriQuestFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    reward_list: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    unlock_quest_list: List[int] = None
    unlock_bosses: List[HatsuneEventBossStatus] = None
    unlock_story_id: int = None
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    daily_clear_count: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    has_drop: int = None
    clan_point: ClanPoint = None
    drop_rewards: List[InventoryInfo] = None
    event_present_list: List[int] = None
    unlock_quiz: List[int] = None
    state_exchange_stamina: eExchangeStaminaState = None
    release_diary_ids: List[int] = None
    new_relay_story_ids: List[int] = None
    new_omp_story_ids: List[int] = None
    user_gold: UserGold = None
class ShioriQuestRetireResponse(ResponseBase):
    pass
class ShioriQuestSkipResponse(ResponseBase):
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    flag_exchange_team_exp: bool = None
    quest_result_list: List[QuestResult] = None
    bonus_reward_list: List[InventoryInfo] = None
    user_gold: UserGold = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    item_list: List[InventoryInfo] = None
    daily_clear_count: int = None
    limited_shop_list: List[LimitedShop] = None
    daily_shop: DailyShop = None
    clan_point: ClanPoint = None
    state_exchange_stamina: eExchangeStaminaState = None
    release_diary_ids: List[int] = None
class ShioriQuestStartResponse(ResponseBase):
    quest_wave_info: List[WaveEnemyInfoList] = None
    user_info: UserStaminaInfo = None
    quest_id: int = None
    battle_log_id: int = None
    seed: int = None
    user_gold: UserGold = None
    support_position: int = None
class ShioriQuizAnswerResponse(ResponseBase):
    is_correct: int = None
    unlock_quest_list: List[int] = None
    unlock_quiz: List[int] = None
    add_present_count: int = None
class ShioriTopResponse(ResponseBase):
    new_event_list: List[int] = None
    clear_event_list: List[int] = None
    my_select_list: List[int] = None
class ShopAlchemyResponse(ResponseBase):
    team_level: int = None
    gold: List[int] = None
    alchemy_reward_list: List[AlchemyReward] = None
    paid_jewel: int = None
    free_jewel: int = None
    paid_gold: int = None
    free_gold: int = None
    alchemy: Alchemy = None
    user_jewel: UserJewel = None
    user_gold: UserGold = None
    alchemy_reward_time: int = None
class ShopBuyMultipleResponse(ResponseBase):
    purchase_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
class ShopBuyResponse(ResponseBase):
    purchase_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
    user_jewel: UserJewel = None
class ShopCloseDailyShopResponse(ResponseBase):
    pass
class ShopCloseLimitedShopResponse(ResponseBase):
    pass
class ShopComebackTutorialDailyShopResponse(ResponseBase):
    daily_shop: DailyShop = None
class ShopItemListResponse(ResponseBase):
    shop_list: List[ShopInfo] = None
    is_got_csc: int = None
class ShopRecoverStaminaResponse(ResponseBase):
    recover_stamina: RecoverStamina = None
    user_jewel: UserJewel = None
    user_info: UserStaminaInfo = None

    def update(self, client: "dataclient"):
        client.jewel = self.user_jewel.free_jewel
        client.stamina = self.user_info.user_stamina

class ShopResetResponse(ResponseBase):
    shop: ShopInfo = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
    user_jewel: UserJewel = None
class SkillLevelUpResponse(ResponseBase):
    unit_data: UnitData = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class SkillRemoveFreeResponse(ResponseBase):
    unit_data: UnitData = None
class SkillSetFreeResponse(ResponseBase):
    unit_data: UnitData = None
class SpaceFinishResponse(ResponseBase):
    damage_result: int = None
    rewards: List[InventoryInfo] = None
    user_gold: UserGold = None
    add_present_count: int = None
class SpaceRetireResponse(ResponseBase):
    pass
class SpaceStartResponse(ResponseBase):
    boss_unit_data: UnitData = None
    limit_time: int = None
    battle_log_id: int = None
    seed: int = None
class SpaceStoryCheckResponse(ResponseBase):
    pass
class SpaceStoryStartResponse(ResponseBase):
    pass
class SpaceSupportUnitList2Response(ResponseBase):
    support_unit_list: List[ClanBattleSupportUnitLight] = None
class SpaceTopResponse(ResponseBase):
    space_id: int = None
    progress: int = None
    space_battle_id: int = None
    boss_hp: int = None
class SrtFinishResponse(ResponseBase):
    turn_num_bonus: int = None
    answer_time_bonus: int = None
    wrong_num_bonus: int = None
    current_score: int = None
    total_score_all: int = None
    special_reward_list: List[InventoryInfo] = None
    add_present_count: int = None
class SrtReadCatalogResponse(ResponseBase):
    pass
class SrtStartResponse(ResponseBase):
    play_id: int = None
    seed: int = None
    answer_limit_time: int = None
class SrtTopResponse(ResponseBase):
    total_score_all: int = None
    high_score_info: SrtHighScoreInfo = None
    catalog_info: List[SrtCatalogInfo] = None
class StoryForceReleaseResponse(ResponseBase):
    pass
class StoryMaintenanceCheckResponse(ResponseBase):
    pass
class StoryQuestStartResponse(ResponseBase):
    quest_wave_info: List[WaveEnemyInfoList] = None
    limit_time: int = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    user_info: UserStaminaInfo = None
    guest_data: List[UnitData] = None
class StoryViewingResponse(ResponseBase):
    reward_info: List[InventoryInfo] = None
    release_contents: List[ReleaseContentData] = None
    add_present_count: int = None
    unlock_story_ids: List[int] = None
    event_id: int = None
    unlocked_sub_story_list: List[int] = None
class SubStoryLtoReadStoryResponse(ResponseBase):
    reward_info: List[InventoryInfo] = None
class SubStorySkeConfirmResponse(ResponseBase):
    pass
class SubStorySkeReadStoryResponse(ResponseBase):
    new_sub_story_info: EventSubStoryInfo = None
class SubStorySspReadSspStoryResponse(ResponseBase):
    pass
class SupportUnitChangeSettingResponse(ResponseBase):
    support_units: SupportUnitSetting = None
    support_time_bonus: List[InventoryInfo] = None
    support_count_bonus: List[InventoryInfo] = None
    add_present_count: int = None
class SupportUnitGetSettingResponse(ResponseBase):
    friend_support_units: List[SupportUnitSetting] = None
    clan_support_units: List[SupportUnitSetting] = None
    clan_support_available_status: int = None
class TestBuyTicketResponse(ResponseBase):
    ticket_status: int = None
class TowerBattleFinishResponse(ResponseBase):
    quest_id: int = None
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    user_gold: UserGold = None
    flag_exchange_team_exp: bool = None
    reward_list: List[InventoryInfo] = None
    add_present_count: int = None
    clan_point: ClanPoint = None
    clan_member_info: List[TowerClanMemberInfo] = None
    is_joined_clan: int = None
class TowerBattleRetireResponse(ResponseBase):
    clan_member_info: List[TowerClanMemberInfo] = None
    is_joined_clan: int = None
class TowerBattleSkipResponse(ResponseBase):
    user_gold: UserGold = None
    add_present_count: int = None
class TowerBattleStartResponse(ResponseBase):
    user_unit: List[UnitData] = None
    versus_user_unit: List[UnitData] = None
    user_info: UserStaminaInfo = None
    user_gold: UserGold = None
    battle_log_id: int = None
    seed: int = None
    support_unit_hp: int = None
class TowerCloisterBattleFinishResponse(ResponseBase):
    quest_id: int = None
    user_gold: UserGold = None
    add_present_count: int = None
    clan_member_info: List[TowerClanMemberInfo] = None
    cloister_remain_clear_count: int = None
    is_joined_clan: int = None
class TowerCloisterBattleRetireResponse(ResponseBase):
    clan_member_info: List[TowerClanMemberInfo] = None
    is_joined_clan: int = None
class TowerCloisterBattleStartResponse(ResponseBase):
    user_unit: List[UnitData] = None
    versus_user_unit1: List[UnitData] = None
    versus_user_unit2: List[UnitData] = None
    versus_user_unit3: List[UnitData] = None
    user_gold: UserGold = None
    battle_log_id: int = None
    seed: int = None
    reward_list: List[InventoryInfo] = None
    support_unit_hp: int = None
class TowerExBattleFinishResponse(ResponseBase):
    quest_id: int = None
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    user_gold: UserGold = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
    clan_point: ClanPoint = None
    clan_member_info: List[TowerClanMemberInfo] = None
    is_joined_clan: int = None
class TowerExBattleRetireResponse(ResponseBase):
    pass
class TowerExBattleStartResponse(ResponseBase):
    battle_log_ids: List[int] = None
    seed_list: List[int] = None
    user_party_list: TowerExPartyInfo = None
    versus_user_unit: List[UnitData] = None
    user_info: UserStaminaInfo = None
    user_gold: UserGold = None
class TowerExSupportUnitList2Response(ResponseBase):
    support_unit_list: List[TowerExDispatchUnitLight] = None
class TowerExSupportUnitListResponse(ResponseBase):
    support_unit_list: List[TowerExDispatchUnit] = None
class TowerRehearsalFinishResponse(ResponseBase):
    clan_member_info: List[TowerClanMemberInfo] = None
    is_joined_clan: int = None
class TowerRehearsalRetireResponse(ResponseBase):
    clan_member_info: List[TowerClanMemberInfo] = None
    is_joined_clan: int = None
class TowerRehearsalStartResponse(ResponseBase):
    user_unit: List[UnitData] = None
    versus_user_unit: List[UnitData] = None
    battle_log_id: int = None
    seed: int = None
    support_unit_hp: int = None
class TowerReplayListResponse(ResponseBase):
    replay_list: List[TowerReplaySummary] = None
class TowerReplayResponse(ResponseBase):
    seed_list: List[int] = None
    party_status_list: TowerReplayPartyStatusList = None
    party_list: TowerReplayPartyList = None
    versus_user_unit: List[UnitData] = None
class TowerReplayReportResponse(ResponseBase):
    pass
class TowerResetResponse(ResponseBase):
    remain_reset_count: int = None
class TowerSupportUnitList2Response(ResponseBase):
    support_unit_list: List[ClanDispatchUnitLight] = None
class TowerSupportUnitListResponse(ResponseBase):
    support_unit_list: List[ClanDispatchUnit] = None
class TowerTopResponse(ResponseBase):
    next_quest_id: int = None
    user_unit: List[TowerUnit] = None
    versus_user_unit: List[TowerUnit] = None
    clan_member_info: List[TowerClanMemberInfo] = None
    remain_reset_count: int = None
    cleared_ex_quest_ids: List[int] = None
    is_joined_clan: int = None
    last_login_schedule_id: int = None
    wave: int = None
    cloister_remain_clear_count: int = None
    cloister_first_cleared_flag: int = None
class TrainingQuestFinishResponse(ResponseBase):
    level_info: LevelInfo = None
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    quest_challenge_count: TrainingQuestCount = None
    rewards: List[InventoryInfo] = None
    add_present_count: int = None
    user_info: UserStaminaInfo = None
    user_gold: UserGold = None
class TrainingQuestRetireResponse(ResponseBase):
    pass
class TrainingQuestSkipResponse(ResponseBase):
    quest_result_list: List[QuestResult] = None
    bonus_reward_list: List[InventoryInfo] = None
    level_info: LevelInfo = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    user_info: UserStaminaInfo = None
    daily_clear_count: int = None
    quest_challenge_count: TrainingQuestCount = None
    add_present_count: int = None
class TrainingQuestStartResponse(ResponseBase):
    quest_wave_info: List[WaveEnemyInfoList] = None
    limit_time: int = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    user_info: UserStaminaInfo = None
    battle_log_id: int = None
    skin_data_for_request: List[SkinDataForRequest] = None
    seed: int = None
    user_gold: UserGold = None
    support_position: int = None
class TtkChooseWeaponResponse(ResponseBase):
    pass
class TtkFinishResponse(ResponseBase):
    life_num_bonus: int = None
    coin_num_bonus: int = None
    current_score: int = None
    total_score_all: int = None
    special_reward_list: List[InventoryInfo] = None
    add_present_count: int = None
class TtkReadCatalogResponse(ResponseBase):
    pass
class TtkReadStoryResponse(ResponseBase):
    pass
class TtkStartResponse(ResponseBase):
    play_id: int = None
    seed: int = None
class TtkTopResponse(ResponseBase):
    total_score_all: int = None
    high_score_info: TtkHighScoreInfo = None
    total_coin: int = None
    weapon_in_equipment: int = None
    unlocked_ttk_story_ids: List[int] = None
    read_ttk_story_ids: List[int] = None
    catalog_info: List[TtkCatalogInfo] = None
    condition_emblem_coin: int = None
class TutorialUpdateResponse(ResponseBase):
    step: int = None
    reward_info_list: List[InventoryInfo] = None
    deck_list: List[DeckData] = None
    stamina_info: UserStaminaInfo = None
    prologue_first: PrologueFirstStep = None
    prologue_latter_d: PrologueLatterDStep = None
    quest_one: QuestOneStep = None
    equip: EquipStep = None
    gacha: GachaStep = None
    quest_two: QuestTwoStep = None
    mission: MissionStep = None
class UekBossBattleFinishResponse(ResponseBase):
    result_type: int = None
    damage_result: int = None
    treasure_rewards: List[InventoryInfo] = None
class UekBossBattleRetireResponse(ResponseBase):
    pass
class UekBossBattleStartResponse(ResponseBase):
    battle_log_id: int = None
    seed: int = None
class UekTopResponse(ResponseBase):
    current_area: int = None
    missions: List[UserMissionInfo] = None
    boss_info: UekBossInfo = None
    rewards: List[InventoryInfo] = None
    add_present_count: int = None
    upper_limit_flag: bool = None
    unlocked_uek_story_ids: List[int] = None
class UniqueEquipCraftResponse(ResponseBase):
    equip_list: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
    user_gold: UserGold = None
class UniqueEquipEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    user_gold: UserGold = None
    item_list: List[InventoryInfo] = None
class UniqueEquipMultiEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    user_gold: UserGold = None
    equip_list: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
class UniqueEquipRankupResponse(ResponseBase):
    unit_data: UnitData = None
    user_gold: UserGold = None
    equip_list: List[InventoryInfo] = None
    item_list: List[InventoryInfo] = None
class UnitCraftEquipResponse(ResponseBase):
    unit_data: UnitData = None
    equip_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
class UnitCraftEquipUniqueResponse(ResponseBase):
    unit_data: UnitData = None
    equip_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    user_gold: UserGold = None
class UnitEquipResponse(ResponseBase):
    unit_data: UnitData = None
    equip_data: InventoryInfo = None
class UnitEvolutionRaritySixResponse(ResponseBase):
    unit_data: UnitData = None
class UnitEvolutionResponse(ResponseBase):
    unit_data_list: List[UnitData] = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class UnitFavoriteResponse(ResponseBase):
    pass
class UnitFreeAutomaticEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    equip_list: List[InventoryInfo] = None
class UnitFreeEquipResponse(ResponseBase):
    unit_data: UnitData = None
    equip_list: List[InventoryInfo] = None
class UnitFreeEvolutionResponse(ResponseBase):
    unit_data: UnitData = None
class UnitFreeLevelUpResponse(ResponseBase):
    unit_data: UnitData = None
class UnitFreeMultiEvolutionResponse(ResponseBase):
    unit_data: UnitData = None
class UnitFreePromotionResponse(ResponseBase):
    unit_data: UnitData = None
    refund_items: List[InventoryInfo] = None
    add_present_count: int = None
    equip_list: List[InventoryInfo] = None
class UnitGrowthEnhanceResponse(ResponseBase):
    unit_data: UnitData = None
    refund_items: List[InventoryInfo] = None
    add_present_count: int = None
    equip_list: List[InventoryInfo] = None
class UnitMultiEquipResponse(ResponseBase):
    unit_data: UnitData = None
    equip_list: List[InventoryInfo] = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class UnitMultiEvolutionResponse(ResponseBase):
    unit_data_list: List[UnitData] = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class UnitMultiPromotionResponse(ResponseBase):
    equip_list: List[InventoryInfo] = None
    item_data: List[InventoryInfo] = None
    refund_items: List[InventoryInfo] = None
    unit_data: UnitData = None
    user_gold: UserGold = None
    add_present_count: int = None
class UnitPromotionResponse(ResponseBase):
    unit_data: UnitData = None
    refund_items: List[InventoryInfo] = None
    add_present_count: int = None
class UnitSetGrowthItemResponse(ResponseBase):
    item_data: List[InventoryInfo] = None
    growth_unit_info: GrowthInfo = None
class UnitUniqueEquipResponse(ResponseBase):
    unit_data: UnitData = None
    equip_data: InventoryInfo = None
class UnlockRaritySixSlotResponse(ResponseBase):
    unit_data: UnitData = None
    user_gold: UserGold = None
    item_data: List[InventoryInfo] = None
class UnlockUnitResponse(ResponseBase):
    unit_data: UnitData = None
    item_data: List[InventoryInfo] = None
class UpdateSkipQuestListResponse(ResponseBase):
    pass
class UpdateTabResponse(ResponseBase):
    pass
class UseExpItemResponse(ResponseBase):
    item_data: List[InventoryInfo] = None
    unit_data: UnitData = None
class UserInviteClanListResponse(ResponseBase):
    list: List[InviteClanDetail] = None
class VoteExecResponse(ResponseBase):
    pass
class VoteTopResponse(ResponseBase):
    voted_unit: VotedUnit = None
    ranking: VoteRanking = None
