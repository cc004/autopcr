from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...util.linq import flow
from ...util.substory import GetSubStoryReader

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
        now = apiclient.datetime
        for story in db.unit_story:
            if (
                story.story_id not in read_story and
                (story.pre_story_id in read_story or now >= db.parse_time(story.force_unlock_time)) and
                (story.pre_story_id_2 in read_story or now >= db.parse_time(story.force_unlock_time_2)) and
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
        now = apiclient.datetime
        for story in db.main_story:
            start_time = db.parse_time(story.start_time)
            if now < start_time:
                self._log(f"剧情{story.title}解锁时间为{story.start_time}，无法观看\n")
                break
            if story.story_id not in read_story and story.pre_story_id in read_story:
                if not await client.unlock_quest_id(story.unlock_quest_id):
                    self._log(f"区域{story.unlock_quest_id}未通关，无法观看{story.title}\n")
                    break
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
            now = apiclient.datetime
            start_time = db.parse_time(story.start_time)
            if now < start_time:
                continue
            if story.story_id not in read_story and story.pre_story_id in read_story:
                if not await client.unlock_quest_id(story.unlock_quest_id):
                    floor_num = db.tower_quest[story.unlock_quest_id].floor_num if story.unlock_quest_id in db.tower_quest else 0
                    self._log(f"层数{floor_num}未通关，无法观看{story.title}\n")
                    break
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
        open_hatsune_id = set(hatsune.event_id for hatsune in db.get_open_hatsune())
        for story in db.event_story_detail:
            if story.story_id not in read_story and story.story_id in unlock_story:
                if (story.visible_type == eStoryVisibleType.EVENT_SPECIAL_STORY or 
                    story.visible_type == eStoryVisibleType.PRE_STORYID_AND_LOVE_LEVEL) and \
                        story.pre_story_id in read_story:
                    await client.read_story(story.story_id)
                    read_story.add(story.story_id)
                    self._log(f"阅读了{story.title}")

                elif story.visible_type == eStoryVisibleType.SEASONALY_DUMMY_STORY: 
                    event_id = db.event_story_data[story.story_group_id].value
                    if event_id not in open_hatsune_id:
                        continue
                    event_top = await client.get_hatsune_top(event_id)
                    additional_stories = {story.story_id: story for story in event_top.additional_stories} if event_top.additional_stories else {}
                    if story.story_id in additional_stories and \
                            additional_stories[story.story_id].is_unlocked and \
                            not additional_stories[story.story_id].is_readed:
                        await client.read_story(story.story_id)
                        read_story.add(story.story_id)
                        self._log(f"阅读了{story.title}")
                # Refraction TODO

        if not self.log:
            raise SkipError("不存在未阅读的活动剧情")
        client.data.read_story_ids = list(read_story)
        self._log(f"共{len(self.log)}篇")

@name('阅读活动子剧情')
@default(True)
class hatsune_sub_story_reading(Module):
    async def do_task(self, client: pcrclient):
        for sub_storys in client.data.event_sub_story.values() or []:
            reader = GetSubStoryReader(sub_storys, client)
            if not reader:
                self._warn(f"暂不支持的活动{db.event_name[sub_storys.event_id]}")
                continue

            if any(sub_story.status == eEventSubStoryStatus.ADDED for sub_story in sub_storys.sub_story_info_list):
                await reader.confirm()
            for sub_story in sub_storys.sub_story_info_list:
                if sub_story.status == eEventSubStoryStatus.UNREAD and reader.is_readable(sub_story.sub_story_id):
                    await reader.read(sub_story.sub_story_id)
                    self._log(f"阅读了{reader.title(sub_story.sub_story_id)}")
                    sub_story.status = eEventSubStoryStatus.READED
                if sub_story.status == eEventSubStoryStatus.READED and reader.is_puzzle_piece(sub_story.sub_story_id):
                    await reader.place_piece(sub_story.sub_story_id)
                    self._log(f"放置了{reader.title(sub_story.sub_story_id)}碎片")
                    sub_story.status = eEventSubStoryStatus.PUZZLE_PLACED
        if not self.log:
            raise SkipError("不存在未阅读的活动子剧情")
        else:
            self._log(f"共{len(self.log)}篇")

@description('阅读当期活动和已通关外传')
@name('阅读活动信赖度')
@default(True)
class hatsune_dear_reading(Module):

    def get_dear_title(self, event_id: int, story_id: int) -> str:
        try:
            group_id = db.dear_story_data[event_id].story_group_id
            dear_story = db.dear_story_detail[group_id][story_id]
            return f"{dear_story.title}-{dear_story.sub_title}"
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"未知剧情{event_id}-{story_id}"

    async def do_task(self, client: pcrclient):
        shiori_event = await client.get_shiori_top()
        for event_id in shiori_event.clear_event_list:
            if self.find_cache(str(event_id)):
                continue
            if event_id not in db.dear_story_data:
                continue

            resp = await client.get_shiori_event_top(event_id)
            if not resp.unchoiced_dear_story_id_list and \
               all(story_id not in client.data.unlock_story_ids for story_id in db.dear_story_detail[db.dear_story_data[event_id].story_group_id]):
                event_name = db.event_name[event_id]
                self._log(f"活动{event_name}信赖度未解锁")
                continue

            resp = await client.get_shiori_dear_top(event_id)
            for story in resp.unlock_dear_story_info_list:
                if not story.is_choiced:
                    await client.read_shiori_dear(event_id, story.story_id)
                    title = self.get_dear_title(event_id, story.story_id)
                    self._log(f"阅读了{title}")

            resp = await client.get_shiori_dear_top(event_id)
            group_id = db.dear_story_data[event_id].story_group_id
            if sum(1 for story in resp.unlock_dear_story_info_list if story.is_choiced) == len(db.dear_story_detail[group_id]):
                self.save_cache(str(event_id), 'readed')

        for event in db.get_open_hatsune():
            resp = (await client.get_hatsune_top(event.event_id))
            if not resp.unchoiced_dear_story_id_list:
                continue
            resp = (await client.get_hatsune_dear_top(event.event_id))
            for story in resp.unlock_dear_story_info_list:
                if not story.is_choiced:
                    await client.read_hatsune_dear(event.event_id, story.story_id)
                    title = self.get_dear_title(event.event_id, story.story_id)
                    self._log(f"阅读了{title}")

        if not self.log:
            raise SkipError("不存在未阅读的活动信赖度剧情")
        self._log(f"共{len(self.log)}篇")

