from dataclasses import field
from typing import Any
from .autosweep import *
from .clan import *
from .cron import *
from .daily import *
from .gacha import *
from .hatsune import *
from .room import *
from .shop import *
from .story import *
from .sweep import *
from .tower import *
from .tools import *
from .travel import *
from .unit import *

@dataclass
class ModuleList:
    name: str = ""
    key: str = ""
    modules: List[Any] = field(default_factory=list)

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
    ]
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
        smart_very_hard_sweep,
        jjc_reward,
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
        smart_normal_sweep,

        all_in_hatsune,

        hatsune_hboss_sweep,
        hatsune_mission_accept1,
        hatsune_gacha_exchange,
        hatsune_mission_accept2,

        jjc_daily,
        pjjc_daily,
        unit_equip_enhance_up,
        unit_skill_level_up,

        mission_receive_last,
        seasonpass_accept,
        seasonpass_reward,

        normal_shop,
        limit_shop,
        underground_shop,
        jjc_shop,
        pjjc_shop,
        clanbattle_shop,
        
        clan_equip_request,
        love_up,
        main_story_reading,
        tower_story_reading,
        hatsune_story_reading,
        hatsune_sub_story_reading,
        guild_story_reading,
        unit_story_reading,
        room_upper_all,
        user_info,
    ]
)

clan_modules = ModuleList(
    '公会',
    'clan',
    [
        unit_promote_batch,
        set_my_party,
    ]
)

danger_modules = ModuleList(
    '危险',
    'danger',
    [
        gacha_start,
    ]
)

tool_modules = ModuleList(
    '工具',
    'tool',
    [
        # cook_pudding,
        remove_cb_support,
        travel_team_view,
        ex_equip_info,
        redeem_unit_swap,
        unit_promote,
        unit_set_unique_equip_growth,
        missing_unit,
        get_need_equip,
        get_normal_quest_recommand,
        get_need_memory,
        get_need_pure_memory,
        get_need_xinsui,
        get_clan_support_unit,
        get_library_import_data,
        jjc_back,
        pjjc_back,
        jjc_info,
        pjjc_info,
        pjjc_shuffle_team,
    ]
)
