from dataclasses import field
from typing import Any
from .autosweep import *
from .box import *
from .abyss import *
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
from .nbb import *  
from .mirage import *
from .bsm import *
from .labyrinth import *

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
        # cron5,
        # cron6,
        cron7,
        cron8,
        cron9,
        cron10,
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
        abyss_quest_sweep,
        abyss_boss_sweep,
        special_underground_skip,
        underground_skip,
        mirage_floor_receive,
        mirage_nemesis_sweep,
        tower_cloister_sweep,
        smart_very_hard_sweep,
        jjc_reward,
        talent_sweep,
        hatsune_dear_reading,
        present_receive,
        talent_sweep2,
        labyrinth_sweep,
        xinsui_sweep,
        starcup_sweep,
        hatsune_h_sweep,
        smart_sweep,
        mirai_very_hard_sweep,
        smart_hard_sweep,
        smart_shiori_sweep,
        mirai_sp1_h_sweep,
        mirai_sp1_shiori_sweep,
        last_normal_quest_sweep,
        lazy_normal_sweep,

        all_in_hatsune,

        hatsune_vhboss_sweep,
        hatsune_hboss_sweep,
        hatsune_mission_accept1,
        hatsune_gacha_exchange,
        hatsune_mission_accept2,

        jjc_daily,
        pjjc_daily,
        # unit_equip_enhance_up,
        # unit_skill_level_up,

        mission_receive_last,
        seasonpass_accept,
        seasonpass_reward,
        role_gacha,

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
        alces_story_reading,
        main_story_reading,
        tower_story_reading,
        hatsune_story_reading,
        seven_obtent_reading,
        hatsune_sub_story_reading,
        guild_story_reading,
        unit_story_reading,
        birthday_story_reading,
        room_upper_all,
        music_buy_all,  # 新增  
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
        get_need_sp_memory,
        get_need_xinsui,
    ],
    hidden_in_batch=True,
)

table_modules = ModuleList(
    '表格',
    'table',
    [
        get_need_pure_memory_box,
    ],
    hidden=False,
    visible_in_batch=False,
)


unit_modules = ModuleList(
    '角色',
    'unit',
    [
        one_click_ex_equip,
        search_unit,
        missing_unit,
        refresh_box,
        unit_promote,
        unit_memory_buy,
        unit_set_unique_equip_growth,
        unit_exceed,
        unit_evolution,
        search_ex_equip_id,
        equip_rainbow_ex,
        equip_pink_ex,
        equip_gold_ex,
    ]
)

clan_modules = ModuleList(
    '公会',
    'clan',
    [
        # unit_promote_batch,
        # unit_memory_buy_batch,
        set_my_party,
        get_box_table,
    ],
    hidden=False,
    visible_in_clan=False,
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
        daily_order_edit,
        labyrinth_start_reroll,
        labyrinth_point_query,
        add_friend,
        search_ex_equip_id,
        ex_equip_rainbow_enchance,
        ex_equip_power_maximun,
        set_my_party2,
        bsm_auto,
        set_cb_support,
        set_dungeon_support,  
        set_friend_support,
        nbb_game,
        remove_normal_ex_equip,
        # calc_best_3star_ex_equip,
        query_player_profile,
        find_talent_quest,
        find_clan_talent_quest,
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
        get_my_support,          # 新增：我的支援  
        clear_my_party,
        remove_cb_ex_equip,
        save_ex_state,        # 新增  
        restore_ex_state,     # 新增  
        remove_cb_support,
        redeem_unit_swap,
        jjc_back,
        pjjc_back,
        jjc_info,
        pjjc_info,
        pjjc_def_shuffle_team,
        pjjc_atk_shuffle_team,
    ]
)
