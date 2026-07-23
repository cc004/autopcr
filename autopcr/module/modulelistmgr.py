from typing import Dict, List, Callable, Any
from .modules import cron_modules, daily_modules, clan_modules, danger_modules, tool_modules, ModuleList, Module, CronModule, planning_modules, unit_modules, table_modules
from .modulemgr import ModuleManager
from ..core.region import get_region, REGION_TW


# Endpoints in this set are present in the TW protocol references and rely on
# master-data tables available in the TW mirror.  Newer CN-only systems stay
# hidden instead of producing a long sequence of API errors during daily runs.
TW_SUPPORTED_MODULES = {
    'cron1', 'cron2', 'cron3', 'cron4', 'cron5', 'cron6',
    'global_config',
    # TW 5.7 request/response schemas and regional master data were audited
    # for these existing modules.  Entries requiring a regional wire adapter
    # remain intentionally excluded.
    'chara_fortune', 'free_gacha',
    'travel_round', 'travel_quest_sweep', 'ex_equip_recycle',
    'special_underground_skip',
    'mirage_floor_receive', 'mirage_nemesis_sweep',
    'tower_cloister_sweep',
    'abyss_quest_sweep', 'abyss_boss_sweep',
    'talent_sweep', 'talent_sweep2',
    'xinsui1_sweep', 'xinsui2_sweep', 'xinsui3_sweep',
    'xinsui4_sweep', 'xinsui5_sweep', 'xinsui6_sweep',
    'xinsui7_sweep', 'xinsui8_sweep', 'xinsui9_sweep',
    'starcup1_sweep', 'starcup2_sweep', 'starcup3_sweep',
    'hatsune_dear_reading', 'smart_sweep',
    'mirai_very_hard_sweep', 'smart_shiori_sweep',
    'mirai_sp1_h_sweep', 'mirai_sp1_shiori_sweep',
    'all_in_hatsune',
    'master_shop_talent', 'master_shop', 'love_up',
    'shiori_mission_check', 'alces_story_reading',
    'ex_equip_rainbow_enchance',
    'seven_obtent_reading',
    'ex_equip_power_maximun', 'set_my_party2',
    'find_talent_quest', 'find_clan_talent_quest',
    'ex_equip_rank_up', 'ex_equip_enhance_up', 'half_schedule',
    'caravan_play', 'caravan_shop_buy', 'clan_battle_knive',
    'ex_equip_info', 'travel_team_view', 'missing_emblem',
    'get_clan_support_unit', 'clear_my_party',
    'remove_cb_ex_equip', 'remove_cb_support', 'redeem_unit_swap',
    'search_unit', 'missing_unit', 'refresh_box', 'unit_promote',
    'unit_memory_buy', 'unit_set_unique_equip_growth',
    'unit_exceed', 'unit_evolution',
    'get_library_import_data', 'get_need_equip',
    'get_normal_quest_recommand', 'get_need_memory',
    'get_need_pure_memory', 'get_need_sp_memory', 'get_need_xinsui',
    'gacha_start', 'gacha_exchange_chara',
    'mission_receive_first', 'mission_receive_last',
    'seasonpass_accept', 'seasonpass_reward',
    'clan_like', 'clan_equip_request',
    'room_like_back', 'room_accept_all', 'room_upper_all',
    'normal_gacha',
    'explore_exp', 'explore_mana', 'underground_skip',
    'jjc_reward', 'present_receive',
    'smart_very_hard_sweep', 'smart_hard_sweep',
    'last_normal_quest_sweep', 'lazy_normal_sweep',
    'hatsune_h_sweep', 'hatsune_vhboss_sweep',
    'hatsune_hboss_sweep', 'hatsune_mission_accept1',
    'hatsune_mission_accept2', 'hatsune_gacha_exchange',
    'normal_shop', 'limit_shop', 'underground_shop',
    'jjc_shop', 'pjjc_shop', 'clanbattle_shop',
    'main_story_reading', 'tower_story_reading',
    'hatsune_story_reading', 'hatsune_sub_story_reading',
    'guild_story_reading', 'unit_story_reading',
    'birthday_story_reading', 'user_info',
}

class ModuleListManager:

    modules: Dict[str, ModuleList] = {
        cron_modules.key: cron_modules,
        daily_modules.key: daily_modules,
        tool_modules.key: tool_modules,
        unit_modules.key: unit_modules,
        planning_modules.key: planning_modules,
        table_modules.key: table_modules,
        clan_modules.key: clan_modules,
        danger_modules.key: danger_modules,
    }
    name_to_modules: Dict[str, Callable] = {m.__name__: m for ml in modules.values() for m in ml.modules}

    def __init__(self, modulemgr: ModuleManager):
        self.modulemgr = modulemgr

    @property
    def daily_modules(self) -> List[Module]:
        return self.get_modules_list('daily')

    @property
    def cron_modules(self) -> List[CronModule]:
        return self.get_modules_list('cron')

    def get_module_from_key(self, key: str) -> Module:
        if key not in self.name_to_modules:
            raise ValueError(f"模块{key}未找到")
        if get_region() == REGION_TW and key not in TW_SUPPORTED_MODULES:
            raise ValueError(f"台服暂不支持模块{key}")
        return self.name_to_modules[key](self.modulemgr)

    def get_modules_list(self, key: str) -> List[Any]:
        modules = self.modules.get(key, ModuleList()).modules
        if get_region() == REGION_TW:
            modules = [m for m in modules if m.__name__ in TW_SUPPORTED_MODULES]
        return [m(self.modulemgr) for m in modules]
    
    def generate_info(self, key: str):
        modules = self.get_modules_list(key)
        return {
            'config': {**{key: m.get_config(key) for m in modules for key in m.config}, **{m.key: m.get_config(m.key) for m in modules}},
            'order': [m.key for m in modules],
            'info': {m.key: m.generate_info() for m in modules},
        }

    def generate_tab(self, clan: bool = False, batch: bool = False):
        modules = []
        for ml in self.modules.values():
            if get_region() == REGION_TW and not any(
                module.__name__ in TW_SUPPORTED_MODULES
                for module in ml.modules
            ):
                continue
            if clan and ml.hidden_in_clan:
                continue
            if batch and ml.hidden_in_batch:
                continue
            if not clan and not batch and ml.hidden:
                continue
            if clan and ml.visible_in_clan or batch and ml.visible_in_batch or not ml.hidden:
                modules.append(ml)
        return [{'key': m.key, 'name': m.name} for m in modules]
