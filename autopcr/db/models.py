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
    _760c9cb243e3777bbfd48b82961efc56e4aacb44d7bd8d98f624eb808665991f: Mapped[str] = mapped_column('760c9cb243e3777bbfd48b82961efc56e4aacb44d7bd8d98f624eb808665991f', Text)


class AisSetting(Base):
    __tablename__ = 'ais_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_op_sub_story_id: Mapped[int] = mapped_column(Integer)
    first_op_release_condition_story_id: Mapped[int] = mapped_column(Integer)
    later_op_sub_story_id: Mapped[int] = mapped_column(Integer)
    later_op_release_condition_quest_id: Mapped[int] = mapped_column(Integer)
    later_op_release_condition_boss_id: Mapped[int] = mapped_column(Integer)
    last_sub_story_id: Mapped[int] = mapped_column(Integer)


class AisStoryDatum(Base):
    __tablename__ = 'ais_story_data'

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    unlock_condition_sub_story_id: Mapped[int] = mapped_column(Integer)
    read_condition_story_id: Mapped[int] = mapped_column(Integer)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class AlbumProductionList(Base):
    __tablename__ = 'album_production_list'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class AlbumVoiceList(Base):
    __tablename__ = 'album_voice_list'

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


class AsbDramaScript(Base):
    __tablename__ = 'asb_drama_script'

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


class AsbStoryDatum(Base):
    __tablename__ = 'asb_story_data'

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    contents_type: Mapped[int] = mapped_column(Integer)
    page_num: Mapped[int] = mapped_column(Integer)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer)
    read_condition_time: Mapped[str] = mapped_column(Text)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    emblem_id: Mapped[int] = mapped_column(Integer)


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

    archive_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_detail: Mapped[str] = mapped_column(Text)
    emblem_id: Mapped[int] = mapped_column(Integer)


class AsmDatum(Base):
    __tablename__ = 'asm_data'

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

    gauge_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trigger_score: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_detail: Mapped[str] = mapped_column(Text)
    unlock_story_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class AsmReactionDatum(Base):
    __tablename__ = 'asm_reaction_data'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class BirthdayLoginBonusDramaScript(Base):
    __tablename__ = 'birthday_login_bonus_drama_script'

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

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_category: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    consume_num: Mapped[int] = mapped_column(Integer)


class BywayQuestDatum(Base):
    __tablename__ = 'byway_quest_data'

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

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_type: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    visible_type: Mapped[int] = mapped_column(Integer)
    pre_story_id: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    lock_all_text: Mapped[int] = mapped_column(Integer)
    can_bookmark: Mapped[int] = mapped_column(Integer)
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
    _3a64499252a3513c4cbfa42757ed104864e7b4594a06facfaf3a11d432ca96a3: Mapped[int] = mapped_column('3a64499252a3513c4cbfa42757ed104864e7b4594a06facfaf3a11d432ca96a3', Integer)
    c7268ece545ee37f8904e4571c509340e98e7bc726d560c4146089766e1c5084: Mapped[int] = mapped_column(Integer)


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    lv_from: Mapped[int] = mapped_column(Integer)
    lv_to: Mapped[int] = mapped_column(Integer)


class CampaignMissionDatum(Base):
    __tablename__ = 'campaign_mission_data'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shiori_group_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer)


class CaravanBuddy(Base):
    __tablename__ = 'caravan_buddy'

    buddy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    effect_description1: Mapped[str] = mapped_column(Text)
    effect_description2: Mapped[str] = mapped_column(Text)
    effect_type: Mapped[int] = mapped_column(Integer)
    effect_value_1: Mapped[int] = mapped_column(Integer)
    effect_value_2: Mapped[int] = mapped_column(Integer)
    effect_turn: Mapped[int] = mapped_column(Integer)


class CaravanBuffDisp(Base):
    __tablename__ = 'caravan_buff_disp'

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

    season_id: Mapped[int] = mapped_column(Integer)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    currency_id: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    stock: Mapped[int] = mapped_column(Integer)


class CaravanDicePattern(Base):
    __tablename__ = 'caravan_dice_pattern'

    dice_odds: Mapped[int] = mapped_column(Integer, primary_key=True)
    pattern: Mapped[int] = mapped_column(Integer)


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scene_type: Mapped[int] = mapped_column(Integer)
    effect_type: Mapped[int] = mapped_column(Integer)
    rank: Mapped[int] = mapped_column(Integer)
    value: Mapped[int] = mapped_column(Integer)


class CaravanEventEffect(Base):
    __tablename__ = 'caravan_event_effect'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _6432219f9578ab1b27c56f7e9697bc5f92fa29153b95e04fddc39a9beca0a341: Mapped[str] = mapped_column('6432219f9578ab1b27c56f7e9697bc5f92fa29153b95e04fddc39a9beca0a341', Text)
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

    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer)
    next_1: Mapped[int] = mapped_column(Integer)
    next_2: Mapped[int] = mapped_column(Integer)
    next_3: Mapped[int] = mapped_column(Integer)
    next_4: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    reference_id: Mapped[int] = mapped_column(Integer)
    pre_1: Mapped[int] = mapped_column(Integer)
    pre_2: Mapped[int] = mapped_column(Integer)
    pre_3: Mapped[int] = mapped_column(Integer)
    pre_4: Mapped[int] = mapped_column(Integer)
    distance_to_goal: Mapped[int] = mapped_column(Integer)


class CaravanMapLayout(Base):
    __tablename__ = 'caravan_map_layout'

    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[int] = mapped_column(Integer)
    position_y: Mapped[int] = mapped_column(Integer)


class CaravanMapObject(Base):
    __tablename__ = 'caravan_map_object'

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


class CaravanRival(Base):
    __tablename__ = 'caravan_rival'

    rival_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    dice_odds: Mapped[int] = mapped_column(Integer)
    unit_id_1: Mapped[int] = mapped_column(Integer)
    unit_id_2: Mapped[int] = mapped_column(Integer)
    unit_id_3: Mapped[int] = mapped_column(Integer)
    bgm_sheet_id: Mapped[str] = mapped_column(Text)
    bgm_que_id: Mapped[str] = mapped_column(Text)


class CaravanRivalBonus(Base):
    __tablename__ = 'caravan_rival_bonus'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer)
    level: Mapped[int] = mapped_column(Integer)
    bonus_label: Mapped[int] = mapped_column(Integer)
    distance_from: Mapped[int] = mapped_column(Integer)
    distance_to: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)
    label_text: Mapped[str] = mapped_column(Text)


class CaravanRivalMinigameList(Base):
    __tablename__ = 'caravan_rival_minigame_list'

    rival_minigame_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rival_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)


class CaravanSchedule(Base):
    __tablename__ = 'caravan_schedule'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scene_type: Mapped[int] = mapped_column(Integer)
    effect_type: Mapped[int] = mapped_column(Integer)
    sound_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)


class CaravanTreasure(Base):
    __tablename__ = 'caravan_treasure'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class CccBsScenarioList(Base):
    __tablename__ = 'ccc_bs_scenario_list'

    ccc_scenario_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CccChara(Base):
    __tablename__ = 'ccc_chara'

    ccc_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[float] = mapped_column(Float)
    end_time: Mapped[float] = mapped_column(Float)


class CccCharaDatum(Base):
    __tablename__ = 'ccc_chara_data'

    ccc_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class CccDropGroupDatum(Base):
    __tablename__ = 'ccc_drop_group_data'

    drop_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    object_id_1: Mapped[int] = mapped_column(Integer)
    object_num_1: Mapped[int] = mapped_column(Integer)
    drop_type_1: Mapped[int] = mapped_column(Integer)
    object_id_2: Mapped[int] = mapped_column(Integer)
    object_num_2: Mapped[int] = mapped_column(Integer)
    drop_type_2: Mapped[int] = mapped_column(Integer)
    object_id_3: Mapped[int] = mapped_column(Integer)
    object_num_3: Mapped[int] = mapped_column(Integer)
    drop_type_3: Mapped[int] = mapped_column(Integer)


class CccObject(Base):
    __tablename__ = 'ccc_object'

    ccc_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_id: Mapped[int] = mapped_column(Integer)
    is_report: Mapped[int] = mapped_column(Integer)
    ccc_object_type: Mapped[int] = mapped_column(Integer)
    fall_speed: Mapped[int] = mapped_column(Integer)
    absorb_frame: Mapped[int] = mapped_column(Integer)
    value_1: Mapped[int] = mapped_column(Integer)
    value_2: Mapped[int] = mapped_column(Integer)


class CccScenario(Base):
    __tablename__ = 'ccc_scenario'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class CggDrama(Base):
    __tablename__ = 'cgg_drama'

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

    gacha_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgg_id: Mapped[int] = mapped_column(Integer)
    gacha_name: Mapped[str] = mapped_column(Text)
    gacha_description: Mapped[str] = mapped_column(Text)
    cost_currency_num: Mapped[int] = mapped_column(Integer)
    gacha_intro: Mapped[str] = mapped_column(Text)


class CggGachaLineup(Base):
    __tablename__ = 'cgg_gacha_lineup'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_type: Mapped[int] = mapped_column(Integer)
    lineup_id: Mapped[int] = mapped_column(Integer)
    goods_id: Mapped[int] = mapped_column(Integer)
    goods_num: Mapped[int] = mapped_column(Integer)


class CggGameSettings(Base):
    __tablename__ = 'cgg_game_settings'

    cgg_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goods_shelf_id: Mapped[int] = mapped_column(Integer)
    a2c9a9c120a81cca2d24deb393029276d97977e4e9d153014bc0a7ac6f4e0801: Mapped[int] = mapped_column(Integer)
    cgg_gacha_currency_id: Mapped[int] = mapped_column(Integer)
    _1845e3d8d4e42fefda930e6e55995f94e55f3735796e2d93c8bb1e95a2166e92: Mapped[int] = mapped_column('1845e3d8d4e42fefda930e6e55995f94e55f3735796e2d93c8bb1e95a2166e92', Integer)
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
    b85cf2a4cc214978c276e702984c3dca690885a6fa356e1fd523f751c357e084: Mapped[int] = mapped_column(Integer)
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
    b088c8e211150b9f414306903d41cc772a221cc1fd78d118def49af9c8a3a446: Mapped[int] = mapped_column(Integer)
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
    a37d3a340fe662d4147392da376de255cb91e968f92e273961e07df06b53b535: Mapped[str] = mapped_column(Text)
    c241d9c35575f999ab9495f46b7b11a23e6432858150c8974f353c86f454a922: Mapped[str] = mapped_column(Text)
    _98bf615e18d24a727576eebc6d26e9d34e527132bea89621d8da851b64b14072: Mapped[str] = mapped_column('98bf615e18d24a727576eebc6d26e9d34e527132bea89621d8da851b64b14072', Text)


class ClanBattleTrainingDatum(Base):
    __tablename__ = 'clan_battle_training_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    training_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[int] = mapped_column(Integer)
    phase: Mapped[int] = mapped_column(Integer)
    map_data_id: Mapped[int] = mapped_column(Integer)


class ClanBattleTrainingSchedule(Base):
    __tablename__ = 'clan_battle_training_schedule'

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
    de62a8a9d3d70ec02c533da10e972c15f15f9b53b10135524a9ac9ce0390e5c7: Mapped[str] = mapped_column(Text)
    a0eede0529d72aab45a9f1959ab6cb91189b9c67b5b745db80b668237fcd476e: Mapped[str] = mapped_column(Text)


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
    _772bad40b2195f2ac6b761e4f89384f656e2bc5a1c925068e27a4951b336948d: Mapped[int] = mapped_column('772bad40b2195f2ac6b761e4f89384f656e2bc5a1c925068e27a4951b336948d', Integer)
    b75d348f016e5fa1ec247c348619a01f68affc3b0550574e8d640ae98e9f74e9: Mapped[int] = mapped_column(Integer)
    _53b3934ed2058cb51421b9ec87e9083c566eecfd2f9ae3e2ba91e645d2c3c350: Mapped[int] = mapped_column('53b3934ed2058cb51421b9ec87e9083c566eecfd2f9ae3e2ba91e645d2c3c350', Integer)
    e585e1e10985a4d61b9040f95511f7471a7150530c658da852f15aa555fc4acc: Mapped[int] = mapped_column(Integer)
    _76690757bfc3437e611020930ed815ec709fad6b11d1660e5aec166153070c54: Mapped[int] = mapped_column('76690757bfc3437e611020930ed815ec709fad6b11d1660e5aec166153070c54', Integer)
    c84c84a07e42ee60059c0907b87f538e3b4384b67cf2a5847a4f261135840b12: Mapped[int] = mapped_column(Integer)
    _7fe25621f885a62f575868427b0419f6f8ce9ec1cdeb68c3fce97cfe9e20f395: Mapped[int] = mapped_column('7fe25621f885a62f575868427b0419f6f8ce9ec1cdeb68c3fce97cfe9e20f395', Integer)
    abc395e1a5b9ca61b4cd960917e94a08944925b053abcd77b3fc14f8da800a79: Mapped[int] = mapped_column(Integer)
    d8d4d25445c3fd34abbac46e899526f1fdaadfd418e22f278f010b942ea350c9: Mapped[int] = mapped_column(Integer)
    _48c386ac01cff557eff19a5d89840b3ce7c807b9e38d61621b6f0e9a33cbeeb2: Mapped[int] = mapped_column('48c386ac01cff557eff19a5d89840b3ce7c807b9e38d61621b6f0e9a33cbeeb2', Integer)
    c263eeea2d9dfd8654300d96683356e56d8bb99f50329056307d331b7e46d3a5: Mapped[int] = mapped_column(Integer)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer)
    a2237ff345e1526121f23949496b5a45b02e2d1320e34270bf89c4f5a33d62cf: Mapped[str] = mapped_column(Text)
    _383ad1deede8a20a0614044cfb2d8246fc49a3cb87e17728e2b83051a1e38838: Mapped[str] = mapped_column('383ad1deede8a20a0614044cfb2d8246fc49a3cb87e17728e2b83051a1e38838', Text)


class DungeonPatternBattle(Base):
    __tablename__ = 'dungeon_pattern_battle'

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

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_area_id: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    quest_type: Mapped[int] = mapped_column(Integer)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    limit_time: Mapped[int] = mapped_column(Integer)
    fa8c1660ccb2df9f7714b7841f6e6d88daae998a1d8a28f6e8e0bb803f979023: Mapped[float] = mapped_column(Float)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer)
    energy_reset_flag: Mapped[int] = mapped_column(Integer)
    emax: Mapped[int] = mapped_column(Integer)
    reward_image_1: Mapped[int] = mapped_column(Integer)
    reward_image_2: Mapped[int] = mapped_column(Integer)
    reward_image_3: Mapped[int] = mapped_column(Integer)
    reward_image_4: Mapped[int] = mapped_column(Integer)
    reward_image_5: Mapped[int] = mapped_column(Integer)
    reward_image_6: Mapped[int] = mapped_column(Integer)
    _6feb2487bd68df5f29b2499dcfb27f42c8c69571bd4ac874de2d2c19bea200fe: Mapped[int] = mapped_column('6feb2487bd68df5f29b2499dcfb27f42c8c69571bd4ac874de2d2c19bea200fe', Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    _3f61eaac9a9e6528d0fde628e4b03fbb70cc276abc3508c3768c2e94ea43772d: Mapped[int] = mapped_column('3f61eaac9a9e6528d0fde628e4b03fbb70cc276abc3508c3768c2e94ea43772d', Integer)
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

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    detail_title: Mapped[str] = mapped_column(Text)
    detail_description: Mapped[str] = mapped_column(Text)
    dvs_story_type: Mapped[int] = mapped_column(Integer)
    _2479ee29a87aa1a46657d26aaac31007018239a4a68cd790d5740b2dae6bac7e: Mapped[int] = mapped_column('2479ee29a87aa1a46657d26aaac31007018239a4a68cd790d5740b2dae6bac7e', Integer)
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
    _2871669de0c81b9fb035a5d07cbef3b5d66f730e08bdccec68be09931b66f8c8: Mapped[str] = mapped_column('2871669de0c81b9fb035a5d07cbef3b5d66f730e08bdccec68be09931b66f8c8', Text)
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
    _6eb82ef66dd64fd4498162e732de1bab26174a9dab3c43bc77dd2e2c5a68ae17: Mapped[str] = mapped_column('6eb82ef66dd64fd4498162e732de1bab26174a9dab3c43bc77dd2e2c5a68ae17', Text)
    b4097c4f503f2dc647b86b00d333e5440b2297afcee86a760afc1ef791753cb8: Mapped[str] = mapped_column(Text)
    ef2b36299663dcd6edc3e1c1bf47f5aa679b49b8dd7c95a020ae8af7adb1ac4e: Mapped[int] = mapped_column(Integer)
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

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    gacha_name: Mapped[str] = mapped_column(Text)
    item_type: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[int] = mapped_column(Integer)
    cost: Mapped[int] = mapped_column(Integer)
    repeat_step: Mapped[int] = mapped_column(Integer)


class EventIntroduction(Base):
    __tablename__ = 'event_introduction'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reminder_id: Mapped[int] = mapped_column(Integer)
    condition_type: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)


class EventRevivalSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_revival_series_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    _91cb551a67dc7797db88d57956fea94676e9cff18266bcf8eb625851c023d4d8: Mapped[int] = mapped_column('91cb551a67dc7797db88d57956fea94676e9cff18266bcf8eb625851c023d4d8', Integer)
    _857ab048fe838223751bdaf87cba1968f31a615bc4bd9b7160a5220ae1bdc212: Mapped[int] = mapped_column('857ab048fe838223751bdaf87cba1968f31a615bc4bd9b7160a5220ae1bdc212', Integer)
    a0eedaeb11af3b056ce4d29730104799209603c37d570f36b9ebe8c1e2c4b6ae: Mapped[int] = mapped_column(Integer)
    _67b9eb34051085d992302cfb9aa03016e3b79fba66c298344b33dc350fd572a8: Mapped[int] = mapped_column('67b9eb34051085d992302cfb9aa03016e3b79fba66c298344b33dc350fd572a8', Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    _24f9b3fcccb166d79bdc78edc481c5cb118873723b73007944cb11f004c45adf: Mapped[int] = mapped_column('24f9b3fcccb166d79bdc78edc481c5cb118873723b73007944cb11f004c45adf', Integer)
    _80dd316dc46f1f4edc4a9f895b36f90f844c3521c48c5da937819332ea491df7: Mapped[int] = mapped_column('80dd316dc46f1f4edc4a9f895b36f90f844c3521c48c5da937819332ea491df7', Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    f32f1463f55eb05e2be72fac8b582e413b7440c7d1dccc450686119887d540cf: Mapped[int] = mapped_column(Integer)
    ae5cacd56d35fbca4726a1e3f683dcfa73af4a6c4d4e1223567f935e7dcbf3f0: Mapped[int] = mapped_column(Integer)
    deda392cbea4d99218f3559efa09351103f788815cbc812216a4e6509cdb6827: Mapped[int] = mapped_column(Integer)
    b95387cb3ebbb283470dea6bfc67e7ed3f8c5169847852d4eeacd7a417fc8538: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    ade3668f3addd9ed33b05c973fe080e019c20ebae1d38c6e07404cd6e0dc47fe: Mapped[int] = mapped_column(Integer)
    _58faa28211ab032719246f141820e4a82e3cd883e2ab68802984db84c49b86ac: Mapped[int] = mapped_column('58faa28211ab032719246f141820e4a82e3cd883e2ab68802984db84c49b86ac', Integer)
    _184bf38b170914e7db6780858b47dbe0ee0942350c0c36c2231e8d4c5720493e: Mapped[int] = mapped_column('184bf38b170914e7db6780858b47dbe0ee0942350c0c36c2231e8d4c5720493e', Integer)
    _38efecfc22b1f8d99e648ac6db6b21edce5795db3200bbf7edf592310b7e6f24: Mapped[int] = mapped_column('38efecfc22b1f8d99e648ac6db6b21edce5795db3200bbf7edf592310b7e6f24', Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    _57f419c86a49011b6568ee0ad01ed30f65ad7d274efad6aafe17392353d75d47: Mapped[int] = mapped_column('57f419c86a49011b6568ee0ad01ed30f65ad7d274efad6aafe17392353d75d47', Integer)
    d1c553f4a5768da9fd39fb36d8c4b1b33707726b9eb32279fbe33f2fa7a60b49: Mapped[int] = mapped_column(Integer)
    _9b9aa9d776994f53460b443a3feb32ace33ed9a20d3317aa1655beb9b9ffaea6: Mapped[int] = mapped_column('9b9aa9d776994f53460b443a3feb32ace33ed9a20d3317aa1655beb9b9ffaea6', Integer)
    _0876e22d65af886bb195394af71d738e780f954d15946b71c994af6e50b14ede: Mapped[int] = mapped_column('0876e22d65af886bb195394af71d738e780f954d15946b71c994af6e50b14ede', Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    _1fcbe455b96e4bf9748d77c33f37393c054bd87a45228cd7354d8e01bf46a3b5: Mapped[int] = mapped_column('1fcbe455b96e4bf9748d77c33f37393c054bd87a45228cd7354d8e01bf46a3b5', Integer)
    _7c9fb1c36538427026925154eea96923c99a7b5a0fa83e1cad8591b8d51c3502: Mapped[int] = mapped_column('7c9fb1c36538427026925154eea96923c99a7b5a0fa83e1cad8591b8d51c3502', Integer)
    _29bfd813923bc2f2de473c302f887077fb801e3566b260ed488f6f90a42a234b: Mapped[int] = mapped_column('29bfd813923bc2f2de473c302f887077fb801e3566b260ed488f6f90a42a234b', Integer)
    ab23bbafd92a7f7f55848868cf989c840a0d4fb8f9e0c87db1f8e06d649b60ae: Mapped[int] = mapped_column(Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    _12e1b293bf16ab15933dde84141ae1551cbdf09195d8dbb192cf43125a65bb20: Mapped[int] = mapped_column('12e1b293bf16ab15933dde84141ae1551cbdf09195d8dbb192cf43125a65bb20', Integer)
    a44cef4cdfa359d96a88723a24f7fb73037db7c1a43a6858764e4db45f28a5ff: Mapped[int] = mapped_column(Integer)


class EventRevivalWaveGroupDatum(Base):
    __tablename__ = 'event_revival_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    _7e68255090d1fd28cabe385f8bd75b9ddb36246be6d1b6c831d6841a678ae53f: Mapped[int] = mapped_column('7e68255090d1fd28cabe385f8bd75b9ddb36246be6d1b6c831d6841a678ae53f', Integer)
    _28adf3d470d399a89c8f58d40fc7c404c89b096a5b85803e304db2662347fd31: Mapped[int] = mapped_column('28adf3d470d399a89c8f58d40fc7c404c89b096a5b85803e304db2662347fd31', Integer)
    fbd6f35f7606a75f81990b5ee589b81aa3a455cc81d8df11e3993b44505bc508: Mapped[int] = mapped_column(Integer)
    cd3b326d8960ad636f5a77a7860da0f22d7098eda6a575570d6b1a08d507e41b: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    _09a5e5a19e834252753002bd00adab85644acea19f13afcbf4da401c40b6674b: Mapped[int] = mapped_column('09a5e5a19e834252753002bd00adab85644acea19f13afcbf4da401c40b6674b', Integer)
    _29964022da6c4c6811d23335d0b75295548d2e03ae94c8517d4e9d99b95e46a4: Mapped[int] = mapped_column('29964022da6c4c6811d23335d0b75295548d2e03ae94c8517d4e9d99b95e46a4', Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    abe507df3181355f4ed76f54fff8f2d93f8b387e00e492661248f23352a655df: Mapped[int] = mapped_column(Integer)
    _2f18bca328a4f7a4662298abfe8808a54f06d50fe5e9c594b5846e3eecd27e84: Mapped[int] = mapped_column('2f18bca328a4f7a4662298abfe8808a54f06d50fe5e9c594b5846e3eecd27e84', Integer)
    _338e5e1eb04d8ac18d6499e36e5ad81602cffe20ba70f85773b7e7ce67a3dbd8: Mapped[int] = mapped_column('338e5e1eb04d8ac18d6499e36e5ad81602cffe20ba70f85773b7e7ce67a3dbd8', Integer)
    ad1961172f54bd49735eaef2e3b380d1ca4ff7c9e78fb7d5e89844835c49f1e9: Mapped[int] = mapped_column(Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    f0345c2e6f5db56b6acb2e7573eeff8cda06e1599f6401426f0739e70847ca75: Mapped[int] = mapped_column(Integer)
    _56b57293759ad803da320fafc3bfaf8a0ea39f89452c1b6f08554e259d0cbf9f: Mapped[int] = mapped_column('56b57293759ad803da320fafc3bfaf8a0ea39f89452c1b6f08554e259d0cbf9f', Integer)
    _84396614330e3d9a58e4f3d0c58017fddc8b0874f9d719accc5c7955bb54b6cd: Mapped[int] = mapped_column('84396614330e3d9a58e4f3d0c58017fddc8b0874f9d719accc5c7955bb54b6cd', Integer)
    b980eca3c7ca28587d4fdee12e77c39a418634336618569a6170ea083128b7d4: Mapped[int] = mapped_column(Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    _9205819f02ec3aefb7eae8422300d568fe4b4bb3057401b56e61b0c4fd795f79: Mapped[int] = mapped_column('9205819f02ec3aefb7eae8422300d568fe4b4bb3057401b56e61b0c4fd795f79', Integer)
    _46c762e9b5f8004b6063daaad12074aff7d4785dbb5532b2d293e08320aa8583: Mapped[int] = mapped_column('46c762e9b5f8004b6063daaad12074aff7d4785dbb5532b2d293e08320aa8583', Integer)
    _8965e657c3f381b8d9996c335ef0e7e864d6dfaf45c25948d8b5afa3171cd2d0: Mapped[int] = mapped_column('8965e657c3f381b8d9996c335ef0e7e864d6dfaf45c25948d8b5afa3171cd2d0', Integer)
    eae7080c34ab175d61c57da1573f9f6d6e308daf32e5d75352b775a872e02fd0: Mapped[int] = mapped_column(Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    fdf3eb7263f8561227c912a31f008604cee092aa18a4c6d3f4590c3226d76048: Mapped[int] = mapped_column(Integer)
    a301ba8cd433812209d5c777b249c9763f315865892bd3d66b4ebbae870ea6a6: Mapped[int] = mapped_column(Integer)
    _9678ecb04fa6d2eab8c34e911b369267f17699557fc1d46c8c17eb42120b5285: Mapped[int] = mapped_column('9678ecb04fa6d2eab8c34e911b369267f17699557fc1d46c8c17eb42120b5285', Integer)
    _4f8b373771d7f52ca0e9da634d994a96aab051dd6d3ea76a2b4e5f4b88a28d4c: Mapped[int] = mapped_column('4f8b373771d7f52ca0e9da634d994a96aab051dd6d3ea76a2b4e5f4b88a28d4c', Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    _681650ce5ba0247e57928bc630e42f592d99ea064aab6a66e032f1644d7c9cfe: Mapped[int] = mapped_column('681650ce5ba0247e57928bc630e42f592d99ea064aab6a66e032f1644d7c9cfe', Integer)
    _1416b729cdc9c34b8a919c68d111271d2981c3a84db57d3cc7fca94df6efb170: Mapped[int] = mapped_column('1416b729cdc9c34b8a919c68d111271d2981c3a84db57d3cc7fca94df6efb170', Integer)


class EventSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_series_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer)
    _6faac35d2b42209e91355deaaadb1d2128d3a0175498902b933dc871071844c2: Mapped[int] = mapped_column('6faac35d2b42209e91355deaaadb1d2128d3a0175498902b933dc871071844c2', Integer)
    a18f1de895d39a0ae6c5b7642b12f4590a9a0054264d288baac83bbe9675f8f1: Mapped[int] = mapped_column(Integer)
    b7b36683f0bda838e6cb55e14ec8d96573b97e746ddf8f344c087cb7404516d2: Mapped[int] = mapped_column(Integer)
    c1516c9991feff10e045cc767163ae41b8ef046493510a30826f13cfacc3308f: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)
    _9fb4a74ffd60afff6b6227408a1ae56ecd58462504aadec088495c9e7c65db43: Mapped[int] = mapped_column('9fb4a74ffd60afff6b6227408a1ae56ecd58462504aadec088495c9e7c65db43', Integer)
    _25aaf09e70dab532e13801b2fb5b84a9f31b5002426f4cf2fa8436273ae7638c: Mapped[int] = mapped_column('25aaf09e70dab532e13801b2fb5b84a9f31b5002426f4cf2fa8436273ae7638c', Integer)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer)
    _7a0e80b6a6a525ab2aa7816a837f2de6a45824168053241d27de2cf3a894c88f: Mapped[int] = mapped_column('7a0e80b6a6a525ab2aa7816a837f2de6a45824168053241d27de2cf3a894c88f', Integer)
    _854474bba103411444f5b2377c7235c573f9bb25d7e2f76ab44447cd52d7ba89: Mapped[int] = mapped_column('854474bba103411444f5b2377c7235c573f9bb25d7e2f76ab44447cd52d7ba89', Integer)
    _4333f36b27e02a844743f721030af880276220afb95eecde086845cd15ad879f: Mapped[int] = mapped_column('4333f36b27e02a844743f721030af880276220afb95eecde086845cd15ad879f', Integer)
    _3bed9f0df21bce7e22ca4e1d2dd87b9c08a6a2cd71790c8f833cf0f75f866638: Mapped[int] = mapped_column('3bed9f0df21bce7e22ca4e1d2dd87b9c08a6a2cd71790c8f833cf0f75f866638', Integer)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer)
    bc87a23632c6db57b97098dd3fcb91132b510b509885ff30a358274bc1b5e1c5: Mapped[int] = mapped_column(Integer)
    dc1828506fff984f10f178681ae7cfa2ac6cb4ec906f05ebf484b77d711259b4: Mapped[int] = mapped_column(Integer)
    _28e12b6e6cb128735111281f9cf7b0c8a23396ba853d19b5ce9e85c0896f18a5: Mapped[int] = mapped_column('28e12b6e6cb128735111281f9cf7b0c8a23396ba853d19b5ce9e85c0896f18a5', Integer)
    _410f8c13ed36b71801d62b84657b384cfefc1f11e6c3d9dc193c5ca2640bda10: Mapped[int] = mapped_column('410f8c13ed36b71801d62b84657b384cfefc1f11e6c3d9dc193c5ca2640bda10', Integer)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer)
    _7252543e0fe18261579847187ee832ebb8f4063d72ff4fa97581c510ca82848b: Mapped[int] = mapped_column('7252543e0fe18261579847187ee832ebb8f4063d72ff4fa97581c510ca82848b', Integer)
    a90cfff2ce45c3892eeeaa7b58778d05ad15f672b680f927067a5ee3ccce7b0c: Mapped[int] = mapped_column(Integer)
    _8fcb4d8bfe27fc6977ba1f17ca8e7f657ba291ed0994acb8baac261e01d1c6a9: Mapped[int] = mapped_column('8fcb4d8bfe27fc6977ba1f17ca8e7f657ba291ed0994acb8baac261e01d1c6a9', Integer)
    _0b64ba2a678cc1ff40c6ade135da6b0e423a799a0c4f39f78c4ef32c928ac074: Mapped[int] = mapped_column('0b64ba2a678cc1ff40c6ade135da6b0e423a799a0c4f39f78c4ef32c928ac074', Integer)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer)
    acea8fcde35065bca1ddfae0d4e31c2ddd24c4fc01d607ec2f2b3b69069b3b3b: Mapped[int] = mapped_column(Integer)
    b413d7f220313b43a83f0335a08c607ee2962e5e61e6815e12bb303e6bde8b17: Mapped[int] = mapped_column(Integer)
    b1383fbfce44054134dea4bea9c789cce4d9fb4af68f614117aed8ada4bf132b: Mapped[int] = mapped_column(Integer)
    _6343b925930cf1ba7650dcd18208267b51962195422c1aef7ea7612fb5b88da6: Mapped[int] = mapped_column('6343b925930cf1ba7650dcd18208267b51962195422c1aef7ea7612fb5b88da6', Integer)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer)
    _10bd97cd9993c7dc3d2decf886ab8a80a7498c326b99f627f9ad2dc8380e4be1: Mapped[int] = mapped_column('10bd97cd9993c7dc3d2decf886ab8a80a7498c326b99f627f9ad2dc8380e4be1', Integer)
    _5cffc491e844eb625ea5cab523ab35c6a397857b6f7508e4a8286a1033f1ad55: Mapped[int] = mapped_column('5cffc491e844eb625ea5cab523ab35c6a397857b6f7508e4a8286a1033f1ad55', Integer)


class EventStoryDatum(Base):
    __tablename__ = 'event_story_data'

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
    can_bookmark: Mapped[int] = mapped_column(Integer)
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

    restriction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExPlus(Base):
    __tablename__ = 'ex_plus'

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


class ExceedLevelStage(Base):
    __tablename__ = 'exceed_level_stage'

    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    increase_level_limit: Mapped[int] = mapped_column(Integer)
    unlock_quest_id: Mapped[int] = mapped_column(Integer)
    unlock_team_level: Mapped[int] = mapped_column(Integer)
    general_exceed_item_id: Mapped[int] = mapped_column(Integer)


class ExceedLevelUnit(Base):
    __tablename__ = 'exceed_level_unit'

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


class ExtraEffectDatum(Base):
    __tablename__ = 'extra_effect_data'

    extra_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_type: Mapped[int] = mapped_column(Integer)
    target_value_1: Mapped[int] = mapped_column(Integer)
    target_value_2: Mapped[int] = mapped_column(Integer)
    set_id: Mapped[int] = mapped_column(Integer)
    exec_timing_1: Mapped[int] = mapped_column(Integer)
    exec_timing_2: Mapped[int] = mapped_column(Integer)
    exec_timing_3: Mapped[int] = mapped_column(Integer)
    exec_timing_4: Mapped[int] = mapped_column(Integer)
    exec_timing_5: Mapped[int] = mapped_column(Integer)
    enemy_id_1: Mapped[int] = mapped_column(Integer)
    enemy_id_2: Mapped[int] = mapped_column(Integer)
    enemy_id_3: Mapped[int] = mapped_column(Integer)
    enemy_id_4: Mapped[int] = mapped_column(Integer)
    enemy_id_5: Mapped[int] = mapped_column(Integer)


class ExtraEffectTargetRange(Base):
    __tablename__ = 'extra_effect_target_range'

    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    set_id: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(Integer)


class ExtraEffectUnitGroup(Base):
    __tablename__ = 'extra_effect_unit_group'

    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)


class FbsSchedule(Base):
    __tablename__ = 'fbs_schedule'

    fbs_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class FixLineupGroupSet(Base):
    __tablename__ = 'fix_lineup_group_set'

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
    a7072d4062c755f987907bd4600f3ef0087d4e142f52651eba59d33de4cb8621: Mapped[int] = mapped_column(Integer)
    _52230f511fe69a4f9a9ad17e7699602e24f1d077d60f545b283d8147d59ce3cb: Mapped[int] = mapped_column('52230f511fe69a4f9a9ad17e7699602e24f1d077d60f545b283d8147d59ce3cb', Integer)
    _7f4d4168c2e1d716ebb3736c699e4aaefc958c6dbae70cfa98a8d1946683bbe6: Mapped[int] = mapped_column('7f4d4168c2e1d716ebb3736c699e4aaefc958c6dbae70cfa98a8d1946683bbe6', Integer)
    reward_id_1: Mapped[int] = mapped_column(Integer)
    a3308bfdd255cf309d99c657f12153e076874e5a6255d4a87a5fbc1611eaa1ac: Mapped[int] = mapped_column(Integer)
    b45cc4ebc338466130eca178014080469dce6bbbfb5354910f7c90ff7ca8a342: Mapped[int] = mapped_column(Integer)
    _2cbb1904c66cfbb57284c90bb89067041feee1ee412cecb339d35ce401f89beb: Mapped[int] = mapped_column('2cbb1904c66cfbb57284c90bb89067041feee1ee412cecb339d35ce401f89beb', Integer)
    _75e3bd5ac53ce641291ab801cccbe419483627542f67e91ce7b205d26306d9a7: Mapped[int] = mapped_column('75e3bd5ac53ce641291ab801cccbe419483627542f67e91ce7b205d26306d9a7', Integer)
    e86b0f3884bcd94f19751cb52864725fb8885ea7866ac74e5ec4be123ecf0e47: Mapped[int] = mapped_column(Integer)
    reward_id_2: Mapped[int] = mapped_column(Integer)
    _0ef298e1962e778bf467a091cdfc87a14981deadc1453151254e65cf7ae61eb6: Mapped[int] = mapped_column('0ef298e1962e778bf467a091cdfc87a14981deadc1453151254e65cf7ae61eb6', Integer)
    a8b8f07c5bc0f4391111fd670142814423f2f32c9947d046b78b2df889693060: Mapped[int] = mapped_column(Integer)
    _2b9ebdee26eca313523ac1e2292f449f40e5f0a082f290a62c0824eeba498ae1: Mapped[int] = mapped_column('2b9ebdee26eca313523ac1e2292f449f40e5f0a082f290a62c0824eeba498ae1', Integer)
    _379ed002344ef74af6c47880031e5a1e2207a00ed6cb0a9f3e9443e9e56e443b: Mapped[int] = mapped_column('379ed002344ef74af6c47880031e5a1e2207a00ed6cb0a9f3e9443e9e56e443b', Integer)
    d464ec7502a4ecafa3cbbbf5a566075a2c16981b085e15981785e2d3aaea678e: Mapped[int] = mapped_column(Integer)
    reward_id_3: Mapped[int] = mapped_column(Integer)
    e568e4bcc07537aa0eca1e461e719fb8217bb09de03f53304a8a621ea79de0ce: Mapped[int] = mapped_column(Integer)
    _2a340f7a704cce568ef64a4f26b66444ce92ac449cf9693c4908c748537db589: Mapped[int] = mapped_column('2a340f7a704cce568ef64a4f26b66444ce92ac449cf9693c4908c748537db589', Integer)
    fd0993a1fce2699b0e195abeff59c07aa13ff300f5fd6fe4a7820fe4046b3030: Mapped[int] = mapped_column(Integer)
    _780f654807112a555a9670a73814c0312d0ea4360c590ed8ddf478300f9bf00c: Mapped[int] = mapped_column('780f654807112a555a9670a73814c0312d0ea4360c590ed8ddf478300f9bf00c', Integer)
    _7aa67977d1f13b57afa5fd6a39a3a09d19d6a4ded513f2a4a96caddddb9f9ad5: Mapped[int] = mapped_column('7aa67977d1f13b57afa5fd6a39a3a09d19d6a4ded513f2a4a96caddddb9f9ad5', Integer)
    reward_id_4: Mapped[int] = mapped_column(Integer)
    _778959c80c43cdaf8bff711216711375c5aafed8fb942c86d399c3513aa8c89d: Mapped[int] = mapped_column('778959c80c43cdaf8bff711216711375c5aafed8fb942c86d399c3513aa8c89d', Integer)
    _678a354f39de2ca7a10f442a62bbb4c42930f628af9116c0ad38d7eff87a2e7e: Mapped[int] = mapped_column('678a354f39de2ca7a10f442a62bbb4c42930f628af9116c0ad38d7eff87a2e7e', Integer)
    d24e33b07c00e507fa0d22afc4d8173a263a3a8bfe104053b4c3f2fd0b070ff0: Mapped[int] = mapped_column(Integer)
    a9f8839ec979053360114752293f3e1021d09f0009f8f0f0ba68d4366c231355: Mapped[int] = mapped_column(Integer)
    _99dab7e9f7ebbdea6553ef8f636eacb816ae45d94c0638557ade0d71bf3adf22: Mapped[int] = mapped_column('99dab7e9f7ebbdea6553ef8f636eacb816ae45d94c0638557ade0d71bf3adf22', Integer)
    reward_id_5: Mapped[int] = mapped_column(Integer)
    _461c3885ce0d57cc0b08fe515d6920bcfdf59caf23466628f868e2bdbf31f555: Mapped[int] = mapped_column('461c3885ce0d57cc0b08fe515d6920bcfdf59caf23466628f868e2bdbf31f555', Integer)
    d91751db33ac743bb712f5b748e971b37b00a8287c3c3f40ac003b469597393c: Mapped[int] = mapped_column(Integer)
    _662909eece59f4c78481795824bd69017ac9d5be8c449705942689902cc89959: Mapped[int] = mapped_column('662909eece59f4c78481795824bd69017ac9d5be8c449705942689902cc89959', Integer)
    _23960b00f3aa888c2ac717941a25e60ca417bda3291277638d84fee9311a836b: Mapped[int] = mapped_column('23960b00f3aa888c2ac717941a25e60ca417bda3291277638d84fee9311a836b', Integer)
    _32117e822075b5582467445fd57137d53cbd5831c99b72de75565b5798a0e90a: Mapped[int] = mapped_column('32117e822075b5582467445fd57137d53cbd5831c99b72de75565b5798a0e90a', Integer)
    reward_id_6: Mapped[int] = mapped_column(Integer)
    _069b5cb6a65e3da5929e876bd9d24b2d95eadc39d7194a13058987d3ef99c7ef: Mapped[int] = mapped_column('069b5cb6a65e3da5929e876bd9d24b2d95eadc39d7194a13058987d3ef99c7ef', Integer)
    _4a0056d65db7a9d2aa1dbc1ee8ba6d21528eea15471b2a8bfdb7674727f63cd3: Mapped[int] = mapped_column('4a0056d65db7a9d2aa1dbc1ee8ba6d21528eea15471b2a8bfdb7674727f63cd3', Integer)
    _77179dcab1daa21132a4b6e672a80d40c00e289603ff5e9fd89e9cfefc611866: Mapped[int] = mapped_column('77179dcab1daa21132a4b6e672a80d40c00e289603ff5e9fd89e9cfefc611866', Integer)
    d9c8ae462ddba9eee15badfdad639079881d863d15f486756fb821acde9a3db5: Mapped[int] = mapped_column(Integer)
    b8342e06a3e71c0c465294c0348e0109ae6057ed7b7271b79418981bee3e820c: Mapped[int] = mapped_column(Integer)
    reward_id_7: Mapped[int] = mapped_column(Integer)
    _8d15fed9f613cd71d66c7f05f42bb0bbfaf563dcf89886c422b26a44130ddba9: Mapped[int] = mapped_column('8d15fed9f613cd71d66c7f05f42bb0bbfaf563dcf89886c422b26a44130ddba9', Integer)
    _8a3caf5c1189351ca9bf5c6576c965630d9d6514514a722679a680ba270a4021: Mapped[int] = mapped_column('8a3caf5c1189351ca9bf5c6576c965630d9d6514514a722679a680ba270a4021', Integer)
    _7d1fc622cb9c412ce04b4b5ba746ab39a376b6def328418dfca27f2ae3c82b3f: Mapped[int] = mapped_column('7d1fc622cb9c412ce04b4b5ba746ab39a376b6def328418dfca27f2ae3c82b3f', Integer)
    adc9e6d1af4f11685aced907ddf484270f4f477b956b4916685db6da7e13b0f3: Mapped[int] = mapped_column(Integer)
    bd837c236ac801bdfd73d4676bc7b508d5c11592200484d4021077a71267a048: Mapped[int] = mapped_column(Integer)
    reward_id_8: Mapped[int] = mapped_column(Integer)
    _7cc79599a633f5b6dda27d2a87a5fd6800cdba95bda188237bb7b0b7c48019a4: Mapped[int] = mapped_column('7cc79599a633f5b6dda27d2a87a5fd6800cdba95bda188237bb7b0b7c48019a4', Integer)
    f430b8666e19dd73182fff6cdb5ce17aeb121eae4c4744036429f5ee404b370a: Mapped[int] = mapped_column(Integer)
    _42695f6eec74176d530829faa7276f3a24c93cb609fce595c3014b5a897c425a: Mapped[int] = mapped_column('42695f6eec74176d530829faa7276f3a24c93cb609fce595c3014b5a897c425a', Integer)
    _96d487d50337b0f7dd4638eec66e2d0dd641c9eb39c721c9fadee6a9f0579f60: Mapped[int] = mapped_column('96d487d50337b0f7dd4638eec66e2d0dd641c9eb39c721c9fadee6a9f0579f60', Integer)
    _8914227971204332793f2cc2ba7e4a608d6bd5aa1529106f1b084363270e3e19: Mapped[int] = mapped_column('8914227971204332793f2cc2ba7e4a608d6bd5aa1529106f1b084363270e3e19', Integer)
    reward_id_9: Mapped[int] = mapped_column(Integer)
    e38b6d9f5e7a35d042468f148a72f567f5f4d808b9c3d436b4ec1e5b5deebec0: Mapped[int] = mapped_column(Integer)
    cce5655af8a39e069610586f3f82b76f3e2ef73c8f0f80c8f2ed1afbb614ed6b: Mapped[int] = mapped_column(Integer)
    _1a09ece650c0851ad9bbe25bb10b0ae599be3d81c5bb7ce775e6e30e519cb60c: Mapped[int] = mapped_column('1a09ece650c0851ad9bbe25bb10b0ae599be3d81c5bb7ce775e6e30e519cb60c', Integer)
    _8929263c5458934ba7ad0395af41f2f4960771b2a39df56f60c6fdb4ece3c7b6: Mapped[int] = mapped_column('8929263c5458934ba7ad0395af41f2f4960771b2a39df56f60c6fdb4ece3c7b6', Integer)
    _2faafbe64c397036249492c3c2bdcc7239d690702af240e9ad6ac83a38706628: Mapped[int] = mapped_column('2faafbe64c397036249492c3c2bdcc7239d690702af240e9ad6ac83a38706628', Integer)
    reward_id_10: Mapped[int] = mapped_column(Integer)
    ccae1b630ab7088c966c0fad28c0505960f10d41bff04c74d2cb8c7cb17c53b6: Mapped[int] = mapped_column(Integer)
    cd94e9ce2aaaae73f5faf7a686c35d18d436c1252ac6309d1a8ae8cdea0c0fe6: Mapped[int] = mapped_column(Integer)
    _84829b2d43ec240b0366d8feeb83d85bcbeb5a5ee5bce5e3d2ebbed2da733c09: Mapped[int] = mapped_column('84829b2d43ec240b0366d8feeb83d85bcbeb5a5ee5bce5e3d2ebbed2da733c09', Integer)
    _1871e1c0b3760ae5d84df74660da0ae9ad00e38a8fa00448531535170f8b08fc: Mapped[int] = mapped_column('1871e1c0b3760ae5d84df74660da0ae9ad00e38a8fa00448531535170f8b08fc', Integer)
    _72f925906c87b04df15dcb057e2dcb67e0e9d8477311079fec758e651eebc0cd: Mapped[int] = mapped_column('72f925906c87b04df15dcb057e2dcb67e0e9d8477311079fec758e651eebc0cd', Integer)
    reward_id_11: Mapped[int] = mapped_column(Integer)
    _5b389396896f9ebbe35455ad25ad29a8f065ec0b18a20249aad98174c2cc6b92: Mapped[int] = mapped_column('5b389396896f9ebbe35455ad25ad29a8f065ec0b18a20249aad98174c2cc6b92', Integer)
    f48b57a0fe90502aab04a0af40613f508b4a2ac0c480d4d4c4d7a2cf3c8399a4: Mapped[int] = mapped_column(Integer)
    _0f632aa0f8b2b5cab5472e7c8a58f6187a3c5cee58c6bd135581353e12f975e7: Mapped[int] = mapped_column('0f632aa0f8b2b5cab5472e7c8a58f6187a3c5cee58c6bd135581353e12f975e7', Integer)
    a19c317481597824c85e7a4619aac13e3b78ca834bbefcb86606a8eb0660aac7: Mapped[int] = mapped_column(Integer)
    _293bc417f042692f2c20ac1445ea18bf702cf3c4955ad77667e5c68ff9976fdd: Mapped[int] = mapped_column('293bc417f042692f2c20ac1445ea18bf702cf3c4955ad77667e5c68ff9976fdd', Integer)
    reward_id_12: Mapped[int] = mapped_column(Integer)
    _2773533a4dc20f8a98b5b66d5d2f68b1915fb6c9418a56b75d3ea2ddb413ea6a: Mapped[int] = mapped_column('2773533a4dc20f8a98b5b66d5d2f68b1915fb6c9418a56b75d3ea2ddb413ea6a', Integer)
    d7ca1cb722cc485f4e609587ef8d939acaf167c9903cc71ac882b617673d7f85: Mapped[int] = mapped_column(Integer)
    _2efe35208becf2b4e59279960261239e285dbd7569d631bf4bea1f9e1bd67a0e: Mapped[int] = mapped_column('2efe35208becf2b4e59279960261239e285dbd7569d631bf4bea1f9e1bd67a0e', Integer)
    _7edc51d71a85080a106d788d6bc5705607e4bf956d936f7d918348471ef71e8e: Mapped[int] = mapped_column('7edc51d71a85080a106d788d6bc5705607e4bf956d936f7d918348471ef71e8e', Integer)
    _7575bbf8cadd9aa04df065cd0f332acbe35f9225e598ab3fffdee9c33a7df8f4: Mapped[int] = mapped_column('7575bbf8cadd9aa04df065cd0f332acbe35f9225e598ab3fffdee9c33a7df8f4', Integer)
    reward_id_13: Mapped[int] = mapped_column(Integer)
    _3fbfbe928ea82f40255abd183d84f37c7c968fbbcf301eaff88f7699d130238e: Mapped[int] = mapped_column('3fbfbe928ea82f40255abd183d84f37c7c968fbbcf301eaff88f7699d130238e', Integer)
    _2305cdc9511efaacff75208a140db806942126a76b9ab55de671dfba5d560416: Mapped[int] = mapped_column('2305cdc9511efaacff75208a140db806942126a76b9ab55de671dfba5d560416', Integer)
    _4ece74ba09db1ffd13c4e5e11460da2169d73e8af129d390f9085be725b9e370: Mapped[int] = mapped_column('4ece74ba09db1ffd13c4e5e11460da2169d73e8af129d390f9085be725b9e370', Integer)
    _3db72b674f662881f6698fb72a2dacc9e350083e6a38a3ab853a12a984f4f5c0: Mapped[int] = mapped_column('3db72b674f662881f6698fb72a2dacc9e350083e6a38a3ab853a12a984f4f5c0', Integer)
    f340dfd31c60c1fc043524418183198311dd1c837235d6f135cd4a2146d30965: Mapped[int] = mapped_column(Integer)
    reward_id_14: Mapped[int] = mapped_column(Integer)
    b174202501f4d65cce4326c4c7908966297c0a963a8415dac4218d5870c83de8: Mapped[int] = mapped_column(Integer)
    _6f95889e6f6b3e3943ea2bc75e56dff338abc2eaf4b3a6f89046ab3b14356031: Mapped[int] = mapped_column('6f95889e6f6b3e3943ea2bc75e56dff338abc2eaf4b3a6f89046ab3b14356031', Integer)
    d9948fce8bfab0d6f8b71c6ab9daf75aa937e5d28e0a9d41d28b42ad5b738f85: Mapped[int] = mapped_column(Integer)
    b357686905a533a45dfd10198ed541be0335fed39aa29b0da1ef25d5769a2c95: Mapped[int] = mapped_column(Integer)
    a73d9b16a6b45d59d3e1da4218b8e1752a978037ff27f3364deb1135a7d7b84e: Mapped[int] = mapped_column(Integer)
    reward_id_15: Mapped[int] = mapped_column(Integer)
    _06e4f25ca2e7adee8803f15c5452c7adc574b6c6d3c96c46a50d666386e1a26d: Mapped[int] = mapped_column('06e4f25ca2e7adee8803f15c5452c7adc574b6c6d3c96c46a50d666386e1a26d', Integer)
    _4fe79cbb759249f5b4a18c0542ae85d03227c0491028b353b1759284441f0634: Mapped[int] = mapped_column('4fe79cbb759249f5b4a18c0542ae85d03227c0491028b353b1759284441f0634', Integer)
    _5d69801bf8dd3478ab42a387eaed8e6a12215d094697cdee5e89db147bf32c52: Mapped[int] = mapped_column('5d69801bf8dd3478ab42a387eaed8e6a12215d094697cdee5e89db147bf32c52', Integer)
    _35c59fa489b40441e7350173b9290bb52b33bf4fabeb836adafd67be7f13d6c4: Mapped[int] = mapped_column('35c59fa489b40441e7350173b9290bb52b33bf4fabeb836adafd67be7f13d6c4', Integer)
    _6886695137964f876b15cc5bda1fba99029642e8b92974ecbb752cc5c062116d: Mapped[int] = mapped_column('6886695137964f876b15cc5bda1fba99029642e8b92974ecbb752cc5c062116d', Integer)
    reward_id_16: Mapped[int] = mapped_column(Integer)
    _2429166d43e4e6a38922297ab3ab24008450ab3bd99064e959a643cb7cfbbc2b: Mapped[int] = mapped_column('2429166d43e4e6a38922297ab3ab24008450ab3bd99064e959a643cb7cfbbc2b', Integer)
    _3038d06979a4410cd2fbc93f1b8e7de221f29d2d869fa2afa8a010c5743ea34f: Mapped[int] = mapped_column('3038d06979a4410cd2fbc93f1b8e7de221f29d2d869fa2afa8a010c5743ea34f', Integer)
    f1cd543bee40dba014a755d9de0fed23acddde218b658abdf2160ae4348ff1eb: Mapped[int] = mapped_column(Integer)
    ba9c2de7f104e233ece48030d1e09c8b83424933001637ac485ed6868c042762: Mapped[int] = mapped_column(Integer)
    _2bf94331351c0ad24bfcc2dc4bd2ce52cd337544873b4260a7803973c70a4402: Mapped[int] = mapped_column('2bf94331351c0ad24bfcc2dc4bd2ce52cd337544873b4260a7803973c70a4402', Integer)
    reward_id_17: Mapped[int] = mapped_column(Integer)
    a66597610807094ac8dbfd37d011aa8141a5851f5fc06a405fb02e94d69fc6f8: Mapped[int] = mapped_column(Integer)
    _956ad1606d921281b2b20eb8870129ec0864ff2073bc5e395c91c3cc5ebda1dc: Mapped[int] = mapped_column('956ad1606d921281b2b20eb8870129ec0864ff2073bc5e395c91c3cc5ebda1dc', Integer)
    _520e6338a824100b362a7c50eda5e7e12dbac8fb83bb6bd832a328ac8097ae5e: Mapped[int] = mapped_column('520e6338a824100b362a7c50eda5e7e12dbac8fb83bb6bd832a328ac8097ae5e', Integer)
    c7431e2e7e8144d1c4ef89a477fca0bf83d654568fa490f8edf8802903b6c2bd: Mapped[int] = mapped_column(Integer)
    _02bcf31fdb244860bad99f40897afd7b4b8923222f3f271a229ae37fb8758bc3: Mapped[int] = mapped_column('02bcf31fdb244860bad99f40897afd7b4b8923222f3f271a229ae37fb8758bc3', Integer)
    reward_id_18: Mapped[int] = mapped_column(Integer)
    _8933c5d0b0b2edf7a821ff7039e442acf3f143275db8da070f6c1fdd622759cb: Mapped[int] = mapped_column('8933c5d0b0b2edf7a821ff7039e442acf3f143275db8da070f6c1fdd622759cb', Integer)
    _0f344914afd4c25c1569c885071b86821e0f953b4602347fa8f7c8a02d44129b: Mapped[int] = mapped_column('0f344914afd4c25c1569c885071b86821e0f953b4602347fa8f7c8a02d44129b', Integer)
    cf33cb4f3504f2214339d5639026390d658e7e23b66d6c0a031c2d908b747543: Mapped[int] = mapped_column(Integer)
    _5d4d708cc11d9e1fab27a11544c31c5a8650714f708ba033142aed971385ee22: Mapped[int] = mapped_column('5d4d708cc11d9e1fab27a11544c31c5a8650714f708ba033142aed971385ee22', Integer)
    _06db4652e888bbe2a35501611c9cb7b927a435b4fa003cf083a6f735ae573edb: Mapped[int] = mapped_column('06db4652e888bbe2a35501611c9cb7b927a435b4fa003cf083a6f735ae573edb', Integer)
    reward_id_19: Mapped[int] = mapped_column(Integer)
    _47bc5343a23c3ba1ca004668f99972724261ec510aa531a03b11a9a5b000f5a2: Mapped[int] = mapped_column('47bc5343a23c3ba1ca004668f99972724261ec510aa531a03b11a9a5b000f5a2', Integer)
    _09b3a9c66ccf13f1abae37ef26674343d7b1654b76ad19dd8aa0548be36e7305: Mapped[int] = mapped_column('09b3a9c66ccf13f1abae37ef26674343d7b1654b76ad19dd8aa0548be36e7305', Integer)
    b0d798a7961601b7dc5799617a6a1e296c72b1ea85ea07d85c01706170860f0c: Mapped[int] = mapped_column(Integer)
    _04bf12ef77adb0bd45260b1bd0e47f049dfe75cf57a47dc683ed632f8a33e1e2: Mapped[int] = mapped_column('04bf12ef77adb0bd45260b1bd0e47f049dfe75cf57a47dc683ed632f8a33e1e2', Integer)
    _6bb6405f3398ce6a3d976cb640c127d4fe95202217b507add28a2cf98940607d: Mapped[int] = mapped_column('6bb6405f3398ce6a3d976cb640c127d4fe95202217b507add28a2cf98940607d', Integer)
    reward_id_20: Mapped[int] = mapped_column(Integer)
    d93b806850bb384ab3460e474454de754761e8a54394499c5792205961fd0e50: Mapped[int] = mapped_column(Integer)
    _82ca1e9fb845dd570fa99599ea2d82283e04ecbb3b31c98afda5f947bd5a9e38: Mapped[int] = mapped_column('82ca1e9fb845dd570fa99599ea2d82283e04ecbb3b31c98afda5f947bd5a9e38', Integer)
    _93d82d35569c4ff9661bead3bf1173e7d636476741722f7ac201a630fabf47f8: Mapped[int] = mapped_column('93d82d35569c4ff9661bead3bf1173e7d636476741722f7ac201a630fabf47f8', Integer)
    _8fd95b699f4d4cd4bb653c3f0637eef8d45f8850a5cef5d8a9c0270dcf0f2486: Mapped[int] = mapped_column('8fd95b699f4d4cd4bb653c3f0637eef8d45f8850a5cef5d8a9c0270dcf0f2486', Integer)


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

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_name: Mapped[str] = mapped_column(Text)
    pick_up_chara_text: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    description_2: Mapped[str] = mapped_column(Text)
    description_sp: Mapped[str] = mapped_column(Text)
    tab_name: Mapped[str] = mapped_column(Text)
    title_id: Mapped[int] = mapped_column(Integer)
    _72fbdd7c98a98ceb80a8e09179e525c5f8f42f8fc39e39ad25cb18a77bfb04c8: Mapped[int] = mapped_column('72fbdd7c98a98ceb80a8e09179e525c5f8f42f8fc39e39ad25cb18a77bfb04c8', Integer)
    pickup_badge: Mapped[int] = mapped_column(Integer)
    gacha_detail: Mapped[int] = mapped_column(Integer)
    gacha_cost_type: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    free_gacha_type: Mapped[int] = mapped_column(Integer)
    free_gacha_interval_time: Mapped[int] = mapped_column(Integer)
    free_gacha_count: Mapped[int] = mapped_column(Integer)
    discount_price: Mapped[int] = mapped_column(Integer)
    _66ef8c63942f398c94b983ac87a4de9557326b08b28117d94bbe9c94ebe6689d: Mapped[str] = mapped_column('66ef8c63942f398c94b983ac87a4de9557326b08b28117d94bbe9c94ebe6689d', Text)
    _90525889c75bb41dba956a78a2e1a24d400ab5cb034419d380183ee182ceab8a: Mapped[str] = mapped_column('90525889c75bb41dba956a78a2e1a24d400ab5cb034419d380183ee182ceab8a', Text)
    gacha_type: Mapped[int] = mapped_column(Integer)
    movie_id: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)
    ticket_id: Mapped[int] = mapped_column(Integer)
    _7e58f2ece02ecb82720082d35d66776d3df8d8764fe1852d0d2fdb77cb475dad: Mapped[int] = mapped_column('7e58f2ece02ecb82720082d35d66776d3df8d8764fe1852d0d2fdb77cb475dad', Integer)
    exchange_id: Mapped[int] = mapped_column(Integer)
    ticket_id_10: Mapped[int] = mapped_column(Integer)
    fe9f63f3a78cdd85cc77172278f3ff2a961711ad18cf18255739206aee0a82be: Mapped[str] = mapped_column(Text)
    _0f6ee94768991bbf83368d85db839424010430559ebde0692b33a14c51803f27: Mapped[str] = mapped_column('0f6ee94768991bbf83368d85db839424010430559ebde0692b33a14c51803f27', Text)
    bec6286113e78aa8991d684bdd7a9827ca6cbc86935f39cf5837124cd337aaea: Mapped[str] = mapped_column(Text)
    _90389271c198450fbccae87f366662cc8be6f3200b5cbaab2dc872ecce4d5617: Mapped[str] = mapped_column('90389271c198450fbccae87f366662cc8be6f3200b5cbaab2dc872ecce4d5617', Text)
    _9fb02bbe4206a1ae3a4d68abb9b3a43945adaeea5c2b18112452dd8bb7eb5508: Mapped[str] = mapped_column('9fb02bbe4206a1ae3a4d68abb9b3a43945adaeea5c2b18112452dd8bb7eb5508', Text)
    _8559a9283fdc0dcca03129b91b58bf0fd5c688655d51005ebedf63bb37377b8c: Mapped[str] = mapped_column('8559a9283fdc0dcca03129b91b58bf0fd5c688655d51005ebedf63bb37377b8c', Text)
    _681af04fe23130ec14d6b99a21edee6852ea32331a79d22b5fd4b285ca2bc57b: Mapped[str] = mapped_column('681af04fe23130ec14d6b99a21edee6852ea32331a79d22b5fd4b285ca2bc57b', Text)
    prizegacha_id: Mapped[int] = mapped_column(Integer)
    _964a72b4195304de3d8e11e2634ff5a0e6d663289999342f51375aba5ff06818: Mapped[int] = mapped_column('964a72b4195304de3d8e11e2634ff5a0e6d663289999342f51375aba5ff06818', Integer)
    gacha_times_limit10: Mapped[int] = mapped_column(Integer)
    pickup_id: Mapped[int] = mapped_column(Integer)


class GachaExchangeLineup(Base):
    __tablename__ = 'gacha_exchange_lineup'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)
    rarity: Mapped[int] = mapped_column(Integer)
    _081829d577eb976ca897885bdd458244bcfe4c3a9d026140ed04562d8fb7cb78: Mapped[int] = mapped_column('081829d577eb976ca897885bdd458244bcfe4c3a9d026140ed04562d8fb7cb78', Integer)
    start_time: Mapped[str] = mapped_column(Text)
    end_time: Mapped[str] = mapped_column(Text)


class GachaPickup(Base):
    __tablename__ = 'gacha_pickup'

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

    _1903299b1bd54b15e23b5dff7cc20ad6a6d4a78c269c90380ba0446d06bbe6cd: Mapped[int] = mapped_column('1903299b1bd54b15e23b5dff7cc20ad6a6d4a78c269c90380ba0446d06bbe6cd', Integer)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_jewel_count: Mapped[int] = mapped_column(Integer)
    get_gold_count: Mapped[int] = mapped_column(Integer)
    b5e4c72d4b0af61a1257df361a9317491cb99ba7382c1ad9294013b2b9d766fc: Mapped[int] = mapped_column(Integer)
    a4b600a06beab5d3a373fd926212f7fdde4ec126dcae37b1ed1b178d41b78a3f: Mapped[int] = mapped_column(Integer)
    _11246b1e2133401b49d27b054498c001ed85630d1d946f9990af7b7545ad675a: Mapped[int] = mapped_column('11246b1e2133401b49d27b054498c001ed85630d1d946f9990af7b7545ad675a', Integer)
    c28db2a0242e99a77012ffeb6f2852a8846874cd36fd78abd8945c3a2f4f48f8: Mapped[int] = mapped_column(Integer)
    c5cff933df879586b3332d39f3cc8242626aeec097933032ead2dc4acfffc6e5: Mapped[int] = mapped_column(Integer)


class GoldsetData2(Base):
    __tablename__ = 'goldset_data_2'

    _981ea293815cc3f92754d829c66c932ff297b582b73c9c2a282aefc0d5590079: Mapped[int] = mapped_column('981ea293815cc3f92754d829c66c932ff297b582b73c9c2a282aefc0d5590079', Integer)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_jewel_count: Mapped[int] = mapped_column(Integer)
    get_gold_count: Mapped[int] = mapped_column(Integer)
    _541a011fe485926eb7316b3d1bf8ebb5379af20d31a7c959496f4808a31170cf: Mapped[int] = mapped_column('541a011fe485926eb7316b3d1bf8ebb5379af20d31a7c959496f4808a31170cf', Integer)
    bb7d97b37dbe264d050ddc09a2776f7a6ba83bac698996f2a0a9d55d6db591df: Mapped[int] = mapped_column(Integer)
    _621ce71e4f5d236bfbec56eefaa459705588a003869431f7c01b7e1998ff797a: Mapped[int] = mapped_column('621ce71e4f5d236bfbec56eefaa459705588a003869431f7c01b7e1998ff797a', Integer)
    d057b82abf1fce0a598bf1db0b5d6f10d5a3c51faf89f0e7123f40b4826e1a78: Mapped[int] = mapped_column(Integer)
    _4e5557dc6368b60fdb123f05a79e5923324082eb9cffdaf4dceb978c2c02bc63: Mapped[int] = mapped_column('4e5557dc6368b60fdb123f05a79e5923324082eb9cffdaf4dceb978c2c02bc63', Integer)
    training_quest_count: Mapped[int] = mapped_column(Integer)


class GoldsetDataTeamlevel(Base):
    __tablename__ = 'goldset_data_teamlevel'

    _6643549019c359cb840d82052bccacac14527f10ae7f7de51cc960ea5fa59896: Mapped[int] = mapped_column('6643549019c359cb840d82052bccacac14527f10ae7f7de51cc960ea5fa59896', Integer)
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_id: Mapped[int] = mapped_column(Integer)
    condition_type: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    target_type: Mapped[int] = mapped_column(Integer)
    bg_after_change_id: Mapped[int] = mapped_column(Integer)


class HatsuneBoss(Base):
    __tablename__ = 'hatsune_boss'

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
    _2c4c2973b7d269913c77e1241eeb560987bc6e0c9a7b4a852cba40250f867ae9: Mapped[str] = mapped_column('2c4c2973b7d269913c77e1241eeb560987bc6e0c9a7b4a852cba40250f867ae9', Text)
    _3604d692497b8e791d972db1a1e342b4edb590e94b420857f8a0b0e1c00ec146: Mapped[int] = mapped_column('3604d692497b8e791d972db1a1e342b4edb590e94b420857f8a0b0e1c00ec146', Integer)
    _7cd45ed96f0962b91d5f8e67288d4c6ef2b28dd9419bbb2a038420f033c36913: Mapped[str] = mapped_column('7cd45ed96f0962b91d5f8e67288d4c6ef2b28dd9419bbb2a038420f033c36913', Text)
    _69cfdcd13472afa580cd38f86cc224590d7895814ebd3f837a9742d4abdbb616: Mapped[str] = mapped_column('69cfdcd13472afa580cd38f86cc224590d7895814ebd3f837a9742d4abdbb616', Text)
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
    _50ad7e4b4689ed2b5490c4b9eda10d4d6fd1ce174cb0d1b14eac58a97a716b55: Mapped[int] = mapped_column('50ad7e4b4689ed2b5490c4b9eda10d4d6fd1ce174cb0d1b14eac58a97a716b55', Integer)
    _1532f0f9387f13a7eafdf7533d0771dff0ee3af3debbb972bdf4bafb64aefdc2: Mapped[str] = mapped_column('1532f0f9387f13a7eafdf7533d0771dff0ee3af3debbb972bdf4bafb64aefdc2', Text)
    _525531a3d4f00cea89cfbaf5df4113c566a6b508d24ed0eaa439b225a6508dbd: Mapped[int] = mapped_column('525531a3d4f00cea89cfbaf5df4113c566a6b508d24ed0eaa439b225a6508dbd', Integer)
    _8cac668f855117c6c438e21899e2dc9bea7cc4495d2a16cee2c8d9ba1987d357: Mapped[int] = mapped_column('8cac668f855117c6c438e21899e2dc9bea7cc4495d2a16cee2c8d9ba1987d357', Integer)
    ea21f30829b7daedeef874ac02a13a501905f7b1d4dd251654f89b13a64f9ddf: Mapped[int] = mapped_column(Integer)
    _3ac0d6c06e0a78a2b9c4aa909d9aa139fccad63314b4b2b7e625ed9a618c4bda: Mapped[int] = mapped_column('3ac0d6c06e0a78a2b9c4aa909d9aa139fccad63314b4b2b7e625ed9a618c4bda', Integer)


class HatsuneBossEnemySetting(Base):
    __tablename__ = 'hatsune_boss_enemy_setting'

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


class HatsuneBossExtraEffect(Base):
    __tablename__ = 'hatsune_boss_extra_effect'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)
    icon_id: Mapped[int] = mapped_column(Integer)
    detail: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(Text)


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)


class HatsuneDiaryDatum(Base):
    __tablename__ = 'hatsune_diary_data'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    icon_type: Mapped[int] = mapped_column(Integer)


class HatsuneExPlusSetting(Base):
    __tablename__ = 'hatsune_ex_plus_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_challenge_count: Mapped[int] = mapped_column(Integer)


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_event_id: Mapped[int] = mapped_column(Integer)
    event_type: Mapped[int] = mapped_column(Integer)
    condition_id: Mapped[int] = mapped_column(Integer)
    param1: Mapped[int] = mapped_column(Integer)
    param2: Mapped[int] = mapped_column(Integer)


class HatsuneMissionRewardDatum(Base):
    __tablename__ = 'hatsune_mission_reward_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneMultiRouteParameter(Base):
    __tablename__ = 'hatsune_multi_route_parameter'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    param_1: Mapped[int] = mapped_column(Integer)
    param_2: Mapped[int] = mapped_column(Integer)
    param_3: Mapped[int] = mapped_column(Integer)
    text_1: Mapped[str] = mapped_column(Text)


class HatsunePresent(Base):
    __tablename__ = 'hatsune_present'

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
    _2117c46558ec76feda55c3de59349e4b3d9c4b15b2b15de38f45f68048a4736e: Mapped[str] = mapped_column('2117c46558ec76feda55c3de59349e4b3d9c4b15b2b15de38f45f68048a4736e', Text)
    _3ac58e6009cbd5917498464978f86802a6e63e5f4c339d09fca17d0b46ef7a07: Mapped[str] = mapped_column('3ac58e6009cbd5917498464978f86802a6e63e5f4c339d09fca17d0b46ef7a07', Text)


class HatsuneQuestArea(Base):
    __tablename__ = 'hatsune_quest_area'

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    area_name: Mapped[str] = mapped_column(Text)
    map_type: Mapped[int] = mapped_column(Integer)
    sheet_id: Mapped[str] = mapped_column(Text)
    que_id: Mapped[str] = mapped_column(Text)
    d378c4707ef9e760873a278b6e0bd671eade8737d6a426b5b33085003e034768: Mapped[str] = mapped_column(Text)
    b5b3a648e2f06bd721881281397bd2c7eb5bef8e4eeb022007e125f72ff4ad5b: Mapped[str] = mapped_column(Text)
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)


class LegionQuestDatum(Base):
    __tablename__ = 'legion_quest_data'

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

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    love_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_unit_id: Mapped[int] = mapped_column(Integer)


class LsvDramaScript(Base):
    __tablename__ = 'lsv_drama_script'

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

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    time_condition: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    read_event_story_id: Mapped[int] = mapped_column(Integer)
    read_condition: Mapped[int] = mapped_column(Integer)


class LsvStoryScript(Base):
    __tablename__ = 'lsv_story_script'

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

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_story_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class Metamorphose(Base):
    __tablename__ = 'metamorphose'

    type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value: Mapped[int] = mapped_column(Integer, primary_key=True)
    prefab_id: Mapped[int] = mapped_column(Integer)


class MhpDramaScript(Base):
    __tablename__ = 'mhp_drama_script'

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

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    notif_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text)


class NydSetting(Base):
    __tablename__ = 'nyd_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    complete_emblem_id: Mapped[int] = mapped_column(Integer)


class NydStoryDatum(Base):
    __tablename__ = 'nyd_story_data'

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    is_first: Mapped[int] = mapped_column(Integer)
    nyd_story_type: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


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

    omp_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    a145d7dcfa99b599b8c67bf6f6b1e7f49619be578aa228ee0112dec512fbad68: Mapped[int] = mapped_column(Integer)
    cf88f3987820d0d8e2f4bdd3890b17bd612ca6914ed0d4369a1ae6ca995ca5b2: Mapped[int] = mapped_column(Integer)
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer)
    pct_point_coefficient: Mapped[int] = mapped_column(Integer)


class PctResult(Base):
    __tablename__ = 'pct_result'

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
    prize_memory_id_21: Mapped[int] = mapped_column(Integer)
    prize_memory_id_22: Mapped[int] = mapped_column(Integer)
    prize_memory_id_23: Mapped[int] = mapped_column(Integer)
    prize_memory_id_24: Mapped[int] = mapped_column(Integer)
    prize_memory_id_25: Mapped[int] = mapped_column(Integer)
    prize_memory_id_26: Mapped[int] = mapped_column(Integer)
    prize_memory_id_27: Mapped[int] = mapped_column(Integer)
    prize_memory_id_28: Mapped[int] = mapped_column(Integer)
    prize_memory_id_29: Mapped[int] = mapped_column(Integer)
    prize_memory_id_30: Mapped[int] = mapped_column(Integer)
    gacha_prize1: Mapped[int] = mapped_column(Integer)
    gacha_prize10: Mapped[int] = mapped_column(Integer)
    ec6cdf318c9ee20a2f84da307b80bf7a53369c657dfbbc548044fd957a2b9481: Mapped[int] = mapped_column(Integer)
    _68d5e3247a4a880b558ff8540b939077f7ad9d17e178f07f2a5ffe8bd8c5fb28: Mapped[int] = mapped_column('68d5e3247a4a880b558ff8540b939077f7ad9d17e178f07f2a5ffe8bd8c5fb28', Integer)
    _56075f91d7e9448b2fae22060c8b66e302e640bbb6cd8de9aef01399e188adee: Mapped[int] = mapped_column('56075f91d7e9448b2fae22060c8b66e302e640bbb6cd8de9aef01399e188adee', Integer)
    disp_prize_fixed_compensation: Mapped[int] = mapped_column(Integer)


class PrizegachaSpDatum(Base):
    __tablename__ = 'prizegacha_sp_data'

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
    af627221b1a9eac517db9881993a21891d1a2fc5e32bd672b127e8ae48cbc65b: Mapped[int] = mapped_column(Integer)
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
    _273145448f498d5299b1ed7396ec69972d314e3f24b945bc6543477d188cea2d: Mapped[int] = mapped_column('273145448f498d5299b1ed7396ec69972d314e3f24b945bc6543477d188cea2d', Integer)
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
    eb9f2a500ec476dcae332e764d80c4c642a42267bb19d188263d6962d193d7f6: Mapped[int] = mapped_column(Integer)
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
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


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
    _4143c6a3249ae3852a35b9c1e9e33d8ecc84b08c1c2f046fbf10306828bd8c38: Mapped[int] = mapped_column('4143c6a3249ae3852a35b9c1e9e33d8ecc84b08c1c2f046fbf10306828bd8c38', Integer)
    _332be3d2825d7bffe32fb73acb20fdb500b7a5f8f47d94a6749b9974b9396d18: Mapped[int] = mapped_column('332be3d2825d7bffe32fb73acb20fdb500b7a5f8f47d94a6749b9974b9396d18', Integer)
    chest_id: Mapped[int] = mapped_column(Integer)
    _28e77d7dc8e61510065c776cf3b0cd35c5db6abb2172b137e633333168936827: Mapped[int] = mapped_column('28e77d7dc8e61510065c776cf3b0cd35c5db6abb2172b137e633333168936827', Integer)
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
    _9332309e1d07153d0b394b93d945067bf7e05c6b1a0d87fbe74df86d76b6da44: Mapped[int] = mapped_column('9332309e1d07153d0b394b93d945067bf7e05c6b1a0d87fbe74df86d76b6da44', Integer)


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
    b28847cf2586a95c850d113ddec4d8537da6f8fa1a2e89c36ed0951892150133: Mapped[int] = mapped_column(Integer)
    d2985af7ba8ffb4844fc4b8690268375141acfad135be1808da7218d2620fac1: Mapped[int] = mapped_column(Integer)


class ShioriDescription(Base):
    __tablename__ = 'shiori_description'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_num: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriQuest(Base):
    __tablename__ = 'shiori_quest'

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

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    unlock_condition_quest_id: Mapped[int] = mapped_column(Integer)
    unlock_condition_boss_id: Mapped[int] = mapped_column(Integer)
    read_condition_event_story_id: Mapped[int] = mapped_column(Integer)


class SkeStoryScript(Base):
    __tablename__ = 'ske_story_script'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer)
    add_times: Mapped[int] = mapped_column(Integer)
    add_times_time: Mapped[str] = mapped_column(Text)


class SreBattleBonus(Base):
    __tablename__ = 'sre_battle_bonus'

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
    ab051262aee45410b04731058d10a635d50dfaab6b7aa68782f45b8cbf8168dc: Mapped[int] = mapped_column(Integer)
    _9325b33689047ad78ca93971aff4d70b1669eeaa21edfc735e09851cce54e448: Mapped[int] = mapped_column('9325b33689047ad78ca93971aff4d70b1669eeaa21edfc735e09851cce54e448', Integer)
    _2f2744e639fde84ac7bfd127a3965ae0c808856a5a2f7d465f961acc5e1baf35: Mapped[int] = mapped_column('2f2744e639fde84ac7bfd127a3965ae0c808856a5a2f7d465f961acc5e1baf35', Integer)
    _4e7a70dac389aafa9b394e2291755420d181043cf25cc6c537b033fff33f753e: Mapped[int] = mapped_column('4e7a70dac389aafa9b394e2291755420d181043cf25cc6c537b033fff33f753e', Integer)
    _377b639c39596722407ec42d7c8fe3783341ff5d6fb3300697932eeaa9b3d611: Mapped[int] = mapped_column('377b639c39596722407ec42d7c8fe3783341ff5d6fb3300697932eeaa9b3d611', Integer)


class SrtTopTalk(Base):
    __tablename__ = 'srt_top_talk'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talk_id: Mapped[int] = mapped_column(Integer)
    chara_index: Mapped[int] = mapped_column(Integer)
    talk_text: Mapped[str] = mapped_column(Text)
    sheet_name: Mapped[str] = mapped_column(Text)
    cue_name: Mapped[str] = mapped_column(Text)
    direction: Mapped[int] = mapped_column(Integer)


class SspStoryDatum(Base):
    __tablename__ = 'ssp_story_data'

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
    can_bookmark: Mapped[int] = mapped_column(Integer)
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
    _714000a5a303f8bcb2143206c8fb5bacfc70b2194b18892e0404a027f825c0ce: Mapped[int] = mapped_column('714000a5a303f8bcb2143206c8fb5bacfc70b2194b18892e0404a027f825c0ce', Integer)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text)
    background_2: Mapped[int] = mapped_column(Integer)
    d4c10192cfa3df5a7f10fdc043ce014df8d2e29758022a2449e6884edfcff587: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text)
    background_3: Mapped[int] = mapped_column(Integer)
    ca5b1bcb1c9a88e530bd50068925fe78697ada3a6a71fe5ee01a73f3d0c9d0d8: Mapped[int] = mapped_column(Integer)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text)
    guest_unit_1: Mapped[int] = mapped_column(Integer)
    guest_unit_2: Mapped[int] = mapped_column(Integer)
    guest_unit_3: Mapped[int] = mapped_column(Integer)
    guest_unit_4: Mapped[int] = mapped_column(Integer)
    guest_unit_5: Mapped[int] = mapped_column(Integer)


class SvdDramaScript(Base):
    __tablename__ = 'svd_drama_script'

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

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    read_condition_time: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_boss_id: Mapped[int] = mapped_column(Integer)
    read_condition: Mapped[int] = mapped_column(Integer)


class SvdStoryScript(Base):
    __tablename__ = 'svd_story_script'

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
    _5a4bd5a32984c842810a7229828ebc49917d2c7702c962923c0cd5b14fd7aa58: Mapped[str] = mapped_column('5a4bd5a32984c842810a7229828ebc49917d2c7702c962923c0cd5b14fd7aa58', Text)
    _6664c040775d90690cd12e6b9a09c467f1baee80d988701d79d98ebd6d36971d: Mapped[str] = mapped_column('6664c040775d90690cd12e6b9a09c467f1baee80d988701d79d98ebd6d36971d', Text)
    ec1634c4a54360cf7be0394f5fff142c6341db3b36c8bbb677c51733c84e4f0c: Mapped[str] = mapped_column(Text)
    _689f0a1ea1c7a42cbfa5acb0651ff543113eaa245f2a6f94a8765e6b8bbdcc51: Mapped[str] = mapped_column('689f0a1ea1c7a42cbfa5acb0651ff543113eaa245f2a6f94a8765e6b8bbdcc51', Text)
    _2e5ead8a61746da40bc18831122284870c3144d0158ee34982c4bc9166587747: Mapped[str] = mapped_column('2e5ead8a61746da40bc18831122284870c3144d0158ee34982c4bc9166587747', Text)
    staging_type: Mapped[int] = mapped_column(Integer)


class Tips(Base):
    __tablename__ = 'tips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)
    tips_index: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)


class TmeMapDatum(Base):
    __tablename__ = 'tme_map_data'

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

    tower_ex_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tower_area_id: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    _334801301ae2ee74a225115d2adcf7fb2dec33d48d9c998ca31fc7ba4c563daf: Mapped[int] = mapped_column('334801301ae2ee74a225115d2adcf7fb2dec33d48d9c998ca31fc7ba4c563daf', Integer)
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

    tower_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tower_area_id: Mapped[int] = mapped_column(Integer)
    floor_num: Mapped[int] = mapped_column(Integer)
    floor_image_type: Mapped[int] = mapped_column(Integer)
    floor_image_add_type: Mapped[int] = mapped_column(Integer)
    open_tower_ex_quest_id: Mapped[int] = mapped_column(Integer)
    boss_floor_flg: Mapped[int] = mapped_column(Integer)
    stamina: Mapped[int] = mapped_column(Integer)
    stamina_start: Mapped[int] = mapped_column(Integer)
    bf70f6f550aad58dfbd745b12897728e9d0270085107420aaa75bd14c5ffe631: Mapped[int] = mapped_column(Integer)
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

    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_1: Mapped[int] = mapped_column(Integer)
    be12884e6eea999a34f376ab22cb5666033dc3df51bbd1163b6b2b7b716986fe: Mapped[str] = mapped_column(Text)
    treasure_type_2: Mapped[int] = mapped_column(Integer)
    fdb7c0cab293d102cb4924641fcde2e7f3a1f682f499f2086164f3e623a0b6f0: Mapped[str] = mapped_column(Text)
    treasure_type_3: Mapped[int] = mapped_column(Integer)
    _4b7239fbfb3a60d237c42790596fc1ab840c394fb3777fcfc8b2c98f51243271: Mapped[str] = mapped_column('4b7239fbfb3a60d237c42790596fc1ab840c394fb3777fcfc8b2c98f51243271', Text)
    treasure_type_4: Mapped[int] = mapped_column(Integer)
    _5a63307069fd6337f6646cf718c14354fe45f6194a69f3b05a961d4177cdbfba: Mapped[str] = mapped_column('5a63307069fd6337f6646cf718c14354fe45f6194a69f3b05a961d4177cdbfba', Text)
    treasure_type_5: Mapped[int] = mapped_column(Integer)
    _98dbaa0a18bb1aa97f76d993762aa6361e4962533a9a378b6e2a4232fa3e44d2: Mapped[str] = mapped_column('98dbaa0a18bb1aa97f76d993762aa6361e4962533a9a378b6e2a4232fa3e44d2', Text)
    treasure_type_6: Mapped[int] = mapped_column(Integer)
    e6609b44e785c314c0839091afc371a636e83aeeaacbf23503d927873b343d24: Mapped[str] = mapped_column(Text)
    treasure_type_7: Mapped[int] = mapped_column(Integer)
    e8c1967df7eb688fa7dfe25c3702f7200ea561086b120c134b21de5530db7f95: Mapped[str] = mapped_column(Text)
    treasure_type_8: Mapped[int] = mapped_column(Integer)
    _4f897858672b174df0bf291380494f9db3b3685d63d9504c95ace17f98e87931: Mapped[str] = mapped_column('4f897858672b174df0bf291380494f9db3b3685d63d9504c95ace17f98e87931', Text)
    treasure_type_9: Mapped[int] = mapped_column(Integer)
    f2950b3bf46219f89bb04094c77a9a700d6dcc9d72173be7d9669518fd33aab4: Mapped[str] = mapped_column(Text)
    treasure_type_10: Mapped[int] = mapped_column(Integer)
    _4db46ee4be3e054fde2e67db725e3df6e75817dcb533d224e3c57d96dd1c9584: Mapped[str] = mapped_column('4db46ee4be3e054fde2e67db725e3df6e75817dcb533d224e3c57d96dd1c9584', Text)


class TowerSchedule(Base):
    __tablename__ = 'tower_schedule'

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
    can_bookmark: Mapped[int] = mapped_column(Integer)
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
    _3ed177daf85109fddcd06c8634bff380a15a03aa1266ad099e041135ed09e309: Mapped[int] = mapped_column('3ed177daf85109fddcd06c8634bff380a15a03aa1266ad099e041135ed09e309', Integer)
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    situation_group_id: Mapped[int] = mapped_column(Integer)
    situation_id: Mapped[int] = mapped_column(Integer)


class TravelQuestSubReward(Base):
    __tablename__ = 'travel_quest_sub_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    disp_order: Mapped[int] = mapped_column(Integer)


class TravelResultExceptUnitGroup(Base):
    __tablename__ = 'travel_result_except_unit_group'

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

    top_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    f4eb1b09bf0ca37828f5fb73bb46879f56e770d54e3f1cf3349101194d856c62: Mapped[int] = mapped_column(Integer)
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
    _37a55c23cfa5fb5195535d450a206169692b25c4737c071809bcf8fde14c758e: Mapped[int] = mapped_column('37a55c23cfa5fb5195535d450a206169692b25c4737c071809bcf8fde14c758e', Integer)
    top_icon_type: Mapped[int] = mapped_column(Integer)


class TravelTopEventDrama(Base):
    __tablename__ = 'travel_top_event_drama'

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
    fc44846adaad86b0bb56918e0b809c3b6b3a39295371b6dac966575f2ec96b9f: Mapped[int] = mapped_column(Integer)
    pos_x: Mapped[int] = mapped_column(Integer)
    pos_y: Mapped[int] = mapped_column(Integer)
    _0f97121e2bddd2a55d105118bffb95419d31d79f4a5aaedce9af71e2a33bdb46: Mapped[int] = mapped_column('0f97121e2bddd2a55d105118bffb95419d31d79f4a5aaedce9af71e2a33bdb46', Integer)


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

    ttk_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ttk_score: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)


class TtkStoryScript(Base):
    __tablename__ = 'ttk_story_script'

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

    spine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    anim_num: Mapped[int] = mapped_column(Integer)


class UniqueEquipConsumeGroup(Base):
    __tablename__ = 'unique_equip_consume_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    index_in_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer)


class UniqueEquipCraftEnhance(Base):
    __tablename__ = 'unique_equip_craft_enhance'

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_group_id: Mapped[int] = mapped_column(Integer)


class UniqueEquipEnhanceRate(Base):
    __tablename__ = 'unique_equip_enhance_rate'

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
    f098976cf592392561b59ced0fa200ed28ed25b44b48874f5b5fa2c65b41a534: Mapped[str] = mapped_column(Text)
    _69f1dedc075748e046e8ebf87d940e9d98bcb4baadcab32a92466145a623268e: Mapped[str] = mapped_column('69f1dedc075748e046e8ebf87d940e9d98bcb4baadcab32a92466145a623268e', Text)
    d1dcda56a74d26d46ac66d2cb84877057879752b9bca52032f0827209d7a91c3: Mapped[int] = mapped_column(Integer)
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

    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer)


class UnitDatum(Base):
    __tablename__ = 'unit_data'

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

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_id: Mapped[int] = mapped_column(Integer)


class UnlockRarity6(Base):
    __tablename__ = 'unlock_rarity_6'

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_search_id: Mapped[int] = mapped_column(Integer)
    unit_id: Mapped[int] = mapped_column(Integer)


class WaveGroupDatum(Base):
    __tablename__ = 'wave_group_data'

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

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repeat_story_id: Mapped[int] = mapped_column(Integer)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class XacStoryDatum(Base):
    __tablename__ = 'xac_story_data'

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    sub_title: Mapped[str] = mapped_column(Text)
    condition_quest_id: Mapped[int] = mapped_column(Integer)
    condition_time: Mapped[str] = mapped_column(Text)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer)
    day: Mapped[int] = mapped_column(Integer)
    balloon_pos_x: Mapped[float] = mapped_column(Float)
    balloon_pos_y: Mapped[float] = mapped_column(Float)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class XehStoryDatum(Base):
    __tablename__ = 'xeh_story_data'

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    reward_type: Mapped[int] = mapped_column(Integer)
    reward_id: Mapped[int] = mapped_column(Integer)
    reward_count: Mapped[int] = mapped_column(Integer)


class YsnStoryDatum(Base):
    __tablename__ = 'ysn_story_data'

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
