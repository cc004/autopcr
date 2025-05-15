from typing import Union
from ..core.pcrclient import pcrclient
from ..core.apiclient import apiclient
from ..model.common import EventSubStory
from ..db.database import db
import datetime

constructor = {}

def EventId(event_id: int):
    def decorator(cls):
        constructor[event_id] = cls
        return cls
    return decorator

class SubStoryReader:

    client: pcrclient

    def is_readable(self, sub_story_id: int) -> bool:
        return True # it seems to be readable when it appear in the substory list
    def is_puzzle_piece(self, sub_story_id: int) -> bool:
        return False

    def title(self, sub_story_id: int) -> str: ...
    async def read(self, sub_story_id: int): ...
    async def place_piece(self, sub_story_id: int): ...
    async def confirm(self): ...

    def __init__(self, client: pcrclient):
        self.client = client

def GetSubStoryReader(sub_story_data: EventSubStory, client: pcrclient) -> Union[SubStoryReader, None]:
    if sub_story_data.event_id in constructor:
        return constructor[sub_story_data.event_id](client)
    return None

@EventId(10122)
class wts_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.wts_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_wts_story(sub_story_id)

@EventId(10120)
class bmy_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.bmy_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_bmy_story(sub_story_id)

@EventId(10118)
class dvs_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.dvs_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_dvs_story(sub_story_id)

@EventId(10116)
class won_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.won_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_won_story(sub_story_id)

@EventId(10110)
@EventId(10111)
class mme_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.mme_story_data[sub_story_id].title

    def is_puzzle_piece(self, sub_story_id: int) -> bool:
        return db.mme_story_data[sub_story_id].is_puzzle_piece == 1

    async def read(self, sub_story_id: int):
        if db.mme_story_data[sub_story_id].original_event_id == 10110:
            await self.client.story_check(sub_story_id)
        await self.client.read_mme_story(sub_story_id)

    async def place_piece(self, sub_story_id: int):
        await self.client.put_mme_piece(sub_story_id)

@EventId(10108)
class dsb_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.dsb_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_dsb_story(sub_story_id)

@EventId(10106)
class xeh_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.xeh_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_xeh_story(sub_story_id)

@EventId(10098)
class lsv_substory(SubStoryReader):

    def is_readable(self, sub_story_id: int) -> bool:
        open_time = db.parse_time(db.lsv_story_data[sub_story_id].time_condition)
        return apiclient.datetime >= open_time

    def title(self, sub_story_id: int) -> str:
        return db.lsv_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_lsv_story(sub_story_id)

@EventId(10084)
@EventId(10085)
class ysn_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.ysn_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        if db.ysn_story_data[sub_story_id].original_event_id == 10084:
            await self.client.story_check(sub_story_id)
        await self.client.read_ysn_story(sub_story_id)

@EventId(10082)
class nop_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return str(sub_story_id)

    async def read(self, sub_story_id: int):
        await self.client.read_nop_story(sub_story_id)

@EventId(10074)
class mhp_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.mhp_story_data[sub_story_id].title + ' ' + db.mhp_story_data[sub_story_id].sub_title

    async def read(self, sub_story_id: int):
        await self.client.read_mhp_story(sub_story_id)

@EventId(10070)
class svd_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.svd_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_svd_story(sub_story_id)

@EventId(10064)
class ssp_dsubstory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.ssp_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_ssp_story(sub_story_id)

@EventId(10058)
@EventId(10059)
class ske_dsubstory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.ske_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_ske_story(sub_story_id)

    async def confirm(self):
        await self.client.confirm_ske_story()

@EventId(10048)
class lto_dsubstory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.lto_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_lto_story(sub_story_id)
