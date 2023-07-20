from ..model.common import ItemType
from ..core.pcrclient import pcrclient
from typing import List, Dict
from ..model.error import *
from ..db.database import db
from ..model.enums import *
from .modulebase import Module
import datetime

import json
import traceback
class ModuleManager:
    _modules: List[type] = []

    def __init__(self, filename):
        self._filename = filename
        from .modules import daily_modules 
        self.modules: List[Module] = [m(self) for m in daily_modules]
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

    def generate_config(self):
        return {
            # 'username': self.data['username'],
            # 'password': self.data['password'],
            'alian': self.data['alian'],
            'qq': "",
            'username': "",
            'password': "",
            'config': {**{key: m.get_config(key) for m in self.modules for key in m.config}, **{m.key: m.get_config(m.key) for m in self.modules}},
            'data': [m.generate_info() for m in self.modules],
            'last_result': self.data.get('_last_result', None)
        }
    
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

    async def get_library_import_data(self):
        try:
            client = self.client
            await client.login()
            msg = client.data.get_library_import_data()
            return msg
        except Exception as e:
            traceback.print_exc()
            raise(e)

    async def get_normal_quest_recommand(self, start_rank: int, like_unit_only: bool) -> List[str]:
        try:
            client = self.client
            await client.login()
            quest_list: List[int] = [id for id, quest in db.normal_quest_data.items() if db.parse_time(quest.start_time) <= datetime.datetime.now()]
            require_equip = client.data.get_equip_demand_gap(start_rank = start_rank, like_unit_only = like_unit_only)
            quest_weight = client.data.get_quest_weght(require_equip)
            quest_id = sorted(quest_list, key = lambda x: quest_weight[x], reverse = True)
            tot = []
            for i in range(10):
                id = quest_id[i]
                name = db.quest_name[id]
                tokens: List[ItemType] = [i for i in db.normal_quest_rewards[id]]
                msg = f"{name}:\n" + '\n'.join([
                    (f'{db.get_inventory_name_san(token)}: {"缺少" if require_equip[token] > 0 else "盈余"}{abs(require_equip[token])}片')
                    for token in tokens])
                tot.append(msg.strip())

            return tot
        except Exception as e:
            traceback.print_exc()
            raise(e)

    async def get_need_equip(self, start_rank: int, like_unit_only: bool):
        try:
            client = self.client
            await client.login()
            demand = list(client.data.get_equip_demand_gap(start_rank, like_unit_only).items())

            demand = sorted(demand, key=lambda x: x[1], reverse=True)

            title = [f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in demand]
            return title
            # return title + msg
        except Exception as e:
            traceback.print_exc()
            raise(e)

    async def get_need_xinsui(self):
        try:
            client = self.client
            await client.login()
            result, need = client.data.get_suixin_demand()
            result = sorted(result, key=lambda x: x[1])
            msg = [f"{db.get_inventory_name_san(item[0])}: 需要{item[1]}片" for item in result]

            store = client.data.get_inventory(db.xinsui) + client.data.get_inventory(db.heart) * 10
            cnt = need - store
            tot = f"当前心碎数量为{store}(大心自动转换成10心碎)，需要{need}，"
            if cnt > 0:
                tot += f"缺口数量为:{cnt}"
            elif cnt < 0:
                tot += f"盈余数量为:{-cnt}"
            else:
                tot += "当前心碎储备刚刚好！"
            msg = [tot] + msg
            return msg
        except Exception as e:
            traceback.print_exc()
            raise(e)

    async def get_need_memory(self):
        try:
            client = self.client
            await client.login()
            demand = list(client.data.get_memory_demand_gap().items())
            demand = sorted(demand, key=lambda x: x[1])

            msg = [f'{db.get_inventory_name_san(item[0])}: {"缺少" if item[1] > 0 else "盈余"}{abs(item[1])}片' for item in demand]
            return msg
        except Exception as e:
            traceback.print_exc()
            raise(e)

    async def do_daily(self):
        await self.do_task(self.modules)

    async def do_task(self, modules: List[Module]):
        result: Dict[str, Dict[str, str]] = {}
        try:
            client = self.client
            await client.login()
            for module in modules:
                result[module.__class__.__name__] = await module.do_from(client)
        except Exception as e:
            traceback.print_exc()
            raise(e)
        finally:
            self.data['_last_result'] = result
        return result

