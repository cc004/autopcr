from abc import abstractclassmethod, abstractproperty
from nonebot import MessageSegment
from hoshino.typing import MessageSegment
import traceback

from .autopcr.module.accountmgr import instance as accountmgr
from ._util import draw, render_forward_msg

class Task():
    def __init__(self, token, bot, ev, qid = None, gid = None, config = {}):
        alian, target = token
        self.info = (alian, target, bot, ev, qid, gid)
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
        alian, target, bot, ev, qid, gid = self.info
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.do_from_key(self.config, self.do_module_list())
            img = await draw(resp, alian + '_'.join(self.do_module_list()))
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            traceback.print_exc()
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

class ClanBattleSupport(TaskList):
    def do_module_list(self) -> list:
        return ["get_clan_support_unit"]

class JJCBack(TaskList):
    def do_module_list(self) -> list:
        return ["jjc_back"]

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
        alian, target, bot, ev, qid, gid = self.info
        try:
            if ev:
                await bot.send(ev, f"[CQ:reply,id={ev.message_id}]开始为{alian}清理日常")
            else:
                await bot.send_group_msg(group_id = gid, message = f"【定时任务】开始为{alian}清理日常")
        except Exception as e: # 风控，怕report_to_su还失败，就不整了
            print(e)

        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.do_daily()
            img = await draw(resp, alian)
            if ev:
                await bot.send(ev, f"[CQ:reply,id={ev.message_id}] {alian}" + MessageSegment.image(f'file:///{img}'))
            else:
                await bot.send_group_msg(group_id = gid, message = f"【定时任务】{alian}" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            if ev:
                await bot.send(ev, f"[CQ:reply,id={ev.message_id}] {alian}:" + str(e))
            else:
                await bot.send_group_msg(group_id = gid, message = f"【定时任务】{alian}:" + str(e))

