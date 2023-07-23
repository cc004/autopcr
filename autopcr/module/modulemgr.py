from ..core.pcrclient import pcrclient
from typing import List, Dict, Union
from ..model.error import *
from ..model.enums import *
from .modulebase import Module

import json
import traceback
class ModuleManager:
    _modules: List[type] = []

    def __init__(self, filename):
        self._filename = filename
        from .modules import daily_modules, tool_modules, cron_modules
        self.cron_modules: List[Module] = [m(self) for m in cron_modules]
        self.daily_modules: List[Module] = [m(self) for m in daily_modules]
        self.tool_modules: List[Module] = [m(self) for m in tool_modules]
        self.name_to_modules: Dict[str, Module] = {m.key: m for m in (self.daily_modules + self.tool_modules)}
        self._crons = []
        self._load_config()
    
    def _load_config(self):
        try:
            with open(self._filename, 'r') as f:
                self.data = json.load(f)
            self.client = self.get_android_client()
            self._load_from(self.data.get('config', {}))
        except:
            traceback.print_exc()
            raise
    
    def _load_from(self, data):
        self._crons.clear()
        for key, value in data.items():
            self.client.keys[key] = value
            
        # for name, module in self.modules.items():
        #     if name in data:
        #         module.open = data[name]
        #         self.data[name] = data[name]
        #     cron = module.cron_hook()
        #     if cron: self._crons.append(cron)
        # # 这里对time1和time2进行兼容
        # if data.get('time1open', False): self._crons.append(int((data['time1'] or "06:00").split(':')[0]))
        # if data.get('time2open', False): self._crons.append(int((data['time2'] or "18:00").split(':')[0]))
    
    def save_config(self):
        with open(self._filename, 'w') as f:
            json.dump(self.data, f)
    
    def get_config(self, name, default):
        return self.client.keys.get(name, default)
    
    def update_config(self, data):
        self._load_from(data)

    def generate_info(self, modules: List[Module]):
        return {
            'alian': self.data['alian'],
            'qq': "",
            'username': "",
            'password': "",
            'config': {**{key: m.get_config(key) for m in modules for key in m.config}, **{m.key: m.get_config(m.key) for m in modules}},
            'order': [m.key for m in modules],
            'data': {m.key: m.generate_info() for m in modules},
            'last_result': self.data.get('_last_result', None)
        }

    def generate_daily_info(self):
        return self.generate_info(self.cron_modules + self.daily_modules)

    def generate_tools_info(self):
        return self.generate_info(self.tool_modules)
    
    async def do_cron(self, hour):
        if hour in self._crons:
            await self.do_daily()

    def get_ios_client(self) -> pcrclient: # Header TODO
        client = pcrclient({
            'account': self.data['username'],
            'password': self.data['password'],
            'channel': 1000,
            'platform': 1
        })
        return client

    def get_android_client(self) -> pcrclient:
        client = pcrclient({
            'account': self.data['username'],
            'password': self.data['password'],
            'channel': 1,
            'platform': 2
        })
        return client

    async def do_daily(self):
        return await self.do_task(self.client.keys, self.daily_modules)

    async def do_from_key(self, config: dict, keys: List[str]):
        config.update({key: True for key in keys})
        modules = [self.name_to_modules[m] for m in keys]
        return await self.do_task(config, modules)

    async def do_task(self, config: dict, modules: List[Module]):
        self.client.keys = config

        resp: Dict[str, Union[List[str], Dict[str, Dict[str, str]]]] = {}
        resp['order'] = [m.key for m in modules]
        resp['result'] = {}
        try:
            client = self.client
            await client.login()
            for module in modules:
                resp['result'][module.__class__.__name__] = await module.do_from(client)
        except Exception as e:
            traceback.print_exc()
            raise(e)
        finally:
            self.data['_last_result'].update(resp['result'])
        return resp

