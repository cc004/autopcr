# coding: utf-8
from sqlalchemy import Column, Float, Index, Integer, Table, Text, UniqueConstraint
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import Session, declarative_base
from typing import Generic, TypeVar, List
from ..util.linq import flow

T = TypeVar('T')

DeclarativeBase = declarative_base()

class Base(Generic[T]):
    @classmethod
    def query(cls, session: Session) -> flow[T]:
        dat = session.query(UniqueEquipmentEnhanceDatum)
        return flow(session.query(cls).all())

class ActualUnitBackground(DeclarativeBase, Base["ActualUnitBackground"]):
    __tablename__ = 'actual_unit_background'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(Text, nullable=False)
    bg_id = Column(Integer, nullable=False)
    face_type = Column(Integer, nullable=False)


class AilmentDatum(DeclarativeBase, Base["AilmentDatum"]):
    __tablename__ = 'ailment_data'

    ailment_id = Column(Integer, primary_key=True)
    ailment_action = Column(Integer, nullable=False)
    ailment_detail_1 = Column(Integer, nullable=False)
    ailment_name = Column(Text, nullable=False)


class AlbumProductionList(DeclarativeBase, Base["AlbumProductionList"]):
    __tablename__ = 'album_production_list'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False, index=True)
    type = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class AlbumVoiceList(DeclarativeBase, Base["AlbumVoiceList"]):
    __tablename__ = 'album_voice_list'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False, index=True)
    sheet_id = Column(Text, nullable=False)
    voice_id = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class ApaSchedule(DeclarativeBase, Base["ApaSchedule"]):
    __tablename__ = 'apa_schedule'

    apa_id = Column(Integer, primary_key=True)
    start_time = Column(Text, nullable=False)
    count_start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    close_time = Column(Text, nullable=False)
    op_story_id = Column(Integer, nullable=False)
    ed_story_id = Column(Integer, nullable=False)
    url_1 = Column(Text, nullable=False)
    url_2 = Column(Text, nullable=False)
    url_3 = Column(Text, nullable=False)


class ArcadeDescription(DeclarativeBase, Base["ArcadeDescription"]):
    __tablename__ = 'arcade_description'
    __table_args__ = (
        Index('arcade_description_0_arcade_id_1_type', 'arcade_id', 'type'),
    )

    id = Column(Integer, primary_key=True)
    arcade_id = Column(Integer, nullable=False, index=True)
    type = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class ArcadeList(DeclarativeBase, Base["ArcadeList"]):
    __tablename__ = 'arcade_list'

    arcade_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    cue_id = Column(Text, nullable=False)
    where_type = Column(Integer, nullable=False)
    banner_start_time = Column(Text, nullable=False)
    banner_end_time = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class ArcadeStoryList(DeclarativeBase, Base["ArcadeStoryList"]):
    __tablename__ = 'arcade_story_list'

    story_id = Column(Integer, primary_key=True)
    arcade_id = Column(Integer, nullable=False, index=True)
    sub_title = Column(Text, nullable=False)


class ArenaDailyRankReward(DeclarativeBase, Base["ArenaDailyRankReward"]):
    __tablename__ = 'arena_daily_rank_reward'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ArenaDefenceReward(DeclarativeBase, Base["ArenaDefenceReward"]):
    __tablename__ = 'arena_defence_reward'

    id = Column(Integer, primary_key=True)
    limit_count = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ArenaMaxRankReward(DeclarativeBase, Base["ArenaMaxRankReward"]):
    __tablename__ = 'arena_max_rank_reward'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ArenaMaxSeasonRankReward(DeclarativeBase, Base["ArenaMaxSeasonRankReward"]):
    __tablename__ = 'arena_max_season_rank_reward'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class Banner(DeclarativeBase, Base["Banner"]):
    __tablename__ = 'banner'

    banner_id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    system_id = Column(Integer, nullable=False)
    gacha_id = Column(Integer, nullable=False)
    condition_id = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text, nullable=False)
    sub_banner_id_1 = Column(Integer, nullable=False)
    is_show_room = Column(Integer, nullable=False)
    url = Column(Text, nullable=False)
    show_type = Column(Integer, nullable=False)
    thumbnail_id = Column(Integer, nullable=False)
    poster_id = Column(Integer, nullable=False)


class BgDatum(DeclarativeBase, Base["BgDatum"]):
    __tablename__ = 'bg_data'

    view_name = Column(Text, primary_key=True)
    bg_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class BirthdayLoginBonusDatum(DeclarativeBase, Base["BirthdayLoginBonusDatum"]):
    __tablename__ = 'birthday_login_bonus_data'

    login_bonus_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    login_bonus_type = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    adv_id = Column(Integer, nullable=False)


class BirthdayLoginBonusDetail(DeclarativeBase, Base["BirthdayLoginBonusDetail"]):
    __tablename__ = 'birthday_login_bonus_detail'

    id = Column(Integer, primary_key=True)
    login_bonus_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_num = Column(Integer, nullable=False)


class BirthdayLoginBonusDramaScript(DeclarativeBase, Base["BirthdayLoginBonusDramaScript"]):
    __tablename__ = 'birthday_login_bonus_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class CampaignBeginnerDatum(DeclarativeBase, Base["CampaignBeginnerDatum"]):
    __tablename__ = 'campaign_beginner_data'

    beginner_id = Column(Integer, primary_key=True)
    id_from = Column(Integer, nullable=False)
    id_to = Column(Integer, nullable=False)


class CampaignFreegacha(DeclarativeBase, Base["CampaignFreegacha"]):
    __tablename__ = 'campaign_freegacha'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, nullable=False)
    freegacha_1 = Column(Integer, nullable=False)
    freegacha_10 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    stock_10_flag = Column(Integer, nullable=False)
    relation_id = Column(Integer, nullable=False)
    relation_count = Column(Integer, nullable=False)


class CampaignFreegachaDatum(DeclarativeBase, Base["CampaignFreegachaDatum"]):
    __tablename__ = 'campaign_freegacha_data'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, nullable=False)
    gacha_id = Column(Integer, nullable=False)


class CampaignFreegachaSp(DeclarativeBase, Base["CampaignFreegachaSp"]):
    __tablename__ = 'campaign_freegacha_sp'

    campaign_id = Column(Integer, primary_key=True)
    max_exec_count = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class CampaignLevelDatum(DeclarativeBase, Base["CampaignLevelDatum"]):
    __tablename__ = 'campaign_level_data'

    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, nullable=False)
    lv_from = Column(Integer, nullable=False)
    lv_to = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    label_color = Column(Text, nullable=False)
    frame_color = Column(Text, nullable=False)


class CampaignMissionCategory(DeclarativeBase, Base["CampaignMissionCategory"]):
    __tablename__ = 'campaign_mission_category'
    __table_args__ = (
        Index('campaign_mission_category_0_campaign_id_1_type', 'campaign_id', 'type'),
    )

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    lv_from = Column(Integer, nullable=False)
    lv_to = Column(Integer, nullable=False)


class CampaignMissionDatum(DeclarativeBase, Base["CampaignMissionDatum"]):
    __tablename__ = 'campaign_mission_data'
    __table_args__ = (
        Index('campaign_mission_data_0_campaign_id_1_type', 'campaign_id', 'type'),
    )

    mission_id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, nullable=False, index=True)
    type = Column(Integer, nullable=False)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_value_4 = Column(Integer)
    condition_value_5 = Column(Integer)
    condition_value_6 = Column(Integer)
    condition_value_7 = Column(Integer)
    condition_value_8 = Column(Integer)
    condition_value_9 = Column(Integer)
    condition_value_10 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    campaign_mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    min_level = Column(Integer, nullable=False)
    max_level = Column(Integer, nullable=False)
    title_color_id = Column(Integer, nullable=False)
    visible_flag = Column(Integer, nullable=False)
    mark_flag = Column(Integer, nullable=False)


class CampaignMissionRewardDatum(DeclarativeBase, Base["CampaignMissionRewardDatum"]):
    __tablename__ = 'campaign_mission_reward_data'

    id = Column(Integer, primary_key=True)
    campaign_mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer)
    reward_num = Column(Integer, nullable=False)


class CampaignMissionSchedule(DeclarativeBase, Base["CampaignMissionSchedule"]):
    __tablename__ = 'campaign_mission_schedule'

    campaign_id = Column(Integer, primary_key=True)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    close_time = Column(Text, nullable=False)


class CampaignSchedule(DeclarativeBase, Base["CampaignSchedule"]):
    __tablename__ = 'campaign_schedule'

    id = Column(Integer, primary_key=True)
    campaign_category = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    system_id = Column(Integer, nullable=False)
    icon_image = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    level_id = Column(Integer, nullable=False)
    shiori_group_id = Column(Integer, nullable=False)
    duplication_order = Column(Integer, nullable=False)
    beginner_id = Column(Integer, nullable=False)


class CampaignShioriGroup(DeclarativeBase, Base["CampaignShioriGroup"]):
    __tablename__ = 'campaign_shiori_group'

    id = Column(Integer, primary_key=True)
    shiori_group_id = Column(Integer, nullable=False, index=True)
    event_id = Column(Integer, nullable=False)


class CggCompletionDatum(DeclarativeBase, Base["CggCompletionDatum"]):
    __tablename__ = 'cgg_completion_data'

    completion_id = Column(Integer, primary_key=True)
    completion_emblem_id = Column(Integer, nullable=False)
    gacha_type = Column(Integer, nullable=False)
    completion_num = Column(Integer, nullable=False)
    secret_goods_id_1 = Column(Integer, nullable=False)
    secret_goods_id_2 = Column(Integer, nullable=False)
    secret_goods_id_3 = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    receive_description = Column(Text, nullable=False)


class CggCompletionRewardDatum(DeclarativeBase, Base["CggCompletionRewardDatum"]):
    __tablename__ = 'cgg_completion_reward_data'

    id = Column(Integer, primary_key=True)
    completion_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_num = Column(Integer, nullable=False)


class CggDrama(DeclarativeBase, Base["CggDrama"]):
    __tablename__ = 'cgg_drama'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class CggGachaInfo(DeclarativeBase, Base["CggGachaInfo"]):
    __tablename__ = 'cgg_gacha_info'

    gacha_type = Column(Integer, primary_key=True)
    cgg_id = Column(Integer, nullable=False, index=True)
    gacha_name = Column(Text, nullable=False)
    gacha_description = Column(Text, nullable=False)
    cost_currency_num = Column(Integer, nullable=False)
    gacha_intro = Column(Text, nullable=False)


class CggGachaLineup(DeclarativeBase, Base["CggGachaLineup"]):
    __tablename__ = 'cgg_gacha_lineup'

    id = Column(Integer, primary_key=True)
    gacha_type = Column(Integer, nullable=False, index=True)
    lineup_id = Column(Integer, nullable=False)
    goods_id = Column(Integer, nullable=False)
    goods_num = Column(Integer, nullable=False)


class CggGameSetting(DeclarativeBase, Base["CggGameSetting"]):
    __tablename__ = 'cgg_game_settings'

    cgg_id = Column(Integer, primary_key=True)
    goods_shelf_id = Column(Integer, nullable=False)
    first_goods_shelf_reward_num = Column(Integer, nullable=False)
    cgg_gacha_currency_id = Column(Integer, nullable=False)
    first_currency_reward_num = Column(Integer, nullable=False)
    exchange_luppi_rate = Column(Integer, nullable=False)
    max_gacha_exchange_count = Column(Integer, nullable=False)
    max_goods_count = Column(Integer, nullable=False)


class CggGoodsDatum(DeclarativeBase, Base["CggGoodsDatum"]):
    __tablename__ = 'cgg_goods_data'

    goods_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    rarity = Column(Integer, nullable=False)
    shelf_position_id = Column(Integer, nullable=False)
    detail_scale_x = Column(Float, nullable=False)
    detail_scale_y = Column(Float, nullable=False)
    description = Column(Text, nullable=False)


class CharaETicketDatum(DeclarativeBase, Base["CharaETicketDatum"]):
    __tablename__ = 'chara_e_ticket_data'

    ticket_id = Column(Integer, primary_key=True)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    jewel_store_id = Column(Integer, nullable=False, unique=True)
    icon_id = Column(Integer, nullable=False)


class CharaFortuneRail(DeclarativeBase, Base["CharaFortuneRail"]):
    __tablename__ = 'chara_fortune_rail'

    rail_id = Column(Integer, primary_key=True)
    gimmick_1_id = Column(Text, nullable=False)
    gimmick_1_x = Column(Integer, nullable=False)
    gimmick_2_id = Column(Text, nullable=False)
    gimmick_2_x = Column(Integer, nullable=False)
    gimmick_3_id = Column(Text, nullable=False)
    gimmick_3_x = Column(Integer, nullable=False)
    gimmick_4_id = Column(Text, nullable=False)
    gimmick_4_x = Column(Integer, nullable=False)
    gimmick_5_id = Column(Text, nullable=False)
    gimmick_5_x = Column(Integer, nullable=False)
    gimmick_6_id = Column(Text, nullable=False)
    gimmick_6_x = Column(Integer, nullable=False)
    gimmick_7_id = Column(Text, nullable=False)
    gimmick_7_x = Column(Integer, nullable=False)
    gimmick_8_id = Column(Text, nullable=False)
    gimmick_8_x = Column(Integer, nullable=False)
    gimmick_9_id = Column(Text, nullable=False)
    gimmick_9_x = Column(Integer, nullable=False)
    gimmick_10_id = Column(Text, nullable=False)
    gimmick_10_x = Column(Integer, nullable=False)


class CharaFortuneReward(DeclarativeBase, Base["CharaFortuneReward"]):
    __tablename__ = 'chara_fortune_reward'

    id = Column(Integer, primary_key=True)
    fortune_id = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    count_5 = Column(Integer, nullable=False)


class CharaFortuneScenario(DeclarativeBase, Base["CharaFortuneScenario"]):
    __tablename__ = 'chara_fortune_scenario'

    scenario_id = Column(Integer, primary_key=True)
    rail_1 = Column(Integer, nullable=False)
    rail_2 = Column(Integer, nullable=False)
    rail_3 = Column(Integer, nullable=False)
    rail_4 = Column(Integer, nullable=False)


class CharaFortuneSchedule(DeclarativeBase, Base["CharaFortuneSchedule"]):
    __tablename__ = 'chara_fortune_schedule'

    fortune_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class CharaIdentity(DeclarativeBase, Base["CharaIdentity"]):
    __tablename__ = 'chara_identity'

    unit_id = Column(Integer, primary_key=True)
    chara_type = Column(Integer, nullable=False)
    chara_type_2 = Column(Integer, nullable=False)
    chara_type_3 = Column(Integer, nullable=False)


class CharaStoryStatu(DeclarativeBase, Base["CharaStoryStatu"]):
    __tablename__ = 'chara_story_status'

    story_id = Column(Integer, primary_key=True)
    unlock_story_name = Column(Text, nullable=False)
    status_type_1 = Column(Integer, nullable=False)
    status_rate_1 = Column(Integer, nullable=False)
    status_type_2 = Column(Integer, nullable=False)
    status_rate_2 = Column(Integer, nullable=False)
    status_type_3 = Column(Integer, nullable=False)
    status_rate_3 = Column(Integer, nullable=False)
    status_type_4 = Column(Integer, nullable=False)
    status_rate_4 = Column(Integer, nullable=False)
    status_type_5 = Column(Integer, nullable=False)
    status_rate_5 = Column(Integer, nullable=False)
    chara_id_1 = Column(Integer, nullable=False)
    chara_id_2 = Column(Integer, nullable=False)
    chara_id_3 = Column(Integer, nullable=False)
    chara_id_4 = Column(Integer, nullable=False)
    chara_id_5 = Column(Integer, nullable=False)
    chara_id_6 = Column(Integer, nullable=False)
    chara_id_7 = Column(Integer, nullable=False)
    chara_id_8 = Column(Integer, nullable=False)
    chara_id_9 = Column(Integer, nullable=False)
    chara_id_10 = Column(Integer, nullable=False)


class CharacterLoveRankupText(DeclarativeBase, Base["CharacterLoveRankupText"]):
    __tablename__ = 'character_love_rankup_text'

    chara_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    love_level = Column(Integer, nullable=False)
    scale = Column(Float, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    voice_id_1 = Column(Integer, nullable=False)
    face_1 = Column(Integer, nullable=False)
    serif_1 = Column(Text, nullable=False)
    voice_id_2 = Column(Integer, nullable=False)
    face_2 = Column(Integer, nullable=False)
    serif_2 = Column(Text, nullable=False)
    voice_id_3 = Column(Integer, nullable=False)
    face_3 = Column(Integer, nullable=False)
    serif_3 = Column(Text, nullable=False)


class ClanBattle2BossDatum(DeclarativeBase, Base["ClanBattle2BossDatum"]):
    __tablename__ = 'clan_battle_2_boss_data'

    boss_id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    order_num = Column(Integer, nullable=False)
    boss_thumb_id = Column(Integer, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    scale_ratio = Column(Float, nullable=False)
    tap_width_ratio = Column(Float, nullable=False)
    tap_height_ratio = Column(Float, nullable=False)
    map_position_x = Column(Integer, nullable=False)
    map_position_y = Column(Integer, nullable=False)
    cursor_position = Column(Integer, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)
    quest_detail_monster_size = Column(Float, nullable=False)
    quest_detail_monster_height = Column(Integer, nullable=False)
    battle_report_monster_size = Column(Float, nullable=False)
    battle_report_monster_height = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    wave_bgm = Column(Text, nullable=False)


class ClanBattle2MapDatum(DeclarativeBase, Base["ClanBattle2MapDatum"]):
    __tablename__ = 'clan_battle_2_map_data'

    id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False, index=True)
    map_bg = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    lap_num_from = Column(Integer, nullable=False)
    lap_num_to = Column(Integer, nullable=False)
    boss_id_1 = Column(Integer, nullable=False)
    boss_id_2 = Column(Integer, nullable=False)
    boss_id_3 = Column(Integer, nullable=False)
    boss_id_4 = Column(Integer, nullable=False)
    boss_id_5 = Column(Integer, nullable=False)
    aura_effect = Column(Integer, nullable=False)
    rsl_unlock_lap = Column(Integer, nullable=False)
    phase = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_group_id_4 = Column(Integer, nullable=False)
    wave_group_id_5 = Column(Integer, nullable=False)
    fix_reward_id_1 = Column(Integer, nullable=False)
    fix_reward_id_2 = Column(Integer, nullable=False)
    fix_reward_id_3 = Column(Integer, nullable=False)
    fix_reward_id_4 = Column(Integer, nullable=False)
    fix_reward_id_5 = Column(Integer, nullable=False)
    damage_rank_id_1 = Column(Integer, nullable=False)
    damage_rank_id_2 = Column(Integer, nullable=False)
    damage_rank_id_3 = Column(Integer, nullable=False)
    damage_rank_id_4 = Column(Integer, nullable=False)
    damage_rank_id_5 = Column(Integer, nullable=False)
    reward_gold_coefficient = Column(Float, nullable=False)
    limited_mana = Column(Integer, nullable=False)
    last_attack_reward_id = Column(Integer, nullable=False)
    score_coefficient_1 = Column(Float, nullable=False)
    score_coefficient_2 = Column(Float, nullable=False)
    score_coefficient_3 = Column(Float, nullable=False)
    score_coefficient_4 = Column(Float, nullable=False)
    score_coefficient_5 = Column(Float, nullable=False)
    param_adjust_id = Column(Integer, nullable=False)
    param_adjust_interval = Column(Integer, nullable=False)


class ClanBattleArchiveClanRank(DeclarativeBase, Base["ClanBattleArchiveClanRank"]):
    __tablename__ = 'clan_battle_archive_clan_rank'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)


class ClanBattleArchivePersonRank(DeclarativeBase, Base["ClanBattleArchivePersonRank"]):
    __tablename__ = 'clan_battle_archive_person_rank'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)


class ClanBattleBattleMissionDatum(DeclarativeBase, Base["ClanBattleBattleMissionDatum"]):
    __tablename__ = 'clan_battle_battle_mission_data'

    mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_value_4 = Column(Integer)
    condition_value_5 = Column(Integer)
    condition_value_6 = Column(Integer)
    condition_value_7 = Column(Integer)
    condition_value_8 = Column(Integer)
    condition_value_9 = Column(Integer)
    condition_value_10 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class ClanBattleBossDamageRank(DeclarativeBase, Base["ClanBattleBossDamageRank"]):
    __tablename__ = 'clan_battle_boss_damage_rank'

    id = Column(Integer, nullable=False)
    damage_rank_id = Column(Integer, primary_key=True, nullable=False, index=True)
    ranking_from = Column(Integer, primary_key=True, nullable=False)
    ranking_to = Column(Integer, primary_key=True, nullable=False)
    odds_group_id = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ClanBattleBossFixReward(DeclarativeBase, Base["ClanBattleBossFixReward"]):
    __tablename__ = 'clan_battle_boss_fix_reward'

    fix_reward_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ClanBattleLastAttackReward(DeclarativeBase, Base["ClanBattleLastAttackReward"]):
    __tablename__ = 'clan_battle_last_attack_reward'

    last_attack_reward_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ClanBattleOddsDatum(DeclarativeBase, Base["ClanBattleOddsDatum"]):
    __tablename__ = 'clan_battle_odds_data'

    odds_group_id = Column(Integer, primary_key=True, nullable=False, index=True)
    team_level_from = Column(Integer, primary_key=True, nullable=False)
    team_level_to = Column(Integer, primary_key=True, nullable=False)
    odds_csv_1 = Column(Text, nullable=False)
    odds_csv_2 = Column(Text, nullable=False)
    odds_csv_3 = Column(Text, nullable=False)
    odds_csv_4 = Column(Text, nullable=False)
    odds_csv_5 = Column(Text, nullable=False)
    odds_csv_6 = Column(Text, nullable=False)
    odds_csv_7 = Column(Text, nullable=False)
    odds_csv_8 = Column(Text, nullable=False)
    odds_csv_9 = Column(Text, nullable=False)
    odds_csv_10 = Column(Text, nullable=False)


class ClanBattleParamAdjust(DeclarativeBase, Base["ClanBattleParamAdjust"]):
    __tablename__ = 'clan_battle_param_adjust'

    param_adjust_id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    normal_atk_cast_time = Column(Integer, nullable=False)
    score_coefficient = Column(Integer, nullable=False)


class ClanBattlePeriod(DeclarativeBase, Base["ClanBattlePeriod"]):
    __tablename__ = 'clan_battle_period'

    clan_battle_id = Column(Integer, primary_key=True, nullable=False, index=True)
    period = Column(Integer, primary_key=True, nullable=False)
    period_detail = Column(Text, nullable=False)
    period_detail_bg = Column(Integer, nullable=False)
    period_detail_s = Column(Text, nullable=False)
    period_detail_bg_s = Column(Integer, nullable=False)
    period_detail_bg_position = Column(Integer, nullable=False)
    period_detail_boss_position_x = Column(Integer, nullable=False)
    period_detail_boss_position_y = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    interval_start = Column(Text, nullable=False)
    interval_end = Column(Text, nullable=False)
    calc_start = Column(Text, nullable=False)
    result_start = Column(Text, nullable=False)
    result_end = Column(Text, nullable=False)
    limit_time = Column(Integer, nullable=False)
    chest_id = Column(Integer, nullable=False)
    quest_detail_rehearsal_label_height = Column(Integer, nullable=False)
    min_carry_over_time = Column(Integer, nullable=False)


class ClanBattlePeriodLapReward(DeclarativeBase, Base["ClanBattlePeriodLapReward"]):
    __tablename__ = 'clan_battle_period_lap_reward'

    id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)
    lap_num_from = Column(Integer, nullable=False)
    lap_num_to = Column(Integer, nullable=False)
    ranking_bonus_group = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ClanBattlePeriodRankReward(DeclarativeBase, Base["ClanBattlePeriodRankReward"]):
    __tablename__ = 'clan_battle_period_rank_reward'

    id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    ranking_bonus_group = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ClanBattleRecommendDatum(DeclarativeBase, Base["ClanBattleRecommendDatum"]):
    __tablename__ = 'clan_battle_recommend_data'

    level_id = Column(Integer, primary_key=True)
    recommend_group = Column(Integer, nullable=False, index=True)
    level_from = Column(Integer, nullable=False)
    level_to = Column(Integer, nullable=False)
    atack_party_count = Column(Integer, nullable=False)
    magic_party_count = Column(Integer, nullable=False)


class ClanBattleSBossDatum(DeclarativeBase, Base["ClanBattleSBossDatum"]):
    __tablename__ = 'clan_battle_s_boss_data'

    boss_id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    order_num = Column(Integer, nullable=False)
    boss_thumb_id = Column(Integer, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    scale_ratio = Column(Float, nullable=False)
    tap_width_ratio = Column(Float, nullable=False)
    tap_height_ratio = Column(Float, nullable=False)
    map_position_x = Column(Integer, nullable=False)
    map_position_y = Column(Integer, nullable=False)
    cursor_position = Column(Integer, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)
    quest_detail_monster_size = Column(Float, nullable=False)
    quest_detail_monster_height = Column(Integer, nullable=False)
    battle_report_monster_size = Column(Float, nullable=False)
    battle_report_monster_height = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    wave_bgm = Column(Text, nullable=False)


class ClanBattleSBossFixReward(DeclarativeBase, Base["ClanBattleSBossFixReward"]):
    __tablename__ = 'clan_battle_s_boss_fix_reward'

    fix_reward_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class ClanBattleSMapDatum(DeclarativeBase, Base["ClanBattleSMapDatum"]):
    __tablename__ = 'clan_battle_s_map_data'

    id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False, index=True)
    map_bg = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    lap_num_from = Column(Integer, nullable=False)
    lap_num_to = Column(Integer, nullable=False)
    boss_id_1 = Column(Integer, nullable=False)
    boss_id_2 = Column(Integer, nullable=False)
    boss_id_3 = Column(Integer, nullable=False)
    boss_id_4 = Column(Integer, nullable=False)
    boss_id_5 = Column(Integer, nullable=False)
    extra_battle_flag1 = Column(Integer, nullable=False)
    extra_battle_flag2 = Column(Integer, nullable=False)
    extra_battle_flag3 = Column(Integer, nullable=False)
    extra_battle_flag4 = Column(Integer, nullable=False)
    extra_battle_flag5 = Column(Integer, nullable=False)
    aura_effect = Column(Integer, nullable=False)
    rsl_unlock_lap = Column(Integer, nullable=False)
    phase = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_group_id_4 = Column(Integer, nullable=False)
    wave_group_id_5 = Column(Integer, nullable=False)
    fix_reward_id_1 = Column(Integer, nullable=False)
    fix_reward_id_2 = Column(Integer, nullable=False)
    fix_reward_id_3 = Column(Integer, nullable=False)
    fix_reward_id_4 = Column(Integer, nullable=False)
    fix_reward_id_5 = Column(Integer, nullable=False)
    damage_rank_id_1 = Column(Integer, nullable=False)
    damage_rank_id_2 = Column(Integer, nullable=False)
    damage_rank_id_3 = Column(Integer, nullable=False)
    damage_rank_id_4 = Column(Integer, nullable=False)
    damage_rank_id_5 = Column(Integer, nullable=False)
    reward_gold_coefficient = Column(Float, nullable=False)
    limited_mana = Column(Integer, nullable=False)
    last_attack_reward_id = Column(Integer, nullable=False)
    score_coefficient_1 = Column(Float, nullable=False)
    score_coefficient_2 = Column(Float, nullable=False)
    score_coefficient_3 = Column(Float, nullable=False)
    score_coefficient_4 = Column(Float, nullable=False)
    score_coefficient_5 = Column(Float, nullable=False)
    param_adjust_id = Column(Integer, nullable=False)
    param_adjust_interval = Column(Integer, nullable=False)


class ClanBattleSParamAdjust(DeclarativeBase, Base["ClanBattleSParamAdjust"]):
    __tablename__ = 'clan_battle_s_param_adjust'

    param_adjust_id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    normal_atk_cast_time = Column(Integer, nullable=False)
    score_coefficient = Column(Integer, nullable=False)


class ClanBattleSchedule(DeclarativeBase, Base["ClanBattleSchedule"]):
    __tablename__ = 'clan_battle_schedule'

    clan_battle_id = Column(Integer, primary_key=True)
    release_month = Column(Integer, nullable=False)
    last_clan_battle_id = Column(Integer, nullable=False)
    point_per_stamina = Column(Integer, nullable=False)
    cost_group_id = Column(Integer, nullable=False)
    cost_group_id_s = Column(Integer, nullable=False)
    map_bgm = Column(Text, nullable=False)
    resource_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class ClanBattleTrainingDatum(DeclarativeBase, Base["ClanBattleTrainingDatum"]):
    __tablename__ = 'clan_battle_training_data'

    id = Column(Integer, primary_key=True)
    training_id = Column(Integer, nullable=False, index=True)
    mode = Column(Integer, nullable=False)
    phase = Column(Integer, nullable=False)
    map_data_id = Column(Integer, nullable=False)


class ClanBattleTrainingSchedule(DeclarativeBase, Base["ClanBattleTrainingSchedule"]):
    __tablename__ = 'clan_battle_training_schedule'

    training_id = Column(Integer, primary_key=True)
    clan_battle_id = Column(Integer, nullable=False, index=True)
    battle_start_time = Column(Text, nullable=False)
    battle_end_time = Column(Text, nullable=False)
    interval_start_time = Column(Text, nullable=False)
    interval_end_time = Column(Text, nullable=False)


class ClanCostGroup(DeclarativeBase, Base["ClanCostGroup"]):
    __tablename__ = 'clan_cost_group'

    id = Column(Integer, primary_key=True)
    cost_group_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)


class ClanGrade(DeclarativeBase, Base["ClanGrade"]):
    __tablename__ = 'clan_grade'

    clan_grade_id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)


class ClanInviteLevelGroup(DeclarativeBase, Base["ClanInviteLevelGroup"]):
    __tablename__ = 'clan_invite_level_group'

    level_group_id = Column(Integer, primary_key=True)
    team_level_from = Column(Integer, nullable=False)
    team_level_to = Column(Integer, nullable=False)


class ClanprofileContent(DeclarativeBase, Base["ClanprofileContent"]):
    __tablename__ = 'clanprofile_content'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    disp_order = Column(Integer, nullable=False)


class CombinedResultMotion(DeclarativeBase, Base["CombinedResultMotion"]):
    __tablename__ = 'combined_result_motion'

    result_id = Column(Integer, primary_key=True)
    unit_id_1 = Column(Integer, nullable=False)
    disp_order_1 = Column(Integer, nullable=False)
    unit_id_2 = Column(Integer, nullable=False)
    disp_order_2 = Column(Integer, nullable=False)
    unit_id_3 = Column(Integer, nullable=False)
    disp_order_3 = Column(Integer, nullable=False)
    unit_id_4 = Column(Integer, nullable=False)
    disp_order_4 = Column(Integer, nullable=False)
    unit_id_5 = Column(Integer, nullable=False)
    disp_order_5 = Column(Integer, nullable=False)


class ContentMapDatum(DeclarativeBase, Base["ContentMapDatum"]):
    __tablename__ = 'content_map_data'

    content_map_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    map_type = Column(Integer, nullable=False)
    area_id = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    quest_position_x = Column(Integer, nullable=False)
    quest_position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    system_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class ContentReleaseDatum(DeclarativeBase, Base["ContentReleaseDatum"]):
    __tablename__ = 'content_release_data'

    system_id = Column(Integer, primary_key=True)
    team_level = Column(Integer, nullable=False)
    story_id = Column(Integer, nullable=False)
    quest_id = Column(Integer, nullable=False)
    dialog = Column(Text, nullable=False)


class CooperationQuestDatum(DeclarativeBase, Base["CooperationQuestDatum"]):
    __tablename__ = 'cooperation_quest_data'

    quest_id = Column(Integer, primary_key=True)
    quest_name = Column(Text, nullable=False)
    difficulty_level = Column(Integer, nullable=False)
    limit_team_level = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    clear_reward_group_id = Column(Integer, nullable=False)
    odds_group_id = Column(Integer, nullable=False)
    lobby_background = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2 = Column(Text, nullable=False)
    wave_bgm_que_id_2 = Column(Text, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3 = Column(Text, nullable=False)
    wave_bgm_que_id_3 = Column(Text, nullable=False)
    enemy_image_1 = Column(Integer, nullable=False)
    enemy_image_2 = Column(Integer, nullable=False)
    enemy_image_3 = Column(Integer, nullable=False)
    enemy_image_4 = Column(Integer, nullable=False)
    enemy_image_5 = Column(Integer, nullable=False)
    first_reward_image_1 = Column(Integer, nullable=False)
    first_reward_image_2 = Column(Integer, nullable=False)
    first_reward_image_3 = Column(Integer, nullable=False)
    first_reward_image_4 = Column(Integer, nullable=False)
    first_reward_image_5 = Column(Integer, nullable=False)
    repeat_reward_image_1 = Column(Integer, nullable=False)
    repeat_reward_image_2 = Column(Integer, nullable=False)
    repeat_reward_image_3 = Column(Integer, nullable=False)
    cooperation_quest_detail_bg_id = Column(Integer, nullable=False)
    cooperation_quest_detail_bg_position = Column(Integer, nullable=False)
    main_enemy_image_wave_1 = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_1 = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_2 = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_3 = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_4 = Column(Integer, nullable=False)
    main_enemy_image_wave_2 = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_1 = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_2 = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_3 = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_4 = Column(Integer, nullable=False)
    main_enemy_image_wave_3 = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_1 = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_2 = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_3 = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_4 = Column(Integer, nullable=False)
    quest_comment = Column(Text, nullable=False)
    unlock_quest_id_1 = Column(Integer, nullable=False)
    unlock_quest_id_2 = Column(Integer, nullable=False)


class CustomMypage(DeclarativeBase, Base["CustomMypage"]):
    __tablename__ = 'custom_mypage'

    still_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    still_group_id = Column(Integer, nullable=False, index=True)
    still_name = Column(Text, nullable=False)
    vertical_still_flg = Column(Integer, nullable=False)
    scroll_direction = Column(Integer, nullable=False)
    mypage_type = Column(Integer, nullable=False)


class CustomMypageGroup(DeclarativeBase, Base["CustomMypageGroup"]):
    __tablename__ = 'custom_mypage_group'

    group_id = Column(Integer, primary_key=True)
    group_name = Column(Text, nullable=False)


class DailyMissionDatum(DeclarativeBase, Base["DailyMissionDatum"]):
    __tablename__ = 'daily_mission_data'

    daily_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    min_level = Column(Integer, nullable=False)
    max_level = Column(Integer, nullable=False)
    title_color_id = Column(Integer, nullable=False)
    visible_flag = Column(Integer, nullable=False)


class DearChara(DeclarativeBase, Base["DearChara"]):
    __tablename__ = 'dear_chara'

    event_id = Column(Integer, primary_key=True, nullable=False, index=True)
    chara_index = Column(Integer, primary_key=True, nullable=False)
    chara_name = Column(Text, nullable=False)
    max_dear_point = Column(Integer, nullable=False)
    reference_type = Column(Integer, nullable=False)
    reference_id = Column(Integer, nullable=False)
    episode_unlock_offset_x = Column(Integer, nullable=False)
    episode_unlock_offset_y = Column(Integer, nullable=False)
    dear_point_up_offset_x = Column(Integer, nullable=False)
    dear_point_up_offset_y = Column(Integer, nullable=False)
    condition_story_id = Column(Integer, nullable=False)


class DearReward(DeclarativeBase, Base["DearReward"]):
    __tablename__ = 'dear_reward'
    __table_args__ = (
        Index('dear_reward_0_event_id_1_chara_index', 'event_id', 'chara_index'),
    )

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    chara_index = Column(Integer, nullable=False)
    dear_point = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class DearSetting(DeclarativeBase, Base["DearSetting"]):
    __tablename__ = 'dear_setting'

    event_id = Column(Integer, primary_key=True)
    system_name = Column(Text, nullable=False)
    tutorial_quest_id = Column(Integer, nullable=False)
    tutorial_chara_index = Column(Integer, nullable=False)
    tutorial_story_id = Column(Integer, nullable=False)


class DearStoryDatum(DeclarativeBase, Base["DearStoryDatum"]):
    __tablename__ = 'dear_story_data'

    story_group_id = Column(Integer, primary_key=True)
    story_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    thumbnail_id = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class DearStoryDetail(DeclarativeBase, Base["DearStoryDetail"]):
    __tablename__ = 'dear_story_detail'
    __table_args__ = (
        Index('dear_story_detail_0_story_group_id_1_chara_index', 'story_group_id', 'chara_index'),
    )

    story_id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    visible_type = Column(Integer, nullable=False)
    story_end = Column(Integer, nullable=False)
    pre_story_id = Column(Integer, nullable=False)
    love_level = Column(Integer, nullable=False)
    requirement_id = Column(Integer, nullable=False)
    unlock_quest_id = Column(Integer, nullable=False)
    story_quest_id = Column(Integer, nullable=False)
    chara_index = Column(Integer, nullable=False)
    condition_event_quest_id = Column(Integer, nullable=False)
    condition_event_boss_id = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_value_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_value_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_value_3 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class DefineSpskill(DeclarativeBase, Base["DefineSpskill"]):
    __tablename__ = 'define_spskill'

    link_skill_slot = Column(Integer, primary_key=True)
    sp_skill_id = Column(Integer, nullable=False, index=True)
    base_skill_id = Column(Integer, nullable=False)
    skill_category = Column(Integer, nullable=False)


class DodgeTpRecovery(DeclarativeBase, Base["DodgeTpRecovery"]):
    __tablename__ = 'dodge_tp_recovery'

    system_id = Column(Integer, primary_key=True)
    recovery_ratio = Column(Float, nullable=False)


class DungeonArea(DeclarativeBase, Base["DungeonArea"]):
    __tablename__ = 'dungeon_area'

    dungeon_area_id = Column(Integer, primary_key=True)
    dungeon_type = Column(Integer, nullable=False)
    dungeon_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    open_area_id = Column(Integer, nullable=False)
    open_quest_id = Column(Integer, nullable=False)
    content_release_story = Column(Integer, nullable=False)
    initial_clear_story = Column(Integer, nullable=False)
    reward_group_id = Column(Integer, nullable=False)
    recommend_level = Column(Integer, nullable=False)
    quest_position_x = Column(Integer, nullable=False)
    quest_position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    recovery_hp_rate = Column(Integer, nullable=False)
    recovery_tp_rate = Column(Integer, nullable=False)


class DungeonAreaDatum(DeclarativeBase, Base["DungeonAreaDatum"]):
    __tablename__ = 'dungeon_area_data'

    dungeon_area_id = Column(Integer, primary_key=True)
    dungeon_type = Column(Integer, nullable=False)
    dungeon_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    open_quest_id = Column(Integer, nullable=False)
    content_release_story = Column(Integer, nullable=False)
    initial_clear_story = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    reward_group_id = Column(Integer, nullable=False)
    recommend_level = Column(Integer, nullable=False)
    quest_position_x = Column(Integer, nullable=False)
    quest_position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    coin_item_id = Column(Integer, nullable=False)
    enemy_image_1 = Column(Integer, nullable=False)
    enemy_image_2 = Column(Integer, nullable=False)
    enemy_image_3 = Column(Integer, nullable=False)
    enemy_image_4 = Column(Integer, nullable=False)
    enemy_image_5 = Column(Integer, nullable=False)
    view_reward_id_1 = Column(Integer, nullable=False)
    view_reward_id_2 = Column(Integer, nullable=False)
    view_reward_id_3 = Column(Integer, nullable=False)
    view_reward_id_4 = Column(Integer, nullable=False)
    view_reward_id_5 = Column(Integer, nullable=False)
    recovery_hp_rate = Column(Integer, nullable=False)
    recovery_tp_rate = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class DungeonQuestDatum(DeclarativeBase, Base["DungeonQuestDatum"]):
    __tablename__ = 'dungeon_quest_data'
    __table_args__ = (
        Index('dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num', unique=True),
    )

    quest_id = Column(Integer, primary_key=True)
    dungeon_area_id = Column(Integer, nullable=False, index=True)
    floor_num = Column(Integer, nullable=False)
    quest_type = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    matching_coefficient = Column(Float, nullable=False)
    parts_hp_save_flag = Column(Integer, nullable=False)
    energy_reset_flag = Column(Integer, nullable=False)
    emax = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_image_6 = Column(Integer, nullable=False)
    reward_coin = Column(Integer, nullable=False)
    chest_id = Column(Integer, nullable=False)
    odds_group_id = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_id = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_position = Column(Integer, nullable=False)
    dungeon_quest_detail_monster_size = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_1 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_2 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_height = Column(Float, nullable=False)
    multi_target_effect_time = Column(Float, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)


class DungeonSkipDatum(DeclarativeBase, Base["DungeonSkipDatum"]):
    __tablename__ = 'dungeon_skip_data'

    area_id = Column(Integer, primary_key=True)
    skip_motion_id = Column(Integer, nullable=False)
    skip_bg_id = Column(Integer, nullable=False)
    skip_position_x = Column(Integer, nullable=False)
    skip_position_y = Column(Integer, nullable=False)
    skip_scale_x = Column(Float, nullable=False)
    skip_scale_y = Column(Float, nullable=False)


class DungeonSpecialBattle(DeclarativeBase, Base["DungeonSpecialBattle"]):
    __tablename__ = 'dungeon_special_battle'
    __table_args__ = (
        Index('dungeon_special_battle_0_quest_id_1_mode', 'quest_id', 'mode', unique=True),
    )

    special_battle_id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, nullable=False, index=True)
    mode = Column(Integer, nullable=False)
    purpose_type = Column(Integer, nullable=False)
    parts_hp_save_flag = Column(Integer, nullable=False)
    trigger_hp = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    action_start_second = Column(Float, nullable=False)
    hp_gauge_color_flag = Column(Integer, nullable=False)
    start_idle_trigger = Column(Integer, nullable=False)
    appear_time = Column(Float, nullable=False)
    detail_boss_bg_size = Column(Float, nullable=False)
    detail_boss_bg_height = Column(Float, nullable=False)
    detail_boss_motion = Column(Text, nullable=False)


class DungeonSpecialEnemySetting(DeclarativeBase, Base["DungeonSpecialEnemySetting"]):
    __tablename__ = 'dungeon_special_enemy_setting'
    __table_args__ = (
        UniqueConstraint('special_battle_id', 'disp_order'),
        Index('dungeon_special_enemy_setting_0_special_battle_id_1_enemy_identify', 'special_battle_id', 'enemy_identify', unique=True)
    )

    id = Column(Integer, primary_key=True)
    special_battle_id = Column(Integer, nullable=False, index=True)
    enemy_identify = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)
    must_kill_flag = Column(Integer, nullable=False)
    detail_offset_x = Column(Float, nullable=False)
    detail_offset_y = Column(Float, nullable=False)
    detail_scale = Column(Float, nullable=False)


class EReduction(DeclarativeBase, Base["EReduction"]):
    __tablename__ = 'e_reduction'

    id = Column(Integer, primary_key=True)
    border = Column(Integer, nullable=False)
    threshold_1 = Column(Integer, nullable=False)
    value_1 = Column(Float, nullable=False)
    threshold_2 = Column(Integer, nullable=False)
    value_2 = Column(Float, nullable=False)
    threshold_3 = Column(Integer, nullable=False)
    value_3 = Column(Float, nullable=False)
    threshold_4 = Column(Integer, nullable=False)
    value_4 = Column(Float, nullable=False)
    threshold_5 = Column(Integer, nullable=False)
    value_5 = Column(Float, nullable=False)


class EmblemDatum(DeclarativeBase, Base["EmblemDatum"]):
    __tablename__ = 'emblem_data'

    emblem_id = Column(Integer, primary_key=True)
    disp_oder = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    emblem_name = Column(Text, nullable=False)
    description_mission_id = Column(Integer, nullable=False)
    event_emblem = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class EmblemMissionDatum(DeclarativeBase, Base["EmblemMissionDatum"]):
    __tablename__ = 'emblem_mission_data'

    mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer, nullable=False)
    condition_value_2 = Column(Integer, nullable=False)
    condition_value_3 = Column(Integer, nullable=False)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer, nullable=False)
    visible_flag = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class EmblemMissionRewardDatum(DeclarativeBase, Base["EmblemMissionRewardDatum"]):
    __tablename__ = 'emblem_mission_reward_data'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False, index=True)
    reward_num = Column(Integer, nullable=False)
    icon_type = Column(Integer, nullable=False)


class EnemyEnableVoice(DeclarativeBase, Base["EnemyEnableVoice"]):
    __tablename__ = 'enemy_enable_voice'

    unit_id = Column(Integer, primary_key=True)
    voice_id = Column(Integer, nullable=False)


class EnemyIgnoreSkillRf(DeclarativeBase, Base["EnemyIgnoreSkillRf"]):
    __tablename__ = 'enemy_ignore_skill_rf'

    enemy_id = Column(Integer, primary_key=True)


class EnemyMPart(DeclarativeBase, Base["EnemyMPart"]):
    __tablename__ = 'enemy_m_parts'

    enemy_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    child_enemy_parameter_1 = Column(Integer, nullable=False)
    child_enemy_parameter_2 = Column(Integer, nullable=False)
    child_enemy_parameter_3 = Column(Integer, nullable=False)
    child_enemy_parameter_4 = Column(Integer, nullable=False)
    child_enemy_parameter_5 = Column(Integer, nullable=False)


class EnemyParameter(DeclarativeBase, Base["EnemyParameter"]):
    __tablename__ = 'enemy_parameter'

    enemy_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    wave_hp_recovery = Column(Integer, nullable=False)
    wave_energy_recovery = Column(Integer, nullable=False)
    dodge = Column(Integer, nullable=False)
    physical_penetrate = Column(Integer, nullable=False)
    magic_penetrate = Column(Integer, nullable=False)
    life_steal = Column(Integer, nullable=False)
    hp_recovery_rate = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    energy_reduce_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    ex_skill_lv_1 = Column(Integer, nullable=False)
    ex_skill_lv_2 = Column(Integer, nullable=False)
    ex_skill_lv_3 = Column(Integer, nullable=False)
    ex_skill_lv_4 = Column(Integer, nullable=False)
    ex_skill_lv_5 = Column(Integer, nullable=False)
    resist_status_id = Column(Integer, nullable=False)
    resist_variation_id = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    unique_equipment_flag_1 = Column(Integer, nullable=False)
    break_durability = Column(Integer, nullable=False)
    virtual_hp = Column(Integer, nullable=False)


class EnemyRewardDatum(DeclarativeBase, Base["EnemyRewardDatum"]):
    __tablename__ = 'enemy_reward_data'

    drop_reward_id = Column(Integer, primary_key=True)
    drop_count = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    odds_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    odds_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    odds_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    odds_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    odds_5 = Column(Integer, nullable=False)


class EquipmentCraft(DeclarativeBase, Base["EquipmentCraft"]):
    __tablename__ = 'equipment_craft'

    equipment_id = Column(Integer, primary_key=True)
    crafted_cost = Column(Integer, nullable=False)
    condition_equipment_id_1 = Column(Integer, nullable=False)
    consume_num_1 = Column(Integer, nullable=False)
    condition_equipment_id_2 = Column(Integer, nullable=False)
    consume_num_2 = Column(Integer, nullable=False)
    condition_equipment_id_3 = Column(Integer, nullable=False)
    consume_num_3 = Column(Integer, nullable=False)
    condition_equipment_id_4 = Column(Integer, nullable=False)
    consume_num_4 = Column(Integer, nullable=False)
    condition_equipment_id_5 = Column(Integer, nullable=False)
    consume_num_5 = Column(Integer, nullable=False)
    condition_equipment_id_6 = Column(Integer, nullable=False)
    consume_num_6 = Column(Integer, nullable=False)
    condition_equipment_id_7 = Column(Integer, nullable=False)
    consume_num_7 = Column(Integer, nullable=False)
    condition_equipment_id_8 = Column(Integer, nullable=False)
    consume_num_8 = Column(Integer, nullable=False)
    condition_equipment_id_9 = Column(Integer, nullable=False)
    consume_num_9 = Column(Integer, nullable=False)
    condition_equipment_id_10 = Column(Integer, nullable=False)
    consume_num_10 = Column(Integer, nullable=False)


class EquipmentDatum(DeclarativeBase, Base["EquipmentDatum"]):
    __tablename__ = 'equipment_data'

    equipment_id = Column(Integer, primary_key=True)
    equipment_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    craft_flg = Column(Integer, nullable=False)
    equipment_enhance_point = Column(Integer, nullable=False)
    sale_price = Column(Integer, nullable=False)
    require_level = Column(Integer, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    enable_donation = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    display_item = Column(Integer, nullable=False)
    item_type = Column(Integer, nullable=False)


class EquipmentDonation(DeclarativeBase, Base["EquipmentDonation"]):
    __tablename__ = 'equipment_donation'

    team_level = Column(Integer, primary_key=True)
    donation_num_once = Column(Integer, nullable=False)
    donation_num_daily = Column(Integer, nullable=False)
    request_num_once = Column(Integer, nullable=False)


class EquipmentEnhanceDatum(DeclarativeBase, Base["EquipmentEnhanceDatum"]):
    __tablename__ = 'equipment_enhance_data'

    promotion_level = Column(Integer, primary_key=True, nullable=False)
    equipment_enhance_level = Column(Integer, primary_key=True, nullable=False)
    needed_point = Column(Integer, nullable=False)
    total_point = Column(Integer, nullable=False)


class EquipmentEnhanceRate(DeclarativeBase, Base["EquipmentEnhanceRate"]):
    __tablename__ = 'equipment_enhance_rate'

    equipment_id = Column(Integer, primary_key=True)
    equipment_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class EventBgDatum(DeclarativeBase, Base["EventBgDatum"]):
    __tablename__ = 'event_bg_data'

    event_id = Column(Integer, primary_key=True)
    bg_id = Column(Integer, nullable=False)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text, nullable=False)


class EventBossTreasureBox(DeclarativeBase, Base["EventBossTreasureBox"]):
    __tablename__ = 'event_boss_treasure_box'

    event_boss_treasure_box_id = Column(Integer, primary_key=True)
    treasure_type_1 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_1 = Column(Integer, nullable=False)
    each_odds_1 = Column(Integer, nullable=False)
    treasure_type_2 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_2 = Column(Integer, nullable=False)
    each_odds_2 = Column(Integer, nullable=False)
    treasure_type_3 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_3 = Column(Integer, nullable=False)
    each_odds_3 = Column(Integer, nullable=False)
    treasure_type_4 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_4 = Column(Integer, nullable=False)
    each_odds_4 = Column(Integer, nullable=False)
    treasure_type_5 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_5 = Column(Integer, nullable=False)
    each_odds_5 = Column(Integer, nullable=False)
    treasure_type_6 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_6 = Column(Integer, nullable=False)
    each_odds_6 = Column(Integer, nullable=False)
    treasure_type_7 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_7 = Column(Integer, nullable=False)
    each_odds_7 = Column(Integer, nullable=False)
    treasure_type_8 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_8 = Column(Integer, nullable=False)
    each_odds_8 = Column(Integer, nullable=False)
    treasure_type_9 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_9 = Column(Integer, nullable=False)
    each_odds_9 = Column(Integer, nullable=False)
    treasure_type_10 = Column(Integer, nullable=False)
    event_boss_treasure_content_id_10 = Column(Integer, nullable=False)
    each_odds_10 = Column(Integer, nullable=False)


class EventBossTreasureContent(DeclarativeBase, Base["EventBossTreasureContent"]):
    __tablename__ = 'event_boss_treasure_content'

    event_boss_treasure_content_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    odds_file_1 = Column(Text, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    odds_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    odds_file_2 = Column(Text, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    odds_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    odds_file_3 = Column(Text, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    odds_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    odds_file_4 = Column(Text, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    odds_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    odds_file_5 = Column(Text, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    odds_5 = Column(Integer, nullable=False)


class EventEffectSetting(DeclarativeBase, Base["EventEffectSetting"]):
    __tablename__ = 'event_effect_setting'

    event_id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Integer, primary_key=True, nullable=False)
    value = Column(Integer, nullable=False)


class EventEnemyParameter(DeclarativeBase, Base["EventEnemyParameter"]):
    __tablename__ = 'event_enemy_parameter'

    enemy_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    wave_hp_recovery = Column(Integer, nullable=False)
    wave_energy_recovery = Column(Integer, nullable=False)
    dodge = Column(Integer, nullable=False)
    physical_penetrate = Column(Integer, nullable=False)
    magic_penetrate = Column(Integer, nullable=False)
    life_steal = Column(Integer, nullable=False)
    hp_recovery_rate = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    energy_reduce_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    ex_skill_lv_1 = Column(Integer, nullable=False)
    ex_skill_lv_2 = Column(Integer, nullable=False)
    ex_skill_lv_3 = Column(Integer, nullable=False)
    ex_skill_lv_4 = Column(Integer, nullable=False)
    ex_skill_lv_5 = Column(Integer, nullable=False)
    resist_status_id = Column(Integer, nullable=False)
    resist_variation_id = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)


class EventEnemyRewardGroup(DeclarativeBase, Base["EventEnemyRewardGroup"]):
    __tablename__ = 'event_enemy_reward_group'

    id = Column(Integer, primary_key=True)
    reward_group_id = Column(Integer, nullable=False)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_num = Column(Integer, nullable=False)
    odds = Column(Integer, nullable=False)


class EventGachaDatum(DeclarativeBase, Base["EventGachaDatum"]):
    __tablename__ = 'event_gacha_data'

    gacha_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    gacha_name = Column(Text, nullable=False)
    item_type = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    repeat_step = Column(Integer, nullable=False)


class EventIntroduction(DeclarativeBase, Base["EventIntroduction"]):
    __tablename__ = 'event_introduction'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    introduction_number = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    maximum_chunk_size_1 = Column(Integer, nullable=False)
    maximum_chunk_size_loop_1 = Column(Integer, nullable=False)
    maximum_chunk_size_2 = Column(Integer, nullable=False)
    maximum_chunk_size_loop_2 = Column(Integer, nullable=False)
    maximum_chunk_size_3 = Column(Integer, nullable=False)
    maximum_chunk_size_loop_3 = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)


class EventNaviComment(DeclarativeBase, Base["EventNaviComment"]):
    __tablename__ = 'event_navi_comment'

    comment_id = Column(Integer, primary_key=True)
    where_type = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    face_type = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    description = Column(Text)
    voice_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    change_face_time = Column(Float, nullable=False)
    change_face_type = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class EventNaviCommentCondition(DeclarativeBase, Base["EventNaviCommentCondition"]):
    __tablename__ = 'event_navi_comment_condition'

    comment_id = Column(Integer, primary_key=True)
    condition_type_1 = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer, nullable=False)
    condition_type_2 = Column(Integer, nullable=False)
    condition_value_2 = Column(Integer, nullable=False)
    condition_type_3 = Column(Integer, nullable=False)
    condition_value_3 = Column(Integer, nullable=False)


class EventReminder(DeclarativeBase, Base["EventReminder"]):
    __tablename__ = 'event_reminder'

    reminder_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    title_text = Column(Text, nullable=False)
    description_text = Column(Text, nullable=False)
    notice_text = Column(Text, nullable=False)
    thumbnail_id = Column(Integer, nullable=False)
    btn_text = Column(Text, nullable=False)
    target_type = Column(Integer, nullable=False)
    target_id = Column(Integer, nullable=False)


class EventReminderCondition(DeclarativeBase, Base["EventReminderCondition"]):
    __tablename__ = 'event_reminder_condition'

    id = Column(Integer, primary_key=True)
    reminder_id = Column(Integer, nullable=False, index=True)
    condition_type = Column(Integer, nullable=False)
    condition_id = Column(Integer, nullable=False)


class EventRevivalSeriesWaveGroupDatum(DeclarativeBase, Base["EventRevivalSeriesWaveGroupDatum"]):
    __tablename__ = 'event_revival_series_wave_group_data'

    id = Column(Integer, primary_key=True)
    wave_group_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    wave = Column(Integer, nullable=False)
    match_lv_min = Column(Integer, nullable=False)
    match_lv_max = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)
    drop_gold_1 = Column(Integer, nullable=False)
    reward_group_id_1 = Column(Integer, nullable=False)
    disp_reward_type_1 = Column(Integer, nullable=False)
    disp_reward_id_1 = Column(Integer, nullable=False)
    reward_lot_count_1 = Column(Integer, nullable=False)
    reward_odds_1 = Column(Integer, nullable=False)
    drop_gold_2 = Column(Integer, nullable=False)
    reward_group_id_2 = Column(Integer, nullable=False)
    disp_reward_type_2 = Column(Integer, nullable=False)
    disp_reward_id_2 = Column(Integer, nullable=False)
    reward_lot_count_2 = Column(Integer, nullable=False)
    reward_odds_2 = Column(Integer, nullable=False)
    drop_gold_3 = Column(Integer, nullable=False)
    reward_group_id_3 = Column(Integer, nullable=False)
    disp_reward_type_3 = Column(Integer, nullable=False)
    disp_reward_id_3 = Column(Integer, nullable=False)
    reward_lot_count_3 = Column(Integer, nullable=False)
    reward_odds_3 = Column(Integer, nullable=False)
    drop_gold_4 = Column(Integer, nullable=False)
    reward_group_id_4 = Column(Integer, nullable=False)
    disp_reward_type_4 = Column(Integer, nullable=False)
    disp_reward_id_4 = Column(Integer, nullable=False)
    reward_lot_count_4 = Column(Integer, nullable=False)
    reward_odds_4 = Column(Integer, nullable=False)
    drop_gold_5 = Column(Integer, nullable=False)
    reward_group_id_5 = Column(Integer, nullable=False)
    disp_reward_type_5 = Column(Integer, nullable=False)
    disp_reward_id_5 = Column(Integer, nullable=False)
    reward_lot_count_5 = Column(Integer, nullable=False)
    reward_odds_5 = Column(Integer, nullable=False)


class EventRevivalWaveGroupDatum(DeclarativeBase, Base["EventRevivalWaveGroupDatum"]):
    __tablename__ = 'event_revival_wave_group_data'

    id = Column(Integer, primary_key=True)
    wave_group_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    wave = Column(Integer, nullable=False)
    match_lv_min = Column(Integer, nullable=False)
    match_lv_max = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)
    drop_gold_1 = Column(Integer, nullable=False)
    reward_group_id_1 = Column(Integer, nullable=False)
    disp_reward_type_1 = Column(Integer, nullable=False)
    disp_reward_id_1 = Column(Integer, nullable=False)
    reward_lot_count_1 = Column(Integer, nullable=False)
    reward_odds_1 = Column(Integer, nullable=False)
    drop_gold_2 = Column(Integer, nullable=False)
    reward_group_id_2 = Column(Integer, nullable=False)
    disp_reward_type_2 = Column(Integer, nullable=False)
    disp_reward_id_2 = Column(Integer, nullable=False)
    reward_lot_count_2 = Column(Integer, nullable=False)
    reward_odds_2 = Column(Integer, nullable=False)
    drop_gold_3 = Column(Integer, nullable=False)
    reward_group_id_3 = Column(Integer, nullable=False)
    disp_reward_type_3 = Column(Integer, nullable=False)
    disp_reward_id_3 = Column(Integer, nullable=False)
    reward_lot_count_3 = Column(Integer, nullable=False)
    reward_odds_3 = Column(Integer, nullable=False)
    drop_gold_4 = Column(Integer, nullable=False)
    reward_group_id_4 = Column(Integer, nullable=False)
    disp_reward_type_4 = Column(Integer, nullable=False)
    disp_reward_id_4 = Column(Integer, nullable=False)
    reward_lot_count_4 = Column(Integer, nullable=False)
    reward_odds_4 = Column(Integer, nullable=False)
    drop_gold_5 = Column(Integer, nullable=False)
    reward_group_id_5 = Column(Integer, nullable=False)
    disp_reward_type_5 = Column(Integer, nullable=False)
    disp_reward_id_5 = Column(Integer, nullable=False)
    reward_lot_count_5 = Column(Integer, nullable=False)
    reward_odds_5 = Column(Integer, nullable=False)


class EventSeriesWaveGroupDatum(DeclarativeBase, Base["EventSeriesWaveGroupDatum"]):
    __tablename__ = 'event_series_wave_group_data'

    id = Column(Integer, primary_key=True)
    wave_group_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    wave = Column(Integer, nullable=False)
    match_lv_min = Column(Integer, nullable=False)
    match_lv_max = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)
    drop_gold_1 = Column(Integer, nullable=False)
    reward_group_id_1 = Column(Integer, nullable=False)
    disp_reward_type_1 = Column(Integer, nullable=False)
    disp_reward_id_1 = Column(Integer, nullable=False)
    reward_lot_count_1 = Column(Integer, nullable=False)
    reward_odds_1 = Column(Integer, nullable=False)
    drop_gold_2 = Column(Integer, nullable=False)
    reward_group_id_2 = Column(Integer, nullable=False)
    disp_reward_type_2 = Column(Integer, nullable=False)
    disp_reward_id_2 = Column(Integer, nullable=False)
    reward_lot_count_2 = Column(Integer, nullable=False)
    reward_odds_2 = Column(Integer, nullable=False)
    drop_gold_3 = Column(Integer, nullable=False)
    reward_group_id_3 = Column(Integer, nullable=False)
    disp_reward_type_3 = Column(Integer, nullable=False)
    disp_reward_id_3 = Column(Integer, nullable=False)
    reward_lot_count_3 = Column(Integer, nullable=False)
    reward_odds_3 = Column(Integer, nullable=False)
    drop_gold_4 = Column(Integer, nullable=False)
    reward_group_id_4 = Column(Integer, nullable=False)
    disp_reward_type_4 = Column(Integer, nullable=False)
    disp_reward_id_4 = Column(Integer, nullable=False)
    reward_lot_count_4 = Column(Integer, nullable=False)
    reward_odds_4 = Column(Integer, nullable=False)
    drop_gold_5 = Column(Integer, nullable=False)
    reward_group_id_5 = Column(Integer, nullable=False)
    disp_reward_type_5 = Column(Integer, nullable=False)
    disp_reward_id_5 = Column(Integer, nullable=False)
    reward_lot_count_5 = Column(Integer, nullable=False)
    reward_odds_5 = Column(Integer, nullable=False)


class EventStoryDatum(DeclarativeBase, Base["EventStoryDatum"]):
    __tablename__ = 'event_story_data'

    story_group_id = Column(Integer, primary_key=True)
    story_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    thumbnail_id = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class EventStoryDetail(DeclarativeBase, Base["EventStoryDetail"]):
    __tablename__ = 'event_story_detail'

    story_id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    visible_type = Column(Integer, nullable=False)
    story_end = Column(Integer, nullable=False)
    pre_story_id = Column(Integer, nullable=False)
    love_level = Column(Integer, nullable=False)
    requirement_id = Column(Integer, nullable=False)
    unlock_quest_id = Column(Integer, nullable=False)
    story_quest_id = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_value_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_value_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_value_3 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class EventTopAdv(DeclarativeBase, Base["EventTopAdv"]):
    __tablename__ = 'event_top_adv'
    __table_args__ = (
        Index('event_top_adv_0_event_id_1_type', 'event_id', 'type'),
    )

    event_top_adv_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    value_1 = Column(Integer, nullable=False)
    value_2 = Column(Integer, nullable=False)
    value_3 = Column(Integer, nullable=False)
    story_id = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    condition_type = Column(Integer, nullable=False)
    condition_story_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class EventWaveGroupDatum(DeclarativeBase, Base["EventWaveGroupDatum"]):
    __tablename__ = 'event_wave_group_data'

    id = Column(Integer, primary_key=True)
    wave_group_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    wave = Column(Integer, nullable=False)
    match_lv_min = Column(Integer, nullable=False)
    match_lv_max = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)
    drop_gold_1 = Column(Integer, nullable=False)
    reward_group_id_1 = Column(Integer, nullable=False)
    disp_reward_type_1 = Column(Integer, nullable=False)
    disp_reward_id_1 = Column(Integer, nullable=False)
    reward_lot_count_1 = Column(Integer, nullable=False)
    reward_odds_1 = Column(Integer, nullable=False)
    drop_gold_2 = Column(Integer, nullable=False)
    reward_group_id_2 = Column(Integer, nullable=False)
    disp_reward_type_2 = Column(Integer, nullable=False)
    disp_reward_id_2 = Column(Integer, nullable=False)
    reward_lot_count_2 = Column(Integer, nullable=False)
    reward_odds_2 = Column(Integer, nullable=False)
    drop_gold_3 = Column(Integer, nullable=False)
    reward_group_id_3 = Column(Integer, nullable=False)
    disp_reward_type_3 = Column(Integer, nullable=False)
    disp_reward_id_3 = Column(Integer, nullable=False)
    reward_lot_count_3 = Column(Integer, nullable=False)
    reward_odds_3 = Column(Integer, nullable=False)
    drop_gold_4 = Column(Integer, nullable=False)
    reward_group_id_4 = Column(Integer, nullable=False)
    disp_reward_type_4 = Column(Integer, nullable=False)
    disp_reward_id_4 = Column(Integer, nullable=False)
    reward_lot_count_4 = Column(Integer, nullable=False)
    reward_odds_4 = Column(Integer, nullable=False)
    drop_gold_5 = Column(Integer, nullable=False)
    reward_group_id_5 = Column(Integer, nullable=False)
    disp_reward_type_5 = Column(Integer, nullable=False)
    disp_reward_id_5 = Column(Integer, nullable=False)
    reward_lot_count_5 = Column(Integer, nullable=False)
    reward_odds_5 = Column(Integer, nullable=False)


class ExceedLevelStage(DeclarativeBase, Base["ExceedLevelStage"]):
    __tablename__ = 'exceed_level_stage'

    exceed_stage = Column(Integer, primary_key=True)
    increase_level_limit = Column(Integer, nullable=False)
    unlock_quest_id = Column(Integer, nullable=False)
    unlock_team_level = Column(Integer, nullable=False)
    general_exceed_item_id = Column(Integer, nullable=False)


class ExceedLevelUnit(DeclarativeBase, Base["ExceedLevelUnit"]):
    __tablename__ = 'exceed_level_unit'

    id = Column(Integer, nullable=False)
    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    exceed_stage = Column(Integer, primary_key=True, nullable=False)
    exceed_item_id = Column(Integer, nullable=False)
    item_id_1 = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    consume_num_1 = Column(Integer, nullable=False)
    item_id_2 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    consume_num_2 = Column(Integer, nullable=False)
    item_id_3 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    consume_num_3 = Column(Integer, nullable=False)
    item_id_4 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    consume_num_4 = Column(Integer, nullable=False)
    item_id_5 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    consume_num_5 = Column(Integer, nullable=False)


class ExceptEr(DeclarativeBase, Base["ExceptEr"]):
    __tablename__ = 'except_er'

    category_id = Column(Integer, primary_key=True)


class ExperienceTeam(DeclarativeBase, Base["ExperienceTeam"]):
    __tablename__ = 'experience_team'

    team_level = Column(Integer, primary_key=True)
    total_exp = Column(Integer, nullable=False)
    max_stamina = Column(Integer, nullable=False)
    over_limit_stamina = Column(Integer, nullable=False)
    recover_stamina_count = Column(Integer, nullable=False)


class ExperienceUnit(DeclarativeBase, Base["ExperienceUnit"]):
    __tablename__ = 'experience_unit'

    unit_level = Column(Integer, primary_key=True)
    total_exp = Column(Integer, nullable=False)


class FixLineupGroupSet(DeclarativeBase, Base["FixLineupGroupSet"]):
    __tablename__ = 'fix_lineup_group_set'
    __table_args__ = (
        Index('fix_lineup_group_set_0_team_level_from_1_team_level_to', 'team_level_from', 'team_level_to'),
    )

    lineup_group_set_id = Column(Integer, primary_key=True, nullable=False)
    team_level_from = Column(Integer, primary_key=True, nullable=False)
    team_level_to = Column(Integer, primary_key=True, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    price_type_1 = Column(Integer, nullable=False)
    currency_id_1 = Column(Integer, nullable=False)
    price_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    price_type_2 = Column(Integer, nullable=False)
    currency_id_2 = Column(Integer, nullable=False)
    price_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    price_type_3 = Column(Integer, nullable=False)
    currency_id_3 = Column(Integer, nullable=False)
    price_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    price_type_4 = Column(Integer, nullable=False)
    currency_id_4 = Column(Integer, nullable=False)
    price_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)
    price_type_5 = Column(Integer, nullable=False)
    currency_id_5 = Column(Integer, nullable=False)
    price_5 = Column(Integer, nullable=False)
    reward_type_6 = Column(Integer, nullable=False)
    reward_id_6 = Column(Integer, nullable=False)
    reward_count_6 = Column(Integer, nullable=False)
    price_type_6 = Column(Integer, nullable=False)
    currency_id_6 = Column(Integer, nullable=False)
    price_6 = Column(Integer, nullable=False)
    reward_type_7 = Column(Integer, nullable=False)
    reward_id_7 = Column(Integer, nullable=False)
    reward_count_7 = Column(Integer, nullable=False)
    price_type_7 = Column(Integer, nullable=False)
    currency_id_7 = Column(Integer, nullable=False)
    price_7 = Column(Integer, nullable=False)
    reward_type_8 = Column(Integer, nullable=False)
    reward_id_8 = Column(Integer, nullable=False)
    reward_count_8 = Column(Integer, nullable=False)
    price_type_8 = Column(Integer, nullable=False)
    currency_id_8 = Column(Integer, nullable=False)
    price_8 = Column(Integer, nullable=False)
    reward_type_9 = Column(Integer, nullable=False)
    reward_id_9 = Column(Integer, nullable=False)
    reward_count_9 = Column(Integer, nullable=False)
    price_type_9 = Column(Integer, nullable=False)
    currency_id_9 = Column(Integer, nullable=False)
    price_9 = Column(Integer, nullable=False)
    reward_type_10 = Column(Integer, nullable=False)
    reward_id_10 = Column(Integer, nullable=False)
    reward_count_10 = Column(Integer, nullable=False)
    price_type_10 = Column(Integer, nullable=False)
    currency_id_10 = Column(Integer, nullable=False)
    price_10 = Column(Integer, nullable=False)
    reward_type_11 = Column(Integer, nullable=False)
    reward_id_11 = Column(Integer, nullable=False)
    reward_count_11 = Column(Integer, nullable=False)
    price_type_11 = Column(Integer, nullable=False)
    currency_id_11 = Column(Integer, nullable=False)
    price_11 = Column(Integer, nullable=False)
    reward_type_12 = Column(Integer, nullable=False)
    reward_id_12 = Column(Integer, nullable=False)
    reward_count_12 = Column(Integer, nullable=False)
    price_type_12 = Column(Integer, nullable=False)
    currency_id_12 = Column(Integer, nullable=False)
    price_12 = Column(Integer, nullable=False)
    reward_type_13 = Column(Integer, nullable=False)
    reward_id_13 = Column(Integer, nullable=False)
    reward_count_13 = Column(Integer, nullable=False)
    price_type_13 = Column(Integer, nullable=False)
    currency_id_13 = Column(Integer, nullable=False)
    price_13 = Column(Integer, nullable=False)
    reward_type_14 = Column(Integer, nullable=False)
    reward_id_14 = Column(Integer, nullable=False)
    reward_count_14 = Column(Integer, nullable=False)
    price_type_14 = Column(Integer, nullable=False)
    currency_id_14 = Column(Integer, nullable=False)
    price_14 = Column(Integer, nullable=False)
    reward_type_15 = Column(Integer, nullable=False)
    reward_id_15 = Column(Integer, nullable=False)
    reward_count_15 = Column(Integer, nullable=False)
    price_type_15 = Column(Integer, nullable=False)
    currency_id_15 = Column(Integer, nullable=False)
    price_15 = Column(Integer, nullable=False)
    reward_type_16 = Column(Integer, nullable=False)
    reward_id_16 = Column(Integer, nullable=False)
    reward_count_16 = Column(Integer, nullable=False)
    price_type_16 = Column(Integer, nullable=False)
    currency_id_16 = Column(Integer, nullable=False)
    price_16 = Column(Integer, nullable=False)
    reward_type_17 = Column(Integer, nullable=False)
    reward_id_17 = Column(Integer, nullable=False)
    reward_count_17 = Column(Integer, nullable=False)
    price_type_17 = Column(Integer, nullable=False)
    currency_id_17 = Column(Integer, nullable=False)
    price_17 = Column(Integer, nullable=False)
    reward_type_18 = Column(Integer, nullable=False)
    reward_id_18 = Column(Integer, nullable=False)
    reward_count_18 = Column(Integer, nullable=False)
    price_type_18 = Column(Integer, nullable=False)
    currency_id_18 = Column(Integer, nullable=False)
    price_18 = Column(Integer, nullable=False)
    reward_type_19 = Column(Integer, nullable=False)
    reward_id_19 = Column(Integer, nullable=False)
    reward_count_19 = Column(Integer, nullable=False)
    price_type_19 = Column(Integer, nullable=False)
    currency_id_19 = Column(Integer, nullable=False)
    price_19 = Column(Integer, nullable=False)
    reward_type_20 = Column(Integer, nullable=False)
    reward_id_20 = Column(Integer, nullable=False)
    reward_count_20 = Column(Integer, nullable=False)
    price_type_20 = Column(Integer, nullable=False)
    currency_id_20 = Column(Integer, nullable=False)
    price_20 = Column(Integer, nullable=False)


class FkeHappeningList(DeclarativeBase, Base["FkeHappeningList"]):
    __tablename__ = 'fke_happening_list'

    happening_id = Column(Integer, primary_key=True)
    happening_name = Column(Text, nullable=False)


class FkeReward(DeclarativeBase, Base["FkeReward"]):
    __tablename__ = 'fke_reward'

    id = Column(Integer, primary_key=True)
    fke_point = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class GachaDatum(DeclarativeBase, Base["GachaDatum"]):
    __tablename__ = 'gacha_data'

    gacha_id = Column(Integer, primary_key=True)
    gacha_name = Column(Text, nullable=False)
    pick_up_chara_text = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    description_2 = Column(Text, nullable=False)
    description_sp = Column(Text, nullable=False)
    parallel_id = Column(Integer, nullable=False)
    pickup_badge = Column(Integer, nullable=False)
    gacha_detail = Column(Integer, nullable=False)
    gacha_cost_type = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    free_gacha_type = Column(Integer, nullable=False)
    free_gacha_interval_time = Column(Integer, nullable=False)
    free_gacha_count = Column(Integer, nullable=False)
    discount_price = Column(Integer, nullable=False)
    gacha_odds = Column(Text, nullable=False)
    gacha_odds_star2 = Column(Text, nullable=False)
    gacha_type = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    ticket_id = Column(Integer, nullable=False)
    special_id = Column(Integer, nullable=False)
    exchange_id = Column(Integer, nullable=False, index=True)
    ticket_id_10 = Column(Integer, nullable=False)
    rarity_odds = Column(Text, nullable=False)
    chara_odds_star1 = Column(Text, nullable=False)
    chara_odds_star2 = Column(Text, nullable=False)
    chara_odds_star3 = Column(Text, nullable=False)
    gacha10_special_odds_star1 = Column(Text, nullable=False)
    gacha10_special_odds_star2 = Column(Text, nullable=False)
    gacha10_special_odds_star3 = Column(Text, nullable=False)
    prizegacha_id = Column(Integer, nullable=False)
    gacha_bonus_id = Column(Integer, nullable=False)
    gacha_times_limit10 = Column(Integer, nullable=False)


class GachaExchangeLineup(DeclarativeBase, Base["GachaExchangeLineup"]):
    __tablename__ = 'gacha_exchange_lineup'

    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer, nullable=False, index=True)
    unit_id = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    gacha_bonus_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class GiftMessage(DeclarativeBase, Base["GiftMessage"]):
    __tablename__ = 'gift_message'

    id = Column(Integer, primary_key=True)
    discription = Column(Text, nullable=False)
    type_1 = Column(Integer, nullable=False)
    type_2 = Column(Integer, nullable=False)
    type_3 = Column(Integer, nullable=False)
    type_4 = Column(Integer, nullable=False)


class GlobalDatum(DeclarativeBase, Base["GlobalDatum"]):
    __tablename__ = 'global_data'

    key_name = Column(Text, primary_key=True)
    value = Column(Integer, nullable=False)
    desc = Column(Text, nullable=False)


class GlossaryDetail(DeclarativeBase, Base["GlossaryDetail"]):
    __tablename__ = 'glossary_detail'

    glossary_id = Column(Integer, primary_key=True)
    glossary_category_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    unlock_story_id = Column(Integer, nullable=False)
    category_type = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)


class GoldsetDatum(DeclarativeBase, Base["GoldsetDatum"]):
    __tablename__ = 'goldset_data'

    id = Column(Integer, nullable=False)
    buy_count = Column(Integer, primary_key=True)
    use_jewel_count = Column(Integer, nullable=False)
    get_gold_count = Column(Integer, nullable=False)
    goldset_odds_1 = Column(Integer, nullable=False)
    goldset_odds_2 = Column(Integer, nullable=False)
    goldset_odds_3 = Column(Integer, nullable=False)
    additional_gold_min_rate = Column(Integer, nullable=False)
    additional_gold_max_rate = Column(Integer, nullable=False)


class GoldsetData2(DeclarativeBase, Base["GoldsetData2"]):
    __tablename__ = 'goldset_data_2'

    id = Column(Integer, nullable=False)
    buy_count = Column(Integer, primary_key=True)
    use_jewel_count = Column(Integer, nullable=False)
    get_gold_count = Column(Integer, nullable=False)
    goldset_odds_1 = Column(Integer, nullable=False)
    goldset_odds_2 = Column(Integer, nullable=False)
    goldset_odds_3 = Column(Integer, nullable=False)
    additional_gold_min_rate = Column(Integer, nullable=False)
    additional_gold_max_rate = Column(Integer, nullable=False)
    training_quest_count = Column(Integer, nullable=False)


class GoldsetDataTeamlevel(DeclarativeBase, Base["GoldsetDataTeamlevel"]):
    __tablename__ = 'goldset_data_teamlevel'

    id = Column(Integer, nullable=False)
    team_level = Column(Integer, primary_key=True)
    initial_get_gold_count = Column(Integer, nullable=False)


class GrandArenaDailyRankReward(DeclarativeBase, Base["GrandArenaDailyRankReward"]):
    __tablename__ = 'grand_arena_daily_rank_reward'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class GrandArenaDefenceReward(DeclarativeBase, Base["GrandArenaDefenceReward"]):
    __tablename__ = 'grand_arena_defence_reward'

    id = Column(Integer, primary_key=True)
    limit_count = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class GrandArenaMaxRankReward(DeclarativeBase, Base["GrandArenaMaxRankReward"]):
    __tablename__ = 'grand_arena_max_rank_reward'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class GrandArenaMaxSeasonRankReward(DeclarativeBase, Base["GrandArenaMaxSeasonRankReward"]):
    __tablename__ = 'grand_arena_max_season_rank_reward'

    id = Column(Integer, primary_key=True)
    rank_from = Column(Integer, nullable=False)
    rank_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class GrowthParameter(DeclarativeBase, Base["GrowthParameter"]):
    __tablename__ = 'growth_parameter'

    growth_id = Column(Integer, primary_key=True)
    growth_type = Column(Integer, nullable=False)
    is_restriction = Column(Integer, nullable=False)
    unit_rarity = Column(Integer, nullable=False)
    unit_level = Column(Integer, nullable=False)
    skill_level = Column(Integer, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    equipment_1 = Column(Integer, nullable=False)
    equipment_2 = Column(Integer, nullable=False)
    equipment_3 = Column(Integer, nullable=False)
    equipment_4 = Column(Integer, nullable=False)
    equipment_5 = Column(Integer, nullable=False)
    equipment_6 = Column(Integer, nullable=False)
    love_level = Column(Integer, nullable=False)


class GrowthParameterUnique(DeclarativeBase, Base["GrowthParameterUnique"]):
    __tablename__ = 'growth_parameter_unique'

    growth_id = Column(Integer, primary_key=True)
    unique_equip_strength_point_1 = Column(Integer, nullable=False)
    unique_equip_strength_point_2 = Column(Integer, nullable=False)
    unique_equip_rank_1 = Column(Integer, nullable=False)
    unique_equip_rank_2 = Column(Integer, nullable=False)


class GrowthRestrictionUnit(DeclarativeBase, Base["GrowthRestrictionUnit"]):
    __tablename__ = 'growth_restriction_unit'

    id = Column(Integer, primary_key=True)
    growth_id = Column(Integer, nullable=False, index=True)
    unit_id = Column(Integer, nullable=False)


class Guild(DeclarativeBase, Base["Guild"]):
    __tablename__ = 'guild'

    guild_id = Column(Integer, primary_key=True)
    guild_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    guild_master = Column(Integer, nullable=False)
    member1 = Column(Integer, nullable=False)
    member2 = Column(Integer, nullable=False)
    member3 = Column(Integer, nullable=False)
    member4 = Column(Integer, nullable=False)
    member5 = Column(Integer, nullable=False)
    member6 = Column(Integer, nullable=False)
    member7 = Column(Integer, nullable=False)
    member8 = Column(Integer, nullable=False)
    member9 = Column(Integer, nullable=False)
    member10 = Column(Integer, nullable=False)
    member11 = Column(Integer, nullable=False)
    member12 = Column(Integer, nullable=False)
    member13 = Column(Integer, nullable=False)
    member14 = Column(Integer, nullable=False)
    member15 = Column(Integer, nullable=False)
    member16 = Column(Integer, nullable=False)
    member17 = Column(Integer, nullable=False)
    member18 = Column(Integer, nullable=False)
    member19 = Column(Integer, nullable=False)
    member20 = Column(Integer, nullable=False)
    member21 = Column(Integer, nullable=False)
    member22 = Column(Integer, nullable=False)
    member23 = Column(Integer, nullable=False)
    member24 = Column(Integer, nullable=False)
    member25 = Column(Integer, nullable=False)
    member26 = Column(Integer, nullable=False)
    member27 = Column(Integer, nullable=False)
    member28 = Column(Integer, nullable=False)
    member29 = Column(Integer, nullable=False)
    member30 = Column(Integer, nullable=False)


class GuildAdditionalMember(DeclarativeBase, Base["GuildAdditionalMember"]):
    __tablename__ = 'guild_additional_member'

    guild_id = Column(Integer, primary_key=True)
    unlock_story_id = Column(Integer, nullable=False)
    thumb_id = Column(Integer, nullable=False)
    member1 = Column(Integer, nullable=False)
    member2 = Column(Integer, nullable=False)
    member3 = Column(Integer, nullable=False)
    member4 = Column(Integer, nullable=False)
    member5 = Column(Integer, nullable=False)
    member6 = Column(Integer, nullable=False)
    member7 = Column(Integer, nullable=False)
    member8 = Column(Integer, nullable=False)
    member9 = Column(Integer, nullable=False)
    member10 = Column(Integer, nullable=False)


class HatsuneBattleMissionDatum(DeclarativeBase, Base["HatsuneBattleMissionDatum"]):
    __tablename__ = 'hatsune_battle_mission_data'

    mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_value_4 = Column(Integer)
    condition_value_5 = Column(Integer)
    condition_value_6 = Column(Integer)
    condition_value_7 = Column(Integer)
    condition_value_8 = Column(Integer)
    condition_value_9 = Column(Integer)
    condition_value_10 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class HatsuneBgChange(DeclarativeBase, Base["HatsuneBgChange"]):
    __tablename__ = 'hatsune_bg_change'

    area_id = Column(Integer, primary_key=True)
    quest_id_1 = Column(Integer, nullable=False)
    quest_id_2 = Column(Integer, nullable=False)
    quest_id_3 = Column(Integer, nullable=False)
    quest_id_4 = Column(Integer, nullable=False)
    quest_id_5 = Column(Integer, nullable=False)


class HatsuneBgChangeDatum(DeclarativeBase, Base["HatsuneBgChangeDatum"]):
    __tablename__ = 'hatsune_bg_change_data'
    __table_args__ = (
        Index('hatsune_bg_change_data_0_target_type_1_area_id', 'target_type', 'area_id'),
    )

    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, nullable=False)
    condition_type = Column(Integer, nullable=False)
    condition_id = Column(Integer, nullable=False)
    target_type = Column(Integer, nullable=False)
    bg_after_change_id = Column(Integer, nullable=False)


class HatsuneBos(DeclarativeBase, Base["HatsuneBos"]):
    __tablename__ = 'hatsune_boss'
    __table_args__ = (
        Index('hatsune_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
    )

    boss_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    area_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    boss_position_x = Column(Integer, nullable=False)
    boss_position_y = Column(Integer, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    icon_display_scale = Column(Float, nullable=False)
    icon_collider_scale = Column(Float, nullable=False)
    use_ticket_num = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    unit_exp = Column(Integer, nullable=False)
    love = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    daily_limit = Column(Integer, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)
    event_boss_treasure_box_id_1 = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False, index=True)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    story_id_wavestart_1 = Column(Integer, nullable=False)
    story_id_waveend_1 = Column(Integer, nullable=False)
    detail_bg_id = Column(Integer, nullable=False)
    detail_bg_position = Column(Integer, nullable=False)
    detail_boss_bg_size = Column(Float, nullable=False)
    detail_boss_bg_height = Column(Float, nullable=False)
    reward_gold_coefficient = Column(Text, nullable=False)
    reward_gold_limit = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    map_position_x = Column(Float, nullable=False)
    map_position_y = Column(Float, nullable=False)
    map_size = Column(Float, nullable=False)
    deatail_aura_size = Column(Float, nullable=False)
    map_aura_size = Column(Float, nullable=False)
    oneblow_count_of_skip_condition = Column(Integer, nullable=False)
    required_skip_ticket_count = Column(Integer, nullable=False)
    retire_flag = Column(Integer, nullable=False)
    disp_on_bg = Column(Integer, nullable=False)
    qd_mode = Column(Integer, nullable=False)
    td_mode = Column(Integer, nullable=False)


class HatsuneBossCondition(DeclarativeBase, Base["HatsuneBossCondition"]):
    __tablename__ = 'hatsune_boss_condition'

    boss_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    condition_quest_id_1 = Column(Integer, nullable=False)
    condition_quest_id_2 = Column(Integer, nullable=False)
    condition_boss_id_1 = Column(Integer, nullable=False)
    condition_boss_id_2 = Column(Integer, nullable=False)
    condition_gacha_step = Column(Integer, nullable=False)
    force_unlock_time = Column(Text, nullable=False)
    release_quest_id_1 = Column(Integer, nullable=False)
    release_quest_id_2 = Column(Integer, nullable=False)
    release_boss_id_1 = Column(Integer, nullable=False)
    release_boss_id_2 = Column(Integer, nullable=False)


class HatsuneBossEnemySetting(DeclarativeBase, Base["HatsuneBossEnemySetting"]):
    __tablename__ = 'hatsune_boss_enemy_setting'
    __table_args__ = (
        Index('hatsune_boss_enemy_setting_0_boss_id_1_event_id', 'boss_id', 'event_id'),
    )

    boss_id = Column(Integer, primary_key=True, nullable=False)
    enemy_identify = Column(Integer, primary_key=True, nullable=False)
    event_id = Column(Integer, nullable=False)
    must_kill_flag = Column(Integer, nullable=False)
    event_boss_treasure_box_id = Column(Integer, nullable=False)
    reward_gold_coefficient = Column(Float, nullable=False)
    reward_gold_limit = Column(Integer, nullable=False)
    detail_offset_x = Column(Integer, nullable=False)
    detail_offset_y = Column(Integer, nullable=False)
    detail_scale = Column(Float, nullable=False)
    map_offset_x = Column(Integer, nullable=False)
    map_offset_y = Column(Integer, nullable=False)
    map_scale = Column(Float, nullable=False)
    map_depth = Column(Integer, nullable=False)


class HatsuneDailyMissionDatum(DeclarativeBase, Base["HatsuneDailyMissionDatum"]):
    __tablename__ = 'hatsune_daily_mission_data'

    daily_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class HatsuneDescription(DeclarativeBase, Base["HatsuneDescription"]):
    __tablename__ = 'hatsune_description'
    __table_args__ = (
        Index('hatsune_description_0_event_id_1_type', 'event_id', 'type'),
    )

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class HatsuneDiaryDatum(DeclarativeBase, Base["HatsuneDiaryDatum"]):
    __tablename__ = 'hatsune_diary_data'

    diary_id = Column(Integer, primary_key=True)
    contents_type = Column(Integer, nullable=False, index=True)
    diary_date = Column(Integer, nullable=False)
    sub_title = Column(Text, nullable=False)
    forced_release_time = Column(Text, nullable=False)
    condition_time = Column(Text, nullable=False)
    condition_story_id = Column(Integer, nullable=False)
    condition_boss_count = Column(Integer, nullable=False)


class HatsuneDiaryLetterScript(DeclarativeBase, Base["HatsuneDiaryLetterScript"]):
    __tablename__ = 'hatsune_diary_letter_script'

    id = Column(Integer, primary_key=True)
    diary_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    line_num = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    seek_time = Column(Float, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class HatsuneDiaryScript(DeclarativeBase, Base["HatsuneDiaryScript"]):
    __tablename__ = 'hatsune_diary_script'

    id = Column(Integer, primary_key=True)
    diary_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    diary_text = Column(Text, nullable=False)
    text_animation_speed = Column(Integer, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class HatsuneDiarySetting(DeclarativeBase, Base["HatsuneDiarySetting"]):
    __tablename__ = 'hatsune_diary_setting'

    event_id = Column(Integer, primary_key=True)
    bgm_sheet_name = Column(Text, nullable=False)
    bgm_cue_name = Column(Text, nullable=False)


class HatsuneEmblemMission(DeclarativeBase, Base["HatsuneEmblemMission"]):
    __tablename__ = 'hatsune_emblem_mission'

    mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer, nullable=False)
    condition_value_2 = Column(Integer, nullable=False)
    condition_value_3 = Column(Integer, nullable=False)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False, index=True)
    visible_flag = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class HatsuneEmblemMissionReward(DeclarativeBase, Base["HatsuneEmblemMissionReward"]):
    __tablename__ = 'hatsune_emblem_mission_reward'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False, index=True)
    reward_num = Column(Integer, nullable=False)
    icon_type = Column(Integer, nullable=False)


class HatsuneItem(DeclarativeBase, Base["HatsuneItem"]):
    __tablename__ = 'hatsune_item'

    event_id = Column(Integer, primary_key=True)
    boss_ticket_id = Column(Integer, nullable=False)
    gacha_ticket_id = Column(Integer, nullable=False)
    unit_material_id_1 = Column(Integer, nullable=False)
    unit_material_id_2 = Column(Integer, nullable=False)
    unit_material_id_3 = Column(Integer, nullable=False)
    unit_material_id_4 = Column(Integer, nullable=False)
    unit_material_id_5 = Column(Integer, nullable=False)
    unit_material_id_6 = Column(Integer, nullable=False)
    unit_material_id_7 = Column(Integer, nullable=False)
    unit_material_id_8 = Column(Integer, nullable=False)
    unit_material_id_9 = Column(Integer, nullable=False)
    unit_material_id_10 = Column(Integer, nullable=False)


class HatsuneLimitChara(DeclarativeBase, Base["HatsuneLimitChara"]):
    __tablename__ = 'hatsune_limit_chara'

    event_boss_id = Column(Integer, primary_key=True)
    limit_chara_type_1 = Column(Integer, nullable=False)


class HatsuneMap(DeclarativeBase, Base["HatsuneMap"]):
    __tablename__ = 'hatsune_map'

    course_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    map_id = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    start_area_id = Column(Integer, nullable=False)
    end_area_id = Column(Integer, nullable=False)


class HatsuneMapEvent(DeclarativeBase, Base["HatsuneMapEvent"]):
    __tablename__ = 'hatsune_map_event'

    id = Column(Integer, primary_key=True)
    target_event_id = Column(Integer, nullable=False, index=True)
    event_type = Column(Integer, nullable=False)
    condition_id = Column(Integer, nullable=False)
    param1 = Column(Integer, nullable=False)
    param2 = Column(Integer, nullable=False)


class HatsuneMissionRewardDatum(DeclarativeBase, Base["HatsuneMissionRewardDatum"]):
    __tablename__ = 'hatsune_mission_reward_data'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer)
    reward_num = Column(Integer, nullable=False)


class HatsuneMultiRouteParameter(DeclarativeBase, Base["HatsuneMultiRouteParameter"]):
    __tablename__ = 'hatsune_multi_route_parameter'

    id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, nullable=False, index=True)
    type = Column(Integer, nullable=False, index=True)
    param_1 = Column(Integer, nullable=False)
    param_2 = Column(Integer, nullable=False)
    param_3 = Column(Integer, nullable=False)
    text_1 = Column(Text, nullable=False)


class HatsunePresent(DeclarativeBase, Base["HatsunePresent"]):
    __tablename__ = 'hatsune_present'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    dialog_title = Column(Text, nullable=False)
    dialog_text = Column(Text, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    condition_mission_id = Column(Integer, nullable=False)
    adv_id = Column(Integer, nullable=False)
    item_type_1 = Column(Integer, nullable=False)
    item_id_1 = Column(Integer, nullable=False)
    item_num_1 = Column(Integer, nullable=False)
    item_type_2 = Column(Integer, nullable=False)
    item_id_2 = Column(Integer, nullable=False)
    item_num_2 = Column(Integer, nullable=False)
    item_type_3 = Column(Integer, nullable=False)
    item_id_3 = Column(Integer, nullable=False)
    item_num_3 = Column(Integer, nullable=False)
    item_type_4 = Column(Integer, nullable=False)
    item_id_4 = Column(Integer, nullable=False)
    item_num_4 = Column(Integer, nullable=False)
    item_type_5 = Column(Integer, nullable=False)
    item_id_5 = Column(Integer, nullable=False)
    item_num_5 = Column(Integer, nullable=False)


class HatsuneQuest(DeclarativeBase, Base["HatsuneQuest"]):
    __tablename__ = 'hatsune_quest'

    quest_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    area_id = Column(Integer, nullable=False)
    quest_seq = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    icon_offset_x = Column(Float, nullable=False)
    icon_offset_y = Column(Float, nullable=False)
    icon_scale = Column(Float, nullable=False)
    stamina = Column(Integer, nullable=False)
    stamina_start = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    unit_exp = Column(Integer, nullable=False)
    love = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    daily_limit = Column(Integer, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)
    rank_reward_group = Column(Integer, nullable=False)
    drop_reward_type = Column(Integer, nullable=False)
    drop_reward_id = Column(Integer, nullable=False)
    drop_reward_num = Column(Integer, nullable=False)
    drop_reward_odds = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    story_id_wavestart_1 = Column(Integer, nullable=False)
    story_id_waveend_1 = Column(Integer, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2 = Column(Text, nullable=False)
    wave_bgm_que_id_2 = Column(Text, nullable=False)
    story_id_wavestart_2 = Column(Integer, nullable=False)
    story_id_waveend_2 = Column(Integer, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3 = Column(Text, nullable=False)
    wave_bgm_que_id_3 = Column(Text, nullable=False)
    story_id_wavestart_3 = Column(Integer, nullable=False)
    story_id_waveend_3 = Column(Integer, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class HatsuneQuestArea(DeclarativeBase, Base["HatsuneQuestArea"]):
    __tablename__ = 'hatsune_quest_area'

    area_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    area_name = Column(Text, nullable=False)
    map_type = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    area_disp = Column(Integer, nullable=False)
    map_id = Column(Integer, nullable=False)
    scroll_width = Column(Integer, nullable=False)
    scroll_height = Column(Integer, nullable=False)
    open_tutorial_id = Column(Integer, nullable=False)
    tutorial_param_1 = Column(Text, nullable=False)
    tutorial_param_2 = Column(Text, nullable=False)
    additional_effect = Column(Integer, nullable=False)


class HatsuneQuestCondition(DeclarativeBase, Base["HatsuneQuestCondition"]):
    __tablename__ = 'hatsune_quest_condition'

    quest_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    condition_quest_id_1 = Column(Integer, nullable=False)
    condition_quest_id_2 = Column(Integer, nullable=False)
    condition_boss_id_1 = Column(Integer, nullable=False)
    condition_boss_id_2 = Column(Integer, nullable=False)
    release_quest_id_1 = Column(Integer, nullable=False)
    release_quest_id_2 = Column(Integer, nullable=False)
    release_boss_id_1 = Column(Integer, nullable=False)
    release_boss_id_2 = Column(Integer, nullable=False)
    condition_main_quest_id = Column(Integer, nullable=False)


class HatsuneQuiz(DeclarativeBase, Base["HatsuneQuiz"]):
    __tablename__ = 'hatsune_quiz'
    __table_args__ = (
        Index('hatsune_quiz_0_event_id_1_release_quest_id', 'event_id', 'release_quest_id'),
    )

    event_id = Column(Integer, nullable=False, index=True)
    quiz_id = Column(Integer, primary_key=True)
    question_title = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    choice_1 = Column(Text, nullable=False)
    choice_2 = Column(Text, nullable=False)
    choice_3 = Column(Text, nullable=False)
    choice_4 = Column(Text, nullable=False)
    choice_5 = Column(Text, nullable=False)
    choice_6 = Column(Text, nullable=False)
    answer = Column(Integer, nullable=False)
    hint = Column(Text, nullable=False)
    resource_id = Column(Integer, nullable=False)
    release_quest_id = Column(Integer, nullable=False)
    quiz_position_x = Column(Integer, nullable=False)
    quiz_position_y = Column(Integer, nullable=False)
    quiz_icon_id = Column(Integer, nullable=False)
    quiz_point_name = Column(Text, nullable=False)
    adv_id_quiz_start = Column(Integer, nullable=False)
    adv_id_quiz_end = Column(Integer, nullable=False)


class HatsuneQuizCondition(DeclarativeBase, Base["HatsuneQuizCondition"]):
    __tablename__ = 'hatsune_quiz_condition'
    __table_args__ = (
        Index('hatsune_quiz_condition_0_event_id_1_quiz_id', 'event_id', 'quiz_id'),
    )

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    quiz_id = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_quiz_id = Column(Integer, nullable=False)
    condition_unit_id = Column(Integer, nullable=False)
    condition_mission_id = Column(Integer, nullable=False)
    condition_time_from = Column(Integer, nullable=False)


class HatsuneQuizReward(DeclarativeBase, Base["HatsuneQuizReward"]):
    __tablename__ = 'hatsune_quiz_reward'

    quiz_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class HatsuneRelayDatum(DeclarativeBase, Base["HatsuneRelayDatum"]):
    __tablename__ = 'hatsune_relay_data'

    relay_story_id = Column(Integer, primary_key=True)
    is_enable_read = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    story_seq = Column(Integer, nullable=False)
    sub_title = Column(Text, nullable=False)


class HatsuneSchedule(DeclarativeBase, Base["HatsuneSchedule"]):
    __tablename__ = 'hatsune_schedule'

    event_id = Column(Integer, primary_key=True)
    teaser_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    close_time = Column(Text, nullable=False)
    background = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    banner_unit_id = Column(Integer, nullable=False)
    count_start_time = Column(Text, nullable=False)
    backgroud_size_x = Column(Integer, nullable=False)
    backgroud_size_y = Column(Integer, nullable=False)
    backgroud_pos_x = Column(Integer, nullable=False)
    backgroud_pos_y = Column(Integer, nullable=False)
    original_event_id = Column(Integer, nullable=False, index=True)
    series_event_id = Column(Integer, nullable=False, index=True)
    teaser_dialog_type = Column(Integer, nullable=False)


class HatsuneSeriesGachaReference(DeclarativeBase, Base["HatsuneSeriesGachaReference"]):
    __tablename__ = 'hatsune_series_gacha_reference'

    event_id = Column(Integer, primary_key=True)
    reference_key_event_id_flag = Column(Integer, nullable=False)


class HatsuneSpecialBattle(DeclarativeBase, Base["HatsuneSpecialBattle"]):
    __tablename__ = 'hatsune_special_battle'

    event_id = Column(Integer, primary_key=True, nullable=False, index=True)
    mode = Column(Integer, primary_key=True, nullable=False)
    recommended_level = Column(Integer, nullable=False)
    purpose_type = Column(Integer, nullable=False)
    purpose_count = Column(Integer, nullable=False)
    trigger_hp = Column(Integer, nullable=False)
    story_id_mode_start = Column(Integer, nullable=False)
    story_id_mode_end = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False, index=True)
    unnecessary_defeat_chara = Column(Integer, nullable=False)
    story_start_second = Column(Float, nullable=False)
    action_start_second = Column(Float, nullable=False)
    hp_gauge_color_flag = Column(Integer, nullable=False)
    start_idle_trigger = Column(Integer, nullable=False)
    appear_time = Column(Float, nullable=False)
    detail_boss_bg_size = Column(Float, nullable=False)
    detail_boss_bg_height = Column(Float, nullable=False)
    detail_boss_motion = Column(Text, nullable=False)
    is_hide_boss = Column(Integer, nullable=False)


class HatsuneSpecialBossTicketCount(DeclarativeBase, Base["HatsuneSpecialBossTicketCount"]):
    __tablename__ = 'hatsune_special_boss_ticket_count'

    id = Column(Integer, primary_key=True)
    challenge_count_from = Column(Integer, nullable=False)
    challenge_count_to = Column(Integer, nullable=False)
    use_ticket_num = Column(Integer, nullable=False)


class HatsuneSpecialEnemy(DeclarativeBase, Base["HatsuneSpecialEnemy"]):
    __tablename__ = 'hatsune_special_enemy'

    enemy_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    mode = Column(Integer, nullable=False)
    enemy_point = Column(Integer, nullable=False)
    initial_position = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)


class HatsuneSpecialMissionDatum(DeclarativeBase, Base["HatsuneSpecialMissionDatum"]):
    __tablename__ = 'hatsune_special_mission_data'

    special_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    purpose_type = Column(Integer, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class HatsuneStationaryMissionDatum(DeclarativeBase, Base["HatsuneStationaryMissionDatum"]):
    __tablename__ = 'hatsune_stationary_mission_data'

    stationary_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False, index=True)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class HatsuneUnlockStoryCondition(DeclarativeBase, Base["HatsuneUnlockStoryCondition"]):
    __tablename__ = 'hatsune_unlock_story_condition'

    story_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    condition_entry = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    condition_mission_id = Column(Integer, nullable=False)
    condition_time = Column(Text, nullable=False)
    condition_story_id = Column(Integer, nullable=False)


class HatsuneUnlockUnitCondition(DeclarativeBase, Base["HatsuneUnlockUnitCondition"]):
    __tablename__ = 'hatsune_unlock_unit_condition'
    __table_args__ = (
        Index('hatsune_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id'),
    )

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)
    condition_mission_id = Column(Integer, nullable=False, index=True)
    top_description = Column(Text, nullable=False)
    description_1 = Column(Text, nullable=False)
    description_2 = Column(Text, nullable=False)


class ItemDatum(DeclarativeBase, Base["ItemDatum"]):
    __tablename__ = 'item_data'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    item_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    limit_num = Column(Integer, nullable=False)
    gojuon_order = Column(Integer, nullable=False)
    sell_check_disp = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class ItemETicketDatum(DeclarativeBase, Base["ItemETicketDatum"]):
    __tablename__ = 'item_e_ticket_data'

    ticket_id = Column(Integer, primary_key=True, nullable=False, index=True)
    exchange_number = Column(Integer, primary_key=True, nullable=False, index=True)
    unit_id = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class KaiserAddTimesDatum(DeclarativeBase, Base["KaiserAddTimesDatum"]):
    __tablename__ = 'kaiser_add_times_data'

    id = Column(Integer, primary_key=True)
    add_times = Column(Integer, nullable=False)
    add_times_time = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)


class KaiserExterminationReward(DeclarativeBase, Base["KaiserExterminationReward"]):
    __tablename__ = 'kaiser_extermination_reward'

    extermination_reward_group = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class KaiserQuestDatum(DeclarativeBase, Base["KaiserQuestDatum"]):
    __tablename__ = 'kaiser_quest_data'

    kaiser_boss_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    map_type = Column(Integer, nullable=False)
    battle_start_story_id = Column(Integer, nullable=False)
    battle_finish_story_id = Column(Integer, nullable=False)
    disappearance_story_id = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    restriction_group_id = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)
    fix_reward_group_id = Column(Integer, nullable=False)
    odds_group_id = Column(Text, nullable=False)
    chest_id = Column(Integer, nullable=False)
    extermination_reward_group = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    bg_position = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    enemy_position_x = Column(Integer, nullable=False)
    enemy_local_position_y = Column(Integer, nullable=False)
    enemy_size_1 = Column(Float, nullable=False)
    result_boss_position_y = Column(Float, nullable=False)
    wave_bgm = Column(Text, nullable=False)
    reward_gold_coefficient = Column(Float, nullable=False)
    limited_mana = Column(Integer, nullable=False)
    clear_story_id_1 = Column(Integer, nullable=False)
    clear_story_id_2 = Column(Integer, nullable=False)


class KaiserRestrictionGroup(DeclarativeBase, Base["KaiserRestrictionGroup"]):
    __tablename__ = 'kaiser_restriction_group'

    restriction_group_id = Column(Integer, primary_key=True, nullable=False, index=True)
    unit_id = Column(Integer, primary_key=True, nullable=False)


class KaiserSchedule(DeclarativeBase, Base["KaiserSchedule"]):
    __tablename__ = 'kaiser_schedule'

    id = Column(Integer, primary_key=True)
    teaser_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    count_start_time = Column(Text, nullable=False)
    close_time = Column(Text, nullable=False)
    story_id = Column(Integer, nullable=False)
    close_story_condition_id = Column(Integer, nullable=False)
    close_story_id = Column(Integer, nullable=False)
    top_bgm = Column(Text, nullable=False)
    top_bg = Column(Text, nullable=False)
    after_bgm = Column(Text, nullable=False)
    after_bg = Column(Text, nullable=False)


class KaiserSpecialBattle(DeclarativeBase, Base["KaiserSpecialBattle"]):
    __tablename__ = 'kaiser_special_battle'

    mode = Column(Integer, primary_key=True)
    recommended_level = Column(Integer, nullable=False)
    purpose_type = Column(Integer, nullable=False)
    purpose_count = Column(Integer, nullable=False)
    trigger_hp = Column(Integer, nullable=False)
    story_id_mode_start = Column(Integer, nullable=False)
    story_id_mode_end = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    unnecessary_defeat_chara = Column(Integer, nullable=False)
    story_start_second = Column(Float, nullable=False)
    action_start_second = Column(Float, nullable=False)
    hp_gauge_color_flag = Column(Integer, nullable=False)
    start_idle_trigger = Column(Integer, nullable=False)
    appear_time = Column(Float, nullable=False)


class KmkNaviComment(DeclarativeBase, Base["KmkNaviComment"]):
    __tablename__ = 'kmk_navi_comment'

    comment_id = Column(Integer, primary_key=True)
    where_type = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    face_type = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    description = Column(Text)
    voice_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    change_face_time = Column(Float, nullable=False)
    change_face_type = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class KmkReward(DeclarativeBase, Base["KmkReward"]):
    __tablename__ = 'kmk_reward'

    id = Column(Integer, primary_key=True)
    kmk_score = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class LegionAddTimesDatum(DeclarativeBase, Base["LegionAddTimesDatum"]):
    __tablename__ = 'legion_add_times_data'

    id = Column(Integer, primary_key=True)
    add_times = Column(Integer, nullable=False)
    add_times_time = Column(Text, nullable=False)


class LegionBattleBonu(DeclarativeBase, Base["LegionBattleBonu"]):
    __tablename__ = 'legion_battle_bonus'
    __table_args__ = (
        Index('legion_battle_bonus_0_type_1_legion_boss_id', 'type', 'legion_boss_id'),
    )

    legion_battle_bonus_id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False, index=True)
    legion_boss_id = Column(Integer, nullable=False)
    condition_hp = Column(Text, nullable=False)
    legion_battle_effect_id = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class LegionBattleBonusEffect(DeclarativeBase, Base["LegionBattleBonusEffect"]):
    __tablename__ = 'legion_battle_bonus_effect'

    legion_battle_effect_id = Column(Integer, primary_key=True)
    enemy_id = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    text_id = Column(Integer, nullable=False)
    skill_id = Column(Integer, nullable=False)
    target_type = Column(Integer, nullable=False)


class LegionBossEnemySetting(DeclarativeBase, Base["LegionBossEnemySetting"]):
    __tablename__ = 'legion_boss_enemy_setting'

    boss_id = Column(Integer, primary_key=True)
    detail_offset_x = Column(Integer, nullable=False)
    detail_offset_y = Column(Integer, nullable=False)
    detail_offset_scale = Column(Float, nullable=False)


class LegionEffect(DeclarativeBase, Base["LegionEffect"]):
    __tablename__ = 'legion_effect'

    effect_id = Column(Integer, primary_key=True)
    bonus_1 = Column(Integer, nullable=False)
    bonus_2 = Column(Integer, nullable=False)
    bonus_3 = Column(Integer, nullable=False)
    bonus_4 = Column(Integer, nullable=False)
    bonus_5 = Column(Integer, nullable=False)


class LegionEffectiveUnit(DeclarativeBase, Base["LegionEffectiveUnit"]):
    __tablename__ = 'legion_effective_unit'

    legion_boss_id = Column(Integer, primary_key=True, nullable=False, index=True)
    unit_id = Column(Integer, primary_key=True, nullable=False)
    effect_id = Column(Integer, nullable=False)
    support_effect_id = Column(Integer, nullable=False)


class LegionExterminationReward(DeclarativeBase, Base["LegionExterminationReward"]):
    __tablename__ = 'legion_extermination_reward'

    extermination_reward_group_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class LegionMissionCategoryDatum(DeclarativeBase, Base["LegionMissionCategoryDatum"]):
    __tablename__ = 'legion_mission_category_data'

    category_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class LegionMissionDatum(DeclarativeBase, Base["LegionMissionDatum"]):
    __tablename__ = 'legion_mission_data'

    legion_mission_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, nullable=False, index=True)
    disp_group = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    legion_boss_id = Column(Integer, nullable=False)
    condition_value = Column(Integer, nullable=False)
    condition_num = Column(Text, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class LegionMissionRewardDatum(DeclarativeBase, Base["LegionMissionRewardDatum"]):
    __tablename__ = 'legion_mission_reward_data'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_num = Column(Integer, nullable=False)


class LegionQuestDatum(DeclarativeBase, Base["LegionQuestDatum"]):
    __tablename__ = 'legion_quest_data'

    legion_boss_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    map_type = Column(Integer, nullable=False, index=True)
    battle_start_story_id = Column(Integer, nullable=False)
    battle_finish_story_id = Column(Integer, nullable=False)
    disappearance_story_id = Column(Integer, nullable=False)
    all_disappearance_story_id = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    max_raid_hp = Column(Text, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)
    challenge_reward_group_id = Column(Integer, nullable=False)
    expel_reward_group_id = Column(Integer, nullable=False)
    extermination_reward_group_id = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    bg_position = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    enemy_position_x = Column(Integer, nullable=False)
    enemy_local_position_y = Column(Integer, nullable=False)
    enemy_size_1 = Column(Float, nullable=False)
    result_boss_position_y = Column(Float, nullable=False)
    wave_bgm = Column(Text, nullable=False)
    clear_story_id_1 = Column(Integer, nullable=False)
    clear_story_id_2 = Column(Integer, nullable=False)
    bonus_max = Column(Integer, nullable=False)


class LegionSchedule(DeclarativeBase, Base["LegionSchedule"]):
    __tablename__ = 'legion_schedule'

    id = Column(Integer, primary_key=True)
    teaser_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    count_start_time = Column(Text, nullable=False)
    close_time = Column(Text, nullable=False)
    story_id = Column(Integer, nullable=False)
    close_story_condition_id = Column(Integer, nullable=False)
    close_story_id = Column(Integer, nullable=False)
    top_bgm = Column(Text, nullable=False)
    top_bg = Column(Text, nullable=False)


class LegionSpecialBattle(DeclarativeBase, Base["LegionSpecialBattle"]):
    __tablename__ = 'legion_special_battle'

    mode = Column(Integer, primary_key=True)
    purpose_type = Column(Integer, nullable=False)
    purpose_count = Column(Integer, nullable=False)
    trigger_hp = Column(Integer, nullable=False)
    story_id_mode_start = Column(Integer, nullable=False)
    story_id_mode_end = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    unnecessary_defeat_chara = Column(Integer, nullable=False)
    story_start_second = Column(Float, nullable=False)
    action_start_second = Column(Float, nullable=False)
    hp_gauge_color_flag = Column(Integer, nullable=False)


class LoginBonusAdv(DeclarativeBase, Base["LoginBonusAdv"]):
    __tablename__ = 'login_bonus_adv'

    id = Column(Integer, primary_key=True)
    login_bonus_id = Column(Integer, nullable=False, index=True)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    count_key = Column(Integer, nullable=False)
    adv_id = Column(Integer, nullable=False)
    read_process_flag = Column(Integer, nullable=False)


class LoginBonusDatum(DeclarativeBase, Base["LoginBonusDatum"]):
    __tablename__ = 'login_bonus_data'

    login_bonus_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    login_bonus_type = Column(Integer, nullable=False)
    count_num = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    bg_id = Column(Integer, nullable=False)
    stamp_id = Column(Integer, nullable=False)
    odds_group_id = Column(Integer, nullable=False)
    adv_play_type = Column(Integer, nullable=False)
    count_type = Column(Integer, nullable=False)


class LoginBonusDetail(DeclarativeBase, Base["LoginBonusDetail"]):
    __tablename__ = 'login_bonus_detail'
    __table_args__ = (
        Index('login_bonus_detail_0_login_bonus_id_1_count', 'login_bonus_id', 'count'),
    )

    id = Column(Integer, primary_key=True)
    login_bonus_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_num = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    voice_id = Column(Integer, nullable=False)
    bg_id = Column(Integer, nullable=False)


class LoginBonusMessageDatum(DeclarativeBase, Base["LoginBonusMessageDatum"]):
    __tablename__ = 'login_bonus_message_data'

    id = Column(Integer, primary_key=True)
    login_bonus_id = Column(Integer, nullable=False, index=True)
    type = Column(Integer, nullable=False)
    day_count = Column(Integer, nullable=False)
    luck_pattern = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    voice_id = Column(Integer, nullable=False)
    additional_type = Column(Integer, nullable=False)
    additional_param = Column(Text, nullable=False)


class LoveChara(DeclarativeBase, Base["LoveChara"]):
    __tablename__ = 'love_chara'

    love_level = Column(Integer, primary_key=True)
    total_love = Column(Integer, nullable=False)
    unlocked_class = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)


class LoveRankup(DeclarativeBase, Base["LoveRankup"]):
    __tablename__ = 'love_rankup'

    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    love_rank = Column(Integer, primary_key=True, nullable=False)
    effect_unit_id = Column(Integer, nullable=False)


class LtoLetterScript(DeclarativeBase, Base["LtoLetterScript"]):
    __tablename__ = 'lto_letter_script'

    id = Column(Integer, primary_key=True)
    letter_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    line_num = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    seek_time = Column(Float, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class LtoStoryDatum(DeclarativeBase, Base["LtoStoryDatum"]):
    __tablename__ = 'lto_story_data'

    sub_story_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    condition_story_id = Column(Integer, nullable=False)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_count = Column(Integer, nullable=False)


class Metamorphose(DeclarativeBase, Base["Metamorphose"]):
    __tablename__ = 'metamorphose'

    type_id = Column(Integer, primary_key=True, nullable=False, index=True)
    condition_value = Column(Integer, primary_key=True, nullable=False)
    prefab_id = Column(Integer, nullable=False)


class MhpDramaScript(DeclarativeBase, Base["MhpDramaScript"]):
    __tablename__ = 'mhp_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class MhpStoryDatum(DeclarativeBase, Base["MhpStoryDatum"]):
    __tablename__ = 'mhp_story_data'

    sub_story_id = Column(Integer, primary_key=True)
    original_event_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    unit_id = Column(Integer, nullable=False, index=True)
    read_condition_time = Column(Text, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    read_condition = Column(Integer, nullable=False)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_count = Column(Integer, nullable=False)


class Minigame(DeclarativeBase, Base["Minigame"]):
    __tablename__ = 'minigame'

    id = Column(Integer, nullable=False)
    minigame_scheme_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    release_conditions_1 = Column(Integer, nullable=False)
    conditions_id_1 = Column(Integer, nullable=False)
    first_time_story_id = Column(Integer, nullable=False)
    display_condition_type = Column(Integer, nullable=False)
    display_condition_id = Column(Integer, nullable=False)
    result_chat_condition_id = Column(Integer, nullable=False)
    score_unit = Column(Text, nullable=False)
    is_enabled_zero_score = Column(Integer, nullable=False)


class MissionRewardDatum(DeclarativeBase, Base["MissionRewardDatum"]):
    __tablename__ = 'mission_reward_data'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer)
    reward_num = Column(Integer, nullable=False)
    lv_from = Column(Integer, nullable=False)
    lv_to = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class Movie(DeclarativeBase, Base["Movie"]):
    __tablename__ = 'movie'

    movie_id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False)
    story_id = Column(Integer, nullable=False, index=True)
    bgm_id = Column(Text, nullable=False)
    se_id = Column(Text, nullable=False)
    my_page_flag = Column(Integer, nullable=False)
    fade_loop_flag = Column(Integer, nullable=False)
    bgm_volume_rate = Column(Float, nullable=False)


class MusicContent(DeclarativeBase, Base["MusicContent"]):
    __tablename__ = 'music_content'

    music_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    total_playing_time = Column(Text, nullable=False)
    listen_start_time = Column(Text, nullable=False)
    detail = Column(Text, nullable=False)
    sheet_id = Column(Text, nullable=False)
    cue_id = Column(Text, nullable=False)


class MusicList(DeclarativeBase, Base["MusicList"]):
    __tablename__ = 'music_list'

    music_id = Column(Integer, primary_key=True)
    list_name = Column(Text, nullable=False)
    font_size = Column(Float, nullable=False)
    pre_shop_start = Column(Text, nullable=False)
    shop_start = Column(Text, nullable=False)
    shop_end = Column(Text, nullable=False)
    story_id = Column(Integer, nullable=False)
    cost_item_num = Column(Integer, nullable=False)
    sort = Column(Integer, nullable=False)
    kana = Column(Text, nullable=False)
    ios_url = Column(Text, nullable=False)
    android_url = Column(Text, nullable=False)
    dmm_url = Column(Text, nullable=False)


class MypageFrame(DeclarativeBase, Base["MypageFrame"]):
    __tablename__ = 'mypage_frame'

    frame_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, index=True)
    frame_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)


class MyprofileContent(DeclarativeBase, Base["MyprofileContent"]):
    __tablename__ = 'myprofile_content'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    disp_order = Column(Integer, nullable=False)


class NaviComment(DeclarativeBase, Base["NaviComment"]):
    __tablename__ = 'navi_comment'

    comment_id = Column(Integer, primary_key=True)
    where_type = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    face_type = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    description = Column(Text)
    voice_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    change_face_time = Column(Float, nullable=False)
    change_face_type = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class NopDramaDatum(DeclarativeBase, Base["NopDramaDatum"]):
    __tablename__ = 'nop_drama_data'

    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer, nullable=False, index=True)
    position_id_1 = Column(Integer, nullable=False)
    position_id_2 = Column(Integer, nullable=False)
    position_id_3 = Column(Integer, nullable=False)
    col_size_x = Column(Integer, nullable=False)
    col_size_y = Column(Integer, nullable=False)
    col_pos_y = Column(Float, nullable=False)
    talk_pos_x = Column(Float, nullable=False)
    talk_pos_y = Column(Float, nullable=False)
    idle_drama_id = Column(Integer, nullable=False)
    talk_drama_id = Column(Integer, nullable=False)
    event_drama_id = Column(Integer, nullable=False)
    create_back_drama_id = Column(Integer, nullable=False)
    create_front_drama_id = Column(Integer, nullable=False)
    sub_story_id = Column(Integer, nullable=False)


class NopDramaScript(DeclarativeBase, Base["NopDramaScript"]):
    __tablename__ = 'nop_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class NotifDatum(DeclarativeBase, Base["NotifDatum"]):
    __tablename__ = 'notif_data'

    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    notif_type = Column(Integer, primary_key=True, nullable=False)
    comment = Column(Text, nullable=False)


class NyxDramaDatum(DeclarativeBase, Base["NyxDramaDatum"]):
    __tablename__ = 'nyx_drama_data'

    drama_id = Column(Integer, primary_key=True)
    story_phase = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    condition_unlocked_story_id = Column(Integer, nullable=False)
    condition_locked_story_id = Column(Integer, nullable=False)


class NyxDramaScript(DeclarativeBase, Base["NyxDramaScript"]):
    __tablename__ = 'nyx_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class NyxPhaseDatum(DeclarativeBase, Base["NyxPhaseDatum"]):
    __tablename__ = 'nyx_phase_data'

    story_phase = Column(Integer, primary_key=True)
    phase_title = Column(Text, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_quest_boss = Column(Integer, nullable=False)


class NyxStoryDatum(DeclarativeBase, Base["NyxStoryDatum"]):
    __tablename__ = 'nyx_story_data'

    story_id = Column(Integer, primary_key=True)
    story_seq = Column(Integer, nullable=False, index=True)
    story_phase = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    read_condition_time = Column(Text, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_count = Column(Integer, nullable=False)
    adv_flg = Column(Integer, nullable=False)
    adv_id = Column(Integer, nullable=False)


class NyxStoryScript(DeclarativeBase, Base["NyxStoryScript"]):
    __tablename__ = 'nyx_story_script'

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    line_num = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    seek_time = Column(Float, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class OddsNameDatum(DeclarativeBase, Base["OddsNameDatum"]):
    __tablename__ = 'odds_name_data'

    id = Column(Integer, primary_key=True)
    odds_file = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    icon_type = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class OmpDrama(DeclarativeBase, Base["OmpDrama"]):
    __tablename__ = 'omp_drama'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class OmpStoryDatum(DeclarativeBase, Base["OmpStoryDatum"]):
    __tablename__ = 'omp_story_data'

    omp_story_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    story_seq = Column(Integer, nullable=False, index=True)
    is_readable_on_result = Column(Integer, nullable=False)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_count = Column(Integer, nullable=False)
    sub_title = Column(Text, nullable=False)


class PctComboCoefficient(DeclarativeBase, Base["PctComboCoefficient"]):
    __tablename__ = 'pct_combo_coefficient'

    id = Column(Integer, primary_key=True)
    combo_min = Column(Integer, nullable=False)
    combo_max = Column(Integer, nullable=False)
    combo_coefficient = Column(Integer, nullable=False)


class PctEvaluation(DeclarativeBase, Base["PctEvaluation"]):
    __tablename__ = 'pct_evaluation'

    evaluation_id = Column(Integer, primary_key=True)
    evaluation_point = Column(Integer, nullable=False)
    fever_point = Column(Integer, nullable=False)
    meet_width = Column(Integer, nullable=False)


class PctGamingMotion(DeclarativeBase, Base["PctGamingMotion"]):
    __tablename__ = 'pct_gaming_motion'

    motion_id = Column(Integer, primary_key=True)
    perfect_count = Column(Integer, nullable=False)
    good_count = Column(Integer, nullable=False)
    nice_count = Column(Integer, nullable=False)
    point = Column(Integer, nullable=False)


class PctItempoint(DeclarativeBase, Base["PctItempoint"]):
    __tablename__ = 'pct_itempoint'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False, index=True)
    pct_point_coefficient = Column(Integer, nullable=False)


class PctResult(DeclarativeBase, Base["PctResult"]):
    __tablename__ = 'pct_result'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=False, index=True)
    score_from = Column(Integer, nullable=False)
    score_to = Column(Integer, nullable=False)
    comment_id_1 = Column(Integer, nullable=False)
    comment_id_2 = Column(Integer, nullable=False)
    comment_id_3 = Column(Integer, nullable=False)
    comment_id_4 = Column(Integer, nullable=False)
    comment_id_5 = Column(Integer, nullable=False)


class PctReward(DeclarativeBase, Base["PctReward"]):
    __tablename__ = 'pct_reward'

    id = Column(Integer, primary_key=True)
    pct_point_type = Column(Integer, nullable=False, index=True)
    pct_point = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class PctSystem(DeclarativeBase, Base["PctSystem"]):
    __tablename__ = 'pct_system'

    id = Column(Integer, primary_key=True)
    pct_base_speed = Column(Integer, nullable=False)
    fever_point_max = Column(Integer, nullable=False)
    fever_time = Column(Integer, nullable=False)
    fever_revention_time = Column(Integer, nullable=False)
    pct_time = Column(Integer, nullable=False)
    chara1 = Column(Integer, nullable=False)
    chara2 = Column(Integer, nullable=False)
    chara1_gauge_choice = Column(Integer, nullable=False)
    chara2_gauge_choice = Column(Integer, nullable=False)


class PctSystemFruit(DeclarativeBase, Base["PctSystemFruit"]):
    __tablename__ = 'pct_system_fruits'

    id = Column(Integer, primary_key=True)
    last_time = Column(Integer, nullable=False)
    appearance = Column(Integer, nullable=False)
    bar_split = Column(Integer, nullable=False)
    appearance_chara_odds = Column(Integer, nullable=False)
    appearance_pattern = Column(Text, nullable=False)
    wait_time = Column(Integer, nullable=False)


class PctTapSpeed(DeclarativeBase, Base["PctTapSpeed"]):
    __tablename__ = 'pct_tap_speed'

    id = Column(Integer, primary_key=True)
    combo_count = Column(Integer, nullable=False)
    speed_magnification = Column(Integer, nullable=False)


class PkbBatterCondition(DeclarativeBase, Base["PkbBatterCondition"]):
    __tablename__ = 'pkb_batter_condition'

    batter_id = Column(Integer, primary_key=True)
    pkb_score = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    detail = Column(Text, nullable=False)
    meet = Column(Integer, nullable=False)
    critical = Column(Integer, nullable=False)
    power = Column(Integer, nullable=False)
    ability_name = Column(Text, nullable=False)
    ability_detail = Column(Text, nullable=False)
    is_playable = Column(Integer, nullable=False)


class PkbDrama(DeclarativeBase, Base["PkbDrama"]):
    __tablename__ = 'pkb_drama'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class PkbDramaDatum(DeclarativeBase, Base["PkbDramaDatum"]):
    __tablename__ = 'pkb_drama_data'

    drama_id = Column(Integer, primary_key=True)
    condition_pitcher_id_1 = Column(Integer, nullable=False)
    condition_pitcher_id_2 = Column(Integer, nullable=False)
    condition_batter_id_1 = Column(Integer, nullable=False)
    condition_batter_id_2 = Column(Integer, nullable=False)


class PkbNaviComment(DeclarativeBase, Base["PkbNaviComment"]):
    __tablename__ = 'pkb_navi_comment'

    comment_id = Column(Integer, primary_key=True)
    where_type = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    face_type = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    description = Column(Text)
    voice_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    change_face_time = Column(Float, nullable=False)
    change_face_type = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class PkbPitcherBallType(DeclarativeBase, Base["PkbPitcherBallType"]):
    __tablename__ = 'pkb_pitcher_ball_type'

    pitcher_id = Column(Integer, primary_key=True, nullable=False, index=True)
    ball_type = Column(Integer, primary_key=True, nullable=False)
    ball_type_name = Column(Text, nullable=False)


class PkbReward(DeclarativeBase, Base["PkbReward"]):
    __tablename__ = 'pkb_reward'

    id = Column(Integer, primary_key=True)
    pkb_score = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class PositionSetting(DeclarativeBase, Base["PositionSetting"]):
    __tablename__ = 'position_setting'

    position_setting_id = Column(Integer, primary_key=True)
    front = Column(Integer, nullable=False)
    middle = Column(Integer, nullable=False)


class PrizegachaDatum(DeclarativeBase, Base["PrizegachaDatum"]):
    __tablename__ = 'prizegacha_data'

    prizegacha_id = Column(Integer, primary_key=True)
    prize_memory_id_1 = Column(Integer, nullable=False)
    prize_memory_id_2 = Column(Integer, nullable=False)
    prize_memory_id_3 = Column(Integer, nullable=False)
    prize_memory_id_4 = Column(Integer, nullable=False)
    prize_memory_id_5 = Column(Integer, nullable=False)
    prize_memory_id_6 = Column(Integer, nullable=False)
    prize_memory_id_7 = Column(Integer, nullable=False)
    prize_memory_id_8 = Column(Integer, nullable=False)
    prize_memory_id_9 = Column(Integer, nullable=False)
    prize_memory_id_10 = Column(Integer, nullable=False)
    prize_memory_id_11 = Column(Integer, nullable=False)
    prize_memory_id_12 = Column(Integer, nullable=False)
    prize_memory_id_13 = Column(Integer, nullable=False)
    prize_memory_id_14 = Column(Integer, nullable=False)
    prize_memory_id_15 = Column(Integer, nullable=False)
    prize_memory_id_16 = Column(Integer, nullable=False)
    prize_memory_id_17 = Column(Integer, nullable=False)
    prize_memory_id_18 = Column(Integer, nullable=False)
    prize_memory_id_19 = Column(Integer, nullable=False)
    prize_memory_id_20 = Column(Integer, nullable=False)
    gacha_prize1 = Column(Integer, nullable=False)
    gacha_prize10 = Column(Integer, nullable=False)
    prize_fixed_compensation = Column(Integer, nullable=False)
    prize_fixed_compensation_quantity = Column(Integer, nullable=False)
    rarity_odds = Column(Integer, nullable=False)
    disp_prize_fixed_compensation = Column(Integer, nullable=False)


class PrizegachaSpDatum(DeclarativeBase, Base["PrizegachaSpDatum"]):
    __tablename__ = 'prizegacha_sp_data'

    gacha_id = Column(Integer, primary_key=True, nullable=False, index=True)
    rarity = Column(Integer, primary_key=True, nullable=False)
    disp_rarity = Column(Integer, nullable=False)


class PrizegachaSpDetail(DeclarativeBase, Base["PrizegachaSpDetail"]):
    __tablename__ = 'prizegacha_sp_detail'

    disp_rarity = Column(Integer, primary_key=True)
    effect_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)


class ProfileFrame(DeclarativeBase, Base["ProfileFrame"]):
    __tablename__ = 'profile_frame'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    type = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    disp_order = Column(Integer, nullable=False)


class PromotionBonu(DeclarativeBase, Base["PromotionBonu"]):
    __tablename__ = 'promotion_bonus'

    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    promotion_level = Column(Integer, primary_key=True, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class PsyDrama(DeclarativeBase, Base["PsyDrama"]):
    __tablename__ = 'psy_drama'

    drama_id = Column(Integer, primary_key=True)
    condition_total_eat = Column(Integer, nullable=False)
    condition_chara_type = Column(Integer, nullable=False)
    condition_time = Column(Text, nullable=False)
    condition_psy_product_1 = Column(Integer, nullable=False)
    condition_psy_product_2 = Column(Integer, nullable=False)
    condition_psy_product_3 = Column(Integer, nullable=False)
    condition_psy_product_4 = Column(Integer, nullable=False)
    condition_psy_product_5 = Column(Integer, nullable=False)
    release_psy_product_id_1 = Column(Integer, nullable=False)
    release_psy_product_id_2 = Column(Integer, nullable=False)
    release_psy_product_id_3 = Column(Integer, nullable=False)
    release_psy_product_id_4 = Column(Integer, nullable=False)
    release_psy_product_id_5 = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)


class PsyDramaScript(DeclarativeBase, Base["PsyDramaScript"]):
    __tablename__ = 'psy_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class PsyNote(DeclarativeBase, Base["PsyNote"]):
    __tablename__ = 'psy_note'

    psy_product_id = Column(Integer, primary_key=True)
    condition_flavor_1 = Column(Integer, nullable=False)
    condition_flavor_2 = Column(Integer, nullable=False)
    psy_product_name = Column(Text, nullable=False)
    flavor_1 = Column(Text, nullable=False)
    flavor_2 = Column(Text, nullable=False)
    flavor_3 = Column(Text, nullable=False)
    disp_order = Column(Integer, nullable=False)
    init_flg = Column(Integer, nullable=False)


class PsyReward(DeclarativeBase, Base["PsyReward"]):
    __tablename__ = 'psy_reward'

    id = Column(Integer, primary_key=True)
    condition_type = Column(Integer, nullable=False)
    condition_num = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class QuestAnnihilation(DeclarativeBase, Base["QuestAnnihilation"]):
    __tablename__ = 'quest_annihilation'

    system_id = Column(Integer, primary_key=True, nullable=False)
    quest_id = Column(Integer, primary_key=True, nullable=False)
    effect_type = Column(Integer, nullable=False)
    quest_effect_position = Column(Integer, nullable=False)
    se_cue_name = Column(Text, nullable=False)


class QuestAreaDatum(DeclarativeBase, Base["QuestAreaDatum"]):
    __tablename__ = 'quest_area_data'

    area_id = Column(Integer, primary_key=True)
    area_name = Column(Text, nullable=False)
    area_display_name = Column(Text, nullable=False)
    map_type = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class QuestConditionDatum(DeclarativeBase, Base["QuestConditionDatum"]):
    __tablename__ = 'quest_condition_data'

    quest_id = Column(Integer, primary_key=True)
    condition_quest_id_1 = Column(Integer, nullable=False)
    condition_quest_id_2 = Column(Integer, nullable=False)
    condition_quest_id_3 = Column(Integer, nullable=False)
    condition_quest_id_4 = Column(Integer, nullable=False)
    condition_quest_id_5 = Column(Integer, nullable=False)
    release_quest_id_1 = Column(Integer, nullable=False)
    release_quest_id_2 = Column(Integer, nullable=False)
    release_quest_id_3 = Column(Integer, nullable=False)
    release_quest_id_4 = Column(Integer, nullable=False)
    release_quest_id_5 = Column(Integer, nullable=False)


class QuestDatum(DeclarativeBase, Base["QuestDatum"]):
    __tablename__ = 'quest_data'

    quest_id = Column(Integer, primary_key=True)
    area_id = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    limit_team_level = Column(Integer, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    stamina = Column(Integer, nullable=False)
    stamina_start = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    unit_exp = Column(Integer, nullable=False)
    love = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    daily_limit = Column(Integer, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)
    rank_reward_group = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    story_id_wavestart_1 = Column(Integer, nullable=False)
    story_id_waveend_1 = Column(Integer, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2 = Column(Text, nullable=False)
    wave_bgm_que_id_2 = Column(Text, nullable=False)
    story_id_wavestart_2 = Column(Integer, nullable=False)
    story_id_waveend_2 = Column(Integer, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3 = Column(Text, nullable=False)
    wave_bgm_que_id_3 = Column(Text, nullable=False)
    story_id_wavestart_3 = Column(Integer, nullable=False)
    story_id_waveend_3 = Column(Integer, nullable=False)
    enemy_image_1 = Column(Integer, nullable=False)
    enemy_image_2 = Column(Integer, nullable=False)
    enemy_image_3 = Column(Integer, nullable=False)
    enemy_image_4 = Column(Integer, nullable=False)
    enemy_image_5 = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    lv_reward_flag = Column(Integer, nullable=False)
    add_treasure_num = Column(Integer, nullable=False)


class QuestDefeatNotice(DeclarativeBase, Base["QuestDefeatNotice"]):
    __tablename__ = 'quest_defeat_notice'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, nullable=False)
    required_team_level = Column(Integer, nullable=False)
    required_quest_id = Column(Integer, nullable=False)


class QuestRewardDatum(DeclarativeBase, Base["QuestRewardDatum"]):
    __tablename__ = 'quest_reward_data'

    reward_group_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class Rarity6QuestDatum(DeclarativeBase, Base["Rarity6QuestDatum"]):
    __tablename__ = 'rarity_6_quest_data'

    rarity_6_quest_id = Column(Integer, nullable=False, index=True)
    unit_id = Column(Integer, primary_key=True)
    quest_name = Column(Text, nullable=False)
    limit_time = Column(Integer, nullable=False)
    recommended_level = Column(Integer, nullable=False)
    reward_group_id = Column(Integer, nullable=False)
    treasure_type = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    bg_position = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    enemy_position_x_1 = Column(Integer, nullable=False)
    enemy_local_position_y_1 = Column(Integer, nullable=False)
    enemy_size_1 = Column(Float, nullable=False)
    enemy_position_x_2 = Column(Integer, nullable=False)
    enemy_local_position_y_2 = Column(Integer, nullable=False)
    enemy_size_2 = Column(Float, nullable=False)
    enemy_position_x_3 = Column(Integer, nullable=False)
    enemy_local_position_y_3 = Column(Integer, nullable=False)
    enemy_size_3 = Column(Float, nullable=False)
    enemy_position_x_4 = Column(Integer, nullable=False)
    enemy_local_position_y_4 = Column(Integer, nullable=False)
    enemy_size_4 = Column(Float, nullable=False)
    enemy_position_x_5 = Column(Integer, nullable=False)
    enemy_local_position_y_5 = Column(Integer, nullable=False)
    enemy_size_5 = Column(Float, nullable=False)
    wave_bgm = Column(Text, nullable=False)


class RedeemStaticPriceGroup(DeclarativeBase, Base["RedeemStaticPriceGroup"]):
    __tablename__ = 'redeem_static_price_group'

    condition_category = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False)


class RedeemUnit(DeclarativeBase, Base["RedeemUnit"]):
    __tablename__ = 'redeem_unit'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False, index=True)
    slot_id = Column(Integer, nullable=False)
    condition_category = Column(Integer, nullable=False)
    condition_id = Column(Integer, nullable=False)
    consume_num = Column(Text, nullable=False)


class RedeemUnitBg(DeclarativeBase, Base["RedeemUnitBg"]):
    __tablename__ = 'redeem_unit_bg'

    unit_id = Column(Integer, primary_key=True)
    bg_id = Column(Integer, nullable=False)


class ResistDatum(DeclarativeBase, Base["ResistDatum"]):
    __tablename__ = 'resist_data'

    resist_status_id = Column(Integer, primary_key=True)
    ailment_1 = Column(Integer, nullable=False)
    ailment_2 = Column(Integer, nullable=False)
    ailment_3 = Column(Integer, nullable=False)
    ailment_4 = Column(Integer, nullable=False)
    ailment_5 = Column(Integer, nullable=False)
    ailment_6 = Column(Integer, nullable=False)
    ailment_7 = Column(Integer, nullable=False)
    ailment_8 = Column(Integer, nullable=False)
    ailment_9 = Column(Integer, nullable=False)
    ailment_10 = Column(Integer, nullable=False)
    ailment_11 = Column(Integer, nullable=False)
    ailment_12 = Column(Integer, nullable=False)
    ailment_13 = Column(Integer, nullable=False)
    ailment_14 = Column(Integer, nullable=False)
    ailment_15 = Column(Integer, nullable=False)
    ailment_16 = Column(Integer, nullable=False)
    ailment_17 = Column(Integer, nullable=False)
    ailment_18 = Column(Integer, nullable=False)
    ailment_19 = Column(Integer, nullable=False)
    ailment_20 = Column(Integer, nullable=False)
    ailment_21 = Column(Integer, nullable=False)
    ailment_22 = Column(Integer, nullable=False)
    ailment_23 = Column(Integer, nullable=False)
    ailment_24 = Column(Integer, nullable=False)
    ailment_25 = Column(Integer, nullable=False)
    ailment_26 = Column(Integer, nullable=False)
    ailment_27 = Column(Integer, nullable=False)
    ailment_28 = Column(Integer, nullable=False)
    ailment_29 = Column(Integer, nullable=False)
    ailment_30 = Column(Integer, nullable=False)
    ailment_31 = Column(Integer, nullable=False)
    ailment_32 = Column(Integer, nullable=False)
    ailment_33 = Column(Integer, nullable=False)
    ailment_34 = Column(Integer, nullable=False)
    ailment_35 = Column(Integer, nullable=False)
    ailment_36 = Column(Integer, nullable=False)
    ailment_37 = Column(Integer, nullable=False)
    ailment_38 = Column(Integer, nullable=False)
    ailment_39 = Column(Integer, nullable=False)
    ailment_40 = Column(Integer, nullable=False)
    ailment_41 = Column(Integer, nullable=False)
    ailment_42 = Column(Integer, nullable=False)
    ailment_43 = Column(Integer, nullable=False)
    ailment_44 = Column(Integer, nullable=False)
    ailment_45 = Column(Integer, nullable=False)
    ailment_46 = Column(Integer, nullable=False)
    ailment_47 = Column(Integer, nullable=False)
    ailment_48 = Column(Integer, nullable=False)
    ailment_49 = Column(Integer, nullable=False)
    ailment_50 = Column(Integer, nullable=False)


class ResistVariationDatum(DeclarativeBase, Base["ResistVariationDatum"]):
    __tablename__ = 'resist_variation_data'

    resist_variation_id = Column(Integer, primary_key=True)
    value_1 = Column(Integer, nullable=False)
    value_2 = Column(Integer, nullable=False)
    value_3 = Column(Integer, nullable=False)
    value_4 = Column(Integer, nullable=False)


class ReturnSpecialfesBanner(DeclarativeBase, Base["ReturnSpecialfesBanner"]):
    __tablename__ = 'return_specialfes_banner'

    gacha_id = Column(Integer, primary_key=True)
    banner_id_1 = Column(Integer, nullable=False)
    banner_id_2 = Column(Integer, nullable=False)
    banner_id_3 = Column(Integer, nullable=False)
    banner_id_4 = Column(Integer, nullable=False)
    banner_id_5 = Column(Integer, nullable=False)
    banner_id_6 = Column(Integer, nullable=False)
    banner_id_7 = Column(Integer, nullable=False)
    banner_id_8 = Column(Integer, nullable=False)
    banner_id_9 = Column(Integer, nullable=False)
    banner_id_10 = Column(Integer, nullable=False)


class RewardCollectGuide(DeclarativeBase, Base["RewardCollectGuide"]):
    __tablename__ = 'reward_collect_guide'

    object_id = Column(Integer, primary_key=True)
    quest_id_1 = Column(Integer, nullable=False)
    quest_id_2 = Column(Integer, nullable=False)
    quest_id_3 = Column(Integer, nullable=False)
    quest_id_4 = Column(Integer, nullable=False)
    quest_id_5 = Column(Integer, nullable=False)
    quest_id_6 = Column(Integer, nullable=False)
    quest_id_7 = Column(Integer, nullable=False)
    quest_id_8 = Column(Integer, nullable=False)
    quest_id_9 = Column(Integer, nullable=False)
    quest_id_10 = Column(Integer, nullable=False)
    system_id_1 = Column(Integer, nullable=False)
    system_id_2 = Column(Integer, nullable=False)
    system_id_3 = Column(Integer, nullable=False)
    system_id_4 = Column(Integer, nullable=False)
    system_id_5 = Column(Integer, nullable=False)


class RoomChange(DeclarativeBase, Base["RoomChange"]):
    __tablename__ = 'room_change'

    room_item_id = Column(Integer, primary_key=True)
    change_id = Column(Integer, nullable=False)
    change_start = Column(Text, nullable=False)
    change_end = Column(Text, nullable=False)


class RoomCharacterPersonality(DeclarativeBase, Base["RoomCharacterPersonality"]):
    __tablename__ = 'room_character_personality'

    character_id = Column(Integer, primary_key=True)
    personality_id = Column(Integer, nullable=False)


class RoomCharacterSkinColor(DeclarativeBase, Base["RoomCharacterSkinColor"]):
    __tablename__ = 'room_character_skin_color'

    character_id = Column(Integer, primary_key=True)
    skin_color_id = Column(Integer, nullable=False)


class RoomChatFormation(DeclarativeBase, Base["RoomChatFormation"]):
    __tablename__ = 'room_chat_formation'

    id = Column(Integer, primary_key=True)
    unit_1_x = Column(Integer, nullable=False)
    unit_1_y = Column(Integer, nullable=False)
    unit_1_dir = Column(Integer, nullable=False)
    unit_2_x = Column(Integer, nullable=False)
    unit_2_y = Column(Integer, nullable=False)
    unit_2_dir = Column(Integer, nullable=False)
    unit_3_x = Column(Integer)
    unit_3_y = Column(Integer)
    unit_3_dir = Column(Integer)
    unit_4_x = Column(Integer)
    unit_4_y = Column(Integer)
    unit_4_dir = Column(Integer)
    unit_5_x = Column(Integer)
    unit_5_y = Column(Integer)
    unit_5_dir = Column(Integer)
    unit_num = Column(Integer, nullable=False)
    unit_id1 = Column(Integer)
    unit_id2 = Column(Integer)
    unit_id3 = Column(Integer)
    unit_id4 = Column(Integer)
    unit_id5 = Column(Integer)
    ignore_unit_id1 = Column(Integer)
    ignore_unit_id2 = Column(Integer)
    ignore_unit_id3 = Column(Integer)
    ignore_unit_id4 = Column(Integer)
    ignore_unit_id5 = Column(Integer)


class RoomChatInfo(DeclarativeBase, Base["RoomChatInfo"]):
    __tablename__ = 'room_chat_info'

    id = Column(Integer, primary_key=True)
    formation_id = Column(Integer, nullable=False)
    scenario_id = Column(Integer, nullable=False)


class RoomChatScenario(DeclarativeBase, Base["RoomChatScenario"]):
    __tablename__ = 'room_chat_scenario'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    scenario_idx = Column(Integer, primary_key=True, nullable=False)
    unit_pos_no = Column(Integer, nullable=False)
    delay = Column(Integer, nullable=False)
    affect_type = Column(Integer, nullable=False)
    anime_id = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)


class RoomEffect(DeclarativeBase, Base["RoomEffect"]):
    __tablename__ = 'room_effect'

    id = Column(Integer, primary_key=True)
    reward_get = Column(Integer, nullable=False)
    jukebox = Column(Integer, nullable=False)
    nebbia = Column(Integer, nullable=False)
    arcade = Column(Integer, nullable=False)
    vegetable = Column(Integer, nullable=False)
    poster = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)


class RoomEffectRewardGet(DeclarativeBase, Base["RoomEffectRewardGet"]):
    __tablename__ = 'room_effect_reward_get'

    id = Column(Integer, primary_key=True, nullable=False)
    level = Column(Integer, primary_key=True, nullable=False)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    max_count = Column(Integer, nullable=False)
    inc_step = Column(Integer, nullable=False)
    interval_second = Column(Integer, nullable=False)
    stock_min_step = Column(Text, nullable=False)
    stock_mid_step = Column(Text, nullable=False)


class RoomEmotionIcon(DeclarativeBase, Base["RoomEmotionIcon"]):
    __tablename__ = 'room_emotion_icon'

    id = Column(Integer, primary_key=True)
    enable_auto = Column(Integer, nullable=False)
    enable_tap = Column(Integer, nullable=False)


class RoomExclusiveCondition(DeclarativeBase, Base["RoomExclusiveCondition"]):
    __tablename__ = 'room_exclusive_condition'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False, index=True)
    room_item_id = Column(Integer, nullable=False, index=True)
    notification = Column(Text, nullable=False)


class RoomItem(DeclarativeBase, Base["RoomItem"]):
    __tablename__ = 'room_item'

    id = Column(Integer, primary_key=True)
    item_type = Column(Integer, nullable=False)
    category = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    max_level = Column(Integer, nullable=False)
    enable_remove = Column(Integer, nullable=False)
    max_possession_num = Column(Integer, nullable=False)
    effect_id_1 = Column(Integer, nullable=False)
    shop_start = Column(Text, nullable=False)
    shop_end = Column(Text, nullable=False)
    shop_new_disp_end = Column(Text, nullable=False)
    cost_item_num = Column(Integer, nullable=False)
    shop_open_type = Column(Integer, nullable=False)
    shop_open_id = Column(Integer, nullable=False)
    shop_open_value = Column(Integer, nullable=False)
    sold_price = Column(Integer, nullable=False)
    sort = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    category_action_type = Column(Integer, nullable=False)


class RoomItemAnnouncement(DeclarativeBase, Base["RoomItemAnnouncement"]):
    __tablename__ = 'room_item_announcement'

    id = Column(Integer, primary_key=True)
    announcement_start = Column(Text, nullable=False)
    announcement_end = Column(Text, nullable=False)
    announcement_text = Column(Text, nullable=False)


class RoomItemDetail(DeclarativeBase, Base["RoomItemDetail"]):
    __tablename__ = 'room_item_detail'
    __table_args__ = (
        Index('room_item_detail_0_lvup_trigger_type_1_lvup_trigger_id', 'lvup_trigger_type', 'lvup_trigger_id'),
        Index('room_item_detail_0_lvup_trigger_type_2_1_lvup_trigger_id_2', 'lvup_trigger_type_2', 'lvup_trigger_id_2')
    )

    room_item_id = Column(Integer, primary_key=True, nullable=False)
    level = Column(Integer, primary_key=True, nullable=False)
    item_detail = Column(Text, nullable=False)
    lvup_trigger_type = Column(Integer, nullable=False)
    lvup_trigger_id = Column(Integer, nullable=False)
    lvup_trigger_value = Column(Integer, nullable=False)
    lvup_trigger_type_2 = Column(Integer, nullable=False)
    lvup_trigger_id_2 = Column(Integer, nullable=False)
    lvup_trigger_value_2 = Column(Integer, nullable=False)
    lvup_item1_type = Column(Integer, nullable=False)
    lvup_item1_id = Column(Integer, nullable=False)
    lvup_item1_num = Column(Integer, nullable=False)
    lvup_time = Column(Integer, nullable=False)


class RoomItemGetAnnouncement(DeclarativeBase, Base["RoomItemGetAnnouncement"]):
    __tablename__ = 'room_item_get_announcement'

    id = Column(Integer, primary_key=True)
    room_item_id = Column(Integer, nullable=False)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text, nullable=False)
    get_date = Column(Text, nullable=False)
    room_announcement_name = Column(Text, nullable=False)


class RoomReleaseDatum(DeclarativeBase, Base["RoomReleaseDatum"]):
    __tablename__ = 'room_release_data'

    system_id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False)
    pre_story_id = Column(Integer, nullable=False)


class RoomSetup(DeclarativeBase, Base["RoomSetup"]):
    __tablename__ = 'room_setup'

    room_item_id = Column(Integer, primary_key=True)
    grid_height = Column(Integer, nullable=False)
    grid_width = Column(Integer, nullable=False)
    unit_id = Column(Integer, nullable=False)


class RoomSkinColor(DeclarativeBase, Base["RoomSkinColor"]):
    __tablename__ = 'room_skin_color'

    skin_color_id = Column(Integer, primary_key=True)
    color_red = Column(Integer, nullable=False)
    color_green = Column(Integer, nullable=False)
    color_blue = Column(Integer, nullable=False)


class RoomUnitComment(DeclarativeBase, Base["RoomUnitComment"]):
    __tablename__ = 'room_unit_comments'

    id = Column(Integer, nullable=False)
    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    trigger = Column(Integer, primary_key=True, nullable=False)
    voice_id = Column(Integer, primary_key=True, nullable=False)
    beloved_step = Column(Integer, nullable=False)
    time = Column(Integer, primary_key=True, nullable=False)
    face_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    insert_word_type = Column(Integer, nullable=False)


class SdNaviComment(DeclarativeBase, Base["SdNaviComment"]):
    __tablename__ = 'sd_navi_comment'

    comment_id = Column(Integer, primary_key=True)
    where_type = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    motion_type = Column(Integer, nullable=False)
    description = Column(Text)
    voice_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class SeasonPack(DeclarativeBase, Base["SeasonPack"]):
    __tablename__ = 'season_pack'

    id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, nullable=False, index=True)
    disp_order = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    receive_text = Column(Text, nullable=False)
    after_text = Column(Text, nullable=False)
    gift_message_id = Column(Integer, nullable=False)
    term = Column(Integer, nullable=False)
    repurchase_day = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)
    system_id_1 = Column(Integer, nullable=False)
    add_num_1 = Column(Integer, nullable=False)
    item_record_id = Column(Integer, nullable=False)
    condition_flg = Column(Integer, nullable=False)
    reward_rate_1 = Column(Integer, nullable=False)


class SeasonpassFoundation(DeclarativeBase, Base["SeasonpassFoundation"]):
    __tablename__ = 'seasonpass_foundation'

    season_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    key_jewel_id = Column(Integer, nullable=False)
    advance_jewel_id = Column(Integer, nullable=False)
    final_jewel_id = Column(Integer, nullable=False)
    extra_level = Column(Integer, nullable=False)
    per_level_point = Column(Integer, nullable=False)
    level_max = Column(Integer, nullable=False)
    weekly_point = Column(Integer, nullable=False)
    level_price = Column(Integer, nullable=False)
    point_change_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    proportion = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    limit_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class SeasonpassLevelReward(DeclarativeBase, Base["SeasonpassLevelReward"]):
    __tablename__ = 'seasonpass_level_reward'

    level_id = Column(Integer, primary_key=True)
    degree = Column(Integer, nullable=False)
    free_reward_type = Column(Integer, nullable=False)
    free_reward_id = Column(Integer, nullable=False)
    free_reward_num = Column(Integer, nullable=False)
    charge_reward_type_1 = Column(Integer, nullable=False)
    charge_reward_id_1 = Column(Integer, nullable=False)
    charge_reward_num_1 = Column(Integer, nullable=False)
    charge_reward_type_2 = Column(Integer, nullable=False)
    charge_reward_id_2 = Column(Integer, nullable=False)
    charge_reward_num_2 = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class SeasonpassMissionDatum(DeclarativeBase, Base["SeasonpassMissionDatum"]):
    __tablename__ = 'seasonpass_mission_data'

    seasonpass_mission_id = Column(Integer, primary_key=True)
    mission_type = Column(Integer, nullable=False)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_value_4 = Column(Integer)
    condition_value_5 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class SeasonpassMissionRewardDatum(DeclarativeBase, Base["SeasonpassMissionRewardDatum"]):
    __tablename__ = 'seasonpass_mission_reward_data'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer)
    reward_num = Column(Integer, nullable=False)


class SecretDungeonEmblemMission(DeclarativeBase, Base["SecretDungeonEmblemMission"]):
    __tablename__ = 'secret_dungeon_emblem_mission'

    mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    mission_description = Column(Text, nullable=False)
    emblem_description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer, nullable=False)
    condition_value_2 = Column(Integer, nullable=False)
    condition_value_3 = Column(Integer, nullable=False)
    condition_num = Column(Text, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    dungeon_area_id = Column(Integer, nullable=False)
    visible_flag = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class SecretDungeonEmblemReward(DeclarativeBase, Base["SecretDungeonEmblemReward"]):
    __tablename__ = 'secret_dungeon_emblem_reward'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False, index=True)
    reward_num = Column(Integer, nullable=False)
    icon_type = Column(Integer, nullable=False)


class SecretDungeonFloorReward(DeclarativeBase, Base["SecretDungeonFloorReward"]):
    __tablename__ = 'secret_dungeon_floor_reward'

    dungeon_area_id = Column(Integer, primary_key=True, nullable=False, index=True)
    clear_count = Column(Integer, primary_key=True, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    clear_effect_flag = Column(Integer, nullable=False)
    icon_type = Column(Integer, nullable=False)


class SecretDungeonFloorSetting(DeclarativeBase, Base["SecretDungeonFloorSetting"]):
    __tablename__ = 'secret_dungeon_floor_setting'
    __table_args__ = (
        Index('secret_dungeon_floor_setting_0_quest_id_1_mode', 'quest_id', 'mode'),
    )

    id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, nullable=False, index=True)
    enemy_identify = Column(Integer, nullable=False)
    mode = Column(Integer, nullable=False)
    enemy_id = Column(Integer, nullable=False)
    floor_position_x = Column(Float, nullable=False)
    floor_position_y = Column(Float, nullable=False)
    floor_scale = Column(Float, nullable=False)
    disp_order = Column(Integer, nullable=False)


class SecretDungeonQuestDatum(DeclarativeBase, Base["SecretDungeonQuestDatum"]):
    __tablename__ = 'secret_dungeon_quest_data'
    __table_args__ = (
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num'),
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_difficulty', 'dungeon_area_id', 'difficulty')
    )

    quest_id = Column(Integer, primary_key=True)
    dungeon_area_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    floor_num = Column(Integer, nullable=False)
    quest_type = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    parts_hp_save_flag = Column(Integer, nullable=False)
    energy_reset_flag = Column(Integer, nullable=False)
    fixed_start_tp_rate = Column(Integer, nullable=False)
    emax = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_image_6 = Column(Integer, nullable=False)
    reward_coin = Column(Integer, nullable=False)
    reward_csc = Column(Integer, nullable=False)
    chest_id = Column(Integer, nullable=False)
    odds_group_id = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_id = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_position = Column(Integer, nullable=False)
    dungeon_quest_detail_monster_size = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_1 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_2 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_3 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_4 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_5 = Column(Float, nullable=False)
    dungeon_quest_detail_monster_height = Column(Float, nullable=False)
    multi_target_effect_time = Column(Float, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)


class SecretDungeonSchedule(DeclarativeBase, Base["SecretDungeonSchedule"]):
    __tablename__ = 'secret_dungeon_schedule'

    dungeon_area_id = Column(Integer, primary_key=True)
    teaser_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    count_start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    close_time = Column(Text, nullable=False)


class SekaiAddTimesDatum(DeclarativeBase, Base["SekaiAddTimesDatum"]):
    __tablename__ = 'sekai_add_times_data'

    id = Column(Integer, primary_key=True)
    sekai_id = Column(Integer, nullable=False)
    add_times = Column(Integer, nullable=False)
    add_times_limit = Column(Integer, nullable=False)
    add_times_time = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)


class SekaiBossDamageRankReward(DeclarativeBase, Base["SekaiBossDamageRankReward"]):
    __tablename__ = 'sekai_boss_damage_rank_reward'

    id = Column(Integer, primary_key=True)
    damage_rank_id = Column(Integer, nullable=False)
    ranking_from = Column(Integer, nullable=False)
    ranking_to = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class SekaiBossFixReward(DeclarativeBase, Base["SekaiBossFixReward"]):
    __tablename__ = 'sekai_boss_fix_reward'

    sekai_id = Column(Integer, nullable=False)
    fix_reward_group_id = Column(Integer, nullable=False)
    fix_reward_id = Column(Integer, primary_key=True)
    boss_total_damage = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    reward_type_6 = Column(Integer, nullable=False)
    reward_id_6 = Column(Integer, nullable=False)
    reward_num_6 = Column(Integer, nullable=False)
    reward_type_7 = Column(Integer, nullable=False)
    reward_id_7 = Column(Integer, nullable=False)
    reward_num_7 = Column(Integer, nullable=False)
    reward_type_8 = Column(Integer, nullable=False)
    reward_id_8 = Column(Integer, nullable=False)
    reward_num_8 = Column(Integer, nullable=False)
    reward_type_9 = Column(Integer, nullable=False)
    reward_id_9 = Column(Integer, nullable=False)
    reward_num_9 = Column(Integer, nullable=False)
    reward_type_10 = Column(Integer, nullable=False)
    reward_id_10 = Column(Integer, nullable=False)
    reward_num_10 = Column(Integer, nullable=False)


class SekaiBossMode(DeclarativeBase, Base["SekaiBossMode"]):
    __tablename__ = 'sekai_boss_mode'

    sekai_boss_mode_id = Column(Integer, primary_key=True)
    sekai_enemy_id = Column(Integer, nullable=False)
    sekai_enemy_level = Column(Text, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)
    quest_detail_monster_size = Column(Float, nullable=False)
    quest_detail_monster_height = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    reward_gold_coefficient = Column(Integer, nullable=False)
    limited_mana = Column(Integer, nullable=False)
    score_coefficient = Column(Integer, nullable=False)


class SekaiEnemyParameter(DeclarativeBase, Base["SekaiEnemyParameter"]):
    __tablename__ = 'sekai_enemy_parameter'

    sekai_enemy_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Text, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    wave_hp_recovery = Column(Integer, nullable=False)
    wave_energy_recovery = Column(Integer, nullable=False)
    dodge = Column(Integer, nullable=False)
    physical_penetrate = Column(Integer, nullable=False)
    magic_penetrate = Column(Integer, nullable=False)
    life_steal = Column(Integer, nullable=False)
    hp_recovery_rate = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    energy_reduce_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    ex_skill_lv_1 = Column(Integer, nullable=False)
    ex_skill_lv_2 = Column(Integer, nullable=False)
    ex_skill_lv_3 = Column(Integer, nullable=False)
    ex_skill_lv_4 = Column(Integer, nullable=False)
    ex_skill_lv_5 = Column(Integer, nullable=False)
    resist_status_id = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)


class SekaiSchedule(DeclarativeBase, Base["SekaiSchedule"]):
    __tablename__ = 'sekai_schedule'

    sekai_id = Column(Integer, primary_key=True)
    last_sekai_id = Column(Integer, nullable=False)
    fix_reward_group_id = Column(Integer, nullable=False)
    damage_rank_id = Column(Integer, nullable=False)
    teaser_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    count_start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    end_losstime = Column(Text, nullable=False)
    result_end = Column(Text, nullable=False)


class SekaiTopDatum(DeclarativeBase, Base["SekaiTopDatum"]):
    __tablename__ = 'sekai_top_data'

    id = Column(Integer, primary_key=True)
    sekai_id = Column(Integer, nullable=False, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    top_bg = Column(Integer, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    scale_ratio = Column(Float, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    boss_mode = Column(Integer, nullable=False)
    sekai_boss_mode_id = Column(Integer, nullable=False)
    boss_hp_from = Column(Text, nullable=False)
    boss_hp_to = Column(Text, nullable=False)
    boss_time_from = Column(Text, nullable=False)
    boss_time_to = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    story_id = Column(Integer, nullable=False)


class SekaiTopStoryDatum(DeclarativeBase, Base["SekaiTopStoryDatum"]):
    __tablename__ = 'sekai_top_story_data'

    sekai_id = Column(Integer, nullable=False, index=True)
    story_id = Column(Integer, primary_key=True)
    boss_time_from = Column(Text, nullable=False)
    boss_time_to = Column(Text, nullable=False)


class SekaiUnlockStoryCondition(DeclarativeBase, Base["SekaiUnlockStoryCondition"]):
    __tablename__ = 'sekai_unlock_story_condition'

    story_id = Column(Integer, primary_key=True)
    sekai_id = Column(Integer, nullable=False)
    condition_entry = Column(Integer, nullable=False)
    condition_fix_reward_id = Column(Integer, nullable=False)
    condition_time = Column(Text, nullable=False)


class SerialCodeDatum(DeclarativeBase, Base["SerialCodeDatum"]):
    __tablename__ = 'serial_code_data'

    serial_campaign_id = Column(Integer, primary_key=True)
    serial_group_id = Column(Integer, nullable=False)
    campaign_name = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    limit_num = Column(Integer, nullable=False)


class SerialGroupDatum(DeclarativeBase, Base["SerialGroupDatum"]):
    __tablename__ = 'serial_group_data'

    serial_group_id = Column(Integer, primary_key=True)
    campaign_name = Column(Text, nullable=False)
    serial_campaign_id_1 = Column(Integer, nullable=False)
    serial_campaign_id_2 = Column(Integer, nullable=False)
    serial_campaign_id_3 = Column(Integer, nullable=False)
    serial_campaign_id_4 = Column(Integer, nullable=False)
    serial_campaign_id_5 = Column(Integer, nullable=False)
    serial_campaign_id_6 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class SeriesUnlockCondition(DeclarativeBase, Base["SeriesUnlockCondition"]):
    __tablename__ = 'series_unlock_condition'

    sequel_event_id = Column(Integer, primary_key=True)
    condition_story_id_1 = Column(Integer, nullable=False)
    condition_story_id_2 = Column(Integer, nullable=False)
    condition_event_id = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)


class ShioriBattleMissionDatum(DeclarativeBase, Base["ShioriBattleMissionDatum"]):
    __tablename__ = 'shiori_battle_mission_data'

    mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_value_4 = Column(Integer)
    condition_value_5 = Column(Integer)
    condition_value_6 = Column(Integer)
    condition_value_7 = Column(Integer)
    condition_value_8 = Column(Integer)
    condition_value_9 = Column(Integer)
    condition_value_10 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class ShioriBos(DeclarativeBase, Base["ShioriBos"]):
    __tablename__ = 'shiori_boss'
    __table_args__ = (
        Index('shiori_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
    )

    boss_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    area_id = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    boss_position_x = Column(Integer, nullable=False)
    boss_position_y = Column(Integer, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    icon_display_scale = Column(Float, nullable=False)
    icon_collider_scale = Column(Float, nullable=False)
    limit_time = Column(Integer, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False, index=True)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    story_id_wavestart_1 = Column(Integer, nullable=False)
    story_id_waveend_1 = Column(Integer, nullable=False)
    detail_bg_id = Column(Integer, nullable=False)
    detail_bg_position = Column(Integer, nullable=False)
    detail_boss_bg_size = Column(Float, nullable=False)
    detail_boss_bg_height = Column(Float, nullable=False)
    map_position_x = Column(Float, nullable=False)
    map_position_y = Column(Float, nullable=False)
    map_size = Column(Float, nullable=False)
    deatail_aura_size = Column(Float, nullable=False)
    map_aura_size = Column(Float, nullable=False)
    disp_on_bg = Column(Integer, nullable=False)
    qd_mode = Column(Integer, nullable=False)


class ShioriBossCondition(DeclarativeBase, Base["ShioriBossCondition"]):
    __tablename__ = 'shiori_boss_condition'

    boss_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    release_quest_id = Column(Integer, nullable=False)
    release_boss_id = Column(Integer, nullable=False)


class ShioriDescription(DeclarativeBase, Base["ShioriDescription"]):
    __tablename__ = 'shiori_description'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False, index=True)
    description = Column(Text, nullable=False)


class ShioriEnemyParameter(DeclarativeBase, Base["ShioriEnemyParameter"]):
    __tablename__ = 'shiori_enemy_parameter'

    enemy_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    wave_hp_recovery = Column(Integer, nullable=False)
    wave_energy_recovery = Column(Integer, nullable=False)
    dodge = Column(Integer, nullable=False)
    physical_penetrate = Column(Integer, nullable=False)
    magic_penetrate = Column(Integer, nullable=False)
    life_steal = Column(Integer, nullable=False)
    hp_recovery_rate = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    energy_reduce_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    ex_skill_lv_1 = Column(Integer, nullable=False)
    ex_skill_lv_2 = Column(Integer, nullable=False)
    ex_skill_lv_3 = Column(Integer, nullable=False)
    ex_skill_lv_4 = Column(Integer, nullable=False)
    ex_skill_lv_5 = Column(Integer, nullable=False)
    resist_status_id = Column(Integer, nullable=False)
    resist_variation_id = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)


class ShioriEventList(DeclarativeBase, Base["ShioriEventList"]):
    __tablename__ = 'shiori_event_list'

    event_id = Column(Integer, primary_key=True)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    condition_story_id = Column(Integer, nullable=False)
    condition_chara_id = Column(Integer, nullable=False)
    condition_main_quest_id = Column(Integer, nullable=False)
    condition_shiori_quest_id = Column(Integer, nullable=False)
    original_event_id = Column(Integer, nullable=False, index=True)
    original_start_time = Column(Text, nullable=False)
    gojuon_order = Column(Integer, nullable=False)
    help_index = Column(Text, nullable=False)


class ShioriItem(DeclarativeBase, Base["ShioriItem"]):
    __tablename__ = 'shiori_item'

    event_id = Column(Integer, primary_key=True)
    unit_material_id_1 = Column(Integer, nullable=False)
    unit_material_id_2 = Column(Integer, nullable=False)


class ShioriMissionRewardDatum(DeclarativeBase, Base["ShioriMissionRewardDatum"]):
    __tablename__ = 'shiori_mission_reward_data'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer)
    reward_num = Column(Integer, nullable=False)


class ShioriQuest(DeclarativeBase, Base["ShioriQuest"]):
    __tablename__ = 'shiori_quest'

    quest_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    area_id = Column(Integer, nullable=False)
    quest_seq = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=False)
    icon_offset_x = Column(Float, nullable=False)
    icon_offset_y = Column(Float, nullable=False)
    icon_scale = Column(Float, nullable=False)
    stamina = Column(Integer, nullable=False)
    stamina_start = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    unit_exp = Column(Integer, nullable=False)
    love = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    daily_limit = Column(Integer, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)
    rank_reward_group = Column(Integer, nullable=False)
    drop_reward_type = Column(Integer, nullable=False)
    drop_reward_id = Column(Integer, nullable=False, index=True)
    drop_reward_num = Column(Integer, nullable=False)
    drop_reward_odds = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    story_id_wavestart_1 = Column(Integer, nullable=False)
    story_id_waveend_1 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2 = Column(Text, nullable=False)
    wave_bgm_que_id_2 = Column(Text, nullable=False)
    story_id_wavestart_2 = Column(Integer, nullable=False)
    story_id_waveend_2 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3 = Column(Text, nullable=False)
    wave_bgm_que_id_3 = Column(Text, nullable=False)
    story_id_wavestart_3 = Column(Integer, nullable=False)
    story_id_waveend_3 = Column(Integer, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)


class ShioriQuestArea(DeclarativeBase, Base["ShioriQuestArea"]):
    __tablename__ = 'shiori_quest_area'

    area_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    area_name = Column(Text, nullable=False)
    map_type = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    area_disp = Column(Integer, nullable=False)
    map_id = Column(Integer, nullable=False)
    scroll_width = Column(Integer, nullable=False)
    scroll_height = Column(Integer, nullable=False)
    open_tutorial_id = Column(Integer, nullable=False)
    tutorial_param_1 = Column(Text, nullable=False)
    tutorial_param_2 = Column(Text, nullable=False)
    additional_effect = Column(Integer, nullable=False)


class ShioriQuestCondition(DeclarativeBase, Base["ShioriQuestCondition"]):
    __tablename__ = 'shiori_quest_condition'

    quest_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    release_quest_id = Column(Integer, nullable=False)
    release_boss_id = Column(Integer, nullable=False)
    condition_main_quest_id = Column(Integer, nullable=False)


class ShioriStationaryMissionDatum(DeclarativeBase, Base["ShioriStationaryMissionDatum"]):
    __tablename__ = 'shiori_stationary_mission_data'

    stationary_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    event_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class ShioriUnlockUnitCondition(DeclarativeBase, Base["ShioriUnlockUnitCondition"]):
    __tablename__ = 'shiori_unlock_unit_condition'
    __table_args__ = (
        Index('shiori_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id'),
    )

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)
    condition_mission_id = Column(Integer, nullable=False, index=True)
    top_description = Column(Text, nullable=False)
    description_1 = Column(Text, nullable=False)
    description_2 = Column(Text, nullable=False)


class ShioriWaveGroupDatum(DeclarativeBase, Base["ShioriWaveGroupDatum"]):
    __tablename__ = 'shiori_wave_group_data'

    wave_group_id = Column(Integer, primary_key=True)
    difficulty = Column(Integer, nullable=False)
    wave = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)
    drop_gold_1 = Column(Integer, nullable=False)
    reward_group_id_1 = Column(Integer, nullable=False)
    disp_reward_type_1 = Column(Integer, nullable=False)
    disp_reward_id_1 = Column(Integer, nullable=False)
    reward_lot_count_1 = Column(Integer, nullable=False)
    reward_odds_1 = Column(Integer, nullable=False)
    drop_gold_2 = Column(Integer, nullable=False)
    reward_group_id_2 = Column(Integer, nullable=False)
    disp_reward_type_2 = Column(Integer, nullable=False)
    disp_reward_id_2 = Column(Integer, nullable=False)
    reward_lot_count_2 = Column(Integer, nullable=False)
    reward_odds_2 = Column(Integer, nullable=False)
    drop_gold_3 = Column(Integer, nullable=False)
    reward_group_id_3 = Column(Integer, nullable=False)
    disp_reward_type_3 = Column(Integer, nullable=False)
    disp_reward_id_3 = Column(Integer, nullable=False)
    reward_lot_count_3 = Column(Integer, nullable=False)
    reward_odds_3 = Column(Integer, nullable=False)
    drop_gold_4 = Column(Integer, nullable=False)
    reward_group_id_4 = Column(Integer, nullable=False)
    disp_reward_type_4 = Column(Integer, nullable=False)
    disp_reward_id_4 = Column(Integer, nullable=False)
    reward_lot_count_4 = Column(Integer, nullable=False)
    reward_odds_4 = Column(Integer, nullable=False)
    drop_gold_5 = Column(Integer, nullable=False)
    reward_group_id_5 = Column(Integer, nullable=False)
    disp_reward_type_5 = Column(Integer, nullable=False)
    disp_reward_id_5 = Column(Integer, nullable=False)
    reward_lot_count_5 = Column(Integer, nullable=False)
    reward_odds_5 = Column(Integer, nullable=False)


class ShopStaticPriceGroup(DeclarativeBase, Base["ShopStaticPriceGroup"]):
    __tablename__ = 'shop_static_price_group'

    id = Column(Integer, primary_key=True)
    price_group_id = Column(Integer, nullable=False)
    buy_count_from = Column(Integer, nullable=False)
    buy_count_to = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)


class SkeStoryDatum(DeclarativeBase, Base["SkeStoryDatum"]):
    __tablename__ = 'ske_story_data'

    sub_story_id = Column(Integer, primary_key=True)
    original_event_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    unlock_condition_quest_id = Column(Integer, nullable=False)
    unlock_condition_boss_id = Column(Integer, nullable=False)
    read_condition_event_story_id = Column(Integer, nullable=False)


class SkeStoryScript(DeclarativeBase, Base["SkeStoryScript"]):
    __tablename__ = 'ske_story_script'

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    line_num = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    seek_time = Column(Float, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class SkillAction(DeclarativeBase, Base["SkillAction"]):
    __tablename__ = 'skill_action'

    action_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, nullable=False)
    action_type = Column(Integer, nullable=False)
    action_detail_1 = Column(Integer, nullable=False)
    action_detail_2 = Column(Integer, nullable=False)
    action_detail_3 = Column(Integer, nullable=False)
    action_value_1 = Column(Float, nullable=False)
    action_value_2 = Column(Float, nullable=False)
    action_value_3 = Column(Float, nullable=False)
    action_value_4 = Column(Float, nullable=False)
    action_value_5 = Column(Float, nullable=False)
    action_value_6 = Column(Float, nullable=False)
    action_value_7 = Column(Float, nullable=False)
    target_assignment = Column(Integer, nullable=False)
    target_area = Column(Integer, nullable=False)
    target_range = Column(Integer, nullable=False)
    target_type = Column(Integer, nullable=False)
    target_number = Column(Integer, nullable=False)
    target_count = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    level_up_disp = Column(Text, nullable=False)


class SkillCost(DeclarativeBase, Base["SkillCost"]):
    __tablename__ = 'skill_cost'

    target_level = Column(Integer, primary_key=True)
    cost = Column(Integer, nullable=False)


class SkillDatum(DeclarativeBase, Base["SkillDatum"]):
    __tablename__ = 'skill_data'

    skill_id = Column(Integer, primary_key=True)
    name = Column(Text)
    skill_type = Column(Integer, nullable=False)
    skill_area_width = Column(Integer, nullable=False)
    skill_cast_time = Column(Float, nullable=False)
    boss_ub_cool_time = Column(Float, nullable=False)
    action_1 = Column(Integer, nullable=False)
    action_2 = Column(Integer, nullable=False)
    action_3 = Column(Integer, nullable=False)
    action_4 = Column(Integer, nullable=False)
    action_5 = Column(Integer, nullable=False)
    action_6 = Column(Integer, nullable=False)
    action_7 = Column(Integer, nullable=False)
    depend_action_1 = Column(Integer, nullable=False)
    depend_action_2 = Column(Integer, nullable=False)
    depend_action_3 = Column(Integer, nullable=False)
    depend_action_4 = Column(Integer, nullable=False)
    depend_action_5 = Column(Integer, nullable=False)
    depend_action_6 = Column(Integer, nullable=False)
    depend_action_7 = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    icon_type = Column(Integer, nullable=False)


class SkipBossDatum(DeclarativeBase, Base["SkipBossDatum"]):
    __tablename__ = 'skip_boss_data'

    boss_id = Column(Integer, primary_key=True)
    skip_motion_id = Column(Integer, nullable=False)
    skip_bg_id = Column(Integer, nullable=False)
    skip_position_x = Column(Integer, nullable=False)
    skip_position_y = Column(Integer, nullable=False)
    skip_scale_x = Column(Float, nullable=False)
    skip_scale_y = Column(Float, nullable=False)


class SkipMonsterDatum(DeclarativeBase, Base["SkipMonsterDatum"]):
    __tablename__ = 'skip_monster_data'

    quest_id = Column(Integer, primary_key=True)
    area_id = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    bg_skip_id = Column(Integer, nullable=False)


class SpBattleVoice(DeclarativeBase, Base["SpBattleVoice"]):
    __tablename__ = 'sp_battle_voice'

    id = Column(Integer, primary_key=True, nullable=False)
    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    voice_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)


class SpDetailVoice(DeclarativeBase, Base["SpDetailVoice"]):
    __tablename__ = 'sp_detail_voice'

    unit_id = Column(Integer, primary_key=True)
    cue_name_1 = Column(Text, nullable=False)
    cue_name_2 = Column(Text, nullable=False)
    cue_name_3 = Column(Text, nullable=False)
    cue_name_4 = Column(Text, nullable=False)
    cue_name_5 = Column(Text, nullable=False)


class SpLoseVoice(DeclarativeBase, Base["SpLoseVoice"]):
    __tablename__ = 'sp_lose_voice'

    original_unit_id = Column(Integer, primary_key=True)
    unit_id_1 = Column(Integer, nullable=False)
    unit_1_pos_x = Column(Integer, nullable=False)
    unit_1_pos_y = Column(Integer, nullable=False)
    unit_1_depth = Column(Integer, nullable=False)
    unit_1_clip = Column(Integer, nullable=False)
    unit_id_2 = Column(Integer, nullable=False)
    unit_2_pos_x = Column(Integer, nullable=False)
    unit_2_pos_y = Column(Integer, nullable=False)
    unit_2_depth = Column(Integer, nullable=False)
    unit_2_clip = Column(Integer, nullable=False)
    unit_id_3 = Column(Integer, nullable=False)
    unit_3_pos_x = Column(Integer, nullable=False)
    unit_3_pos_y = Column(Integer, nullable=False)
    unit_3_depth = Column(Integer, nullable=False)
    unit_3_clip = Column(Integer, nullable=False)
    unit_only_disp = Column(Integer, nullable=False)
    speaker_unit_id_1 = Column(Integer, nullable=False)
    speaker_unit_id_2 = Column(Integer, nullable=False)
    speaker_unit_id_3 = Column(Integer, nullable=False)
    speaker_unit_id_4 = Column(Integer, nullable=False)
    speaker_unit_id_5 = Column(Integer, nullable=False)
    speaker_unit_id_6 = Column(Integer, nullable=False)
    speaker_unit_id_7 = Column(Integer, nullable=False)
    speaker_unit_id_8 = Column(Integer, nullable=False)
    speaker_unit_id_9 = Column(Integer, nullable=False)
    speaker_unit_id_10 = Column(Integer, nullable=False)


class SpLoseVoiceGroup(DeclarativeBase, Base["SpLoseVoiceGroup"]):
    __tablename__ = 'sp_lose_voice_group'

    group_id = Column(Integer, primary_key=True, nullable=False)
    unit_id = Column(Integer, primary_key=True, nullable=False)
    speaker_unit_id = Column(Integer, nullable=False)


class SpaceBattleDatum(DeclarativeBase, Base["SpaceBattleDatum"]):
    __tablename__ = 'space_battle_data'

    space_battle_id = Column(Integer, primary_key=True)
    space_enemy_id = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    quest_detail_bg_id = Column(Integer, nullable=False)
    quest_detail_bg_position = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)


class SpaceSchedule(DeclarativeBase, Base["SpaceSchedule"]):
    __tablename__ = 'space_schedule'

    space_id = Column(Integer, primary_key=True)
    teaser_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    count_start_time = Column(Text, nullable=False)
    count_end_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    sid = Column(Integer, nullable=False)
    pre_story_id = Column(Integer, nullable=False)


class SpaceTopDatum(DeclarativeBase, Base["SpaceTopDatum"]):
    __tablename__ = 'space_top_data'

    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, nullable=False, index=True)
    space_battle_id = Column(Integer, nullable=False)
    part_flag = Column(Integer, nullable=False)
    story_id = Column(Integer, nullable=False, index=True)
    time_from = Column(Text, nullable=False)
    time_to = Column(Text, nullable=False)
    skip_battle_time = Column(Text, nullable=False)
    name = Column(Text, nullable=False)


class SpecialStill(DeclarativeBase, Base["SpecialStill"]):
    __tablename__ = 'special_still'

    still_id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    back_momory_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)


class SpecialStoryBanner(DeclarativeBase, Base["SpecialStoryBanner"]):
    __tablename__ = 'special_story_banner'

    id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False, index=True)
    start_time = Column(Text, nullable=False)
    remind_end_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class SpecialfesBanner(DeclarativeBase, Base["SpecialfesBanner"]):
    __tablename__ = 'specialfes_banner'

    gacha_id = Column(Integer, primary_key=True)
    banner_id_1 = Column(Integer, nullable=False)
    banner_id_2 = Column(Integer, nullable=False)
    banner_id_3 = Column(Integer, nullable=False)
    banner_id_4 = Column(Integer, nullable=False)
    banner_id_5 = Column(Integer, nullable=False)
    banner_id_6 = Column(Integer, nullable=False)
    banner_id_7 = Column(Integer, nullable=False)
    banner_id_8 = Column(Integer, nullable=False)
    banner_id_9 = Column(Integer, nullable=False)
    banner_id_10 = Column(Integer, nullable=False)


class SpskillLabelDatum(DeclarativeBase, Base["SpskillLabelDatum"]):
    __tablename__ = 'spskill_label_data'

    unit_id = Column(Integer, primary_key=True)
    normal_label_text = Column(Text, nullable=False)
    sp_label_text = Column(Text, nullable=False)


class SpskillLvInitializeDatum(DeclarativeBase, Base["SpskillLvInitializeDatum"]):
    __tablename__ = 'spskill_lv_initialize_data'

    initialize_skill_id = Column(Integer, primary_key=True)
    base_skill_id = Column(Integer, nullable=False)

class SrtAction(DeclarativeBase, Base["SrtAction"]):
    __tablename__ = 'srt_action'

    action_name = Column(Text, primary_key=True)
    inori_action = Column(Text, nullable=False)
    dragon_action = Column(Text, nullable=False)
    kaya_action = Column(Text, nullable=False)
    homare_action = Column(Text, nullable=False)
    talk_text_type = Column(Integer, nullable=False)
    talk_text = Column(Text, nullable=False)
    voice_list = Column(Text, nullable=False)


class SrtPanel(DeclarativeBase, Base["SrtPanel"]):
    __tablename__ = 'srt_panel'

    reading_id = Column(Integer, primary_key=True)
    reading = Column(Text, nullable=False)
    read_type = Column(Integer, nullable=False)
    panel_id = Column(Integer, nullable=False, index=True)
    detail_text = Column(Text, nullable=False)
    version = Column(Integer, nullable=False, index=True)
    head_symbol = Column(Text, nullable=False)
    tail_symbol = Column(Text, nullable=False)


class SrtReward(DeclarativeBase, Base["SrtReward"]):
    __tablename__ = 'srt_reward'

    id = Column(Integer, primary_key=True)
    srt_score = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class SrtScore(DeclarativeBase, Base["SrtScore"]):
    __tablename__ = 'srt_score'

    difficulty_level = Column(Integer, primary_key=True)
    coefficient_read_type_1 = Column(Integer, nullable=False)
    coefficient_read_type_2 = Column(Integer, nullable=False)
    coefficient_read_type_3 = Column(Integer, nullable=False)
    coefficient_count_priconne_panel = Column(Integer, nullable=False)
    coefficient_fever = Column(Integer, nullable=False)
    constant_turn_bonus = Column(Integer, nullable=False)
    coefficient_turn_bonus = Column(Integer, nullable=False)
    coefficient_avg_answer_time = Column(Integer, nullable=False)
    constant_wrong_num = Column(Integer, nullable=False)
    coefficient_wrong_num = Column(Integer, nullable=False)


class SrtTopTalk(DeclarativeBase, Base["SrtTopTalk"]):
    __tablename__ = 'srt_top_talk'

    id = Column(Integer, primary_key=True)
    talk_id = Column(Integer, nullable=False, index=True)
    chara_index = Column(Integer, nullable=False)
    talk_text = Column(Text, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    direction = Column(Integer, nullable=False)


class SspStoryDatum(DeclarativeBase, Base["SspStoryDatum"]):
    __tablename__ = 'ssp_story_data'

    sub_story_id = Column(Integer, primary_key=True)
    original_event_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    contents_type = Column(Integer, nullable=False, index=True)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    read_condition = Column(Integer, nullable=False)


class Stamp(DeclarativeBase, Base["Stamp"]):
    __tablename__ = 'stamp'

    stamp_id = Column(Integer, primary_key=True)
    disp_order = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text, nullable=False)


class StationaryMissionDatum(DeclarativeBase, Base["StationaryMissionDatum"]):
    __tablename__ = 'stationary_mission_data'

    stationary_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    category_icon = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer)
    condition_value_2 = Column(Integer)
    condition_value_3 = Column(Integer)
    condition_value_4 = Column(Integer)
    condition_value_5 = Column(Integer)
    condition_value_6 = Column(Integer)
    condition_value_7 = Column(Integer)
    condition_value_8 = Column(Integer)
    condition_value_9 = Column(Integer)
    condition_value_10 = Column(Integer)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)
    system_id = Column(Integer)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    min_level = Column(Integer, nullable=False)
    max_level = Column(Integer, nullable=False)
    title_color_id = Column(Integer, nullable=False)
    visible_flag = Column(Integer, nullable=False)


class Still(DeclarativeBase, Base["Still"]):
    __tablename__ = 'still'

    still_id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False)
    story_id = Column(Integer, nullable=False, index=True)
    still_group_id = Column(Integer, nullable=False, index=True)
    vertical_still_flg = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    unit_id_1 = Column(Integer, nullable=False)
    unit_id_2 = Column(Integer, nullable=False)
    unit_id_3 = Column(Integer, nullable=False)
    unit_id_4 = Column(Integer, nullable=False)
    unit_id_5 = Column(Integer, nullable=False)
    unit_id_6 = Column(Integer, nullable=False)
    unit_id_7 = Column(Integer, nullable=False)
    unit_id_8 = Column(Integer, nullable=False)
    unit_id_9 = Column(Integer, nullable=False)
    unit_id_10 = Column(Integer, nullable=False)
    facial_id = Column(Integer, nullable=False)
    album_ignore = Column(Integer, nullable=False)
    my_page_flag = Column(Integer, nullable=False)
    scroll_direction = Column(Integer, nullable=False)


class StoryCharacterMask(DeclarativeBase, Base["StoryCharacterMask"]):
    __tablename__ = 'story_character_mask'

    chara_id = Column(Integer, primary_key=True)
    offset = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    softness = Column(Float, nullable=False)


class StoryDatum(DeclarativeBase, Base["StoryDatum"]):
    __tablename__ = 'story_data'

    story_group_id = Column(Integer, primary_key=True)
    story_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    thumbnail_id = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    condition_free_flag = Column(Integer, nullable=False)
    gojuon_order = Column(Integer, nullable=False)


class StoryDetail(DeclarativeBase, Base["StoryDetail"]):
    __tablename__ = 'story_detail'

    story_id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    visible_type = Column(Integer, nullable=False)
    story_end = Column(Integer, nullable=False)
    pre_story_id = Column(Integer, nullable=False)
    force_unlock_time = Column(Text, nullable=False)
    pre_story_id_2 = Column(Integer, nullable=False)
    force_unlock_time_2 = Column(Text, nullable=False)
    love_level = Column(Integer, nullable=False)
    requirement_id = Column(Integer, nullable=False)
    unlock_quest_id = Column(Integer, nullable=False)
    story_quest_id = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_value_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_value_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_value_3 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class StoryQuestDatum(DeclarativeBase, Base["StoryQuestDatum"]):
    __tablename__ = 'story_quest_data'

    story_quest_id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    limit_time = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2 = Column(Text, nullable=False)
    wave_bgm_que_id_2 = Column(Text, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3 = Column(Text, nullable=False)
    wave_bgm_que_id_3 = Column(Text, nullable=False)
    guest_unit_1 = Column(Integer, nullable=False)
    guest_unit_2 = Column(Integer, nullable=False)
    guest_unit_3 = Column(Integer, nullable=False)
    guest_unit_4 = Column(Integer, nullable=False)
    guest_unit_5 = Column(Integer, nullable=False)


class SvdDramaScript(DeclarativeBase, Base["SvdDramaScript"]):
    __tablename__ = 'svd_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class SvdStoryDatum(DeclarativeBase, Base["SvdStoryDatum"]):
    __tablename__ = 'svd_story_data'

    sub_story_id = Column(Integer, primary_key=True)
    original_event_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    read_condition_time = Column(Text, nullable=False)
    condition_quest_id = Column(Integer, nullable=False)
    condition_boss_id = Column(Integer, nullable=False)
    read_condition = Column(Integer, nullable=False)


class SvdStoryScript(DeclarativeBase, Base["SvdStoryScript"]):
    __tablename__ = 'svd_story_script'

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    line_num = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    seek_time = Column(Float, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class TaqCompletionReward(DeclarativeBase, Base["TaqCompletionReward"]):
    __tablename__ = 'taq_completion_rewards'

    id = Column(Integer, primary_key=True)
    completion_num = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    emblem_id = Column(Integer, nullable=False)


class TaqDatum(DeclarativeBase, Base["TaqDatum"]):
    __tablename__ = 'taq_data'

    taq_no = Column(Integer, primary_key=True)
    genre = Column(Integer, nullable=False)
    taq_type = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    word = Column(Text, nullable=False)
    chunk = Column(Text, nullable=False)
    detail = Column(Text, nullable=False)
    detail_2 = Column(Text, nullable=False)
    assist_detail = Column(Text, nullable=False)
    image_id = Column(Integer, nullable=False)
    char_no_1 = Column(Integer, nullable=False)
    char_no_2 = Column(Integer, nullable=False)
    char_no_3 = Column(Integer, nullable=False)
    char_no_4 = Column(Integer, nullable=False)
    char_no_5 = Column(Integer, nullable=False)
    input_type_1 = Column(Integer, nullable=False)
    input_type_2 = Column(Integer, nullable=False)
    input_type_3 = Column(Integer, nullable=False)
    input_type_4 = Column(Integer, nullable=False)
    input_type_5 = Column(Integer, nullable=False)


class TaqDramaScript(DeclarativeBase, Base["TaqDramaScript"]):
    __tablename__ = 'taq_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class TaqGameSetting(DeclarativeBase, Base["TaqGameSetting"]):
    __tablename__ = 'taq_game_setting'

    id = Column(Integer, primary_key=True)
    lottery_rate = Column(Float, nullable=False)
    help_use_count_normal = Column(Integer, nullable=False)
    help_use_count_hard = Column(Integer, nullable=False)
    help_use_count_veryhard = Column(Integer, nullable=False)


class TaqGenre(DeclarativeBase, Base["TaqGenre"]):
    __tablename__ = 'taq_genre'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(Text, nullable=False)


class TaqGoodUnit(DeclarativeBase, Base["TaqGoodUnit"]):
    __tablename__ = 'taq_good_unit'

    taq_no = Column(Integer, primary_key=True)
    unit_id_1 = Column(Integer, nullable=False)
    unit_id_2 = Column(Integer, nullable=False)
    unit_id_3 = Column(Integer, nullable=False)
    unit_id_4 = Column(Integer, nullable=False)
    unit_id_5 = Column(Integer, nullable=False)
    unit_id_6 = Column(Integer, nullable=False)
    unit_id_7 = Column(Integer, nullable=False)
    unit_id_8 = Column(Integer, nullable=False)
    unit_id_9 = Column(Integer, nullable=False)
    unit_id_10 = Column(Integer, nullable=False)


class TaqIncorrectWord(DeclarativeBase, Base["TaqIncorrectWord"]):
    __tablename__ = 'taq_incorrect_word'

    word_id = Column(Integer, primary_key=True)
    incorrect_word = Column(Text, nullable=False)


class TaqKanjiList(DeclarativeBase, Base["TaqKanjiList"]):
    __tablename__ = 'taq_kanji_list'

    id = Column(Integer, primary_key=True)
    kanji = Column(Text, nullable=False)


class TaqNecessaryWord(DeclarativeBase, Base["TaqNecessaryWord"]):
    __tablename__ = 'taq_necessary_word'

    taq_no = Column(Integer, primary_key=True)
    necessary_word_1 = Column(Text, nullable=False)
    unnecessary_word_1 = Column(Text, nullable=False)
    necessary_word_2 = Column(Text, nullable=False)
    unnecessary_word_2 = Column(Text, nullable=False)
    necessary_word_3 = Column(Text, nullable=False)
    unnecessary_word_3 = Column(Text, nullable=False)
    necessary_word_4 = Column(Text, nullable=False)
    unnecessary_word_4 = Column(Text, nullable=False)
    necessary_word_5 = Column(Text, nullable=False)
    unnecessary_word_5 = Column(Text, nullable=False)


class TaqReward(DeclarativeBase, Base["TaqReward"]):
    __tablename__ = 'taq_rewards'

    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class TaqUnit(DeclarativeBase, Base["TaqUnit"]):
    __tablename__ = 'taq_unit'

    unit_id = Column(Integer, primary_key=True)
    sort_order = Column(Integer, nullable=False)
    personality_id = Column(Integer, nullable=False)
    genre_status_1 = Column(Integer, nullable=False)
    genre_status_2 = Column(Integer, nullable=False)
    genre_status_3 = Column(Integer, nullable=False)
    genre_status_4 = Column(Integer, nullable=False)
    genre_status_5 = Column(Integer, nullable=False)
    genre_status_6 = Column(Integer, nullable=False)


class ThumbnailHideCondition(DeclarativeBase, Base["ThumbnailHideCondition"]):
    __tablename__ = 'thumbnail_hide_condition'

    story_group_id = Column(Integer, primary_key=True)
    hide_story_id_from = Column(Integer, nullable=False)
    hide_story_id_to = Column(Integer, nullable=False)
    unlock_condition_story_id = Column(Integer, nullable=False)


class TicketGachaDatum(DeclarativeBase, Base["TicketGachaDatum"]):
    __tablename__ = 'ticket_gacha_data'

    gacha_id = Column(Integer, primary_key=True)
    gacha_name = Column(Text, nullable=False)
    gacha_type = Column(Integer, nullable=False)
    ticket_id = Column(Integer, nullable=False)
    gacha_times = Column(Integer, nullable=False)
    gacha_detail = Column(Integer, nullable=False)
    guarantee_rarity = Column(Text, nullable=False)
    rarity_odds = Column(Text, nullable=False)
    chara_odds_star1 = Column(Text, nullable=False)
    chara_odds_star2 = Column(Text, nullable=False)
    chara_odds_star3 = Column(Text, nullable=False)
    staging_type = Column(Integer, nullable=False)


class Tip(DeclarativeBase, Base["Tip"]):
    __tablename__ = 'tips'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    tips_index = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)


class TmeMapDatum(DeclarativeBase, Base["TmeMapDatum"]):
    __tablename__ = 'tme_map_data'

    tme_object_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    condition_story_id = Column(Integer, nullable=False)
    area_difficulty_type = Column(Integer, nullable=False)
    release_effect = Column(Integer, nullable=False)
    tap_effect = Column(Integer, nullable=False)


class TowerAreaDatum(DeclarativeBase, Base["TowerAreaDatum"]):
    __tablename__ = 'tower_area_data'

    tower_area_id = Column(Integer, primary_key=True)
    max_floor_num = Column(Integer, nullable=False)
    area_bg = Column(Integer, nullable=False)
    tower_bgm = Column(Text, nullable=False)
    cloister_quest_id = Column(Integer, nullable=False)


class TowerCloisterQuestDatum(DeclarativeBase, Base["TowerCloisterQuestDatum"]):
    __tablename__ = 'tower_cloister_quest_data'

    tower_cloister_quest_id = Column(Integer, primary_key=True)
    daily_limit = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    recovery_hp_rate = Column(Integer, nullable=False)
    recovery_tp_rate = Column(Integer, nullable=False)
    start_tp_rate = Column(Integer, nullable=False)
    fix_reward_group_id = Column(Integer, nullable=False)
    drop_reward_group_id = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_bgm = Column(Text, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    w1_enemy_position_x_1 = Column(Integer, nullable=False)
    w1_enemy_local_position_y_1 = Column(Integer, nullable=False)
    w1_enemy_size_1 = Column(Float, nullable=False)
    w1_enemy_position_x_2 = Column(Integer, nullable=False)
    w1_enemy_local_position_y_2 = Column(Integer, nullable=False)
    w1_enemy_size_2 = Column(Float, nullable=False)
    w1_enemy_position_x_3 = Column(Integer, nullable=False)
    w1_enemy_local_position_y_3 = Column(Integer, nullable=False)
    w1_enemy_size_3 = Column(Float, nullable=False)
    w1_enemy_position_x_4 = Column(Integer, nullable=False)
    w1_enemy_local_position_y_4 = Column(Integer, nullable=False)
    w1_enemy_size_4 = Column(Float, nullable=False)
    w1_enemy_position_x_5 = Column(Integer, nullable=False)
    w1_enemy_local_position_y_5 = Column(Integer, nullable=False)
    w1_enemy_size_5 = Column(Float, nullable=False)
    w2_enemy_position_x_1 = Column(Integer, nullable=False)
    w2_enemy_local_position_y_1 = Column(Integer, nullable=False)
    w2_enemy_size_1 = Column(Float, nullable=False)
    w2_enemy_position_x_2 = Column(Integer, nullable=False)
    w2_enemy_local_position_y_2 = Column(Integer, nullable=False)
    w2_enemy_size_2 = Column(Float, nullable=False)
    w2_enemy_position_x_3 = Column(Integer, nullable=False)
    w2_enemy_local_position_y_3 = Column(Integer, nullable=False)
    w2_enemy_size_3 = Column(Float, nullable=False)
    w2_enemy_position_x_4 = Column(Integer, nullable=False)
    w2_enemy_local_position_y_4 = Column(Integer, nullable=False)
    w2_enemy_size_4 = Column(Float, nullable=False)
    w2_enemy_position_x_5 = Column(Integer, nullable=False)
    w2_enemy_local_position_y_5 = Column(Integer, nullable=False)
    w2_enemy_size_5 = Column(Float, nullable=False)
    w3_enemy_position_x_1 = Column(Integer, nullable=False)
    w3_enemy_local_position_y_1 = Column(Integer, nullable=False)
    w3_enemy_size_1 = Column(Float, nullable=False)
    w3_enemy_position_x_2 = Column(Integer, nullable=False)
    w3_enemy_local_position_y_2 = Column(Integer, nullable=False)
    w3_enemy_size_2 = Column(Float, nullable=False)
    w3_enemy_position_x_3 = Column(Integer, nullable=False)
    w3_enemy_local_position_y_3 = Column(Integer, nullable=False)
    w3_enemy_size_3 = Column(Float, nullable=False)
    w3_enemy_position_x_4 = Column(Integer, nullable=False)
    w3_enemy_local_position_y_4 = Column(Integer, nullable=False)
    w3_enemy_size_4 = Column(Float, nullable=False)
    w3_enemy_position_x_5 = Column(Integer, nullable=False)
    w3_enemy_local_position_y_5 = Column(Integer, nullable=False)
    w3_enemy_size_5 = Column(Float, nullable=False)
    background = Column(Integer, nullable=False)
    bg_position = Column(Integer, nullable=False)


class TowerEnemyParameter(DeclarativeBase, Base["TowerEnemyParameter"]):
    __tablename__ = 'tower_enemy_parameter'

    enemy_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    wave_hp_recovery = Column(Integer, nullable=False)
    wave_energy_recovery = Column(Integer, nullable=False)
    dodge = Column(Integer, nullable=False)
    physical_penetrate = Column(Integer, nullable=False)
    magic_penetrate = Column(Integer, nullable=False)
    life_steal = Column(Integer, nullable=False)
    hp_recovery_rate = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    energy_reduce_rate = Column(Integer, nullable=False)
    union_burst_level = Column(Integer, nullable=False)
    main_skill_lv_1 = Column(Integer, nullable=False)
    main_skill_lv_2 = Column(Integer, nullable=False)
    main_skill_lv_3 = Column(Integer, nullable=False)
    main_skill_lv_4 = Column(Integer, nullable=False)
    main_skill_lv_5 = Column(Integer, nullable=False)
    main_skill_lv_6 = Column(Integer, nullable=False)
    main_skill_lv_7 = Column(Integer, nullable=False)
    main_skill_lv_8 = Column(Integer, nullable=False)
    main_skill_lv_9 = Column(Integer, nullable=False)
    main_skill_lv_10 = Column(Integer, nullable=False)
    ex_skill_lv_1 = Column(Integer, nullable=False)
    ex_skill_lv_2 = Column(Integer, nullable=False)
    ex_skill_lv_3 = Column(Integer, nullable=False)
    ex_skill_lv_4 = Column(Integer, nullable=False)
    ex_skill_lv_5 = Column(Integer, nullable=False)
    resist_status_id = Column(Integer, nullable=False)
    resist_variation_id = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    enemy_color = Column(Integer, nullable=False)


class TowerExQuestDatum(DeclarativeBase, Base["TowerExQuestDatum"]):
    __tablename__ = 'tower_ex_quest_data'

    tower_ex_quest_id = Column(Integer, primary_key=True)
    tower_area_id = Column(Integer, nullable=False)
    floor_num = Column(Integer, nullable=False, index=True)
    stamina = Column(Integer, nullable=False)
    stamina_start = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)
    additional_reward_type = Column(Integer, nullable=False)
    additional_reward_id = Column(Integer, nullable=False)
    fix_reward_group_id = Column(Integer, nullable=False)
    chest_id = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    bg_position = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    enemy_position_x_1 = Column(Integer, nullable=False)
    enemy_local_position_y_1 = Column(Integer, nullable=False)
    enemy_size_1 = Column(Float, nullable=False)
    enemy_position_x_2 = Column(Integer, nullable=False)
    enemy_local_position_y_2 = Column(Integer, nullable=False)
    enemy_size_2 = Column(Float, nullable=False)
    enemy_position_x_3 = Column(Integer, nullable=False)
    enemy_local_position_y_3 = Column(Integer, nullable=False)
    enemy_size_3 = Column(Float, nullable=False)
    enemy_position_x_4 = Column(Integer, nullable=False)
    enemy_local_position_y_4 = Column(Integer, nullable=False)
    enemy_size_4 = Column(Float, nullable=False)
    enemy_position_x_5 = Column(Integer, nullable=False)
    enemy_local_position_y_5 = Column(Integer, nullable=False)
    enemy_size_5 = Column(Float, nullable=False)
    wave_bgm = Column(Text, nullable=False)
    clp_flag = Column(Integer, nullable=False)
    skip_level = Column(Integer, nullable=False)


class TowerQuestDatum(DeclarativeBase, Base["TowerQuestDatum"]):
    __tablename__ = 'tower_quest_data'

    tower_quest_id = Column(Integer, primary_key=True)
    tower_area_id = Column(Integer, nullable=False)
    floor_num = Column(Integer, nullable=False, index=True)
    floor_image_type = Column(Integer, nullable=False)
    floor_image_add_type = Column(Integer, nullable=False)
    open_tower_ex_quest_id = Column(Integer, nullable=False)
    boss_floor_flg = Column(Integer, nullable=False)
    stamina = Column(Integer, nullable=False)
    stamina_start = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    recovery_hp_rate = Column(Integer, nullable=False)
    recovery_tp_rate = Column(Integer, nullable=False)
    start_tp_rate = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)
    additional_reward_type = Column(Integer, nullable=False)
    additional_reward_id = Column(Integer, nullable=False)
    fix_reward_group_id = Column(Integer, nullable=False)
    odds_group_id = Column(Integer, nullable=False)
    chest_id = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    bg_position = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    enemy_position_x_1 = Column(Integer, nullable=False)
    enemy_local_position_y_1 = Column(Integer, nullable=False)
    enemy_size_1 = Column(Float, nullable=False)
    enemy_position_x_2 = Column(Integer, nullable=False)
    enemy_local_position_y_2 = Column(Integer, nullable=False)
    enemy_size_2 = Column(Float, nullable=False)
    enemy_position_x_3 = Column(Integer, nullable=False)
    enemy_local_position_y_3 = Column(Integer, nullable=False)
    enemy_size_3 = Column(Float, nullable=False)
    enemy_position_x_4 = Column(Integer, nullable=False)
    enemy_local_position_y_4 = Column(Integer, nullable=False)
    enemy_size_4 = Column(Float, nullable=False)
    enemy_position_x_5 = Column(Integer, nullable=False)
    enemy_local_position_y_5 = Column(Integer, nullable=False)
    enemy_size_5 = Column(Float, nullable=False)
    wave_bgm = Column(Text, nullable=False)
    clp_flag = Column(Integer, nullable=False)
    skip_level = Column(Integer, nullable=False)


class TowerQuestFixRewardGroup(DeclarativeBase, Base["TowerQuestFixRewardGroup"]):
    __tablename__ = 'tower_quest_fix_reward_group'

    fix_reward_group_id = Column(Integer, primary_key=True)
    treasure_type_1 = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    treasure_type_2 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    treasure_type_3 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    treasure_type_4 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    treasure_type_5 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    treasure_type_6 = Column(Integer, nullable=False)
    reward_type_6 = Column(Integer, nullable=False)
    reward_id_6 = Column(Integer, nullable=False)
    reward_num_6 = Column(Integer, nullable=False)
    treasure_type_7 = Column(Integer, nullable=False)
    reward_type_7 = Column(Integer, nullable=False)
    reward_id_7 = Column(Integer, nullable=False)
    reward_num_7 = Column(Integer, nullable=False)
    treasure_type_8 = Column(Integer, nullable=False)
    reward_type_8 = Column(Integer, nullable=False)
    reward_id_8 = Column(Integer, nullable=False)
    reward_num_8 = Column(Integer, nullable=False)
    treasure_type_9 = Column(Integer, nullable=False)
    reward_type_9 = Column(Integer, nullable=False)
    reward_id_9 = Column(Integer, nullable=False)
    reward_num_9 = Column(Integer, nullable=False)
    treasure_type_10 = Column(Integer, nullable=False)
    reward_type_10 = Column(Integer, nullable=False)
    reward_id_10 = Column(Integer, nullable=False)
    reward_num_10 = Column(Integer, nullable=False)


class TowerQuestOddsGroup(DeclarativeBase, Base["TowerQuestOddsGroup"]):
    __tablename__ = 'tower_quest_odds_group'

    odds_group_id = Column(Integer, primary_key=True, nullable=False, index=True)
    team_level_from = Column(Integer, primary_key=True, nullable=False)
    team_level_to = Column(Integer, primary_key=True, nullable=False)
    treasure_type_1 = Column(Integer, nullable=False)
    odds_csv_1 = Column(Text, nullable=False)
    treasure_type_2 = Column(Integer, nullable=False)
    odds_csv_2 = Column(Text, nullable=False)
    treasure_type_3 = Column(Integer, nullable=False)
    odds_csv_3 = Column(Text, nullable=False)
    treasure_type_4 = Column(Integer, nullable=False)
    odds_csv_4 = Column(Text, nullable=False)
    treasure_type_5 = Column(Integer, nullable=False)
    odds_csv_5 = Column(Text, nullable=False)
    treasure_type_6 = Column(Integer, nullable=False)
    odds_csv_6 = Column(Text, nullable=False)
    treasure_type_7 = Column(Integer, nullable=False)
    odds_csv_7 = Column(Text, nullable=False)
    treasure_type_8 = Column(Integer, nullable=False)
    odds_csv_8 = Column(Text, nullable=False)
    treasure_type_9 = Column(Integer, nullable=False)
    odds_csv_9 = Column(Text, nullable=False)
    treasure_type_10 = Column(Integer, nullable=False)
    odds_csv_10 = Column(Text, nullable=False)


class TowerSchedule(DeclarativeBase, Base["TowerSchedule"]):
    __tablename__ = 'tower_schedule'

    tower_schedule_id = Column(Integer, primary_key=True)
    max_tower_area_id = Column(Integer, nullable=False)
    opening_story_id = Column(Integer, nullable=False, index=True)
    count_start_time = Column(Text, nullable=False)
    recovery_disable_time = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class TowerStoryDatum(DeclarativeBase, Base["TowerStoryDatum"]):
    __tablename__ = 'tower_story_data'

    story_group_id = Column(Integer, primary_key=True)
    story_type = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    thumbnail_id = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class TowerStoryDetail(DeclarativeBase, Base["TowerStoryDetail"]):
    __tablename__ = 'tower_story_detail'

    story_id = Column(Integer, primary_key=True)
    story_group_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    sub_title = Column(Text, nullable=False)
    visible_type = Column(Integer, nullable=False)
    story_end = Column(Integer, nullable=False)
    pre_story_id = Column(Integer, nullable=False)
    love_level = Column(Integer, nullable=False)
    requirement_id = Column(Integer, nullable=False)
    unlock_quest_id = Column(Integer, nullable=False)
    story_quest_id = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_value_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_value_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_value_3 = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class TowerWaveGroupDatum(DeclarativeBase, Base["TowerWaveGroupDatum"]):
    __tablename__ = 'tower_wave_group_data'

    id = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, primary_key=True)
    odds = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)


class TrainingQuestDatum(DeclarativeBase, Base["TrainingQuestDatum"]):
    __tablename__ = 'training_quest_data'

    quest_id = Column(Integer, primary_key=True)
    area_id = Column(Integer, nullable=False)
    quest_name = Column(Text, nullable=False)
    limit_team_level = Column(Integer, nullable=False)
    unlock_quest_id_1 = Column(Integer, nullable=False)
    unlock_quest_id_2 = Column(Integer, nullable=False)
    stamina = Column(Integer, nullable=False)
    stamina_start = Column(Integer, nullable=False)
    team_exp = Column(Integer, nullable=False)
    unit_exp = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    rank_reward_group = Column(Integer, nullable=False)
    background_1 = Column(Integer, nullable=False)
    wave_group_id_1 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1 = Column(Text, nullable=False)
    wave_bgm_que_id_1 = Column(Text, nullable=False)
    background_2 = Column(Integer, nullable=False)
    wave_group_id_2 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2 = Column(Text, nullable=False)
    wave_bgm_que_id_2 = Column(Text, nullable=False)
    background_3 = Column(Integer, nullable=False)
    wave_group_id_3 = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3 = Column(Text, nullable=False)
    wave_bgm_que_id_3 = Column(Text, nullable=False)
    enemy_image_1 = Column(Integer, nullable=False)
    enemy_image_2 = Column(Integer, nullable=False)
    enemy_image_3 = Column(Integer, nullable=False)
    enemy_image_4 = Column(Integer, nullable=False)
    enemy_image_5 = Column(Integer, nullable=False)
    reward_image_1 = Column(Integer, nullable=False)
    reward_image_2 = Column(Integer, nullable=False)
    reward_image_3 = Column(Integer, nullable=False)
    reward_image_4 = Column(Integer, nullable=False)
    reward_image_5 = Column(Integer, nullable=False)
    training_quest_detail_bg_id = Column(Integer, nullable=False)
    training_quest_detail_bg_position = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class TrialBattleCategory(DeclarativeBase, Base["TrialBattleCategory"]):
    __tablename__ = 'trial_battle_category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(Text, nullable=False)
    icon_id = Column(Integer, nullable=False)
    label_type_1 = Column(Integer, nullable=False)
    label_type_2 = Column(Integer, nullable=False)
    label_type_3 = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    description_detail = Column(Text, nullable=False)


class TrialBattleDatum(DeclarativeBase, Base["TrialBattleDatum"]):
    __tablename__ = 'trial_battle_data'

    quest_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, nullable=False, index=True)
    difficulty = Column(Integer, nullable=False)
    battle_name = Column(Text, nullable=False)
    detail_bg_id = Column(Integer, nullable=False)
    detail_bg_position = Column(Integer, nullable=False)
    detail_boss_bg_size = Column(Integer, nullable=False)
    detail_boss_bg_height = Column(Integer, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    limit_time = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    wave_group_id = Column(Integer, nullable=False)
    wave_bgm_sheet_id = Column(Text, nullable=False)
    wave_bgm_que_id = Column(Text, nullable=False)
    clear_reward_group = Column(Integer, nullable=False)


class TrialBattleMissionDatum(DeclarativeBase, Base["TrialBattleMissionDatum"]):
    __tablename__ = 'trial_battle_mission_data'

    trial_mission_id = Column(Integer, primary_key=True)
    disp_group = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    quest_id = Column(Integer, nullable=False)
    condition_value = Column(Integer, nullable=False)
    condition_num = Column(Integer, nullable=False)
    mission_reward_id = Column(Integer, nullable=False)


class TrialBattleMissionReward(DeclarativeBase, Base["TrialBattleMissionReward"]):
    __tablename__ = 'trial_battle_mission_reward'

    id = Column(Integer, primary_key=True)
    mission_reward_id = Column(Integer, nullable=False, index=True)
    reward_type = Column(Integer, nullable=False)
    reward_id = Column(Integer, nullable=False)
    reward_num = Column(Integer, nullable=False)


class TrialBattleRewardDatum(DeclarativeBase, Base["TrialBattleRewardDatum"]):
    __tablename__ = 'trial_battle_reward_data'

    reward_group_id = Column(Integer, primary_key=True)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)


class TtkDrama(DeclarativeBase, Base["TtkDrama"]):
    __tablename__ = 'ttk_drama'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class TtkEnemy(DeclarativeBase, Base["TtkEnemy"]):
    __tablename__ = 'ttk_enemy'

    enemy_id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    coin = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)


class TtkNaviComment(DeclarativeBase, Base["TtkNaviComment"]):
    __tablename__ = 'ttk_navi_comment'

    comment_id = Column(Integer, primary_key=True)
    where_type = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    face_type = Column(Integer, nullable=False)
    character_name = Column(Text, nullable=False)
    description = Column(Text)
    voice_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    change_face_time = Column(Float, nullable=False)
    change_face_type = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class TtkReward(DeclarativeBase, Base["TtkReward"]):
    __tablename__ = 'ttk_reward'

    id = Column(Integer, primary_key=True)
    ttk_score = Column(Integer, nullable=False, index=True)
    mission_detail = Column(Text, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_count_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_count_5 = Column(Integer, nullable=False)


class TtkScore(DeclarativeBase, Base["TtkScore"]):
    __tablename__ = 'ttk_score'

    difficulty_level = Column(Integer, primary_key=True)
    coefficient_difficulty = Column(Integer, nullable=False)
    coefficient_coin_score = Column(Integer, nullable=False)
    life = Column(Integer, nullable=False)
    coefficient_wrong_num = Column(Integer, nullable=False)


class TtkStory(DeclarativeBase, Base["TtkStory"]):
    __tablename__ = 'ttk_story'

    ttk_story_id = Column(Integer, primary_key=True)
    ttk_score = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)


class TtkStoryScript(DeclarativeBase, Base["TtkStoryScript"]):
    __tablename__ = 'ttk_story_script'

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False, index=True)
    seq_num = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    line_num = Column(Integer, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    seek_time = Column(Float, nullable=False)
    sheet_name = Column(Text, nullable=False)
    cue_name = Column(Text, nullable=False)
    command = Column(Integer, nullable=False)
    command_param = Column(Float, nullable=False)


class TtkWeapon(DeclarativeBase, Base["TtkWeapon"]):
    __tablename__ = 'ttk_weapon'

    ttk_weapon_id = Column(Integer, primary_key=True)
    ttk_score = Column(Integer, nullable=False, index=True)
    name = Column(Text, nullable=False)


class UbAutoDatum(DeclarativeBase, Base["UbAutoDatum"]):
    __tablename__ = 'ub_auto_data'

    ub_auto_id = Column(Integer, primary_key=True)
    auto_type = Column(Integer, nullable=False)
    auto_detail_1 = Column(Integer, nullable=False)
    auto_detail_2 = Column(Integer, nullable=False)
    auto_detail_3 = Column(Integer, nullable=False)
    auto_detail_4 = Column(Integer, nullable=False)
    auto_detail_5 = Column(Integer, nullable=False)
    auto_value_1 = Column(Integer, nullable=False)
    auto_value_2 = Column(Integer, nullable=False)
    auto_value_3 = Column(Integer, nullable=False)
    auto_value_4 = Column(Integer, nullable=False)
    auto_value_5 = Column(Integer, nullable=False)


class UbAutoDefine(DeclarativeBase, Base["UbAutoDefine"]):
    __tablename__ = 'ub_auto_define'

    skill_id = Column(Integer, primary_key=True)
    ub_auto_id_1 = Column(Integer, nullable=False)
    ub_auto_id_2 = Column(Integer, nullable=False)
    ub_auto_id_3 = Column(Integer, nullable=False)
    ub_auto_id_4 = Column(Integer, nullable=False)
    ub_auto_id_5 = Column(Integer, nullable=False)


class UekBos(DeclarativeBase, Base["UekBos"]):
    __tablename__ = 'uek_boss'

    area = Column(Integer, primary_key=True)
    quest_name = Column(Text, nullable=False)
    limit_time = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    background = Column(Integer, nullable=False)
    enemy_id = Column(Integer, nullable=False, index=True)
    bgm_sheet_id = Column(Text, nullable=False)
    bgm_que_id = Column(Text, nullable=False)
    detail_bg_id = Column(Integer, nullable=False)
    detail_bg_position = Column(Integer, nullable=False)
    detail_boss_bg_size = Column(Float, nullable=False)
    detail_boss_bg_height = Column(Integer, nullable=False)
    result_boss_position_y = Column(Integer, nullable=False)
    result_movie = Column(Integer, nullable=False)


class UekDrama(DeclarativeBase, Base["UekDrama"]):
    __tablename__ = 'uek_drama'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class UekMission(DeclarativeBase, Base["UekMission"]):
    __tablename__ = 'uek_mission'

    mission_id = Column(Integer, primary_key=True)
    area = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    mission_condition = Column(Integer, nullable=False)
    condition_value_1 = Column(Integer, nullable=False)
    condition_value_2 = Column(Integer, nullable=False)
    condition_value_3 = Column(Integer, nullable=False)
    condition_value_4 = Column(Integer, nullable=False)
    condition_value_5 = Column(Integer, nullable=False)
    condition_num = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    reward_id_4 = Column(Integer, nullable=False)
    reward_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    reward_id_5 = Column(Integer, nullable=False)
    reward_num_5 = Column(Integer, nullable=False)
    system_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)


class UekSpineAnimLink(DeclarativeBase, Base["UekSpineAnimLink"]):
    __tablename__ = 'uek_spine_anim_link'

    spine_id = Column(Integer, primary_key=True)
    anim_num = Column(Integer, nullable=False, index=True)


class UniqueEquipEnhanceRate(DeclarativeBase, Base["UniqueEquipEnhanceRate"]):
    __tablename__ = 'unique_equip_enhance_rate'

    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, nullable=False, index=True)
    min_lv = Column(Integer, nullable=False)
    max_lv = Column(Integer, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class UniqueEquipmentBonu(DeclarativeBase, Base["UniqueEquipmentBonu"]):
    __tablename__ = 'unique_equipment_bonus'

    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, nullable=False, index=True)
    min_lv = Column(Integer, nullable=False)
    max_lv = Column(Integer, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class UniqueEquipmentCraft(DeclarativeBase, Base["UniqueEquipmentCraft"]):
    __tablename__ = 'unique_equipment_craft'

    equip_id = Column(Integer, primary_key=True)
    crafted_cost = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    item_id_1 = Column(Integer, nullable=False)
    consume_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    item_id_2 = Column(Integer, nullable=False)
    consume_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    item_id_3 = Column(Integer, nullable=False)
    consume_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    item_id_4 = Column(Integer, nullable=False)
    consume_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    item_id_5 = Column(Integer, nullable=False)
    consume_num_5 = Column(Integer, nullable=False)
    reward_type_6 = Column(Integer, nullable=False)
    item_id_6 = Column(Integer, nullable=False)
    consume_num_6 = Column(Integer, nullable=False)
    reward_type_7 = Column(Integer, nullable=False)
    item_id_7 = Column(Integer, nullable=False)
    consume_num_7 = Column(Integer, nullable=False)
    reward_type_8 = Column(Integer, nullable=False)
    item_id_8 = Column(Integer, nullable=False)
    consume_num_8 = Column(Integer, nullable=False)
    reward_type_9 = Column(Integer, nullable=False)
    item_id_9 = Column(Integer, nullable=False)
    consume_num_9 = Column(Integer, nullable=False)
    reward_type_10 = Column(Integer, nullable=False)
    item_id_10 = Column(Integer, nullable=False)
    consume_num_10 = Column(Integer, nullable=False)


class UniqueEquipmentDatum(DeclarativeBase, Base["UniqueEquipmentDatum"]):
    __tablename__ = 'unique_equipment_data'

    equipment_id = Column(Integer, primary_key=True)
    equipment_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    craft_flg = Column(Integer, nullable=False)
    equipment_enhance_point = Column(Integer, nullable=False)
    sale_price = Column(Integer, nullable=False)
    require_level = Column(Integer, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    enable_donation = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)


class UniqueEquipmentEnhanceDatum(DeclarativeBase, Base["UniqueEquipmentEnhanceDatum"]):
    __tablename__ = 'unique_equipment_enhance_data'

    equip_slot = Column(Integer, primary_key=True, nullable=False)
    enhance_level = Column(Integer, primary_key=True, nullable=False)
    needed_point = Column(Integer, nullable=False)
    total_point = Column(Integer, nullable=False)
    needed_mana = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)


class UniqueEquipmentEnhanceRate(DeclarativeBase, Base["UniqueEquipmentEnhanceRate"]):
    __tablename__ = 'unique_equipment_enhance_rate'

    equipment_id = Column(Integer, primary_key=True)
    equipment_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    promotion_level = Column(Integer, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class UniqueEquipmentRankup(DeclarativeBase, Base["UniqueEquipmentRankup"]):
    __tablename__ = 'unique_equipment_rankup'

    equip_id = Column(Integer, primary_key=True, nullable=False, index=True)
    unique_equip_rank = Column(Integer, primary_key=True, nullable=False)
    unit_level = Column(Integer, nullable=False)
    crafted_cost = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    item_id_1 = Column(Integer, nullable=False)
    consume_num_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    item_id_2 = Column(Integer, nullable=False)
    consume_num_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    item_id_3 = Column(Integer, nullable=False)
    consume_num_3 = Column(Integer, nullable=False)
    reward_type_4 = Column(Integer, nullable=False)
    item_id_4 = Column(Integer, nullable=False)
    consume_num_4 = Column(Integer, nullable=False)
    reward_type_5 = Column(Integer, nullable=False)
    item_id_5 = Column(Integer, nullable=False)
    consume_num_5 = Column(Integer, nullable=False)
    reward_type_6 = Column(Integer, nullable=False)
    item_id_6 = Column(Integer, nullable=False)
    consume_num_6 = Column(Integer, nullable=False)
    reward_type_7 = Column(Integer, nullable=False)
    item_id_7 = Column(Integer, nullable=False)
    consume_num_7 = Column(Integer, nullable=False)
    reward_type_8 = Column(Integer, nullable=False)
    item_id_8 = Column(Integer, nullable=False)
    consume_num_8 = Column(Integer, nullable=False)
    reward_type_9 = Column(Integer, nullable=False)
    item_id_9 = Column(Integer, nullable=False)
    consume_num_9 = Column(Integer, nullable=False)
    reward_type_10 = Column(Integer, nullable=False)
    item_id_10 = Column(Integer, nullable=False)
    consume_num_10 = Column(Integer, nullable=False)


class UnitAttackPattern(DeclarativeBase, Base["UnitAttackPattern"]):
    __tablename__ = 'unit_attack_pattern'

    pattern_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    loop_start = Column(Integer, nullable=False)
    loop_end = Column(Integer, nullable=False)
    atk_pattern_1 = Column(Integer, nullable=False)
    atk_pattern_2 = Column(Integer, nullable=False)
    atk_pattern_3 = Column(Integer, nullable=False)
    atk_pattern_4 = Column(Integer, nullable=False)
    atk_pattern_5 = Column(Integer, nullable=False)
    atk_pattern_6 = Column(Integer, nullable=False)
    atk_pattern_7 = Column(Integer, nullable=False)
    atk_pattern_8 = Column(Integer, nullable=False)
    atk_pattern_9 = Column(Integer, nullable=False)
    atk_pattern_10 = Column(Integer, nullable=False)
    atk_pattern_11 = Column(Integer, nullable=False)
    atk_pattern_12 = Column(Integer, nullable=False)
    atk_pattern_13 = Column(Integer, nullable=False)
    atk_pattern_14 = Column(Integer, nullable=False)
    atk_pattern_15 = Column(Integer, nullable=False)
    atk_pattern_16 = Column(Integer, nullable=False)
    atk_pattern_17 = Column(Integer, nullable=False)
    atk_pattern_18 = Column(Integer, nullable=False)
    atk_pattern_19 = Column(Integer, nullable=False)
    atk_pattern_20 = Column(Integer, nullable=False)


class UnitBackground(DeclarativeBase, Base["UnitBackground"]):
    __tablename__ = 'unit_background'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(Text, nullable=False)
    bg_id = Column(Integer, nullable=False)
    bg_name = Column(Text, nullable=False)
    position = Column(Float, nullable=False)
    face_type = Column(Integer, nullable=False)


class UnitClipSetting(DeclarativeBase, Base["UnitClipSetting"]):
    __tablename__ = 'unit_clip_setting'

    clip_id = Column(Integer, primary_key=True)
    center_x = Column(Integer, nullable=False)
    size_x = Column(Integer, nullable=False)
    softness_x = Column(Integer, nullable=False)


class UnitComment(DeclarativeBase, Base["UnitComment"]):
    __tablename__ = 'unit_comments'
    __table_args__ = (
        Index('unit_comments_0_unit_id_1_use_type', 'unit_id', 'use_type'),
    )

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False, index=True)
    use_type = Column(Integer, nullable=False)
    voice_id = Column(Integer, nullable=False)
    face_id = Column(Integer, nullable=False)
    change_time = Column(Float, nullable=False)
    change_face = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    all_comments_flag = Column(Integer, nullable=False)
    target_unit_id = Column(Integer, nullable=False)
    face_id_2 = Column(Integer, nullable=False)
    change_time_2 = Column(Float, nullable=False)
    change_face_2 = Column(Integer, nullable=False)
    face_id_3 = Column(Integer, nullable=False)
    change_time_3 = Column(Float, nullable=False)
    change_face_3 = Column(Integer, nullable=False)


class UnitConversion(DeclarativeBase, Base["UnitConversion"]):
    __tablename__ = 'unit_conversion'

    original_unit_id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False, unique=True)


class UnitDatum(DeclarativeBase, Base["UnitDatum"]):
    __tablename__ = 'unit_data'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(Text, nullable=False)
    kana = Column(Text, nullable=False)
    prefab_id = Column(Integer, nullable=False)
    prefab_id_battle = Column(Integer, nullable=False)
    is_limited = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    motion_type = Column(Integer, nullable=False)
    se_type = Column(Integer, nullable=False)
    move_speed = Column(Integer, nullable=False)
    search_area_width = Column(Integer, nullable=False)
    atk_type = Column(Integer, nullable=False)
    normal_atk_cast_time = Column(Float, nullable=False)
    cutin_1 = Column(Integer, nullable=False)
    cutin_2 = Column(Integer, nullable=False)
    cutin1_star6 = Column(Integer, nullable=False)
    cutin2_star6 = Column(Integer, nullable=False)
    guild_id = Column(Integer, nullable=False)
    exskill_display = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    only_disp_owned = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    original_unit_id = Column(Integer, nullable=False)


class UnitEnemyDatum(DeclarativeBase, Base["UnitEnemyDatum"]):
    __tablename__ = 'unit_enemy_data'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(Text, nullable=False)
    prefab_id = Column(Integer, nullable=False)
    motion_type = Column(Integer, nullable=False)
    se_type = Column(Integer, nullable=False)
    move_speed = Column(Integer, nullable=False)
    search_area_width = Column(Integer, nullable=False)
    atk_type = Column(Integer, nullable=False)
    normal_atk_cast_time = Column(Float, nullable=False)
    cutin = Column(Integer, nullable=False)
    cutin_star6 = Column(Integer, nullable=False)
    visual_change_flag = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)


class UnitIntroduction(DeclarativeBase, Base["UnitIntroduction"]):
    __tablename__ = 'unit_introduction'

    id = Column(Integer, primary_key=True)
    gacha_id = Column(Integer, nullable=False, index=True)
    introduction_number = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)
    maximum_chunk_size_1 = Column(Integer, nullable=False)
    maximum_chunk_size_loop_1 = Column(Integer, nullable=False)
    maximum_chunk_size_2 = Column(Integer, nullable=False)
    maximum_chunk_size_loop_2 = Column(Integer, nullable=False)
    maximum_chunk_size_3 = Column(Integer, nullable=False)
    maximum_chunk_size_loop_3 = Column(Integer, nullable=False)


class UnitMotionList(DeclarativeBase, Base["UnitMotionList"]):
    __tablename__ = 'unit_motion_list'

    unit_id = Column(Integer, primary_key=True)
    sp_motion = Column(Integer, nullable=False)


class UnitMypagePo(DeclarativeBase, Base["UnitMypagePo"]):
    __tablename__ = 'unit_mypage_pos'

    id = Column(Integer, primary_key=True)
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    scale = Column(Float, nullable=False)


class UnitPosAdjustment(DeclarativeBase, Base["UnitPosAdjustment"]):
    __tablename__ = 'unit_pos_adjustment'

    unit_id = Column(Integer, primary_key=True)
    id_1 = Column(Integer, nullable=False)
    id_2 = Column(Integer, nullable=False)
    id_3 = Column(Integer, nullable=False)
    home_1_pos_x = Column(Integer, nullable=False)
    home_1_pos_y = Column(Integer, nullable=False)
    home_1_depth = Column(Integer, nullable=False)
    home_1_clip = Column(Integer, nullable=False)
    home_2_pos_x = Column(Integer, nullable=False)
    home_2_pos_y = Column(Integer, nullable=False)
    home_2_depth = Column(Integer, nullable=False)
    home_2_clip = Column(Integer, nullable=False)
    home_3_pos_x = Column(Integer, nullable=False)
    home_3_pos_y = Column(Integer, nullable=False)
    home_3_depth = Column(Integer, nullable=False)
    home_3_clip = Column(Integer, nullable=False)
    profile_1_pos_x = Column(Integer, nullable=False)
    profile_1_pos_y = Column(Integer, nullable=False)
    profile_1_depth = Column(Integer, nullable=False)
    profile_1_scale = Column(Float, nullable=False)
    profile_1_clip = Column(Integer, nullable=False)
    profile_2_pos_x = Column(Integer, nullable=False)
    profile_2_pos_y = Column(Integer, nullable=False)
    profile_2_depth = Column(Integer, nullable=False)
    profile_2_scale = Column(Float, nullable=False)
    profile_2_clip = Column(Integer, nullable=False)
    profile_3_pos_x = Column(Integer, nullable=False)
    profile_3_pos_y = Column(Integer, nullable=False)
    profile_3_depth = Column(Integer, nullable=False)
    profile_3_scale = Column(Float, nullable=False)
    profile_3_clip = Column(Integer, nullable=False)
    actual_id1 = Column(Integer, nullable=False)
    actual_1_pos_x = Column(Integer, nullable=False)
    actual_1_pos_y = Column(Integer, nullable=False)
    actual_1_depth = Column(Integer, nullable=False)
    actual_1_clip = Column(Integer, nullable=False)
    actual_id2 = Column(Integer, nullable=False)
    actual_2_pos_x = Column(Integer, nullable=False)
    actual_2_pos_y = Column(Integer, nullable=False)
    actual_2_depth = Column(Integer, nullable=False)
    actual_2_clip = Column(Integer, nullable=False)
    actual_id3 = Column(Integer, nullable=False)
    actual_3_pos_x = Column(Integer, nullable=False)
    actual_3_pos_y = Column(Integer, nullable=False)
    actual_3_depth = Column(Integer, nullable=False)
    actual_3_clip = Column(Integer, nullable=False)
    skip_position_x = Column(Integer, nullable=False)
    friend_pos_x = Column(Integer, nullable=False)
    is_myprofile_image = Column(Integer, nullable=False)


class UnitProfile(DeclarativeBase, Base["UnitProfile"]):
    __tablename__ = 'unit_profile'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(Text, nullable=False)
    age = Column(Text, nullable=False)
    guild = Column(Text, nullable=False)
    race = Column(Text, nullable=False)
    height = Column(Text, nullable=False)
    weight = Column(Text, nullable=False)
    birth_month = Column(Text, nullable=False)
    birth_day = Column(Text, nullable=False)
    blood_type = Column(Text, nullable=False)
    favorite = Column(Text, nullable=False)
    voice = Column(Text, nullable=False)
    voice_id = Column(Integer, nullable=False)
    catch_copy = Column(Text, nullable=False)
    self_text = Column(Text, nullable=False)
    guild_id = Column(Text, nullable=False)


class UnitPromotion(DeclarativeBase, Base["UnitPromotion"]):
    __tablename__ = 'unit_promotion'

    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    promotion_level = Column(Integer, primary_key=True, nullable=False)
    equip_slot_1 = Column(Integer, nullable=False)
    equip_slot_2 = Column(Integer, nullable=False)
    equip_slot_3 = Column(Integer, nullable=False)
    equip_slot_4 = Column(Integer, nullable=False)
    equip_slot_5 = Column(Integer, nullable=False)
    equip_slot_6 = Column(Integer, nullable=False)


class UnitPromotionStatu(DeclarativeBase, Base["UnitPromotionStatu"]):
    __tablename__ = 'unit_promotion_status'

    unit_id = Column(Integer, primary_key=True, nullable=False)
    promotion_level = Column(Integer, primary_key=True, nullable=False)
    hp = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)


class UnitRarity(DeclarativeBase, Base["UnitRarity"]):
    __tablename__ = 'unit_rarity'

    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    rarity = Column(Integer, primary_key=True, nullable=False)
    hp = Column(Float, nullable=False)
    hp_growth = Column(Float, nullable=False)
    atk = Column(Float, nullable=False)
    atk_growth = Column(Float, nullable=False)
    magic_str = Column(Float, nullable=False)
    magic_str_growth = Column(Float, nullable=False)
    _def = Column('def', Float, nullable=False)
    def_growth = Column(Float, nullable=False)
    magic_def = Column(Float, nullable=False)
    magic_def_growth = Column(Float, nullable=False)
    physical_critical = Column(Float, nullable=False)
    physical_critical_growth = Column(Float, nullable=False)
    magic_critical = Column(Float, nullable=False)
    magic_critical_growth = Column(Float, nullable=False)
    wave_hp_recovery = Column(Float, nullable=False)
    wave_hp_recovery_growth = Column(Float, nullable=False)
    wave_energy_recovery = Column(Float, nullable=False)
    wave_energy_recovery_growth = Column(Float, nullable=False)
    dodge = Column(Float, nullable=False)
    dodge_growth = Column(Float, nullable=False)
    physical_penetrate = Column(Float, nullable=False)
    physical_penetrate_growth = Column(Float, nullable=False)
    magic_penetrate = Column(Float, nullable=False)
    magic_penetrate_growth = Column(Float, nullable=False)
    life_steal = Column(Float, nullable=False)
    life_steal_growth = Column(Float, nullable=False)
    hp_recovery_rate = Column(Float, nullable=False)
    hp_recovery_rate_growth = Column(Float, nullable=False)
    energy_recovery_rate = Column(Float, nullable=False)
    energy_recovery_rate_growth = Column(Float, nullable=False)
    energy_reduce_rate = Column(Float, nullable=False)
    energy_reduce_rate_growth = Column(Float, nullable=False)
    unit_material_id = Column(Integer, nullable=False, index=True)
    consume_num = Column(Integer, nullable=False)
    consume_gold = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    accuracy_growth = Column(Float, nullable=False)


class UnitSkillDatum(DeclarativeBase, Base["UnitSkillDatum"]):
    __tablename__ = 'unit_skill_data'

    unit_id = Column(Integer, primary_key=True)
    union_burst = Column(Integer, nullable=False)
    main_skill_1 = Column(Integer, nullable=False)
    main_skill_2 = Column(Integer, nullable=False)
    main_skill_3 = Column(Integer, nullable=False)
    main_skill_4 = Column(Integer, nullable=False)
    main_skill_5 = Column(Integer, nullable=False)
    main_skill_6 = Column(Integer, nullable=False)
    main_skill_7 = Column(Integer, nullable=False)
    main_skill_8 = Column(Integer, nullable=False)
    main_skill_9 = Column(Integer, nullable=False)
    main_skill_10 = Column(Integer, nullable=False)
    ex_skill_1 = Column(Integer, nullable=False)
    ex_skill_evolution_1 = Column(Integer, nullable=False)
    ex_skill_2 = Column(Integer, nullable=False)
    ex_skill_evolution_2 = Column(Integer, nullable=False)
    ex_skill_3 = Column(Integer, nullable=False)
    ex_skill_evolution_3 = Column(Integer, nullable=False)
    ex_skill_4 = Column(Integer, nullable=False)
    ex_skill_evolution_4 = Column(Integer, nullable=False)
    ex_skill_5 = Column(Integer, nullable=False)
    ex_skill_evolution_5 = Column(Integer, nullable=False)
    sp_union_burst = Column(Integer, nullable=False)
    sp_skill_1 = Column(Integer, nullable=False)
    sp_skill_2 = Column(Integer, nullable=False)
    sp_skill_3 = Column(Integer, nullable=False)
    sp_skill_4 = Column(Integer, nullable=False)
    sp_skill_5 = Column(Integer, nullable=False)
    union_burst_evolution = Column(Integer, nullable=False)
    main_skill_evolution_1 = Column(Integer, nullable=False)
    main_skill_evolution_2 = Column(Integer, nullable=False)
    sp_skill_evolution_1 = Column(Integer, nullable=False)
    sp_skill_evolution_2 = Column(Integer, nullable=False)


class UnitSkillDataRf(DeclarativeBase, Base["UnitSkillDataRf"]):
    __tablename__ = 'unit_skill_data_rf'

    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, nullable=False, index=True)
    rf_skill_id = Column(Integer, nullable=False, index=True)
    min_lv = Column(Integer, nullable=False)
    max_lv = Column(Integer, nullable=False)


class UnitStatusCoefficient(DeclarativeBase, Base["UnitStatusCoefficient"]):
    __tablename__ = 'unit_status_coefficient'

    coefficient_id = Column(Integer, primary_key=True)
    hp_coefficient = Column(Float, nullable=False)
    atk_coefficient = Column(Float, nullable=False)
    magic_str_coefficient = Column(Float, nullable=False)
    def_coefficient = Column(Float, nullable=False)
    magic_def_coefficient = Column(Float, nullable=False)
    physical_critical_coefficient = Column(Float, nullable=False)
    magic_critical_coefficient = Column(Float, nullable=False)
    wave_hp_recovery_coefficient = Column(Float, nullable=False)
    wave_energy_recovery_coefficient = Column(Float, nullable=False)
    dodge_coefficient = Column(Float, nullable=False)
    physical_penetrate_coefficient = Column(Float, nullable=False)
    magic_penetrate_coefficient = Column(Float, nullable=False)
    life_steal_coefficient = Column(Float, nullable=False)
    hp_recovery_rate_coefficient = Column(Float, nullable=False)
    energy_recovery_rate_coefficient = Column(Float, nullable=False)
    energy_reduce_rate_coefficient = Column(Float, nullable=False)
    skill_lv_coefficient = Column(Float, nullable=False)
    exskill_evolution_coefficient = Column(Integer, nullable=False)
    overall_coefficient = Column(Float, nullable=False)
    accuracy_coefficient = Column(Float, nullable=False)
    skill1_evolution_coefficient = Column(Integer, nullable=False)
    skill1_evolution_slv_coefficient = Column(Float, nullable=False)
    ub_evolution_coefficient = Column(Integer, nullable=False)
    ub_evolution_slv_coefficient = Column(Float, nullable=False)


class UnitUniqueEquip(DeclarativeBase, Base["UnitUniqueEquip"]):
    __tablename__ = 'unit_unique_equip'

    unit_id = Column(Integer, primary_key=True)
    equip_slot = Column(Integer, nullable=False)
    equip_id = Column(Integer, nullable=False)


class UnlockRarity6(DeclarativeBase, Base["UnlockRarity6"]):
    __tablename__ = 'unlock_rarity_6'
    __table_args__ = (
        Index('unlock_rarity_6_0_unit_id_1_unlock_level', 'unit_id', 'unlock_level'),
        Index('unlock_rarity_6_0_unit_id_1_slot_id', 'unit_id', 'slot_id')
    )

    unit_id = Column(Integer, primary_key=True, nullable=False, index=True)
    slot_id = Column(Integer, primary_key=True, nullable=False)
    unlock_level = Column(Integer, primary_key=True, nullable=False)
    unlock_flag = Column(Integer, nullable=False)
    consume_gold = Column(Integer, nullable=False)
    material_type = Column(Integer, nullable=False)
    material_id = Column(Integer, nullable=False, index=True)
    material_count = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    atk = Column(Integer, nullable=False)
    magic_str = Column(Integer, nullable=False)
    _def = Column('def', Integer, nullable=False)
    magic_def = Column(Integer, nullable=False)
    physical_critical = Column(Integer, nullable=False)
    magic_critical = Column(Integer, nullable=False)
    wave_hp_recovery = Column(Integer, nullable=False)
    wave_energy_recovery = Column(Integer, nullable=False)
    dodge = Column(Integer, nullable=False)
    physical_penetrate = Column(Integer, nullable=False)
    magic_penetrate = Column(Integer, nullable=False)
    life_steal = Column(Integer, nullable=False)
    hp_recovery_rate = Column(Integer, nullable=False)
    energy_recovery_rate = Column(Integer, nullable=False)
    energy_reduce_rate = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)


class UnlockSkillDatum(DeclarativeBase, Base["UnlockSkillDatum"]):
    __tablename__ = 'unlock_skill_data'

    promotion_level = Column(Integer, nullable=False)
    unlock_skill = Column(Integer, primary_key=True)


class UnlockUnitCondition(DeclarativeBase, Base["UnlockUnitCondition"]):
    __tablename__ = 'unlock_unit_condition'

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(Text, nullable=False)
    class_id = Column(Integer, nullable=False)
    pre_unit_id = Column(Integer, nullable=False)
    condition_type_1 = Column(Integer, nullable=False)
    condition_type_detail_1 = Column(Integer, nullable=False)
    condition_id_1 = Column(Integer, nullable=False)
    count_1 = Column(Integer, nullable=False)
    condition_type_2 = Column(Integer, nullable=False)
    condition_type_detail_2 = Column(Integer, nullable=False)
    condition_id_2 = Column(Integer, nullable=False)
    count_2 = Column(Integer, nullable=False)
    condition_type_3 = Column(Integer, nullable=False)
    condition_type_detail_3 = Column(Integer, nullable=False)
    condition_id_3 = Column(Integer, nullable=False)
    count_3 = Column(Integer, nullable=False)
    condition_type_4 = Column(Integer, nullable=False)
    condition_type_detail_4 = Column(Integer, nullable=False)
    condition_id_4 = Column(Integer, nullable=False)
    count_4 = Column(Integer, nullable=False)
    condition_type_5 = Column(Integer, nullable=False)
    condition_type_detail_5 = Column(Integer, nullable=False)
    condition_id_5 = Column(Integer, nullable=False)
    count_5 = Column(Integer, nullable=False)
    release_effect_type = Column(Integer, nullable=False)


class VisualCustomize(DeclarativeBase, Base["VisualCustomize"]):
    __tablename__ = 'visual_customize'

    id = Column(Integer, primary_key=True)
    title_prefab = Column(Integer, nullable=False)
    title_movie = Column(Integer, nullable=False)
    title_voice = Column(Integer, nullable=False)
    story_top_movie = Column(Integer, nullable=False)
    quest_top_movie = Column(Integer, nullable=False)
    profile_logo = Column(Integer, nullable=False)
    watched_story_id = Column(Integer, nullable=False)
    start_time = Column(Text, nullable=False)
    end_time = Column(Text, nullable=False)


class VoiceGroup(DeclarativeBase, Base["VoiceGroup"]):
    __tablename__ = 'voice_group'

    group_id = Column(Integer, primary_key=True)
    group_id_comment = Column(Text, nullable=False)
    group_unit_id_01 = Column(Integer, nullable=False)
    group_unit_id_02 = Column(Integer, nullable=False)
    group_unit_id_03 = Column(Integer, nullable=False)
    group_unit_id_04 = Column(Integer, nullable=False)
    group_unit_id_05 = Column(Integer, nullable=False)


class VoiceGroupChara(DeclarativeBase, Base["VoiceGroupChara"]):
    __tablename__ = 'voice_group_chara'

    group_unit_id = Column(Integer, primary_key=True)
    group_unit_id_comment = Column(Text, nullable=False)
    unit_id_01 = Column(Integer, nullable=False)
    unit_id_02 = Column(Integer, nullable=False)
    unit_id_03 = Column(Integer, nullable=False)
    unit_id_04 = Column(Integer, nullable=False)
    unit_id_05 = Column(Integer, nullable=False)
    unit_id_06 = Column(Integer, nullable=False)
    unit_id_07 = Column(Integer, nullable=False)
    unit_id_08 = Column(Integer, nullable=False)
    unit_id_09 = Column(Integer, nullable=False)
    unit_id_10 = Column(Integer, nullable=False)


class VoteDatum(DeclarativeBase, Base["VoteDatum"]):
    __tablename__ = 'vote_data'

    vote_id = Column(Integer, primary_key=True)
    vote_start_time = Column(Text, nullable=False)
    vote_end_time = Column(Text, nullable=False)
    result_start_time = Column(Text, nullable=False)
    result_end_time = Column(Text, nullable=False)
    start_story_id = Column(Integer, nullable=False)
    result_story_id = Column(Integer, nullable=False)


class VoteInfo(DeclarativeBase, Base["VoteInfo"]):
    __tablename__ = 'vote_info'

    vote_id = Column(Integer, primary_key=True, nullable=False)
    vote_help_index = Column(Integer, primary_key=True, nullable=False)
    vote_title = Column(Text, nullable=False)
    vote_help = Column(Text, nullable=False)


class VoteUnit(DeclarativeBase, Base["VoteUnit"]):
    __tablename__ = 'vote_unit'

    vote_id = Column(Integer, primary_key=True, nullable=False)
    unit_id = Column(Integer, primary_key=True, nullable=False)
    unit_rarity = Column(Integer, nullable=False)


class WacBirthdayDramaScript(DeclarativeBase, Base["WacBirthdayDramaScript"]):
    __tablename__ = 'wac_birthday_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class WacDatum(DeclarativeBase, Base["WacDatum"]):
    __tablename__ = 'wac_data'

    wac_id = Column(Integer, primary_key=True, nullable=False)
    date_id = Column(Integer, primary_key=True, nullable=False)
    unlock_time = Column(Text, nullable=False)
    pre_drama_id = Column(Integer, nullable=False)
    post_drama_id = Column(Integer, nullable=False)
    idle_drama_id = Column(Integer, nullable=False)
    bg_id = Column(Integer, nullable=False)
    effect_id = Column(Integer, nullable=False)
    mural_group_id = Column(Integer, nullable=False, index=True)
    mural_offset_x = Column(Float, nullable=False)
    birthday_login_bonus_id = Column(Integer, nullable=False)
    unit_id_1 = Column(Integer, nullable=False)
    unit_id_2 = Column(Integer, nullable=False)
    draw_end_to_center = Column(Integer, nullable=False)


class WacDramaScript(DeclarativeBase, Base["WacDramaScript"]):
    __tablename__ = 'wac_drama_script'

    command_id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, nullable=False, index=True)
    command_type = Column(Integer, nullable=False)
    param_01 = Column(Text, nullable=False)
    param_02 = Column(Text, nullable=False)
    param_03 = Column(Text, nullable=False)
    param_04 = Column(Text, nullable=False)
    param_05 = Column(Text, nullable=False)
    param_06 = Column(Text, nullable=False)
    param_07 = Column(Text, nullable=False)
    param_08 = Column(Text, nullable=False)


class WacMuralBgDatum(DeclarativeBase, Base["WacMuralBgDatum"]):
    __tablename__ = 'wac_mural_bg_data'

    wac_id = Column(Integer, primary_key=True, nullable=False)
    date_id = Column(Integer, primary_key=True, nullable=False)
    bg_id = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    start_offset_x = Column(Text, nullable=False)
    end_offset_x = Column(Text, nullable=False)


class WacMuralDatum(DeclarativeBase, Base["WacMuralDatum"]):
    __tablename__ = 'wac_mural_data'

    mural_group_id = Column(Integer, primary_key=True, nullable=False, index=True)
    date_id = Column(Integer, primary_key=True, nullable=False)
    parts_id = Column(Integer, nullable=False)
    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)


class WacPresentStillDatum(DeclarativeBase, Base["WacPresentStillDatum"]):
    __tablename__ = 'wac_present_still_data'

    wac_id = Column(Integer, primary_key=True, nullable=False)
    date_id = Column(Integer, primary_key=True, nullable=False)
    still_id = Column(Integer, nullable=False)


class WaveGroupDatum(DeclarativeBase, Base["WaveGroupDatum"]):
    __tablename__ = 'wave_group_data'

    id = Column(Integer, primary_key=True)
    wave_group_id = Column(Integer, nullable=False)
    odds = Column(Integer, nullable=False)
    enemy_id_1 = Column(Integer, nullable=False)
    drop_gold_1 = Column(Integer, nullable=False)
    drop_reward_id_1 = Column(Integer, nullable=False)
    enemy_id_2 = Column(Integer, nullable=False)
    drop_gold_2 = Column(Integer, nullable=False)
    drop_reward_id_2 = Column(Integer, nullable=False)
    enemy_id_3 = Column(Integer, nullable=False)
    drop_gold_3 = Column(Integer, nullable=False)
    drop_reward_id_3 = Column(Integer, nullable=False)
    enemy_id_4 = Column(Integer, nullable=False)
    drop_gold_4 = Column(Integer, nullable=False)
    drop_reward_id_4 = Column(Integer, nullable=False)
    enemy_id_5 = Column(Integer, nullable=False)
    drop_gold_5 = Column(Integer, nullable=False)
    drop_reward_id_5 = Column(Integer, nullable=False)
    guest_enemy_id = Column(Integer, nullable=False)
    guest_lane = Column(Integer, nullable=False)


class Worldmap(DeclarativeBase, Base["Worldmap"]):
    __tablename__ = 'worldmap'

    course_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    map_id = Column(Integer, nullable=False)
    sheet_id = Column(Text, nullable=False)
    que_id = Column(Text, nullable=False)
    start_area_id = Column(Integer, nullable=False)
    end_area_id = Column(Integer, nullable=False)


class YsnStoryDatum(DeclarativeBase, Base["YsnStoryDatum"]):
    __tablename__ = 'ysn_story_data'

    sub_story_id = Column(Integer, primary_key=True)
    original_event_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    condition_story_id = Column(Integer, nullable=False)
    disp_order = Column(Integer, nullable=False)
    reward_type_1 = Column(Integer, nullable=False)
    reward_id_1 = Column(Integer, nullable=False)
    reward_count_1 = Column(Integer, nullable=False)
    reward_type_2 = Column(Integer, nullable=False)
    reward_id_2 = Column(Integer, nullable=False)
    reward_count_2 = Column(Integer, nullable=False)
    reward_type_3 = Column(Integer, nullable=False)
    reward_id_3 = Column(Integer, nullable=False)
    reward_count_3 = Column(Integer, nullable=False)
