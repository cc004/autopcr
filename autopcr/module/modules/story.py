from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.linq import flow
import datetime

@name('阅读公会剧情')
@default(True)
class guild_story_reading(Module):

    async def do_task(self, client: pcrclient):

        def guild_love_sum(guild_id: int) -> int:
            return (
            flow(getattr(db.guild_data[guild_id], f"member{i}") for i in range(1, 31)) 
            .where(lambda x: x != 0 and x in client.data.unit_love_data) 
            .sum(lambda x: client.data.unit_love_data[x].love_level)
            )

        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        for story in db.guild_story:
            if (
                story.story_id not in read_story and
                story.pre_story_id in read_story and
                guild_love_sum(story.requirement_id) >= story.love_level
                ):
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        if not self.log:
            raise SkipError("不存在未阅读的公会剧情")
        client.data.read_story_ids = list(read_story)
        self._log(f"共{len(self.log)}篇")

@name('阅读角色剧情')
@default(False)
class unit_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        for story in db.unit_story:
            if (
                story.story_id not in read_story and
                story.pre_story_id in read_story and
                story.story_group_id in client.data.unit_love_data and 
                client.data.unit_love_data[story.story_group_id].love_level >= story.love_level
                ):
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        if not self.log:
            raise SkipError("不存在未阅读的角色剧情")
        client.data.read_story_ids = list(read_story)
        self._log(f"共{len(self.log)}篇")

@name('阅读主线剧情')
@default(True)
class main_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        for story in db.main_story:
            if story.story_id not in read_story and story.pre_story_id in read_story:
                if not await client.unlock_quest_id(story.unlock_quest_id):
                    raise AbortError(f"区域{story.unlock_quest_id}未通关，无法观看{story.title}\n")
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        client.data.read_story_ids = list(read_story)
        if not self.log:
            raise SkipError("不存在未阅读的主线剧情")
        self._log(f"共{len(self.log)}篇")

@name('阅读露娜塔剧情')
@default(True)
class tower_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        for story in db.tower_story:
            now = datetime.datetime.now()
            start_time = db.parse_time(story.start_time)
            if now < start_time:
                continue
            if story.story_id not in read_story and story.pre_story_id in read_story:
                if not await client.unlock_quest_id(story.unlock_quest_id):
                    raise AbortError(f"层数{db.tower_quest[story.unlock_quest_id].floor_num}未通关，无法观看{story.title}\n")
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        client.data.read_story_ids = list(read_story)
        if not self.log:
            raise SkipError("不存在未阅读的露娜塔剧情")
        self._log(f"共{len(self.log)}篇")

@name('阅读活动剧情')
@default(True)
class hatsune_story_reading(Module):
    async def do_task(self, client: pcrclient):
        read_story = set(client.data.read_story_ids)
        read_story.add(0) # no pre story
        unlock_story = set(client.data.unlock_story_ids)
        for story in db.event_story:
            if story.story_id not in read_story and story.pre_story_id in read_story and story.story_id in unlock_story:
                await client.read_story(story.story_id)
                read_story.add(story.story_id)
                self._log(f"阅读了{story.title}")

        if not self.log:
            raise SkipError("不存在未阅读的活动剧情")
        client.data.read_story_ids = list(read_story)
        self._log(f"共{len(self.log)}篇")

@description('仅阅读当期活动')
@name('阅读活动信赖度')
@default(True)
class hatsune_dear_reading(Module):
    async def do_task(self, client: pcrclient):
        event_active = False
        for event in db.get_open_hatsune():
            event_active = True
            resp = (await client.get_hatsune_top(event.event_id))
            if resp.unchoiced_dear_story_id_list == None:
                continue
            resp = (await client.get_hatsune_dear_top(event.event_id))
            for story in resp.unlock_dear_story_info_list:
                if not story.is_choiced:
                    await client.read_dear(event.event_id, story.story_id)
                    self._log(f"阅读了{story.story_id}")

        if not event_active:
            raise SkipError("当前无可进入的活动")
        if not self.log:
            raise SkipError("不存在未阅读的活动信赖度剧情")
        self._log(f"共{len(self.log)}篇")

