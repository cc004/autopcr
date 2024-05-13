# coding: utf-8
# type: ignore
# Data( => Datum(

from typing import Optional

from sqlalchemy import Float, Index, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from typing import Generic, TypeVar
from ..util.linq import flow

T = TypeVar('T')

class Base(DeclarativeBase, Generic[T]):
    @classmethod
    def query(cls, session: Session) -> flow[T]:
        return flow(session.query(cls).all())


class ActualUnitBackground(Base):
    __tablename__ = 'actual_unit_background'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text)
    bg_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)


class AilmentDatum(Base):
    __tablename__ = 'ailment_data'

    ailment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ailment_action: Mapped[int] = mapped_column(Integer)
    ailment_detail_1: Mapped[int] = mapped_column(Integer)
    ailment_name: Mapped[str] = mapped_column(Text)


class AlbumProductionList(Base):
    __tablename__ = 'album_production_list'
    __table_args__ = (
        Index('album_production_list_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class AlbumVoiceList(Base):
    __tablename__ = 'album_voice_list'
    __table_args__ = (
        Index('album_voice_list_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class ApaSchedule(Base):
    __tablename__ = 'apa_schedule'

    apa_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)
    op_story_id: Mapped[int] = mapped_column(Integer)
    ed_story_id: Mapped[int] = mapped_column(Integer)
    url_1: Mapped[str] = mapped_column(Text)
    url_2: Mapped[str] = mapped_column(Text)
    url_3: Mapped[str] = mapped_column(Text)


class AppIcon(Base):
    __tablename__ = 'app_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ArcadeDescription(Base):
    __tablename__ = 'arcade_description'
    __table_args__ = (
        Index('arcade_description_0_arcade_id', 'arcade_id'),
        Index('arcade_description_0_arcade_id_1_type', 'arcade_id', 'type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arcade_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    image_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class ArcadeList(Base):
    __tablename__ = 'arcade_list'

    arcade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    cue_id: Mapped[str] = mapped_column(Text)
    where_type: Mapped[int] = mapped_column(Integer)
    banner_start_time: Mapped[str] = mapped_column(Text)
    banner_end_time: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    clan_chat_title: Mapped[str] = mapped_column(Text)


class ArcadeStoryList(Base):
    __tablename__ = 'arcade_story_list'
    __table_args__ = (
        Index('arcade_story_list_0_arcade_id', 'arcade_id'),
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arcade_id: Mapped[int] = mapped_column(Integer)
    sub_title: Mapped[str] = mapped_column(Text)


class ArenaDailyRankReward(Base):
    __tablename__ = 'arena_daily_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ArenaDefenceReward(Base):
    __tablename__ = 'arena_defence_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_count: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ArenaMaxRankReward(Base):
    __tablename__ = 'arena_max_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ArenaMaxSeasonRankReward(Base):
    __tablename__ = 'arena_max_season_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class Asm4ChoiceDatum(Base):
    __tablename__ = 'asm_4_choice_data'

    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    choice_1: Mapped[str] = mapped_column(Text)
    image_id_1: Mapped[int] = mapped_column(Integer)
    choice_2: Mapped[str] = mapped_column(Text)
    image_id_2: Mapped[int] = mapped_column(Integer)
    choice_3: Mapped[str] = mapped_column(Text)
    image_id_3: Mapped[int] = mapped_column(Integer)
    choice_4: Mapped[str] = mapped_column(Text)
    image_id_4: Mapped[int] = mapped_column(Integer)
    correct_answer: Mapped[int] = mapped_column(Integer)


class AsmArchiveCompletionReward(Base):
    __tablename__ = 'asm_archive_completion_reward'
    __table_args__ = (
        Index('asm_archive_completion_reward_0_emblem_id', 'emblem_id'),
    )

    archive_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_detail: Mapped[str] = mapped_column(Text)
    emblem_id: Mapped[int] = mapped_column(Integer)


class AsmDatum(Base):
    __tablename__ = 'asm_data'
    __table_args__ = (
        Index('asm_data_0_difficulty', 'difficulty'),
        Index('asm_data_0_genre_id', 'genre_id'),
        Index('asm_data_0_genre_id_1_difficulty', 'genre_id', 'difficulty')
    )

    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    asm_type: Mapped[int] = mapped_column(Integer)
    image_id: Mapped[int] = mapped_column(Integer)
    detail: Mapped[str] = mapped_column(Text)
    category: Mapped[int] = mapped_column(Integer)


class AsmGameSetting(Base):
    __tablename__ = 'asm_game_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lottery_rate: Mapped[float] = mapped_column(Float)
    normal_limit_time: Mapped[int] = mapped_column(Integer)
    normal_quiz_num: Mapped[int] = mapped_column(Integer)
    concentration_limit_time: Mapped[int] = mapped_column(Integer)
    concentration_quiz_limit_num: Mapped[int] = mapped_column(Integer)
    incorrect_answer_penalty_time: Mapped[int] = mapped_column(Integer)
    help_use_count_normal: Mapped[int] = mapped_column(Integer)
    help_use_count_hard: Mapped[int] = mapped_column(Integer)
    help_use_count_veryhard: Mapped[int] = mapped_column(Integer)
    limit_score: Mapped[int] = mapped_column(Integer)
    unlock_concentration_mode_score_1: Mapped[int] = mapped_column(Integer)
    unlock_concentration_mode_score_2: Mapped[int] = mapped_column(Integer)


class AsmManyAnswersDatum(Base):
    __tablename__ = 'asm_many_answers_data'

    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    choice_1: Mapped[str] = mapped_column(Text)
    image_id_1: Mapped[int] = mapped_column(Integer)
    choice_2: Mapped[str] = mapped_column(Text)
    image_id_2: Mapped[int] = mapped_column(Integer)
    choice_3: Mapped[str] = mapped_column(Text)
    image_id_3: Mapped[int] = mapped_column(Integer)
    choice_4: Mapped[str] = mapped_column(Text)
    image_id_4: Mapped[int] = mapped_column(Integer)
    is_correct_1: Mapped[int] = mapped_column(Integer)
    is_correct_2: Mapped[int] = mapped_column(Integer)
    is_correct_3: Mapped[int] = mapped_column(Integer)
    is_correct_4: Mapped[int] = mapped_column(Integer)


class AsmMemoryGauge(Base):
    __tablename__ = 'asm_memory_gauge'
    __table_args__ = (
        Index('asm_memory_gauge_0_gauge_id', 'gauge_id'),
        Index('asm_memory_gauge_0_unlock_story_id', 'unlock_story_id')
    )

    gauge_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trigger_score: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_detail: Mapped[str] = mapped_column(Text)
    unlock_story_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class AsmReactionDatum(Base):
    __tablename__ = 'asm_reaction_data'
    __table_args__ = (
        Index('asm_reaction_data_0_unit_id_1_reaction_type', 'unit_id', 'reaction_type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[int] = mapped_column(Integer)
    reaction_type: Mapped[int] = mapped_column(Integer)
    condition_param_1: Mapped[int] = mapped_column(Integer)
    condition_param_2: Mapped[int] = mapped_column(Integer)
    condition_param_3: Mapped[int] = mapped_column(Integer)
    face_id: Mapped[int] = mapped_column(Integer)
    face_change_time: Mapped[float] = mapped_column(Float)
    change_face_id: Mapped[int] = mapped_column(Integer)
    face_change_effect_id: Mapped[int] = mapped_column(Integer)
    cue_name: Mapped[str] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)


class AsmTrueOrFalseDatum(Base):
    __tablename__ = 'asm_true_or_false_data'

    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    correct_answer: Mapped[int] = mapped_column(Integer)


class Banner(Base):
    __tablename__ = 'banner'

    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    system_id: Mapped[int] = mapped_column(Integer)
    gacha_id: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    priority: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[str] = mapped_column(Text)
    end_date: Mapped[str] = mapped_column(Text)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer)
    is_show_room: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(Text)
    show_type: Mapped[int] = mapped_column(Integer)
    thumbnail_id: Mapped[int] = mapped_column(Integer)
    poster_id: Mapped[int] = mapped_column(Integer)


class BeginnerCharaETicketDatum(Base):
    __tablename__ = 'beginner_chara_e_ticket_data'

    beginner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beginner_type: Mapped[int] = mapped_column(Integer)
    jewel_store_id: Mapped[int] = mapped_column(Integer)
    chara_e_ticket_id: Mapped[int] = mapped_column(Integer)
    beginner_limit_hour: Mapped[int] = mapped_column(Integer)
    forced_exchange_hour: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    icon_id: Mapped[int] = mapped_column(Integer)


class BgDatum(Base):
    __tablename__ = 'bg_data'

    view_name: Mapped[str] = mapped_column(Text, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)


class BirthdayLoginBonusDatum(Base):
    __tablename__ = 'birthday_login_bonus_data'

    login_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    login_bonus_type: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    adv_id: Mapped[int] = mapped_column(Integer)


class BirthdayLoginBonusDetail(Base):
    __tablename__ = 'birthday_login_bonus_detail'
    __table_args__ = (
        Index('birthday_login_bonus_detail_0_login_bonus_id', 'login_bonus_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class BirthdayLoginBonusDramaScript(Base):
    __tablename__ = 'birthday_login_bonus_drama_script'
    __table_args__ = (
        Index('birthday_login_bonus_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class BmyNaviComment(Base):
    __tablename__ = 'bmy_navi_comment'
    __table_args__ = (
        Index('bmy_navi_comment_0_where_type', 'where_type'),
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    voice_id: Mapped[int] = mapped_column(Integer)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    original_event_id: Mapped[int] = mapped_column(Integer)


class BmyStoryDatum(Base):
    __tablename__ = 'bmy_story_data'
    __table_args__ = (
        Index('bmy_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class BroadcastSchedule(Base):
    __tablename__ = 'broadcast_schedule'

    broadcast_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(Text)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class BywayBattleQuestDatum(Base):
    __tablename__ = 'byway_battle_quest_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auto_restrict_type: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer)
    enemy_image_1: Mapped[int] = mapped_column(Integer)
    enemy_image_2: Mapped[int] = mapped_column(Integer)
    enemy_image_3: Mapped[int] = mapped_column(Integer)
    enemy_image_4: Mapped[int] = mapped_column(Integer)
    enemy_image_5: Mapped[int] = mapped_column(Integer)


class BywayDeliveryQuestDatum(Base):
    __tablename__ = 'byway_delivery_quest_data'
    __table_args__ = (
        Index('byway_delivery_quest_data_0_quest_id', 'quest_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_category: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    consume_num: Mapped[int] = mapped_column(Integer)


class BywayQuestDatum(Base):
    __tablename__ = 'byway_quest_data'
    __table_args__ = (
        Index('byway_quest_data_0_area_id', 'area_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    byway_quest_type: Mapped[int] = mapped_column(Integer)
    area_id: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    detail: Mapped[str] = mapped_column(Text)


class BywayStoryDetail(Base):
    __tablename__ = 'byway_story_detail'
    __table_args__ = (
        Index('byway_story_detail_0_pre_story_id', 'pre_story_id'),
        Index('byway_story_detail_0_unlock_quest_id', 'unlock_quest_id')
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_type: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    visible_type: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    lock_all_text: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_value_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_value_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_value_3: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class CampaignBeginnerDatum(Base):
    __tablename__ = 'campaign_beginner_data'

    beginner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_from: Mapped[int] = mapped_column(Integer)
    id_to: Mapped[int] = mapped_column(Integer)


class CampaignFreegacha(Base):
    __tablename__ = 'campaign_freegacha'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer)
    freegacha_1: Mapped[int] = mapped_column(Integer)
    freegacha_10: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    stock_10_flag: Mapped[int] = mapped_column(Integer)
    relation_id: Mapped[int] = mapped_column(Integer)
    relation_count: Mapped[int] = mapped_column(Integer)


class CampaignFreegachaDatum(Base):
    __tablename__ = 'campaign_freegacha_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer)
    gacha_id: Mapped[int] = mapped_column(Integer)


class CampaignFreegachaSp(Base):
    __tablename__ = 'campaign_freegacha_sp'

    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_exec_count: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class CampaignLevelDatum(Base):
    __tablename__ = 'campaign_level_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level_id: Mapped[int] = mapped_column(Integer)
    lv_from: Mapped[int] = mapped_column(Integer)
    lv_to: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    label_color: Mapped[str] = mapped_column(Text)
    frame_color: Mapped[str] = mapped_column(Text)


class CampaignMissionCategory(Base):
    __tablename__ = 'campaign_mission_category'
    __table_args__ = (
        Index('campaign_mission_category_0_campaign_id_1_type', 'campaign_id', 'type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    lv_from: Mapped[int] = mapped_column(Integer)
    lv_to: Mapped[int] = mapped_column(Integer)


class CampaignMissionDatum(Base):
    __tablename__ = 'campaign_mission_data'
    __table_args__ = (
        Index('campaign_mission_data_0_campaign_id', 'campaign_id'),
        Index('campaign_mission_data_0_campaign_id_1_type', 'campaign_id', 'type')
    )

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    campaign_mission_reward_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    min_level: Mapped[int] = mapped_column(Integer)
    max_level: Mapped[int] = mapped_column(Integer)
    title_color_id: Mapped[int] = mapped_column(Integer)
    visible_flag: Mapped[int] = mapped_column(Integer)
    mark_flag: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class CampaignMissionRewardDatum(Base):
    __tablename__ = 'campaign_mission_reward_data'
    __table_args__ = (
        Index('campaign_mission_reward_data_0_campaign_mission_reward_id', 'campaign_mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class CampaignMissionSchedule(Base):
    __tablename__ = 'campaign_mission_schedule'

    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)


class CampaignSchedule(Base):
    __tablename__ = 'campaign_schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_category: Mapped[int] = mapped_column(Integer)
    value: Mapped[float] = mapped_column(Float)
    system_id: Mapped[int] = mapped_column(Integer)
    icon_image: Mapped[int] = mapped_column(Integer)
    lv_from: Mapped[int] = mapped_column(Integer)
    lv_to: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    level_id: Mapped[int] = mapped_column(Integer)
    shiori_group_id: Mapped[int] = mapped_column(Integer)
    duplication_order: Mapped[int] = mapped_column(Integer)
    beginner_id: Mapped[int] = mapped_column(Integer)
    campaign_type: Mapped[int] = mapped_column(Integer)


class CampaignShioriGroup(Base):
    __tablename__ = 'campaign_shiori_group'
    __table_args__ = (
        Index('campaign_shiori_group_0_shiori_group_id', 'shiori_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shiori_group_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)


class CaravanBuffDisp(Base):
    __tablename__ = 'caravan_buff_disp'
    __table_args__ = (
        Index('caravan_buff_disp_0_type_1_effect_id', 'type', 'effect_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    effect_id: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    count_from: Mapped[int] = mapped_column(Integer)
    count_to: Mapped[int] = mapped_column(Integer)


class CaravanCoinShopLineup(Base):
    __tablename__ = 'caravan_coin_shop_lineup'
    __table_args__ = (
        Index('caravan_coin_shop_lineup_0_season_id', 'season_id'),
    )

    season_id: Mapped[int] = mapped_column(Integer)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    currency_id: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    stock: Mapped[int] = mapped_column(Integer)


class CaravanDiceRewardPeriod(Base):
    __tablename__ = 'caravan_dice_reward_period'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class CaravanDish(Base):
    __tablename__ = 'caravan_dish'

    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    new_line_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    effect_description: Mapped[str] = mapped_column(Text)
    sub_effect_description: Mapped[str] = mapped_column(Text)
    sold_price: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(Integer)
    effect_type: Mapped[int] = mapped_column(Integer)
    effect_value: Mapped[int] = mapped_column(Integer)
    effect_turn: Mapped[int] = mapped_column(Integer)
    effect_times: Mapped[int] = mapped_column(Integer)
    prefab_id: Mapped[int] = mapped_column(Integer)
    disable_category: Mapped[int] = mapped_column(Integer)
    sub_effect_type: Mapped[int] = mapped_column(Integer)
    sub_effect_value: Mapped[int] = mapped_column(Integer)


class CaravanDishReward(Base):
    __tablename__ = 'caravan_dish_reward'

    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class CaravanDishTurnEffect(Base):
    __tablename__ = 'caravan_dish_turn_effect'

    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn_to: Mapped[int] = mapped_column(Integer)
    effect_value: Mapped[int] = mapped_column(Integer)


class CaravanDrama(Base):
    __tablename__ = 'caravan_drama'
    __table_args__ = (
        Index('caravan_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class CaravanEffectSetting(Base):
    __tablename__ = 'caravan_effect_setting'
    __table_args__ = (
        Index('caravan_effect_setting_0_scene_type', 'scene_type'),
        Index('caravan_effect_setting_0_scene_type_1_effect_type', 'scene_type', 'effect_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scene_type: Mapped[int] = mapped_column(Integer)
    effect_type: Mapped[int] = mapped_column(Integer)
    rank: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)


class CaravanEventEffect(Base):
    __tablename__ = 'caravan_event_effect'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    effect_type: Mapped[int] = mapped_column(Integer)
    effect_value: Mapped[int] = mapped_column(Integer)
    effect_turn: Mapped[int] = mapped_column(Integer)
    effect_times: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(Integer)


class CaravanExcludeCountBlock(Base):
    __tablename__ = 'caravan_exclude_count_block'

    exclude_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_type_1: Mapped[int] = mapped_column(Integer)
    block_type_2: Mapped[int] = mapped_column(Integer)
    block_type_3: Mapped[int] = mapped_column(Integer)


class CaravanGachaBlockLineup(Base):
    __tablename__ = 'caravan_gacha_block_lineup'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normal_gacha_odds: Mapped[int] = mapped_column(Integer)
    normal_gacha_cost: Mapped[int] = mapped_column(Integer)
    rare_gacha_odds: Mapped[int] = mapped_column(Integer)
    rare_gacha_cost: Mapped[int] = mapped_column(Integer)
    premium_gacha_odds: Mapped[int] = mapped_column(Integer)
    premium_gacha_cost: Mapped[int] = mapped_column(Integer)


class CaravanGoalBonus(Base):
    __tablename__ = 'caravan_goal_bonus'
    __table_args__ = (
        Index('caravan_goal_bonus_0_season_id', 'season_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer)
    early_level: Mapped[int] = mapped_column(Integer)
    bonus_label: Mapped[int] = mapped_column(Integer)
    early_from: Mapped[int] = mapped_column(Integer)
    early_to: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class CaravanMap(Base):
    __tablename__ = 'caravan_map'
    __table_args__ = (
        Index('caravan_map_0_season_id', 'season_id'),
    )

    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer)
    next_1: Mapped[int] = mapped_column(Integer)
    next_2: Mapped[int] = mapped_column(Integer)
    next_3: Mapped[int] = mapped_column(Integer)
    next_4: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    reference_id: Mapped[int] = mapped_column(Integer)


class CaravanMapLayout(Base):
    __tablename__ = 'caravan_map_layout'

    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)


class CaravanMapObject(Base):
    __tablename__ = 'caravan_map_object'
    __table_args__ = (
        Index('caravan_map_object_0_season_id', 'season_id'),
    )

    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer)
    object_type: Mapped[int] = mapped_column(Integer)
    position_x: Mapped[float] = mapped_column(Float)
    position_y: Mapped[float] = mapped_column(Float)


class CaravanMileBlockReward(Base):
    __tablename__ = 'caravan_mile_block_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    upgrade_id: Mapped[int] = mapped_column(Integer)


class CaravanNaviComment(Base):
    __tablename__ = 'caravan_navi_comment'
    __table_args__ = (
        Index('caravan_navi_comment_0_season_id', 'season_id'),
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    season_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)


class CaravanSchedule(Base):
    __tablename__ = 'caravan_schedule'
    __table_args__ = (
        Index('caravan_schedule_0_coin_id', 'coin_id'),
    )

    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_block_id: Mapped[int] = mapped_column(Integer)
    target_turn: Mapped[int] = mapped_column(Integer)
    coin_id: Mapped[int] = mapped_column(Integer)
    bg_id: Mapped[int] = mapped_column(Integer)
    bgm_sheet_id: Mapped[str] = mapped_column(Text)
    bgm_que_id: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    shop_close_time: Mapped[str] = mapped_column(Text)


class CaravanShopBlockRank(Base):
    __tablename__ = 'caravan_shop_block_rank'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    upgrade_id: Mapped[int] = mapped_column(Integer)


class CaravanSoundSetting(Base):
    __tablename__ = 'caravan_sound_setting'
    __table_args__ = (
        Index('caravan_sound_setting_0_scene_type', 'scene_type'),
        Index('caravan_sound_setting_0_scene_type_1_effect_type', 'scene_type', 'effect_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scene_type: Mapped[int] = mapped_column(Integer)
    effect_type: Mapped[int] = mapped_column(Integer)
    sound_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)


class CaravanTreasure(Base):
    __tablename__ = 'caravan_treasure'
    __table_args__ = (
        Index('caravan_treasure_0_rarity_1_appraise_flag', 'rarity', 'appraise_flag'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    new_line_name: Mapped[str] = mapped_column(Text)
    rarity: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    reset_value: Mapped[int] = mapped_column(Integer)
    appraise_flag: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class CaravanTreasureBlockRank(Base):
    __tablename__ = 'caravan_treasure_block_rank'

    odds_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    upgrade_id: Mapped[int] = mapped_column(Integer)


class CaravanTreasureBlockReal(Base):
    __tablename__ = 'caravan_treasure_block_real'
    __table_args__ = (
        Index('caravan_treasure_block_real_0_odds_id', 'odds_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class CccChara(Base):
    __tablename__ = 'ccc_chara'

    ccc_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[float] = mapped_column(Float)
    end_time: Mapped[float] = mapped_column(Float)


class CccObject(Base):
    __tablename__ = 'ccc_object'

    ccc_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_report: Mapped[int] = mapped_column(Integer)
    ccc_object_type: Mapped[int] = mapped_column(Integer)
    fall_speed: Mapped[int] = mapped_column(Integer)
    absorb_frame: Mapped[int] = mapped_column(Integer)
    value_1: Mapped[int] = mapped_column(Integer)


class CccScenario(Base):
    __tablename__ = 'ccc_scenario'
    __table_args__ = (
        Index('ccc_scenario_0_ccc_scenario_id', 'ccc_scenario_id'),
    )

    idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    ccc_scenario_id: Mapped[int] = mapped_column(Integer)
    ccc_object_id: Mapped[int] = mapped_column(Integer)
    position: Mapped[int] = mapped_column(Integer)
    frame: Mapped[int] = mapped_column(Integer)


class CggCompletionDatum(Base):
    __tablename__ = 'cgg_completion_data'

    completion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_emblem_id: Mapped[int] = mapped_column(Integer)
    gacha_type: Mapped[int] = mapped_column(Integer)
    completion_num: Mapped[int] = mapped_column(Integer)
    secret_goods_id_1: Mapped[int] = mapped_column(Integer)
    secret_goods_id_2: Mapped[int] = mapped_column(Integer)
    secret_goods_id_3: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    receive_description: Mapped[str] = mapped_column(Text)


class CggCompletionRewardDatum(Base):
    __tablename__ = 'cgg_completion_reward_data'
    __table_args__ = (
        Index('cgg_completion_reward_data_0_completion_id', 'completion_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class CggDrama(Base):
    __tablename__ = 'cgg_drama'
    __table_args__ = (
        Index('cgg_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class CggGachaInfo(Base):
    __tablename__ = 'cgg_gacha_info'
    __table_args__ = (
        Index('cgg_gacha_info_0_cgg_id', 'cgg_id'),
    )

    gacha_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgg_id: Mapped[int] = mapped_column(Integer)
    gacha_name: Mapped[str] = mapped_column(Text)
    gacha_description: Mapped[str] = mapped_column(Text)
    cost_currency_num: Mapped[int] = mapped_column(Integer)
    gacha_intro: Mapped[str] = mapped_column(Text)


class CggGachaLineup(Base):
    __tablename__ = 'cgg_gacha_lineup'
    __table_args__ = (
        Index('cgg_gacha_lineup_0_gacha_type', 'gacha_type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_type: Mapped[int] = mapped_column(Integer)
    lineup_id: Mapped[int] = mapped_column(Integer)
    goods_id: Mapped[int] = mapped_column(Integer)
    goods_num: Mapped[int] = mapped_column(Integer)


class CggGameSettings(Base):
    __tablename__ = 'cgg_game_settings'

    cgg_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goods_shelf_id: Mapped[int] = mapped_column(Integer)
    first_goods_shelf_reward_num: Mapped[int] = mapped_column(Integer)
    cgg_gacha_currency_id: Mapped[int] = mapped_column(Integer)
    first_currency_reward_num: Mapped[int] = mapped_column(Integer)
    exchange_luppi_rate: Mapped[int] = mapped_column(Integer)
    max_gacha_exchange_count: Mapped[int] = mapped_column(Integer)
    max_goods_count: Mapped[int] = mapped_column(Integer)


class CggGoodsDatum(Base):
    __tablename__ = 'cgg_goods_data'

    goods_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    rarity: Mapped[int] = mapped_column(Integer)
    shelf_position_id: Mapped[int] = mapped_column(Integer)
    detail_scale_x: Mapped[float] = mapped_column(Float)
    detail_scale_y: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)


class CharaETicketDatum(Base):
    __tablename__ = 'chara_e_ticket_data'
    __table_args__ = (
        Index('chara_e_ticket_data_0_jewel_store_id', 'jewel_store_id', unique=True),
    )

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    jewel_store_id: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)


class CharaFortuneRail(Base):
    __tablename__ = 'chara_fortune_rail'

    rail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gimmick_1_id: Mapped[str] = mapped_column(Text)
    gimmick_1_x: Mapped[int] = mapped_column(Integer)
    gimmick_2_id: Mapped[str] = mapped_column(Text)
    gimmick_2_x: Mapped[int] = mapped_column(Integer)
    gimmick_3_id: Mapped[str] = mapped_column(Text)
    gimmick_3_x: Mapped[int] = mapped_column(Integer)
    gimmick_4_id: Mapped[str] = mapped_column(Text)
    gimmick_4_x: Mapped[int] = mapped_column(Integer)
    gimmick_5_id: Mapped[str] = mapped_column(Text)
    gimmick_5_x: Mapped[int] = mapped_column(Integer)
    gimmick_6_id: Mapped[str] = mapped_column(Text)
    gimmick_6_x: Mapped[int] = mapped_column(Integer)
    gimmick_7_id: Mapped[str] = mapped_column(Text)
    gimmick_7_x: Mapped[int] = mapped_column(Integer)
    gimmick_8_id: Mapped[str] = mapped_column(Text)
    gimmick_8_x: Mapped[int] = mapped_column(Integer)
    gimmick_9_id: Mapped[str] = mapped_column(Text)
    gimmick_9_x: Mapped[int] = mapped_column(Integer)
    gimmick_10_id: Mapped[str] = mapped_column(Text)
    gimmick_10_x: Mapped[int] = mapped_column(Integer)


class CharaFortuneReward(Base):
    __tablename__ = 'chara_fortune_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fortune_id: Mapped[int] = mapped_column(Integer)
    rank: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    count_5: Mapped[int] = mapped_column(Integer)


class CharaFortuneScenario(Base):
    __tablename__ = 'chara_fortune_scenario'

    scenario_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rail_1: Mapped[int] = mapped_column(Integer)
    rail_2: Mapped[int] = mapped_column(Integer)
    rail_3: Mapped[int] = mapped_column(Integer)
    rail_4: Mapped[int] = mapped_column(Integer)


class CharaFortuneSchedule(Base):
    __tablename__ = 'chara_fortune_schedule'

    fortune_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class CharaIdentity(Base):
    __tablename__ = 'chara_identity'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_type: Mapped[int] = mapped_column(Integer)
    chara_type_2: Mapped[int] = mapped_column(Integer)
    chara_type_3: Mapped[int] = mapped_column(Integer)


class CharaStoryStatus(Base):
    __tablename__ = 'chara_story_status'

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_story_name: Mapped[str] = mapped_column(Text)
    status_type_1: Mapped[int] = mapped_column(Integer)
    status_rate_1: Mapped[int] = mapped_column(Integer)
    status_type_2: Mapped[int] = mapped_column(Integer)
    status_rate_2: Mapped[int] = mapped_column(Integer)
    status_type_3: Mapped[int] = mapped_column(Integer)
    status_rate_3: Mapped[int] = mapped_column(Integer)
    status_type_4: Mapped[int] = mapped_column(Integer)
    status_rate_4: Mapped[int] = mapped_column(Integer)
    status_type_5: Mapped[int] = mapped_column(Integer)
    status_rate_5: Mapped[int] = mapped_column(Integer)
    chara_id_1: Mapped[int] = mapped_column(Integer)
    chara_id_2: Mapped[int] = mapped_column(Integer)
    chara_id_3: Mapped[int] = mapped_column(Integer)
    chara_id_4: Mapped[int] = mapped_column(Integer)
    chara_id_5: Mapped[int] = mapped_column(Integer)
    chara_id_6: Mapped[int] = mapped_column(Integer)
    chara_id_7: Mapped[int] = mapped_column(Integer)
    chara_id_8: Mapped[int] = mapped_column(Integer)
    chara_id_9: Mapped[int] = mapped_column(Integer)
    chara_id_10: Mapped[int] = mapped_column(Integer)
    chara_id_11: Mapped[int] = mapped_column(Integer)
    chara_id_12: Mapped[int] = mapped_column(Integer)
    chara_id_13: Mapped[int] = mapped_column(Integer)
    chara_id_14: Mapped[int] = mapped_column(Integer)
    chara_id_15: Mapped[int] = mapped_column(Integer)
    chara_id_16: Mapped[int] = mapped_column(Integer)
    chara_id_17: Mapped[int] = mapped_column(Integer)
    chara_id_18: Mapped[int] = mapped_column(Integer)
    chara_id_19: Mapped[int] = mapped_column(Integer)
    chara_id_20: Mapped[int] = mapped_column(Integer)


class CharacterLoveRankupText(Base):
    __tablename__ = 'character_love_rankup_text'

    chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    love_level: Mapped[int] = mapped_column(Integer)
    scale: Mapped[float] = mapped_column(Float)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    voice_id_1: Mapped[int] = mapped_column(Integer)
    face_1: Mapped[int] = mapped_column(Integer)
    serif_1: Mapped[str] = mapped_column(Text)
    voice_id_2: Mapped[int] = mapped_column(Integer)
    face_2: Mapped[int] = mapped_column(Integer)
    serif_2: Mapped[str] = mapped_column(Text)
    voice_id_3: Mapped[int] = mapped_column(Integer)
    face_3: Mapped[int] = mapped_column(Integer)
    serif_3: Mapped[str] = mapped_column(Text)


class ClanBattle2BossDatum(Base):
    __tablename__ = 'clan_battle_2_boss_data'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    order_num: Mapped[int] = mapped_column(Integer)
    boss_thumb_id: Mapped[int] = mapped_column(Integer)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    scale_ratio: Mapped[float] = mapped_column(Float)
    tap_width_ratio: Mapped[float] = mapped_column(Float)
    tap_height_ratio: Mapped[float] = mapped_column(Float)
    map_position_x: Mapped[int] = mapped_column(Integer)
    map_position_y: Mapped[int] = mapped_column(Integer)
    cursor_position: Mapped[int] = mapped_column(Integer)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    quest_detail_monster_size: Mapped[float] = mapped_column(Float)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer)
    battle_report_monster_size: Mapped[float] = mapped_column(Float)
    battle_report_monster_height: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    wave_bgm: Mapped[str] = mapped_column(Text)


class ClanBattle2MapDatum(Base):
    __tablename__ = 'clan_battle_2_map_data'
    __table_args__ = (
        Index('clan_battle_2_map_data_0_clan_battle_id', 'clan_battle_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    map_bg: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    lap_num_from: Mapped[int] = mapped_column(Integer)
    lap_num_to: Mapped[int] = mapped_column(Integer)
    boss_id_1: Mapped[int] = mapped_column(Integer)
    boss_id_2: Mapped[int] = mapped_column(Integer)
    boss_id_3: Mapped[int] = mapped_column(Integer)
    boss_id_4: Mapped[int] = mapped_column(Integer)
    boss_id_5: Mapped[int] = mapped_column(Integer)
    aura_effect: Mapped[int] = mapped_column(Integer)
    rsl_unlock_lap: Mapped[int] = mapped_column(Integer)
    phase: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_4: Mapped[int] = mapped_column(Integer)
    wave_group_id_5: Mapped[int] = mapped_column(Integer)
    fix_reward_id_1: Mapped[int] = mapped_column(Integer)
    fix_reward_id_2: Mapped[int] = mapped_column(Integer)
    fix_reward_id_3: Mapped[int] = mapped_column(Integer)
    fix_reward_id_4: Mapped[int] = mapped_column(Integer)
    fix_reward_id_5: Mapped[int] = mapped_column(Integer)
    damage_rank_id_1: Mapped[int] = mapped_column(Integer)
    damage_rank_id_2: Mapped[int] = mapped_column(Integer)
    damage_rank_id_3: Mapped[int] = mapped_column(Integer)
    damage_rank_id_4: Mapped[int] = mapped_column(Integer)
    damage_rank_id_5: Mapped[int] = mapped_column(Integer)
    reward_gold_coefficient: Mapped[float] = mapped_column(Float)
    limited_mana: Mapped[int] = mapped_column(Integer)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer)
    score_coefficient_1: Mapped[float] = mapped_column(Float)
    score_coefficient_2: Mapped[float] = mapped_column(Float)
    score_coefficient_3: Mapped[float] = mapped_column(Float)
    score_coefficient_4: Mapped[float] = mapped_column(Float)
    score_coefficient_5: Mapped[float] = mapped_column(Float)
    param_adjust_id: Mapped[int] = mapped_column(Integer)
    param_adjust_interval: Mapped[int] = mapped_column(Integer)


class ClanBattleArchiveClanRank(Base):
    __tablename__ = 'clan_battle_archive_clan_rank'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)


class ClanBattleArchivePersonRank(Base):
    __tablename__ = 'clan_battle_archive_person_rank'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)


class ClanBattleBattleMissionDatum(Base):
    __tablename__ = 'clan_battle_battle_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class ClanBattleBossDamageRank(Base):
    __tablename__ = 'clan_battle_boss_damage_rank'
    __table_args__ = (
        Index('clan_battle_boss_damage_rank_0_damage_rank_id', 'damage_rank_id'),
    )

    id: Mapped[int] = mapped_column(Integer)
    damage_rank_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ranking_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    ranking_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_group_id: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ClanBattleBossFixReward(Base):
    __tablename__ = 'clan_battle_boss_fix_reward'

    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ClanBattleLastAttackReward(Base):
    __tablename__ = 'clan_battle_last_attack_reward'

    last_attack_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ClanBattleOddsDatum(Base):
    __tablename__ = 'clan_battle_odds_data'
    __table_args__ = (
        Index('clan_battle_odds_data_0_odds_group_id', 'odds_group_id'),
    )

    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_csv_1: Mapped[str] = mapped_column(Text)
    odds_csv_2: Mapped[str] = mapped_column(Text)
    odds_csv_3: Mapped[str] = mapped_column(Text)
    odds_csv_4: Mapped[str] = mapped_column(Text)
    odds_csv_5: Mapped[str] = mapped_column(Text)
    odds_csv_6: Mapped[str] = mapped_column(Text)
    odds_csv_7: Mapped[str] = mapped_column(Text)
    odds_csv_8: Mapped[str] = mapped_column(Text)
    odds_csv_9: Mapped[str] = mapped_column(Text)
    odds_csv_10: Mapped[str] = mapped_column(Text)


class ClanBattleParamAdjust(Base):
    __tablename__ = 'clan_battle_param_adjust'

    param_adjust_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)
    normal_atk_cast_time: Mapped[int] = mapped_column(Integer)
    score_coefficient: Mapped[int] = mapped_column(Integer)


class ClanBattlePeriod(Base):
    __tablename__ = 'clan_battle_period'
    __table_args__ = (
        Index('clan_battle_period_0_clan_battle_id', 'clan_battle_id'),
    )

    clan_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_detail: Mapped[str] = mapped_column(Text)
    period_detail_bg: Mapped[int] = mapped_column(Integer)
    period_detail_s: Mapped[str] = mapped_column(Text)
    period_detail_bg_s: Mapped[int] = mapped_column(Integer)
    period_detail_bg_position: Mapped[int] = mapped_column(Integer)
    period_detail_boss_position_x: Mapped[int] = mapped_column(Integer)
    period_detail_boss_position_y: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    interval_start: Mapped[str] = mapped_column(Text)
    interval_end: Mapped[str] = mapped_column(Text)
    calc_start: Mapped[str] = mapped_column(Text)
    result_start: Mapped[str] = mapped_column(Text)
    result_end: Mapped[str] = mapped_column(Text)
    limit_time: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    quest_detail_rehearsal_label_height: Mapped[int] = mapped_column(Integer)
    min_carry_over_time: Mapped[int] = mapped_column(Integer)


class ClanBattlePeriodLapReward(Base):
    __tablename__ = 'clan_battle_period_lap_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    period: Mapped[int] = mapped_column(Integer)
    lap_num_from: Mapped[int] = mapped_column(Integer)
    lap_num_to: Mapped[int] = mapped_column(Integer)
    ranking_bonus_group: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ClanBattlePeriodRankReward(Base):
    __tablename__ = 'clan_battle_period_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    period: Mapped[int] = mapped_column(Integer)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    ranking_bonus_group: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ClanBattleRecommendDatum(Base):
    __tablename__ = 'clan_battle_recommend_data'
    __table_args__ = (
        Index('clan_battle_recommend_data_0_recommend_group', 'recommend_group'),
    )

    level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommend_group: Mapped[int] = mapped_column(Integer)
    level_from: Mapped[int] = mapped_column(Integer)
    level_to: Mapped[int] = mapped_column(Integer)
    atack_party_count: Mapped[int] = mapped_column(Integer)
    magic_party_count: Mapped[int] = mapped_column(Integer)


class ClanBattleSBossDatum(Base):
    __tablename__ = 'clan_battle_s_boss_data'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    order_num: Mapped[int] = mapped_column(Integer)
    boss_thumb_id: Mapped[int] = mapped_column(Integer)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    scale_ratio: Mapped[float] = mapped_column(Float)
    tap_width_ratio: Mapped[float] = mapped_column(Float)
    tap_height_ratio: Mapped[float] = mapped_column(Float)
    map_position_x: Mapped[int] = mapped_column(Integer)
    map_position_y: Mapped[int] = mapped_column(Integer)
    cursor_position: Mapped[int] = mapped_column(Integer)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    quest_detail_monster_size: Mapped[float] = mapped_column(Float)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer)
    battle_report_monster_size: Mapped[float] = mapped_column(Float)
    battle_report_monster_height: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    wave_bgm: Mapped[str] = mapped_column(Text)


class ClanBattleSBossFixReward(Base):
    __tablename__ = 'clan_battle_s_boss_fix_reward'

    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class ClanBattleSMapDatum(Base):
    __tablename__ = 'clan_battle_s_map_data'
    __table_args__ = (
        Index('clan_battle_s_map_data_0_clan_battle_id', 'clan_battle_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    map_bg: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    lap_num_from: Mapped[int] = mapped_column(Integer)
    lap_num_to: Mapped[int] = mapped_column(Integer)
    boss_id_1: Mapped[int] = mapped_column(Integer)
    boss_id_2: Mapped[int] = mapped_column(Integer)
    boss_id_3: Mapped[int] = mapped_column(Integer)
    boss_id_4: Mapped[int] = mapped_column(Integer)
    boss_id_5: Mapped[int] = mapped_column(Integer)
    extra_battle_flag1: Mapped[int] = mapped_column(Integer)
    extra_battle_flag2: Mapped[int] = mapped_column(Integer)
    extra_battle_flag3: Mapped[int] = mapped_column(Integer)
    extra_battle_flag4: Mapped[int] = mapped_column(Integer)
    extra_battle_flag5: Mapped[int] = mapped_column(Integer)
    aura_effect: Mapped[int] = mapped_column(Integer)
    rsl_unlock_lap: Mapped[int] = mapped_column(Integer)
    phase: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_4: Mapped[int] = mapped_column(Integer)
    wave_group_id_5: Mapped[int] = mapped_column(Integer)
    fix_reward_id_1: Mapped[int] = mapped_column(Integer)
    fix_reward_id_2: Mapped[int] = mapped_column(Integer)
    fix_reward_id_3: Mapped[int] = mapped_column(Integer)
    fix_reward_id_4: Mapped[int] = mapped_column(Integer)
    fix_reward_id_5: Mapped[int] = mapped_column(Integer)
    damage_rank_id_1: Mapped[int] = mapped_column(Integer)
    damage_rank_id_2: Mapped[int] = mapped_column(Integer)
    damage_rank_id_3: Mapped[int] = mapped_column(Integer)
    damage_rank_id_4: Mapped[int] = mapped_column(Integer)
    damage_rank_id_5: Mapped[int] = mapped_column(Integer)
    reward_gold_coefficient: Mapped[float] = mapped_column(Float)
    limited_mana: Mapped[int] = mapped_column(Integer)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer)
    score_coefficient_1: Mapped[float] = mapped_column(Float)
    score_coefficient_2: Mapped[float] = mapped_column(Float)
    score_coefficient_3: Mapped[float] = mapped_column(Float)
    score_coefficient_4: Mapped[float] = mapped_column(Float)
    score_coefficient_5: Mapped[float] = mapped_column(Float)
    param_adjust_id: Mapped[int] = mapped_column(Integer)
    param_adjust_interval: Mapped[int] = mapped_column(Integer)


class ClanBattleSParamAdjust(Base):
    __tablename__ = 'clan_battle_s_param_adjust'

    param_adjust_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)
    normal_atk_cast_time: Mapped[int] = mapped_column(Integer)
    score_coefficient: Mapped[int] = mapped_column(Integer)


class ClanBattleSchedule(Base):
    __tablename__ = 'clan_battle_schedule'

    clan_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_month: Mapped[int] = mapped_column(Integer)
    last_clan_battle_id: Mapped[int] = mapped_column(Integer)
    point_per_stamina: Mapped[int] = mapped_column(Integer)
    cost_group_id: Mapped[int] = mapped_column(Integer)
    cost_group_id_s: Mapped[int] = mapped_column(Integer)
    map_bgm: Mapped[str] = mapped_column(Text)
    resource_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    mode_change_start_time: Mapped[str] = mapped_column(Text)
    mode_change_end_time: Mapped[str] = mapped_column(Text)
    mode_change_remind_time: Mapped[str] = mapped_column(Text)


class ClanBattleTrainingDatum(Base):
    __tablename__ = 'clan_battle_training_data'
    __table_args__ = (
        Index('clan_battle_training_data_0_training_id', 'training_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    training_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[int] = mapped_column(Integer)
    phase: Mapped[int] = mapped_column(Integer)
    map_data_id: Mapped[int] = mapped_column(Integer)


class ClanBattleTrainingSchedule(Base):
    __tablename__ = 'clan_battle_training_schedule'
    __table_args__ = (
        Index('clan_battle_training_schedule_0_clan_battle_id', 'clan_battle_id'),
    )

    training_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clan_battle_id: Mapped[int] = mapped_column(Integer)
    battle_start_time: Mapped[str] = mapped_column(Text)
    battle_end_time: Mapped[str] = mapped_column(Text)
    interval_start_time: Mapped[str] = mapped_column(Text)
    interval_end_time: Mapped[str] = mapped_column(Text)


class ClanCostGroup(Base):
    __tablename__ = 'clan_cost_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost_group_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    cost: Mapped[int] = mapped_column(Integer)


class ClanGrade(Base):
    __tablename__ = 'clan_grade'

    clan_grade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)


class ClanInviteLevelGroup(Base):
    __tablename__ = 'clan_invite_level_group'

    level_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_from: Mapped[int] = mapped_column(Integer)
    team_level_to: Mapped[int] = mapped_column(Integer)


class ClanprofileContent(Base):
    __tablename__ = 'clanprofile_content'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    disp_order: Mapped[int] = mapped_column(Integer)


class ColosseumEnhanceDatum(Base):
    __tablename__ = 'colosseum_enhance_data'
    __table_args__ = (
        Index('colosseum_enhance_data_0_enhance_id', 'enhance_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_id: Mapped[int] = mapped_column(Integer)
    min_level: Mapped[int] = mapped_column(Integer)
    max_level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    equipment_slot_1: Mapped[int] = mapped_column(Integer)
    equipment_slot_2: Mapped[int] = mapped_column(Integer)
    equipment_slot_3: Mapped[int] = mapped_column(Integer)
    equipment_slot_4: Mapped[int] = mapped_column(Integer)
    equipment_slot_5: Mapped[int] = mapped_column(Integer)
    equipment_slot_6: Mapped[int] = mapped_column(Integer)
    unique_equipment_level_1: Mapped[int] = mapped_column(Integer)
    unique_equipment_level_2: Mapped[int] = mapped_column(Integer)


class ColosseumMissionDatum(Base):
    __tablename__ = 'colosseum_mission_data'
    __table_args__ = (
        Index('colosseum_mission_data_0_schedule_id_1_difficulty', 'schedule_id', 'difficulty'),
    )

    schedule_id: Mapped[int] = mapped_column(Integer)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer)
    disp_group: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)


class ColosseumMissionRewardDatum(Base):
    __tablename__ = 'colosseum_mission_reward_data'
    __table_args__ = (
        Index('colosseum_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class ColosseumQuestDatum(Base):
    __tablename__ = 'colosseum_quest_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    slot_id: Mapped[int] = mapped_column(Integer)
    display_unit_id: Mapped[int] = mapped_column(Integer)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    unit_id_3: Mapped[int] = mapped_column(Integer)
    unit_id_4: Mapped[int] = mapped_column(Integer)
    unit_id_5: Mapped[int] = mapped_column(Integer)
    enhance_id_1: Mapped[int] = mapped_column(Integer)
    enhance_id_2: Mapped[int] = mapped_column(Integer)
    enhance_id_3: Mapped[int] = mapped_column(Integer)
    enhance_id_4: Mapped[int] = mapped_column(Integer)
    enhance_id_5: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)


class ColosseumScheduleDatum(Base):
    __tablename__ = 'colosseum_schedule_data'

    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)
    calc_start: Mapped[str] = mapped_column(Text)
    result_start: Mapped[str] = mapped_column(Text)


class ColosseumScore(Base):
    __tablename__ = 'colosseum_score'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    win_pt: Mapped[int] = mapped_column(Integer)
    time_pt_rate: Mapped[int] = mapped_column(Integer)
    bonus_pos_1: Mapped[int] = mapped_column(Integer)
    bonus_param_1: Mapped[int] = mapped_column(Integer)
    bonus_pos_2: Mapped[int] = mapped_column(Integer)
    bonus_param_2: Mapped[int] = mapped_column(Integer)
    threshold_pt_1: Mapped[int] = mapped_column(Integer)
    threshold_pt_2: Mapped[int] = mapped_column(Integer)


class CombinedResultMotion(Base):
    __tablename__ = 'combined_result_motion'

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    disp_order_1: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    disp_order_2: Mapped[int] = mapped_column(Integer)
    unit_id_3: Mapped[int] = mapped_column(Integer)
    disp_order_3: Mapped[int] = mapped_column(Integer)
    unit_id_4: Mapped[int] = mapped_column(Integer)
    disp_order_4: Mapped[int] = mapped_column(Integer)
    unit_id_5: Mapped[int] = mapped_column(Integer)
    disp_order_5: Mapped[int] = mapped_column(Integer)


class ContentMapDatum(Base):
    __tablename__ = 'content_map_data'

    content_map_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    area_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    quest_position_x: Mapped[int] = mapped_column(Integer)
    quest_position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    system_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class ContentReleaseDatum(Base):
    __tablename__ = 'content_release_data'

    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer)
    quest_id: Mapped[int] = mapped_column(Integer)
    dialog: Mapped[str] = mapped_column(Text)


class CooperationQuestDatum(Base):
    __tablename__ = 'cooperation_quest_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text)
    difficulty_level: Mapped[int] = mapped_column(Integer)
    limit_team_level: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    exp: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer)
    odds_group_id: Mapped[int] = mapped_column(Integer)
    lobby_background: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    enemy_image_1: Mapped[int] = mapped_column(Integer)
    enemy_image_2: Mapped[int] = mapped_column(Integer)
    enemy_image_3: Mapped[int] = mapped_column(Integer)
    enemy_image_4: Mapped[int] = mapped_column(Integer)
    enemy_image_5: Mapped[int] = mapped_column(Integer)
    first_reward_image_1: Mapped[int] = mapped_column(Integer)
    first_reward_image_2: Mapped[int] = mapped_column(Integer)
    first_reward_image_3: Mapped[int] = mapped_column(Integer)
    first_reward_image_4: Mapped[int] = mapped_column(Integer)
    first_reward_image_5: Mapped[int] = mapped_column(Integer)
    repeat_reward_image_1: Mapped[int] = mapped_column(Integer)
    repeat_reward_image_2: Mapped[int] = mapped_column(Integer)
    repeat_reward_image_3: Mapped[int] = mapped_column(Integer)
    cooperation_quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    cooperation_quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    main_enemy_image_wave_1: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_1_1: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_1_2: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_1_3: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_1_4: Mapped[int] = mapped_column(Integer)
    main_enemy_image_wave_2: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_2_1: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_2_2: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_2_3: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_2_4: Mapped[int] = mapped_column(Integer)
    main_enemy_image_wave_3: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_3_1: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_3_2: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_3_3: Mapped[int] = mapped_column(Integer)
    sub_enemy_image_wave_3_4: Mapped[int] = mapped_column(Integer)
    quest_comment: Mapped[str] = mapped_column(Text)
    unlock_quest_id_1: Mapped[int] = mapped_column(Integer)
    unlock_quest_id_2: Mapped[int] = mapped_column(Integer)


class CustomMypage(Base):
    __tablename__ = 'custom_mypage'
    __table_args__ = (
        Index('custom_mypage_0_still_group_id', 'still_group_id'),
    )

    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)
    still_group_id: Mapped[int] = mapped_column(Integer)
    still_name: Mapped[str] = mapped_column(Text)
    vertical_still_flg: Mapped[int] = mapped_column(Integer)
    scroll_direction: Mapped[int] = mapped_column(Integer)
    mypage_type: Mapped[int] = mapped_column(Integer)


class CustomMypageGroup(Base):
    __tablename__ = 'custom_mypage_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(Text)


class DailyMissionDatum(Base):
    __tablename__ = 'daily_mission_data'

    daily_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    min_level: Mapped[int] = mapped_column(Integer)
    max_level: Mapped[int] = mapped_column(Integer)
    title_color_id: Mapped[int] = mapped_column(Integer)
    visible_flag: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class DearChara(Base):
    __tablename__ = 'dear_chara'
    __table_args__ = (
        Index('dear_chara_0_event_id', 'event_id'),
    )

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_name: Mapped[str] = mapped_column(Text)
    max_dear_point: Mapped[int] = mapped_column(Integer)
    reference_type: Mapped[int] = mapped_column(Integer)
    reference_id: Mapped[int] = mapped_column(Integer)
    episode_unlock_offset_x: Mapped[int] = mapped_column(Integer)
    episode_unlock_offset_y: Mapped[int] = mapped_column(Integer)
    dear_point_up_offset_x: Mapped[int] = mapped_column(Integer)
    dear_point_up_offset_y: Mapped[int] = mapped_column(Integer)
    condition_story_id: Mapped[int] = mapped_column(Integer)


class DearReward(Base):
    __tablename__ = 'dear_reward'
    __table_args__ = (
        Index('dear_reward_0_event_id_1_chara_index', 'event_id', 'chara_index'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    chara_index: Mapped[int] = mapped_column(Integer)
    dear_point: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class DearSetting(Base):
    __tablename__ = 'dear_setting'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_name: Mapped[str] = mapped_column(Text)
    tutorial_quest_id: Mapped[int] = mapped_column(Integer)
    tutorial_chara_index: Mapped[int] = mapped_column(Integer)
    tutorial_story_id: Mapped[int] = mapped_column(Integer)


class DearStoryDatum(Base):
    __tablename__ = 'dear_story_data'
    __table_args__ = (
        Index('dear_story_data_0_value', 'value'),
    )

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    thumbnail_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class DearStoryDetail(Base):
    __tablename__ = 'dear_story_detail'
    __table_args__ = (
        Index('dear_story_detail_0_story_group_id', 'story_group_id'),
        Index('dear_story_detail_0_story_group_id_1_chara_index', 'story_group_id', 'chara_index')
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    visible_type: Mapped[int] = mapped_column(Integer)
    story_end: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)
    love_level: Mapped[int] = mapped_column(Integer)
    requirement_id: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    story_quest_id: Mapped[int] = mapped_column(Integer)
    chara_index: Mapped[int] = mapped_column(Integer)
    condition_event_quest_id: Mapped[int] = mapped_column(Integer)
    condition_event_boss_id: Mapped[int] = mapped_column(Integer)
    lock_all_text: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_value_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_value_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_value_3: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class DefineSpskill(Base):
    __tablename__ = 'define_spskill'
    __table_args__ = (
        Index('define_spskill_0_sp_skill_id', 'sp_skill_id'),
    )

    link_skill_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    sp_skill_id: Mapped[int] = mapped_column(Integer)
    base_skill_id: Mapped[int] = mapped_column(Integer)
    skill_category: Mapped[int] = mapped_column(Integer)


class DodgeTpRecovery(Base):
    __tablename__ = 'dodge_tp_recovery'

    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recovery_ratio: Mapped[float] = mapped_column(Float)


class DsbDramaScript(Base):
    __tablename__ = 'dsb_drama_script'
    __table_args__ = (
        Index('dsb_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class DsbStoryDatum(Base):
    __tablename__ = 'dsb_story_data'
    __table_args__ = (
        Index('dsb_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_time: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    owner_unit_id: Mapped[int] = mapped_column(Integer)
    guest_unit_id: Mapped[int] = mapped_column(Integer)
    day_num: Mapped[int] = mapped_column(Integer)
    material_text: Mapped[str] = mapped_column(Text)
    effect_text: Mapped[str] = mapped_column(Text)
    article_text: Mapped[str] = mapped_column(Text)


class DungeonArea(Base):
    __tablename__ = 'dungeon_area'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_type: Mapped[int] = mapped_column(Integer)
    dungeon_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    open_area_id: Mapped[int] = mapped_column(Integer)
    open_quest_id: Mapped[int] = mapped_column(Integer)
    content_release_story: Mapped[int] = mapped_column(Integer)
    initial_clear_story: Mapped[int] = mapped_column(Integer)
    reward_group_id: Mapped[int] = mapped_column(Integer)
    recommend_level: Mapped[int] = mapped_column(Integer)
    quest_position_x: Mapped[int] = mapped_column(Integer)
    quest_position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer)


class DungeonAreaDatum(Base):
    __tablename__ = 'dungeon_area_data'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_type: Mapped[int] = mapped_column(Integer)
    dungeon_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    open_quest_id: Mapped[int] = mapped_column(Integer)
    content_release_story: Mapped[int] = mapped_column(Integer)
    initial_clear_story: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    reward_group_id: Mapped[int] = mapped_column(Integer)
    recommend_level: Mapped[int] = mapped_column(Integer)
    quest_position_x: Mapped[int] = mapped_column(Integer)
    quest_position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    coin_item_id: Mapped[int] = mapped_column(Integer)
    enemy_image_1: Mapped[int] = mapped_column(Integer)
    enemy_image_2: Mapped[int] = mapped_column(Integer)
    enemy_image_3: Mapped[int] = mapped_column(Integer)
    enemy_image_4: Mapped[int] = mapped_column(Integer)
    enemy_image_5: Mapped[int] = mapped_column(Integer)
    view_reward_id_1: Mapped[int] = mapped_column(Integer)
    view_reward_id_2: Mapped[int] = mapped_column(Integer)
    view_reward_id_3: Mapped[int] = mapped_column(Integer)
    view_reward_id_4: Mapped[int] = mapped_column(Integer)
    view_reward_id_5: Mapped[int] = mapped_column(Integer)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class DungeonPatternBattle(Base):
    __tablename__ = 'dungeon_pattern_battle'
    __table_args__ = (
        Index('dungeon_pattern_battle_0_quest_id', 'quest_id'),
        Index('dungeon_pattern_battle_0_quest_id_1_pattern', 'quest_id', 'pattern', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer)
    pattern: Mapped[int] = mapped_column(Integer)
    trigger_type_1: Mapped[int] = mapped_column(Integer)
    trigger_value_1: Mapped[int] = mapped_column(Integer)
    next_pattern_1: Mapped[int] = mapped_column(Integer)
    trigger_type_2: Mapped[int] = mapped_column(Integer)
    trigger_value_2: Mapped[int] = mapped_column(Integer)
    next_pattern_2: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    detail_unit_id: Mapped[int] = mapped_column(Integer)
    detail_monster_position_x_1: Mapped[float] = mapped_column(Float)
    detail_monster_position_y_1: Mapped[float] = mapped_column(Float)
    detail_monster_scale_1: Mapped[float] = mapped_column(Float)
    floor_unit_id: Mapped[int] = mapped_column(Integer)
    floor_monster_position_x_1: Mapped[float] = mapped_column(Float)
    floor_monster_position_y_1: Mapped[float] = mapped_column(Float)
    floor_monster_scale_1: Mapped[float] = mapped_column(Float)


class DungeonQuestDatum(Base):
    __tablename__ = 'dungeon_quest_data'
    __table_args__ = (
        Index('dungeon_quest_data_0_dungeon_area_id', 'dungeon_area_id'),
        Index('dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num', unique=True)
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_area_id: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    quest_type: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    matching_coefficient: Mapped[float] = mapped_column(Float)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer)
    energy_reset_flag: Mapped[int] = mapped_column(Integer)
    emax: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_image_6: Mapped[int] = mapped_column(Integer)
    reward_coin: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    odds_group_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    dungeon_quest_detail_monster_size: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_1: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_2: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_height: Mapped[float] = mapped_column(Float)
    multi_target_effect_time: Mapped[float] = mapped_column(Float)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)


class DungeonSkipDatum(Base):
    __tablename__ = 'dungeon_skip_data'

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_motion_id: Mapped[int] = mapped_column(Integer)
    skip_bg_id: Mapped[int] = mapped_column(Integer)
    skip_position_x: Mapped[int] = mapped_column(Integer)
    skip_position_y: Mapped[int] = mapped_column(Integer)
    skip_scale_x: Mapped[float] = mapped_column(Float)
    skip_scale_y: Mapped[float] = mapped_column(Float)


class DungeonSpecialBattle(Base):
    __tablename__ = 'dungeon_special_battle'
    __table_args__ = (
        Index('dungeon_special_battle_0_quest_id', 'quest_id'),
        Index('dungeon_special_battle_0_quest_id_1_mode', 'quest_id', 'mode', unique=True)
    )

    special_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[int] = mapped_column(Integer)
    purpose_type: Mapped[int] = mapped_column(Integer)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer)
    trigger_hp: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    action_start_second: Mapped[float] = mapped_column(Float)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer)
    start_idle_trigger: Mapped[int] = mapped_column(Integer)
    appear_time: Mapped[float] = mapped_column(Float)
    detail_boss_bg_size: Mapped[float] = mapped_column(Float)
    detail_boss_bg_height: Mapped[float] = mapped_column(Float)
    detail_boss_motion: Mapped[str] = mapped_column(Text)


class DungeonSpecialEnemySetting(Base):
    __tablename__ = 'dungeon_special_enemy_setting'
    __table_args__ = (
        UniqueConstraint('special_battle_id', 'disp_order'),
        Index('dungeon_special_enemy_setting_0_special_battle_id', 'special_battle_id'),
        Index('dungeon_special_enemy_setting_0_special_battle_id_1_enemy_identify', 'special_battle_id', 'enemy_identify', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    special_battle_id: Mapped[int] = mapped_column(Integer)
    enemy_identify: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    must_kill_flag: Mapped[int] = mapped_column(Integer)
    detail_offset_x: Mapped[float] = mapped_column(Float)
    detail_offset_y: Mapped[float] = mapped_column(Float)
    detail_scale: Mapped[float] = mapped_column(Float)


class DvsStoryDatum(Base):
    __tablename__ = 'dvs_story_data'
    __table_args__ = (
        Index('dvs_story_data_0_dvs_story_type', 'dvs_story_type'),
        Index('dvs_story_data_0_original_event_id', 'original_event_id')
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    detail_title: Mapped[str] = mapped_column(Text)
    detail_description: Mapped[str] = mapped_column(Text)
    dvs_story_type: Mapped[int] = mapped_column(Integer)
    is_last: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)


class EReduction(Base):
    __tablename__ = 'e_reduction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    border: Mapped[int] = mapped_column(Integer)
    threshold_1: Mapped[int] = mapped_column(Integer)
    value_1: Mapped[float] = mapped_column(Float)
    threshold_2: Mapped[int] = mapped_column(Integer)
    value_2: Mapped[float] = mapped_column(Float)
    threshold_3: Mapped[int] = mapped_column(Integer)
    value_3: Mapped[float] = mapped_column(Float)
    threshold_4: Mapped[int] = mapped_column(Integer)
    value_4: Mapped[float] = mapped_column(Float)
    threshold_5: Mapped[int] = mapped_column(Integer)
    value_5: Mapped[float] = mapped_column(Float)


class EmblemDatum(Base):
    __tablename__ = 'emblem_data'

    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_oder: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    emblem_name: Mapped[str] = mapped_column(Text)
    description_mission_id: Mapped[int] = mapped_column(Integer)
    event_emblem: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class EmblemMissionDatum(Base):
    __tablename__ = 'emblem_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_value_2: Mapped[int] = mapped_column(Integer)
    condition_value_3: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    system_id: Mapped[int] = mapped_column(Integer)
    visible_flag: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class EmblemMissionRewardDatum(Base):
    __tablename__ = 'emblem_mission_reward_data'
    __table_args__ = (
        Index('emblem_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
        Index('emblem_mission_reward_data_0_reward_id', 'reward_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    icon_type: Mapped[int] = mapped_column(Integer)


class EnemyEnableVoice(Base):
    __tablename__ = 'enemy_enable_voice'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_id: Mapped[int] = mapped_column(Integer)


class EnemyIgnoreSkillRf(Base):
    __tablename__ = 'enemy_ignore_skill_rf'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyMParts(Base):
    __tablename__ = 'enemy_m_parts'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    child_enemy_parameter_1: Mapped[int] = mapped_column(Integer)
    child_enemy_parameter_2: Mapped[int] = mapped_column(Integer)
    child_enemy_parameter_3: Mapped[int] = mapped_column(Integer)
    child_enemy_parameter_4: Mapped[int] = mapped_column(Integer)
    child_enemy_parameter_5: Mapped[int] = mapped_column(Integer)


class EnemyParameter(Base):
    __tablename__ = 'enemy_parameter'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer)
    resist_status_id: Mapped[int] = mapped_column(Integer)
    resist_variation_id: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer)
    break_durability: Mapped[int] = mapped_column(Integer)
    virtual_hp: Mapped[int] = mapped_column(Integer)


class EnemyRewardDatum(Base):
    __tablename__ = 'enemy_reward_data'

    drop_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drop_count: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    odds_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    odds_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    odds_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    odds_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    odds_5: Mapped[int] = mapped_column(Integer)


class EnvironmentSkillDetail(Base):
    __tablename__ = 'environment_skill_detail'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    icon_type: Mapped[int] = mapped_column(Integer)


class EquipmentCraft(Base):
    __tablename__ = 'equipment_craft'

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    crafted_cost: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_1: Mapped[int] = mapped_column(Integer)
    consume_num_1: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_2: Mapped[int] = mapped_column(Integer)
    consume_num_2: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_3: Mapped[int] = mapped_column(Integer)
    consume_num_3: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_4: Mapped[int] = mapped_column(Integer)
    consume_num_4: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_5: Mapped[int] = mapped_column(Integer)
    consume_num_5: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_6: Mapped[int] = mapped_column(Integer)
    consume_num_6: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_7: Mapped[int] = mapped_column(Integer)
    consume_num_7: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_8: Mapped[int] = mapped_column(Integer)
    consume_num_8: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_9: Mapped[int] = mapped_column(Integer)
    consume_num_9: Mapped[int] = mapped_column(Integer)
    condition_equipment_id_10: Mapped[int] = mapped_column(Integer)
    consume_num_10: Mapped[int] = mapped_column(Integer)


class EquipmentDatum(Base):
    __tablename__ = 'equipment_data'
    __table_args__ = (
        Index('equipment_data_0_original_equipment_id', 'original_equipment_id'),
    )

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    original_equipment_id: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    equipment_type: Mapped[int] = mapped_column(Integer)
    equipment_category: Mapped[int] = mapped_column(Integer)
    craft_flg: Mapped[int] = mapped_column(Integer)
    equipment_enhance_point: Mapped[int] = mapped_column(Integer)
    sale_price: Mapped[int] = mapped_column(Integer)
    require_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    enable_donation: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[float] = mapped_column(Float)
    display_item: Mapped[int] = mapped_column(Integer)
    item_type: Mapped[int] = mapped_column(Integer)


class EquipmentDonation(Base):
    __tablename__ = 'equipment_donation'

    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    donation_num_once: Mapped[int] = mapped_column(Integer)
    donation_num_daily: Mapped[int] = mapped_column(Integer)
    request_num_once: Mapped[int] = mapped_column(Integer)


class EquipmentEnhanceDatum(Base):
    __tablename__ = 'equipment_enhance_data'

    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_point: Mapped[int] = mapped_column(Integer)
    total_point: Mapped[int] = mapped_column(Integer)


class EquipmentEnhanceRate(Base):
    __tablename__ = 'equipment_enhance_rate'

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)


class EventBgDatum(Base):
    __tablename__ = 'event_bg_data'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[str] = mapped_column(Text)
    end_date: Mapped[str] = mapped_column(Text)


class EventBossTreasureBox(Base):
    __tablename__ = 'event_boss_treasure_box'

    event_boss_treasure_box_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_1: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_1: Mapped[int] = mapped_column(Integer)
    each_odds_1: Mapped[int] = mapped_column(Integer)
    treasure_type_2: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_2: Mapped[int] = mapped_column(Integer)
    each_odds_2: Mapped[int] = mapped_column(Integer)
    treasure_type_3: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_3: Mapped[int] = mapped_column(Integer)
    each_odds_3: Mapped[int] = mapped_column(Integer)
    treasure_type_4: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_4: Mapped[int] = mapped_column(Integer)
    each_odds_4: Mapped[int] = mapped_column(Integer)
    treasure_type_5: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_5: Mapped[int] = mapped_column(Integer)
    each_odds_5: Mapped[int] = mapped_column(Integer)
    treasure_type_6: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_6: Mapped[int] = mapped_column(Integer)
    each_odds_6: Mapped[int] = mapped_column(Integer)
    treasure_type_7: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_7: Mapped[int] = mapped_column(Integer)
    each_odds_7: Mapped[int] = mapped_column(Integer)
    treasure_type_8: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_8: Mapped[int] = mapped_column(Integer)
    each_odds_8: Mapped[int] = mapped_column(Integer)
    treasure_type_9: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_9: Mapped[int] = mapped_column(Integer)
    each_odds_9: Mapped[int] = mapped_column(Integer)
    treasure_type_10: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_content_id_10: Mapped[int] = mapped_column(Integer)
    each_odds_10: Mapped[int] = mapped_column(Integer)


class EventBossTreasureContent(Base):
    __tablename__ = 'event_boss_treasure_content'

    event_boss_treasure_content_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    odds_file_1: Mapped[str] = mapped_column(Text)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    odds_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    odds_file_2: Mapped[str] = mapped_column(Text)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    odds_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    odds_file_3: Mapped[str] = mapped_column(Text)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    odds_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    odds_file_4: Mapped[str] = mapped_column(Text)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    odds_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    odds_file_5: Mapped[str] = mapped_column(Text)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    odds_5: Mapped[int] = mapped_column(Integer)


class EventEffectSetting(Base):
    __tablename__ = 'event_effect_setting'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)


class EventEnemyParameter(Base):
    __tablename__ = 'event_enemy_parameter'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer)
    resist_status_id: Mapped[int] = mapped_column(Integer)
    resist_variation_id: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)


class EventEnemyRewardGroup(Base):
    __tablename__ = 'event_enemy_reward_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    odds: Mapped[int] = mapped_column(Integer)


class EventGachaDatum(Base):
    __tablename__ = 'event_gacha_data'
    __table_args__ = (
        Index('event_gacha_data_0_event_id', 'event_id'),
    )

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    gacha_name: Mapped[str] = mapped_column(Text)
    item_type: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[int] = mapped_column(Integer)
    cost: Mapped[int] = mapped_column(Integer)
    repeat_step: Mapped[int] = mapped_column(Integer)


class EventIntroduction(Base):
    __tablename__ = 'event_introduction'
    __table_args__ = (
        Index('event_introduction_0_event_id', 'event_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    introduction_number: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    maximum_chunk_size_1: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_loop_1: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_2: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_loop_2: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_3: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_loop_3: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)


class EventNaviComment(Base):
    __tablename__ = 'event_navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)


class EventNaviCommentCondition(Base):
    __tablename__ = 'event_navi_comment_condition'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type_1: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_type_2: Mapped[int] = mapped_column(Integer)
    condition_value_2: Mapped[int] = mapped_column(Integer)
    condition_type_3: Mapped[int] = mapped_column(Integer)
    condition_value_3: Mapped[int] = mapped_column(Integer)


class EventReminder(Base):
    __tablename__ = 'event_reminder'
    __table_args__ = (
        Index('event_reminder_0_event_id', 'event_id'),
    )

    reminder_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    title_text: Mapped[str] = mapped_column(Text)
    description_text: Mapped[str] = mapped_column(Text)
    notice_text: Mapped[str] = mapped_column(Text)
    thumbnail_id: Mapped[int] = mapped_column(Integer)
    btn_text: Mapped[str] = mapped_column(Text)
    target_type: Mapped[int] = mapped_column(Integer)
    target_id: Mapped[int] = mapped_column(Integer)


class EventReminderCondition(Base):
    __tablename__ = 'event_reminder_condition'
    __table_args__ = (
        Index('event_reminder_condition_0_reminder_id', 'reminder_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reminder_id: Mapped[int] = mapped_column(Integer)
    condition_type: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)


class EventRevivalSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_revival_series_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    wave: Mapped[int] = mapped_column(Integer)
    match_lv_min: Mapped[int] = mapped_column(Integer)
    match_lv_max: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    reward_group_id_1: Mapped[int] = mapped_column(Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer)
    reward_odds_1: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    reward_group_id_2: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer)
    reward_odds_2: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    reward_group_id_3: Mapped[int] = mapped_column(Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer)
    reward_odds_3: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    reward_group_id_4: Mapped[int] = mapped_column(Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer)
    reward_odds_4: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    reward_group_id_5: Mapped[int] = mapped_column(Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer)
    reward_odds_5: Mapped[int] = mapped_column(Integer)


class EventRevivalWaveGroupDatum(Base):
    __tablename__ = 'event_revival_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    wave: Mapped[int] = mapped_column(Integer)
    match_lv_min: Mapped[int] = mapped_column(Integer)
    match_lv_max: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    reward_group_id_1: Mapped[int] = mapped_column(Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer)
    reward_odds_1: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    reward_group_id_2: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer)
    reward_odds_2: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    reward_group_id_3: Mapped[int] = mapped_column(Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer)
    reward_odds_3: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    reward_group_id_4: Mapped[int] = mapped_column(Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer)
    reward_odds_4: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    reward_group_id_5: Mapped[int] = mapped_column(Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer)
    reward_odds_5: Mapped[int] = mapped_column(Integer)


class EventSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_series_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    wave: Mapped[int] = mapped_column(Integer)
    match_lv_min: Mapped[int] = mapped_column(Integer)
    match_lv_max: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    reward_group_id_1: Mapped[int] = mapped_column(Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer)
    reward_odds_1: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    reward_group_id_2: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer)
    reward_odds_2: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    reward_group_id_3: Mapped[int] = mapped_column(Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer)
    reward_odds_3: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    reward_group_id_4: Mapped[int] = mapped_column(Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer)
    reward_odds_4: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    reward_group_id_5: Mapped[int] = mapped_column(Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer)
    reward_odds_5: Mapped[int] = mapped_column(Integer)


class EventStoryDatum(Base):
    __tablename__ = 'event_story_data'
    __table_args__ = (
        Index('event_story_data_0_value', 'value'),
    )

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    thumbnail_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class EventStoryDetail(Base):
    __tablename__ = 'event_story_detail'
    __table_args__ = (
        Index('event_story_detail_0_story_group_id', 'story_group_id'),
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    visible_type: Mapped[int] = mapped_column(Integer)
    story_end: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)
    pre_story_id_2: Mapped[int] = mapped_column(Integer)
    love_level: Mapped[int] = mapped_column(Integer)
    requirement_id: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    story_quest_id: Mapped[int] = mapped_column(Integer)
    lock_all_text: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_value_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_value_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_value_3: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class EventTopAdv(Base):
    __tablename__ = 'event_top_adv'
    __table_args__ = (
        Index('event_top_adv_0_event_id_1_type', 'event_id', 'type'),
    )

    event_top_adv_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    value_1: Mapped[int] = mapped_column(Integer)
    value_2: Mapped[int] = mapped_column(Integer)
    value_3: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    condition_type: Mapped[int] = mapped_column(Integer)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class EventWaveGroupDatum(Base):
    __tablename__ = 'event_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    wave: Mapped[int] = mapped_column(Integer)
    match_lv_min: Mapped[int] = mapped_column(Integer)
    match_lv_max: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    reward_group_id_1: Mapped[int] = mapped_column(Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer)
    reward_odds_1: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    reward_group_id_2: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer)
    reward_odds_2: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    reward_group_id_3: Mapped[int] = mapped_column(Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer)
    reward_odds_3: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    reward_group_id_4: Mapped[int] = mapped_column(Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer)
    reward_odds_4: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    reward_group_id_5: Mapped[int] = mapped_column(Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer)
    reward_odds_5: Mapped[int] = mapped_column(Integer)


class ExEquipmentCategory(Base):
    __tablename__ = 'ex_equipment_category'

    category: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(Text)
    category_base: Mapped[str] = mapped_column(Text)
    outline: Mapped[str] = mapped_column(Text)
    recycle_item_id: Mapped[int] = mapped_column(Integer)


class ExEquipmentDatum(Base):
    __tablename__ = 'ex_equipment_data'

    ex_equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    rarity: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(Integer)
    restriction_id: Mapped[int] = mapped_column(Integer)
    clan_battle_equip_flag: Mapped[int] = mapped_column(Integer)
    is_force_protected: Mapped[int] = mapped_column(Integer)
    max_rank_flag: Mapped[int] = mapped_column(Integer)
    default_hp: Mapped[int] = mapped_column(Integer)
    max_hp: Mapped[int] = mapped_column(Integer)
    default_atk: Mapped[int] = mapped_column(Integer)
    max_atk: Mapped[int] = mapped_column(Integer)
    default_magic_str: Mapped[int] = mapped_column(Integer)
    max_magic_str: Mapped[int] = mapped_column(Integer)
    default_def: Mapped[int] = mapped_column(Integer)
    max_def: Mapped[int] = mapped_column(Integer)
    default_magic_def: Mapped[int] = mapped_column(Integer)
    max_magic_def: Mapped[int] = mapped_column(Integer)
    default_physical_critical: Mapped[int] = mapped_column(Integer)
    max_physical_critical: Mapped[int] = mapped_column(Integer)
    default_magic_critical: Mapped[int] = mapped_column(Integer)
    max_magic_critical: Mapped[int] = mapped_column(Integer)
    default_wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    max_wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    default_wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    max_wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    default_dodge: Mapped[int] = mapped_column(Integer)
    max_dodge: Mapped[int] = mapped_column(Integer)
    default_physical_penetrate: Mapped[int] = mapped_column(Integer)
    max_physical_penetrate: Mapped[int] = mapped_column(Integer)
    default_magic_penetrate: Mapped[int] = mapped_column(Integer)
    max_magic_penetrate: Mapped[int] = mapped_column(Integer)
    default_life_steal: Mapped[int] = mapped_column(Integer)
    max_life_steal: Mapped[int] = mapped_column(Integer)
    default_hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    max_hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    default_energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    max_energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    default_energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    max_energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    default_accuracy: Mapped[int] = mapped_column(Integer)
    max_accuracy: Mapped[int] = mapped_column(Integer)
    passive_skill_id_1: Mapped[int] = mapped_column(Integer)
    passive_skill_id_2: Mapped[int] = mapped_column(Integer)
    passive_skill_power: Mapped[int] = mapped_column(Integer)


class ExEquipmentEnhanceDatum(Base):
    __tablename__ = 'ex_equipment_enhance_data'
    __table_args__ = (
        Index('ex_equipment_enhance_data_0_rarity', 'rarity'),
    )

    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_mana: Mapped[int] = mapped_column(Integer)
    needed_point: Mapped[int] = mapped_column(Integer)
    total_point: Mapped[int] = mapped_column(Integer)
    rankup_level: Mapped[int] = mapped_column(Integer)


class ExEquipmentRankupDatum(Base):
    __tablename__ = 'ex_equipment_rankup_data'

    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    rankup_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_gold: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[int] = mapped_column(Integer)


class ExEquipmentRecycleReward(Base):
    __tablename__ = 'ex_equipment_recycle_reward'

    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_pt_coefficient: Mapped[int] = mapped_column(Integer)
    coin_coefficient: Mapped[int] = mapped_column(Integer)


class ExEquipmentRestrictionUnit(Base):
    __tablename__ = 'ex_equipment_restriction_unit'
    __table_args__ = (
        Index('ex_equipment_restriction_unit_0_restriction_id', 'restriction_id'),
    )

    restriction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExceedLevelStage(Base):
    __tablename__ = 'exceed_level_stage'

    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    increase_level_limit: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    unlock_team_level: Mapped[int] = mapped_column(Integer)
    general_exceed_item_id: Mapped[int] = mapped_column(Integer)


class ExceedLevelUnit(Base):
    __tablename__ = 'exceed_level_unit'
    __table_args__ = (
        Index('exceed_level_unit_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    exceed_item_id: Mapped[int] = mapped_column(Integer)
    item_id_1: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    consume_num_1: Mapped[int] = mapped_column(Integer)
    item_id_2: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    consume_num_2: Mapped[int] = mapped_column(Integer)
    item_id_3: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    consume_num_3: Mapped[int] = mapped_column(Integer)
    item_id_4: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    consume_num_4: Mapped[int] = mapped_column(Integer)
    item_id_5: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    consume_num_5: Mapped[int] = mapped_column(Integer)


class ExceptEr(Base):
    __tablename__ = 'except_er'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExperienceTeam(Base):
    __tablename__ = 'experience_team'

    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_exp: Mapped[int] = mapped_column(Integer)
    max_stamina: Mapped[int] = mapped_column(Integer)
    over_limit_stamina: Mapped[int] = mapped_column(Integer)
    recover_stamina_count: Mapped[int] = mapped_column(Integer)


class ExperienceUnit(Base):
    __tablename__ = 'experience_unit'

    unit_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_exp: Mapped[int] = mapped_column(Integer)


class FbsSchedule(Base):
    __tablename__ = 'fbs_schedule'

    fbs_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class FixLineupGroupSet(Base):
    __tablename__ = 'fix_lineup_group_set'
    __table_args__ = (
        Index('fix_lineup_group_set_0_team_level_from_1_team_level_to', 'team_level_from', 'team_level_to'),
    )

    lineup_group_set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    price_type_1: Mapped[int] = mapped_column(Integer)
    currency_id_1: Mapped[int] = mapped_column(Integer)
    price_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    price_type_2: Mapped[int] = mapped_column(Integer)
    currency_id_2: Mapped[int] = mapped_column(Integer)
    price_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    price_type_3: Mapped[int] = mapped_column(Integer)
    currency_id_3: Mapped[int] = mapped_column(Integer)
    price_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    price_type_4: Mapped[int] = mapped_column(Integer)
    currency_id_4: Mapped[int] = mapped_column(Integer)
    price_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    price_type_5: Mapped[int] = mapped_column(Integer)
    currency_id_5: Mapped[int] = mapped_column(Integer)
    price_5: Mapped[int] = mapped_column(Integer)
    reward_type_6: Mapped[int] = mapped_column(Integer)
    reward_id_6: Mapped[int] = mapped_column(Integer)
    reward_count_6: Mapped[int] = mapped_column(Integer)
    price_type_6: Mapped[int] = mapped_column(Integer)
    currency_id_6: Mapped[int] = mapped_column(Integer)
    price_6: Mapped[int] = mapped_column(Integer)
    reward_type_7: Mapped[int] = mapped_column(Integer)
    reward_id_7: Mapped[int] = mapped_column(Integer)
    reward_count_7: Mapped[int] = mapped_column(Integer)
    price_type_7: Mapped[int] = mapped_column(Integer)
    currency_id_7: Mapped[int] = mapped_column(Integer)
    price_7: Mapped[int] = mapped_column(Integer)
    reward_type_8: Mapped[int] = mapped_column(Integer)
    reward_id_8: Mapped[int] = mapped_column(Integer)
    reward_count_8: Mapped[int] = mapped_column(Integer)
    price_type_8: Mapped[int] = mapped_column(Integer)
    currency_id_8: Mapped[int] = mapped_column(Integer)
    price_8: Mapped[int] = mapped_column(Integer)
    reward_type_9: Mapped[int] = mapped_column(Integer)
    reward_id_9: Mapped[int] = mapped_column(Integer)
    reward_count_9: Mapped[int] = mapped_column(Integer)
    price_type_9: Mapped[int] = mapped_column(Integer)
    currency_id_9: Mapped[int] = mapped_column(Integer)
    price_9: Mapped[int] = mapped_column(Integer)
    reward_type_10: Mapped[int] = mapped_column(Integer)
    reward_id_10: Mapped[int] = mapped_column(Integer)
    reward_count_10: Mapped[int] = mapped_column(Integer)
    price_type_10: Mapped[int] = mapped_column(Integer)
    currency_id_10: Mapped[int] = mapped_column(Integer)
    price_10: Mapped[int] = mapped_column(Integer)
    reward_type_11: Mapped[int] = mapped_column(Integer)
    reward_id_11: Mapped[int] = mapped_column(Integer)
    reward_count_11: Mapped[int] = mapped_column(Integer)
    price_type_11: Mapped[int] = mapped_column(Integer)
    currency_id_11: Mapped[int] = mapped_column(Integer)
    price_11: Mapped[int] = mapped_column(Integer)
    reward_type_12: Mapped[int] = mapped_column(Integer)
    reward_id_12: Mapped[int] = mapped_column(Integer)
    reward_count_12: Mapped[int] = mapped_column(Integer)
    price_type_12: Mapped[int] = mapped_column(Integer)
    currency_id_12: Mapped[int] = mapped_column(Integer)
    price_12: Mapped[int] = mapped_column(Integer)
    reward_type_13: Mapped[int] = mapped_column(Integer)
    reward_id_13: Mapped[int] = mapped_column(Integer)
    reward_count_13: Mapped[int] = mapped_column(Integer)
    price_type_13: Mapped[int] = mapped_column(Integer)
    currency_id_13: Mapped[int] = mapped_column(Integer)
    price_13: Mapped[int] = mapped_column(Integer)
    reward_type_14: Mapped[int] = mapped_column(Integer)
    reward_id_14: Mapped[int] = mapped_column(Integer)
    reward_count_14: Mapped[int] = mapped_column(Integer)
    price_type_14: Mapped[int] = mapped_column(Integer)
    currency_id_14: Mapped[int] = mapped_column(Integer)
    price_14: Mapped[int] = mapped_column(Integer)
    reward_type_15: Mapped[int] = mapped_column(Integer)
    reward_id_15: Mapped[int] = mapped_column(Integer)
    reward_count_15: Mapped[int] = mapped_column(Integer)
    price_type_15: Mapped[int] = mapped_column(Integer)
    currency_id_15: Mapped[int] = mapped_column(Integer)
    price_15: Mapped[int] = mapped_column(Integer)
    reward_type_16: Mapped[int] = mapped_column(Integer)
    reward_id_16: Mapped[int] = mapped_column(Integer)
    reward_count_16: Mapped[int] = mapped_column(Integer)
    price_type_16: Mapped[int] = mapped_column(Integer)
    currency_id_16: Mapped[int] = mapped_column(Integer)
    price_16: Mapped[int] = mapped_column(Integer)
    reward_type_17: Mapped[int] = mapped_column(Integer)
    reward_id_17: Mapped[int] = mapped_column(Integer)
    reward_count_17: Mapped[int] = mapped_column(Integer)
    price_type_17: Mapped[int] = mapped_column(Integer)
    currency_id_17: Mapped[int] = mapped_column(Integer)
    price_17: Mapped[int] = mapped_column(Integer)
    reward_type_18: Mapped[int] = mapped_column(Integer)
    reward_id_18: Mapped[int] = mapped_column(Integer)
    reward_count_18: Mapped[int] = mapped_column(Integer)
    price_type_18: Mapped[int] = mapped_column(Integer)
    currency_id_18: Mapped[int] = mapped_column(Integer)
    price_18: Mapped[int] = mapped_column(Integer)
    reward_type_19: Mapped[int] = mapped_column(Integer)
    reward_id_19: Mapped[int] = mapped_column(Integer)
    reward_count_19: Mapped[int] = mapped_column(Integer)
    price_type_19: Mapped[int] = mapped_column(Integer)
    currency_id_19: Mapped[int] = mapped_column(Integer)
    price_19: Mapped[int] = mapped_column(Integer)
    reward_type_20: Mapped[int] = mapped_column(Integer)
    reward_id_20: Mapped[int] = mapped_column(Integer)
    reward_count_20: Mapped[int] = mapped_column(Integer)
    price_type_20: Mapped[int] = mapped_column(Integer)
    currency_id_20: Mapped[int] = mapped_column(Integer)
    price_20: Mapped[int] = mapped_column(Integer)


class FixLineupGroupSetDatum(Base):
    __tablename__ = 'fix_lineup_group_set_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lineup_group_set_id: Mapped[int] = mapped_column(Integer)
    team_level_from: Mapped[int] = mapped_column(Integer)
    team_level_to: Mapped[int] = mapped_column(Integer)
    box_count_from: Mapped[int] = mapped_column(Integer)
    box_count_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    price_type_1: Mapped[int] = mapped_column(Integer)
    currency_id_1: Mapped[int] = mapped_column(Integer)
    price_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    price_type_2: Mapped[int] = mapped_column(Integer)
    currency_id_2: Mapped[int] = mapped_column(Integer)
    price_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    price_type_3: Mapped[int] = mapped_column(Integer)
    currency_id_3: Mapped[int] = mapped_column(Integer)
    price_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    price_type_4: Mapped[int] = mapped_column(Integer)
    currency_id_4: Mapped[int] = mapped_column(Integer)
    price_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    price_type_5: Mapped[int] = mapped_column(Integer)
    currency_id_5: Mapped[int] = mapped_column(Integer)
    price_5: Mapped[int] = mapped_column(Integer)
    reward_type_6: Mapped[int] = mapped_column(Integer)
    reward_id_6: Mapped[int] = mapped_column(Integer)
    reward_count_6: Mapped[int] = mapped_column(Integer)
    price_type_6: Mapped[int] = mapped_column(Integer)
    currency_id_6: Mapped[int] = mapped_column(Integer)
    price_6: Mapped[int] = mapped_column(Integer)
    reward_type_7: Mapped[int] = mapped_column(Integer)
    reward_id_7: Mapped[int] = mapped_column(Integer)
    reward_count_7: Mapped[int] = mapped_column(Integer)
    price_type_7: Mapped[int] = mapped_column(Integer)
    currency_id_7: Mapped[int] = mapped_column(Integer)
    price_7: Mapped[int] = mapped_column(Integer)
    reward_type_8: Mapped[int] = mapped_column(Integer)
    reward_id_8: Mapped[int] = mapped_column(Integer)
    reward_count_8: Mapped[int] = mapped_column(Integer)
    price_type_8: Mapped[int] = mapped_column(Integer)
    currency_id_8: Mapped[int] = mapped_column(Integer)
    price_8: Mapped[int] = mapped_column(Integer)
    reward_type_9: Mapped[int] = mapped_column(Integer)
    reward_id_9: Mapped[int] = mapped_column(Integer)
    reward_count_9: Mapped[int] = mapped_column(Integer)
    price_type_9: Mapped[int] = mapped_column(Integer)
    currency_id_9: Mapped[int] = mapped_column(Integer)
    price_9: Mapped[int] = mapped_column(Integer)
    reward_type_10: Mapped[int] = mapped_column(Integer)
    reward_id_10: Mapped[int] = mapped_column(Integer)
    reward_count_10: Mapped[int] = mapped_column(Integer)
    price_type_10: Mapped[int] = mapped_column(Integer)
    currency_id_10: Mapped[int] = mapped_column(Integer)
    price_10: Mapped[int] = mapped_column(Integer)
    reward_type_11: Mapped[int] = mapped_column(Integer)
    reward_id_11: Mapped[int] = mapped_column(Integer)
    reward_count_11: Mapped[int] = mapped_column(Integer)
    price_type_11: Mapped[int] = mapped_column(Integer)
    currency_id_11: Mapped[int] = mapped_column(Integer)
    price_11: Mapped[int] = mapped_column(Integer)
    reward_type_12: Mapped[int] = mapped_column(Integer)
    reward_id_12: Mapped[int] = mapped_column(Integer)
    reward_count_12: Mapped[int] = mapped_column(Integer)
    price_type_12: Mapped[int] = mapped_column(Integer)
    currency_id_12: Mapped[int] = mapped_column(Integer)
    price_12: Mapped[int] = mapped_column(Integer)
    reward_type_13: Mapped[int] = mapped_column(Integer)
    reward_id_13: Mapped[int] = mapped_column(Integer)
    reward_count_13: Mapped[int] = mapped_column(Integer)
    price_type_13: Mapped[int] = mapped_column(Integer)
    currency_id_13: Mapped[int] = mapped_column(Integer)
    price_13: Mapped[int] = mapped_column(Integer)
    reward_type_14: Mapped[int] = mapped_column(Integer)
    reward_id_14: Mapped[int] = mapped_column(Integer)
    reward_count_14: Mapped[int] = mapped_column(Integer)
    price_type_14: Mapped[int] = mapped_column(Integer)
    currency_id_14: Mapped[int] = mapped_column(Integer)
    price_14: Mapped[int] = mapped_column(Integer)
    reward_type_15: Mapped[int] = mapped_column(Integer)
    reward_id_15: Mapped[int] = mapped_column(Integer)
    reward_count_15: Mapped[int] = mapped_column(Integer)
    price_type_15: Mapped[int] = mapped_column(Integer)
    currency_id_15: Mapped[int] = mapped_column(Integer)
    price_15: Mapped[int] = mapped_column(Integer)
    reward_type_16: Mapped[int] = mapped_column(Integer)
    reward_id_16: Mapped[int] = mapped_column(Integer)
    reward_count_16: Mapped[int] = mapped_column(Integer)
    price_type_16: Mapped[int] = mapped_column(Integer)
    currency_id_16: Mapped[int] = mapped_column(Integer)
    price_16: Mapped[int] = mapped_column(Integer)
    reward_type_17: Mapped[int] = mapped_column(Integer)
    reward_id_17: Mapped[int] = mapped_column(Integer)
    reward_count_17: Mapped[int] = mapped_column(Integer)
    price_type_17: Mapped[int] = mapped_column(Integer)
    currency_id_17: Mapped[int] = mapped_column(Integer)
    price_17: Mapped[int] = mapped_column(Integer)
    reward_type_18: Mapped[int] = mapped_column(Integer)
    reward_id_18: Mapped[int] = mapped_column(Integer)
    reward_count_18: Mapped[int] = mapped_column(Integer)
    price_type_18: Mapped[int] = mapped_column(Integer)
    currency_id_18: Mapped[int] = mapped_column(Integer)
    price_18: Mapped[int] = mapped_column(Integer)
    reward_type_19: Mapped[int] = mapped_column(Integer)
    reward_id_19: Mapped[int] = mapped_column(Integer)
    reward_count_19: Mapped[int] = mapped_column(Integer)
    price_type_19: Mapped[int] = mapped_column(Integer)
    currency_id_19: Mapped[int] = mapped_column(Integer)
    price_19: Mapped[int] = mapped_column(Integer)
    reward_type_20: Mapped[int] = mapped_column(Integer)
    reward_id_20: Mapped[int] = mapped_column(Integer)
    reward_count_20: Mapped[int] = mapped_column(Integer)
    price_type_20: Mapped[int] = mapped_column(Integer)
    currency_id_20: Mapped[int] = mapped_column(Integer)
    price_20: Mapped[int] = mapped_column(Integer)


class FkeHappeningList(Base):
    __tablename__ = 'fke_happening_list'

    happening_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    happening_name: Mapped[str] = mapped_column(Text)


class FkeReward(Base):
    __tablename__ = 'fke_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fke_point: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class GachaDatum(Base):
    __tablename__ = 'gacha_data'
    __table_args__ = (
        Index('gacha_data_0_exchange_id', 'exchange_id'),
    )

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_name: Mapped[str] = mapped_column(Text)
    pick_up_chara_text: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    description_2: Mapped[str] = mapped_column(Text)
    description_sp: Mapped[str] = mapped_column(Text)
    parallel_id: Mapped[int] = mapped_column(Integer)
    pickup_badge: Mapped[int] = mapped_column(Integer)
    gacha_detail: Mapped[int] = mapped_column(Integer)
    gacha_cost_type: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    free_gacha_type: Mapped[int] = mapped_column(Integer)
    free_gacha_interval_time: Mapped[int] = mapped_column(Integer)
    free_gacha_count: Mapped[int] = mapped_column(Integer)
    discount_price: Mapped[int] = mapped_column(Integer)
    gacha_odds: Mapped[str] = mapped_column(Text)
    gacha_odds_star2: Mapped[str] = mapped_column(Text)
    gacha_type: Mapped[int] = mapped_column(Integer)
    movie_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    ticket_id: Mapped[int] = mapped_column(Integer)
    special_id: Mapped[int] = mapped_column(Integer)
    exchange_id: Mapped[int] = mapped_column(Integer)
    ticket_id_10: Mapped[int] = mapped_column(Integer)
    rarity_odds: Mapped[str] = mapped_column(Text)
    chara_odds_star1: Mapped[str] = mapped_column(Text)
    chara_odds_star2: Mapped[str] = mapped_column(Text)
    chara_odds_star3: Mapped[str] = mapped_column(Text)
    gacha10_special_odds_star1: Mapped[str] = mapped_column(Text)
    gacha10_special_odds_star2: Mapped[str] = mapped_column(Text)
    gacha10_special_odds_star3: Mapped[str] = mapped_column(Text)
    prizegacha_id: Mapped[int] = mapped_column(Integer)
    gacha_bonus_id: Mapped[int] = mapped_column(Integer)
    gacha_times_limit10: Mapped[int] = mapped_column(Integer)
    pickup_id: Mapped[int] = mapped_column(Integer)


class GachaExchangeLineup(Base):
    __tablename__ = 'gacha_exchange_lineup'
    __table_args__ = (
        Index('gacha_exchange_lineup_0_exchange_id', 'exchange_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    gacha_bonus_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class GachaPickup(Base):
    __tablename__ = 'gacha_pickup'
    __table_args__ = (
        Index('gacha_pickup_0_id', 'id'),
        Index('gacha_pickup_0_id_1_reward_id', 'id', 'reward_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)


class GiftMessage(Base):
    __tablename__ = 'gift_message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discription: Mapped[str] = mapped_column(Text)
    type_1: Mapped[int] = mapped_column(Integer)
    type_2: Mapped[int] = mapped_column(Integer)
    type_3: Mapped[int] = mapped_column(Integer)
    type_4: Mapped[int] = mapped_column(Integer)


class GlobalDatum(Base):
    __tablename__ = 'global_data'

    key_name: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)
    desc: Mapped[str] = mapped_column(Text)


class GlossaryDetail(Base):
    __tablename__ = 'glossary_detail'

    glossary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    glossary_category_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    unlock_story_id: Mapped[int] = mapped_column(Integer)
    category_type: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)


class GoldsetDatum(Base):
    __tablename__ = 'goldset_data'

    id: Mapped[int] = mapped_column(Integer)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_jewel_count: Mapped[int] = mapped_column(Integer)
    get_gold_count: Mapped[int] = mapped_column(Integer)
    goldset_odds_1: Mapped[int] = mapped_column(Integer)
    goldset_odds_2: Mapped[int] = mapped_column(Integer)
    goldset_odds_3: Mapped[int] = mapped_column(Integer)
    additional_gold_min_rate: Mapped[int] = mapped_column(Integer)
    additional_gold_max_rate: Mapped[int] = mapped_column(Integer)


class GoldsetData2(Base):
    __tablename__ = 'goldset_data_2'

    id: Mapped[int] = mapped_column(Integer)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_jewel_count: Mapped[int] = mapped_column(Integer)
    get_gold_count: Mapped[int] = mapped_column(Integer)
    goldset_odds_1: Mapped[int] = mapped_column(Integer)
    goldset_odds_2: Mapped[int] = mapped_column(Integer)
    goldset_odds_3: Mapped[int] = mapped_column(Integer)
    additional_gold_min_rate: Mapped[int] = mapped_column(Integer)
    additional_gold_max_rate: Mapped[int] = mapped_column(Integer)
    training_quest_count: Mapped[int] = mapped_column(Integer)


class GoldsetDataTeamlevel(Base):
    __tablename__ = 'goldset_data_teamlevel'

    id: Mapped[int] = mapped_column(Integer)
    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    initial_get_gold_count: Mapped[int] = mapped_column(Integer)


class GrandArenaDailyRankReward(Base):
    __tablename__ = 'grand_arena_daily_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class GrandArenaDefenceReward(Base):
    __tablename__ = 'grand_arena_defence_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_count: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class GrandArenaMaxRankReward(Base):
    __tablename__ = 'grand_arena_max_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class GrandArenaMaxSeasonRankReward(Base):
    __tablename__ = 'grand_arena_max_season_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer)
    rank_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class GrowthParameter(Base):
    __tablename__ = 'growth_parameter'

    growth_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    growth_type: Mapped[int] = mapped_column(Integer)
    is_restriction: Mapped[int] = mapped_column(Integer)
    unit_rarity: Mapped[int] = mapped_column(Integer)
    unit_level: Mapped[int] = mapped_column(Integer)
    skill_level: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    equipment_1: Mapped[int] = mapped_column(Integer)
    equipment_2: Mapped[int] = mapped_column(Integer)
    equipment_3: Mapped[int] = mapped_column(Integer)
    equipment_4: Mapped[int] = mapped_column(Integer)
    equipment_5: Mapped[int] = mapped_column(Integer)
    equipment_6: Mapped[int] = mapped_column(Integer)
    love_level: Mapped[int] = mapped_column(Integer)


class GrowthParameterUnique(Base):
    __tablename__ = 'growth_parameter_unique'

    growth_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_equip_strength_point_1: Mapped[int] = mapped_column(Integer)
    unique_equip_strength_point_2: Mapped[int] = mapped_column(Integer)
    unique_equip_rank_1: Mapped[int] = mapped_column(Integer)
    unique_equip_rank_2: Mapped[int] = mapped_column(Integer)


class GrowthRestrictionUnit(Base):
    __tablename__ = 'growth_restriction_unit'
    __table_args__ = (
        Index('growth_restriction_unit_0_growth_id', 'growth_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    growth_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)


class Guild(Base):
    __tablename__ = 'guild'

    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    guild_master: Mapped[int] = mapped_column(Integer)
    member1: Mapped[int] = mapped_column(Integer)
    member2: Mapped[int] = mapped_column(Integer)
    member3: Mapped[int] = mapped_column(Integer)
    member4: Mapped[int] = mapped_column(Integer)
    member5: Mapped[int] = mapped_column(Integer)
    member6: Mapped[int] = mapped_column(Integer)
    member7: Mapped[int] = mapped_column(Integer)
    member8: Mapped[int] = mapped_column(Integer)
    member9: Mapped[int] = mapped_column(Integer)
    member10: Mapped[int] = mapped_column(Integer)
    member11: Mapped[int] = mapped_column(Integer)
    member12: Mapped[int] = mapped_column(Integer)
    member13: Mapped[int] = mapped_column(Integer)
    member14: Mapped[int] = mapped_column(Integer)
    member15: Mapped[int] = mapped_column(Integer)
    member16: Mapped[int] = mapped_column(Integer)
    member17: Mapped[int] = mapped_column(Integer)
    member18: Mapped[int] = mapped_column(Integer)
    member19: Mapped[int] = mapped_column(Integer)
    member20: Mapped[int] = mapped_column(Integer)
    member21: Mapped[int] = mapped_column(Integer)
    member22: Mapped[int] = mapped_column(Integer)
    member23: Mapped[int] = mapped_column(Integer)
    member24: Mapped[int] = mapped_column(Integer)
    member25: Mapped[int] = mapped_column(Integer)
    member26: Mapped[int] = mapped_column(Integer)
    member27: Mapped[int] = mapped_column(Integer)
    member28: Mapped[int] = mapped_column(Integer)
    member29: Mapped[int] = mapped_column(Integer)
    member30: Mapped[int] = mapped_column(Integer)


class GuildAdditionalMember(Base):
    __tablename__ = 'guild_additional_member'

    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_story_id: Mapped[int] = mapped_column(Integer)
    thumb_id: Mapped[int] = mapped_column(Integer)
    member1: Mapped[int] = mapped_column(Integer)
    member2: Mapped[int] = mapped_column(Integer)
    member3: Mapped[int] = mapped_column(Integer)
    member4: Mapped[int] = mapped_column(Integer)
    member5: Mapped[int] = mapped_column(Integer)
    member6: Mapped[int] = mapped_column(Integer)
    member7: Mapped[int] = mapped_column(Integer)
    member8: Mapped[int] = mapped_column(Integer)
    member9: Mapped[int] = mapped_column(Integer)
    member10: Mapped[int] = mapped_column(Integer)


class HatsuneBattleMissionDatum(Base):
    __tablename__ = 'hatsune_battle_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneBgChange(Base):
    __tablename__ = 'hatsune_bg_change'

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id_1: Mapped[int] = mapped_column(Integer)
    quest_id_2: Mapped[int] = mapped_column(Integer)
    quest_id_3: Mapped[int] = mapped_column(Integer)
    quest_id_4: Mapped[int] = mapped_column(Integer)
    quest_id_5: Mapped[int] = mapped_column(Integer)


class HatsuneBgChangeDatum(Base):
    __tablename__ = 'hatsune_bg_change_data'
    __table_args__ = (
        Index('hatsune_bg_change_data_0_target_type_1_area_id', 'target_type', 'area_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int] = mapped_column(Integer)
    condition_type: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    target_type: Mapped[int] = mapped_column(Integer)
    bg_after_change_id: Mapped[int] = mapped_column(Integer)


class HatsuneBoss(Base):
    __tablename__ = 'hatsune_boss'
    __table_args__ = (
        Index('hatsune_boss_0_event_id', 'event_id'),
        Index('hatsune_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
        Index('hatsune_boss_0_wave_group_id_1', 'wave_group_id_1')
    )

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    boss_position_x: Mapped[int] = mapped_column(Integer)
    boss_position_y: Mapped[int] = mapped_column(Integer)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    icon_display_scale: Mapped[float] = mapped_column(Float)
    icon_collider_scale: Mapped[float] = mapped_column(Float)
    use_ticket_num: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    unit_exp: Mapped[int] = mapped_column(Integer)
    love: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    daily_limit: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_box_id_1: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer)
    detail_bg_id: Mapped[int] = mapped_column(Integer)
    detail_bg_position: Mapped[int] = mapped_column(Integer)
    detail_boss_bg_size: Mapped[float] = mapped_column(Float)
    detail_boss_bg_height: Mapped[float] = mapped_column(Float)
    reward_gold_coefficient: Mapped[str] = mapped_column(Text)
    reward_gold_limit: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    map_position_x: Mapped[float] = mapped_column(Float)
    map_position_y: Mapped[float] = mapped_column(Float)
    map_size: Mapped[float] = mapped_column(Float)
    map_arrow_offset: Mapped[float] = mapped_column(Float)
    deatail_aura_size: Mapped[float] = mapped_column(Float)
    map_aura_size: Mapped[float] = mapped_column(Float)
    oneblow_count_of_skip_condition: Mapped[int] = mapped_column(Integer)
    required_skip_ticket_count: Mapped[int] = mapped_column(Integer)
    retire_flag: Mapped[int] = mapped_column(Integer)
    disp_on_bg: Mapped[int] = mapped_column(Integer)
    qd_mode: Mapped[int] = mapped_column(Integer)
    td_mode: Mapped[int] = mapped_column(Integer)


class HatsuneBossCondition(Base):
    __tablename__ = 'hatsune_boss_condition'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer)
    condition_boss_id_1: Mapped[int] = mapped_column(Integer)
    condition_boss_id_2: Mapped[int] = mapped_column(Integer)
    condition_gacha_step: Mapped[int] = mapped_column(Integer)
    force_unlock_time: Mapped[str] = mapped_column(Text)
    release_quest_id_1: Mapped[int] = mapped_column(Integer)
    release_quest_id_2: Mapped[int] = mapped_column(Integer)
    release_boss_id_1: Mapped[int] = mapped_column(Integer)
    release_boss_id_2: Mapped[int] = mapped_column(Integer)


class HatsuneBossEnemySetting(Base):
    __tablename__ = 'hatsune_boss_enemy_setting'
    __table_args__ = (
        Index('hatsune_boss_enemy_setting_0_boss_id_1_event_id', 'boss_id', 'event_id'),
    )

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_identify: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    must_kill_flag: Mapped[int] = mapped_column(Integer)
    event_boss_treasure_box_id: Mapped[int] = mapped_column(Integer)
    reward_gold_coefficient: Mapped[float] = mapped_column(Float)
    reward_gold_limit: Mapped[int] = mapped_column(Integer)
    detail_offset_x: Mapped[int] = mapped_column(Integer)
    detail_offset_y: Mapped[int] = mapped_column(Integer)
    detail_scale: Mapped[float] = mapped_column(Float)
    map_offset_x: Mapped[int] = mapped_column(Integer)
    map_offset_y: Mapped[int] = mapped_column(Integer)
    map_scale: Mapped[float] = mapped_column(Float)
    map_depth: Mapped[int] = mapped_column(Integer)


class HatsuneDailyMissionDatum(Base):
    __tablename__ = 'hatsune_daily_mission_data'

    daily_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneDescription(Base):
    __tablename__ = 'hatsune_description'
    __table_args__ = (
        Index('hatsune_description_0_event_id_1_type', 'event_id', 'type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class HatsuneDiaryDatum(Base):
    __tablename__ = 'hatsune_diary_data'
    __table_args__ = (
        Index('hatsune_diary_data_0_contents_type', 'contents_type'),
    )

    diary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contents_type: Mapped[int] = mapped_column(Integer)
    diary_date: Mapped[int] = mapped_column(Integer)
    sub_title: Mapped[str] = mapped_column(Text)
    forced_release_time: Mapped[str] = mapped_column(Text)
    condition_time: Mapped[str] = mapped_column(Text)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    condition_boss_count: Mapped[int] = mapped_column(Integer)


class HatsuneDiaryLetterScript(Base):
    __tablename__ = 'hatsune_diary_letter_script'
    __table_args__ = (
        Index('hatsune_diary_letter_script_0_diary_id', 'diary_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diary_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class HatsuneDiaryScript(Base):
    __tablename__ = 'hatsune_diary_script'
    __table_args__ = (
        Index('hatsune_diary_script_0_diary_id', 'diary_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diary_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    diary_text: Mapped[str] = mapped_column(Text)
    text_animation_speed: Mapped[int] = mapped_column(Integer)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class HatsuneDiarySetting(Base):
    __tablename__ = 'hatsune_diary_setting'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bgm_sheet_name: Mapped[str] = mapped_column(Text)
    bgm_cue_name: Mapped[str] = mapped_column(Text)


class HatsuneEmblemMission(Base):
    __tablename__ = 'hatsune_emblem_mission'
    __table_args__ = (
        Index('hatsune_emblem_mission_0_event_id', 'event_id'),
    )

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_value_2: Mapped[int] = mapped_column(Integer)
    condition_value_3: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    system_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    visible_flag: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class HatsuneEmblemMissionReward(Base):
    __tablename__ = 'hatsune_emblem_mission_reward'
    __table_args__ = (
        Index('hatsune_emblem_mission_reward_0_mission_reward_id', 'mission_reward_id'),
        Index('hatsune_emblem_mission_reward_0_reward_id', 'reward_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    icon_type: Mapped[int] = mapped_column(Integer)


class HatsuneItem(Base):
    __tablename__ = 'hatsune_item'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_ticket_id: Mapped[int] = mapped_column(Integer)
    gacha_ticket_id: Mapped[int] = mapped_column(Integer)
    unit_material_id_1: Mapped[int] = mapped_column(Integer)
    unit_material_id_2: Mapped[int] = mapped_column(Integer)
    unit_material_id_3: Mapped[int] = mapped_column(Integer)
    unit_material_id_4: Mapped[int] = mapped_column(Integer)
    unit_material_id_5: Mapped[int] = mapped_column(Integer)
    unit_material_id_6: Mapped[int] = mapped_column(Integer)
    unit_material_id_7: Mapped[int] = mapped_column(Integer)
    unit_material_id_8: Mapped[int] = mapped_column(Integer)
    unit_material_id_9: Mapped[int] = mapped_column(Integer)
    unit_material_id_10: Mapped[int] = mapped_column(Integer)


class HatsuneLimitChara(Base):
    __tablename__ = 'hatsune_limit_chara'

    event_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_chara_type_1: Mapped[int] = mapped_column(Integer)


class HatsuneMap(Base):
    __tablename__ = 'hatsune_map'

    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    map_id: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    start_area_id: Mapped[int] = mapped_column(Integer)
    end_area_id: Mapped[int] = mapped_column(Integer)


class HatsuneMapEvent(Base):
    __tablename__ = 'hatsune_map_event'
    __table_args__ = (
        Index('hatsune_map_event_0_target_event_id', 'target_event_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_event_id: Mapped[int] = mapped_column(Integer)
    event_type: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    param1: Mapped[int] = mapped_column(Integer)
    param2: Mapped[int] = mapped_column(Integer)


class HatsuneMissionRewardDatum(Base):
    __tablename__ = 'hatsune_mission_reward_data'
    __table_args__ = (
        Index('hatsune_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneMultiRouteParameter(Base):
    __tablename__ = 'hatsune_multi_route_parameter'
    __table_args__ = (
        Index('hatsune_multi_route_parameter_0_quest_id', 'quest_id'),
        Index('hatsune_multi_route_parameter_0_type', 'type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    param_1: Mapped[int] = mapped_column(Integer)
    param_2: Mapped[int] = mapped_column(Integer)
    param_3: Mapped[int] = mapped_column(Integer)
    text_1: Mapped[str] = mapped_column(Text)


class HatsunePresent(Base):
    __tablename__ = 'hatsune_present'
    __table_args__ = (
        Index('hatsune_present_0_event_id', 'event_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    dialog_title: Mapped[str] = mapped_column(Text)
    dialog_text: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    condition_mission_id: Mapped[int] = mapped_column(Integer)
    adv_id: Mapped[int] = mapped_column(Integer)
    item_type_1: Mapped[int] = mapped_column(Integer)
    item_id_1: Mapped[int] = mapped_column(Integer)
    item_num_1: Mapped[int] = mapped_column(Integer)
    item_type_2: Mapped[int] = mapped_column(Integer)
    item_id_2: Mapped[int] = mapped_column(Integer)
    item_num_2: Mapped[int] = mapped_column(Integer)
    item_type_3: Mapped[int] = mapped_column(Integer)
    item_id_3: Mapped[int] = mapped_column(Integer)
    item_num_3: Mapped[int] = mapped_column(Integer)
    item_type_4: Mapped[int] = mapped_column(Integer)
    item_id_4: Mapped[int] = mapped_column(Integer)
    item_num_4: Mapped[int] = mapped_column(Integer)
    item_type_5: Mapped[int] = mapped_column(Integer)
    item_id_5: Mapped[int] = mapped_column(Integer)
    item_num_5: Mapped[int] = mapped_column(Integer)


class HatsuneQuest(Base):
    __tablename__ = 'hatsune_quest'
    __table_args__ = (
        Index('hatsune_quest_0_event_id', 'event_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_id: Mapped[int] = mapped_column(Integer)
    quest_seq: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    icon_offset_x: Mapped[float] = mapped_column(Float)
    icon_offset_y: Mapped[float] = mapped_column(Float)
    icon_scale: Mapped[float] = mapped_column(Float)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    unit_exp: Mapped[int] = mapped_column(Integer)
    love: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    daily_limit: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    rank_reward_group: Mapped[int] = mapped_column(Integer)
    drop_reward_type: Mapped[int] = mapped_column(Integer)
    drop_reward_id: Mapped[int] = mapped_column(Integer)
    drop_reward_num: Mapped[int] = mapped_column(Integer)
    drop_reward_odds: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class HatsuneQuestArea(Base):
    __tablename__ = 'hatsune_quest_area'
    __table_args__ = (
        Index('hatsune_quest_area_0_event_id', 'event_id'),
    )

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    area_disp: Mapped[int] = mapped_column(Integer)
    map_id: Mapped[int] = mapped_column(Integer)
    scroll_width: Mapped[int] = mapped_column(Integer)
    scroll_height: Mapped[int] = mapped_column(Integer)
    open_tutorial_id: Mapped[int] = mapped_column(Integer)
    tutorial_param_1: Mapped[str] = mapped_column(Text)
    tutorial_param_2: Mapped[str] = mapped_column(Text)
    additional_effect: Mapped[int] = mapped_column(Integer)


class HatsuneQuestCondition(Base):
    __tablename__ = 'hatsune_quest_condition'
    __table_args__ = (
        Index('hatsune_quest_condition_0_event_id', 'event_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer)
    condition_boss_id_1: Mapped[int] = mapped_column(Integer)
    condition_boss_id_2: Mapped[int] = mapped_column(Integer)
    release_quest_id_1: Mapped[int] = mapped_column(Integer)
    release_quest_id_2: Mapped[int] = mapped_column(Integer)
    release_boss_id_1: Mapped[int] = mapped_column(Integer)
    release_boss_id_2: Mapped[int] = mapped_column(Integer)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer)


class HatsuneQuiz(Base):
    __tablename__ = 'hatsune_quiz'
    __table_args__ = (
        Index('hatsune_quiz_0_event_id', 'event_id'),
        Index('hatsune_quiz_0_event_id_1_release_quest_id', 'event_id', 'release_quest_id')
    )

    event_id: Mapped[int] = mapped_column(Integer)
    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_title: Mapped[str] = mapped_column(Text)
    question: Mapped[str] = mapped_column(Text)
    choice_1: Mapped[str] = mapped_column(Text)
    choice_2: Mapped[str] = mapped_column(Text)
    choice_3: Mapped[str] = mapped_column(Text)
    choice_4: Mapped[str] = mapped_column(Text)
    choice_5: Mapped[str] = mapped_column(Text)
    choice_6: Mapped[str] = mapped_column(Text)
    answer: Mapped[int] = mapped_column(Integer)
    hint: Mapped[str] = mapped_column(Text)
    resource_id: Mapped[int] = mapped_column(Integer)
    release_quest_id: Mapped[int] = mapped_column(Integer)
    quiz_position_x: Mapped[int] = mapped_column(Integer)
    quiz_position_y: Mapped[int] = mapped_column(Integer)
    quiz_icon_id: Mapped[int] = mapped_column(Integer)
    quiz_point_name: Mapped[str] = mapped_column(Text)
    adv_id_quiz_start: Mapped[int] = mapped_column(Integer)
    adv_id_quiz_end: Mapped[int] = mapped_column(Integer)


class HatsuneQuizCondition(Base):
    __tablename__ = 'hatsune_quiz_condition'
    __table_args__ = (
        Index('hatsune_quiz_condition_0_event_id_1_quiz_id', 'event_id', 'quiz_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    quiz_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_quiz_id: Mapped[int] = mapped_column(Integer)
    condition_unit_id: Mapped[int] = mapped_column(Integer)
    condition_mission_id: Mapped[int] = mapped_column(Integer)
    condition_time_from: Mapped[int] = mapped_column(Integer)


class HatsuneQuizReward(Base):
    __tablename__ = 'hatsune_quiz_reward'

    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class HatsuneRelayDatum(Base):
    __tablename__ = 'hatsune_relay_data'

    relay_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_enable_read: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    story_seq: Mapped[int] = mapped_column(Integer)
    sub_title: Mapped[str] = mapped_column(Text)


class HatsuneSchedule(Base):
    __tablename__ = 'hatsune_schedule'
    __table_args__ = (
        Index('hatsune_schedule_0_original_event_id', 'original_event_id'),
        Index('hatsune_schedule_0_series_event_id', 'series_event_id')
    )

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)
    background: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    banner_unit_id: Mapped[int] = mapped_column(Integer)
    count_start_time: Mapped[str] = mapped_column(Text)
    backgroud_size_x: Mapped[int] = mapped_column(Integer)
    backgroud_size_y: Mapped[int] = mapped_column(Integer)
    backgroud_pos_x: Mapped[int] = mapped_column(Integer)
    backgroud_pos_y: Mapped[int] = mapped_column(Integer)
    original_event_id: Mapped[int] = mapped_column(Integer)
    series_event_id: Mapped[int] = mapped_column(Integer)
    teaser_dialog_type: Mapped[int] = mapped_column(Integer)


class HatsuneSeriesGachaReference(Base):
    __tablename__ = 'hatsune_series_gacha_reference'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reference_key_event_id_flag: Mapped[int] = mapped_column(Integer)


class HatsuneSpecialBattle(Base):
    __tablename__ = 'hatsune_special_battle'
    __table_args__ = (
        Index('hatsune_special_battle_0_event_id', 'event_id'),
        Index('hatsune_special_battle_0_wave_group_id', 'wave_group_id')
    )

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommended_level: Mapped[int] = mapped_column(Integer)
    purpose_type: Mapped[int] = mapped_column(Integer)
    purpose_count: Mapped[int] = mapped_column(Integer)
    trigger_hp: Mapped[int] = mapped_column(Integer)
    story_id_mode_start: Mapped[int] = mapped_column(Integer)
    story_id_mode_end: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer)
    story_start_second: Mapped[float] = mapped_column(Float)
    action_start_second: Mapped[float] = mapped_column(Float)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer)
    start_idle_trigger: Mapped[int] = mapped_column(Integer)
    appear_time: Mapped[float] = mapped_column(Float)
    detail_boss_bg_size: Mapped[float] = mapped_column(Float)
    detail_boss_bg_height: Mapped[float] = mapped_column(Float)
    detail_boss_motion: Mapped[str] = mapped_column(Text)
    is_hide_boss: Mapped[int] = mapped_column(Integer)


class HatsuneSpecialBossTicketCount(Base):
    __tablename__ = 'hatsune_special_boss_ticket_count'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    challenge_count_from: Mapped[int] = mapped_column(Integer)
    challenge_count_to: Mapped[int] = mapped_column(Integer)
    use_ticket_num: Mapped[int] = mapped_column(Integer)


class HatsuneSpecialEnemy(Base):
    __tablename__ = 'hatsune_special_enemy'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[int] = mapped_column(Integer)
    enemy_point: Mapped[int] = mapped_column(Integer)
    initial_position: Mapped[int] = mapped_column(Integer)
    order: Mapped[int] = mapped_column(Integer)


class HatsuneSpecialMissionDatum(Base):
    __tablename__ = 'hatsune_special_mission_data'

    special_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    purpose_type: Mapped[int] = mapped_column(Integer)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneStationaryMissionDatum(Base):
    __tablename__ = 'hatsune_stationary_mission_data'
    __table_args__ = (
        Index('hatsune_stationary_mission_data_0_event_id', 'event_id'),
    )

    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneUnlockStoryCondition(Base):
    __tablename__ = 'hatsune_unlock_story_condition'
    __table_args__ = (
        Index('hatsune_unlock_story_condition_0_event_id', 'event_id'),
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_entry: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    condition_mission_id: Mapped[int] = mapped_column(Integer)
    condition_time: Mapped[str] = mapped_column(Text)
    condition_story_id: Mapped[int] = mapped_column(Integer)


class HatsuneUnlockUnitCondition(Base):
    __tablename__ = 'hatsune_unlock_unit_condition'
    __table_args__ = (
        Index('hatsune_unlock_unit_condition_0_condition_mission_id', 'condition_mission_id'),
        Index('hatsune_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_mission_id: Mapped[int] = mapped_column(Integer)
    top_description: Mapped[str] = mapped_column(Text)
    description_1: Mapped[str] = mapped_column(Text)
    description_2: Mapped[str] = mapped_column(Text)


class HpDrainAt(Base):
    __tablename__ = 'hp_drain_at'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_value: Mapped[int] = mapped_column(Integer)
    correction_value: Mapped[float] = mapped_column(Float)


class ItemDatum(Base):
    __tablename__ = 'item_data'

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    promotion_level: Mapped[int] = mapped_column(Integer)
    item_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    limit_num: Mapped[int] = mapped_column(Integer)
    gojuon_order: Mapped[int] = mapped_column(Integer)
    sell_check_disp: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class ItemETicketDatum(Base):
    __tablename__ = 'item_e_ticket_data'
    __table_args__ = (
        Index('item_e_ticket_data_0_exchange_number', 'exchange_number'),
        Index('item_e_ticket_data_0_ticket_id', 'ticket_id')
    )

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class KaiserAddTimesDatum(Base):
    __tablename__ = 'kaiser_add_times_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times: Mapped[int] = mapped_column(Integer)
    add_times_time: Mapped[str] = mapped_column(Text)
    duration: Mapped[int] = mapped_column(Integer)


class KaiserExterminationReward(Base):
    __tablename__ = 'kaiser_extermination_reward'

    extermination_reward_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class KaiserQuestDatum(Base):
    __tablename__ = 'kaiser_quest_data'

    kaiser_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    battle_start_story_id: Mapped[int] = mapped_column(Integer)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer)
    disappearance_story_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    restriction_group_id: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer)
    odds_group_id: Mapped[str] = mapped_column(Text)
    chest_id: Mapped[int] = mapped_column(Integer)
    extermination_reward_group: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    enemy_position_x: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    result_boss_position_y: Mapped[float] = mapped_column(Float)
    wave_bgm: Mapped[str] = mapped_column(Text)
    reward_gold_coefficient: Mapped[float] = mapped_column(Float)
    limited_mana: Mapped[int] = mapped_column(Integer)
    clear_story_id_1: Mapped[int] = mapped_column(Integer)
    clear_story_id_2: Mapped[int] = mapped_column(Integer)


class KaiserRestrictionGroup(Base):
    __tablename__ = 'kaiser_restriction_group'
    __table_args__ = (
        Index('kaiser_restriction_group_0_restriction_group_id', 'restriction_group_id'),
    )

    restriction_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class KaiserSchedule(Base):
    __tablename__ = 'kaiser_schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)
    story_id: Mapped[int] = mapped_column(Integer)
    close_story_condition_id: Mapped[int] = mapped_column(Integer)
    close_story_id: Mapped[int] = mapped_column(Integer)
    top_bgm: Mapped[str] = mapped_column(Text)
    top_bg: Mapped[str] = mapped_column(Text)
    after_bgm: Mapped[str] = mapped_column(Text)
    after_bg: Mapped[str] = mapped_column(Text)


class KaiserSpecialBattle(Base):
    __tablename__ = 'kaiser_special_battle'

    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommended_level: Mapped[int] = mapped_column(Integer)
    purpose_type: Mapped[int] = mapped_column(Integer)
    purpose_count: Mapped[int] = mapped_column(Integer)
    trigger_hp: Mapped[int] = mapped_column(Integer)
    story_id_mode_start: Mapped[int] = mapped_column(Integer)
    story_id_mode_end: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer)
    story_start_second: Mapped[float] = mapped_column(Float)
    action_start_second: Mapped[float] = mapped_column(Float)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer)
    start_idle_trigger: Mapped[int] = mapped_column(Integer)
    appear_time: Mapped[float] = mapped_column(Float)


class KmkNaviComment(Base):
    __tablename__ = 'kmk_navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)


class KmkReward(Base):
    __tablename__ = 'kmk_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kmk_score: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class LegionAddTimesDatum(Base):
    __tablename__ = 'legion_add_times_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times: Mapped[int] = mapped_column(Integer)
    add_times_time: Mapped[str] = mapped_column(Text)


class LegionBattleBonus(Base):
    __tablename__ = 'legion_battle_bonus'
    __table_args__ = (
        Index('legion_battle_bonus_0_type', 'type'),
        Index('legion_battle_bonus_0_type_1_legion_boss_id', 'type', 'legion_boss_id')
    )

    legion_battle_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    legion_boss_id: Mapped[int] = mapped_column(Integer)
    condition_hp: Mapped[str] = mapped_column(Text)
    legion_battle_effect_id: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class LegionBattleBonusEffect(Base):
    __tablename__ = 'legion_battle_bonus_effect'

    legion_battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    text_id: Mapped[int] = mapped_column(Integer)
    skill_id: Mapped[int] = mapped_column(Integer)
    target_type: Mapped[int] = mapped_column(Integer)


class LegionBossEnemySetting(Base):
    __tablename__ = 'legion_boss_enemy_setting'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_offset_x: Mapped[int] = mapped_column(Integer)
    detail_offset_y: Mapped[int] = mapped_column(Integer)
    detail_offset_scale: Mapped[float] = mapped_column(Float)


class LegionEffect(Base):
    __tablename__ = 'legion_effect'

    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_1: Mapped[int] = mapped_column(Integer)
    bonus_2: Mapped[int] = mapped_column(Integer)
    bonus_3: Mapped[int] = mapped_column(Integer)
    bonus_4: Mapped[int] = mapped_column(Integer)
    bonus_5: Mapped[int] = mapped_column(Integer)


class LegionEffectiveUnit(Base):
    __tablename__ = 'legion_effective_unit'
    __table_args__ = (
        Index('legion_effective_unit_0_legion_boss_id', 'legion_boss_id'),
    )

    legion_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id: Mapped[int] = mapped_column(Integer)
    support_effect_id: Mapped[int] = mapped_column(Integer)


class LegionExterminationReward(Base):
    __tablename__ = 'legion_extermination_reward'

    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class LegionMissionCategoryDatum(Base):
    __tablename__ = 'legion_mission_category_data'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)


class LegionMissionDatum(Base):
    __tablename__ = 'legion_mission_data'
    __table_args__ = (
        Index('legion_mission_data_0_category_id', 'category_id'),
    )

    legion_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer)
    disp_group: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    legion_boss_id: Mapped[int] = mapped_column(Integer)
    condition_value: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[str] = mapped_column(Text)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class LegionMissionRewardDatum(Base):
    __tablename__ = 'legion_mission_reward_data'
    __table_args__ = (
        Index('legion_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class LegionQuestDatum(Base):
    __tablename__ = 'legion_quest_data'
    __table_args__ = (
        Index('legion_quest_data_0_map_type', 'map_type'),
    )

    legion_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    battle_start_story_id: Mapped[int] = mapped_column(Integer)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer)
    disappearance_story_id: Mapped[int] = mapped_column(Integer)
    all_disappearance_story_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    max_raid_hp: Mapped[str] = mapped_column(Text)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer)
    expel_reward_group_id: Mapped[int] = mapped_column(Integer)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    enemy_position_x: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    result_boss_position_y: Mapped[float] = mapped_column(Float)
    wave_bgm: Mapped[str] = mapped_column(Text)
    clear_story_id_1: Mapped[int] = mapped_column(Integer)
    clear_story_id_2: Mapped[int] = mapped_column(Integer)
    bonus_max: Mapped[int] = mapped_column(Integer)


class LegionSchedule(Base):
    __tablename__ = 'legion_schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)
    story_id: Mapped[int] = mapped_column(Integer)
    close_story_condition_id: Mapped[int] = mapped_column(Integer)
    close_story_id: Mapped[int] = mapped_column(Integer)
    top_bgm: Mapped[str] = mapped_column(Text)
    top_bg: Mapped[str] = mapped_column(Text)


class LegionSpecialBattle(Base):
    __tablename__ = 'legion_special_battle'

    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer)
    purpose_count: Mapped[int] = mapped_column(Integer)
    trigger_hp: Mapped[int] = mapped_column(Integer)
    story_id_mode_start: Mapped[int] = mapped_column(Integer)
    story_id_mode_end: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer)
    story_start_second: Mapped[float] = mapped_column(Float)
    action_start_second: Mapped[float] = mapped_column(Float)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer)


class LoginBonusAdv(Base):
    __tablename__ = 'login_bonus_adv'
    __table_args__ = (
        Index('login_bonus_adv_0_login_bonus_id', 'login_bonus_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    count_key: Mapped[int] = mapped_column(Integer)
    adv_id: Mapped[int] = mapped_column(Integer)
    read_process_flag: Mapped[int] = mapped_column(Integer)


class LoginBonusDatum(Base):
    __tablename__ = 'login_bonus_data'

    login_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    login_bonus_type: Mapped[int] = mapped_column(Integer)
    count_num: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    bg_id: Mapped[int] = mapped_column(Integer)
    stamp_id: Mapped[int] = mapped_column(Integer)
    odds_group_id: Mapped[int] = mapped_column(Integer)
    adv_play_type: Mapped[int] = mapped_column(Integer)
    count_type: Mapped[int] = mapped_column(Integer)


class LoginBonusDetail(Base):
    __tablename__ = 'login_bonus_detail'
    __table_args__ = (
        Index('login_bonus_detail_0_login_bonus_id_1_count', 'login_bonus_id', 'count'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_id: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    bg_id: Mapped[int] = mapped_column(Integer)


class LoginBonusMessageDatum(Base):
    __tablename__ = 'login_bonus_message_data'
    __table_args__ = (
        Index('login_bonus_message_data_0_login_bonus_id', 'login_bonus_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    day_count: Mapped[int] = mapped_column(Integer)
    luck_pattern: Mapped[int] = mapped_column(Integer)
    rate: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    additional_type: Mapped[int] = mapped_column(Integer)
    additional_param: Mapped[str] = mapped_column(Text)


class LoveChara(Base):
    __tablename__ = 'love_chara'

    love_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_love: Mapped[int] = mapped_column(Integer)
    unlocked_class: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)


class LoveRankup(Base):
    __tablename__ = 'love_rankup'
    __table_args__ = (
        Index('love_rankup_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    love_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_unit_id: Mapped[int] = mapped_column(Integer)


class LsvDramaScript(Base):
    __tablename__ = 'lsv_drama_script'
    __table_args__ = (
        Index('lsv_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class LsvStoryDatum(Base):
    __tablename__ = 'lsv_story_data'
    __table_args__ = (
        Index('lsv_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    time_condition: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    read_event_story_id: Mapped[int] = mapped_column(Integer)
    read_condition: Mapped[int] = mapped_column(Integer)


class LsvStoryScript(Base):
    __tablename__ = 'lsv_story_script'
    __table_args__ = (
        Index('lsv_story_script_0_story_id', 'story_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class LtoLetterScript(Base):
    __tablename__ = 'lto_letter_script'
    __table_args__ = (
        Index('lto_letter_script_0_letter_id', 'letter_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    letter_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class LtoStoryDatum(Base):
    __tablename__ = 'lto_story_data'
    __table_args__ = (
        Index('lto_story_data_0_event_id', 'event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class Metamorphose(Base):
    __tablename__ = 'metamorphose'
    __table_args__ = (
        Index('metamorphose_0_type_id', 'type_id'),
    )

    type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value: Mapped[int] = mapped_column(Integer, primary_key=True)
    prefab_id: Mapped[int] = mapped_column(Integer)


class MhpDramaScript(Base):
    __tablename__ = 'mhp_drama_script'
    __table_args__ = (
        Index('mhp_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class MhpStoryDatum(Base):
    __tablename__ = 'mhp_story_data'
    __table_args__ = (
        Index('mhp_story_data_0_original_event_id', 'original_event_id'),
        Index('mhp_story_data_0_unit_id', 'unit_id')
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    unit_id: Mapped[int] = mapped_column(Integer)
    read_condition_time: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    read_condition: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class Minigame(Base):
    __tablename__ = 'minigame'
    __table_args__ = (
        Index('minigame_0_event_id', 'event_id'),
    )

    id: Mapped[int] = mapped_column(Integer)
    minigame_scheme_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    release_conditions_1: Mapped[int] = mapped_column(Integer)
    conditions_id_1: Mapped[int] = mapped_column(Integer)
    first_time_story_id: Mapped[int] = mapped_column(Integer)
    display_condition_type: Mapped[int] = mapped_column(Integer)
    display_condition_id: Mapped[int] = mapped_column(Integer)
    result_chat_condition_id: Mapped[int] = mapped_column(Integer)
    score_unit: Mapped[str] = mapped_column(Text)
    is_enabled_zero_score: Mapped[int] = mapped_column(Integer)


class MirokuBossDatum(Base):
    __tablename__ = 'miroku_boss_data'

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    limit_time: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    enemy_position_x: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer)
    enemy_size: Mapped[float] = mapped_column(Float)
    result_boss_position_y: Mapped[float] = mapped_column(Float)
    wave_bgm_sheet: Mapped[str] = mapped_column(Text)
    clear_story_id_1: Mapped[int] = mapped_column(Integer)
    clear_story_id_2: Mapped[int] = mapped_column(Integer)
    disappearance_story_id: Mapped[int] = mapped_column(Integer)


class MirokuSpecialBattle(Base):
    __tablename__ = 'miroku_special_battle'

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer)
    purpose_count: Mapped[int] = mapped_column(Integer)
    trigger_hp: Mapped[int] = mapped_column(Integer)
    story_id_mode_start: Mapped[int] = mapped_column(Integer)
    story_id_mode_end: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer)
    wave_bgm_que: Mapped[str] = mapped_column(Text)
    wave_bgm_block_id: Mapped[int] = mapped_column(Integer)
    story_start_block_id: Mapped[int] = mapped_column(Integer)
    story_start_after_block_id: Mapped[int] = mapped_column(Integer)
    story_end_block_id: Mapped[int] = mapped_column(Integer)
    story_end_after_block_id: Mapped[int] = mapped_column(Integer)
    story_start_second: Mapped[float] = mapped_column(Float)
    action_start_second: Mapped[float] = mapped_column(Float)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer)


class MissionCategoryIcon(Base):
    __tablename__ = 'mission_category_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_name: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(Text)


class MissionRewardDatum(Base):
    __tablename__ = 'mission_reward_data'
    __table_args__ = (
        Index('mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    lv_from: Mapped[int] = mapped_column(Integer)
    lv_to: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class MmeStoryDatum(Base):
    __tablename__ = 'mme_story_data'
    __table_args__ = (
        Index('mme_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    is_puzzle_piece: Mapped[int] = mapped_column(Integer)
    is_last: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class Movie(Base):
    __tablename__ = 'movie'
    __table_args__ = (
        Index('movie_0_story_id', 'story_id'),
    )

    movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer)
    bgm_id: Mapped[str] = mapped_column(Text)
    se_id: Mapped[str] = mapped_column(Text)
    my_page_flag: Mapped[int] = mapped_column(Integer)
    fade_loop_flag: Mapped[int] = mapped_column(Integer)
    bgm_volume_rate: Mapped[float] = mapped_column(Float)


class MusicContent(Base):
    __tablename__ = 'music_content'

    music_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    total_playing_time: Mapped[str] = mapped_column(Text)
    listen_start_time: Mapped[str] = mapped_column(Text)
    detail: Mapped[str] = mapped_column(Text)
    sheet_id: Mapped[str] = mapped_column(Text)
    cue_id: Mapped[str] = mapped_column(Text)


class MusicList(Base):
    __tablename__ = 'music_list'

    music_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    list_name: Mapped[str] = mapped_column(Text)
    font_size: Mapped[float] = mapped_column(Float)
    pre_shop_start: Mapped[str] = mapped_column(Text)
    shop_start: Mapped[str] = mapped_column(Text)
    shop_end: Mapped[str] = mapped_column(Text)
    story_id: Mapped[int] = mapped_column(Integer)
    cost_item_num: Mapped[int] = mapped_column(Integer)
    sort: Mapped[int] = mapped_column(Integer)
    kana: Mapped[str] = mapped_column(Text)
    ios_url: Mapped[str] = mapped_column(Text)
    android_url: Mapped[str] = mapped_column(Text)
    dmm_url: Mapped[str] = mapped_column(Text)


class MypageFrame(Base):
    __tablename__ = 'mypage_frame'
    __table_args__ = (
        Index('mypage_frame_0_group_id', 'group_id'),
    )

    frame_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)
    frame_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)


class MyprofileContent(Base):
    __tablename__ = 'myprofile_content'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    disp_order: Mapped[int] = mapped_column(Integer)


class NaviComment(Base):
    __tablename__ = 'navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    unlock_story_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)


class NopDramaDatum(Base):
    __tablename__ = 'nop_drama_data'
    __table_args__ = (
        Index('nop_drama_data_0_stage_id', 'stage_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stage_id: Mapped[int] = mapped_column(Integer)
    position_id_1: Mapped[int] = mapped_column(Integer)
    position_id_2: Mapped[int] = mapped_column(Integer)
    position_id_3: Mapped[int] = mapped_column(Integer)
    col_size_x: Mapped[int] = mapped_column(Integer)
    col_size_y: Mapped[int] = mapped_column(Integer)
    col_pos_y: Mapped[float] = mapped_column(Float)
    talk_pos_x: Mapped[float] = mapped_column(Float)
    talk_pos_y: Mapped[float] = mapped_column(Float)
    idle_drama_id: Mapped[int] = mapped_column(Integer)
    talk_drama_id: Mapped[int] = mapped_column(Integer)
    event_drama_id: Mapped[int] = mapped_column(Integer)
    create_back_drama_id: Mapped[int] = mapped_column(Integer)
    create_front_drama_id: Mapped[int] = mapped_column(Integer)
    sub_story_id: Mapped[int] = mapped_column(Integer)


class NopDramaScript(Base):
    __tablename__ = 'nop_drama_script'
    __table_args__ = (
        Index('nop_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class NotifDatum(Base):
    __tablename__ = 'notif_data'
    __table_args__ = (
        Index('notif_data_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    notif_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text)


class NyxDramaDatum(Base):
    __tablename__ = 'nyx_drama_data'

    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_phase: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    condition_unlocked_story_id: Mapped[int] = mapped_column(Integer)
    condition_locked_story_id: Mapped[int] = mapped_column(Integer)


class NyxDramaScript(Base):
    __tablename__ = 'nyx_drama_script'
    __table_args__ = (
        Index('nyx_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class NyxPhaseDatum(Base):
    __tablename__ = 'nyx_phase_data'

    story_phase: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase_title: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_quest_boss: Mapped[int] = mapped_column(Integer)


class NyxStoryDatum(Base):
    __tablename__ = 'nyx_story_data'
    __table_args__ = (
        Index('nyx_story_data_0_story_phase', 'story_phase'),
        Index('nyx_story_data_0_story_seq', 'story_seq')
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_seq: Mapped[int] = mapped_column(Integer)
    story_phase: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    read_condition_time: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_count: Mapped[int] = mapped_column(Integer)
    adv_flg: Mapped[int] = mapped_column(Integer)
    adv_id: Mapped[int] = mapped_column(Integer)


class NyxStoryScript(Base):
    __tablename__ = 'nyx_story_script'
    __table_args__ = (
        Index('nyx_story_script_0_story_id', 'story_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class OddsNameDatum(Base):
    __tablename__ = 'odds_name_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_file: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)
    icon_type: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class OmpDrama(Base):
    __tablename__ = 'omp_drama'
    __table_args__ = (
        Index('omp_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class OmpStoryDatum(Base):
    __tablename__ = 'omp_story_data'
    __table_args__ = (
        Index('omp_story_data_0_event_id', 'event_id'),
        Index('omp_story_data_0_story_seq', 'story_seq')
    )

    omp_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    story_seq: Mapped[int] = mapped_column(Integer)
    is_readable_on_result: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    sub_title: Mapped[str] = mapped_column(Text)


class PctComboCoefficient(Base):
    __tablename__ = 'pct_combo_coefficient'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    combo_min: Mapped[int] = mapped_column(Integer)
    combo_max: Mapped[int] = mapped_column(Integer)
    combo_coefficient: Mapped[int] = mapped_column(Integer)


class PctEvaluation(Base):
    __tablename__ = 'pct_evaluation'

    evaluation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evaluation_point: Mapped[int] = mapped_column(Integer)
    fever_point: Mapped[int] = mapped_column(Integer)
    meet_width: Mapped[int] = mapped_column(Integer)


class PctGamingMotion(Base):
    __tablename__ = 'pct_gaming_motion'

    motion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    perfect_count: Mapped[int] = mapped_column(Integer)
    good_count: Mapped[int] = mapped_column(Integer)
    nice_count: Mapped[int] = mapped_column(Integer)
    point: Mapped[int] = mapped_column(Integer)


class PctItempoint(Base):
    __tablename__ = 'pct_itempoint'
    __table_args__ = (
        Index('pct_itempoint_0_item_id', 'item_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer)
    pct_point_coefficient: Mapped[int] = mapped_column(Integer)


class PctResult(Base):
    __tablename__ = 'pct_result'
    __table_args__ = (
        Index('pct_result_0_character_id', 'character_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer)
    score_from: Mapped[int] = mapped_column(Integer)
    score_to: Mapped[int] = mapped_column(Integer)
    comment_id_1: Mapped[int] = mapped_column(Integer)
    comment_id_2: Mapped[int] = mapped_column(Integer)
    comment_id_3: Mapped[int] = mapped_column(Integer)
    comment_id_4: Mapped[int] = mapped_column(Integer)
    comment_id_5: Mapped[int] = mapped_column(Integer)


class PctReward(Base):
    __tablename__ = 'pct_reward'
    __table_args__ = (
        Index('pct_reward_0_pct_point_type', 'pct_point_type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pct_point_type: Mapped[int] = mapped_column(Integer)
    pct_point: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class PctSystem(Base):
    __tablename__ = 'pct_system'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pct_base_speed: Mapped[int] = mapped_column(Integer)
    fever_point_max: Mapped[int] = mapped_column(Integer)
    fever_time: Mapped[int] = mapped_column(Integer)
    fever_revention_time: Mapped[int] = mapped_column(Integer)
    pct_time: Mapped[int] = mapped_column(Integer)
    chara1: Mapped[int] = mapped_column(Integer)
    chara2: Mapped[int] = mapped_column(Integer)
    chara1_gauge_choice: Mapped[int] = mapped_column(Integer)
    chara2_gauge_choice: Mapped[int] = mapped_column(Integer)


class PctSystemFruits(Base):
    __tablename__ = 'pct_system_fruits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_time: Mapped[int] = mapped_column(Integer)
    appearance: Mapped[int] = mapped_column(Integer)
    bar_split: Mapped[int] = mapped_column(Integer)
    appearance_chara_odds: Mapped[int] = mapped_column(Integer)
    appearance_pattern: Mapped[str] = mapped_column(Text)
    wait_time: Mapped[int] = mapped_column(Integer)


class PctTapSpeed(Base):
    __tablename__ = 'pct_tap_speed'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    combo_count: Mapped[int] = mapped_column(Integer)
    speed_magnification: Mapped[int] = mapped_column(Integer)


class PkbBatterCondition(Base):
    __tablename__ = 'pkb_batter_condition'

    batter_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pkb_score: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    detail: Mapped[str] = mapped_column(Text)
    meet: Mapped[int] = mapped_column(Integer)
    critical: Mapped[int] = mapped_column(Integer)
    power: Mapped[int] = mapped_column(Integer)
    ability_name: Mapped[str] = mapped_column(Text)
    ability_detail: Mapped[str] = mapped_column(Text)
    is_playable: Mapped[int] = mapped_column(Integer)


class PkbDrama(Base):
    __tablename__ = 'pkb_drama'
    __table_args__ = (
        Index('pkb_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class PkbDramaDatum(Base):
    __tablename__ = 'pkb_drama_data'

    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_pitcher_id_1: Mapped[int] = mapped_column(Integer)
    condition_pitcher_id_2: Mapped[int] = mapped_column(Integer)
    condition_batter_id_1: Mapped[int] = mapped_column(Integer)
    condition_batter_id_2: Mapped[int] = mapped_column(Integer)


class PkbNaviComment(Base):
    __tablename__ = 'pkb_navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)


class PkbPitcherBallType(Base):
    __tablename__ = 'pkb_pitcher_ball_type'
    __table_args__ = (
        Index('pkb_pitcher_ball_type_0_pitcher_id', 'pitcher_id'),
    )

    pitcher_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ball_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    ball_type_name: Mapped[str] = mapped_column(Text)


class PkbReward(Base):
    __tablename__ = 'pkb_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pkb_score: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class PositionSetting(Base):
    __tablename__ = 'position_setting'

    position_setting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    front: Mapped[int] = mapped_column(Integer)
    middle: Mapped[int] = mapped_column(Integer)


class PrizegachaDatum(Base):
    __tablename__ = 'prizegacha_data'

    prizegacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prize_memory_id_1: Mapped[int] = mapped_column(Integer)
    prize_memory_id_2: Mapped[int] = mapped_column(Integer)
    prize_memory_id_3: Mapped[int] = mapped_column(Integer)
    prize_memory_id_4: Mapped[int] = mapped_column(Integer)
    prize_memory_id_5: Mapped[int] = mapped_column(Integer)
    prize_memory_id_6: Mapped[int] = mapped_column(Integer)
    prize_memory_id_7: Mapped[int] = mapped_column(Integer)
    prize_memory_id_8: Mapped[int] = mapped_column(Integer)
    prize_memory_id_9: Mapped[int] = mapped_column(Integer)
    prize_memory_id_10: Mapped[int] = mapped_column(Integer)
    prize_memory_id_11: Mapped[int] = mapped_column(Integer)
    prize_memory_id_12: Mapped[int] = mapped_column(Integer)
    prize_memory_id_13: Mapped[int] = mapped_column(Integer)
    prize_memory_id_14: Mapped[int] = mapped_column(Integer)
    prize_memory_id_15: Mapped[int] = mapped_column(Integer)
    prize_memory_id_16: Mapped[int] = mapped_column(Integer)
    prize_memory_id_17: Mapped[int] = mapped_column(Integer)
    prize_memory_id_18: Mapped[int] = mapped_column(Integer)
    prize_memory_id_19: Mapped[int] = mapped_column(Integer)
    prize_memory_id_20: Mapped[int] = mapped_column(Integer)
    gacha_prize1: Mapped[int] = mapped_column(Integer)
    gacha_prize10: Mapped[int] = mapped_column(Integer)
    prize_fixed_compensation: Mapped[int] = mapped_column(Integer)
    prize_fixed_compensation_quantity: Mapped[int] = mapped_column(Integer)
    rarity_odds: Mapped[int] = mapped_column(Integer)
    disp_prize_fixed_compensation: Mapped[int] = mapped_column(Integer)


class PrizegachaSpDatum(Base):
    __tablename__ = 'prizegacha_sp_data'
    __table_args__ = (
        Index('prizegacha_sp_data_0_gacha_id', 'gacha_id'),
    )

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_rarity: Mapped[int] = mapped_column(Integer)


class PrizegachaSpDetail(Base):
    __tablename__ = 'prizegacha_sp_detail'

    disp_rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)


class ProfileFrame(Base):
    __tablename__ = 'profile_frame'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    disp_order: Mapped[int] = mapped_column(Integer)


class PromotionBonus(Base):
    __tablename__ = 'promotion_bonus'
    __table_args__ = (
        Index('promotion_bonus_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)


class PsyDrama(Base):
    __tablename__ = 'psy_drama'

    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_total_eat: Mapped[int] = mapped_column(Integer)
    condition_chara_type: Mapped[int] = mapped_column(Integer)
    condition_time: Mapped[str] = mapped_column(Text)
    condition_psy_product_1: Mapped[int] = mapped_column(Integer)
    condition_psy_product_2: Mapped[int] = mapped_column(Integer)
    condition_psy_product_3: Mapped[int] = mapped_column(Integer)
    condition_psy_product_4: Mapped[int] = mapped_column(Integer)
    condition_psy_product_5: Mapped[int] = mapped_column(Integer)
    release_psy_product_id_1: Mapped[int] = mapped_column(Integer)
    release_psy_product_id_2: Mapped[int] = mapped_column(Integer)
    release_psy_product_id_3: Mapped[int] = mapped_column(Integer)
    release_psy_product_id_4: Mapped[int] = mapped_column(Integer)
    release_psy_product_id_5: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)


class PsyDramaScript(Base):
    __tablename__ = 'psy_drama_script'
    __table_args__ = (
        Index('psy_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class PsyNote(Base):
    __tablename__ = 'psy_note'

    psy_product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_flavor_1: Mapped[int] = mapped_column(Integer)
    condition_flavor_2: Mapped[int] = mapped_column(Integer)
    psy_product_name: Mapped[str] = mapped_column(Text)
    flavor_1: Mapped[str] = mapped_column(Text)
    flavor_2: Mapped[str] = mapped_column(Text)
    flavor_3: Mapped[str] = mapped_column(Text)
    disp_order: Mapped[int] = mapped_column(Integer)
    init_flg: Mapped[int] = mapped_column(Integer)


class PsyReward(Base):
    __tablename__ = 'psy_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class QuestAnnihilation(Base):
    __tablename__ = 'quest_annihilation'

    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_type: Mapped[int] = mapped_column(Integer)
    quest_effect_position: Mapped[int] = mapped_column(Integer)
    se_cue_name: Mapped[str] = mapped_column(Text)


class QuestAreaDatum(Base):
    __tablename__ = 'quest_area_data'
    __table_args__ = (
        Index('quest_area_data_0_map_type', 'map_type'),
    )

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_name: Mapped[str] = mapped_column(Text)
    area_display_name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class QuestConditionDatum(Base):
    __tablename__ = 'quest_condition_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer)
    condition_quest_id_3: Mapped[int] = mapped_column(Integer)
    condition_quest_id_4: Mapped[int] = mapped_column(Integer)
    condition_quest_id_5: Mapped[int] = mapped_column(Integer)
    release_quest_id_1: Mapped[int] = mapped_column(Integer)
    release_quest_id_2: Mapped[int] = mapped_column(Integer)
    release_quest_id_3: Mapped[int] = mapped_column(Integer)
    release_quest_id_4: Mapped[int] = mapped_column(Integer)
    release_quest_id_5: Mapped[int] = mapped_column(Integer)


class QuestDatum(Base):
    __tablename__ = 'quest_data'
    __table_args__ = (
        Index('quest_data_0_area_id', 'area_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    limit_team_level: Mapped[int] = mapped_column(Integer)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    unit_exp: Mapped[int] = mapped_column(Integer)
    love: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    daily_limit: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    rank_reward_group: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer)
    enemy_image_1: Mapped[int] = mapped_column(Integer)
    enemy_image_2: Mapped[int] = mapped_column(Integer)
    enemy_image_3: Mapped[int] = mapped_column(Integer)
    enemy_image_4: Mapped[int] = mapped_column(Integer)
    enemy_image_5: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    lv_reward_flag: Mapped[int] = mapped_column(Integer)
    add_treasure_num: Mapped[int] = mapped_column(Integer)


class QuestDefeatNotice(Base):
    __tablename__ = 'quest_defeat_notice'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_id: Mapped[int] = mapped_column(Integer)
    required_team_level: Mapped[int] = mapped_column(Integer)
    required_quest_id: Mapped[int] = mapped_column(Integer)


class QuestRewardDatum(Base):
    __tablename__ = 'quest_reward_data'

    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class Rarity6QuestDatum(Base):
    __tablename__ = 'rarity_6_quest_data'
    __table_args__ = (
        Index('rarity_6_quest_data_0_rarity_6_quest_id', 'rarity_6_quest_id'),
    )

    rarity_6_quest_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text)
    limit_time: Mapped[int] = mapped_column(Integer)
    recommended_level: Mapped[int] = mapped_column(Integer)
    reward_group_id: Mapped[int] = mapped_column(Integer)
    treasure_type: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    enemy_size_2: Mapped[float] = mapped_column(Float)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    enemy_size_3: Mapped[float] = mapped_column(Float)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    enemy_size_4: Mapped[float] = mapped_column(Float)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    enemy_size_5: Mapped[float] = mapped_column(Float)
    wave_bgm: Mapped[str] = mapped_column(Text)


class RecoverStamina(Base):
    __tablename__ = 'recover_stamina'

    count: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer)


class RedeemStaticPriceGroup(Base):
    __tablename__ = 'redeem_static_price_group'

    condition_category: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer)


class RedeemUnit(Base):
    __tablename__ = 'redeem_unit'
    __table_args__ = (
        Index('redeem_unit_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    slot_id: Mapped[int] = mapped_column(Integer)
    condition_category: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    consume_num: Mapped[str] = mapped_column(Text)


class RedeemUnitBg(Base):
    __tablename__ = 'redeem_unit_bg'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer)


class ResistDatum(Base):
    __tablename__ = 'resist_data'

    resist_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ailment_1: Mapped[int] = mapped_column(Integer)
    ailment_2: Mapped[int] = mapped_column(Integer)
    ailment_3: Mapped[int] = mapped_column(Integer)
    ailment_4: Mapped[int] = mapped_column(Integer)
    ailment_5: Mapped[int] = mapped_column(Integer)
    ailment_6: Mapped[int] = mapped_column(Integer)
    ailment_7: Mapped[int] = mapped_column(Integer)
    ailment_8: Mapped[int] = mapped_column(Integer)
    ailment_9: Mapped[int] = mapped_column(Integer)
    ailment_10: Mapped[int] = mapped_column(Integer)
    ailment_11: Mapped[int] = mapped_column(Integer)
    ailment_12: Mapped[int] = mapped_column(Integer)
    ailment_13: Mapped[int] = mapped_column(Integer)
    ailment_14: Mapped[int] = mapped_column(Integer)
    ailment_15: Mapped[int] = mapped_column(Integer)
    ailment_16: Mapped[int] = mapped_column(Integer)
    ailment_17: Mapped[int] = mapped_column(Integer)
    ailment_18: Mapped[int] = mapped_column(Integer)
    ailment_19: Mapped[int] = mapped_column(Integer)
    ailment_20: Mapped[int] = mapped_column(Integer)
    ailment_21: Mapped[int] = mapped_column(Integer)
    ailment_22: Mapped[int] = mapped_column(Integer)
    ailment_23: Mapped[int] = mapped_column(Integer)
    ailment_24: Mapped[int] = mapped_column(Integer)
    ailment_25: Mapped[int] = mapped_column(Integer)
    ailment_26: Mapped[int] = mapped_column(Integer)
    ailment_27: Mapped[int] = mapped_column(Integer)
    ailment_28: Mapped[int] = mapped_column(Integer)
    ailment_29: Mapped[int] = mapped_column(Integer)
    ailment_30: Mapped[int] = mapped_column(Integer)
    ailment_31: Mapped[int] = mapped_column(Integer)
    ailment_32: Mapped[int] = mapped_column(Integer)
    ailment_33: Mapped[int] = mapped_column(Integer)
    ailment_34: Mapped[int] = mapped_column(Integer)
    ailment_35: Mapped[int] = mapped_column(Integer)
    ailment_36: Mapped[int] = mapped_column(Integer)
    ailment_37: Mapped[int] = mapped_column(Integer)
    ailment_38: Mapped[int] = mapped_column(Integer)
    ailment_39: Mapped[int] = mapped_column(Integer)
    ailment_40: Mapped[int] = mapped_column(Integer)
    ailment_41: Mapped[int] = mapped_column(Integer)
    ailment_42: Mapped[int] = mapped_column(Integer)
    ailment_43: Mapped[int] = mapped_column(Integer)
    ailment_44: Mapped[int] = mapped_column(Integer)
    ailment_45: Mapped[int] = mapped_column(Integer)
    ailment_46: Mapped[int] = mapped_column(Integer)
    ailment_47: Mapped[int] = mapped_column(Integer)
    ailment_48: Mapped[int] = mapped_column(Integer)
    ailment_49: Mapped[int] = mapped_column(Integer)
    ailment_50: Mapped[int] = mapped_column(Integer)


class ResistVariationDatum(Base):
    __tablename__ = 'resist_variation_data'

    resist_variation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_1: Mapped[int] = mapped_column(Integer)
    value_2: Mapped[int] = mapped_column(Integer)
    value_3: Mapped[int] = mapped_column(Integer)
    value_4: Mapped[int] = mapped_column(Integer)


class ReturnSpecialfesBanner(Base):
    __tablename__ = 'return_specialfes_banner'

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banner_id_1: Mapped[int] = mapped_column(Integer)
    banner_id_2: Mapped[int] = mapped_column(Integer)
    banner_id_3: Mapped[int] = mapped_column(Integer)
    banner_id_4: Mapped[int] = mapped_column(Integer)
    banner_id_5: Mapped[int] = mapped_column(Integer)
    banner_id_6: Mapped[int] = mapped_column(Integer)
    banner_id_7: Mapped[int] = mapped_column(Integer)
    banner_id_8: Mapped[int] = mapped_column(Integer)
    banner_id_9: Mapped[int] = mapped_column(Integer)
    banner_id_10: Mapped[int] = mapped_column(Integer)


class RewardCollectGuide(Base):
    __tablename__ = 'reward_collect_guide'

    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id_1: Mapped[int] = mapped_column(Integer)
    quest_id_2: Mapped[int] = mapped_column(Integer)
    quest_id_3: Mapped[int] = mapped_column(Integer)
    quest_id_4: Mapped[int] = mapped_column(Integer)
    quest_id_5: Mapped[int] = mapped_column(Integer)
    quest_id_6: Mapped[int] = mapped_column(Integer)
    quest_id_7: Mapped[int] = mapped_column(Integer)
    quest_id_8: Mapped[int] = mapped_column(Integer)
    quest_id_9: Mapped[int] = mapped_column(Integer)
    quest_id_10: Mapped[int] = mapped_column(Integer)
    system_id_1: Mapped[int] = mapped_column(Integer)
    system_id_2: Mapped[int] = mapped_column(Integer)
    system_id_3: Mapped[int] = mapped_column(Integer)
    system_id_4: Mapped[int] = mapped_column(Integer)
    system_id_5: Mapped[int] = mapped_column(Integer)


class RoomChange(Base):
    __tablename__ = 'room_change'

    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_id: Mapped[int] = mapped_column(Integer)
    change_start: Mapped[str] = mapped_column(Text)
    change_end: Mapped[str] = mapped_column(Text)


class RoomCharacterPersonality(Base):
    __tablename__ = 'room_character_personality'

    character_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    personality_id: Mapped[int] = mapped_column(Integer)


class RoomCharacterSkinColor(Base):
    __tablename__ = 'room_character_skin_color'

    character_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skin_color_id: Mapped[int] = mapped_column(Integer)


class RoomChatFormation(Base):
    __tablename__ = 'room_chat_formation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_1_x: Mapped[int] = mapped_column(Integer)
    unit_1_y: Mapped[int] = mapped_column(Integer)
    unit_1_dir: Mapped[int] = mapped_column(Integer)
    unit_2_x: Mapped[int] = mapped_column(Integer)
    unit_2_y: Mapped[int] = mapped_column(Integer)
    unit_2_dir: Mapped[int] = mapped_column(Integer)
    unit_num: Mapped[int] = mapped_column(Integer)
    unit_3_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_dir: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_dir: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_dir: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id1: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id2: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id3: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id4: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id5: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id1: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id2: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id3: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id4: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id5: Mapped[Optional[int]] = mapped_column(Integer)


class RoomChatInfo(Base):
    __tablename__ = 'room_chat_info'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    formation_id: Mapped[int] = mapped_column(Integer)
    scenario_id: Mapped[int] = mapped_column(Integer)


class RoomChatScenario(Base):
    __tablename__ = 'room_chat_scenario'
    __table_args__ = (
        Index('room_chat_scenario_0_id', 'id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_pos_no: Mapped[int] = mapped_column(Integer)
    delay: Mapped[int] = mapped_column(Integer)
    affect_type: Mapped[int] = mapped_column(Integer)
    anime_id: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)


class RoomEffect(Base):
    __tablename__ = 'room_effect'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_get: Mapped[int] = mapped_column(Integer)
    jukebox: Mapped[int] = mapped_column(Integer)
    nebbia: Mapped[int] = mapped_column(Integer)
    arcade: Mapped[int] = mapped_column(Integer)
    vegetable: Mapped[int] = mapped_column(Integer)
    poster: Mapped[int] = mapped_column(Integer)
    stock: Mapped[int] = mapped_column(Integer)


class RoomEffectRewardGet(Base):
    __tablename__ = 'room_effect_reward_get'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    max_count: Mapped[int] = mapped_column(Integer)
    inc_step: Mapped[int] = mapped_column(Integer)
    interval_second: Mapped[int] = mapped_column(Integer)
    stock_min_step: Mapped[str] = mapped_column(Text)
    stock_mid_step: Mapped[str] = mapped_column(Text)


class RoomEmotionIcon(Base):
    __tablename__ = 'room_emotion_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enable_auto: Mapped[int] = mapped_column(Integer)
    enable_tap: Mapped[int] = mapped_column(Integer)


class RoomExclusiveCondition(Base):
    __tablename__ = 'room_exclusive_condition'
    __table_args__ = (
        Index('room_exclusive_condition_0_room_item_id', 'room_item_id'),
        Index('room_exclusive_condition_0_unit_id', 'unit_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    room_item_id: Mapped[int] = mapped_column(Integer)
    notification: Mapped[str] = mapped_column(Text)


class RoomItem(Base):
    __tablename__ = 'room_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_type: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    max_level: Mapped[int] = mapped_column(Integer)
    enable_remove: Mapped[int] = mapped_column(Integer)
    max_possession_num: Mapped[int] = mapped_column(Integer)
    effect_id_1: Mapped[int] = mapped_column(Integer)
    shop_start: Mapped[str] = mapped_column(Text)
    shop_end: Mapped[str] = mapped_column(Text)
    shop_new_disp_end: Mapped[str] = mapped_column(Text)
    cost_item_num: Mapped[int] = mapped_column(Integer)
    shop_open_type: Mapped[int] = mapped_column(Integer)
    shop_open_id: Mapped[int] = mapped_column(Integer)
    shop_open_value: Mapped[int] = mapped_column(Integer)
    sold_price: Mapped[int] = mapped_column(Integer)
    sort: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    category_action_type: Mapped[int] = mapped_column(Integer)


class RoomItemAnnouncement(Base):
    __tablename__ = 'room_item_announcement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    announcement_start: Mapped[str] = mapped_column(Text)
    announcement_end: Mapped[str] = mapped_column(Text)
    announcement_text: Mapped[str] = mapped_column(Text)


class RoomItemDetail(Base):
    __tablename__ = 'room_item_detail'
    __table_args__ = (
        Index('room_item_detail_0_lvup_trigger_type_1_lvup_trigger_id', 'lvup_trigger_type', 'lvup_trigger_id'),
        Index('room_item_detail_0_lvup_trigger_type_2_1_lvup_trigger_id_2', 'lvup_trigger_type_2', 'lvup_trigger_id_2')
    )

    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_detail: Mapped[str] = mapped_column(Text)
    lvup_trigger_type: Mapped[int] = mapped_column(Integer)
    lvup_trigger_id: Mapped[int] = mapped_column(Integer)
    lvup_trigger_value: Mapped[int] = mapped_column(Integer)
    lvup_trigger_type_2: Mapped[int] = mapped_column(Integer)
    lvup_trigger_id_2: Mapped[int] = mapped_column(Integer)
    lvup_trigger_value_2: Mapped[int] = mapped_column(Integer)
    lvup_item1_type: Mapped[int] = mapped_column(Integer)
    lvup_item1_id: Mapped[int] = mapped_column(Integer)
    lvup_item1_num: Mapped[int] = mapped_column(Integer)
    lvup_time: Mapped[int] = mapped_column(Integer)


class RoomItemGetAnnouncement(Base):
    __tablename__ = 'room_item_get_announcement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_item_id: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[str] = mapped_column(Text)
    end_date: Mapped[str] = mapped_column(Text)
    get_date: Mapped[str] = mapped_column(Text)
    room_announcement_name: Mapped[str] = mapped_column(Text)


class RoomReleaseDatum(Base):
    __tablename__ = 'room_release_data'

    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)


class RoomSetup(Base):
    __tablename__ = 'room_setup'

    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grid_height: Mapped[int] = mapped_column(Integer)
    grid_width: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)


class RoomSkinColor(Base):
    __tablename__ = 'room_skin_color'

    skin_color_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    color_red: Mapped[int] = mapped_column(Integer)
    color_green: Mapped[int] = mapped_column(Integer)
    color_blue: Mapped[int] = mapped_column(Integer)


class RoomUnitComments(Base):
    __tablename__ = 'room_unit_comments'
    __table_args__ = (
        Index('room_unit_comments_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trigger: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beloved_step: Mapped[int] = mapped_column(Integer)
    time: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    insert_word_type: Mapped[int] = mapped_column(Integer)


class SdNaviComment(Base):
    __tablename__ = 'sd_navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    motion_type: Mapped[int] = mapped_column(Integer)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)


class SeasonPack(Base):
    __tablename__ = 'season_pack'
    __table_args__ = (
        Index('season_pack_0_mission_id', 'mission_id'),
        Index('season_pack_0_pack_type', 'pack_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    receive_text: Mapped[str] = mapped_column(Text)
    after_text: Mapped[str] = mapped_column(Text)
    gift_message_id: Mapped[int] = mapped_column(Integer)
    term: Mapped[int] = mapped_column(Integer)
    repurchase_day: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)
    system_id_1: Mapped[int] = mapped_column(Integer)
    add_num_1: Mapped[int] = mapped_column(Integer)
    item_record_id: Mapped[int] = mapped_column(Integer)
    condition_flg: Mapped[int] = mapped_column(Integer)
    reward_rate_1: Mapped[int] = mapped_column(Integer)
    pack_type: Mapped[int] = mapped_column(Integer)


class SeasonpassFoundation(Base):
    __tablename__ = 'seasonpass_foundation'

    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    key_jewel_id: Mapped[int] = mapped_column(Integer)
    advance_jewel_id: Mapped[int] = mapped_column(Integer)
    final_jewel_id: Mapped[int] = mapped_column(Integer)
    extra_level: Mapped[int] = mapped_column(Integer)
    per_level_point: Mapped[int] = mapped_column(Integer)
    level_max: Mapped[int] = mapped_column(Integer)
    weekly_point: Mapped[int] = mapped_column(Integer)
    level_price: Mapped[int] = mapped_column(Integer)
    point_change_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    proportion: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    limit_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class SeasonpassLevelReward(Base):
    __tablename__ = 'seasonpass_level_reward'

    level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    degree: Mapped[int] = mapped_column(Integer)
    free_reward_type: Mapped[int] = mapped_column(Integer)
    free_reward_id: Mapped[int] = mapped_column(Integer)
    free_reward_num: Mapped[int] = mapped_column(Integer)
    charge_reward_type_1: Mapped[int] = mapped_column(Integer)
    charge_reward_id_1: Mapped[int] = mapped_column(Integer)
    charge_reward_num_1: Mapped[int] = mapped_column(Integer)
    charge_reward_type_2: Mapped[int] = mapped_column(Integer)
    charge_reward_id_2: Mapped[int] = mapped_column(Integer)
    charge_reward_num_2: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)


class SeasonpassMissionDatum(Base):
    __tablename__ = 'seasonpass_mission_data'

    seasonpass_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_type: Mapped[int] = mapped_column(Integer)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class SeasonpassMissionRewardDatum(Base):
    __tablename__ = 'seasonpass_mission_reward_data'
    __table_args__ = (
        Index('seasonpass_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class SecretDungeonEmblemMission(Base):
    __tablename__ = 'secret_dungeon_emblem_mission'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    mission_description: Mapped[str] = mapped_column(Text)
    emblem_description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_value_2: Mapped[int] = mapped_column(Integer)
    condition_value_3: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[str] = mapped_column(Text)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    dungeon_area_id: Mapped[int] = mapped_column(Integer)
    visible_flag: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class SecretDungeonEmblemReward(Base):
    __tablename__ = 'secret_dungeon_emblem_reward'
    __table_args__ = (
        Index('secret_dungeon_emblem_reward_0_mission_reward_id', 'mission_reward_id'),
        Index('secret_dungeon_emblem_reward_0_reward_id', 'reward_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    icon_type: Mapped[int] = mapped_column(Integer)


class SecretDungeonEnemyInfo(Base):
    __tablename__ = 'secret_dungeon_enemy_info'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    floor_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_name: Mapped[str] = mapped_column(Text)


class SecretDungeonFloorReward(Base):
    __tablename__ = 'secret_dungeon_floor_reward'
    __table_args__ = (
        Index('secret_dungeon_floor_reward_0_dungeon_area_id', 'dungeon_area_id'),
    )

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clear_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    clear_effect_flag: Mapped[int] = mapped_column(Integer)
    icon_type: Mapped[int] = mapped_column(Integer)


class SecretDungeonFloorSetting(Base):
    __tablename__ = 'secret_dungeon_floor_setting'
    __table_args__ = (
        Index('secret_dungeon_floor_setting_0_quest_id', 'quest_id'),
        Index('secret_dungeon_floor_setting_0_quest_id_1_mode', 'quest_id', 'mode')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer)
    enemy_identify: Mapped[int] = mapped_column(Integer)
    mode: Mapped[int] = mapped_column(Integer)
    enemy_id: Mapped[int] = mapped_column(Integer)
    floor_position_x: Mapped[float] = mapped_column(Float)
    floor_position_y: Mapped[float] = mapped_column(Float)
    floor_scale: Mapped[float] = mapped_column(Float)
    disp_order: Mapped[int] = mapped_column(Integer)


class SecretDungeonQuestDatum(Base):
    __tablename__ = 'secret_dungeon_quest_data'
    __table_args__ = (
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_difficulty', 'dungeon_area_id', 'difficulty'),
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num')
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_area_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    quest_type: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer)
    energy_reset_flag: Mapped[int] = mapped_column(Integer)
    fixed_start_tp_rate: Mapped[int] = mapped_column(Integer)
    emax: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_image_6: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    reward_coin: Mapped[int] = mapped_column(Integer)
    reward_csc: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    odds_group_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    dungeon_quest_detail_monster_size: Mapped[float] = mapped_column(Float)
    quest_detail_monster_scale_1: Mapped[float] = mapped_column(Float)
    quest_detail_monster_scale_2: Mapped[float] = mapped_column(Float)
    quest_detail_monster_scale_3: Mapped[float] = mapped_column(Float)
    quest_detail_monster_scale_4: Mapped[float] = mapped_column(Float)
    quest_detail_monster_scale_5: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_1: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_2: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_3: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_4: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_position_x_5: Mapped[float] = mapped_column(Float)
    dungeon_quest_detail_monster_height: Mapped[float] = mapped_column(Float)
    multi_target_effect_time: Mapped[float] = mapped_column(Float)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)


class SecretDungeonSchedule(Base):
    __tablename__ = 'secret_dungeon_schedule'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)


class SekaiAddTimesDatum(Base):
    __tablename__ = 'sekai_add_times_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sekai_id: Mapped[int] = mapped_column(Integer)
    add_times: Mapped[int] = mapped_column(Integer)
    add_times_limit: Mapped[int] = mapped_column(Integer)
    add_times_time: Mapped[str] = mapped_column(Text)
    duration: Mapped[int] = mapped_column(Integer)


class SekaiBossDamageRankReward(Base):
    __tablename__ = 'sekai_boss_damage_rank_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    damage_rank_id: Mapped[int] = mapped_column(Integer)
    ranking_from: Mapped[int] = mapped_column(Integer)
    ranking_to: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class SekaiBossFixReward(Base):
    __tablename__ = 'sekai_boss_fix_reward'

    sekai_id: Mapped[int] = mapped_column(Integer)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_total_damage: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    reward_type_6: Mapped[int] = mapped_column(Integer)
    reward_id_6: Mapped[int] = mapped_column(Integer)
    reward_num_6: Mapped[int] = mapped_column(Integer)
    reward_type_7: Mapped[int] = mapped_column(Integer)
    reward_id_7: Mapped[int] = mapped_column(Integer)
    reward_num_7: Mapped[int] = mapped_column(Integer)
    reward_type_8: Mapped[int] = mapped_column(Integer)
    reward_id_8: Mapped[int] = mapped_column(Integer)
    reward_num_8: Mapped[int] = mapped_column(Integer)
    reward_type_9: Mapped[int] = mapped_column(Integer)
    reward_id_9: Mapped[int] = mapped_column(Integer)
    reward_num_9: Mapped[int] = mapped_column(Integer)
    reward_type_10: Mapped[int] = mapped_column(Integer)
    reward_id_10: Mapped[int] = mapped_column(Integer)
    reward_num_10: Mapped[int] = mapped_column(Integer)


class SekaiBossMode(Base):
    __tablename__ = 'sekai_boss_mode'

    sekai_boss_mode_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sekai_enemy_id: Mapped[int] = mapped_column(Integer)
    sekai_enemy_level: Mapped[str] = mapped_column(Text)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    quest_detail_monster_size: Mapped[float] = mapped_column(Float)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    reward_gold_coefficient: Mapped[int] = mapped_column(Integer)
    limited_mana: Mapped[int] = mapped_column(Integer)
    score_coefficient: Mapped[int] = mapped_column(Integer)


class SekaiEnemyParameter(Base):
    __tablename__ = 'sekai_enemy_parameter'

    sekai_enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[str] = mapped_column(Text)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer)
    resist_status_id: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)


class SekaiSchedule(Base):
    __tablename__ = 'sekai_schedule'

    sekai_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_sekai_id: Mapped[int] = mapped_column(Integer)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer)
    damage_rank_id: Mapped[int] = mapped_column(Integer)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    end_losstime: Mapped[str] = mapped_column(Text)
    result_end: Mapped[str] = mapped_column(Text)


class SekaiTopDatum(Base):
    __tablename__ = 'sekai_top_data'
    __table_args__ = (
        Index('sekai_top_data_0_sekai_id', 'sekai_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sekai_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    top_bg: Mapped[int] = mapped_column(Integer)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    scale_ratio: Mapped[float] = mapped_column(Float)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    boss_mode: Mapped[int] = mapped_column(Integer)
    sekai_boss_mode_id: Mapped[int] = mapped_column(Integer)
    boss_hp_from: Mapped[str] = mapped_column(Text)
    boss_hp_to: Mapped[str] = mapped_column(Text)
    boss_time_from: Mapped[str] = mapped_column(Text)
    boss_time_to: Mapped[str] = mapped_column(Text)
    duration: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer)


class SekaiTopStoryDatum(Base):
    __tablename__ = 'sekai_top_story_data'
    __table_args__ = (
        Index('sekai_top_story_data_0_sekai_id', 'sekai_id'),
    )

    sekai_id: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_time_from: Mapped[str] = mapped_column(Text)
    boss_time_to: Mapped[str] = mapped_column(Text)


class SekaiUnlockStoryCondition(Base):
    __tablename__ = 'sekai_unlock_story_condition'

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sekai_id: Mapped[int] = mapped_column(Integer)
    condition_entry: Mapped[int] = mapped_column(Integer)
    condition_fix_reward_id: Mapped[int] = mapped_column(Integer)
    condition_time: Mapped[str] = mapped_column(Text)


class SerialCodeDatum(Base):
    __tablename__ = 'serial_code_data'

    serial_campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    serial_group_id: Mapped[int] = mapped_column(Integer)
    campaign_name: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    limit_num: Mapped[int] = mapped_column(Integer)
    count_share_id: Mapped[int] = mapped_column(Integer)


class SerialGroupDatum(Base):
    __tablename__ = 'serial_group_data'

    serial_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_name: Mapped[str] = mapped_column(Text)
    serial_campaign_id_1: Mapped[int] = mapped_column(Integer)
    serial_campaign_id_2: Mapped[int] = mapped_column(Integer)
    serial_campaign_id_3: Mapped[int] = mapped_column(Integer)
    serial_campaign_id_4: Mapped[int] = mapped_column(Integer)
    serial_campaign_id_5: Mapped[int] = mapped_column(Integer)
    serial_campaign_id_6: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class SeriesUnlockCondition(Base):
    __tablename__ = 'series_unlock_condition'

    sequel_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id_1: Mapped[int] = mapped_column(Integer)
    condition_story_id_2: Mapped[int] = mapped_column(Integer)
    condition_event_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)


class ShioriBattleMissionDatum(Base):
    __tablename__ = 'shiori_battle_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriBoss(Base):
    __tablename__ = 'shiori_boss'
    __table_args__ = (
        Index('shiori_boss_0_event_id', 'event_id'),
        Index('shiori_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
        Index('shiori_boss_0_wave_group_id_1', 'wave_group_id_1')
    )

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    boss_position_x: Mapped[int] = mapped_column(Integer)
    boss_position_y: Mapped[int] = mapped_column(Integer)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    icon_display_scale: Mapped[float] = mapped_column(Float)
    icon_collider_scale: Mapped[float] = mapped_column(Float)
    limit_time: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer)
    detail_bg_id: Mapped[int] = mapped_column(Integer)
    detail_bg_position: Mapped[int] = mapped_column(Integer)
    detail_boss_bg_size: Mapped[float] = mapped_column(Float)
    detail_boss_bg_height: Mapped[float] = mapped_column(Float)
    map_position_x: Mapped[float] = mapped_column(Float)
    map_position_y: Mapped[float] = mapped_column(Float)
    map_size: Mapped[float] = mapped_column(Float)
    map_arrow_offset: Mapped[float] = mapped_column(Float)
    deatail_aura_size: Mapped[float] = mapped_column(Float)
    map_aura_size: Mapped[float] = mapped_column(Float)
    disp_on_bg: Mapped[int] = mapped_column(Integer)
    qd_mode: Mapped[int] = mapped_column(Integer)
    td_mode: Mapped[int] = mapped_column(Integer)


class ShioriBossCondition(Base):
    __tablename__ = 'shiori_boss_condition'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    release_quest_id: Mapped[int] = mapped_column(Integer)
    release_boss_id: Mapped[int] = mapped_column(Integer)


class ShioriDescription(Base):
    __tablename__ = 'shiori_description'
    __table_args__ = (
        Index('shiori_description_0_type', 'type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class ShioriEnemyParameter(Base):
    __tablename__ = 'shiori_enemy_parameter'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer)
    resist_status_id: Mapped[int] = mapped_column(Integer)
    resist_variation_id: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)


class ShioriEventList(Base):
    __tablename__ = 'shiori_event_list'
    __table_args__ = (
        Index('shiori_event_list_0_original_event_id', 'original_event_id'),
        Index('shiori_event_list_0_series_event_id', 'series_event_id')
    )

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    banner_y: Mapped[int] = mapped_column(Integer)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    condition_chara_id: Mapped[int] = mapped_column(Integer)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer)
    condition_shiori_quest_id: Mapped[int] = mapped_column(Integer)
    original_event_id: Mapped[int] = mapped_column(Integer)
    series_event_id: Mapped[int] = mapped_column(Integer)
    original_start_time: Mapped[str] = mapped_column(Text)
    gojuon_order: Mapped[int] = mapped_column(Integer)
    help_index: Mapped[str] = mapped_column(Text)


class ShioriItem(Base):
    __tablename__ = 'shiori_item'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_material_id_1: Mapped[int] = mapped_column(Integer)
    unit_material_id_2: Mapped[int] = mapped_column(Integer)


class ShioriMissionRewardDatum(Base):
    __tablename__ = 'shiori_mission_reward_data'
    __table_args__ = (
        Index('shiori_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriQuest(Base):
    __tablename__ = 'shiori_quest'
    __table_args__ = (
        Index('shiori_quest_0_drop_reward_id', 'drop_reward_id'),
        Index('shiori_quest_0_event_id', 'event_id')
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_id: Mapped[int] = mapped_column(Integer)
    quest_seq: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    icon_offset_x: Mapped[float] = mapped_column(Float)
    icon_offset_y: Mapped[float] = mapped_column(Float)
    icon_scale: Mapped[float] = mapped_column(Float)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    unit_exp: Mapped[int] = mapped_column(Integer)
    love: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    daily_limit: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    rank_reward_group: Mapped[int] = mapped_column(Integer)
    drop_reward_type: Mapped[int] = mapped_column(Integer)
    drop_reward_id: Mapped[int] = mapped_column(Integer)
    drop_reward_num: Mapped[int] = mapped_column(Integer)
    drop_reward_odds: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)


class ShioriQuestArea(Base):
    __tablename__ = 'shiori_quest_area'
    __table_args__ = (
        Index('shiori_quest_area_0_event_id', 'event_id'),
    )

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    area_disp: Mapped[int] = mapped_column(Integer)
    map_id: Mapped[int] = mapped_column(Integer)
    scroll_width: Mapped[int] = mapped_column(Integer)
    scroll_height: Mapped[int] = mapped_column(Integer)
    open_tutorial_id: Mapped[int] = mapped_column(Integer)
    tutorial_param_1: Mapped[str] = mapped_column(Text)
    tutorial_param_2: Mapped[str] = mapped_column(Text)
    additional_effect: Mapped[int] = mapped_column(Integer)


class ShioriQuestCondition(Base):
    __tablename__ = 'shiori_quest_condition'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    release_quest_id: Mapped[int] = mapped_column(Integer)
    release_boss_id: Mapped[int] = mapped_column(Integer)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer)


class ShioriStationaryMissionDatum(Base):
    __tablename__ = 'shiori_stationary_mission_data'

    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriUnlockUnitCondition(Base):
    __tablename__ = 'shiori_unlock_unit_condition'
    __table_args__ = (
        Index('shiori_unlock_unit_condition_0_condition_mission_id', 'condition_mission_id'),
        Index('shiori_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_mission_id: Mapped[int] = mapped_column(Integer)
    top_description: Mapped[str] = mapped_column(Text)
    description_1: Mapped[str] = mapped_column(Text)
    description_2: Mapped[str] = mapped_column(Text)


class ShioriWaveGroupDatum(Base):
    __tablename__ = 'shiori_wave_group_data'

    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer)
    wave: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    reward_group_id_1: Mapped[int] = mapped_column(Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer)
    reward_odds_1: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    reward_group_id_2: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer)
    reward_odds_2: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    reward_group_id_3: Mapped[int] = mapped_column(Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer)
    reward_odds_3: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    reward_group_id_4: Mapped[int] = mapped_column(Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer)
    reward_odds_4: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    reward_group_id_5: Mapped[int] = mapped_column(Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer)
    reward_odds_5: Mapped[int] = mapped_column(Integer)


class ShopStaticPriceGroup(Base):
    __tablename__ = 'shop_static_price_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price_group_id: Mapped[int] = mapped_column(Integer)
    buy_count_from: Mapped[int] = mapped_column(Integer)
    buy_count_to: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)


class SjrChara(Base):
    __tablename__ = 'sjr_chara'

    sjr_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    personality: Mapped[int] = mapped_column(Integer)
    speed: Mapped[int] = mapped_column(Integer)
    tired_coefficient: Mapped[int] = mapped_column(Integer)
    spring: Mapped[int] = mapped_column(Integer)
    resume_time: Mapped[float] = mapped_column(Float)
    proper_id: Mapped[int] = mapped_column(Integer)
    ub_id: Mapped[int] = mapped_column(Integer)
    tp_length: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    recommend_type_1: Mapped[int] = mapped_column(Integer)
    recommend_type_2: Mapped[int] = mapped_column(Integer)
    recommend_type_3: Mapped[int] = mapped_column(Integer)


class SjrCourse(Base):
    __tablename__ = 'sjr_course'

    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    difficulty_level: Mapped[int] = mapped_column(Integer)
    feature: Mapped[int] = mapped_column(Integer)
    length: Mapped[int] = mapped_column(Integer)
    peek_pos: Mapped[int] = mapped_column(Integer)
    time: Mapped[float] = mapped_column(Float)
    rail_1: Mapped[int] = mapped_column(Integer)
    rail_2: Mapped[int] = mapped_column(Integer)
    rail_3: Mapped[int] = mapped_column(Integer)


class SjrDramaScript(Base):
    __tablename__ = 'sjr_drama_script'
    __table_args__ = (
        Index('sjr_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class SjrEmblem(Base):
    __tablename__ = 'sjr_emblem'

    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class SjrFeatureGroup(Base):
    __tablename__ = 'sjr_feature_group'

    feature_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)


class SjrNameFormer(Base):
    __tablename__ = 'sjr_name_former'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    constrain_group: Mapped[int] = mapped_column(Integer)
    condition_type_1: Mapped[int] = mapped_column(Integer)
    condition_type_2: Mapped[int] = mapped_column(Integer)
    condition_type_3: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_value_2: Mapped[int] = mapped_column(Integer)
    condition_value_3: Mapped[int] = mapped_column(Integer)


class SjrNameLater(Base):
    __tablename__ = 'sjr_name_later'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    name_group: Mapped[int] = mapped_column(Integer)
    score_from: Mapped[int] = mapped_column(Integer)
    score_to: Mapped[int] = mapped_column(Integer)


class SjrNpcActionOdds(Base):
    __tablename__ = 'sjr_npc_action_odds'
    __table_args__ = (
        Index('sjr_npc_action_odds_0_action_odds_id', 'action_odds_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_odds_id: Mapped[int] = mapped_column(Integer)
    distance: Mapped[int] = mapped_column(Integer)
    angle: Mapped[int] = mapped_column(Integer)
    rate: Mapped[int] = mapped_column(Integer)


class SjrParameterEvaluation(Base):
    __tablename__ = 'sjr_parameter_evaluation'

    parameter_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    border_1: Mapped[float] = mapped_column(Float)
    border_2: Mapped[float] = mapped_column(Float)
    border_3: Mapped[float] = mapped_column(Float)


class SjrProperEvaluation(Base):
    __tablename__ = 'sjr_proper_evaluation'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    border_1: Mapped[int] = mapped_column(Integer)
    border_2: Mapped[int] = mapped_column(Integer)


class SjrProperFeature(Base):
    __tablename__ = 'sjr_proper_feature'

    proper_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feature_group_1: Mapped[int] = mapped_column(Integer)
    feature_group_2: Mapped[int] = mapped_column(Integer)
    feature_group_3: Mapped[int] = mapped_column(Integer)
    value_1: Mapped[int] = mapped_column(Integer)
    value_2: Mapped[int] = mapped_column(Integer)
    value_3: Mapped[int] = mapped_column(Integer)


class SjrRail(Base):
    __tablename__ = 'sjr_rail'
    __table_args__ = (
        Index('sjr_rail_0_rail_id', 'rail_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rail_id: Mapped[int] = mapped_column(Integer)
    gimmick_id: Mapped[int] = mapped_column(Integer)
    gimmick_pos: Mapped[int] = mapped_column(Integer)


class SjrReward(Base):
    __tablename__ = 'sjr_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sjr_score: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class SjrScore(Base):
    __tablename__ = 'sjr_score'

    round: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_score: Mapped[int] = mapped_column(Integer)
    second_score: Mapped[int] = mapped_column(Integer)
    third_score: Mapped[int] = mapped_column(Integer)
    time_score: Mapped[int] = mapped_column(Integer)
    action_score: Mapped[int] = mapped_column(Integer)
    normal_bonus: Mapped[float] = mapped_column(Float)
    hard_bonus: Mapped[float] = mapped_column(Float)
    extra_bonus: Mapped[float] = mapped_column(Float)


class SjrUbDatum(Base):
    __tablename__ = 'sjr_ub_data'

    ub_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    top_description: Mapped[str] = mapped_column(Text)
    in_game_description: Mapped[str] = mapped_column(Text)
    ub_type: Mapped[int] = mapped_column(Integer)
    ub_value_1: Mapped[int] = mapped_column(Integer)
    ub_value_2: Mapped[int] = mapped_column(Integer)
    ub_value_3: Mapped[int] = mapped_column(Integer)
    ub_value_4: Mapped[int] = mapped_column(Integer)


class SkeStoryDatum(Base):
    __tablename__ = 'ske_story_data'
    __table_args__ = (
        Index('ske_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    unlock_condition_quest_id: Mapped[int] = mapped_column(Integer)
    unlock_condition_boss_id: Mapped[int] = mapped_column(Integer)
    read_condition_event_story_id: Mapped[int] = mapped_column(Integer)


class SkeStoryScript(Base):
    __tablename__ = 'ske_story_script'
    __table_args__ = (
        Index('ske_story_script_0_story_id', 'story_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class SkillAction(Base):
    __tablename__ = 'skill_action'

    action_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_id: Mapped[int] = mapped_column(Integer)
    action_type: Mapped[int] = mapped_column(Integer)
    action_detail_1: Mapped[int] = mapped_column(Integer)
    action_detail_2: Mapped[int] = mapped_column(Integer)
    action_detail_3: Mapped[int] = mapped_column(Integer)
    action_value_1: Mapped[float] = mapped_column(Float)
    action_value_2: Mapped[float] = mapped_column(Float)
    action_value_3: Mapped[float] = mapped_column(Float)
    action_value_4: Mapped[float] = mapped_column(Float)
    action_value_5: Mapped[float] = mapped_column(Float)
    action_value_6: Mapped[float] = mapped_column(Float)
    action_value_7: Mapped[float] = mapped_column(Float)
    target_assignment: Mapped[int] = mapped_column(Integer)
    target_area: Mapped[int] = mapped_column(Integer)
    target_range: Mapped[int] = mapped_column(Integer)
    target_type: Mapped[int] = mapped_column(Integer)
    target_number: Mapped[int] = mapped_column(Integer)
    target_count: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    level_up_disp: Mapped[str] = mapped_column(Text)


class SkillCost(Base):
    __tablename__ = 'skill_cost'

    target_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer)


class SkillDatum(Base):
    __tablename__ = 'skill_data'

    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_type: Mapped[int] = mapped_column(Integer)
    skill_area_width: Mapped[int] = mapped_column(Integer)
    skill_cast_time: Mapped[float] = mapped_column(Float)
    boss_ub_cool_time: Mapped[float] = mapped_column(Float)
    action_1: Mapped[int] = mapped_column(Integer)
    action_2: Mapped[int] = mapped_column(Integer)
    action_3: Mapped[int] = mapped_column(Integer)
    action_4: Mapped[int] = mapped_column(Integer)
    action_5: Mapped[int] = mapped_column(Integer)
    action_6: Mapped[int] = mapped_column(Integer)
    action_7: Mapped[int] = mapped_column(Integer)
    action_8: Mapped[int] = mapped_column(Integer)
    action_9: Mapped[int] = mapped_column(Integer)
    action_10: Mapped[int] = mapped_column(Integer)
    depend_action_1: Mapped[int] = mapped_column(Integer)
    depend_action_2: Mapped[int] = mapped_column(Integer)
    depend_action_3: Mapped[int] = mapped_column(Integer)
    depend_action_4: Mapped[int] = mapped_column(Integer)
    depend_action_5: Mapped[int] = mapped_column(Integer)
    depend_action_6: Mapped[int] = mapped_column(Integer)
    depend_action_7: Mapped[int] = mapped_column(Integer)
    depend_action_8: Mapped[int] = mapped_column(Integer)
    depend_action_9: Mapped[int] = mapped_column(Integer)
    depend_action_10: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    icon_type: Mapped[int] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(Text)


class SkipBossDatum(Base):
    __tablename__ = 'skip_boss_data'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_motion_id: Mapped[int] = mapped_column(Integer)
    skip_bg_id: Mapped[int] = mapped_column(Integer)
    skip_position_x: Mapped[int] = mapped_column(Integer)
    skip_position_y: Mapped[int] = mapped_column(Integer)
    skip_scale_x: Mapped[float] = mapped_column(Float)
    skip_scale_y: Mapped[float] = mapped_column(Float)


class SkipMonsterDatum(Base):
    __tablename__ = 'skip_monster_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    bg_skip_id: Mapped[int] = mapped_column(Integer)


class SpBattleVoice(Base):
    __tablename__ = 'sp_battle_voice'
    __table_args__ = (
        Index('sp_battle_voice_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)


class SpDetailVoice(Base):
    __tablename__ = 'sp_detail_voice'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cue_name_1: Mapped[str] = mapped_column(Text)
    cue_name_2: Mapped[str] = mapped_column(Text)
    cue_name_3: Mapped[str] = mapped_column(Text)
    cue_name_4: Mapped[str] = mapped_column(Text)
    cue_name_5: Mapped[str] = mapped_column(Text)


class SpLoseVoice(Base):
    __tablename__ = 'sp_lose_voice'

    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    unit_1_pos_x: Mapped[int] = mapped_column(Integer)
    unit_1_pos_y: Mapped[int] = mapped_column(Integer)
    unit_1_depth: Mapped[int] = mapped_column(Integer)
    unit_1_clip: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    unit_2_pos_x: Mapped[int] = mapped_column(Integer)
    unit_2_pos_y: Mapped[int] = mapped_column(Integer)
    unit_2_depth: Mapped[int] = mapped_column(Integer)
    unit_2_clip: Mapped[int] = mapped_column(Integer)
    unit_id_3: Mapped[int] = mapped_column(Integer)
    unit_3_pos_x: Mapped[int] = mapped_column(Integer)
    unit_3_pos_y: Mapped[int] = mapped_column(Integer)
    unit_3_depth: Mapped[int] = mapped_column(Integer)
    unit_3_clip: Mapped[int] = mapped_column(Integer)
    unit_only_disp: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_1: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_2: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_3: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_4: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_5: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_6: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_7: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_8: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_9: Mapped[int] = mapped_column(Integer)
    speaker_unit_id_10: Mapped[int] = mapped_column(Integer)


class SpLoseVoiceGroup(Base):
    __tablename__ = 'sp_lose_voice_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speaker_unit_id: Mapped[int] = mapped_column(Integer)


class SpaceBattleDatum(Base):
    __tablename__ = 'space_battle_data'

    space_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    space_enemy_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    clear_reward_group: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)


class SpaceSchedule(Base):
    __tablename__ = 'space_schedule'

    space_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    count_end_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    sid: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)


class SpaceTopDatum(Base):
    __tablename__ = 'space_top_data'
    __table_args__ = (
        Index('space_top_data_0_space_id', 'space_id'),
        Index('space_top_data_0_story_id', 'story_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    space_id: Mapped[int] = mapped_column(Integer)
    space_battle_id: Mapped[int] = mapped_column(Integer)
    part_flag: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer)
    time_from: Mapped[str] = mapped_column(Text)
    time_to: Mapped[str] = mapped_column(Text)
    skip_battle_time: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)


class SpecialStill(Base):
    __tablename__ = 'special_still'

    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    back_momory_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)


class SpecialStoryBanner(Base):
    __tablename__ = 'special_story_banner'
    __table_args__ = (
        Index('special_story_banner_0_story_group_id', 'story_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    remind_end_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class SpecialfesBanner(Base):
    __tablename__ = 'specialfes_banner'

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banner_id_1: Mapped[int] = mapped_column(Integer)
    banner_id_2: Mapped[int] = mapped_column(Integer)
    banner_id_3: Mapped[int] = mapped_column(Integer)
    banner_id_4: Mapped[int] = mapped_column(Integer)
    banner_id_5: Mapped[int] = mapped_column(Integer)
    banner_id_6: Mapped[int] = mapped_column(Integer)
    banner_id_7: Mapped[int] = mapped_column(Integer)
    banner_id_8: Mapped[int] = mapped_column(Integer)
    banner_id_9: Mapped[int] = mapped_column(Integer)
    banner_id_10: Mapped[int] = mapped_column(Integer)


class SpotDramaScriptDatum(Base):
    __tablename__ = 'spot_drama_script_data'
    __table_args__ = (
        Index('spot_drama_script_data_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class SpskillLabelDatum(Base):
    __tablename__ = 'spskill_label_data'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normal_label_text: Mapped[str] = mapped_column(Text)
    sp_label_text: Mapped[str] = mapped_column(Text)


class SpskillLvInitializeDatum(Base):
    __tablename__ = 'spskill_lv_initialize_data'

    initialize_skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_skill_id: Mapped[int] = mapped_column(Integer)


class SreAddTimesDatum(Base):
    __tablename__ = 'sre_add_times_data'
    __table_args__ = (
        Index('sre_add_times_data_0_sre_id', 'sre_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer)
    add_times: Mapped[int] = mapped_column(Integer)
    add_times_time: Mapped[str] = mapped_column(Text)


class SreBattleBonus(Base):
    __tablename__ = 'sre_battle_bonus'
    __table_args__ = (
        Index('sre_battle_bonus_0_sre_id_1_sre_boss_id', 'sre_id', 'sre_boss_id'),
        Index('sre_battle_bonus_0_sre_id_1_type', 'sre_id', 'type'),
        Index('sre_battle_bonus_0_type', 'type'),
        Index('sre_battle_bonus_0_type_1_sre_boss_id', 'type', 'sre_boss_id')
    )

    sre_battle_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    sre_boss_id: Mapped[int] = mapped_column(Integer)
    sre_id: Mapped[int] = mapped_column(Integer)
    phase: Mapped[int] = mapped_column(Integer)
    condition_hp: Mapped[str] = mapped_column(Text)
    condition_time: Mapped[int] = mapped_column(Integer)
    sre_battle_effect_id: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    battle_bonus_story_id: Mapped[int] = mapped_column(Integer)


class SreBattleBonusEffect(Base):
    __tablename__ = 'sre_battle_bonus_effect'

    sre_battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    text_id: Mapped[int] = mapped_column(Integer)
    skill_id: Mapped[int] = mapped_column(Integer)
    target_type: Mapped[int] = mapped_column(Integer)


class SreBossDatum(Base):
    __tablename__ = 'sre_boss_data'
    __table_args__ = (
        Index('sre_boss_data_0_sre_id', 'sre_id'),
        Index('sre_boss_data_0_sre_id_1_phase', 'sre_id', 'phase')
    )

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    battle_start_story_id: Mapped[int] = mapped_column(Integer)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer)
    disappearance_story_id: Mapped[int] = mapped_column(Integer)
    all_disappearance_story_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    max_raid_hp: Mapped[str] = mapped_column(Text)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer)
    challenge_odds_group_id: Mapped[int] = mapped_column(Integer)
    expel_reward_group_id: Mapped[int] = mapped_column(Integer)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    result_boss_position_y_1: Mapped[float] = mapped_column(Float)
    lane_priority_1: Mapped[int] = mapped_column(Integer)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    enemy_size_2: Mapped[float] = mapped_column(Float)
    result_boss_position_y_2: Mapped[float] = mapped_column(Float)
    lane_priority_2: Mapped[int] = mapped_column(Integer)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    enemy_size_3: Mapped[float] = mapped_column(Float)
    result_boss_position_y_3: Mapped[float] = mapped_column(Float)
    lane_priority_3: Mapped[int] = mapped_column(Integer)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    enemy_size_4: Mapped[float] = mapped_column(Float)
    result_boss_position_y_4: Mapped[float] = mapped_column(Float)
    lane_priority_4: Mapped[int] = mapped_column(Integer)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    enemy_size_5: Mapped[float] = mapped_column(Float)
    result_boss_position_y_5: Mapped[float] = mapped_column(Float)
    lane_priority_5: Mapped[int] = mapped_column(Integer)
    wave_bgm: Mapped[str] = mapped_column(Text)
    bonus_max: Mapped[int] = mapped_column(Integer)
    deck_number: Mapped[int] = mapped_column(Integer)


class SreEffect(Base):
    __tablename__ = 'sre_effect'

    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_1: Mapped[int] = mapped_column(Integer)
    bonus_2: Mapped[int] = mapped_column(Integer)
    bonus_3: Mapped[int] = mapped_column(Integer)
    bonus_4: Mapped[int] = mapped_column(Integer)
    bonus_5: Mapped[int] = mapped_column(Integer)


class SreEffectiveUnit(Base):
    __tablename__ = 'sre_effective_unit'
    __table_args__ = (
        Index('sre_effective_unit_0_sre_boss_id_1_sre_id', 'sre_boss_id', 'sre_id'),
    )

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id: Mapped[int] = mapped_column(Integer)
    support_effect_id: Mapped[int] = mapped_column(Integer)


class SreEnemyParameter(Base):
    __tablename__ = 'sre_enemy_parameter'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer)
    resist_status_id: Mapped[int] = mapped_column(Integer)
    resist_variation_id: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer)
    break_durability: Mapped[int] = mapped_column(Integer)
    virtual_hp: Mapped[int] = mapped_column(Integer)


class SreExterminationReward(Base):
    __tablename__ = 'sre_extermination_reward'

    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class SreMissionCategoryDatum(Base):
    __tablename__ = 'sre_mission_category_data'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)


class SreMissionDatum(Base):
    __tablename__ = 'sre_mission_data'
    __table_args__ = (
        Index('sre_mission_data_0_sre_id', 'sre_id'),
        Index('sre_mission_data_0_sre_id_1_category_id', 'sre_id', 'category_id')
    )

    sre_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer)
    disp_group: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    sre_boss_id: Mapped[int] = mapped_column(Integer)
    condition_value: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[str] = mapped_column(Text)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class SreMissionRewardDatum(Base):
    __tablename__ = 'sre_mission_reward_data'
    __table_args__ = (
        Index('sre_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class SreQuestDifficultyDatum(Base):
    __tablename__ = 'sre_quest_difficulty_data'

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)


class SreSchedule(Base):
    __tablename__ = 'sre_schedule'

    sre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    teaser_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    count_start_time: Mapped[str] = mapped_column(Text)
    close_time: Mapped[str] = mapped_column(Text)
    story_id: Mapped[int] = mapped_column(Integer)
    close_story_condition_id: Mapped[int] = mapped_column(Integer)
    close_story_id: Mapped[int] = mapped_column(Integer)
    top_bgm: Mapped[str] = mapped_column(Text)
    top_bg: Mapped[str] = mapped_column(Text)


class SreWaveGroupDatum(Base):
    __tablename__ = 'sre_wave_group_data'
    __table_args__ = (
        Index('sre_wave_group_data_0_wave_group_id', 'wave_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    odds: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    drop_reward_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    drop_reward_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    drop_reward_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    drop_reward_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    drop_reward_id_5: Mapped[int] = mapped_column(Integer)
    guest_enemy_id: Mapped[int] = mapped_column(Integer)
    guest_lane: Mapped[int] = mapped_column(Integer)


class SrtAction(Base):
    __tablename__ = 'srt_action'

    action_name: Mapped[str] = mapped_column(Text, primary_key=True)
    inori_action: Mapped[str] = mapped_column(Text)
    dragon_action: Mapped[str] = mapped_column(Text)
    kaya_action: Mapped[str] = mapped_column(Text)
    homare_action: Mapped[str] = mapped_column(Text)
    talk_text_type: Mapped[int] = mapped_column(Integer)
    talk_text: Mapped[str] = mapped_column(Text)
    voice_list: Mapped[str] = mapped_column(Text)


class SrtPanel(Base):
    __tablename__ = 'srt_panel'
    __table_args__ = (
        Index('srt_panel_0_panel_id', 'panel_id'),
        Index('srt_panel_0_version', 'version')
    )

    reading_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reading: Mapped[str] = mapped_column(Text)
    read_type: Mapped[int] = mapped_column(Integer)
    panel_id: Mapped[int] = mapped_column(Integer)
    detail_text: Mapped[str] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer)
    head_symbol: Mapped[str] = mapped_column(Text)
    tail_symbol: Mapped[str] = mapped_column(Text)


class SrtReward(Base):
    __tablename__ = 'srt_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    srt_score: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class SrtScore(Base):
    __tablename__ = 'srt_score'

    difficulty_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    coefficient_read_type_1: Mapped[int] = mapped_column(Integer)
    coefficient_read_type_2: Mapped[int] = mapped_column(Integer)
    coefficient_read_type_3: Mapped[int] = mapped_column(Integer)
    coefficient_count_priconne_panel: Mapped[int] = mapped_column(Integer)
    coefficient_fever: Mapped[int] = mapped_column(Integer)
    constant_turn_bonus: Mapped[int] = mapped_column(Integer)
    coefficient_turn_bonus: Mapped[int] = mapped_column(Integer)
    coefficient_avg_answer_time: Mapped[int] = mapped_column(Integer)
    constant_wrong_num: Mapped[int] = mapped_column(Integer)
    coefficient_wrong_num: Mapped[int] = mapped_column(Integer)


class SrtTopTalk(Base):
    __tablename__ = 'srt_top_talk'
    __table_args__ = (
        Index('srt_top_talk_0_talk_id', 'talk_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talk_id: Mapped[int] = mapped_column(Integer)
    chara_index: Mapped[int] = mapped_column(Integer)
    talk_text: Mapped[str] = mapped_column(Text)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    direction: Mapped[int] = mapped_column(Integer)


class SspStoryDatum(Base):
    __tablename__ = 'ssp_story_data'
    __table_args__ = (
        Index('ssp_story_data_0_contents_type', 'contents_type'),
        Index('ssp_story_data_0_original_event_id', 'original_event_id')
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    contents_type: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    read_condition: Mapped[int] = mapped_column(Integer)


class Stamp(Base):
    __tablename__ = 'stamp'

    stamp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[str] = mapped_column(Text)
    end_date: Mapped[str] = mapped_column(Text)


class StationaryMissionDatum(Base):
    __tablename__ = 'stationary_mission_data'

    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    category_icon: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    min_level: Mapped[int] = mapped_column(Integer)
    max_level: Mapped[int] = mapped_column(Integer)
    title_color_id: Mapped[int] = mapped_column(Integer)
    visible_flag: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class Still(Base):
    __tablename__ = 'still'
    __table_args__ = (
        Index('still_0_still_group_id', 'still_group_id'),
        Index('still_0_story_id', 'story_id')
    )

    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    story_id: Mapped[int] = mapped_column(Integer)
    still_group_id: Mapped[int] = mapped_column(Integer)
    vertical_still_flg: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    unit_id_3: Mapped[int] = mapped_column(Integer)
    unit_id_4: Mapped[int] = mapped_column(Integer)
    unit_id_5: Mapped[int] = mapped_column(Integer)
    unit_id_6: Mapped[int] = mapped_column(Integer)
    unit_id_7: Mapped[int] = mapped_column(Integer)
    unit_id_8: Mapped[int] = mapped_column(Integer)
    unit_id_9: Mapped[int] = mapped_column(Integer)
    unit_id_10: Mapped[int] = mapped_column(Integer)
    facial_id: Mapped[int] = mapped_column(Integer)
    album_ignore: Mapped[int] = mapped_column(Integer)
    my_page_flag: Mapped[int] = mapped_column(Integer)
    scroll_direction: Mapped[int] = mapped_column(Integer)


class StoryBulkSkip(Base):
    __tablename__ = 'story_bulk_skip'

    bulk_skip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_from: Mapped[int] = mapped_column(Integer)
    story_id_to: Mapped[int] = mapped_column(Integer)
    release_level: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    balloon_sprite_name: Mapped[str] = mapped_column(Text)
    label_sprite_name: Mapped[str] = mapped_column(Text)
    button_sprite_name: Mapped[str] = mapped_column(Text)


class StoryCharacterMask(Base):
    __tablename__ = 'story_character_mask'

    chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offset: Mapped[float] = mapped_column(Float)
    size: Mapped[float] = mapped_column(Float)
    softness: Mapped[float] = mapped_column(Float)


class StoryDatum(Base):
    __tablename__ = 'story_data'

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    thumbnail_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer)
    condition_free_flag: Mapped[int] = mapped_column(Integer)
    gojuon_order: Mapped[int] = mapped_column(Integer)


class StoryDetail(Base):
    __tablename__ = 'story_detail'
    __table_args__ = (
        Index('story_detail_0_unlock_quest_id', 'unlock_quest_id'),
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    visible_type: Mapped[int] = mapped_column(Integer)
    story_end: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)
    force_unlock_time: Mapped[str] = mapped_column(Text)
    pre_story_id_2: Mapped[int] = mapped_column(Integer)
    force_unlock_time_2: Mapped[str] = mapped_column(Text)
    love_level: Mapped[int] = mapped_column(Integer)
    requirement_id: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    story_quest_id: Mapped[int] = mapped_column(Integer)
    lock_all_text: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_value_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_value_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_value_3: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class StoryQuestDatum(Base):
    __tablename__ = 'story_quest_data'

    story_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    limit_time: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    guest_unit_1: Mapped[int] = mapped_column(Integer)
    guest_unit_2: Mapped[int] = mapped_column(Integer)
    guest_unit_3: Mapped[int] = mapped_column(Integer)
    guest_unit_4: Mapped[int] = mapped_column(Integer)
    guest_unit_5: Mapped[int] = mapped_column(Integer)


class SvdDramaScript(Base):
    __tablename__ = 'svd_drama_script'
    __table_args__ = (
        Index('svd_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class SvdStoryDatum(Base):
    __tablename__ = 'svd_story_data'
    __table_args__ = (
        Index('svd_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    read_condition_time: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    read_condition: Mapped[int] = mapped_column(Integer)


class SvdStoryScript(Base):
    __tablename__ = 'svd_story_script'
    __table_args__ = (
        Index('svd_story_script_0_story_id', 'story_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class TaqCompletionRewards(Base):
    __tablename__ = 'taq_completion_rewards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_num: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    emblem_id: Mapped[int] = mapped_column(Integer)


class TaqDatum(Base):
    __tablename__ = 'taq_data'

    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre: Mapped[int] = mapped_column(Integer)
    taq_type: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    word: Mapped[str] = mapped_column(Text)
    chunk: Mapped[str] = mapped_column(Text)
    detail: Mapped[str] = mapped_column(Text)
    detail_2: Mapped[str] = mapped_column(Text)
    assist_detail: Mapped[str] = mapped_column(Text)
    image_id: Mapped[int] = mapped_column(Integer)
    char_no_1: Mapped[int] = mapped_column(Integer)
    char_no_2: Mapped[int] = mapped_column(Integer)
    char_no_3: Mapped[int] = mapped_column(Integer)
    char_no_4: Mapped[int] = mapped_column(Integer)
    char_no_5: Mapped[int] = mapped_column(Integer)
    input_type_1: Mapped[int] = mapped_column(Integer)
    input_type_2: Mapped[int] = mapped_column(Integer)
    input_type_3: Mapped[int] = mapped_column(Integer)
    input_type_4: Mapped[int] = mapped_column(Integer)
    input_type_5: Mapped[int] = mapped_column(Integer)


class TaqDramaScript(Base):
    __tablename__ = 'taq_drama_script'
    __table_args__ = (
        Index('taq_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class TaqGameSetting(Base):
    __tablename__ = 'taq_game_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lottery_rate: Mapped[float] = mapped_column(Float)
    help_use_count_normal: Mapped[int] = mapped_column(Integer)
    help_use_count_hard: Mapped[int] = mapped_column(Integer)
    help_use_count_veryhard: Mapped[int] = mapped_column(Integer)


class TaqGenre(Base):
    __tablename__ = 'taq_genre'

    genre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre_name: Mapped[str] = mapped_column(Text)


class TaqGoodUnit(Base):
    __tablename__ = 'taq_good_unit'

    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    unit_id_3: Mapped[int] = mapped_column(Integer)
    unit_id_4: Mapped[int] = mapped_column(Integer)
    unit_id_5: Mapped[int] = mapped_column(Integer)
    unit_id_6: Mapped[int] = mapped_column(Integer)
    unit_id_7: Mapped[int] = mapped_column(Integer)
    unit_id_8: Mapped[int] = mapped_column(Integer)
    unit_id_9: Mapped[int] = mapped_column(Integer)
    unit_id_10: Mapped[int] = mapped_column(Integer)


class TaqIncorrectWord(Base):
    __tablename__ = 'taq_incorrect_word'

    word_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incorrect_word: Mapped[str] = mapped_column(Text)


class TaqKanjiList(Base):
    __tablename__ = 'taq_kanji_list'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kanji: Mapped[str] = mapped_column(Text)


class TaqNecessaryWord(Base):
    __tablename__ = 'taq_necessary_word'

    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    necessary_word_1: Mapped[str] = mapped_column(Text)
    unnecessary_word_1: Mapped[str] = mapped_column(Text)
    necessary_word_2: Mapped[str] = mapped_column(Text)
    unnecessary_word_2: Mapped[str] = mapped_column(Text)
    necessary_word_3: Mapped[str] = mapped_column(Text)
    unnecessary_word_3: Mapped[str] = mapped_column(Text)
    necessary_word_4: Mapped[str] = mapped_column(Text)
    unnecessary_word_4: Mapped[str] = mapped_column(Text)
    necessary_word_5: Mapped[str] = mapped_column(Text)
    unnecessary_word_5: Mapped[str] = mapped_column(Text)


class TaqRewards(Base):
    __tablename__ = 'taq_rewards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class TaqUnit(Base):
    __tablename__ = 'taq_unit'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sort_order: Mapped[int] = mapped_column(Integer)
    personality_id: Mapped[int] = mapped_column(Integer)
    genre_status_1: Mapped[int] = mapped_column(Integer)
    genre_status_2: Mapped[int] = mapped_column(Integer)
    genre_status_3: Mapped[int] = mapped_column(Integer)
    genre_status_4: Mapped[int] = mapped_column(Integer)
    genre_status_5: Mapped[int] = mapped_column(Integer)
    genre_status_6: Mapped[int] = mapped_column(Integer)


class TdfBattleEffect(Base):
    __tablename__ = 'tdf_battle_effect'
    __table_args__ = (
        Index('tdf_battle_effect_0_quest_id', 'quest_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer)
    icon_name: Mapped[str] = mapped_column(Text)
    effect_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class TdfDifficultyIconDatum(Base):
    __tablename__ = 'tdf_difficulty_icon_data'

    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_name: Mapped[str] = mapped_column(Text)
    effect_id: Mapped[int] = mapped_column(Integer)


class TdfPhaseDatum(Base):
    __tablename__ = 'tdf_phase_data'

    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    need_clear_num: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class TdfQuestDatum(Base):
    __tablename__ = 'tdf_quest_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_time: Mapped[int] = mapped_column(Integer)
    limit_num: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    reward_group_id: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    enemy_size_2: Mapped[float] = mapped_column(Float)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    enemy_size_3: Mapped[float] = mapped_column(Float)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    enemy_size_4: Mapped[float] = mapped_column(Float)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    enemy_size_5: Mapped[float] = mapped_column(Float)
    wave_bgm: Mapped[str] = mapped_column(Text)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)


class TdfSchedule(Base):
    __tablename__ = 'tdf_schedule'

    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_start_time: Mapped[str] = mapped_column(Text)
    recovery_disable_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    ex_quest_id: Mapped[int] = mapped_column(Integer)


class TdfTopOffset(Base):
    __tablename__ = 'tdf_top_offset'

    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)


class TdfWaveGroupDatum(Base):
    __tablename__ = 'tdf_wave_group_data'

    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)


class ThumbnailHideCondition(Base):
    __tablename__ = 'thumbnail_hide_condition'

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hide_story_id_from: Mapped[int] = mapped_column(Integer)
    hide_story_id_to: Mapped[int] = mapped_column(Integer)
    unlock_condition_story_id: Mapped[int] = mapped_column(Integer)
    is_hide_title: Mapped[int] = mapped_column(Integer)


class TicketGachaDatum(Base):
    __tablename__ = 'ticket_gacha_data'

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_name: Mapped[str] = mapped_column(Text)
    gacha_type: Mapped[int] = mapped_column(Integer)
    ticket_id: Mapped[int] = mapped_column(Integer)
    gacha_times: Mapped[int] = mapped_column(Integer)
    gacha_detail: Mapped[int] = mapped_column(Integer)
    guarantee_rarity: Mapped[str] = mapped_column(Text)
    rarity_odds: Mapped[str] = mapped_column(Text)
    chara_odds_star1: Mapped[str] = mapped_column(Text)
    chara_odds_star2: Mapped[str] = mapped_column(Text)
    chara_odds_star3: Mapped[str] = mapped_column(Text)
    staging_type: Mapped[int] = mapped_column(Integer)


class Tips(Base):
    __tablename__ = 'tips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)
    tips_index: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)


class TmeMapDatum(Base):
    __tablename__ = 'tme_map_data'
    __table_args__ = (
        Index('tme_map_data_0_event_id', 'event_id'),
    )

    tme_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    area_difficulty_type: Mapped[int] = mapped_column(Integer)
    release_effect: Mapped[int] = mapped_column(Integer)
    tap_effect: Mapped[int] = mapped_column(Integer)


class TowerAreaDatum(Base):
    __tablename__ = 'tower_area_data'

    tower_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_floor_num: Mapped[int] = mapped_column(Integer)
    area_bg: Mapped[int] = mapped_column(Integer)
    tower_bgm: Mapped[str] = mapped_column(Text)
    cloister_quest_id: Mapped[int] = mapped_column(Integer)


class TowerCloisterQuestDatum(Base):
    __tablename__ = 'tower_cloister_quest_data'

    tower_cloister_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    daily_limit: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer)
    start_tp_rate: Mapped[int] = mapped_column(Integer)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer)
    drop_reward_group_id: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_bgm: Mapped[str] = mapped_column(Text)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    w1_enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    w1_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    w1_enemy_size_1: Mapped[float] = mapped_column(Float)
    w1_enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    w1_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    w1_enemy_size_2: Mapped[float] = mapped_column(Float)
    w1_enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    w1_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    w1_enemy_size_3: Mapped[float] = mapped_column(Float)
    w1_enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    w1_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    w1_enemy_size_4: Mapped[float] = mapped_column(Float)
    w1_enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    w1_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    w1_enemy_size_5: Mapped[float] = mapped_column(Float)
    w2_enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    w2_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    w2_enemy_size_1: Mapped[float] = mapped_column(Float)
    w2_enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    w2_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    w2_enemy_size_2: Mapped[float] = mapped_column(Float)
    w2_enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    w2_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    w2_enemy_size_3: Mapped[float] = mapped_column(Float)
    w2_enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    w2_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    w2_enemy_size_4: Mapped[float] = mapped_column(Float)
    w2_enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    w2_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    w2_enemy_size_5: Mapped[float] = mapped_column(Float)
    w3_enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    w3_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    w3_enemy_size_1: Mapped[float] = mapped_column(Float)
    w3_enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    w3_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    w3_enemy_size_2: Mapped[float] = mapped_column(Float)
    w3_enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    w3_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    w3_enemy_size_3: Mapped[float] = mapped_column(Float)
    w3_enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    w3_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    w3_enemy_size_4: Mapped[float] = mapped_column(Float)
    w3_enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    w3_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    w3_enemy_size_5: Mapped[float] = mapped_column(Float)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)


class TowerEnemyParameter(Base):
    __tablename__ = 'tower_enemy_parameter'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    union_burst_level: Mapped[int] = mapped_column(Integer)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer)
    resist_status_id: Mapped[int] = mapped_column(Integer)
    resist_variation_id: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)
    enemy_color: Mapped[int] = mapped_column(Integer)


class TowerExQuestDatum(Base):
    __tablename__ = 'tower_ex_quest_data'
    __table_args__ = (
        Index('tower_ex_quest_data_0_floor_num', 'floor_num'),
    )

    tower_ex_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tower_area_id: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    additional_reward_type: Mapped[int] = mapped_column(Integer)
    additional_reward_id: Mapped[int] = mapped_column(Integer)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    enemy_size_2: Mapped[float] = mapped_column(Float)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    enemy_size_3: Mapped[float] = mapped_column(Float)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    enemy_size_4: Mapped[float] = mapped_column(Float)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    enemy_size_5: Mapped[float] = mapped_column(Float)
    wave_bgm: Mapped[str] = mapped_column(Text)
    clp_flag: Mapped[int] = mapped_column(Integer)
    skip_level: Mapped[int] = mapped_column(Integer)


class TowerQuestDatum(Base):
    __tablename__ = 'tower_quest_data'
    __table_args__ = (
        Index('tower_quest_data_0_floor_num', 'floor_num'),
    )

    tower_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tower_area_id: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    floor_image_type: Mapped[int] = mapped_column(Integer)
    floor_image_add_type: Mapped[int] = mapped_column(Integer)
    open_tower_ex_quest_id: Mapped[int] = mapped_column(Integer)
    boss_floor_flg: Mapped[int] = mapped_column(Integer)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer)
    start_tp_rate: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)
    additional_reward_type: Mapped[int] = mapped_column(Integer)
    additional_reward_id: Mapped[int] = mapped_column(Integer)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer)
    odds_group_id: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    bg_position: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer)
    enemy_size_1: Mapped[float] = mapped_column(Float)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer)
    enemy_size_2: Mapped[float] = mapped_column(Float)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer)
    enemy_size_3: Mapped[float] = mapped_column(Float)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer)
    enemy_size_4: Mapped[float] = mapped_column(Float)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer)
    enemy_size_5: Mapped[float] = mapped_column(Float)
    wave_bgm: Mapped[str] = mapped_column(Text)
    clp_flag: Mapped[int] = mapped_column(Integer)
    skip_level: Mapped[int] = mapped_column(Integer)


class TowerQuestFixRewardGroup(Base):
    __tablename__ = 'tower_quest_fix_reward_group'

    fix_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_1: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    treasure_type_2: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    treasure_type_3: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    treasure_type_4: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    treasure_type_5: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    treasure_type_6: Mapped[int] = mapped_column(Integer)
    reward_type_6: Mapped[int] = mapped_column(Integer)
    reward_id_6: Mapped[int] = mapped_column(Integer)
    reward_num_6: Mapped[int] = mapped_column(Integer)
    treasure_type_7: Mapped[int] = mapped_column(Integer)
    reward_type_7: Mapped[int] = mapped_column(Integer)
    reward_id_7: Mapped[int] = mapped_column(Integer)
    reward_num_7: Mapped[int] = mapped_column(Integer)
    treasure_type_8: Mapped[int] = mapped_column(Integer)
    reward_type_8: Mapped[int] = mapped_column(Integer)
    reward_id_8: Mapped[int] = mapped_column(Integer)
    reward_num_8: Mapped[int] = mapped_column(Integer)
    treasure_type_9: Mapped[int] = mapped_column(Integer)
    reward_type_9: Mapped[int] = mapped_column(Integer)
    reward_id_9: Mapped[int] = mapped_column(Integer)
    reward_num_9: Mapped[int] = mapped_column(Integer)
    treasure_type_10: Mapped[int] = mapped_column(Integer)
    reward_type_10: Mapped[int] = mapped_column(Integer)
    reward_id_10: Mapped[int] = mapped_column(Integer)
    reward_num_10: Mapped[int] = mapped_column(Integer)


class TowerQuestOddsGroup(Base):
    __tablename__ = 'tower_quest_odds_group'
    __table_args__ = (
        Index('tower_quest_odds_group_0_odds_group_id', 'odds_group_id'),
    )

    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_1: Mapped[int] = mapped_column(Integer)
    odds_csv_1: Mapped[str] = mapped_column(Text)
    treasure_type_2: Mapped[int] = mapped_column(Integer)
    odds_csv_2: Mapped[str] = mapped_column(Text)
    treasure_type_3: Mapped[int] = mapped_column(Integer)
    odds_csv_3: Mapped[str] = mapped_column(Text)
    treasure_type_4: Mapped[int] = mapped_column(Integer)
    odds_csv_4: Mapped[str] = mapped_column(Text)
    treasure_type_5: Mapped[int] = mapped_column(Integer)
    odds_csv_5: Mapped[str] = mapped_column(Text)
    treasure_type_6: Mapped[int] = mapped_column(Integer)
    odds_csv_6: Mapped[str] = mapped_column(Text)
    treasure_type_7: Mapped[int] = mapped_column(Integer)
    odds_csv_7: Mapped[str] = mapped_column(Text)
    treasure_type_8: Mapped[int] = mapped_column(Integer)
    odds_csv_8: Mapped[str] = mapped_column(Text)
    treasure_type_9: Mapped[int] = mapped_column(Integer)
    odds_csv_9: Mapped[str] = mapped_column(Text)
    treasure_type_10: Mapped[int] = mapped_column(Integer)
    odds_csv_10: Mapped[str] = mapped_column(Text)


class TowerSchedule(Base):
    __tablename__ = 'tower_schedule'
    __table_args__ = (
        Index('tower_schedule_0_opening_story_id', 'opening_story_id'),
    )

    tower_schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_tower_area_id: Mapped[int] = mapped_column(Integer)
    opening_story_id: Mapped[int] = mapped_column(Integer)
    count_start_time: Mapped[str] = mapped_column(Text)
    recovery_disable_time: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class TowerStoryDatum(Base):
    __tablename__ = 'tower_story_data'

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_type: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    thumbnail_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class TowerStoryDetail(Base):
    __tablename__ = 'tower_story_detail'

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    visible_type: Mapped[int] = mapped_column(Integer)
    story_end: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)
    love_level: Mapped[int] = mapped_column(Integer)
    requirement_id: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    story_quest_id: Mapped[int] = mapped_column(Integer)
    lock_all_text: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_value_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_value_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_value_3: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class TowerWaveGroupDatum(Base):
    __tablename__ = 'tower_wave_group_data'

    id: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)


class TpRecoveryAt(Base):
    __tablename__ = 'tp_recovery_at'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_value: Mapped[int] = mapped_column(Integer)
    correction_value: Mapped[float] = mapped_column(Float)


class TrainingQuestDatum(Base):
    __tablename__ = 'training_quest_data'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int] = mapped_column(Integer)
    quest_name: Mapped[str] = mapped_column(Text)
    limit_team_level: Mapped[int] = mapped_column(Integer)
    unlock_quest_id_1: Mapped[int] = mapped_column(Integer)
    unlock_quest_id_2: Mapped[int] = mapped_column(Integer)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    team_exp: Mapped[int] = mapped_column(Integer)
    unit_exp: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    rank_reward_group: Mapped[int] = mapped_column(Integer)
    background_1: Mapped[int] = mapped_column(Integer)
    wave_group_id_1: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    background_2: Mapped[int] = mapped_column(Integer)
    wave_group_id_2: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    background_3: Mapped[int] = mapped_column(Integer)
    wave_group_id_3: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    enemy_image_1: Mapped[int] = mapped_column(Integer)
    enemy_image_2: Mapped[int] = mapped_column(Integer)
    enemy_image_3: Mapped[int] = mapped_column(Integer)
    enemy_image_4: Mapped[int] = mapped_column(Integer)
    enemy_image_5: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    training_quest_detail_bg_id: Mapped[int] = mapped_column(Integer)
    training_quest_detail_bg_position: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class TravelAreaDatum(Base):
    __tablename__ = 'travel_area_data'

    travel_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_area_name: Mapped[str] = mapped_column(Text)
    condition_team_lv: Mapped[int] = mapped_column(Integer)
    bg_id: Mapped[int] = mapped_column(Integer)
    top_icon_id: Mapped[int] = mapped_column(Integer)
    top_icon_x: Mapped[int] = mapped_column(Integer)
    top_icon_y: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class TravelDecreaseTimeCost(Base):
    __tablename__ = 'travel_decrease_time_cost'

    count: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer)


class TravelExEventDatum(Base):
    __tablename__ = 'travel_ex_event_data'

    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    disp_order: Mapped[int] = mapped_column(Integer)


class TravelExEventDrama(Base):
    __tablename__ = 'travel_ex_event_drama'
    __table_args__ = (
        Index('travel_ex_event_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class TravelQuestDatum(Base):
    __tablename__ = 'travel_quest_data'
    __table_args__ = (
        Index('travel_quest_data_0_travel_area_id', 'travel_area_id'),
    )

    travel_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_area_id: Mapped[int] = mapped_column(Integer)
    travel_quest_name: Mapped[str] = mapped_column(Text)
    limit_unit_num: Mapped[int] = mapped_column(Integer)
    need_power: Mapped[int] = mapped_column(Integer)
    travel_time: Mapped[int] = mapped_column(Integer)
    travel_time_decrease_limit: Mapped[int] = mapped_column(Integer)
    travel_decrease_flag: Mapped[int] = mapped_column(Integer)
    main_reward_1: Mapped[int] = mapped_column(Integer)
    main_reward_2: Mapped[int] = mapped_column(Integer)
    main_reward_3: Mapped[int] = mapped_column(Integer)
    main_reward_4: Mapped[int] = mapped_column(Integer)
    main_reward_5: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    icon_x: Mapped[int] = mapped_column(Integer)
    icon_y: Mapped[int] = mapped_column(Integer)
    situation_group_id: Mapped[int] = mapped_column(Integer)


class TravelQuestResult(Base):
    __tablename__ = 'travel_quest_result'

    situation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    except_unit_group_id: Mapped[int] = mapped_column(Integer)


class TravelQuestResultGroup(Base):
    __tablename__ = 'travel_quest_result_group'
    __table_args__ = (
        Index('travel_quest_result_group_0_situation_group_id', 'situation_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    situation_group_id: Mapped[int] = mapped_column(Integer)
    situation_id: Mapped[int] = mapped_column(Integer)


class TravelQuestSubReward(Base):
    __tablename__ = 'travel_quest_sub_reward'
    __table_args__ = (
        Index('travel_quest_sub_reward_0_reward_id', 'reward_id'),
        Index('travel_quest_sub_reward_0_travel_quest_id', 'travel_quest_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)


class TravelResultExceptUnitGroup(Base):
    __tablename__ = 'travel_result_except_unit_group'
    __table_args__ = (
        Index('travel_result_except_unit_group_0_except_unit_group_id', 'except_unit_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    except_unit_group_id: Mapped[int] = mapped_column(Integer)
    except_unit_id: Mapped[int] = mapped_column(Integer)


class TravelRoundEventDatum(Base):
    __tablename__ = 'travel_round_event_data'

    round_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    round: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_id: Mapped[int] = mapped_column(Integer)
    transition_drama_id: Mapped[int] = mapped_column(Integer)
    main_drama_id: Mapped[int] = mapped_column(Integer)
    left_door_pre_drama_id: Mapped[int] = mapped_column(Integer)
    right_door_pre_drama_id: Mapped[int] = mapped_column(Integer)
    event_icon_id: Mapped[int] = mapped_column(Integer)
    travel_treasure_box_type: Mapped[int] = mapped_column(Integer)


class TravelRoundEventDrama(Base):
    __tablename__ = 'travel_round_event_drama'
    __table_args__ = (
        Index('travel_round_event_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class TravelStartDrama(Base):
    __tablename__ = 'travel_start_drama'
    __table_args__ = (
        Index('travel_start_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class TravelTopEventDatum(Base):
    __tablename__ = 'travel_top_event_data'
    __table_args__ = (
        Index('travel_top_event_data_0_top_event_id', 'top_event_id'),
    )

    top_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_group: Mapped[int] = mapped_column(Integer)
    drama_type: Mapped[int] = mapped_column(Integer)
    pattern: Mapped[int] = mapped_column(Integer, primary_key=True)
    zoom_offset_x: Mapped[int] = mapped_column(Integer)
    zoom_offset_y: Mapped[int] = mapped_column(Integer)
    pre_drama_id: Mapped[int] = mapped_column(Integer)
    main_drama_id: Mapped[int] = mapped_column(Integer)
    branch_id_1: Mapped[int] = mapped_column(Integer)
    branch_id_2: Mapped[int] = mapped_column(Integer)
    branch_id_3: Mapped[int] = mapped_column(Integer)
    branch_id_4: Mapped[int] = mapped_column(Integer)
    branch_id_5: Mapped[int] = mapped_column(Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    top_icon_type: Mapped[int] = mapped_column(Integer)


class TravelTopEventDrama(Base):
    __tablename__ = 'travel_top_event_drama'
    __table_args__ = (
        Index('travel_top_event_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class TravelTopEventPosDetail(Base):
    __tablename__ = 'travel_top_event_pos_detail'

    pos_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_group_id: Mapped[int] = mapped_column(Integer)
    pos_x: Mapped[int] = mapped_column(Integer)
    pos_y: Mapped[int] = mapped_column(Integer)
    all_pos_flag: Mapped[int] = mapped_column(Integer)


class TrialBattleCategory(Base):
    __tablename__ = 'trial_battle_category'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(Text)
    icon_id: Mapped[int] = mapped_column(Integer)
    label_type_1: Mapped[int] = mapped_column(Integer)
    label_type_2: Mapped[int] = mapped_column(Integer)
    label_type_3: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    description_detail: Mapped[str] = mapped_column(Text)


class TrialBattleDatum(Base):
    __tablename__ = 'trial_battle_data'
    __table_args__ = (
        Index('trial_battle_data_0_category_id', 'category_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    battle_name: Mapped[str] = mapped_column(Text)
    detail_bg_id: Mapped[int] = mapped_column(Integer)
    detail_bg_position: Mapped[int] = mapped_column(Integer)
    detail_boss_bg_size: Mapped[int] = mapped_column(Integer)
    detail_boss_bg_height: Mapped[int] = mapped_column(Integer)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id: Mapped[str] = mapped_column(Text)
    clear_reward_group: Mapped[int] = mapped_column(Integer)


class TrialBattleMissionDatum(Base):
    __tablename__ = 'trial_battle_mission_data'

    trial_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    quest_id: Mapped[int] = mapped_column(Integer)
    condition_value: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    mission_reward_id: Mapped[int] = mapped_column(Integer)


class TrialBattleMissionReward(Base):
    __tablename__ = 'trial_battle_mission_reward'
    __table_args__ = (
        Index('trial_battle_mission_reward_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class TrialBattleRewardDatum(Base):
    __tablename__ = 'trial_battle_reward_data'

    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)


class TtkDrama(Base):
    __tablename__ = 'ttk_drama'
    __table_args__ = (
        Index('ttk_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class TtkEnemy(Base):
    __tablename__ = 'ttk_enemy'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    coin: Mapped[int] = mapped_column(Integer)
    max: Mapped[int] = mapped_column(Integer)


class TtkNaviComment(Base):
    __tablename__ = 'ttk_navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    character_name: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)


class TtkReward(Base):
    __tablename__ = 'ttk_reward'
    __table_args__ = (
        Index('ttk_reward_0_ttk_score', 'ttk_score'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ttk_score: Mapped[int] = mapped_column(Integer)
    mission_detail: Mapped[str] = mapped_column(Text)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_count_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_count_5: Mapped[int] = mapped_column(Integer)


class TtkScore(Base):
    __tablename__ = 'ttk_score'

    difficulty_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    coefficient_difficulty: Mapped[int] = mapped_column(Integer)
    coefficient_coin_score: Mapped[int] = mapped_column(Integer)
    life: Mapped[int] = mapped_column(Integer)
    coefficient_wrong_num: Mapped[int] = mapped_column(Integer)


class TtkStory(Base):
    __tablename__ = 'ttk_story'
    __table_args__ = (
        Index('ttk_story_0_ttk_score', 'ttk_score'),
    )

    ttk_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ttk_score: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)


class TtkStoryScript(Base):
    __tablename__ = 'ttk_story_script'
    __table_args__ = (
        Index('ttk_story_script_0_story_id', 'story_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class TtkWeapon(Base):
    __tablename__ = 'ttk_weapon'
    __table_args__ = (
        Index('ttk_weapon_0_ttk_score', 'ttk_score'),
    )

    ttk_weapon_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ttk_score: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)


class UbAutoDatum(Base):
    __tablename__ = 'ub_auto_data'

    ub_auto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auto_type: Mapped[int] = mapped_column(Integer)
    auto_detail_1: Mapped[int] = mapped_column(Integer)
    auto_detail_2: Mapped[int] = mapped_column(Integer)
    auto_detail_3: Mapped[int] = mapped_column(Integer)
    auto_detail_4: Mapped[int] = mapped_column(Integer)
    auto_detail_5: Mapped[int] = mapped_column(Integer)
    auto_value_1: Mapped[int] = mapped_column(Integer)
    auto_value_2: Mapped[int] = mapped_column(Integer)
    auto_value_3: Mapped[int] = mapped_column(Integer)
    auto_value_4: Mapped[int] = mapped_column(Integer)
    auto_value_5: Mapped[int] = mapped_column(Integer)


class UbAutoDefine(Base):
    __tablename__ = 'ub_auto_define'

    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ub_auto_id_1: Mapped[int] = mapped_column(Integer)
    ub_auto_id_2: Mapped[int] = mapped_column(Integer)
    ub_auto_id_3: Mapped[int] = mapped_column(Integer)
    ub_auto_id_4: Mapped[int] = mapped_column(Integer)
    ub_auto_id_5: Mapped[int] = mapped_column(Integer)


class UekBoss(Base):
    __tablename__ = 'uek_boss'
    __table_args__ = (
        Index('uek_boss_0_enemy_id', 'enemy_id'),
    )

    area: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text)
    limit_time: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    background: Mapped[int] = mapped_column(Integer)
    enemy_id: Mapped[int] = mapped_column(Integer)
    bgm_sheet_id: Mapped[str] = mapped_column(Text)
    bgm_que_id: Mapped[str] = mapped_column(Text)
    detail_bg_id: Mapped[int] = mapped_column(Integer)
    detail_bg_position: Mapped[int] = mapped_column(Integer)
    detail_boss_bg_size: Mapped[float] = mapped_column(Float)
    detail_boss_bg_height: Mapped[int] = mapped_column(Integer)
    result_boss_position_y: Mapped[int] = mapped_column(Integer)
    result_movie: Mapped[int] = mapped_column(Integer)


class UekDrama(Base):
    __tablename__ = 'uek_drama'
    __table_args__ = (
        Index('uek_drama_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class UekMission(Base):
    __tablename__ = 'uek_mission'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    mission_condition: Mapped[int] = mapped_column(Integer)
    condition_value_1: Mapped[int] = mapped_column(Integer)
    condition_value_2: Mapped[int] = mapped_column(Integer)
    condition_value_3: Mapped[int] = mapped_column(Integer)
    condition_value_4: Mapped[int] = mapped_column(Integer)
    condition_value_5: Mapped[int] = mapped_column(Integer)
    condition_num: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    reward_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    reward_num_5: Mapped[int] = mapped_column(Integer)
    system_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)


class UekSpineAnimLink(Base):
    __tablename__ = 'uek_spine_anim_link'
    __table_args__ = (
        Index('uek_spine_anim_link_0_anim_num', 'anim_num'),
    )

    spine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    anim_num: Mapped[int] = mapped_column(Integer)


class UniqueEquipConsumeGroup(Base):
    __tablename__ = 'unique_equip_consume_group'
    __table_args__ = (
        Index('unique_equip_consume_group_0_group_id', 'group_id'),
        Index('unique_equip_consume_group_0_item_id', 'item_id', unique=True)
    )

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    index_in_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer)


class UniqueEquipCraftEnhance(Base):
    __tablename__ = 'unique_equip_craft_enhance'
    __table_args__ = (
        Index('unique_equip_craft_enhance_0_consume_group_id', 'consume_group_id'),
    )

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_group_id: Mapped[int] = mapped_column(Integer)


class UniqueEquipEnhanceRate(Base):
    __tablename__ = 'unique_equip_enhance_rate'
    __table_args__ = (
        Index('unique_equip_enhance_rate_0_equipment_id', 'equipment_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(Integer)
    min_lv: Mapped[int] = mapped_column(Integer)
    max_lv: Mapped[int] = mapped_column(Integer)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)


class UniqueEquipmentBonus(Base):
    __tablename__ = 'unique_equipment_bonus'
    __table_args__ = (
        Index('unique_equipment_bonus_0_equipment_id', 'equipment_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(Integer)
    min_lv: Mapped[int] = mapped_column(Integer)
    max_lv: Mapped[int] = mapped_column(Integer)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)


class UniqueEquipmentCraft(Base):
    __tablename__ = 'unique_equipment_craft'

    equip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    crafted_cost: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    item_id_1: Mapped[int] = mapped_column(Integer)
    consume_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    item_id_2: Mapped[int] = mapped_column(Integer)
    consume_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    item_id_3: Mapped[int] = mapped_column(Integer)
    consume_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    item_id_4: Mapped[int] = mapped_column(Integer)
    consume_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    item_id_5: Mapped[int] = mapped_column(Integer)
    consume_num_5: Mapped[int] = mapped_column(Integer)
    reward_type_6: Mapped[int] = mapped_column(Integer)
    item_id_6: Mapped[int] = mapped_column(Integer)
    consume_num_6: Mapped[int] = mapped_column(Integer)
    reward_type_7: Mapped[int] = mapped_column(Integer)
    item_id_7: Mapped[int] = mapped_column(Integer)
    consume_num_7: Mapped[int] = mapped_column(Integer)
    reward_type_8: Mapped[int] = mapped_column(Integer)
    item_id_8: Mapped[int] = mapped_column(Integer)
    consume_num_8: Mapped[int] = mapped_column(Integer)
    reward_type_9: Mapped[int] = mapped_column(Integer)
    item_id_9: Mapped[int] = mapped_column(Integer)
    consume_num_9: Mapped[int] = mapped_column(Integer)
    reward_type_10: Mapped[int] = mapped_column(Integer)
    item_id_10: Mapped[int] = mapped_column(Integer)
    consume_num_10: Mapped[int] = mapped_column(Integer)


class UniqueEquipmentDatum(Base):
    __tablename__ = 'unique_equipment_data'

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    promotion_level: Mapped[int] = mapped_column(Integer)
    craft_flg: Mapped[int] = mapped_column(Integer)
    equipment_enhance_point: Mapped[int] = mapped_column(Integer)
    sale_price: Mapped[int] = mapped_column(Integer)
    require_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    enable_donation: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[float] = mapped_column(Float)


class UniqueEquipmentEnhanceDatum(Base):
    __tablename__ = 'unique_equipment_enhance_data'

    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_point: Mapped[int] = mapped_column(Integer)
    total_point: Mapped[int] = mapped_column(Integer)
    needed_mana: Mapped[int] = mapped_column(Integer)
    rank: Mapped[int] = mapped_column(Integer)


class UniqueEquipmentEnhanceRate(Base):
    __tablename__ = 'unique_equipment_enhance_rate'

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    promotion_level: Mapped[int] = mapped_column(Integer)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)


class UniqueEquipmentRankup(Base):
    __tablename__ = 'unique_equipment_rankup'
    __table_args__ = (
        Index('unique_equipment_rankup_0_equip_id', 'equip_id'),
    )

    equip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_equip_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_level: Mapped[int] = mapped_column(Integer)
    crafted_cost: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    item_id_1: Mapped[int] = mapped_column(Integer)
    consume_num_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    item_id_2: Mapped[int] = mapped_column(Integer)
    consume_num_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    item_id_3: Mapped[int] = mapped_column(Integer)
    consume_num_3: Mapped[int] = mapped_column(Integer)
    reward_type_4: Mapped[int] = mapped_column(Integer)
    item_id_4: Mapped[int] = mapped_column(Integer)
    consume_num_4: Mapped[int] = mapped_column(Integer)
    reward_type_5: Mapped[int] = mapped_column(Integer)
    item_id_5: Mapped[int] = mapped_column(Integer)
    consume_num_5: Mapped[int] = mapped_column(Integer)
    reward_type_6: Mapped[int] = mapped_column(Integer)
    item_id_6: Mapped[int] = mapped_column(Integer)
    consume_num_6: Mapped[int] = mapped_column(Integer)
    reward_type_7: Mapped[int] = mapped_column(Integer)
    item_id_7: Mapped[int] = mapped_column(Integer)
    consume_num_7: Mapped[int] = mapped_column(Integer)
    reward_type_8: Mapped[int] = mapped_column(Integer)
    item_id_8: Mapped[int] = mapped_column(Integer)
    consume_num_8: Mapped[int] = mapped_column(Integer)
    reward_type_9: Mapped[int] = mapped_column(Integer)
    item_id_9: Mapped[int] = mapped_column(Integer)
    consume_num_9: Mapped[int] = mapped_column(Integer)
    reward_type_10: Mapped[int] = mapped_column(Integer)
    item_id_10: Mapped[int] = mapped_column(Integer)
    consume_num_10: Mapped[int] = mapped_column(Integer)


class UnitAttackPattern(Base):
    __tablename__ = 'unit_attack_pattern'

    pattern_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    loop_start: Mapped[int] = mapped_column(Integer)
    loop_end: Mapped[int] = mapped_column(Integer)
    atk_pattern_1: Mapped[int] = mapped_column(Integer)
    atk_pattern_2: Mapped[int] = mapped_column(Integer)
    atk_pattern_3: Mapped[int] = mapped_column(Integer)
    atk_pattern_4: Mapped[int] = mapped_column(Integer)
    atk_pattern_5: Mapped[int] = mapped_column(Integer)
    atk_pattern_6: Mapped[int] = mapped_column(Integer)
    atk_pattern_7: Mapped[int] = mapped_column(Integer)
    atk_pattern_8: Mapped[int] = mapped_column(Integer)
    atk_pattern_9: Mapped[int] = mapped_column(Integer)
    atk_pattern_10: Mapped[int] = mapped_column(Integer)
    atk_pattern_11: Mapped[int] = mapped_column(Integer)
    atk_pattern_12: Mapped[int] = mapped_column(Integer)
    atk_pattern_13: Mapped[int] = mapped_column(Integer)
    atk_pattern_14: Mapped[int] = mapped_column(Integer)
    atk_pattern_15: Mapped[int] = mapped_column(Integer)
    atk_pattern_16: Mapped[int] = mapped_column(Integer)
    atk_pattern_17: Mapped[int] = mapped_column(Integer)
    atk_pattern_18: Mapped[int] = mapped_column(Integer)
    atk_pattern_19: Mapped[int] = mapped_column(Integer)
    atk_pattern_20: Mapped[int] = mapped_column(Integer)


class UnitBackground(Base):
    __tablename__ = 'unit_background'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text)
    bg_id: Mapped[int] = mapped_column(Integer)
    bg_name: Mapped[str] = mapped_column(Text)
    position: Mapped[float] = mapped_column(Float)
    face_type: Mapped[int] = mapped_column(Integer)


class UnitClipSetting(Base):
    __tablename__ = 'unit_clip_setting'

    clip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    center_x: Mapped[int] = mapped_column(Integer)
    size_x: Mapped[int] = mapped_column(Integer)
    softness_x: Mapped[int] = mapped_column(Integer)


class UnitComments(Base):
    __tablename__ = 'unit_comments'
    __table_args__ = (
        Index('unit_comments_0_unit_id', 'unit_id'),
        Index('unit_comments_0_unit_id_1_use_type', 'unit_id', 'use_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    use_type: Mapped[int] = mapped_column(Integer)
    voice_id: Mapped[int] = mapped_column(Integer)
    face_id: Mapped[int] = mapped_column(Integer)
    change_time: Mapped[float] = mapped_column(Float)
    change_face: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    all_comments_flag: Mapped[int] = mapped_column(Integer)
    target_unit_id: Mapped[int] = mapped_column(Integer)
    face_id_2: Mapped[int] = mapped_column(Integer)
    change_time_2: Mapped[float] = mapped_column(Float)
    change_face_2: Mapped[int] = mapped_column(Integer)
    face_id_3: Mapped[int] = mapped_column(Integer)
    change_time_3: Mapped[float] = mapped_column(Float)
    change_face_3: Mapped[int] = mapped_column(Integer)


class UnitConversion(Base):
    __tablename__ = 'unit_conversion'
    __table_args__ = (
        Index('unit_conversion_0_unit_id', 'unit_id', unique=True),
    )

    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)


class UnitDatum(Base):
    __tablename__ = 'unit_data'
    __table_args__ = (
        Index('unit_data_0_original_unit_id', 'original_unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text)
    kana: Mapped[str] = mapped_column(Text)
    prefab_id: Mapped[int] = mapped_column(Integer)
    prefab_id_battle: Mapped[int] = mapped_column(Integer)
    is_limited: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    motion_type: Mapped[int] = mapped_column(Integer)
    se_type: Mapped[int] = mapped_column(Integer)
    move_speed: Mapped[int] = mapped_column(Integer)
    search_area_width: Mapped[int] = mapped_column(Integer)
    atk_type: Mapped[int] = mapped_column(Integer)
    normal_atk_cast_time: Mapped[float] = mapped_column(Float)
    cutin_1: Mapped[int] = mapped_column(Integer)
    cutin_2: Mapped[int] = mapped_column(Integer)
    cutin1_star6: Mapped[int] = mapped_column(Integer)
    cutin2_star6: Mapped[int] = mapped_column(Integer)
    guild_id: Mapped[int] = mapped_column(Integer)
    exskill_display: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    only_disp_owned: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    original_unit_id: Mapped[int] = mapped_column(Integer)


class UnitEnemyDatum(Base):
    __tablename__ = 'unit_enemy_data'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text)
    prefab_id: Mapped[int] = mapped_column(Integer)
    motion_type: Mapped[int] = mapped_column(Integer)
    se_type: Mapped[int] = mapped_column(Integer)
    move_speed: Mapped[int] = mapped_column(Integer)
    search_area_width: Mapped[int] = mapped_column(Integer)
    atk_type: Mapped[int] = mapped_column(Integer)
    normal_atk_cast_time: Mapped[float] = mapped_column(Float)
    cutin: Mapped[int] = mapped_column(Integer)
    cutin_star6: Mapped[int] = mapped_column(Integer)
    visual_change_flag: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)


class UnitExEquipmentSlot(Base):
    __tablename__ = 'unit_ex_equipment_slot'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_category_1: Mapped[int] = mapped_column(Integer)
    slot_category_2: Mapped[int] = mapped_column(Integer)
    slot_category_3: Mapped[int] = mapped_column(Integer)


class UnitIntroduction(Base):
    __tablename__ = 'unit_introduction'
    __table_args__ = (
        Index('unit_introduction_0_gacha_id', 'gacha_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_id: Mapped[int] = mapped_column(Integer)
    introduction_number: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    maximum_chunk_size_1: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_loop_1: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_2: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_loop_2: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_3: Mapped[int] = mapped_column(Integer)
    maximum_chunk_size_loop_3: Mapped[int] = mapped_column(Integer)


class UnitMotionList(Base):
    __tablename__ = 'unit_motion_list'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sp_motion: Mapped[int] = mapped_column(Integer)


class UnitMypagePos(Base):
    __tablename__ = 'unit_mypage_pos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    scale: Mapped[float] = mapped_column(Float)


class UnitPosAdjustment(Base):
    __tablename__ = 'unit_pos_adjustment'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_1: Mapped[int] = mapped_column(Integer)
    id_2: Mapped[int] = mapped_column(Integer)
    id_3: Mapped[int] = mapped_column(Integer)
    home_1_pos_x: Mapped[int] = mapped_column(Integer)
    home_1_pos_y: Mapped[int] = mapped_column(Integer)
    home_1_depth: Mapped[int] = mapped_column(Integer)
    home_1_clip: Mapped[int] = mapped_column(Integer)
    home_2_pos_x: Mapped[int] = mapped_column(Integer)
    home_2_pos_y: Mapped[int] = mapped_column(Integer)
    home_2_depth: Mapped[int] = mapped_column(Integer)
    home_2_clip: Mapped[int] = mapped_column(Integer)
    home_3_pos_x: Mapped[int] = mapped_column(Integer)
    home_3_pos_y: Mapped[int] = mapped_column(Integer)
    home_3_depth: Mapped[int] = mapped_column(Integer)
    home_3_clip: Mapped[int] = mapped_column(Integer)
    profile_1_pos_x: Mapped[int] = mapped_column(Integer)
    profile_1_pos_y: Mapped[int] = mapped_column(Integer)
    profile_1_depth: Mapped[int] = mapped_column(Integer)
    profile_1_scale: Mapped[float] = mapped_column(Float)
    profile_1_clip: Mapped[int] = mapped_column(Integer)
    profile_2_pos_x: Mapped[int] = mapped_column(Integer)
    profile_2_pos_y: Mapped[int] = mapped_column(Integer)
    profile_2_depth: Mapped[int] = mapped_column(Integer)
    profile_2_scale: Mapped[float] = mapped_column(Float)
    profile_2_clip: Mapped[int] = mapped_column(Integer)
    profile_3_pos_x: Mapped[int] = mapped_column(Integer)
    profile_3_pos_y: Mapped[int] = mapped_column(Integer)
    profile_3_depth: Mapped[int] = mapped_column(Integer)
    profile_3_scale: Mapped[float] = mapped_column(Float)
    profile_3_clip: Mapped[int] = mapped_column(Integer)
    actual_id1: Mapped[int] = mapped_column(Integer)
    actual_1_pos_x: Mapped[int] = mapped_column(Integer)
    actual_1_pos_y: Mapped[int] = mapped_column(Integer)
    actual_1_depth: Mapped[int] = mapped_column(Integer)
    actual_1_clip: Mapped[int] = mapped_column(Integer)
    actual_id2: Mapped[int] = mapped_column(Integer)
    actual_2_pos_x: Mapped[int] = mapped_column(Integer)
    actual_2_pos_y: Mapped[int] = mapped_column(Integer)
    actual_2_depth: Mapped[int] = mapped_column(Integer)
    actual_2_clip: Mapped[int] = mapped_column(Integer)
    actual_id3: Mapped[int] = mapped_column(Integer)
    actual_3_pos_x: Mapped[int] = mapped_column(Integer)
    actual_3_pos_y: Mapped[int] = mapped_column(Integer)
    actual_3_depth: Mapped[int] = mapped_column(Integer)
    actual_3_clip: Mapped[int] = mapped_column(Integer)
    skip_position_x: Mapped[int] = mapped_column(Integer)
    friend_pos_x: Mapped[int] = mapped_column(Integer)
    is_myprofile_image: Mapped[int] = mapped_column(Integer)


class UnitProfile(Base):
    __tablename__ = 'unit_profile'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text)
    age: Mapped[str] = mapped_column(Text)
    guild: Mapped[str] = mapped_column(Text)
    race: Mapped[str] = mapped_column(Text)
    height: Mapped[str] = mapped_column(Text)
    weight: Mapped[str] = mapped_column(Text)
    birth_month: Mapped[str] = mapped_column(Text)
    birth_day: Mapped[str] = mapped_column(Text)
    blood_type: Mapped[str] = mapped_column(Text)
    favorite: Mapped[str] = mapped_column(Text)
    voice: Mapped[str] = mapped_column(Text)
    voice_id: Mapped[int] = mapped_column(Integer)
    catch_copy: Mapped[str] = mapped_column(Text)
    self_text: Mapped[str] = mapped_column(Text)
    guild_id: Mapped[str] = mapped_column(Text)


class UnitPromotion(Base):
    __tablename__ = 'unit_promotion'
    __table_args__ = (
        Index('unit_promotion_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot_1: Mapped[int] = mapped_column(Integer)
    equip_slot_2: Mapped[int] = mapped_column(Integer)
    equip_slot_3: Mapped[int] = mapped_column(Integer)
    equip_slot_4: Mapped[int] = mapped_column(Integer)
    equip_slot_5: Mapped[int] = mapped_column(Integer)
    equip_slot_6: Mapped[int] = mapped_column(Integer)


class UnitPromotionStatus(Base):
    __tablename__ = 'unit_promotion_status'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    magic_def: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)


class UnitRarity(Base):
    __tablename__ = 'unit_rarity'
    __table_args__ = (
        Index('unit_rarity_0_unit_id', 'unit_id'),
        Index('unit_rarity_0_unit_material_id', 'unit_material_id')
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp: Mapped[float] = mapped_column(Float)
    hp_growth: Mapped[float] = mapped_column(Float)
    atk: Mapped[float] = mapped_column(Float)
    atk_growth: Mapped[float] = mapped_column(Float)
    magic_str: Mapped[float] = mapped_column(Float)
    magic_str_growth: Mapped[float] = mapped_column(Float)
    def_: Mapped[float] = mapped_column('def', Float)
    def_growth: Mapped[float] = mapped_column(Float)
    magic_def: Mapped[float] = mapped_column(Float)
    magic_def_growth: Mapped[float] = mapped_column(Float)
    physical_critical: Mapped[float] = mapped_column(Float)
    physical_critical_growth: Mapped[float] = mapped_column(Float)
    magic_critical: Mapped[float] = mapped_column(Float)
    magic_critical_growth: Mapped[float] = mapped_column(Float)
    wave_hp_recovery: Mapped[float] = mapped_column(Float)
    wave_hp_recovery_growth: Mapped[float] = mapped_column(Float)
    wave_energy_recovery: Mapped[float] = mapped_column(Float)
    wave_energy_recovery_growth: Mapped[float] = mapped_column(Float)
    dodge: Mapped[float] = mapped_column(Float)
    dodge_growth: Mapped[float] = mapped_column(Float)
    physical_penetrate: Mapped[float] = mapped_column(Float)
    physical_penetrate_growth: Mapped[float] = mapped_column(Float)
    magic_penetrate: Mapped[float] = mapped_column(Float)
    magic_penetrate_growth: Mapped[float] = mapped_column(Float)
    life_steal: Mapped[float] = mapped_column(Float)
    life_steal_growth: Mapped[float] = mapped_column(Float)
    hp_recovery_rate: Mapped[float] = mapped_column(Float)
    hp_recovery_rate_growth: Mapped[float] = mapped_column(Float)
    energy_recovery_rate: Mapped[float] = mapped_column(Float)
    energy_recovery_rate_growth: Mapped[float] = mapped_column(Float)
    energy_reduce_rate: Mapped[float] = mapped_column(Float)
    energy_reduce_rate_growth: Mapped[float] = mapped_column(Float)
    unit_material_id: Mapped[int] = mapped_column(Integer)
    consume_num: Mapped[int] = mapped_column(Integer)
    consume_gold: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[float] = mapped_column(Float)
    accuracy_growth: Mapped[float] = mapped_column(Float)


class UnitSkillDatum(Base):
    __tablename__ = 'unit_skill_data'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    union_burst: Mapped[int] = mapped_column(Integer)
    main_skill_1: Mapped[int] = mapped_column(Integer)
    main_skill_2: Mapped[int] = mapped_column(Integer)
    main_skill_3: Mapped[int] = mapped_column(Integer)
    main_skill_4: Mapped[int] = mapped_column(Integer)
    main_skill_5: Mapped[int] = mapped_column(Integer)
    main_skill_6: Mapped[int] = mapped_column(Integer)
    main_skill_7: Mapped[int] = mapped_column(Integer)
    main_skill_8: Mapped[int] = mapped_column(Integer)
    main_skill_9: Mapped[int] = mapped_column(Integer)
    main_skill_10: Mapped[int] = mapped_column(Integer)
    ex_skill_1: Mapped[int] = mapped_column(Integer)
    ex_skill_evolution_1: Mapped[int] = mapped_column(Integer)
    ex_skill_2: Mapped[int] = mapped_column(Integer)
    ex_skill_evolution_2: Mapped[int] = mapped_column(Integer)
    ex_skill_3: Mapped[int] = mapped_column(Integer)
    ex_skill_evolution_3: Mapped[int] = mapped_column(Integer)
    ex_skill_4: Mapped[int] = mapped_column(Integer)
    ex_skill_evolution_4: Mapped[int] = mapped_column(Integer)
    ex_skill_5: Mapped[int] = mapped_column(Integer)
    ex_skill_evolution_5: Mapped[int] = mapped_column(Integer)
    sp_union_burst: Mapped[int] = mapped_column(Integer)
    sp_skill_1: Mapped[int] = mapped_column(Integer)
    sp_skill_2: Mapped[int] = mapped_column(Integer)
    sp_skill_3: Mapped[int] = mapped_column(Integer)
    sp_skill_4: Mapped[int] = mapped_column(Integer)
    sp_skill_5: Mapped[int] = mapped_column(Integer)
    union_burst_evolution: Mapped[int] = mapped_column(Integer)
    main_skill_evolution_1: Mapped[int] = mapped_column(Integer)
    main_skill_evolution_2: Mapped[int] = mapped_column(Integer)
    sp_skill_evolution_1: Mapped[int] = mapped_column(Integer)
    sp_skill_evolution_2: Mapped[int] = mapped_column(Integer)


class UnitSkillDataRf(Base):
    __tablename__ = 'unit_skill_data_rf'
    __table_args__ = (
        Index('unit_skill_data_rf_0_rf_skill_id', 'rf_skill_id'),
        Index('unit_skill_data_rf_0_skill_id', 'skill_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(Integer)
    rf_skill_id: Mapped[int] = mapped_column(Integer)
    min_lv: Mapped[int] = mapped_column(Integer)
    max_lv: Mapped[int] = mapped_column(Integer)


class UnitStatusCoefficient(Base):
    __tablename__ = 'unit_status_coefficient'

    coefficient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp_coefficient: Mapped[float] = mapped_column(Float)
    atk_coefficient: Mapped[float] = mapped_column(Float)
    magic_str_coefficient: Mapped[float] = mapped_column(Float)
    def_coefficient: Mapped[float] = mapped_column(Float)
    magic_def_coefficient: Mapped[float] = mapped_column(Float)
    physical_critical_coefficient: Mapped[float] = mapped_column(Float)
    magic_critical_coefficient: Mapped[float] = mapped_column(Float)
    wave_hp_recovery_coefficient: Mapped[float] = mapped_column(Float)
    wave_energy_recovery_coefficient: Mapped[float] = mapped_column(Float)
    dodge_coefficient: Mapped[float] = mapped_column(Float)
    physical_penetrate_coefficient: Mapped[float] = mapped_column(Float)
    magic_penetrate_coefficient: Mapped[float] = mapped_column(Float)
    life_steal_coefficient: Mapped[float] = mapped_column(Float)
    hp_recovery_rate_coefficient: Mapped[float] = mapped_column(Float)
    energy_recovery_rate_coefficient: Mapped[float] = mapped_column(Float)
    energy_reduce_rate_coefficient: Mapped[float] = mapped_column(Float)
    skill_lv_coefficient: Mapped[float] = mapped_column(Float)
    exskill_evolution_coefficient: Mapped[int] = mapped_column(Integer)
    overall_coefficient: Mapped[float] = mapped_column(Float)
    accuracy_coefficient: Mapped[float] = mapped_column(Float)
    skill1_evolution_coefficient: Mapped[int] = mapped_column(Integer)
    skill1_evolution_slv_coefficient: Mapped[float] = mapped_column(Float)
    skill2_evolution_coefficient: Mapped[int] = mapped_column(Integer)
    skill2_evolution_slv_coefficient: Mapped[float] = mapped_column(Float)
    ub_evolution_coefficient: Mapped[int] = mapped_column(Integer)
    ub_evolution_slv_coefficient: Mapped[float] = mapped_column(Float)


class UnitUniqueEquip(Base):
    __tablename__ = 'unit_unique_equip'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot: Mapped[int] = mapped_column(Integer)
    equip_id: Mapped[int] = mapped_column(Integer)


class UnitUniqueEquipment(Base):
    __tablename__ = 'unit_unique_equipment'
    __table_args__ = (
        Index('unit_unique_equipment_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_id: Mapped[int] = mapped_column(Integer)


class UnlockRarity6(Base):
    __tablename__ = 'unlock_rarity_6'
    __table_args__ = (
        Index('unlock_rarity_6_0_material_id', 'material_id'),
        Index('unlock_rarity_6_0_unit_id', 'unit_id'),
        Index('unlock_rarity_6_0_unit_id_1_slot_id', 'unit_id', 'slot_id'),
        Index('unlock_rarity_6_0_unit_id_1_unlock_level', 'unit_id', 'unlock_level')
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_flag: Mapped[int] = mapped_column(Integer)
    consume_gold: Mapped[int] = mapped_column(Integer)
    material_type: Mapped[int] = mapped_column(Integer)
    material_id: Mapped[int] = mapped_column(Integer)
    material_count: Mapped[int] = mapped_column(Integer)
    hp: Mapped[int] = mapped_column(Integer)
    atk: Mapped[int] = mapped_column(Integer)
    magic_str: Mapped[int] = mapped_column(Integer)
    def_: Mapped[int] = mapped_column('def', Integer)
    magic_def: Mapped[int] = mapped_column(Integer)
    physical_critical: Mapped[int] = mapped_column(Integer)
    magic_critical: Mapped[int] = mapped_column(Integer)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer)
    dodge: Mapped[int] = mapped_column(Integer)
    physical_penetrate: Mapped[int] = mapped_column(Integer)
    magic_penetrate: Mapped[int] = mapped_column(Integer)
    life_steal: Mapped[int] = mapped_column(Integer)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)


class UnlockSkillDatum(Base):
    __tablename__ = 'unlock_skill_data'

    promotion_level: Mapped[int] = mapped_column(Integer)
    unlock_skill: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnlockUnitCondition(Base):
    __tablename__ = 'unlock_unit_condition'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text)
    class_id: Mapped[int] = mapped_column(Integer)
    pre_unit_id: Mapped[int] = mapped_column(Integer)
    condition_type_1: Mapped[int] = mapped_column(Integer)
    condition_type_detail_1: Mapped[int] = mapped_column(Integer)
    condition_id_1: Mapped[int] = mapped_column(Integer)
    count_1: Mapped[int] = mapped_column(Integer)
    condition_type_2: Mapped[int] = mapped_column(Integer)
    condition_type_detail_2: Mapped[int] = mapped_column(Integer)
    condition_id_2: Mapped[int] = mapped_column(Integer)
    count_2: Mapped[int] = mapped_column(Integer)
    condition_type_3: Mapped[int] = mapped_column(Integer)
    condition_type_detail_3: Mapped[int] = mapped_column(Integer)
    condition_id_3: Mapped[int] = mapped_column(Integer)
    count_3: Mapped[int] = mapped_column(Integer)
    condition_type_4: Mapped[int] = mapped_column(Integer)
    condition_type_detail_4: Mapped[int] = mapped_column(Integer)
    condition_id_4: Mapped[int] = mapped_column(Integer)
    count_4: Mapped[int] = mapped_column(Integer)
    condition_type_5: Mapped[int] = mapped_column(Integer)
    condition_type_detail_5: Mapped[int] = mapped_column(Integer)
    condition_id_5: Mapped[int] = mapped_column(Integer)
    count_5: Mapped[int] = mapped_column(Integer)
    release_effect_type: Mapped[int] = mapped_column(Integer)


class VisualCustomize(Base):
    __tablename__ = 'visual_customize'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_prefab: Mapped[int] = mapped_column(Integer)
    title_movie: Mapped[int] = mapped_column(Integer)
    title_voice: Mapped[int] = mapped_column(Integer)
    story_top_movie: Mapped[int] = mapped_column(Integer)
    quest_top_movie: Mapped[int] = mapped_column(Integer)
    profile_logo: Mapped[int] = mapped_column(Integer)
    watched_story_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class VoiceGroup(Base):
    __tablename__ = 'voice_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id_comment: Mapped[str] = mapped_column(Text)
    group_unit_id_01: Mapped[int] = mapped_column(Integer)
    group_unit_id_02: Mapped[int] = mapped_column(Integer)
    group_unit_id_03: Mapped[int] = mapped_column(Integer)
    group_unit_id_04: Mapped[int] = mapped_column(Integer)
    group_unit_id_05: Mapped[int] = mapped_column(Integer)


class VoiceGroupChara(Base):
    __tablename__ = 'voice_group_chara'

    group_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_unit_id_comment: Mapped[str] = mapped_column(Text)
    unit_id_01: Mapped[int] = mapped_column(Integer)
    unit_id_02: Mapped[int] = mapped_column(Integer)
    unit_id_03: Mapped[int] = mapped_column(Integer)
    unit_id_04: Mapped[int] = mapped_column(Integer)
    unit_id_05: Mapped[int] = mapped_column(Integer)
    unit_id_06: Mapped[int] = mapped_column(Integer)
    unit_id_07: Mapped[int] = mapped_column(Integer)
    unit_id_08: Mapped[int] = mapped_column(Integer)
    unit_id_09: Mapped[int] = mapped_column(Integer)
    unit_id_10: Mapped[int] = mapped_column(Integer)


class VoteDatum(Base):
    __tablename__ = 'vote_data'

    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_start_time: Mapped[str] = mapped_column(Text)
    vote_end_time: Mapped[str] = mapped_column(Text)
    result_start_time: Mapped[str] = mapped_column(Text)
    result_end_time: Mapped[str] = mapped_column(Text)
    start_story_id: Mapped[int] = mapped_column(Integer)
    result_story_id: Mapped[int] = mapped_column(Integer)


class VoteInfo(Base):
    __tablename__ = 'vote_info'

    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_help_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_title: Mapped[str] = mapped_column(Text)
    vote_help: Mapped[str] = mapped_column(Text)


class VoteUnit(Base):
    __tablename__ = 'vote_unit'

    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_rarity: Mapped[int] = mapped_column(Integer)


class WacBirthdayDramaScript(Base):
    __tablename__ = 'wac_birthday_drama_script'
    __table_args__ = (
        Index('wac_birthday_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class WacDatum(Base):
    __tablename__ = 'wac_data'
    __table_args__ = (
        Index('wac_data_0_mural_group_id', 'mural_group_id'),
    )

    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_time: Mapped[str] = mapped_column(Text)
    pre_drama_id: Mapped[int] = mapped_column(Integer)
    post_drama_id: Mapped[int] = mapped_column(Integer)
    idle_drama_id: Mapped[int] = mapped_column(Integer)
    bg_id: Mapped[int] = mapped_column(Integer)
    effect_id: Mapped[int] = mapped_column(Integer)
    mural_group_id: Mapped[int] = mapped_column(Integer)
    mural_offset_x: Mapped[float] = mapped_column(Float)
    birthday_login_bonus_id: Mapped[int] = mapped_column(Integer)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    draw_end_to_center: Mapped[int] = mapped_column(Integer)
    unit_search_id: Mapped[int] = mapped_column(Integer)


class WacDramaScript(Base):
    __tablename__ = 'wac_drama_script'
    __table_args__ = (
        Index('wac_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer)
    command_type: Mapped[int] = mapped_column(Integer)
    param_01: Mapped[str] = mapped_column(Text)
    param_02: Mapped[str] = mapped_column(Text)
    param_03: Mapped[str] = mapped_column(Text)
    param_04: Mapped[str] = mapped_column(Text)
    param_05: Mapped[str] = mapped_column(Text)
    param_06: Mapped[str] = mapped_column(Text)
    param_07: Mapped[str] = mapped_column(Text)
    param_08: Mapped[str] = mapped_column(Text)


class WacMuralBgDatum(Base):
    __tablename__ = 'wac_mural_bg_data'

    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    start_offset_x: Mapped[str] = mapped_column(Text)
    end_offset_x: Mapped[str] = mapped_column(Text)


class WacMuralDatum(Base):
    __tablename__ = 'wac_mural_data'
    __table_args__ = (
        Index('wac_mural_data_0_mural_group_id', 'mural_group_id'),
    )

    mural_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parts_id: Mapped[int] = mapped_column(Integer)
    pos_x: Mapped[int] = mapped_column(Integer)
    pos_y: Mapped[int] = mapped_column(Integer)
    depth: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)


class WacPresentStillDatum(Base):
    __tablename__ = 'wac_present_still_data'

    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    still_id: Mapped[int] = mapped_column(Integer)


class WacUnitSearchDatum(Base):
    __tablename__ = 'wac_unit_search_data'
    __table_args__ = (
        Index('wac_unit_search_data_0_unit_id', 'unit_id'),
        Index('wac_unit_search_data_0_unit_search_id', 'unit_search_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_search_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)


class WaveGroupDatum(Base):
    __tablename__ = 'wave_group_data'
    __table_args__ = (
        Index('wave_group_data_0_wave_group_id', 'wave_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    odds: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    drop_gold_1: Mapped[int] = mapped_column(Integer)
    drop_reward_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    drop_gold_2: Mapped[int] = mapped_column(Integer)
    drop_reward_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    drop_gold_3: Mapped[int] = mapped_column(Integer)
    drop_reward_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    drop_gold_4: Mapped[int] = mapped_column(Integer)
    drop_reward_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    drop_gold_5: Mapped[int] = mapped_column(Integer)
    drop_reward_id_5: Mapped[int] = mapped_column(Integer)
    guest_enemy_id: Mapped[int] = mapped_column(Integer)
    guest_lane: Mapped[int] = mapped_column(Integer)


class WonStoryDatum(Base):
    __tablename__ = 'won_story_data'
    __table_args__ = (
        Index('won_story_data_0_note_id', 'note_id'),
        Index('won_story_data_0_original_event_id', 'original_event_id'),
        Index('won_story_data_0_unit_id_1_is_last', 'unit_id', 'is_last')
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    is_last: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    note_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)
    order: Mapped[int] = mapped_column(Integer)


class WonStoryScript(Base):
    __tablename__ = 'won_story_script'
    __table_args__ = (
        Index('won_story_script_0_story_id', 'story_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    seq_num: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    line_num: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    seek_time: Mapped[float] = mapped_column(Float)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    command: Mapped[int] = mapped_column(Integer)
    command_param: Mapped[float] = mapped_column(Float)


class Worldmap(Base):
    __tablename__ = 'worldmap'
    __table_args__ = (
        Index('worldmap_0_map_type', 'map_type'),
    )

    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    map_id: Mapped[int] = mapped_column(Integer)
    map_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    start_area_id: Mapped[int] = mapped_column(Integer)
    end_area_id: Mapped[int] = mapped_column(Integer)
    view_mode: Mapped[int] = mapped_column(Integer)
    tutorial_adv_id: Mapped[int] = mapped_column(Integer)


class WtmStoryDatum(Base):
    __tablename__ = 'wtm_story_data'
    __table_args__ = (
        Index('wtm_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    wtm_story_type: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_sub_story_id_1: Mapped[int] = mapped_column(Integer)
    condition_sub_story_id_2: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    emblem_id: Mapped[int] = mapped_column(Integer)


class WtsNaviComment(Base):
    __tablename__ = 'wts_navi_comment'
    __table_args__ = (
        Index('wts_navi_comment_0_where_type', 'where_type'),
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer)
    character_id: Mapped[int] = mapped_column(Integer)
    face_type: Mapped[int] = mapped_column(Integer)
    voice_id: Mapped[int] = mapped_column(Integer)
    pos_x: Mapped[float] = mapped_column(Float)
    pos_y: Mapped[float] = mapped_column(Float)
    change_face_time: Mapped[float] = mapped_column(Float)
    change_face_type: Mapped[int] = mapped_column(Integer)
    original_event_id: Mapped[int] = mapped_column(Integer)


class WtsStoryDatum(Base):
    __tablename__ = 'wts_story_data'
    __table_args__ = (
        Index('wts_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repeat_story_id: Mapped[int] = mapped_column(Integer)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class XehStoryDatum(Base):
    __tablename__ = 'xeh_story_data'
    __table_args__ = (
        Index('xeh_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class YsnStoryDatum(Base):
    __tablename__ = 'ysn_story_data'
    __table_args__ = (
        Index('ysn_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)
    reward_type_1: Mapped[int] = mapped_column(Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    reward_count_1: Mapped[int] = mapped_column(Integer)
    reward_type_2: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    reward_count_2: Mapped[int] = mapped_column(Integer)
    reward_type_3: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    reward_count_3: Mapped[int] = mapped_column(Integer)
