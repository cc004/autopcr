# coding: utf-8
# type: ignore

from sqlalchemy import Column, Float, Index, Integer, Table, Text, UniqueConstraint
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import Session, declarative_base
from typing import Generic, TypeVar, List, Iterator, Tuple
from ..model.common import eInventoryType
from ..model.custom import ItemType
from ..util.linq import flow

T = TypeVar('T')

DeclarativeBase = declarative_base()

class Base(Generic[T]):
    @classmethod
    def query(cls, session: Session) -> flow[T]:
        return flow(session.query(cls).all())

class ActualUnitBackground(DeclarativeBase, Base["ActualUnitBackground"]):
    __tablename__ = 'actual_unit_background'

    unit_id: int = Column(Integer, primary_key=True)
    unit_name: str = Column(Text, nullable=False)
    bg_id: int = Column(Integer, nullable=False)
    face_type: int = Column(Integer, nullable=False)


class AilmentDatum(DeclarativeBase, Base["AilmentDatum"]):
    __tablename__ = 'ailment_data'

    ailment_id: int = Column(Integer, primary_key=True)
    ailment_action: int = Column(Integer, nullable=False)
    ailment_detail_1: int = Column(Integer, nullable=False)
    ailment_name: str = Column(Text, nullable=False)


class AlbumProductionList(DeclarativeBase, Base["AlbumProductionList"]):
    __tablename__ = 'album_production_list'

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False, index=True)
    type: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)


class AlbumVoiceList(DeclarativeBase, Base["AlbumVoiceList"]):
    __tablename__ = 'album_voice_list'

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False, index=True)
    sheet_id: str = Column(Text, nullable=False)
    voice_id: str = Column(Text, nullable=False)
    title: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)


class ApaSchedule(DeclarativeBase, Base["ApaSchedule"]):
    __tablename__ = 'apa_schedule'

    apa_id: int = Column(Integer, primary_key=True)
    start_time: str = Column(Text, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    close_time: str = Column(Text, nullable=False)
    op_story_id: int = Column(Integer, nullable=False)
    ed_story_id: int = Column(Integer, nullable=False)
    url_1: str = Column(Text, nullable=False)
    url_2: str = Column(Text, nullable=False)
    url_3: str = Column(Text, nullable=False)


class ArcadeDescription(DeclarativeBase, Base["ArcadeDescription"]):
    __tablename__ = 'arcade_description'
    __table_args__ = (
        Index('arcade_description_0_arcade_id_1_type', 'arcade_id', 'type'),
    )

    id: int = Column(Integer, primary_key=True)
    arcade_id: int = Column(Integer, nullable=False, index=True)
    type: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)


class ArcadeList(DeclarativeBase, Base["ArcadeList"]):
    __tablename__ = 'arcade_list'

    arcade_id: int = Column(Integer, primary_key=True)
    title: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    price: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    cue_id: str = Column(Text, nullable=False)
    where_type: int = Column(Integer, nullable=False)
    banner_start_time: str = Column(Text, nullable=False)
    banner_end_time: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)


class ArcadeStoryList(DeclarativeBase, Base["ArcadeStoryList"]):
    __tablename__ = 'arcade_story_list'

    story_id: int = Column(Integer, primary_key=True)
    arcade_id: int = Column(Integer, nullable=False, index=True)
    sub_title: str = Column(Text, nullable=False)


class ArenaDailyRankReward(DeclarativeBase, Base["ArenaDailyRankReward"]):
    __tablename__ = 'arena_daily_rank_reward'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ArenaDefenceReward(DeclarativeBase, Base["ArenaDefenceReward"]):
    __tablename__ = 'arena_defence_reward'

    id: int = Column(Integer, primary_key=True)
    limit_count: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ArenaMaxRankReward(DeclarativeBase, Base["ArenaMaxRankReward"]):
    __tablename__ = 'arena_max_rank_reward'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ArenaMaxSeasonRankReward(DeclarativeBase, Base["ArenaMaxSeasonRankReward"]):
    __tablename__ = 'arena_max_season_rank_reward'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class Banner(DeclarativeBase, Base["Banner"]):
    __tablename__ = 'banner'

    banner_id: int = Column(Integer, primary_key=True)
    type: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer, nullable=False)
    gacha_id: int = Column(Integer, nullable=False)
    condition_id: int = Column(Integer, nullable=False)
    priority: int = Column(Integer, nullable=False)
    start_date: str = Column(Text, nullable=False)
    end_date: str = Column(Text, nullable=False)
    sub_banner_id_1: int = Column(Integer, nullable=False)
    is_show_room: int = Column(Integer, nullable=False)
    url: str = Column(Text, nullable=False)
    show_type: int = Column(Integer, nullable=False)
    thumbnail_id: int = Column(Integer, nullable=False)
    poster_id: int = Column(Integer, nullable=False)


class BgDatum(DeclarativeBase, Base["BgDatum"]):
    __tablename__ = 'bg_data'

    view_name: str = Column(Text, primary_key=True)
    bg_id: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class BirthdayLoginBonusDatum(DeclarativeBase, Base["BirthdayLoginBonusDatum"]):
    __tablename__ = 'birthday_login_bonus_data'

    login_bonus_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    login_bonus_type: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    adv_id: int = Column(Integer, nullable=False)


class BirthdayLoginBonusDetail(DeclarativeBase, Base["BirthdayLoginBonusDetail"]):
    __tablename__ = 'birthday_login_bonus_detail'

    id: int = Column(Integer, primary_key=True)
    login_bonus_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_num: int = Column(Integer, nullable=False)


class BirthdayLoginBonusDramaScript(DeclarativeBase, Base["BirthdayLoginBonusDramaScript"]):
    __tablename__ = 'birthday_login_bonus_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class CampaignBeginnerDatum(DeclarativeBase, Base["CampaignBeginnerDatum"]):
    __tablename__ = 'campaign_beginner_data'

    beginner_id: int = Column(Integer, primary_key=True)
    id_from: int = Column(Integer, nullable=False)
    id_to: int = Column(Integer, nullable=False)


class CampaignFreegacha(DeclarativeBase, Base["CampaignFreegacha"]):
    __tablename__ = 'campaign_freegacha'

    id: int = Column(Integer, primary_key=True)
    campaign_id: int = Column(Integer, nullable=False)
    freegacha_1: int = Column(Integer, nullable=False)
    freegacha_10: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    stock_10_flag: int = Column(Integer, nullable=False)
    relation_id: int = Column(Integer, nullable=False)
    relation_count: int = Column(Integer, nullable=False)


class CampaignFreegachaDatum(DeclarativeBase, Base["CampaignFreegachaDatum"]):
    __tablename__ = 'campaign_freegacha_data'

    id: int = Column(Integer, primary_key=True)
    campaign_id: int = Column(Integer, nullable=False)
    gacha_id: int = Column(Integer, nullable=False)


class CampaignFreegachaSp(DeclarativeBase, Base["CampaignFreegachaSp"]):
    __tablename__ = 'campaign_freegacha_sp'

    campaign_id: int = Column(Integer, primary_key=True)
    max_exec_count: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class CampaignLevelDatum(DeclarativeBase, Base["CampaignLevelDatum"]):
    __tablename__ = 'campaign_level_data'

    id: int = Column(Integer, primary_key=True)
    level_id: int = Column(Integer, nullable=False)
    lv_from: int = Column(Integer, nullable=False)
    lv_to: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)
    label_color: str = Column(Text, nullable=False)
    frame_color: str = Column(Text, nullable=False)


class CampaignMissionCategory(DeclarativeBase, Base["CampaignMissionCategory"]):
    __tablename__ = 'campaign_mission_category'
    __table_args__ = (
        Index('campaign_mission_category_0_campaign_id_1_type', 'campaign_id', 'type'),
    )

    id: int = Column(Integer, primary_key=True)
    campaign_id: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    lv_from: int = Column(Integer, nullable=False)
    lv_to: int = Column(Integer, nullable=False)


class CampaignMissionDatum(DeclarativeBase, Base["CampaignMissionDatum"]):
    __tablename__ = 'campaign_mission_data'
    __table_args__ = (
        Index('campaign_mission_data_0_campaign_id_1_type', 'campaign_id', 'type'),
    )

    mission_id: int = Column(Integer, primary_key=True)
    campaign_id: int = Column(Integer, nullable=False, index=True)
    type: int = Column(Integer, nullable=False)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_value_4: int = Column(Integer)
    condition_value_5: int = Column(Integer)
    condition_value_6: int = Column(Integer)
    condition_value_7: int = Column(Integer)
    condition_value_8: int = Column(Integer)
    condition_value_9: int = Column(Integer)
    condition_value_10: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    campaign_mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    min_level: int = Column(Integer, nullable=False)
    max_level: int = Column(Integer, nullable=False)
    title_color_id: int = Column(Integer, nullable=False)
    visible_flag: int = Column(Integer, nullable=False)
    mark_flag: int = Column(Integer, nullable=False)


class CampaignMissionRewardDatum(DeclarativeBase, Base["CampaignMissionRewardDatum"]):
    __tablename__ = 'campaign_mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    campaign_mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer)
    reward_num: int = Column(Integer, nullable=False)


class CampaignMissionSchedule(DeclarativeBase, Base["CampaignMissionSchedule"]):
    __tablename__ = 'campaign_mission_schedule'

    campaign_id: int = Column(Integer, primary_key=True)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    close_time: str = Column(Text, nullable=False)


class CampaignSchedule(DeclarativeBase, Base["CampaignSchedule"]):
    __tablename__ = 'campaign_schedule'

    id: int = Column(Integer, primary_key=True)
    campaign_category: int = Column(Integer, nullable=False)
    value: float = Column(Float, nullable=False)
    system_id: int = Column(Integer, nullable=False)
    icon_image: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    level_id: int = Column(Integer, nullable=False)
    shiori_group_id: int = Column(Integer, nullable=False)
    duplication_order: int = Column(Integer, nullable=False)
    beginner_id: int = Column(Integer, nullable=False)


class CampaignShioriGroup(DeclarativeBase, Base["CampaignShioriGroup"]):
    __tablename__ = 'campaign_shiori_group'

    id: int = Column(Integer, primary_key=True)
    shiori_group_id: int = Column(Integer, nullable=False, index=True)
    event_id: int = Column(Integer, nullable=False)


class CggCompletionDatum(DeclarativeBase, Base["CggCompletionDatum"]):
    __tablename__ = 'cgg_completion_data'

    completion_id: int = Column(Integer, primary_key=True)
    completion_emblem_id: int = Column(Integer, nullable=False)
    gacha_type: int = Column(Integer, nullable=False)
    completion_num: int = Column(Integer, nullable=False)
    secret_goods_id_1: int = Column(Integer, nullable=False)
    secret_goods_id_2: int = Column(Integer, nullable=False)
    secret_goods_id_3: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    receive_description: str = Column(Text, nullable=False)


class CggCompletionRewardDatum(DeclarativeBase, Base["CggCompletionRewardDatum"]):
    __tablename__ = 'cgg_completion_reward_data'

    id: int = Column(Integer, primary_key=True)
    completion_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_num: int = Column(Integer, nullable=False)


class CggDrama(DeclarativeBase, Base["CggDrama"]):
    __tablename__ = 'cgg_drama'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class CggGachaInfo(DeclarativeBase, Base["CggGachaInfo"]):
    __tablename__ = 'cgg_gacha_info'

    gacha_type: int = Column(Integer, primary_key=True)
    cgg_id: int = Column(Integer, nullable=False, index=True)
    gacha_name: str = Column(Text, nullable=False)
    gacha_description: str = Column(Text, nullable=False)
    cost_currency_num: int = Column(Integer, nullable=False)
    gacha_intro: str = Column(Text, nullable=False)


class CggGachaLineup(DeclarativeBase, Base["CggGachaLineup"]):
    __tablename__ = 'cgg_gacha_lineup'

    id: int = Column(Integer, primary_key=True)
    gacha_type: int = Column(Integer, nullable=False, index=True)
    lineup_id: int = Column(Integer, nullable=False)
    goods_id: int = Column(Integer, nullable=False)
    goods_num: int = Column(Integer, nullable=False)


class CggGameSetting(DeclarativeBase, Base["CggGameSetting"]):
    __tablename__ = 'cgg_game_settings'

    cgg_id: int = Column(Integer, primary_key=True)
    goods_shelf_id: int = Column(Integer, nullable=False)
    first_goods_shelf_reward_num: int = Column(Integer, nullable=False)
    cgg_gacha_currency_id: int = Column(Integer, nullable=False)
    first_currency_reward_num: int = Column(Integer, nullable=False)
    exchange_luppi_rate: int = Column(Integer, nullable=False)
    max_gacha_exchange_count: int = Column(Integer, nullable=False)
    max_goods_count: int = Column(Integer, nullable=False)


class CggGoodsDatum(DeclarativeBase, Base["CggGoodsDatum"]):
    __tablename__ = 'cgg_goods_data'

    goods_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    shelf_position_id: int = Column(Integer, nullable=False)
    detail_scale_x: float = Column(Float, nullable=False)
    detail_scale_y: float = Column(Float, nullable=False)
    description: str = Column(Text, nullable=False)


class CharaETicketDatum(DeclarativeBase, Base["CharaETicketDatum"]):
    __tablename__ = 'chara_e_ticket_data'

    ticket_id: int = Column(Integer, primary_key=True)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    jewel_store_id: int = Column(Integer, nullable=False, unique=True)
    icon_id: int = Column(Integer, nullable=False)


class CharaFortuneRail(DeclarativeBase, Base["CharaFortuneRail"]):
    __tablename__ = 'chara_fortune_rail'

    rail_id: int = Column(Integer, primary_key=True)
    gimmick_1_id: str = Column(Text, nullable=False)
    gimmick_1_x: int = Column(Integer, nullable=False)
    gimmick_2_id: str = Column(Text, nullable=False)
    gimmick_2_x: int = Column(Integer, nullable=False)
    gimmick_3_id: str = Column(Text, nullable=False)
    gimmick_3_x: int = Column(Integer, nullable=False)
    gimmick_4_id: str = Column(Text, nullable=False)
    gimmick_4_x: int = Column(Integer, nullable=False)
    gimmick_5_id: str = Column(Text, nullable=False)
    gimmick_5_x: int = Column(Integer, nullable=False)
    gimmick_6_id: str = Column(Text, nullable=False)
    gimmick_6_x: int = Column(Integer, nullable=False)
    gimmick_7_id: str = Column(Text, nullable=False)
    gimmick_7_x: int = Column(Integer, nullable=False)
    gimmick_8_id: str = Column(Text, nullable=False)
    gimmick_8_x: int = Column(Integer, nullable=False)
    gimmick_9_id: str = Column(Text, nullable=False)
    gimmick_9_x: int = Column(Integer, nullable=False)
    gimmick_10_id: str = Column(Text, nullable=False)
    gimmick_10_x: int = Column(Integer, nullable=False)


class CharaFortuneReward(DeclarativeBase, Base["CharaFortuneReward"]):
    __tablename__ = 'chara_fortune_reward'

    id: int = Column(Integer, primary_key=True)
    fortune_id: int = Column(Integer, nullable=False)
    rank: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    count_5: int = Column(Integer, nullable=False)


class CharaFortuneScenario(DeclarativeBase, Base["CharaFortuneScenario"]):
    __tablename__ = 'chara_fortune_scenario'

    scenario_id: int = Column(Integer, primary_key=True)
    rail_1: int = Column(Integer, nullable=False)
    rail_2: int = Column(Integer, nullable=False)
    rail_3: int = Column(Integer, nullable=False)
    rail_4: int = Column(Integer, nullable=False)


class CharaFortuneSchedule(DeclarativeBase, Base["CharaFortuneSchedule"]):
    __tablename__ = 'chara_fortune_schedule'

    fortune_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class CharaIdentity(DeclarativeBase, Base["CharaIdentity"]):
    __tablename__ = 'chara_identity'

    unit_id: int = Column(Integer, primary_key=True)
    chara_type: int = Column(Integer, nullable=False)
    chara_type_2: int = Column(Integer, nullable=False)
    chara_type_3: int = Column(Integer, nullable=False)


class CharaStoryStatu(DeclarativeBase, Base["CharaStoryStatu"]):
    __tablename__ = 'chara_story_status'

    story_id: int = Column(Integer, primary_key=True)
    unlock_story_name: str = Column(Text, nullable=False)
    status_type_1: int = Column(Integer, nullable=False)
    status_rate_1: int = Column(Integer, nullable=False)
    status_type_2: int = Column(Integer, nullable=False)
    status_rate_2: int = Column(Integer, nullable=False)
    status_type_3: int = Column(Integer, nullable=False)
    status_rate_3: int = Column(Integer, nullable=False)
    status_type_4: int = Column(Integer, nullable=False)
    status_rate_4: int = Column(Integer, nullable=False)
    status_type_5: int = Column(Integer, nullable=False)
    status_rate_5: int = Column(Integer, nullable=False)
    chara_id_1: int = Column(Integer, nullable=False)
    chara_id_2: int = Column(Integer, nullable=False)
    chara_id_3: int = Column(Integer, nullable=False)
    chara_id_4: int = Column(Integer, nullable=False)
    chara_id_5: int = Column(Integer, nullable=False)
    chara_id_6: int = Column(Integer, nullable=False)
    chara_id_7: int = Column(Integer, nullable=False)
    chara_id_8: int = Column(Integer, nullable=False)
    chara_id_9: int = Column(Integer, nullable=False)
    chara_id_10: int = Column(Integer, nullable=False)


class CharacterLoveRankupText(DeclarativeBase, Base["CharacterLoveRankupText"]):
    __tablename__ = 'character_love_rankup_text'

    chara_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    love_level: int = Column(Integer, nullable=False)
    scale: float = Column(Float, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    voice_id_1: int = Column(Integer, nullable=False)
    face_1: int = Column(Integer, nullable=False)
    serif_1: str = Column(Text, nullable=False)
    voice_id_2: int = Column(Integer, nullable=False)
    face_2: int = Column(Integer, nullable=False)
    serif_2: str = Column(Text, nullable=False)
    voice_id_3: int = Column(Integer, nullable=False)
    face_3: int = Column(Integer, nullable=False)
    serif_3: str = Column(Text, nullable=False)


class ClanBattle2BossDatum(DeclarativeBase, Base["ClanBattle2BossDatum"]):
    __tablename__ = 'clan_battle_2_boss_data'

    boss_id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    order_num: int = Column(Integer, nullable=False)
    boss_thumb_id: int = Column(Integer, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    scale_ratio: float = Column(Float, nullable=False)
    tap_width_ratio: float = Column(Float, nullable=False)
    tap_height_ratio: float = Column(Float, nullable=False)
    map_position_x: int = Column(Integer, nullable=False)
    map_position_y: int = Column(Integer, nullable=False)
    cursor_position: int = Column(Integer, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)
    quest_detail_monster_size: float = Column(Float, nullable=False)
    quest_detail_monster_height: int = Column(Integer, nullable=False)
    battle_report_monster_size: float = Column(Float, nullable=False)
    battle_report_monster_height: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)


class ClanBattle2MapDatum(DeclarativeBase, Base["ClanBattle2MapDatum"]):
    __tablename__ = 'clan_battle_2_map_data'

    id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False, index=True)
    map_bg: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    lap_num_from: int = Column(Integer, nullable=False)
    lap_num_to: int = Column(Integer, nullable=False)
    boss_id_1: int = Column(Integer, nullable=False)
    boss_id_2: int = Column(Integer, nullable=False)
    boss_id_3: int = Column(Integer, nullable=False)
    boss_id_4: int = Column(Integer, nullable=False)
    boss_id_5: int = Column(Integer, nullable=False)
    aura_effect: int = Column(Integer, nullable=False)
    rsl_unlock_lap: int = Column(Integer, nullable=False)
    phase: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_group_id_4: int = Column(Integer, nullable=False)
    wave_group_id_5: int = Column(Integer, nullable=False)
    fix_reward_id_1: int = Column(Integer, nullable=False)
    fix_reward_id_2: int = Column(Integer, nullable=False)
    fix_reward_id_3: int = Column(Integer, nullable=False)
    fix_reward_id_4: int = Column(Integer, nullable=False)
    fix_reward_id_5: int = Column(Integer, nullable=False)
    damage_rank_id_1: int = Column(Integer, nullable=False)
    damage_rank_id_2: int = Column(Integer, nullable=False)
    damage_rank_id_3: int = Column(Integer, nullable=False)
    damage_rank_id_4: int = Column(Integer, nullable=False)
    damage_rank_id_5: int = Column(Integer, nullable=False)
    reward_gold_coefficient: float = Column(Float, nullable=False)
    limited_mana: int = Column(Integer, nullable=False)
    last_attack_reward_id: int = Column(Integer, nullable=False)
    score_coefficient_1: float = Column(Float, nullable=False)
    score_coefficient_2: float = Column(Float, nullable=False)
    score_coefficient_3: float = Column(Float, nullable=False)
    score_coefficient_4: float = Column(Float, nullable=False)
    score_coefficient_5: float = Column(Float, nullable=False)
    param_adjust_id: int = Column(Integer, nullable=False)
    param_adjust_interval: int = Column(Integer, nullable=False)


class ClanBattleArchiveClanRank(DeclarativeBase, Base["ClanBattleArchiveClanRank"]):
    __tablename__ = 'clan_battle_archive_clan_rank'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)


class ClanBattleArchivePersonRank(DeclarativeBase, Base["ClanBattleArchivePersonRank"]):
    __tablename__ = 'clan_battle_archive_person_rank'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)


class ClanBattleBattleMissionDatum(DeclarativeBase, Base["ClanBattleBattleMissionDatum"]):
    __tablename__ = 'clan_battle_battle_mission_data'

    mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_value_4: int = Column(Integer)
    condition_value_5: int = Column(Integer)
    condition_value_6: int = Column(Integer)
    condition_value_7: int = Column(Integer)
    condition_value_8: int = Column(Integer)
    condition_value_9: int = Column(Integer)
    condition_value_10: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class ClanBattleBossDamageRank(DeclarativeBase, Base["ClanBattleBossDamageRank"]):
    __tablename__ = 'clan_battle_boss_damage_rank'

    id: int = Column(Integer, nullable=False)
    damage_rank_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    ranking_from: int = Column(Integer, primary_key=True, nullable=False)
    ranking_to: int = Column(Integer, primary_key=True, nullable=False)
    odds_group_id: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ClanBattleBossFixReward(DeclarativeBase, Base["ClanBattleBossFixReward"]):
    __tablename__ = 'clan_battle_boss_fix_reward'

    fix_reward_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ClanBattleLastAttackReward(DeclarativeBase, Base["ClanBattleLastAttackReward"]):
    __tablename__ = 'clan_battle_last_attack_reward'

    last_attack_reward_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ClanBattleOddsDatum(DeclarativeBase, Base["ClanBattleOddsDatum"]):
    __tablename__ = 'clan_battle_odds_data'

    odds_group_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    team_level_from: int = Column(Integer, primary_key=True, nullable=False)
    team_level_to: int = Column(Integer, primary_key=True, nullable=False)
    odds_csv_1: str = Column(Text, nullable=False)
    odds_csv_2: str = Column(Text, nullable=False)
    odds_csv_3: str = Column(Text, nullable=False)
    odds_csv_4: str = Column(Text, nullable=False)
    odds_csv_5: str = Column(Text, nullable=False)
    odds_csv_6: str = Column(Text, nullable=False)
    odds_csv_7: str = Column(Text, nullable=False)
    odds_csv_8: str = Column(Text, nullable=False)
    odds_csv_9: str = Column(Text, nullable=False)
    odds_csv_10: str = Column(Text, nullable=False)


class ClanBattleParamAdjust(DeclarativeBase, Base["ClanBattleParamAdjust"]):
    __tablename__ = 'clan_battle_param_adjust'

    param_adjust_id: int = Column(Integer, primary_key=True)
    level: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)
    normal_atk_cast_time: int = Column(Integer, nullable=False)
    score_coefficient: int = Column(Integer, nullable=False)


class ClanBattlePeriod(DeclarativeBase, Base["ClanBattlePeriod"]):
    __tablename__ = 'clan_battle_period'

    clan_battle_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    period: int = Column(Integer, primary_key=True, nullable=False)
    period_detail: str = Column(Text, nullable=False)
    period_detail_bg: int = Column(Integer, nullable=False)
    period_detail_s: str = Column(Text, nullable=False)
    period_detail_bg_s: int = Column(Integer, nullable=False)
    period_detail_bg_position: int = Column(Integer, nullable=False)
    period_detail_boss_position_x: int = Column(Integer, nullable=False)
    period_detail_boss_position_y: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    interval_start: str = Column(Text, nullable=False)
    interval_end: str = Column(Text, nullable=False)
    calc_start: str = Column(Text, nullable=False)
    result_start: str = Column(Text, nullable=False)
    result_end: str = Column(Text, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    chest_id: int = Column(Integer, nullable=False)
    quest_detail_rehearsal_label_height: int = Column(Integer, nullable=False)
    min_carry_over_time: int = Column(Integer, nullable=False)


class ClanBattlePeriodLapReward(DeclarativeBase, Base["ClanBattlePeriodLapReward"]):
    __tablename__ = 'clan_battle_period_lap_reward'

    id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False)
    period: int = Column(Integer, nullable=False)
    lap_num_from: int = Column(Integer, nullable=False)
    lap_num_to: int = Column(Integer, nullable=False)
    ranking_bonus_group: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ClanBattlePeriodRankReward(DeclarativeBase, Base["ClanBattlePeriodRankReward"]):
    __tablename__ = 'clan_battle_period_rank_reward'

    id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False)
    period: int = Column(Integer, nullable=False)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    ranking_bonus_group: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ClanBattleRecommendDatum(DeclarativeBase, Base["ClanBattleRecommendDatum"]):
    __tablename__ = 'clan_battle_recommend_data'

    level_id: int = Column(Integer, primary_key=True)
    recommend_group: int = Column(Integer, nullable=False, index=True)
    level_from: int = Column(Integer, nullable=False)
    level_to: int = Column(Integer, nullable=False)
    atack_party_count: int = Column(Integer, nullable=False)
    magic_party_count: int = Column(Integer, nullable=False)


class ClanBattleSBossDatum(DeclarativeBase, Base["ClanBattleSBossDatum"]):
    __tablename__ = 'clan_battle_s_boss_data'

    boss_id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    order_num: int = Column(Integer, nullable=False)
    boss_thumb_id: int = Column(Integer, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    scale_ratio: float = Column(Float, nullable=False)
    tap_width_ratio: float = Column(Float, nullable=False)
    tap_height_ratio: float = Column(Float, nullable=False)
    map_position_x: int = Column(Integer, nullable=False)
    map_position_y: int = Column(Integer, nullable=False)
    cursor_position: int = Column(Integer, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)
    quest_detail_monster_size: float = Column(Float, nullable=False)
    quest_detail_monster_height: int = Column(Integer, nullable=False)
    battle_report_monster_size: float = Column(Float, nullable=False)
    battle_report_monster_height: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)


class ClanBattleSBossFixReward(DeclarativeBase, Base["ClanBattleSBossFixReward"]):
    __tablename__ = 'clan_battle_s_boss_fix_reward'

    fix_reward_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class ClanBattleSMapDatum(DeclarativeBase, Base["ClanBattleSMapDatum"]):
    __tablename__ = 'clan_battle_s_map_data'

    id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False, index=True)
    map_bg: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    lap_num_from: int = Column(Integer, nullable=False)
    lap_num_to: int = Column(Integer, nullable=False)
    boss_id_1: int = Column(Integer, nullable=False)
    boss_id_2: int = Column(Integer, nullable=False)
    boss_id_3: int = Column(Integer, nullable=False)
    boss_id_4: int = Column(Integer, nullable=False)
    boss_id_5: int = Column(Integer, nullable=False)
    extra_battle_flag1: int = Column(Integer, nullable=False)
    extra_battle_flag2: int = Column(Integer, nullable=False)
    extra_battle_flag3: int = Column(Integer, nullable=False)
    extra_battle_flag4: int = Column(Integer, nullable=False)
    extra_battle_flag5: int = Column(Integer, nullable=False)
    aura_effect: int = Column(Integer, nullable=False)
    rsl_unlock_lap: int = Column(Integer, nullable=False)
    phase: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_group_id_4: int = Column(Integer, nullable=False)
    wave_group_id_5: int = Column(Integer, nullable=False)
    fix_reward_id_1: int = Column(Integer, nullable=False)
    fix_reward_id_2: int = Column(Integer, nullable=False)
    fix_reward_id_3: int = Column(Integer, nullable=False)
    fix_reward_id_4: int = Column(Integer, nullable=False)
    fix_reward_id_5: int = Column(Integer, nullable=False)
    damage_rank_id_1: int = Column(Integer, nullable=False)
    damage_rank_id_2: int = Column(Integer, nullable=False)
    damage_rank_id_3: int = Column(Integer, nullable=False)
    damage_rank_id_4: int = Column(Integer, nullable=False)
    damage_rank_id_5: int = Column(Integer, nullable=False)
    reward_gold_coefficient: float = Column(Float, nullable=False)
    limited_mana: int = Column(Integer, nullable=False)
    last_attack_reward_id: int = Column(Integer, nullable=False)
    score_coefficient_1: float = Column(Float, nullable=False)
    score_coefficient_2: float = Column(Float, nullable=False)
    score_coefficient_3: float = Column(Float, nullable=False)
    score_coefficient_4: float = Column(Float, nullable=False)
    score_coefficient_5: float = Column(Float, nullable=False)
    param_adjust_id: int = Column(Integer, nullable=False)
    param_adjust_interval: int = Column(Integer, nullable=False)


class ClanBattleSParamAdjust(DeclarativeBase, Base["ClanBattleSParamAdjust"]):
    __tablename__ = 'clan_battle_s_param_adjust'

    param_adjust_id: int = Column(Integer, primary_key=True)
    level: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)
    normal_atk_cast_time: int = Column(Integer, nullable=False)
    score_coefficient: int = Column(Integer, nullable=False)


class ClanBattleSchedule(DeclarativeBase, Base["ClanBattleSchedule"]):
    __tablename__ = 'clan_battle_schedule'

    clan_battle_id: int = Column(Integer, primary_key=True)
    release_month: int = Column(Integer, nullable=False)
    last_clan_battle_id: int = Column(Integer, nullable=False)
    point_per_stamina: int = Column(Integer, nullable=False)
    cost_group_id: int = Column(Integer, nullable=False)
    cost_group_id_s: int = Column(Integer, nullable=False)
    map_bgm: str = Column(Text, nullable=False)
    resource_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class ClanBattleTrainingDatum(DeclarativeBase, Base["ClanBattleTrainingDatum"]):
    __tablename__ = 'clan_battle_training_data'

    id: int = Column(Integer, primary_key=True)
    training_id: int = Column(Integer, nullable=False, index=True)
    mode: int = Column(Integer, nullable=False)
    phase: int = Column(Integer, nullable=False)
    map_data_id: int = Column(Integer, nullable=False)


class ClanBattleTrainingSchedule(DeclarativeBase, Base["ClanBattleTrainingSchedule"]):
    __tablename__ = 'clan_battle_training_schedule'

    training_id: int = Column(Integer, primary_key=True)
    clan_battle_id: int = Column(Integer, nullable=False, index=True)
    battle_start_time: str = Column(Text, nullable=False)
    battle_end_time: str = Column(Text, nullable=False)
    interval_start_time: str = Column(Text, nullable=False)
    interval_end_time: str = Column(Text, nullable=False)


class ClanCostGroup(DeclarativeBase, Base["ClanCostGroup"]):
    __tablename__ = 'clan_cost_group'

    id: int = Column(Integer, primary_key=True)
    cost_group_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    count: int = Column(Integer, nullable=False)
    cost: int = Column(Integer, nullable=False)


class ClanGrade(DeclarativeBase, Base["ClanGrade"]):
    __tablename__ = 'clan_grade'

    clan_grade_id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)


class ClanInviteLevelGroup(DeclarativeBase, Base["ClanInviteLevelGroup"]):
    __tablename__ = 'clan_invite_level_group'

    level_group_id: int = Column(Integer, primary_key=True)
    team_level_from: int = Column(Integer, nullable=False)
    team_level_to: int = Column(Integer, nullable=False)


class ClanprofileContent(DeclarativeBase, Base["ClanprofileContent"]):
    __tablename__ = 'clanprofile_content'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    disp_order: int = Column(Integer, nullable=False)


class CombinedResultMotion(DeclarativeBase, Base["CombinedResultMotion"]):
    __tablename__ = 'combined_result_motion'

    result_id: int = Column(Integer, primary_key=True)
    unit_id_1: int = Column(Integer, nullable=False)
    disp_order_1: int = Column(Integer, nullable=False)
    unit_id_2: int = Column(Integer, nullable=False)
    disp_order_2: int = Column(Integer, nullable=False)
    unit_id_3: int = Column(Integer, nullable=False)
    disp_order_3: int = Column(Integer, nullable=False)
    unit_id_4: int = Column(Integer, nullable=False)
    disp_order_4: int = Column(Integer, nullable=False)
    unit_id_5: int = Column(Integer, nullable=False)
    disp_order_5: int = Column(Integer, nullable=False)


class ContentMapDatum(DeclarativeBase, Base["ContentMapDatum"]):
    __tablename__ = 'content_map_data'

    content_map_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    map_type: int = Column(Integer, nullable=False)
    area_id: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    quest_position_x: int = Column(Integer, nullable=False)
    quest_position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class ContentReleaseDatum(DeclarativeBase, Base["ContentReleaseDatum"]):
    __tablename__ = 'content_release_data'

    system_id: int = Column(Integer, primary_key=True)
    team_level: int = Column(Integer, nullable=False)
    story_id: int = Column(Integer, nullable=False)
    quest_id: int = Column(Integer, nullable=False)
    dialog: str = Column(Text, nullable=False)


class CooperationQuestDatum(DeclarativeBase, Base["CooperationQuestDatum"]):
    __tablename__ = 'cooperation_quest_data'

    quest_id: int = Column(Integer, primary_key=True)
    quest_name: str = Column(Text, nullable=False)
    difficulty_level: int = Column(Integer, nullable=False)
    limit_team_level: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    exp: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    clear_reward_group_id: int = Column(Integer, nullable=False)
    odds_group_id: int = Column(Integer, nullable=False)
    lobby_background: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2: str = Column(Text, nullable=False)
    wave_bgm_que_id_2: str = Column(Text, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3: str = Column(Text, nullable=False)
    wave_bgm_que_id_3: str = Column(Text, nullable=False)
    enemy_image_1: int = Column(Integer, nullable=False)
    enemy_image_2: int = Column(Integer, nullable=False)
    enemy_image_3: int = Column(Integer, nullable=False)
    enemy_image_4: int = Column(Integer, nullable=False)
    enemy_image_5: int = Column(Integer, nullable=False)
    first_reward_image_1: int = Column(Integer, nullable=False)
    first_reward_image_2: int = Column(Integer, nullable=False)
    first_reward_image_3: int = Column(Integer, nullable=False)
    first_reward_image_4: int = Column(Integer, nullable=False)
    first_reward_image_5: int = Column(Integer, nullable=False)
    repeat_reward_image_1: int = Column(Integer, nullable=False)
    repeat_reward_image_2: int = Column(Integer, nullable=False)
    repeat_reward_image_3: int = Column(Integer, nullable=False)
    cooperation_quest_detail_bg_id: int = Column(Integer, nullable=False)
    cooperation_quest_detail_bg_position: int = Column(Integer, nullable=False)
    main_enemy_image_wave_1: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_1: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_2: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_3: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_1_4: int = Column(Integer, nullable=False)
    main_enemy_image_wave_2: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_1: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_2: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_3: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_2_4: int = Column(Integer, nullable=False)
    main_enemy_image_wave_3: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_1: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_2: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_3: int = Column(Integer, nullable=False)
    sub_enemy_image_wave_3_4: int = Column(Integer, nullable=False)
    quest_comment: str = Column(Text, nullable=False)
    unlock_quest_id_1: int = Column(Integer, nullable=False)
    unlock_quest_id_2: int = Column(Integer, nullable=False)


class CustomMypage(DeclarativeBase, Base["CustomMypage"]):
    __tablename__ = 'custom_mypage'

    still_id: int = Column(Integer, primary_key=True)
    group_id: int = Column(Integer, nullable=False)
    still_group_id: int = Column(Integer, nullable=False, index=True)
    still_name: str = Column(Text, nullable=False)
    vertical_still_flg: int = Column(Integer, nullable=False)
    scroll_direction: int = Column(Integer, nullable=False)
    mypage_type: int = Column(Integer, nullable=False)


class CustomMypageGroup(DeclarativeBase, Base["CustomMypageGroup"]):
    __tablename__ = 'custom_mypage_group'

    group_id: int = Column(Integer, primary_key=True)
    group_name: str = Column(Text, nullable=False)


class DailyMissionDatum(DeclarativeBase, Base["DailyMissionDatum"]):
    __tablename__ = 'daily_mission_data'

    daily_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    min_level: int = Column(Integer, nullable=False)
    max_level: int = Column(Integer, nullable=False)
    title_color_id: int = Column(Integer, nullable=False)
    visible_flag: int = Column(Integer, nullable=False)


class DearChara(DeclarativeBase, Base["DearChara"]):
    __tablename__ = 'dear_chara'

    event_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    chara_index: int = Column(Integer, primary_key=True, nullable=False)
    chara_name: str = Column(Text, nullable=False)
    max_dear_point: int = Column(Integer, nullable=False)
    reference_type: int = Column(Integer, nullable=False)
    reference_id: int = Column(Integer, nullable=False)
    episode_unlock_offset_x: int = Column(Integer, nullable=False)
    episode_unlock_offset_y: int = Column(Integer, nullable=False)
    dear_point_up_offset_x: int = Column(Integer, nullable=False)
    dear_point_up_offset_y: int = Column(Integer, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)


class DearReward(DeclarativeBase, Base["DearReward"]):
    __tablename__ = 'dear_reward'
    __table_args__ = (
        Index('dear_reward_0_event_id_1_chara_index', 'event_id', 'chara_index'),
    )

    id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    chara_index: int = Column(Integer, nullable=False)
    dear_point: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class DearSetting(DeclarativeBase, Base["DearSetting"]):
    __tablename__ = 'dear_setting'

    event_id: int = Column(Integer, primary_key=True)
    system_name: str = Column(Text, nullable=False)
    tutorial_quest_id: int = Column(Integer, nullable=False)
    tutorial_chara_index: int = Column(Integer, nullable=False)
    tutorial_story_id: int = Column(Integer, nullable=False)


class DearStoryDatum(DeclarativeBase, Base["DearStoryDatum"]):
    __tablename__ = 'dear_story_data'

    story_group_id: int = Column(Integer, primary_key=True)
    story_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    thumbnail_id: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class DearStoryDetail(DeclarativeBase, Base["DearStoryDetail"]):
    __tablename__ = 'dear_story_detail'
    __table_args__ = (
        Index('dear_story_detail_0_story_group_id_1_chara_index', 'story_group_id', 'chara_index'),
    )

    story_id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    visible_type: int = Column(Integer, nullable=False)
    story_end: int = Column(Integer, nullable=False)
    pre_story_id: int = Column(Integer, nullable=False)
    love_level: int = Column(Integer, nullable=False)
    requirement_id: int = Column(Integer, nullable=False)
    unlock_quest_id: int = Column(Integer, nullable=False)
    story_quest_id: int = Column(Integer, nullable=False)
    chara_index: int = Column(Integer, nullable=False)
    condition_event_quest_id: int = Column(Integer, nullable=False)
    condition_event_boss_id: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_value_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_value_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_value_3: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class DefineSpskill(DeclarativeBase, Base["DefineSpskill"]):
    __tablename__ = 'define_spskill'

    link_skill_slot: int = Column(Integer, primary_key=True)
    sp_skill_id: int = Column(Integer, nullable=False, index=True)
    base_skill_id: int = Column(Integer, nullable=False)
    skill_category: int = Column(Integer, nullable=False)


class DodgeTpRecovery(DeclarativeBase, Base["DodgeTpRecovery"]):
    __tablename__ = 'dodge_tp_recovery'

    system_id: int = Column(Integer, primary_key=True)
    recovery_ratio: float = Column(Float, nullable=False)


class DungeonArea(DeclarativeBase, Base["DungeonArea"]):
    __tablename__ = 'dungeon_area'

    dungeon_area_id: int = Column(Integer, primary_key=True)
    dungeon_type: int = Column(Integer, nullable=False)
    dungeon_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    open_area_id: int = Column(Integer, nullable=False)
    open_quest_id: int = Column(Integer, nullable=False)
    content_release_story: int = Column(Integer, nullable=False)
    initial_clear_story: int = Column(Integer, nullable=False)
    reward_group_id: int = Column(Integer, nullable=False)
    recommend_level: int = Column(Integer, nullable=False)
    quest_position_x: int = Column(Integer, nullable=False)
    quest_position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    recovery_hp_rate: int = Column(Integer, nullable=False)
    recovery_tp_rate: int = Column(Integer, nullable=False)


class DungeonAreaDatum(DeclarativeBase, Base["DungeonAreaDatum"]):
    __tablename__ = 'dungeon_area_data'

    dungeon_area_id: int = Column(Integer, primary_key=True)
    dungeon_type: int = Column(Integer, nullable=False)
    dungeon_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    open_quest_id: int = Column(Integer, nullable=False)
    content_release_story: int = Column(Integer, nullable=False)
    initial_clear_story: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    reward_group_id: int = Column(Integer, nullable=False)
    recommend_level: int = Column(Integer, nullable=False)
    quest_position_x: int = Column(Integer, nullable=False)
    quest_position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    coin_item_id: int = Column(Integer, nullable=False)
    enemy_image_1: int = Column(Integer, nullable=False)
    enemy_image_2: int = Column(Integer, nullable=False)
    enemy_image_3: int = Column(Integer, nullable=False)
    enemy_image_4: int = Column(Integer, nullable=False)
    enemy_image_5: int = Column(Integer, nullable=False)
    view_reward_id_1: int = Column(Integer, nullable=False)
    view_reward_id_2: int = Column(Integer, nullable=False)
    view_reward_id_3: int = Column(Integer, nullable=False)
    view_reward_id_4: int = Column(Integer, nullable=False)
    view_reward_id_5: int = Column(Integer, nullable=False)
    recovery_hp_rate: int = Column(Integer, nullable=False)
    recovery_tp_rate: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class DungeonQuestDatum(DeclarativeBase, Base["DungeonQuestDatum"]):
    __tablename__ = 'dungeon_quest_data'
    __table_args__ = (
        Index('dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num', unique=True),
    )

    quest_id: int = Column(Integer, primary_key=True)
    dungeon_area_id: int = Column(Integer, nullable=False, index=True)
    floor_num: int = Column(Integer, nullable=False)
    quest_type: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    matching_coefficient: float = Column(Float, nullable=False)
    parts_hp_save_flag: int = Column(Integer, nullable=False)
    energy_reset_flag: int = Column(Integer, nullable=False)
    emax: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_image_6: int = Column(Integer, nullable=False)
    reward_coin: int = Column(Integer, nullable=False)
    chest_id: int = Column(Integer, nullable=False)
    odds_group_id: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_id: int = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: int = Column(Integer, nullable=False)
    dungeon_quest_detail_monster_size: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_1: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_2: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_height: float = Column(Float, nullable=False)
    multi_target_effect_time: float = Column(Float, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)


class DungeonSkipDatum(DeclarativeBase, Base["DungeonSkipDatum"]):
    __tablename__ = 'dungeon_skip_data'

    area_id: int = Column(Integer, primary_key=True)
    skip_motion_id: int = Column(Integer, nullable=False)
    skip_bg_id: int = Column(Integer, nullable=False)
    skip_position_x: int = Column(Integer, nullable=False)
    skip_position_y: int = Column(Integer, nullable=False)
    skip_scale_x: float = Column(Float, nullable=False)
    skip_scale_y: float = Column(Float, nullable=False)


class DungeonSpecialBattle(DeclarativeBase, Base["DungeonSpecialBattle"]):
    __tablename__ = 'dungeon_special_battle'
    __table_args__ = (
        Index('dungeon_special_battle_0_quest_id_1_mode', 'quest_id', 'mode', unique=True),
    )

    special_battle_id: int = Column(Integer, primary_key=True)
    quest_id: int = Column(Integer, nullable=False, index=True)
    mode: int = Column(Integer, nullable=False)
    purpose_type: int = Column(Integer, nullable=False)
    parts_hp_save_flag: int = Column(Integer, nullable=False)
    trigger_hp: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    action_start_second: float = Column(Float, nullable=False)
    hp_gauge_color_flag: int = Column(Integer, nullable=False)
    start_idle_trigger: int = Column(Integer, nullable=False)
    appear_time: float = Column(Float, nullable=False)
    detail_boss_bg_size: float = Column(Float, nullable=False)
    detail_boss_bg_height: float = Column(Float, nullable=False)
    detail_boss_motion: str = Column(Text, nullable=False)


class DungeonSpecialEnemySetting(DeclarativeBase, Base["DungeonSpecialEnemySetting"]):
    __tablename__ = 'dungeon_special_enemy_setting'
    __table_args__ = (
        UniqueConstraint('special_battle_id', 'disp_order'),
        Index('dungeon_special_enemy_setting_0_special_battle_id_1_enemy_identify', 'special_battle_id', 'enemy_identify', unique=True)
    )

    id: int = Column(Integer, primary_key=True)
    special_battle_id: int = Column(Integer, nullable=False, index=True)
    enemy_identify: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    must_kill_flag: int = Column(Integer, nullable=False)
    detail_offset_x: float = Column(Float, nullable=False)
    detail_offset_y: float = Column(Float, nullable=False)
    detail_scale: float = Column(Float, nullable=False)


class EReduction(DeclarativeBase, Base["EReduction"]):
    __tablename__ = 'e_reduction'

    id: int = Column(Integer, primary_key=True)
    border: int = Column(Integer, nullable=False)
    threshold_1: int = Column(Integer, nullable=False)
    value_1: float = Column(Float, nullable=False)
    threshold_2: int = Column(Integer, nullable=False)
    value_2: float = Column(Float, nullable=False)
    threshold_3: int = Column(Integer, nullable=False)
    value_3: float = Column(Float, nullable=False)
    threshold_4: int = Column(Integer, nullable=False)
    value_4: float = Column(Float, nullable=False)
    threshold_5: int = Column(Integer, nullable=False)
    value_5: float = Column(Float, nullable=False)


class EmblemDatum(DeclarativeBase, Base["EmblemDatum"]):
    __tablename__ = 'emblem_data'

    emblem_id: int = Column(Integer, primary_key=True)
    disp_oder: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    emblem_name: str = Column(Text, nullable=False)
    description_mission_id: int = Column(Integer, nullable=False)
    event_emblem: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class EmblemMissionDatum(DeclarativeBase, Base["EmblemMissionDatum"]):
    __tablename__ = 'emblem_mission_data'

    mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer, nullable=False)
    condition_value_2: int = Column(Integer, nullable=False)
    condition_value_3: int = Column(Integer, nullable=False)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer, nullable=False)
    visible_flag: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class EmblemMissionRewardDatum(DeclarativeBase, Base["EmblemMissionRewardDatum"]):
    __tablename__ = 'emblem_mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False, index=True)
    reward_num: int = Column(Integer, nullable=False)
    icon_type: int = Column(Integer, nullable=False)


class EnemyEnableVoice(DeclarativeBase, Base["EnemyEnableVoice"]):
    __tablename__ = 'enemy_enable_voice'

    unit_id: int = Column(Integer, primary_key=True)
    voice_id: int = Column(Integer, nullable=False)


class EnemyIgnoreSkillRf(DeclarativeBase, Base["EnemyIgnoreSkillRf"]):
    __tablename__ = 'enemy_ignore_skill_rf'

    enemy_id: int = Column(Integer, primary_key=True)


class EnemyMPart(DeclarativeBase, Base["EnemyMPart"]):
    __tablename__ = 'enemy_m_parts'

    enemy_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    child_enemy_parameter_1: int = Column(Integer, nullable=False)
    child_enemy_parameter_2: int = Column(Integer, nullable=False)
    child_enemy_parameter_3: int = Column(Integer, nullable=False)
    child_enemy_parameter_4: int = Column(Integer, nullable=False)
    child_enemy_parameter_5: int = Column(Integer, nullable=False)


class EnemyParameter(DeclarativeBase, Base["EnemyParameter"]):
    __tablename__ = 'enemy_parameter'

    enemy_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)
    level: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    wave_hp_recovery: int = Column(Integer, nullable=False)
    wave_energy_recovery: int = Column(Integer, nullable=False)
    dodge: int = Column(Integer, nullable=False)
    physical_penetrate: int = Column(Integer, nullable=False)
    magic_penetrate: int = Column(Integer, nullable=False)
    life_steal: int = Column(Integer, nullable=False)
    hp_recovery_rate: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    energy_reduce_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    ex_skill_lv_1: int = Column(Integer, nullable=False)
    ex_skill_lv_2: int = Column(Integer, nullable=False)
    ex_skill_lv_3: int = Column(Integer, nullable=False)
    ex_skill_lv_4: int = Column(Integer, nullable=False)
    ex_skill_lv_5: int = Column(Integer, nullable=False)
    resist_status_id: int = Column(Integer, nullable=False)
    resist_variation_id: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)
    unique_equipment_flag_1: int = Column(Integer, nullable=False)
    break_durability: int = Column(Integer, nullable=False)
    virtual_hp: int = Column(Integer, nullable=False)

class Reward:
    def __init__(self, reward_type: int, reward_id: int, reward_num: int, odds: int):
        self.reward_item: ItemType = (eInventoryType(reward_type), reward_id)
        self.reward_num = reward_num
        self.odds = odds

class EnemyRewardDatum(DeclarativeBase, Base["EnemyRewardDatum"]):
    __tablename__ = 'enemy_reward_data'

    drop_reward_id: int = Column(Integer, primary_key=True)
    drop_count: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    odds_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    odds_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    odds_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    odds_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    odds_5: int = Column(Integer, nullable=False)

    def get_rewards(self) -> Iterator[Reward]:
        yield Reward(self.reward_type_1, self.reward_id_1, self.reward_num_1, self.odds_1)
        yield Reward(self.reward_type_2, self.reward_id_2, self.reward_num_2, self.odds_2)
        yield Reward(self.reward_type_3, self.reward_id_3, self.reward_num_3, self.odds_3)
        yield Reward(self.reward_type_4, self.reward_id_4, self.reward_num_4, self.odds_4)
        yield Reward(self.reward_type_5, self.reward_id_5, self.reward_num_5, self.odds_5)


class EquipmentCraft(DeclarativeBase, Base["EquipmentCraft"]):
    __tablename__ = 'equipment_craft'

    equipment_id: int = Column(Integer, primary_key=True)
    crafted_cost: int = Column(Integer, nullable=False)
    condition_equipment_id_1: int = Column(Integer, nullable=False)
    consume_num_1: int = Column(Integer, nullable=False)
    condition_equipment_id_2: int = Column(Integer, nullable=False)
    consume_num_2: int = Column(Integer, nullable=False)
    condition_equipment_id_3: int = Column(Integer, nullable=False)
    consume_num_3: int = Column(Integer, nullable=False)
    condition_equipment_id_4: int = Column(Integer, nullable=False)
    consume_num_4: int = Column(Integer, nullable=False)
    condition_equipment_id_5: int = Column(Integer, nullable=False)
    consume_num_5: int = Column(Integer, nullable=False)
    condition_equipment_id_6: int = Column(Integer, nullable=False)
    consume_num_6: int = Column(Integer, nullable=False)
    condition_equipment_id_7: int = Column(Integer, nullable=False)
    consume_num_7: int = Column(Integer, nullable=False)
    condition_equipment_id_8: int = Column(Integer, nullable=False)
    consume_num_8: int = Column(Integer, nullable=False)
    condition_equipment_id_9: int = Column(Integer, nullable=False)
    consume_num_9: int = Column(Integer, nullable=False)
    condition_equipment_id_10: int = Column(Integer, nullable=False)
    consume_num_10: int = Column(Integer, nullable=False)

    def get_materials(self) -> Iterator[Tuple[ItemType, int]]:
        yield ((eInventoryType.Equip, self.condition_equipment_id_1), self.consume_num_1)
        yield ((eInventoryType.Equip, self.condition_equipment_id_2), self.consume_num_2)
        yield ((eInventoryType.Equip, self.condition_equipment_id_3), self.consume_num_3)
        yield ((eInventoryType.Equip, self.condition_equipment_id_4), self.consume_num_4)
        yield ((eInventoryType.Equip, self.condition_equipment_id_5), self.consume_num_5)
        yield ((eInventoryType.Equip, self.condition_equipment_id_6), self.consume_num_6)
        yield ((eInventoryType.Equip, self.condition_equipment_id_7), self.consume_num_7)
        yield ((eInventoryType.Equip, self.condition_equipment_id_8), self.consume_num_8)
        yield ((eInventoryType.Equip, self.condition_equipment_id_9), self.consume_num_9)
        yield ((eInventoryType.Equip, self.condition_equipment_id_10), self.consume_num_10)


class EquipmentDatum(DeclarativeBase, Base["EquipmentDatum"]):
    __tablename__ = 'equipment_data'

    equipment_id: int = Column(Integer, primary_key=True)
    equipment_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    craft_flg: int = Column(Integer, nullable=False)
    equipment_enhance_point: int = Column(Integer, nullable=False)
    sale_price: int = Column(Integer, nullable=False)
    require_level: int = Column(Integer, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    enable_donation: int = Column(Integer, nullable=False)
    accuracy: float = Column(Float, nullable=False)
    display_item: int = Column(Integer, nullable=False)
    item_type: int = Column(Integer, nullable=False)


class EquipmentDonation(DeclarativeBase, Base["EquipmentDonation"]):
    __tablename__ = 'equipment_donation'

    team_level: int = Column(Integer, primary_key=True)
    donation_num_once: int = Column(Integer, nullable=False)
    donation_num_daily: int = Column(Integer, nullable=False)
    request_num_once: int = Column(Integer, nullable=False)


class EquipmentEnhanceDatum(DeclarativeBase, Base["EquipmentEnhanceDatum"]):
    __tablename__ = 'equipment_enhance_data'

    promotion_level: int = Column(Integer, primary_key=True, nullable=False)
    equipment_enhance_level: int = Column(Integer, primary_key=True, nullable=False)
    needed_point: int = Column(Integer, nullable=False)
    total_point: int = Column(Integer, nullable=False)


class EquipmentEnhanceRate(DeclarativeBase, Base["EquipmentEnhanceRate"]):
    __tablename__ = 'equipment_enhance_rate'

    equipment_id: int = Column(Integer, primary_key=True)
    equipment_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class EventBgDatum(DeclarativeBase, Base["EventBgDatum"]):
    __tablename__ = 'event_bg_data'

    event_id: int = Column(Integer, primary_key=True)
    bg_id: int = Column(Integer, nullable=False)
    start_date: str = Column(Text, nullable=False)
    end_date: str = Column(Text, nullable=False)


class EventBossTreasureBox(DeclarativeBase, Base["EventBossTreasureBox"]):
    __tablename__ = 'event_boss_treasure_box'

    event_boss_treasure_box_id: int = Column(Integer, primary_key=True)
    treasure_type_1: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_1: int = Column(Integer, nullable=False)
    each_odds_1: int = Column(Integer, nullable=False)
    treasure_type_2: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_2: int = Column(Integer, nullable=False)
    each_odds_2: int = Column(Integer, nullable=False)
    treasure_type_3: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_3: int = Column(Integer, nullable=False)
    each_odds_3: int = Column(Integer, nullable=False)
    treasure_type_4: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_4: int = Column(Integer, nullable=False)
    each_odds_4: int = Column(Integer, nullable=False)
    treasure_type_5: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_5: int = Column(Integer, nullable=False)
    each_odds_5: int = Column(Integer, nullable=False)
    treasure_type_6: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_6: int = Column(Integer, nullable=False)
    each_odds_6: int = Column(Integer, nullable=False)
    treasure_type_7: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_7: int = Column(Integer, nullable=False)
    each_odds_7: int = Column(Integer, nullable=False)
    treasure_type_8: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_8: int = Column(Integer, nullable=False)
    each_odds_8: int = Column(Integer, nullable=False)
    treasure_type_9: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_9: int = Column(Integer, nullable=False)
    each_odds_9: int = Column(Integer, nullable=False)
    treasure_type_10: int = Column(Integer, nullable=False)
    event_boss_treasure_content_id_10: int = Column(Integer, nullable=False)
    each_odds_10: int = Column(Integer, nullable=False)


class EventBossTreasureContent(DeclarativeBase, Base["EventBossTreasureContent"]):
    __tablename__ = 'event_boss_treasure_content'

    event_boss_treasure_content_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    odds_file_1: str = Column(Text, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    odds_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    odds_file_2: str = Column(Text, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    odds_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    odds_file_3: str = Column(Text, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    odds_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    odds_file_4: str = Column(Text, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    odds_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    odds_file_5: str = Column(Text, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    odds_5: int = Column(Integer, nullable=False)


class EventEffectSetting(DeclarativeBase, Base["EventEffectSetting"]):
    __tablename__ = 'event_effect_setting'

    event_id: int = Column(Integer, primary_key=True, nullable=False)
    type: int = Column(Integer, primary_key=True, nullable=False)
    value: int = Column(Integer, nullable=False)


class EventEnemyParameter(DeclarativeBase, Base["EventEnemyParameter"]):
    __tablename__ = 'event_enemy_parameter'

    enemy_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    level: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    wave_hp_recovery: int = Column(Integer, nullable=False)
    wave_energy_recovery: int = Column(Integer, nullable=False)
    dodge: int = Column(Integer, nullable=False)
    physical_penetrate: int = Column(Integer, nullable=False)
    magic_penetrate: int = Column(Integer, nullable=False)
    life_steal: int = Column(Integer, nullable=False)
    hp_recovery_rate: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    energy_reduce_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    ex_skill_lv_1: int = Column(Integer, nullable=False)
    ex_skill_lv_2: int = Column(Integer, nullable=False)
    ex_skill_lv_3: int = Column(Integer, nullable=False)
    ex_skill_lv_4: int = Column(Integer, nullable=False)
    ex_skill_lv_5: int = Column(Integer, nullable=False)
    resist_status_id: int = Column(Integer, nullable=False)
    resist_variation_id: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)


class EventEnemyRewardGroup(DeclarativeBase, Base["EventEnemyRewardGroup"]):
    __tablename__ = 'event_enemy_reward_group'

    id: int = Column(Integer, primary_key=True)
    reward_group_id: int = Column(Integer, nullable=False)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_num: int = Column(Integer, nullable=False)
    odds: int = Column(Integer, nullable=False)


class EventGachaDatum(DeclarativeBase, Base["EventGachaDatum"]):
    __tablename__ = 'event_gacha_data'

    gacha_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    gacha_name: str = Column(Text, nullable=False)
    item_type: int = Column(Integer, nullable=False)
    item_id: int = Column(Integer, nullable=False)
    cost: int = Column(Integer, nullable=False)
    repeat_step: int = Column(Integer, nullable=False)


class EventIntroduction(DeclarativeBase, Base["EventIntroduction"]):
    __tablename__ = 'event_introduction'

    id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    introduction_number: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    maximum_chunk_size_1: int = Column(Integer, nullable=False)
    maximum_chunk_size_loop_1: int = Column(Integer, nullable=False)
    maximum_chunk_size_2: int = Column(Integer, nullable=False)
    maximum_chunk_size_loop_2: int = Column(Integer, nullable=False)
    maximum_chunk_size_3: int = Column(Integer, nullable=False)
    maximum_chunk_size_loop_3: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)


class EventNaviComment(DeclarativeBase, Base["EventNaviComment"]):
    __tablename__ = 'event_navi_comment'

    comment_id: int = Column(Integer, primary_key=True)
    where_type: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    face_type: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    description: str = Column(Text)
    voice_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    pos_x: float = Column(Float, nullable=False)
    pos_y: float = Column(Float, nullable=False)
    change_face_time: float = Column(Float, nullable=False)
    change_face_type: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class EventNaviCommentCondition(DeclarativeBase, Base["EventNaviCommentCondition"]):
    __tablename__ = 'event_navi_comment_condition'

    comment_id: int = Column(Integer, primary_key=True)
    condition_type_1: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer, nullable=False)
    condition_type_2: int = Column(Integer, nullable=False)
    condition_value_2: int = Column(Integer, nullable=False)
    condition_type_3: int = Column(Integer, nullable=False)
    condition_value_3: int = Column(Integer, nullable=False)


class EventReminder(DeclarativeBase, Base["EventReminder"]):
    __tablename__ = 'event_reminder'

    reminder_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    title_text: str = Column(Text, nullable=False)
    description_text: str = Column(Text, nullable=False)
    notice_text: str = Column(Text, nullable=False)
    thumbnail_id: int = Column(Integer, nullable=False)
    btn_text: str = Column(Text, nullable=False)
    target_type: int = Column(Integer, nullable=False)
    target_id: int = Column(Integer, nullable=False)


class EventReminderCondition(DeclarativeBase, Base["EventReminderCondition"]):
    __tablename__ = 'event_reminder_condition'

    id: int = Column(Integer, primary_key=True)
    reminder_id: int = Column(Integer, nullable=False, index=True)
    condition_type: int = Column(Integer, nullable=False)
    condition_id: int = Column(Integer, nullable=False)


class EventRevivalSeriesWaveGroupDatum(DeclarativeBase, Base["EventRevivalSeriesWaveGroupDatum"]):
    __tablename__ = 'event_revival_series_wave_group_data'

    id: int = Column(Integer, primary_key=True)
    wave_group_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    wave: int = Column(Integer, nullable=False)
    match_lv_min: int = Column(Integer, nullable=False)
    match_lv_max: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)
    drop_gold_1: int = Column(Integer, nullable=False)
    reward_group_id_1: int = Column(Integer, nullable=False)
    disp_reward_type_1: int = Column(Integer, nullable=False)
    disp_reward_id_1: int = Column(Integer, nullable=False)
    reward_lot_count_1: int = Column(Integer, nullable=False)
    reward_odds_1: int = Column(Integer, nullable=False)
    drop_gold_2: int = Column(Integer, nullable=False)
    reward_group_id_2: int = Column(Integer, nullable=False)
    disp_reward_type_2: int = Column(Integer, nullable=False)
    disp_reward_id_2: int = Column(Integer, nullable=False)
    reward_lot_count_2: int = Column(Integer, nullable=False)
    reward_odds_2: int = Column(Integer, nullable=False)
    drop_gold_3: int = Column(Integer, nullable=False)
    reward_group_id_3: int = Column(Integer, nullable=False)
    disp_reward_type_3: int = Column(Integer, nullable=False)
    disp_reward_id_3: int = Column(Integer, nullable=False)
    reward_lot_count_3: int = Column(Integer, nullable=False)
    reward_odds_3: int = Column(Integer, nullable=False)
    drop_gold_4: int = Column(Integer, nullable=False)
    reward_group_id_4: int = Column(Integer, nullable=False)
    disp_reward_type_4: int = Column(Integer, nullable=False)
    disp_reward_id_4: int = Column(Integer, nullable=False)
    reward_lot_count_4: int = Column(Integer, nullable=False)
    reward_odds_4: int = Column(Integer, nullable=False)
    drop_gold_5: int = Column(Integer, nullable=False)
    reward_group_id_5: int = Column(Integer, nullable=False)
    disp_reward_type_5: int = Column(Integer, nullable=False)
    disp_reward_id_5: int = Column(Integer, nullable=False)
    reward_lot_count_5: int = Column(Integer, nullable=False)
    reward_odds_5: int = Column(Integer, nullable=False)


class EventRevivalWaveGroupDatum(DeclarativeBase, Base["EventRevivalWaveGroupDatum"]):
    __tablename__ = 'event_revival_wave_group_data'

    id: int = Column(Integer, primary_key=True)
    wave_group_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    wave: int = Column(Integer, nullable=False)
    match_lv_min: int = Column(Integer, nullable=False)
    match_lv_max: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)
    drop_gold_1: int = Column(Integer, nullable=False)
    reward_group_id_1: int = Column(Integer, nullable=False)
    disp_reward_type_1: int = Column(Integer, nullable=False)
    disp_reward_id_1: int = Column(Integer, nullable=False)
    reward_lot_count_1: int = Column(Integer, nullable=False)
    reward_odds_1: int = Column(Integer, nullable=False)
    drop_gold_2: int = Column(Integer, nullable=False)
    reward_group_id_2: int = Column(Integer, nullable=False)
    disp_reward_type_2: int = Column(Integer, nullable=False)
    disp_reward_id_2: int = Column(Integer, nullable=False)
    reward_lot_count_2: int = Column(Integer, nullable=False)
    reward_odds_2: int = Column(Integer, nullable=False)
    drop_gold_3: int = Column(Integer, nullable=False)
    reward_group_id_3: int = Column(Integer, nullable=False)
    disp_reward_type_3: int = Column(Integer, nullable=False)
    disp_reward_id_3: int = Column(Integer, nullable=False)
    reward_lot_count_3: int = Column(Integer, nullable=False)
    reward_odds_3: int = Column(Integer, nullable=False)
    drop_gold_4: int = Column(Integer, nullable=False)
    reward_group_id_4: int = Column(Integer, nullable=False)
    disp_reward_type_4: int = Column(Integer, nullable=False)
    disp_reward_id_4: int = Column(Integer, nullable=False)
    reward_lot_count_4: int = Column(Integer, nullable=False)
    reward_odds_4: int = Column(Integer, nullable=False)
    drop_gold_5: int = Column(Integer, nullable=False)
    reward_group_id_5: int = Column(Integer, nullable=False)
    disp_reward_type_5: int = Column(Integer, nullable=False)
    disp_reward_id_5: int = Column(Integer, nullable=False)
    reward_lot_count_5: int = Column(Integer, nullable=False)
    reward_odds_5: int = Column(Integer, nullable=False)


class EventSeriesWaveGroupDatum(DeclarativeBase, Base["EventSeriesWaveGroupDatum"]):
    __tablename__ = 'event_series_wave_group_data'

    id: int = Column(Integer, primary_key=True)
    wave_group_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    wave: int = Column(Integer, nullable=False)
    match_lv_min: int = Column(Integer, nullable=False)
    match_lv_max: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)
    drop_gold_1: int = Column(Integer, nullable=False)
    reward_group_id_1: int = Column(Integer, nullable=False)
    disp_reward_type_1: int = Column(Integer, nullable=False)
    disp_reward_id_1: int = Column(Integer, nullable=False)
    reward_lot_count_1: int = Column(Integer, nullable=False)
    reward_odds_1: int = Column(Integer, nullable=False)
    drop_gold_2: int = Column(Integer, nullable=False)
    reward_group_id_2: int = Column(Integer, nullable=False)
    disp_reward_type_2: int = Column(Integer, nullable=False)
    disp_reward_id_2: int = Column(Integer, nullable=False)
    reward_lot_count_2: int = Column(Integer, nullable=False)
    reward_odds_2: int = Column(Integer, nullable=False)
    drop_gold_3: int = Column(Integer, nullable=False)
    reward_group_id_3: int = Column(Integer, nullable=False)
    disp_reward_type_3: int = Column(Integer, nullable=False)
    disp_reward_id_3: int = Column(Integer, nullable=False)
    reward_lot_count_3: int = Column(Integer, nullable=False)
    reward_odds_3: int = Column(Integer, nullable=False)
    drop_gold_4: int = Column(Integer, nullable=False)
    reward_group_id_4: int = Column(Integer, nullable=False)
    disp_reward_type_4: int = Column(Integer, nullable=False)
    disp_reward_id_4: int = Column(Integer, nullable=False)
    reward_lot_count_4: int = Column(Integer, nullable=False)
    reward_odds_4: int = Column(Integer, nullable=False)
    drop_gold_5: int = Column(Integer, nullable=False)
    reward_group_id_5: int = Column(Integer, nullable=False)
    disp_reward_type_5: int = Column(Integer, nullable=False)
    disp_reward_id_5: int = Column(Integer, nullable=False)
    reward_lot_count_5: int = Column(Integer, nullable=False)
    reward_odds_5: int = Column(Integer, nullable=False)


class EventStoryDatum(DeclarativeBase, Base["EventStoryDatum"]):
    __tablename__ = 'event_story_data'

    story_group_id: int = Column(Integer, primary_key=True)
    story_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    thumbnail_id: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class EventStoryDetail(DeclarativeBase, Base["EventStoryDetail"]):
    __tablename__ = 'event_story_detail'

    story_id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    visible_type: int = Column(Integer, nullable=False)
    story_end: int = Column(Integer, nullable=False)
    pre_story_id: int = Column(Integer, nullable=False)
    love_level: int = Column(Integer, nullable=False)
    requirement_id: int = Column(Integer, nullable=False)
    unlock_quest_id: int = Column(Integer, nullable=False)
    story_quest_id: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_value_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_value_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_value_3: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class EventTopAdv(DeclarativeBase, Base["EventTopAdv"]):
    __tablename__ = 'event_top_adv'
    __table_args__ = (
        Index('event_top_adv_0_event_id_1_type', 'event_id', 'type'),
    )

    event_top_adv_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    value_1: int = Column(Integer, nullable=False)
    value_2: int = Column(Integer, nullable=False)
    value_3: int = Column(Integer, nullable=False)
    story_id: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    condition_type: int = Column(Integer, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class EventWaveGroupDatum(DeclarativeBase, Base["EventWaveGroupDatum"]):
    __tablename__ = 'event_wave_group_data'

    id: int = Column(Integer, primary_key=True)
    wave_group_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    wave: int = Column(Integer, nullable=False)
    match_lv_min: int = Column(Integer, nullable=False)
    match_lv_max: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)
    drop_gold_1: int = Column(Integer, nullable=False)
    reward_group_id_1: int = Column(Integer, nullable=False)
    disp_reward_type_1: int = Column(Integer, nullable=False)
    disp_reward_id_1: int = Column(Integer, nullable=False)
    reward_lot_count_1: int = Column(Integer, nullable=False)
    reward_odds_1: int = Column(Integer, nullable=False)
    drop_gold_2: int = Column(Integer, nullable=False)
    reward_group_id_2: int = Column(Integer, nullable=False)
    disp_reward_type_2: int = Column(Integer, nullable=False)
    disp_reward_id_2: int = Column(Integer, nullable=False)
    reward_lot_count_2: int = Column(Integer, nullable=False)
    reward_odds_2: int = Column(Integer, nullable=False)
    drop_gold_3: int = Column(Integer, nullable=False)
    reward_group_id_3: int = Column(Integer, nullable=False)
    disp_reward_type_3: int = Column(Integer, nullable=False)
    disp_reward_id_3: int = Column(Integer, nullable=False)
    reward_lot_count_3: int = Column(Integer, nullable=False)
    reward_odds_3: int = Column(Integer, nullable=False)
    drop_gold_4: int = Column(Integer, nullable=False)
    reward_group_id_4: int = Column(Integer, nullable=False)
    disp_reward_type_4: int = Column(Integer, nullable=False)
    disp_reward_id_4: int = Column(Integer, nullable=False)
    reward_lot_count_4: int = Column(Integer, nullable=False)
    reward_odds_4: int = Column(Integer, nullable=False)
    drop_gold_5: int = Column(Integer, nullable=False)
    reward_group_id_5: int = Column(Integer, nullable=False)
    disp_reward_type_5: int = Column(Integer, nullable=False)
    disp_reward_id_5: int = Column(Integer, nullable=False)
    reward_lot_count_5: int = Column(Integer, nullable=False)
    reward_odds_5: int = Column(Integer, nullable=False)


class ExceedLevelStage(DeclarativeBase, Base["ExceedLevelStage"]):
    __tablename__ = 'exceed_level_stage'

    exceed_stage: int = Column(Integer, primary_key=True)
    increase_level_limit: int = Column(Integer, nullable=False)
    unlock_quest_id: int = Column(Integer, nullable=False)
    unlock_team_level: int = Column(Integer, nullable=False)
    general_exceed_item_id: int = Column(Integer, nullable=False)


class ExceedLevelUnit(DeclarativeBase, Base["ExceedLevelUnit"]):
    __tablename__ = 'exceed_level_unit'

    id: int = Column(Integer, nullable=False)
    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    exceed_stage: int = Column(Integer, primary_key=True, nullable=False)
    exceed_item_id: int = Column(Integer, nullable=False)
    item_id_1: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    consume_num_1: int = Column(Integer, nullable=False)
    item_id_2: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    consume_num_2: int = Column(Integer, nullable=False)
    item_id_3: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    consume_num_3: int = Column(Integer, nullable=False)
    item_id_4: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    consume_num_4: int = Column(Integer, nullable=False)
    item_id_5: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    consume_num_5: int = Column(Integer, nullable=False)


class ExceptEr(DeclarativeBase, Base["ExceptEr"]):
    __tablename__ = 'except_er'

    category_id: int = Column(Integer, primary_key=True)


class ExperienceTeam(DeclarativeBase, Base["ExperienceTeam"]):
    __tablename__ = 'experience_team'

    team_level: int = Column(Integer, primary_key=True)
    total_exp: int = Column(Integer, nullable=False)
    max_stamina: int = Column(Integer, nullable=False)
    over_limit_stamina: int = Column(Integer, nullable=False)
    recover_stamina_count: int = Column(Integer, nullable=False)


class ExperienceUnit(DeclarativeBase, Base["ExperienceUnit"]):
    __tablename__ = 'experience_unit'

    unit_level: int = Column(Integer, primary_key=True)
    total_exp: int = Column(Integer, nullable=False)


class FixLineupGroupSet(DeclarativeBase, Base["FixLineupGroupSet"]):
    __tablename__ = 'fix_lineup_group_set'
    __table_args__ = (
        Index('fix_lineup_group_set_0_team_level_from_1_team_level_to', 'team_level_from', 'team_level_to'),
    )

    lineup_group_set_id: int = Column(Integer, primary_key=True, nullable=False)
    team_level_from: int = Column(Integer, primary_key=True, nullable=False)
    team_level_to: int = Column(Integer, primary_key=True, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    price_type_1: int = Column(Integer, nullable=False)
    currency_id_1: int = Column(Integer, nullable=False)
    price_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    price_type_2: int = Column(Integer, nullable=False)
    currency_id_2: int = Column(Integer, nullable=False)
    price_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    price_type_3: int = Column(Integer, nullable=False)
    currency_id_3: int = Column(Integer, nullable=False)
    price_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    price_type_4: int = Column(Integer, nullable=False)
    currency_id_4: int = Column(Integer, nullable=False)
    price_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)
    price_type_5: int = Column(Integer, nullable=False)
    currency_id_5: int = Column(Integer, nullable=False)
    price_5: int = Column(Integer, nullable=False)
    reward_type_6: int = Column(Integer, nullable=False)
    reward_id_6: int = Column(Integer, nullable=False)
    reward_count_6: int = Column(Integer, nullable=False)
    price_type_6: int = Column(Integer, nullable=False)
    currency_id_6: int = Column(Integer, nullable=False)
    price_6: int = Column(Integer, nullable=False)
    reward_type_7: int = Column(Integer, nullable=False)
    reward_id_7: int = Column(Integer, nullable=False)
    reward_count_7: int = Column(Integer, nullable=False)
    price_type_7: int = Column(Integer, nullable=False)
    currency_id_7: int = Column(Integer, nullable=False)
    price_7: int = Column(Integer, nullable=False)
    reward_type_8: int = Column(Integer, nullable=False)
    reward_id_8: int = Column(Integer, nullable=False)
    reward_count_8: int = Column(Integer, nullable=False)
    price_type_8: int = Column(Integer, nullable=False)
    currency_id_8: int = Column(Integer, nullable=False)
    price_8: int = Column(Integer, nullable=False)
    reward_type_9: int = Column(Integer, nullable=False)
    reward_id_9: int = Column(Integer, nullable=False)
    reward_count_9: int = Column(Integer, nullable=False)
    price_type_9: int = Column(Integer, nullable=False)
    currency_id_9: int = Column(Integer, nullable=False)
    price_9: int = Column(Integer, nullable=False)
    reward_type_10: int = Column(Integer, nullable=False)
    reward_id_10: int = Column(Integer, nullable=False)
    reward_count_10: int = Column(Integer, nullable=False)
    price_type_10: int = Column(Integer, nullable=False)
    currency_id_10: int = Column(Integer, nullable=False)
    price_10: int = Column(Integer, nullable=False)
    reward_type_11: int = Column(Integer, nullable=False)
    reward_id_11: int = Column(Integer, nullable=False)
    reward_count_11: int = Column(Integer, nullable=False)
    price_type_11: int = Column(Integer, nullable=False)
    currency_id_11: int = Column(Integer, nullable=False)
    price_11: int = Column(Integer, nullable=False)
    reward_type_12: int = Column(Integer, nullable=False)
    reward_id_12: int = Column(Integer, nullable=False)
    reward_count_12: int = Column(Integer, nullable=False)
    price_type_12: int = Column(Integer, nullable=False)
    currency_id_12: int = Column(Integer, nullable=False)
    price_12: int = Column(Integer, nullable=False)
    reward_type_13: int = Column(Integer, nullable=False)
    reward_id_13: int = Column(Integer, nullable=False)
    reward_count_13: int = Column(Integer, nullable=False)
    price_type_13: int = Column(Integer, nullable=False)
    currency_id_13: int = Column(Integer, nullable=False)
    price_13: int = Column(Integer, nullable=False)
    reward_type_14: int = Column(Integer, nullable=False)
    reward_id_14: int = Column(Integer, nullable=False)
    reward_count_14: int = Column(Integer, nullable=False)
    price_type_14: int = Column(Integer, nullable=False)
    currency_id_14: int = Column(Integer, nullable=False)
    price_14: int = Column(Integer, nullable=False)
    reward_type_15: int = Column(Integer, nullable=False)
    reward_id_15: int = Column(Integer, nullable=False)
    reward_count_15: int = Column(Integer, nullable=False)
    price_type_15: int = Column(Integer, nullable=False)
    currency_id_15: int = Column(Integer, nullable=False)
    price_15: int = Column(Integer, nullable=False)
    reward_type_16: int = Column(Integer, nullable=False)
    reward_id_16: int = Column(Integer, nullable=False)
    reward_count_16: int = Column(Integer, nullable=False)
    price_type_16: int = Column(Integer, nullable=False)
    currency_id_16: int = Column(Integer, nullable=False)
    price_16: int = Column(Integer, nullable=False)
    reward_type_17: int = Column(Integer, nullable=False)
    reward_id_17: int = Column(Integer, nullable=False)
    reward_count_17: int = Column(Integer, nullable=False)
    price_type_17: int = Column(Integer, nullable=False)
    currency_id_17: int = Column(Integer, nullable=False)
    price_17: int = Column(Integer, nullable=False)
    reward_type_18: int = Column(Integer, nullable=False)
    reward_id_18: int = Column(Integer, nullable=False)
    reward_count_18: int = Column(Integer, nullable=False)
    price_type_18: int = Column(Integer, nullable=False)
    currency_id_18: int = Column(Integer, nullable=False)
    price_18: int = Column(Integer, nullable=False)
    reward_type_19: int = Column(Integer, nullable=False)
    reward_id_19: int = Column(Integer, nullable=False)
    reward_count_19: int = Column(Integer, nullable=False)
    price_type_19: int = Column(Integer, nullable=False)
    currency_id_19: int = Column(Integer, nullable=False)
    price_19: int = Column(Integer, nullable=False)
    reward_type_20: int = Column(Integer, nullable=False)
    reward_id_20: int = Column(Integer, nullable=False)
    reward_count_20: int = Column(Integer, nullable=False)
    price_type_20: int = Column(Integer, nullable=False)
    currency_id_20: int = Column(Integer, nullable=False)
    price_20: int = Column(Integer, nullable=False)


class FkeHappeningList(DeclarativeBase, Base["FkeHappeningList"]):
    __tablename__ = 'fke_happening_list'

    happening_id: int = Column(Integer, primary_key=True)
    happening_name: str = Column(Text, nullable=False)


class FkeReward(DeclarativeBase, Base["FkeReward"]):
    __tablename__ = 'fke_reward'

    id: int = Column(Integer, primary_key=True)
    fke_point: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class GachaDatum(DeclarativeBase, Base["GachaDatum"]):
    __tablename__ = 'gacha_data'

    gacha_id: int = Column(Integer, primary_key=True)
    gacha_name: str = Column(Text, nullable=False)
    pick_up_chara_text: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    description_2: str = Column(Text, nullable=False)
    description_sp: str = Column(Text, nullable=False)
    parallel_id: int = Column(Integer, nullable=False)
    pickup_badge: int = Column(Integer, nullable=False)
    gacha_detail: int = Column(Integer, nullable=False)
    gacha_cost_type: int = Column(Integer, nullable=False)
    price: int = Column(Integer, nullable=False)
    free_gacha_type: int = Column(Integer, nullable=False)
    free_gacha_interval_time: int = Column(Integer, nullable=False)
    free_gacha_count: int = Column(Integer, nullable=False)
    discount_price: int = Column(Integer, nullable=False)
    gacha_odds: str = Column(Text, nullable=False)
    gacha_odds_star2: str = Column(Text, nullable=False)
    gacha_type: int = Column(Integer, nullable=False)
    movie_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    ticket_id: int = Column(Integer, nullable=False)
    special_id: int = Column(Integer, nullable=False)
    exchange_id: int = Column(Integer, nullable=False, index=True)
    ticket_id_10: int = Column(Integer, nullable=False)
    rarity_odds: str = Column(Text, nullable=False)
    chara_odds_star1: str = Column(Text, nullable=False)
    chara_odds_star2: str = Column(Text, nullable=False)
    chara_odds_star3: str = Column(Text, nullable=False)
    gacha10_special_odds_star1: str = Column(Text, nullable=False)
    gacha10_special_odds_star2: str = Column(Text, nullable=False)
    gacha10_special_odds_star3: str = Column(Text, nullable=False)
    prizegacha_id: int = Column(Integer, nullable=False)
    gacha_bonus_id: int = Column(Integer, nullable=False)
    gacha_times_limit10: int = Column(Integer, nullable=False)


class GachaExchangeLineup(DeclarativeBase, Base["GachaExchangeLineup"]):
    __tablename__ = 'gacha_exchange_lineup'

    id: int = Column(Integer, primary_key=True)
    exchange_id: int = Column(Integer, nullable=False, index=True)
    unit_id: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    gacha_bonus_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class GiftMessage(DeclarativeBase, Base["GiftMessage"]):
    __tablename__ = 'gift_message'

    id: int = Column(Integer, primary_key=True)
    discription: str = Column(Text, nullable=False)
    type_1: int = Column(Integer, nullable=False)
    type_2: int = Column(Integer, nullable=False)
    type_3: int = Column(Integer, nullable=False)
    type_4: int = Column(Integer, nullable=False)


class GlobalDatum(DeclarativeBase, Base["GlobalDatum"]):
    __tablename__ = 'global_data'

    key_name: str = Column(Text, primary_key=True)
    value: int = Column(Integer, nullable=False)
    desc: str = Column(Text, nullable=False)


class GlossaryDetail(DeclarativeBase, Base["GlossaryDetail"]):
    __tablename__ = 'glossary_detail'

    glossary_id: int = Column(Integer, primary_key=True)
    glossary_category_id: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    unlock_story_id: int = Column(Integer, nullable=False)
    category_type: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)


class GoldsetDatum(DeclarativeBase, Base["GoldsetDatum"]):
    __tablename__ = 'goldset_data'

    id: int = Column(Integer, nullable=False)
    buy_count: int = Column(Integer, primary_key=True)
    use_jewel_count: int = Column(Integer, nullable=False)
    get_gold_count: int = Column(Integer, nullable=False)
    goldset_odds_1: int = Column(Integer, nullable=False)
    goldset_odds_2: int = Column(Integer, nullable=False)
    goldset_odds_3: int = Column(Integer, nullable=False)
    additional_gold_min_rate: int = Column(Integer, nullable=False)
    additional_gold_max_rate: int = Column(Integer, nullable=False)


class GoldsetData2(DeclarativeBase, Base["GoldsetData2"]):
    __tablename__ = 'goldset_data_2'

    id: int = Column(Integer, nullable=False)
    buy_count: int = Column(Integer, primary_key=True)
    use_jewel_count: int = Column(Integer, nullable=False)
    get_gold_count: int = Column(Integer, nullable=False)
    goldset_odds_1: int = Column(Integer, nullable=False)
    goldset_odds_2: int = Column(Integer, nullable=False)
    goldset_odds_3: int = Column(Integer, nullable=False)
    additional_gold_min_rate: int = Column(Integer, nullable=False)
    additional_gold_max_rate: int = Column(Integer, nullable=False)
    training_quest_count: int = Column(Integer, nullable=False)


class GoldsetDataTeamlevel(DeclarativeBase, Base["GoldsetDataTeamlevel"]):
    __tablename__ = 'goldset_data_teamlevel'

    id: int = Column(Integer, nullable=False)
    team_level: int = Column(Integer, primary_key=True)
    initial_get_gold_count: int = Column(Integer, nullable=False)


class GrandArenaDailyRankReward(DeclarativeBase, Base["GrandArenaDailyRankReward"]):
    __tablename__ = 'grand_arena_daily_rank_reward'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class GrandArenaDefenceReward(DeclarativeBase, Base["GrandArenaDefenceReward"]):
    __tablename__ = 'grand_arena_defence_reward'

    id: int = Column(Integer, primary_key=True)
    limit_count: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class GrandArenaMaxRankReward(DeclarativeBase, Base["GrandArenaMaxRankReward"]):
    __tablename__ = 'grand_arena_max_rank_reward'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class GrandArenaMaxSeasonRankReward(DeclarativeBase, Base["GrandArenaMaxSeasonRankReward"]):
    __tablename__ = 'grand_arena_max_season_rank_reward'

    id: int = Column(Integer, primary_key=True)
    rank_from: int = Column(Integer, nullable=False)
    rank_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class GrowthParameter(DeclarativeBase, Base["GrowthParameter"]):
    __tablename__ = 'growth_parameter'

    growth_id: int = Column(Integer, primary_key=True)
    growth_type: int = Column(Integer, nullable=False)
    is_restriction: int = Column(Integer, nullable=False)
    unit_rarity: int = Column(Integer, nullable=False)
    unit_level: int = Column(Integer, nullable=False)
    skill_level: int = Column(Integer, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    equipment_1: int = Column(Integer, nullable=False)
    equipment_2: int = Column(Integer, nullable=False)
    equipment_3: int = Column(Integer, nullable=False)
    equipment_4: int = Column(Integer, nullable=False)
    equipment_5: int = Column(Integer, nullable=False)
    equipment_6: int = Column(Integer, nullable=False)
    love_level: int = Column(Integer, nullable=False)


class GrowthParameterUnique(DeclarativeBase, Base["GrowthParameterUnique"]):
    __tablename__ = 'growth_parameter_unique'

    growth_id: int = Column(Integer, primary_key=True)
    unique_equip_strength_point_1: int = Column(Integer, nullable=False)
    unique_equip_strength_point_2: int = Column(Integer, nullable=False)
    unique_equip_rank_1: int = Column(Integer, nullable=False)
    unique_equip_rank_2: int = Column(Integer, nullable=False)


class GrowthRestrictionUnit(DeclarativeBase, Base["GrowthRestrictionUnit"]):
    __tablename__ = 'growth_restriction_unit'

    id: int = Column(Integer, primary_key=True)
    growth_id: int = Column(Integer, nullable=False, index=True)
    unit_id: int = Column(Integer, nullable=False)


class Guild(DeclarativeBase, Base["Guild"]):
    __tablename__ = 'guild'

    guild_id: int = Column(Integer, primary_key=True)
    guild_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    guild_master: int = Column(Integer, nullable=False)
    member1: int = Column(Integer, nullable=False)
    member2: int = Column(Integer, nullable=False)
    member3: int = Column(Integer, nullable=False)
    member4: int = Column(Integer, nullable=False)
    member5: int = Column(Integer, nullable=False)
    member6: int = Column(Integer, nullable=False)
    member7: int = Column(Integer, nullable=False)
    member8: int = Column(Integer, nullable=False)
    member9: int = Column(Integer, nullable=False)
    member10: int = Column(Integer, nullable=False)
    member11: int = Column(Integer, nullable=False)
    member12: int = Column(Integer, nullable=False)
    member13: int = Column(Integer, nullable=False)
    member14: int = Column(Integer, nullable=False)
    member15: int = Column(Integer, nullable=False)
    member16: int = Column(Integer, nullable=False)
    member17: int = Column(Integer, nullable=False)
    member18: int = Column(Integer, nullable=False)
    member19: int = Column(Integer, nullable=False)
    member20: int = Column(Integer, nullable=False)
    member21: int = Column(Integer, nullable=False)
    member22: int = Column(Integer, nullable=False)
    member23: int = Column(Integer, nullable=False)
    member24: int = Column(Integer, nullable=False)
    member25: int = Column(Integer, nullable=False)
    member26: int = Column(Integer, nullable=False)
    member27: int = Column(Integer, nullable=False)
    member28: int = Column(Integer, nullable=False)
    member29: int = Column(Integer, nullable=False)
    member30: int = Column(Integer, nullable=False)


class GuildAdditionalMember(DeclarativeBase, Base["GuildAdditionalMember"]):
    __tablename__ = 'guild_additional_member'

    guild_id: int = Column(Integer, primary_key=True)
    unlock_story_id: int = Column(Integer, nullable=False)
    thumb_id: int = Column(Integer, nullable=False)
    member1: int = Column(Integer, nullable=False)
    member2: int = Column(Integer, nullable=False)
    member3: int = Column(Integer, nullable=False)
    member4: int = Column(Integer, nullable=False)
    member5: int = Column(Integer, nullable=False)
    member6: int = Column(Integer, nullable=False)
    member7: int = Column(Integer, nullable=False)
    member8: int = Column(Integer, nullable=False)
    member9: int = Column(Integer, nullable=False)
    member10: int = Column(Integer, nullable=False)


class HatsuneBattleMissionDatum(DeclarativeBase, Base["HatsuneBattleMissionDatum"]):
    __tablename__ = 'hatsune_battle_mission_data'

    mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_value_4: int = Column(Integer)
    condition_value_5: int = Column(Integer)
    condition_value_6: int = Column(Integer)
    condition_value_7: int = Column(Integer)
    condition_value_8: int = Column(Integer)
    condition_value_9: int = Column(Integer)
    condition_value_10: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class HatsuneBgChange(DeclarativeBase, Base["HatsuneBgChange"]):
    __tablename__ = 'hatsune_bg_change'

    area_id: int = Column(Integer, primary_key=True)
    quest_id_1: int = Column(Integer, nullable=False)
    quest_id_2: int = Column(Integer, nullable=False)
    quest_id_3: int = Column(Integer, nullable=False)
    quest_id_4: int = Column(Integer, nullable=False)
    quest_id_5: int = Column(Integer, nullable=False)


class HatsuneBgChangeDatum(DeclarativeBase, Base["HatsuneBgChangeDatum"]):
    __tablename__ = 'hatsune_bg_change_data'
    __table_args__ = (
        Index('hatsune_bg_change_data_0_target_type_1_area_id', 'target_type', 'area_id'),
    )

    id: int = Column(Integer, primary_key=True)
    area_id: int = Column(Integer, nullable=False)
    condition_type: int = Column(Integer, nullable=False)
    condition_id: int = Column(Integer, nullable=False)
    target_type: int = Column(Integer, nullable=False)
    bg_after_change_id: int = Column(Integer, nullable=False)


class HatsuneBos(DeclarativeBase, Base["HatsuneBos"]):
    __tablename__ = 'hatsune_boss'
    __table_args__ = (
        Index('hatsune_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
    )

    boss_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    area_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    boss_position_x: int = Column(Integer, nullable=False)
    boss_position_y: int = Column(Integer, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    icon_display_scale: float = Column(Float, nullable=False)
    icon_collider_scale: float = Column(Float, nullable=False)
    use_ticket_num: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    unit_exp: int = Column(Integer, nullable=False)
    love: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    daily_limit: int = Column(Integer, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)
    event_boss_treasure_box_id_1: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False, index=True)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    story_id_wavestart_1: int = Column(Integer, nullable=False)
    story_id_waveend_1: int = Column(Integer, nullable=False)
    detail_bg_id: int = Column(Integer, nullable=False)
    detail_bg_position: int = Column(Integer, nullable=False)
    detail_boss_bg_size: float = Column(Float, nullable=False)
    detail_boss_bg_height: float = Column(Float, nullable=False)
    reward_gold_coefficient: str = Column(Text, nullable=False)
    reward_gold_limit: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    map_position_x: float = Column(Float, nullable=False)
    map_position_y: float = Column(Float, nullable=False)
    map_size: float = Column(Float, nullable=False)
    deatail_aura_size: float = Column(Float, nullable=False)
    map_aura_size: float = Column(Float, nullable=False)
    oneblow_count_of_skip_condition: int = Column(Integer, nullable=False)
    required_skip_ticket_count: int = Column(Integer, nullable=False)
    retire_flag: int = Column(Integer, nullable=False)
    disp_on_bg: int = Column(Integer, nullable=False)
    qd_mode: int = Column(Integer, nullable=False)
    td_mode: int = Column(Integer, nullable=False)


class HatsuneBossCondition(DeclarativeBase, Base["HatsuneBossCondition"]):
    __tablename__ = 'hatsune_boss_condition'

    boss_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    condition_quest_id_1: int = Column(Integer, nullable=False)
    condition_quest_id_2: int = Column(Integer, nullable=False)
    condition_boss_id_1: int = Column(Integer, nullable=False)
    condition_boss_id_2: int = Column(Integer, nullable=False)
    condition_gacha_step: int = Column(Integer, nullable=False)
    force_unlock_time: str = Column(Text, nullable=False)
    release_quest_id_1: int = Column(Integer, nullable=False)
    release_quest_id_2: int = Column(Integer, nullable=False)
    release_boss_id_1: int = Column(Integer, nullable=False)
    release_boss_id_2: int = Column(Integer, nullable=False)


class HatsuneBossEnemySetting(DeclarativeBase, Base["HatsuneBossEnemySetting"]):
    __tablename__ = 'hatsune_boss_enemy_setting'
    __table_args__ = (
        Index('hatsune_boss_enemy_setting_0_boss_id_1_event_id', 'boss_id', 'event_id'),
    )

    boss_id: int = Column(Integer, primary_key=True, nullable=False)
    enemy_identify: int = Column(Integer, primary_key=True, nullable=False)
    event_id: int = Column(Integer, nullable=False)
    must_kill_flag: int = Column(Integer, nullable=False)
    event_boss_treasure_box_id: int = Column(Integer, nullable=False)
    reward_gold_coefficient: float = Column(Float, nullable=False)
    reward_gold_limit: int = Column(Integer, nullable=False)
    detail_offset_x: int = Column(Integer, nullable=False)
    detail_offset_y: int = Column(Integer, nullable=False)
    detail_scale: float = Column(Float, nullable=False)
    map_offset_x: int = Column(Integer, nullable=False)
    map_offset_y: int = Column(Integer, nullable=False)
    map_scale: float = Column(Float, nullable=False)
    map_depth: int = Column(Integer, nullable=False)


class HatsuneDailyMissionDatum(DeclarativeBase, Base["HatsuneDailyMissionDatum"]):
    __tablename__ = 'hatsune_daily_mission_data'

    daily_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class HatsuneDescription(DeclarativeBase, Base["HatsuneDescription"]):
    __tablename__ = 'hatsune_description'
    __table_args__ = (
        Index('hatsune_description_0_event_id_1_type', 'event_id', 'type'),
    )

    id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)


class HatsuneDiaryDatum(DeclarativeBase, Base["HatsuneDiaryDatum"]):
    __tablename__ = 'hatsune_diary_data'

    diary_id: int = Column(Integer, primary_key=True)
    contents_type: int = Column(Integer, nullable=False, index=True)
    diary_date: int = Column(Integer, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    forced_release_time: str = Column(Text, nullable=False)
    condition_time: str = Column(Text, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)
    condition_boss_count: int = Column(Integer, nullable=False)


class HatsuneDiaryLetterScript(DeclarativeBase, Base["HatsuneDiaryLetterScript"]):
    __tablename__ = 'hatsune_diary_letter_script'

    id: int = Column(Integer, primary_key=True)
    diary_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    line_num: int = Column(Integer, nullable=False)
    start_pos: int = Column(Integer, nullable=False)
    end_pos: int = Column(Integer, nullable=False)
    seek_time: float = Column(Float, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class HatsuneDiaryScript(DeclarativeBase, Base["HatsuneDiaryScript"]):
    __tablename__ = 'hatsune_diary_script'

    id: int = Column(Integer, primary_key=True)
    diary_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    diary_text: str = Column(Text, nullable=False)
    text_animation_speed: int = Column(Integer, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class HatsuneDiarySetting(DeclarativeBase, Base["HatsuneDiarySetting"]):
    __tablename__ = 'hatsune_diary_setting'

    event_id: int = Column(Integer, primary_key=True)
    bgm_sheet_name: str = Column(Text, nullable=False)
    bgm_cue_name: str = Column(Text, nullable=False)


class HatsuneEmblemMission(DeclarativeBase, Base["HatsuneEmblemMission"]):
    __tablename__ = 'hatsune_emblem_mission'

    mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer, nullable=False)
    condition_value_2: int = Column(Integer, nullable=False)
    condition_value_3: int = Column(Integer, nullable=False)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False, index=True)
    visible_flag: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class HatsuneEmblemMissionReward(DeclarativeBase, Base["HatsuneEmblemMissionReward"]):
    __tablename__ = 'hatsune_emblem_mission_reward'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False, index=True)
    reward_num: int = Column(Integer, nullable=False)
    icon_type: int = Column(Integer, nullable=False)


class HatsuneItem(DeclarativeBase, Base["HatsuneItem"]):
    __tablename__ = 'hatsune_item'

    event_id: int = Column(Integer, primary_key=True)
    boss_ticket_id: int = Column(Integer, nullable=False)
    gacha_ticket_id: int = Column(Integer, nullable=False)
    unit_material_id_1: int = Column(Integer, nullable=False)
    unit_material_id_2: int = Column(Integer, nullable=False)
    unit_material_id_3: int = Column(Integer, nullable=False)
    unit_material_id_4: int = Column(Integer, nullable=False)
    unit_material_id_5: int = Column(Integer, nullable=False)
    unit_material_id_6: int = Column(Integer, nullable=False)
    unit_material_id_7: int = Column(Integer, nullable=False)
    unit_material_id_8: int = Column(Integer, nullable=False)
    unit_material_id_9: int = Column(Integer, nullable=False)
    unit_material_id_10: int = Column(Integer, nullable=False)


class HatsuneLimitChara(DeclarativeBase, Base["HatsuneLimitChara"]):
    __tablename__ = 'hatsune_limit_chara'

    event_boss_id: int = Column(Integer, primary_key=True)
    limit_chara_type_1: int = Column(Integer, nullable=False)


class HatsuneMap(DeclarativeBase, Base["HatsuneMap"]):
    __tablename__ = 'hatsune_map'

    course_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)
    map_id: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    start_area_id: int = Column(Integer, nullable=False)
    end_area_id: int = Column(Integer, nullable=False)


class HatsuneMapEvent(DeclarativeBase, Base["HatsuneMapEvent"]):
    __tablename__ = 'hatsune_map_event'

    id: int = Column(Integer, primary_key=True)
    target_event_id: int = Column(Integer, nullable=False, index=True)
    event_type: int = Column(Integer, nullable=False)
    condition_id: int = Column(Integer, nullable=False)
    param1: int = Column(Integer, nullable=False)
    param2: int = Column(Integer, nullable=False)


class HatsuneMissionRewardDatum(DeclarativeBase, Base["HatsuneMissionRewardDatum"]):
    __tablename__ = 'hatsune_mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer)
    reward_num: int = Column(Integer, nullable=False)


class HatsuneMultiRouteParameter(DeclarativeBase, Base["HatsuneMultiRouteParameter"]):
    __tablename__ = 'hatsune_multi_route_parameter'

    id: int = Column(Integer, primary_key=True)
    quest_id: int = Column(Integer, nullable=False, index=True)
    type: int = Column(Integer, nullable=False, index=True)
    param_1: int = Column(Integer, nullable=False)
    param_2: int = Column(Integer, nullable=False)
    param_3: int = Column(Integer, nullable=False)
    text_1: str = Column(Text, nullable=False)


class HatsunePresent(DeclarativeBase, Base["HatsunePresent"]):
    __tablename__ = 'hatsune_present'

    id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    dialog_title: str = Column(Text, nullable=False)
    dialog_text: str = Column(Text, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    condition_mission_id: int = Column(Integer, nullable=False)
    adv_id: int = Column(Integer, nullable=False)
    item_type_1: int = Column(Integer, nullable=False)
    item_id_1: int = Column(Integer, nullable=False)
    item_num_1: int = Column(Integer, nullable=False)
    item_type_2: int = Column(Integer, nullable=False)
    item_id_2: int = Column(Integer, nullable=False)
    item_num_2: int = Column(Integer, nullable=False)
    item_type_3: int = Column(Integer, nullable=False)
    item_id_3: int = Column(Integer, nullable=False)
    item_num_3: int = Column(Integer, nullable=False)
    item_type_4: int = Column(Integer, nullable=False)
    item_id_4: int = Column(Integer, nullable=False)
    item_num_4: int = Column(Integer, nullable=False)
    item_type_5: int = Column(Integer, nullable=False)
    item_id_5: int = Column(Integer, nullable=False)
    item_num_5: int = Column(Integer, nullable=False)


class HatsuneQuest(DeclarativeBase, Base["HatsuneQuest"]):
    __tablename__ = 'hatsune_quest'

    quest_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    area_id: int = Column(Integer, nullable=False)
    quest_seq: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    icon_offset_x: float = Column(Float, nullable=False)
    icon_offset_y: float = Column(Float, nullable=False)
    icon_scale: float = Column(Float, nullable=False)
    stamina: int = Column(Integer, nullable=False)
    stamina_start: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    unit_exp: int = Column(Integer, nullable=False)
    love: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    daily_limit: int = Column(Integer, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)
    rank_reward_group: int = Column(Integer, nullable=False)
    drop_reward_type: int = Column(Integer, nullable=False)
    drop_reward_id: int = Column(Integer, nullable=False)
    drop_reward_num: int = Column(Integer, nullable=False)
    drop_reward_odds: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    story_id_wavestart_1: int = Column(Integer, nullable=False)
    story_id_waveend_1: int = Column(Integer, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2: str = Column(Text, nullable=False)
    wave_bgm_que_id_2: str = Column(Text, nullable=False)
    story_id_wavestart_2: int = Column(Integer, nullable=False)
    story_id_waveend_2: int = Column(Integer, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3: str = Column(Text, nullable=False)
    wave_bgm_que_id_3: str = Column(Text, nullable=False)
    story_id_wavestart_3: int = Column(Integer, nullable=False)
    story_id_waveend_3: int = Column(Integer, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class HatsuneQuestArea(DeclarativeBase, Base["HatsuneQuestArea"]):
    __tablename__ = 'hatsune_quest_area'

    area_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    area_name: str = Column(Text, nullable=False)
    map_type: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    area_disp: int = Column(Integer, nullable=False)
    map_id: int = Column(Integer, nullable=False)
    scroll_width: int = Column(Integer, nullable=False)
    scroll_height: int = Column(Integer, nullable=False)
    open_tutorial_id: int = Column(Integer, nullable=False)
    tutorial_param_1: str = Column(Text, nullable=False)
    tutorial_param_2: str = Column(Text, nullable=False)
    additional_effect: int = Column(Integer, nullable=False)


class HatsuneQuestCondition(DeclarativeBase, Base["HatsuneQuestCondition"]):
    __tablename__ = 'hatsune_quest_condition'

    quest_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    condition_quest_id_1: int = Column(Integer, nullable=False)
    condition_quest_id_2: int = Column(Integer, nullable=False)
    condition_boss_id_1: int = Column(Integer, nullable=False)
    condition_boss_id_2: int = Column(Integer, nullable=False)
    release_quest_id_1: int = Column(Integer, nullable=False)
    release_quest_id_2: int = Column(Integer, nullable=False)
    release_boss_id_1: int = Column(Integer, nullable=False)
    release_boss_id_2: int = Column(Integer, nullable=False)
    condition_main_quest_id: int = Column(Integer, nullable=False)


class HatsuneQuiz(DeclarativeBase, Base["HatsuneQuiz"]):
    __tablename__ = 'hatsune_quiz'
    __table_args__ = (
        Index('hatsune_quiz_0_event_id_1_release_quest_id', 'event_id', 'release_quest_id'),
    )

    event_id: int = Column(Integer, nullable=False, index=True)
    quiz_id: int = Column(Integer, primary_key=True)
    question_title: str = Column(Text, nullable=False)
    question: str = Column(Text, nullable=False)
    choice_1: str = Column(Text, nullable=False)
    choice_2: str = Column(Text, nullable=False)
    choice_3: str = Column(Text, nullable=False)
    choice_4: str = Column(Text, nullable=False)
    choice_5: str = Column(Text, nullable=False)
    choice_6: str = Column(Text, nullable=False)
    answer: int = Column(Integer, nullable=False)
    hint: str = Column(Text, nullable=False)
    resource_id: int = Column(Integer, nullable=False)
    release_quest_id: int = Column(Integer, nullable=False)
    quiz_position_x: int = Column(Integer, nullable=False)
    quiz_position_y: int = Column(Integer, nullable=False)
    quiz_icon_id: int = Column(Integer, nullable=False)
    quiz_point_name: str = Column(Text, nullable=False)
    adv_id_quiz_start: int = Column(Integer, nullable=False)
    adv_id_quiz_end: int = Column(Integer, nullable=False)


class HatsuneQuizCondition(DeclarativeBase, Base["HatsuneQuizCondition"]):
    __tablename__ = 'hatsune_quiz_condition'
    __table_args__ = (
        Index('hatsune_quiz_condition_0_event_id_1_quiz_id', 'event_id', 'quiz_id'),
    )

    id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    quiz_id: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_quiz_id: int = Column(Integer, nullable=False)
    condition_unit_id: int = Column(Integer, nullable=False)
    condition_mission_id: int = Column(Integer, nullable=False)
    condition_time_from: int = Column(Integer, nullable=False)


class HatsuneQuizReward(DeclarativeBase, Base["HatsuneQuizReward"]):
    __tablename__ = 'hatsune_quiz_reward'

    quiz_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class HatsuneRelayDatum(DeclarativeBase, Base["HatsuneRelayDatum"]):
    __tablename__ = 'hatsune_relay_data'

    relay_story_id: int = Column(Integer, primary_key=True)
    is_enable_read: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    story_seq: int = Column(Integer, nullable=False)
    sub_title: str = Column(Text, nullable=False)


class HatsuneSchedule(DeclarativeBase, Base["HatsuneSchedule"]):
    __tablename__ = 'hatsune_schedule'

    event_id: int = Column(Integer, primary_key=True)
    teaser_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    close_time: str = Column(Text, nullable=False)
    background: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    banner_unit_id: int = Column(Integer, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    backgroud_size_x: int = Column(Integer, nullable=False)
    backgroud_size_y: int = Column(Integer, nullable=False)
    backgroud_pos_x: int = Column(Integer, nullable=False)
    backgroud_pos_y: int = Column(Integer, nullable=False)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    series_event_id: int = Column(Integer, nullable=False, index=True)
    teaser_dialog_type: int = Column(Integer, nullable=False)


class HatsuneSeriesGachaReference(DeclarativeBase, Base["HatsuneSeriesGachaReference"]):
    __tablename__ = 'hatsune_series_gacha_reference'

    event_id: int = Column(Integer, primary_key=True)
    reference_key_event_id_flag: int = Column(Integer, nullable=False)


class HatsuneSpecialBattle(DeclarativeBase, Base["HatsuneSpecialBattle"]):
    __tablename__ = 'hatsune_special_battle'

    event_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    mode: int = Column(Integer, primary_key=True, nullable=False)
    recommended_level: int = Column(Integer, nullable=False)
    purpose_type: int = Column(Integer, nullable=False)
    purpose_count: int = Column(Integer, nullable=False)
    trigger_hp: int = Column(Integer, nullable=False)
    story_id_mode_start: int = Column(Integer, nullable=False)
    story_id_mode_end: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False, index=True)
    unnecessary_defeat_chara: int = Column(Integer, nullable=False)
    story_start_second: float = Column(Float, nullable=False)
    action_start_second: float = Column(Float, nullable=False)
    hp_gauge_color_flag: int = Column(Integer, nullable=False)
    start_idle_trigger: int = Column(Integer, nullable=False)
    appear_time: float = Column(Float, nullable=False)
    detail_boss_bg_size: float = Column(Float, nullable=False)
    detail_boss_bg_height: float = Column(Float, nullable=False)
    detail_boss_motion: str = Column(Text, nullable=False)
    is_hide_boss: int = Column(Integer, nullable=False)


class HatsuneSpecialBossTicketCount(DeclarativeBase, Base["HatsuneSpecialBossTicketCount"]):
    __tablename__ = 'hatsune_special_boss_ticket_count'

    id: int = Column(Integer, primary_key=True)
    challenge_count_from: int = Column(Integer, nullable=False)
    challenge_count_to: int = Column(Integer, nullable=False)
    use_ticket_num: int = Column(Integer, nullable=False)


class HatsuneSpecialEnemy(DeclarativeBase, Base["HatsuneSpecialEnemy"]):
    __tablename__ = 'hatsune_special_enemy'

    enemy_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    mode: int = Column(Integer, nullable=False)
    enemy_point: int = Column(Integer, nullable=False)
    initial_position: int = Column(Integer, nullable=False)
    order: int = Column(Integer, nullable=False)


class HatsuneSpecialMissionDatum(DeclarativeBase, Base["HatsuneSpecialMissionDatum"]):
    __tablename__ = 'hatsune_special_mission_data'

    special_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    purpose_type: int = Column(Integer, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class HatsuneStationaryMissionDatum(DeclarativeBase, Base["HatsuneStationaryMissionDatum"]):
    __tablename__ = 'hatsune_stationary_mission_data'

    stationary_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False, index=True)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class HatsuneUnlockStoryCondition(DeclarativeBase, Base["HatsuneUnlockStoryCondition"]):
    __tablename__ = 'hatsune_unlock_story_condition'

    story_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    condition_entry: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    condition_mission_id: int = Column(Integer, nullable=False)
    condition_time: str = Column(Text, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)


class HatsuneUnlockUnitCondition(DeclarativeBase, Base["HatsuneUnlockUnitCondition"]):
    __tablename__ = 'hatsune_unlock_unit_condition'
    __table_args__ = (
        Index('hatsune_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id'),
    )

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)
    condition_mission_id: int = Column(Integer, nullable=False, index=True)
    top_description: str = Column(Text, nullable=False)
    description_1: str = Column(Text, nullable=False)
    description_2: str = Column(Text, nullable=False)


class ItemDatum(DeclarativeBase, Base["ItemDatum"]):
    __tablename__ = 'item_data'

    item_id: int = Column(Integer, primary_key=True)
    item_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    item_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)
    price: int = Column(Integer, nullable=False)
    limit_num: int = Column(Integer, nullable=False)
    gojuon_order: int = Column(Integer, nullable=False)
    sell_check_disp: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class ItemETicketDatum(DeclarativeBase, Base["ItemETicketDatum"]):
    __tablename__ = 'item_e_ticket_data'

    ticket_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    exchange_number: int = Column(Integer, primary_key=True, nullable=False, index=True)
    unit_id: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class KaiserAddTimesDatum(DeclarativeBase, Base["KaiserAddTimesDatum"]):
    __tablename__ = 'kaiser_add_times_data'

    id: int = Column(Integer, primary_key=True)
    add_times: int = Column(Integer, nullable=False)
    add_times_time: str = Column(Text, nullable=False)
    duration: int = Column(Integer, nullable=False)


class KaiserExterminationReward(DeclarativeBase, Base["KaiserExterminationReward"]):
    __tablename__ = 'kaiser_extermination_reward'

    extermination_reward_group: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class KaiserQuestDatum(DeclarativeBase, Base["KaiserQuestDatum"]):
    __tablename__ = 'kaiser_quest_data'

    kaiser_boss_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    map_type: int = Column(Integer, nullable=False)
    battle_start_story_id: int = Column(Integer, nullable=False)
    battle_finish_story_id: int = Column(Integer, nullable=False)
    disappearance_story_id: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    restriction_group_id: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)
    fix_reward_group_id: int = Column(Integer, nullable=False)
    odds_group_id: str = Column(Text, nullable=False)
    chest_id: int = Column(Integer, nullable=False)
    extermination_reward_group: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    bg_position: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    enemy_position_x: int = Column(Integer, nullable=False)
    enemy_local_position_y: int = Column(Integer, nullable=False)
    enemy_size_1: float = Column(Float, nullable=False)
    result_boss_position_y: float = Column(Float, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)
    reward_gold_coefficient: float = Column(Float, nullable=False)
    limited_mana: int = Column(Integer, nullable=False)
    clear_story_id_1: int = Column(Integer, nullable=False)
    clear_story_id_2: int = Column(Integer, nullable=False)


class KaiserRestrictionGroup(DeclarativeBase, Base["KaiserRestrictionGroup"]):
    __tablename__ = 'kaiser_restriction_group'

    restriction_group_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    unit_id: int = Column(Integer, primary_key=True, nullable=False)


class KaiserSchedule(DeclarativeBase, Base["KaiserSchedule"]):
    __tablename__ = 'kaiser_schedule'

    id: int = Column(Integer, primary_key=True)
    teaser_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    close_time: str = Column(Text, nullable=False)
    story_id: int = Column(Integer, nullable=False)
    close_story_condition_id: int = Column(Integer, nullable=False)
    close_story_id: int = Column(Integer, nullable=False)
    top_bgm: str = Column(Text, nullable=False)
    top_bg: str = Column(Text, nullable=False)
    after_bgm: str = Column(Text, nullable=False)
    after_bg: str = Column(Text, nullable=False)


class KaiserSpecialBattle(DeclarativeBase, Base["KaiserSpecialBattle"]):
    __tablename__ = 'kaiser_special_battle'

    mode: int = Column(Integer, primary_key=True)
    recommended_level: int = Column(Integer, nullable=False)
    purpose_type: int = Column(Integer, nullable=False)
    purpose_count: int = Column(Integer, nullable=False)
    trigger_hp: int = Column(Integer, nullable=False)
    story_id_mode_start: int = Column(Integer, nullable=False)
    story_id_mode_end: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    unnecessary_defeat_chara: int = Column(Integer, nullable=False)
    story_start_second: float = Column(Float, nullable=False)
    action_start_second: float = Column(Float, nullable=False)
    hp_gauge_color_flag: int = Column(Integer, nullable=False)
    start_idle_trigger: int = Column(Integer, nullable=False)
    appear_time: float = Column(Float, nullable=False)


class KmkNaviComment(DeclarativeBase, Base["KmkNaviComment"]):
    __tablename__ = 'kmk_navi_comment'

    comment_id: int = Column(Integer, primary_key=True)
    where_type: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    face_type: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    description: str = Column(Text)
    voice_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    pos_x: float = Column(Float, nullable=False)
    pos_y: float = Column(Float, nullable=False)
    change_face_time: float = Column(Float, nullable=False)
    change_face_type: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class KmkReward(DeclarativeBase, Base["KmkReward"]):
    __tablename__ = 'kmk_reward'

    id: int = Column(Integer, primary_key=True)
    kmk_score: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class LegionAddTimesDatum(DeclarativeBase, Base["LegionAddTimesDatum"]):
    __tablename__ = 'legion_add_times_data'

    id: int = Column(Integer, primary_key=True)
    add_times: int = Column(Integer, nullable=False)
    add_times_time: str = Column(Text, nullable=False)


class LegionBattleBonu(DeclarativeBase, Base["LegionBattleBonu"]):
    __tablename__ = 'legion_battle_bonus'
    __table_args__ = (
        Index('legion_battle_bonus_0_type_1_legion_boss_id', 'type', 'legion_boss_id'),
    )

    legion_battle_bonus_id: int = Column(Integer, primary_key=True)
    type: int = Column(Integer, nullable=False, index=True)
    legion_boss_id: int = Column(Integer, nullable=False)
    condition_hp: str = Column(Text, nullable=False)
    legion_battle_effect_id: int = Column(Integer, nullable=False)
    duration: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)


class LegionBattleBonusEffect(DeclarativeBase, Base["LegionBattleBonusEffect"]):
    __tablename__ = 'legion_battle_bonus_effect'

    legion_battle_effect_id: int = Column(Integer, primary_key=True)
    enemy_id: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    text_id: int = Column(Integer, nullable=False)
    skill_id: int = Column(Integer, nullable=False)
    target_type: int = Column(Integer, nullable=False)


class LegionBossEnemySetting(DeclarativeBase, Base["LegionBossEnemySetting"]):
    __tablename__ = 'legion_boss_enemy_setting'

    boss_id: int = Column(Integer, primary_key=True)
    detail_offset_x: int = Column(Integer, nullable=False)
    detail_offset_y: int = Column(Integer, nullable=False)
    detail_offset_scale: float = Column(Float, nullable=False)


class LegionEffect(DeclarativeBase, Base["LegionEffect"]):
    __tablename__ = 'legion_effect'

    effect_id: int = Column(Integer, primary_key=True)
    bonus_1: int = Column(Integer, nullable=False)
    bonus_2: int = Column(Integer, nullable=False)
    bonus_3: int = Column(Integer, nullable=False)
    bonus_4: int = Column(Integer, nullable=False)
    bonus_5: int = Column(Integer, nullable=False)


class LegionEffectiveUnit(DeclarativeBase, Base["LegionEffectiveUnit"]):
    __tablename__ = 'legion_effective_unit'

    legion_boss_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    unit_id: int = Column(Integer, primary_key=True, nullable=False)
    effect_id: int = Column(Integer, nullable=False)
    support_effect_id: int = Column(Integer, nullable=False)


class LegionExterminationReward(DeclarativeBase, Base["LegionExterminationReward"]):
    __tablename__ = 'legion_extermination_reward'

    extermination_reward_group_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class LegionMissionCategoryDatum(DeclarativeBase, Base["LegionMissionCategoryDatum"]):
    __tablename__ = 'legion_mission_category_data'

    category_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)


class LegionMissionDatum(DeclarativeBase, Base["LegionMissionDatum"]):
    __tablename__ = 'legion_mission_data'

    legion_mission_id: int = Column(Integer, primary_key=True)
    category_id: int = Column(Integer, nullable=False, index=True)
    disp_group: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    legion_boss_id: int = Column(Integer, nullable=False)
    condition_value: int = Column(Integer, nullable=False)
    condition_num: str = Column(Text, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class LegionMissionRewardDatum(DeclarativeBase, Base["LegionMissionRewardDatum"]):
    __tablename__ = 'legion_mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_num: int = Column(Integer, nullable=False)


class LegionQuestDatum(DeclarativeBase, Base["LegionQuestDatum"]):
    __tablename__ = 'legion_quest_data'

    legion_boss_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    map_type: int = Column(Integer, nullable=False, index=True)
    battle_start_story_id: int = Column(Integer, nullable=False)
    battle_finish_story_id: int = Column(Integer, nullable=False)
    disappearance_story_id: int = Column(Integer, nullable=False)
    all_disappearance_story_id: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    max_raid_hp: str = Column(Text, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)
    challenge_reward_group_id: int = Column(Integer, nullable=False)
    expel_reward_group_id: int = Column(Integer, nullable=False)
    extermination_reward_group_id: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    bg_position: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    enemy_position_x: int = Column(Integer, nullable=False)
    enemy_local_position_y: int = Column(Integer, nullable=False)
    enemy_size_1: float = Column(Float, nullable=False)
    result_boss_position_y: float = Column(Float, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)
    clear_story_id_1: int = Column(Integer, nullable=False)
    clear_story_id_2: int = Column(Integer, nullable=False)
    bonus_max: int = Column(Integer, nullable=False)


class LegionSchedule(DeclarativeBase, Base["LegionSchedule"]):
    __tablename__ = 'legion_schedule'

    id: int = Column(Integer, primary_key=True)
    teaser_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    close_time: str = Column(Text, nullable=False)
    story_id: int = Column(Integer, nullable=False)
    close_story_condition_id: int = Column(Integer, nullable=False)
    close_story_id: int = Column(Integer, nullable=False)
    top_bgm: str = Column(Text, nullable=False)
    top_bg: str = Column(Text, nullable=False)


class LegionSpecialBattle(DeclarativeBase, Base["LegionSpecialBattle"]):
    __tablename__ = 'legion_special_battle'

    mode: int = Column(Integer, primary_key=True)
    purpose_type: int = Column(Integer, nullable=False)
    purpose_count: int = Column(Integer, nullable=False)
    trigger_hp: int = Column(Integer, nullable=False)
    story_id_mode_start: int = Column(Integer, nullable=False)
    story_id_mode_end: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    unnecessary_defeat_chara: int = Column(Integer, nullable=False)
    story_start_second: float = Column(Float, nullable=False)
    action_start_second: float = Column(Float, nullable=False)
    hp_gauge_color_flag: int = Column(Integer, nullable=False)


class LoginBonusAdv(DeclarativeBase, Base["LoginBonusAdv"]):
    __tablename__ = 'login_bonus_adv'

    id: int = Column(Integer, primary_key=True)
    login_bonus_id: int = Column(Integer, nullable=False, index=True)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    count_key: int = Column(Integer, nullable=False)
    adv_id: int = Column(Integer, nullable=False)
    read_process_flag: int = Column(Integer, nullable=False)


class LoginBonusDatum(DeclarativeBase, Base["LoginBonusDatum"]):
    __tablename__ = 'login_bonus_data'

    login_bonus_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    login_bonus_type: int = Column(Integer, nullable=False)
    count_num: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    bg_id: int = Column(Integer, nullable=False)
    stamp_id: int = Column(Integer, nullable=False)
    odds_group_id: int = Column(Integer, nullable=False)
    adv_play_type: int = Column(Integer, nullable=False)
    count_type: int = Column(Integer, nullable=False)


class LoginBonusDetail(DeclarativeBase, Base["LoginBonusDetail"]):
    __tablename__ = 'login_bonus_detail'
    __table_args__ = (
        Index('login_bonus_detail_0_login_bonus_id_1_count', 'login_bonus_id', 'count'),
    )

    id: int = Column(Integer, primary_key=True)
    login_bonus_id: int = Column(Integer, nullable=False)
    count: int = Column(Integer, nullable=False)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_num: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    voice_id: int = Column(Integer, nullable=False)
    bg_id: int = Column(Integer, nullable=False)


class LoginBonusMessageDatum(DeclarativeBase, Base["LoginBonusMessageDatum"]):
    __tablename__ = 'login_bonus_message_data'

    id: int = Column(Integer, primary_key=True)
    login_bonus_id: int = Column(Integer, nullable=False, index=True)
    type: int = Column(Integer, nullable=False)
    day_count: int = Column(Integer, nullable=False)
    luck_pattern: int = Column(Integer, nullable=False)
    rate: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    message: str = Column(Text, nullable=False)
    voice_id: int = Column(Integer, nullable=False)
    additional_type: int = Column(Integer, nullable=False)
    additional_param: str = Column(Text, nullable=False)


class LoveChara(DeclarativeBase, Base["LoveChara"]):
    __tablename__ = 'love_chara'

    love_level: int = Column(Integer, primary_key=True)
    total_love: int = Column(Integer, nullable=False)
    unlocked_class: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)


class LoveRankup(DeclarativeBase, Base["LoveRankup"]):
    __tablename__ = 'love_rankup'

    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    love_rank: int = Column(Integer, primary_key=True, nullable=False)
    effect_unit_id: int = Column(Integer, nullable=False)


class LtoLetterScript(DeclarativeBase, Base["LtoLetterScript"]):
    __tablename__ = 'lto_letter_script'

    id: int = Column(Integer, primary_key=True)
    letter_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    line_num: int = Column(Integer, nullable=False)
    start_pos: int = Column(Integer, nullable=False)
    end_pos: int = Column(Integer, nullable=False)
    seek_time: float = Column(Float, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class LtoStoryDatum(DeclarativeBase, Base["LtoStoryDatum"]):
    __tablename__ = 'lto_story_data'

    sub_story_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_count: int = Column(Integer, nullable=False)


class Metamorphose(DeclarativeBase, Base["Metamorphose"]):
    __tablename__ = 'metamorphose'

    type_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    condition_value: int = Column(Integer, primary_key=True, nullable=False)
    prefab_id: int = Column(Integer, nullable=False)


class MhpDramaScript(DeclarativeBase, Base["MhpDramaScript"]):
    __tablename__ = 'mhp_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class MhpStoryDatum(DeclarativeBase, Base["MhpStoryDatum"]):
    __tablename__ = 'mhp_story_data'

    sub_story_id: int = Column(Integer, primary_key=True)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    unit_id: int = Column(Integer, nullable=False, index=True)
    read_condition_time: str = Column(Text, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    read_condition: int = Column(Integer, nullable=False)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_count: int = Column(Integer, nullable=False)


class Minigame(DeclarativeBase, Base["Minigame"]):
    __tablename__ = 'minigame'

    id: int = Column(Integer, nullable=False)
    minigame_scheme_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    release_conditions_1: int = Column(Integer, nullable=False)
    conditions_id_1: int = Column(Integer, nullable=False)
    first_time_story_id: int = Column(Integer, nullable=False)
    display_condition_type: int = Column(Integer, nullable=False)
    display_condition_id: int = Column(Integer, nullable=False)
    result_chat_condition_id: int = Column(Integer, nullable=False)
    score_unit: str = Column(Text, nullable=False)
    is_enabled_zero_score: int = Column(Integer, nullable=False)


class MissionRewardDatum(DeclarativeBase, Base["MissionRewardDatum"]):
    __tablename__ = 'mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer)
    reward_num: int = Column(Integer, nullable=False)
    lv_from: int = Column(Integer, nullable=False)
    lv_to: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class Movie(DeclarativeBase, Base["Movie"]):
    __tablename__ = 'movie'

    movie_id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False)
    story_id: int = Column(Integer, nullable=False, index=True)
    bgm_id: str = Column(Text, nullable=False)
    se_id: str = Column(Text, nullable=False)
    my_page_flag: int = Column(Integer, nullable=False)
    fade_loop_flag: int = Column(Integer, nullable=False)
    bgm_volume_rate: float = Column(Float, nullable=False)


class MusicContent(DeclarativeBase, Base["MusicContent"]):
    __tablename__ = 'music_content'

    music_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    total_playing_time: str = Column(Text, nullable=False)
    listen_start_time: str = Column(Text, nullable=False)
    detail: str = Column(Text, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    cue_id: str = Column(Text, nullable=False)


class MusicList(DeclarativeBase, Base["MusicList"]):
    __tablename__ = 'music_list'

    music_id: int = Column(Integer, primary_key=True)
    list_name: str = Column(Text, nullable=False)
    font_size: float = Column(Float, nullable=False)
    pre_shop_start: str = Column(Text, nullable=False)
    shop_start: str = Column(Text, nullable=False)
    shop_end: str = Column(Text, nullable=False)
    story_id: int = Column(Integer, nullable=False)
    cost_item_num: int = Column(Integer, nullable=False)
    sort: int = Column(Integer, nullable=False)
    kana: str = Column(Text, nullable=False)
    ios_url: str = Column(Text, nullable=False)
    android_url: str = Column(Text, nullable=False)
    dmm_url: str = Column(Text, nullable=False)


class MypageFrame(DeclarativeBase, Base["MypageFrame"]):
    __tablename__ = 'mypage_frame'

    frame_id: int = Column(Integer, primary_key=True)
    group_id: int = Column(Integer, nullable=False, index=True)
    frame_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)


class MyprofileContent(DeclarativeBase, Base["MyprofileContent"]):
    __tablename__ = 'myprofile_content'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    disp_order: int = Column(Integer, nullable=False)


class NaviComment(DeclarativeBase, Base["NaviComment"]):
    __tablename__ = 'navi_comment'

    comment_id: int = Column(Integer, primary_key=True)
    where_type: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    face_type: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    description: str = Column(Text)
    voice_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    pos_x: float = Column(Float, nullable=False)
    pos_y: float = Column(Float, nullable=False)
    change_face_time: float = Column(Float, nullable=False)
    change_face_type: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class NopDramaDatum(DeclarativeBase, Base["NopDramaDatum"]):
    __tablename__ = 'nop_drama_data'

    id: int = Column(Integer, primary_key=True)
    stage_id: int = Column(Integer, nullable=False, index=True)
    position_id_1: int = Column(Integer, nullable=False)
    position_id_2: int = Column(Integer, nullable=False)
    position_id_3: int = Column(Integer, nullable=False)
    col_size_x: int = Column(Integer, nullable=False)
    col_size_y: int = Column(Integer, nullable=False)
    col_pos_y: float = Column(Float, nullable=False)
    talk_pos_x: float = Column(Float, nullable=False)
    talk_pos_y: float = Column(Float, nullable=False)
    idle_drama_id: int = Column(Integer, nullable=False)
    talk_drama_id: int = Column(Integer, nullable=False)
    event_drama_id: int = Column(Integer, nullable=False)
    create_back_drama_id: int = Column(Integer, nullable=False)
    create_front_drama_id: int = Column(Integer, nullable=False)
    sub_story_id: int = Column(Integer, nullable=False)


class NopDramaScript(DeclarativeBase, Base["NopDramaScript"]):
    __tablename__ = 'nop_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class NotifDatum(DeclarativeBase, Base["NotifDatum"]):
    __tablename__ = 'notif_data'

    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    notif_type: int = Column(Integer, primary_key=True, nullable=False)
    comment: str = Column(Text, nullable=False)


class NyxDramaDatum(DeclarativeBase, Base["NyxDramaDatum"]):
    __tablename__ = 'nyx_drama_data'

    drama_id: int = Column(Integer, primary_key=True)
    story_phase: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    condition_unlocked_story_id: int = Column(Integer, nullable=False)
    condition_locked_story_id: int = Column(Integer, nullable=False)


class NyxDramaScript(DeclarativeBase, Base["NyxDramaScript"]):
    __tablename__ = 'nyx_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class NyxPhaseDatum(DeclarativeBase, Base["NyxPhaseDatum"]):
    __tablename__ = 'nyx_phase_data'

    story_phase: int = Column(Integer, primary_key=True)
    phase_title: str = Column(Text, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_quest_boss: int = Column(Integer, nullable=False)


class NyxStoryDatum(DeclarativeBase, Base["NyxStoryDatum"]):
    __tablename__ = 'nyx_story_data'

    story_id: int = Column(Integer, primary_key=True)
    story_seq: int = Column(Integer, nullable=False, index=True)
    story_phase: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    read_condition_time: str = Column(Text, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_count: int = Column(Integer, nullable=False)
    adv_flg: int = Column(Integer, nullable=False)
    adv_id: int = Column(Integer, nullable=False)


class NyxStoryScript(DeclarativeBase, Base["NyxStoryScript"]):
    __tablename__ = 'nyx_story_script'

    id: int = Column(Integer, primary_key=True)
    story_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    line_num: int = Column(Integer, nullable=False)
    start_pos: int = Column(Integer, nullable=False)
    end_pos: int = Column(Integer, nullable=False)
    seek_time: float = Column(Float, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class OddsNameDatum(DeclarativeBase, Base["OddsNameDatum"]):
    __tablename__ = 'odds_name_data'

    id: int = Column(Integer, primary_key=True)
    odds_file: str = Column(Text, nullable=False)
    name: str = Column(Text, nullable=False)
    icon_type: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)


class OmpDrama(DeclarativeBase, Base["OmpDrama"]):
    __tablename__ = 'omp_drama'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class OmpStoryDatum(DeclarativeBase, Base["OmpStoryDatum"]):
    __tablename__ = 'omp_story_data'

    omp_story_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    story_seq: int = Column(Integer, nullable=False, index=True)
    is_readable_on_result: int = Column(Integer, nullable=False)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_count: int = Column(Integer, nullable=False)
    sub_title: str = Column(Text, nullable=False)


class PctComboCoefficient(DeclarativeBase, Base["PctComboCoefficient"]):
    __tablename__ = 'pct_combo_coefficient'

    id: int = Column(Integer, primary_key=True)
    combo_min: int = Column(Integer, nullable=False)
    combo_max: int = Column(Integer, nullable=False)
    combo_coefficient: int = Column(Integer, nullable=False)


class PctEvaluation(DeclarativeBase, Base["PctEvaluation"]):
    __tablename__ = 'pct_evaluation'

    evaluation_id: int = Column(Integer, primary_key=True)
    evaluation_point: int = Column(Integer, nullable=False)
    fever_point: int = Column(Integer, nullable=False)
    meet_width: int = Column(Integer, nullable=False)


class PctGamingMotion(DeclarativeBase, Base["PctGamingMotion"]):
    __tablename__ = 'pct_gaming_motion'

    motion_id: int = Column(Integer, primary_key=True)
    perfect_count: int = Column(Integer, nullable=False)
    good_count: int = Column(Integer, nullable=False)
    nice_count: int = Column(Integer, nullable=False)
    point: int = Column(Integer, nullable=False)


class PctItempoint(DeclarativeBase, Base["PctItempoint"]):
    __tablename__ = 'pct_itempoint'

    id: int = Column(Integer, primary_key=True)
    item_id: int = Column(Integer, nullable=False, index=True)
    pct_point_coefficient: int = Column(Integer, nullable=False)


class PctResult(DeclarativeBase, Base["PctResult"]):
    __tablename__ = 'pct_result'

    id: int = Column(Integer, primary_key=True)
    character_id: int = Column(Integer, nullable=False, index=True)
    score_from: int = Column(Integer, nullable=False)
    score_to: int = Column(Integer, nullable=False)
    comment_id_1: int = Column(Integer, nullable=False)
    comment_id_2: int = Column(Integer, nullable=False)
    comment_id_3: int = Column(Integer, nullable=False)
    comment_id_4: int = Column(Integer, nullable=False)
    comment_id_5: int = Column(Integer, nullable=False)


class PctReward(DeclarativeBase, Base["PctReward"]):
    __tablename__ = 'pct_reward'

    id: int = Column(Integer, primary_key=True)
    pct_point_type: int = Column(Integer, nullable=False, index=True)
    pct_point: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class PctSystem(DeclarativeBase, Base["PctSystem"]):
    __tablename__ = 'pct_system'

    id: int = Column(Integer, primary_key=True)
    pct_base_speed: int = Column(Integer, nullable=False)
    fever_point_max: int = Column(Integer, nullable=False)
    fever_time: int = Column(Integer, nullable=False)
    fever_revention_time: int = Column(Integer, nullable=False)
    pct_time: int = Column(Integer, nullable=False)
    chara1: int = Column(Integer, nullable=False)
    chara2: int = Column(Integer, nullable=False)
    chara1_gauge_choice: int = Column(Integer, nullable=False)
    chara2_gauge_choice: int = Column(Integer, nullable=False)


class PctSystemFruit(DeclarativeBase, Base["PctSystemFruit"]):
    __tablename__ = 'pct_system_fruits'

    id: int = Column(Integer, primary_key=True)
    last_time: int = Column(Integer, nullable=False)
    appearance: int = Column(Integer, nullable=False)
    bar_split: int = Column(Integer, nullable=False)
    appearance_chara_odds: int = Column(Integer, nullable=False)
    appearance_pattern: str = Column(Text, nullable=False)
    wait_time: int = Column(Integer, nullable=False)


class PctTapSpeed(DeclarativeBase, Base["PctTapSpeed"]):
    __tablename__ = 'pct_tap_speed'

    id: int = Column(Integer, primary_key=True)
    combo_count: int = Column(Integer, nullable=False)
    speed_magnification: int = Column(Integer, nullable=False)


class PkbBatterCondition(DeclarativeBase, Base["PkbBatterCondition"]):
    __tablename__ = 'pkb_batter_condition'

    batter_id: int = Column(Integer, primary_key=True)
    pkb_score: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)
    detail: str = Column(Text, nullable=False)
    meet: int = Column(Integer, nullable=False)
    critical: int = Column(Integer, nullable=False)
    power: int = Column(Integer, nullable=False)
    ability_name: str = Column(Text, nullable=False)
    ability_detail: str = Column(Text, nullable=False)
    is_playable: int = Column(Integer, nullable=False)


class PkbDrama(DeclarativeBase, Base["PkbDrama"]):
    __tablename__ = 'pkb_drama'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class PkbDramaDatum(DeclarativeBase, Base["PkbDramaDatum"]):
    __tablename__ = 'pkb_drama_data'

    drama_id: int = Column(Integer, primary_key=True)
    condition_pitcher_id_1: int = Column(Integer, nullable=False)
    condition_pitcher_id_2: int = Column(Integer, nullable=False)
    condition_batter_id_1: int = Column(Integer, nullable=False)
    condition_batter_id_2: int = Column(Integer, nullable=False)


class PkbNaviComment(DeclarativeBase, Base["PkbNaviComment"]):
    __tablename__ = 'pkb_navi_comment'

    comment_id: int = Column(Integer, primary_key=True)
    where_type: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    face_type: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    description: str = Column(Text)
    voice_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    pos_x: float = Column(Float, nullable=False)
    pos_y: float = Column(Float, nullable=False)
    change_face_time: float = Column(Float, nullable=False)
    change_face_type: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class PkbPitcherBallType(DeclarativeBase, Base["PkbPitcherBallType"]):
    __tablename__ = 'pkb_pitcher_ball_type'

    pitcher_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    ball_type: int = Column(Integer, primary_key=True, nullable=False)
    ball_type_name: str = Column(Text, nullable=False)


class PkbReward(DeclarativeBase, Base["PkbReward"]):
    __tablename__ = 'pkb_reward'

    id: int = Column(Integer, primary_key=True)
    pkb_score: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class PositionSetting(DeclarativeBase, Base["PositionSetting"]):
    __tablename__ = 'position_setting'

    position_setting_id: int = Column(Integer, primary_key=True)
    front: int = Column(Integer, nullable=False)
    middle: int = Column(Integer, nullable=False)


class PrizegachaDatum(DeclarativeBase, Base["PrizegachaDatum"]):
    __tablename__ = 'prizegacha_data'

    prizegacha_id: int = Column(Integer, primary_key=True)
    prize_memory_id_1: int = Column(Integer, nullable=False)
    prize_memory_id_2: int = Column(Integer, nullable=False)
    prize_memory_id_3: int = Column(Integer, nullable=False)
    prize_memory_id_4: int = Column(Integer, nullable=False)
    prize_memory_id_5: int = Column(Integer, nullable=False)
    prize_memory_id_6: int = Column(Integer, nullable=False)
    prize_memory_id_7: int = Column(Integer, nullable=False)
    prize_memory_id_8: int = Column(Integer, nullable=False)
    prize_memory_id_9: int = Column(Integer, nullable=False)
    prize_memory_id_10: int = Column(Integer, nullable=False)
    prize_memory_id_11: int = Column(Integer, nullable=False)
    prize_memory_id_12: int = Column(Integer, nullable=False)
    prize_memory_id_13: int = Column(Integer, nullable=False)
    prize_memory_id_14: int = Column(Integer, nullable=False)
    prize_memory_id_15: int = Column(Integer, nullable=False)
    prize_memory_id_16: int = Column(Integer, nullable=False)
    prize_memory_id_17: int = Column(Integer, nullable=False)
    prize_memory_id_18: int = Column(Integer, nullable=False)
    prize_memory_id_19: int = Column(Integer, nullable=False)
    prize_memory_id_20: int = Column(Integer, nullable=False)
    gacha_prize1: int = Column(Integer, nullable=False)
    gacha_prize10: int = Column(Integer, nullable=False)
    prize_fixed_compensation: int = Column(Integer, nullable=False)
    prize_fixed_compensation_quantity: int = Column(Integer, nullable=False)
    rarity_odds: int = Column(Integer, nullable=False)
    disp_prize_fixed_compensation: int = Column(Integer, nullable=False)


class PrizegachaSpDatum(DeclarativeBase, Base["PrizegachaSpDatum"]):
    __tablename__ = 'prizegacha_sp_data'

    gacha_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    rarity: int = Column(Integer, primary_key=True, nullable=False)
    disp_rarity: int = Column(Integer, nullable=False)


class PrizegachaSpDetail(DeclarativeBase, Base["PrizegachaSpDetail"]):
    __tablename__ = 'prizegacha_sp_detail'

    disp_rarity: int = Column(Integer, primary_key=True)
    effect_id: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)


class ProfileFrame(DeclarativeBase, Base["ProfileFrame"]):
    __tablename__ = 'profile_frame'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    type: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    disp_order: int = Column(Integer, nullable=False)


class PromotionBonu(DeclarativeBase, Base["PromotionBonu"]):
    __tablename__ = 'promotion_bonus'

    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    promotion_level: int = Column(Integer, primary_key=True, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class PsyDrama(DeclarativeBase, Base["PsyDrama"]):
    __tablename__ = 'psy_drama'

    drama_id: int = Column(Integer, primary_key=True)
    condition_total_eat: int = Column(Integer, nullable=False)
    condition_chara_type: int = Column(Integer, nullable=False)
    condition_time: str = Column(Text, nullable=False)
    condition_psy_product_1: int = Column(Integer, nullable=False)
    condition_psy_product_2: int = Column(Integer, nullable=False)
    condition_psy_product_3: int = Column(Integer, nullable=False)
    condition_psy_product_4: int = Column(Integer, nullable=False)
    condition_psy_product_5: int = Column(Integer, nullable=False)
    release_psy_product_id_1: int = Column(Integer, nullable=False)
    release_psy_product_id_2: int = Column(Integer, nullable=False)
    release_psy_product_id_3: int = Column(Integer, nullable=False)
    release_psy_product_id_4: int = Column(Integer, nullable=False)
    release_psy_product_id_5: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)


class PsyDramaScript(DeclarativeBase, Base["PsyDramaScript"]):
    __tablename__ = 'psy_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class PsyNote(DeclarativeBase, Base["PsyNote"]):
    __tablename__ = 'psy_note'

    psy_product_id: int = Column(Integer, primary_key=True)
    condition_flavor_1: int = Column(Integer, nullable=False)
    condition_flavor_2: int = Column(Integer, nullable=False)
    psy_product_name: str = Column(Text, nullable=False)
    flavor_1: str = Column(Text, nullable=False)
    flavor_2: str = Column(Text, nullable=False)
    flavor_3: str = Column(Text, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    init_flg: int = Column(Integer, nullable=False)


class PsyReward(DeclarativeBase, Base["PsyReward"]):
    __tablename__ = 'psy_reward'

    id: int = Column(Integer, primary_key=True)
    condition_type: int = Column(Integer, nullable=False)
    condition_num: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)


class QuestAnnihilation(DeclarativeBase, Base["QuestAnnihilation"]):
    __tablename__ = 'quest_annihilation'

    system_id: int = Column(Integer, primary_key=True, nullable=False)
    quest_id: int = Column(Integer, primary_key=True, nullable=False)
    effect_type: int = Column(Integer, nullable=False)
    quest_effect_position: int = Column(Integer, nullable=False)
    se_cue_name: str = Column(Text, nullable=False)


class QuestAreaDatum(DeclarativeBase, Base["QuestAreaDatum"]):
    __tablename__ = 'quest_area_data'

    area_id: int = Column(Integer, primary_key=True)
    area_name: str = Column(Text, nullable=False)
    area_display_name: str = Column(Text, nullable=False)
    map_type: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class QuestConditionDatum(DeclarativeBase, Base["QuestConditionDatum"]):
    __tablename__ = 'quest_condition_data'

    quest_id: int = Column(Integer, primary_key=True)
    condition_quest_id_1: int = Column(Integer, nullable=False)
    condition_quest_id_2: int = Column(Integer, nullable=False)
    condition_quest_id_3: int = Column(Integer, nullable=False)
    condition_quest_id_4: int = Column(Integer, nullable=False)
    condition_quest_id_5: int = Column(Integer, nullable=False)
    release_quest_id_1: int = Column(Integer, nullable=False)
    release_quest_id_2: int = Column(Integer, nullable=False)
    release_quest_id_3: int = Column(Integer, nullable=False)
    release_quest_id_4: int = Column(Integer, nullable=False)
    release_quest_id_5: int = Column(Integer, nullable=False)


class QuestDatum(DeclarativeBase, Base["QuestDatum"]):
    __tablename__ = 'quest_data'

    quest_id: int = Column(Integer, primary_key=True)
    area_id: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    limit_team_level: int = Column(Integer, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    stamina: int = Column(Integer, nullable=False)
    stamina_start: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    unit_exp: int = Column(Integer, nullable=False)
    love: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    daily_limit: int = Column(Integer, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)
    rank_reward_group: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    story_id_wavestart_1: int = Column(Integer, nullable=False)
    story_id_waveend_1: int = Column(Integer, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2: str = Column(Text, nullable=False)
    wave_bgm_que_id_2: str = Column(Text, nullable=False)
    story_id_wavestart_2: int = Column(Integer, nullable=False)
    story_id_waveend_2: int = Column(Integer, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3: str = Column(Text, nullable=False)
    wave_bgm_que_id_3: str = Column(Text, nullable=False)
    story_id_wavestart_3: int = Column(Integer, nullable=False)
    story_id_waveend_3: int = Column(Integer, nullable=False)
    enemy_image_1: int = Column(Integer, nullable=False)
    enemy_image_2: int = Column(Integer, nullable=False)
    enemy_image_3: int = Column(Integer, nullable=False)
    enemy_image_4: int = Column(Integer, nullable=False)
    enemy_image_5: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    lv_reward_flag: int = Column(Integer, nullable=False)
    add_treasure_num: int = Column(Integer, nullable=False)

    def get_wave_group_ids(self) -> Iterator[int]:
        yield self.wave_group_id_1
        yield self.wave_group_id_2
        yield self.wave_group_id_3

class QuestDefeatNotice(DeclarativeBase, Base["QuestDefeatNotice"]):
    __tablename__ = 'quest_defeat_notice'

    id: int = Column(Integer, primary_key=True)
    image_id: int = Column(Integer, nullable=False)
    required_team_level: int = Column(Integer, nullable=False)
    required_quest_id: int = Column(Integer, nullable=False)


class QuestRewardDatum(DeclarativeBase, Base["QuestRewardDatum"]):
    __tablename__ = 'quest_reward_data'

    reward_group_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class Rarity6QuestDatum(DeclarativeBase, Base["Rarity6QuestDatum"]):
    __tablename__ = 'rarity_6_quest_data'

    rarity_6_quest_id: int = Column(Integer, nullable=False, index=True)
    unit_id: int = Column(Integer, primary_key=True)
    quest_name: str = Column(Text, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    recommended_level: int = Column(Integer, nullable=False)
    reward_group_id: int = Column(Integer, nullable=False)
    treasure_type: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    bg_position: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    enemy_position_x_1: int = Column(Integer, nullable=False)
    enemy_local_position_y_1: int = Column(Integer, nullable=False)
    enemy_size_1: float = Column(Float, nullable=False)
    enemy_position_x_2: int = Column(Integer, nullable=False)
    enemy_local_position_y_2: int = Column(Integer, nullable=False)
    enemy_size_2: float = Column(Float, nullable=False)
    enemy_position_x_3: int = Column(Integer, nullable=False)
    enemy_local_position_y_3: int = Column(Integer, nullable=False)
    enemy_size_3: float = Column(Float, nullable=False)
    enemy_position_x_4: int = Column(Integer, nullable=False)
    enemy_local_position_y_4: int = Column(Integer, nullable=False)
    enemy_size_4: float = Column(Float, nullable=False)
    enemy_position_x_5: int = Column(Integer, nullable=False)
    enemy_local_position_y_5: int = Column(Integer, nullable=False)
    enemy_size_5: float = Column(Float, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)


class RedeemStaticPriceGroup(DeclarativeBase, Base["RedeemStaticPriceGroup"]):
    __tablename__ = 'redeem_static_price_group'

    condition_category: int = Column(Integer, primary_key=True)
    count: int = Column(Integer, nullable=False)


class RedeemUnit(DeclarativeBase, Base["RedeemUnit"]):
    __tablename__ = 'redeem_unit'

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False, index=True)
    slot_id: int = Column(Integer, nullable=False)
    condition_category: int = Column(Integer, nullable=False)
    condition_id: int = Column(Integer, nullable=False)
    consume_num: str = Column(Text, nullable=False)


class RedeemUnitBg(DeclarativeBase, Base["RedeemUnitBg"]):
    __tablename__ = 'redeem_unit_bg'

    unit_id: int = Column(Integer, primary_key=True)
    bg_id: int = Column(Integer, nullable=False)


class ResistDatum(DeclarativeBase, Base["ResistDatum"]):
    __tablename__ = 'resist_data'

    resist_status_id: int = Column(Integer, primary_key=True)
    ailment_1: int = Column(Integer, nullable=False)
    ailment_2: int = Column(Integer, nullable=False)
    ailment_3: int = Column(Integer, nullable=False)
    ailment_4: int = Column(Integer, nullable=False)
    ailment_5: int = Column(Integer, nullable=False)
    ailment_6: int = Column(Integer, nullable=False)
    ailment_7: int = Column(Integer, nullable=False)
    ailment_8: int = Column(Integer, nullable=False)
    ailment_9: int = Column(Integer, nullable=False)
    ailment_10: int = Column(Integer, nullable=False)
    ailment_11: int = Column(Integer, nullable=False)
    ailment_12: int = Column(Integer, nullable=False)
    ailment_13: int = Column(Integer, nullable=False)
    ailment_14: int = Column(Integer, nullable=False)
    ailment_15: int = Column(Integer, nullable=False)
    ailment_16: int = Column(Integer, nullable=False)
    ailment_17: int = Column(Integer, nullable=False)
    ailment_18: int = Column(Integer, nullable=False)
    ailment_19: int = Column(Integer, nullable=False)
    ailment_20: int = Column(Integer, nullable=False)
    ailment_21: int = Column(Integer, nullable=False)
    ailment_22: int = Column(Integer, nullable=False)
    ailment_23: int = Column(Integer, nullable=False)
    ailment_24: int = Column(Integer, nullable=False)
    ailment_25: int = Column(Integer, nullable=False)
    ailment_26: int = Column(Integer, nullable=False)
    ailment_27: int = Column(Integer, nullable=False)
    ailment_28: int = Column(Integer, nullable=False)
    ailment_29: int = Column(Integer, nullable=False)
    ailment_30: int = Column(Integer, nullable=False)
    ailment_31: int = Column(Integer, nullable=False)
    ailment_32: int = Column(Integer, nullable=False)
    ailment_33: int = Column(Integer, nullable=False)
    ailment_34: int = Column(Integer, nullable=False)
    ailment_35: int = Column(Integer, nullable=False)
    ailment_36: int = Column(Integer, nullable=False)
    ailment_37: int = Column(Integer, nullable=False)
    ailment_38: int = Column(Integer, nullable=False)
    ailment_39: int = Column(Integer, nullable=False)
    ailment_40: int = Column(Integer, nullable=False)
    ailment_41: int = Column(Integer, nullable=False)
    ailment_42: int = Column(Integer, nullable=False)
    ailment_43: int = Column(Integer, nullable=False)
    ailment_44: int = Column(Integer, nullable=False)
    ailment_45: int = Column(Integer, nullable=False)
    ailment_46: int = Column(Integer, nullable=False)
    ailment_47: int = Column(Integer, nullable=False)
    ailment_48: int = Column(Integer, nullable=False)
    ailment_49: int = Column(Integer, nullable=False)
    ailment_50: int = Column(Integer, nullable=False)


class ResistVariationDatum(DeclarativeBase, Base["ResistVariationDatum"]):
    __tablename__ = 'resist_variation_data'

    resist_variation_id: int = Column(Integer, primary_key=True)
    value_1: int = Column(Integer, nullable=False)
    value_2: int = Column(Integer, nullable=False)
    value_3: int = Column(Integer, nullable=False)
    value_4: int = Column(Integer, nullable=False)


class ReturnSpecialfesBanner(DeclarativeBase, Base["ReturnSpecialfesBanner"]):
    __tablename__ = 'return_specialfes_banner'

    gacha_id: int = Column(Integer, primary_key=True)
    banner_id_1: int = Column(Integer, nullable=False)
    banner_id_2: int = Column(Integer, nullable=False)
    banner_id_3: int = Column(Integer, nullable=False)
    banner_id_4: int = Column(Integer, nullable=False)
    banner_id_5: int = Column(Integer, nullable=False)
    banner_id_6: int = Column(Integer, nullable=False)
    banner_id_7: int = Column(Integer, nullable=False)
    banner_id_8: int = Column(Integer, nullable=False)
    banner_id_9: int = Column(Integer, nullable=False)
    banner_id_10: int = Column(Integer, nullable=False)


class RewardCollectGuide(DeclarativeBase, Base["RewardCollectGuide"]):
    __tablename__ = 'reward_collect_guide'

    object_id: int = Column(Integer, primary_key=True)
    quest_id_1: int = Column(Integer, nullable=False)
    quest_id_2: int = Column(Integer, nullable=False)
    quest_id_3: int = Column(Integer, nullable=False)
    quest_id_4: int = Column(Integer, nullable=False)
    quest_id_5: int = Column(Integer, nullable=False)
    quest_id_6: int = Column(Integer, nullable=False)
    quest_id_7: int = Column(Integer, nullable=False)
    quest_id_8: int = Column(Integer, nullable=False)
    quest_id_9: int = Column(Integer, nullable=False)
    quest_id_10: int = Column(Integer, nullable=False)
    system_id_1: int = Column(Integer, nullable=False)
    system_id_2: int = Column(Integer, nullable=False)
    system_id_3: int = Column(Integer, nullable=False)
    system_id_4: int = Column(Integer, nullable=False)
    system_id_5: int = Column(Integer, nullable=False)


class RoomChange(DeclarativeBase, Base["RoomChange"]):
    __tablename__ = 'room_change'

    room_item_id: int = Column(Integer, primary_key=True)
    change_id: int = Column(Integer, nullable=False)
    change_start: str = Column(Text, nullable=False)
    change_end: str = Column(Text, nullable=False)


class RoomCharacterPersonality(DeclarativeBase, Base["RoomCharacterPersonality"]):
    __tablename__ = 'room_character_personality'

    character_id: int = Column(Integer, primary_key=True)
    personality_id: int = Column(Integer, nullable=False)


class RoomCharacterSkinColor(DeclarativeBase, Base["RoomCharacterSkinColor"]):
    __tablename__ = 'room_character_skin_color'

    character_id: int = Column(Integer, primary_key=True)
    skin_color_id: int = Column(Integer, nullable=False)


class RoomChatFormation(DeclarativeBase, Base["RoomChatFormation"]):
    __tablename__ = 'room_chat_formation'

    id: int = Column(Integer, primary_key=True)
    unit_1_x: int = Column(Integer, nullable=False)
    unit_1_y: int = Column(Integer, nullable=False)
    unit_1_dir: int = Column(Integer, nullable=False)
    unit_2_x: int = Column(Integer, nullable=False)
    unit_2_y: int = Column(Integer, nullable=False)
    unit_2_dir: int = Column(Integer, nullable=False)
    unit_3_x: int = Column(Integer)
    unit_3_y: int = Column(Integer)
    unit_3_dir: int = Column(Integer)
    unit_4_x: int = Column(Integer)
    unit_4_y: int = Column(Integer)
    unit_4_dir: int = Column(Integer)
    unit_5_x: int = Column(Integer)
    unit_5_y: int = Column(Integer)
    unit_5_dir: int = Column(Integer)
    unit_num: int = Column(Integer, nullable=False)
    unit_id1: int = Column(Integer)
    unit_id2: int = Column(Integer)
    unit_id3: int = Column(Integer)
    unit_id4: int = Column(Integer)
    unit_id5: int = Column(Integer)
    ignore_unit_id1: int = Column(Integer)
    ignore_unit_id2: int = Column(Integer)
    ignore_unit_id3: int = Column(Integer)
    ignore_unit_id4: int = Column(Integer)
    ignore_unit_id5: int = Column(Integer)


class RoomChatInfo(DeclarativeBase, Base["RoomChatInfo"]):
    __tablename__ = 'room_chat_info'

    id: int = Column(Integer, primary_key=True)
    formation_id: int = Column(Integer, nullable=False)
    scenario_id: int = Column(Integer, nullable=False)


class RoomChatScenario(DeclarativeBase, Base["RoomChatScenario"]):
    __tablename__ = 'room_chat_scenario'

    id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    scenario_idx: int = Column(Integer, primary_key=True, nullable=False)
    unit_pos_no: int = Column(Integer, nullable=False)
    delay: int = Column(Integer, nullable=False)
    affect_type: int = Column(Integer, nullable=False)
    anime_id: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)


class RoomEffect(DeclarativeBase, Base["RoomEffect"]):
    __tablename__ = 'room_effect'

    id: int = Column(Integer, primary_key=True)
    reward_get: int = Column(Integer, nullable=False)
    jukebox: int = Column(Integer, nullable=False)
    nebbia: int = Column(Integer, nullable=False)
    arcade: int = Column(Integer, nullable=False)
    vegetable: int = Column(Integer, nullable=False)
    poster: int = Column(Integer, nullable=False)
    stock: int = Column(Integer, nullable=False)


class RoomEffectRewardGet(DeclarativeBase, Base["RoomEffectRewardGet"]):
    __tablename__ = 'room_effect_reward_get'

    id: int = Column(Integer, primary_key=True, nullable=False)
    level: int = Column(Integer, primary_key=True, nullable=False)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    max_count: int = Column(Integer, nullable=False)
    inc_step: int = Column(Integer, nullable=False)
    interval_second: int = Column(Integer, nullable=False)
    stock_min_step: str = Column(Text, nullable=False)
    stock_mid_step: str = Column(Text, nullable=False)


class RoomEmotionIcon(DeclarativeBase, Base["RoomEmotionIcon"]):
    __tablename__ = 'room_emotion_icon'

    id: int = Column(Integer, primary_key=True)
    enable_auto: int = Column(Integer, nullable=False)
    enable_tap: int = Column(Integer, nullable=False)


class RoomExclusiveCondition(DeclarativeBase, Base["RoomExclusiveCondition"]):
    __tablename__ = 'room_exclusive_condition'

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False, index=True)
    room_item_id: int = Column(Integer, nullable=False, index=True)
    notification: str = Column(Text, nullable=False)


class RoomItem(DeclarativeBase, Base["RoomItem"]):
    __tablename__ = 'room_item'

    id: int = Column(Integer, primary_key=True)
    item_type: int = Column(Integer, nullable=False)
    category: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)
    max_level: int = Column(Integer, nullable=False)
    enable_remove: int = Column(Integer, nullable=False)
    max_possession_num: int = Column(Integer, nullable=False)
    effect_id_1: int = Column(Integer, nullable=False)
    shop_start: str = Column(Text, nullable=False)
    shop_end: str = Column(Text, nullable=False)
    shop_new_disp_end: str = Column(Text, nullable=False)
    cost_item_num: int = Column(Integer, nullable=False)
    shop_open_type: int = Column(Integer, nullable=False)
    shop_open_id: int = Column(Integer, nullable=False)
    shop_open_value: int = Column(Integer, nullable=False)
    sold_price: int = Column(Integer, nullable=False)
    sort: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    category_action_type: int = Column(Integer, nullable=False)


class RoomItemAnnouncement(DeclarativeBase, Base["RoomItemAnnouncement"]):
    __tablename__ = 'room_item_announcement'

    id: int = Column(Integer, primary_key=True)
    announcement_start: str = Column(Text, nullable=False)
    announcement_end: str = Column(Text, nullable=False)
    announcement_text: str = Column(Text, nullable=False)


class RoomItemDetail(DeclarativeBase, Base["RoomItemDetail"]):
    __tablename__ = 'room_item_detail'
    __table_args__ = (
        Index('room_item_detail_0_lvup_trigger_type_1_lvup_trigger_id', 'lvup_trigger_type', 'lvup_trigger_id'),
        Index('room_item_detail_0_lvup_trigger_type_2_1_lvup_trigger_id_2', 'lvup_trigger_type_2', 'lvup_trigger_id_2')
    )

    room_item_id: int = Column(Integer, primary_key=True, nullable=False)
    level: int = Column(Integer, primary_key=True, nullable=False)
    item_detail: str = Column(Text, nullable=False)
    lvup_trigger_type: int = Column(Integer, nullable=False)
    lvup_trigger_id: int = Column(Integer, nullable=False)
    lvup_trigger_value: int = Column(Integer, nullable=False)
    lvup_trigger_type_2: int = Column(Integer, nullable=False)
    lvup_trigger_id_2: int = Column(Integer, nullable=False)
    lvup_trigger_value_2: int = Column(Integer, nullable=False)
    lvup_item1_type: int = Column(Integer, nullable=False)
    lvup_item1_id: int = Column(Integer, nullable=False)
    lvup_item1_num: int = Column(Integer, nullable=False)
    lvup_time: int = Column(Integer, nullable=False)


class RoomItemGetAnnouncement(DeclarativeBase, Base["RoomItemGetAnnouncement"]):
    __tablename__ = 'room_item_get_announcement'

    id: int = Column(Integer, primary_key=True)
    room_item_id: int = Column(Integer, nullable=False)
    start_date: str = Column(Text, nullable=False)
    end_date: str = Column(Text, nullable=False)
    get_date: str = Column(Text, nullable=False)
    room_announcement_name: str = Column(Text, nullable=False)


class RoomReleaseDatum(DeclarativeBase, Base["RoomReleaseDatum"]):
    __tablename__ = 'room_release_data'

    system_id: int = Column(Integer, primary_key=True)
    story_id: int = Column(Integer, nullable=False)
    pre_story_id: int = Column(Integer, nullable=False)


class RoomSetup(DeclarativeBase, Base["RoomSetup"]):
    __tablename__ = 'room_setup'

    room_item_id: int = Column(Integer, primary_key=True)
    grid_height: int = Column(Integer, nullable=False)
    grid_width: int = Column(Integer, nullable=False)
    unit_id: int = Column(Integer, nullable=False)


class RoomSkinColor(DeclarativeBase, Base["RoomSkinColor"]):
    __tablename__ = 'room_skin_color'

    skin_color_id: int = Column(Integer, primary_key=True)
    color_red: int = Column(Integer, nullable=False)
    color_green: int = Column(Integer, nullable=False)
    color_blue: int = Column(Integer, nullable=False)


class RoomUnitComment(DeclarativeBase, Base["RoomUnitComment"]):
    __tablename__ = 'room_unit_comments'

    id: int = Column(Integer, nullable=False)
    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    trigger: int = Column(Integer, primary_key=True, nullable=False)
    voice_id: int = Column(Integer, primary_key=True, nullable=False)
    beloved_step: int = Column(Integer, nullable=False)
    time: int = Column(Integer, primary_key=True, nullable=False)
    face_id: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    insert_word_type: int = Column(Integer, nullable=False)


class SdNaviComment(DeclarativeBase, Base["SdNaviComment"]):
    __tablename__ = 'sd_navi_comment'

    comment_id: int = Column(Integer, primary_key=True)
    where_type: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    motion_type: int = Column(Integer, nullable=False)
    description: str = Column(Text)
    voice_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class SeasonPack(DeclarativeBase, Base["SeasonPack"]):
    __tablename__ = 'season_pack'

    id: int = Column(Integer, primary_key=True)
    mission_id: int = Column(Integer, nullable=False, index=True)
    disp_order: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    receive_text: str = Column(Text, nullable=False)
    after_text: str = Column(Text, nullable=False)
    gift_message_id: int = Column(Integer, nullable=False)
    term: int = Column(Integer, nullable=False)
    repurchase_day: int = Column(Integer, nullable=False)
    group_id: int = Column(Integer, nullable=False)
    system_id_1: int = Column(Integer, nullable=False)
    add_num_1: int = Column(Integer, nullable=False)
    item_record_id: int = Column(Integer, nullable=False)
    condition_flg: int = Column(Integer, nullable=False)
    reward_rate_1: int = Column(Integer, nullable=False)


class SeasonpassFoundation(DeclarativeBase, Base["SeasonpassFoundation"]):
    __tablename__ = 'seasonpass_foundation'

    season_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    key_jewel_id: int = Column(Integer, nullable=False)
    advance_jewel_id: int = Column(Integer, nullable=False)
    final_jewel_id: int = Column(Integer, nullable=False)
    extra_level: int = Column(Integer, nullable=False)
    per_level_point: int = Column(Integer, nullable=False)
    level_max: int = Column(Integer, nullable=False)
    weekly_point: int = Column(Integer, nullable=False)
    level_price: int = Column(Integer, nullable=False)
    point_change_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    proportion: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    limit_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class SeasonpassLevelReward(DeclarativeBase, Base["SeasonpassLevelReward"]):
    __tablename__ = 'seasonpass_level_reward'

    level_id: int = Column(Integer, primary_key=True)
    degree: int = Column(Integer, nullable=False)
    free_reward_type: int = Column(Integer, nullable=False)
    free_reward_id: int = Column(Integer, nullable=False)
    free_reward_num: int = Column(Integer, nullable=False)
    charge_reward_type_1: int = Column(Integer, nullable=False)
    charge_reward_id_1: int = Column(Integer, nullable=False)
    charge_reward_num_1: int = Column(Integer, nullable=False)
    charge_reward_type_2: int = Column(Integer, nullable=False)
    charge_reward_id_2: int = Column(Integer, nullable=False)
    charge_reward_num_2: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class SeasonpassMissionDatum(DeclarativeBase, Base["SeasonpassMissionDatum"]):
    __tablename__ = 'seasonpass_mission_data'

    seasonpass_mission_id: int = Column(Integer, primary_key=True)
    mission_type: int = Column(Integer, nullable=False)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_value_4: int = Column(Integer)
    condition_value_5: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class SeasonpassMissionRewardDatum(DeclarativeBase, Base["SeasonpassMissionRewardDatum"]):
    __tablename__ = 'seasonpass_mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer)
    reward_num: int = Column(Integer, nullable=False)


class SecretDungeonEmblemMission(DeclarativeBase, Base["SecretDungeonEmblemMission"]):
    __tablename__ = 'secret_dungeon_emblem_mission'

    mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    mission_description: str = Column(Text, nullable=False)
    emblem_description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer, nullable=False)
    condition_value_2: int = Column(Integer, nullable=False)
    condition_value_3: int = Column(Integer, nullable=False)
    condition_num: str = Column(Text, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    dungeon_area_id: int = Column(Integer, nullable=False)
    visible_flag: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class SecretDungeonEmblemReward(DeclarativeBase, Base["SecretDungeonEmblemReward"]):
    __tablename__ = 'secret_dungeon_emblem_reward'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False, index=True)
    reward_num: int = Column(Integer, nullable=False)
    icon_type: int = Column(Integer, nullable=False)


class SecretDungeonFloorReward(DeclarativeBase, Base["SecretDungeonFloorReward"]):
    __tablename__ = 'secret_dungeon_floor_reward'

    dungeon_area_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    clear_count: int = Column(Integer, primary_key=True, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    clear_effect_flag: int = Column(Integer, nullable=False)
    icon_type: int = Column(Integer, nullable=False)


class SecretDungeonFloorSetting(DeclarativeBase, Base["SecretDungeonFloorSetting"]):
    __tablename__ = 'secret_dungeon_floor_setting'
    __table_args__ = (
        Index('secret_dungeon_floor_setting_0_quest_id_1_mode', 'quest_id', 'mode'),
    )

    id: int = Column(Integer, primary_key=True)
    quest_id: int = Column(Integer, nullable=False, index=True)
    enemy_identify: int = Column(Integer, nullable=False)
    mode: int = Column(Integer, nullable=False)
    enemy_id: int = Column(Integer, nullable=False)
    floor_position_x: float = Column(Float, nullable=False)
    floor_position_y: float = Column(Float, nullable=False)
    floor_scale: float = Column(Float, nullable=False)
    disp_order: int = Column(Integer, nullable=False)


class SecretDungeonQuestDatum(DeclarativeBase, Base["SecretDungeonQuestDatum"]):
    __tablename__ = 'secret_dungeon_quest_data'
    __table_args__ = (
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num'),
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_difficulty', 'dungeon_area_id', 'difficulty')
    )

    quest_id: int = Column(Integer, primary_key=True)
    dungeon_area_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    floor_num: int = Column(Integer, nullable=False)
    quest_type: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    parts_hp_save_flag: int = Column(Integer, nullable=False)
    energy_reset_flag: int = Column(Integer, nullable=False)
    fixed_start_tp_rate: int = Column(Integer, nullable=False)
    emax: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_image_6: int = Column(Integer, nullable=False)
    reward_coin: int = Column(Integer, nullable=False)
    reward_csc: int = Column(Integer, nullable=False)
    chest_id: int = Column(Integer, nullable=False)
    odds_group_id: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_id: int = Column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: int = Column(Integer, nullable=False)
    dungeon_quest_detail_monster_size: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_1: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_2: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_3: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_4: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_position_x_5: float = Column(Float, nullable=False)
    dungeon_quest_detail_monster_height: float = Column(Float, nullable=False)
    multi_target_effect_time: float = Column(Float, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)


class SecretDungeonSchedule(DeclarativeBase, Base["SecretDungeonSchedule"]):
    __tablename__ = 'secret_dungeon_schedule'

    dungeon_area_id: int = Column(Integer, primary_key=True)
    teaser_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    close_time: str = Column(Text, nullable=False)


class SekaiAddTimesDatum(DeclarativeBase, Base["SekaiAddTimesDatum"]):
    __tablename__ = 'sekai_add_times_data'

    id: int = Column(Integer, primary_key=True)
    sekai_id: int = Column(Integer, nullable=False)
    add_times: int = Column(Integer, nullable=False)
    add_times_limit: int = Column(Integer, nullable=False)
    add_times_time: str = Column(Text, nullable=False)
    duration: int = Column(Integer, nullable=False)


class SekaiBossDamageRankReward(DeclarativeBase, Base["SekaiBossDamageRankReward"]):
    __tablename__ = 'sekai_boss_damage_rank_reward'

    id: int = Column(Integer, primary_key=True)
    damage_rank_id: int = Column(Integer, nullable=False)
    ranking_from: int = Column(Integer, nullable=False)
    ranking_to: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class SekaiBossFixReward(DeclarativeBase, Base["SekaiBossFixReward"]):
    __tablename__ = 'sekai_boss_fix_reward'

    sekai_id: int = Column(Integer, nullable=False)
    fix_reward_group_id: int = Column(Integer, nullable=False)
    fix_reward_id: int = Column(Integer, primary_key=True)
    boss_total_damage: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    reward_type_6: int = Column(Integer, nullable=False)
    reward_id_6: int = Column(Integer, nullable=False)
    reward_num_6: int = Column(Integer, nullable=False)
    reward_type_7: int = Column(Integer, nullable=False)
    reward_id_7: int = Column(Integer, nullable=False)
    reward_num_7: int = Column(Integer, nullable=False)
    reward_type_8: int = Column(Integer, nullable=False)
    reward_id_8: int = Column(Integer, nullable=False)
    reward_num_8: int = Column(Integer, nullable=False)
    reward_type_9: int = Column(Integer, nullable=False)
    reward_id_9: int = Column(Integer, nullable=False)
    reward_num_9: int = Column(Integer, nullable=False)
    reward_type_10: int = Column(Integer, nullable=False)
    reward_id_10: int = Column(Integer, nullable=False)
    reward_num_10: int = Column(Integer, nullable=False)


class SekaiBossMode(DeclarativeBase, Base["SekaiBossMode"]):
    __tablename__ = 'sekai_boss_mode'

    sekai_boss_mode_id: int = Column(Integer, primary_key=True)
    sekai_enemy_id: int = Column(Integer, nullable=False)
    sekai_enemy_level: str = Column(Text, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)
    quest_detail_monster_size: float = Column(Float, nullable=False)
    quest_detail_monster_height: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    reward_gold_coefficient: int = Column(Integer, nullable=False)
    limited_mana: int = Column(Integer, nullable=False)
    score_coefficient: int = Column(Integer, nullable=False)


class SekaiEnemyParameter(DeclarativeBase, Base["SekaiEnemyParameter"]):
    __tablename__ = 'sekai_enemy_parameter'

    sekai_enemy_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)
    level: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: str = Column(Text, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    wave_hp_recovery: int = Column(Integer, nullable=False)
    wave_energy_recovery: int = Column(Integer, nullable=False)
    dodge: int = Column(Integer, nullable=False)
    physical_penetrate: int = Column(Integer, nullable=False)
    magic_penetrate: int = Column(Integer, nullable=False)
    life_steal: int = Column(Integer, nullable=False)
    hp_recovery_rate: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    energy_reduce_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    ex_skill_lv_1: int = Column(Integer, nullable=False)
    ex_skill_lv_2: int = Column(Integer, nullable=False)
    ex_skill_lv_3: int = Column(Integer, nullable=False)
    ex_skill_lv_4: int = Column(Integer, nullable=False)
    ex_skill_lv_5: int = Column(Integer, nullable=False)
    resist_status_id: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)


class SekaiSchedule(DeclarativeBase, Base["SekaiSchedule"]):
    __tablename__ = 'sekai_schedule'

    sekai_id: int = Column(Integer, primary_key=True)
    last_sekai_id: int = Column(Integer, nullable=False)
    fix_reward_group_id: int = Column(Integer, nullable=False)
    damage_rank_id: int = Column(Integer, nullable=False)
    teaser_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    end_losstime: str = Column(Text, nullable=False)
    result_end: str = Column(Text, nullable=False)


class SekaiTopDatum(DeclarativeBase, Base["SekaiTopDatum"]):
    __tablename__ = 'sekai_top_data'

    id: int = Column(Integer, primary_key=True)
    sekai_id: int = Column(Integer, nullable=False, index=True)
    name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    top_bg: int = Column(Integer, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    scale_ratio: float = Column(Float, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    boss_mode: int = Column(Integer, nullable=False)
    sekai_boss_mode_id: int = Column(Integer, nullable=False)
    boss_hp_from: str = Column(Text, nullable=False)
    boss_hp_to: str = Column(Text, nullable=False)
    boss_time_from: str = Column(Text, nullable=False)
    boss_time_to: str = Column(Text, nullable=False)
    duration: int = Column(Integer, nullable=False)
    story_id: int = Column(Integer, nullable=False)


class SekaiTopStoryDatum(DeclarativeBase, Base["SekaiTopStoryDatum"]):
    __tablename__ = 'sekai_top_story_data'

    sekai_id: int = Column(Integer, nullable=False, index=True)
    story_id: int = Column(Integer, primary_key=True)
    boss_time_from: str = Column(Text, nullable=False)
    boss_time_to: str = Column(Text, nullable=False)


class SekaiUnlockStoryCondition(DeclarativeBase, Base["SekaiUnlockStoryCondition"]):
    __tablename__ = 'sekai_unlock_story_condition'

    story_id: int = Column(Integer, primary_key=True)
    sekai_id: int = Column(Integer, nullable=False)
    condition_entry: int = Column(Integer, nullable=False)
    condition_fix_reward_id: int = Column(Integer, nullable=False)
    condition_time: str = Column(Text, nullable=False)


class SerialCodeDatum(DeclarativeBase, Base["SerialCodeDatum"]):
    __tablename__ = 'serial_code_data'

    serial_campaign_id: int = Column(Integer, primary_key=True)
    serial_group_id: int = Column(Integer, nullable=False)
    campaign_name: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    limit_num: int = Column(Integer, nullable=False)


class SerialGroupDatum(DeclarativeBase, Base["SerialGroupDatum"]):
    __tablename__ = 'serial_group_data'

    serial_group_id: int = Column(Integer, primary_key=True)
    campaign_name: str = Column(Text, nullable=False)
    serial_campaign_id_1: int = Column(Integer, nullable=False)
    serial_campaign_id_2: int = Column(Integer, nullable=False)
    serial_campaign_id_3: int = Column(Integer, nullable=False)
    serial_campaign_id_4: int = Column(Integer, nullable=False)
    serial_campaign_id_5: int = Column(Integer, nullable=False)
    serial_campaign_id_6: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class SeriesUnlockCondition(DeclarativeBase, Base["SeriesUnlockCondition"]):
    __tablename__ = 'series_unlock_condition'

    sequel_event_id: int = Column(Integer, primary_key=True)
    condition_story_id_1: int = Column(Integer, nullable=False)
    condition_story_id_2: int = Column(Integer, nullable=False)
    condition_event_id: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)


class ShioriBattleMissionDatum(DeclarativeBase, Base["ShioriBattleMissionDatum"]):
    __tablename__ = 'shiori_battle_mission_data'

    mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_value_4: int = Column(Integer)
    condition_value_5: int = Column(Integer)
    condition_value_6: int = Column(Integer)
    condition_value_7: int = Column(Integer)
    condition_value_8: int = Column(Integer)
    condition_value_9: int = Column(Integer)
    condition_value_10: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class ShioriBos(DeclarativeBase, Base["ShioriBos"]):
    __tablename__ = 'shiori_boss'
    __table_args__ = (
        Index('shiori_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
    )

    boss_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    area_id: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    boss_position_x: int = Column(Integer, nullable=False)
    boss_position_y: int = Column(Integer, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    icon_display_scale: float = Column(Float, nullable=False)
    icon_collider_scale: float = Column(Float, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False, index=True)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    story_id_wavestart_1: int = Column(Integer, nullable=False)
    story_id_waveend_1: int = Column(Integer, nullable=False)
    detail_bg_id: int = Column(Integer, nullable=False)
    detail_bg_position: int = Column(Integer, nullable=False)
    detail_boss_bg_size: float = Column(Float, nullable=False)
    detail_boss_bg_height: float = Column(Float, nullable=False)
    map_position_x: float = Column(Float, nullable=False)
    map_position_y: float = Column(Float, nullable=False)
    map_size: float = Column(Float, nullable=False)
    deatail_aura_size: float = Column(Float, nullable=False)
    map_aura_size: float = Column(Float, nullable=False)
    disp_on_bg: int = Column(Integer, nullable=False)
    qd_mode: int = Column(Integer, nullable=False)


class ShioriBossCondition(DeclarativeBase, Base["ShioriBossCondition"]):
    __tablename__ = 'shiori_boss_condition'

    boss_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    release_quest_id: int = Column(Integer, nullable=False)
    release_boss_id: int = Column(Integer, nullable=False)


class ShioriDescription(DeclarativeBase, Base["ShioriDescription"]):
    __tablename__ = 'shiori_description'

    id: int = Column(Integer, primary_key=True)
    type: int = Column(Integer, nullable=False, index=True)
    description: str = Column(Text, nullable=False)


class ShioriEnemyParameter(DeclarativeBase, Base["ShioriEnemyParameter"]):
    __tablename__ = 'shiori_enemy_parameter'

    enemy_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    level: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    wave_hp_recovery: int = Column(Integer, nullable=False)
    wave_energy_recovery: int = Column(Integer, nullable=False)
    dodge: int = Column(Integer, nullable=False)
    physical_penetrate: int = Column(Integer, nullable=False)
    magic_penetrate: int = Column(Integer, nullable=False)
    life_steal: int = Column(Integer, nullable=False)
    hp_recovery_rate: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    energy_reduce_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    ex_skill_lv_1: int = Column(Integer, nullable=False)
    ex_skill_lv_2: int = Column(Integer, nullable=False)
    ex_skill_lv_3: int = Column(Integer, nullable=False)
    ex_skill_lv_4: int = Column(Integer, nullable=False)
    ex_skill_lv_5: int = Column(Integer, nullable=False)
    resist_status_id: int = Column(Integer, nullable=False)
    resist_variation_id: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)


class ShioriEventList(DeclarativeBase, Base["ShioriEventList"]):
    __tablename__ = 'shiori_event_list'

    event_id: int = Column(Integer, primary_key=True)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)
    condition_chara_id: int = Column(Integer, nullable=False)
    condition_main_quest_id: int = Column(Integer, nullable=False)
    condition_shiori_quest_id: int = Column(Integer, nullable=False)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    original_start_time: str = Column(Text, nullable=False)
    gojuon_order: int = Column(Integer, nullable=False)
    help_index: str = Column(Text, nullable=False)


class ShioriItem(DeclarativeBase, Base["ShioriItem"]):
    __tablename__ = 'shiori_item'

    event_id: int = Column(Integer, primary_key=True)
    unit_material_id_1: int = Column(Integer, nullable=False)
    unit_material_id_2: int = Column(Integer, nullable=False)


class ShioriMissionRewardDatum(DeclarativeBase, Base["ShioriMissionRewardDatum"]):
    __tablename__ = 'shiori_mission_reward_data'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer)
    reward_num: int = Column(Integer, nullable=False)


class ShioriQuest(DeclarativeBase, Base["ShioriQuest"]):
    __tablename__ = 'shiori_quest'

    quest_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    area_id: int = Column(Integer, nullable=False)
    quest_seq: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    position_x: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    icon_offset_x: float = Column(Float, nullable=False)
    icon_offset_y: float = Column(Float, nullable=False)
    icon_scale: float = Column(Float, nullable=False)
    stamina: int = Column(Integer, nullable=False)
    stamina_start: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    unit_exp: int = Column(Integer, nullable=False)
    love: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    daily_limit: int = Column(Integer, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)
    rank_reward_group: int = Column(Integer, nullable=False)
    drop_reward_type: int = Column(Integer, nullable=False)
    drop_reward_id: int = Column(Integer, nullable=False, index=True)
    drop_reward_num: int = Column(Integer, nullable=False)
    drop_reward_odds: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    story_id_wavestart_1: int = Column(Integer, nullable=False)
    story_id_waveend_1: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2: str = Column(Text, nullable=False)
    wave_bgm_que_id_2: str = Column(Text, nullable=False)
    story_id_wavestart_2: int = Column(Integer, nullable=False)
    story_id_waveend_2: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3: str = Column(Text, nullable=False)
    wave_bgm_que_id_3: str = Column(Text, nullable=False)
    story_id_wavestart_3: int = Column(Integer, nullable=False)
    story_id_waveend_3: int = Column(Integer, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)


class ShioriQuestArea(DeclarativeBase, Base["ShioriQuestArea"]):
    __tablename__ = 'shiori_quest_area'

    area_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    area_name: str = Column(Text, nullable=False)
    map_type: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    area_disp: int = Column(Integer, nullable=False)
    map_id: int = Column(Integer, nullable=False)
    scroll_width: int = Column(Integer, nullable=False)
    scroll_height: int = Column(Integer, nullable=False)
    open_tutorial_id: int = Column(Integer, nullable=False)
    tutorial_param_1: str = Column(Text, nullable=False)
    tutorial_param_2: str = Column(Text, nullable=False)
    additional_effect: int = Column(Integer, nullable=False)


class ShioriQuestCondition(DeclarativeBase, Base["ShioriQuestCondition"]):
    __tablename__ = 'shiori_quest_condition'

    quest_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    release_quest_id: int = Column(Integer, nullable=False)
    release_boss_id: int = Column(Integer, nullable=False)
    condition_main_quest_id: int = Column(Integer, nullable=False)


class ShioriStationaryMissionDatum(DeclarativeBase, Base["ShioriStationaryMissionDatum"]):
    __tablename__ = 'shiori_stationary_mission_data'

    stationary_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    event_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class ShioriUnlockUnitCondition(DeclarativeBase, Base["ShioriUnlockUnitCondition"]):
    __tablename__ = 'shiori_unlock_unit_condition'
    __table_args__ = (
        Index('shiori_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id'),
    )

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)
    condition_mission_id: int = Column(Integer, nullable=False, index=True)
    top_description: str = Column(Text, nullable=False)
    description_1: str = Column(Text, nullable=False)
    description_2: str = Column(Text, nullable=False)


class ShioriWaveGroupDatum(DeclarativeBase, Base["ShioriWaveGroupDatum"]):
    __tablename__ = 'shiori_wave_group_data'

    wave_group_id: int = Column(Integer, primary_key=True)
    difficulty: int = Column(Integer, nullable=False)
    wave: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)
    drop_gold_1: int = Column(Integer, nullable=False)
    reward_group_id_1: int = Column(Integer, nullable=False)
    disp_reward_type_1: int = Column(Integer, nullable=False)
    disp_reward_id_1: int = Column(Integer, nullable=False)
    reward_lot_count_1: int = Column(Integer, nullable=False)
    reward_odds_1: int = Column(Integer, nullable=False)
    drop_gold_2: int = Column(Integer, nullable=False)
    reward_group_id_2: int = Column(Integer, nullable=False)
    disp_reward_type_2: int = Column(Integer, nullable=False)
    disp_reward_id_2: int = Column(Integer, nullable=False)
    reward_lot_count_2: int = Column(Integer, nullable=False)
    reward_odds_2: int = Column(Integer, nullable=False)
    drop_gold_3: int = Column(Integer, nullable=False)
    reward_group_id_3: int = Column(Integer, nullable=False)
    disp_reward_type_3: int = Column(Integer, nullable=False)
    disp_reward_id_3: int = Column(Integer, nullable=False)
    reward_lot_count_3: int = Column(Integer, nullable=False)
    reward_odds_3: int = Column(Integer, nullable=False)
    drop_gold_4: int = Column(Integer, nullable=False)
    reward_group_id_4: int = Column(Integer, nullable=False)
    disp_reward_type_4: int = Column(Integer, nullable=False)
    disp_reward_id_4: int = Column(Integer, nullable=False)
    reward_lot_count_4: int = Column(Integer, nullable=False)
    reward_odds_4: int = Column(Integer, nullable=False)
    drop_gold_5: int = Column(Integer, nullable=False)
    reward_group_id_5: int = Column(Integer, nullable=False)
    disp_reward_type_5: int = Column(Integer, nullable=False)
    disp_reward_id_5: int = Column(Integer, nullable=False)
    reward_lot_count_5: int = Column(Integer, nullable=False)
    reward_odds_5: int = Column(Integer, nullable=False)


class ShopStaticPriceGroup(DeclarativeBase, Base["ShopStaticPriceGroup"]):
    __tablename__ = 'shop_static_price_group'

    id: int = Column(Integer, primary_key=True)
    price_group_id: int = Column(Integer, nullable=False)
    buy_count_from: int = Column(Integer, nullable=False)
    buy_count_to: int = Column(Integer, nullable=False)
    count: int = Column(Integer, nullable=False)


class SkeStoryDatum(DeclarativeBase, Base["SkeStoryDatum"]):
    __tablename__ = 'ske_story_data'

    sub_story_id: int = Column(Integer, primary_key=True)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    unlock_condition_quest_id: int = Column(Integer, nullable=False)
    unlock_condition_boss_id: int = Column(Integer, nullable=False)
    read_condition_event_story_id: int = Column(Integer, nullable=False)


class SkeStoryScript(DeclarativeBase, Base["SkeStoryScript"]):
    __tablename__ = 'ske_story_script'

    id: int = Column(Integer, primary_key=True)
    story_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    line_num: int = Column(Integer, nullable=False)
    start_pos: int = Column(Integer, nullable=False)
    end_pos: int = Column(Integer, nullable=False)
    seek_time: float = Column(Float, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class SkillAction(DeclarativeBase, Base["SkillAction"]):
    __tablename__ = 'skill_action'

    action_id: int = Column(Integer, primary_key=True)
    class_id: int = Column(Integer, nullable=False)
    action_type: int = Column(Integer, nullable=False)
    action_detail_1: int = Column(Integer, nullable=False)
    action_detail_2: int = Column(Integer, nullable=False)
    action_detail_3: int = Column(Integer, nullable=False)
    action_value_1: float = Column(Float, nullable=False)
    action_value_2: float = Column(Float, nullable=False)
    action_value_3: float = Column(Float, nullable=False)
    action_value_4: float = Column(Float, nullable=False)
    action_value_5: float = Column(Float, nullable=False)
    action_value_6: float = Column(Float, nullable=False)
    action_value_7: float = Column(Float, nullable=False)
    target_assignment: int = Column(Integer, nullable=False)
    target_area: int = Column(Integer, nullable=False)
    target_range: int = Column(Integer, nullable=False)
    target_type: int = Column(Integer, nullable=False)
    target_number: int = Column(Integer, nullable=False)
    target_count: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    level_up_disp: str = Column(Text, nullable=False)


class SkillCost(DeclarativeBase, Base["SkillCost"]):
    __tablename__ = 'skill_cost'

    target_level: int = Column(Integer, primary_key=True)
    cost: int = Column(Integer, nullable=False)


class SkillDatum(DeclarativeBase, Base["SkillDatum"]):
    __tablename__ = 'skill_data'

    skill_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text)
    skill_type: int = Column(Integer, nullable=False)
    skill_area_width: int = Column(Integer, nullable=False)
    skill_cast_time: float = Column(Float, nullable=False)
    boss_ub_cool_time: float = Column(Float, nullable=False)
    action_1: int = Column(Integer, nullable=False)
    action_2: int = Column(Integer, nullable=False)
    action_3: int = Column(Integer, nullable=False)
    action_4: int = Column(Integer, nullable=False)
    action_5: int = Column(Integer, nullable=False)
    action_6: int = Column(Integer, nullable=False)
    action_7: int = Column(Integer, nullable=False)
    depend_action_1: int = Column(Integer, nullable=False)
    depend_action_2: int = Column(Integer, nullable=False)
    depend_action_3: int = Column(Integer, nullable=False)
    depend_action_4: int = Column(Integer, nullable=False)
    depend_action_5: int = Column(Integer, nullable=False)
    depend_action_6: int = Column(Integer, nullable=False)
    depend_action_7: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    icon_type: int = Column(Integer, nullable=False)


class SkipBossDatum(DeclarativeBase, Base["SkipBossDatum"]):
    __tablename__ = 'skip_boss_data'

    boss_id: int = Column(Integer, primary_key=True)
    skip_motion_id: int = Column(Integer, nullable=False)
    skip_bg_id: int = Column(Integer, nullable=False)
    skip_position_x: int = Column(Integer, nullable=False)
    skip_position_y: int = Column(Integer, nullable=False)
    skip_scale_x: float = Column(Float, nullable=False)
    skip_scale_y: float = Column(Float, nullable=False)


class SkipMonsterDatum(DeclarativeBase, Base["SkipMonsterDatum"]):
    __tablename__ = 'skip_monster_data'

    quest_id: int = Column(Integer, primary_key=True)
    area_id: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    bg_skip_id: int = Column(Integer, nullable=False)


class SpBattleVoice(DeclarativeBase, Base["SpBattleVoice"]):
    __tablename__ = 'sp_battle_voice'

    id: int = Column(Integer, primary_key=True, nullable=False)
    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    voice_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)


class SpDetailVoice(DeclarativeBase, Base["SpDetailVoice"]):
    __tablename__ = 'sp_detail_voice'

    unit_id: int = Column(Integer, primary_key=True)
    cue_name_1: str = Column(Text, nullable=False)
    cue_name_2: str = Column(Text, nullable=False)
    cue_name_3: str = Column(Text, nullable=False)
    cue_name_4: str = Column(Text, nullable=False)
    cue_name_5: str = Column(Text, nullable=False)


class SpLoseVoice(DeclarativeBase, Base["SpLoseVoice"]):
    __tablename__ = 'sp_lose_voice'

    original_unit_id: int = Column(Integer, primary_key=True)
    unit_id_1: int = Column(Integer, nullable=False)
    unit_1_pos_x: int = Column(Integer, nullable=False)
    unit_1_pos_y: int = Column(Integer, nullable=False)
    unit_1_depth: int = Column(Integer, nullable=False)
    unit_1_clip: int = Column(Integer, nullable=False)
    unit_id_2: int = Column(Integer, nullable=False)
    unit_2_pos_x: int = Column(Integer, nullable=False)
    unit_2_pos_y: int = Column(Integer, nullable=False)
    unit_2_depth: int = Column(Integer, nullable=False)
    unit_2_clip: int = Column(Integer, nullable=False)
    unit_id_3: int = Column(Integer, nullable=False)
    unit_3_pos_x: int = Column(Integer, nullable=False)
    unit_3_pos_y: int = Column(Integer, nullable=False)
    unit_3_depth: int = Column(Integer, nullable=False)
    unit_3_clip: int = Column(Integer, nullable=False)
    unit_only_disp: int = Column(Integer, nullable=False)
    speaker_unit_id_1: int = Column(Integer, nullable=False)
    speaker_unit_id_2: int = Column(Integer, nullable=False)
    speaker_unit_id_3: int = Column(Integer, nullable=False)
    speaker_unit_id_4: int = Column(Integer, nullable=False)
    speaker_unit_id_5: int = Column(Integer, nullable=False)
    speaker_unit_id_6: int = Column(Integer, nullable=False)
    speaker_unit_id_7: int = Column(Integer, nullable=False)
    speaker_unit_id_8: int = Column(Integer, nullable=False)
    speaker_unit_id_9: int = Column(Integer, nullable=False)
    speaker_unit_id_10: int = Column(Integer, nullable=False)


class SpLoseVoiceGroup(DeclarativeBase, Base["SpLoseVoiceGroup"]):
    __tablename__ = 'sp_lose_voice_group'

    group_id: int = Column(Integer, primary_key=True, nullable=False)
    unit_id: int = Column(Integer, primary_key=True, nullable=False)
    speaker_unit_id: int = Column(Integer, nullable=False)


class SpaceBattleDatum(DeclarativeBase, Base["SpaceBattleDatum"]):
    __tablename__ = 'space_battle_data'

    space_battle_id: int = Column(Integer, primary_key=True)
    space_enemy_id: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    quest_detail_bg_id: int = Column(Integer, nullable=False)
    quest_detail_bg_position: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)


class SpaceSchedule(DeclarativeBase, Base["SpaceSchedule"]):
    __tablename__ = 'space_schedule'

    space_id: int = Column(Integer, primary_key=True)
    teaser_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    count_start_time: str = Column(Text, nullable=False)
    count_end_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    sid: int = Column(Integer, nullable=False)
    pre_story_id: int = Column(Integer, nullable=False)


class SpaceTopDatum(DeclarativeBase, Base["SpaceTopDatum"]):
    __tablename__ = 'space_top_data'

    id: int = Column(Integer, primary_key=True)
    space_id: int = Column(Integer, nullable=False, index=True)
    space_battle_id: int = Column(Integer, nullable=False)
    part_flag: int = Column(Integer, nullable=False)
    story_id: int = Column(Integer, nullable=False, index=True)
    time_from: str = Column(Text, nullable=False)
    time_to: str = Column(Text, nullable=False)
    skip_battle_time: str = Column(Text, nullable=False)
    name: str = Column(Text, nullable=False)


class SpecialStill(DeclarativeBase, Base["SpecialStill"]):
    __tablename__ = 'special_still'

    still_id: int = Column(Integer, primary_key=True)
    type: int = Column(Integer, nullable=False)
    back_momory_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)


class SpecialStoryBanner(DeclarativeBase, Base["SpecialStoryBanner"]):
    __tablename__ = 'special_story_banner'

    id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False, index=True)
    start_time: str = Column(Text, nullable=False)
    remind_end_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class SpecialfesBanner(DeclarativeBase, Base["SpecialfesBanner"]):
    __tablename__ = 'specialfes_banner'

    gacha_id: int = Column(Integer, primary_key=True)
    banner_id_1: int = Column(Integer, nullable=False)
    banner_id_2: int = Column(Integer, nullable=False)
    banner_id_3: int = Column(Integer, nullable=False)
    banner_id_4: int = Column(Integer, nullable=False)
    banner_id_5: int = Column(Integer, nullable=False)
    banner_id_6: int = Column(Integer, nullable=False)
    banner_id_7: int = Column(Integer, nullable=False)
    banner_id_8: int = Column(Integer, nullable=False)
    banner_id_9: int = Column(Integer, nullable=False)
    banner_id_10: int = Column(Integer, nullable=False)


class SpskillLabelDatum(DeclarativeBase, Base["SpskillLabelDatum"]):
    __tablename__ = 'spskill_label_data'

    unit_id: int = Column(Integer, primary_key=True)
    normal_label_text: str = Column(Text, nullable=False)
    sp_label_text: str = Column(Text, nullable=False)


class SpskillLvInitializeDatum(DeclarativeBase, Base["SpskillLvInitializeDatum"]):
    __tablename__ = 'spskill_lv_initialize_data'

    initialize_skill_id: int = Column(Integer, primary_key=True)
    base_skill_id: int = Column(Integer, nullable=False)

class SrtAction(DeclarativeBase, Base["SrtAction"]):
    __tablename__ = 'srt_action'

    action_name: str = Column(Text, primary_key=True)
    inori_action: str = Column(Text, nullable=False)
    dragon_action: str = Column(Text, nullable=False)
    kaya_action: str = Column(Text, nullable=False)
    homare_action: str = Column(Text, nullable=False)
    talk_text_type: int = Column(Integer, nullable=False)
    talk_text: str = Column(Text, nullable=False)
    voice_list: str = Column(Text, nullable=False)


class SrtPanel(DeclarativeBase, Base["SrtPanel"]):
    __tablename__ = 'srt_panel'

    reading_id: int = Column(Integer, primary_key=True)
    reading: str = Column(Text, nullable=False)
    read_type: int = Column(Integer, nullable=False)
    panel_id: int = Column(Integer, nullable=False, index=True)
    detail_text: str = Column(Text, nullable=False)
    version: int = Column(Integer, nullable=False, index=True)
    head_symbol: str = Column(Text, nullable=False)
    tail_symbol: str = Column(Text, nullable=False)


class SrtReward(DeclarativeBase, Base["SrtReward"]):
    __tablename__ = 'srt_reward'

    id: int = Column(Integer, primary_key=True)
    srt_score: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class SrtScore(DeclarativeBase, Base["SrtScore"]):
    __tablename__ = 'srt_score'

    difficulty_level: int = Column(Integer, primary_key=True)
    coefficient_read_type_1: int = Column(Integer, nullable=False)
    coefficient_read_type_2: int = Column(Integer, nullable=False)
    coefficient_read_type_3: int = Column(Integer, nullable=False)
    coefficient_count_priconne_panel: int = Column(Integer, nullable=False)
    coefficient_fever: int = Column(Integer, nullable=False)
    constant_turn_bonus: int = Column(Integer, nullable=False)
    coefficient_turn_bonus: int = Column(Integer, nullable=False)
    coefficient_avg_answer_time: int = Column(Integer, nullable=False)
    constant_wrong_num: int = Column(Integer, nullable=False)
    coefficient_wrong_num: int = Column(Integer, nullable=False)


class SrtTopTalk(DeclarativeBase, Base["SrtTopTalk"]):
    __tablename__ = 'srt_top_talk'

    id: int = Column(Integer, primary_key=True)
    talk_id: int = Column(Integer, nullable=False, index=True)
    chara_index: int = Column(Integer, nullable=False)
    talk_text: str = Column(Text, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    direction: int = Column(Integer, nullable=False)


class SspStoryDatum(DeclarativeBase, Base["SspStoryDatum"]):
    __tablename__ = 'ssp_story_data'

    sub_story_id: int = Column(Integer, primary_key=True)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    contents_type: int = Column(Integer, nullable=False, index=True)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    read_condition: int = Column(Integer, nullable=False)


class Stamp(DeclarativeBase, Base["Stamp"]):
    __tablename__ = 'stamp'

    stamp_id: int = Column(Integer, primary_key=True)
    disp_order: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    start_date: str = Column(Text, nullable=False)
    end_date: str = Column(Text, nullable=False)


class StationaryMissionDatum(DeclarativeBase, Base["StationaryMissionDatum"]):
    __tablename__ = 'stationary_mission_data'

    stationary_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    category_icon: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer)
    condition_value_2: int = Column(Integer)
    condition_value_3: int = Column(Integer)
    condition_value_4: int = Column(Integer)
    condition_value_5: int = Column(Integer)
    condition_value_6: int = Column(Integer)
    condition_value_7: int = Column(Integer)
    condition_value_8: int = Column(Integer)
    condition_value_9: int = Column(Integer)
    condition_value_10: int = Column(Integer)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    min_level: int = Column(Integer, nullable=False)
    max_level: int = Column(Integer, nullable=False)
    title_color_id: int = Column(Integer, nullable=False)
    visible_flag: int = Column(Integer, nullable=False)


class Still(DeclarativeBase, Base["Still"]):
    __tablename__ = 'still'

    still_id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False)
    story_id: int = Column(Integer, nullable=False, index=True)
    still_group_id: int = Column(Integer, nullable=False, index=True)
    vertical_still_flg: int = Column(Integer, nullable=False)
    position_y: int = Column(Integer, nullable=False)
    unit_id_1: int = Column(Integer, nullable=False)
    unit_id_2: int = Column(Integer, nullable=False)
    unit_id_3: int = Column(Integer, nullable=False)
    unit_id_4: int = Column(Integer, nullable=False)
    unit_id_5: int = Column(Integer, nullable=False)
    unit_id_6: int = Column(Integer, nullable=False)
    unit_id_7: int = Column(Integer, nullable=False)
    unit_id_8: int = Column(Integer, nullable=False)
    unit_id_9: int = Column(Integer, nullable=False)
    unit_id_10: int = Column(Integer, nullable=False)
    facial_id: int = Column(Integer, nullable=False)
    album_ignore: int = Column(Integer, nullable=False)
    my_page_flag: int = Column(Integer, nullable=False)
    scroll_direction: int = Column(Integer, nullable=False)


class StoryCharacterMask(DeclarativeBase, Base["StoryCharacterMask"]):
    __tablename__ = 'story_character_mask'

    chara_id: int = Column(Integer, primary_key=True)
    offset: float = Column(Float, nullable=False)
    size: float = Column(Float, nullable=False)
    softness: float = Column(Float, nullable=False)


class StoryDatum(DeclarativeBase, Base["StoryDatum"]):
    __tablename__ = 'story_data'

    story_group_id: int = Column(Integer, primary_key=True)
    story_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    thumbnail_id: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    order: int = Column(Integer, nullable=False)
    condition_free_flag: int = Column(Integer, nullable=False)
    gojuon_order: int = Column(Integer, nullable=False)


class StoryDetail(DeclarativeBase, Base["StoryDetail"]):
    __tablename__ = 'story_detail'

    story_id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    visible_type: int = Column(Integer, nullable=False)
    story_end: int = Column(Integer, nullable=False)
    pre_story_id: int = Column(Integer, nullable=False)
    force_unlock_time: str = Column(Text, nullable=False)
    pre_story_id_2: int = Column(Integer, nullable=False)
    force_unlock_time_2: str = Column(Text, nullable=False)
    love_level: int = Column(Integer, nullable=False)
    requirement_id: int = Column(Integer, nullable=False)
    unlock_quest_id: int = Column(Integer, nullable=False)
    story_quest_id: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_value_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_value_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_value_3: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class StoryQuestDatum(DeclarativeBase, Base["StoryQuestDatum"]):
    __tablename__ = 'story_quest_data'

    story_quest_id: int = Column(Integer, primary_key=True)
    story_id: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2: str = Column(Text, nullable=False)
    wave_bgm_que_id_2: str = Column(Text, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3: str = Column(Text, nullable=False)
    wave_bgm_que_id_3: str = Column(Text, nullable=False)
    guest_unit_1: int = Column(Integer, nullable=False)
    guest_unit_2: int = Column(Integer, nullable=False)
    guest_unit_3: int = Column(Integer, nullable=False)
    guest_unit_4: int = Column(Integer, nullable=False)
    guest_unit_5: int = Column(Integer, nullable=False)


class SvdDramaScript(DeclarativeBase, Base["SvdDramaScript"]):
    __tablename__ = 'svd_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class SvdStoryDatum(DeclarativeBase, Base["SvdStoryDatum"]):
    __tablename__ = 'svd_story_data'

    sub_story_id: int = Column(Integer, primary_key=True)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    read_condition_time: str = Column(Text, nullable=False)
    condition_quest_id: int = Column(Integer, nullable=False)
    condition_boss_id: int = Column(Integer, nullable=False)
    read_condition: int = Column(Integer, nullable=False)


class SvdStoryScript(DeclarativeBase, Base["SvdStoryScript"]):
    __tablename__ = 'svd_story_script'

    id: int = Column(Integer, primary_key=True)
    story_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    line_num: int = Column(Integer, nullable=False)
    start_pos: int = Column(Integer, nullable=False)
    end_pos: int = Column(Integer, nullable=False)
    seek_time: float = Column(Float, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class TaqCompletionReward(DeclarativeBase, Base["TaqCompletionReward"]):
    __tablename__ = 'taq_completion_rewards'

    id: int = Column(Integer, primary_key=True)
    completion_num: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    emblem_id: int = Column(Integer, nullable=False)


class TaqDatum(DeclarativeBase, Base["TaqDatum"]):
    __tablename__ = 'taq_data'

    taq_no: int = Column(Integer, primary_key=True)
    genre: int = Column(Integer, nullable=False)
    taq_type: int = Column(Integer, nullable=False)
    difficulty: int = Column(Integer, nullable=False)
    word: str = Column(Text, nullable=False)
    chunk: str = Column(Text, nullable=False)
    detail: str = Column(Text, nullable=False)
    detail_2: str = Column(Text, nullable=False)
    assist_detail: str = Column(Text, nullable=False)
    image_id: int = Column(Integer, nullable=False)
    char_no_1: int = Column(Integer, nullable=False)
    char_no_2: int = Column(Integer, nullable=False)
    char_no_3: int = Column(Integer, nullable=False)
    char_no_4: int = Column(Integer, nullable=False)
    char_no_5: int = Column(Integer, nullable=False)
    input_type_1: int = Column(Integer, nullable=False)
    input_type_2: int = Column(Integer, nullable=False)
    input_type_3: int = Column(Integer, nullable=False)
    input_type_4: int = Column(Integer, nullable=False)
    input_type_5: int = Column(Integer, nullable=False)


class TaqDramaScript(DeclarativeBase, Base["TaqDramaScript"]):
    __tablename__ = 'taq_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class TaqGameSetting(DeclarativeBase, Base["TaqGameSetting"]):
    __tablename__ = 'taq_game_setting'

    id: int = Column(Integer, primary_key=True)
    lottery_rate: float = Column(Float, nullable=False)
    help_use_count_normal: int = Column(Integer, nullable=False)
    help_use_count_hard: int = Column(Integer, nullable=False)
    help_use_count_veryhard: int = Column(Integer, nullable=False)


class TaqGenre(DeclarativeBase, Base["TaqGenre"]):
    __tablename__ = 'taq_genre'

    genre_id: int = Column(Integer, primary_key=True)
    genre_name: str = Column(Text, nullable=False)


class TaqGoodUnit(DeclarativeBase, Base["TaqGoodUnit"]):
    __tablename__ = 'taq_good_unit'

    taq_no: int = Column(Integer, primary_key=True)
    unit_id_1: int = Column(Integer, nullable=False)
    unit_id_2: int = Column(Integer, nullable=False)
    unit_id_3: int = Column(Integer, nullable=False)
    unit_id_4: int = Column(Integer, nullable=False)
    unit_id_5: int = Column(Integer, nullable=False)
    unit_id_6: int = Column(Integer, nullable=False)
    unit_id_7: int = Column(Integer, nullable=False)
    unit_id_8: int = Column(Integer, nullable=False)
    unit_id_9: int = Column(Integer, nullable=False)
    unit_id_10: int = Column(Integer, nullable=False)


class TaqIncorrectWord(DeclarativeBase, Base["TaqIncorrectWord"]):
    __tablename__ = 'taq_incorrect_word'

    word_id: int = Column(Integer, primary_key=True)
    incorrect_word: str = Column(Text, nullable=False)


class TaqKanjiList(DeclarativeBase, Base["TaqKanjiList"]):
    __tablename__ = 'taq_kanji_list'

    id: int = Column(Integer, primary_key=True)
    kanji: str = Column(Text, nullable=False)


class TaqNecessaryWord(DeclarativeBase, Base["TaqNecessaryWord"]):
    __tablename__ = 'taq_necessary_word'

    taq_no: int = Column(Integer, primary_key=True)
    necessary_word_1: str = Column(Text, nullable=False)
    unnecessary_word_1: str = Column(Text, nullable=False)
    necessary_word_2: str = Column(Text, nullable=False)
    unnecessary_word_2: str = Column(Text, nullable=False)
    necessary_word_3: str = Column(Text, nullable=False)
    unnecessary_word_3: str = Column(Text, nullable=False)
    necessary_word_4: str = Column(Text, nullable=False)
    unnecessary_word_4: str = Column(Text, nullable=False)
    necessary_word_5: str = Column(Text, nullable=False)
    unnecessary_word_5: str = Column(Text, nullable=False)


class TaqReward(DeclarativeBase, Base["TaqReward"]):
    __tablename__ = 'taq_rewards'

    id: int = Column(Integer, primary_key=True)
    score: int = Column(Integer, nullable=False)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class TaqUnit(DeclarativeBase, Base["TaqUnit"]):
    __tablename__ = 'taq_unit'

    unit_id: int = Column(Integer, primary_key=True)
    sort_order: int = Column(Integer, nullable=False)
    personality_id: int = Column(Integer, nullable=False)
    genre_status_1: int = Column(Integer, nullable=False)
    genre_status_2: int = Column(Integer, nullable=False)
    genre_status_3: int = Column(Integer, nullable=False)
    genre_status_4: int = Column(Integer, nullable=False)
    genre_status_5: int = Column(Integer, nullable=False)
    genre_status_6: int = Column(Integer, nullable=False)


class ThumbnailHideCondition(DeclarativeBase, Base["ThumbnailHideCondition"]):
    __tablename__ = 'thumbnail_hide_condition'

    story_group_id: int = Column(Integer, primary_key=True)
    hide_story_id_from: int = Column(Integer, nullable=False)
    hide_story_id_to: int = Column(Integer, nullable=False)
    unlock_condition_story_id: int = Column(Integer, nullable=False)


class TicketGachaDatum(DeclarativeBase, Base["TicketGachaDatum"]):
    __tablename__ = 'ticket_gacha_data'

    gacha_id: int = Column(Integer, primary_key=True)
    gacha_name: str = Column(Text, nullable=False)
    gacha_type: int = Column(Integer, nullable=False)
    ticket_id: int = Column(Integer, nullable=False)
    gacha_times: int = Column(Integer, nullable=False)
    gacha_detail: int = Column(Integer, nullable=False)
    guarantee_rarity: str = Column(Text, nullable=False)
    rarity_odds: str = Column(Text, nullable=False)
    chara_odds_star1: str = Column(Text, nullable=False)
    chara_odds_star2: str = Column(Text, nullable=False)
    chara_odds_star3: str = Column(Text, nullable=False)
    staging_type: int = Column(Integer, nullable=False)


class Tip(DeclarativeBase, Base["Tip"]):
    __tablename__ = 'tips'

    id: int = Column(Integer, primary_key=True)
    value: int = Column(Integer, nullable=False)
    tips_index: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)


class TmeMapDatum(DeclarativeBase, Base["TmeMapDatum"]):
    __tablename__ = 'tme_map_data'

    tme_object_id: int = Column(Integer, primary_key=True)
    event_id: int = Column(Integer, nullable=False, index=True)
    condition_story_id: int = Column(Integer, nullable=False)
    area_difficulty_type: int = Column(Integer, nullable=False)
    release_effect: int = Column(Integer, nullable=False)
    tap_effect: int = Column(Integer, nullable=False)


class TowerAreaDatum(DeclarativeBase, Base["TowerAreaDatum"]):
    __tablename__ = 'tower_area_data'

    tower_area_id: int = Column(Integer, primary_key=True)
    max_floor_num: int = Column(Integer, nullable=False)
    area_bg: int = Column(Integer, nullable=False)
    tower_bgm: str = Column(Text, nullable=False)
    cloister_quest_id: int = Column(Integer, nullable=False)


class TowerCloisterQuestDatum(DeclarativeBase, Base["TowerCloisterQuestDatum"]):
    __tablename__ = 'tower_cloister_quest_data'

    tower_cloister_quest_id: int = Column(Integer, primary_key=True)
    daily_limit: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    recovery_hp_rate: int = Column(Integer, nullable=False)
    recovery_tp_rate: int = Column(Integer, nullable=False)
    start_tp_rate: int = Column(Integer, nullable=False)
    fix_reward_group_id: int = Column(Integer, nullable=False)
    drop_reward_group_id: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    w1_enemy_position_x_1: int = Column(Integer, nullable=False)
    w1_enemy_local_position_y_1: int = Column(Integer, nullable=False)
    w1_enemy_size_1: float = Column(Float, nullable=False)
    w1_enemy_position_x_2: int = Column(Integer, nullable=False)
    w1_enemy_local_position_y_2: int = Column(Integer, nullable=False)
    w1_enemy_size_2: float = Column(Float, nullable=False)
    w1_enemy_position_x_3: int = Column(Integer, nullable=False)
    w1_enemy_local_position_y_3: int = Column(Integer, nullable=False)
    w1_enemy_size_3: float = Column(Float, nullable=False)
    w1_enemy_position_x_4: int = Column(Integer, nullable=False)
    w1_enemy_local_position_y_4: int = Column(Integer, nullable=False)
    w1_enemy_size_4: float = Column(Float, nullable=False)
    w1_enemy_position_x_5: int = Column(Integer, nullable=False)
    w1_enemy_local_position_y_5: int = Column(Integer, nullable=False)
    w1_enemy_size_5: float = Column(Float, nullable=False)
    w2_enemy_position_x_1: int = Column(Integer, nullable=False)
    w2_enemy_local_position_y_1: int = Column(Integer, nullable=False)
    w2_enemy_size_1: float = Column(Float, nullable=False)
    w2_enemy_position_x_2: int = Column(Integer, nullable=False)
    w2_enemy_local_position_y_2: int = Column(Integer, nullable=False)
    w2_enemy_size_2: float = Column(Float, nullable=False)
    w2_enemy_position_x_3: int = Column(Integer, nullable=False)
    w2_enemy_local_position_y_3: int = Column(Integer, nullable=False)
    w2_enemy_size_3: float = Column(Float, nullable=False)
    w2_enemy_position_x_4: int = Column(Integer, nullable=False)
    w2_enemy_local_position_y_4: int = Column(Integer, nullable=False)
    w2_enemy_size_4: float = Column(Float, nullable=False)
    w2_enemy_position_x_5: int = Column(Integer, nullable=False)
    w2_enemy_local_position_y_5: int = Column(Integer, nullable=False)
    w2_enemy_size_5: float = Column(Float, nullable=False)
    w3_enemy_position_x_1: int = Column(Integer, nullable=False)
    w3_enemy_local_position_y_1: int = Column(Integer, nullable=False)
    w3_enemy_size_1: float = Column(Float, nullable=False)
    w3_enemy_position_x_2: int = Column(Integer, nullable=False)
    w3_enemy_local_position_y_2: int = Column(Integer, nullable=False)
    w3_enemy_size_2: float = Column(Float, nullable=False)
    w3_enemy_position_x_3: int = Column(Integer, nullable=False)
    w3_enemy_local_position_y_3: int = Column(Integer, nullable=False)
    w3_enemy_size_3: float = Column(Float, nullable=False)
    w3_enemy_position_x_4: int = Column(Integer, nullable=False)
    w3_enemy_local_position_y_4: int = Column(Integer, nullable=False)
    w3_enemy_size_4: float = Column(Float, nullable=False)
    w3_enemy_position_x_5: int = Column(Integer, nullable=False)
    w3_enemy_local_position_y_5: int = Column(Integer, nullable=False)
    w3_enemy_size_5: float = Column(Float, nullable=False)
    background: int = Column(Integer, nullable=False)
    bg_position: int = Column(Integer, nullable=False)


class TowerEnemyParameter(DeclarativeBase, Base["TowerEnemyParameter"]):
    __tablename__ = 'tower_enemy_parameter'

    enemy_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    name: str = Column(Text, nullable=False)
    level: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    wave_hp_recovery: int = Column(Integer, nullable=False)
    wave_energy_recovery: int = Column(Integer, nullable=False)
    dodge: int = Column(Integer, nullable=False)
    physical_penetrate: int = Column(Integer, nullable=False)
    magic_penetrate: int = Column(Integer, nullable=False)
    life_steal: int = Column(Integer, nullable=False)
    hp_recovery_rate: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    energy_reduce_rate: int = Column(Integer, nullable=False)
    union_burst_level: int = Column(Integer, nullable=False)
    main_skill_lv_1: int = Column(Integer, nullable=False)
    main_skill_lv_2: int = Column(Integer, nullable=False)
    main_skill_lv_3: int = Column(Integer, nullable=False)
    main_skill_lv_4: int = Column(Integer, nullable=False)
    main_skill_lv_5: int = Column(Integer, nullable=False)
    main_skill_lv_6: int = Column(Integer, nullable=False)
    main_skill_lv_7: int = Column(Integer, nullable=False)
    main_skill_lv_8: int = Column(Integer, nullable=False)
    main_skill_lv_9: int = Column(Integer, nullable=False)
    main_skill_lv_10: int = Column(Integer, nullable=False)
    ex_skill_lv_1: int = Column(Integer, nullable=False)
    ex_skill_lv_2: int = Column(Integer, nullable=False)
    ex_skill_lv_3: int = Column(Integer, nullable=False)
    ex_skill_lv_4: int = Column(Integer, nullable=False)
    ex_skill_lv_5: int = Column(Integer, nullable=False)
    resist_status_id: int = Column(Integer, nullable=False)
    resist_variation_id: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)
    enemy_color: int = Column(Integer, nullable=False)


class TowerExQuestDatum(DeclarativeBase, Base["TowerExQuestDatum"]):
    __tablename__ = 'tower_ex_quest_data'

    tower_ex_quest_id: int = Column(Integer, primary_key=True)
    tower_area_id: int = Column(Integer, nullable=False)
    floor_num: int = Column(Integer, nullable=False, index=True)
    stamina: int = Column(Integer, nullable=False)
    stamina_start: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)
    additional_reward_type: int = Column(Integer, nullable=False)
    additional_reward_id: int = Column(Integer, nullable=False)
    fix_reward_group_id: int = Column(Integer, nullable=False)
    chest_id: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    bg_position: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    enemy_position_x_1: int = Column(Integer, nullable=False)
    enemy_local_position_y_1: int = Column(Integer, nullable=False)
    enemy_size_1: float = Column(Float, nullable=False)
    enemy_position_x_2: int = Column(Integer, nullable=False)
    enemy_local_position_y_2: int = Column(Integer, nullable=False)
    enemy_size_2: float = Column(Float, nullable=False)
    enemy_position_x_3: int = Column(Integer, nullable=False)
    enemy_local_position_y_3: int = Column(Integer, nullable=False)
    enemy_size_3: float = Column(Float, nullable=False)
    enemy_position_x_4: int = Column(Integer, nullable=False)
    enemy_local_position_y_4: int = Column(Integer, nullable=False)
    enemy_size_4: float = Column(Float, nullable=False)
    enemy_position_x_5: int = Column(Integer, nullable=False)
    enemy_local_position_y_5: int = Column(Integer, nullable=False)
    enemy_size_5: float = Column(Float, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)
    clp_flag: int = Column(Integer, nullable=False)
    skip_level: int = Column(Integer, nullable=False)


class TowerQuestDatum(DeclarativeBase, Base["TowerQuestDatum"]):
    __tablename__ = 'tower_quest_data'

    tower_quest_id: int = Column(Integer, primary_key=True)
    tower_area_id: int = Column(Integer, nullable=False)
    floor_num: int = Column(Integer, nullable=False, index=True)
    floor_image_type: int = Column(Integer, nullable=False)
    floor_image_add_type: int = Column(Integer, nullable=False)
    open_tower_ex_quest_id: int = Column(Integer, nullable=False)
    boss_floor_flg: int = Column(Integer, nullable=False)
    stamina: int = Column(Integer, nullable=False)
    stamina_start: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    recovery_hp_rate: int = Column(Integer, nullable=False)
    recovery_tp_rate: int = Column(Integer, nullable=False)
    start_tp_rate: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)
    additional_reward_type: int = Column(Integer, nullable=False)
    additional_reward_id: int = Column(Integer, nullable=False)
    fix_reward_group_id: int = Column(Integer, nullable=False)
    odds_group_id: int = Column(Integer, nullable=False)
    chest_id: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    bg_position: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    enemy_position_x_1: int = Column(Integer, nullable=False)
    enemy_local_position_y_1: int = Column(Integer, nullable=False)
    enemy_size_1: float = Column(Float, nullable=False)
    enemy_position_x_2: int = Column(Integer, nullable=False)
    enemy_local_position_y_2: int = Column(Integer, nullable=False)
    enemy_size_2: float = Column(Float, nullable=False)
    enemy_position_x_3: int = Column(Integer, nullable=False)
    enemy_local_position_y_3: int = Column(Integer, nullable=False)
    enemy_size_3: float = Column(Float, nullable=False)
    enemy_position_x_4: int = Column(Integer, nullable=False)
    enemy_local_position_y_4: int = Column(Integer, nullable=False)
    enemy_size_4: float = Column(Float, nullable=False)
    enemy_position_x_5: int = Column(Integer, nullable=False)
    enemy_local_position_y_5: int = Column(Integer, nullable=False)
    enemy_size_5: float = Column(Float, nullable=False)
    wave_bgm: str = Column(Text, nullable=False)
    clp_flag: int = Column(Integer, nullable=False)
    skip_level: int = Column(Integer, nullable=False)


class TowerQuestFixRewardGroup(DeclarativeBase, Base["TowerQuestFixRewardGroup"]):
    __tablename__ = 'tower_quest_fix_reward_group'

    fix_reward_group_id: int = Column(Integer, primary_key=True)
    treasure_type_1: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    treasure_type_2: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    treasure_type_3: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    treasure_type_4: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    treasure_type_5: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    treasure_type_6: int = Column(Integer, nullable=False)
    reward_type_6: int = Column(Integer, nullable=False)
    reward_id_6: int = Column(Integer, nullable=False)
    reward_num_6: int = Column(Integer, nullable=False)
    treasure_type_7: int = Column(Integer, nullable=False)
    reward_type_7: int = Column(Integer, nullable=False)
    reward_id_7: int = Column(Integer, nullable=False)
    reward_num_7: int = Column(Integer, nullable=False)
    treasure_type_8: int = Column(Integer, nullable=False)
    reward_type_8: int = Column(Integer, nullable=False)
    reward_id_8: int = Column(Integer, nullable=False)
    reward_num_8: int = Column(Integer, nullable=False)
    treasure_type_9: int = Column(Integer, nullable=False)
    reward_type_9: int = Column(Integer, nullable=False)
    reward_id_9: int = Column(Integer, nullable=False)
    reward_num_9: int = Column(Integer, nullable=False)
    treasure_type_10: int = Column(Integer, nullable=False)
    reward_type_10: int = Column(Integer, nullable=False)
    reward_id_10: int = Column(Integer, nullable=False)
    reward_num_10: int = Column(Integer, nullable=False)


class TowerQuestOddsGroup(DeclarativeBase, Base["TowerQuestOddsGroup"]):
    __tablename__ = 'tower_quest_odds_group'

    odds_group_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    team_level_from: int = Column(Integer, primary_key=True, nullable=False)
    team_level_to: int = Column(Integer, primary_key=True, nullable=False)
    treasure_type_1: int = Column(Integer, nullable=False)
    odds_csv_1: str = Column(Text, nullable=False)
    treasure_type_2: int = Column(Integer, nullable=False)
    odds_csv_2: str = Column(Text, nullable=False)
    treasure_type_3: int = Column(Integer, nullable=False)
    odds_csv_3: str = Column(Text, nullable=False)
    treasure_type_4: int = Column(Integer, nullable=False)
    odds_csv_4: str = Column(Text, nullable=False)
    treasure_type_5: int = Column(Integer, nullable=False)
    odds_csv_5: str = Column(Text, nullable=False)
    treasure_type_6: int = Column(Integer, nullable=False)
    odds_csv_6: str = Column(Text, nullable=False)
    treasure_type_7: int = Column(Integer, nullable=False)
    odds_csv_7: str = Column(Text, nullable=False)
    treasure_type_8: int = Column(Integer, nullable=False)
    odds_csv_8: str = Column(Text, nullable=False)
    treasure_type_9: int = Column(Integer, nullable=False)
    odds_csv_9: str = Column(Text, nullable=False)
    treasure_type_10: int = Column(Integer, nullable=False)
    odds_csv_10: str = Column(Text, nullable=False)


class TowerSchedule(DeclarativeBase, Base["TowerSchedule"]):
    __tablename__ = 'tower_schedule'

    tower_schedule_id: int = Column(Integer, primary_key=True)
    max_tower_area_id: int = Column(Integer, nullable=False)
    opening_story_id: int = Column(Integer, nullable=False, index=True)
    count_start_time: str = Column(Text, nullable=False)
    recovery_disable_time: str = Column(Text, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class TowerStoryDatum(DeclarativeBase, Base["TowerStoryDatum"]):
    __tablename__ = 'tower_story_data'

    story_group_id: int = Column(Integer, primary_key=True)
    story_type: int = Column(Integer, nullable=False)
    value: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    thumbnail_id: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class TowerStoryDetail(DeclarativeBase, Base["TowerStoryDetail"]):
    __tablename__ = 'tower_story_detail'

    story_id: int = Column(Integer, primary_key=True)
    story_group_id: int = Column(Integer, nullable=False)
    title: str = Column(Text, nullable=False)
    sub_title: str = Column(Text, nullable=False)
    visible_type: int = Column(Integer, nullable=False)
    story_end: int = Column(Integer, nullable=False)
    pre_story_id: int = Column(Integer, nullable=False)
    love_level: int = Column(Integer, nullable=False)
    requirement_id: int = Column(Integer, nullable=False)
    unlock_quest_id: int = Column(Integer, nullable=False)
    story_quest_id: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_value_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_value_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_value_3: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class TowerWaveGroupDatum(DeclarativeBase, Base["TowerWaveGroupDatum"]):
    __tablename__ = 'tower_wave_group_data'

    id: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, primary_key=True)
    odds: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)


class TrainingQuestDatum(DeclarativeBase, Base["TrainingQuestDatum"]):
    __tablename__ = 'training_quest_data'

    quest_id: int = Column(Integer, primary_key=True)
    area_id: int = Column(Integer, nullable=False)
    quest_name: str = Column(Text, nullable=False)
    limit_team_level: int = Column(Integer, nullable=False)
    unlock_quest_id_1: int = Column(Integer, nullable=False)
    unlock_quest_id_2: int = Column(Integer, nullable=False)
    stamina: int = Column(Integer, nullable=False)
    stamina_start: int = Column(Integer, nullable=False)
    team_exp: int = Column(Integer, nullable=False)
    unit_exp: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    rank_reward_group: int = Column(Integer, nullable=False)
    background_1: int = Column(Integer, nullable=False)
    wave_group_id_1: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_1: str = Column(Text, nullable=False)
    wave_bgm_que_id_1: str = Column(Text, nullable=False)
    background_2: int = Column(Integer, nullable=False)
    wave_group_id_2: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_2: str = Column(Text, nullable=False)
    wave_bgm_que_id_2: str = Column(Text, nullable=False)
    background_3: int = Column(Integer, nullable=False)
    wave_group_id_3: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id_3: str = Column(Text, nullable=False)
    wave_bgm_que_id_3: str = Column(Text, nullable=False)
    enemy_image_1: int = Column(Integer, nullable=False)
    enemy_image_2: int = Column(Integer, nullable=False)
    enemy_image_3: int = Column(Integer, nullable=False)
    enemy_image_4: int = Column(Integer, nullable=False)
    enemy_image_5: int = Column(Integer, nullable=False)
    reward_image_1: int = Column(Integer, nullable=False)
    reward_image_2: int = Column(Integer, nullable=False)
    reward_image_3: int = Column(Integer, nullable=False)
    reward_image_4: int = Column(Integer, nullable=False)
    reward_image_5: int = Column(Integer, nullable=False)
    training_quest_detail_bg_id: int = Column(Integer, nullable=False)
    training_quest_detail_bg_position: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class TrialBattleCategory(DeclarativeBase, Base["TrialBattleCategory"]):
    __tablename__ = 'trial_battle_category'

    category_id: int = Column(Integer, primary_key=True)
    category_name: str = Column(Text, nullable=False)
    icon_id: int = Column(Integer, nullable=False)
    label_type_1: int = Column(Integer, nullable=False)
    label_type_2: int = Column(Integer, nullable=False)
    label_type_3: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    description_detail: str = Column(Text, nullable=False)


class TrialBattleDatum(DeclarativeBase, Base["TrialBattleDatum"]):
    __tablename__ = 'trial_battle_data'

    quest_id: int = Column(Integer, primary_key=True)
    category_id: int = Column(Integer, nullable=False, index=True)
    difficulty: int = Column(Integer, nullable=False)
    battle_name: str = Column(Text, nullable=False)
    detail_bg_id: int = Column(Integer, nullable=False)
    detail_bg_position: int = Column(Integer, nullable=False)
    detail_boss_bg_size: int = Column(Integer, nullable=False)
    detail_boss_bg_height: int = Column(Integer, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    wave_group_id: int = Column(Integer, nullable=False)
    wave_bgm_sheet_id: str = Column(Text, nullable=False)
    wave_bgm_que_id: str = Column(Text, nullable=False)
    clear_reward_group: int = Column(Integer, nullable=False)


class TrialBattleMissionDatum(DeclarativeBase, Base["TrialBattleMissionDatum"]):
    __tablename__ = 'trial_battle_mission_data'

    trial_mission_id: int = Column(Integer, primary_key=True)
    disp_group: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    quest_id: int = Column(Integer, nullable=False)
    condition_value: int = Column(Integer, nullable=False)
    condition_num: int = Column(Integer, nullable=False)
    mission_reward_id: int = Column(Integer, nullable=False)


class TrialBattleMissionReward(DeclarativeBase, Base["TrialBattleMissionReward"]):
    __tablename__ = 'trial_battle_mission_reward'

    id: int = Column(Integer, primary_key=True)
    mission_reward_id: int = Column(Integer, nullable=False, index=True)
    reward_type: int = Column(Integer, nullable=False)
    reward_id: int = Column(Integer, nullable=False)
    reward_num: int = Column(Integer, nullable=False)


class TrialBattleRewardDatum(DeclarativeBase, Base["TrialBattleRewardDatum"]):
    __tablename__ = 'trial_battle_reward_data'

    reward_group_id: int = Column(Integer, primary_key=True)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)


class TtkDrama(DeclarativeBase, Base["TtkDrama"]):
    __tablename__ = 'ttk_drama'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class TtkEnemy(DeclarativeBase, Base["TtkEnemy"]):
    __tablename__ = 'ttk_enemy'

    enemy_id: int = Column(Integer, primary_key=True)
    score: int = Column(Integer, nullable=False)
    coin: int = Column(Integer, nullable=False)
    max: int = Column(Integer, nullable=False)


class TtkNaviComment(DeclarativeBase, Base["TtkNaviComment"]):
    __tablename__ = 'ttk_navi_comment'

    comment_id: int = Column(Integer, primary_key=True)
    where_type: int = Column(Integer, nullable=False)
    character_id: int = Column(Integer, nullable=False)
    face_type: int = Column(Integer, nullable=False)
    character_name: str = Column(Text, nullable=False)
    description: str = Column(Text)
    voice_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    pos_x: float = Column(Float, nullable=False)
    pos_y: float = Column(Float, nullable=False)
    change_face_time: float = Column(Float, nullable=False)
    change_face_type: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class TtkReward(DeclarativeBase, Base["TtkReward"]):
    __tablename__ = 'ttk_reward'

    id: int = Column(Integer, primary_key=True)
    ttk_score: int = Column(Integer, nullable=False, index=True)
    mission_detail: str = Column(Text, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_count_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_count_5: int = Column(Integer, nullable=False)


class TtkScore(DeclarativeBase, Base["TtkScore"]):
    __tablename__ = 'ttk_score'

    difficulty_level: int = Column(Integer, primary_key=True)
    coefficient_difficulty: int = Column(Integer, nullable=False)
    coefficient_coin_score: int = Column(Integer, nullable=False)
    life: int = Column(Integer, nullable=False)
    coefficient_wrong_num: int = Column(Integer, nullable=False)


class TtkStory(DeclarativeBase, Base["TtkStory"]):
    __tablename__ = 'ttk_story'

    ttk_story_id: int = Column(Integer, primary_key=True)
    ttk_score: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)


class TtkStoryScript(DeclarativeBase, Base["TtkStoryScript"]):
    __tablename__ = 'ttk_story_script'

    id: int = Column(Integer, primary_key=True)
    story_id: int = Column(Integer, nullable=False, index=True)
    seq_num: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    line_num: int = Column(Integer, nullable=False)
    start_pos: int = Column(Integer, nullable=False)
    end_pos: int = Column(Integer, nullable=False)
    seek_time: float = Column(Float, nullable=False)
    sheet_name: str = Column(Text, nullable=False)
    cue_name: str = Column(Text, nullable=False)
    command: int = Column(Integer, nullable=False)
    command_param: float = Column(Float, nullable=False)


class TtkWeapon(DeclarativeBase, Base["TtkWeapon"]):
    __tablename__ = 'ttk_weapon'

    ttk_weapon_id: int = Column(Integer, primary_key=True)
    ttk_score: int = Column(Integer, nullable=False, index=True)
    name: str = Column(Text, nullable=False)


class UbAutoDatum(DeclarativeBase, Base["UbAutoDatum"]):
    __tablename__ = 'ub_auto_data'

    ub_auto_id: int = Column(Integer, primary_key=True)
    auto_type: int = Column(Integer, nullable=False)
    auto_detail_1: int = Column(Integer, nullable=False)
    auto_detail_2: int = Column(Integer, nullable=False)
    auto_detail_3: int = Column(Integer, nullable=False)
    auto_detail_4: int = Column(Integer, nullable=False)
    auto_detail_5: int = Column(Integer, nullable=False)
    auto_value_1: int = Column(Integer, nullable=False)
    auto_value_2: int = Column(Integer, nullable=False)
    auto_value_3: int = Column(Integer, nullable=False)
    auto_value_4: int = Column(Integer, nullable=False)
    auto_value_5: int = Column(Integer, nullable=False)


class UbAutoDefine(DeclarativeBase, Base["UbAutoDefine"]):
    __tablename__ = 'ub_auto_define'

    skill_id: int = Column(Integer, primary_key=True)
    ub_auto_id_1: int = Column(Integer, nullable=False)
    ub_auto_id_2: int = Column(Integer, nullable=False)
    ub_auto_id_3: int = Column(Integer, nullable=False)
    ub_auto_id_4: int = Column(Integer, nullable=False)
    ub_auto_id_5: int = Column(Integer, nullable=False)


class UekBos(DeclarativeBase, Base["UekBos"]):
    __tablename__ = 'uek_boss'

    area: int = Column(Integer, primary_key=True)
    quest_name: str = Column(Text, nullable=False)
    limit_time: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    background: int = Column(Integer, nullable=False)
    enemy_id: int = Column(Integer, nullable=False, index=True)
    bgm_sheet_id: str = Column(Text, nullable=False)
    bgm_que_id: str = Column(Text, nullable=False)
    detail_bg_id: int = Column(Integer, nullable=False)
    detail_bg_position: int = Column(Integer, nullable=False)
    detail_boss_bg_size: float = Column(Float, nullable=False)
    detail_boss_bg_height: int = Column(Integer, nullable=False)
    result_boss_position_y: int = Column(Integer, nullable=False)
    result_movie: int = Column(Integer, nullable=False)


class UekDrama(DeclarativeBase, Base["UekDrama"]):
    __tablename__ = 'uek_drama'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class UekMission(DeclarativeBase, Base["UekMission"]):
    __tablename__ = 'uek_mission'

    mission_id: int = Column(Integer, primary_key=True)
    area: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    mission_condition: int = Column(Integer, nullable=False)
    condition_value_1: int = Column(Integer, nullable=False)
    condition_value_2: int = Column(Integer, nullable=False)
    condition_value_3: int = Column(Integer, nullable=False)
    condition_value_4: int = Column(Integer, nullable=False)
    condition_value_5: int = Column(Integer, nullable=False)
    condition_num: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    reward_id_4: int = Column(Integer, nullable=False)
    reward_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    reward_id_5: int = Column(Integer, nullable=False)
    reward_num_5: int = Column(Integer, nullable=False)
    system_id: int = Column(Integer, nullable=False)
    event_id: int = Column(Integer, nullable=False)


class UekSpineAnimLink(DeclarativeBase, Base["UekSpineAnimLink"]):
    __tablename__ = 'uek_spine_anim_link'

    spine_id: int = Column(Integer, primary_key=True)
    anim_num: int = Column(Integer, nullable=False, index=True)


class UniqueEquipEnhanceRate(DeclarativeBase, Base["UniqueEquipEnhanceRate"]):
    __tablename__ = 'unique_equip_enhance_rate'

    id: int = Column(Integer, primary_key=True)
    equipment_id: int = Column(Integer, nullable=False, index=True)
    min_lv: int = Column(Integer, nullable=False)
    max_lv: int = Column(Integer, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class UniqueEquipmentBonu(DeclarativeBase, Base["UniqueEquipmentBonu"]):
    __tablename__ = 'unique_equipment_bonus'

    id: int = Column(Integer, primary_key=True)
    equipment_id: int = Column(Integer, nullable=False, index=True)
    min_lv: int = Column(Integer, nullable=False)
    max_lv: int = Column(Integer, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class UniqueEquipmentCraft(DeclarativeBase, Base["UniqueEquipmentCraft"]):
    __tablename__ = 'unique_equipment_craft'

    equip_id: int = Column(Integer, primary_key=True)
    crafted_cost: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    item_id_1: int = Column(Integer, nullable=False)
    consume_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    item_id_2: int = Column(Integer, nullable=False)
    consume_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    item_id_3: int = Column(Integer, nullable=False)
    consume_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    item_id_4: int = Column(Integer, nullable=False)
    consume_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    item_id_5: int = Column(Integer, nullable=False)
    consume_num_5: int = Column(Integer, nullable=False)
    reward_type_6: int = Column(Integer, nullable=False)
    item_id_6: int = Column(Integer, nullable=False)
    consume_num_6: int = Column(Integer, nullable=False)
    reward_type_7: int = Column(Integer, nullable=False)
    item_id_7: int = Column(Integer, nullable=False)
    consume_num_7: int = Column(Integer, nullable=False)
    reward_type_8: int = Column(Integer, nullable=False)
    item_id_8: int = Column(Integer, nullable=False)
    consume_num_8: int = Column(Integer, nullable=False)
    reward_type_9: int = Column(Integer, nullable=False)
    item_id_9: int = Column(Integer, nullable=False)
    consume_num_9: int = Column(Integer, nullable=False)
    reward_type_10: int = Column(Integer, nullable=False)
    item_id_10: int = Column(Integer, nullable=False)
    consume_num_10: int = Column(Integer, nullable=False)


class UniqueEquipmentDatum(DeclarativeBase, Base["UniqueEquipmentDatum"]):
    __tablename__ = 'unique_equipment_data'

    equipment_id: int = Column(Integer, primary_key=True)
    equipment_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    craft_flg: int = Column(Integer, nullable=False)
    equipment_enhance_point: int = Column(Integer, nullable=False)
    sale_price: int = Column(Integer, nullable=False)
    require_level: int = Column(Integer, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    enable_donation: int = Column(Integer, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class UniqueEquipmentEnhanceDatum(DeclarativeBase, Base["UniqueEquipmentEnhanceDatum"]):
    __tablename__ = 'unique_equipment_enhance_data'

    equip_slot: int = Column(Integer, primary_key=True, nullable=False)
    enhance_level: int = Column(Integer, primary_key=True, nullable=False)
    needed_point: int = Column(Integer, nullable=False)
    total_point: int = Column(Integer, nullable=False)
    needed_mana: int = Column(Integer, nullable=False)
    rank: int = Column(Integer, nullable=False)


class UniqueEquipmentEnhanceRate(DeclarativeBase, Base["UniqueEquipmentEnhanceRate"]):
    __tablename__ = 'unique_equipment_enhance_rate'

    equipment_id: int = Column(Integer, primary_key=True)
    equipment_name: str = Column(Text, nullable=False)
    description: str = Column(Text, nullable=False)
    promotion_level: int = Column(Integer, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class UniqueEquipmentRankup(DeclarativeBase, Base["UniqueEquipmentRankup"]):
    __tablename__ = 'unique_equipment_rankup'

    equip_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    unique_equip_rank: int = Column(Integer, primary_key=True, nullable=False)
    unit_level: int = Column(Integer, nullable=False)
    crafted_cost: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    item_id_1: int = Column(Integer, nullable=False)
    consume_num_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    item_id_2: int = Column(Integer, nullable=False)
    consume_num_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    item_id_3: int = Column(Integer, nullable=False)
    consume_num_3: int = Column(Integer, nullable=False)
    reward_type_4: int = Column(Integer, nullable=False)
    item_id_4: int = Column(Integer, nullable=False)
    consume_num_4: int = Column(Integer, nullable=False)
    reward_type_5: int = Column(Integer, nullable=False)
    item_id_5: int = Column(Integer, nullable=False)
    consume_num_5: int = Column(Integer, nullable=False)
    reward_type_6: int = Column(Integer, nullable=False)
    item_id_6: int = Column(Integer, nullable=False)
    consume_num_6: int = Column(Integer, nullable=False)
    reward_type_7: int = Column(Integer, nullable=False)
    item_id_7: int = Column(Integer, nullable=False)
    consume_num_7: int = Column(Integer, nullable=False)
    reward_type_8: int = Column(Integer, nullable=False)
    item_id_8: int = Column(Integer, nullable=False)
    consume_num_8: int = Column(Integer, nullable=False)
    reward_type_9: int = Column(Integer, nullable=False)
    item_id_9: int = Column(Integer, nullable=False)
    consume_num_9: int = Column(Integer, nullable=False)
    reward_type_10: int = Column(Integer, nullable=False)
    item_id_10: int = Column(Integer, nullable=False)
    consume_num_10: int = Column(Integer, nullable=False)


class UnitAttackPattern(DeclarativeBase, Base["UnitAttackPattern"]):
    __tablename__ = 'unit_attack_pattern'

    pattern_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False)
    loop_start: int = Column(Integer, nullable=False)
    loop_end: int = Column(Integer, nullable=False)
    atk_pattern_1: int = Column(Integer, nullable=False)
    atk_pattern_2: int = Column(Integer, nullable=False)
    atk_pattern_3: int = Column(Integer, nullable=False)
    atk_pattern_4: int = Column(Integer, nullable=False)
    atk_pattern_5: int = Column(Integer, nullable=False)
    atk_pattern_6: int = Column(Integer, nullable=False)
    atk_pattern_7: int = Column(Integer, nullable=False)
    atk_pattern_8: int = Column(Integer, nullable=False)
    atk_pattern_9: int = Column(Integer, nullable=False)
    atk_pattern_10: int = Column(Integer, nullable=False)
    atk_pattern_11: int = Column(Integer, nullable=False)
    atk_pattern_12: int = Column(Integer, nullable=False)
    atk_pattern_13: int = Column(Integer, nullable=False)
    atk_pattern_14: int = Column(Integer, nullable=False)
    atk_pattern_15: int = Column(Integer, nullable=False)
    atk_pattern_16: int = Column(Integer, nullable=False)
    atk_pattern_17: int = Column(Integer, nullable=False)
    atk_pattern_18: int = Column(Integer, nullable=False)
    atk_pattern_19: int = Column(Integer, nullable=False)
    atk_pattern_20: int = Column(Integer, nullable=False)


class UnitBackground(DeclarativeBase, Base["UnitBackground"]):
    __tablename__ = 'unit_background'

    unit_id: int = Column(Integer, primary_key=True)
    unit_name: str = Column(Text, nullable=False)
    bg_id: int = Column(Integer, nullable=False)
    bg_name: str = Column(Text, nullable=False)
    position: float = Column(Float, nullable=False)
    face_type: int = Column(Integer, nullable=False)


class UnitClipSetting(DeclarativeBase, Base["UnitClipSetting"]):
    __tablename__ = 'unit_clip_setting'

    clip_id: int = Column(Integer, primary_key=True)
    center_x: int = Column(Integer, nullable=False)
    size_x: int = Column(Integer, nullable=False)
    softness_x: int = Column(Integer, nullable=False)


class UnitComment(DeclarativeBase, Base["UnitComment"]):
    __tablename__ = 'unit_comments'
    __table_args__ = (
        Index('unit_comments_0_unit_id_1_use_type', 'unit_id', 'use_type'),
    )

    id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False, index=True)
    use_type: int = Column(Integer, nullable=False)
    voice_id: int = Column(Integer, nullable=False)
    face_id: int = Column(Integer, nullable=False)
    change_time: float = Column(Float, nullable=False)
    change_face: int = Column(Integer, nullable=False)
    description: str = Column(Text, nullable=False)
    all_comments_flag: int = Column(Integer, nullable=False)
    target_unit_id: int = Column(Integer, nullable=False)
    face_id_2: int = Column(Integer, nullable=False)
    change_time_2: float = Column(Float, nullable=False)
    change_face_2: int = Column(Integer, nullable=False)
    face_id_3: int = Column(Integer, nullable=False)
    change_time_3: float = Column(Float, nullable=False)
    change_face_3: int = Column(Integer, nullable=False)


class UnitConversion(DeclarativeBase, Base["UnitConversion"]):
    __tablename__ = 'unit_conversion'

    original_unit_id: int = Column(Integer, primary_key=True)
    unit_id: int = Column(Integer, nullable=False, unique=True)


class UnitDatum(DeclarativeBase, Base["UnitDatum"]):
    __tablename__ = 'unit_data'

    unit_id: int = Column(Integer, primary_key=True)
    unit_name: str = Column(Text, nullable=False)
    kana: str = Column(Text, nullable=False)
    prefab_id: int = Column(Integer, nullable=False)
    prefab_id_battle: int = Column(Integer, nullable=False)
    is_limited: int = Column(Integer, nullable=False)
    rarity: int = Column(Integer, nullable=False)
    motion_type: int = Column(Integer, nullable=False)
    se_type: int = Column(Integer, nullable=False)
    move_speed: int = Column(Integer, nullable=False)
    search_area_width: int = Column(Integer, nullable=False)
    atk_type: int = Column(Integer, nullable=False)
    normal_atk_cast_time: float = Column(Float, nullable=False)
    cutin_1: int = Column(Integer, nullable=False)
    cutin_2: int = Column(Integer, nullable=False)
    cutin1_star6: int = Column(Integer, nullable=False)
    cutin2_star6: int = Column(Integer, nullable=False)
    guild_id: int = Column(Integer, nullable=False)
    exskill_display: int = Column(Integer, nullable=False)
    comment: str = Column(Text, nullable=False)
    only_disp_owned: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    original_unit_id: int = Column(Integer, nullable=False)


class UnitEnemyDatum(DeclarativeBase, Base["UnitEnemyDatum"]):
    __tablename__ = 'unit_enemy_data'

    unit_id: int = Column(Integer, primary_key=True)
    unit_name: str = Column(Text, nullable=False)
    prefab_id: int = Column(Integer, nullable=False)
    motion_type: int = Column(Integer, nullable=False)
    se_type: int = Column(Integer, nullable=False)
    move_speed: int = Column(Integer, nullable=False)
    search_area_width: int = Column(Integer, nullable=False)
    atk_type: int = Column(Integer, nullable=False)
    normal_atk_cast_time: float = Column(Float, nullable=False)
    cutin: int = Column(Integer, nullable=False)
    cutin_star6: int = Column(Integer, nullable=False)
    visual_change_flag: int = Column(Integer, nullable=False)
    comment: str = Column(Text, nullable=False)


class UnitIntroduction(DeclarativeBase, Base["UnitIntroduction"]):
    __tablename__ = 'unit_introduction'

    id: int = Column(Integer, primary_key=True)
    gacha_id: int = Column(Integer, nullable=False, index=True)
    introduction_number: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)
    maximum_chunk_size_1: int = Column(Integer, nullable=False)
    maximum_chunk_size_loop_1: int = Column(Integer, nullable=False)
    maximum_chunk_size_2: int = Column(Integer, nullable=False)
    maximum_chunk_size_loop_2: int = Column(Integer, nullable=False)
    maximum_chunk_size_3: int = Column(Integer, nullable=False)
    maximum_chunk_size_loop_3: int = Column(Integer, nullable=False)


class UnitMotionList(DeclarativeBase, Base["UnitMotionList"]):
    __tablename__ = 'unit_motion_list'

    unit_id: int = Column(Integer, primary_key=True)
    sp_motion: int = Column(Integer, nullable=False)


class UnitMypagePo(DeclarativeBase, Base["UnitMypagePo"]):
    __tablename__ = 'unit_mypage_pos'

    id: int = Column(Integer, primary_key=True)
    pos_x: float = Column(Float, nullable=False)
    pos_y: float = Column(Float, nullable=False)
    scale: float = Column(Float, nullable=False)


class UnitPosAdjustment(DeclarativeBase, Base["UnitPosAdjustment"]):
    __tablename__ = 'unit_pos_adjustment'

    unit_id: int = Column(Integer, primary_key=True)
    id_1: int = Column(Integer, nullable=False)
    id_2: int = Column(Integer, nullable=False)
    id_3: int = Column(Integer, nullable=False)
    home_1_pos_x: int = Column(Integer, nullable=False)
    home_1_pos_y: int = Column(Integer, nullable=False)
    home_1_depth: int = Column(Integer, nullable=False)
    home_1_clip: int = Column(Integer, nullable=False)
    home_2_pos_x: int = Column(Integer, nullable=False)
    home_2_pos_y: int = Column(Integer, nullable=False)
    home_2_depth: int = Column(Integer, nullable=False)
    home_2_clip: int = Column(Integer, nullable=False)
    home_3_pos_x: int = Column(Integer, nullable=False)
    home_3_pos_y: int = Column(Integer, nullable=False)
    home_3_depth: int = Column(Integer, nullable=False)
    home_3_clip: int = Column(Integer, nullable=False)
    profile_1_pos_x: int = Column(Integer, nullable=False)
    profile_1_pos_y: int = Column(Integer, nullable=False)
    profile_1_depth: int = Column(Integer, nullable=False)
    profile_1_scale: float = Column(Float, nullable=False)
    profile_1_clip: int = Column(Integer, nullable=False)
    profile_2_pos_x: int = Column(Integer, nullable=False)
    profile_2_pos_y: int = Column(Integer, nullable=False)
    profile_2_depth: int = Column(Integer, nullable=False)
    profile_2_scale: float = Column(Float, nullable=False)
    profile_2_clip: int = Column(Integer, nullable=False)
    profile_3_pos_x: int = Column(Integer, nullable=False)
    profile_3_pos_y: int = Column(Integer, nullable=False)
    profile_3_depth: int = Column(Integer, nullable=False)
    profile_3_scale: float = Column(Float, nullable=False)
    profile_3_clip: int = Column(Integer, nullable=False)
    actual_id1: int = Column(Integer, nullable=False)
    actual_1_pos_x: int = Column(Integer, nullable=False)
    actual_1_pos_y: int = Column(Integer, nullable=False)
    actual_1_depth: int = Column(Integer, nullable=False)
    actual_1_clip: int = Column(Integer, nullable=False)
    actual_id2: int = Column(Integer, nullable=False)
    actual_2_pos_x: int = Column(Integer, nullable=False)
    actual_2_pos_y: int = Column(Integer, nullable=False)
    actual_2_depth: int = Column(Integer, nullable=False)
    actual_2_clip: int = Column(Integer, nullable=False)
    actual_id3: int = Column(Integer, nullable=False)
    actual_3_pos_x: int = Column(Integer, nullable=False)
    actual_3_pos_y: int = Column(Integer, nullable=False)
    actual_3_depth: int = Column(Integer, nullable=False)
    actual_3_clip: int = Column(Integer, nullable=False)
    skip_position_x: int = Column(Integer, nullable=False)
    friend_pos_x: int = Column(Integer, nullable=False)
    is_myprofile_image: int = Column(Integer, nullable=False)


class UnitProfile(DeclarativeBase, Base["UnitProfile"]):
    __tablename__ = 'unit_profile'

    unit_id: int = Column(Integer, primary_key=True)
    unit_name: str = Column(Text, nullable=False)
    age: str = Column(Text, nullable=False)
    guild: str = Column(Text, nullable=False)
    race: str = Column(Text, nullable=False)
    height: str = Column(Text, nullable=False)
    weight: str = Column(Text, nullable=False)
    birth_month: str = Column(Text, nullable=False)
    birth_day: str = Column(Text, nullable=False)
    blood_type: str = Column(Text, nullable=False)
    favorite: str = Column(Text, nullable=False)
    voice: str = Column(Text, nullable=False)
    voice_id: int = Column(Integer, nullable=False)
    catch_copy: str = Column(Text, nullable=False)
    self_text: str = Column(Text, nullable=False)
    guild_id: str = Column(Text, nullable=False)


class UnitPromotion(DeclarativeBase, Base["UnitPromotion"]):
    __tablename__ = 'unit_promotion'

    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    promotion_level: int = Column(Integer, primary_key=True, nullable=False)
    equip_slot_1: int = Column(Integer, nullable=False)
    equip_slot_2: int = Column(Integer, nullable=False)
    equip_slot_3: int = Column(Integer, nullable=False)
    equip_slot_4: int = Column(Integer, nullable=False)
    equip_slot_5: int = Column(Integer, nullable=False)
    equip_slot_6: int = Column(Integer, nullable=False)


class UnitPromotionStatu(DeclarativeBase, Base["UnitPromotionStatu"]):
    __tablename__ = 'unit_promotion_status'

    unit_id: int = Column(Integer, primary_key=True, nullable=False)
    promotion_level: int = Column(Integer, primary_key=True, nullable=False)
    hp: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    accuracy: float = Column(Float, nullable=False)


class UnitRarity(DeclarativeBase, Base["UnitRarity"]):
    __tablename__ = 'unit_rarity'

    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    rarity: int = Column(Integer, primary_key=True, nullable=False)
    hp: float = Column(Float, nullable=False)
    hp_growth: float = Column(Float, nullable=False)
    atk: float = Column(Float, nullable=False)
    atk_growth: float = Column(Float, nullable=False)
    magic_str: float = Column(Float, nullable=False)
    magic_str_growth: float = Column(Float, nullable=False)
    _def: float = Column('def', Float, nullable=False)
    def_growth: float = Column(Float, nullable=False)
    magic_def: float = Column(Float, nullable=False)
    magic_def_growth: float = Column(Float, nullable=False)
    physical_critical: float = Column(Float, nullable=False)
    physical_critical_growth: float = Column(Float, nullable=False)
    magic_critical: float = Column(Float, nullable=False)
    magic_critical_growth: float = Column(Float, nullable=False)
    wave_hp_recovery: float = Column(Float, nullable=False)
    wave_hp_recovery_growth: float = Column(Float, nullable=False)
    wave_energy_recovery: float = Column(Float, nullable=False)
    wave_energy_recovery_growth: float = Column(Float, nullable=False)
    dodge: float = Column(Float, nullable=False)
    dodge_growth: float = Column(Float, nullable=False)
    physical_penetrate: float = Column(Float, nullable=False)
    physical_penetrate_growth: float = Column(Float, nullable=False)
    magic_penetrate: float = Column(Float, nullable=False)
    magic_penetrate_growth: float = Column(Float, nullable=False)
    life_steal: float = Column(Float, nullable=False)
    life_steal_growth: float = Column(Float, nullable=False)
    hp_recovery_rate: float = Column(Float, nullable=False)
    hp_recovery_rate_growth: float = Column(Float, nullable=False)
    energy_recovery_rate: float = Column(Float, nullable=False)
    energy_recovery_rate_growth: float = Column(Float, nullable=False)
    energy_reduce_rate: float = Column(Float, nullable=False)
    energy_reduce_rate_growth: float = Column(Float, nullable=False)
    unit_material_id: int = Column(Integer, nullable=False, index=True)
    consume_num: int = Column(Integer, nullable=False)
    consume_gold: int = Column(Integer, nullable=False)
    accuracy: float = Column(Float, nullable=False)
    accuracy_growth: float = Column(Float, nullable=False)


class UnitSkillDatum(DeclarativeBase, Base["UnitSkillDatum"]):
    __tablename__ = 'unit_skill_data'

    unit_id: int = Column(Integer, primary_key=True)
    union_burst: int = Column(Integer, nullable=False)
    main_skill_1: int = Column(Integer, nullable=False)
    main_skill_2: int = Column(Integer, nullable=False)
    main_skill_3: int = Column(Integer, nullable=False)
    main_skill_4: int = Column(Integer, nullable=False)
    main_skill_5: int = Column(Integer, nullable=False)
    main_skill_6: int = Column(Integer, nullable=False)
    main_skill_7: int = Column(Integer, nullable=False)
    main_skill_8: int = Column(Integer, nullable=False)
    main_skill_9: int = Column(Integer, nullable=False)
    main_skill_10: int = Column(Integer, nullable=False)
    ex_skill_1: int = Column(Integer, nullable=False)
    ex_skill_evolution_1: int = Column(Integer, nullable=False)
    ex_skill_2: int = Column(Integer, nullable=False)
    ex_skill_evolution_2: int = Column(Integer, nullable=False)
    ex_skill_3: int = Column(Integer, nullable=False)
    ex_skill_evolution_3: int = Column(Integer, nullable=False)
    ex_skill_4: int = Column(Integer, nullable=False)
    ex_skill_evolution_4: int = Column(Integer, nullable=False)
    ex_skill_5: int = Column(Integer, nullable=False)
    ex_skill_evolution_5: int = Column(Integer, nullable=False)
    sp_union_burst: int = Column(Integer, nullable=False)
    sp_skill_1: int = Column(Integer, nullable=False)
    sp_skill_2: int = Column(Integer, nullable=False)
    sp_skill_3: int = Column(Integer, nullable=False)
    sp_skill_4: int = Column(Integer, nullable=False)
    sp_skill_5: int = Column(Integer, nullable=False)
    union_burst_evolution: int = Column(Integer, nullable=False)
    main_skill_evolution_1: int = Column(Integer, nullable=False)
    main_skill_evolution_2: int = Column(Integer, nullable=False)
    sp_skill_evolution_1: int = Column(Integer, nullable=False)
    sp_skill_evolution_2: int = Column(Integer, nullable=False)


class UnitSkillDataRf(DeclarativeBase, Base["UnitSkillDataRf"]):
    __tablename__ = 'unit_skill_data_rf'

    id: int = Column(Integer, primary_key=True)
    skill_id: int = Column(Integer, nullable=False, index=True)
    rf_skill_id: int = Column(Integer, nullable=False, index=True)
    min_lv: int = Column(Integer, nullable=False)
    max_lv: int = Column(Integer, nullable=False)


class UnitStatusCoefficient(DeclarativeBase, Base["UnitStatusCoefficient"]):
    __tablename__ = 'unit_status_coefficient'

    coefficient_id: int = Column(Integer, primary_key=True)
    hp_coefficient: float = Column(Float, nullable=False)
    atk_coefficient: float = Column(Float, nullable=False)
    magic_str_coefficient: float = Column(Float, nullable=False)
    def_coefficient: float = Column(Float, nullable=False)
    magic_def_coefficient: float = Column(Float, nullable=False)
    physical_critical_coefficient: float = Column(Float, nullable=False)
    magic_critical_coefficient: float = Column(Float, nullable=False)
    wave_hp_recovery_coefficient: float = Column(Float, nullable=False)
    wave_energy_recovery_coefficient: float = Column(Float, nullable=False)
    dodge_coefficient: float = Column(Float, nullable=False)
    physical_penetrate_coefficient: float = Column(Float, nullable=False)
    magic_penetrate_coefficient: float = Column(Float, nullable=False)
    life_steal_coefficient: float = Column(Float, nullable=False)
    hp_recovery_rate_coefficient: float = Column(Float, nullable=False)
    energy_recovery_rate_coefficient: float = Column(Float, nullable=False)
    energy_reduce_rate_coefficient: float = Column(Float, nullable=False)
    skill_lv_coefficient: float = Column(Float, nullable=False)
    exskill_evolution_coefficient: int = Column(Integer, nullable=False)
    overall_coefficient: float = Column(Float, nullable=False)
    accuracy_coefficient: float = Column(Float, nullable=False)
    skill1_evolution_coefficient: int = Column(Integer, nullable=False)
    skill1_evolution_slv_coefficient: float = Column(Float, nullable=False)
    ub_evolution_coefficient: int = Column(Integer, nullable=False)
    ub_evolution_slv_coefficient: float = Column(Float, nullable=False)


class UnitUniqueEquip(DeclarativeBase, Base["UnitUniqueEquip"]):
    __tablename__ = 'unit_unique_equip'

    unit_id: int = Column(Integer, primary_key=True)
    equip_slot: int = Column(Integer, nullable=False)
    equip_id: int = Column(Integer, nullable=False)


class UnlockRarity6(DeclarativeBase, Base["UnlockRarity6"]):
    __tablename__ = 'unlock_rarity_6'
    __table_args__ = (
        Index('unlock_rarity_6_0_unit_id_1_unlock_level', 'unit_id', 'unlock_level'),
        Index('unlock_rarity_6_0_unit_id_1_slot_id', 'unit_id', 'slot_id')
    )

    unit_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    slot_id: int = Column(Integer, primary_key=True, nullable=False)
    unlock_level: int = Column(Integer, primary_key=True, nullable=False)
    unlock_flag: int = Column(Integer, nullable=False)
    consume_gold: int = Column(Integer, nullable=False)
    material_type: int = Column(Integer, nullable=False)
    material_id: int = Column(Integer, nullable=False, index=True)
    material_count: int = Column(Integer, nullable=False)
    hp: int = Column(Integer, nullable=False)
    atk: int = Column(Integer, nullable=False)
    magic_str: int = Column(Integer, nullable=False)
    _def: int = Column('def', Integer, nullable=False)
    magic_def: int = Column(Integer, nullable=False)
    physical_critical: int = Column(Integer, nullable=False)
    magic_critical: int = Column(Integer, nullable=False)
    wave_hp_recovery: int = Column(Integer, nullable=False)
    wave_energy_recovery: int = Column(Integer, nullable=False)
    dodge: int = Column(Integer, nullable=False)
    physical_penetrate: int = Column(Integer, nullable=False)
    magic_penetrate: int = Column(Integer, nullable=False)
    life_steal: int = Column(Integer, nullable=False)
    hp_recovery_rate: int = Column(Integer, nullable=False)
    energy_recovery_rate: int = Column(Integer, nullable=False)
    energy_reduce_rate: int = Column(Integer, nullable=False)
    accuracy: int = Column(Integer, nullable=False)


class UnlockSkillDatum(DeclarativeBase, Base["UnlockSkillDatum"]):
    __tablename__ = 'unlock_skill_data'

    promotion_level: int = Column(Integer, nullable=False)
    unlock_skill: int = Column(Integer, primary_key=True)


class UnlockUnitCondition(DeclarativeBase, Base["UnlockUnitCondition"]):
    __tablename__ = 'unlock_unit_condition'

    unit_id: int = Column(Integer, primary_key=True)
    unit_name: str = Column(Text, nullable=False)
    class_id: int = Column(Integer, nullable=False)
    pre_unit_id: int = Column(Integer, nullable=False)
    condition_type_1: int = Column(Integer, nullable=False)
    condition_type_detail_1: int = Column(Integer, nullable=False)
    condition_id_1: int = Column(Integer, nullable=False)
    count_1: int = Column(Integer, nullable=False)
    condition_type_2: int = Column(Integer, nullable=False)
    condition_type_detail_2: int = Column(Integer, nullable=False)
    condition_id_2: int = Column(Integer, nullable=False)
    count_2: int = Column(Integer, nullable=False)
    condition_type_3: int = Column(Integer, nullable=False)
    condition_type_detail_3: int = Column(Integer, nullable=False)
    condition_id_3: int = Column(Integer, nullable=False)
    count_3: int = Column(Integer, nullable=False)
    condition_type_4: int = Column(Integer, nullable=False)
    condition_type_detail_4: int = Column(Integer, nullable=False)
    condition_id_4: int = Column(Integer, nullable=False)
    count_4: int = Column(Integer, nullable=False)
    condition_type_5: int = Column(Integer, nullable=False)
    condition_type_detail_5: int = Column(Integer, nullable=False)
    condition_id_5: int = Column(Integer, nullable=False)
    count_5: int = Column(Integer, nullable=False)
    release_effect_type: int = Column(Integer, nullable=False)


class VisualCustomize(DeclarativeBase, Base["VisualCustomize"]):
    __tablename__ = 'visual_customize'

    id: int = Column(Integer, primary_key=True)
    title_prefab: int = Column(Integer, nullable=False)
    title_movie: int = Column(Integer, nullable=False)
    title_voice: int = Column(Integer, nullable=False)
    story_top_movie: int = Column(Integer, nullable=False)
    quest_top_movie: int = Column(Integer, nullable=False)
    profile_logo: int = Column(Integer, nullable=False)
    watched_story_id: int = Column(Integer, nullable=False)
    start_time: str = Column(Text, nullable=False)
    end_time: str = Column(Text, nullable=False)


class VoiceGroup(DeclarativeBase, Base["VoiceGroup"]):
    __tablename__ = 'voice_group'

    group_id: int = Column(Integer, primary_key=True)
    group_id_comment: str = Column(Text, nullable=False)
    group_unit_id_01: int = Column(Integer, nullable=False)
    group_unit_id_02: int = Column(Integer, nullable=False)
    group_unit_id_03: int = Column(Integer, nullable=False)
    group_unit_id_04: int = Column(Integer, nullable=False)
    group_unit_id_05: int = Column(Integer, nullable=False)


class VoiceGroupChara(DeclarativeBase, Base["VoiceGroupChara"]):
    __tablename__ = 'voice_group_chara'

    group_unit_id: int = Column(Integer, primary_key=True)
    group_unit_id_comment: str = Column(Text, nullable=False)
    unit_id_01: int = Column(Integer, nullable=False)
    unit_id_02: int = Column(Integer, nullable=False)
    unit_id_03: int = Column(Integer, nullable=False)
    unit_id_04: int = Column(Integer, nullable=False)
    unit_id_05: int = Column(Integer, nullable=False)
    unit_id_06: int = Column(Integer, nullable=False)
    unit_id_07: int = Column(Integer, nullable=False)
    unit_id_08: int = Column(Integer, nullable=False)
    unit_id_09: int = Column(Integer, nullable=False)
    unit_id_10: int = Column(Integer, nullable=False)


class VoteDatum(DeclarativeBase, Base["VoteDatum"]):
    __tablename__ = 'vote_data'

    vote_id: int = Column(Integer, primary_key=True)
    vote_start_time: str = Column(Text, nullable=False)
    vote_end_time: str = Column(Text, nullable=False)
    result_start_time: str = Column(Text, nullable=False)
    result_end_time: str = Column(Text, nullable=False)
    start_story_id: int = Column(Integer, nullable=False)
    result_story_id: int = Column(Integer, nullable=False)


class VoteInfo(DeclarativeBase, Base["VoteInfo"]):
    __tablename__ = 'vote_info'

    vote_id: int = Column(Integer, primary_key=True, nullable=False)
    vote_help_index: int = Column(Integer, primary_key=True, nullable=False)
    vote_title: str = Column(Text, nullable=False)
    vote_help: str = Column(Text, nullable=False)


class VoteUnit(DeclarativeBase, Base["VoteUnit"]):
    __tablename__ = 'vote_unit'

    vote_id: int = Column(Integer, primary_key=True, nullable=False)
    unit_id: int = Column(Integer, primary_key=True, nullable=False)
    unit_rarity: int = Column(Integer, nullable=False)


class WacBirthdayDramaScript(DeclarativeBase, Base["WacBirthdayDramaScript"]):
    __tablename__ = 'wac_birthday_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class WacDatum(DeclarativeBase, Base["WacDatum"]):
    __tablename__ = 'wac_data'

    wac_id: int = Column(Integer, primary_key=True, nullable=False)
    date_id: int = Column(Integer, primary_key=True, nullable=False)
    unlock_time: str = Column(Text, nullable=False)
    pre_drama_id: int = Column(Integer, nullable=False)
    post_drama_id: int = Column(Integer, nullable=False)
    idle_drama_id: int = Column(Integer, nullable=False)
    bg_id: int = Column(Integer, nullable=False)
    effect_id: int = Column(Integer, nullable=False)
    mural_group_id: int = Column(Integer, nullable=False, index=True)
    mural_offset_x: float = Column(Float, nullable=False)
    birthday_login_bonus_id: int = Column(Integer, nullable=False)
    unit_id_1: int = Column(Integer, nullable=False)
    unit_id_2: int = Column(Integer, nullable=False)
    draw_end_to_center: int = Column(Integer, nullable=False)


class WacDramaScript(DeclarativeBase, Base["WacDramaScript"]):
    __tablename__ = 'wac_drama_script'

    command_id: int = Column(Integer, primary_key=True)
    drama_id: int = Column(Integer, nullable=False, index=True)
    command_type: int = Column(Integer, nullable=False)
    param_01: str = Column(Text, nullable=False)
    param_02: str = Column(Text, nullable=False)
    param_03: str = Column(Text, nullable=False)
    param_04: str = Column(Text, nullable=False)
    param_05: str = Column(Text, nullable=False)
    param_06: str = Column(Text, nullable=False)
    param_07: str = Column(Text, nullable=False)
    param_08: str = Column(Text, nullable=False)


class WacMuralBgDatum(DeclarativeBase, Base["WacMuralBgDatum"]):
    __tablename__ = 'wac_mural_bg_data'

    wac_id: int = Column(Integer, primary_key=True, nullable=False)
    date_id: int = Column(Integer, primary_key=True, nullable=False)
    bg_id: int = Column(Integer, nullable=False)
    type: int = Column(Integer, nullable=False)
    start_offset_x: str = Column(Text, nullable=False)
    end_offset_x: str = Column(Text, nullable=False)


class WacMuralDatum(DeclarativeBase, Base["WacMuralDatum"]):
    __tablename__ = 'wac_mural_data'

    mural_group_id: int = Column(Integer, primary_key=True, nullable=False, index=True)
    date_id: int = Column(Integer, primary_key=True, nullable=False)
    parts_id: int = Column(Integer, nullable=False)
    pos_x: int = Column(Integer, nullable=False)
    pos_y: int = Column(Integer, nullable=False)
    depth: int = Column(Integer, nullable=False)
    width: int = Column(Integer, nullable=False)
    height: int = Column(Integer, nullable=False)


class WacPresentStillDatum(DeclarativeBase, Base["WacPresentStillDatum"]):
    __tablename__ = 'wac_present_still_data'

    wac_id: int = Column(Integer, primary_key=True, nullable=False)
    date_id: int = Column(Integer, primary_key=True, nullable=False)
    still_id: int = Column(Integer, nullable=False)


class WaveGroupDatum(DeclarativeBase, Base["WaveGroupDatum"]):
    __tablename__ = 'wave_group_data'

    id: int = Column(Integer, primary_key=True)
    wave_group_id: int = Column(Integer, nullable=False)
    odds: int = Column(Integer, nullable=False)
    enemy_id_1: int = Column(Integer, nullable=False)
    drop_gold_1: int = Column(Integer, nullable=False)
    drop_reward_id_1: int = Column(Integer, nullable=False)
    enemy_id_2: int = Column(Integer, nullable=False)
    drop_gold_2: int = Column(Integer, nullable=False)
    drop_reward_id_2: int = Column(Integer, nullable=False)
    enemy_id_3: int = Column(Integer, nullable=False)
    drop_gold_3: int = Column(Integer, nullable=False)
    drop_reward_id_3: int = Column(Integer, nullable=False)
    enemy_id_4: int = Column(Integer, nullable=False)
    drop_gold_4: int = Column(Integer, nullable=False)
    drop_reward_id_4: int = Column(Integer, nullable=False)
    enemy_id_5: int = Column(Integer, nullable=False)
    drop_gold_5: int = Column(Integer, nullable=False)
    drop_reward_id_5: int = Column(Integer, nullable=False)
    guest_enemy_id: int = Column(Integer, nullable=False)
    guest_lane: int = Column(Integer, nullable=False)

    def get_drop_reward_ids(self) -> Iterator[int]:
        yield self.drop_reward_id_1
        yield self.drop_reward_id_2
        yield self.drop_reward_id_3
        yield self.drop_reward_id_4
        yield self.drop_reward_id_5

class Worldmap(DeclarativeBase, Base["Worldmap"]):
    __tablename__ = 'worldmap'

    course_id: int = Column(Integer, primary_key=True)
    name: str = Column(Text, nullable=False)
    map_id: int = Column(Integer, nullable=False)
    sheet_id: str = Column(Text, nullable=False)
    que_id: str = Column(Text, nullable=False)
    start_area_id: int = Column(Integer, nullable=False)
    end_area_id: int = Column(Integer, nullable=False)


class YsnStoryDatum(DeclarativeBase, Base["YsnStoryDatum"]):
    __tablename__ = 'ysn_story_data'

    sub_story_id: int = Column(Integer, primary_key=True)
    original_event_id: int = Column(Integer, nullable=False, index=True)
    title: str = Column(Text, nullable=False)
    condition_story_id: int = Column(Integer, nullable=False)
    disp_order: int = Column(Integer, nullable=False)
    reward_type_1: int = Column(Integer, nullable=False)
    reward_id_1: int = Column(Integer, nullable=False)
    reward_count_1: int = Column(Integer, nullable=False)
    reward_type_2: int = Column(Integer, nullable=False)
    reward_id_2: int = Column(Integer, nullable=False)
    reward_count_2: int = Column(Integer, nullable=False)
    reward_type_3: int = Column(Integer, nullable=False)
    reward_id_3: int = Column(Integer, nullable=False)
    reward_count_3: int = Column(Integer, nullable=False)
