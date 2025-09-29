from typing import List, Dict
from .enums import *
from pydantic import BaseModel, Field

class SkillLevelInfo(BaseModel):
    skill_id: int = None
    skill_level: int = None
    slot_number: int = None
class EquipSlot(BaseModel):
    id: int = None
    is_slot: bool = None
    enhancement_level: int = None
    enhancement_pt: int = None
    rank: int = None
    status: int = None
class StatusParam(BaseModel):
    hp: int = None
    atk: int = None
    _def: int = Field(alias='def')
    magic_str: int = None
    magic_def: int = None
    physical_critical: int = None
    magic_critical: int = None
    wave_hp_recovery: int = None
    wave_energy_recovery: int = None
    hp_recovery_rate: int = None
    physical_penetrate: int = None
    magic_penetrate: int = None
    life_steal: int = None
    dodge: int = None
    energy_reduce_rate: int = None
    energy_recovery_rate: int = None
    accuracy: int = None
class UnitParam(BaseModel):
    base_param: StatusParam = None
    equip_param: StatusParam = None
class StatusParamShort(BaseModel):
    hp: int = None
    atk: int = None
    _def: int = Field(alias='def')
    matk: int = None
    mdef: int = None
    crt: int = None
    mcrt: int = None
    hrec: int = None
    erec: int = None
    hrec_rate: int = None
    pnt: int = None
    mpnt: int = None
    life_steal: int = None
    dodge: int = None
    erec_rate: int = None
    ered_rate: int = None
    accuracy: int = None
class SkinData(BaseModel):
    icon_skin_id: int = None
    sd_skin_id: int = None
    still_skin_id: int = None
    motion_id: int = None
class UnlockRarity6Slot(BaseModel):
    quest_clear: int = None
    slot_1: int = None
    slot_2: int = None
    slot_3: int = None
    Status1: int = None
    Status2: int = None
    Status3: int = None
class ExtraEquipSlot(BaseModel):
    serial_id: int = None
    ex_equipment_id: int = None
    enhancement_pt: int = None
class UnitData(BaseModel):
    id: int = None
    get_time: int = None
    start_rarety: int = None
    unit_rarity: int = None
    battle_rarity: int = None
    unit_level: int = None
    unit_exp: int = None
    promotion_level: ePromotionLevel = None
    union_burst: List[SkillLevelInfo] = None
    main_skill: List[SkillLevelInfo] = None
    ex_skill: List[SkillLevelInfo] = None
    free_skill: List[SkillLevelInfo] = None
    equip_slot: List[EquipSlot] = None
    unique_equip_slot: List[EquipSlot] = None
    exceed_stage: int = None
    unit_param: UnitParam = None
    bonus_param: StatusParamShort = None
    resist_status_id: int = None
    resist_variation_id: int = None
    power: int = None
    skin_data: SkinData = None
    identify_num: int = None
    favorite_flag: int = None
    unlock_rarity_6_item: UnlockRarity6Slot = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    cb_ex_equip_slot: List[ExtraEquipSlot] = None
    TotalHpWithoutExtra: int = None
    TotalHp: int = None
    TotalAtkWithoutExtra: int = None
    TotalAtk: int = None
    TotalDefWithoutExtra: int = None
    TotalDef: int = None
    TotalMagicAtkWithoutExtra: int = None
    TotalMagicAtk: int = None
    TotalMagicDefWithoutExtra: int = None
    TotalMagicDef: int = None
    TotalCriticalWithoutExtra: int = None
    TotalCritical: int = None
    TotalMagicCriticalWithoutExtra: int = None
    TotalMagicCritical: int = None
    TotalWaveHpRecovery: int = None
    TotalWaveEnergyRecovery: int = None
    TotalHpRecoveryRate: int = None
    TotalPhysicalPenetrate: int = None
    TotalMagicPenetrate: int = None
    TotalLifeSteal: int = None
    TotalDodge: int = None
    TotalAccuracy: int = None
    TotalEnergyRecoveryRate: int = None
    TotalEnergyReduceRate: int = None
    UniqueEquipSlot1: EquipSlot = None
    UniqueEquipSlot2: EquipSlot = None
class DuplicateUnitInfo(BaseModel):
    unit_id: int = None
    rarity: int = None
    count: int = None
class ExtraEquipInfo(BaseModel):
    serial_id: int = None
    ex_equipment_id: int = None
    enhancement_pt: int = None
    rank: int = None
    protection_flag: int = None
class InventoryInfo(BaseModel):
    id: int = None
    type: eInventoryType = None
    count: int = None
    received: int = None
    stock: int = None
    unit_data: UnitData = None
    exchange_data: DuplicateUnitInfo = None
    ex_equip: ExtraEquipInfo = None
class UnitDataForView(BaseModel):
    id: int = None
    unit_level: int = None
    unit_rarity: int = None
    battle_rarity: int = None
    promotion_level: ePromotionLevel = None
    power: int = None
    skin_data: SkinData = None
    unique_equip_slot: List[EquipSlot] = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    cb_ex_equip_slot: List[ExtraEquipSlot] = None
class EmblemData(BaseModel):
    emblem_id: int = None
    ex_value: int = None
class SearchOpponent(BaseModel):
    viewer_id: int = None
    rank: int = None
    user_name: str = None
    team_level: int = None
    favorite_unit: UnitDataForView = None
    arena_deck: List[UnitData] = None
    emblem: EmblemData = None
class UnitDamageInfo(BaseModel):
    viewer_id: int = None
    unit_id: int = None
    damage: int = None
    rarity: int = None
    skin_data: SkinData = None
class UnitHpInfo(BaseModel):
    viewer_id: int = None
    unit_id: int = None
    hp: int = None
class ArenaWaveResult(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitHpInfo] = None
    wave_num: int = None
    remain_time: int = None
class ArenaInfo(BaseModel):
    max_battle_number: float = None
    battle_number: int = None
    interval_end_time: int = None
    yesterday_defend_number: int = None
    highest_rank: int = None
    season_highest_rank: int = None
    rank: int = None
    group: int = None
    group_moving_release_time: int = None
    already_suspend: int = None
class VersusResultDetail(BaseModel):
    log_id: int = None
    is_challenge: int = None
    vs_user_team_level: int = None
    vs_user_name: str = None
    win_or_lose: int = None
    emblem: EmblemData = None
    user_arena_deck: List[UnitDataForView] = None
    vs_user_arena_deck: List[UnitDataForView] = None
    damage_list: List[UnitDamageInfo] = None
class OpponentUser(BaseModel):
    viewer_id: int = None
    user_name: str = None
    team_level: int = None
    favorite_unit: UnitDataForView = None
    total_power: int = None
    emblem: EmblemData = None
class VersusResult(BaseModel):
    log_id: int = None
    versus_time: int = None
    win_or_lose: int = None
    opponent_user: OpponentUser = None
class DeckData(BaseModel):
    deck_number: ePartyType = None
    unit_id_1: int = None
    unit_id_2: int = None
    unit_id_3: int = None
    unit_id_4: int = None
    unit_id_5: int = None
class UserJewel(BaseModel):
    jewel: int = None
    free_jewel: int = None
class RankingSearchOpponent(BaseModel):
    viewer_id: int = None
    rank: int = None
    user_name: str = None
    team_level: int = None
    favorite_unit: UnitDataForView = None
    arena_deck: List[UnitDataForView] = None
    emblem: EmblemData = None
class ArenaWaveInfo(BaseModel):
    user_arena_deck: List[UnitData] = None
    vs_user_arena_deck: List[UnitData] = None
    seed: int = None
    battle_log_id: int = None
    wave_num: int = None
class ItemInfo(BaseModel):
    item_id: int = None
    item_num: int = None
    current_num: int = None
class UserEquipParameterIdCount(BaseModel):
    id: int = None
    count: int = None
class SkillLevelUpDetail(BaseModel):
    location: int = None
    step: int = None
    current_level: int = None
class UserGold(BaseModel):
    gold_id_pay: int = None
    gold_id_free: int = None
class InventoryInfoPost(BaseModel):
    id: int = None
    type: int = None
    count: int = None
class ShopBuyInfo(BaseModel):
    system_id: int = None
    slot_id: int = None
    current_currency_num: int = None
    number: int = None
class CggCompletionInfoList(BaseModel):
    newly_completion_id_list: List[int] = None
    newly_emblem_id_list: List[int] = None
    reward_info_list: List[InventoryInfo] = None
class CggGoodsInfo(BaseModel):
    goods_id: int = None
    goods_count: int = None
    new_flag: int = None
class CggGachaGoodsStatus(BaseModel):
    lineup_id: int = None
    remain_num: int = None
class CggGachaStatus(BaseModel):
    gacha_type: int = None
    gacha_status: List[CggGachaGoodsStatus] = None
class ChangeRarityUnit(BaseModel):
    unit_id: int = None
    battle_rarity: int = None
class RoleInfo(BaseModel):
    viewer_id: int = None
    role_id: int = None
class UnitDataForClanMember(BaseModel):
    unit_id: int = None
    position: int = None
    evolution: int = None
    battle_rarity: int = None
    level: int = None
    promotion_level: int = None
    dispatch_count: int = None
    dispatch_status: int = None
    dispatch_start_time: int = None
    current_dispatch_bonus: int = None
    skin_data: SkinData = None
    unique_equipped_list: List[int] = None
class ClanMemberInfo(BaseModel):
    viewer_id: int = None
    name: str = None
    emblem: EmblemData = None
    role: eClanRole = None
    level: int = None
    favorite_unit: UnitDataForView = None
    dispatch_units: List[UnitDataForClanMember] = None
    last_login_time: int = None
    total_power: int = None
class SkinDataForRequest(BaseModel):
    unit_id: int = None
    icon_skin_id: int = None
    sd_skin_id: int = None
    still_skin_id: int = None
    motion_id: int = None
class CharaExchangeTicketReward(BaseModel):
    unit_id: int = None
    unit_rarity: int = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
class AgreementStatus(BaseModel):
    ver: int = None
    state: int = None
class ClanBattleBattleLogFavorite(BaseModel):
    target_viewer_id: int = None
    battle_log_ids: List[int] = None
class MyLogUnitData(BaseModel):
    unit_id: int = None
    unit_rarity: int = None
    unit_level: int = None
    promotion_level: int = None
    damage: int = None
    skin_data: SkinData = None
    unique_equip_slot: List[EquipSlot] = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    cb_ex_equip_slot: List[ExtraEquipSlot] = None
    viewer_id: int = None
class ClanBattleBattleLog(BaseModel):
    target_viewer_id: int = None
    battle_log_id: int = None
    battle_type: int = None
    order_num: int = None
    lap_num: int = None
    battle_end_time: int = None
    total_damage: int = None
    user_name: str = None
    enemy_damage: int = None
    is_auto: int = None
    units: List[MyLogUnitData] = None
    phase: int = None
class BossHistory(BaseModel):
    id: int = None
    difficulty: int = None
    lap_num: int = None
    order_num: int = None
    clear_time: int = None
    attack_count: int = None
class DamageHistory(BaseModel):
    viewer_id: int = None
    enemy_id: int = None
    name: str = None
    damage: int = None
    kill: int = None
    create_time: int = None
    history_id: int = None
    lap_num: int = None
    order_num: int = None
class MemberScoreRanking(BaseModel):
    name: str = None
    favorite_unit: UnitDataForView = None
    rank: int = None
    score: int = None
    total_power: int = None
    emblem: EmblemData = None
    viewer_id: int = None
class BossRankingInClanPhase(BaseModel):
    phase_num: int = None
    enemy_id: int = None
    my_rank_pos: int = None
    ranking: List[MemberScoreRanking] = None
class BossRankingInClan(BaseModel):
    order_num: int = None
    latest_phase_num: int = None
    phases: List[BossRankingInClanPhase] = None
class BossRank(BaseModel):
    enemy_id: int = None
    rank: int = None
class MemberBossRanks(BaseModel):
    name: str = None
    favorite_unit: UnitDataForView = None
    emblem: EmblemData = None
    bosses: List[BossRank] = None
    viewer_id: int = None
    score: int = None
class BossRankingInClanSummaryPhase(BaseModel):
    phase_num: int = None
    my_member_pos: int = None
    members: List[MemberBossRanks] = None
class BossRankingInClanSummary(BaseModel):
    latest_phase_num: int = None
    phases: List[BossRankingInClanSummaryPhase] = None
class MyLogEnemyData(BaseModel):
    enemy_id: int = None
    damage: int = None
class MyLog(BaseModel):
    mylog_id: int = None
    battle_log_id: int = None
    is_auto: int = None
    lap_num: int = None
    phase_num: int = None
    order_num: int = None
    battle_time: int = None
    total_damage: int = None
    units: List[MyLogUnitData] = None
    enemy: MyLogEnemyData = None
    clan_battle_mode: int = None
class DamageReport(BaseModel):
    viewer_id: int = None
    name: str = None
    favorite_unit: UnitDataForView = None
    damage: int = None
    rank: int = None
    emblem: EmblemData = None
class ClanBattleBattleLogFavoriteDeleted(BaseModel):
    target_viewer_id: int = None
    battle_log_id: int = None
class ClanBattleFinishUnit(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitHpInfo] = None
class UnitUnionBurstTimeline(BaseModel):
    unit_id: int = None
    remain_time: int = None
    is_battle_finish: int = None
class HistoryReport(BaseModel):
    viewer_id: int = None
    unit_id: int = None
    unit_rarity: int = None
    damage: int = None
    skin_data: SkinData = None
class UserMissionInfo(BaseModel):
    mission_id: int = None
    disp_order: int = None
    sort_filter_type: int = None
    mission_status: eMissionStatusType = None
    clear_num: int = None
    team_level: int = None
    receive_status: int = None
    not_exist: bool = None
    is_level_specific_mission: bool = None
class PeriodRanking(BaseModel):
    clan_name: str = None
    member_num: int = None
    leader_viewer_id: int = None
    leader_name: str = None
    emblem: EmblemData = None
    leader_favorite_unit: UnitDataForView = None
    rank: int = None
    damage: int = None
    grade_rank: int = None
class ClanBattleRecord(BaseModel):
    clan_battle_id: int = None
    clan_name: str = None
    clan_battle_mode: int = None
    clan_rank: int = None
    clan_score: int = None
    own_rank: int = None
    own_score: int = None
    solo_lap_num: int = None
    solo_kill_num: int = None
class ClanBattleSuggestDeck(BaseModel):
    total_damage: int = None
    level_id: int = None
    party_type: int = None
    battle_time: int = None
    start_remain_time: int = None
    win_or_lose: int = None
    enc_key: str = None
    manual_clear_flags: int = None
    deck: List[UnitDataForView] = None
class SkillLevelInfoLight(BaseModel):
    skill_level: int = None
class EquipSlotLight(BaseModel):
    is_slot: bool = None
    enhancement_pt: int = None
    rank: int = None
class UnitDataLight(BaseModel):
    id: int = None
    get_time: int = None
    start_rarety: int = None
    unit_rarity: int = None
    battle_rarity: int = None
    unit_level: int = None
    unit_exp: int = None
    promotion_level: ePromotionLevel = None
    union_burst: List[SkillLevelInfoLight] = None
    main_skill: List[SkillLevelInfoLight] = None
    ex_skill: List[SkillLevelInfoLight] = None
    equip_slot: List[EquipSlotLight] = None
    unique_equip_slot: List[EquipSlotLight] = None
    bonus_param: StatusParamShort = None
    resist_status_id: int = None
    resist_variation_id: int = None
    power: int = None
    skin_data: SkinData = None
    identify_num: int = None
    favorite_flag: int = None
    unlock_rarity_6_item: UnlockRarity6Slot = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    cb_ex_equip_slot: List[ExtraEquipSlot] = None
class ClanBattleSupportUnitLight(BaseModel):
    unit_data: UnitDataLight = None
    current_support_unit: int = None
    stock_index: int = None
    owner_viewer_id: int = None
    owner_name: str = None
    remaining_count: int = None
class ClanBattleSupportUnit(BaseModel):
    unit_data: UnitData = None
    current_support_unit: int = None
    stock_index: int = None
    owner_viewer_id: int = None
    owner_name: str = None
    remaining_count: int = None
class BattleTimelineUnitData(BaseModel):
    unit_id: int = None
    unit_rarity: int = None
    unit_level: int = None
    promotion_level: int = None
    damage: int = None
class BossInfo(BaseModel):
    order_num: int = None
    lap_num: int = None
    enemy_id: int = None
    max_hp: int = None
    current_hp: int = None
    phase: int = None
class BossReward(BaseModel):
    clan_battle_id: int = None
    lap_num: int = None
    order_num: int = None
    id: int = None
    kill_time: int = None
    reward_info: List[InventoryInfo] = None
    period: int = None
    phase: int = None
    clan_battle_mode: int = None
class RankResult(BaseModel):
    clan_battle_id: int = None
    period: int = None
    clan_rank: int = None
    rank_in_clan: int = None
    clan_battle_mode: int = None
    lap_num: int = None
    total_kill_count: int = None
    battle_joined: int = None
class ClanBattleCarryOverInfo(BaseModel):
    stock_index: int = None
    time: int = None
    using_unit: List[int] = None
    support_owner_viewer_id: int = None
    support_unit: UnitDataForView = None
    change_phase: int = None
class ClanBattleTopUserClanInformation(BaseModel):
    clan_name: str = None
    clan_role: int = None
class ClanBattleExtraBattleChallengeRewardInfo(BaseModel):
    challenge_count: int = None
    reward_info: List[InventoryInfo] = None
class BlockUserDetail(BaseModel):
    block_id: int = None
    clan_name: str = None
    team_level: int = None
    owner_name: str = None
    favorite_unit: UnitDataForView = None
    owner_last_login_time: int = None
class ChatMessageInfo(BaseModel):
    viewer_id: int = None
    message_id: int = None
    message_type: eClanChatMessageType = None
    message: str = None
    create_time: int = None
    disp_minigame_button: eClanChatPlayButtonCondition = None
class ChatMemberInfo(BaseModel):
    viewer_id: int = None
    name: str = None
    level: int = None
    favorite_unit: UnitDataForView = None
    emblem: EmblemData = None
class EquipDonate(BaseModel):
    equip_id: int = None
    num: int = None
    name: str = None
class EquipRequests(BaseModel):
    message_id: int = None
    equip_id: int = None
    request_num: int = None
    donation_num: int = None
    user_donation_num: int = None
    history: List[EquipDonate] = None
    is_finish_checked: int = None
    viewer_id: int = None
class UserEquipParameter(BaseModel):
    equip_id: int = None
    equip_count: int = None
class ClanInfo(BaseModel):
    clan_id: int = None
    leader_viewer_id: int = None
    leader_name: str = None
    leader_favorite_unit: UnitDataForView = None
    clan_name: str = None
    description: str = None
    join_condition: eClanJoinCondition = None
    member_num: int = None
    activity: eClanActivityGuideline = None
    grade_rank: int = None
    current_period_ranking: int = None
    clan_battle_mode: int = None
class ClanData(BaseModel):
    detail: ClanInfo = None
    members: List[ClanMemberInfo] = None
class InventoryInfoShort(BaseModel):
    id: int = None
    stock: int = None
    create_time: int = None
class InvitedUserDetail(BaseModel):
    viewer_id: int = None
    invite_id: int = None
    user_name: str = None
    favorite_unit: UnitDataForView = None
    team_level: int = None
    user_last_login_time: int = None
    emblem: EmblemData = None
class JoinRequestUserInfo(BaseModel):
    viewer_id: int = None
    name: str = None
    level: int = None
    comment: str = None
    favorite_unit: UnitDataForView = None
    emblem: EmblemData = None
class UserStaminaInfo(BaseModel):
    user_stamina: int = None
    stamina_full_recovery_time: int = None
class UnitHpInfoForFriendBattle(BaseModel):
    viewer_id: int = None
    unit_id: int = None
    hp: int = None
    hp_rate: int = None
class FriendBattleResult(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitHpInfoForFriendBattle] = None
    wave_num: int = None
    remain_time: int = None
class PracticeWaveInfo(BaseModel):
    battle_log_id: int = None
    seed: int = None
    user_deck: List[UnitData] = None
    vs_user_deck: List[UnitData] = None
    wave_num: int = None
class SkipGoldRewardInfo(BaseModel):
    count: int = None
class QuestResult(BaseModel):
    reward_list: List[InventoryInfo] = None
    acquired_gold: int = None
    acquired_team_exp: int = None
    acquired_gold_list: List[SkipGoldRewardInfo] = None
class DailyTaskParam(BaseModel):
    event_id: int = None
    boss_id: int = None
    is_renewal: bool = None
    unsold_items: List[InventoryInfo] = None
    buy_count: int = None
    skip_dungeon_area_id: int = None
    can_enter: bool = None
    special_dungeon_area_id: int = None
    skip_quest_id: int = None
    skip_count: int = None
    normal_gacha_ids: List[int] = None
    clan_id: int = None
    random_clan_member_id: int = None
    random_clan_member_name: str = None
    remaining_count: int = None
    is_season_changed: bool = None
    special_dungeon_challenged: bool = None
class DailyTaskData(BaseModel):
    task_type: int = None
    status: int = None
    params: DailyTaskParam = None
class DeckListData(BaseModel):
    deck_number: int = None
    unit_list: List[int] = None
class SkillLimitCounter(BaseModel):
    skill_id: int = None
    counter: int = None
class DimensionFaultQueryUnit(BaseModel):
    owner_viewer_id: int = None
    unit_id: int = None
    identify_num: int = None
    damage: int = None
    hp: int = None
    skill_limit_counter: List[SkillLimitCounter] = None
class DimensionFaultSupportUnit(BaseModel):
    unit_data: UnitDataLight = None
    owner_viewer_id: int = None
    owner_name: str = None
    FullUnitData: UnitData = None
    enable: int = None
    current_support_unit: int = None
    hp: int = None
class DimensionFaultVersusUnit(BaseModel):
    unit_id: int = None
    identify_num: int = None
    current_hp: int = None
class CurrentPhaseInfo(BaseModel):
    slot_id: int = None
    quest_id: int = None
    versus_user_unit: List[DimensionFaultVersusUnit] = None
class PartsInfo(BaseModel):
    parts_id: int = None
    hp: int = None
class DungeonQueryUnit(BaseModel):
    owner_viewer_id: int = None
    unit_id: int = None
    retired: int = None
    hp: int = None
    energy: int = None
    skill_limit_counter: List[SkillLimitCounter] = None
    damage: int = None
    parts_list: List[PartsInfo] = None
class DungeonUnit(BaseModel):
    unit_id: int = None
    hp: int = None
    energy: int = None
    skill_limit_counter: List[SkillLimitCounter] = None
    max_hp: int = None
    power: int = None
    level: int = None
    rarity: int = None
    promotion_level: int = None
    skin_data: SkinData = None
    unique_equipped_list: List[int] = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    cb_ex_equip_slot: List[ExtraEquipSlot] = None
    parts_list: List[PartsInfo] = None
class DungeonQuest(BaseModel):
    quest_id: int = None
    limit_time: int = None
    background: int = None
    chest_id: int = None
    versus_viewer_id: int = None
    name: str = None
    versus_unit_list: List[DungeonUnit] = None
class RestChallengeInfo(BaseModel):
    dungeon_type: int = None
    count: int = None
    max_count: int = None
class DungeonBattleMission(BaseModel):
    mission_id: int = None
    condition_value: int = None
    is_complete: bool = None
class DungeonBattleStartUnit(BaseModel):
    owner_viewer_id: int = None
    unit_id: int = None
class ClanDispatchUnitLight(BaseModel):
    current_support_unit: int = None
    enable: int = None
    energy: int = None
    hp: int = None
    owner_name: str = None
    owner_viewer_id: int = None
    unit_data: UnitDataLight = None
class DungeonSpecialBattleFinishUnit(BaseModel):
    energy: int = None
    hp: int = None
    damage: int = None
    rarity: int = None
    owner_viewer_id: int = None
    skill_limit_counter: List[SkillLimitCounter] = None
    unit_id: int = None
class DungeonEnemyDamage(BaseModel):
    enemy_identify: int = None
    total_damage: int = None
class DungeonEnemyUnit(BaseModel):
    unit_id: int = None
    hp: int = None
class DungeonEnemyInfo(BaseModel):
    enemy_unit: List[DungeonEnemyUnit] = None
    enemy_point: int = None
    seed: int = None
    mode: int = None
class UserEmblem(BaseModel):
    emblem_id: int = None
    ex_value: int = None
class ExtraEquipProtectInfo(BaseModel):
    serial_id: int = None
    protection_flag: int = None
class EventBoxGachaHitRewardInfo(BaseModel):
    box_set_id: int = None
    hit_reward_count: int = None
class HatsuneEventBossStatus(BaseModel):
    boss_id: int = None
    hp: int = None
    is_unlocked: int = None
    appear_num: int = None
    attack_num: int = None
    kill_num: int = None
    is_force_unlocked: int = None
    daily_kill_count: int = None
    oneblow_kill_count: int = None
    remain_time: int = None
    enemy_identify: int = None
class EventBoxGachaSet(BaseModel):
    box_set_id: int = None
    step: int = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
    inbox_count: int = None
    remain_inbox_count: int = None
    reset_target: int = None
    disp_group: int = None
    odds_file: str = None
class EventGachaInfo(BaseModel):
    gacha_step: int = None
    box_set_list: List[EventBoxGachaSet] = None
class PracticeDeckData(BaseModel):
    deck_number: int = None
    deck_name: str = None
    unit_id_1: int = None
    unit_id_2: int = None
    unit_id_3: int = None
    unit_id_4: int = None
    unit_id_5: int = None
    mask_bit_flag: int = None
class FriendDeckInfo(BaseModel):
    deck_number: int = None
    mask_bif_flag: int = None
    unit_data: List[UnitDataForView] = None
class FriendBattleInfo(BaseModel):
    viewer_id: int = None
    name: str = None
    emblem: EmblemData = None
    level: int = None
    favorite_unit: UnitDataForView = None
    deck_list: List[FriendDeckInfo] = None
class FriendInfo(BaseModel):
    viewer_id: int = None
    name: str = None
    emblem: EmblemData = None
    level: int = None
    favorite_unit: UnitDataForView = None
    last_login_time: int = None
    total_power: int = None
    friend_num: int = None
class CampaignTarget(BaseModel):
    viewer_id: int = None
    target_flag: bool = None
class GachaPointInfo(BaseModel):
    exchange_id: int = None
    current_point: int = None
    max_point: int = None
class GachaBonusResult(BaseModel):
    bonus_1: InventoryInfo = None
    bonus_2: InventoryInfo = None
    bonus_3: InventoryInfo = None
    bonus_4: InventoryInfo = None
    bonus_5: InventoryInfo = None
    bonus_6: InventoryInfo = None
    bonus_7: InventoryInfo = None
    bonus_8: InventoryInfo = None
    bonus_9: InventoryInfo = None
    bonus_10: InventoryInfo = None
class GrowthParameterList(BaseModel):
    unit_rarity: int = None
    unit_level: int = None
    skill_level: int = None
    promotion_level: int = None
    equipment_1: int = None
    equipment_2: int = None
    equipment_3: int = None
    equipment_4: int = None
    equipment_5: int = None
    equipment_6: int = None
    love_level: int = None
    growth_id_list: List[int] = None
    unique_equip_strength_point_1: int = None
    unique_equip_strength_point_2: int = None
    unique_equip_rank_1: int = None
    unique_equip_rank_2: int = None
    equip_slot: List[int] = None
class GrowthInfo(BaseModel):
    unit_id: int = None
    growth_parameter_list: GrowthParameterList = None
class GachaGrowthUnitInfo(BaseModel):
    growth_1: GrowthInfo = None
    growth_2: GrowthInfo = None
    growth_3: GrowthInfo = None
    growth_4: GrowthInfo = None
    growth_5: GrowthInfo = None
    growth_6: GrowthInfo = None
    growth_7: GrowthInfo = None
    growth_8: GrowthInfo = None
    growth_9: GrowthInfo = None
    growth_10: GrowthInfo = None
class PrizeRewardInfoDetail(BaseModel):
    rarity: int = None
    rewards: List[InventoryInfo] = None
class PrizeRewardInfo(BaseModel):
    prize_1: PrizeRewardInfoDetail = None
    prize_2: PrizeRewardInfoDetail = None
    prize_3: PrizeRewardInfoDetail = None
    prize_4: PrizeRewardInfoDetail = None
    prize_5: PrizeRewardInfoDetail = None
    prize_6: PrizeRewardInfoDetail = None
    prize_7: PrizeRewardInfoDetail = None
    prize_8: PrizeRewardInfoDetail = None
    prize_9: PrizeRewardInfoDetail = None
    prize_10: PrizeRewardInfoDetail = None
class RecommendUnit(BaseModel):
    unit_id: int = None
    display_order: int = None
    growth_id: int = None
class GachaBonusItem(BaseModel):
    target_unit_id: int = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
    IsLimitCountReward: bool = None
class RemainLimitCountBonusData(BaseModel):
    RemainLimitCountBonus: int = None
    target_unit_id: int = None
class GachaParameter(BaseModel):
    id: int = None
    type: eGachaType = None
    start_time: int = None
    end_time: int = None
    cost_num_single: int = None
    ticket_id: int = None
    free_gacha_interval_time: int = None
    discount_price: int = None
    exchange_id: int = None
    free_exec_times: int = None
    last_free_gacha_time: int = None
    discount_exec_times: int = None
    last_discount_gacha_time: int = None
    recommend_unit: List[RecommendUnit] = None
    url_param: str = None
    ticket_id_10: int = None
    selected_item_id: int = None
    bonus_item_list: List[GachaBonusItem] = None
    free_gacha_campaign_id: int = None
    exec_count: int = None
    select_pickup_slot_num: int = None
    priority_list: List[int] = None
    RemainLimitCountBonus: int = None
    RemainExecGachaBonus: int = None
    original_gacha_id: int = None
    remain_exec_count: int = None
    ExecBonusItemList: List[GachaBonusItem] = None
    RemainLimitCountBonusList: List[RemainLimitCountBonusData] = None
class CampaignGachaInfo(BaseModel):
    campaign_id: int = None
    fg1_exec_cnt: int = None
    fg1_last_exec_time: int = None
    fg10_exec_cnt: int = None
    fg10_last_exec_time: int = None
class GachaPointReset(BaseModel):
    exchange_id: int = None
    lost_gacha_point: int = None
class TicketGachaParameter(BaseModel):
    id: int = None
    start_time: int = None
    end_time: int = None
    ticket_id: int = None
    exec_times: int = None
    url_param: str = None
    is_chara_exchange_ticket: bool = None
class GachaPrizeHistoryList(BaseModel):
    exec_count: int = None
    rarity: int = None
    exec_time: int = None
class GachaPrizeItemDetail(BaseModel):
    rarity: int = None
    odds: float = None
    odds_in_10th: float = None
    reward_list: List[InventoryInfo] = None
class SupportUnitStatus(BaseModel):
    owner_name: str = None
    owner_viewer_id: int = None
    unit_data: UnitDataLight = None
    UserPositionStatus: int = None
    UnitParamData: UnitData = None
class GrandArenaInfo(BaseModel):
    max_battle_number: int = None
    battle_number: int = None
    interval_end_time: int = None
    winning_number: int = None
    yesterday_defend_number: int = None
    highest_rank: int = None
    season_highest_rank: int = None
    rank: int = None
    group: int = None
    group_moving_release_time: int = None
    already_suspend: int = None
    round_max_limited_times: int = None
    daily_max_limited_times: int = None
    round_times: int = None
    round_end_time: int = None
    daily_times: int = None
class GrandArenaDeck(BaseModel):
    first: List[UnitDataForView] = None
    second: List[UnitDataForView] = None
    third: List[UnitDataForView] = None
class GrandArenaSearchOpponent(BaseModel):
    viewer_id: int = None
    rank: int = None
    winning_number: int = None
    user_name: str = None
    team_level: int = None
    favorite_unit: UnitDataForView = None
    emblem: EmblemData = None
    last_match_flag: bool = None
    grand_arena_deck: GrandArenaDeck = None
class RankingGroupInfo(BaseModel):
    group_id: int = None
    is_destination: int = None
class GrandArenaDamageInfo(BaseModel):
    first_result: List[UnitDamageInfo] = None
    second_result: List[UnitDamageInfo] = None
    third_result: List[UnitDamageInfo] = None
class GrandArenaHistoryDetailInfo(BaseModel):
    log_id: int = None
    is_challenge: int = None
    vs_user_viewer_id: int = None
    vs_user_team_level: int = None
    vs_user_name: str = None
    win_or_lose: List[int] = None
    emblem: EmblemData = None
    user_grand_arena_deck: GrandArenaDeck = None
    vs_user_grand_arena_deck: GrandArenaDeck = None
    damage_list: GrandArenaDamageInfo = None
class GrandArenaOppnentUserInfo(BaseModel):
    viewer_id: int = None
    user_name: str = None
    team_level: int = None
    favorite_unit: UnitDataForView = None
    total_power: int = None
    emblem: EmblemData = None
class GrandArenaHistoryInfo(BaseModel):
    log_id: int = None
    versus_time: int = None
    is_challenge: int = None
    win_or_lose: int = None
    emblem: EmblemData = None
    win_number: int = None
    lose_number: int = None
    opponent_user: GrandArenaOppnentUserInfo = None
class UnitOriginalHpInfo(BaseModel):
    viewer_id: int = None
    unit_id: int = None
    hp: int = None
    original_hp: int = None
class HatsuneBossBattleFinishUnit(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitOriginalHpInfo] = None
class EventEnemyDamageInfo(BaseModel):
    enemy_identify: int = None
    total_damage: int = None
class GaugeInfo(BaseModel):
    start_level: int = None
    total: int = None
    unit_id: int = None
    chara_id: int = None
class ExpStatus(BaseModel):
    unit_id: int = None
    level: int = None
    Exp: int = None
    progress: int = None
    Upgrade: int = None
    unit_param: UnitParam = None
    NextExp: int = None
    ExpRatio: float = None
class LoveStatus(BaseModel):
    chara_id: int = None
    level: int = None
    total: int = None
    progress: int = None
    Upgrade: int = None
    ratio: float = None
class LevelParameter(BaseModel):
    team: ExpStatus = None
    unit: List[ExpStatus] = None
    love: List[LoveStatus] = None
class LevelInfo(BaseModel):
    team: GaugeInfo = None
    unit: List[GaugeInfo] = None
    love: List[GaugeInfo] = None
    ParsedLevelParam: LevelParameter = None
class EventSubStoryInfo(BaseModel):
    sub_story_id: int = None
    status: eEventSubStoryStatus = None
class EventHitTreasureInfo(BaseModel):
    enemy_identify: int = None
    hit_treasure_index_list: List[int] = None
class DearPointInfo(BaseModel):
    chara_index: int = None
    dear_point: int = None
class DearStoryInfo(BaseModel):
    story_id: int = None
    is_choiced: int = None
class ReleaseContentData(BaseModel):
    system_id: eSystemId = None
    deck_list: List[DeckData] = None
class SeasonPackRewardInfo(BaseModel):
    reward_type: int = None
    reward_id: int = None
    reward_count: int = None
class UserSeasonPackInfo(BaseModel):
    mission_id: int = None
    buy_id: int = None
    season_end_time: int = None
    extended: int = None
    received: int = None
    rewards: List[SeasonPackRewardInfo] = None
class HatsuneSeriesInfo(BaseModel):
    event_id: int = None
    is_hard_quest_unlocked: bool = None
    bosses: List[HatsuneEventBossStatus] = None
class LimitedShop(BaseModel):
    system_id: int = None
    close_time: int = None
class Price(BaseModel):
    currency_id: int = None
    currency_num: int = None
class ShopItem(BaseModel):
    type: eInventoryType = None
    slot_id: int = None
    item_id: int = None
    num: int = None
    sold: int = None
    end_time: int = None
    price: Price = None
    exchange_count: int = None
    available_num: int = None
    price_group: int = None
    seq_id: int = None
    stock_count: int = None
    purchase_count: int = None
    renewal_time: int = None
    banner_type: eShopItemBannerType = None
    gojuon_order: int = None
    DescriptionId: int = None
    IsUnlimitedStock: bool = None
class DailyShop(BaseModel):
    system_id: int = None
    item_list: List[ShopItem] = None
    add_item_list: List[ShopItem] = None
    remaining_appear_count: int = None
    max_appear_num: int = None
class ClanPoint(BaseModel):
    before_point: int = None
    after_point: int = None
    before_count: int = None
    after_count: int = None
    cost_group_id: int = None
class WaveEnemyInfo(BaseModel):
    enemy_id: int = None
    drop_gold: int = None
    drop_reward: List[InventoryInfo] = None
class WaveEnemyInfoList(BaseModel):
    enemy_info_list: List[WaveEnemyInfo] = None
class HatsuneUserEventQuest(BaseModel):
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    is_unlocked: int = None
    limit_time: int = None
    wave_pattern_ids: List[int] = None
    daily_clear_count: int = None
    daily_recovery_count: int = None
class EventQuizInfo(BaseModel):
    quiz_id: int = None
    is_correct: int = None
class HatsuneEventBossEnemyInfo(BaseModel):
    boss_id: int = None
    enemy_identify: int = None
    hp: int = None
class QuestRecoverInfo(BaseModel):
    quest_id: int = None
    daily_recovery_count: int = None
class EventSpecialEnemyUnit(BaseModel):
    unit_id: int = None
    hp: int = None
    order: int = None
class EventEnemyInfo(BaseModel):
    enemy_unit: List[EventSpecialEnemyUnit] = None
    enemy_point: int = None
    seed: int = None
    mode: int = None
    kill_order: List[int] = None
class ReplayUnitDataForView(BaseModel):
    id: int = None
    unit_level: int = None
    unit_rarity: int = None
    battle_rarity: int = None
    promotion_level: ePromotionLevel = None
    skin_data: SkinData = None
    unique_equip_slot: List[EquipSlot] = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    is_alive: int = None
class EventSpecialBattleExHistory(BaseModel):
    attack_num: int = None
    total_power: int = None
    damage: int = None
    mode: int = None
    unit_data: List[ReplayUnitDataForView] = None
    manual_flags: int = None
class SpecialBattleInfo(BaseModel):
    enemy_unit: List[UnitHpInfo] = None
    enemy_point: int = None
    mode: int = None
    kill_limit: int = None
class HatsuneEventStatus(BaseModel):
    event_type: int = None
    event_id: int = None
    period: int = None
class HatsuneEventStoryState(BaseModel):
    story_id: int = None
    is_unlocked: int = None
    is_readed: bool = None
class HatsuneLoginBonusData(BaseModel):
    todays_count: int = None
    rewards: List[InventoryInfo] = None
class EventSpecialBattleExRankingInfo(BaseModel):
    rank: int = None
    appear_num: int = None
    total_attack_num: int = None
    total_attack_num_mode_1: int = None
    total_attack_num_mode_2: int = None
    total_attack_num_mode_3: int = None
    new: int = None
class UnreadMessageList(BaseModel):
    equip_requests: List[EquipRequests] = None
class UserClan(BaseModel):
    clan_id: int = None
    clan_name: str = None
    latest_request_time: int = None
    donation_num: int = None
    leave_time: int = None
    clan_member_count: int = None
class UserQuestInfo(BaseModel):
    quest_id: int = None
    clear_flg: int = None
    result_type: int = None
    daily_clear_count: int = None
    daily_recovery_count: int = None
class DungeonInfo(BaseModel):
    enter_area_id: int = None
    rest_challenge_count: List[RestChallengeInfo] = None
class TrainingQuestCount(BaseModel):
    gold_quest: int = None
    exp_quest: int = None
class AlchemyReward(BaseModel):
    reward_info_list: List[InventoryInfo] = None
class LastFriendTime(BaseModel):
    accept: int = None
    pending: int = None
class CharaExchangeTicketProductData(BaseModel):
    csv_data_id: str = None
    number_of_product_purchased: int = None
    start_time: int = None
    end_time: int = None
class ShioriQuestInfo(BaseModel):
    quest_list: List[UserQuestInfo] = None
    dead_boss_list: List[int] = None
class TravelNotificationInfo(BaseModel):
    travel_end_time: int = None
    playable_secret_travel_count: int = None
class AcquiredReleaseCoin(BaseModel):
    system_id: int = None
    is_acquired: int = None
class KaiserBossInfo(BaseModel):
    kaiser_boss_id: int = None
    progress: int = None
    condition_count: int = None
    current_hp: int = None
    kill_count: int = None
    mode: int = None
    enemy_point: int = None
    attack_count: int = None
class BossBattleFinishUnit(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitHpInfo] = None
class KaiserBattleSupportRental(BaseModel):
    support_num: int = None
    owner_viewer_id: int = None
    support_unit_id: int = None
class SupportUnitSetting(BaseModel):
    unit_id: int = None
    position: int = None
    support_start_time: int = None
    friend_support_count: int = None
    general_support_count: int = None
    clan_support_count: int = None
    friend_support_reward: int = None
    SupportType: int = None
class KmkKillList(BaseModel):
    low: int = None
    middle: int = None
    high: int = None
class LegionMainEnemyUnit(BaseModel):
    unit_id: int = None
    current_hp: int = None
    battle_hp: int = None
    damage: int = None
class LegionBossInfo(BaseModel):
    legion_boss_id: int = None
    mode: int = None
    attack_count: int = None
    enemy_status_list: List[LegionMainEnemyUnit] = None
class LegionMainEnemyInfo(BaseModel):
    enemy_unit: List[LegionMainEnemyUnit] = None
    seed: int = None
    mode: int = None
class LegionBattleSupportRental(BaseModel):
    support_num: int = None
    owner_viewer_id: int = None
    support_unit_id: int = None
class LegionMainModeInfo(BaseModel):
    seed: int = None
    mode: int = None
class LegionBattleBonus(BaseModel):
    legion_boss_id: int = None
    start_time_list: List[int] = None
class UserInfo(BaseModel):
    viewer_id: int = None
    user_name: str = None
    user_comment: str = None
    emblem: EmblemData = None
    team_level: int = None
    user_stamina: int = None
    team_exp: int = None
    favorite_unit_id: int = None
    tutorial_flag: int = None
    user_birth: int = None
    stamina_full_recovery_time: int = None
    arena_rank: int = None
    invite_accept_flag: int = None
    reg_time: int = None
class UserBankGoldInfo(BaseModel):
    bank_gold: int = None
    highest_bank_gold: int = None
class UserChara(BaseModel):
    chara_id: int = None
    chara_love: int = None
    love_level: int = None
class LoadDeckData(BaseModel):
    deck_number: ePartyType = None
    unit_id_1: int = None
    unit_id_2: int = None
    unit_id_3: int = None
    unit_id_4: int = None
    unit_id_5: int = None
    battle_rarity_1: int = None
    battle_rarity_2: int = None
    battle_rarity_3: int = None
    battle_rarity_4: int = None
    battle_rarity_5: int = None
class RestrictionExtraEquip(BaseModel):
    serial_id: int = None
    unit_id: int = None
class Alchemy(BaseModel):
    max_count: int = None
    exec_count: int = None
class RecoverStamina(BaseModel):
    count: int = None
    exec_count: int = None
    recovery: int = None
    cost: int = None
class Shop(BaseModel):
    alchemy: Alchemy = None
    recover_stamina: RecoverStamina = None
class StrCoinCost(BaseModel):
    idx: int = None
    cost: int = None
class StrJewelCost(BaseModel):
    idx: int = None
    cost: int = None
class EquipStrSetting(BaseModel):
    lower_rank: int = None
    coin_cost: List[StrCoinCost] = None
    jewel_cost: List[StrJewelCost] = None
class QuestSetting(BaseModel):
    recovery_time: int = None
    challenge_count_special_gold: int = None
    challenge_count_special_exp: int = None
class DungeonSetting(BaseModel):
    support_rental_cost_coefficient: int = None
    border_unit_level: int = None
    support_lv_band: int = None
class IniPair(BaseModel):
    key: int = None
    val: int = None
class UnitSetting(BaseModel):
    max_evolution: int = None
    change_to_material: List[IniPair] = None
    material_extra_available_num: int = None
class ArenaSetting(BaseModel):
    time_reset_cost: int = None
    count_reset_cost: int = None
class GrandArenaSetting(BaseModel):
    time_reset_cost: int = None
    count_reset_cost: int = None
class LimitSetting(BaseModel):
    limit_equipment_num: int = None
    limit_gold: int = None
    limit_free_gold: int = None
    limit_jewel: int = None
    limit_free_jewel: int = None
    limit_bank_free_gold: int = None
class ClanSetting(BaseModel):
    max_member_num: int = None
    max_leader_num: int = None
    max_sub_leader_num: int = None
    dispatch_interval: int = None
    chat_num_per_time: int = None
    chat_max_num: int = None
    chat_expire_sec: int = None
    chat_polling_time: int = None
    gold_unit_period: int = None
    gold_base: int = None
    gold_rate_power: float = None
    gold_per_dispatch_count: int = None
    rejoin_restriction_time: int = None
    like_reward: int = None
    daily_like_reward_limit: int = None
    be_liked_reward: int = None
    daily_be_liked_reward_limit: int = None
    equipment_request_interval: int = None
    search_clan_default_activity: int = None
    search_clan_default_join_condition: int = None
    search_clan_default_member_condition_range: int = None
    notify_support_gold_border: int = None
    clan_activity_max: int = None
    rental_cost_fixed_border_team_lv: int = None
    rental_cost_rate_per_team_lv: int = None
    rental_cost_fixed: int = None
class ClanBattleSetting(BaseModel):
    default_difficulty: int = None
    default_challenge_count: int = None
    clan_point_coefficient: int = None
    support_rental_cost_coefficient: int = None
    border_unit_level: int = None
    grace_time: int = None
    dispatch_count_bonus_limit: int = None
    dispatch_time_bonus_limit: int = None
    hp_recovery_time: int = None
    can_use_hp_border: int = None
    support_lv_band: int = None
    monster_detail_reload_interval: int = None
    mode_change_limit_hours: int = None
    mode_change_limit_start_hours: int = None
    mode_change_limit_remind_hours: int = None
    party_copy_open_time: int = None
class FriendSetting(BaseModel):
    limit_accept: int = None
    limit_request: int = None
    limit_pending: int = None
class RoomSetting(BaseModel):
    extension_room_storage_cost: int = None
    extension_room_storage_num: int = None
    max_room_storage_num: int = None
    shortening_time: int = None
    use_jewel: int = None
    not_stock_term: int = None
    max_stock_count: int = None
class TowerSetting(BaseModel):
    initial_energy: int = None
    timeup_hp_penalty: int = None
    timeup_energy_penalty: int = None
    support_rental_cost_coefficient: int = None
    reduce_enemy_energy_value: int = None
    reduce_enemy_energy_lower_limit: int = None
    get_cleared_ex_quest_interval: int = None
    support_lv_band: int = None
    usable_unit_count: int = None
class RecoverChallengeCountSetting(BaseModel):
    recovery: int = None
    recovery_max_count: int = None
    cost: List[int] = None
class SendApi(BaseModel):
    notice: int = None
    home: int = None
class BattleLogType(BaseModel):
    miss: int = None
    set_damage: int = None
    set_abnormal: int = None
    set_recovery: int = None
    set_buff_debuff: int = None
    set_state: int = None
    button_tap: int = None
    set_energy: int = None
    damage_charge: int = None
    give_value_additional: int = None
    give_value_multiply: int = None
    wave_end_hp: int = None
    wave_end_damage_amount: int = None
    _break: int = Field(alias='break')
    suspend_count: int = None
class NormalGachaTerm(BaseModel):
    time: str = None
class NormalGachaSetting(BaseModel):
    term_list: List[NormalGachaTerm] = None
class CartoonSetting(BaseModel):
    open_time_sp: int = None
    open_time_dmm: int = None
class UniqueEquipLimitSetting(BaseModel):
    equip_slot: int = None
    promotion: int = None
    rarity: int = None
class UniqueEquipSetting(BaseModel):
    limit_list: List[UniqueEquipLimitSetting] = None
class UnreadStoryNoticeSetting(BaseModel):
    time: str = None
    type: int = None
class BulkSkipSetting(BaseModel):
    default_skip_count: int = None
    max_skip_count: int = None
class FriendSupportUnitIniSetting(BaseModel):
    support_interval: int = None
    gold_unit_period: int = None
    gold_base: int = None
    gold_rate_power: float = None
    gold_per_support_count: int = None
    support_count_bonus_daily_limit: int = None
    support_count_bonus_limit: int = None
    support_time_bonus_limit: int = None
    limit_unit_level: int = None
    consume_gold_rate: int = None
    consume_gold_limit: int = None
    support_lv_band: int = None
class KaiserBattleIniSetting(BaseModel):
    support_lv_band: int = None
    support_limit: int = None
    allowable_damage_coefficient: float = None
    allowable_enemy_point: int = None
    allowable_barrier_point: int = None
    remaining_count_max: int = None
class StoryRaidEvenBattletIniSetting(BaseModel):
    support_limit: int = None
    support_change_interval: int = None
    remaining_count_max: int = None
    limit_unit_level: int = None
class SerialCodeIniSetting(BaseModel):
    restrict_release_sec: int = None
class TravelIniSetting(BaseModel):
    default_daily_retire_limit_count: int = None
    travel_quest_max_repeat_count: int = None
    decrease_time_by_ticket: int = None
    decrease_time_by_jewel: int = None
    travel_start_max_deck_count: int = None
    over_power_decrease_time_coefficient: float = None
    default_secret_travel_appear_limit_count: int = None
    decrease_ticket_daily_use_limit_count: int = None
class ExEquipIniSetting(BaseModel):
    ex_equip_limit_consume_num: int = None
    ex_equip_limit_possession_num: int = None
    ex_equip_limit_protection_num: int = None
class MaxOnceConsumeGoldSetting(BaseModel):
    redeem_unit: int = None
    multi_automatic_enhance: int = None
class SpecialFesDiscountIniSetting(BaseModel):
    open_time: int = None
    limit_count: int = None
    cost: int = None
class CaravanSetting(BaseModel):
    limit_caravan_mile: int = None
    limit_caravan_lottery: int = None
    limit_caravan_treasure: int = None
    limit_caravan_treasure_by_type: int = None
    IsEnableCaravanCoinShopBuyBulk: bool = None
class MultiRankUnitLimitSetting(BaseModel):
    multi_rank_unit_limit: int = None
class StoryBookmarkIniSetting(BaseModel):
    story_bookmark_limit_count: int = None
class TalentQuestIniSetting(BaseModel):
    DailyBonusUseLimitCount: int = None
    DailyClearLimitCount: int = None
    recovery_max_count: int = None
    RecoveryCost: int = None
class MyPartyIniSetting(BaseModel):
    TabPartyNum: int = None
class LogBarrierIniSetting(BaseModel):
    Coefficient: int = None
    Threshold: int = None
class SynchroIniSetting(BaseModel):
    LevelThresholdUnitNum: int = None
    RankThresholdUnitNum: int = None
class AbyssIniSetting(BaseModel):
    DailyClearLimitCount: int = None
class IniSetting(BaseModel):
    equipment_enhance: EquipStrSetting = None
    quest: QuestSetting = None
    dungeon: DungeonSetting = None
    unit: UnitSetting = None
    arena: ArenaSetting = None
    grand_arena: GrandArenaSetting = None
    limit: LimitSetting = None
    clan: ClanSetting = None
    clan_battle: ClanBattleSetting = None
    friend: FriendSetting = None
    room: RoomSetting = None
    tower: TowerSetting = None
    recover_challenge_count: RecoverChallengeCountSetting = None
    very_hard_recover_challenge_count: RecoverChallengeCountSetting = None
    send_api: SendApi = None
    battle_log_type: BattleLogType = None
    normal_gacha: NormalGachaSetting = None
    require_exchange_point: int = None
    hatsune_recover_challenge_count: RecoverChallengeCountSetting = None
    cartoon: CartoonSetting = None
    unique_equip: UniqueEquipSetting = None
    equip_recover_challenge_count: RecoverChallengeCountSetting = None
    high_rarity_equip_recover_challenge_count: RecoverChallengeCountSetting = None
    unread_story_notice: UnreadStoryNoticeSetting = None
    max_boss_battle_skip_num: int = None
    max_gacha_count: int = None
    multiple_skip: BulkSkipSetting = None
    friend_support_unit: FriendSupportUnitIniSetting = None
    kaiser_battle: KaiserBattleIniSetting = None
    legion_battle: StoryRaidEvenBattletIniSetting = None
    sre: StoryRaidEvenBattletIniSetting = None
    serial_code: SerialCodeIniSetting = None
    arena_skip_upper_rank: int = None
    loop_box_multi_gacha_count: int = None
    travel: TravelIniSetting = None
    ex_equip: ExEquipIniSetting = None
    max_once_consume_gold: MaxOnceConsumeGoldSetting = None
    sfd: SpecialFesDiscountIniSetting = None
    caravan: CaravanSetting = None
    multi_rank_unit_limit: MultiRankUnitLimitSetting = None
    story_bookmark: StoryBookmarkIniSetting = None
    TalentQuest: TalentQuestIniSetting = None
    MyParty: MyPartyIniSetting = None
    LogBarrier: LogBarrierIniSetting = None
    Synchro: SynchroIniSetting = None
    Abyss: AbyssIniSetting = None
class LoginBonusData(BaseModel):
    campaign_id: int = None
    total_count: int = None
    count_num: int = None
    type: str = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
    lottery_type: int = None
class LoginBonusList(BaseModel):
    first: List[LoginBonusData] = None
    normal: List[LoginBonusData] = None
    campaign: List[LoginBonusData] = None
    lottery: List[LoginBonusData] = None
    adv: List[LoginBonusData] = None
    countdown: List[LoginBonusData] = None
    birthday: List[LoginBonusData] = None
    story_read_process: List[LoginBonusData] = None
class ClanBattleData(BaseModel):
    now_open: int = None
    is_interval: int = None
    next_open_time: int = None
    mode_change_limit_time: int = None
    mode_change_limit_start_time: int = None
    mode_change_limit_remind_time: int = None
    is_extra_battle_cleared: int = None
class EventStatus(BaseModel):
    event_type: int = None
    event_id: int = None
    period: int = None
class TowerStatus(BaseModel):
    cleared_floor_num: int = None
    last_login_schedule_id: int = None
class MusicIdData(BaseModel):
    bgm_key: eBGMKey = None
    music_id: int = None
class StartDashFesInfo(BaseModel):
    end_time: int = None
    original_gacha_id: int = None
    sdfes_gacha_point_info: GachaPointInfo = None
    supply_unit_id_list: List[int] = None
    can_campaign_gacha: int = None
    sfd_dcc: int = None
class ReturnFesInfo(BaseModel):
    end_time: int = None
    original_gacha_id: int = None
    gacha_point_info: GachaPointInfo = None
    supply_unit_id_list: List[int] = None
    can_campaign_gacha: int = None
class RaceLoginBonusInfo(BaseModel):
    fortune_id: int = None
    rank: int = None
    seed: int = None
    unit_list: List[int] = None
    scenario_id: int = None
class CampaignDate(BaseModel):
    start_time: str = None
    end_time: str = None
class UserBirthDayVoice(BaseModel):
    birthday: int = None
    birthday_period: int = None
class MaintenanceStatus(BaseModel):
    _from: int = Field(alias='from')
    to: int = None
    FromDateTime: int = None
    ToDateTime: int = None
class MyPartyExtraEquipSlot(BaseModel):
    slot: int = None
    ex_equipment_id: int = None
    enhancement_pt: int = None
class MyPartyExEquipInfo(BaseModel):
    unit_id: int = None
    ex_equip_slot: List[MyPartyExtraEquipSlot] = None
    cb_ex_equip_slot: List[MyPartyExtraEquipSlot] = None
class UserMyParty(BaseModel):
    tab_number: int = None
    party_number: int = None
    party_label_type: int = None
    party_name: str = None
    unit_id_1: int = None
    unit_id_2: int = None
    unit_id_3: int = None
    unit_id_4: int = None
    unit_id_5: int = None
    battle_rarity_1: int = None
    battle_rarity_2: int = None
    battle_rarity_3: int = None
    battle_rarity_4: int = None
    battle_rarity_5: int = None
    ex_equip_1: MyPartyExEquipInfo = None
    ex_equip_2: MyPartyExEquipInfo = None
    ex_equip_3: MyPartyExEquipInfo = None
    ex_equip_4: MyPartyExEquipInfo = None
    ex_equip_5: MyPartyExEquipInfo = None
class UserMyPartyTab(BaseModel):
    tab_number: int = None
    tab_name: str = None
class UserMyQuest(BaseModel):
    tab_number: int = None
    tab_name: str = None
    skip_count: int = None
    skip_list: List[int] = None
    item_list: List[int] = None
    difficulty_list: List[int] = None
    InitialSkipCount: int = None
class CounterStopCoinInfo(BaseModel):
    count: int = None
    max: int = None
class CounterStopCoinExchange(BaseModel):
    weekly: CounterStopCoinInfo = None
class MyPage(BaseModel):
    type: int = None
    id: int = None
    music_id: int = None
    still_skin_id: int = None
    frame_id: int = None
class EventSubStory(BaseModel):
    event_id: int = None
    unlocked: List[int] = None
    read: List[int] = None
    sub_story_info_list: List[EventSubStoryInfo] = None
class PartMaintenanceStatus(BaseModel):
    maintenance_id: int = None
    _from: int = Field(alias='from')
    to: int = None
class RedeemUnitSlotInfo(BaseModel):
    slot_id: int = None
    register_num: int = None
class RedeemUnitInfo(BaseModel):
    unit_id: int = None
    slot_info: List[RedeemUnitSlotInfo] = None
class TaqGameSetting(BaseModel):
    first_interval_time: int = None
    wave_answer_time: int = None
    wave_interval_time: int = None
class SreTermInfo(BaseModel):
    sre_id: int = None
    term: int = None
class SreEnemyUnit(BaseModel):
    unit_id: int = None
    current_hp: int = None
    damage: int = None
class SreMainEnemyInfo(BaseModel):
    enemy_unit: List[SreEnemyUnit] = None
    seed: int = None
    mode: int = None
class SreMainBossInfo(BaseModel):
    sre_boss_id: int = None
    mode: int = None
    attack_count: int = None
    enemy_status_list: List[SreEnemyUnit] = None
class SreSupportRental(BaseModel):
    support_num: int = None
    owner_viewer_id: int = None
    support_unit_id: int = None
class SreMainModeInfo(BaseModel):
    seed: int = None
    mode: int = None
class MissionRequestFlag(BaseModel):
    quest_clear_rank: int = None
class PostMultiUnlockRarity6Slot(BaseModel):
    slot_id: int = None
    current_unlock_level: int = None
    after_unlock_level: int = None
    current_material_num: int = None
class MusicPurchasedData(BaseModel):
    music_id: int = None
    purchased_time: int = None
class MyPageOld(BaseModel):
    type: int = None
    id: int = None
    music_id: int = None
    still_skin_id: int = None
class OtherClanData(BaseModel):
    detail: ClanInfo = None
    members: List[ClanMemberInfo] = None
    invite_id: int = None
    block_id: int = None
class PctGradeInfo(BaseModel):
    grade_type: int = None
    grade_count: int = None
class PctBonusInfo(BaseModel):
    bonus_type: int = None
    bonus_count: int = None
    add_point: int = None
class PctUnitPointInfo(BaseModel):
    unit_id: int = None
    pct_point: int = None
class PctCacaoInfo(BaseModel):
    cacao_id: int = None
    stock: int = None
class PkbReplay(BaseModel):
    pitcher: int = None
    batter: int = None
    seed: int = None
    batting_time: int = None
    batting_pos: List[float] = None
    gauge: int = None
    happen_triggers: List[int] = None
    adrenaline_count: int = None
class PkbBattingResultInfo(BaseModel):
    batting_distance: int = None
    replay: PkbReplay = None
class PkbReadRankingInfo(BaseModel):
    category: int = None
    difficulty_level: int = None
class PkbHighScoreInfo(BaseModel):
    normal: int = None
    hard: int = None
    very_hard: int = None
    extra: int = None
class PkbCatalogBatter(BaseModel):
    batter_id: int = None
    batting_num: int = None
    hit_num: int = None
    status: int = None
class PkbCatalogPitcher(BaseModel):
    pitcher_id: int = None
    status: int = None
    unlocked_ball_type: List[int] = None
class PkbCatalogInfo(BaseModel):
    batter: List[PkbCatalogBatter] = None
    pitcher: List[PkbCatalogPitcher] = None
class PkbRankingRecordSingle(BaseModel):
    record_value: int = None
    status: int = None
    replay: PkbReplay = None
class PkbRankingSingle(BaseModel):
    normal: List[PkbRankingRecordSingle] = None
    hard: List[PkbRankingRecordSingle] = None
    very_hard: List[PkbRankingRecordSingle] = None
    extra: List[PkbRankingRecordSingle] = None
class PkbRankingRecordTotal(BaseModel):
    record_value: int = None
    status: int = None
    replay_list: List[PkbReplay] = None
class PkbRankingTotal(BaseModel):
    normal: List[PkbRankingRecordTotal] = None
    hard: List[PkbRankingRecordTotal] = None
    very_hard: List[PkbRankingRecordTotal] = None
    extra: List[PkbRankingRecordTotal] = None
class PkbRankingInfo(BaseModel):
    single_distance: PkbRankingSingle = None
    total_distance: PkbRankingTotal = None
    home_run_num: PkbRankingTotal = None
class PresentHistoryInfo(BaseModel):
    present_id: int = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
    message_id: int = None
    message_param_value_1: int = None
    message_param_value_2: int = None
    message_param_value_3: int = None
    message_param_value_4: int = None
    create_time: int = None
    message_text: str = None
class PresentParameter(BaseModel):
    present_id: int = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
    reward_rarity: int = None
    message_id: int = None
    message_param_value_1: int = None
    message_param_value_2: int = None
    message_param_value_3: int = None
    message_param_value_4: int = None
    reward_limit_flag: eRewardLimitType = None
    reward_limit_time: int = None
    create_time: int = None
    message_text: str = None
class ArenaCountInfo(BaseModel):
    battle_number: int = None
class GrandArenaCountInfo(BaseModel):
    battle_number: int = None
class ProfileUserInfo(BaseModel):
    viewer_id: int = None
    user_name: str = None
    user_comment: str = None
    team_level: int = None
    team_exp: int = None
    arena_rank: int = None
    arena_group: int = None
    arena_time: int = None
    grand_arena_rank: int = None
    grand_arena_group: int = None
    grand_arena_time: int = None
    open_story_num: int = None
    unit_num: int = None
    total_power: int = None
    tower_cleared_floor_num: int = None
    tower_cleared_ex_quest_count: int = None
    emblem: EmblemData = None
    last_login_time: int = None
    friend_num: int = None
    PrincessKnightRankTotalExp: int = None
class ProfileQuestInfo(BaseModel):
    normal_quest: List[int] = None
    hard_quest: List[int] = None
    very_hard_quest: List[int] = None
    byway_quest: int = None
class SupportUnitForProfile(BaseModel):
    position: int = None
    unit_data: UnitDataLight = None
class ClanProfileCardDisplayStatus(BaseModel):
    level: bool = None
    member: bool = None
class ClanProfileCardSetting(BaseModel):
    unit_id: int = None
    skin: int = None
    background: int = None
    frame: int = None
    disp_status: ClanProfileCardDisplayStatus = None
    invite_comment: str = None
    comment: str = None
class ClanProfileCardClanInfo(BaseModel):
    clan_name: str = None
    clan_battle_id: int = None
    period: int = None
    rank: int = None
    grade_rank: int = None
    level: int = None
    member_num: int = None
    join_condition: int = None
    activity: int = None
    last_clan_battle_mode: int = None
    last_battle_joined: int = None
class MyProfileCardDisplayStatus(BaseModel):
    viewer_id: bool = None
    level: bool = None
    power: bool = None
    clan_battle: bool = None
    arena: bool = None
    grand_arena: bool = None
    tower: bool = None
    princess_knight_rank: bool = None
class MyProfileCardSetting(BaseModel):
    unit_id: int = None
    skin: int = None
    emblem_id: int = None
    background: int = None
    frame: int = None
    disp_status: MyProfileCardDisplayStatus = None
    comment: str = None
class MyProfileCardScore(BaseModel):
    clan_battle_id: int = None
    clan_battle_score: int = None
    arena_rank: int = None
    grand_arena_rank: int = None
    tower_cleared_floor_num: int = None
    tower_cleared_ex_quest_count: int = None
    clan_id: int = None
    emblem_id_list: List[int] = None
    last_clan_battle_mode: int = None
class PsyCookingStatus(BaseModel):
    frame_id: int = None
    pudding_id: int = None
    start_time: str = None
class PsyPuddingNote(BaseModel):
    pudding_id: int = None
    count: int = None
    flavor_status: int = None
    read_status: int = None
class PsyDramaList(BaseModel):
    drama_id: int = None
    read_status: int = None
class PsySetting(BaseModel):
    exchange_rate: int = None
    material_item_id: int = None
    use_material_count: int = None
    pudding_complete_time: int = None
class UserStory(BaseModel):
    story_id: int = None
    state: eStoryStatus = None
    pre_watched_flag: int = None
    special_flag: int = None
class QuestReplayData(BaseModel):
    clear_flg: int = None
    team_level: int = None
    power: int = None
    seed: int = None
    enc_key: str = None
    manual_clear_flags: int = None
    unit_info: List[UnitDataForView] = None
class QuestSkipInfo(BaseModel):
    quest_id: int = None
    skip_count: int = None
class QuestResultList(BaseModel):
    quest_result: List[QuestResult] = None
    quest_id: int = None
    daily_clear_count: int = None
class RedeemUnitRegisterItemInfo(BaseModel):
    id: int = None
    count: int = None
class DeckListDataForView(BaseModel):
    deck_number: int = None
    deck_data_for_view: List[UnitDataForView] = None
class RoomUserInfo(BaseModel):
    viewer_id: int = None
    name: str = None
    comment: str = None
    team_level: int = None
    today_like_flag: bool = None
    like_time: int = None
    flag_read: bool = None
    total_liked: int = None
    like_reward: int = None
    favorite_unit: UnitDataForView = None
    DeckListForClient: List[DeckListDataForView] = None
    emblem: EmblemData = None
class RoomItemPosition(BaseModel):
    serial_id: int = None
    direction: int = None
    x: int = None
    y: int = None
class RoomTheme(BaseModel):
    floor_theme: int = None
    wall_theme: int = None
    background_theme: int = None
class RoomFloorLayout(BaseModel):
    floor: List[RoomItemPosition] = None
    wall: List[RoomItemPosition] = None
    theme: RoomTheme = None
class RoomUserItem(BaseModel):
    serial_id: int = None
    room_item_id: int = None
    room_item_level: int = None
    RoomItemSkinId: int = None
    level_up_end_time: int = None
    item_base_time: int = None
    item_count: int = None
class MaxExecNumList(BaseModel):
    arena_limit: int = None
    convert_rupee_limit: int = None
    dungeon_limit: int = None
    special_quest_limit: int = None
    stamina_limit: int = None
class SendGiftData(BaseModel):
    item_id: int = None
    item_num: int = None
    current_item_num: int = None
class RoomItemPositionForMyset(BaseModel):
    room_item_id: int = None
    direction: int = None
    x: int = None
    y: int = None
class RoomFloorLayoutForMyset(BaseModel):
    floor: List[RoomItemPositionForMyset] = None
    wall: List[RoomItemPositionForMyset] = None
    theme: RoomTheme = None
class RoomWholeLayoutForMyset(BaseModel):
    background_theme: int = None
    floor_layout: RoomFloorLayoutForMyset = None
class RoomMysetElement(BaseModel):
    myset_index: int = None
    myset_name: str = None
    myset_update_time: str = None
    myset_layout: RoomWholeLayoutForMyset = None
class RoomWholeLayout(BaseModel):
    background_theme: int = None
    floor_layout: List[RoomFloorLayout] = None
class RoomItemGetTime(BaseModel):
    room_item_id: int = None
    get_time: int = None
class RoomExtensionItem(BaseModel):
    serial_id: int = None
    room_item_id: int = None
    color_id: int = None
class SekaiRanking(BaseModel):
    name: str = None
    favorite_unit: UnitDataForView = None
    rank: int = None
    damage: int = None
    total_power: int = None
class PaymentGoldDetail(BaseModel):
    id: int = None
    name: str = None
    price: int = None
    charge_jewel_num: int = None
    charge_gold_num: int = None
    display_order: int = None
    current_gold: int = None
class PaymentJewelDetail(BaseModel):
    id: int = None
    name: str = None
    price: int = None
    charge_jewel_num: int = None
    display_order: int = None
    current_jewel: int = None
class ShopInfo(BaseModel):
    system_id: int = None
    reset_count: int = None
    next_renewal_time: int = None
    reset_cost: int = None
    reset_cost_id: int = None
    close_time: int = None
    remaining_appear_count: int = None
    max_appear_num: int = None
    item_list: List[ShopItem] = None
class SjrHighScoreInfo(BaseModel):
    gp_type: int = None
    difficulty_level: int = None
    high_score: int = None
class DungeonMylogUnit(BaseModel):
    viewer_id: int = None
    unit_id: int = None
    unit_rarity: int = None
    battle_rarity: int = None
    unit_level: int = None
    promotion_level: int = None
    damage: int = None
    is_dead: int = None
    unique_equip_slot: List[EquipSlot] = None
    ex_equip_slot: List[ExtraEquipSlot] = None
    cb_ex_equip_slot: List[ExtraEquipSlot] = None
class DungeonMylogEnemy(BaseModel):
    enemy_id: int = None
    damage: int = None
    is_dead: int = None
class DungeonMylog(BaseModel):
    quest_id: int = None
    battle_log_id: int = None
    total_damage: int = None
    battle_time: int = None
    win_or_lose: int = None
    auto_type: int = None
    units: List[DungeonMylogUnit] = None
    enemy: List[DungeonMylogEnemy] = None
class SreBurstDownTargetTime(BaseModel):
    sre_boss_id: int = None
    target_time: int = None
class SreRaidBossDifficulty(BaseModel):
    difficulty: int = None
    attack_count: int = None
    enemy_status_list: List[SreEnemyUnit] = None
class SreRaidBossInfo(BaseModel):
    sre_boss_id: int = None
    raid_hp: int = None
    difficulty_list: List[SreRaidBossDifficulty] = None
class SreBonus(BaseModel):
    sre_boss_id: int = None
    start_time_list: List[int] = None
    ex_start_time_list: List[int] = None
class SrtCatalogInfo(BaseModel):
    reading_id: int = None
    status: eSrtCatalogStatus = None
class SrtHighScoreInfo(BaseModel):
    normal: int = None
    hard: int = None
    extra: int = None
class TaqRoomInfo(BaseModel):
    host_viewer_id: int = None
    difficulty_level: eTaqDifficultyLevel = None
    quiz_type: eTaqQuizType = None
    entry_type: eTaqEntryType = None
    search_no: int = None
    entry_count: int = None
    seed: int = None
    status: eTaqGameServerStatus = None
    wave_no: int = None
class TaqQuizUserInfo(BaseModel):
    viewer_id: int = None
    position: int = None
    user_name: str = None
    unit_id: int = None
    user_end_time: str = None
    is_npc: bool = None
class TaqAnswerInfo(BaseModel):
    viewer_id: int = None
    wave_no: int = None
    position: int = None
    answer_no: int = None
    is_npc: bool = None
class TaqScoreResult(BaseModel):
    room_correct_count: int = None
    room_correct_score: int = None
    personal_correct_count: int = None
    personal_correct_score: int = None
    elapsed_msec_avg: int = None
    elapsed_msec_avg_score: int = None
    coop_bonus_count: int = None
    coop_bonus_rate: float = None
    total_score: int = None
class TaqRewardInfo(BaseModel):
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
class TaqSearchRoomInfo(BaseModel):
    room_id: int = None
    host_viewer_id: int = None
    unit_id: int = None
    difficulty_level: int = None
    quiz_type: int = None
    host_user_name: str = None
    entry_count: int = None
class TaqRoomUserInfo(BaseModel):
    viewer_id: int = None
    user_name: str = None
    unit_id: int = None
    emblem_id: int = None
    clan_id: int = None
class TaqQuizBookStatus(BaseModel):
    quiz_no: int = None
    status: eTaqQuizStatus = None
class TaqSoloAnswer(BaseModel):
    wave_no: int = None
    quiz_no: int = None
    answer_no: int = None
    elapsed_msec: int = None
    answer_char_no: int = None
class TowerQueryUnit(BaseModel):
    owner_viewer_id: int = None
    unit_id: int = None
    identify_num: int = None
    damage: int = None
    hp: int = None
    energy: int = None
    skill_limit_counter: List[SkillLimitCounter] = None
class TowerClearedUserInfo(BaseModel):
    viewer_id: int = None
    user_name: str = None
    team_level: int = None
    favorite_unit: UnitDataForView = None
    cleared_time: int = None
    emblem: EmblemData = None
class ClearedExQuestList(BaseModel):
    quest_id: int = None
    ex_cleared_time: int = None
class TowerClanMemberInfo(BaseModel):
    cleared_data: TowerClearedUserInfo = None
    floor_num: int = None
    cleared_ex_quest_list: List[ClearedExQuestList] = None
    cloister_cleared_time: int = None
class TowerWaveResultUnitInfo(BaseModel):
    unit_id: int = None
    owner_viewer_id: int = None
    damage: int = None
    is_alive: int = None
class TowerWaveResultInfo(BaseModel):
    wave_num: int = None
    unit_info_list: List[TowerWaveResultUnitInfo] = None
    remain_time: int = None
class TowerExPartyInfo(BaseModel):
    first: List[UnitData] = None
    second: List[UnitData] = None
    third: List[UnitData] = None
class TowerExDispatchUnitLight(BaseModel):
    owner_viewer_id: int = None
    owner_name: str = None
    enable: int = None
    current_support_unit: int = None
    unit_data: UnitDataLight = None
class TowerExDispatchUnit(BaseModel):
    owner_viewer_id: int = None
    owner_name: str = None
    enable: int = None
    current_support_unit: int = None
    unit_data: UnitData = None
class TowerReplayPartyInfo(BaseModel):
    power: int = None
    unit_info: List[ReplayUnitDataForView] = None
class TowerReplaySummary(BaseModel):
    team_level: int = None
    win_party: int = None
    enc_key: str = None
    party_list: List[TowerReplayPartyInfo] = None
    auto_type: int = None
class TowerUnit(BaseModel):
    unit_id: int = None
    identify_num: int = None
    hp: int = None
    energy: int = None
    skill_limit_counter: List[SkillLimitCounter] = None
    max_hp: int = None
    saved_hp: int = None
    level: int = None
    rarity: int = None
    promotion_level: int = None
    enemy_color: int = None
    skin_data: SkinData = None
class TowerReplayPartyStatusList(BaseModel):
    party_status_1: List[TowerUnit] = None
    party_status_2: List[TowerUnit] = None
    party_status_3: List[TowerUnit] = None
class TowerReplayPartyList(BaseModel):
    party_1: List[UnitData] = None
    party_2: List[UnitData] = None
    party_3: List[UnitData] = None
class ClanDispatchUnit(BaseModel):
    owner_viewer_id: int = None
    owner_name: str = None
    enable: int = None
    current_support_unit: int = None
    hp: int = None
    energy: int = None
    unit_data: UnitData = None
class TravelDecreaseItem(BaseModel):
    jewel: int = None
    item: int = None
class TravelCurrentCurrencyNum(BaseModel):
    jewel: int = None
    item: int = None
class TravelQuestInfo(BaseModel):
    travel_quest_id: int = None
    travel_id: int = None
    appear_travel_id: int = None
    travel_start_time: int = None
    travel_end_time: int = None
    decrease_time: int = None
    travel_deck: List[int] = None
    total_lap_count: int = None
    received_count: int = None
    total_power: int = None
class TravelCampaignInfo(BaseModel):
    travel_id: int = None
    start_lap: int = None
    end_lap: int = None
    campaign_id_list: List[int] = None
class TravelExtraEquipAutoRecycleOptionData(BaseModel):
    rarity: List[int] = None
    frame: List[int] = None
    category: List[int] = None
class TravelAppearSecretQuest(BaseModel):
    travel_quest_id: int = None
    appear_travel_id: int = None
class TravelExtraEquipAutoRecycleResultData(BaseModel):
    ex_equipment_id: int = None
    recycle_num: int = None
class TravelAppearEventData(BaseModel):
    still_id: int = None
    reward_list: List[InventoryInfo] = None
    appear_secret_travel: TravelAppearSecretQuest = None
    ex_auto_recycle_result: List[TravelExtraEquipAutoRecycleResultData] = None
class TravelResult(BaseModel):
    travel_quest_id: int = None
    travel_id: int = None
    lap_count: int = None
    reward_list: List[InventoryInfo] = None
    acquired_gold: int = None
    appear_event_list: List[TravelAppearEventData] = None
    ex_auto_recycle_result: List[TravelExtraEquipAutoRecycleResultData] = None
class TravelStartInfo(BaseModel):
    travel_quest_id: int = None
    travel_deck: List[int] = None
    decrease_time_item: TravelDecreaseItem = None
    total_lap_count: int = None
class TravelQuestAddLap(BaseModel):
    travel_id: int = None
    add_lap_count: int = None
class SecretTravelStartInfo(BaseModel):
    travel_quest_id: int = None
    appear_travel_id: int = None
    travel_deck: List[int] = None
    decrease_time_item: TravelDecreaseItem = None
    total_lap_count: int = None
class TravelAppearTopEvent(BaseModel):
    top_event_appear_id: int = None
    top_event_id: int = None
    top_event_pos_id: int = None
    top_event_rarity: int = None
    top_event_choice_flag: int = None
    top_event_skin_id_list: List[int] = None
    TopEventPattern: int = None
    IsDebugCreate: bool = None
    IsDebugDispTreasure: bool = None
    DebugChoiceSelectDramaId: int = None
    DebugDispRewardNum: int = None
class TrialBattleFinishUnit(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitHpInfo] = None
class TrialBattleSupportUnit(BaseModel):
    unit_data: UnitDataLight = None
    owner_viewer_id: int = None
    owner_name: str = None
    UnitParamData: UnitData = None
class TrialBattleQuestInfo(BaseModel):
    quest_id: int = None
    clear_flg: int = None
class TtkBeatEnemyInfo(BaseModel):
    enemy_id: int = None
    beat_num: int = None
class TtkHighScoreInfo(BaseModel):
    normal: int = None
    hard: int = None
    extra: int = None
    endless: int = None
class TtkCatalogInfo(BaseModel):
    enemy_id: int = None
    total_beat_num: int = None
    status: int = None
class TutorialStoryQuestStart(BaseModel):
    quest_wave_info: List[WaveEnemyInfoList] = None
    limit_time: int = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    user_info: UserStaminaInfo = None
    guest_data: List[UnitData] = None
class PrologueFirstStep(BaseModel):
    story_quest_start: TutorialStoryQuestStart = None
class PrologueLatterDStep(BaseModel):
    story_quest_start: TutorialStoryQuestStart = None
class TutorialHomeIndex(BaseModel):
    mission_count: int = None
    unread_message_count: int = None
    user_clan: UserClan = None
class TutorialQuestStart(BaseModel):
    quest_wave_info: List[WaveEnemyInfoList] = None
    limit_time: int = None
    quest_id: int = None
    enemy_list: List[UnitData] = None
    user_info: UserStaminaInfo = None
    battle_log_id: int = None
class TutorialQuestFinish(BaseModel):
    level_info: LevelInfo = None
    user_info: UserStaminaInfo = None
    flag_exchange_team_exp: bool = None
    unlock_quest_list: List[int] = None
    open_story_ids: List[UserStory] = None
    quest_id: int = None
    clear_flag: int = None
    result_type: int = None
    daily_clear_count: int = None
    rewards: List[InventoryInfo] = None
    add_present_count: int = None
class QuestOneStep(BaseModel):
    home_index: TutorialHomeIndex = None
    quest_start: TutorialQuestStart = None
    quest_finish: TutorialQuestFinish = None
class TutorialUnitEquip(BaseModel):
    unit_data: UnitData = None
    equip_data: InventoryInfo = None
class EquipStep(BaseModel):
    unit_equip_1: TutorialUnitEquip = None
    unit_equip_2: TutorialUnitEquip = None
class TutorialGachaIndex(BaseModel):
    gacha_info: List[GachaParameter] = None
class GachaStep(BaseModel):
    gacha_index: TutorialGachaIndex = None
class TutorialGachaExec(BaseModel):
    reward_info_list: List[InventoryInfo] = None
    add_present_count: int = None
class QuestTwoStep(BaseModel):
    gacha_exec: TutorialGachaExec = None
    home_index: TutorialHomeIndex = None
    quest_start: TutorialQuestStart = None
    quest_finish: TutorialQuestFinish = None
class TutorialMissionIndex(BaseModel):
    missions: List[UserMissionInfo] = None
    daily_reset_time: int = None
class TutorialMissionAccept(BaseModel):
    team_level: int = None
    team_exp: int = None
    stamina_info: UserStaminaInfo = None
    rewards: List[InventoryInfo] = None
    flag_exchange_team_exp: bool = None
    add_present_count: int = None
class MissionStep(BaseModel):
    mission_index: TutorialMissionIndex = None
    mission_accept: TutorialMissionAccept = None
class UekBossInfo(BaseModel):
    enemy_id: int = None
    hp: int = None
    attack_num: int = None
class EnhanceRecipe(BaseModel):
    id: int = None
    type: int = None
    count: int = None
    current_count: int = None
class ExtraEquipChangeSlot(BaseModel):
    slot: int = None
    serial_id: int = None
class ExtraEquipChangeUnit(BaseModel):
    unit_id: int = None
    ex_equip_slot: List[ExtraEquipChangeSlot] = None
    cb_ex_equip_slot: List[ExtraEquipChangeSlot] = None
class EnhanceSlot(BaseModel):
    slot_num: int = None
    current_enhancement_pt: int = None
    enhance_item_list: List[InventoryInfoPost] = None
class MultiAutomaticEnhance(BaseModel):
    unit_id: int = None
    levelup_item_list: List[ItemInfo] = None
    skill_levelup_list: List[SkillLevelUpDetail] = None
    equip_slot_num_list: List[int] = None
    equip_recipe_list: List[UserEquipParameterIdCount] = None
    enhance_slot_list: List[EnhanceSlot] = None
class RequiredMaterialList(BaseModel):
    equip_list: List[UserEquipParameterIdCount] = None
class UserMyQuestForPost(BaseModel):
    tab_number: int = None
    tab_name: str = None
    skip_count: int = None
    skip_list: List[int] = None
class InviteClanDetail(BaseModel):
    clan_id: int = None
    leader_viewer_id: int = None
    invite_id: int = None
    leader_name: str = None
    leader_favorite_unit: UnitDataForView = None
    clan_name: str = None
    description: str = None
    invite_message: str = None
    join_condition: eClanJoinCondition = None
    activity: eClanActivityGuideline = None
    clan_battle_mode: int = None
    member_num: int = None
    grade_rank: int = None
class VotedUnit(BaseModel):
    rarity_1: int = None
    rarity_2: int = None
    rarity_3: int = None
class VoteRank(BaseModel):
    rank: int = None
    unit_id: int = None
    ratio: int = None
class VoteRanking(BaseModel):
    rarity_1: List[VoteRank] = None
    rarity_2: List[VoteRank] = None
    rarity_3: List[VoteRank] = None
class AbyssBossScoreReward(BaseModel):
    reward_list: List[InventoryInfo] = None
class AbyssUserBoss(BaseModel):
    boss_id: int = None
    EnemyIndex: int = None
    boss_hp: int = None
    BestDamage: int = None
class AbyssDailyClearCountList(BaseModel):
    quest_id: int = None
    daily_clear_count: int = None
class AbyssQuestSkipResult(BaseModel):
    quest_id: int = None
    quest_result: List[QuestResult] = None
class AcnBattleFinishUnit(BaseModel):
    unit_damage_list: List[UnitDamageInfo] = None
    unit_hp_list: List[UnitHpInfo] = None
class AcnMission(BaseModel):
    mission_id: int = None
    mission_status: eMissionStatusType = None
    clear_num: int = None
class AcnModeInfo(BaseModel):
    seed: int = None
    mode: int = None
class AcnEndlessBattleInfo(BaseModel):
    difficulty: int = None
    TodayIndividualKillCount: int = None
    IndividualTotalKillCount: int = None
class AcnEnemyUnit(BaseModel):
    unit_id: int = None
    hp: int = None
class AcnBossBattleInfo(BaseModel):
    quest_id: int = None
    difficulty: int = None
    IndividualTotalKillCount: int = None
    challenge_count: int = None
    enemy_status_list: List[AcnEnemyUnit] = None
class AcnSpecialBattleInfo(BaseModel):
    IndividualTotalKillCount: int = None
    challenge_count: int = None
    enemy_unit: List[AcnEnemyUnit] = None
    enemy_point: int = None
    mode: int = None
class AcnUnknownBattleInfo(BaseModel):
    IndividualTotalKillCount: int = None
    challenge_count: int = None
    enemy_unit: List[AcnEnemyUnit] = None
    step: int = None
class AcnUnlockQuestMission(BaseModel):
    mission_id: int = None
    start_time: int = None
    progress: int = None
    story_id: int = None
    end_time: int = None
class AcnUnknownEnemyUnit(BaseModel):
    unit_id: int = None
    current_hp: int = None
class ArenaDefendInfo(BaseModel):
    round_max_limited_times: int = None
    daily_max_limited_times: int = None
    round_times: int = None
    round_end_time: int = None
    daily_times: int = None
class TalentLevelInfo(BaseModel):
    talent_id: int = None
    total_point: int = None
class TalentSkillNodeInfo(BaseModel):
    node_id: int = None
    enhance_level: int = None
class TeamSkillNodeInfo(BaseModel):
    node_id: int = None
    enhance_level: int = None
class PrincessKnightInfo(BaseModel):
    TalentLevelInfoList: List[TalentLevelInfo] = None
    TalentSkillLastEnhancedPageNodeList: List[TalentSkillNodeInfo] = None
    TeamSkillLatestNode: TeamSkillNodeInfo = None
class AsmAnswerInfo(BaseModel):
    wave_no: int = None
    asm_id: int = None
    answer: List[int] = None
    elapsed_msec: int = None
    is_correct: bool = None
class AsmScoreResult(BaseModel):
    correct_count: int = None
    correct_score: int = None
    elapsed_msec_avg: int = None
    elapsed_msec_avg_score: int = None
    total_score: int = None
    past_high_score: int = None
class AsmRewardInfo(BaseModel):
    trigger_score: int = None
    reward_type: eInventoryType = None
    reward_id: int = None
    reward_count: int = None
class AsmUnlockStory(BaseModel):
    trigger_score: int = None
    story_id: int = None
class AsmMemoryGaugeEmblem(BaseModel):
    trigger_score: int = None
    emblem_id: int = None
class AsmCompletionEmblem(BaseModel):
    archive_num: int = None
    emblem_id: int = None
class AsmArchiveInfo(BaseModel):
    asm_id: int = None
    status: int = None
class AsmMemoryGaugeInfo(BaseModel):
    gauge_id: int = None
    score: int = None
class BywayDeliveryItemInfo(BaseModel):
    slot_id: int = None
    condition_id: int = None
    consume_num: int = None
class BuyBulkBuyItemList(BaseModel):
    slot_id: int = None
    count: int = None
class RollResultListData(BaseModel):
    RollTurnNum: int = None
    spots_list: List[int] = None
class RivalInfo(BaseModel):
    rival_id: int = None
    block_id: int = None
    skip_count: int = None
    minigame_id: int = None
    minigame_start_count: int = None
    minigame_retire_reward: List[InventoryInfo] = None
    spots: int = None
    spots_list: List[int] = None
    after_block_id: int = None
    next_rival_id: int = None
    rate: int = None
class CaravanDishSellData(BaseModel):
    id: int = None
    current_num: int = None
    sell_num: int = None
class CaravanDishData(BaseModel):
    id: int = None
    stock: int = None
class CaravanShopBlockLineup(BaseModel):
    slot_id: int = None
    type: int = None
    item_id: int = None
    num: int = None
    price: int = None
    discounted_price: int = None
    discount_rate: int = None
    is_sold: int = None
class CccFinishItemCountInfo(BaseModel):
    ccc_object_id: int = None
    count: int = None
class CaravanGoalBonusTreasureData(BaseModel):
    id: int = None
    count: int = None
class CaravanTreasureAppraisalData(BaseModel):
    id: int = None
    result_id: int = None
class CaravanDishEffectData(BaseModel):
    id: int = None
    effect_turn: int = None
    effect_count: int = None
class CaravanEventEffectData(BaseModel):
    event_id: int = None
    effect_turn: int = None
    effect_count: int = None
class CaravanTreasureData(BaseModel):
    id: int = None
    stock: int = None
class CaravanCoinShopData(BaseModel):
    slot_id: int = None
    purchase_count: int = None
class CaravanResetTreasureData(BaseModel):
    id: int = None
    count: int = None
class CaravanTopGoalReward(BaseModel):
    goal_turn: int = None
    lottery_result_list: List[InventoryInfo] = None
    treasure_appraisal_list: List[CaravanTreasureAppraisalData] = None
    reset_treasure_list: List[CaravanResetTreasureData] = None
class CaravanBuddyListInfoData(BaseModel):
    buddy_id: int = None
    turn: int = None
    exec_count: int = None
    is_appear: bool = None
class DiceMultiRollSpotsData(BaseModel):
    spots: int = None
    RemainSpots: int = None
    IsAppliedTurn: int = None
class ColosseumBattleFinishUnitInfo(BaseModel):
    damage: int = None
    unit_id: int = None
    hp: int = None
    passive_skill_hp: int = None
class ColosseumScore(BaseModel):
    quest_id: int = None
    score: int = None
    battle_point: int = None
    win_point: int = None
    enemy_hp_point: int = None
    unit_hp_point: int = None
    team_level: int = None
    remain_time: int = None
    remain_time_point: int = None
    bonus_applied_point_1: int = None
    bonus_applied_point_2: int = None
class ColosseumUnitDamageInfo(BaseModel):
    is_my_unit: int = None
    unit_id: int = None
    damage: int = None
class ColosseumHistoryInfo(BaseModel):
    replay_log_id: int = None
    win_or_lose: int = None
    user_unit_info: List[UnitDataForView] = None
    versus_user_unit_info: List[UnitDataForView] = None
    damage_list: List[ColosseumUnitDamageInfo] = None
    score: ColosseumScore = None
class ColosseumRankingInfo(BaseModel):
    rank: int = None
    team_level: int = None
    user_name: str = None
    emblem: EmblemData = None
    favorite_unit: UnitDataForView = None
    total_score: int = None
class DomeBattleFinishUnitInfo(BaseModel):
    damage: int = None
    unit_id: int = None
    hp: int = None
    passive_skill_hp: int = None
class DomeQuestChallengeStatus(BaseModel):
    quest_id: int = None
    StatusList: List[int] = None
class DomeUnitDamageInfo(BaseModel):
    is_my_unit: int = None
    unit_id: int = None
    damage: int = None
class DomeHistoryInfo(BaseModel):
    replay_log_id: int = None
    win_or_lose: int = None
    user_unit_info: List[UnitDataForView] = None
    versus_user_unit_info: List[UnitDataForView] = None
    damage_list: List[DomeUnitDamageInfo] = None
class GachaBonusResultList(BaseModel):
    bonus_1: List[InventoryInfo] = None
    bonus_2: List[InventoryInfo] = None
    bonus_3: List[InventoryInfo] = None
    bonus_4: List[InventoryInfo] = None
    bonus_5: List[InventoryInfo] = None
    bonus_6: List[InventoryInfo] = None
    bonus_7: List[InventoryInfo] = None
    bonus_8: List[InventoryInfo] = None
    bonus_9: List[InventoryInfo] = None
    bonus_10: List[InventoryInfo] = None
class MonthlyFreeGachaInfo(BaseModel):
    fg1_exec_cnt: int = None
    fg1_last_exec_time: int = None
    fg10_exec_cnt: int = None
    fg10_last_exec_time: int = None
class ExPlusInfo(BaseModel):
    enemy_unit: List[UnitHpInfo] = None
    enemy_point: int = None
    mode: int = None
class HatsuneQuestBulkSkipInfo(BaseModel):
    skip_count: int = None
    skip_list: List[int] = None
class StorySkipInfo(BaseModel):
    skip_type: eStorySkipType = None
    scroll_coordinate: str = None
class TopicStoryInfo(BaseModel):
    sub_story_id: int = None
    point: int = None
    is_unlocked: bool = None
class GetTopicInfo(BaseModel):
    idx: int = None
    TopicId: int = None
    IsPointUp: bool = None
class TopicAddInfo(BaseModel):
    GuestCharaIndex: int = None
    AdditionalTopicList: List[GetTopicInfo] = None
class ExpectedTopicFixedInfo(BaseModel):
    TopicId: int = None
    count: int = None
class ExpectedTopicInfo(BaseModel):
    chara_index: int = None
    ExpectedTopicList: List[ExpectedTopicFixedInfo] = None
    RandomTopicCount: int = None
    IsShowSign: bool = None
class BeginnerCharaExchangeTicketProductData(BaseModel):
    csv_data_id: int = None
    beginner_id: int = None
    ticket_id: int = None
    ticket_count: int = None
    forced_exchange_time: int = None
    number_of_product_purchased: int = None
    start_time: int = None
    end_time: int = None
class SeasonPassData(BaseModel):
    SeasonPassRewards: Dict[int, List[int]] = None
    HasBuy: bool = None
    point_limit_flag: int = None
    exchange_rewards: List[InventoryInfo] = None
    season_id: int = None
    is_buy: int = None
    seasonpass_level: int = None
    user_point: int = None
    weekly_point: int = None
    missions: List[UserMissionInfo] = None
    received_rewards: List[int] = None
class StoryBookmarkInfo(BaseModel):
    command_index: int = None
    tag_number_list: List[int] = None
class StoryBookmark(BaseModel):
    story_id: int = None
    bookmark_info: StoryBookmarkInfo = None
    StoryGroupId: int = None
class TalentQuestAreaInfo(BaseModel):
    TalentId: int = None
    DailyBonusUseCount: int = None
    daily_clear_count: int = None
    daily_recovery_count: int = None
class GuaranteeGachaCounter(BaseModel):
    gacha_id: int = None
    remain_exec_count: int = None
class BannerLinkedPackList(BaseModel):
    id: int = None
    remaining_count: int = None
    start_time: int = None
    end_time: int = None
class MonthlyGachaInfo(BaseModel):
    end_time: int = None
    original_gacha_id: int = None
    exchange_num: int = None
    max_exchange_num: int = None
    gacha_point_info: GachaPointInfo = None
class TotalScoreList(BaseModel):
    NbbCharaType: int = None
    total_score: int = None
class HighScoreList(BaseModel):
    difficulty: int = None
    high_score: int = None
class RenameAvailableTimes(BaseModel):
    user_name: int = None
    user_comment: int = None
class TalentQuestRecoverInfo(BaseModel):
    TalentId: int = None
    daily_recovery_count: int = None
class ExchangeRewards(BaseModel):
    id: int = None
    type: int = None
    count: int = None
    stock: int = None
    received: int = None
class TravelRoundEventResult(BaseModel):
    result: eRoundEventResultType = None
    result_drama_id: int = None
    reward_list: List[InventoryInfo] = None
class TravelAppearRoundEvent(BaseModel):
    round_event_id: int = None
    skin_id_list: List[int] = None
    round: int = None
    left_door_effect_id: int = None
    right_door_effect_id: int = None
    expect_reward_list: List[InventoryInfo] = None
class MultiAutomaticPromotion(BaseModel):
    unit_id: int = None
    equip_recipe_list: List[RequiredMaterialList] = None
    item_list: List[ItemInfo] = None
