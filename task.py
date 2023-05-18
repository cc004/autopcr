from nonebot import MessageSegment
from hoshino.typing import MessageSegment

from .autopcr.module.modulebase import ModuleManager
from .util import draw

class Task():
    def __init__(self, alian, target, bot, ev):
        self.info = (alian, target, bot, ev)

    async def do_task(self):
        alian, target, bot, ev = self.info 
        mgr = ModuleManager(target)

        await bot.send(ev, f"[CQ:reply,id={ev.message_id}]开始为{alian}清理日常")
        try:
            resp = await mgr.do_task()
            img = await draw(resp, target)
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + MessageSegment.image(f'file:///{img}'))
        except Exception as e:
            await bot.send(ev, f"[CQ:reply,id={ev.message_id}]" + str(e))

        return ev.user_id, target

