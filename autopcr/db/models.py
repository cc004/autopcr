# coding: utf-8
# type: ignore
# Data( => Datum(

from typing import Optional

from sqlalchemy import Integer, REAL, Text, UniqueConstraint
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

    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)


class AbdStoryScript(Base):
    __tablename__ = 'abd_story_script'

    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssBattleEffect(Base):
    __tablename__ = 'abyss_battle_effect'

    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)


class AbyssBossDatum(Base):
    __tablename__ = 'abyss_boss_data'

    use_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_clear_score_bonus: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    score_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    release_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssBossDisplayDatum(Base):
    __tablename__ = 'abyss_boss_display_data'

    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    result_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssClearReward(Base):
    __tablename__ = 'abyss_clear_reward'

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssEnemyParameter(Base):
    __tablename__ = 'abyss_enemy_parameter'

    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssQuestDatum(Base):
    __tablename__ = 'abyss_quest_data'

    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    drop_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssQuestDisplayDatum(Base):
    __tablename__ = 'abyss_quest_display_data'

    wave_bgm_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_5: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_scale_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssSchedule(Base):
    __tablename__ = 'abyss_schedule'

    talent_id: Mapped[int] = mapped_column(Integer, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    boss_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class AbyssScoreReward(Base):
    __tablename__ = 'abyss_score_reward'

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    abyss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class AbyssWaveGroupDatum(Base):
    __tablename__ = 'abyss_wave_group_data'

    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnAdv(Base):
    __tablename__ = 'acn_adv'

    trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnEndlessBattleSetting(Base):
    __tablename__ = 'acn_endless_battle_setting'

    _35b148db517edba5c8562aa98530b65ba82acc0cd0c411458f34a04ee06371ec: Mapped[int] = mapped_column('35b148db517edba5c8562aa98530b65ba82acc0cd0c411458f34a04ee06371ec', Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    _44770a40b427b6fa6d959579627629c08dec1800be86351330075e4218b48932: Mapped[int] = mapped_column('44770a40b427b6fa6d959579627629c08dec1800be86351330075e4218b48932', Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)
    _00f4c3dbef3c2ee166429eefe7edb32d2d877734bf2ebe88db597d2d44d9027f: Mapped[int] = mapped_column('00f4c3dbef3c2ee166429eefe7edb32d2d877734bf2ebe88db597d2d44d9027f', Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_gold_num: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnEnemyParameter(Base):
    __tablename__ = 'acn_enemy_parameter'

    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnGaugeSectionDatum(Base):
    __tablename__ = 'acn_gauge_section_data'

    rate_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    section: Mapped[int] = mapped_column(Integer, primary_key=True)
    inferior_trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    superior_trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gauge_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnMissionDatum(Base):
    __tablename__ = 'acn_mission_data'

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    acn_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class AcnMissionRewardDatum(Base):
    __tablename__ = 'acn_mission_reward_data'

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnMultiBossSetting(Base):
    __tablename__ = 'acn_multi_boss_setting'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    die_position_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    die_position_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    die_motion_pause_time: Mapped[float] = mapped_column(REAL, nullable=False)


class AcnQuestDatum(Base):
    __tablename__ = 'acn_quest_data'

    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    next_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    lane_priority_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_offset_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_offset_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_offset_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    lane_priority_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    deck_number: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_offset_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    lane_priority_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    restriction_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ae0dd1ec7dc20598557b60b90aac0e72678980afb6cf1df6d9d4c1b97b0feac7: Mapped[str] = mapped_column(Text, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_3: Mapped[float] = mapped_column(REAL, nullable=False)
    gauge_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnQuestDifficultyDatum(Base):
    __tablename__ = 'acn_quest_difficulty_data'

    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_boss_ticket: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    b75059c082edbd98f0b21492cf2b18c9ddd737f71e063ae7289dd463d248ea9a: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnRestrictionUnitGroup(Base):
    __tablename__ = 'acn_restriction_unit_group'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restriction_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnSchedule(Base):
    __tablename__ = 'acn_schedule'

    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_accept_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    unlock_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    after_bgm: Mapped[str] = mapped_column(Text, nullable=False)


class AcnSpecialBattle(Base):
    __tablename__ = 'acn_special_battle'

    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnStorySkipReward(Base):
    __tablename__ = 'acn_story_skip_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AcnUnknownBattle(Base):
    __tablename__ = 'acn_unknown_battle'

    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    step: Mapped[int] = mapped_column(Integer, primary_key=True)


class AcnWaveGroupDatum(Base):
    __tablename__ = 'acn_wave_group_data'

    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ActualUnitBackground(Base):
    __tablename__ = 'actual_unit_background'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)


class AilmentDatum(Base):
    __tablename__ = 'ailment_data'

    _9a1d900f9ae1e8474fef93c56e53855c120f47e0180f21651d1d8faaaf34a401: Mapped[str] = mapped_column('9a1d900f9ae1e8474fef93c56e53855c120f47e0180f21651d1d8faaaf34a401', Text, nullable=False)
    ailment_action: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ailment_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AisSetting(Base):
    __tablename__ = 'ais_setting'

    later_op_release_condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_op_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    later_op_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_op_release_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    last_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    later_op_release_condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AisStoryDatum(Base):
    __tablename__ = 'ais_story_data'

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AlbumProductionList(Base):
    __tablename__ = 'album_production_list'

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AlbumVoiceList(Base):
    __tablename__ = 'album_voice_list'

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)


class AlternativeItemDatum(Base):
    __tablename__ = 'alternative_item_data'

    src_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dst_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_rate: Mapped[int] = mapped_column(Integer, nullable=False)


class ApaSchedule(Base):
    __tablename__ = 'apa_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    op_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    ed_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    url_1: Mapped[str] = mapped_column(Text, nullable=False)
    url_2: Mapped[str] = mapped_column(Text, nullable=False)
    url_3: Mapped[str] = mapped_column(Text, nullable=False)
    apa_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class ApgAttractionDatum(Base):
    __tablename__ = 'apg_attraction_data'

    detail_description: Mapped[str] = mapped_column(Text, nullable=False)
    _7e0dac3cbddd90814b2150cc058212b059fa5990f31ec65ac2754ccaf56f51c2: Mapped[str] = mapped_column('7e0dac3cbddd90814b2150cc058212b059fa5990f31ec65ac2754ccaf56f51c2', Text, nullable=False)
    attraction_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ApgDramaScript(Base):
    __tablename__ = 'apg_drama_script'

    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class ApgStoryDatum(Base):
    __tablename__ = 'apg_story_data'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    _9d73a0d97f70466bbb60668e389b9a427236a3fec029d560634c2dc928d5c8e3: Mapped[str] = mapped_column('9d73a0d97f70466bbb60668e389b9a427236a3fec029d560634c2dc928d5c8e3', Text, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attraction_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class AppIcon(Base):
    __tablename__ = 'app_icon'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ArcadeDescription(Base):
    __tablename__ = 'arcade_description'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    arcade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ArcadeList(Base):
    __tablename__ = 'arcade_list'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    banner_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_chat_title: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    cue_id: Mapped[str] = mapped_column(Text, nullable=False)
    banner_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    arcade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)


class ArcadeStoryList(Base):
    __tablename__ = 'arcade_story_list'

    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arcade_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaDailyRankReward(Base):
    __tablename__ = 'arena_daily_rank_reward'

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaDefenceReward(Base):
    __tablename__ = 'arena_defence_reward'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_count: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaMaxRankReward(Base):
    __tablename__ = 'arena_max_rank_reward'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)


class ArenaMaxSeasonRankReward(Base):
    __tablename__ = 'arena_max_season_rank_reward'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class AsbDramaScript(Base):
    __tablename__ = 'asb_drama_script'

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class AsbStoryDatum(Base):
    __tablename__ = 'asb_story_data'

    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    page_num: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Asm4ChoiceDatum(Base):
    __tablename__ = 'asm_4_choice_data'

    image_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_1: Mapped[str] = mapped_column(Text, nullable=False)
    image_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_4: Mapped[str] = mapped_column(Text, nullable=False)
    choice_3: Mapped[str] = mapped_column(Text, nullable=False)
    image_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answer: Mapped[int] = mapped_column(Integer, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    choice_2: Mapped[str] = mapped_column(Text, nullable=False)


class AsmArchiveCompletionReward(Base):
    __tablename__ = 'asm_archive_completion_reward'

    archive_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    completion_detail: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmDatum(Base):
    __tablename__ = 'asm_data'

    asm_type: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AsmGameSetting(Base):
    __tablename__ = 'asm_game_setting'

    help_use_count_veryhard: Mapped[int] = mapped_column(Integer, nullable=False)
    help_use_count_normal: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normal_limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    incorrect_answer_penalty_time: Mapped[int] = mapped_column(Integer, nullable=False)
    concentration_quiz_limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_quiz_num: Mapped[int] = mapped_column(Integer, nullable=False)
    help_use_count_hard: Mapped[int] = mapped_column(Integer, nullable=False)
    lottery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    concentration_limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_concentration_mode_score_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_concentration_mode_score_2: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmManyAnswersDatum(Base):
    __tablename__ = 'asm_many_answers_data'

    is_correct_1: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_2: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct_2: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_4: Mapped[str] = mapped_column(Text, nullable=False)
    image_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    choice_3: Mapped[str] = mapped_column(Text, nullable=False)
    image_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_1: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct_3: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    is_correct_4: Mapped[int] = mapped_column(Integer, nullable=False)


class AsmMemoryGauge(Base):
    __tablename__ = 'asm_memory_gauge'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gauge_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trigger_score: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_detail: Mapped[str] = mapped_column(Text, nullable=False)


class AsmReactionDatum(Base):
    __tablename__ = 'asm_reaction_data'

    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_param_3: Mapped[int] = mapped_column(Integer, nullable=False)
    face_change_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_change_time: Mapped[float] = mapped_column(REAL, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reaction_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_param_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_param_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class AsmTrueOrFalseDatum(Base):
    __tablename__ = 'asm_true_or_false_data'

    correct_answer: Mapped[int] = mapped_column(Integer, nullable=False)
    asm_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Banner(Base):
    __tablename__ = 'banner'

    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    show_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_show_room: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BannerNews(Base):
    __tablename__ = 'banner_news'

    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_show_room: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    poster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    show_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)


class BeginnerCharaETicketDatum(Base):
    __tablename__ = 'beginner_chara_e_ticket_data'

    forced_exchange_hour: Mapped[int] = mapped_column(Integer, nullable=False)
    jewel_store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_e_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    beginner_type: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    beginner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beginner_limit_hour: Mapped[int] = mapped_column(Integer, nullable=False)


class BgDatum(Base):
    __tablename__ = 'bg_data'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    view_name: Mapped[str] = mapped_column(Text, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BirthdayLoginBonusDatum(Base):
    __tablename__ = 'birthday_login_bonus_data'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BirthdayLoginBonusDetail(Base):
    __tablename__ = 'birthday_login_bonus_detail'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BirthdayLoginBonusDramaScript(Base):
    __tablename__ = 'birthday_login_bonus_drama_script'

    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class BmyNaviComment(Base):
    __tablename__ = 'bmy_navi_comment'

    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class BmyStoryDatum(Base):
    __tablename__ = 'bmy_story_data'

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class BroadcastSchedule(Base):
    __tablename__ = 'broadcast_schedule'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    broadcast_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BulletinCalendar(Base):
    __tablename__ = 'bulletin_calendar'

    url: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    banner_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    show_type: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_show_room: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)


class BywayBattleQuestDatum(Base):
    __tablename__ = 'byway_battle_quest_data'

    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_restrict_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)


class BywayDeliveryQuestDatum(Base):
    __tablename__ = 'byway_delivery_quest_data'

    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_category: Mapped[int] = mapped_column(Integer, nullable=False)


class BywayQuestDatum(Base):
    __tablename__ = 'byway_quest_data'

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    byway_quest_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class BywayStoryDetail(Base):
    __tablename__ = 'byway_story_detail'

    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    color_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CampaignBeginnerDatum(Base):
    __tablename__ = 'campaign_beginner_data'

    id_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    beginner_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CampaignFreegacha(Base):
    __tablename__ = 'campaign_freegacha'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    _5402edb284541b4f9d69bc8da6b040cb6d9bae43d9c57cede0ba884c6760e054: Mapped[int] = mapped_column('5402edb284541b4f9d69bc8da6b040cb6d9bae43d9c57cede0ba884c6760e054', Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _1dc034f51b0bc4e394529d2a653b94c203f1056028004e168f536cf09813a8a1: Mapped[int] = mapped_column('1dc034f51b0bc4e394529d2a653b94c203f1056028004e168f536cf09813a8a1', Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_10_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    freegacha_1: Mapped[int] = mapped_column(Integer, nullable=False)
    freegacha_10: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignFreegachaDatum(Base):
    __tablename__ = 'campaign_freegacha_data'

    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignFreegachaSp(Base):
    __tablename__ = 'campaign_freegacha_sp'

    max_exec_count: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class CampaignLevelDatum(Base):
    __tablename__ = 'campaign_level_data'

    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, nullable=False)
    label_color: Mapped[str] = mapped_column(Text, nullable=False)
    frame_color: Mapped[str] = mapped_column(Text, nullable=False)


class CampaignMissionCategory(Base):
    __tablename__ = 'campaign_mission_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignMissionDatum(Base):
    __tablename__ = 'campaign_mission_data'

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    title_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mark_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class CampaignMissionRewardDatum(Base):
    __tablename__ = 'campaign_mission_reward_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class CampaignMissionSchedule(Base):
    __tablename__ = 'campaign_mission_schedule'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CampaignSchedule(Base):
    __tablename__ = 'campaign_schedule'

    level_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_image: Mapped[int] = mapped_column(Integer, nullable=False)
    duplication_order: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_category: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_type: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[float] = mapped_column(REAL, nullable=False)
    shiori_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    beginner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)


class CampaignShioriGroup(Base):
    __tablename__ = 'campaign_shiori_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shiori_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanBuddy(Base):
    __tablename__ = 'caravan_buddy'

    effect_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_description1: Mapped[str] = mapped_column(Text, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    buddy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    effect_description2: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanBuffDisp(Base):
    __tablename__ = 'caravan_buff_disp'

    count_from: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    count_to: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanChangeBlockType(Base):
    __tablename__ = 'caravan_change_block_type'

    reference_id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    change_block_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_type_to: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_from: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanCoinShopLineup(Base):
    __tablename__ = 'caravan_coin_shop_lineup'

    currency_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDicePattern(Base):
    __tablename__ = 'caravan_dice_pattern'

    dice_odds: Mapped[int] = mapped_column(Integer, primary_key=True)
    pattern: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDiceRewardPeriod(Base):
    __tablename__ = 'caravan_dice_reward_period'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanDish(Base):
    __tablename__ = 'caravan_dish'

    new_line_name: Mapped[str] = mapped_column(Text, nullable=False)
    disable_category: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    sub_effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_description: Mapped[str] = mapped_column(Text, nullable=False)
    sub_effect_description: Mapped[str] = mapped_column(Text, nullable=False)
    sub_effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sold_price: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_times: Mapped[int] = mapped_column(Integer, nullable=False)
    recipe_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanDishDrawable(Base):
    __tablename__ = 'caravan_dish_drawable'

    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanDishReward(Base):
    __tablename__ = 'caravan_dish_reward'

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDishTurnEffect(Base):
    __tablename__ = 'caravan_dish_turn_effect'

    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)
    turn_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    turn_to: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanDrama(Base):
    __tablename__ = 'caravan_drama'

    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanEffectSetting(Base):
    __tablename__ = 'caravan_effect_setting'

    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    scene_type: Mapped[int] = mapped_column(Integer, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanEventEffect(Base):
    __tablename__ = 'caravan_event_effect'

    ff1e69db35d970eaf6fa51a9017e465b15e17c0869ffc91b86cc0125e3adc1f7: Mapped[str] = mapped_column(Text, nullable=False)
    effect_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_times: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_value: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanExcludeCountBlock(Base):
    __tablename__ = 'caravan_exclude_count_block'

    block_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exclude_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanGachaBlockLineup(Base):
    __tablename__ = 'caravan_gacha_block_lineup'

    premium_gacha_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    rare_gacha_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_gacha_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_gacha_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    rare_gacha_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    premium_gacha_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanGoalBonus(Base):
    __tablename__ = 'caravan_goal_bonus'

    bonus_label: Mapped[int] = mapped_column(Integer, nullable=False)
    early_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    early_level: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    early_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanMap(Base):
    __tablename__ = 'caravan_map'

    pre_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_4: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    next_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_2: Mapped[int] = mapped_column(Integer, nullable=False)
    next_2: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)
    next_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_1: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_to_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    next_3: Mapped[int] = mapped_column(Integer, nullable=False)
    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanMapLayout(Base):
    __tablename__ = 'caravan_map_layout'

    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    block_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanMapObject(Base):
    __tablename__ = 'caravan_map_object'

    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    object_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanMileBlockReward(Base):
    __tablename__ = 'caravan_mile_block_reward'

    count: Mapped[int] = mapped_column(Integer, nullable=False)
    upgrade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanNaviComment(Base):
    __tablename__ = 'caravan_navi_comment'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class CaravanRival(Base):
    __tablename__ = 'caravan_rival'

    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rival_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    dice_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanRivalBonus(Base):
    __tablename__ = 'caravan_rival_bonus'

    bonus_label: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    label_text: Mapped[str] = mapped_column(Text, nullable=False)


class CaravanRivalMinigameList(Base):
    __tablename__ = 'caravan_rival_minigame_list'

    rival_minigame_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    rival_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanSchedule(Base):
    __tablename__ = 'caravan_schedule'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_close_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    coin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    target_turn: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    minigame_retire_reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    start_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_caravan_dish_by_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanShopBlockRank(Base):
    __tablename__ = 'caravan_shop_block_rank'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    upgrade_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanShortcut(Base):
    __tablename__ = 'caravan_shortcut'

    shortcut_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    remove_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_point_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    remove_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanSoundSetting(Base):
    __tablename__ = 'caravan_sound_setting'

    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    scene_type: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    sound_type: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CaravanTreasure(Base):
    __tablename__ = 'caravan_treasure'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appraise_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    reset_value: Mapped[int] = mapped_column(Integer, nullable=False)
    new_line_name: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanTreasureBlockRank(Base):
    __tablename__ = 'caravan_treasure_block_rank'

    odds_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    upgrade_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CaravanTreasureBlockReal(Base):
    __tablename__ = 'caravan_treasure_block_real'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


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
    ccc_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class CccDropGroupDatum(Base):
    __tablename__ = 'ccc_drop_group_data'

    object_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    object_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drop_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    object_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class CccObject(Base):
    __tablename__ = 'ccc_object'

    ccc_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ccc_object_type: Mapped[int] = mapped_column(Integer, nullable=False)
    absorb_frame: Mapped[int] = mapped_column(Integer, nullable=False)
    is_report: Mapped[int] = mapped_column(Integer, nullable=False)
    fall_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CccScenario(Base):
    __tablename__ = 'ccc_scenario'

    ccc_object_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ccc_scenario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    frame: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    idx: Mapped[int] = mapped_column(Integer, primary_key=True)


class CggCompletionDatum(Base):
    __tablename__ = 'cgg_completion_data'

    secret_goods_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    receive_description: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    completion_num: Mapped[int] = mapped_column(Integer, nullable=False)
    secret_goods_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    secret_goods_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class CggCompletionRewardDatum(Base):
    __tablename__ = 'cgg_completion_reward_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)


class CggDrama(Base):
    __tablename__ = 'cgg_drama'

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class CggGachaInfo(Base):
    __tablename__ = 'cgg_gacha_info'

    cgg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_intro: Mapped[str] = mapped_column(Text, nullable=False)
    cost_currency_num: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_description: Mapped[str] = mapped_column(Text, nullable=False)


class CggGachaLineup(Base):
    __tablename__ = 'cgg_gacha_lineup'

    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lineup_id: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CggGameSettings(Base):
    __tablename__ = 'cgg_game_settings'

    max_goods_count: Mapped[int] = mapped_column(Integer, nullable=False)
    cgg_gacha_currency_id: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_shelf_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_luppi_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    cgg_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _7615fde5529ef50144d3be8384f060cbf0426caf0fae794297e6cfa782f58def: Mapped[int] = mapped_column('7615fde5529ef50144d3be8384f060cbf0426caf0fae794297e6cfa782f58def', Integer, nullable=False)
    max_gacha_exchange_count: Mapped[int] = mapped_column(Integer, nullable=False)
    _7f7fba9ca9d4daebea81e66f51cc1984dda866bbd6521c51a0ad69636e438734: Mapped[int] = mapped_column('7f7fba9ca9d4daebea81e66f51cc1984dda866bbd6521c51a0ad69636e438734', Integer, nullable=False)


class CggGoodsDatum(Base):
    __tablename__ = 'cgg_goods_data'

    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    shelf_position_id: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    detail_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)


class CharaETicketDatum(Base):
    __tablename__ = 'chara_e_ticket_data'

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    jewel_store_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class CharaFortuneRail(Base):
    __tablename__ = 'chara_fortune_rail'

    rail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gimmick_1_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_7_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_8_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_5_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_1_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_2_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_6_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_7_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_3_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_9_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_9_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_8_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_10_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_4_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_10_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_6_id: Mapped[str] = mapped_column(Text, nullable=False)
    gimmick_4_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_5_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_2_x: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_3_x: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaFortuneReward(Base):
    __tablename__ = 'chara_fortune_reward'

    count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fortune_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaFortuneScenario(Base):
    __tablename__ = 'chara_fortune_scenario'

    rail_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    scenario_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_2: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaFortuneSchedule(Base):
    __tablename__ = 'chara_fortune_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    fortune_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class CharaIdentity(Base):
    __tablename__ = 'chara_identity'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_type: Mapped[int] = mapped_column(Integer, nullable=False)


class CharaStoryStatus(Base):
    __tablename__ = 'chara_story_status'

    status_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_name: Mapped[str] = mapped_column(Text, nullable=False)
    chara_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_3: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_5: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    status_rate_1: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class CharacterLoveRankupText(Base):
    __tablename__ = 'character_love_rankup_text'

    chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    serif_1: Mapped[str] = mapped_column(Text, nullable=False)
    serif_3: Mapped[str] = mapped_column(Text, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    scale: Mapped[float] = mapped_column(REAL, nullable=False)
    face_3: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    serif_2: Mapped[str] = mapped_column(Text, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    face_1: Mapped[int] = mapped_column(Integer, nullable=False)
    face_2: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattle2BossDatum(Base):
    __tablename__ = 'clan_battle_2_boss_data'

    map_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    tap_height_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    tap_width_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    map_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_thumb_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cursor_position: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    scale_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattle2MapDatum(Base):
    __tablename__ = 'clan_battle_2_map_data'

    boss_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_3: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_from: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_4: Mapped[float] = mapped_column(REAL, nullable=False)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    damage_rank_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_5: Mapped[float] = mapped_column(REAL, nullable=False)
    score_coefficient_1: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_2: Mapped[float] = mapped_column(REAL, nullable=False)
    lap_num_to: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _9839d7b3914c87cc1bfc2fe48f919e352a579e1194ff638265860d675405972a: Mapped[int] = mapped_column('9839d7b3914c87cc1bfc2fe48f919e352a579e1194ff638265860d675405972a', Integer, nullable=False)


class ClanBattleArchiveClanRank(Base):
    __tablename__ = 'clan_battle_archive_clan_rank'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleArchivePersonRank(Base):
    __tablename__ = 'clan_battle_archive_person_rank'

    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleBattleMissionDatum(Base):
    __tablename__ = 'clan_battle_battle_mission_data'

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class ClanBattleBossDamageRank(Base):
    __tablename__ = 'clan_battle_boss_damage_rank'

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleBossFixReward(Base):
    __tablename__ = 'clan_battle_boss_fix_reward'

    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleLastAttackReward(Base):
    __tablename__ = 'clan_battle_last_attack_reward'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleOddsDatum(Base):
    __tablename__ = 'clan_battle_odds_data'

    odds_csv_3: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_9: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_2: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_5: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_4: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_1: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_8: Mapped[str] = mapped_column(Text, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_csv_10: Mapped[str] = mapped_column(Text, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_csv_7: Mapped[str] = mapped_column(Text, nullable=False)
    odds_csv_6: Mapped[str] = mapped_column(Text, nullable=False)


class ClanBattleParamAdjust(Base):
    __tablename__ = 'clan_battle_param_adjust'

    normal_atk_cast_time: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattlePeriod(Base):
    __tablename__ = 'clan_battle_period'

    interval_end: Mapped[str] = mapped_column(Text, nullable=False)
    result_start: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    calc_start: Mapped[str] = mapped_column(Text, nullable=False)
    min_carry_over_time: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail: Mapped[str] = mapped_column(Text, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_rehearsal_label_height: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    period_detail_s: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_detail_bg_s: Mapped[int] = mapped_column(Integer, nullable=False)
    result_end: Mapped[str] = mapped_column(Text, nullable=False)
    period_detail_boss_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_start: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class ClanBattlePeriodLapReward(Base):
    __tablename__ = 'clan_battle_period_lap_reward'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_from: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ranking_bonus_group: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattlePeriodRankReward(Base):
    __tablename__ = 'clan_battle_period_rank_reward'

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_bonus_group: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleRecommendDatum(Base):
    __tablename__ = 'clan_battle_recommend_data'

    magic_party_count: Mapped[int] = mapped_column(Integer, nullable=False)
    level_from: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_group: Mapped[int] = mapped_column(Integer, nullable=False)
    atack_party_count: Mapped[int] = mapped_column(Integer, nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level_to: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSBossDatum(Base):
    __tablename__ = 'clan_battle_s_boss_data'

    battle_report_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_width_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    map_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_height_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scale_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    cursor_position: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_thumb_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_report_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSBossFixReward(Base):
    __tablename__ = 'clan_battle_s_boss_fix_reward'

    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSMapDatum(Base):
    __tablename__ = 'clan_battle_s_map_data'

    extra_battle_flag2: Mapped[int] = mapped_column(Integer, nullable=False)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_3: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    last_attack_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_2: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    fix_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_from: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    aura_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    lap_num_to: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_4: Mapped[float] = mapped_column(REAL, nullable=False)
    fix_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _8ef26f934854b8ac0e05c48892a5fac84082f4c23df4e91726b3cd8fd1fbf54a: Mapped[int] = mapped_column('8ef26f934854b8ac0e05c48892a5fac84082f4c23df4e91726b3cd8fd1fbf54a', Integer, nullable=False)
    boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_1: Mapped[float] = mapped_column(REAL, nullable=False)
    damage_rank_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_battle_flag4: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient_5: Mapped[float] = mapped_column(REAL, nullable=False)


class ClanBattleSParamAdjust(Base):
    __tablename__ = 'clan_battle_s_param_adjust'

    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_atk_cast_time: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    param_adjust_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleSchedule(Base):
    __tablename__ = 'clan_battle_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    cc465f9a5ab8b3bee99b475b340ac6d5b6ef661c27a6cbd41fed94b70cec1e1b: Mapped[str] = mapped_column(Text, nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    point_per_stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_group_id_s: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    b6db198c84f70b67992bbacfb72ccc31600fdc487b36e603ff2b53d19def25ec: Mapped[str] = mapped_column(Text, nullable=False)
    _877a15acd0d6f644d4d6c509f9f72f65269a4c43a8e434bcfef53798fdd3de8a: Mapped[str] = mapped_column('877a15acd0d6f644d4d6c509f9f72f65269a4c43a8e434bcfef53798fdd3de8a', Text, nullable=False)
    map_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    release_month: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    last_clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ClanBattleTrainingDatum(Base):
    __tablename__ = 'clan_battle_training_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    map_data_id: Mapped[int] = mapped_column(Integer, nullable=False)
    training_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanBattleTrainingSchedule(Base):
    __tablename__ = 'clan_battle_training_schedule'

    clan_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    battle_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    training_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interval_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    battle_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class ClanCostGroup(Base):
    __tablename__ = 'clan_cost_group'

    cost_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanGrade(Base):
    __tablename__ = 'clan_grade'

    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_grade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanInviteLevelGroup(Base):
    __tablename__ = 'clan_invite_level_group'

    level_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_level_to: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, nullable=False)


class ClanprofileContent(Base):
    __tablename__ = 'clanprofile_content'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class ColosseumEnhanceDatum(Base):
    __tablename__ = 'colosseum_enhance_data'

    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumMissionDatum(Base):
    __tablename__ = 'colosseum_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumMissionRewardDatum(Base):
    __tablename__ = 'colosseum_mission_reward_data'

    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumQuestDatum(Base):
    __tablename__ = 'colosseum_quest_data'

    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    princess_knight_enhance_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    display_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class ColosseumScheduleDatum(Base):
    __tablename__ = 'colosseum_schedule_data'

    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dd4c5e8236f596ebf830eb4b0e77b7cb7d94d08d7ba7a92b21bd59481abed143: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    d14b3487c7e188ad87815657eb71dc94c497618a63c8dae5291b30acdd158388: Mapped[str] = mapped_column(Text, nullable=False)


class ColosseumScore(Base):
    __tablename__ = 'colosseum_score'

    bonus_param_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time_pt_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_pos_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_param_1: Mapped[int] = mapped_column(Integer, nullable=False)
    win_pt: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_pt_1: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_pt_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_pos_1: Mapped[int] = mapped_column(Integer, nullable=False)


class CombinedResultMotion(Base):
    __tablename__ = 'combined_result_motion'

    disp_order_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_1: Mapped[int] = mapped_column(Integer, nullable=False)
    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class ContentMapDatum(Base):
    __tablename__ = 'content_map_data'

    content_map_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_y: Mapped[int] = mapped_column(Integer, nullable=False)


class ContentReleaseDatum(Base):
    __tablename__ = 'content_release_data'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dialog: Mapped[str] = mapped_column(Text, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level: Mapped[int] = mapped_column(Integer, nullable=False)


class ContentsReleaseCondition(Base):
    __tablename__ = 'contents_release_condition'

    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)


class CooperationQuestDatum(Base):
    __tablename__ = 'cooperation_quest_data'

    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    sub_enemy_image_wave_1_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False)
    cooperation_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_2_4: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    first_reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    sub_enemy_image_wave_2_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_2_1: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_enemy_image_wave_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    repeat_reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_enemy_image_wave_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_1: Mapped[int] = mapped_column(Integer, nullable=False)
    repeat_reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_1_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    sub_enemy_image_wave_3_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_enemy_image_wave_1: Mapped[int] = mapped_column(Integer, nullable=False)
    exp: Mapped[int] = mapped_column(Integer, nullable=False)
    repeat_reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    lobby_background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_comment: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    first_reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_3_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_enemy_image_wave_2_2: Mapped[int] = mapped_column(Integer, nullable=False)
    cooperation_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)


class CustomMypage(Base):
    __tablename__ = 'custom_mypage'

    still_name: Mapped[str] = mapped_column(Text, nullable=False)
    mypage_type: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_direction: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    still_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    vertical_still_flg: Mapped[int] = mapped_column(Integer, nullable=False)


class CustomMypageGroup(Base):
    __tablename__ = 'custom_mypage_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(Text, nullable=False)


class DailyMissionDatum(Base):
    __tablename__ = 'daily_mission_data'

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    title_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)


class DearChara(Base):
    __tablename__ = 'dear_chara'

    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)
    episode_unlock_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    max_dear_point: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point_up_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    episode_unlock_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chara_name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    dear_point_up_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)


class DearReward(Base):
    __tablename__ = 'dear_reward'

    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    dear_point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)


class DearSetting(Base):
    __tablename__ = 'dear_setting'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tutorial_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    system_name: Mapped[str] = mapped_column(Text, nullable=False)


class DearStoryDatum(Base):
    __tablename__ = 'dear_story_data'

    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class DearStoryDetail(Base):
    __tablename__ = 'dear_story_detail'

    condition_event_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_event_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)


class DefineSpskill(Base):
    __tablename__ = 'define_spskill'

    link_skill_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    sp_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    base_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_category: Mapped[int] = mapped_column(Integer, nullable=False)


class DodgeTpRecovery(Base):
    __tablename__ = 'dodge_tp_recovery'

    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recovery_ratio: Mapped[float] = mapped_column(REAL, nullable=False)


class DomeBattleEffect(Base):
    __tablename__ = 'dome_battle_effect'

    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class DomeMissionDatum(Base):
    __tablename__ = 'dome_mission_data'

    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_icon_on_bar: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeMissionRewardDatum(Base):
    __tablename__ = 'dome_mission_reward_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeQuestChallengeDatum(Base):
    __tablename__ = 'dome_quest_challenge_data'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    challenge_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    challenge_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeQuestDatum(Base):
    __tablename__ = 'dome_quest_data'

    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    challenge_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    display_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    round_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_effect_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ea2fbd792ffabd6c271ce7621d82e1e4586af58d1012ace06a8da06c0931b00b: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeQuestReward(Base):
    __tablename__ = 'dome_quest_reward'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)


class DomeScheduleDatum(Base):
    __tablename__ = 'dome_schedule_data'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class DomeUnitEnhanceDatum(Base):
    __tablename__ = 'dome_unit_enhance_data'

    equipment_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_2: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_level_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)


class DsbDramaScript(Base):
    __tablename__ = 'dsb_drama_script'

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class DsbStoryDatum(Base):
    __tablename__ = 'dsb_story_data'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    article_text: Mapped[str] = mapped_column(Text, nullable=False)
    effect_text: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    day_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guest_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    material_text: Mapped[str] = mapped_column(Text, nullable=False)


class DungeonArea(Base):
    __tablename__ = 'dungeon_area'

    dungeon_name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_level: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_clear_story: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    open_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_release_story: Mapped[int] = mapped_column(Integer, nullable=False)
    open_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonAreaDatum(Base):
    __tablename__ = 'dungeon_area_data'

    initial_clear_story: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    _6b8bd3865cad599289de5685fd7267a9563bb32c7e736f033fc810c7b7fec186: Mapped[int] = mapped_column('6b8bd3865cad599289de5685fd7267a9563bb32c7e736f033fc810c7b7fec186', Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    c0654625975507ff3140bb0ffe500408f01389294438eff0ef0ff64b3bffe695: Mapped[int] = mapped_column(Integer, nullable=False)
    _8ff9154d35336deaccfd3699e53450de96884008876779f89e155ac7a0ed5b32: Mapped[int] = mapped_column('8ff9154d35336deaccfd3699e53450de96884008876779f89e155ac7a0ed5b32', Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    f4ee34013eff1c932f8566e97413d67a6fd6dc9d96203c06d28b6a1864b69249: Mapped[int] = mapped_column(Integer, nullable=False)
    open_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _297c4232000624568b7174b6fdc61d335dbe50f846a83b213637e822f607bd4f: Mapped[int] = mapped_column('297c4232000624568b7174b6fdc61d335dbe50f846a83b213637e822f607bd4f', Integer, nullable=False)
    dungeon_name: Mapped[str] = mapped_column(Text, nullable=False)
    content_release_story: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    _2342351e1d94247e7b5777580c637037e72a45f5c477a56129745d003b6e2fb5: Mapped[int] = mapped_column('2342351e1d94247e7b5777580c637037e72a45f5c477a56129745d003b6e2fb5', Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _6ead63dcf54ac7c47772684c5a420c17a452399485ed9eba3babd2d423b3c6c0: Mapped[int] = mapped_column('6ead63dcf54ac7c47772684c5a420c17a452399485ed9eba3babd2d423b3c6c0', Integer, nullable=False)
    _5bef987da94f25e68b2eb8d210e93b1961e3fdef7e33b9d915eb9d1a615d4610: Mapped[str] = mapped_column('5bef987da94f25e68b2eb8d210e93b1961e3fdef7e33b9d915eb9d1a615d4610', Text, nullable=False)
    dungeon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    ba072d599c25cac590f86084721ae29fc50e92a983ea6d72d860d9f4d5a496f5: Mapped[int] = mapped_column(Integer, nullable=False)
    _8e05bf70d736c36a7fc2174d2994cb5f520ce8b1993545b37f9082c056f3173e: Mapped[int] = mapped_column('8e05bf70d736c36a7fc2174d2994cb5f520ce8b1993545b37f9082c056f3173e', Integer, nullable=False)
    recommend_level: Mapped[int] = mapped_column(Integer, nullable=False)
    e5746529cba54059fb44d4ea0317adfcc461796564909a2a21e690f54e8b24d9: Mapped[int] = mapped_column(Integer, nullable=False)
    _0bb3e332ae636ead84266a17d11a5afe247d95c022f14b59434b524f2a4d3750: Mapped[str] = mapped_column('0bb3e332ae636ead84266a17d11a5afe247d95c022f14b59434b524f2a4d3750', Text, nullable=False)
    a7d1b54f8d36178d35b922380f29c52f20cfccf325d2f398d18d08760618444f: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonPatternBattle(Base):
    __tablename__ = 'dungeon_pattern_battle'

    trigger_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_monster_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    pattern: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_monster_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_monster_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    next_pattern_2: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_monster_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    next_pattern_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonQuestDatum(Base):
    __tablename__ = 'dungeon_quest_data'

    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    _2b66822ba6809487dd234e52967502877b27f365bb6a75587352981e8e1d76aa: Mapped[float] = mapped_column('2b66822ba6809487dd234e52967502877b27f365bb6a75587352981e8e1d76aa', REAL, nullable=False)
    emax: Mapped[int] = mapped_column(Integer, nullable=False)
    _2010fad5abaf64353273a35c88cd9a5feea14c389ccf44b65c5bcf3d84bb6d7c: Mapped[int] = mapped_column('2010fad5abaf64353273a35c88cd9a5feea14c389ccf44b65c5bcf3d84bb6d7c', Integer, nullable=False)
    energy_reset_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_6: Mapped[int] = mapped_column(Integer, nullable=False)
    fd6b6ec56c0999c989415553f637097adfdc621ffacf28fe0876bf8411f36c84: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    dungeon_quest_detail_monster_position_x_2: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_type: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_height: Mapped[float] = mapped_column(REAL, nullable=False)
    multi_target_effect_time: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonSkipDatum(Base):
    __tablename__ = 'dungeon_skip_data'

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_motion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonSpecialBattle(Base):
    __tablename__ = 'dungeon_special_battle'

    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)
    special_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)


class DungeonSpecialEnemySetting(Base):
    __tablename__ = 'dungeon_special_enemy_setting'
    __table_args__ = (
        UniqueConstraint('special_battle_id', 'disp_order'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_offset_y: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_identify: Mapped[int] = mapped_column(Integer, nullable=False)
    special_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    must_kill_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class DvsStoryDatum(Base):
    __tablename__ = 'dvs_story_data'

    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    _136657d3be67a4603e5f585782382553762b6a23a878f1617ba6ddafe8e184cc: Mapped[int] = mapped_column('136657d3be67a4603e5f585782382553762b6a23a878f1617ba6ddafe8e184cc', Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    dvs_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    detail_title: Mapped[str] = mapped_column(Text, nullable=False)


class EReduction(Base):
    __tablename__ = 'e_reduction'

    value_4: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    border: Mapped[int] = mapped_column(Integer, nullable=False)
    value_5: Mapped[float] = mapped_column(REAL, nullable=False)
    value_3: Mapped[float] = mapped_column(REAL, nullable=False)
    threshold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_2: Mapped[float] = mapped_column(REAL, nullable=False)
    threshold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[float] = mapped_column(REAL, nullable=False)
    threshold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold_4: Mapped[int] = mapped_column(Integer, nullable=False)


class EmblemDatum(Base):
    __tablename__ = 'emblem_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_name: Mapped[str] = mapped_column(Text, nullable=False)
    description_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_emblem: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_oder: Mapped[int] = mapped_column(Integer, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EmblemMissionDatum(Base):
    __tablename__ = 'emblem_mission_data'

    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)


class EmblemMissionRewardDatum(Base):
    __tablename__ = 'emblem_mission_reward_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyEnableVoice(Base):
    __tablename__ = 'enemy_enable_voice'

    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyIgnoreSkillRf(Base):
    __tablename__ = 'enemy_ignore_skill_rf'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EnemyMParts(Base):
    __tablename__ = 'enemy_m_parts'

    child_enemy_parameter_4: Mapped[int] = mapped_column(Integer, nullable=False)
    child_enemy_parameter_1: Mapped[int] = mapped_column(Integer, nullable=False)
    child_enemy_parameter_3: Mapped[int] = mapped_column(Integer, nullable=False)
    a67bb16839d66b7d683dc34687c42381ad7a7491c3dd343d638badd969dc814c: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_enemy_parameter_5: Mapped[int] = mapped_column(Integer, nullable=False)
    child_enemy_parameter_2: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyParameter(Base):
    __tablename__ = 'enemy_parameter'

    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyRewardDatum(Base):
    __tablename__ = 'enemy_reward_data'

    odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class EnemyTalentWeakness(Base):
    __tablename__ = 'enemy_talent_weakness'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resist_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EnvironmentSkillDetail(Base):
    __tablename__ = 'environment_skill_detail'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EquipmentCraft(Base):
    __tablename__ = 'equipment_craft'

    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_equipment_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    crafted_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_equipment_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)


class EquipmentDatum(Base):
    __tablename__ = 'equipment_data'

    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_type: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_name: Mapped[str] = mapped_column(Text, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    require_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    sale_price: Mapped[int] = mapped_column(Integer, nullable=False)
    craft_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_category: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    display_item: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    original_equipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    enable_donation: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_enhance_point: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EquipmentDonation(Base):
    __tablename__ = 'equipment_donation'

    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    donation_num_daily: Mapped[int] = mapped_column(Integer, nullable=False)
    request_num_once: Mapped[int] = mapped_column(Integer, nullable=False)
    donation_num_once: Mapped[int] = mapped_column(Integer, nullable=False)


class EquipmentEnhanceDatum(Base):
    __tablename__ = 'equipment_enhance_data'

    total_point: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_point: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class EquipmentEnhanceRate(Base):
    __tablename__ = 'equipment_enhance_rate'

    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    _73f9f300c8e251d4ec0555399dc97e3673965fedff5346b990d261d37dd6f741: Mapped[str] = mapped_column('73f9f300c8e251d4ec0555399dc97e3673965fedff5346b990d261d37dd6f741', Text, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    f46ce48c3c3cf05a552b71464601c856a3d4dc3a3c40e1d49e6f1e8d6d35e5f1: Mapped[str] = mapped_column(Text, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    _281f93cf334bc9daee92ed2c67f686f9b18fb4c975b3efe7dd0230df8633ffce: Mapped[int] = mapped_column('281f93cf334bc9daee92ed2c67f686f9b18fb4c975b3efe7dd0230df8633ffce', Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)


class EventBgDatum(Base):
    __tablename__ = 'event_bg_data'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EventBossTreasureBox(Base):
    __tablename__ = 'event_boss_treasure_box'

    event_boss_treasure_content_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_9: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_box_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_boss_treasure_content_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_8: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_7: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    event_boss_treasure_content_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_6: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    each_odds_1: Mapped[int] = mapped_column(Integer, nullable=False)


class EventBossTreasureContent(Base):
    __tablename__ = 'event_boss_treasure_content'

    event_boss_treasure_content_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_3: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_5: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_2: Mapped[str] = mapped_column(Text, nullable=False)
    odds_file_1: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_file_4: Mapped[str] = mapped_column(Text, nullable=False)
    odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class EventEffectSetting(Base):
    __tablename__ = 'event_effect_setting'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class EventEnemyParameter(Base):
    __tablename__ = 'event_enemy_parameter'

    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)


class EventEnemyRewardGroup(Base):
    __tablename__ = 'event_enemy_reward_group'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventGachaDatum(Base):
    __tablename__ = 'event_gacha_data'

    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repeat_step: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)


class EventIntroduction(Base):
    __tablename__ = 'event_introduction'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    maximum_chunk_size_1: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    introduction_number: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    maximum_chunk_size_loop_2: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_loop_3: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    maximum_chunk_size_loop_1: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_3: Mapped[int] = mapped_column(Integer, nullable=False)


class EventNaviComment(Base):
    __tablename__ = 'event_navi_comment'

    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class EventNaviCommentCondition(Base):
    __tablename__ = 'event_navi_comment_condition'

    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)


class EventReminder(Base):
    __tablename__ = 'event_reminder'

    btn_text: Mapped[str] = mapped_column(Text, nullable=False)
    notice_text: Mapped[str] = mapped_column(Text, nullable=False)
    title_text: Mapped[str] = mapped_column(Text, nullable=False)
    description_text: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reminder_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventReminderCondition(Base):
    __tablename__ = 'event_reminder_condition'

    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reminder_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EventRevivalSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_revival_series_wave_group_data'

    _39ba849d0c663a8acd0e21cca4dfde56df6b692f23c2593a9bccd0cccfa37e78: Mapped[int] = mapped_column('39ba849d0c663a8acd0e21cca4dfde56df6b692f23c2593a9bccd0cccfa37e78', Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    d20bcabef2b0ba6953768d0d2031ab0893e2b8900819a52fe7807bc0cc3c2eb9: Mapped[int] = mapped_column(Integer, nullable=False)
    _71c10fb6da2100e6492a0a06660ffbffc46db80de6570992968b71083dc3c96c: Mapped[int] = mapped_column('71c10fb6da2100e6492a0a06660ffbffc46db80de6570992968b71083dc3c96c', Integer, nullable=False)
    _446c632ff85fd3ffd2222d04c3a6f7d291f5f1b8b2041794a1f1b72fbec9c755: Mapped[int] = mapped_column('446c632ff85fd3ffd2222d04c3a6f7d291f5f1b8b2041794a1f1b72fbec9c755', Integer, nullable=False)
    _3690b18132caf2eb9e403fb913bbfca5b849348cc15a8eda9a63a06f4eb17da9: Mapped[int] = mapped_column('3690b18132caf2eb9e403fb913bbfca5b849348cc15a8eda9a63a06f4eb17da9', Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _547798650c98772e79a799c46081039a5fa933df96780e371a01b35e032fa768: Mapped[int] = mapped_column('547798650c98772e79a799c46081039a5fa933df96780e371a01b35e032fa768', Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _824d2328daf89a5923bed4f6e23e0dae0e13e1ad50602fbee6d703a6261aba4e: Mapped[int] = mapped_column('824d2328daf89a5923bed4f6e23e0dae0e13e1ad50602fbee6d703a6261aba4e', Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    e7c598d176a22c6a67909644b10c7939528e1c670fdfef435f8ee21172cc9ab4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    _6a94337554fd18732b5a541b1b2caca0601c34b2f942d61110ed2ea99a10f361: Mapped[int] = mapped_column('6a94337554fd18732b5a541b1b2caca0601c34b2f942d61110ed2ea99a10f361', Integer, nullable=False)
    _811194b8172ed3924b77df087f99ee9775342496821743deb6adfa0685e74203: Mapped[int] = mapped_column('811194b8172ed3924b77df087f99ee9775342496821743deb6adfa0685e74203', Integer, nullable=False)
    _495db657ab083b38cd78cd6da48217247da7569d1e20bea72d77650e0347e549: Mapped[int] = mapped_column('495db657ab083b38cd78cd6da48217247da7569d1e20bea72d77650e0347e549', Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    _743729b18e9decfea186adaef2178e4950ecb659c8f8bb6cbb70e9d1f07a8cde: Mapped[int] = mapped_column('743729b18e9decfea186adaef2178e4950ecb659c8f8bb6cbb70e9d1f07a8cde', Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    a2f1049e0661d51391c9923b6a7cc71180b8d41e74cfd23cd3839773a9b856ed: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _9250304ab483b8822c50c0951e111ee8456400366b3ca3d5d5b11caa694c277e: Mapped[int] = mapped_column('9250304ab483b8822c50c0951e111ee8456400366b3ca3d5d5b11caa694c277e', Integer, nullable=False)
    f3bd6b653c5e97e6d413b9b64cc6ccfdb78a1d654adf307e662ecc936da359c7: Mapped[int] = mapped_column(Integer, nullable=False)
    _9ce6a8695336444ef098e0c82d2128a7fa60d93d224dab81d1881d8a672238a9: Mapped[int] = mapped_column('9ce6a8695336444ef098e0c82d2128a7fa60d93d224dab81d1881d8a672238a9', Integer, nullable=False)
    _06caf65d0ec5c23e408433f132c6e9944231d25d8edb601197dbd18359f57968: Mapped[int] = mapped_column('06caf65d0ec5c23e408433f132c6e9944231d25d8edb601197dbd18359f57968', Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    _675bdfef384ffc2b06990db9c444d25846c5447043e43a209ae99ca53baae953: Mapped[int] = mapped_column('675bdfef384ffc2b06990db9c444d25846c5447043e43a209ae99ca53baae953', Integer, nullable=False)
    _18630b84f6ec94b5ee58de616d7725b669f6e0c67249d6e746c840583dfb86d4: Mapped[int] = mapped_column('18630b84f6ec94b5ee58de616d7725b669f6e0c67249d6e746c840583dfb86d4', Integer, nullable=False)
    a0fb82da29933f04f7ca7c95f43cd720fbd3eeea55df01bf244ef2c9b699e2fa: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _28ac95bfce00bd86a316a24744bc8ac8c81cd8e33cbd1c260e0006123502180e: Mapped[int] = mapped_column('28ac95bfce00bd86a316a24744bc8ac8c81cd8e33cbd1c260e0006123502180e', Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    c7a2ae1dba58e3229acb9c187e1170c7a930fae29db18485205e8bd8b622f182: Mapped[int] = mapped_column(Integer, nullable=False)
    _390eb56845f1f8781b3502cf12c7a08c0f8c72da11a5e6d84f94a8d6d686f07b: Mapped[int] = mapped_column('390eb56845f1f8781b3502cf12c7a08c0f8c72da11a5e6d84f94a8d6d686f07b', Integer, nullable=False)
    _95a24a90806b01f8dc0827febea529e8cc744388caf63f61c388e3524017a247: Mapped[int] = mapped_column('95a24a90806b01f8dc0827febea529e8cc744388caf63f61c388e3524017a247', Integer, nullable=False)


class EventRevivalWaveGroupDatum(Base):
    __tablename__ = 'event_revival_wave_group_data'

    _3f5a035fd5ebddbaa861a86a5da039b319e968b6bb6c5829887b69c72998bba8: Mapped[int] = mapped_column('3f5a035fd5ebddbaa861a86a5da039b319e968b6bb6c5829887b69c72998bba8', Integer, nullable=False)
    e1423d06700d408891ab956ea5e12b39d7cd6510f61ba079aacce8f70f601cd9: Mapped[int] = mapped_column(Integer, nullable=False)
    d2ceaeac36a1eba504a49a55778c84439bb8eeca031e3a271780fb9f603d57f9: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    a8429b1f29bcb7a272b9aa56fa4a82de011a025e9541027b67335a093ba60293: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    b164d613336b82afc69f1e587f3d52ad781cc55782d22ff8e15e20ff69f97799: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _6e5126dc204a33b7ca68832e366f93f14c3df72447deedfe0f33cde103ee8b5e: Mapped[int] = mapped_column('6e5126dc204a33b7ca68832e366f93f14c3df72447deedfe0f33cde103ee8b5e', Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _4b9a32c08d030864ad1f2a0059b656aaac53713fa1e152bd0e552301d242ac04: Mapped[int] = mapped_column('4b9a32c08d030864ad1f2a0059b656aaac53713fa1e152bd0e552301d242ac04', Integer, nullable=False)
    _5155c5adc88da9fab88575c98cecaf4a8fc286ec5c74d12f8689684819f29d0c: Mapped[int] = mapped_column('5155c5adc88da9fab88575c98cecaf4a8fc286ec5c74d12f8689684819f29d0c', Integer, nullable=False)
    _86e1732f754b9a453ec378c1b595fe1c1ba4c7ce9e1fa8119df00a86b649a18c: Mapped[int] = mapped_column('86e1732f754b9a453ec378c1b595fe1c1ba4c7ce9e1fa8119df00a86b649a18c', Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _7a001df8ab7332406b2e05f49a40e671fb1782beada6f44e2c40860c3e4dc1e6: Mapped[int] = mapped_column('7a001df8ab7332406b2e05f49a40e671fb1782beada6f44e2c40860c3e4dc1e6', Integer, nullable=False)
    _055922e0d5d07292fb6131bd3743f2bb779bdc33a626bba0ead90de74dad00dd: Mapped[int] = mapped_column('055922e0d5d07292fb6131bd3743f2bb779bdc33a626bba0ead90de74dad00dd', Integer, nullable=False)
    df1fa3ac5209dec2167790bb983e31cd6c7f49874776a301a11a74b2ca82ea0d: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    _7c0b5906e38589d104302d8cebc0336d08ee9e516a96ae97c22d01a4ae22b4b9: Mapped[int] = mapped_column('7c0b5906e38589d104302d8cebc0336d08ee9e516a96ae97c22d01a4ae22b4b9', Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    _91815e4855e0e4fe3c20dca9c246952651cb16da5a5a9b1749ad0c418609f6c3: Mapped[int] = mapped_column('91815e4855e0e4fe3c20dca9c246952651cb16da5a5a9b1749ad0c418609f6c3', Integer, nullable=False)
    a9b226f0a3eac434035d514dc8b0f711494f23385c0797f9a77e608d665665c1: Mapped[int] = mapped_column(Integer, nullable=False)
    d9f16e4afdd740c36c87deec82f1e2c72df50cd60573269261cd7273b2b01b0f: Mapped[int] = mapped_column(Integer, nullable=False)
    cffc73377dfac584b90ca346e6e140d942fa2cf1a8e2a9aff29f99bf707aaf23: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bcd833da42475f1aacdc14aefb6137e6b06d39956f216c57b066ff37123365c4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ff4079cc567979195792e3ac37326afa903794bc85ada47e276f806ef535d2d8: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    dd7c91b1c452e28df7a5db5e71e771914d433aefffbee5ad3b805717b951bf65: Mapped[int] = mapped_column(Integer, nullable=False)
    ba87eabe2c45117165e5cec03471970744e47ce378029e7912d3d14a7a8c5253: Mapped[int] = mapped_column(Integer, nullable=False)
    _2fbfbe7da31be7f13afadeb554a7aa96a3c4c86f17935c9d7c4f360b3e7dd80d: Mapped[int] = mapped_column('2fbfbe7da31be7f13afadeb554a7aa96a3c4c86f17935c9d7c4f360b3e7dd80d', Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    _4282cbf4bc042b0d67524b73a61d6f3edd12dd1d4a32552ef9fa17ae7fffa241: Mapped[int] = mapped_column('4282cbf4bc042b0d67524b73a61d6f3edd12dd1d4a32552ef9fa17ae7fffa241', Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _1419f40411c8d28cc4b99a06a6d607a5afbd7720c9669f7b16fb026256b30957: Mapped[int] = mapped_column('1419f40411c8d28cc4b99a06a6d607a5afbd7720c9669f7b16fb026256b30957', Integer, nullable=False)


class EventSeriesWaveGroupDatum(Base):
    __tablename__ = 'event_series_wave_group_data'

    ba4926d6470044bcb4e9858aad2e52a87c201ec2de550247eb4b4dea44edd8fa: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    eddb4e5206f6257f3c3d6964f4bf59e3e687d6eb359ebab8c0e6701b675388f1: Mapped[int] = mapped_column(Integer, nullable=False)
    _81fcd36cc8973dc2330b2334ff09ef0a90e9b158b18cdb35071f9cb6a5f16391: Mapped[int] = mapped_column('81fcd36cc8973dc2330b2334ff09ef0a90e9b158b18cdb35071f9cb6a5f16391', Integer, nullable=False)
    _4f20b88fc6640cfdd6256b8c396966e678280d8d5315e640ef8018b53389b024: Mapped[int] = mapped_column('4f20b88fc6640cfdd6256b8c396966e678280d8d5315e640ef8018b53389b024', Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _5ef42abdebfb7f88a6bf2d6342304e343c595d33c0ff041d647664858124ae44: Mapped[int] = mapped_column('5ef42abdebfb7f88a6bf2d6342304e343c595d33c0ff041d647664858124ae44', Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    _49ed9d40568ff724dffaab822f45782301479fc4965cd7e19278c8ede757f716: Mapped[int] = mapped_column('49ed9d40568ff724dffaab822f45782301479fc4965cd7e19278c8ede757f716', Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    _10c0a7a21facf314a45c7fe544ede99d2a6ce268b937b391522c5d69ec90cd86: Mapped[int] = mapped_column('10c0a7a21facf314a45c7fe544ede99d2a6ce268b937b391522c5d69ec90cd86', Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ba1ecb2d7a5877aca2cb9eb8b6b5a8e24c5a4408b0a06024b8c7a190b8f69d59: Mapped[int] = mapped_column(Integer, nullable=False)
    cbb8c5d852b621eee60dd4cb4364f34701e087294721b6b11c1290ace7df07cd: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _4e167b06bd3f8c89ac9dbbc50f7e56a2f0af53720cb21457e8b4db0e2a124091: Mapped[int] = mapped_column('4e167b06bd3f8c89ac9dbbc50f7e56a2f0af53720cb21457e8b4db0e2a124091', Integer, nullable=False)
    _977377ee84eb5a42af57fe97cea05454361422b1f005b2b760f6b515596c47c8: Mapped[int] = mapped_column('977377ee84eb5a42af57fe97cea05454361422b1f005b2b760f6b515596c47c8', Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    b2a25d94c84e6e0c3ce9bd8bb04688a6cde3eeac29f0019e2c1df1045df87e1c: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _6d017fd5d6a450edc05a432bc95b4b07205e3100793ad71730f22d1995f704e9: Mapped[int] = mapped_column('6d017fd5d6a450edc05a432bc95b4b07205e3100793ad71730f22d1995f704e9', Integer, nullable=False)
    _8c8e70adeeebd175db2002b2f1f14221ee7e7717dce85c8654cd7d016abb552e: Mapped[int] = mapped_column('8c8e70adeeebd175db2002b2f1f14221ee7e7717dce85c8654cd7d016abb552e', Integer, nullable=False)
    f0e9df4268bc29c4989824d9fb0af8308266093c322677fc9505720c556a4eb0: Mapped[int] = mapped_column(Integer, nullable=False)
    _20af4f4198851dbd17535fd10a4704eb328869f1f3851290a2223e16b1bd39af: Mapped[int] = mapped_column('20af4f4198851dbd17535fd10a4704eb328869f1f3851290a2223e16b1bd39af', Integer, nullable=False)
    _5ea2b82b62f9f8b137802cb783b9e98bd43ef5b5a6d7748d6685d91df707c96b: Mapped[int] = mapped_column('5ea2b82b62f9f8b137802cb783b9e98bd43ef5b5a6d7748d6685d91df707c96b', Integer, nullable=False)
    _2625d0d7d99a372e57553a82b25f8902b566fe4bb7f954674058239e93767dd7: Mapped[int] = mapped_column('2625d0d7d99a372e57553a82b25f8902b566fe4bb7f954674058239e93767dd7', Integer, nullable=False)
    _2f0a734374b6c2d20e07c1fa0ef60619625e3fff3a09a658a56c8f4052caf5ec: Mapped[int] = mapped_column('2f0a734374b6c2d20e07c1fa0ef60619625e3fff3a09a658a56c8f4052caf5ec', Integer, nullable=False)
    e11c2587c23e683b856f68a886795e451fd456c8d4e18ceb99c314192a08ed97: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    _9a53fbbbaa0d23aec4d6bdf69aad96a3942ada297c217905be38eb3c203cd5e0: Mapped[int] = mapped_column('9a53fbbbaa0d23aec4d6bdf69aad96a3942ada297c217905be38eb3c203cd5e0', Integer, nullable=False)
    b3222a2a064e1007dd2cc66224bc538d5f5d97d28dad387690d99a5933e12506: Mapped[int] = mapped_column(Integer, nullable=False)
    c711768f6264ca6f47e1dfda577c31dd751a2de9600b00df25bbdb7a662d836c: Mapped[int] = mapped_column(Integer, nullable=False)
    cc50760462ce8c4696a5dffb2ea28162db8c661692ee850b02eda00420edb190: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class EventStoryDatum(Base):
    __tablename__ = 'event_story_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class EventStoryDetail(Base):
    __tablename__ = 'event_story_detail'

    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class EventTopAdv(Base):
    __tablename__ = 'event_top_adv'

    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_top_adv_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class EventWaveGroupDatum(Base):
    __tablename__ = 'event_wave_group_data'

    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    match_lv_min: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_lv_max: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentCategory(Base):
    __tablename__ = 'ex_equipment_category'

    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    outline: Mapped[str] = mapped_column(Text, nullable=False)
    recycle_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_base: Mapped[str] = mapped_column(Text, nullable=False)


class ExEquipmentDatum(Base):
    __tablename__ = 'ex_equipment_data'

    default_wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    default_energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    default_hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    max_rank_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    max_atk: Mapped[int] = mapped_column(Integer, nullable=False)
    is_force_protected: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    max_wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    max_life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    max_energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_skill_power: Mapped[int] = mapped_column(Integer, nullable=False)
    max_magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    restriction_id: Mapped[int] = mapped_column(Integer, nullable=False)
    max_energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    default_physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    max_physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    max_accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    default_atk: Mapped[int] = mapped_column(Integer, nullable=False)
    max_dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    default_wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    default_dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    default_energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    default_physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    default_def: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_battle_equip_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    max_def: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_skill_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    max_physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    passive_skill_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    max_hp: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentEnhanceDatum(Base):
    __tablename__ = 'ex_equipment_enhance_data'

    rankup_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    needed_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    needed_point: Mapped[int] = mapped_column(Integer, nullable=False)
    total_point: Mapped[int] = mapped_column(Integer, nullable=False)


class ExEquipmentRankupDatum(Base):
    __tablename__ = 'ex_equipment_rankup_data'

    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rankup_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExEquipmentRecycleReward(Base):
    __tablename__ = 'ex_equipment_recycle_reward'

    enhance_pt_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    coin_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExEquipmentRestrictionUnit(Base):
    __tablename__ = 'ex_equipment_restriction_unit'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restriction_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExPlus(Base):
    __tablename__ = 'ex_plus'

    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    is_hide_boss: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)


class ExceedLevelStage(Base):
    __tablename__ = 'exceed_level_stage'

    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    general_exceed_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    increase_level_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ExceedLevelUnit(Base):
    __tablename__ = 'exceed_level_unit'

    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    exceed_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exceed_stage: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExceptEr(Base):
    __tablename__ = 'except_er'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExperienceKnightRank(Base):
    __tablename__ = 'experience_knight_rank'

    total_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    knight_rank: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExperienceTalentLevel(Base):
    __tablename__ = 'experience_talent_level'

    total_point: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_enhance_value: Mapped[int] = mapped_column(Integer, nullable=False)


class ExperienceTeam(Base):
    __tablename__ = 'experience_team'

    recover_stamina_count: Mapped[int] = mapped_column(Integer, nullable=False)
    over_limit_stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    total_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_stamina: Mapped[int] = mapped_column(Integer, nullable=False)


class ExperienceUnit(Base):
    __tablename__ = 'experience_unit'

    total_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class ExtraEffectDatum(Base):
    __tablename__ = 'extra_effect_data'

    target_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_4: Mapped[int] = mapped_column(Integer, nullable=False)
    set_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_3: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_1: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    exec_timing_2: Mapped[int] = mapped_column(Integer, nullable=False)


class ExtraEffectTargetRange(Base):
    __tablename__ = 'extra_effect_target_range'

    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    set_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ExtraEffectUnitGroup(Base):
    __tablename__ = 'extra_effect_unit_group'

    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class FbsSchedule(Base):
    __tablename__ = 'fbs_schedule'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    fbs_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class FixLineupGroupSet(Base):
    __tablename__ = 'fix_lineup_group_set'

    reward_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_8: Mapped[int] = mapped_column(Integer, nullable=False)
    lineup_group_set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_12: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_12: Mapped[int] = mapped_column(Integer, nullable=False)
    price_11: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_19: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_19: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_20: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_18: Mapped[int] = mapped_column(Integer, nullable=False)
    price_4: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    price_7: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    price_10: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_11: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_18: Mapped[int] = mapped_column(Integer, nullable=False)
    price_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_7: Mapped[int] = mapped_column(Integer, nullable=False)
    price_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_19: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_13: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    price_5: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_14: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    price_13: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)
    currency_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_13: Mapped[int] = mapped_column(Integer, nullable=False)
    price_14: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_17: Mapped[int] = mapped_column(Integer, nullable=False)
    price_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_17: Mapped[int] = mapped_column(Integer, nullable=False)
    price_12: Mapped[int] = mapped_column(Integer, nullable=False)
    price_6: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    price_16: Mapped[int] = mapped_column(Integer, nullable=False)
    price_17: Mapped[int] = mapped_column(Integer, nullable=False)
    price_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_16: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    price_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    price_19: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_11: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_11: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_17: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_12: Mapped[int] = mapped_column(Integer, nullable=False)
    price_18: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    price_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_20: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_14: Mapped[int] = mapped_column(Integer, nullable=False)
    price_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_14: Mapped[int] = mapped_column(Integer, nullable=False)
    currency_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    price_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_13: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_15: Mapped[int] = mapped_column(Integer, nullable=False)


class FixLineupGroupSetDatum(Base):
    __tablename__ = 'fix_lineup_group_set_data'

    reward_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    _3f8a222f64c95e85eb9fae03edba4aa808d26b3fb98d384f446206f2442c1479: Mapped[int] = mapped_column('3f8a222f64c95e85eb9fae03edba4aa808d26b3fb98d384f446206f2442c1479', Integer, nullable=False)
    d8b8823dc4fba8cdb89dc7c51b6087e71c7c5e511fa5d8c98a54d9d253bdc69b: Mapped[int] = mapped_column(Integer, nullable=False)
    b6c500aa23f2b910dd2574316bab3c44d037171146ddc569d280419322559406: Mapped[int] = mapped_column(Integer, nullable=False)
    _65e311d5419b86d09de91e1baccdbdb29ef3116e41176f097be1810ba3742aa2: Mapped[int] = mapped_column('65e311d5419b86d09de91e1baccdbdb29ef3116e41176f097be1810ba3742aa2', Integer, nullable=False)
    _216fd61263286bddce9be57a7a8c89e82e747f4cd2d4a4cfce7863aef888cfb4: Mapped[int] = mapped_column('216fd61263286bddce9be57a7a8c89e82e747f4cd2d4a4cfce7863aef888cfb4', Integer, nullable=False)
    d6ec9bf11791724e0f74bb1098c3f1974596d8bbdaea03376888c0e64d0eb451: Mapped[int] = mapped_column(Integer, nullable=False)
    _91188efc62c77970502859871f134f6d14d8552486553abed5be160b8af0fb2c: Mapped[int] = mapped_column('91188efc62c77970502859871f134f6d14d8552486553abed5be160b8af0fb2c', Integer, nullable=False)
    _191086f4e482cbfe5b565f7348b29677d7ced93d96d4eba32ad564da55442404: Mapped[int] = mapped_column('191086f4e482cbfe5b565f7348b29677d7ced93d96d4eba32ad564da55442404', Integer, nullable=False)
    _7d7b0741ad8d1bbf97c83b373f5190665db4b980bf0bb530b2b3483663ab6fd1: Mapped[int] = mapped_column('7d7b0741ad8d1bbf97c83b373f5190665db4b980bf0bb530b2b3483663ab6fd1', Integer, nullable=False)
    reward_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _4161aea9fd27bf522c103f3fbdfad5c184a99452658395772d3e89f547be334e: Mapped[int] = mapped_column('4161aea9fd27bf522c103f3fbdfad5c184a99452658395772d3e89f547be334e', Integer, nullable=False)
    _50ae4ba402f3e6e69a4c444fbd4a0205a471445db1af7ee6808e5476ac0f8af1: Mapped[int] = mapped_column('50ae4ba402f3e6e69a4c444fbd4a0205a471445db1af7ee6808e5476ac0f8af1', Integer, nullable=False)
    ddc33d01d038ec09b61d6874a504a1be2a8388eafccc83612d6ac59f33bc68f7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    _36d9579bd2e71da2967c833eba12d86ae4c9a121780b629f297a6041181e843e: Mapped[int] = mapped_column('36d9579bd2e71da2967c833eba12d86ae4c9a121780b629f297a6041181e843e', Integer, nullable=False)
    ecee7bf00a576b090ab3539125fc5cc0c7fe04801dca84d39a31dfdbf515f0e1: Mapped[int] = mapped_column(Integer, nullable=False)
    _99edd0ead6d76c1bd12ff677b67b8ee0cfa59be05b23aa0613344e973018e1a5: Mapped[int] = mapped_column('99edd0ead6d76c1bd12ff677b67b8ee0cfa59be05b23aa0613344e973018e1a5', Integer, nullable=False)
    dba47fe71d3ddc7878ac6e1e9869be078b46c58a1b1a5282610137084a73a727: Mapped[int] = mapped_column(Integer, nullable=False)
    f3506dd4794aa06156334f56a3d53825cc77f781beb2ec4e1b3e11affde50dd3: Mapped[int] = mapped_column(Integer, nullable=False)
    _079aa4ba90d195469432c9fe00864a13052b377fd36612d2afc32e6cf3b62560: Mapped[int] = mapped_column('079aa4ba90d195469432c9fe00864a13052b377fd36612d2afc32e6cf3b62560', Integer, nullable=False)
    _1d23c5fa7f82001ebaae39c3a95cc73e295188a1cbbbe25daeffcbf560b9b295: Mapped[int] = mapped_column('1d23c5fa7f82001ebaae39c3a95cc73e295188a1cbbbe25daeffcbf560b9b295', Integer, nullable=False)
    _53386babd34ed734388bccb4389f7ec1ee31bd01a031cfe525776b2a7a07930b: Mapped[int] = mapped_column('53386babd34ed734388bccb4389f7ec1ee31bd01a031cfe525776b2a7a07930b', Integer, nullable=False)
    _7f1a5e072b6a0b1201daeec5eeef5a2a844798dacdc5a4751cb506ba89bfa5f0: Mapped[int] = mapped_column('7f1a5e072b6a0b1201daeec5eeef5a2a844798dacdc5a4751cb506ba89bfa5f0', Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    f84afc258529ad244a75fd85dfb6aa9a442545a2af9e62e16bf5f9d58b0002a0: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    df45e0ace6899e3292e171a192c6901526ee7418efa2e097faf0781f91f0276c: Mapped[int] = mapped_column(Integer, nullable=False)
    _70918373b5c82fbea7ff011638fa9501630b64ec79d70d897341fdf873fddf80: Mapped[int] = mapped_column('70918373b5c82fbea7ff011638fa9501630b64ec79d70d897341fdf873fddf80', Integer, nullable=False)
    _4927ce7bda13f0444a6b65b17a3bb6c633e1800f38dd10e6436c1800b7dd0abf: Mapped[int] = mapped_column('4927ce7bda13f0444a6b65b17a3bb6c633e1800f38dd10e6436c1800b7dd0abf', Integer, nullable=False)
    adf0e00e4431078919e1077a83626c5422094f42ab1d9d3daca76091cff5f230: Mapped[int] = mapped_column(Integer, nullable=False)
    _66b4cac08a8c1d37909782ed32ee1d65ea0ff2a27c2bf2496b8f036c9a151160: Mapped[int] = mapped_column('66b4cac08a8c1d37909782ed32ee1d65ea0ff2a27c2bf2496b8f036c9a151160', Integer, nullable=False)
    bca3ca60e5ff4726734e346fc1b9d83a2374008897c61be0a5b1ab6c741688b9: Mapped[int] = mapped_column(Integer, nullable=False)
    _1b0e308c719e7864019fd4bc5e77f49865ceedb878d9d1243f8d3ec77c38e306: Mapped[int] = mapped_column('1b0e308c719e7864019fd4bc5e77f49865ceedb878d9d1243f8d3ec77c38e306', Integer, nullable=False)
    _1416634b084dc20468947c7bbb4a554baa8bcaca3c3f65341cfac036b2ec4f87: Mapped[int] = mapped_column('1416634b084dc20468947c7bbb4a554baa8bcaca3c3f65341cfac036b2ec4f87', Integer, nullable=False)
    d13aad4505b91dc27f2d8457629f95d7fe2fe551573618a542794cf102f34972: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    _692eb82702a99468e996889cd62ec94a32f129c9513e3201c61ed71242d1f362: Mapped[int] = mapped_column('692eb82702a99468e996889cd62ec94a32f129c9513e3201c61ed71242d1f362', Integer, nullable=False)
    reward_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    b0f6d6f9bf2803d21593667f1a9e8b643657ccc9bee31623b6420c6b4e953a24: Mapped[int] = mapped_column(Integer, nullable=False)
    _3fc4637f03bee0380ea0ddcffadd9ed82e0c39a749a0d35c8f755dcb10389bf1: Mapped[int] = mapped_column('3fc4637f03bee0380ea0ddcffadd9ed82e0c39a749a0d35c8f755dcb10389bf1', Integer, nullable=False)
    _4d676a1c7c6d9dc4b75224de5878814384f37fc5e48cccf8ebcd81500d6f985b: Mapped[int] = mapped_column('4d676a1c7c6d9dc4b75224de5878814384f37fc5e48cccf8ebcd81500d6f985b', Integer, nullable=False)
    c6a8de4a77446a388509637cf46c031eef198e12623b67f1dbb6f8d7e49952fb: Mapped[int] = mapped_column(Integer, nullable=False)
    e5354c517077c4686b899ed496fc1b16384ffef346ab0b323984661642b35b7a: Mapped[int] = mapped_column(Integer, nullable=False)
    _10fef1d0dd2b0066e0e6cae64c8f1809e41c5398e419270a61176a027372d93c: Mapped[int] = mapped_column('10fef1d0dd2b0066e0e6cae64c8f1809e41c5398e419270a61176a027372d93c', Integer, nullable=False)
    _97b38154417acb599c4e1ea3d5d83eef61f03d52e3a10ef7acadd4e0fe2573a5: Mapped[int] = mapped_column('97b38154417acb599c4e1ea3d5d83eef61f03d52e3a10ef7acadd4e0fe2573a5', Integer, nullable=False)
    abf5d13c609817af3c7aea107e2308aa6fb0d7738acf54bda492eb7bd2b6223d: Mapped[int] = mapped_column(Integer, nullable=False)
    da64f19924e2dc6daed072da4872c159b0f1928f6d3ded1a944ada1689d8bbfc: Mapped[int] = mapped_column(Integer, nullable=False)
    _1246933c8046eb70e551bf9b04b7d36b762e0c543fa704100bd84f72bd0aa483: Mapped[int] = mapped_column('1246933c8046eb70e551bf9b04b7d36b762e0c543fa704100bd84f72bd0aa483', Integer, nullable=False)
    _91b5aa3cd03b060e2710f38a548b11c95084b0920fddf13140ed5e8354b14335: Mapped[int] = mapped_column('91b5aa3cd03b060e2710f38a548b11c95084b0920fddf13140ed5e8354b14335', Integer, nullable=False)
    _734ab8d52d5d28d73cecd67f61000df0bd3c4071e353ccb3e806a15fec849557: Mapped[int] = mapped_column('734ab8d52d5d28d73cecd67f61000df0bd3c4071e353ccb3e806a15fec849557', Integer, nullable=False)
    _909f85ff116c38e9aa9920692ade10a5f584e4c35ad4c9c6c72ea687511ceed2: Mapped[int] = mapped_column('909f85ff116c38e9aa9920692ade10a5f584e4c35ad4c9c6c72ea687511ceed2', Integer, nullable=False)
    _0a729507505812a33316134599733513c7dd3d912b35f14e9aad6bdd557891b0: Mapped[int] = mapped_column('0a729507505812a33316134599733513c7dd3d912b35f14e9aad6bdd557891b0', Integer, nullable=False)
    _53b3890615be57a2b594f1deaa9e5bac03ea582ce31a60e24e7eb81944d0ff80: Mapped[int] = mapped_column('53b3890615be57a2b594f1deaa9e5bac03ea582ce31a60e24e7eb81944d0ff80', Integer, nullable=False)
    _49de932a4195a2b624fc7dfae96b6f2a228f49a0bc313ffa16ba0a3bd0003bc0: Mapped[int] = mapped_column('49de932a4195a2b624fc7dfae96b6f2a228f49a0bc313ffa16ba0a3bd0003bc0', Integer, nullable=False)
    a4ac187c32ac1a3e8f6b30e00ea9bc87be71a24f114b9ad3dc1fd71bad0801ab: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    e5a957191959e01037ebdcc778a3fafb48c1a10e3c68b32a28dbf45d45cf13cf: Mapped[int] = mapped_column(Integer, nullable=False)
    bba250a91458cc10cb129b0def6170be5855067f3b486c2a8a24c978034cf65c: Mapped[int] = mapped_column(Integer, nullable=False)
    _5234a0bdea83f256ce8e8880badaf0e72126220554a1591c715e2c143e838c0d: Mapped[int] = mapped_column('5234a0bdea83f256ce8e8880badaf0e72126220554a1591c715e2c143e838c0d', Integer, nullable=False)
    _664801122418a3ccf2cfb0422bb1a213f28257d93e9596d3c77d5d05b569b305: Mapped[int] = mapped_column('664801122418a3ccf2cfb0422bb1a213f28257d93e9596d3c77d5d05b569b305', Integer, nullable=False)
    _0b616bc4c359a31dfe762491b21c7dcea8dbc3f3f6198d151cdfc6f10ac4b014: Mapped[int] = mapped_column('0b616bc4c359a31dfe762491b21c7dcea8dbc3f3f6198d151cdfc6f10ac4b014', Integer, nullable=False)
    _8137dbdc5d0a5906aa159fdfb50edb8420bb7e56cfe1f75abb56d23653b4267c: Mapped[int] = mapped_column('8137dbdc5d0a5906aa159fdfb50edb8420bb7e56cfe1f75abb56d23653b4267c', Integer, nullable=False)
    _4d83cf2e1b5a5bf09668f2ec3d278a5444b1a90c2debd1dee364235360053d8f: Mapped[int] = mapped_column('4d83cf2e1b5a5bf09668f2ec3d278a5444b1a90c2debd1dee364235360053d8f', Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    f4bbf1823b5b6383e66081526e36f934b8495364478ea96811ef23e7b16968d3: Mapped[int] = mapped_column(Integer, nullable=False)
    _968bff3a5f31cdb81ddaf18a3a5b0c3af6281a7f4ad9a14a2403a1d94ca8582b: Mapped[int] = mapped_column('968bff3a5f31cdb81ddaf18a3a5b0c3af6281a7f4ad9a14a2403a1d94ca8582b', Integer, nullable=False)
    _6a296e57f22274fef322624c89cc8a0ad4cd8914cb612e08f4c5a6e565b56e6a: Mapped[int] = mapped_column('6a296e57f22274fef322624c89cc8a0ad4cd8914cb612e08f4c5a6e565b56e6a', Integer, nullable=False)
    f999fa03deec85b042babef89e34e073e6226b174a181dd150a6d12d8c89299b: Mapped[int] = mapped_column(Integer, nullable=False)
    _6f30a81f856d080051ae74686f61c761fcb706547246d93914a52314d18a2bc9: Mapped[int] = mapped_column('6f30a81f856d080051ae74686f61c761fcb706547246d93914a52314d18a2bc9', Integer, nullable=False)
    _3c774ffea0292e7cc859a759f532ca32dafc490a7af199dbcfc5922a3ca4d860: Mapped[int] = mapped_column('3c774ffea0292e7cc859a759f532ca32dafc490a7af199dbcfc5922a3ca4d860', Integer, nullable=False)
    ba755c274a138a23ecf99550372ea10dd8aba673680b1534f1f9e5b568d9fd1b: Mapped[int] = mapped_column(Integer, nullable=False)
    _6a85f55eddea00022b84b5da1dd1e96e412c5b726418234dd2b46a7b3af59f9b: Mapped[int] = mapped_column('6a85f55eddea00022b84b5da1dd1e96e412c5b726418234dd2b46a7b3af59f9b', Integer, nullable=False)
    _63a594180ca8496b2480c46e17676291f167bc3e509b28bd4495745830324932: Mapped[int] = mapped_column('63a594180ca8496b2480c46e17676291f167bc3e509b28bd4495745830324932', Integer, nullable=False)
    _4386e09ca4639a6c6f7a0168b5d6f0b62a287066b741cd1b6bfc0f1d8ba817e6: Mapped[int] = mapped_column('4386e09ca4639a6c6f7a0168b5d6f0b62a287066b741cd1b6bfc0f1d8ba817e6', Integer, nullable=False)
    dc1fa870e74dd54dcb0946a44f85131b1e5ecf678ee4e2587f38c803617ac174: Mapped[int] = mapped_column(Integer, nullable=False)
    _5f4d243e931bebf2aae7b179c6837846bff63bed70b8882e648a03a497649fe1: Mapped[int] = mapped_column('5f4d243e931bebf2aae7b179c6837846bff63bed70b8882e648a03a497649fe1', Integer, nullable=False)
    db26a8ab4725bd0eb8172d4752bd1f8257a323ca10f104221ef58d2ea71f0f9f: Mapped[int] = mapped_column(Integer, nullable=False)
    _26d16e8c994155c32140354243ea2e2b95388827c5de4d62c9f94c929894bacc: Mapped[int] = mapped_column('26d16e8c994155c32140354243ea2e2b95388827c5de4d62c9f94c929894bacc', Integer, nullable=False)
    _8b671597002a30e3195d5124822fee3ca93e2a6f3d40ed7d84c948d439381a1b: Mapped[int] = mapped_column('8b671597002a30e3195d5124822fee3ca93e2a6f3d40ed7d84c948d439381a1b', Integer, nullable=False)
    e4ac4168e2bf13d51fc64bad0d4007185ddf4b52c83a0bc67469e659b13ecc66: Mapped[int] = mapped_column(Integer, nullable=False)
    _4ad56f16391e379bc7725a11c237b99a2be5b4b67e5e22d8d462a0b362a3fcd5: Mapped[int] = mapped_column('4ad56f16391e379bc7725a11c237b99a2be5b4b67e5e22d8d462a0b362a3fcd5', Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    dfd768d4a7800054d06bef1a19f4a43cbdb3905a129399c37cdd9e6ac1a6d867: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    d3d4b38f02a7bc695e886131ff41f26df129a004aff8e3870b1152bfd0f357c9: Mapped[int] = mapped_column(Integer, nullable=False)
    _1ee8d9a127879e73cc7c395b8367626fda0c5447c1460a5eb0858a455bf1140c: Mapped[int] = mapped_column('1ee8d9a127879e73cc7c395b8367626fda0c5447c1460a5eb0858a455bf1140c', Integer, nullable=False)
    e0cda4ca83564d5aa7773410eb449d4e23f3fd1df43bad3f3ecab485ae74be77: Mapped[int] = mapped_column(Integer, nullable=False)
    _8ce052a722f73f8eb54e5fd71788f4707c2d1ab4757b523a4766f15de793079e: Mapped[int] = mapped_column('8ce052a722f73f8eb54e5fd71788f4707c2d1ab4757b523a4766f15de793079e', Integer, nullable=False)
    reward_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    b3cd5a2c4dd78299e18ffe4472a813abcc0c7e2d325753bdd7e4b2b3e9071b38: Mapped[int] = mapped_column(Integer, nullable=False)
    _9d26443883c81f8d5ee4dbd8085d917dfe3ff4ac7a7c18ffc25bd289d45a28b5: Mapped[int] = mapped_column('9d26443883c81f8d5ee4dbd8085d917dfe3ff4ac7a7c18ffc25bd289d45a28b5', Integer, nullable=False)
    _96fd68e76c4f4f4e240c384e624132ca27656b16ef49271a5bff6e4a287a5f00: Mapped[int] = mapped_column('96fd68e76c4f4f4e240c384e624132ca27656b16ef49271a5bff6e4a287a5f00', Integer, nullable=False)
    _4ea7db3d348b7dcab736c4416f59785b16d959f5f64247cbab261d8b9c1c7520: Mapped[int] = mapped_column('4ea7db3d348b7dcab736c4416f59785b16d959f5f64247cbab261d8b9c1c7520', Integer, nullable=False)
    _9809fc7e5a4ac708c35d3ca64056c35dc853918dfbe39ecde7502ae30b0de122: Mapped[int] = mapped_column('9809fc7e5a4ac708c35d3ca64056c35dc853918dfbe39ecde7502ae30b0de122', Integer, nullable=False)
    a5f1405d0416f77aafad8fee637b5d0fba169952304e923b7e7d7552a683403c: Mapped[int] = mapped_column(Integer, nullable=False)
    lineup_group_set_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    c725d0ff63d5896b4e03814bb34f71c3e5b862f67b74c212145bd5eb4986fedc: Mapped[int] = mapped_column(Integer, nullable=False)
    fdc64c7be1661033af1b921849b9707b048a5afc3fb277edeb6b0a763825eae1: Mapped[int] = mapped_column(Integer, nullable=False)
    cb571a8058fafd9b8a78d5d065f6a2545c8f42baea74aefc09a36099d2a3d226: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    _4d95b50cefe187b909e1754fd1541e8afae4c60b3712f7348e85dc256f2a56b8: Mapped[int] = mapped_column('4d95b50cefe187b909e1754fd1541e8afae4c60b3712f7348e85dc256f2a56b8', Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    a8667497c725686e2bb6cd03e61c5ff1e8bce4b4b0353e4be1a1e5132f61a551: Mapped[int] = mapped_column(Integer, nullable=False)
    b47341c074f5f59c68aeadfcfd5b51df609a60fa16b3bc253ba7e56bbcaafcd0: Mapped[int] = mapped_column(Integer, nullable=False)
    _96573b95e05c928d7f36cce56257531123148e8844ae70dcb56f6ee5ff8894d0: Mapped[int] = mapped_column('96573b95e05c928d7f36cce56257531123148e8844ae70dcb56f6ee5ff8894d0', Integer, nullable=False)
    _80b71709b68c48b338bd944ce77a390fcde9517f774f1cad277a2a2494ef998a: Mapped[int] = mapped_column('80b71709b68c48b338bd944ce77a390fcde9517f774f1cad277a2a2494ef998a', Integer, nullable=False)
    b81055a52ee98df3981fcbdcdde963d9ce0ee5f07b7495f677c446a6feb380a7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    _8f0f3aebb50b43c7e19618517e7ce55f33b7a3cf5620e3708f7c13d481574d56: Mapped[int] = mapped_column('8f0f3aebb50b43c7e19618517e7ce55f33b7a3cf5620e3708f7c13d481574d56', Integer, nullable=False)
    _2f6f6965290b1ae81a3e9c5dfbabddc93266187dd0d3dc7de8ebec75b0623c72: Mapped[int] = mapped_column('2f6f6965290b1ae81a3e9c5dfbabddc93266187dd0d3dc7de8ebec75b0623c72', Integer, nullable=False)
    _976ff7ff8756cbf24f99dd55d2100af8af13c5370514ed143e0a2a78529adf98: Mapped[int] = mapped_column('976ff7ff8756cbf24f99dd55d2100af8af13c5370514ed143e0a2a78529adf98', Integer, nullable=False)
    bc00766d7820753287d0eeb71d548a38503bb35cb5799dd9fbd879c199ad36dc: Mapped[int] = mapped_column(Integer, nullable=False)
    _8be59a990aab637035df5cc99d4aac0a14838fe8290d30c84536b7037d064b8b: Mapped[int] = mapped_column('8be59a990aab637035df5cc99d4aac0a14838fe8290d30c84536b7037d064b8b', Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, nullable=False)
    _0aa5c3a7570849c3cb9a64b992db74a054d47d71c499c967836d71c66e9b578e: Mapped[int] = mapped_column('0aa5c3a7570849c3cb9a64b992db74a054d47d71c499c967836d71c66e9b578e', Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, nullable=False)
    _7f22112645a07b951a23e47c10c49f189d3a8072747e76d13f93122ebaffa9f7: Mapped[int] = mapped_column('7f22112645a07b951a23e47c10c49f189d3a8072747e76d13f93122ebaffa9f7', Integer, nullable=False)
    _1773ed978dc25fcc1daf6eee4fbe68bb16fa8557145f30ccb4c364fe92eee07b: Mapped[int] = mapped_column('1773ed978dc25fcc1daf6eee4fbe68bb16fa8557145f30ccb4c364fe92eee07b', Integer, nullable=False)
    _52766f9588e32b9a5c00ab743cf112ea4f64f08e23c6f6f0d2d4782762ae1f1c: Mapped[int] = mapped_column('52766f9588e32b9a5c00ab743cf112ea4f64f08e23c6f6f0d2d4782762ae1f1c', Integer, nullable=False)


class FkeHappeningList(Base):
    __tablename__ = 'fke_happening_list'

    happening_name: Mapped[str] = mapped_column(Text, nullable=False)
    happening_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class FkeReward(Base):
    __tablename__ = 'fke_reward'

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    fke_point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class FpcDramaScript(Base):
    __tablename__ = 'fpc_drama_script'

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class FpcSetting(Base):
    __tablename__ = 'fpc_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class FpcStoryDatum(Base):
    __tablename__ = 'fpc_story_data'

    fpc_voice_type: Mapped[int] = mapped_column(Integer, nullable=False)
    fff8073b26802738f3c7b9351514b4678813a047b598d449cf586e98bd9b0487: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    _9d057639d0e707881e5928d9392aea047bb8768148da699252a8edab18f19e37: Mapped[int] = mapped_column('9d057639d0e707881e5928d9392aea047bb8768148da699252a8edab18f19e37', Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    e7355f4939010a010b64d0cd266ee38bb469ca6dceb18ec11d14342fefdfb35c: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    adc666fd5665ffbc062948f5a80d60759e5a581ddbc9aec70702de7efaa988a7: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    _66e4839c5c28a86618679152fc45328d17832897c5a2bed92f0532e88a9f6356: Mapped[int] = mapped_column('66e4839c5c28a86618679152fc45328d17832897c5a2bed92f0532e88a9f6356', Integer, nullable=False)


class GachaDatum(Base):
    __tablename__ = 'gacha_data'

    pick_up_chara_text: Mapped[str] = mapped_column(Text, nullable=False)
    _2bc8503081255ec4dc28a2127f5bb7392c3134c066202ee8eb716f5963c19a5b: Mapped[str] = mapped_column('2bc8503081255ec4dc28a2127f5bb7392c3134c066202ee8eb716f5963c19a5b', Text, nullable=False)
    prizegacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _6622bb255578c550e928b43e2446281382869f1c35d113f57b84c0c5086bef38: Mapped[str] = mapped_column('6622bb255578c550e928b43e2446281382869f1c35d113f57b84c0c5086bef38', Text, nullable=False)
    gacha_cost_type: Mapped[int] = mapped_column(Integer, nullable=False)
    _993ba3a40b8b2e9813b7dd10c250635612613c223ae1a78a3f314f970331211a: Mapped[str] = mapped_column('993ba3a40b8b2e9813b7dd10c250635612613c223ae1a78a3f314f970331211a', Text, nullable=False)
    _965fe29d3de2ba226d7d53001356e49918fc1ce76b5523fc88677d3e3b81bfe8: Mapped[str] = mapped_column('965fe29d3de2ba226d7d53001356e49918fc1ce76b5523fc88677d3e3b81bfe8', Text, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_times_limit10: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    f711ded9958cd75536ca209739ee12ba08e47ac9ad8fc9336e47ade083375b3c: Mapped[int] = mapped_column(Integer, nullable=False)
    description_sp: Mapped[str] = mapped_column(Text, nullable=False)
    f0b0336806f5dfbd6cef3a56a5e79ff5acf71ecb2699685d4ef2e7be0d835c56: Mapped[int] = mapped_column(Integer, nullable=False)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=False)
    c0edb922166bd990c2bea7c868d3ad4ed4de58e10e395266c28d21eafd713256: Mapped[str] = mapped_column(Text, nullable=False)
    description_2: Mapped[str] = mapped_column(Text, nullable=False)
    pickup_badge: Mapped[int] = mapped_column(Integer, nullable=False)
    _2f76a0707231682992771ae531c1ffe726c8256c122dadd98c2d118ea51bb0a0: Mapped[int] = mapped_column('2f76a0707231682992771ae531c1ffe726c8256c122dadd98c2d118ea51bb0a0', Integer, nullable=False)
    free_gacha_count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    _9f4420b51c48d5859678f424cde3fc8cdf1dbc392d7760a2aea9693cc3e31a41: Mapped[str] = mapped_column('9f4420b51c48d5859678f424cde3fc8cdf1dbc392d7760a2aea9693cc3e31a41', Text, nullable=False)
    pickup_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    free_gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_detail: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _16ae915bfad65b85aee0b4c0faf5f9967e6af80e6cc2647b132ccba6346037cf: Mapped[str] = mapped_column('16ae915bfad65b85aee0b4c0faf5f9967e6af80e6cc2647b132ccba6346037cf', Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    ticket_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tab_name: Mapped[str] = mapped_column(Text, nullable=False)
    _8964ef885281944c80510056f200f598e1816267ef5543ab861fc8b4b096534e: Mapped[int] = mapped_column('8964ef885281944c80510056f200f598e1816267ef5543ab861fc8b4b096534e', Integer, nullable=False)
    title_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cd8395264af43301eb0a702c72393bdf510aafbda8385f2c326c6a5cb2c046c4: Mapped[int] = mapped_column(Integer, nullable=False)
    _9f6648416325c0d7e2002d46b9e16f5c3dd6c5ea60118a827c9f1361eac3f7ad: Mapped[str] = mapped_column('9f6648416325c0d7e2002d46b9e16f5c3dd6c5ea60118a827c9f1361eac3f7ad', Text, nullable=False)
    _040554958e378b331bb95476ac52c357057bfd28e5486c2f6c26d0ce4ea9e2d9: Mapped[str] = mapped_column('040554958e378b331bb95476ac52c357057bfd28e5486c2f6c26d0ce4ea9e2d9', Text, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    free_gacha_interval_time: Mapped[int] = mapped_column(Integer, nullable=False)


class GachaExchangeLineup(Base):
    __tablename__ = 'gacha_exchange_lineup'

    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dced7e5434636f85afb1f27bdc2dbd38d0ea843e6f8e4b29708a8a2c37733c44: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    pickup_gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)


class GachaPickup(Base):
    __tablename__ = 'gacha_pickup'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class GiftMessage(Base):
    __tablename__ = 'gift_message'

    type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discription: Mapped[str] = mapped_column(Text, nullable=False)


class GlobalDatum(Base):
    __tablename__ = 'global_data'

    desc: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    key_name: Mapped[str] = mapped_column(Text, primary_key=True)


class GlossaryDetail(Base):
    __tablename__ = 'glossary_detail'

    glossary_category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    glossary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_type: Mapped[int] = mapped_column(Integer, nullable=False)


class GoldsetDatum(Base):
    __tablename__ = 'goldset_data'

    f02fdf334a258d835cf9a00f32e01aa65fb4870f3cf1f567612da02ae8244b78: Mapped[int] = mapped_column(Integer, nullable=False)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_jewel_count: Mapped[int] = mapped_column(Integer, nullable=False)
    get_gold_count: Mapped[int] = mapped_column(Integer, nullable=False)
    _4a3d8f40b6f0acf3c768862570fedfc98156f7d0b113a1d2faa346d0259801df: Mapped[int] = mapped_column('4a3d8f40b6f0acf3c768862570fedfc98156f7d0b113a1d2faa346d0259801df', Integer, nullable=False)
    _3560bf711b2a4d0186757216136387ef0e2f8fd2835811324f6f5091e9dfee5e: Mapped[int] = mapped_column('3560bf711b2a4d0186757216136387ef0e2f8fd2835811324f6f5091e9dfee5e', Integer, nullable=False)
    _4601005419b3dd2fa2a698dc17e4adc8648de86264df231d075d92ec04cb316f: Mapped[int] = mapped_column('4601005419b3dd2fa2a698dc17e4adc8648de86264df231d075d92ec04cb316f', Integer, nullable=False)
    _868568a523fcb007eba6d44689d7e1c76fb3357575408f28c8185a5f1c7e7fae: Mapped[int] = mapped_column('868568a523fcb007eba6d44689d7e1c76fb3357575408f28c8185a5f1c7e7fae', Integer, nullable=False)
    aad3a8261b3f9388551bcac31dfab69f14abf9ab354c11311788a5969699c454: Mapped[int] = mapped_column(Integer, nullable=False)


class GoldsetData2(Base):
    __tablename__ = 'goldset_data_2'

    d9f02b6be6bf402c3ba2c3956a09f7dbf41cd589608f92a8b55af6454de3d5e7: Mapped[int] = mapped_column(Integer, nullable=False)
    _4ef1e6becfa7cb0cc7dd28343456c19312c2dbf9dc30204a0bebcde4862d271b: Mapped[int] = mapped_column('4ef1e6becfa7cb0cc7dd28343456c19312c2dbf9dc30204a0bebcde4862d271b', Integer, nullable=False)
    training_quest_count: Mapped[int] = mapped_column(Integer, nullable=False)
    ab0647cc34cce62ba461a578dfab1130e46e04e5fe30be3cf730114f970b5ec7: Mapped[int] = mapped_column(Integer, nullable=False)
    _4c19f98b7c8ecd85166af4c1d441cac8b6569b4927fd59b77919a6ac3b54a58f: Mapped[int] = mapped_column('4c19f98b7c8ecd85166af4c1d441cac8b6569b4927fd59b77919a6ac3b54a58f', Integer, nullable=False)
    use_jewel_count: Mapped[int] = mapped_column(Integer, nullable=False)
    buy_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    _23033cce20f6137f04abfbbde5aa70fba83fc20def55b0203671e89e193f689a: Mapped[int] = mapped_column('23033cce20f6137f04abfbbde5aa70fba83fc20def55b0203671e89e193f689a', Integer, nullable=False)
    get_gold_count: Mapped[int] = mapped_column(Integer, nullable=False)
    _635c09f14b4a9910121fed34025b2a4d10b23c5183a3d8afb2a4a654b749f7a2: Mapped[int] = mapped_column('635c09f14b4a9910121fed34025b2a4d10b23c5183a3d8afb2a4a654b749f7a2', Integer, nullable=False)


class GoldsetDataTeamlevel(Base):
    __tablename__ = 'goldset_data_teamlevel'

    initial_get_gold_count: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    _12f6d519b6933a635666097131df0e93184791eae75b5383bdd32fa055569c09: Mapped[int] = mapped_column('12f6d519b6933a635666097131df0e93184791eae75b5383bdd32fa055569c09', Integer, nullable=False)


class GrandArenaDailyRankReward(Base):
    __tablename__ = 'grand_arena_daily_rank_reward'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class GrandArenaDefenceReward(Base):
    __tablename__ = 'grand_arena_defence_reward'

    limit_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class GrandArenaMaxRankReward(Base):
    __tablename__ = 'grand_arena_max_rank_reward'

    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)


class GrandArenaMaxSeasonRankReward(Base):
    __tablename__ = 'grand_arena_max_season_rank_reward'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class GrowthParameter(Base):
    __tablename__ = 'growth_parameter'

    growth_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_3: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_6: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_5: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_type: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    is_restriction: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_1: Mapped[int] = mapped_column(Integer, nullable=False)


class GrowthParameterUnique(Base):
    __tablename__ = 'growth_parameter_unique'

    unique_equip_strength_point_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equip_rank_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equip_rank_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equip_strength_point_1: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class GrowthRestrictionUnit(Base):
    __tablename__ = 'growth_restriction_unit'

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Guild(Base):
    __tablename__ = 'guild'

    member23: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_name: Mapped[str] = mapped_column(Text, nullable=False)
    member11: Mapped[int] = mapped_column(Integer, nullable=False)
    member28: Mapped[int] = mapped_column(Integer, nullable=False)
    member13: Mapped[int] = mapped_column(Integer, nullable=False)
    member29: Mapped[int] = mapped_column(Integer, nullable=False)
    member4: Mapped[int] = mapped_column(Integer, nullable=False)
    member17: Mapped[int] = mapped_column(Integer, nullable=False)
    member26: Mapped[int] = mapped_column(Integer, nullable=False)
    member3: Mapped[int] = mapped_column(Integer, nullable=False)
    member12: Mapped[int] = mapped_column(Integer, nullable=False)
    member27: Mapped[int] = mapped_column(Integer, nullable=False)
    member9: Mapped[int] = mapped_column(Integer, nullable=False)
    member16: Mapped[int] = mapped_column(Integer, nullable=False)
    member7: Mapped[int] = mapped_column(Integer, nullable=False)
    member10: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    member6: Mapped[int] = mapped_column(Integer, nullable=False)
    member5: Mapped[int] = mapped_column(Integer, nullable=False)
    member24: Mapped[int] = mapped_column(Integer, nullable=False)
    member14: Mapped[int] = mapped_column(Integer, nullable=False)
    member20: Mapped[int] = mapped_column(Integer, nullable=False)
    member2: Mapped[int] = mapped_column(Integer, nullable=False)
    member1: Mapped[int] = mapped_column(Integer, nullable=False)
    member25: Mapped[int] = mapped_column(Integer, nullable=False)
    member19: Mapped[int] = mapped_column(Integer, nullable=False)
    member22: Mapped[int] = mapped_column(Integer, nullable=False)
    member30: Mapped[int] = mapped_column(Integer, nullable=False)
    member8: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member18: Mapped[int] = mapped_column(Integer, nullable=False)
    member15: Mapped[int] = mapped_column(Integer, nullable=False)
    member21: Mapped[int] = mapped_column(Integer, nullable=False)
    guild_master: Mapped[int] = mapped_column(Integer, nullable=False)


class GuildAdditionalMember(Base):
    __tablename__ = 'guild_additional_member'

    guild_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member1: Mapped[int] = mapped_column(Integer, nullable=False)
    member6: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    member8: Mapped[int] = mapped_column(Integer, nullable=False)
    member4: Mapped[int] = mapped_column(Integer, nullable=False)
    member2: Mapped[int] = mapped_column(Integer, nullable=False)
    member5: Mapped[int] = mapped_column(Integer, nullable=False)
    member9: Mapped[int] = mapped_column(Integer, nullable=False)
    member7: Mapped[int] = mapped_column(Integer, nullable=False)
    member10: Mapped[int] = mapped_column(Integer, nullable=False)
    thumb_id: Mapped[int] = mapped_column(Integer, nullable=False)
    member3: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBattleMissionDatum(Base):
    __tablename__ = 'hatsune_battle_mission_data'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneBgChange(Base):
    __tablename__ = 'hatsune_bg_change'

    quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneBgChangeDatum(Base):
    __tablename__ = 'hatsune_bg_change_data'

    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bg_after_change_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBoss(Base):
    __tablename__ = 'hatsune_boss'

    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    qd_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    deatail_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    required_skip_ticket_count: Mapped[int] = mapped_column(Integer, nullable=False)
    _4e0201d550564f30f3a7aa4be48dc5c3c89e3d082ee7cabb1a7be1149cdf3ad3: Mapped[str] = mapped_column('4e0201d550564f30f3a7aa4be48dc5c3c89e3d082ee7cabb1a7be1149cdf3ad3', Text, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    f9a2e2c3513bb2de21d0272b76144cf91291666bc29fe88dc90a31317bc8131c: Mapped[str] = mapped_column(Text, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    map_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    map_size: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    e615f98682eb354867811253e46425f2f0db99f95a34dd8cb832095ac5526180: Mapped[str] = mapped_column(Text, nullable=False)
    map_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    _91d0651e22969b9011e0d15159fb07d3fe42f5398a7bd28d4ff9e5b00d314ecc: Mapped[int] = mapped_column('91d0651e22969b9011e0d15159fb07d3fe42f5398a7bd28d4ff9e5b00d314ecc', Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    use_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_collider_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    oneblow_count_of_skip_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_display_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    event_boss_treasure_box_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    map_arrow_offset: Mapped[float] = mapped_column(REAL, nullable=False)
    td_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    retire_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_on_bg: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneBossCondition(Base):
    __tablename__ = 'hatsune_boss_condition'

    condition_boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    b77fc14ba45ccab4e66da409ca0a471fcb9bb76ad22485f40e83282d0316dd78: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    e0e2b5a70eb964ed54723ccb566c785363f90aee19e1975636a45f855b45f6fc: Mapped[int] = mapped_column(Integer, nullable=False)
    _2981193e8172341168ee8c861022f3ebd5f8d11c369ce84a3a875b8e4f194a5a: Mapped[int] = mapped_column('2981193e8172341168ee8c861022f3ebd5f8d11c369ce84a3a875b8e4f194a5a', Integer, nullable=False)
    _2e2cde92c53eaca0f60c37a88e31ab1199f69be472e6ff82372dc09377118345: Mapped[int] = mapped_column('2e2cde92c53eaca0f60c37a88e31ab1199f69be472e6ff82372dc09377118345', Integer, nullable=False)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    b8ab70d9c2860909e30b017a9e959d089835b1d87a2ba429623ea2a62abc1cf1: Mapped[int] = mapped_column(Integer, nullable=False)
    _96634a3b54c87031bd0c3ed6f26f3faa258cd065d1a79d5c1e3da35318712bec: Mapped[int] = mapped_column('96634a3b54c87031bd0c3ed6f26f3faa258cd065d1a79d5c1e3da35318712bec', Integer, nullable=False)


class HatsuneBossEnemySetting(Base):
    __tablename__ = 'hatsune_boss_enemy_setting'

    detail_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    event_boss_treasure_box_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    map_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    map_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    map_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_identify: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    must_kill_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneBossExtraEffect(Base):
    __tablename__ = 'hatsune_boss_extra_effect'

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDailyMissionDatum(Base):
    __tablename__ = 'hatsune_daily_mission_data'

    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneDescription(Base):
    __tablename__ = 'hatsune_description'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDiaryDatum(Base):
    __tablename__ = 'hatsune_diary_data'

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    forced_release_time: Mapped[str] = mapped_column(Text, nullable=False)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    diary_date: Mapped[int] = mapped_column(Integer, nullable=False)
    diary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDiaryLetterScript(Base):
    __tablename__ = 'hatsune_diary_letter_script'

    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    diary_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneDiaryScript(Base):
    __tablename__ = 'hatsune_diary_script'

    diary_text: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    text_animation_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    diary_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneDiarySetting(Base):
    __tablename__ = 'hatsune_diary_setting'

    bgm_sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneEmblemMission(Base):
    __tablename__ = 'hatsune_emblem_mission'

    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneEmblemMissionReward(Base):
    __tablename__ = 'hatsune_emblem_mission_reward'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneExPlusSetting(Base):
    __tablename__ = 'hatsune_ex_plus_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_challenge_count: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneItem(Base):
    __tablename__ = 'hatsune_item'

    gacha_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_material_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneLimitChara(Base):
    __tablename__ = 'hatsune_limit_chara'

    event_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_chara_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneMap(Base):
    __tablename__ = 'hatsune_map'

    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneMapEvent(Base):
    __tablename__ = 'hatsune_map_event'

    event_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param1: Mapped[int] = mapped_column(Integer, nullable=False)
    param2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneMissionRewardDatum(Base):
    __tablename__ = 'hatsune_mission_reward_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneMultiRouteParameter(Base):
    __tablename__ = 'hatsune_multi_route_parameter'

    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_2: Mapped[int] = mapped_column(Integer, nullable=False)
    param_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_1: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsunePointCounter(Base):
    __tablename__ = 'hatsune_point_counter'

    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    counter_type: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsunePresent(Base):
    __tablename__ = 'hatsune_present'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dialog_text: Mapped[str] = mapped_column(Text, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    dialog_title: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneQuest(Base):
    __tablename__ = 'hatsune_quest'

    drop_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    drop_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    icon_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _2a505b39bd92aaad6ab93fcddedafb5ce16ecd2199637c24c1d7a48b6168f5cb: Mapped[str] = mapped_column('2a505b39bd92aaad6ab93fcddedafb5ce16ecd2199637c24c1d7a48b6168f5cb', Text, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    b3f7201ae28bcdf7071a605e1c6a654d5157fbc0b54f53999e8658d3b643c1b3: Mapped[str] = mapped_column(Text, nullable=False)
    quest_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_offset_y: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneQuestArea(Base):
    __tablename__ = 'hatsune_quest_area'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dba5009f6e31a6dba2f72f827f54e3f811e6f5b1a5b93331b7055ba48370223c: Mapped[str] = mapped_column(Text, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_param_2: Mapped[str] = mapped_column(Text, nullable=False)
    scroll_width: Mapped[int] = mapped_column(Integer, nullable=False)
    c94151d0e64035d4adba61cf05d68a7fa6d3853e32fc060166d8cba8e1e10c08: Mapped[str] = mapped_column(Text, nullable=False)
    open_tutorial_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_height: Mapped[int] = mapped_column(Integer, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    tutorial_param_1: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneQuestCondition(Base):
    __tablename__ = 'hatsune_quest_condition'

    release_boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuiz(Base):
    __tablename__ = 'hatsune_quiz'

    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_title: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id_quiz_end: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    choice_5: Mapped[str] = mapped_column(Text, nullable=False)
    hint: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_3: Mapped[str] = mapped_column(Text, nullable=False)
    choice_2: Mapped[str] = mapped_column(Text, nullable=False)
    choice_6: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_point_name: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id_quiz_start: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    choice_4: Mapped[str] = mapped_column(Text, nullable=False)
    choice_1: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneQuizCondition(Base):
    __tablename__ = 'hatsune_quiz_condition'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_time_from: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quiz_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneQuizReward(Base):
    __tablename__ = 'hatsune_quiz_reward'

    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneRelayDatum(Base):
    __tablename__ = 'hatsune_relay_data'

    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    is_enable_read: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    relay_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class HatsuneSchedule(Base):
    __tablename__ = 'hatsune_schedule'

    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    backgroud_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    teaser_dialog_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    series_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    backgroud_size_y: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    backgroud_size_x: Mapped[int] = mapped_column(Integer, nullable=False)
    backgroud_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class HatsuneSeriesGachaReference(Base):
    __tablename__ = 'hatsune_series_gacha_reference'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reference_key_event_id_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSpecialBattle(Base):
    __tablename__ = 'hatsune_special_battle'

    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    is_hide_boss: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_motion: Mapped[str] = mapped_column(Text, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSpecialBossTicketCount(Base):
    __tablename__ = 'hatsune_special_boss_ticket_count'

    challenge_count_from: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_count_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    use_ticket_num: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSpecialEnemy(Base):
    __tablename__ = 'hatsune_special_enemy'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_point: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneSpecialMissionDatum(Base):
    __tablename__ = 'hatsune_special_mission_data'

    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    special_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneStationaryMissionDatum(Base):
    __tablename__ = 'hatsune_stationary_mission_data'

    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class HatsuneUnlockStoryCondition(Base):
    __tablename__ = 'hatsune_unlock_story_condition'

    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_entry: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class HatsuneUnlockUnitCondition(Base):
    __tablename__ = 'hatsune_unlock_unit_condition'

    description_2: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description_1: Mapped[str] = mapped_column(Text, nullable=False)


class HpDrainAt(Base):
    __tablename__ = 'hp_drain_at'

    correction_value: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_value: Mapped[int] = mapped_column(Integer, nullable=False)


class ItemDatum(Base):
    __tablename__ = 'item_data'

    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    item_name: Mapped[str] = mapped_column(Text, nullable=False)
    sell_check_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)


class ItemETicketDatum(Base):
    __tablename__ = 'item_e_ticket_data'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)


class JewelStoreNew(Base):
    __tablename__ = 'jewel_store_new'

    item_5: Mapped[str] = mapped_column(Text, nullable=False)
    icon_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_2: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_3: Mapped[str] = mapped_column(Text, nullable=False)
    icon_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_4: Mapped[str] = mapped_column(Text, nullable=False)
    ext_param: Mapped[str] = mapped_column(Text, nullable=False)
    color: Mapped[str] = mapped_column(Text, nullable=False)
    item_3: Mapped[str] = mapped_column(Text, nullable=False)
    bg: Mapped[int] = mapped_column(Integer, nullable=False)
    catagory: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_1: Mapped[str] = mapped_column(Text, nullable=False)
    text_2: Mapped[str] = mapped_column(Text, nullable=False)
    text_1: Mapped[str] = mapped_column(Text, nullable=False)


class KaiserAddTimesDatum(Base):
    __tablename__ = 'kaiser_add_times_data'

    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)


class KaiserExterminationReward(Base):
    __tablename__ = 'kaiser_extermination_reward'

    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class KaiserQuestDatum(Base):
    __tablename__ = 'kaiser_quest_data'

    battle_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    restriction_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    result_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    kaiser_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    clear_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)


class KaiserRestrictionGroup(Base):
    __tablename__ = 'kaiser_restriction_group'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restriction_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class KaiserSchedule(Base):
    __tablename__ = 'kaiser_schedule'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    after_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bg: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    after_bg: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class KaiserSpecialBattle(Base):
    __tablename__ = 'kaiser_special_battle'

    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    start_idle_trigger: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    appear_time: Mapped[float] = mapped_column(REAL, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)


class KmkNaviComment(Base):
    __tablename__ = 'kmk_navi_comment'

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class KmkReward(Base):
    __tablename__ = 'kmk_reward'

    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    kmk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class KnightMissionDatum(Base):
    __tablename__ = 'knight_mission_data'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class KnightMissionRewardDatum(Base):
    __tablename__ = 'knight_mission_reward_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class KnightRankMaterialSetting(Base):
    __tablename__ = 'knight_rank_material_setting'

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, primary_key=True)


class LegionAddTimesDatum(Base):
    __tablename__ = 'legion_add_times_data'

    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionBattleBonus(Base):
    __tablename__ = 'legion_battle_bonus'

    legion_battle_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_hp: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    legion_battle_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionBattleBonusEffect(Base):
    __tablename__ = 'legion_battle_bonus_effect'

    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    text_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionBossEnemySetting(Base):
    __tablename__ = 'legion_boss_enemy_setting'

    detail_offset_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LegionEffect(Base):
    __tablename__ = 'legion_effect'

    bonus_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_3: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_1: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionEffectiveUnit(Base):
    __tablename__ = 'legion_effective_unit'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    legion_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    support_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionExterminationReward(Base):
    __tablename__ = 'legion_extermination_reward'

    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionMissionCategoryDatum(Base):
    __tablename__ = 'legion_mission_category_data'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LegionMissionDatum(Base):
    __tablename__ = 'legion_mission_data'

    legion_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    legion_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionMissionRewardDatum(Base):
    __tablename__ = 'legion_mission_reward_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionQuestDatum(Base):
    __tablename__ = 'legion_quest_data'

    bonus_max: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    legion_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    max_raid_hp: Mapped[str] = mapped_column(Text, nullable=False)
    battle_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    expel_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    all_disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)


class LegionSchedule(Base):
    __tablename__ = 'legion_schedule'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_bg: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class LegionSpecialBattle(Base):
    __tablename__ = 'legion_special_battle'

    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)


class LoginBonusAdv(Base):
    __tablename__ = 'login_bonus_adv'

    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_key: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    read_process_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class LoginBonusDatum(Base):
    __tablename__ = 'login_bonus_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_type: Mapped[int] = mapped_column(Integer, nullable=False)
    login_bonus_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    adv_play_type: Mapped[int] = mapped_column(Integer, nullable=False)
    count_num: Mapped[int] = mapped_column(Integer, nullable=False)
    stamp_id: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LoginBonusDetail(Base):
    __tablename__ = 'login_bonus_detail'

    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class LoginBonusMessageDatum(Base):
    __tablename__ = 'login_bonus_message_data'

    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_type: Mapped[int] = mapped_column(Integer, nullable=False)
    rate: Mapped[int] = mapped_column(Integer, nullable=False)
    login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    day_count: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    luck_pattern: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_param: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LoveChara(Base):
    __tablename__ = 'love_chara'

    total_love: Mapped[int] = mapped_column(Integer, nullable=False)
    unlocked_class: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)


class LoveRankup(Base):
    __tablename__ = 'love_rankup'

    effect_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    love_rank: Mapped[int] = mapped_column(Integer, primary_key=True)


class LssNaviComment(Base):
    __tablename__ = 'lss_navi_comment'

    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)


class LssStoryDatum(Base):
    __tablename__ = 'lss_story_data'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class LsvDramaScript(Base):
    __tablename__ = 'lsv_drama_script'

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)


class LsvStoryDatum(Base):
    __tablename__ = 'lsv_story_data'

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_event_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    time_condition: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LsvStoryScript(Base):
    __tablename__ = 'lsv_story_script'

    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class LtoLetterScript(Base):
    __tablename__ = 'lto_letter_script'

    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    letter_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)


class LtoStoryDatum(Base):
    __tablename__ = 'lto_story_data'

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Metamorphose(Base):
    __tablename__ = 'metamorphose'

    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_value: Mapped[int] = mapped_column(Integer, primary_key=True)


class MhpDramaScript(Base):
    __tablename__ = 'mhp_drama_script'

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)


class MhpStoryDatum(Base):
    __tablename__ = 'mhp_story_data'

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)


class Minigame(Base):
    __tablename__ = 'minigame'

    release_conditions_1: Mapped[int] = mapped_column(Integer, nullable=False)
    conditions_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    display_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_chat_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    minigame_scheme_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score_unit: Mapped[str] = mapped_column(Text, nullable=False)
    first_time_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_enabled_zero_score: Mapped[int] = mapped_column(Integer, nullable=False)
    display_condition_type: Mapped[int] = mapped_column(Integer, nullable=False)


class MirokuBossDatum(Base):
    __tablename__ = 'miroku_boss_data'

    clear_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    clear_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet: Mapped[str] = mapped_column(Text, nullable=False)


class MirokuSpecialBattle(Base):
    __tablename__ = 'miroku_special_battle'

    purpose_count: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end_after_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_mode_end: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que: Mapped[str] = mapped_column(Text, nullable=False)
    purpose_type: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id_mode_start: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_start_second: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_gauge_color_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    story_start_after_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unnecessary_defeat_chara: Mapped[int] = mapped_column(Integer, nullable=False)


class MissionCategoryIcon(Base):
    __tablename__ = 'mission_category_icon'

    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    color: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MissionRewardDatum(Base):
    __tablename__ = 'mission_reward_data'

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    lv_to: Mapped[int] = mapped_column(Integer, nullable=False)
    lv_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class MmeStoryDatum(Base):
    __tablename__ = 'mme_story_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_last: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_puzzle_piece: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Movie(Base):
    __tablename__ = 'movie'

    fade_loop_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bgm_volume_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    bgm_id: Mapped[str] = mapped_column(Text, nullable=False)
    se_id: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    my_page_flag: Mapped[int] = mapped_column(Integer, nullable=False)


class MusicContent(Base):
    __tablename__ = 'music_content'

    detail: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    music_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    cue_id: Mapped[str] = mapped_column(Text, nullable=False)
    total_playing_time: Mapped[str] = mapped_column(Text, nullable=False)
    listen_start_time: Mapped[str] = mapped_column(Text, nullable=False)


class MusicList(Base):
    __tablename__ = 'music_list'

    list_name: Mapped[str] = mapped_column(Text, nullable=False)
    ios_url: Mapped[str] = mapped_column(Text, nullable=False)
    font_size: Mapped[float] = mapped_column(REAL, nullable=False)
    cost_item_num: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    dmm_url: Mapped[str] = mapped_column(Text, nullable=False)
    android_url: Mapped[str] = mapped_column(Text, nullable=False)
    music_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kana: Mapped[str] = mapped_column(Text, nullable=False)
    pre_shop_start: Mapped[str] = mapped_column(Text, nullable=False)
    sort: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_end: Mapped[str] = mapped_column(Text, nullable=False)
    shop_start: Mapped[str] = mapped_column(Text, nullable=False)


class MypageCharacterMovie(Base):
    __tablename__ = 'mypage_character_movie'

    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    skin_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MypageFrame(Base):
    __tablename__ = 'mypage_frame'

    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MyprofileContent(Base):
    __tablename__ = 'myprofile_content'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class NaviComment(Base):
    __tablename__ = 'navi_comment'

    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class NbbDramaScript(Base):
    __tablename__ = 'nbb_drama_script'

    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class NbbEmblem(Base):
    __tablename__ = 'nbb_emblem'

    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    one_play_score: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class NbbFaceIconActionDatum(Base):
    __tablename__ = 'nbb_face_icon_action_data'

    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_cue_1: Mapped[str] = mapped_column(Text, nullable=False)
    text_1: Mapped[str] = mapped_column(Text, nullable=False)
    play_time: Mapped[int] = mapped_column(Integer, nullable=False)
    face_icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_cue_2: Mapped[str] = mapped_column(Text, nullable=False)
    action_param: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_2: Mapped[str] = mapped_column(Text, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbFirstFrame(Base):
    __tablename__ = 'nbb_first_frame'

    row_41: Mapped[int] = mapped_column(Integer, nullable=False)
    row_60: Mapped[int] = mapped_column(Integer, nullable=False)
    row_5: Mapped[int] = mapped_column(Integer, nullable=False)
    row_10: Mapped[int] = mapped_column(Integer, nullable=False)
    row_46: Mapped[int] = mapped_column(Integer, nullable=False)
    row_31: Mapped[int] = mapped_column(Integer, nullable=False)
    row_55: Mapped[int] = mapped_column(Integer, nullable=False)
    row_30: Mapped[int] = mapped_column(Integer, nullable=False)
    row_16: Mapped[int] = mapped_column(Integer, nullable=False)
    row_29: Mapped[int] = mapped_column(Integer, nullable=False)
    row_57: Mapped[int] = mapped_column(Integer, nullable=False)
    row_25: Mapped[int] = mapped_column(Integer, nullable=False)
    row_44: Mapped[int] = mapped_column(Integer, nullable=False)
    row_53: Mapped[int] = mapped_column(Integer, nullable=False)
    row_51: Mapped[int] = mapped_column(Integer, nullable=False)
    row_42: Mapped[int] = mapped_column(Integer, nullable=False)
    row_17: Mapped[int] = mapped_column(Integer, nullable=False)
    row_47: Mapped[int] = mapped_column(Integer, nullable=False)
    row_58: Mapped[int] = mapped_column(Integer, nullable=False)
    row_8: Mapped[int] = mapped_column(Integer, nullable=False)
    row_50: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False)
    row_11: Mapped[int] = mapped_column(Integer, nullable=False)
    row_54: Mapped[int] = mapped_column(Integer, nullable=False)
    row_35: Mapped[int] = mapped_column(Integer, nullable=False)
    row_38: Mapped[int] = mapped_column(Integer, nullable=False)
    lane: Mapped[int] = mapped_column(Integer, nullable=False)
    row_14: Mapped[int] = mapped_column(Integer, nullable=False)
    row_40: Mapped[int] = mapped_column(Integer, nullable=False)
    row_45: Mapped[int] = mapped_column(Integer, nullable=False)
    row_49: Mapped[int] = mapped_column(Integer, nullable=False)
    row_2: Mapped[int] = mapped_column(Integer, nullable=False)
    row_1: Mapped[int] = mapped_column(Integer, nullable=False)
    row_52: Mapped[int] = mapped_column(Integer, nullable=False)
    row_23: Mapped[int] = mapped_column(Integer, nullable=False)
    row_20: Mapped[int] = mapped_column(Integer, nullable=False)
    row_28: Mapped[int] = mapped_column(Integer, nullable=False)
    row_6: Mapped[int] = mapped_column(Integer, nullable=False)
    row_56: Mapped[int] = mapped_column(Integer, nullable=False)
    row_36: Mapped[int] = mapped_column(Integer, nullable=False)
    row_48: Mapped[int] = mapped_column(Integer, nullable=False)
    row_26: Mapped[int] = mapped_column(Integer, nullable=False)
    row_59: Mapped[int] = mapped_column(Integer, nullable=False)
    row_19: Mapped[int] = mapped_column(Integer, nullable=False)
    row_15: Mapped[int] = mapped_column(Integer, nullable=False)
    row_3: Mapped[int] = mapped_column(Integer, nullable=False)
    row_27: Mapped[int] = mapped_column(Integer, nullable=False)
    row_13: Mapped[int] = mapped_column(Integer, nullable=False)
    row_22: Mapped[int] = mapped_column(Integer, nullable=False)
    row_7: Mapped[int] = mapped_column(Integer, nullable=False)
    row_4: Mapped[int] = mapped_column(Integer, nullable=False)
    row_18: Mapped[int] = mapped_column(Integer, nullable=False)
    row_43: Mapped[int] = mapped_column(Integer, nullable=False)
    row_33: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    row_12: Mapped[int] = mapped_column(Integer, nullable=False)
    row_24: Mapped[int] = mapped_column(Integer, nullable=False)
    row_37: Mapped[int] = mapped_column(Integer, nullable=False)
    row_9: Mapped[int] = mapped_column(Integer, nullable=False)
    row_32: Mapped[int] = mapped_column(Integer, nullable=False)
    row_34: Mapped[int] = mapped_column(Integer, nullable=False)
    row_39: Mapped[int] = mapped_column(Integer, nullable=False)
    row_21: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbFrame(Base):
    __tablename__ = 'nbb_frame'

    row_39: Mapped[int] = mapped_column(Integer, nullable=False)
    row_22: Mapped[int] = mapped_column(Integer, nullable=False)
    row_28: Mapped[int] = mapped_column(Integer, nullable=False)
    row_13: Mapped[int] = mapped_column(Integer, nullable=False)
    row_16: Mapped[int] = mapped_column(Integer, nullable=False)
    row_19: Mapped[int] = mapped_column(Integer, nullable=False)
    row_35: Mapped[int] = mapped_column(Integer, nullable=False)
    row_38: Mapped[int] = mapped_column(Integer, nullable=False)
    row_44: Mapped[int] = mapped_column(Integer, nullable=False)
    row_53: Mapped[int] = mapped_column(Integer, nullable=False)
    row_47: Mapped[int] = mapped_column(Integer, nullable=False)
    row_60: Mapped[int] = mapped_column(Integer, nullable=False)
    row_58: Mapped[int] = mapped_column(Integer, nullable=False)
    row_1: Mapped[int] = mapped_column(Integer, nullable=False)
    min_clear_num: Mapped[int] = mapped_column(Integer, nullable=False)
    row_23: Mapped[int] = mapped_column(Integer, nullable=False)
    row_43: Mapped[int] = mapped_column(Integer, nullable=False)
    lane: Mapped[int] = mapped_column(Integer, nullable=False)
    row_21: Mapped[int] = mapped_column(Integer, nullable=False)
    row_30: Mapped[int] = mapped_column(Integer, nullable=False)
    row_24: Mapped[int] = mapped_column(Integer, nullable=False)
    row_31: Mapped[int] = mapped_column(Integer, nullable=False)
    row_9: Mapped[int] = mapped_column(Integer, nullable=False)
    row_37: Mapped[int] = mapped_column(Integer, nullable=False)
    row_2: Mapped[int] = mapped_column(Integer, nullable=False)
    row_57: Mapped[int] = mapped_column(Integer, nullable=False)
    row_5: Mapped[int] = mapped_column(Integer, nullable=False)
    row_55: Mapped[int] = mapped_column(Integer, nullable=False)
    row_18: Mapped[int] = mapped_column(Integer, nullable=False)
    row_33: Mapped[int] = mapped_column(Integer, nullable=False)
    row_52: Mapped[int] = mapped_column(Integer, nullable=False)
    row_4: Mapped[int] = mapped_column(Integer, nullable=False)
    row_25: Mapped[int] = mapped_column(Integer, nullable=False)
    row_51: Mapped[int] = mapped_column(Integer, nullable=False)
    row_48: Mapped[int] = mapped_column(Integer, nullable=False)
    row_12: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    row_6: Mapped[int] = mapped_column(Integer, nullable=False)
    row_10: Mapped[int] = mapped_column(Integer, nullable=False)
    row_26: Mapped[int] = mapped_column(Integer, nullable=False)
    row_40: Mapped[int] = mapped_column(Integer, nullable=False)
    row_17: Mapped[int] = mapped_column(Integer, nullable=False)
    row_8: Mapped[int] = mapped_column(Integer, nullable=False)
    row_27: Mapped[int] = mapped_column(Integer, nullable=False)
    row_56: Mapped[int] = mapped_column(Integer, nullable=False)
    row_34: Mapped[int] = mapped_column(Integer, nullable=False)
    row_42: Mapped[int] = mapped_column(Integer, nullable=False)
    row_7: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    row_50: Mapped[int] = mapped_column(Integer, nullable=False)
    row_15: Mapped[int] = mapped_column(Integer, nullable=False)
    row_49: Mapped[int] = mapped_column(Integer, nullable=False)
    row_14: Mapped[int] = mapped_column(Integer, nullable=False)
    row_45: Mapped[int] = mapped_column(Integer, nullable=False)
    row_41: Mapped[int] = mapped_column(Integer, nullable=False)
    row_20: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False)
    row_59: Mapped[int] = mapped_column(Integer, nullable=False)
    row_36: Mapped[int] = mapped_column(Integer, nullable=False)
    row_3: Mapped[int] = mapped_column(Integer, nullable=False)
    row_46: Mapped[int] = mapped_column(Integer, nullable=False)
    row_11: Mapped[int] = mapped_column(Integer, nullable=False)
    row_54: Mapped[int] = mapped_column(Integer, nullable=False)
    row_29: Mapped[int] = mapped_column(Integer, nullable=False)
    row_32: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbFrameLottery(Base):
    __tablename__ = 'nbb_frame_lottery'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    difficulty_3: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_4: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_2: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_1: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbModeSetting(Base):
    __tablename__ = 'nbb_mode_setting'

    length: Mapped[int] = mapped_column(Integer, nullable=False)
    soldier_init_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mode_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    support_ratio: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbNaviComment(Base):
    __tablename__ = 'nbb_navi_comment'

    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class NbbObjDatum(Base):
    __tablename__ = 'nbb_obj_data'

    obj_type: Mapped[int] = mapped_column(Integer, nullable=False)
    obj_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    obj_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    obj_value: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbScoreReward(Base):
    __tablename__ = 'nbb_score_reward'

    detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    nbb_chara_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbSpeedSetting(Base):
    __tablename__ = 'nbb_speed_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)


class NbbSupportDetail(Base):
    __tablename__ = 'nbb_support_detail'

    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    support_time: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_6: Mapped[int] = mapped_column(Integer, nullable=False)
    support_type: Mapped[int] = mapped_column(Integer, nullable=False)
    value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    support_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class NbbSupportFrame(Base):
    __tablename__ = 'nbb_support_frame'

    row_5: Mapped[int] = mapped_column(Integer, nullable=False)
    row_38: Mapped[int] = mapped_column(Integer, nullable=False)
    row_56: Mapped[int] = mapped_column(Integer, nullable=False)
    row_17: Mapped[int] = mapped_column(Integer, nullable=False)
    row_14: Mapped[int] = mapped_column(Integer, nullable=False)
    row_27: Mapped[int] = mapped_column(Integer, nullable=False)
    row_53: Mapped[int] = mapped_column(Integer, nullable=False)
    min_clear_num: Mapped[int] = mapped_column(Integer, nullable=False)
    row_4: Mapped[int] = mapped_column(Integer, nullable=False)
    row_36: Mapped[int] = mapped_column(Integer, nullable=False)
    row_51: Mapped[int] = mapped_column(Integer, nullable=False)
    row_24: Mapped[int] = mapped_column(Integer, nullable=False)
    row_20: Mapped[int] = mapped_column(Integer, nullable=False)
    row_47: Mapped[int] = mapped_column(Integer, nullable=False)
    row_18: Mapped[int] = mapped_column(Integer, nullable=False)
    row_55: Mapped[int] = mapped_column(Integer, nullable=False)
    row_26: Mapped[int] = mapped_column(Integer, nullable=False)
    row_10: Mapped[int] = mapped_column(Integer, nullable=False)
    row_41: Mapped[int] = mapped_column(Integer, nullable=False)
    row_44: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    row_2: Mapped[int] = mapped_column(Integer, nullable=False)
    row_42: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_id: Mapped[int] = mapped_column(Integer, nullable=False)
    row_22: Mapped[int] = mapped_column(Integer, nullable=False)
    row_40: Mapped[int] = mapped_column(Integer, nullable=False)
    row_54: Mapped[int] = mapped_column(Integer, nullable=False)
    row_60: Mapped[int] = mapped_column(Integer, nullable=False)
    row_45: Mapped[int] = mapped_column(Integer, nullable=False)
    row_46: Mapped[int] = mapped_column(Integer, nullable=False)
    row_30: Mapped[int] = mapped_column(Integer, nullable=False)
    lane: Mapped[int] = mapped_column(Integer, nullable=False)
    row_37: Mapped[int] = mapped_column(Integer, nullable=False)
    row_35: Mapped[int] = mapped_column(Integer, nullable=False)
    row_57: Mapped[int] = mapped_column(Integer, nullable=False)
    row_19: Mapped[int] = mapped_column(Integer, nullable=False)
    row_9: Mapped[int] = mapped_column(Integer, nullable=False)
    row_39: Mapped[int] = mapped_column(Integer, nullable=False)
    row_7: Mapped[int] = mapped_column(Integer, nullable=False)
    row_3: Mapped[int] = mapped_column(Integer, nullable=False)
    row_52: Mapped[int] = mapped_column(Integer, nullable=False)
    row_12: Mapped[int] = mapped_column(Integer, nullable=False)
    row_1: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    row_31: Mapped[int] = mapped_column(Integer, nullable=False)
    row_49: Mapped[int] = mapped_column(Integer, nullable=False)
    row_21: Mapped[int] = mapped_column(Integer, nullable=False)
    row_25: Mapped[int] = mapped_column(Integer, nullable=False)
    row_29: Mapped[int] = mapped_column(Integer, nullable=False)
    row_6: Mapped[int] = mapped_column(Integer, nullable=False)
    row_43: Mapped[int] = mapped_column(Integer, nullable=False)
    row_28: Mapped[int] = mapped_column(Integer, nullable=False)
    row_16: Mapped[int] = mapped_column(Integer, nullable=False)
    row_48: Mapped[int] = mapped_column(Integer, nullable=False)
    row_59: Mapped[int] = mapped_column(Integer, nullable=False)
    row_58: Mapped[int] = mapped_column(Integer, nullable=False)
    row_11: Mapped[int] = mapped_column(Integer, nullable=False)
    row_34: Mapped[int] = mapped_column(Integer, nullable=False)
    row_32: Mapped[int] = mapped_column(Integer, nullable=False)
    row_33: Mapped[int] = mapped_column(Integer, nullable=False)
    row_13: Mapped[int] = mapped_column(Integer, nullable=False)
    row_15: Mapped[int] = mapped_column(Integer, nullable=False)
    row_8: Mapped[int] = mapped_column(Integer, nullable=False)
    row_23: Mapped[int] = mapped_column(Integer, nullable=False)
    row_50: Mapped[int] = mapped_column(Integer, nullable=False)


class NopDramaDatum(Base):
    __tablename__ = 'nop_drama_data'

    talk_pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    talk_pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    position_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    col_size_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    create_front_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talk_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    idle_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    event_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    col_pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    create_back_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_id: Mapped[int] = mapped_column(Integer, nullable=False)
    col_size_y: Mapped[int] = mapped_column(Integer, nullable=False)


class NopDramaScript(Base):
    __tablename__ = 'nop_drama_script'

    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class NotifDatum(Base):
    __tablename__ = 'notif_data'

    comment: Mapped[str] = mapped_column(Text, nullable=False)
    notif_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class NydSetting(Base):
    __tablename__ = 'nyd_setting'

    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    complete_emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class NydStoryDatum(Base):
    __tablename__ = 'nyd_story_data'

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_first: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    nyd_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)


class NyxDramaDatum(Base):
    __tablename__ = 'nyx_drama_data'

    condition_locked_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_unlocked_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_phase: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class NyxDramaScript(Base):
    __tablename__ = 'nyx_drama_script'

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)


class NyxPhaseDatum(Base):
    __tablename__ = 'nyx_phase_data'

    story_phase: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    phase_title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_boss: Mapped[int] = mapped_column(Integer, nullable=False)


class NyxStoryDatum(Base):
    __tablename__ = 'nyx_story_data'

    adv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    story_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_phase: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    adv_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_count: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)


class NyxStoryScript(Base):
    __tablename__ = 'nyx_story_script'

    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class OddsNameDatum(Base):
    __tablename__ = 'odds_name_data'

    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    odds_file: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class OmpDrama(Base):
    __tablename__ = 'omp_drama'

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)


class OmpStoryDatum(Base):
    __tablename__ = 'omp_story_data'

    story_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    d4c4454de46546adbfb72fb4cf1febb113b69a0efdc466a476ce182e01a6f284: Mapped[int] = mapped_column(Integer, nullable=False)
    is_readable_on_result: Mapped[int] = mapped_column(Integer, nullable=False)
    omp_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    f6511b64957561cc87b56c9f55f73a578c1e89c00cd50154093b027260412303: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ParamType(Base):
    __tablename__ = 'param_type'

    ratio: Mapped[int] = mapped_column(Integer, nullable=False)
    parameter_name: Mapped[str] = mapped_column(Text, nullable=False)
    is_percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    parameter_type: Mapped[int] = mapped_column(Integer, primary_key=True)


class PctComboCoefficient(Base):
    __tablename__ = 'pct_combo_coefficient'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    combo_min: Mapped[int] = mapped_column(Integer, nullable=False)
    combo_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    combo_max: Mapped[int] = mapped_column(Integer, nullable=False)


class PctEvaluation(Base):
    __tablename__ = 'pct_evaluation'

    meet_width: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_point: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fever_point: Mapped[int] = mapped_column(Integer, nullable=False)


class PctGamingMotion(Base):
    __tablename__ = 'pct_gaming_motion'

    point: Mapped[int] = mapped_column(Integer, nullable=False)
    good_count: Mapped[int] = mapped_column(Integer, nullable=False)
    motion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    perfect_count: Mapped[int] = mapped_column(Integer, nullable=False)
    nice_count: Mapped[int] = mapped_column(Integer, nullable=False)


class PctItempoint(Base):
    __tablename__ = 'pct_itempoint'

    pct_point_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class PctResult(Base):
    __tablename__ = 'pct_result'

    comment_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    score_from: Mapped[int] = mapped_column(Integer, nullable=False)
    score_to: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)


class PctReward(Base):
    __tablename__ = 'pct_reward'

    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_point: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_point_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)


class PctSystem(Base):
    __tablename__ = 'pct_system'

    fever_point_max: Mapped[int] = mapped_column(Integer, nullable=False)
    fever_time: Mapped[int] = mapped_column(Integer, nullable=False)
    chara2_gauge_choice: Mapped[int] = mapped_column(Integer, nullable=False)
    chara2: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_time: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fever_revention_time: Mapped[int] = mapped_column(Integer, nullable=False)
    chara1: Mapped[int] = mapped_column(Integer, nullable=False)
    chara1_gauge_choice: Mapped[int] = mapped_column(Integer, nullable=False)
    pct_base_speed: Mapped[int] = mapped_column(Integer, nullable=False)


class PctSystemFruits(Base):
    __tablename__ = 'pct_system_fruits'

    appearance_pattern: Mapped[str] = mapped_column(Text, nullable=False)
    wait_time: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appearance: Mapped[int] = mapped_column(Integer, nullable=False)
    last_time: Mapped[int] = mapped_column(Integer, nullable=False)
    bar_split: Mapped[int] = mapped_column(Integer, nullable=False)
    appearance_chara_odds: Mapped[int] = mapped_column(Integer, nullable=False)


class PctTapSpeed(Base):
    __tablename__ = 'pct_tap_speed'

    combo_count: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speed_magnification: Mapped[int] = mapped_column(Integer, nullable=False)


class PkbBatterCondition(Base):
    __tablename__ = 'pkb_batter_condition'

    ability_name: Mapped[str] = mapped_column(Text, nullable=False)
    is_playable: Mapped[int] = mapped_column(Integer, nullable=False)
    batter_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meet: Mapped[int] = mapped_column(Integer, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)
    ability_detail: Mapped[str] = mapped_column(Text, nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    critical: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    pkb_score: Mapped[int] = mapped_column(Integer, nullable=False)


class PkbDrama(Base):
    __tablename__ = 'pkb_drama'

    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)


class PkbDramaDatum(Base):
    __tablename__ = 'pkb_drama_data'

    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_batter_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_pitcher_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_pitcher_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_batter_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class PkbNaviComment(Base):
    __tablename__ = 'pkb_navi_comment'

    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class PkbPitcherBallType(Base):
    __tablename__ = 'pkb_pitcher_ball_type'

    ball_type_name: Mapped[str] = mapped_column(Text, nullable=False)
    ball_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    pitcher_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class PkbReward(Base):
    __tablename__ = 'pkb_reward'

    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pkb_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)


class PositionSetting(Base):
    __tablename__ = 'position_setting'

    position_setting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    front: Mapped[int] = mapped_column(Integer, nullable=False)
    middle: Mapped[int] = mapped_column(Integer, nullable=False)


class PrizegachaDatum(Base):
    __tablename__ = 'prizegacha_data'

    prize_memory_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    d64865c322b124f729315c4cd85c8d033d6e788e1f9af600499538a9ed5b04ae: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_25: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_17: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_24: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_20: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_prize10: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_prize1: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_14: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    prizegacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prize_memory_id_11: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_23: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_27: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_26: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_12: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_28: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_prize_fixed_compensation: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_13: Mapped[int] = mapped_column(Integer, nullable=False)
    ad8514391f7ac9ec2a62580492141ded61acd7388dbd39961ffb52c618ee1418: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_18: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_30: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_16: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_22: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_15: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_19: Mapped[int] = mapped_column(Integer, nullable=False)
    e8fa39cbab4bdee1b4a180671f7c589e053b6dc65eff181c225e8804bcbc41a0: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_29: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_memory_id_21: Mapped[int] = mapped_column(Integer, nullable=False)


class PrizegachaSpDatum(Base):
    __tablename__ = 'prizegacha_sp_data'

    disp_rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)


class PrizegachaSpDetail(Base):
    __tablename__ = 'prizegacha_sp_detail'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_rarity: Mapped[int] = mapped_column(Integer, primary_key=True)


class ProfileFrame(Base):
    __tablename__ = 'profile_frame'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class PromotionBonus(Base):
    __tablename__ = 'promotion_bonus'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)


class PsyDrama(Base):
    __tablename__ = 'psy_drama'

    condition_psy_product_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    release_psy_product_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_psy_product_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_total_eat: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_5: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_chara_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_psy_product_3: Mapped[int] = mapped_column(Integer, nullable=False)


class PsyDramaScript(Base):
    __tablename__ = 'psy_drama_script'

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)


class PsyNote(Base):
    __tablename__ = 'psy_note'

    psy_product_name: Mapped[str] = mapped_column(Text, nullable=False)
    init_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    flavor_3: Mapped[str] = mapped_column(Text, nullable=False)
    condition_flavor_1: Mapped[int] = mapped_column(Integer, nullable=False)
    psy_product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_flavor_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    flavor_2: Mapped[str] = mapped_column(Text, nullable=False)
    flavor_1: Mapped[str] = mapped_column(Text, nullable=False)


class PsyReward(Base):
    __tablename__ = 'psy_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestAnnihilation(Base):
    __tablename__ = 'quest_annihilation'

    quest_effect_position: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    se_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class QuestAreaDatum(Base):
    __tablename__ = 'quest_area_data'

    area_display_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)


class QuestConditionDatum(Base):
    __tablename__ = 'quest_condition_data'

    condition_quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    release_quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestDatum(Base):
    __tablename__ = 'quest_data'

    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    camera_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    add_treasure_num: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    camera_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    camera_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    _8c5efaf258e8b459188b0654bde6f8e14176cccb7ae3a28d567f6e1fd50f7853: Mapped[int] = mapped_column('8c5efaf258e8b459188b0654bde6f8e14176cccb7ae3a28d567f6e1fd50f7853', Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestDefeatNotice(Base):
    __tablename__ = 'quest_defeat_notice'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    required_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    required_team_level: Mapped[int] = mapped_column(Integer, nullable=False)


class QuestRewardDatum(Base):
    __tablename__ = 'quest_reward_data'

    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class RagDramaScript(Base):
    __tablename__ = 'rag_drama_script'

    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class RagStoryDatum(Base):
    __tablename__ = 'rag_story_data'

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RagTopDrama(Base):
    __tablename__ = 'rag_top_drama'

    rag_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Rarity6QuestDatum(Base):
    __tablename__ = 'rarity_6_quest_data'

    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity_6_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)


class RecoverStamina(Base):
    __tablename__ = 'recover_stamina'

    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, primary_key=True)


class RedeemStaticPriceGroup(Base):
    __tablename__ = 'redeem_static_price_group'

    condition_category: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)


class RedeemUnit(Base):
    __tablename__ = 'redeem_unit'

    consume_num: Mapped[str] = mapped_column(Text, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_category: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RedeemUnitBg(Base):
    __tablename__ = 'redeem_unit_bg'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ReplaceTutorialCharacter(Base):
    __tablename__ = 'replace_tutorial_character'

    navi_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    navi_position_x: Mapped[int] = mapped_column(Integer, nullable=False)


class ResistDatum(Base):
    __tablename__ = 'resist_data'

    ailment_92: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_71: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_9: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_49: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_87: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_46: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_26: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_69: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_82: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_61: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_52: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_30: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_12: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_7: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_18: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_84: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_19: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_36: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_24: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_64: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_97: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_85: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_27: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_53: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_76: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_74: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_65: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_66: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_22: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_98: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_20: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_58: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_25: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_23: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_43: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_79: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_88: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_33: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_68: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_17: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_10: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ailment_94: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_80: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_55: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_78: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_41: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_50: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_38: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_60: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_29: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_45: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_62: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_72: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_32: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_73: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_47: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_100: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_11: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_40: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_42: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_89: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_91: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_59: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_13: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_21: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_16: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_54: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_67: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_31: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_75: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_57: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_28: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_37: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_56: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_15: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_8: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_83: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_90: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_93: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_48: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_81: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_70: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_95: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_6: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_99: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_86: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_51: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_63: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_39: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_14: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_34: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_77: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_35: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_44: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_96: Mapped[int] = mapped_column(Integer, nullable=False)
    ailment_4: Mapped[int] = mapped_column(Integer, nullable=False)


class ResistVariationDatum(Base):
    __tablename__ = 'resist_variation_data'

    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ReturnSpecialfesBanner(Base):
    __tablename__ = 'return_specialfes_banner'

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banner_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_8: Mapped[int] = mapped_column(Integer, nullable=False)


class RewardCollectGuide(Base):
    __tablename__ = 'reward_collect_guide'

    quest_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomChange(Base):
    __tablename__ = 'room_change'

    change_start: Mapped[str] = mapped_column(Text, nullable=False)
    change_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_end: Mapped[str] = mapped_column(Text, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomCharacterPersonality(Base):
    __tablename__ = 'room_character_personality'

    character_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    personality_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomCharacterSkinColor(Base):
    __tablename__ = 'room_character_skin_color'

    skin_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomChatFormation(Base):
    __tablename__ = 'room_chat_formation'

    unit_2_x: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_dir: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_dir: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_x: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id2: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id3: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_x: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id5: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id1: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_dir: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id4: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_y: Mapped[Optional[int]] = mapped_column(Integer)
    unit_3_dir: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_dir: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id2: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id5: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_x: Mapped[Optional[int]] = mapped_column(Integer)
    unit_id3: Mapped[Optional[int]] = mapped_column(Integer)
    unit_5_x: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id4: Mapped[Optional[int]] = mapped_column(Integer)
    ignore_unit_id1: Mapped[Optional[int]] = mapped_column(Integer)
    unit_4_y: Mapped[Optional[int]] = mapped_column(Integer)


class RoomChatInfo(Base):
    __tablename__ = 'room_chat_info'

    scenario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    formation_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomChatScenario(Base):
    __tablename__ = 'room_chat_scenario'

    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    delay: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    anime_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_pos_no: Mapped[int] = mapped_column(Integer, nullable=False)
    scenario_idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    affect_type: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomEffect(Base):
    __tablename__ = 'room_effect'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    arcade: Mapped[int] = mapped_column(Integer, nullable=False)
    poster: Mapped[int] = mapped_column(Integer, nullable=False)
    jukebox: Mapped[int] = mapped_column(Integer, nullable=False)
    nebbia: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_get: Mapped[int] = mapped_column(Integer, nullable=False)
    vegetable: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomEffectRewardGet(Base):
    __tablename__ = 'room_effect_reward_get'

    stock_mid_step: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inc_step: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_min_step: Mapped[str] = mapped_column(Text, nullable=False)
    interval_second: Mapped[int] = mapped_column(Integer, nullable=False)
    max_count: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomEmotionIcon(Base):
    __tablename__ = 'room_emotion_icon'

    enable_auto: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enable_tap: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomExclusiveCondition(Base):
    __tablename__ = 'room_exclusive_condition'

    notification: Mapped[str] = mapped_column(Text, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomItem(Base):
    __tablename__ = 'room_item'

    category_action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enable_remove: Mapped[int] = mapped_column(Integer, nullable=False)
    sort: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_item_num: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_start: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    max_possession_num: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_end: Mapped[str] = mapped_column(Text, nullable=False)
    sold_price: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_open_type: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_new_disp_end: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_open_value: Mapped[int] = mapped_column(Integer, nullable=False)
    shop_open_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomItemAnnouncement(Base):
    __tablename__ = 'room_item_announcement'

    announcement_end: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    announcement_start: Mapped[str] = mapped_column(Text, nullable=False)
    announcement_text: Mapped[str] = mapped_column(Text, nullable=False)


class RoomItemDetail(Base):
    __tablename__ = 'room_item_detail'

    lvup_trigger_id: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, primary_key=True)
    lvup_trigger_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_detail: Mapped[str] = mapped_column(Text, nullable=False)
    lvup_time: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_item1_num: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_item1_type: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    lvup_trigger_value: Mapped[int] = mapped_column(Integer, nullable=False)
    _8e3cc55e48529ad8960cdbad832b181d578c454ce18180a7adbcb997d8f339af: Mapped[int] = mapped_column('8e3cc55e48529ad8960cdbad832b181d578c454ce18180a7adbcb997d8f339af', Integer, nullable=False)


class RoomItemGetAnnouncement(Base):
    __tablename__ = 'room_item_get_announcement'

    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    room_announcement_name: Mapped[str] = mapped_column(Text, nullable=False)
    get_date: Mapped[str] = mapped_column(Text, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomReleaseDatum(Base):
    __tablename__ = 'room_release_data'

    system_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomReplaceUnit(Base):
    __tablename__ = 'room_replace_unit'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    replace_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomSetup(Base):
    __tablename__ = 'room_setup'

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    grid_height: Mapped[int] = mapped_column(Integer, nullable=False)
    grid_width: Mapped[int] = mapped_column(Integer, nullable=False)
    room_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class RoomSkinColor(Base):
    __tablename__ = 'room_skin_color'

    color_blue: Mapped[int] = mapped_column(Integer, nullable=False)
    color_green: Mapped[int] = mapped_column(Integer, nullable=False)
    skin_color_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    color_red: Mapped[int] = mapped_column(Integer, nullable=False)


class RoomUnitComments(Base):
    __tablename__ = 'room_unit_comments'

    time: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    insert_word_type: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beloved_step: Mapped[int] = mapped_column(Integer, nullable=False)


class SdNaviComment(Base):
    __tablename__ = 'sd_navi_comment'

    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    motion_type: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class SeasonPack(Base):
    __tablename__ = 'season_pack'

    after_text: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    add_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pack_type: Mapped[int] = mapped_column(Integer, nullable=False)
    item_record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_rate_1: Mapped[int] = mapped_column(Integer, nullable=False)
    receive_text: Mapped[str] = mapped_column(Text, nullable=False)
    term: Mapped[int] = mapped_column(Integer, nullable=False)
    gift_message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    repurchase_day: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _53244168f7e330ff98fb41e714e014e8aec986886c86b97abea66af797582639: Mapped[int] = mapped_column('53244168f7e330ff98fb41e714e014e8aec986886c86b97abea66af797582639', Integer, nullable=False)
    system_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonpassFoundation(Base):
    __tablename__ = 'seasonpass_foundation'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    level_max: Mapped[int] = mapped_column(Integer, nullable=False)
    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    point_change_type: Mapped[int] = mapped_column(Integer, nullable=False)
    advance_jewel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    key_jewel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    level_price: Mapped[int] = mapped_column(Integer, nullable=False)
    final_jewel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    weekly_point: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    extra_level: Mapped[int] = mapped_column(Integer, nullable=False)
    proportion: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[str] = mapped_column(Text, nullable=False)
    per_level_point: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonpassLevelReward(Base):
    __tablename__ = 'seasonpass_level_reward'

    charge_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    free_reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    degree: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    free_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    charge_reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    free_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    charge_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SeasonpassMissionDatum(Base):
    __tablename__ = 'seasonpass_mission_data'

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    seasonpass_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class SeasonpassMissionRewardDatum(Base):
    __tablename__ = 'seasonpass_mission_reward_data'

    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class SecretDungeonEmblemMission(Base):
    __tablename__ = 'secret_dungeon_emblem_mission'

    emblem_description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_description: Mapped[str] = mapped_column(Text, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SecretDungeonEmblemReward(Base):
    __tablename__ = 'secret_dungeon_emblem_reward'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class SecretDungeonEnemyInfo(Base):
    __tablename__ = 'secret_dungeon_enemy_info'

    enemy_name: Mapped[str] = mapped_column(Text, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SecretDungeonFloorReward(Base):
    __tablename__ = 'secret_dungeon_floor_reward'

    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clear_effect_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_count: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SecretDungeonFloorSetting(Base):
    __tablename__ = 'secret_dungeon_floor_setting'

    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_identify: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    floor_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SecretDungeonQuestDatum(Base):
    __tablename__ = 'secret_dungeon_quest_data'

    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_monster_scale_5: Mapped[float] = mapped_column(REAL, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_3: Mapped[float] = mapped_column(REAL, nullable=False)
    emax: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_4: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_type: Mapped[int] = mapped_column(Integer, nullable=False)
    multi_target_effect_time: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_monster_height: Mapped[float] = mapped_column(REAL, nullable=False)
    parts_hp_save_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_scale_1: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    dungeon_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    c154a57a02c4be58a1a7f10c8b323e2798447d44573d789a21b81a82175d9d68: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_scale_3: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_2: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_scale_4: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reset_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    _2ebdda5410bddeaa6251460bd1d29262963cd308097003b45f0710b4b56f13bb: Mapped[int] = mapped_column('2ebdda5410bddeaa6251460bd1d29262963cd308097003b45f0710b4b56f13bb', Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_5: Mapped[float] = mapped_column(REAL, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_6: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    _15da8e25f58030e1345b1618ef4788ae6aad7430a6e95a799cd5faad012ae231: Mapped[int] = mapped_column('15da8e25f58030e1345b1618ef4788ae6aad7430a6e95a799cd5faad012ae231', Integer, nullable=False)
    quest_detail_monster_scale_2: Mapped[float] = mapped_column(REAL, nullable=False)
    fixed_start_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    dungeon_quest_detail_monster_position_x_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)


class SecretDungeonSchedule(Base):
    __tablename__ = 'secret_dungeon_schedule'

    dungeon_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)


class SekaiAddTimesDatum(Base):
    __tablename__ = 'sekai_add_times_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiBossDamageRankReward(Base):
    __tablename__ = 'sekai_boss_damage_rank_reward'

    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_rank_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_from: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking_to: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiBossFixReward(Base):
    __tablename__ = 'sekai_boss_fix_reward'

    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_total_damage: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiBossMode(Base):
    __tablename__ = 'sekai_boss_mode'

    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    sekai_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    score_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_enemy_level: Mapped[str] = mapped_column(Text, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_size: Mapped[float] = mapped_column(REAL, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_gold_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_boss_mode_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limited_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_monster_height: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiEnemyParameter(Base):
    __tablename__ = 'sekai_enemy_parameter'

    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[str] = mapped_column(Text, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SekaiSchedule(Base):
    __tablename__ = 'sekai_schedule'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    damage_rank_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_losstime: Mapped[str] = mapped_column(Text, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    last_sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_end: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiTopDatum(Base):
    __tablename__ = 'sekai_top_data'

    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    top_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_time_from: Mapped[str] = mapped_column(Text, nullable=False)
    scale_ratio: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    boss_hp_from: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    boss_hp_to: Mapped[str] = mapped_column(Text, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    sekai_boss_mode_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_time_to: Mapped[str] = mapped_column(Text, nullable=False)


class SekaiTopStoryDatum(Base):
    __tablename__ = 'sekai_top_story_data'

    boss_time_from: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_time_to: Mapped[str] = mapped_column(Text, nullable=False)
    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SekaiUnlockStoryCondition(Base):
    __tablename__ = 'sekai_unlock_story_condition'

    sekai_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_fix_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_entry: Mapped[int] = mapped_column(Integer, nullable=False)


class SelectionTicketDatum(Base):
    __tablename__ = 'selection_ticket_data'

    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    exchange_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SerialCodeDatum(Base):
    __tablename__ = 'serial_code_data'

    serial_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    d31c8101be0a84db51c951ddd2f139296618fda52591bc8e467a25ac4deab31f: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_name: Mapped[str] = mapped_column(Text, nullable=False)
    limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class SerialGroupDatum(Base):
    __tablename__ = 'serial_group_data'

    serial_campaign_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    serial_campaign_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    campaign_name: Mapped[str] = mapped_column(Text, nullable=False)
    serial_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    serial_campaign_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_campaign_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class SeriesUnlockCondition(Base):
    __tablename__ = 'series_unlock_condition'

    sequel_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriBattleMissionDatum(Base):
    __tablename__ = 'shiori_battle_mission_data'

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriBoss(Base):
    __tablename__ = 'shiori_boss'

    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_collider_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_x: Mapped[float] = mapped_column(REAL, nullable=False)
    deatail_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    map_size: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_position_y: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    td_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    map_arrow_offset: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_on_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[float] = mapped_column(REAL, nullable=False)
    qd_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_display_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_aura_size: Mapped[float] = mapped_column(REAL, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriBossCondition(Base):
    __tablename__ = 'shiori_boss_condition'

    _1fe8344e4c3faed240f1800670f4552c29add8eb5c98bcc3f5b7b63a6c828e88: Mapped[int] = mapped_column('1fe8344e4c3faed240f1800670f4552c29add8eb5c98bcc3f5b7b63a6c828e88', Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    _8d65aae5dfc6e387c9e5dc056553b1418bebba9ecf7e08100d140f6c3ebd6bb3: Mapped[int] = mapped_column('8d65aae5dfc6e387c9e5dc056553b1418bebba9ecf7e08100d140f6c3ebd6bb3', Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriDescription(Base):
    __tablename__ = 'shiori_description'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriEnemyParameter(Base):
    __tablename__ = 'shiori_enemy_parameter'

    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriEventList(Base):
    __tablename__ = 'shiori_event_list'

    condition_chara_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    series_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    help_index: Mapped[str] = mapped_column(Text, nullable=False)
    banner_y: Mapped[int] = mapped_column(Integer, nullable=False)
    original_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_shiori_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriItem(Base):
    __tablename__ = 'shiori_item'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_material_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_material_id_1: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriMissionRewardDatum(Base):
    __tablename__ = 'shiori_mission_reward_data'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriQuest(Base):
    __tablename__ = 'shiori_quest'

    story_id_wavestart_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    icon_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_wavestart_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_waveend_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_wavestart_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    icon_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    drop_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_odds: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_offset_y: Mapped[float] = mapped_column(REAL, nullable=False)
    story_id_waveend_2: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriQuestArea(Base):
    __tablename__ = 'shiori_quest_area'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    open_tutorial_id: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_width: Mapped[int] = mapped_column(Integer, nullable=False)
    area_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    tutorial_param_1: Mapped[str] = mapped_column(Text, nullable=False)
    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    tutorial_param_2: Mapped[str] = mapped_column(Text, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_height: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShioriQuestCondition(Base):
    __tablename__ = 'shiori_quest_condition'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_main_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ShioriStationaryMissionDatum(Base):
    __tablename__ = 'shiori_stationary_mission_data'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)


class ShioriUnlockUnitCondition(Base):
    __tablename__ = 'shiori_unlock_unit_condition'

    description_1: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    top_description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_mission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description_2: Mapped[str] = mapped_column(Text, nullable=False)


class ShioriWaveGroupDatum(Base):
    __tablename__ = 'shiori_wave_group_data'

    disp_reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_1: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_2: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_odds_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_lot_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_odds_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class ShopItemDescription(Base):
    __tablename__ = 'shop_item_description'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ShopStaticPriceGroup(Base):
    __tablename__ = 'shop_static_price_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buy_count_from: Mapped[int] = mapped_column(Integer, nullable=False)
    buy_count_to: Mapped[int] = mapped_column(Integer, nullable=False)
    price_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrChara(Base):
    __tablename__ = 'sjr_chara'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    resume_time: Mapped[float] = mapped_column(REAL, nullable=False)
    proper_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    recommend_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sjr_chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spring: Mapped[int] = mapped_column(Integer, nullable=False)
    personality: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tired_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tp_length: Mapped[float] = mapped_column(REAL, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrCourse(Base):
    __tablename__ = 'sjr_course'

    rail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    peek_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    feature: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[float] = mapped_column(REAL, nullable=False)
    rail_3: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrDramaScript(Base):
    __tablename__ = 'sjr_drama_script'

    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrEmblem(Base):
    __tablename__ = 'sjr_emblem'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    emblem_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrFeatureGroup(Base):
    __tablename__ = 'sjr_feature_group'

    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    feature_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrNameFormer(Base):
    __tablename__ = 'sjr_name_former'

    condition_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    constrain_group: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    condition_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrNameLater(Base):
    __tablename__ = 'sjr_name_later'

    score_to: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    score_from: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_group: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrNpcActionOdds(Base):
    __tablename__ = 'sjr_npc_action_odds'

    action_odds_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rate: Mapped[int] = mapped_column(Integer, nullable=False)
    distance: Mapped[int] = mapped_column(Integer, nullable=False)
    angle: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrParameterEvaluation(Base):
    __tablename__ = 'sjr_parameter_evaluation'

    border_2: Mapped[float] = mapped_column(REAL, nullable=False)
    border_1: Mapped[float] = mapped_column(REAL, nullable=False)
    border_3: Mapped[float] = mapped_column(REAL, nullable=False)
    parameter_type: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrProperEvaluation(Base):
    __tablename__ = 'sjr_proper_evaluation'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    border_1: Mapped[int] = mapped_column(Integer, nullable=False)
    border_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrProperFeature(Base):
    __tablename__ = 'sjr_proper_feature'

    feature_group_3: Mapped[int] = mapped_column(Integer, nullable=False)
    proper_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feature_group_1: Mapped[int] = mapped_column(Integer, nullable=False)
    value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    feature_group_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrRail(Base):
    __tablename__ = 'sjr_rail'

    gimmick_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gimmick_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrReward(Base):
    __tablename__ = 'sjr_reward'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sjr_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)


class SjrScore(Base):
    __tablename__ = 'sjr_score'

    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_score: Mapped[int] = mapped_column(Integer, nullable=False)
    hard_bonus: Mapped[float] = mapped_column(REAL, nullable=False)
    first_score: Mapped[int] = mapped_column(Integer, nullable=False)
    normal_bonus: Mapped[float] = mapped_column(REAL, nullable=False)
    time_score: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_bonus: Mapped[float] = mapped_column(REAL, nullable=False)
    third_score: Mapped[int] = mapped_column(Integer, nullable=False)
    second_score: Mapped[int] = mapped_column(Integer, nullable=False)
    round: Mapped[int] = mapped_column(Integer, primary_key=True)


class SjrUbDatum(Base):
    __tablename__ = 'sjr_ub_data'

    ub_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    in_game_description: Mapped[str] = mapped_column(Text, nullable=False)
    ub_type: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ub_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    top_description: Mapped[str] = mapped_column(Text, nullable=False)


class SkeStoryDatum(Base):
    __tablename__ = 'ske_story_data'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    read_condition_event_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unlock_condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SkeStoryScript(Base):
    __tablename__ = 'ske_story_script'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)


class SkillAction(Base):
    __tablename__ = 'skill_action'

    action_value_1: Mapped[float] = mapped_column(REAL, nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_value_7: Mapped[float] = mapped_column(REAL, nullable=False)
    action_value_4: Mapped[float] = mapped_column(REAL, nullable=False)
    action_value_2: Mapped[float] = mapped_column(REAL, nullable=False)
    target_number: Mapped[int] = mapped_column(Integer, nullable=False)
    target_range: Mapped[int] = mapped_column(Integer, nullable=False)
    action_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_6: Mapped[float] = mapped_column(REAL, nullable=False)
    target_area: Mapped[int] = mapped_column(Integer, nullable=False)
    action_detail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    level_up_disp: Mapped[str] = mapped_column(Text, nullable=False)
    target_count: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    action_detail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_5: Mapped[float] = mapped_column(REAL, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_assignment: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    action_value_3: Mapped[float] = mapped_column(REAL, nullable=False)


class SkillCost(Base):
    __tablename__ = 'skill_cost'

    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    target_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class SkillDatum(Base):
    __tablename__ = 'skill_data'

    depend_action_7: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_6: Mapped[int] = mapped_column(Integer, nullable=False)
    action_7: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_10: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_ub_cool_time: Mapped[float] = mapped_column(REAL, nullable=False)
    action_2: Mapped[int] = mapped_column(Integer, nullable=False)
    action_3: Mapped[int] = mapped_column(Integer, nullable=False)
    action_1: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_3: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_4: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_8: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_9: Mapped[int] = mapped_column(Integer, nullable=False)
    action_4: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_1: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_area_width: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_2: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    depend_action_10: Mapped[int] = mapped_column(Integer, nullable=False)
    action_6: Mapped[int] = mapped_column(Integer, nullable=False)
    action_9: Mapped[int] = mapped_column(Integer, nullable=False)
    action_5: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_cast_time: Mapped[float] = mapped_column(REAL, nullable=False)
    action_8: Mapped[int] = mapped_column(Integer, nullable=False)
    depend_action_5: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text)


class SkipBossDatum(Base):
    __tablename__ = 'skip_boss_data'

    skip_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skip_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_motion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SkipMonsterDatum(Base):
    __tablename__ = 'skip_monster_data'

    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_skip_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SpBattleVoice(Base):
    __tablename__ = 'sp_battle_voice'

    value: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    voice_type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SpDetailVoice(Base):
    __tablename__ = 'sp_detail_voice'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cue_name_1: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_3: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_2: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_4: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name_5: Mapped[str] = mapped_column(Text, nullable=False)


class SpLoseVoice(Base):
    __tablename__ = 'sp_lose_voice'

    unit_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_only_disp: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker_unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)


class SpLoseVoiceGroup(Base):
    __tablename__ = 'sp_lose_voice_group'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speaker_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SpaceBattleDatum(Base):
    __tablename__ = 'space_battle_data'

    background: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    space_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    space_battle_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)


class SpaceSchedule(Base):
    __tablename__ = 'space_schedule'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)
    space_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sid: Mapped[int] = mapped_column(Integer, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SpaceTopDatum(Base):
    __tablename__ = 'space_top_data'

    part_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    space_battle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_battle_time: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    space_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    time_from: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time_to: Mapped[str] = mapped_column(Text, nullable=False)


class SpecialStill(Base):
    __tablename__ = 'special_still'

    back_momory_type: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SpecialStoryBanner(Base):
    __tablename__ = 'special_story_banner'

    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    remind_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class SpecialfesBanner(Base):
    __tablename__ = 'specialfes_banner'

    banner_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banner_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    banner_id_8: Mapped[int] = mapped_column(Integer, nullable=False)


class SpotDramaScriptDatum(Base):
    __tablename__ = 'spot_drama_script_data'

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class SpskillLabelDatum(Base):
    __tablename__ = 'spskill_label_data'

    normal_label_text: Mapped[str] = mapped_column(Text, nullable=False)
    sp_label_text: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SpskillLvInitializeDatum(Base):
    __tablename__ = 'spskill_lv_initialize_data'

    initialize_skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SreAddTimesDatum(Base):
    __tablename__ = 'sre_add_times_data'

    add_times_time: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    add_times: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SreBattleBonus(Base):
    __tablename__ = 'sre_battle_bonus'

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_bonus_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_hp: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    sre_battle_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_battle_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SreBattleBonusEffect(Base):
    __tablename__ = 'sre_battle_bonus_effect'

    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    text_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_battle_effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreBossDatum(Base):
    __tablename__ = 'sre_boss_data'

    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_finish_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    challenge_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    all_disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lane_priority_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    phase: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    challenge_odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    deck_number: Mapped[int] = mapped_column(Integer, nullable=False)
    lane_priority_5: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_5: Mapped[float] = mapped_column(REAL, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    disappearance_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    max_raid_hp: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    result_boss_position_y_1: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y_2: Mapped[float] = mapped_column(REAL, nullable=False)
    result_boss_position_y_3: Mapped[float] = mapped_column(REAL, nullable=False)
    expel_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_max: Mapped[int] = mapped_column(Integer, nullable=False)


class SreEffect(Base):
    __tablename__ = 'sre_effect'

    effect_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bonus_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_5: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_4: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_3: Mapped[int] = mapped_column(Integer, nullable=False)


class SreEffectiveUnit(Base):
    __tablename__ = 'sre_effective_unit'

    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    support_effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreEnemyParameter(Base):
    __tablename__ = 'sre_enemy_parameter'

    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreExterminationReward(Base):
    __tablename__ = 'sre_extermination_reward'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    extermination_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreMissionCategoryDatum(Base):
    __tablename__ = 'sre_mission_category_data'

    name: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreMissionDatum(Base):
    __tablename__ = 'sre_mission_data'

    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)


class SreMissionRewardDatum(Base):
    __tablename__ = 'sre_mission_reward_data'

    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreQuestDifficultyDatum(Base):
    __tablename__ = 'sre_quest_difficulty_data'

    sre_boss_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)


class SreSchedule(Base):
    __tablename__ = 'sre_schedule'

    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    close_story_condition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    close_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_bg: Mapped[str] = mapped_column(Text, nullable=False)
    top_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    close_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    sre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teaser_time: Mapped[str] = mapped_column(Text, nullable=False)


class SreWaveGroupDatum(Base):
    __tablename__ = 'sre_wave_group_data'

    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drop_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)


class SrtAction(Base):
    __tablename__ = 'srt_action'

    homare_action: Mapped[str] = mapped_column(Text, nullable=False)
    inori_action: Mapped[str] = mapped_column(Text, nullable=False)
    talk_text: Mapped[str] = mapped_column(Text, nullable=False)
    voice_list: Mapped[str] = mapped_column(Text, nullable=False)
    action_name: Mapped[str] = mapped_column(Text, primary_key=True)
    kaya_action: Mapped[str] = mapped_column(Text, nullable=False)
    talk_text_type: Mapped[int] = mapped_column(Integer, nullable=False)
    dragon_action: Mapped[str] = mapped_column(Text, nullable=False)


class SrtPanel(Base):
    __tablename__ = 'srt_panel'

    read_type: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_text: Mapped[str] = mapped_column(Text, nullable=False)
    head_symbol: Mapped[str] = mapped_column(Text, nullable=False)
    reading: Mapped[str] = mapped_column(Text, nullable=False)
    reading_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    panel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    tail_symbol: Mapped[str] = mapped_column(Text, nullable=False)


class SrtReward(Base):
    __tablename__ = 'srt_reward'

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    srt_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)


class SrtScore(Base):
    __tablename__ = 'srt_score'

    coefficient_count_priconne_panel: Mapped[int] = mapped_column(Integer, nullable=False)
    d4a09e8363d0ff21a0b3f0ef5cb776e61661830e07d3955dbab74625921ecd28: Mapped[int] = mapped_column(Integer, nullable=False)
    fd16c22680e2cf94556348bc2ee355256869848ce3201a84519bef2e981e9703: Mapped[int] = mapped_column(Integer, nullable=False)
    a9a0e46bcaa32bf035c2a94ee4d850bad0a8590aa67cfb910bb09453a12dd71a: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_read_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_read_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fe86f9c811978791dbe24be81070010223d31efe7a84b8a4f8f254f57d23ed5e: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_fever: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    ad3d1766c8d048e5b989201a27ca550c2045dfe4d3f59f84ca4e50e538d7abc5: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_read_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class SrtTopTalk(Base):
    __tablename__ = 'srt_top_talk'

    talk_text: Mapped[str] = mapped_column(Text, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, nullable=False)
    direction: Mapped[int] = mapped_column(Integer, nullable=False)
    talk_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)


class SspStoryDatum(Base):
    __tablename__ = 'ssp_story_data'

    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    contents_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Stamp(Base):
    __tablename__ = 'stamp'

    end_date: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    stamp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class StationaryMissionDatum(Base):
    __tablename__ = 'stationary_mission_data'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title_color_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_icon: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    stationary_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    condition_value_9: Mapped[Optional[int]] = mapped_column(Integer)
    system_id: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_8: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_1: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_4: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_3: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_10: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_2: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_5: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_6: Mapped[Optional[int]] = mapped_column(Integer)
    condition_value_7: Mapped[Optional[int]] = mapped_column(Integer)


class Still(Base):
    __tablename__ = 'still'

    unit_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    my_page_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    vertical_still_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    still_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    facial_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    album_ignore: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll_direction: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_9: Mapped[int] = mapped_column(Integer, nullable=False)


class StoryBulkSkip(Base):
    __tablename__ = 'story_bulk_skip'

    button_sprite_name: Mapped[str] = mapped_column(Text, nullable=False)
    release_level: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_id_from: Mapped[int] = mapped_column(Integer, nullable=False)
    bulk_skip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_sprite_name: Mapped[str] = mapped_column(Text, nullable=False)
    balloon_sprite_name: Mapped[str] = mapped_column(Text, nullable=False)


class StoryCharacterMask(Base):
    __tablename__ = 'story_character_mask'

    offset: Mapped[float] = mapped_column(REAL, nullable=False)
    softness: Mapped[float] = mapped_column(REAL, nullable=False)
    chara_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    size: Mapped[float] = mapped_column(REAL, nullable=False)


class StoryDatum(Base):
    __tablename__ = 'story_data'

    value: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_free_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    gojuon_order: Mapped[int] = mapped_column(Integer, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class StoryDetail(Base):
    __tablename__ = 'story_detail'

    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    read_process_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    force_unlock_time: Mapped[str] = mapped_column(Text, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    force_unlock_time_2: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class StoryQuestDatum(Base):
    __tablename__ = 'story_quest_data'

    guest_unit_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    guest_unit_4: Mapped[int] = mapped_column(Integer, nullable=False)
    _61b98b787e11b939a0bf73ed564935514437ce69328ee7a562af58fc6cf852a6: Mapped[int] = mapped_column('61b98b787e11b939a0bf73ed564935514437ce69328ee7a562af58fc6cf852a6', Integer, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_unit_5: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    guest_unit_1: Mapped[int] = mapped_column(Integer, nullable=False)
    _3c90aa9d959f5b1af70cc547813ea20f6b8bb693cc7ab0c837c2e459e49ea9c3: Mapped[int] = mapped_column('3c90aa9d959f5b1af70cc547813ea20f6b8bb693cc7ab0c837c2e459e49ea9c3', Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    _376881aebfd57804d0cd354cd93070449d4b38d019ad289bc41f7de87e2bf523: Mapped[int] = mapped_column('376881aebfd57804d0cd354cd93070449d4b38d019ad289bc41f7de87e2bf523', Integer, nullable=False)
    guest_unit_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)


class SvdDramaScript(Base):
    __tablename__ = 'svd_drama_script'

    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)


class SvdStoryDatum(Base):
    __tablename__ = 'svd_story_data'

    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class SvdStoryScript(Base):
    __tablename__ = 'svd_story_script'

    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)


class Talent(Base):
    __tablename__ = 'talent'

    talent_color: Mapped[str] = mapped_column(Text, nullable=False)
    talent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_name: Mapped[str] = mapped_column(Text, nullable=False)


class TalentFormationBonus(Base):
    __tablename__ = 'talent_formation_bonus'

    formation_bonus_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_bonus_5: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_1: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_2: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_3: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_bonus_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentFormationOverwrite(Base):
    __tablename__ = 'talent_formation_overwrite'

    formation_bonus_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    target_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[int] = mapped_column(Integer, nullable=False)
    formation_bonus_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentLevelMaterial(Base):
    __tablename__ = 'talent_level_material'

    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    point: Mapped[int] = mapped_column(Integer, nullable=False)
    idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestAreaDatum(Base):
    __tablename__ = 'talent_quest_area_data'

    area_name: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    area_display_name: Mapped[str] = mapped_column(Text, nullable=False)
    talent_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)


class TalentQuestBattleEffect(Base):
    __tablename__ = 'talent_quest_battle_effect'

    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)


class TalentQuestBattleQuestDatum(Base):
    __tablename__ = 'talent_quest_battle_quest_data'

    quest_battle_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    detail_enemy_local_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    area_map_boss_icon_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    detail_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    area_map_boss_icon_scale_y: Mapped[float] = mapped_column(REAL, nullable=False)
    area_map_boss_icon_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    area_map_boss_icon_scale_x: Mapped[float] = mapped_column(REAL, nullable=False)


class TalentQuestClearReward01(Base):
    __tablename__ = 'talent_quest_clear_reward01'

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward02(Base):
    __tablename__ = 'talent_quest_clear_reward02'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward03(Base):
    __tablename__ = 'talent_quest_clear_reward03'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TalentQuestClearReward04(Base):
    __tablename__ = 'talent_quest_clear_reward04'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestClearReward05(Base):
    __tablename__ = 'talent_quest_clear_reward05'

    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestConditionDatum(Base):
    __tablename__ = 'talent_quest_condition_data'

    release_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_talent_skill_page: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus01(Base):
    __tablename__ = 'talent_quest_daily_bonus01'

    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus02(Base):
    __tablename__ = 'talent_quest_daily_bonus02'

    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus03(Base):
    __tablename__ = 'talent_quest_daily_bonus03'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus04(Base):
    __tablename__ = 'talent_quest_daily_bonus04'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDailyBonus05(Base):
    __tablename__ = 'talent_quest_daily_bonus05'

    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestDatum(Base):
    __tablename__ = 'talent_quest_data'

    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_knight_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    love: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    drop_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_bonus_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestEnemyParameter(Base):
    __tablename__ = 'talent_quest_enemy_parameter'

    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    virtual_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    unique_equipment_flag_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    break_durability: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentQuestWaveGroupDatum(Base):
    __tablename__ = 'talent_quest_wave_group_data'

    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillEnhanceDatum(Base):
    __tablename__ = 'talent_skill_enhance_data'

    talent_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    parameter_type: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_value: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillEnhanceLevel(Base):
    __tablename__ = 'talent_skill_enhance_level'

    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillNode(Base):
    __tablename__ = 'talent_skill_node'

    enhance_level_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_2: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    page_num: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_4: Mapped[int] = mapped_column(Integer, nullable=False)
    title_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TalentSkillTitle(Base):
    __tablename__ = 'talent_skill_title'

    title_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_text: Mapped[str] = mapped_column(Text, nullable=False)


class TalentWeakness(Base):
    __tablename__ = 'talent_weakness'

    talent_3: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_5: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_1: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_2: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqCompletionRewards(Base):
    __tablename__ = 'taq_completion_rewards'

    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    completion_num: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqDatum(Base):
    __tablename__ = 'taq_data'

    detail: Mapped[str] = mapped_column(Text, nullable=False)
    input_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_2: Mapped[str] = mapped_column(Text, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[int] = mapped_column(Integer, nullable=False)
    word: Mapped[str] = mapped_column(Text, nullable=False)
    input_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    taq_type: Mapped[int] = mapped_column(Integer, nullable=False)
    assist_detail: Mapped[str] = mapped_column(Text, nullable=False)
    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    char_no_2: Mapped[int] = mapped_column(Integer, nullable=False)
    char_no_1: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    char_no_3: Mapped[int] = mapped_column(Integer, nullable=False)
    char_no_5: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    char_no_4: Mapped[int] = mapped_column(Integer, nullable=False)
    input_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk: Mapped[str] = mapped_column(Text, nullable=False)


class TaqDramaScript(Base):
    __tablename__ = 'taq_drama_script'

    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class TaqGameSetting(Base):
    __tablename__ = 'taq_game_setting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    help_use_count_hard: Mapped[int] = mapped_column(Integer, nullable=False)
    lottery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    help_use_count_veryhard: Mapped[int] = mapped_column(Integer, nullable=False)
    help_use_count_normal: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqGenre(Base):
    __tablename__ = 'taq_genre'

    genre_name: Mapped[str] = mapped_column(Text, nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TaqGoodUnit(Base):
    __tablename__ = 'taq_good_unit'

    unit_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_5: Mapped[int] = mapped_column(Integer, nullable=False)


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

    unnecessary_word_2: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_1: Mapped[str] = mapped_column(Text, nullable=False)
    taq_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    necessary_word_4: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_5: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_5: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_2: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_3: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_3: Mapped[str] = mapped_column(Text, nullable=False)
    necessary_word_1: Mapped[str] = mapped_column(Text, nullable=False)
    unnecessary_word_4: Mapped[str] = mapped_column(Text, nullable=False)


class TaqRewards(Base):
    __tablename__ = 'taq_rewards'

    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TaqUnit(Base):
    __tablename__ = 'taq_unit'

    genre_status_1: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_2: Mapped[int] = mapped_column(Integer, nullable=False)
    personality_id: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_4: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_5: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_status_6: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TdfBattleEffect(Base):
    __tablename__ = 'tdf_battle_effect'

    effect_name: Mapped[str] = mapped_column(Text, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TdfDifficultyIconDatum(Base):
    __tablename__ = 'tdf_difficulty_icon_data'

    difficulty: Mapped[int] = mapped_column(Integer, primary_key=True)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_name: Mapped[str] = mapped_column(Text, nullable=False)


class TdfPhaseDatum(Base):
    __tablename__ = 'tdf_phase_data'

    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    phase_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    need_clear_num: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfQuestDatum(Base):
    __tablename__ = 'tdf_quest_data'

    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfSchedule(Base):
    __tablename__ = 'tdf_schedule'

    recovery_disable_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    ex_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TdfTopOffset(Base):
    __tablename__ = 'tdf_top_offset'

    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)


class TdfWaveGroupDatum(Base):
    __tablename__ = 'tdf_wave_group_data'

    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TeamSkillEnhanceDatum(Base):
    __tablename__ = 'team_skill_enhance_data'

    parameter_type: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_value: Mapped[int] = mapped_column(Integer, nullable=False)
    talent_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TeamSkillEnhanceLevel(Base):
    __tablename__ = 'team_skill_enhance_level'

    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)


class TeamSkillNode(Base):
    __tablename__ = 'team_skill_node'

    title_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    noise_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    node_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_node_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)


class TeamSkillTitle(Base):
    __tablename__ = 'team_skill_title'

    title_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_text: Mapped[str] = mapped_column(Text, nullable=False)


class ThumbnailHideCondition(Base):
    __tablename__ = 'thumbnail_hide_condition'

    hide_story_id_from: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_hide_title: Mapped[int] = mapped_column(Integer, nullable=False)
    hide_story_id_to: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TicketGachaDatum(Base):
    __tablename__ = 'ticket_gacha_data'

    gacha_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_times: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_type: Mapped[int] = mapped_column(Integer, nullable=False)
    _32f23ec641b2cbffb667f3cf9236779f3b0a3ca9adc37750879710f26144be75: Mapped[str] = mapped_column('32f23ec641b2cbffb667f3cf9236779f3b0a3ca9adc37750879710f26144be75', Text, nullable=False)
    staging_type: Mapped[int] = mapped_column(Integer, nullable=False)
    _64221fab7752f88b9ec07fa3f25d30d3474a447c120dcffa35e75532746db3be: Mapped[str] = mapped_column('64221fab7752f88b9ec07fa3f25d30d3474a447c120dcffa35e75532746db3be', Text, nullable=False)
    da0f5a9ef7d12bc6d6f3d7da9a43e531e4b345cad3cf623ec3a6d834ea1fde1f: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_name: Mapped[str] = mapped_column(Text, nullable=False)
    b7f4cf9576addb197140be17750cce76791b4563adb1393fa6ffe502a1517ab9: Mapped[str] = mapped_column(Text, nullable=False)
    gacha_detail: Mapped[int] = mapped_column(Integer, nullable=False)
    _62890f3ff99e376340eb60e8e093abbd31b7595496e7d84d06ca6f74e533381c: Mapped[str] = mapped_column('62890f3ff99e376340eb60e8e093abbd31b7595496e7d84d06ca6f74e533381c', Text, nullable=False)


class Tips(Base):
    __tablename__ = 'tips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tips_index: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class TmeMapDatum(Base):
    __tablename__ = 'tme_map_data'

    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tap_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_effect: Mapped[int] = mapped_column(Integer, nullable=False)
    tme_object_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_difficulty_type: Mapped[int] = mapped_column(Integer, nullable=False)


class TopicTalkChara(Base):
    __tablename__ = 'topic_talk_chara'

    name_effect_color: Mapped[str] = mapped_column(Text, nullable=False)
    chara_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    chara_name: Mapped[str] = mapped_column(Text, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_icon_color: Mapped[str] = mapped_column(Text, nullable=False)
    reference_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TopicTalkDrama(Base):
    __tablename__ = 'topic_talk_drama'

    lottery_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    knight_skin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TopicTalkDramaScript(Base):
    __tablename__ = 'topic_talk_drama_script'

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class TopicTalkMission(Base):
    __tablename__ = 'topic_talk_mission'

    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class TopicTalkSetting(Base):
    __tablename__ = 'topic_talk_setting'

    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_bonus_ticket_count: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    daily_free_count: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_boss_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_cue_sheet: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TopicTalkStory(Base):
    __tablename__ = 'topic_talk_story'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_point: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    read_condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_point_2: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_point_3: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    relation_topic_point_1: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class TopicTalkTopicDatum(Base):
    __tablename__ = 'topic_talk_topic_data'

    topic_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_type: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_name: Mapped[str] = mapped_column(Text, nullable=False)


class TowerAreaDatum(Base):
    __tablename__ = 'tower_area_data'

    area_bg: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    tower_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cloister_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    max_floor_num: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerCloisterQuestDatum(Base):
    __tablename__ = 'tower_cloister_quest_data'

    w1_enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    start_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_cloister_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    w1_enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    w3_enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    w2_enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    w1_enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    w1_enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    w3_enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    w2_enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerEnemyParameter(Base):
    __tablename__ = 'tower_enemy_parameter'

    main_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_6: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_9: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_10: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_color: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resist_variation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_7: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_1: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_level: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    resist_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_3: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_5: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_2: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_lv_8: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_lv_4: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerExQuestDatum(Base):
    __tablename__ = 'tower_ex_quest_data'

    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    tower_ex_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_level: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    ee0e308bf4166d85be0f278b75089be71cfab1defe4f12588efec7a2207d2bf4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clp_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerQuestDatum(Base):
    __tablename__ = 'tower_quest_data'

    start_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_hp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_5: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_image_add_type: Mapped[int] = mapped_column(Integer, nullable=False)
    chest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_4: Mapped[int] = mapped_column(Integer, nullable=False)
    clp_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm: Mapped[str] = mapped_column(Text, nullable=False)
    tower_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_image_type: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_num: Mapped[int] = mapped_column(Integer, nullable=False)
    boss_floor_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_5: Mapped[float] = mapped_column(REAL, nullable=False)
    additional_reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_5: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_tp_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_4: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_2: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_size_1: Mapped[float] = mapped_column(REAL, nullable=False)
    enemy_position_x_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_local_position_y_3: Mapped[int] = mapped_column(Integer, nullable=False)
    tower_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_size_3: Mapped[float] = mapped_column(REAL, nullable=False)
    skip_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_position_x_4: Mapped[int] = mapped_column(Integer, nullable=False)
    open_tower_ex_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    b08501834ba2876178bc5055ad97f3a9df3e5c6f358047a7a7acc4a178a5aeea: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerQuestFixRewardGroup(Base):
    __tablename__ = 'tower_quest_fix_reward_group'

    reward_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    fix_reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    treasure_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_6: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerQuestOddsGroup(Base):
    __tablename__ = 'tower_quest_odds_group'

    treasure_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    _07a359833b3254f3c3b5d66f81d7bf6aae22189a18a3efabdc60747ea3c4f661: Mapped[str] = mapped_column('07a359833b3254f3c3b5d66f81d7bf6aae22189a18a3efabdc60747ea3c4f661', Text, nullable=False)
    _191e3e1b3b1b979211f6f5b8f2704ca76e488f30a1fa57013c217682c748a3e9: Mapped[str] = mapped_column('191e3e1b3b1b979211f6f5b8f2704ca76e488f30a1fa57013c217682c748a3e9', Text, nullable=False)
    _346a84b7b9b62a9b056c84d6e2b71d5d0f8fb3cbc8b4d0c86fc01cc36753660a: Mapped[str] = mapped_column('346a84b7b9b62a9b056c84d6e2b71d5d0f8fb3cbc8b4d0c86fc01cc36753660a', Text, nullable=False)
    treasure_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    aa7e3309ce01fd461069f3875f51485b9561bfce4237efa337d11eb391e49a4e: Mapped[str] = mapped_column(Text, nullable=False)
    _64ef74bad9b83e91ee582f60f51028e155a05c9a863c9b191985e775f84f0075: Mapped[str] = mapped_column('64ef74bad9b83e91ee582f60f51028e155a05c9a863c9b191985e775f84f0075', Text, nullable=False)
    treasure_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    c58ed77864dde32c3fea9f24e2374041622c807943f991788a436c8610aef81d: Mapped[str] = mapped_column(Text, nullable=False)
    odds_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _42a1753697321e385a90eabc48eec90be0943bab79352620e87b06f002c00af2: Mapped[str] = mapped_column('42a1753697321e385a90eabc48eec90be0943bab79352620e87b06f002c00af2', Text, nullable=False)
    treasure_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    _9a98d56728c311220aa297c09b06c241065f05ff1c3384d67bdb4239c7a2eaa7: Mapped[str] = mapped_column('9a98d56728c311220aa297c09b06c241065f05ff1c3384d67bdb4239c7a2eaa7', Text, nullable=False)
    treasure_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    _655d7b4c1126e7d0ac4d5c651ab6afb00c411337fe158c6fb46b67f1ab55e9a3: Mapped[str] = mapped_column('655d7b4c1126e7d0ac4d5c651ab6afb00c411337fe158c6fb46b67f1ab55e9a3', Text, nullable=False)
    treasure_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    treasure_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_from: Mapped[int] = mapped_column(Integer, primary_key=True)
    _18cc7be68e7c19a7fff27d6bcaca96f87aa75cb5c8681a233c14a084306e3fd1: Mapped[str] = mapped_column('18cc7be68e7c19a7fff27d6bcaca96f87aa75cb5c8681a233c14a084306e3fd1', Text, nullable=False)
    treasure_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    team_level_to: Mapped[int] = mapped_column(Integer, primary_key=True)


class TowerSchedule(Base):
    __tablename__ = 'tower_schedule'

    max_tower_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recovery_disable_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    count_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    opening_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    tower_schedule_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TowerStoryDatum(Base):
    __tablename__ = 'tower_story_data'

    story_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerStoryDetail(Base):
    __tablename__ = 'tower_story_detail'

    reward_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    story_end: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    visible_type: Mapped[int] = mapped_column(Integer, nullable=False)
    story_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requirement_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lock_all_text: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    love_level: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    story_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    can_bookmark: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_value_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TowerWaveGroupDatum(Base):
    __tablename__ = 'tower_wave_group_data'

    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TpRecoveryAt(Base):
    __tablename__ = 'tp_recovery_at'

    correction_value: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    limit_value: Mapped[int] = mapped_column(Integer, nullable=False)


class TprPanelDatum(Base):
    __tablename__ = 'tpr_panel_data'

    another_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    another_parts_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_parts_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    panel_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TprStoryDatum(Base):
    __tablename__ = 'tpr_story_data'

    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_panel_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TrainingQuestDatum(Base):
    __tablename__ = 'training_quest_data'

    team_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    background_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_quest_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    wave_bgm_que_id_3: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id_1: Mapped[str] = mapped_column(Text, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_team_level: Mapped[int] = mapped_column(Integer, nullable=False)
    rank_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_3: Mapped[int] = mapped_column(Integer, nullable=False)
    training_quest_detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_4: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id_2: Mapped[str] = mapped_column(Text, nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    background_2: Mapped[int] = mapped_column(Integer, nullable=False)
    training_quest_detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    background_1: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_image_5: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    enemy_image_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_image_2: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wave_group_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_start: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelAreaDatum(Base):
    __tablename__ = 'travel_area_data'

    _0c018c1fb2ab31196e9e6ad7d43a10daf85e41ebee942c1debb9eb9e6ef36e6d: Mapped[int] = mapped_column('0c018c1fb2ab31196e9e6ad7d43a10daf85e41ebee942c1debb9eb9e6ef36e6d', Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    top_icon_y: Mapped[int] = mapped_column(Integer, nullable=False)
    top_icon_x: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_area_name: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    travel_area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    top_icon_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelDecreaseTimeCost(Base):
    __tablename__ = 'travel_decrease_time_cost'

    count: Mapped[int] = mapped_column(Integer, primary_key=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelDramaExceptUnit(Base):
    __tablename__ = 'travel_drama_except_unit'

    type: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelExEventDatum(Base):
    __tablename__ = 'travel_ex_event_data'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    still_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelExEventDrama(Base):
    __tablename__ = 'travel_ex_event_drama'

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)


class TravelQuestDatum(Base):
    __tablename__ = 'travel_quest_data'

    main_reward_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_1: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_unit_num: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_3: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_time_decrease_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_y: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    main_reward_5: Mapped[int] = mapped_column(Integer, nullable=False)
    situation_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_time: Mapped[int] = mapped_column(Integer, nullable=False)
    need_power: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_decrease_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_reward_2: Mapped[int] = mapped_column(Integer, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    icon_x: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelQuestResult(Base):
    __tablename__ = 'travel_quest_result'

    except_unit_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    situation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelQuestResultGroup(Base):
    __tablename__ = 'travel_quest_result_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    situation_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    situation_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelQuestSubReward(Base):
    __tablename__ = 'travel_quest_sub_reward'

    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelResultExceptUnitGroup(Base):
    __tablename__ = 'travel_result_except_unit_group'

    except_unit_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    except_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelRoundEventDatum(Base):
    __tablename__ = 'travel_round_event_data'

    round_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transition_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    round: Mapped[int] = mapped_column(Integer, primary_key=True)
    main_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    right_door_pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_treasure_box_type: Mapped[int] = mapped_column(Integer, nullable=False)
    event_icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    left_door_pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelRoundEventDrama(Base):
    __tablename__ = 'travel_round_event_drama'

    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelStartDrama(Base):
    __tablename__ = 'travel_start_drama'

    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TravelTopEventDatum(Base):
    __tablename__ = 'travel_top_event_data'

    top_icon_type: Mapped[int] = mapped_column(Integer, nullable=False)
    top_event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_type: Mapped[int] = mapped_column(Integer, nullable=False)
    _93eb751ea051ddf608062b1e50a13d4b1bd4ccf8925beecdae1bbefe046de1bf: Mapped[int] = mapped_column('93eb751ea051ddf608062b1e50a13d4b1bd4ccf8925beecdae1bbefe046de1bf', Integer, nullable=False)
    zoom_offset_y: Mapped[int] = mapped_column(Integer, nullable=False)
    branch_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pattern: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    branch_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    zoom_offset_x: Mapped[int] = mapped_column(Integer, nullable=False)
    _56f3372436654cd9acefae2c806258fc500107054a6a3b33b2f36c25e5be6531: Mapped[int] = mapped_column('56f3372436654cd9acefae2c806258fc500107054a6a3b33b2f36c25e5be6531', Integer, nullable=False)
    branch_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    branch_id_4: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelTopEventDrama(Base):
    __tablename__ = 'travel_top_event_drama'

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)


class TravelTopEventPosDetail(Base):
    __tablename__ = 'travel_top_event_pos_detail'

    _1db0150b591e95b50da3e8c95697ee55634ae7d77be7f6f3ab0584d1dfad00f2: Mapped[int] = mapped_column('1db0150b591e95b50da3e8c95697ee55634ae7d77be7f6f3ab0584d1dfad00f2', Integer, nullable=False)
    pos_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _37b700d359d8ecc98b09fa6fbcd8536d65a6168e9460b84b2272f30b1fb27f5a: Mapped[int] = mapped_column('37b700d359d8ecc98b09fa6fbcd8536d65a6168e9460b84b2272f30b1fb27f5a', Integer, nullable=False)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleCategory(Base):
    __tablename__ = 'trial_battle_category'

    description: Mapped[str] = mapped_column(Text, nullable=False)
    description_detail: Mapped[str] = mapped_column(Text, nullable=False)
    icon_id: Mapped[int] = mapped_column(Integer, nullable=False)
    label_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    label_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    label_type_3: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleDatum(Base):
    __tablename__ = 'trial_battle_data'

    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    detail_boss_bg_size: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    battle_name: Mapped[str] = mapped_column(Text, nullable=False)
    detail_boss_bg_height: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    clear_reward_group: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleMissionDatum(Base):
    __tablename__ = 'trial_battle_mission_data'

    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_group: Mapped[int] = mapped_column(Integer, nullable=False)
    trial_mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleMissionReward(Base):
    __tablename__ = 'trial_battle_mission_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleRewardDatum(Base):
    __tablename__ = 'trial_battle_reward_data'

    reward_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)


class TrialBattleTalentWeakness(Base):
    __tablename__ = 'trial_battle_talent_weakness'

    wave_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    talent_weakness: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkDrama(Base):
    __tablename__ = 'ttk_drama'

    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)


class TtkEnemy(Base):
    __tablename__ = 'ttk_enemy'

    enemy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    max: Mapped[int] = mapped_column(Integer, nullable=False)
    coin: Mapped[int] = mapped_column(Integer, nullable=False)


class TtkNaviComment(Base):
    __tablename__ = 'ttk_navi_comment'

    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    character_name: Mapped[str] = mapped_column(Text, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class TtkReward(Base):
    __tablename__ = 'ttk_reward'

    reward_count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ttk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_detail: Mapped[str] = mapped_column(Text, nullable=False)


class TtkScore(Base):
    __tablename__ = 'ttk_score'

    coefficient_coin_score: Mapped[int] = mapped_column(Integer, nullable=False)
    life: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    coefficient_wrong_num: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class TtkStory(Base):
    __tablename__ = 'ttk_story'

    ttk_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ttk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class TtkStoryScript(Base):
    __tablename__ = 'ttk_story_script'

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)


class TtkWeapon(Base):
    __tablename__ = 'ttk_weapon'

    ttk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    ttk_weapon_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class UbAutoDatum(Base):
    __tablename__ = 'ub_auto_data'

    auto_detail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_auto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auto_detail_5: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_detail_4: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_type: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_detail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_value_2: Mapped[int] = mapped_column(Integer, nullable=False)


class UbAutoDefine(Base):
    __tablename__ = 'ub_auto_define'

    ub_auto_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_auto_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_auto_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_auto_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ub_auto_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UekBoss(Base):
    __tablename__ = 'uek_boss'

    enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[int] = mapped_column(Integer, primary_key=True)
    result_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    result_boss_position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_que_id: Mapped[str] = mapped_column(Text, nullable=False)
    detail_boss_bg_size: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_position: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    background: Mapped[int] = mapped_column(Integer, nullable=False)
    detail_boss_bg_height: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_time: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    quest_name: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    bgm_sheet_id: Mapped[str] = mapped_column(Text, nullable=False)


class UekDrama(Base):
    __tablename__ = 'uek_drama'

    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)


class UekMission(Base):
    __tablename__ = 'uek_mission'

    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    mission_condition: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_value_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_num: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class UekSpineAnimLink(Base):
    __tablename__ = 'uek_spine_anim_link'

    spine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    anim_num: Mapped[int] = mapped_column(Integer, nullable=False)


class UniqueEquipConsumeGroup(Base):
    __tablename__ = 'unique_equip_consume_group'

    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    index_in_group: Mapped[int] = mapped_column(Integer, primary_key=True)


class UniqueEquipCraftEnhance(Base):
    __tablename__ = 'unique_equip_craft_enhance'

    consume_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UniqueEquipEnhanceRate(Base):
    __tablename__ = 'unique_equip_enhance_rate'

    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    min_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    max_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentBonus(Base):
    __tablename__ = 'unique_equipment_bonus'

    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    max_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    min_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentCraft(Base):
    __tablename__ = 'unique_equipment_craft'

    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    crafted_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_8: Mapped[int] = mapped_column(Integer, nullable=False)


class UniqueEquipmentDatum(Base):
    __tablename__ = 'unique_equipment_data'

    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    sale_price: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_enhance_point: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    craft_flg: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    require_level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_name: Mapped[str] = mapped_column(Text, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    enable_donation: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)


class UniqueEquipmentEnhanceDatum(Base):
    __tablename__ = 'unique_equipment_enhance_data'

    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_point: Mapped[int] = mapped_column(Integer, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    needed_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    needed_point: Mapped[int] = mapped_column(Integer, nullable=False)
    enhance_level: Mapped[int] = mapped_column(Integer, primary_key=True)


class UniqueEquipmentEnhanceRate(Base):
    __tablename__ = 'unique_equipment_enhance_rate'

    cbaa120c3843d24c161dbfa4e7b2e4d774b6c99613f069db4431bb81b1d5e6de: Mapped[str] = mapped_column(Text, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    _0573b6dce7ac7f437720695f81b88ee94008cd457834c58fcc1b803e29b39afc: Mapped[int] = mapped_column('0573b6dce7ac7f437720695f81b88ee94008cd457834c58fcc1b803e29b39afc', Integer, nullable=False)
    da55285c5d44cff9b2793ec6c88cd29c2c366d47c30dc4ba7c786960e67c695e: Mapped[str] = mapped_column(Text, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    equipment_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UniqueEquipmentRankup(Base):
    __tablename__ = 'unique_equipment_rankup'

    consume_num_9: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_8: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_10: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unique_equip_rank: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id_9: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_7: Mapped[int] = mapped_column(Integer, nullable=False)
    crafted_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_2: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_1: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_8: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_6: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_9: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_8: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_7: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id_7: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_3: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_num_6: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitAttackPattern(Base):
    __tablename__ = 'unit_attack_pattern'

    atk_pattern_18: Mapped[int] = mapped_column(Integer, nullable=False)
    loop_start: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_5: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_17: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_10: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_3: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_20: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_14: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_2: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_13: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_4: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_15: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_1: Mapped[int] = mapped_column(Integer, nullable=False)
    pattern_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atk_pattern_12: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_9: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_7: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    loop_end: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_8: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_19: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_11: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_16: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_pattern_6: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitBackground(Base):
    __tablename__ = 'unit_background'

    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[float] = mapped_column(REAL, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)


class UnitClipSetting(Base):
    __tablename__ = 'unit_clip_setting'

    clip_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    center_x: Mapped[int] = mapped_column(Integer, nullable=False)
    softness_x: Mapped[int] = mapped_column(Integer, nullable=False)
    size_x: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitComments(Base):
    __tablename__ = 'unit_comments'

    change_time: Mapped[float] = mapped_column(REAL, nullable=False)
    face_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_time_3: Mapped[float] = mapped_column(REAL, nullable=False)
    all_comments_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    use_type: Mapped[int] = mapped_column(Integer, nullable=False)
    face_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    change_face_3: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_time_2: Mapped[float] = mapped_column(REAL, nullable=False)
    face_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_2: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitConversion(Base):
    __tablename__ = 'unit_conversion'

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitDatum(Base):
    __tablename__ = 'unit_data'

    motion_type: Mapped[int] = mapped_column(Integer, nullable=False)
    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin2_star6: Mapped[int] = mapped_column(Integer, nullable=False)
    kana: Mapped[str] = mapped_column(Text, nullable=False)
    move_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    normal_atk_cast_time: Mapped[float] = mapped_column(REAL, nullable=False)
    only_disp_owned: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    se_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin1_star6: Mapped[int] = mapped_column(Integer, nullable=False)
    exskill_display: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    guild_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_limited: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cutin_1: Mapped[int] = mapped_column(Integer, nullable=False)
    search_area_width: Mapped[int] = mapped_column(Integer, nullable=False)
    prefab_id_battle: Mapped[int] = mapped_column(Integer, nullable=False)
    original_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitEnemyDatum(Base):
    __tablename__ = 'unit_enemy_data'

    motion_type: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin: Mapped[int] = mapped_column(Integer, nullable=False)
    cutin_star6: Mapped[int] = mapped_column(Integer, nullable=False)
    move_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    search_area_width: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    se_type: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_type: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    normal_atk_cast_time: Mapped[float] = mapped_column(REAL, nullable=False)
    visual_change_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    prefab_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)


class UnitExEquipmentSlot(Base):
    __tablename__ = 'unit_ex_equipment_slot'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_category_2: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_category_3: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_category_1: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitIntroduction(Base):
    __tablename__ = 'unit_introduction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    maximum_chunk_size_loop_3: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_2: Mapped[int] = mapped_column(Integer, nullable=False)
    introduction_number: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_loop_1: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    maximum_chunk_size_loop_2: Mapped[int] = mapped_column(Integer, nullable=False)
    gacha_id: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_1: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_chunk_size_3: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)


class UnitMotionList(Base):
    __tablename__ = 'unit_motion_list'

    sp_motion: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnitMypagePos(Base):
    __tablename__ = 'unit_mypage_pos'

    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scale: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitPosAdjustment(Base):
    __tablename__ = 'unit_pos_adjustment'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    is_myprofile_image: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    profile_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    skip_position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_id3: Mapped[int] = mapped_column(Integer, nullable=False)
    id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    friend_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    home_1_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    home_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_id1: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    home_1_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_3_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_1_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    home_3_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_scale: Mapped[float] = mapped_column(REAL, nullable=False)
    profile_2_depth: Mapped[int] = mapped_column(Integer, nullable=False)
    home_2_clip: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_2_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_2_pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    home_1_pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_id2: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitProfile(Base):
    __tablename__ = 'unit_profile'

    birth_month: Mapped[str] = mapped_column(Text, nullable=False)
    guild_id: Mapped[str] = mapped_column(Text, nullable=False)
    blood_type: Mapped[str] = mapped_column(Text, nullable=False)
    birth_day: Mapped[str] = mapped_column(Text, nullable=False)
    catch_copy: Mapped[str] = mapped_column(Text, nullable=False)
    height: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    age: Mapped[str] = mapped_column(Text, nullable=False)
    self_text: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    voice: Mapped[str] = mapped_column(Text, nullable=False)
    guild: Mapped[str] = mapped_column(Text, nullable=False)
    favorite: Mapped[str] = mapped_column(Text, nullable=False)
    race: Mapped[str] = mapped_column(Text, nullable=False)


class UnitPromotion(Base):
    __tablename__ = 'unit_promotion'

    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot_5: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_2: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_6: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_1: Mapped[int] = mapped_column(Integer, nullable=False)
    equip_slot_4: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot_3: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitPromotionStatus(Base):
    __tablename__ = 'unit_promotion_status'

    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    promotion_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitRarity(Base):
    __tablename__ = 'unit_rarity'

    accuracy_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    def_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    atk: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_material_id: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    dodge: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate: Mapped[float] = mapped_column(REAL, nullable=False)
    consume_num: Mapped[int] = mapped_column(Integer, nullable=False)
    atk_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_critical_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    hp: Mapped[float] = mapped_column(REAL, nullable=False)
    rarity: Mapped[int] = mapped_column(Integer, primary_key=True)
    life_steal: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_penetrate: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical_growth: Mapped[float] = mapped_column(REAL, nullable=False)
    def_: Mapped[float] = mapped_column('def', REAL, nullable=False)
    accuracy: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_str_growth: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitSkillDatum(Base):
    __tablename__ = 'unit_skill_data'

    main_skill_10: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ex_skill_evolution_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_9: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_4: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_3: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_2: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_5: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_4: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_evolution_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_7: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_evolution_1: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_8: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_6: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_union_burst: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_evolution_2: Mapped[int] = mapped_column(Integer, nullable=False)
    union_burst_evolution: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_2: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_3: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_1: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_5: Mapped[int] = mapped_column(Integer, nullable=False)
    main_skill_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_1: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_evolution_2: Mapped[int] = mapped_column(Integer, nullable=False)
    ex_skill_evolution_5: Mapped[int] = mapped_column(Integer, nullable=False)
    sp_skill_4: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitSkillDataRf(Base):
    __tablename__ = 'unit_skill_data_rf'

    rf_skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    max_lv: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, nullable=False)
    min_lv: Mapped[int] = mapped_column(Integer, nullable=False)


class UnitStatusCoefficient(Base):
    __tablename__ = 'unit_status_coefficient'

    dodge_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_def_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    accuracy_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    physical_critical_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_hp_recovery_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    wave_energy_recovery_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill2_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    exskill_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    def_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    coefficient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    magic_critical_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_recovery_rate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    hp_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_reduce_rate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    overall_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    ub_evolution_slv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill1_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_penetrate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    ub_evolution_coefficient: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_str_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    magic_penetrate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill2_evolution_slv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    atk_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    life_steal_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    energy_recovery_rate_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill1_evolution_slv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)
    skill_lv_coefficient: Mapped[float] = mapped_column(REAL, nullable=False)


class UnitTalent(Base):
    __tablename__ = 'unit_talent'

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

    equip_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equip_slot: Mapped[int] = mapped_column(Integer, primary_key=True)


class UnlockRarity6(Base):
    __tablename__ = 'unlock_rarity_6'

    wave_hp_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    consume_gold: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_energy_recovery: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_reduce_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_recovery_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_count: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_level: Mapped[int] = mapped_column(Integer, primary_key=True)
    physical_penetrate: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    material_type: Mapped[int] = mapped_column(Integer, nullable=False)
    magic_def: Mapped[int] = mapped_column(Integer, nullable=False)
    def_: Mapped[int] = mapped_column('def', Integer, nullable=False)
    magic_str: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_critical: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    life_steal: Mapped[int] = mapped_column(Integer, nullable=False)
    dodge: Mapped[int] = mapped_column(Integer, nullable=False)
    atk: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)


class UnlockSkillDatum(Base):
    __tablename__ = 'unlock_skill_data'

    unlock_skill: Mapped[int] = mapped_column(Integer, primary_key=True)
    promotion_level: Mapped[int] = mapped_column(Integer, nullable=False)


class UnlockUnitCondition(Base):
    __tablename__ = 'unlock_unit_condition'

    condition_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_name: Mapped[str] = mapped_column(Text, nullable=False)
    count_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_2: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_4: Mapped[int] = mapped_column(Integer, nullable=False)
    count_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
    count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pre_unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    release_effect_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_4: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_5: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_type_detail_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class VisualCustomize(Base):
    __tablename__ = 'visual_customize'

    story_top_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    profile_logo: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    watched_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    quest_top_movie: Mapped[int] = mapped_column(Integer, nullable=False)
    title_prefab: Mapped[int] = mapped_column(Integer, nullable=False)
    title_voice: Mapped[int] = mapped_column(Integer, nullable=False)


class VoiceGroup(Base):
    __tablename__ = 'voice_group'

    group_unit_id_01: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_02: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_04: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id_comment: Mapped[str] = mapped_column(Text, nullable=False)
    group_unit_id_05: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_03: Mapped[int] = mapped_column(Integer, nullable=False)


class VoiceGroupChara(Base):
    __tablename__ = 'voice_group_chara'

    unit_id_06: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_07: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_05: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_01: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_02: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id_08: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_03: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_10: Mapped[int] = mapped_column(Integer, nullable=False)
    group_unit_id_comment: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_09: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_04: Mapped[int] = mapped_column(Integer, nullable=False)


class VoteDatum(Base):
    __tablename__ = 'vote_data'

    result_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    vote_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    result_start_time: Mapped[str] = mapped_column(Text, nullable=False)
    result_end_time: Mapped[str] = mapped_column(Text, nullable=False)
    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_end_time: Mapped[str] = mapped_column(Text, nullable=False)


class VoteInfo(Base):
    __tablename__ = 'vote_info'

    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_help: Mapped[str] = mapped_column(Text, nullable=False)
    vote_title: Mapped[str] = mapped_column(Text, nullable=False)
    vote_help_index: Mapped[int] = mapped_column(Integer, primary_key=True)


class VoteUnit(Base):
    __tablename__ = 'vote_unit'

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vote_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_rarity: Mapped[int] = mapped_column(Integer, nullable=False)


class WacBirthdayDramaScript(Base):
    __tablename__ = 'wac_birthday_drama_script'

    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class WacDatum(Base):
    __tablename__ = 'wac_data'

    post_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    idle_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    birthday_login_bonus_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mural_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_search_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unlock_time: Mapped[str] = mapped_column(Text, nullable=False)
    unit_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    pre_drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    effect_id: Mapped[int] = mapped_column(Integer, nullable=False)
    mural_offset_x: Mapped[float] = mapped_column(REAL, nullable=False)
    draw_end_to_center: Mapped[int] = mapped_column(Integer, nullable=False)


class WacDramaScript(Base):
    __tablename__ = 'wac_drama_script'

    param_06: Mapped[str] = mapped_column(Text, nullable=False)
    drama_id: Mapped[int] = mapped_column(Integer, nullable=False)
    param_05: Mapped[str] = mapped_column(Text, nullable=False)
    param_03: Mapped[str] = mapped_column(Text, nullable=False)
    command_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    param_01: Mapped[str] = mapped_column(Text, nullable=False)
    param_04: Mapped[str] = mapped_column(Text, nullable=False)
    param_08: Mapped[str] = mapped_column(Text, nullable=False)
    param_02: Mapped[str] = mapped_column(Text, nullable=False)
    command_type: Mapped[int] = mapped_column(Integer, nullable=False)
    param_07: Mapped[str] = mapped_column(Text, nullable=False)


class WacMuralBgDatum(Base):
    __tablename__ = 'wac_mural_bg_data'

    end_offset_x: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_offset_x: Mapped[str] = mapped_column(Text, nullable=False)
    bg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WacMuralDatum(Base):
    __tablename__ = 'wac_mural_data'

    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mural_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_x: Mapped[int] = mapped_column(Integer, nullable=False)
    parts_id: Mapped[int] = mapped_column(Integer, nullable=False)
    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_y: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)


class WacPresentStillDatum(Base):
    __tablename__ = 'wac_present_still_data'

    date_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    still_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wac_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WacUnitSearchDatum(Base):
    __tablename__ = 'wac_unit_search_data'

    unit_search_id: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)


class WaveGroupDatum(Base):
    __tablename__ = 'wave_group_data'

    enemy_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_2: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_5: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_lane: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    guest_enemy_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wave_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    odds: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enemy_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_gold_3: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_4: Mapped[int] = mapped_column(Integer, nullable=False)
    drop_reward_id_5: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_id_3: Mapped[int] = mapped_column(Integer, nullable=False)


class WonStoryDatum(Base):
    __tablename__ = 'won_story_data'

    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_last: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    note_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class WonStoryScript(Base):
    __tablename__ = 'won_story_script'

    type: Mapped[int] = mapped_column(Integer, nullable=False)
    command_param: Mapped[float] = mapped_column(REAL, nullable=False)
    cue_name: Mapped[str] = mapped_column(Text, nullable=False)
    sheet_name: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    seq_num: Mapped[int] = mapped_column(Integer, nullable=False)
    seek_time: Mapped[float] = mapped_column(REAL, nullable=False)
    end_pos: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    command: Mapped[int] = mapped_column(Integer, nullable=False)
    line_num: Mapped[int] = mapped_column(Integer, nullable=False)


class Worldmap(Base):
    __tablename__ = 'worldmap'

    sheet_id: Mapped[str] = mapped_column(Text, nullable=False)
    view_mode: Mapped[int] = mapped_column(Integer, nullable=False)
    map_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_area_id: Mapped[int] = mapped_column(Integer, nullable=False)
    map_type: Mapped[int] = mapped_column(Integer, nullable=False)
    que_id: Mapped[str] = mapped_column(Text, nullable=False)
    tutorial_adv_id: Mapped[int] = mapped_column(Integer, nullable=False)


class WtmStoryDatum(Base):
    __tablename__ = 'wtm_story_data'

    emblem_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    wtm_story_type: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_sub_story_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_sub_story_id_2: Mapped[int] = mapped_column(Integer, nullable=False)


class WtsNaviComment(Base):
    __tablename__ = 'wts_navi_comment'

    character_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    where_type: Mapped[int] = mapped_column(Integer, nullable=False)
    face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    change_face_time: Mapped[float] = mapped_column(REAL, nullable=False)
    pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change_face_type: Mapped[int] = mapped_column(Integer, nullable=False)
    voice_id: Mapped[int] = mapped_column(Integer, nullable=False)


class WtsStoryDatum(Base):
    __tablename__ = 'wts_story_data'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    repeat_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)


class XacStoryDatum(Base):
    __tablename__ = 'xac_story_data'

    title: Mapped[str] = mapped_column(Text, nullable=False)
    condition_quest_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_time: Mapped[str] = mapped_column(Text, nullable=False)
    balloon_pos_y: Mapped[float] = mapped_column(REAL, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    balloon_pos_x: Mapped[float] = mapped_column(REAL, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    condition_sub_story_id: Mapped[int] = mapped_column(Integer, nullable=False)


class XehStoryDatum(Base):
    __tablename__ = 'xeh_story_data'

    reward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count: Mapped[int] = mapped_column(Integer, nullable=False)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)


class YsnStoryDatum(Base):
    __tablename__ = 'ysn_story_data'

    condition_story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_3: Mapped[int] = mapped_column(Integer, nullable=False)
    sub_story_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_3: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_count_2: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_id_1: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_1: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    reward_count_1: Mapped[int] = mapped_column(Integer, nullable=False)
    disp_order: Mapped[int] = mapped_column(Integer, nullable=False)
    reward_type_2: Mapped[int] = mapped_column(Integer, nullable=False)
