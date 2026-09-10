from typing import Dict, List, Callable, Any
from .modules import cron_modules, daily_modules, clan_modules, danger_modules, tool_modules, ModuleList, Module, CronModule, planning_modules, unit_modules, table_modules
from .modulemgr import ModuleManager  
  
from ..constants import DAILY_ORDER_KEY
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
        return self.name_to_modules[key](self.modulemgr)

    def get_modules_list(self, key: str) -> List[Any]:  
        modules = self.modules.get(key, ModuleList()).modules  
  
        # 仅对「日常」做个人顺序重排，其余 tab 保持默认顺序  
        if key == 'daily':  
            order = self.modulemgr.config.get(DAILY_ORDER_KEY, None)  
            if order:  
                # 建立 类实例化后的 key -> 类 的映射（保留默认相对顺序）  
                key_to_cls = {}  
                for m in modules:  
                    key_to_cls[m(self.modulemgr).key] = m  
  
                sorted_modules = []  
                used = set()  
                # 1) 先按账号存储的顺序放入仍存在的模块  
                for k in order:  
                    if k in key_to_cls and k not in used:  
                        sorted_modules.append(key_to_cls[k])  
                        used.add(k)  
                # 2) 再把存储顺序里没提到的模块，按默认顺序补到后面  
                for m in modules:  
                    mk = m(self.modulemgr).key  
                    if mk not in used:  
                        sorted_modules.append(m)  
                        used.add(mk)  
                modules = sorted_modules  
  
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
            if clan and ml.hidden_in_clan:
                continue
            if batch and ml.hidden_in_batch:
                continue
            if not clan and not batch and ml.hidden:
                continue
            if clan and ml.visible_in_clan or batch and ml.visible_in_batch or not ml.hidden:
                modules.append(ml)
        return [{'key': m.key, 'name': m.name} for m in modules]
