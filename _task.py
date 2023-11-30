from abc import abstractclassmethod, abstractmethod, abstractproperty
import traceback

from .autopcr.module.accountmgr import instance as accountmgr
from ._util import draw

class callback:
    @abstractmethod
    async def send(self, msg: str = '', img: str = ''): ...

    @abstractmethod
    async def request_validate(self, url: str): ...

class Task():
    def __init__(self, token, callback: callback, config={}):
        _, target = token
        self.callback = callback
        self.config = config
        self.token = token
        self.username = accountmgr.load(target, readonly=True).username

    @abstractclassmethod
    async def do_task(self): ...

class TaskList(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractclassmethod
    def do_module_list(self) -> list: ...

    async def do_task(self):
        alian, target = self.token
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.do_from_key(self.config, self.do_module_list())
            img = await draw(resp, alian + '_' + '_'.join(self.do_module_list()), self.callback.qid)
            self.callback.send(img = img)
        except Exception as e:
            traceback.print_exc()
            self.callback.send(msg = str(e))

class ClanBattleSupport(TaskList):
    def do_module_list(self) -> list:
        return ["get_clan_support_unit"]

class JJCBack(TaskList):
    def do_module_list(self) -> list:
        return ["jjc_back"]

class PJJCBack(TaskList):
    def do_module_list(self) -> list:
        return ["pjjc_back"]

class QuestRecommand(TaskList):
    def do_module_list(self) -> list:
        return ["get_normal_quest_recommand"]

class FindEquip(TaskList):
    def do_module_list(self) -> list:
        return ["get_need_equip"]

class GetLibraryImport(TaskList):
    def do_module_list(self) -> list:
        return ["get_library_import_data"]

class FindXinsui(TaskList):
    def do_module_list(self) -> list:
        return ["get_need_xinsui"]

class FindMemory(TaskList):
    def do_module_list(self) -> list:
        return ["get_need_memory"]

class Gacha(TaskList):
    def do_module_list(self) -> list:
        return ["gacha_start"]

class DailyClean(Task):
    async def do_task(self):
        alian, target = self.token
        try:
            await self.callback.send(msg = f"开始为{alian}清理日常")
        except Exception as e:  # 风控，怕report_to_su还失败，就不整了
            print(e)

        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.do_daily()
            img = await draw(resp, alian, self.callback.qid)
            await self.callback.send(msg = alian, img = img)
        except Exception as e:
            await self.callback.send(msg = f'{alian}: {e}')
