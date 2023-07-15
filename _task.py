from abc import abstractclassmethod
from nonebot import MessageSegment
from hoshino.typing import MessageSegment

from .autopcr.module.modulebase import ModuleManager
from .autopcr.module.accountmgr import instance as accountmgr
from ._util import draw, draw_line, render_forward_msg

class Task():
    def __init__(self, token, bot, ev, qid = None, gid = None):
        alian, target = token
        self.info = (alian, target, bot, ev, qid, gid)
        self.token = token

    @abstractclassmethod
    async def do_task(self): ...

class QuestRecommand(Task):
    def __init__(self, start_rank = None, like_unit_only = None, *args, **kwargs):
        self.start_rank = start_rank
        self.like_unit_only = like_unit_only
        super().__init__(*args, **kwargs)

    async def do_task(self):
        alian, target, bot, ev, qid, gid = self.info 
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.get_normal_quest_recommand(self.start_rank, self.like_unit_only)
            img = await draw_line(resp, alian)
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

class FindEquip(Task):
    def __init__(self, start_rank = None, like_unit_only = None, *args, **kwargs):
        self.start_rank = start_rank
        self.like_unit_only = like_unit_only
        super().__init__(*args, **kwargs)

    async def do_task(self):
        alian, target, bot, ev, qid, gid = self.info 
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.get_need_equip(self.start_rank, self.like_unit_only)
            img = await draw_line(resp, alian)
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

class GetLibraryImport(Task):
    async def do_task(self):
        alian, target, bot, ev, qid, gid = self.info 
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.get_library_import_data()
            msg = render_forward_msg([resp])
            await bot.send_group_forward_msg(group_id=ev.group_id, messages=msg)
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

class FindXinsui(Task):
    async def do_task(self):
        alian, target, bot, ev, qid, gid = self.info
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.get_need_xinsui()
            img = await draw_line(resp, alian)
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

class FindMemory(Task):
    async def do_task(self):
        alian, target, bot, ev, qid, gid = self.info
        try:
            async with accountmgr.load(target) as mgr:
                resp = await mgr.get_need_memory()
            img = await draw_line(resp, alian)
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

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
                resp = await mgr.do_task()
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

