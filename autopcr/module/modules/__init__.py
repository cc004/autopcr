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

cron_modules = [
    cron1,
    cron2,
    cron3,
    cron4,
]

daily_modules = [
    global_config,
    chara_fortune,
    mission_receive_first,
    clan_like,
    room_like_back,
    free_gacha,
    normal_gacha,
    room_accept_all,
    explore_exp,
    explore_mana,
    underground_skip,
    tower_cloister_sweep,
    smart_very_hard_sweep,
    jjc_reward,
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
    smart_hard_sweep,
    smart_normal_sweep,

    all_in_hatsune,

    hatsune_hboss_sweep,
    hatsune_mission_accept1,
    hatsune_gacha_exchange,
    hatsune_mission_accept2,

    mission_receive_last,

    normal_shop,
    limit_shop,
    underground_shop,
    jjc_shop,
    pjjc_shop,

    love_up,
    main_story_reading,
    tower_story_reading,
    hatsune_story_reading,
    guild_story_reading,
    unit_story_reading,
    room_upper_all,
    user_info,
]

tool_modules = [
    get_library_import_data,
    get_need_equip,
    get_need_memory,
    get_need_xinsui,
    get_normal_quest_recommand,
]
