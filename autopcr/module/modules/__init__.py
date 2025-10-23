from dataclasses import field
from typing import Any
from .autosweep import *
from .box import *
from .nologin import *
from .caravan import *
from .clan import *
from .cron import *
from .daily import *
from .exequip import *
from .gacha import *
from .hatsune import *
from .room import *
from .shiori import *
from .shop import *
from .story import *
from .sweep import *
from .tower import *
from .tools import *
from .travel import *
from .unit import *
from .talent import *

@dataclass
class ModuleList:
    name: str = ""
    key: str = ""
    modules: List[Any] = field(default_factory=list)
    hidden_in_batch: bool = False
    hidden_in_clan: bool = False
    hidden: bool = False
    visible_in_clan: bool = False
    visible_in_batch: bool = False

cron_modules = ModuleList(
    '定时',
    'cron',
    [
        cron1,
        cron2,
        cron3,
        cron4,
        cron5,
        cron6,
    ],
    hidden_in_batch=True,
    hidden_in_clan=True,
)

daily_modules = ModuleList(
    '日常',
    'daily',
    [
        global_config,
        chara_fortune,
        mission_receive_first,
        clan_like,
        room_like_back,
        free_gacha,
        normal_gacha,
        monthly_gacha,
        room_accept_all,
        travel_round,
        travel_quest_sweep,
        ex_equip_recycle,
        explore_exp,
        explore_mana,
        underground_skip,
        special_underground_skip,
        tower_cloister_sweep,
        jjc_reward,
        talent_sweep,
        smart_very_hard_sweep,
        xinsui8_sweep,
        xinsui7_sweep,
        xinsui6_sweep,
        xinsui5_sweep,
        xinsui4_sweep,
        xinsui3_sweep,
        xinsui2_sweep,
        xinsui1_sweep,
        starcup2_sweep,
        starcup1_sweep, 
        hatsune_h_sweep,
        hatsune_dear_reading,
        present_receive,
        smart_sweep,
        mirai_very_hard_sweep,
        smart_hard_sweep,
        smart_shiori_sweep,
        last_normal_quest_sweep,
        lazy_normal_sweep,

        all_in_hatsune,

        hatsune_vhboss_sweep,
        hatsune_hboss_sweep,
        hatsune_mission_accept1,
        hatsune_gacha_exchange,
        hatsune_mission_accept2,

        # unit_equip_enhance_up,
        # unit_skill_level_up,

        mission_receive_last,
        seasonpass_accept,
        seasonpass_reward,

        normal_shop,
        limit_shop,
        underground_shop,
        jjc_shop,
        pjjc_shop,
        clanbattle_shop,
        master_shop_talent,
        master_shop,

        clan_equip_request,
        love_up,
        shiori_mission_check,
        main_story_reading,
        tower_story_reading,
        hatsune_story_reading,
        hatsune_sub_story_reading,
        guild_story_reading,
        unit_story_reading,
        birthday_story_reading,
        room_upper_all,
        user_info,
    ]
)

planning_modules = ModuleList(
    '规划',
    'planning',
    [
        get_library_import_data,
        get_need_equip,
        get_normal_quest_recommand,
        get_need_memory,
        get_need_pure_memory,
        get_need_xinsui,
    ],
    hidden_in_batch=True,
)

table_modules = ModuleList(
    '表格',
    'table',
    [
        get_talent_info,
        get_need_pure_memory_box,
    ],
    hidden=True,
    visible_in_batch=True,
)


unit_modules = ModuleList(
    '角色',
    'unit',
    [
        search_unit,
        missing_unit,
        refresh_box,
        unit_promote,
        unit_memory_buy,
        unit_set_unique_equip_growth,
        unit_exceed,
        unit_evolution,
    ]
)

clan_modules = ModuleList(
    '公会',
    'clan',
    [
        unit_promote_batch,
        unit_memory_buy_batch,
        set_my_party,
        get_box_table,
    ],
    hidden=True,
    visible_in_clan=True,
)

danger_modules = ModuleList(
    '危险',
    'danger',
    [
        gacha_start,
        gacha_exchange_chara,
    ],
    hidden_in_clan=True,
)

tool_modules = ModuleList(
    '工具',
    'tool',
    [
        find_talent_quest,
        find_clan_talent_quest,
        # return_jewel,
        # cook_pudding,
        ex_equip_rank_up,
        ex_equip_enhance_up,
        half_schedule,
        caravan_play,
        caravan_shop_buy,
        clan_battle_knive,
        ex_equip_info,
        travel_team_view,
        missing_emblem,
        get_clan_support_unit,
        clear_my_party,
        remove_cb_ex_equip,
        remove_cb_support,
        redeem_unit_swap,
    ]
)
