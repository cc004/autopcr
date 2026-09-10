# coding: utf-8
# type: ignore
# Data( => Datum(

from typing import Optional

from sqlalchemy import Index, Integer, REAL, Text, UniqueConstraint
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from typing import Generic, TypeVar
from ..util.linq import flow

T = TypeVar('T')

class Base(DeclarativeBase, Generic[T]):
    @classmethod
    def query(cls, session: Session) -> flow[T]:
        return flow(session.query(cls).all())


class AbdStoryDatum(Base):
    __tablename__ = 'abd_story_data'
    __table_args__ = (
        Index('abd_story_data_0_original_event_id', 'original_event_id'),
    )

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AbdStoryScript(Base):
    __tablename__ = 'abd_story_script'
    __table_args__ = (
        Index('abd_story_script_0_sub_story_id', 'sub_story_id'),
    )

    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AbyssBattleEffect(Base):
    __tablename__ = 'abyss_battle_effect'
    __table_args__ = (
        Index('abyss_battle_effect_0_quest_id', 'quest_id'),
    )

    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class AbyssBossDatum(Base):
    __tablename__ = 'abyss_boss_data'
    __table_args__ = (
        Index('abyss_boss_data_0_abyss_id', 'abyss_id'),
    )

    first_clear_score_bonus: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drop_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    score_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    use_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)
    release_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssBossDisplayDatum(Base):
    __tablename__ = 'abyss_boss_display_data'

    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    result_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AbyssClearReward(Base):
    __tablename__ = 'abyss_clear_reward'

    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssEnemyParameter(Base):
    __tablename__ = 'abyss_enemy_parameter'

    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssQuestDatum(Base):
    __tablename__ = 'abyss_quest_data'
    __table_args__ = (
        Index('abyss_quest_data_0_abyss_id', 'abyss_id'),
    )

    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssQuestDisplayDatum(Base):
    __tablename__ = 'abyss_quest_display_data'

    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_scale_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_5: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_scale_2: Mapped[float] = mapped_column(REAL, nullable=False)


class AbyssSchedule(Base):
    __tablename__ = 'abyss_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    talent_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)


class AbyssScoreReward(Base):
    __tablename__ = 'abyss_score_reward'
    __table_args__ = (
        Index('abyss_score_reward_0_abyss_id', 'abyss_id'),
    )

    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssWaveGroupDatum(Base):
    __tablename__ = 'abyss_wave_group_data'
    __table_args__ = (
        Index('abyss_wave_group_data_0_wave_group_id', 'wave_group_id'),
    )

    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnAdv(Base):
    __tablename__ = 'acn_adv'
    __table_args__ = (
        Index('acn_adv_0_trigger_type', 'trigger_type'),
    )

    trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnEndlessBattleSetting(Base):
    __tablename__ = 'acn_endless_battle_setting'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_gold_num: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnEnemyParameter(Base):
    __tablename__ = 'acn_enemy_parameter'

    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnGaugeSectionDatum(Base):
    __tablename__ = 'acn_gauge_section_data'
    __table_args__ = (
        Index('acn_gauge_section_data_0_gauge_mission_id', 'gauge_mission_id'),
    )

    gauge_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[int] = mapped_column(Integer, primary_key=True)
    rate_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    inferior_trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    superior_trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnMissionDatum(Base):
    __tablename__ = 'acn_mission_data'
    __table_args__ = (
        Index('acn_mission_data_0_mission_condition', 'mission_condition'),
    )

    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    acn_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class AcnMissionRewardDatum(Base):
    __tablename__ = 'acn_mission_reward_data'
    __table_args__ = (
        Index('acn_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnMultiBossSetting(Base):
    __tablename__ = 'acn_multi_boss_setting'

    die_position_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    die_motion_pause_time: Mapped[float] = mapped_column(REAL, nullable=False)
    die_position_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnQuestDatum(Base):
    __tablename__ = 'acn_quest_data'

    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    restriction_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_2: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_offset_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    deck_number: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_offset_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_3: Mapped[float] = mapped_column(REAL, nullable=False)
    lane_priority_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    next_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    aura_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    gauge_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnQuestDifficultyDatum(Base):
    __tablename__ = 'acn_quest_difficulty_data'
    __table_args__ = (
        Index('acn_quest_difficulty_data_0_condition_id', 'condition_id'),
        Index('acn_quest_difficulty_data_0_quest_id', 'quest_id'),
        Index('acn_quest_difficulty_data_0_quest_id_1_difficulty', 'quest_id', 'difficulty')
    )

    consume_boss_ticket: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnRestrictionUnitGroup(Base):
    __tablename__ = 'acn_restriction_unit_group'
    __table_args__ = (
        Index('acn_restriction_unit_group_0_restriction_group_id', 'restriction_group_id'),
    )

    restriction_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnSchedule(Base):
    __tablename__ = 'acn_schedule'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    after_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_accept_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class AcnSpecialBattle(Base):
    __tablename__ = 'acn_special_battle'

    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)


class AcnStorySkipReward(Base):
    __tablename__ = 'acn_story_skip_reward'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnUnknownBattle(Base):
    __tablename__ = 'acn_unknown_battle'

    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    step: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnWaveGroupDatum(Base):
    __tablename__ = 'acn_wave_group_data'

    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ActualUnitBackground(Base):
    __tablename__ = 'actual_unit_background'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)


class AilmentDatum(Base):
    __tablename__ = 'ailment_data'

    ailment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ailment_action: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AisSetting(Base):
    __tablename__ = 'ais_setting'

    first_op_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_op_release_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    last_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    later_op_release_condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    later_op_release_condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    later_op_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AisStoryDatum(Base):
    __tablename__ = 'ais_story_data'
    __table_args__ = (
        Index('ais_story_data_0_original_event_id', 'original_event_id'),
        Index('ais_story_data_0_read_condition_sub_story_id', 'read_condition_sub_story_id'),
        Index('ais_story_data_0_unlock_condition_sub_story_id', 'unlock_condition_sub_story_id')
    )

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AlbumProductionList(Base):
    __tablename__ = 'album_production_list'
    __table_args__ = (
        Index('album_production_list_0_unit_id', 'unit_id'),
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AlbumVoiceList(Base):
    __tablename__ = 'album_voice_list'
    __table_args__ = (
        Index('album_voice_list_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AlcesCost(Base):
    __tablename__ = 'alces_cost'

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AlcesDrama(Base):
    __tablename__ = 'alces_drama'
    __table_args__ = (
        Index('alces_drama_0_story_id', 'story_id'),
    )

    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AlcesDramaScript(Base):
    __tablename__ = 'alces_drama_script'
    __table_args__ = (
        Index('alces_drama_script_0_drama_id', 'drama_id'),
    )

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class AlcesExecCost(Base):
    __tablename__ = 'alces_exec_cost'

    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    alces_purpose: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class AlcesSetting(Base):
    __tablename__ = 'alces_setting'

    setting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class AlcesStory(Base):
    __tablename__ = 'alces_story'

    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AlternativeItemDatum(Base):
    __tablename__ = 'alternative_item_data'
    __table_args__ = (
        Index('alternative_item_data_0_dst_item_id', 'dst_item_id'),
    )

    src_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dst_item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ApaSchedule(Base):
    __tablename__ = 'apa_schedule'

    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    apa_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    url_1: Mapped[str] = mapped_column(Text, nullable=False)
    url_2: Mapped[str] = mapped_column(Text, nullable=False)
    ed_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    op_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    url_3: Mapped[str] = mapped_column(Text, nullable=False)


class ApgAttractionDatum(Base):
    __tablename__ = 'apg_attraction_data'

    detail_description: Mapped[str] = mapped_column(Text, nullable=False)
    attraction_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ApgDramaScript(Base):
    __tablename__ = 'apg_drama_script'
    __table_args__ = (
        Index('apg_drama_script_0_drama_id', 'drama_id'),
    )

    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class ApgStoryDatum(Base):
    __tablename__ = 'apg_story_data'
    __table_args__ = (
        Index('apg_story_data_0_attraction_id', 'attraction_id'),
        Index('apg_story_data_0_original_event_id', 'original_event_id')
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    attraction_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AppIcon(Base):
    __tablename__ = 'app_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ArcadeDescription(Base):
    __tablename__ = 'arcade_description'
    __table_args__ = (
        Index('arcade_description_0_arcade_id', 'arcade_id'),
        Index('arcade_description_0_arcade_id_1_type', 'arcade_id', 'type')
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    arcade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class ArcadeList(Base):
    __tablename__ = 'arcade_list'

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_chat_title: Mapped[str] = mapped_column(Text, nullable=False)
    arcade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    banner_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    banner_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_id: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class ArcadeStoryList(Base):
    __tablename__ = 'arcade_story_list'
    __table_args__ = (
        Index('arcade_story_list_0_arcade_id', 'arcade_id'),
    )

    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arcade_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaDailyRankReward(Base):
    __tablename__ = 'arena_daily_rank_reward'

    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaDefenceReward(Base):
    __tablename__ = 'arena_defence_reward'

    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_count: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaMaxRankReward(Base):
    __tablename__ = 'arena_max_rank_reward'

    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaMaxSeasonRankReward(Base):
    __tablename__ = 'arena_max_season_rank_reward'

    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AsbDramaScript(Base):
    __tablename__ = 'asb_drama_script'
    __table_args__ = (
        Index('asb_drama_script_0_drama_id', 'drama_id'),
    )

    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)


class AsbStoryDatum(Base):
    __tablename__ = 'asb_story_data'
    __table_args__ = (
        Index('asb_story_data_0_condition_sub_story_id', 'condition_sub_story_id'),
        Index('asb_story_data_0_original_event_id', 'original_event_id')
    )

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    page_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class Asm4ChoiceDatum(Base):
    __tablename__ = 'asm_4_choice_data'

    choice_2: Mapped[str] = mapped_column(Text, nullable=False)
    image_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_4: Mapped[str] = mapped_column(Text, nullable=False)
    choice_1: Mapped[str] = mapped_column(Text, nullable=False)
    correct_answer: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_3: Mapped[str] = mapped_column(Text, nullable=False)


class AsmArchiveCompletionReward(Base):
    __tablename__ = 'asm_archive_completion_reward'
    __table_args__ = (
        Index('asm_archive_completion_reward_0_emblem_id', 'emblem_id'),
    )

    archive_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_detail: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmDatum(Base):
    __tablename__ = 'asm_data'
    __table_args__ = (
        Index('asm_data_0_difficulty', 'difficulty'),
        Index('asm_data_0_genre_id', 'genre_id'),
        Index('asm_data_0_genre_id_1_difficulty', 'genre_id', 'difficulty')
    )

    asm_type: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmGameSetting(Base):
    __tablename__ = 'asm_game_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concentration_quiz_limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    incorrect_answer_penalty_time: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    concentration_limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_concentration_mode_score_2: Mapped[int] = mapped_column(Integer, nullable=False)
    help_use_count_hard: Mapped[int] = mapped_column(Integer, nullable=False)
    lottery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    help_use_count_veryhard: Mapped[int] = mapped_column(Integer, nullable=False)
    help_use_count_normal: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_quiz_num: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_concentration_mode_score_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_score: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmManyAnswersDatum(Base):
    __tablename__ = 'asm_many_answers_data'

    choice_3: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct_2: Mapped[int] = mapped_column(Integer, nullable=False)
    is_correct_1: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    is_correct_4: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_4: Mapped[str] = mapped_column(Text, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    choice_1: Mapped[str] = mapped_column(Text, nullable=False)
    image_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    is_correct_3: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_2: Mapped[str] = mapped_column(Text, nullable=False)


class AsmMemoryGauge(Base):
    __tablename__ = 'asm_memory_gauge'
    __table_args__ = (
        Index('asm_memory_gauge_0_gauge_id', 'gauge_id'),
        Index('asm_memory_gauge_0_unlock_story_id', 'unlock_story_id')
    )

    gauge_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_score: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmReactionDatum(Base):
    __tablename__ = 'asm_reaction_data'
    __table_args__ = (
        Index('asm_reaction_data_0_unit_id_1_reaction_type', 'unit_id', 'reaction_type'),
    )

    face_change_time: Mapped[float] = mapped_column(REAL, nullable=False)
    condition_param_1: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    reaction_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_change_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_param_2: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_param_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmTrueOrFalseDatum(Base):
    __tablename__ = 'asm_true_or_false_data'

    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    correct_answer: Mapped[int] = mapped_column(Integer, nullable=False)


class Banner(Base):
    __tablename__ = 'banner'

    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    poster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_show_room: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    show_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BannerNews(Base):
    __tablename__ = 'banner_news'

    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    show_type: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_show_room: Mapped[int] = mapped_column(Integer, nullable=False)


class BeginnerCharaETicketDatum(Base):
    __tablename__ = 'beginner_chara_e_ticket_data'

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_e_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    beginner_type: Mapped[int] = mapped_column(Integer, nullable=False)
    beginner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beginner_limit_hour: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    forced_exchange_hour: Mapped[int] = mapped_column(Integer, nullable=False)
    jewel_store_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BgDatum(Base):
    __tablename__ = 'bg_data'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    view_name: Mapped[str] = mapped_column(Text, primary_key=True)


class BirthdayLoginBonusDatum(Base):
    __tablename__ = 'birthday_login_bonus_data'

    login_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    login_bonus_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BirthdayLoginBonusDetail(Base):
    __tablename__ = 'birthday_login_bonus_detail'
    __table_args__ = (
        Index('birthday_login_bonus_detail_0_login_bonus_id', 'login_bonus_id'),
    )

    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BirthdayLoginBonusDramaScript(Base):
    __tablename__ = 'birthday_login_bonus_drama_script'
    __table_args__ = (
        Index('birthday_login_bonus_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)


class BmyNaviComment(Base):
    __tablename__ = 'bmy_navi_comment'
    __table_args__ = (
        Index('bmy_navi_comment_0_where_type', 'where_type'),
    )

    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)


class BmyStoryDatum(Base):
    __tablename__ = 'bmy_story_data'
    __table_args__ = (
        Index('bmy_story_data_0_original_event_id', 'original_event_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BroadcastSchedule(Base):
    __tablename__ = 'broadcast_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    button_text: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    broadcast_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dialog_title: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)


class BsmActionDatum(Base):
    __tablename__ = 'bsm_action_data'

    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    value_6: Mapped[int] = mapped_column(Integer, nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmActionTrigger(Base):
    __tablename__ = 'bsm_action_trigger'
    __table_args__ = (
        Index('bsm_action_trigger_0_trigger_id', 'trigger_id'),
    )

    trigger_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmBackground(Base):
    __tablename__ = 'bsm_background'
    __table_args__ = (
        Index('bsm_background_0_background_id', 'background_id'),
    )

    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    background_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_outdoor: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BsmChara(Base):
    __tablename__ = 'bsm_chara'
    __table_args__ = (
        Index('bsm_chara_0_unlock_solo_mode_id', 'unlock_solo_mode_id'),
    )

    bsm_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    passive_support_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    active_trigger_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_description: Mapped[str] = mapped_column(Text, nullable=False)
    effect_title: Mapped[str] = mapped_column(Text, nullable=False)
    unlock_solo_mode_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    is_leader: Mapped[int] = mapped_column(Integer, nullable=False)
    active_trigger_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_support_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    skin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_support_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmDefaultMachines(Base):
    __tablename__ = 'bsm_default_machines'

    machine_name: Mapped[str] = mapped_column(Text, nullable=False)
    machine_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BsmDramaScript(Base):
    __tablename__ = 'bsm_drama_script'
    __table_args__ = (
        Index('bsm_drama_script_0_drama_id', 'drama_id'),
    )

    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class BsmMission(Base):
    __tablename__ = 'bsm_mission'

    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    premise_cleared_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    navigation: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmMissionReward(Base):
    __tablename__ = 'bsm_mission_reward'
    __table_args__ = (
        Index('bsm_mission_reward_0_mission_reward_id', 'mission_reward_id'),
    )

    joint_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmNaviComment(Base):
    __tablename__ = 'bsm_navi_comment'
    __table_args__ = (
        Index('bsm_navi_comment_0_where_type', 'where_type'),
    )

    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class BsmParts(Base):
    __tablename__ = 'bsm_parts'
    __table_args__ = (
        Index('bsm_parts_0_category', 'category'),
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)
    shape: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attack: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmPartsBonus(Base):
    __tablename__ = 'bsm_parts_bonus'

    bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_shape: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    target_category: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_target: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmPartsJoint(Base):
    __tablename__ = 'bsm_parts_joint'

    weapon_pos_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    gadget_pos_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_pos_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_pos_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    joint_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gadget_pos_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_pos_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_pos_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_pos_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmPartsJointIcon(Base):
    __tablename__ = 'bsm_parts_joint_icon'
    __table_args__ = (
        Index('bsm_parts_joint_icon_0_shape', 'shape'),
    )

    pos_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shape: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmPassiveSupport(Base):
    __tablename__ = 'bsm_passive_support'

    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_support_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_target: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmRecycle(Base):
    __tablename__ = 'bsm_recycle'
    __table_args__ = (
        Index('bsm_recycle_0_category', 'category'),
    )

    time: Mapped[int] = mapped_column(Integer, nullable=False)
    is_bonus: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    recycle_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BsmSoloMode(Base):
    __tablename__ = 'bsm_solo_mode'
    __table_args__ = (
        Index('bsm_solo_mode_0_stage_num', 'stage_num'),
    )

    member_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)
    gadget_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_num: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_parts_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    gadget_bonus_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    gadget_bonus_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    solo_mode_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wheel_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_bonus_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_parts_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    gadget_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_bonus_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_bonus_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    machine_name: Mapped[str] = mapped_column(Text, nullable=False)
    weapon_bonus_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    body_parts_id: Mapped[int] = mapped_column(Integer, nullable=False)
    member_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    weapon_bonus_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    leader_id: Mapped[int] = mapped_column(Integer, nullable=False)
    body_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    body_joint_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wheel_bonus_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmSoloModeReward(Base):
    __tablename__ = 'bsm_solo_mode_reward'
    __table_args__ = (
        Index('bsm_solo_mode_reward_0_solo_mode_id', 'solo_mode_id'),
    )

    joint_id: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    solo_mode_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_slot_num: Mapped[int] = mapped_column(Integer, primary_key=True)


class BsmTriggerConditionCollide(Base):
    __tablename__ = 'bsm_trigger_condition_collide'

    collide_target: Mapped[int] = mapped_column(Integer, nullable=False)
    collide_type: Mapped[int] = mapped_column(Integer, nullable=False)
    collider_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timing: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmTriggerConditionTime(Base):
    __tablename__ = 'bsm_trigger_condition_time'

    condition_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wait_time: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmTriggerConditionValue(Base):
    __tablename__ = 'bsm_trigger_condition_value'

    threshold: Mapped[int] = mapped_column(Integer, nullable=False)
    target_value_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    compare_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BsmTriggerDatum(Base):
    __tablename__ = 'bsm_trigger_data'
    __table_args__ = (
        Index('bsm_trigger_data_0_bsm_object_type', 'bsm_object_type'),
    )

    cool_time: Mapped[int] = mapped_column(Integer, nullable=False)
    bsm_object_type: Mapped[int] = mapped_column(Integer, nullable=False)
    object_index: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bsm_object_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BulletinCalendar(Base):
    __tablename__ = 'bulletin_calendar'

    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_show_room: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    show_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)


class BywayBattleQuestDatum(Base):
    __tablename__ = 'byway_battle_quest_data'

    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_restrict_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)


class BywayDeliveryQuestDatum(Base):
    __tablename__ = 'byway_delivery_quest_data'
    __table_args__ = (
        Index('byway_delivery_quest_data_0_quest_id', 'quest_id'),
    )

    condition_category: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BywayQuestDatum(Base):
    __tablename__ = 'byway_quest_data'
    __table_args__ = (
        Index('byway_quest_data_0_area_id', 'area_id'),
    )

    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    byway_quest_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class BywayStoryDetail(Base):
    __tablename__ = 'byway_story_detail'
    __table_args__ = (
        Index('byway_story_detail_0_pre_story_id', 'pre_story_id'),
        Index('byway_story_detail_0_unlock_quest_id', 'unlock_quest_id')
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    color_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignBeginnerDatum(Base):
    __tablename__ = 'campaign_beginner_data'

    id_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    beginner_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CampaignFreegacha(Base):
    __tablename__ = 'campaign_freegacha'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_10_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    freegacha_1: Mapped[int] = mapped_column(Integer, nullable=False)
    freegacha_10: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class CampaignFreegachaDatum(Base):
    __tablename__ = 'campaign_freegacha_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignFreegachaSp(Base):
    __tablename__ = 'campaign_freegacha_sp'

    max_exec_count: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class CampaignLevelDatum(Base):
    __tablename__ = 'campaign_level_data'

    label_color: Mapped[str] = mapped_column(Text, nullable=False)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_color: Mapped[str] = mapped_column(Text, nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignMissionCategory(Base):
    __tablename__ = 'campaign_mission_category'
    __table_args__ = (
        Index('campaign_mission_category_0_campaign_id_1_type', 'campaign_id', 'type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignMissionDatum(Base):
    __tablename__ = 'campaign_mission_data'
    __table_args__ = (
        Index('campaign_mission_data_0_campaign_id', 'campaign_id'),
        Index('campaign_mission_data_0_campaign_id_1_type', 'campaign_id', 'type')
    )

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mark_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    title_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)


class CampaignMissionRewardDatum(Base):
    __tablename__ = 'campaign_mission_reward_data'
    __table_args__ = (
        Index('campaign_mission_reward_data_0_campaign_mission_reward_id', 'campaign_mission_reward_id'),
    )

    campaign_mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class CampaignMissionSchedule(Base):
    __tablename__ = 'campaign_mission_schedule'

    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class CampaignSchedule(Base):
    __tablename__ = 'campaign_schedule'
    __table_args__ = (
        Index('campaign_schedule_0_campaign_category', 'campaign_category'),
    )

    shiori_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_type: Mapped[int] = mapped_column(Integer, nullable=False)
    duplication_order: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_category: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    icon_image: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beginner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[float] = mapped_column(REAL, nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignShioriGroup(Base):
    __tablename__ = 'campaign_shiori_group'
    __table_args__ = (
        Index('campaign_shiori_group_0_shiori_group_id', 'shiori_group_id'),
    )

    shiori_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanBuddy(Base):
    __tablename__ = 'caravan_buddy'

    effect_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_description1: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    effect_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_description2: Mapped[str] = mapped_column(Text, nullable=False)
    buddy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanBuffDisp(Base):
    __tablename__ = 'caravan_buff_disp'
    __table_args__ = (
        Index('caravan_buff_disp_0_type_1_effect_id', 'type', 'effect_id'),
    )

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count_from: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_to: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanChangeBlockType(Base):
    __tablename__ = 'caravan_change_block_type'

    reference_id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_to: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_from: Mapped[int] = mapped_column(Integer, nullable=False)
    change_block_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanCoinShopLineup(Base):
    __tablename__ = 'caravan_coin_shop_lineup'
    __table_args__ = (
        Index('caravan_coin_shop_lineup_0_season_id', 'season_id'),
    )

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDicePattern(Base):
    __tablename__ = 'caravan_dice_pattern'

    pattern: Mapped[int] = mapped_column(Integer, nullable=False)
    dice_odds: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanDiceRewardPeriod(Base):
    __tablename__ = 'caravan_dice_reward_period'

    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanDish(Base):
    __tablename__ = 'caravan_dish'

    disable_category: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_times: Mapped[int] = mapped_column(Integer, nullable=False)
    sold_price: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    sub_effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_effect_description: Mapped[str] = mapped_column(Text, nullable=False)
    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    new_line_name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_description: Mapped[str] = mapped_column(Text, nullable=False)
    recipe_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDishDrawable(Base):
    __tablename__ = 'caravan_dish_drawable'

    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanDishReward(Base):
    __tablename__ = 'caravan_dish_reward'

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDishTurnEffect(Base):
    __tablename__ = 'caravan_dish_turn_effect'

    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    turn_to: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDrama(Base):
    __tablename__ = 'caravan_drama'
    __table_args__ = (
        Index('caravan_drama_0_drama_id', 'drama_id'),
    )

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanEffectSetting(Base):
    __tablename__ = 'caravan_effect_setting'
    __table_args__ = (
        Index('caravan_effect_setting_0_scene_type', 'scene_type'),
        Index('caravan_effect_setting_0_scene_type_1_effect_type', 'scene_type', 'effect_type')
    )

    scene_type: Mapped[int] = mapped_column(Integer, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanEventEffect(Base):
    __tablename__ = 'caravan_event_effect'

    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_times: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanExcludeCountBlock(Base):
    __tablename__ = 'caravan_exclude_count_block'

    exclude_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanGachaBlockLineup(Base):
    __tablename__ = 'caravan_gacha_block_lineup'

    premium_gacha_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    rare_gacha_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    rare_gacha_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_gacha_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normal_gacha_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    premium_gacha_odds: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanGoalBonus(Base):
    __tablename__ = 'caravan_goal_bonus'
    __table_args__ = (
        Index('caravan_goal_bonus_0_season_id', 'season_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    early_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    early_from: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_label: Mapped[int] = mapped_column(Integer, nullable=False)
    early_level: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanMap(Base):
    __tablename__ = 'caravan_map'
    __table_args__ = (
        Index('caravan_map_0_season_id', 'season_id'),
    )

    next_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_to_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_3: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pre_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_2: Mapped[int] = mapped_column(Integer, nullable=False)
    next_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_1: Mapped[int] = mapped_column(Integer, nullable=False)
    next_2: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    next_4: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanMapLayout(Base):
    __tablename__ = 'caravan_map_layout'

    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanMapObject(Base):
    __tablename__ = 'caravan_map_object'
    __table_args__ = (
        Index('caravan_map_object_0_season_id', 'season_id'),
    )

    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_type: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[float] = mapped_column(REAL, nullable=False)


class CaravanMileBlockReward(Base):
    __tablename__ = 'caravan_mile_block_reward'

    upgrade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanNaviComment(Base):
    __tablename__ = 'caravan_navi_comment'
    __table_args__ = (
        Index('caravan_navi_comment_0_season_id', 'season_id'),
    )

    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class CaravanRival(Base):
    __tablename__ = 'caravan_rival'

    dice_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rival_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanRivalBonus(Base):
    __tablename__ = 'caravan_rival_bonus'
    __table_args__ = (
        Index('caravan_rival_bonus_0_season_id', 'season_id'),
    )

    bonus_label: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_text: Mapped[str] = mapped_column(Text, nullable=False)
    distance_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanRivalMinigameList(Base):
    __tablename__ = 'caravan_rival_minigame_list'

    rival_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rival_minigame_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanSchedule(Base):
    __tablename__ = 'caravan_schedule'
    __table_args__ = (
        Index('caravan_schedule_0_coin_id', 'coin_id'),
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    skip_dice_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_close_time: Mapped[str] = mapped_column(Text, nullable=False)
    limit_caravan_dish_by_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    coin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    minigame_retire_reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    target_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_limit_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    start_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_target_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanShopBlockRank(Base):
    __tablename__ = 'caravan_shop_block_rank'

    upgrade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanShortcut(Base):
    __tablename__ = 'caravan_shortcut'

    remove_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    shortcut_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    remove_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    end_point_block_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanSkipReward(Base):
    __tablename__ = 'caravan_skip_reward'
    __table_args__ = (
        Index('caravan_skip_reward_0_season_id', 'season_id'),
    )

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_label: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fastest_goal_turn_to: Mapped[int] = mapped_column(Integer, nullable=False)
    fastest_goal_turn_from: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanSoundSetting(Base):
    __tablename__ = 'caravan_sound_setting'
    __table_args__ = (
        Index('caravan_sound_setting_0_scene_type', 'scene_type'),
        Index('caravan_sound_setting_0_scene_type_1_effect_type', 'scene_type', 'effect_type')
    )

    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    scene_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sound_type: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanTreasure(Base):
    __tablename__ = 'caravan_treasure'
    __table_args__ = (
        Index('caravan_treasure_0_rarity_1_appraise_flag', 'rarity', 'appraise_flag'),
    )

    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    appraise_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    reset_value: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    new_line_name: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanTreasureBlockRank(Base):
    __tablename__ = 'caravan_treasure_block_rank'

    upgrade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanTreasureBlockReal(Base):
    __tablename__ = 'caravan_treasure_block_real'
    __table_args__ = (
        Index('caravan_treasure_block_real_0_odds_id', 'odds_id'),
    )

    odds_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CccBsScenarioList(Base):
    __tablename__ = 'ccc_bs_scenario_list'

    ccc_scenario_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CccChara(Base):
    __tablename__ = 'ccc_chara'

    start_time: Mapped[float] = mapped_column(REAL, nullable=False)
    ccc_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[float] = mapped_column(REAL, nullable=False)


class CccCharaDatum(Base):
    __tablename__ = 'ccc_chara_data'

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    ccc_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class CccDropGroupDatum(Base):
    __tablename__ = 'ccc_drop_group_data'

    drop_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drop_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    object_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    object_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    object_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CccObject(Base):
    __tablename__ = 'ccc_object'

    is_report: Mapped[int] = mapped_column(Integer, nullable=False)
    ccc_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    fall_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ccc_object_type: Mapped[int] = mapped_column(Integer, nullable=False)
    absorb_frame: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class CccScenario(Base):
    __tablename__ = 'ccc_scenario'
    __table_args__ = (
        Index('ccc_scenario_0_ccc_scenario_id', 'ccc_scenario_id'),
    )

    idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    ccc_object_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ccc_scenario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    frame: Mapped[int] = mapped_column(Integer, nullable=False)


class CggCompletionDatum(Base):
    __tablename__ = 'cgg_completion_data'

    completion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    secret_goods_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_num: Mapped[int] = mapped_column(Integer, nullable=False)
    receive_description: Mapped[str] = mapped_column(Text, nullable=False)
    completion_emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    secret_goods_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    secret_goods_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CggCompletionRewardDatum(Base):
    __tablename__ = 'cgg_completion_reward_data'
    __table_args__ = (
        Index('cgg_completion_reward_data_0_completion_id', 'completion_id'),
    )

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CggDrama(Base):
    __tablename__ = 'cgg_drama'
    __table_args__ = (
        Index('cgg_drama_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class CggGachaInfo(Base):
    __tablename__ = 'cgg_gacha_info'
    __table_args__ = (
        Index('cgg_gacha_info_0_cgg_id', 'cgg_id'),
    )

    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    cost_currency_num: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_description: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_intro: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    cgg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CggGachaLineup(Base):
    __tablename__ = 'cgg_gacha_lineup'
    __table_args__ = (
        Index('cgg_gacha_lineup_0_gacha_type', 'gacha_type'),
    )

    goods_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lineup_id: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CggGameSettings(Base):
    __tablename__ = 'cgg_game_settings'

    max_goods_count: Mapped[int] = mapped_column(Integer, nullable=False)
    max_gacha_exchange_count: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_shelf_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cgg_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_luppi_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    cgg_gacha_currency_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CggGoodsDatum(Base):
    __tablename__ = 'cgg_goods_data'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    shelf_position_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    goods_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)


class CharaETicketDatum(Base):
    __tablename__ = 'chara_e_ticket_data'
    __table_args__ = (
        Index('chara_e_ticket_data_0_jewel_store_id', 'jewel_store_id', unique=True),
    )

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    jewel_store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class CharaFortuneRail(Base):
    __tablename__ = 'chara_fortune_rail'

    gimmick_6_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_3_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_9_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_7_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_1_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_5_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_7_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_8_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_6_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_4_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_1_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_10_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_2_id: Mapped[str] = mapped_column(Text, nullable=False)
    rail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gimmick_3_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_10_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_8_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_9_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_4_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_5_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_2_x: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaFortuneReward(Base):
    __tablename__ = 'chara_fortune_reward'

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fortune_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    count_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaFortuneScenario(Base):
    __tablename__ = 'chara_fortune_scenario'

    rail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    scenario_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CharaFortuneSchedule(Base):
    __tablename__ = 'chara_fortune_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    fortune_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CharaIdentity(Base):
    __tablename__ = 'chara_identity'

    chara_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaStoryStatus(Base):
    __tablename__ = 'chara_story_status'

    chara_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_1: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_name: Mapped[str] = mapped_column(Text, nullable=False)
    status_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_3: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_5: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_7: Mapped[int] = mapped_column(Integer, nullable=False)


class CharacterLoveRankupText(Base):
    __tablename__ = 'character_love_rankup_text'

    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    face_3: Mapped[int] = mapped_column(Integer, nullable=False)
    scale: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_1: Mapped[int] = mapped_column(Integer, nullable=False)
    serif_3: Mapped[str] = mapped_column(Text, nullable=False)
    serif_2: Mapped[str] = mapped_column(Text, nullable=False)
    face_2: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    serif_1: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class CidpBanner(Base):
    __tablename__ = 'cidp_banner'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)


class ClanBattle2BossDatum(Base):
    __tablename__ = 'clan_battle_2_boss_data'

    cursor_position: Mapped[int] = mapped_column(Integer, nullable=False)
    scale_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    map_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_width_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_thumb_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_height_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    map_position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattle2MapDatum(Base):
    __tablename__ = 'clan_battle_2_map_data'
    __table_args__ = (
        Index('clan_battle_2_map_data_0_clan_battle_id', 'clan_battle_id'),
    )

    fix_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_5: Mapped[float] = mapped_column(REAL, nullable=False)
    score_coefficient_2: Mapped[float] = mapped_column(REAL, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_to: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_1: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_4: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    map_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_3: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_from: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleArchiveClanRank(Base):
    __tablename__ = 'clan_battle_archive_clan_rank'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleArchivePersonRank(Base):
    __tablename__ = 'clan_battle_archive_person_rank'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleBattleMissionDatum(Base):
    __tablename__ = 'clan_battle_battle_mission_data'

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)


class ClanBattleBossDamageRank(Base):
    __tablename__ = 'clan_battle_boss_damage_rank'
    __table_args__ = (
        Index('clan_battle_boss_damage_rank_0_damage_rank_id', 'damage_rank_id'),
    )

    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleBossFixReward(Base):
    __tablename__ = 'clan_battle_boss_fix_reward'

    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleLastAttackReward(Base):
    __tablename__ = 'clan_battle_last_attack_reward'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleOddsDatum(Base):
    __tablename__ = 'clan_battle_odds_data'
    __table_args__ = (
        Index('clan_battle_odds_data_0_odds_group_id', 'odds_group_id'),
    )

    odds_csv_3: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_8: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_2: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_5: Mapped[str] = mapped_column(Text, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_csv_4: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_9: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_7: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_10: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_6: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_1: Mapped[str] = mapped_column(Text, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)


class ClanBattleParamAdjust(Base):
    __tablename__ = 'clan_battle_param_adjust'

    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    score_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_atk_cast_time: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattlePeriod(Base):
    __tablename__ = 'clan_battle_period'
    __table_args__ = (
        Index('clan_battle_period_0_clan_battle_id', 'clan_battle_id'),
    )

    quest_detail_rehearsal_label_height: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail: Mapped[str] = mapped_column(Text, nullable=False)
    period_detail_s: Mapped[str] = mapped_column(Text, nullable=False)
    period_detail_bg_s: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_boss_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_end: Mapped[str] = mapped_column(Text, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_start: Mapped[str] = mapped_column(Text, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    calc_start: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    period_detail_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    result_end: Mapped[str] = mapped_column(Text, nullable=False)
    min_carry_over_time: Mapped[int] = mapped_column(Integer, nullable=False)
    result_start: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[int] = mapped_column(Integer, primary_key=True)


class ClanBattlePeriodLapReward(Base):
    __tablename__ = 'clan_battle_period_lap_reward'

    lap_num_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_bonus_group: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattlePeriodRankReward(Base):
    __tablename__ = 'clan_battle_period_rank_reward'

    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_bonus_group: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleRecommendDatum(Base):
    __tablename__ = 'clan_battle_recommend_data'
    __table_args__ = (
        Index('clan_battle_recommend_data_0_recommend_group', 'recommend_group'),
    )

    level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level_from: Mapped[int] = mapped_column(Integer, nullable=False)
    atack_party_count: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_group: Mapped[int] = mapped_column(Integer, nullable=False)
    level_to: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_party_count: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSBossDatum(Base):
    __tablename__ = 'clan_battle_s_boss_data'

    boss_thumb_id: Mapped[int] = mapped_column(Integer, nullable=False)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    scale_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_width_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    cursor_position: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_height_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSBossFixReward(Base):
    __tablename__ = 'clan_battle_s_boss_fix_reward'

    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSMapDatum(Base):
    __tablename__ = 'clan_battle_s_map_data'
    __table_args__ = (
        Index('clan_battle_s_map_data_0_clan_battle_id', 'clan_battle_id'),
    )

    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_4: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    map_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag4: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_from: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    fix_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_2: Mapped[float] = mapped_column(REAL, nullable=False)
    lap_num_to: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag5: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag2: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag1: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_3: Mapped[float] = mapped_column(REAL, nullable=False)
    score_coefficient_5: Mapped[float] = mapped_column(REAL, nullable=False)
    param_adjust_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_1: Mapped[float] = mapped_column(REAL, nullable=False)


class ClanBattleSParamAdjust(Base):
    __tablename__ = 'clan_battle_s_param_adjust'

    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_atk_cast_time: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSchedule(Base):
    __tablename__ = 'clan_battle_schedule'

    clan_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    point_per_stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_group_id_s: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    release_month: Mapped[int] = mapped_column(Integer, nullable=False)
    map_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    last_clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class ClanBattleTrainingDatum(Base):
    __tablename__ = 'clan_battle_training_data'
    __table_args__ = (
        Index('clan_battle_training_data_0_training_id', 'training_id'),
    )

    training_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    map_data_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleTrainingSchedule(Base):
    __tablename__ = 'clan_battle_training_schedule'
    __table_args__ = (
        Index('clan_battle_training_schedule_0_clan_battle_id', 'clan_battle_id'),
    )

    battle_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    interval_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    training_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interval_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class ClanCostGroup(Base):
    __tablename__ = 'clan_cost_group'

    cost_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanGrade(Base):
    __tablename__ = 'clan_grade'

    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_grade_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ClanInviteLevelGroup(Base):
    __tablename__ = 'clan_invite_level_group'

    team_level_from: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, nullable=False)
    level_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ClanprofileContent(Base):
    __tablename__ = 'clanprofile_content'

    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ColosseumEnhanceDatum(Base):
    __tablename__ = 'colosseum_enhance_data'
    __table_args__ = (
        Index('colosseum_enhance_data_0_enhance_id', 'enhance_id'),
    )

    equipment_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumMissionDatum(Base):
    __tablename__ = 'colosseum_mission_data'
    __table_args__ = (
        Index('colosseum_mission_data_0_schedule_id_1_difficulty', 'schedule_id', 'difficulty'),
    )

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ColosseumMissionRewardDatum(Base):
    __tablename__ = 'colosseum_mission_reward_data'
    __table_args__ = (
        Index('colosseum_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumQuestDatum(Base):
    __tablename__ = 'colosseum_quest_data'

    enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    display_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    princess_knight_enhance_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumScheduleDatum(Base):
    __tablename__ = 'colosseum_schedule_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class ColosseumScore(Base):
    __tablename__ = 'colosseum_score'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    threshold_pt_1: Mapped[int] = mapped_column(Integer, nullable=False)
    win_pt: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_pos_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_param_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_param_1: Mapped[int] = mapped_column(Integer, nullable=False)
    time_pt_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_pos_2: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_pt_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CombinedResultMotion(Base):
    __tablename__ = 'combined_result_motion'

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class ContentMapDatum(Base):
    __tablename__ = 'content_map_data'

    quest_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    content_map_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    quest_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ContentReleaseDatum(Base):
    __tablename__ = 'content_release_data'

    dialog: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level: Mapped[int] = mapped_column(Integer, nullable=False)


class ContentsReleaseCondition(Base):
    __tablename__ = 'contents_release_condition'

    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CooperationQuestDatum(Base):
    __tablename__ = 'cooperation_quest_data'

    cooperation_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_enemy_image_wave_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_2_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    sub_enemy_image_wave_2_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_enemy_image_wave_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    repeat_reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_2_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    repeat_reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_2_4: Mapped[int] = mapped_column(Integer, nullable=False)
    repeat_reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_enemy_image_wave_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_comment: Mapped[str] = mapped_column(Text, nullable=False)
    first_reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    cooperation_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_4: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lobby_background: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    exp: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    first_reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CrownSchedule(Base):
    __tablename__ = 'crown_schedule'
    __table_args__ = (
        Index('crown_schedule_0_event_id', 'event_id'),
    )

    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class CrownUniqueMissionDatum(Base):
    __tablename__ = 'crown_unique_mission_data'
    __table_args__ = (
        Index('crown_unique_mission_data_0_event_id', 'event_id'),
        Index('crown_unique_mission_data_0_event_id_1_mission_type', 'event_id', 'mission_type')
    )

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    restrict_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[Optional[int]] = mapped_column(Integer)
    destination_system_id: Mapped[Optional[int]] = mapped_column(Integer)


class CustomMypage(Base):
    __tablename__ = 'custom_mypage'
    __table_args__ = (
        Index('custom_mypage_0_still_group_id', 'still_group_id'),
    )

    scroll_direction: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    still_name: Mapped[str] = mapped_column(Text, nullable=False)
    still_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mypage_type: Mapped[int] = mapped_column(Integer, nullable=False)
    vertical_still_flg: Mapped[int] = mapped_column(Integer, nullable=False)


class CustomMypageGroup(Base):
    __tablename__ = 'custom_mypage_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(Text, nullable=False)


class DailyMissionDatum(Base):
    __tablename__ = 'daily_mission_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    title_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class DearChara(Base):
    __tablename__ = 'dear_chara'
    __table_args__ = (
        Index('dear_chara_0_event_id', 'event_id'),
    )

    max_dear_point: Mapped[int] = mapped_column(Integer, nullable=False)
    episode_unlock_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_type: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point_up_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point_up_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    episode_unlock_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_name: Mapped[str] = mapped_column(Text, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DearReward(Base):
    __tablename__ = 'dear_reward'
    __table_args__ = (
        Index('dear_reward_0_event_id_1_chara_index', 'event_id', 'chara_index'),
    )

    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class DearSetting(Base):
    __tablename__ = 'dear_setting'

    tutorial_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tutorial_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_name: Mapped[str] = mapped_column(Text, nullable=False)
    tutorial_chara_index: Mapped[int] = mapped_column(Integer, nullable=False)


class DearStoryDatum(Base):
    __tablename__ = 'dear_story_data'
    __table_args__ = (
        Index('dear_story_data_0_value', 'value'),
    )

    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class DearStoryDetail(Base):
    __tablename__ = 'dear_story_detail'
    __table_args__ = (
        Index('dear_story_detail_0_story_group_id', 'story_group_id'),
        Index('dear_story_detail_0_story_group_id_1_chara_index', 'story_group_id', 'chara_index')
    )

    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_event_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_event_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)


class DefeatTips(Base):
    __tablename__ = 'defeat_tips'
    __table_args__ = (
        Index('defeat_tips_0_tips_group_id', 'tips_group_id'),
    )

    required_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tips_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    move_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tips_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class DefeatTipsCondition(Base):
    __tablename__ = 'defeat_tips_condition'

    tips_group_ids: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    necessary_next_id: Mapped[int] = mapped_column(Integer, nullable=False)
    next_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DefineSpskill(Base):
    __tablename__ = 'define_spskill'
    __table_args__ = (
        Index('define_spskill_0_sp_skill_id', 'sp_skill_id'),
    )

    sp_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_category: Mapped[int] = mapped_column(Integer, nullable=False)
    link_skill_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DodgeTpRecovery(Base):
    __tablename__ = 'dodge_tp_recovery'

    recovery_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class DomeBattleEffect(Base):
    __tablename__ = 'dome_battle_effect'

    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)


class DomeMissionDatum(Base):
    __tablename__ = 'dome_mission_data'
    __table_args__ = (
        Index('dome_mission_data_0_schedule_id', 'schedule_id'),
    )

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    disp_icon_on_bar: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeMissionRewardDatum(Base):
    __tablename__ = 'dome_mission_reward_data'
    __table_args__ = (
        Index('dome_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeQuestChallengeDatum(Base):
    __tablename__ = 'dome_quest_challenge_data'

    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    challenge_condition: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeQuestDatum(Base):
    __tablename__ = 'dome_quest_data'
    __table_args__ = (
        Index('dome_quest_data_0_schedule_id', 'schedule_id'),
    )

    unit_enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    display_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    round_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeQuestReward(Base):
    __tablename__ = 'dome_quest_reward'

    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeScheduleDatum(Base):
    __tablename__ = 'dome_schedule_data'

    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)


class DomeUnitEnhanceDatum(Base):
    __tablename__ = 'dome_unit_enhance_data'

    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_1: Mapped[int] = mapped_column(Integer, nullable=False)


class DsbDramaScript(Base):
    __tablename__ = 'dsb_drama_script'
    __table_args__ = (
        Index('dsb_drama_script_0_drama_id', 'drama_id'),
    )

    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class DsbStoryDatum(Base):
    __tablename__ = 'dsb_story_data'
    __table_args__ = (
        Index('dsb_story_data_0_original_event_id', 'original_event_id'),
    )

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    article_text: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    day_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    material_text: Mapped[str] = mapped_column(Text, nullable=False)
    effect_text: Mapped[str] = mapped_column(Text, nullable=False)


class DungeonArea(Base):
    __tablename__ = 'dungeon_area'

    initial_clear_story: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    open_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    open_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    content_release_story: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_level: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonAreaDatum(Base):
    __tablename__ = 'dungeon_area_data'

    recommend_level: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_release_story: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_clear_story: Mapped[int] = mapped_column(Integer, nullable=False)
    open_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class DungeonPatternBattle(Base):
    __tablename__ = 'dungeon_pattern_battle'
    __table_args__ = (
        Index('dungeon_pattern_battle_0_quest_id', 'quest_id'),
        Index('dungeon_pattern_battle_0_quest_id_1_pattern', 'quest_id', 'pattern', unique=True)
    )

    pattern: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_monster_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    next_pattern_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_monster_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    trigger_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_monster_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    floor_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    trigger_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    next_pattern_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_monster_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    floor_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonQuestDatum(Base):
    __tablename__ = 'dungeon_quest_data'
    __table_args__ = (
        Index('dungeon_quest_data_0_dungeon_area_id', 'dungeon_area_id'),
        Index('dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num', unique=True)
    )

    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_6: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    emax: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reset_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_2: Mapped[float] = mapped_column(REAL, nullable=False)
    multi_target_effect_time: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_monster_height: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonSkipDatum(Base):
    __tablename__ = 'dungeon_skip_data'

    skip_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_motion_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonSpecialBattle(Base):
    __tablename__ = 'dungeon_special_battle'
    __table_args__ = (
        Index('dungeon_special_battle_0_quest_id', 'quest_id'),
        Index('dungeon_special_battle_0_quest_id_1_mode', 'quest_id', 'mode', unique=True)
    )

    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    special_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonSpecialEnemySetting(Base):
    __tablename__ = 'dungeon_special_enemy_setting'
    __table_args__ = (
        UniqueConstraint('special_battle_id', 'disp_order'),
        Index('dungeon_special_enemy_setting_0_special_battle_id', 'special_battle_id'),
        Index('dungeon_special_enemy_setting_0_special_battle_id_1_enemy_identify', 'special_battle_id', 'enemy_identify', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_identify: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    special_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_offset_y: Mapped[float] = mapped_column(REAL, nullable=False)
    must_kill_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class DvsStoryDatum(Base):
    __tablename__ = 'dvs_story_data'
    __table_args__ = (
        Index('dvs_story_data_0_dvs_story_type', 'dvs_story_type'),
        Index('dvs_story_data_0_original_event_id', 'original_event_id')
    )

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dvs_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class EReduction(Base):
    __tablename__ = 'e_reduction'

    value_1: Mapped[float] = mapped_column(REAL, nullable=False)
    value_4: Mapped[float] = mapped_column(REAL, nullable=False)
    value_5: Mapped[float] = mapped_column(REAL, nullable=False)
    threshold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    border: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[float] = mapped_column(REAL, nullable=False)
    value_2: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EmblemConditionDescription(Base):
    __tablename__ = 'emblem_condition_description'

    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_description: Mapped[str] = mapped_column(Text, nullable=False)


class EmblemDatum(Base):
    __tablename__ = 'emblem_data'

    disp_oder: Mapped[int] = mapped_column(Integer, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    emblem_name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_emblem: Mapped[int] = mapped_column(Integer, nullable=False)


class EmblemMissionDatum(Base):
    __tablename__ = 'emblem_mission_data'

    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EmblemMissionRewardDatum(Base):
    __tablename__ = 'emblem_mission_reward_data'
    __table_args__ = (
        Index('emblem_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
        Index('emblem_mission_reward_data_0_reward_id', 'reward_id')
    )

    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyCommentOverride(Base):
    __tablename__ = 'enemy_comment_override'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)


class EnemyEnableVoice(Base):
    __tablename__ = 'enemy_enable_voice'

    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyIgnoreSkillRf(Base):
    __tablename__ = 'enemy_ignore_skill_rf'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyMParts(Base):
    __tablename__ = 'enemy_m_parts'

    child_enemy_parameter_3: Mapped[int] = mapped_column(Integer, nullable=False)
    child_enemy_parameter_1: Mapped[int] = mapped_column(Integer, nullable=False)
    child_enemy_parameter_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_enemy_parameter_5: Mapped[int] = mapped_column(Integer, nullable=False)
    child_enemy_parameter_4: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyParameter(Base):
    __tablename__ = 'enemy_parameter'

    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyRewardDatum(Base):
    __tablename__ = 'enemy_reward_data'

    drop_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_1: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyTagDatum(Base):
    __tablename__ = 'enemy_tag_data'
    __table_args__ = (
        Index('enemy_tag_data_0_enemy_id', 'enemy_id'),
        Index('enemy_tag_data_0_unit_id', 'unit_id')
    )

    tag_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    tag_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyTagSetting(Base):
    __tablename__ = 'enemy_tag_setting'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyTalentWeakness(Base):
    __tablename__ = 'enemy_talent_weakness'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resist_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EnvironmentSkillDetail(Base):
    __tablename__ = 'environment_skill_detail'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class EquipConvertAlcesPoint(Base):
    __tablename__ = 'equip_convert_alces_point'

    equipment_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    alces_point: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class EquipmentCraft(Base):
    __tablename__ = 'equipment_craft'

    condition_equipment_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    crafted_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_equipment_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_9: Mapped[int] = mapped_column(Integer, nullable=False)


class EquipmentDatum(Base):
    __tablename__ = 'equipment_data'
    __table_args__ = (
        Index('equipment_data_0_original_equipment_id', 'original_equipment_id'),
    )

    equipment_type: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_name: Mapped[str] = mapped_column(Text, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    original_equipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    sale_price: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_category: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    craft_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    require_level: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_enhance_point: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    enable_donation: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    display_item: Mapped[int] = mapped_column(Integer, nullable=False)


class EquipmentDonation(Base):
    __tablename__ = 'equipment_donation'

    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    donation_num_daily: Mapped[int] = mapped_column(Integer, nullable=False)
    request_num_once: Mapped[int] = mapped_column(Integer, nullable=False)
    donation_num_once: Mapped[int] = mapped_column(Integer, nullable=False)


class EquipmentEnhanceDatum(Base):
    __tablename__ = 'equipment_enhance_data'

    equipment_enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_point: Mapped[int] = mapped_column(Integer, nullable=False)
    total_point: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class EquipmentEnhanceRate(Base):
    __tablename__ = 'equipment_enhance_rate'

    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)


class EventBgDatum(Base):
    __tablename__ = 'event_bg_data'

    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventBossTreasureBox(Base):
    __tablename__ = 'event_boss_treasure_box'

    each_odds_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_8: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_9: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_box_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    each_odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_6: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_7: Mapped[int] = mapped_column(Integer, nullable=False)


class EventBossTreasureContent(Base):
    __tablename__ = 'event_boss_treasure_content'

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_3: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_2: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_4: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_5: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_1: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class EventEffectSetting(Base):
    __tablename__ = 'event_effect_setting'

    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class EventEnemyParameter(Base):
    __tablename__ = 'event_enemy_parameter'

    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventEnemyRewardGroup(Base):
    __tablename__ = 'event_enemy_reward_group'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EventGachaDatum(Base):
    __tablename__ = 'event_gacha_data'
    __table_args__ = (
        Index('event_gacha_data_0_event_id', 'event_id'),
    )

    repeat_step: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventIntroduction(Base):
    __tablename__ = 'event_introduction'
    __table_args__ = (
        Index('event_introduction_0_event_id', 'event_id'),
    )

    maximum_chunk_size_loop_2: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_loop_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_2: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    introduction_number: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_1: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    maximum_chunk_size_loop_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class EventNaviComment(Base):
    __tablename__ = 'event_navi_comment'

    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class EventNaviCommentCondition(Base):
    __tablename__ = 'event_navi_comment_condition'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class EventReminder(Base):
    __tablename__ = 'event_reminder'
    __table_args__ = (
        Index('event_reminder_0_event_id', 'event_id'),
    )

    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title_text: Mapped[str] = mapped_column(Text, nullable=False)
    reminder_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    notice_text: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description_text: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    btn_text: Mapped[str] = mapped_column(Text, nullable=False)


class EventReminderCondition(Base):
    __tablename__ = 'event_reminder_condition'
    __table_args__ = (
        Index('event_reminder_condition_0_reminder_id', 'reminder_id'),
    )

    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reminder_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventRevivalSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_revival_series_wave_group_data'

    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class EventRevivalWaveGroupDatum(Base):
    __tablename__ = 'event_revival_wave_group_data'

    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class EventSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_series_wave_group_data'

    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class EventStoryDatum(Base):
    __tablename__ = 'event_story_data'
    __table_args__ = (
        Index('event_story_data_0_value', 'value'),
    )

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)


class EventStoryDetail(Base):
    __tablename__ = 'event_story_detail'
    __table_args__ = (
        Index('event_story_detail_0_story_group_id', 'story_group_id'),
    )

    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventTopAdv(Base):
    __tablename__ = 'event_top_adv'
    __table_args__ = (
        Index('event_top_adv_0_event_id_1_type', 'event_id', 'type'),
    )

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_top_adv_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventWaveGroupDatum(Base):
    __tablename__ = 'event_wave_group_data'

    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    match_lv_min: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    match_lv_max: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipConvertAlcesCoin(Base):
    __tablename__ = 'ex_equip_convert_alces_coin'

    ex_equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alces_coin: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipConvertAlcesPoint(Base):
    __tablename__ = 'ex_equip_convert_alces_point'

    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    alces_point: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentCategory(Base):
    __tablename__ = 'ex_equipment_category'

    recycle_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_base: Mapped[str] = mapped_column(Text, nullable=False)
    outline: Mapped[str] = mapped_column(Text, nullable=False)


class ExEquipmentDatum(Base):
    __tablename__ = 'ex_equipment_data'

    max_physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    max_rank_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    max_wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    default_def: Mapped[int] = mapped_column(Integer, nullable=False)
    max_physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_equip_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    default_dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_skill_power: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    default_atk: Mapped[int] = mapped_column(Integer, nullable=False)
    restriction_id: Mapped[int] = mapped_column(Integer, nullable=False)
    default_energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    default_magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_skill_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    default_life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    default_physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    max_def: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    is_force_protected: Mapped[int] = mapped_column(Integer, nullable=False)
    max_life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    max_hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    default_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_skill_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    max_energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    default_physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    max_dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    max_atk: Mapped[int] = mapped_column(Integer, nullable=False)
    default_accuracy: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentEnhanceDatum(Base):
    __tablename__ = 'ex_equipment_enhance_data'
    __table_args__ = (
        Index('ex_equipment_enhance_data_0_rarity', 'rarity'),
    )

    total_point: Mapped[int] = mapped_column(Integer, nullable=False)
    needed_point: Mapped[int] = mapped_column(Integer, nullable=False)
    rankup_level: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExEquipmentRankupDatum(Base):
    __tablename__ = 'ex_equipment_rankup_data'

    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    rankup_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentRecycleReward(Base):
    __tablename__ = 'ex_equipment_recycle_reward'

    coin_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_pt_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentRestrictionUnit(Base):
    __tablename__ = 'ex_equipment_restriction_unit'
    __table_args__ = (
        Index('ex_equipment_restriction_unit_0_restriction_id', 'restriction_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restriction_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExEquipmentSubStatus(Base):
    __tablename__ = 'ex_equipment_sub_status'
    __table_args__ = (
        Index('ex_equipment_sub_status_0_group_id', 'group_id'),
    )

    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentSubStatusGroup(Base):
    __tablename__ = 'ex_equipment_sub_status_group'

    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExPlus(Base):
    __tablename__ = 'ex_plus'
    __table_args__ = (
        Index('ex_plus_0_event_id', 'event_id'),
        Index('ex_plus_0_wave_group_id', 'wave_group_id')
    )

    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    is_hide_boss: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)


class ExceedLevelStage(Base):
    __tablename__ = 'exceed_level_stage'

    general_exceed_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    increase_level_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ExceedLevelUnit(Base):
    __tablename__ = 'exceed_level_unit'
    __table_args__ = (
        Index('exceed_level_unit_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    exceed_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ExceptEr(Base):
    __tablename__ = 'except_er'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExchangeTicketDatum(Base):
    __tablename__ = 'exchange_ticket_data'

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ExperienceKnightRank(Base):
    __tablename__ = 'experience_knight_rank'

    knight_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_exp: Mapped[int] = mapped_column(Integer, nullable=False)


class ExperienceTalentLevel(Base):
    __tablename__ = 'experience_talent_level'

    total_point: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_enhance_value: Mapped[int] = mapped_column(Integer, nullable=False)


class ExperienceTeam(Base):
    __tablename__ = 'experience_team'

    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    over_limit_stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    max_stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    recover_stamina_count: Mapped[int] = mapped_column(Integer, nullable=False)


class ExperienceUnit(Base):
    __tablename__ = 'experience_unit'

    total_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExtraEffectDatum(Base):
    __tablename__ = 'extra_effect_data'
    __table_args__ = (
        Index('extra_effect_data_0_content_type_1_target_value_1', 'content_type', 'target_value_1'),
    )

    content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_3: Mapped[int] = mapped_column(Integer, nullable=False)
    set_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    target_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_2: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ExtraEffectTargetRange(Base):
    __tablename__ = 'extra_effect_target_range'
    __table_args__ = (
        Index('extra_effect_target_range_0_set_id', 'set_id'),
    )

    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    set_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ExtraEffectUnitGroup(Base):
    __tablename__ = 'extra_effect_unit_group'
    __table_args__ = (
        Index('extra_effect_unit_group_0_group_id', 'group_id'),
    )

    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class FbsSchedule(Base):
    __tablename__ = 'fbs_schedule'
    __table_args__ = (
        Index('fbs_schedule_0_story_id', 'story_id'),
    )

    fbs_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class FixLineupGroupSet(Base):
    __tablename__ = 'fix_lineup_group_set'
    __table_args__ = (
        Index('fix_lineup_group_set_0_team_level_from_1_team_level_to', 'team_level_from', 'team_level_to'),
    )

    price_type_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    price_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_13: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_19: Mapped[int] = mapped_column(Integer, nullable=False)
    price_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_19: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_12: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_18: Mapped[int] = mapped_column(Integer, nullable=False)
    lineup_group_set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    price_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_11: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_12: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_13: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_13: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_20: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_15: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_18: Mapped[int] = mapped_column(Integer, nullable=False)
    price_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    price_17: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    price_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_17: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_17: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    price_9: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    price_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_8: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_11: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    price_15: Mapped[int] = mapped_column(Integer, nullable=False)
    price_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_11: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    currency_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_17: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_13: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_10: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_6: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    price_12: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_11: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_19: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    price_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_18: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    price_4: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_12: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    price_19: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    price_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)


class FixLineupGroupSetDatum(Base):
    __tablename__ = 'fix_lineup_group_set_data'

    reward_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    lineup_group_set_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class FkeHappeningList(Base):
    __tablename__ = 'fke_happening_list'

    happening_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    happening_name: Mapped[str] = mapped_column(Text, nullable=False)


class FkeReward(Base):
    __tablename__ = 'fke_reward'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    fke_point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class FpcDramaScript(Base):
    __tablename__ = 'fpc_drama_script'
    __table_args__ = (
        Index('fpc_drama_script_0_drama_id', 'drama_id'),
    )

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class FpcSetting(Base):
    __tablename__ = 'fpc_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class FpcStoryDatum(Base):
    __tablename__ = 'fpc_story_data'
    __table_args__ = (
        Index('fpc_story_data_0_original_event_id', 'original_event_id'),
    )

    period: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fpc_voice_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class GachaDatum(Base):
    __tablename__ = 'gacha_data'
    __table_args__ = (
        Index('gacha_data_0_exchange_id', 'exchange_id'),
    )

    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_detail: Mapped[int] = mapped_column(Integer, nullable=False)
    pick_up_chara_text: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    pickup_id: Mapped[int] = mapped_column(Integer, nullable=False)
    prizegacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pickup_badge: Mapped[int] = mapped_column(Integer, nullable=False)
    description_sp: Mapped[str] = mapped_column(Text, nullable=False)
    title_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_times_limit10: Mapped[int] = mapped_column(Integer, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    description_2: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    free_gacha_interval_time: Mapped[int] = mapped_column(Integer, nullable=False)
    free_gacha_count: Mapped[int] = mapped_column(Integer, nullable=False)
    tab_name: Mapped[str] = mapped_column(Text, nullable=False)
    ticket_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_cost_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=False)
    free_gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)


class GachaExchangeLineup(Base):
    __tablename__ = 'gacha_exchange_lineup'
    __table_args__ = (
        Index('gacha_exchange_lineup_0_exchange_id', 'exchange_id'),
    )

    pickup_gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    exchange_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class GachaPickup(Base):
    __tablename__ = 'gacha_pickup'
    __table_args__ = (
        Index('gacha_pickup_0_id', 'id'),
        Index('gacha_pickup_0_id_1_reward_id', 'id', 'reward_id')
    )

    priority: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class GiftMessage(Base):
    __tablename__ = 'gift_message'

    type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    discription: Mapped[str] = mapped_column(Text, nullable=False)


class GlobalDatum(Base):
    __tablename__ = 'global_data'

    value: Mapped[int] = mapped_column(Integer, nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=False)
    key_name: Mapped[str] = mapped_column(Text, primary_key=True)


class GlossaryDetail(Base):
    __tablename__ = 'glossary_detail'

    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    glossary_category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    glossary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    category_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class GoldsetDatum(Base):
    __tablename__ = 'goldset_data'

    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_jewel_count: Mapped[int] = mapped_column(Integer, nullable=False)
    get_gold_count: Mapped[int] = mapped_column(Integer, nullable=False)


class GoldsetDatum2(Base):
    __tablename__ = 'goldset_data_2'

    training_quest_count: Mapped[int] = mapped_column(Integer, nullable=False)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    get_gold_count: Mapped[int] = mapped_column(Integer, nullable=False)
    use_jewel_count: Mapped[int] = mapped_column(Integer, nullable=False)


class GoldsetDatumTeamlevel(Base):
    __tablename__ = 'goldset_data_teamlevel'

    initial_get_gold_count: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class GrandArenaDailyRankReward(Base):
    __tablename__ = 'grand_arena_daily_rank_reward'

    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class GrandArenaDefenceReward(Base):
    __tablename__ = 'grand_arena_defence_reward'

    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class GrandArenaMaxRankReward(Base):
    __tablename__ = 'grand_arena_max_rank_reward'

    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)


class GrandArenaMaxSeasonRankReward(Base):
    __tablename__ = 'grand_arena_max_season_rank_reward'

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)


class GrowthParameter(Base):
    __tablename__ = 'growth_parameter'

    equipment_2: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_restriction: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_4: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_6: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_type: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_3: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_level: Mapped[int] = mapped_column(Integer, nullable=False)


class GrowthParameterUnique(Base):
    __tablename__ = 'growth_parameter_unique'

    unique_equip_rank_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equip_strength_point_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equip_rank_1: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_equip_strength_point_2: Mapped[int] = mapped_column(Integer, nullable=False)


class GrowthRestrictionUnit(Base):
    __tablename__ = 'growth_restriction_unit'
    __table_args__ = (
        Index('growth_restriction_unit_0_growth_id', 'growth_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Guild(Base):
    __tablename__ = 'guild'

    member14: Mapped[int] = mapped_column(Integer, nullable=False)
    member20: Mapped[int] = mapped_column(Integer, nullable=False)
    member6: Mapped[int] = mapped_column(Integer, nullable=False)
    member15: Mapped[int] = mapped_column(Integer, nullable=False)
    member17: Mapped[int] = mapped_column(Integer, nullable=False)
    member22: Mapped[int] = mapped_column(Integer, nullable=False)
    member16: Mapped[int] = mapped_column(Integer, nullable=False)
    member21: Mapped[int] = mapped_column(Integer, nullable=False)
    member2: Mapped[int] = mapped_column(Integer, nullable=False)
    member18: Mapped[int] = mapped_column(Integer, nullable=False)
    member5: Mapped[int] = mapped_column(Integer, nullable=False)
    member1: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    member7: Mapped[int] = mapped_column(Integer, nullable=False)
    member28: Mapped[int] = mapped_column(Integer, nullable=False)
    member12: Mapped[int] = mapped_column(Integer, nullable=False)
    member19: Mapped[int] = mapped_column(Integer, nullable=False)
    member26: Mapped[int] = mapped_column(Integer, nullable=False)
    member30: Mapped[int] = mapped_column(Integer, nullable=False)
    member3: Mapped[int] = mapped_column(Integer, nullable=False)
    member29: Mapped[int] = mapped_column(Integer, nullable=False)
    member24: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_master: Mapped[int] = mapped_column(Integer, nullable=False)
    member8: Mapped[int] = mapped_column(Integer, nullable=False)
    member23: Mapped[int] = mapped_column(Integer, nullable=False)
    member9: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_name: Mapped[str] = mapped_column(Text, nullable=False)
    member27: Mapped[int] = mapped_column(Integer, nullable=False)
    member4: Mapped[int] = mapped_column(Integer, nullable=False)
    member13: Mapped[int] = mapped_column(Integer, nullable=False)
    member25: Mapped[int] = mapped_column(Integer, nullable=False)
    member10: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member11: Mapped[int] = mapped_column(Integer, nullable=False)


class GuildAdditionalMember(Base):
    __tablename__ = 'guild_additional_member'

    member7: Mapped[int] = mapped_column(Integer, nullable=False)
    member3: Mapped[int] = mapped_column(Integer, nullable=False)
    member4: Mapped[int] = mapped_column(Integer, nullable=False)
    member5: Mapped[int] = mapped_column(Integer, nullable=False)
    member8: Mapped[int] = mapped_column(Integer, nullable=False)
    member1: Mapped[int] = mapped_column(Integer, nullable=False)
    member2: Mapped[int] = mapped_column(Integer, nullable=False)
    thumb_id: Mapped[int] = mapped_column(Integer, nullable=False)
    member10: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member9: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    member6: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBattleMissionDatum(Base):
    __tablename__ = 'hatsune_battle_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneBgChange(Base):
    __tablename__ = 'hatsune_bg_change'

    quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBgChangeDatum(Base):
    __tablename__ = 'hatsune_bg_change_data'
    __table_args__ = (
        Index('hatsune_bg_change_data_0_target_type_1_area_id', 'target_type', 'area_id'),
    )

    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_after_change_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBoss(Base):
    __tablename__ = 'hatsune_boss'
    __table_args__ = (
        Index('hatsune_boss_0_event_id', 'event_id'),
        Index('hatsune_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
        Index('hatsune_boss_0_wave_group_id_1', 'wave_group_id_1')
    )

    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    required_skip_ticket_count: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_on_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_display_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    retire_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    map_arrow_offset: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    oneblow_count_of_skip_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    td_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    map_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    deatail_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    qd_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_collider_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    map_size: Mapped[float] = mapped_column(REAL, nullable=False)
    event_boss_treasure_box_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    use_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBossCondition(Base):
    __tablename__ = 'hatsune_boss_condition'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBossEnemySetting(Base):
    __tablename__ = 'hatsune_boss_enemy_setting'
    __table_args__ = (
        Index('hatsune_boss_enemy_setting_0_boss_id_1_event_id', 'boss_id', 'event_id'),
    )

    event_boss_treasure_box_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_identify: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    map_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    must_kill_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_gold_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    map_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBossExtraEffect(Base):
    __tablename__ = 'hatsune_boss_extra_effect'
    __table_args__ = (
        Index('hatsune_boss_extra_effect_0_boss_id', 'boss_id'),
        Index('hatsune_boss_extra_effect_0_boss_id_1_unit_id', 'boss_id', 'unit_id')
    )

    detail: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneDailyMissionDatum(Base):
    __tablename__ = 'hatsune_daily_mission_data'

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneDescription(Base):
    __tablename__ = 'hatsune_description'
    __table_args__ = (
        Index('hatsune_description_0_event_id_1_type', 'event_id', 'type'),
    )

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDiaryDatum(Base):
    __tablename__ = 'hatsune_diary_data'
    __table_args__ = (
        Index('hatsune_diary_data_0_contents_type', 'contents_type'),
    )

    diary_date: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    forced_release_time: Mapped[str] = mapped_column(Text, nullable=False)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_count: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    diary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDiaryLetterScript(Base):
    __tablename__ = 'hatsune_diary_letter_script'
    __table_args__ = (
        Index('hatsune_diary_letter_script_0_diary_id', 'diary_id'),
    )

    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    diary_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDiaryScript(Base):
    __tablename__ = 'hatsune_diary_script'
    __table_args__ = (
        Index('hatsune_diary_script_0_diary_id', 'diary_id'),
    )

    command: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    diary_text: Mapped[str] = mapped_column(Text, nullable=False)
    diary_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_animation_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneDiarySetting(Base):
    __tablename__ = 'hatsune_diary_setting'

    bgm_sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneEmblemMission(Base):
    __tablename__ = 'hatsune_emblem_mission'
    __table_args__ = (
        Index('hatsune_emblem_mission_0_event_id', 'event_id'),
    )

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneEmblemMissionReward(Base):
    __tablename__ = 'hatsune_emblem_mission_reward'
    __table_args__ = (
        Index('hatsune_emblem_mission_reward_0_mission_reward_id', 'mission_reward_id'),
        Index('hatsune_emblem_mission_reward_0_reward_id', 'reward_id')
    )

    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneExPlusSetting(Base):
    __tablename__ = 'hatsune_ex_plus_setting'

    limit_challenge_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneItem(Base):
    __tablename__ = 'hatsune_item'

    unit_material_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_material_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_9: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneLimitChara(Base):
    __tablename__ = 'hatsune_limit_chara'

    event_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_chara_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneMap(Base):
    __tablename__ = 'hatsune_map'

    end_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_area_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneMapEvent(Base):
    __tablename__ = 'hatsune_map_event'
    __table_args__ = (
        Index('hatsune_map_event_0_target_event_id', 'target_event_id'),
    )

    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param1: Mapped[int] = mapped_column(Integer, nullable=False)
    target_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneMissionRewardDatum(Base):
    __tablename__ = 'hatsune_mission_reward_data'
    __table_args__ = (
        Index('hatsune_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneMultiRouteParameter(Base):
    __tablename__ = 'hatsune_multi_route_parameter'
    __table_args__ = (
        Index('hatsune_multi_route_parameter_0_quest_id', 'quest_id'),
        Index('hatsune_multi_route_parameter_0_type', 'type')
    )

    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_2: Mapped[int] = mapped_column(Integer, nullable=False)
    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    param_3: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsunePointCounter(Base):
    __tablename__ = 'hatsune_point_counter'

    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    counter_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsunePresent(Base):
    __tablename__ = 'hatsune_present'
    __table_args__ = (
        Index('hatsune_present_0_event_id', 'event_id'),
    )

    item_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    dialog_title: Mapped[str] = mapped_column(Text, nullable=False)
    item_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dialog_text: Mapped[str] = mapped_column(Text, nullable=False)
    item_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuest(Base):
    __tablename__ = 'hatsune_quest'
    __table_args__ = (
        Index('hatsune_quest_0_event_id', 'event_id'),
    )

    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    drop_reward_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    icon_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_offset_y: Mapped[float] = mapped_column(REAL, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuestArea(Base):
    __tablename__ = 'hatsune_quest_area'
    __table_args__ = (
        Index('hatsune_quest_area_0_event_id', 'event_id'),
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_param_1: Mapped[str] = mapped_column(Text, nullable=False)
    area_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_param_2: Mapped[str] = mapped_column(Text, nullable=False)
    scroll_width: Mapped[int] = mapped_column(Integer, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    additional_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    open_tutorial_id: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scroll_height: Mapped[int] = mapped_column(Integer, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuestCondition(Base):
    __tablename__ = 'hatsune_quest_condition'
    __table_args__ = (
        Index('hatsune_quest_condition_0_event_id', 'event_id'),
    )

    condition_boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    release_boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuiz(Base):
    __tablename__ = 'hatsune_quiz'
    __table_args__ = (
        Index('hatsune_quiz_0_event_id', 'event_id'),
        Index('hatsune_quiz_0_event_id_1_release_quest_id', 'event_id', 'release_quest_id')
    )

    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_4: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id_quiz_start: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_id_quiz_end: Mapped[int] = mapped_column(Integer, nullable=False)
    question_title: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    answer: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_6: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_2: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_point_name: Mapped[str] = mapped_column(Text, nullable=False)
    choice_3: Mapped[str] = mapped_column(Text, nullable=False)
    choice_5: Mapped[str] = mapped_column(Text, nullable=False)
    choice_1: Mapped[str] = mapped_column(Text, nullable=False)
    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    hint: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneQuizCondition(Base):
    __tablename__ = 'hatsune_quiz_condition'
    __table_args__ = (
        Index('hatsune_quiz_condition_0_event_id_1_quiz_id', 'event_id', 'quiz_id'),
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quiz_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time_from: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuizReward(Base):
    __tablename__ = 'hatsune_quiz_reward'

    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneRelayDatum(Base):
    __tablename__ = 'hatsune_relay_data'

    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    relay_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_enable_read: Mapped[int] = mapped_column(Integer, nullable=False)
    story_seq: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSchedule(Base):
    __tablename__ = 'hatsune_schedule'
    __table_args__ = (
        Index('hatsune_schedule_0_original_event_id', 'original_event_id'),
        Index('hatsune_schedule_0_series_event_id', 'series_event_id')
    )

    backgroud_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_dialog_type: Mapped[int] = mapped_column(Integer, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    backgroud_size_y: Mapped[int] = mapped_column(Integer, nullable=False)
    backgroud_size_x: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    series_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    backgroud_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSeriesGachaReference(Base):
    __tablename__ = 'hatsune_series_gacha_reference'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reference_key_event_id_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSpecialBattle(Base):
    __tablename__ = 'hatsune_special_battle'
    __table_args__ = (
        Index('hatsune_special_battle_0_event_id', 'event_id'),
        Index('hatsune_special_battle_0_wave_group_id', 'wave_group_id')
    )

    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    is_hide_boss: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneSpecialBossTicketCount(Base):
    __tablename__ = 'hatsune_special_boss_ticket_count'

    use_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_count_to: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_count_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneSpecialEnemy(Base):
    __tablename__ = 'hatsune_special_enemy'

    initial_position: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_point: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneSpecialMissionDatum(Base):
    __tablename__ = 'hatsune_special_mission_data'

    special_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneStationaryMissionDatum(Base):
    __tablename__ = 'hatsune_stationary_mission_data'
    __table_args__ = (
        Index('hatsune_stationary_mission_data_0_event_id', 'event_id'),
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneUnlockStoryCondition(Base):
    __tablename__ = 'hatsune_unlock_story_condition'
    __table_args__ = (
        Index('hatsune_unlock_story_condition_0_event_id', 'event_id'),
    )

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_entry: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneUnlockUnitCondition(Base):
    __tablename__ = 'hatsune_unlock_unit_condition'
    __table_args__ = (
        Index('hatsune_unlock_unit_condition_0_condition_mission_id', 'condition_mission_id'),
        Index('hatsune_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id')
    )

    description_2: Mapped[str] = mapped_column(Text, nullable=False)
    top_description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description_1: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HpDrainAt(Base):
    __tablename__ = 'hp_drain_at'

    correction_value: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_value: Mapped[int] = mapped_column(Integer, nullable=False)


class ItemConvertAlcesPoint(Base):
    __tablename__ = 'item_convert_alces_point'

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alces_point: Mapped[int] = mapped_column(Integer, nullable=False)


class ItemDatum(Base):
    __tablename__ = 'item_data'

    limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    item_name: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sell_check_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class ItemETicketDatum(Base):
    __tablename__ = 'item_e_ticket_data'
    __table_args__ = (
        Index('item_e_ticket_data_0_exchange_number', 'exchange_number'),
        Index('item_e_ticket_data_0_ticket_id', 'ticket_id')
    )

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    exchange_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class JewelStoreNew(Base):
    __tablename__ = 'jewel_store_new'

    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    catagory: Mapped[int] = mapped_column(Integer, nullable=False)
    item_5: Mapped[str] = mapped_column(Text, nullable=False)
    bg: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ext_param: Mapped[str] = mapped_column(Text, nullable=False)
    text_2: Mapped[str] = mapped_column(Text, nullable=False)
    icon_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_2: Mapped[str] = mapped_column(Text, nullable=False)
    item_1: Mapped[str] = mapped_column(Text, nullable=False)
    item_3: Mapped[str] = mapped_column(Text, nullable=False)
    icon_3: Mapped[int] = mapped_column(Integer, nullable=False)
    text_3: Mapped[str] = mapped_column(Text, nullable=False)
    color: Mapped[str] = mapped_column(Text, nullable=False)
    item_4: Mapped[str] = mapped_column(Text, nullable=False)


class KaiserAddTimesDatum(Base):
    __tablename__ = 'kaiser_add_times_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)


class KaiserExterminationReward(Base):
    __tablename__ = 'kaiser_extermination_reward'

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)


class KaiserQuestDatum(Base):
    __tablename__ = 'kaiser_quest_data'

    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    restriction_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    kaiser_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    clear_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    odds_group_id: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer, nullable=False)


class KaiserRestrictionGroup(Base):
    __tablename__ = 'kaiser_restriction_group'
    __table_args__ = (
        Index('kaiser_restriction_group_0_restriction_group_id', 'restriction_group_id'),
    )

    restriction_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class KaiserSchedule(Base):
    __tablename__ = 'kaiser_schedule'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    after_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    after_bg: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bg: Mapped[str] = mapped_column(Text, nullable=False)


class KaiserSpecialBattle(Base):
    __tablename__ = 'kaiser_special_battle'

    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)


class KmkNaviComment(Base):
    __tablename__ = 'kmk_navi_comment'

    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class KmkReward(Base):
    __tablename__ = 'kmk_reward'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    kmk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class KnightMissionDatum(Base):
    __tablename__ = 'knight_mission_data'

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class KnightMissionRewardDatum(Base):
    __tablename__ = 'knight_mission_reward_data'
    __table_args__ = (
        Index('knight_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class KnightRankMaterialSetting(Base):
    __tablename__ = 'knight_rank_material_setting'

    point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthBgm(Base):
    __tablename__ = 'labyrinth_bgm'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)


class LabyrinthBlockPosition(Base):
    __tablename__ = 'labyrinth_block_position'

    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    block_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_index: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthCoinShopLineup(Base):
    __tablename__ = 'labyrinth_coin_shop_lineup'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    lineup_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lineup_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthDifficultyDatum(Base):
    __tablename__ = 'labyrinth_difficulty_data'

    score_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_reward_shard: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_reward_token: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_reward_coin: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_decrease_time: Mapped[int] = mapped_column(Integer, nullable=False)
    map_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_reward_treasure_box: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthDifficultyEffect(Base):
    __tablename__ = 'labyrinth_difficulty_effect'
    __table_args__ = (
        Index('labyrinth_difficulty_effect_0_difficulty', 'difficulty'),
    )

    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthDifficultyEnemyDatum(Base):
    __tablename__ = 'labyrinth_difficulty_enemy_data'

    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_3: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_4: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_2: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEnemyParameter(Base):
    __tablename__ = 'labyrinth_enemy_parameter'

    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEnhanceDatum(Base):
    __tablename__ = 'labyrinth_enhance_data'

    effect_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEnhanceInformation(Base):
    __tablename__ = 'labyrinth_enhance_information'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    information_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthEnhanceNode(Base):
    __tablename__ = 'labyrinth_enhance_node'

    information_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_2: Mapped[int] = mapped_column(Integer, nullable=False)
    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_rare: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_3: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEnterGuild(Base):
    __tablename__ = 'labyrinth_enter_guild'

    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_relic_id: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_name: Mapped[str] = mapped_column(Text, nullable=False)
    guild_master_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEnterReward(Base):
    __tablename__ = 'labyrinth_enter_reward'
    __table_args__ = (
        Index('labyrinth_enter_reward_0_reward_group_id', 'reward_group_id'),
    )

    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEvent(Base):
    __tablename__ = 'labyrinth_event'

    choice_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_text: Mapped[str] = mapped_column(Text, nullable=False)
    choice_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthEventChoice(Base):
    __tablename__ = 'labyrinth_event_choice'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_comment: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_animation: Mapped[str] = mapped_column(Text, nullable=False)
    choice_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthEventDrama(Base):
    __tablename__ = 'labyrinth_event_drama'
    __table_args__ = (
        Index('labyrinth_event_drama_0_drama_id', 'drama_id'),
    )

    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class LabyrinthEventEffectRewardEmpty(Base):
    __tablename__ = 'labyrinth_event_effect_reward_empty'
    __table_args__ = (
        Index('labyrinth_event_effect_reward_empty_0_effect_type', 'effect_type'),
    )

    effect_value: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class LabyrinthEventResult(Base):
    __tablename__ = 'labyrinth_event_result'

    effect_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    event_result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_2: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthExQuestDatumDisplay(Base):
    __tablename__ = 'labyrinth_ex_quest_data_display'

    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    map_point_enemy_size: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    map_point_enemy_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    map_point_enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthMapBgDatum(Base):
    __tablename__ = 'labyrinth_map_bg_data'

    width: Mapped[int] = mapped_column(Integer, nullable=False)
    offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    column: Mapped[int] = mapped_column(Integer, primary_key=True)
    offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    height: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthMission(Base):
    __tablename__ = 'labyrinth_mission'
    __table_args__ = (
        Index('labyrinth_mission_0_category_id', 'category_id'),
    )

    condition_guild_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthMissionReward(Base):
    __tablename__ = 'labyrinth_mission_reward'
    __table_args__ = (
        Index('labyrinth_mission_reward_0_mission_reward_id', 'mission_reward_id'),
    )

    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthNpcUnitDatum(Base):
    __tablename__ = 'labyrinth_npc_unit_data'

    enhance_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthNpcUnitEnhanceDatum(Base):
    __tablename__ = 'labyrinth_npc_unit_enhance_data'

    ex_equip_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equip_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equip_enhance_level_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equip_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equip_enhance_level_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equip_enhance_level_3: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthPointReward(Base):
    __tablename__ = 'labyrinth_point_reward'

    labyrinth_point: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthQuestDatum(Base):
    __tablename__ = 'labyrinth_quest_data'

    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_type: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthQuestDatumDisplay(Base):
    __tablename__ = 'labyrinth_quest_data_display'

    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthRelic(Base):
    __tablename__ = 'labyrinth_relic'

    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    first_acquisition_jewel: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_num: Mapped[int] = mapped_column(Integer, nullable=False)
    relic_mark_id: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    relic_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_description: Mapped[str] = mapped_column(Text, nullable=False)
    effect_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    relic_mark_count: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthRelicEffect(Base):
    __tablename__ = 'labyrinth_relic_effect'

    effect_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthRelicEffectGroup(Base):
    __tablename__ = 'labyrinth_relic_effect_group'

    effect_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthRelicMarkEffect(Base):
    __tablename__ = 'labyrinth_relic_mark_effect'
    __table_args__ = (
        Index('labyrinth_relic_mark_effect_0_relic_mark_id', 'relic_mark_id'),
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    relic_mark_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_count: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthRelicMarkSeries(Base):
    __tablename__ = 'labyrinth_relic_mark_series'

    relic_mark_title: Mapped[str] = mapped_column(Text, nullable=False)
    relic_mark_series_name: Mapped[str] = mapped_column(Text, nullable=False)
    relic_mark_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    series_description: Mapped[str] = mapped_column(Text, nullable=False)


class LabyrinthRelicRestrictGroup(Base):
    __tablename__ = 'labyrinth_relic_restrict_group'
    __table_args__ = (
        Index('labyrinth_relic_restrict_group_0_group_id', 'group_id'),
    )

    relic_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthRewardByGuild(Base):
    __tablename__ = 'labyrinth_reward_by_guild'

    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthSetting(Base):
    __tablename__ = 'labyrinth_setting'

    setting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthSkillActionReplace(Base):
    __tablename__ = 'labyrinth_skill_action_replace'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    action_value_4: Mapped[float] = mapped_column(REAL, nullable=False)
    action_value_7: Mapped[float] = mapped_column(REAL, nullable=False)
    target_count: Mapped[int] = mapped_column(Integer, nullable=False)
    action_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_5: Mapped[float] = mapped_column(REAL, nullable=False)
    action_detail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    action_detail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_range: Mapped[int] = mapped_column(Integer, nullable=False)
    target_assignment: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_6: Mapped[float] = mapped_column(REAL, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_2: Mapped[float] = mapped_column(REAL, nullable=False)
    target_area: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_1: Mapped[float] = mapped_column(REAL, nullable=False)
    target_number: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_3: Mapped[float] = mapped_column(REAL, nullable=False)


class LabyrinthSkipDisplay(Base):
    __tablename__ = 'labyrinth_skip_display'

    enemy_unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthSummonUnit(Base):
    __tablename__ = 'labyrinth_summon_unit'

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    summon_num: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    summon_type: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthTreasureDisplay(Base):
    __tablename__ = 'labyrinth_treasure_display'
    __table_args__ = (
        Index('labyrinth_treasure_display_0_guild_id', 'guild_id'),
    )

    reward_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image: Mapped[int] = mapped_column(Integer, nullable=False)


class LabyrinthUnitHighlighting(Base):
    __tablename__ = 'labyrinth_unit_highlighting'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthVoiceSetting(Base):
    __tablename__ = 'labyrinth_voice_setting'

    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cue_sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    scene_type: Mapped[int] = mapped_column(Integer, primary_key=True)


class LabyrinthWaveGroupDatum(Base):
    __tablename__ = 'labyrinth_wave_group_data'

    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionAddTimesDatum(Base):
    __tablename__ = 'legion_add_times_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionBattleBonus(Base):
    __tablename__ = 'legion_battle_bonus'
    __table_args__ = (
        Index('legion_battle_bonus_0_type', 'type'),
        Index('legion_battle_bonus_0_type_1_legion_boss_id', 'type', 'legion_boss_id')
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_hp: Mapped[str] = mapped_column(Text, nullable=False)
    legion_battle_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_battle_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionBattleBonusEffect(Base):
    __tablename__ = 'legion_battle_bonus_effect'

    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    text_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LegionBossEnemySetting(Base):
    __tablename__ = 'legion_boss_enemy_setting'

    detail_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_offset_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionEffect(Base):
    __tablename__ = 'legion_effect'

    bonus_3: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_1: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionEffectiveUnit(Base):
    __tablename__ = 'legion_effective_unit'
    __table_args__ = (
        Index('legion_effective_unit_0_legion_boss_id', 'legion_boss_id'),
    )

    legion_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    support_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LegionExterminationReward(Base):
    __tablename__ = 'legion_extermination_reward'

    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionMissionCategoryDatum(Base):
    __tablename__ = 'legion_mission_category_data'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class LegionMissionDatum(Base):
    __tablename__ = 'legion_mission_data'
    __table_args__ = (
        Index('legion_mission_data_0_category_id', 'category_id'),
    )

    condition_num: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class LegionMissionRewardDatum(Base):
    __tablename__ = 'legion_mission_reward_data'
    __table_args__ = (
        Index('legion_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionQuestDatum(Base):
    __tablename__ = 'legion_quest_data'
    __table_args__ = (
        Index('legion_quest_data_0_map_type', 'map_type'),
    )

    battle_finish_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    expel_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    all_disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    battle_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_max: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    max_raid_hp: Mapped[str] = mapped_column(Text, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)


class LegionSchedule(Base):
    __tablename__ = 'legion_schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bg: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class LegionSpecialBattle(Base):
    __tablename__ = 'legion_special_battle'

    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)


class LimitedMissionCategory(Base):
    __tablename__ = 'limited_mission_category'

    release_condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    label_type: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_receive_period: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    complete_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    short_name: Mapped[str] = mapped_column(Text, nullable=False)
    display_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class LimitedMissionDetail(Base):
    __tablename__ = 'limited_mission_detail'
    __table_args__ = (
        Index('limited_mission_detail_0_step_id', 'step_id'),
    )

    reward_icon_2: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_icon_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_icon_1: Mapped[int] = mapped_column(Integer, nullable=False)
    label_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    step_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)


class LimitedMissionGroup(Base):
    __tablename__ = 'limited_mission_group'
    __table_args__ = (
        Index('limited_mission_group_0_category_id', 'category_id'),
        Index('limited_mission_group_0_release_condition_group_id', 'release_condition_group_id')
    )

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    complete_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    notification: Mapped[str] = mapped_column(Text, nullable=False)
    release_condition_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class LimitedMissionLabelSetting(Base):
    __tablename__ = 'limited_mission_label_setting'

    label_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    color: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    color2: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)


class LimitedMissionMoveView(Base):
    __tablename__ = 'limited_mission_move_view'

    mission_condition: Mapped[int] = mapped_column(Integer, primary_key=True)
    notification: Mapped[str] = mapped_column(Text, nullable=False)
    move_view_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LimitedMissionReward(Base):
    __tablename__ = 'limited_mission_reward'
    __table_args__ = (
        Index('limited_mission_reward_0_reward_group_id', 'reward_group_id'),
    )

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LimitedMissionStep(Base):
    __tablename__ = 'limited_mission_step'
    __table_args__ = (
        Index('limited_mission_step_0_group_id', 'group_id'),
        Index('limited_mission_step_0_release_condition_step_id', 'release_condition_step_id')
    )

    step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_condition_step_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class ListoryNaviComment(Base):
    __tablename__ = 'listory_navi_comment'
    __table_args__ = (
        Index('listory_navi_comment_0_event_id', 'event_id'),
        Index('listory_navi_comment_0_event_id_1_character_id', 'event_id', 'character_id')
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)


class ListorySetting(Base):
    __tablename__ = 'listory_setting'

    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    all_read_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    opening_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ListoryTutorial(Base):
    __tablename__ = 'listory_tutorial'
    __table_args__ = (
        Index('listory_tutorial_0_event_id', 'event_id'),
    )

    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    navi_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class LoginBonusAdv(Base):
    __tablename__ = 'login_bonus_adv'
    __table_args__ = (
        Index('login_bonus_adv_0_login_bonus_id', 'login_bonus_id'),
    )

    count_key: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    read_process_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class LoginBonusDatum(Base):
    __tablename__ = 'login_bonus_data'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    login_bonus_type: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    stamp_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count_type: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_num: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_play_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class LoginBonusDetail(Base):
    __tablename__ = 'login_bonus_detail'
    __table_args__ = (
        Index('login_bonus_detail_0_login_bonus_id_1_count', 'login_bonus_id', 'count'),
    )

    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)


class LoginBonusMessageDatum(Base):
    __tablename__ = 'login_bonus_message_data'
    __table_args__ = (
        Index('login_bonus_message_data_0_login_bonus_id', 'login_bonus_id'),
    )

    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_param: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    luck_pattern: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_type: Mapped[int] = mapped_column(Integer, nullable=False)
    rate: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    day_count: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class LoveChara(Base):
    __tablename__ = 'love_chara'

    unlocked_class: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_love: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)


class LoveRankup(Base):
    __tablename__ = 'love_rankup'
    __table_args__ = (
        Index('love_rankup_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    love_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LssNaviComment(Base):
    __tablename__ = 'lss_navi_comment'
    __table_args__ = (
        Index('lss_navi_comment_0_character_id', 'character_id'),
        Index('lss_navi_comment_0_where_type', 'where_type')
    )

    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)


class LssStoryDatum(Base):
    __tablename__ = 'lss_story_data'
    __table_args__ = (
        Index('lss_story_data_0_original_event_id', 'original_event_id'),
        Index('lss_story_data_0_read_condition_sub_story_id', 'read_condition_sub_story_id')
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LsvDramaScript(Base):
    __tablename__ = 'lsv_drama_script'
    __table_args__ = (
        Index('lsv_drama_script_0_drama_id', 'drama_id'),
    )

    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class LsvStoryDatum(Base):
    __tablename__ = 'lsv_story_data'
    __table_args__ = (
        Index('lsv_story_data_0_original_event_id', 'original_event_id'),
    )

    read_event_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    time_condition: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)


class LsvStoryScript(Base):
    __tablename__ = 'lsv_story_script'
    __table_args__ = (
        Index('lsv_story_script_0_story_id', 'story_id'),
    )

    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)


class LtoLetterScript(Base):
    __tablename__ = 'lto_letter_script'
    __table_args__ = (
        Index('lto_letter_script_0_letter_id', 'letter_id'),
    )

    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    letter_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class LtoStoryDatum(Base):
    __tablename__ = 'lto_story_data'
    __table_args__ = (
        Index('lto_story_data_0_event_id', 'event_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)


class Metamorphose(Base):
    __tablename__ = 'metamorphose'
    __table_args__ = (
        Index('metamorphose_0_type_id', 'type_id'),
    )

    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value: Mapped[int] = mapped_column(Integer, primary_key=True)


class MhpDramaScript(Base):
    __tablename__ = 'mhp_drama_script'
    __table_args__ = (
        Index('mhp_drama_script_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)


class MhpStoryDatum(Base):
    __tablename__ = 'mhp_story_data'
    __table_args__ = (
        Index('mhp_story_data_0_original_event_id', 'original_event_id'),
        Index('mhp_story_data_0_unit_id', 'unit_id')
    )

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Minigame(Base):
    __tablename__ = 'minigame'
    __table_args__ = (
        Index('minigame_0_event_id', 'event_id'),
    )

    release_conditions_1: Mapped[int] = mapped_column(Integer, nullable=False)
    is_enabled_zero_score: Mapped[int] = mapped_column(Integer, nullable=False)
    first_time_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_chat_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    conditions_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    score_unit: Mapped[str] = mapped_column(Text, nullable=False)
    minigame_scheme_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    display_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageBattleEffect(Base):
    __tablename__ = 'mirage_battle_effect'
    __table_args__ = (
        Index('mirage_battle_effect_0_quest_id', 'quest_id'),
    )

    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class MirageClearReward(Base):
    __tablename__ = 'mirage_clear_reward'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageEnemyParameter(Base):
    __tablename__ = 'mirage_enemy_parameter'

    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageFloorQuest(Base):
    __tablename__ = 'mirage_floor_quest'

    clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    release_time: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageFloorQuestDisplay(Base):
    __tablename__ = 'mirage_floor_quest_display'

    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageFloorSetting(Base):
    __tablename__ = 'mirage_floor_setting'

    floor_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pool_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageNemesisArea(Base):
    __tablename__ = 'mirage_nemesis_area'

    nemesis_area_name: Mapped[str] = mapped_column(Text, nullable=False)
    nemesis_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_time: Mapped[str] = mapped_column(Text, nullable=False)


class MirageNemesisQuest(Base):
    __tablename__ = 'mirage_nemesis_quest'
    __table_args__ = (
        Index('mirage_nemesis_quest_0_nemesis_id', 'nemesis_id'),
    )

    clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_time: Mapped[str] = mapped_column(Text, nullable=False)
    nemesis_id: Mapped[int] = mapped_column(Integer, nullable=False)
    area_level: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MirageNemesisQuestDisplay(Base):
    __tablename__ = 'mirage_nemesis_quest_display'

    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_enemy_size: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_enemy_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)


class MiragePoolRewardDisplay(Base):
    __tablename__ = 'mirage_pool_reward_display'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_max: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_min: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)


class MirageSetting(Base):
    __tablename__ = 'mirage_setting'

    pool_reward_accumulate_day_num_max: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_count_max: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MirageWaveGroupDatum(Base):
    __tablename__ = 'mirage_wave_group_data'

    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class MirokuBossDatum(Base):
    __tablename__ = 'miroku_boss_data'

    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)


class MirokuSpecialBattle(Base):
    __tablename__ = 'miroku_special_battle'

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que: Mapped[str] = mapped_column(Text, nullable=False)
    story_end_after_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_start_after_block_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MissionCategoryIcon(Base):
    __tablename__ = 'mission_category_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    color: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)


class MissionRewardDatum(Base):
    __tablename__ = 'mission_reward_data'
    __table_args__ = (
        Index('mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class MmeStoryDatum(Base):
    __tablename__ = 'mme_story_data'
    __table_args__ = (
        Index('mme_story_data_0_original_event_id', 'original_event_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    is_last: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_puzzle_piece: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class Movie(Base):
    __tablename__ = 'movie'
    __table_args__ = (
        Index('movie_0_story_id', 'story_id'),
    )

    fade_loop_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_id: Mapped[str] = mapped_column(Text, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_volume_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    se_id: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    my_page_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MreBgDatum(Base):
    __tablename__ = 'mre_bg_data'
    __table_args__ = (
        Index('mre_bg_data_0_mre_id', 'mre_id'),
    )

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MreBossReward(Base):
    __tablename__ = 'mre_boss_reward'

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class MreEnemyParameter(Base):
    __tablename__ = 'mre_enemy_parameter'

    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)


class MreGachaDatum(Base):
    __tablename__ = 'mre_gacha_data'

    reset_item_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    box_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MreMissionDatum(Base):
    __tablename__ = 'mre_mission_data'
    __table_args__ = (
        Index('mre_mission_data_0_mission_id', 'mission_id'),
        Index('mre_mission_data_0_mre_id', 'mre_id'),
        Index('mre_mission_data_0_mre_id_1_mission_type', 'mre_id', 'mission_type')
    )

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    destination_system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)


class MreNaviComment(Base):
    __tablename__ = 'mre_navi_comment'

    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class MrePickupBanner(Base):
    __tablename__ = 'mre_pickup_banner'
    __table_args__ = (
        Index('mre_pickup_banner_0_schedule_id', 'schedule_id'),
    )

    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MreQuestDatum(Base):
    __tablename__ = 'mre_quest_data'
    __table_args__ = (
        Index('mre_quest_data_0_mre_id', 'mre_id'),
    )

    clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    first_clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size: Mapped[float] = mapped_column(REAL, nullable=False)


class MreRaidHpReward(Base):
    __tablename__ = 'mre_raid_hp_reward'
    __table_args__ = (
        Index('mre_raid_hp_reward_0_mre_id', 'mre_id'),
    )

    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    total_hp_damage_ratio: Mapped[int] = mapped_column(Integer, nullable=False)
    raid_hp_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)


class MreSchedule(Base):
    __tablename__ = 'mre_schedule'
    __table_args__ = (
        Index('mre_schedule_0_mre_id', 'mre_id'),
    )

    boss_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reminder_day: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    max_raid_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MreSetting(Base):
    __tablename__ = 'mre_setting'

    mre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    top_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    top_boss_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    banner_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_boss_size: Mapped[float] = mapped_column(REAL, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class MreStoryDatum(Base):
    __tablename__ = 'mre_story_data'
    __table_args__ = (
        Index('mre_story_data_0_mre_id', 'mre_id'),
        Index('mre_story_data_0_mre_id_1_story_type', 'mre_id', 'story_type')
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_index: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mre_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MreTutorialDatum(Base):
    __tablename__ = 'mre_tutorial_data'
    __table_args__ = (
        Index('mre_tutorial_data_0_event_type_1_tutorial_type', 'event_type', 'tutorial_type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tutorial_image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_type: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_text: Mapped[str] = mapped_column(Text, nullable=False)


class MreWaveGroupDatum(Base):
    __tablename__ = 'mre_wave_group_data'

    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)


class MusicContent(Base):
    __tablename__ = 'music_content'

    detail: Mapped[str] = mapped_column(Text, nullable=False)
    music_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_playing_time: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    cue_id: Mapped[str] = mapped_column(Text, nullable=False)
    listen_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class MusicList(Base):
    __tablename__ = 'music_list'

    shop_start: Mapped[str] = mapped_column(Text, nullable=False)
    shop_end: Mapped[str] = mapped_column(Text, nullable=False)
    list_name: Mapped[str] = mapped_column(Text, nullable=False)
    font_size: Mapped[float] = mapped_column(REAL, nullable=False)
    pre_shop_start: Mapped[str] = mapped_column(Text, nullable=False)
    kana: Mapped[str] = mapped_column(Text, nullable=False)
    music_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dmm_url: Mapped[str] = mapped_column(Text, nullable=False)
    android_url: Mapped[str] = mapped_column(Text, nullable=False)
    ios_url: Mapped[str] = mapped_column(Text, nullable=False)
    sort: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_item_num: Mapped[int] = mapped_column(Integer, nullable=False)


class MyProfilePictureFrame(Base):
    __tablename__ = 'my_profile_picture_frame'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    pic_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    ext_param: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    fps: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class MypageCharacterMovie(Base):
    __tablename__ = 'mypage_character_movie'

    skin_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)


class MypageFrame(Base):
    __tablename__ = 'mypage_frame'
    __table_args__ = (
        Index('mypage_frame_0_group_id', 'group_id'),
    )

    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    frame_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MyprofileContent(Base):
    __tablename__ = 'myprofile_content'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)


class NaviComment(Base):
    __tablename__ = 'navi_comment'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class NbbDramaScript(Base):
    __tablename__ = 'nbb_drama_script'
    __table_args__ = (
        Index('nbb_drama_script_0_drama_id', 'drama_id'),
    )

    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class NbbEmblem(Base):
    __tablename__ = 'nbb_emblem'

    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    one_play_score: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class NbbFaceIconActionDatum(Base):
    __tablename__ = 'nbb_face_icon_action_data'
    __table_args__ = (
        Index('nbb_face_icon_action_data_0_action_type', 'action_type'),
    )

    voice_cue_1: Mapped[str] = mapped_column(Text, nullable=False)
    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    play_time: Mapped[int] = mapped_column(Integer, nullable=False)
    action_param: Mapped[int] = mapped_column(Integer, nullable=False)
    face_icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    text_2: Mapped[str] = mapped_column(Text, nullable=False)
    voice_cue_2: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class NbbFirstFrame(Base):
    __tablename__ = 'nbb_first_frame'
    __table_args__ = (
        Index('nbb_first_frame_0_frame_id', 'frame_id'),
    )

    row_36: Mapped[int] = mapped_column(Integer, nullable=False)
    row_26: Mapped[int] = mapped_column(Integer, nullable=False)
    row_15: Mapped[int] = mapped_column(Integer, nullable=False)
    row_51: Mapped[int] = mapped_column(Integer, nullable=False)
    row_52: Mapped[int] = mapped_column(Integer, nullable=False)
    row_7: Mapped[int] = mapped_column(Integer, nullable=False)
    row_42: Mapped[int] = mapped_column(Integer, nullable=False)
    row_58: Mapped[int] = mapped_column(Integer, nullable=False)
    row_16: Mapped[int] = mapped_column(Integer, nullable=False)
    row_9: Mapped[int] = mapped_column(Integer, nullable=False)
    row_17: Mapped[int] = mapped_column(Integer, nullable=False)
    row_60: Mapped[int] = mapped_column(Integer, nullable=False)
    row_56: Mapped[int] = mapped_column(Integer, nullable=False)
    row_20: Mapped[int] = mapped_column(Integer, nullable=False)
    row_41: Mapped[int] = mapped_column(Integer, nullable=False)
    row_57: Mapped[int] = mapped_column(Integer, nullable=False)
    row_49: Mapped[int] = mapped_column(Integer, nullable=False)
    row_59: Mapped[int] = mapped_column(Integer, nullable=False)
    row_35: Mapped[int] = mapped_column(Integer, nullable=False)
    row_30: Mapped[int] = mapped_column(Integer, nullable=False)
    row_23: Mapped[int] = mapped_column(Integer, nullable=False)
    row_40: Mapped[int] = mapped_column(Integer, nullable=False)
    row_45: Mapped[int] = mapped_column(Integer, nullable=False)
    row_8: Mapped[int] = mapped_column(Integer, nullable=False)
    row_38: Mapped[int] = mapped_column(Integer, nullable=False)
    row_47: Mapped[int] = mapped_column(Integer, nullable=False)
    lane: Mapped[int] = mapped_column(Integer, nullable=False)
    row_10: Mapped[int] = mapped_column(Integer, nullable=False)
    row_3: Mapped[int] = mapped_column(Integer, nullable=False)
    row_33: Mapped[int] = mapped_column(Integer, nullable=False)
    row_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    row_31: Mapped[int] = mapped_column(Integer, nullable=False)
    row_21: Mapped[int] = mapped_column(Integer, nullable=False)
    row_48: Mapped[int] = mapped_column(Integer, nullable=False)
    row_22: Mapped[int] = mapped_column(Integer, nullable=False)
    row_50: Mapped[int] = mapped_column(Integer, nullable=False)
    row_1: Mapped[int] = mapped_column(Integer, nullable=False)
    row_29: Mapped[int] = mapped_column(Integer, nullable=False)
    row_43: Mapped[int] = mapped_column(Integer, nullable=False)
    row_32: Mapped[int] = mapped_column(Integer, nullable=False)
    row_46: Mapped[int] = mapped_column(Integer, nullable=False)
    row_39: Mapped[int] = mapped_column(Integer, nullable=False)
    row_27: Mapped[int] = mapped_column(Integer, nullable=False)
    row_12: Mapped[int] = mapped_column(Integer, nullable=False)
    row_24: Mapped[int] = mapped_column(Integer, nullable=False)
    row_11: Mapped[int] = mapped_column(Integer, nullable=False)
    row_53: Mapped[int] = mapped_column(Integer, nullable=False)
    row_4: Mapped[int] = mapped_column(Integer, nullable=False)
    row_18: Mapped[int] = mapped_column(Integer, nullable=False)
    row_44: Mapped[int] = mapped_column(Integer, nullable=False)
    row_34: Mapped[int] = mapped_column(Integer, nullable=False)
    row_55: Mapped[int] = mapped_column(Integer, nullable=False)
    row_25: Mapped[int] = mapped_column(Integer, nullable=False)
    row_6: Mapped[int] = mapped_column(Integer, nullable=False)
    row_19: Mapped[int] = mapped_column(Integer, nullable=False)
    row_54: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False)
    row_13: Mapped[int] = mapped_column(Integer, nullable=False)
    row_2: Mapped[int] = mapped_column(Integer, nullable=False)
    row_14: Mapped[int] = mapped_column(Integer, nullable=False)
    row_28: Mapped[int] = mapped_column(Integer, nullable=False)
    row_37: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbFrame(Base):
    __tablename__ = 'nbb_frame'
    __table_args__ = (
        Index('nbb_frame_0_difficulty', 'difficulty'),
    )

    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    row_23: Mapped[int] = mapped_column(Integer, nullable=False)
    row_41: Mapped[int] = mapped_column(Integer, nullable=False)
    row_28: Mapped[int] = mapped_column(Integer, nullable=False)
    row_47: Mapped[int] = mapped_column(Integer, nullable=False)
    row_6: Mapped[int] = mapped_column(Integer, nullable=False)
    row_44: Mapped[int] = mapped_column(Integer, nullable=False)
    row_45: Mapped[int] = mapped_column(Integer, nullable=False)
    min_clear_num: Mapped[int] = mapped_column(Integer, nullable=False)
    row_52: Mapped[int] = mapped_column(Integer, nullable=False)
    row_55: Mapped[int] = mapped_column(Integer, nullable=False)
    row_56: Mapped[int] = mapped_column(Integer, nullable=False)
    row_48: Mapped[int] = mapped_column(Integer, nullable=False)
    row_49: Mapped[int] = mapped_column(Integer, nullable=False)
    row_9: Mapped[int] = mapped_column(Integer, nullable=False)
    row_16: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    row_32: Mapped[int] = mapped_column(Integer, nullable=False)
    row_36: Mapped[int] = mapped_column(Integer, nullable=False)
    row_21: Mapped[int] = mapped_column(Integer, nullable=False)
    row_2: Mapped[int] = mapped_column(Integer, nullable=False)
    row_7: Mapped[int] = mapped_column(Integer, nullable=False)
    row_4: Mapped[int] = mapped_column(Integer, nullable=False)
    row_57: Mapped[int] = mapped_column(Integer, nullable=False)
    row_17: Mapped[int] = mapped_column(Integer, nullable=False)
    row_27: Mapped[int] = mapped_column(Integer, nullable=False)
    row_34: Mapped[int] = mapped_column(Integer, nullable=False)
    row_13: Mapped[int] = mapped_column(Integer, nullable=False)
    row_42: Mapped[int] = mapped_column(Integer, nullable=False)
    row_12: Mapped[int] = mapped_column(Integer, nullable=False)
    row_60: Mapped[int] = mapped_column(Integer, nullable=False)
    row_59: Mapped[int] = mapped_column(Integer, nullable=False)
    row_39: Mapped[int] = mapped_column(Integer, nullable=False)
    row_30: Mapped[int] = mapped_column(Integer, nullable=False)
    row_24: Mapped[int] = mapped_column(Integer, nullable=False)
    row_31: Mapped[int] = mapped_column(Integer, nullable=False)
    row_22: Mapped[int] = mapped_column(Integer, nullable=False)
    row_15: Mapped[int] = mapped_column(Integer, nullable=False)
    row_18: Mapped[int] = mapped_column(Integer, nullable=False)
    row_1: Mapped[int] = mapped_column(Integer, nullable=False)
    row_37: Mapped[int] = mapped_column(Integer, nullable=False)
    row_20: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False)
    row_5: Mapped[int] = mapped_column(Integer, nullable=False)
    row_38: Mapped[int] = mapped_column(Integer, nullable=False)
    lane: Mapped[int] = mapped_column(Integer, nullable=False)
    row_58: Mapped[int] = mapped_column(Integer, nullable=False)
    row_11: Mapped[int] = mapped_column(Integer, nullable=False)
    row_3: Mapped[int] = mapped_column(Integer, nullable=False)
    row_29: Mapped[int] = mapped_column(Integer, nullable=False)
    row_35: Mapped[int] = mapped_column(Integer, nullable=False)
    row_8: Mapped[int] = mapped_column(Integer, nullable=False)
    row_50: Mapped[int] = mapped_column(Integer, nullable=False)
    row_53: Mapped[int] = mapped_column(Integer, nullable=False)
    row_40: Mapped[int] = mapped_column(Integer, nullable=False)
    row_19: Mapped[int] = mapped_column(Integer, nullable=False)
    row_14: Mapped[int] = mapped_column(Integer, nullable=False)
    row_46: Mapped[int] = mapped_column(Integer, nullable=False)
    row_10: Mapped[int] = mapped_column(Integer, nullable=False)
    row_51: Mapped[int] = mapped_column(Integer, nullable=False)
    row_33: Mapped[int] = mapped_column(Integer, nullable=False)
    row_26: Mapped[int] = mapped_column(Integer, nullable=False)
    row_25: Mapped[int] = mapped_column(Integer, nullable=False)
    row_43: Mapped[int] = mapped_column(Integer, nullable=False)
    row_54: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbFrameLottery(Base):
    __tablename__ = 'nbb_frame_lottery'
    __table_args__ = (
        Index('nbb_frame_lottery_0_mode', 'mode'),
    )

    difficulty_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty_1: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_4: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_2: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbModeSetting(Base):
    __tablename__ = 'nbb_mode_setting'

    mode_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    soldier_init_num: Mapped[int] = mapped_column(Integer, nullable=False)
    support_ratio: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbNaviComment(Base):
    __tablename__ = 'nbb_navi_comment'

    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class NbbObjDatum(Base):
    __tablename__ = 'nbb_obj_data'

    obj_value: Mapped[int] = mapped_column(Integer, nullable=False)
    obj_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    obj_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    obj_type: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbScoreReward(Base):
    __tablename__ = 'nbb_score_reward'
    __table_args__ = (
        Index('nbb_score_reward_0_id', 'id'),
        Index('nbb_score_reward_0_nbb_chara_type', 'nbb_chara_type')
    )

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    nbb_chara_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class NbbSpeedSetting(Base):
    __tablename__ = 'nbb_speed_setting'
    __table_args__ = (
        Index('nbb_speed_setting_0_mode', 'mode'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbSupportDetail(Base):
    __tablename__ = 'nbb_support_detail'

    value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    value_6: Mapped[int] = mapped_column(Integer, nullable=False)
    support_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    support_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    support_time: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbSupportFrame(Base):
    __tablename__ = 'nbb_support_frame'
    __table_args__ = (
        Index('nbb_support_frame_0_difficulty', 'difficulty'),
    )

    row_52: Mapped[int] = mapped_column(Integer, nullable=False)
    row_16: Mapped[int] = mapped_column(Integer, nullable=False)
    row_40: Mapped[int] = mapped_column(Integer, nullable=False)
    row_27: Mapped[int] = mapped_column(Integer, nullable=False)
    row_12: Mapped[int] = mapped_column(Integer, nullable=False)
    row_36: Mapped[int] = mapped_column(Integer, nullable=False)
    row_28: Mapped[int] = mapped_column(Integer, nullable=False)
    row_33: Mapped[int] = mapped_column(Integer, nullable=False)
    row_50: Mapped[int] = mapped_column(Integer, nullable=False)
    row_4: Mapped[int] = mapped_column(Integer, nullable=False)
    row_14: Mapped[int] = mapped_column(Integer, nullable=False)
    row_39: Mapped[int] = mapped_column(Integer, nullable=False)
    row_13: Mapped[int] = mapped_column(Integer, nullable=False)
    row_48: Mapped[int] = mapped_column(Integer, nullable=False)
    row_8: Mapped[int] = mapped_column(Integer, nullable=False)
    min_clear_num: Mapped[int] = mapped_column(Integer, nullable=False)
    row_53: Mapped[int] = mapped_column(Integer, nullable=False)
    row_34: Mapped[int] = mapped_column(Integer, nullable=False)
    row_42: Mapped[int] = mapped_column(Integer, nullable=False)
    row_3: Mapped[int] = mapped_column(Integer, nullable=False)
    row_25: Mapped[int] = mapped_column(Integer, nullable=False)
    row_30: Mapped[int] = mapped_column(Integer, nullable=False)
    row_7: Mapped[int] = mapped_column(Integer, nullable=False)
    row_49: Mapped[int] = mapped_column(Integer, nullable=False)
    row_37: Mapped[int] = mapped_column(Integer, nullable=False)
    row_23: Mapped[int] = mapped_column(Integer, nullable=False)
    row_45: Mapped[int] = mapped_column(Integer, nullable=False)
    row_41: Mapped[int] = mapped_column(Integer, nullable=False)
    row_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    row_58: Mapped[int] = mapped_column(Integer, nullable=False)
    row_54: Mapped[int] = mapped_column(Integer, nullable=False)
    row_15: Mapped[int] = mapped_column(Integer, nullable=False)
    row_57: Mapped[int] = mapped_column(Integer, nullable=False)
    row_35: Mapped[int] = mapped_column(Integer, nullable=False)
    row_1: Mapped[int] = mapped_column(Integer, nullable=False)
    row_51: Mapped[int] = mapped_column(Integer, nullable=False)
    row_19: Mapped[int] = mapped_column(Integer, nullable=False)
    row_18: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False)
    row_10: Mapped[int] = mapped_column(Integer, nullable=False)
    row_22: Mapped[int] = mapped_column(Integer, nullable=False)
    row_44: Mapped[int] = mapped_column(Integer, nullable=False)
    row_29: Mapped[int] = mapped_column(Integer, nullable=False)
    row_9: Mapped[int] = mapped_column(Integer, nullable=False)
    lane: Mapped[int] = mapped_column(Integer, nullable=False)
    row_11: Mapped[int] = mapped_column(Integer, nullable=False)
    row_46: Mapped[int] = mapped_column(Integer, nullable=False)
    row_55: Mapped[int] = mapped_column(Integer, nullable=False)
    row_32: Mapped[int] = mapped_column(Integer, nullable=False)
    row_43: Mapped[int] = mapped_column(Integer, nullable=False)
    row_47: Mapped[int] = mapped_column(Integer, nullable=False)
    row_38: Mapped[int] = mapped_column(Integer, nullable=False)
    row_6: Mapped[int] = mapped_column(Integer, nullable=False)
    row_59: Mapped[int] = mapped_column(Integer, nullable=False)
    row_60: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    row_2: Mapped[int] = mapped_column(Integer, nullable=False)
    row_31: Mapped[int] = mapped_column(Integer, nullable=False)
    row_17: Mapped[int] = mapped_column(Integer, nullable=False)
    row_20: Mapped[int] = mapped_column(Integer, nullable=False)
    row_24: Mapped[int] = mapped_column(Integer, nullable=False)
    row_26: Mapped[int] = mapped_column(Integer, nullable=False)
    row_56: Mapped[int] = mapped_column(Integer, nullable=False)
    row_21: Mapped[int] = mapped_column(Integer, nullable=False)


class NopDramaDatum(Base):
    __tablename__ = 'nop_drama_data'
    __table_args__ = (
        Index('nop_drama_data_0_stage_id', 'stage_id'),
    )

    create_front_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    talk_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    col_size_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    col_pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    create_back_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    idle_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    talk_pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    talk_pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    col_size_y: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class NopDramaScript(Base):
    __tablename__ = 'nop_drama_script'
    __table_args__ = (
        Index('nop_drama_script_0_drama_id', 'drama_id'),
    )

    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)


class NotifDatum(Base):
    __tablename__ = 'notif_data'
    __table_args__ = (
        Index('notif_data_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    notif_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)


class NydSetting(Base):
    __tablename__ = 'nyd_setting'

    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    complete_emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)


class NydStoryDatum(Base):
    __tablename__ = 'nyd_story_data'
    __table_args__ = (
        Index('nyd_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    nyd_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    is_first: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)


class NyxDramaDatum(Base):
    __tablename__ = 'nyx_drama_data'

    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_phase: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_locked_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_unlocked_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class NyxDramaScript(Base):
    __tablename__ = 'nyx_drama_script'
    __table_args__ = (
        Index('nyx_drama_script_0_drama_id', 'drama_id'),
    )

    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class NyxPhaseDatum(Base):
    __tablename__ = 'nyx_phase_data'

    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_boss: Mapped[int] = mapped_column(Integer, nullable=False)
    story_phase: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase_title: Mapped[str] = mapped_column(Text, nullable=False)


class NyxStoryDatum(Base):
    __tablename__ = 'nyx_story_data'
    __table_args__ = (
        Index('nyx_story_data_0_story_phase', 'story_phase'),
        Index('nyx_story_data_0_story_seq', 'story_seq')
    )

    story_phase: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_count: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_seq: Mapped[int] = mapped_column(Integer, nullable=False)


class NyxStoryScript(Base):
    __tablename__ = 'nyx_story_script'
    __table_args__ = (
        Index('nyx_story_script_0_story_id', 'story_id'),
    )

    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)


class ObtentContentRelation(Base):
    __tablename__ = 'obtent_content_relation'
    __table_args__ = (
        Index('obtent_content_relation_0_after_content_type_1_after_content_id', 'after_content_type', 'after_content_id'),
        Index('obtent_content_relation_0_event_id', 'event_id')
    )

    after_content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    after_content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    before_content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    before_content_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ObtentDecoList(Base):
    __tablename__ = 'obtent_deco_list'
    __table_args__ = (
        Index('obtent_deco_list_0_event_id', 'event_id'),
        Index('obtent_deco_list_0_event_id_1_parent_view_id', 'event_id', 'parent_view_id')
    )

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    effect_priority: Mapped[int] = mapped_column(Integer, nullable=False)
    object_name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_read_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_view_id: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_object_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ObtentDocument(Base):
    __tablename__ = 'obtent_document'
    __table_args__ = (
        Index('obtent_document_0_event_id_1_document_id', 'event_id', 'document_id'),
    )

    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    page_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ObtentDramaScript(Base):
    __tablename__ = 'obtent_drama_script'
    __table_args__ = (
        Index('obtent_drama_script_0_drama_id', 'drama_id'),
    )

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class ObtentNaviComment(Base):
    __tablename__ = 'obtent_navi_comment'
    __table_args__ = (
        Index('obtent_navi_comment_0_event_id', 'event_id'),
        Index('obtent_navi_comment_0_event_id_1_obtent_view_id', 'event_id', 'obtent_view_id')
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    obtent_view_id: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class ObtentObjectList(Base):
    __tablename__ = 'obtent_object_list'
    __table_args__ = (
        Index('obtent_object_list_0_condition_story_id', 'condition_story_id'),
        Index('obtent_object_list_0_event_id', 'event_id'),
        Index('obtent_object_list_0_event_id_1_parent_view_id', 'event_id', 'parent_view_id'),
        Index('obtent_object_list_0_object_story_type_1_object_story_id', 'object_story_type', 'object_story_id')
    )

    parent_view_id: Mapped[int] = mapped_column(Integer, nullable=False)
    force_move: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_caption: Mapped[str] = mapped_column(Text, nullable=False)
    parent_object_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_read_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_priority: Mapped[int] = mapped_column(Integer, nullable=False)
    object_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_name: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)


class ObtentStillList(Base):
    __tablename__ = 'obtent_still_list'
    __table_args__ = (
        Index('obtent_still_list_0_condition_story_id', 'condition_story_id'),
        Index('obtent_still_list_0_original_event_id', 'original_event_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    still_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ObtentTutorial(Base):
    __tablename__ = 'obtent_tutorial'
    __table_args__ = (
        Index('obtent_tutorial_0_event_id', 'event_id'),
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    navi_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)


class OddsNameDatum(Base):
    __tablename__ = 'odds_name_data'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    odds_file: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class OmpDrama(Base):
    __tablename__ = 'omp_drama'
    __table_args__ = (
        Index('omp_drama_0_drama_id', 'drama_id'),
    )

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class OmpStoryDatum(Base):
    __tablename__ = 'omp_story_data'
    __table_args__ = (
        Index('omp_story_data_0_event_id', 'event_id'),
        Index('omp_story_data_0_story_seq', 'story_seq')
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    story_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    is_readable_on_result: Mapped[int] = mapped_column(Integer, nullable=False)
    omp_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class ParamType(Base):
    __tablename__ = 'param_type'

    parameter_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    ratio: Mapped[int] = mapped_column(Integer, nullable=False)
    parameter_name: Mapped[str] = mapped_column(Text, nullable=False)


class PctComboCoefficient(Base):
    __tablename__ = 'pct_combo_coefficient'

    combo_min: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    combo_max: Mapped[int] = mapped_column(Integer, nullable=False)
    combo_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)


class PctEvaluation(Base):
    __tablename__ = 'pct_evaluation'

    evaluation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evaluation_point: Mapped[int] = mapped_column(Integer, nullable=False)
    meet_width: Mapped[int] = mapped_column(Integer, nullable=False)
    fever_point: Mapped[int] = mapped_column(Integer, nullable=False)


class PctGamingMotion(Base):
    __tablename__ = 'pct_gaming_motion'

    nice_count: Mapped[int] = mapped_column(Integer, nullable=False)
    perfect_count: Mapped[int] = mapped_column(Integer, nullable=False)
    motion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    good_count: Mapped[int] = mapped_column(Integer, nullable=False)
    point: Mapped[int] = mapped_column(Integer, nullable=False)


class PctItempoint(Base):
    __tablename__ = 'pct_itempoint'
    __table_args__ = (
        Index('pct_itempoint_0_item_id', 'item_id'),
    )

    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_point_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class PctResult(Base):
    __tablename__ = 'pct_result'
    __table_args__ = (
        Index('pct_result_0_character_id', 'character_id'),
    )

    score_to: Mapped[int] = mapped_column(Integer, nullable=False)
    score_from: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class PctReward(Base):
    __tablename__ = 'pct_reward'
    __table_args__ = (
        Index('pct_reward_0_pct_point_type', 'pct_point_type'),
    )

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_point_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)


class PctSystem(Base):
    __tablename__ = 'pct_system'

    chara1: Mapped[int] = mapped_column(Integer, nullable=False)
    chara2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara2_gauge_choice: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_base_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_time: Mapped[int] = mapped_column(Integer, nullable=False)
    fever_time: Mapped[int] = mapped_column(Integer, nullable=False)
    fever_revention_time: Mapped[int] = mapped_column(Integer, nullable=False)
    chara1_gauge_choice: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fever_point_max: Mapped[int] = mapped_column(Integer, nullable=False)


class PctSystemFruits(Base):
    __tablename__ = 'pct_system_fruits'

    last_time: Mapped[int] = mapped_column(Integer, nullable=False)
    appearance: Mapped[int] = mapped_column(Integer, nullable=False)
    bar_split: Mapped[int] = mapped_column(Integer, nullable=False)
    appearance_chara_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appearance_pattern: Mapped[str] = mapped_column(Text, nullable=False)
    wait_time: Mapped[int] = mapped_column(Integer, nullable=False)


class PctTapSpeed(Base):
    __tablename__ = 'pct_tap_speed'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speed_magnification: Mapped[int] = mapped_column(Integer, nullable=False)
    combo_count: Mapped[int] = mapped_column(Integer, nullable=False)


class PkbBatterCondition(Base):
    __tablename__ = 'pkb_batter_condition'

    ability_name: Mapped[str] = mapped_column(Text, nullable=False)
    meet: Mapped[int] = mapped_column(Integer, nullable=False)
    ability_detail: Mapped[str] = mapped_column(Text, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    batter_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pkb_score: Mapped[int] = mapped_column(Integer, nullable=False)
    is_playable: Mapped[int] = mapped_column(Integer, nullable=False)
    critical: Mapped[int] = mapped_column(Integer, nullable=False)


class PkbDrama(Base):
    __tablename__ = 'pkb_drama'
    __table_args__ = (
        Index('pkb_drama_0_drama_id', 'drama_id'),
    )

    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)


class PkbDramaDatum(Base):
    __tablename__ = 'pkb_drama_data'

    condition_batter_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_pitcher_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_pitcher_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_batter_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class PkbNaviComment(Base):
    __tablename__ = 'pkb_navi_comment'

    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class PkbPitcherBallType(Base):
    __tablename__ = 'pkb_pitcher_ball_type'
    __table_args__ = (
        Index('pkb_pitcher_ball_type_0_pitcher_id', 'pitcher_id'),
    )

    ball_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    ball_type_name: Mapped[str] = mapped_column(Text, nullable=False)
    pitcher_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class PkbReward(Base):
    __tablename__ = 'pkb_reward'

    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pkb_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class PositionSetting(Base):
    __tablename__ = 'position_setting'

    position_setting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    middle: Mapped[int] = mapped_column(Integer, nullable=False)
    front: Mapped[int] = mapped_column(Integer, nullable=False)


class PrequelEventStoryDatum(Base):
    __tablename__ = 'prequel_event_story_data'
    __table_args__ = (
        Index('prequel_event_story_data_0_after_story_id', 'after_story_id'),
    )

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    after_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class PrizegachaDatum(Base):
    __tablename__ = 'prizegacha_data'

    disp_prize_fixed_compensation: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_35: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_31: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_21: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_prize10: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_25: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_34: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_22: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_24: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_37: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_29: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_27: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_prize1: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_30: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_32: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_28: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_36: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_33: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_23: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_38: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_39: Mapped[int] = mapped_column(Integer, nullable=False)
    prizegacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prize_memory_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_40: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_26: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_12: Mapped[int] = mapped_column(Integer, nullable=False)


class PrizegachaSpDatum(Base):
    __tablename__ = 'prizegacha_sp_data'
    __table_args__ = (
        Index('prizegacha_sp_data_0_gacha_id', 'gacha_id'),
    )

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)


class PrizegachaSpDetail(Base):
    __tablename__ = 'prizegacha_sp_detail'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    disp_rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ProfileFrame(Base):
    __tablename__ = 'profile_frame'

    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class PromotionBonus(Base):
    __tablename__ = 'promotion_bonus'
    __table_args__ = (
        Index('promotion_bonus_0_unit_id', 'unit_id'),
    )

    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)


class PsyDrama(Base):
    __tablename__ = 'psy_drama'

    release_psy_product_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    release_psy_product_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_5: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_chara_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_total_eat: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_psy_product_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_1: Mapped[int] = mapped_column(Integer, nullable=False)


class PsyDramaScript(Base):
    __tablename__ = 'psy_drama_script'
    __table_args__ = (
        Index('psy_drama_script_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class PsyNote(Base):
    __tablename__ = 'psy_note'

    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_flavor_1: Mapped[int] = mapped_column(Integer, nullable=False)
    psy_product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    init_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_flavor_2: Mapped[int] = mapped_column(Integer, nullable=False)
    flavor_2: Mapped[str] = mapped_column(Text, nullable=False)
    flavor_1: Mapped[str] = mapped_column(Text, nullable=False)
    flavor_3: Mapped[str] = mapped_column(Text, nullable=False)
    psy_product_name: Mapped[str] = mapped_column(Text, nullable=False)


class PsyReward(Base):
    __tablename__ = 'psy_reward'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestAnnihilation(Base):
    __tablename__ = 'quest_annihilation'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_effect_position: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    se_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestAreaDatum(Base):
    __tablename__ = 'quest_area_data'
    __table_args__ = (
        Index('quest_area_data_0_map_type', 'map_type'),
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    area_display_name: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestConditionDatum(Base):
    __tablename__ = 'quest_condition_data'

    condition_quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestDatum(Base):
    __tablename__ = 'quest_data'
    __table_args__ = (
        Index('quest_data_0_area_id', 'area_id'),
    )

    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    camera_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    add_treasure_num: Mapped[int] = mapped_column(Integer, nullable=False)
    camera_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    camera_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestRewardDatum(Base):
    __tablename__ = 'quest_reward_data'

    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)


class RagDramaScript(Base):
    __tablename__ = 'rag_drama_script'
    __table_args__ = (
        Index('rag_drama_script_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)


class RagStoryDatum(Base):
    __tablename__ = 'rag_story_data'
    __table_args__ = (
        Index('rag_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class RagTopDrama(Base):
    __tablename__ = 'rag_top_drama'

    rag_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Rarity6QuestDatum(Base):
    __tablename__ = 'rarity_6_quest_data'
    __table_args__ = (
        Index('rarity_6_quest_data_0_rarity_6_quest_id', 'rarity_6_quest_id'),
    )

    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity_6_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    treasure_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)


class RecoverStamina(Base):
    __tablename__ = 'recover_stamina'

    count: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)


class RedeemStaticPriceGroup(Base):
    __tablename__ = 'redeem_static_price_group'

    condition_category: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)


class RedeemUnit(Base):
    __tablename__ = 'redeem_unit'
    __table_args__ = (
        Index('redeem_unit_0_unit_id', 'unit_id'),
    )

    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_category: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RedeemUnitBg(Base):
    __tablename__ = 'redeem_unit_bg'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ReferenceCharaTypeGroup(Base):
    __tablename__ = 'reference_chara_type_group'
    __table_args__ = (
        Index('reference_chara_type_group_0_group_id', 'group_id'),
    )

    chara_type: Mapped[int] = mapped_column(Integer, nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RelicActionExecTime(Base):
    __tablename__ = 'relic_action_exec_time'
    __table_args__ = (
        Index('relic_action_exec_time_0_action_id', 'action_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exec_time: Mapped[float] = mapped_column(REAL, nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RelicSkillExecTime(Base):
    __tablename__ = 'relic_skill_exec_time'
    __table_args__ = (
        Index('relic_skill_exec_time_0_skill_id', 'skill_id'),
    )

    exec_time: Mapped[float] = mapped_column(REAL, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ReplaceTutorialCharacter(Base):
    __tablename__ = 'replace_tutorial_character'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    navi_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    navi_position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class ResistDatum(Base):
    __tablename__ = 'resist_data'

    ailment_25: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_73: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ailment_79: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_100: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_92: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_31: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_41: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_93: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_18: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_52: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_50: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_54: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_26: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_75: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_88: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_83: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_22: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_57: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_99: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_8: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_96: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_19: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_33: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_30: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_34: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_17: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_65: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_81: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_64: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_98: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_56: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_77: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_47: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_53: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_94: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_74: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_6: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_49: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_76: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_63: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_9: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_97: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_24: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_87: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_82: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_72: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_35: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_89: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_62: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_51: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_70: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_15: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_84: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_10: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_48: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_95: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_68: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_67: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_44: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_39: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_42: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_11: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_29: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_13: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_69: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_71: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_90: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_61: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_38: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_59: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_14: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_32: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_60: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_43: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_27: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_46: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_23: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_36: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_80: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_85: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_20: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_40: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_86: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_66: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_55: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_58: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_16: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_21: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_12: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_28: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_7: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_45: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_91: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_37: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_78: Mapped[int] = mapped_column(Integer, nullable=False)


class ResistVariationDatum(Base):
    __tablename__ = 'resist_variation_data'

    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_4: Mapped[int] = mapped_column(Integer, nullable=False)


class ReturnSpecialfesBanner(Base):
    __tablename__ = 'return_specialfes_banner'

    banner_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banner_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_7: Mapped[int] = mapped_column(Integer, nullable=False)


class RewardCollectGuide(Base):
    __tablename__ = 'reward_collect_guide'

    system_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomChange(Base):
    __tablename__ = 'room_change'

    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_end: Mapped[str] = mapped_column(Text, nullable=False)
    change_start: Mapped[str] = mapped_column(Text, nullable=False)
    change_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomCharacterPersonality(Base):
    __tablename__ = 'room_character_personality'

    personality_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomCharacterSkinColor(Base):
    __tablename__ = 'room_character_skin_color'

    skin_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomChatFormation(Base):
    __tablename__ = 'room_chat_formation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_dir: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_x: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_x: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_dir: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id5: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id4: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_dir: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id4: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id2: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id1: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_dir: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id3: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id5: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id3: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id2: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_dir: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id1: Mapped[Optional[int]] = mapped_column(Integer)


class RoomChatInfo(Base):
    __tablename__ = 'room_chat_info'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    formation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scenario_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomChatScenario(Base):
    __tablename__ = 'room_chat_scenario'
    __table_args__ = (
        Index('room_chat_scenario_0_id', 'id'),
    )

    delay: Mapped[int] = mapped_column(Integer, nullable=False)
    anime_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_pos_no: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    affect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    scenario_idx: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomEffect(Base):
    __tablename__ = 'room_effect'

    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    nebbia: Mapped[int] = mapped_column(Integer, nullable=False)
    vegetable: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_get: Mapped[int] = mapped_column(Integer, nullable=False)
    arcade: Mapped[int] = mapped_column(Integer, nullable=False)
    poster: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jukebox: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomEffectRewardGet(Base):
    __tablename__ = 'room_effect_reward_get'

    interval_second: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_min_step: Mapped[str] = mapped_column(Text, nullable=False)
    stock_mid_step: Mapped[str] = mapped_column(Text, nullable=False)
    inc_step: Mapped[int] = mapped_column(Integer, nullable=False)
    max_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomEmotionIcon(Base):
    __tablename__ = 'room_emotion_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enable_tap: Mapped[int] = mapped_column(Integer, nullable=False)
    enable_auto: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomExceptUnit(Base):
    __tablename__ = 'room_except_unit'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomExclusiveCondition(Base):
    __tablename__ = 'room_exclusive_condition'
    __table_args__ = (
        Index('room_exclusive_condition_0_room_item_id', 'room_item_id'),
        Index('room_exclusive_condition_0_unit_id', 'unit_id')
    )

    room_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    notification: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomItem(Base):
    __tablename__ = 'room_item'

    max_possession_num: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_start: Mapped[str] = mapped_column(Text, nullable=False)
    category_action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_item_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_end: Mapped[str] = mapped_column(Text, nullable=False)
    sold_price: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_new_disp_end: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_open_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_open_type: Mapped[int] = mapped_column(Integer, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enable_remove: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_open_value: Mapped[int] = mapped_column(Integer, nullable=False)
    sort: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class RoomItemAnnouncement(Base):
    __tablename__ = 'room_item_announcement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    announcement_end: Mapped[str] = mapped_column(Text, nullable=False)
    announcement_start: Mapped[str] = mapped_column(Text, nullable=False)
    announcement_text: Mapped[str] = mapped_column(Text, nullable=False)


class RoomItemDetail(Base):
    __tablename__ = 'room_item_detail'
    __table_args__ = (
        Index('room_item_detail_0_lvup_trigger_type_1_lvup_trigger_id', 'lvup_trigger_type', 'lvup_trigger_id'),
        Index('room_item_detail_0_lvup_trigger_type_2_1_lvup_trigger_id_2', 'lvup_trigger_type_2', 'lvup_trigger_id_2')
    )

    lvup_trigger_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_item1_num: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_item1_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_value: Mapped[int] = mapped_column(Integer, nullable=False)
    item_detail: Mapped[str] = mapped_column(Text, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, primary_key=True)
    lvup_trigger_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_time: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomItemGetAnnouncement(Base):
    __tablename__ = 'room_item_get_announcement'

    get_date: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    room_announcement_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomReleaseDatum(Base):
    __tablename__ = 'room_release_data'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomReplaceUnit(Base):
    __tablename__ = 'room_replace_unit'
    __table_args__ = (
        Index('room_replace_unit_0_replace_unit_id', 'replace_unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    replace_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomSetup(Base):
    __tablename__ = 'room_setup'

    grid_width: Mapped[int] = mapped_column(Integer, nullable=False)
    grid_height: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomSkinColor(Base):
    __tablename__ = 'room_skin_color'

    color_red: Mapped[int] = mapped_column(Integer, nullable=False)
    skin_color_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    color_green: Mapped[int] = mapped_column(Integer, nullable=False)
    color_blue: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomUnitComments(Base):
    __tablename__ = 'room_unit_comments'
    __table_args__ = (
        Index('room_unit_comments_0_unit_id', 'unit_id'),
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    insert_word_type: Mapped[int] = mapped_column(Integer, nullable=False)
    face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trigger: Mapped[int] = mapped_column(Integer, primary_key=True)
    beloved_step: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SdNaviComment(Base):
    __tablename__ = 'sd_navi_comment'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    motion_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class SeasonPack(Base):
    __tablename__ = 'season_pack'
    __table_args__ = (
        Index('season_pack_0_mission_id', 'mission_id'),
        Index('season_pack_0_pack_type', 'pack_type')
    )

    pack_type: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gift_message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    after_text: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    receive_text: Mapped[str] = mapped_column(Text, nullable=False)
    repurchase_day: Mapped[int] = mapped_column(Integer, nullable=False)
    item_record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_rate_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonPackItem(Base):
    __tablename__ = 'season_pack_item'
    __table_args__ = (
        Index('season_pack_item_0_item_record_id', 'item_record_id'),
    )

    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    give_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonPackOverwrite(Base):
    __tablename__ = 'season_pack_overwrite'

    android_url: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    season_pack_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ios_url: Mapped[str] = mapped_column(Text, nullable=False)
    dmm_url: Mapped[str] = mapped_column(Text, nullable=False)
    shop_category: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonpassFoundation(Base):
    __tablename__ = 'seasonpass_foundation'

    level_max: Mapped[int] = mapped_column(Integer, nullable=False)
    point_change_type: Mapped[int] = mapped_column(Integer, nullable=False)
    advance_jewel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    per_level_point: Mapped[int] = mapped_column(Integer, nullable=False)
    level_price: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    weekly_point: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    final_jewel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    key_jewel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    help_url: Mapped[int] = mapped_column(Integer, nullable=False)
    proportion: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    extra_level: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SeasonpassLevelReward(Base):
    __tablename__ = 'seasonpass_level_reward'
    __table_args__ = (
        Index('seasonpass_level_reward_0_event_id', 'event_id'),
    )

    charge_reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    free_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    charge_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    charge_reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    degree: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    free_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    free_reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonpassMissionDatum(Base):
    __tablename__ = 'seasonpass_mission_data'

    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    seasonpass_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class SeasonpassMissionRewardDatum(Base):
    __tablename__ = 'seasonpass_mission_reward_data'
    __table_args__ = (
        Index('seasonpass_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class SecretDungeonEmblemMission(Base):
    __tablename__ = 'secret_dungeon_emblem_mission'

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[str] = mapped_column(Text, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SecretDungeonEmblemReward(Base):
    __tablename__ = 'secret_dungeon_emblem_reward'
    __table_args__ = (
        Index('secret_dungeon_emblem_reward_0_mission_reward_id', 'mission_reward_id'),
        Index('secret_dungeon_emblem_reward_0_reward_id', 'reward_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)


class SecretDungeonEnemyInfo(Base):
    __tablename__ = 'secret_dungeon_enemy_info'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_name: Mapped[str] = mapped_column(Text, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, primary_key=True)


class SecretDungeonFloorReward(Base):
    __tablename__ = 'secret_dungeon_floor_reward'
    __table_args__ = (
        Index('secret_dungeon_floor_reward_0_dungeon_area_id', 'dungeon_area_id'),
    )

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_effect_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_count: Mapped[int] = mapped_column(Integer, primary_key=True)


class SecretDungeonFloorSetting(Base):
    __tablename__ = 'secret_dungeon_floor_setting'
    __table_args__ = (
        Index('secret_dungeon_floor_setting_0_quest_id', 'quest_id'),
        Index('secret_dungeon_floor_setting_0_quest_id_1_mode', 'quest_id', 'mode')
    )

    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    floor_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    floor_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_identify: Mapped[int] = mapped_column(Integer, nullable=False)


class SecretDungeonQuestDatum(Base):
    __tablename__ = 'secret_dungeon_quest_data'
    __table_args__ = (
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_difficulty', 'dungeon_area_id', 'difficulty'),
        Index('secret_dungeon_quest_data_0_dungeon_area_id_1_floor_num', 'dungeon_area_id', 'floor_num')
    )

    reward_image_6: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_monster_scale_4: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_monster_scale_5: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reset_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_2: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_4: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_height: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    emax: Mapped[int] = mapped_column(Integer, nullable=False)
    fixed_start_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_5: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_monster_scale_3: Mapped[float] = mapped_column(REAL, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    multi_target_effect_time: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_3: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_scale_2: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_type: Mapped[int] = mapped_column(Integer, nullable=False)


class SecretDungeonSchedule(Base):
    __tablename__ = 'secret_dungeon_schedule'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class SekaiAddTimesDatum(Base):
    __tablename__ = 'sekai_add_times_data'

    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiBossDamageRankReward(Base):
    __tablename__ = 'sekai_boss_damage_rank_reward'

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiBossFixReward(Base):
    __tablename__ = 'sekai_boss_fix_reward'

    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_total_damage: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiBossMode(Base):
    __tablename__ = 'sekai_boss_mode'

    sekai_enemy_level: Mapped[str] = mapped_column(Text, nullable=False)
    score_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_boss_mode_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)


class SekaiEnemyParameter(Base):
    __tablename__ = 'sekai_enemy_parameter'

    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[str] = mapped_column(Text, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiSchedule(Base):
    __tablename__ = 'sekai_schedule'

    result_end: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    damage_rank_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_losstime: Mapped[str] = mapped_column(Text, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    last_sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class SekaiTopDatum(Base):
    __tablename__ = 'sekai_top_data'
    __table_args__ = (
        Index('sekai_top_data_0_sekai_id', 'sekai_id'),
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    boss_hp_from: Mapped[str] = mapped_column(Text, nullable=False)
    boss_time_from: Mapped[str] = mapped_column(Text, nullable=False)
    scale_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_time_to: Mapped[str] = mapped_column(Text, nullable=False)
    sekai_boss_mode_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    top_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_hp_to: Mapped[str] = mapped_column(Text, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    boss_mode: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiTopStoryDatum(Base):
    __tablename__ = 'sekai_top_story_data'
    __table_args__ = (
        Index('sekai_top_story_data_0_sekai_id', 'sekai_id'),
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_time_from: Mapped[str] = mapped_column(Text, nullable=False)
    boss_time_to: Mapped[str] = mapped_column(Text, nullable=False)


class SekaiUnlockStoryCondition(Base):
    __tablename__ = 'sekai_unlock_story_condition'

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_entry: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_fix_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SelectionTicketDatum(Base):
    __tablename__ = 'selection_ticket_data'
    __table_args__ = (
        Index('selection_ticket_data_0_exchange_number', 'exchange_number'),
        Index('selection_ticket_data_0_ticket_id', 'ticket_id')
    )

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SerialCodeDatum(Base):
    __tablename__ = 'serial_code_data'

    campaign_name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    serial_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SerialGroupDatum(Base):
    __tablename__ = 'serial_group_data'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    serial_campaign_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_name: Mapped[str] = mapped_column(Text, nullable=False)
    serial_campaign_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    serial_campaign_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SeriesUnlockCondition(Base):
    __tablename__ = 'series_unlock_condition'

    condition_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sequel_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenBgDatum(Base):
    __tablename__ = 'seven_bg_data'
    __table_args__ = (
        Index('seven_bg_data_0_event_id_1_type', 'event_id', 'type'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenBossDatum(Base):
    __tablename__ = 'seven_boss_data'
    __table_args__ = (
        Index('seven_boss_data_0_event_id', 'event_id'),
        Index('seven_boss_data_0_event_id_1_difficulty', 'event_id', 'difficulty')
    )

    battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)


class SevenBossEnemySetting(Base):
    __tablename__ = 'seven_boss_enemy_setting'

    must_kill_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_point: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    result_boss_height: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_size: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_identify: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_height: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_position: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenBossExtraEffect(Base):
    __tablename__ = 'seven_boss_extra_effect'
    __table_args__ = (
        Index('seven_boss_extra_effect_0_quest_id', 'quest_id'),
    )

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SevenClearReward(Base):
    __tablename__ = 'seven_clear_reward'

    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenCommonMissionDatum(Base):
    __tablename__ = 'seven_common_mission_data'
    __table_args__ = (
        Index('seven_common_mission_data_0_mission_group_id_1_mission_type', 'mission_group_id', 'mission_type'),
        Index('seven_common_mission_data_0_mission_id', 'mission_id')
    )

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    revival_type: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    destination_system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value: Mapped[Optional[int]] = mapped_column(Integer)


class SevenContentsCondition(Base):
    __tablename__ = 'seven_contents_condition'
    __table_args__ = (
        Index('seven_contents_condition_0_contents_type', 'contents_type'),
        Index('seven_contents_condition_0_event_id', 'event_id')
    )

    contents_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest: Mapped[int] = mapped_column(Integer, nullable=False)
    contents_name: Mapped[str] = mapped_column(Text, nullable=False)


class SevenDearChara(Base):
    __tablename__ = 'seven_dear_chara'
    __table_args__ = (
        Index('seven_dear_chara_0_event_id', 'event_id'),
        Index('seven_dear_chara_0_event_id_1_reference_id', 'event_id', 'reference_id')
    )

    chara_name: Mapped[str] = mapped_column(Text, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    episode_unlock_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point_up_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dear_point_up_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_type: Mapped[int] = mapped_column(Integer, nullable=False)
    max_dear_point: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    episode_unlock_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenDearPointReward(Base):
    __tablename__ = 'seven_dear_point_reward'
    __table_args__ = (
        Index('seven_dear_point_reward_0_event_id_1_chara_index', 'event_id', 'chara_index'),
    )

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenDearStoryDetail(Base):
    __tablename__ = 'seven_dear_story_detail'
    __table_args__ = (
        Index('seven_dear_story_detail_0_chara_index', 'chara_index'),
    )

    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point_3: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dear_point_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenEffectSetting(Base):
    __tablename__ = 'seven_effect_setting'

    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SevenEnemyParameter(Base):
    __tablename__ = 'seven_enemy_parameter'

    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenEventAdv(Base):
    __tablename__ = 'seven_event_adv'
    __table_args__ = (
        Index('seven_event_adv_0_event_id', 'event_id'),
        Index('seven_event_adv_0_event_id_1_type', 'event_id', 'type'),
        Index('seven_event_adv_0_story_id', 'story_id')
    )

    event_adv_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenEventSetting(Base):
    __tablename__ = 'seven_event_setting'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    quest_featured_item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_featured_item_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    banner_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_featured_item_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_featured_item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    sp_plus_limit_challenge_count: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_featured_item_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_featured_item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenGachaDatum(Base):
    __tablename__ = 'seven_gacha_data'

    reset_item_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    box_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SevenLimitChara(Base):
    __tablename__ = 'seven_limit_chara'

    limit_chara_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_chara_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_chara_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenNaviComment(Base):
    __tablename__ = 'seven_navi_comment'

    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class SevenQuestDatum(Base):
    __tablename__ = 'seven_quest_data'
    __table_args__ = (
        Index('seven_quest_data_0_event_id', 'event_id'),
    )

    battle_bg_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_index: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_bg_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    first_clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_bg_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenScenarioSupport(Base):
    __tablename__ = 'seven_scenario_support'
    __table_args__ = (
        Index('seven_scenario_support_0_event_id', 'event_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class SevenSchedule(Base):
    __tablename__ = 'seven_schedule'
    __table_args__ = (
        Index('seven_schedule_0_event_id', 'event_id'),
    )

    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class SevenSpecialBattleDetail(Base):
    __tablename__ = 'seven_special_battle_detail'
    __table_args__ = (
        Index('seven_special_battle_detail_0_quest_id', 'quest_id'),
    )

    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[float] = mapped_column(REAL, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    mode_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mode_end_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenStoryDatum(Base):
    __tablename__ = 'seven_story_data'
    __table_args__ = (
        Index('seven_story_data_0_event_id', 'event_id'),
        Index('seven_story_data_0_event_id_1_contents_type', 'event_id', 'contents_type'),
        Index('seven_story_data_0_event_id_1_story_index', 'event_id', 'story_index'),
        Index('seven_story_data_0_event_id_1_story_type', 'event_id', 'story_type')
    )

    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_type: Mapped[int] = mapped_column(Integer, nullable=False)
    direction_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_index: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class SevenTutorialDatum(Base):
    __tablename__ = 'seven_tutorial_data'
    __table_args__ = (
        Index('seven_tutorial_data_0_event_type_1_tutorial_type', 'event_type', 'tutorial_type'),
    )

    tutorial_image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tutorial_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_text: Mapped[str] = mapped_column(Text, nullable=False)


class SevenUniqueMissionDatum(Base):
    __tablename__ = 'seven_unique_mission_data'
    __table_args__ = (
        Index('seven_unique_mission_data_0_event_id', 'event_id'),
        Index('seven_unique_mission_data_0_event_id_1_mission_type', 'event_id', 'mission_type')
    )

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    revival_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    destination_system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value: Mapped[Optional[int]] = mapped_column(Integer)


class SevenWaveGroupDatum(Base):
    __tablename__ = 'seven_wave_group_data'

    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriBattleMissionDatum(Base):
    __tablename__ = 'shiori_battle_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriBoss(Base):
    __tablename__ = 'shiori_boss'
    __table_args__ = (
        Index('shiori_boss_0_event_id', 'event_id'),
        Index('shiori_boss_0_event_id_1_difficulty', 'event_id', 'difficulty'),
        Index('shiori_boss_0_wave_group_id_1', 'wave_group_id_1')
    )

    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    map_arrow_offset: Mapped[float] = mapped_column(REAL, nullable=False)
    map_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    qd_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_on_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    deatail_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    td_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    map_size: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    icon_collider_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    icon_display_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriBossCondition(Base):
    __tablename__ = 'shiori_boss_condition'

    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriDescription(Base):
    __tablename__ = 'shiori_description'
    __table_args__ = (
        Index('shiori_description_0_type', 'type'),
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriEnemyParameter(Base):
    __tablename__ = 'shiori_enemy_parameter'

    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriEventList(Base):
    __tablename__ = 'shiori_event_list'
    __table_args__ = (
        Index('shiori_event_list_0_original_event_id', 'original_event_id'),
        Index('shiori_event_list_0_series_event_id', 'series_event_id')
    )

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    banner_y: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_chara_id: Mapped[int] = mapped_column(Integer, nullable=False)
    series_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    help_index: Mapped[str] = mapped_column(Text, nullable=False)
    condition_shiori_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriItem(Base):
    __tablename__ = 'shiori_item'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_material_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriMissionRewardDatum(Base):
    __tablename__ = 'shiori_mission_reward_data'
    __table_args__ = (
        Index('shiori_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriQuest(Base):
    __tablename__ = 'shiori_quest'
    __table_args__ = (
        Index('shiori_quest_0_drop_reward_id', 'drop_reward_id'),
        Index('shiori_quest_0_event_id', 'event_id')
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_offset_y: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriQuestArea(Base):
    __tablename__ = 'shiori_quest_area'
    __table_args__ = (
        Index('shiori_quest_area_0_event_id', 'event_id'),
    )

    scroll_height: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_param_1: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    open_tutorial_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    area_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_width: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_param_2: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)


class ShioriQuestCondition(Base):
    __tablename__ = 'shiori_quest_condition'

    condition_main_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriStationaryMissionDatum(Base):
    __tablename__ = 'shiori_stationary_mission_data'

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriUnlockUnitCondition(Base):
    __tablename__ = 'shiori_unlock_unit_condition'
    __table_args__ = (
        Index('shiori_unlock_unit_condition_0_condition_mission_id', 'condition_mission_id'),
        Index('shiori_unlock_unit_condition_0_unit_id_1_event_id', 'unit_id', 'event_id')
    )

    description_1: Mapped[str] = mapped_column(Text, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description_2: Mapped[str] = mapped_column(Text, nullable=False)
    top_description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriWaveGroupDatum(Base):
    __tablename__ = 'shiori_wave_group_data'

    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class ShopItemDescription(Base):
    __tablename__ = 'shop_item_description'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class ShopStaticPriceGroup(Base):
    __tablename__ = 'shop_static_price_group'

    buy_count_to: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    price_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buy_count_from: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrChara(Base):
    __tablename__ = 'sjr_chara'

    spring: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tp_length: Mapped[float] = mapped_column(REAL, nullable=False)
    personality: Mapped[int] = mapped_column(Integer, nullable=False)
    proper_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sjr_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ub_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tired_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrCourse(Base):
    __tablename__ = 'sjr_course'

    peek_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[float] = mapped_column(REAL, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    feature: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrDramaScript(Base):
    __tablename__ = 'sjr_drama_script'
    __table_args__ = (
        Index('sjr_drama_script_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class SjrEmblem(Base):
    __tablename__ = 'sjr_emblem'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrFeatureGroup(Base):
    __tablename__ = 'sjr_feature_group'

    feature_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrNameFormer(Base):
    __tablename__ = 'sjr_name_former'

    condition_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    constrain_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrNameLater(Base):
    __tablename__ = 'sjr_name_later'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score_to: Mapped[int] = mapped_column(Integer, nullable=False)
    name_group: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    score_from: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrNpcActionOdds(Base):
    __tablename__ = 'sjr_npc_action_odds'
    __table_args__ = (
        Index('sjr_npc_action_odds_0_action_odds_id', 'action_odds_id'),
    )

    angle: Mapped[int] = mapped_column(Integer, nullable=False)
    distance: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_odds_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rate: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrParameterEvaluation(Base):
    __tablename__ = 'sjr_parameter_evaluation'

    border_1: Mapped[float] = mapped_column(REAL, nullable=False)
    border_2: Mapped[float] = mapped_column(REAL, nullable=False)
    border_3: Mapped[float] = mapped_column(REAL, nullable=False)
    parameter_type: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrProperEvaluation(Base):
    __tablename__ = 'sjr_proper_evaluation'

    border_2: Mapped[int] = mapped_column(Integer, nullable=False)
    border_1: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrProperFeature(Base):
    __tablename__ = 'sjr_proper_feature'

    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    feature_group_2: Mapped[int] = mapped_column(Integer, nullable=False)
    feature_group_1: Mapped[int] = mapped_column(Integer, nullable=False)
    proper_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feature_group_3: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrRail(Base):
    __tablename__ = 'sjr_rail'
    __table_args__ = (
        Index('sjr_rail_0_rail_id', 'rail_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gimmick_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrReward(Base):
    __tablename__ = 'sjr_reward'

    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sjr_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)


class SjrScore(Base):
    __tablename__ = 'sjr_score'

    third_score: Mapped[int] = mapped_column(Integer, nullable=False)
    round: Mapped[int] = mapped_column(Integer, primary_key=True)
    extra_bonus: Mapped[float] = mapped_column(REAL, nullable=False)
    hard_bonus: Mapped[float] = mapped_column(REAL, nullable=False)
    action_score: Mapped[int] = mapped_column(Integer, nullable=False)
    first_score: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_bonus: Mapped[float] = mapped_column(REAL, nullable=False)
    time_score: Mapped[int] = mapped_column(Integer, nullable=False)
    second_score: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrUbDatum(Base):
    __tablename__ = 'sjr_ub_data'

    in_game_description: Mapped[str] = mapped_column(Text, nullable=False)
    ub_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ub_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    top_description: Mapped[str] = mapped_column(Text, nullable=False)
    ub_type: Mapped[int] = mapped_column(Integer, nullable=False)


class SkeStoryDatum(Base):
    __tablename__ = 'ske_story_data'
    __table_args__ = (
        Index('ske_story_data_0_original_event_id', 'original_event_id'),
    )

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_event_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class SkeStoryScript(Base):
    __tablename__ = 'ske_story_script'
    __table_args__ = (
        Index('ske_story_script_0_story_id', 'story_id'),
    )

    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class SkillAction(Base):
    __tablename__ = 'skill_action'

    action_value_7: Mapped[float] = mapped_column(REAL, nullable=False)
    action_value_6: Mapped[float] = mapped_column(REAL, nullable=False)
    action_detail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    action_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    target_count: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_2: Mapped[float] = mapped_column(REAL, nullable=False)
    action_detail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    level_up_disp: Mapped[str] = mapped_column(Text, nullable=False)
    action_value_5: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_assignment: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_1: Mapped[float] = mapped_column(REAL, nullable=False)
    target_number: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_3: Mapped[float] = mapped_column(REAL, nullable=False)
    target_range: Mapped[int] = mapped_column(Integer, nullable=False)
    target_area: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_4: Mapped[float] = mapped_column(REAL, nullable=False)


class SkillCost(Base):
    __tablename__ = 'skill_cost'

    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    target_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class SkillDatum(Base):
    __tablename__ = 'skill_data'

    action_10: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_1: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_6: Mapped[int] = mapped_column(Integer, nullable=False)
    action_5: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_area_width: Mapped[int] = mapped_column(Integer, nullable=False)
    action_8: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_type: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_4: Mapped[int] = mapped_column(Integer, nullable=False)
    action_6: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_cast_time: Mapped[float] = mapped_column(REAL, nullable=False)
    action_4: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_7: Mapped[int] = mapped_column(Integer, nullable=False)
    action_3: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_9: Mapped[int] = mapped_column(Integer, nullable=False)
    action_7: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_ub_cool_time: Mapped[float] = mapped_column(REAL, nullable=False)
    depend_action_10: Mapped[int] = mapped_column(Integer, nullable=False)
    action_2: Mapped[int] = mapped_column(Integer, nullable=False)
    action_9: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_3: Mapped[int] = mapped_column(Integer, nullable=False)
    action_1: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    depend_action_8: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_2: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_5: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text)


class SkipBossDatum(Base):
    __tablename__ = 'skip_boss_data'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_motion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)


class SkipMonsterDatum(Base):
    __tablename__ = 'skip_monster_data'

    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    bg_skip_id: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SpBattleVoice(Base):
    __tablename__ = 'sp_battle_voice'
    __table_args__ = (
        Index('sp_battle_voice_0_unit_id', 'unit_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class SpDetailVoice(Base):
    __tablename__ = 'sp_detail_voice'

    cue_name_2: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_1: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_3: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_5: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_4: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SpLoseVoice(Base):
    __tablename__ = 'sp_lose_voice'

    unit_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_only_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speaker_unit_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)


class SpLoseVoiceGroup(Base):
    __tablename__ = 'sp_lose_voice_group'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speaker_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SpaceBattleDatum(Base):
    __tablename__ = 'space_battle_data'

    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    space_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    space_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)


class SpaceSchedule(Base):
    __tablename__ = 'space_schedule'

    sid: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    space_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class SpaceTopDatum(Base):
    __tablename__ = 'space_top_data'
    __table_args__ = (
        Index('space_top_data_0_space_id', 'space_id'),
        Index('space_top_data_0_story_id', 'story_id')
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)
    part_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    time_from: Mapped[str] = mapped_column(Text, nullable=False)
    time_to: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    space_id: Mapped[int] = mapped_column(Integer, nullable=False)
    space_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_battle_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SpecialStill(Base):
    __tablename__ = 'special_still'

    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    back_momory_type: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class SpecialStoryBanner(Base):
    __tablename__ = 'special_story_banner'
    __table_args__ = (
        Index('special_story_banner_0_story_group_id', 'story_group_id'),
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    remind_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class SpecialfesBanner(Base):
    __tablename__ = 'specialfes_banner'

    banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banner_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class SpotDramaScriptDatum(Base):
    __tablename__ = 'spot_drama_script_data'
    __table_args__ = (
        Index('spot_drama_script_data_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class SpskillLabelDatum(Base):
    __tablename__ = 'spskill_label_data'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normal_label_text: Mapped[str] = mapped_column(Text, nullable=False)
    sp_label_text: Mapped[str] = mapped_column(Text, nullable=False)


class SpskillLvInitializeDatum(Base):
    __tablename__ = 'spskill_lv_initialize_data'

    base_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    initialize_skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreAddTimesDatum(Base):
    __tablename__ = 'sre_add_times_data'
    __table_args__ = (
        Index('sre_add_times_data_0_sre_id', 'sre_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)


class SreBattleBonus(Base):
    __tablename__ = 'sre_battle_bonus'
    __table_args__ = (
        Index('sre_battle_bonus_0_sre_id_1_sre_boss_id', 'sre_id', 'sre_boss_id'),
        Index('sre_battle_bonus_0_sre_id_1_type', 'sre_id', 'type'),
        Index('sre_battle_bonus_0_type', 'type'),
        Index('sre_battle_bonus_0_type_1_sre_boss_id', 'type', 'sre_boss_id')
    )

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_battle_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    battle_bonus_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_hp: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_battle_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)


class SreBattleBonusEffect(Base):
    __tablename__ = 'sre_battle_bonus_effect'

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    text_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreBossDatum(Base):
    __tablename__ = 'sre_boss_data'
    __table_args__ = (
        Index('sre_boss_data_0_sre_id', 'sre_id'),
        Index('sre_boss_data_0_sre_id_1_phase', 'sre_id', 'phase')
    )

    result_boss_position_y_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_5: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    all_disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    lane_priority_5: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    max_raid_hp: Mapped[str] = mapped_column(Text, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_3: Mapped[float] = mapped_column(REAL, nullable=False)
    deck_number: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_3: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    expel_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_max: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    battle_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    challenge_odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)


class SreEffect(Base):
    __tablename__ = 'sre_effect'

    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_3: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SreEffectiveUnit(Base):
    __tablename__ = 'sre_effective_unit'
    __table_args__ = (
        Index('sre_effective_unit_0_sre_boss_id_1_sre_id', 'sre_boss_id', 'sre_id'),
    )

    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    support_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SreEnemyParameter(Base):
    __tablename__ = 'sre_enemy_parameter'

    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)


class SreExterminationReward(Base):
    __tablename__ = 'sre_extermination_reward'

    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class SreMissionCategoryDatum(Base):
    __tablename__ = 'sre_mission_category_data'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreMissionDatum(Base):
    __tablename__ = 'sre_mission_data'
    __table_args__ = (
        Index('sre_mission_data_0_sre_id', 'sre_id'),
        Index('sre_mission_data_0_sre_id_1_category_id', 'sre_id', 'category_id')
    )

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreMissionRewardDatum(Base):
    __tablename__ = 'sre_mission_reward_data'
    __table_args__ = (
        Index('sre_mission_reward_data_0_mission_reward_id', 'mission_reward_id'),
    )

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class SreQuestDifficultyDatum(Base):
    __tablename__ = 'sre_quest_difficulty_data'

    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SreSchedule(Base):
    __tablename__ = 'sre_schedule'
    __table_args__ = (
        Index('sre_schedule_0_close_story_condition_id', 'close_story_condition_id'),
    )

    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bg: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SreWaveGroupDatum(Base):
    __tablename__ = 'sre_wave_group_data'
    __table_args__ = (
        Index('sre_wave_group_data_0_wave_group_id', 'wave_group_id'),
    )

    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class SrtAction(Base):
    __tablename__ = 'srt_action'

    voice_list: Mapped[str] = mapped_column(Text, nullable=False)
    dragon_action: Mapped[str] = mapped_column(Text, nullable=False)
    talk_text: Mapped[str] = mapped_column(Text, nullable=False)
    inori_action: Mapped[str] = mapped_column(Text, nullable=False)
    action_name: Mapped[str] = mapped_column(Text, primary_key=True)
    homare_action: Mapped[str] = mapped_column(Text, nullable=False)
    talk_text_type: Mapped[int] = mapped_column(Integer, nullable=False)
    kaya_action: Mapped[str] = mapped_column(Text, nullable=False)


class SrtPanel(Base):
    __tablename__ = 'srt_panel'
    __table_args__ = (
        Index('srt_panel_0_panel_id', 'panel_id'),
        Index('srt_panel_0_version', 'version')
    )

    reading: Mapped[str] = mapped_column(Text, nullable=False)
    detail_text: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    reading_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    head_symbol: Mapped[str] = mapped_column(Text, nullable=False)
    read_type: Mapped[int] = mapped_column(Integer, nullable=False)
    panel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tail_symbol: Mapped[str] = mapped_column(Text, nullable=False)


class SrtReward(Base):
    __tablename__ = 'srt_reward'

    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    srt_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class SrtScore(Base):
    __tablename__ = 'srt_score'

    coefficient_count_priconne_panel: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_read_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_fever: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_read_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_read_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class SrtTopTalk(Base):
    __tablename__ = 'srt_top_talk'
    __table_args__ = (
        Index('srt_top_talk_0_talk_id', 'talk_id'),
    )

    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    talk_text: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    direction: Mapped[int] = mapped_column(Integer, nullable=False)
    talk_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SspStoryDatum(Base):
    __tablename__ = 'ssp_story_data'
    __table_args__ = (
        Index('ssp_story_data_0_contents_type', 'contents_type'),
        Index('ssp_story_data_0_original_event_id', 'original_event_id')
    )

    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Stamp(Base):
    __tablename__ = 'stamp'

    stamp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class StationaryMissionDatum(Base):
    __tablename__ = 'stationary_mission_data'

    title_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)


class Still(Base):
    __tablename__ = 'still'
    __table_args__ = (
        Index('still_0_still_group_id', 'still_group_id'),
        Index('still_0_story_id', 'story_id')
    )

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_direction: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    still_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    my_page_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    facial_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    vertical_still_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    album_ignore: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class StoryBulkSkip(Base):
    __tablename__ = 'story_bulk_skip'

    release_level: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_from: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    button_sprite_name: Mapped[str] = mapped_column(Text, nullable=False)
    balloon_sprite_name: Mapped[str] = mapped_column(Text, nullable=False)
    bulk_skip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_sprite_name: Mapped[str] = mapped_column(Text, nullable=False)


class StoryCharacterMask(Base):
    __tablename__ = 'story_character_mask'

    softness: Mapped[float] = mapped_column(REAL, nullable=False)
    offset: Mapped[float] = mapped_column(REAL, nullable=False)
    chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    size: Mapped[float] = mapped_column(REAL, nullable=False)


class StoryDatum(Base):
    __tablename__ = 'story_data'

    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_free_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)


class StoryDetail(Base):
    __tablename__ = 'story_detail'
    __table_args__ = (
        Index('story_detail_0_pre_story_id', 'pre_story_id'),
        Index('story_detail_0_story_group_id_1_pre_story_id', 'story_group_id', 'pre_story_id'),
        Index('story_detail_0_unlock_quest_id', 'unlock_quest_id'),
        Index('story_detail_0_visible_type', 'visible_type')
    )

    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    force_unlock_time: Mapped[str] = mapped_column(Text, nullable=False)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    read_process_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    force_unlock_time_2: Mapped[str] = mapped_column(Text, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class StoryFbsTop(Base):
    __tablename__ = 'story_fbs_top'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time_max: Mapped[str] = mapped_column(Text, nullable=False)
    start_time_min: Mapped[str] = mapped_column(Text, nullable=False)
    is_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)


class StoryQuestDatum(Base):
    __tablename__ = 'story_quest_data'

    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_unit_4: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    guest_unit_5: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_unit_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_unit_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    guest_unit_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)


class SvdDramaScript(Base):
    __tablename__ = 'svd_drama_script'
    __table_args__ = (
        Index('svd_drama_script_0_drama_id', 'drama_id'),
    )

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class SvdStoryDatum(Base):
    __tablename__ = 'svd_story_data'
    __table_args__ = (
        Index('svd_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SvdStoryScript(Base):
    __tablename__ = 'svd_story_script'
    __table_args__ = (
        Index('svd_story_script_0_story_id', 'story_id'),
    )

    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)


class Talent(Base):
    __tablename__ = 'talent'

    talent_name: Mapped[str] = mapped_column(Text, nullable=False)
    talent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_color: Mapped[str] = mapped_column(Text, nullable=False)


class TalentFormationBonus(Base):
    __tablename__ = 'talent_formation_bonus'

    talent_bonus_5: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_bonus_4: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_1: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_3: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentFormationOverwrite(Base):
    __tablename__ = 'talent_formation_overwrite'
    __table_args__ = (
        Index('talent_formation_overwrite_0_content_type_1_target_value_1', 'content_type', 'target_value_1'),
    )

    target_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    target_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentLevelMaterial(Base):
    __tablename__ = 'talent_level_material'
    __table_args__ = (
        Index('talent_level_material_0_talent_id', 'talent_id'),
    )

    idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestAreaDatum(Base):
    __tablename__ = 'talent_quest_area_data'
    __table_args__ = (
        Index('talent_quest_area_data_0_talent_id', 'talent_id'),
    )

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_display_name: Mapped[str] = mapped_column(Text, nullable=False)


class TalentQuestBattleEffect(Base):
    __tablename__ = 'talent_quest_battle_effect'
    __table_args__ = (
        Index('talent_quest_battle_effect_0_quest_id', 'quest_id'),
    )

    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestBattleQuestDatum(Base):
    __tablename__ = 'talent_quest_battle_quest_data'

    detail_enemy_local_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_enemy_local_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    area_map_boss_icon_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_enemy_local_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    area_map_boss_icon_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    area_map_boss_icon_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_map_boss_icon_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward01(Base):
    __tablename__ = 'talent_quest_clear_reward01'
    __table_args__ = (
        Index('talent_quest_clear_reward01_0_reward_group_id', 'reward_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward02(Base):
    __tablename__ = 'talent_quest_clear_reward02'
    __table_args__ = (
        Index('talent_quest_clear_reward02_0_reward_group_id', 'reward_group_id'),
    )

    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward03(Base):
    __tablename__ = 'talent_quest_clear_reward03'
    __table_args__ = (
        Index('talent_quest_clear_reward03_0_reward_group_id', 'reward_group_id'),
    )

    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward04(Base):
    __tablename__ = 'talent_quest_clear_reward04'
    __table_args__ = (
        Index('talent_quest_clear_reward04_0_reward_group_id', 'reward_group_id'),
    )

    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward05(Base):
    __tablename__ = 'talent_quest_clear_reward05'
    __table_args__ = (
        Index('talent_quest_clear_reward05_0_reward_group_id', 'reward_group_id'),
    )

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestConditionDatum(Base):
    __tablename__ = 'talent_quest_condition_data'

    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_talent_skill_page: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus01(Base):
    __tablename__ = 'talent_quest_daily_bonus01'
    __table_args__ = (
        Index('talent_quest_daily_bonus01_0_reward_group_id', 'reward_group_id'),
    )

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus02(Base):
    __tablename__ = 'talent_quest_daily_bonus02'
    __table_args__ = (
        Index('talent_quest_daily_bonus02_0_reward_group_id', 'reward_group_id'),
    )

    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus03(Base):
    __tablename__ = 'talent_quest_daily_bonus03'
    __table_args__ = (
        Index('talent_quest_daily_bonus03_0_reward_group_id', 'reward_group_id'),
    )

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus04(Base):
    __tablename__ = 'talent_quest_daily_bonus04'
    __table_args__ = (
        Index('talent_quest_daily_bonus04_0_reward_group_id', 'reward_group_id'),
    )

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus05(Base):
    __tablename__ = 'talent_quest_daily_bonus05'
    __table_args__ = (
        Index('talent_quest_daily_bonus05_0_reward_group_id', 'reward_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDatum(Base):
    __tablename__ = 'talent_quest_data'
    __table_args__ = (
        Index('talent_quest_data_0_area_id', 'area_id'),
    )

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_bonus_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_knight_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestEnemyParameter(Base):
    __tablename__ = 'talent_quest_enemy_parameter'

    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestWaveGroupDatum(Base):
    __tablename__ = 'talent_quest_wave_group_data'
    __table_args__ = (
        Index('talent_quest_wave_group_data_0_wave_group_id', 'wave_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillEnhanceDatum(Base):
    __tablename__ = 'talent_skill_enhance_data'

    parameter_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_value: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillEnhanceLevel(Base):
    __tablename__ = 'talent_skill_enhance_level'

    enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillNode(Base):
    __tablename__ = 'talent_skill_node'
    __table_args__ = (
        Index('talent_skill_node_0_page_num', 'page_num'),
    )

    enhance_level_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_5: Mapped[int] = mapped_column(Integer, nullable=False)
    title_id: Mapped[int] = mapped_column(Integer, nullable=False)
    page_num: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_1: Mapped[int] = mapped_column(Integer, nullable=False)
    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TalentSkillTitle(Base):
    __tablename__ = 'talent_skill_title'

    title_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_text: Mapped[str] = mapped_column(Text, nullable=False)


class TalentWeakness(Base):
    __tablename__ = 'talent_weakness'

    talent_1: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_2: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_3: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_4: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_5: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqCompletionRewards(Base):
    __tablename__ = 'taq_completion_rewards'

    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TaqDatum(Base):
    __tablename__ = 'taq_data'

    char_no_5: Mapped[int] = mapped_column(Integer, nullable=False)
    taq_type: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    char_no_1: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[int] = mapped_column(Integer, nullable=False)
    word: Mapped[str] = mapped_column(Text, nullable=False)
    input_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    assist_detail: Mapped[str] = mapped_column(Text, nullable=False)
    char_no_4: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    chunk: Mapped[str] = mapped_column(Text, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    char_no_3: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_2: Mapped[str] = mapped_column(Text, nullable=False)
    char_no_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqDramaScript(Base):
    __tablename__ = 'taq_drama_script'
    __table_args__ = (
        Index('taq_drama_script_0_drama_id', 'drama_id'),
    )

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)


class TaqGameSetting(Base):
    __tablename__ = 'taq_game_setting'

    lottery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    help_use_count_veryhard: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    help_use_count_hard: Mapped[int] = mapped_column(Integer, nullable=False)
    help_use_count_normal: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqGenre(Base):
    __tablename__ = 'taq_genre'

    genre_name: Mapped[str] = mapped_column(Text, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TaqGoodUnit(Base):
    __tablename__ = 'taq_good_unit'

    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqIncorrectWord(Base):
    __tablename__ = 'taq_incorrect_word'

    word_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incorrect_word: Mapped[str] = mapped_column(Text, nullable=False)


class TaqKanjiList(Base):
    __tablename__ = 'taq_kanji_list'

    kanji: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TaqNecessaryWord(Base):
    __tablename__ = 'taq_necessary_word'

    necessary_word_1: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_4: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_5: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_5: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_3: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_3: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_2: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_1: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_2: Mapped[str] = mapped_column(Text, nullable=False)
    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    unnecessary_word_4: Mapped[str] = mapped_column(Text, nullable=False)


class TaqRewards(Base):
    __tablename__ = 'taq_rewards'

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)


class TaqUnit(Base):
    __tablename__ = 'taq_unit'

    genre_status_5: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre_status_6: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_2: Mapped[int] = mapped_column(Integer, nullable=False)
    personality_id: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfBattleEffect(Base):
    __tablename__ = 'tdf_battle_effect'
    __table_args__ = (
        Index('tdf_battle_effect_0_quest_id', 'quest_id'),
    )

    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class TdfDifficultyIconDatum(Base):
    __tablename__ = 'tdf_difficulty_icon_data'

    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfPhaseDatum(Base):
    __tablename__ = 'tdf_phase_data'

    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    need_clear_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    phase_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfQuestDatum(Base):
    __tablename__ = 'tdf_quest_data'

    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfSchedule(Base):
    __tablename__ = 'tdf_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ex_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_disable_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class TdfTopOffset(Base):
    __tablename__ = 'tdf_top_offset'

    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfWaveGroupDatum(Base):
    __tablename__ = 'tdf_wave_group_data'

    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TeamSkillEnhanceDatum(Base):
    __tablename__ = 'team_skill_enhance_data'

    talent_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_value: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    parameter_type: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TeamSkillEnhanceLevel(Base):
    __tablename__ = 'team_skill_enhance_level'

    enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TeamSkillNode(Base):
    __tablename__ = 'team_skill_node'

    enhance_level_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_id: Mapped[int] = mapped_column(Integer, nullable=False)
    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_level_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    noise_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TeamSkillTitle(Base):
    __tablename__ = 'team_skill_title'

    title_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_text: Mapped[str] = mapped_column(Text, nullable=False)


class ThumbnailHideCondition(Base):
    __tablename__ = 'thumbnail_hide_condition'

    hide_story_id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_hide_title: Mapped[int] = mapped_column(Integer, nullable=False)
    hide_story_id_from: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TicketGachaDatum(Base):
    __tablename__ = 'ticket_gacha_data'

    gacha_detail: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    staging_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_times: Mapped[int] = mapped_column(Integer, nullable=False)


class Tips(Base):
    __tablename__ = 'tips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    tips_index: Mapped[int] = mapped_column(Integer, nullable=False)


class TmeMapDatum(Base):
    __tablename__ = 'tme_map_data'
    __table_args__ = (
        Index('tme_map_data_0_event_id', 'event_id'),
    )

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    tme_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    area_difficulty_type: Mapped[int] = mapped_column(Integer, nullable=False)


class TopicTalkChara(Base):
    __tablename__ = 'topic_talk_chara'
    __table_args__ = (
        Index('topic_talk_chara_0_original_event_id', 'original_event_id'),
    )

    name_icon_color: Mapped[str] = mapped_column(Text, nullable=False)
    reference_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_name: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_effect_color: Mapped[str] = mapped_column(Text, nullable=False)


class TopicTalkDrama(Base):
    __tablename__ = 'topic_talk_drama'

    knight_skin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lottery_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TopicTalkDramaScript(Base):
    __tablename__ = 'topic_talk_drama_script'
    __table_args__ = (
        Index('topic_talk_drama_script_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class TopicTalkMission(Base):
    __tablename__ = 'topic_talk_mission'
    __table_args__ = (
        Index('topic_talk_mission_0_original_event_id', 'original_event_id'),
        Index('topic_talk_mission_0_original_event_id_1_mission_type', 'original_event_id', 'mission_type')
    )

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TopicTalkSetting(Base):
    __tablename__ = 'topic_talk_setting'

    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_free_count: Mapped[int] = mapped_column(Integer, nullable=False)
    first_bonus_ticket_count: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TopicTalkStory(Base):
    __tablename__ = 'topic_talk_story'
    __table_args__ = (
        Index('topic_talk_story_0_original_event_id', 'original_event_id'),
    )

    relation_topic_point_3: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_point: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_point_1: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_point_2: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TopicTalkTopicDatum(Base):
    __tablename__ = 'topic_talk_topic_data'
    __table_args__ = (
        Index('topic_talk_topic_data_0_original_event_id', 'original_event_id'),
        Index('topic_talk_topic_data_0_original_event_id_1_rarity', 'original_event_id', 'rarity')
    )

    topic_name: Mapped[str] = mapped_column(Text, nullable=False)
    topic_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_type: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TotalRechargeMissionDatum(Base):
    __tablename__ = 'total_recharge_mission_data'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TotalRechargeReward(Base):
    __tablename__ = 'total_recharge_reward'

    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TotalRechargeSchedule(Base):
    __tablename__ = 'total_recharge_schedule'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class TowerAreaDatum(Base):
    __tablename__ = 'tower_area_data'

    area_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    max_floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cloister_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_bgm: Mapped[str] = mapped_column(Text, nullable=False)


class TowerCloisterQuestDatum(Base):
    __tablename__ = 'tower_cloister_quest_data'

    w1_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    start_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    drop_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    w2_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_cloister_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    w2_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerEnemyParameter(Base):
    __tablename__ = 'tower_enemy_parameter'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_color: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerExQuestDatum(Base):
    __tablename__ = 'tower_ex_quest_data'
    __table_args__ = (
        Index('tower_ex_quest_data_0_floor_num', 'floor_num'),
    )

    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_ex_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    clp_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerQuestDatum(Base):
    __tablename__ = 'tower_quest_data'
    __table_args__ = (
        Index('tower_quest_data_0_floor_num', 'floor_num'),
    )

    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    open_tower_ex_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clp_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    start_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_floor_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_image_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_image_add_type: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)


class TowerQuestFixRewardGroup(Base):
    __tablename__ = 'tower_quest_fix_reward_group'

    treasure_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerQuestOddsGroup(Base):
    __tablename__ = 'tower_quest_odds_group'
    __table_args__ = (
        Index('tower_quest_odds_group_0_odds_group_id', 'odds_group_id'),
    )

    treasure_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)


class TowerSchedule(Base):
    __tablename__ = 'tower_schedule'
    __table_args__ = (
        Index('tower_schedule_0_opening_story_id', 'opening_story_id'),
    )

    opening_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    tower_schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    max_tower_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    recovery_disable_time: Mapped[str] = mapped_column(Text, nullable=False)


class TowerStoryDatum(Base):
    __tablename__ = 'tower_story_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerStoryDetail(Base):
    __tablename__ = 'tower_story_detail'

    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerWaveGroupDatum(Base):
    __tablename__ = 'tower_wave_group_data'

    id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)


class TpRecoveryAt(Base):
    __tablename__ = 'tp_recovery_at'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_value: Mapped[int] = mapped_column(Integer, nullable=False)
    correction_value: Mapped[float] = mapped_column(REAL, nullable=False)


class TprPanelDatum(Base):
    __tablename__ = 'tpr_panel_data'

    another_parts_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    panel_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    another_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TprStoryDatum(Base):
    __tablename__ = 'tpr_story_data'
    __table_args__ = (
        Index('tpr_story_data_0_original_event_id', 'original_event_id'),
    )

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_panel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)


class TrainingQuestDatum(Base):
    __tablename__ = 'training_quest_data'

    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    training_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    training_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    limit_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    unlock_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelAreaDatum(Base):
    __tablename__ = 'travel_area_data'

    travel_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_area_name: Mapped[str] = mapped_column(Text, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_icon_x: Mapped[int] = mapped_column(Integer, nullable=False)
    top_icon_y: Mapped[int] = mapped_column(Integer, nullable=False)
    top_icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelDecreaseTimeCost(Base):
    __tablename__ = 'travel_decrease_time_cost'

    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelDramaExceptUnit(Base):
    __tablename__ = 'travel_drama_except_unit'
    __table_args__ = (
        Index('travel_drama_except_unit_0_type', 'type'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelExEventDatum(Base):
    __tablename__ = 'travel_ex_event_data'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelExEventDrama(Base):
    __tablename__ = 'travel_ex_event_drama'
    __table_args__ = (
        Index('travel_ex_event_drama_0_drama_id', 'drama_id'),
    )

    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelQuestDatum(Base):
    __tablename__ = 'travel_quest_data'
    __table_args__ = (
        Index('travel_quest_data_0_travel_area_id', 'travel_area_id'),
    )

    travel_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    situation_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_y: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_time: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_4: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_time_decrease_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_x: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_unit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_3: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_decrease_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    need_power: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelQuestResult(Base):
    __tablename__ = 'travel_quest_result'

    situation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    except_unit_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelQuestResultGroup(Base):
    __tablename__ = 'travel_quest_result_group'
    __table_args__ = (
        Index('travel_quest_result_group_0_situation_group_id', 'situation_group_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    situation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    situation_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelQuestSubReward(Base):
    __tablename__ = 'travel_quest_sub_reward'
    __table_args__ = (
        Index('travel_quest_sub_reward_0_reward_id', 'reward_id'),
        Index('travel_quest_sub_reward_0_travel_quest_id', 'travel_quest_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelResultExceptUnitGroup(Base):
    __tablename__ = 'travel_result_except_unit_group'
    __table_args__ = (
        Index('travel_result_except_unit_group_0_except_unit_group_id', 'except_unit_group_id'),
    )

    except_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    except_unit_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelRoundEventDatum(Base):
    __tablename__ = 'travel_round_event_data'

    round_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    left_door_pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    round: Mapped[int] = mapped_column(Integer, primary_key=True)
    transition_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_id: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_treasure_box_type: Mapped[int] = mapped_column(Integer, nullable=False)
    right_door_pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelRoundEventDrama(Base):
    __tablename__ = 'travel_round_event_drama'
    __table_args__ = (
        Index('travel_round_event_drama_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class TravelStartDrama(Base):
    __tablename__ = 'travel_start_drama'
    __table_args__ = (
        Index('travel_start_drama_0_drama_id', 'drama_id'),
    )

    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class TravelTopEventDatum(Base):
    __tablename__ = 'travel_top_event_data'
    __table_args__ = (
        Index('travel_top_event_data_0_top_event_id', 'top_event_id'),
    )

    pattern: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    branch_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    branch_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    zoom_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    top_icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    branch_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    zoom_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    main_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelTopEventDrama(Base):
    __tablename__ = 'travel_top_event_drama'
    __table_args__ = (
        Index('travel_top_event_drama_0_drama_id', 'drama_id'),
    )

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class TravelTopEventPosDetail(Base):
    __tablename__ = 'travel_top_event_pos_detail'

    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TrialBattleCategory(Base):
    __tablename__ = 'trial_battle_category'

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    label_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    description_detail: Mapped[str] = mapped_column(Text, nullable=False)
    label_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    label_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TrialBattleDatum(Base):
    __tablename__ = 'trial_battle_data'
    __table_args__ = (
        Index('trial_battle_data_0_category_id', 'category_id'),
    )

    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_name: Mapped[str] = mapped_column(Text, nullable=False)
    detail_boss_bg_height: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_size: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleMissionDatum(Base):
    __tablename__ = 'trial_battle_mission_data'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    trial_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleMissionReward(Base):
    __tablename__ = 'trial_battle_mission_reward'
    __table_args__ = (
        Index('trial_battle_mission_reward_0_mission_reward_id', 'mission_reward_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleRewardDatum(Base):
    __tablename__ = 'trial_battle_reward_data'

    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleTalentWeakness(Base):
    __tablename__ = 'trial_battle_talent_weakness'

    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_weakness: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkDrama(Base):
    __tablename__ = 'ttk_drama'
    __table_args__ = (
        Index('ttk_drama_0_drama_id', 'drama_id'),
    )

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class TtkEnemy(Base):
    __tablename__ = 'ttk_enemy'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    coin: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkNaviComment(Base):
    __tablename__ = 'ttk_navi_comment'

    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class TtkReward(Base):
    __tablename__ = 'ttk_reward'
    __table_args__ = (
        Index('ttk_reward_0_ttk_score', 'ttk_score'),
    )

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ttk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkScore(Base):
    __tablename__ = 'ttk_score'

    difficulty_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    coefficient_coin_score: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    life: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_wrong_num: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkStory(Base):
    __tablename__ = 'ttk_story'
    __table_args__ = (
        Index('ttk_story_0_ttk_score', 'ttk_score'),
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    ttk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    ttk_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TtkStoryScript(Base):
    __tablename__ = 'ttk_story_script'
    __table_args__ = (
        Index('ttk_story_script_0_story_id', 'story_id'),
    )

    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkWeapon(Base):
    __tablename__ = 'ttk_weapon'
    __table_args__ = (
        Index('ttk_weapon_0_ttk_score', 'ttk_score'),
    )

    ttk_weapon_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ttk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class UekBoss(Base):
    __tablename__ = 'uek_boss'
    __table_args__ = (
        Index('uek_boss_0_enemy_id', 'enemy_id'),
    )

    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    result_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)


class UekDrama(Base):
    __tablename__ = 'uek_drama'
    __table_args__ = (
        Index('uek_drama_0_drama_id', 'drama_id'),
    )

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class UekMission(Base):
    __tablename__ = 'uek_mission'

    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class UekSpineAnimLink(Base):
    __tablename__ = 'uek_spine_anim_link'
    __table_args__ = (
        Index('uek_spine_anim_link_0_anim_num', 'anim_num'),
    )

    anim_num: Mapped[int] = mapped_column(Integer, nullable=False)
    spine_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UniqueEquipConsumeGroup(Base):
    __tablename__ = 'unique_equip_consume_group'
    __table_args__ = (
        Index('unique_equip_consume_group_0_group_id', 'group_id'),
        Index('unique_equip_consume_group_0_item_id', 'item_id', unique=True)
    )

    index_in_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class UniqueEquipCraftEnhance(Base):
    __tablename__ = 'unique_equip_craft_enhance'
    __table_args__ = (
        Index('unique_equip_craft_enhance_0_consume_group_id', 'consume_group_id'),
    )

    consume_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UniqueEquipEnhanceRate(Base):
    __tablename__ = 'unique_equip_enhance_rate'
    __table_args__ = (
        Index('unique_equip_enhance_rate_0_equipment_id', 'equipment_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    min_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    max_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentBonus(Base):
    __tablename__ = 'unique_equipment_bonus'
    __table_args__ = (
        Index('unique_equipment_bonus_0_equipment_id', 'equipment_id'),
    )

    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    max_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    min_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentCraft(Base):
    __tablename__ = 'unique_equipment_craft'

    consume_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    crafted_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class UniqueEquipmentDatum(Base):
    __tablename__ = 'unique_equipment_data'

    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    enable_donation: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    craft_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    sale_price: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    require_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_name: Mapped[str] = mapped_column(Text, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_enhance_point: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentEnhanceDatum(Base):
    __tablename__ = 'unique_equipment_enhance_data'

    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    needed_point: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    total_point: Mapped[int] = mapped_column(Integer, nullable=False)


class UniqueEquipmentEnhanceRate(Base):
    __tablename__ = 'unique_equipment_enhance_rate'

    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentRankup(Base):
    __tablename__ = 'unique_equipment_rankup'
    __table_args__ = (
        Index('unique_equipment_rankup_0_equip_id', 'equip_id'),
    )

    item_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    crafted_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unique_equip_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitAttackPattern(Base):
    __tablename__ = 'unit_attack_pattern'

    atk_pattern_15: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_19: Mapped[int] = mapped_column(Integer, nullable=False)
    pattern_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atk_pattern_7: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_2: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_12: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_8: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_18: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_6: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_16: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_14: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    loop_start: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_4: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_3: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_1: Mapped[int] = mapped_column(Integer, nullable=False)
    loop_end: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_5: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_17: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_20: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_10: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_11: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_9: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_13: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitBackground(Base):
    __tablename__ = 'unit_background'

    position: Mapped[float] = mapped_column(REAL, nullable=False)
    bg_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitClipSetting(Base):
    __tablename__ = 'unit_clip_setting'

    center_x: Mapped[int] = mapped_column(Integer, nullable=False)
    size_x: Mapped[int] = mapped_column(Integer, nullable=False)
    clip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    softness_x: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitComments(Base):
    __tablename__ = 'unit_comments'
    __table_args__ = (
        Index('unit_comments_0_unit_id', 'unit_id'),
        Index('unit_comments_0_unit_id_1_use_type', 'unit_id', 'use_type')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    change_time_2: Mapped[float] = mapped_column(REAL, nullable=False)
    face_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    change_time: Mapped[float] = mapped_column(REAL, nullable=False)
    target_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face: Mapped[int] = mapped_column(Integer, nullable=False)
    face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_2: Mapped[int] = mapped_column(Integer, nullable=False)
    use_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_time_3: Mapped[float] = mapped_column(REAL, nullable=False)
    all_comments_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitConversion(Base):
    __tablename__ = 'unit_conversion'
    __table_args__ = (
        Index('unit_conversion_0_unit_id', 'unit_id', unique=True),
    )

    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitDatum(Base):
    __tablename__ = 'unit_data'
    __table_args__ = (
        Index('unit_data_0_original_unit_id', 'original_unit_id'),
    )

    cutin2_star6: Mapped[int] = mapped_column(Integer, nullable=False)
    se_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin_2: Mapped[int] = mapped_column(Integer, nullable=False)
    kana: Mapped[str] = mapped_column(Text, nullable=False)
    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    move_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_collab: Mapped[int] = mapped_column(Integer, nullable=False)
    only_disp_owned: Mapped[int] = mapped_column(Integer, nullable=False)
    prefab_id_battle: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_atk_cast_time: Mapped[float] = mapped_column(REAL, nullable=False)
    motion_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    search_area_width: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    exskill_display: Mapped[int] = mapped_column(Integer, nullable=False)
    is_limited: Mapped[int] = mapped_column(Integer, nullable=False)
    original_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin1_star6: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class UnitEnemyDatum(Base):
    __tablename__ = 'unit_enemy_data'

    motion_type: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin_star6: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    search_area_width: Mapped[int] = mapped_column(Integer, nullable=False)
    se_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    normal_atk_cast_time: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visual_change_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    move_speed: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitExEquipmentSlot(Base):
    __tablename__ = 'unit_ex_equipment_slot'

    slot_category_1: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_category_2: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_category_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitIntroduction(Base):
    __tablename__ = 'unit_introduction'
    __table_args__ = (
        Index('unit_introduction_0_gacha_id', 'gacha_id'),
    )

    maximum_chunk_size_loop_1: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_1: Mapped[int] = mapped_column(Integer, nullable=False)
    introduction_number: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_loop_2: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    maximum_chunk_size_3: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    maximum_chunk_size_loop_3: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class UnitMotionList(Base):
    __tablename__ = 'unit_motion_list'

    sp_motion: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitMypagePos(Base):
    __tablename__ = 'unit_mypage_pos'

    scale: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitPosAdjustment(Base):
    __tablename__ = 'unit_pos_adjustment'

    actual_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    is_myprofile_image: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    home_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    profile_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_id3: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_id1: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    home_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    home_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    friend_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_id2: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    home_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitProfile(Base):
    __tablename__ = 'unit_profile'

    blood_type: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    age: Mapped[str] = mapped_column(Text, nullable=False)
    race: Mapped[str] = mapped_column(Text, nullable=False)
    guild_id: Mapped[str] = mapped_column(Text, nullable=False)
    favorite: Mapped[str] = mapped_column(Text, nullable=False)
    voice: Mapped[str] = mapped_column(Text, nullable=False)
    catch_copy: Mapped[str] = mapped_column(Text, nullable=False)
    guild: Mapped[str] = mapped_column(Text, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    birth_day: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[str] = mapped_column(Text, nullable=False)
    birth_month: Mapped[str] = mapped_column(Text, nullable=False)
    self_text: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[str] = mapped_column(Text, nullable=False)


class UnitPromotion(Base):
    __tablename__ = 'unit_promotion'
    __table_args__ = (
        Index('unit_promotion_0_unit_id', 'unit_id'),
    )

    equip_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitPromotionStatus(Base):
    __tablename__ = 'unit_promotion_status'

    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)


class UnitRarity(Base):
    __tablename__ = 'unit_rarity'
    __table_args__ = (
        Index('unit_rarity_0_unit_id', 'unit_id'),
        Index('unit_rarity_0_unit_material_id', 'unit_material_id')
    )

    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    def_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    atk_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_material_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_energy_recovery_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitRoleDatum(Base):
    __tablename__ = 'unit_role_data'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_role_id: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitRoleGachaLevel(Base):
    __tablename__ = 'unit_role_gacha_level'

    gacha_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_min_slot_level: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_count: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitRoleMasteryEnhanceDatum(Base):
    __tablename__ = 'unit_role_mastery_enhance_data'

    slot_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_param_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    role_param_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mastery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enhance_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitRoleMasteryId(Base):
    __tablename__ = 'unit_role_mastery_id'
    __table_args__ = (
        UniqueConstraint('unit_role_id', 'slot_id'),
    )

    slot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mastery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_role_id: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitRoleMasteryItemDatum(Base):
    __tablename__ = 'unit_role_mastery_item_data'
    __table_args__ = (
        Index('unit_role_mastery_item_data_0_mastery_id', 'mastery_id'),
    )

    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    mastery_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitRoleMasteryLevel(Base):
    __tablename__ = 'unit_role_mastery_level'
    __table_args__ = (
        Index('unit_role_mastery_level_0_mastery_id', 'mastery_id'),
    )

    num: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    mastery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitRoleMasterySlotDatum(Base):
    __tablename__ = 'unit_role_mastery_slot_data'

    slot_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    mastery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class UnitRoleType(Base):
    __tablename__ = 'unit_role_type'

    unit_role_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_role_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitSkillDatum(Base):
    __tablename__ = 'unit_skill_data'

    ex_skill_evolution_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_9: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_10: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_evolution: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_evolution_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_union_burst: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_4: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_6: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_evolution_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_evolution_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sp_skill_evolution_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_1: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitSkillDatumRf(Base):
    __tablename__ = 'unit_skill_data_rf'
    __table_args__ = (
        Index('unit_skill_data_rf_0_rf_skill_id', 'rf_skill_id'),
        Index('unit_skill_data_rf_0_skill_id', 'skill_id')
    )

    rf_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    min_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    max_lv: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitStatusCoefficient(Base):
    __tablename__ = 'unit_status_coefficient'

    skill_lv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill2_evolution_slv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    exskill_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill1_evolution_slv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    overall_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    atk_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill2_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    ub_evolution_slv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    def_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill1_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    coefficient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_def_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitTalent(Base):
    __tablename__ = 'unit_talent'
    __table_args__ = (
        Index('unit_talent_0_unit_id', 'unit_id'),
    )

    setting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitUniqueEquip(Base):
    __tablename__ = 'unit_unique_equip'

    equip_slot: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitUniqueEquipment(Base):
    __tablename__ = 'unit_unique_equipment'
    __table_args__ = (
        Index('unit_unique_equipment_0_unit_id', 'unit_id'),
    )

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_id: Mapped[int] = mapped_column(Integer, nullable=False)


class UnlockRarity6(Base):
    __tablename__ = 'unlock_rarity_6'
    __table_args__ = (
        Index('unlock_rarity_6_0_material_id', 'material_id'),
        Index('unlock_rarity_6_0_unit_id', 'unit_id'),
        Index('unlock_rarity_6_0_unit_id_1_slot_id', 'unit_id', 'slot_id'),
        Index('unlock_rarity_6_0_unit_id_1_unlock_level', 'unit_id', 'unlock_level')
    )

    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    material_count: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    material_type: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)


class UnlockSkillDatum(Base):
    __tablename__ = 'unlock_skill_data'

    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_skill: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnlockUnitCondition(Base):
    __tablename__ = 'unlock_unit_condition'

    condition_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_type_detail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_5: Mapped[int] = mapped_column(Integer, nullable=False)
    count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class VisualCustomize(Base):
    __tablename__ = 'visual_customize'

    quest_top_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_top_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    title_voice: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_logo: Mapped[int] = mapped_column(Integer, nullable=False)
    title_prefab: Mapped[int] = mapped_column(Integer, nullable=False)
    watched_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class VoiceGroup(Base):
    __tablename__ = 'voice_group'

    group_unit_id_01: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_05: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id_comment: Mapped[str] = mapped_column(Text, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_unit_id_03: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_02: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_04: Mapped[int] = mapped_column(Integer, nullable=False)


class VoiceGroupChara(Base):
    __tablename__ = 'voice_group_chara'

    unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_05: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_02: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_03: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_01: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_04: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_08: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_comment: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_06: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_07: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_09: Mapped[int] = mapped_column(Integer, nullable=False)


class VoteDatum(Base):
    __tablename__ = 'vote_data'

    result_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    result_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    vote_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    vote_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    result_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class VoteInfo(Base):
    __tablename__ = 'vote_info'

    vote_help: Mapped[str] = mapped_column(Text, nullable=False)
    vote_title: Mapped[str] = mapped_column(Text, nullable=False)
    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_help_index: Mapped[int] = mapped_column(Integer, primary_key=True)


class VoteUnit(Base):
    __tablename__ = 'vote_unit'

    unit_rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WacBirthdayDramaScript(Base):
    __tablename__ = 'wac_birthday_drama_script'
    __table_args__ = (
        Index('wac_birthday_drama_script_0_drama_id', 'drama_id'),
    )

    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class WacDatum(Base):
    __tablename__ = 'wac_data'
    __table_args__ = (
        Index('wac_data_0_mural_group_id', 'mural_group_id'),
    )

    idle_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_search_id: Mapped[int] = mapped_column(Integer, nullable=False)
    birthday_login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_time: Mapped[str] = mapped_column(Text, nullable=False)
    pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    draw_end_to_center: Mapped[int] = mapped_column(Integer, nullable=False)
    post_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mural_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mural_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WacDramaScript(Base):
    __tablename__ = 'wac_drama_script'
    __table_args__ = (
        Index('wac_drama_script_0_drama_id', 'drama_id'),
    )

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class WacMuralBgDatum(Base):
    __tablename__ = 'wac_mural_bg_data'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_offset_x: Mapped[str] = mapped_column(Text, nullable=False)
    end_offset_x: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WacMuralDatum(Base):
    __tablename__ = 'wac_mural_data'
    __table_args__ = (
        Index('wac_mural_data_0_mural_group_id', 'mural_group_id'),
    )

    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    mural_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WacPresentStillDatum(Base):
    __tablename__ = 'wac_present_still_data'

    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    still_id: Mapped[int] = mapped_column(Integer, nullable=False)


class WacUnitSearchDatum(Base):
    __tablename__ = 'wac_unit_search_data'
    __table_args__ = (
        Index('wac_unit_search_data_0_unit_id', 'unit_id'),
        Index('wac_unit_search_data_0_unit_search_id', 'unit_search_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_search_id: Mapped[int] = mapped_column(Integer, nullable=False)


class WaveGroupDatum(Base):
    __tablename__ = 'wave_group_data'
    __table_args__ = (
        Index('wave_group_data_0_wave_group_id', 'wave_group_id'),
    )

    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class WonStoryDatum(Base):
    __tablename__ = 'won_story_data'
    __table_args__ = (
        Index('won_story_data_0_note_id', 'note_id'),
        Index('won_story_data_0_original_event_id', 'original_event_id'),
        Index('won_story_data_0_unit_id_1_is_last', 'unit_id', 'is_last')
    )

    order: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_last: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    note_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class WonStoryScript(Base):
    __tablename__ = 'won_story_script'
    __table_args__ = (
        Index('won_story_script_0_story_id', 'story_id'),
    )

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)


class Worldmap(Base):
    __tablename__ = 'worldmap'
    __table_args__ = (
        Index('worldmap_0_map_type', 'map_type'),
    )

    tutorial_adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    view_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    start_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    end_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class WtmStoryDatum(Base):
    __tablename__ = 'wtm_story_data'
    __table_args__ = (
        Index('wtm_story_data_0_original_event_id', 'original_event_id'),
    )

    wtm_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_sub_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_sub_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class WtsNaviComment(Base):
    __tablename__ = 'wts_navi_comment'
    __table_args__ = (
        Index('wts_navi_comment_0_where_type', 'where_type'),
    )

    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)


class WtsStoryDatum(Base):
    __tablename__ = 'wts_story_data'
    __table_args__ = (
        Index('wts_story_data_0_original_event_id', 'original_event_id'),
    )

    repeat_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class XacStoryDatum(Base):
    __tablename__ = 'xac_story_data'
    __table_args__ = (
        Index('xac_story_data_0_original_event_id', 'original_event_id'),
    )

    condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    balloon_pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    balloon_pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class XehStoryDatum(Base):
    __tablename__ = 'xeh_story_data'
    __table_args__ = (
        Index('xeh_story_data_0_original_event_id', 'original_event_id'),
    )

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class YsnStoryDatum(Base):
    __tablename__ = 'ysn_story_data'
    __table_args__ = (
        Index('ysn_story_data_0_original_event_id', 'original_event_id'),
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)