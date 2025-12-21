from enum import IntEnum
from typing import Callable, List, Union

from ..model.enums import eFpcOperationType, eFpcPeriod
from ..model.enums import eEventSubStoryStatus

from .linq import flow
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
    special: bool = False

    def is_readable(self, sub_story_id: int) -> bool:
        return True # it seems to be readable when it appear in the substory list
    def is_puzzle_piece(self, sub_story_id: int) -> bool:
        return False

    def title(self, sub_story_id: int) -> str: ...
    async def read(self, sub_story_id: int): ...
    async def place_piece(self, sub_story_id: int): ...
    async def special_read(self, sub_storys: List[EventSubStory], _log: Callable): ...
    async def confirm(self): ...
    async def prepare(self):
        pass

    def __init__(self, client: pcrclient):
        self.client = client

def GetSubStoryReader(sub_story_data: EventSubStory, client: pcrclient) -> Union[SubStoryReader, None]:
    if sub_story_data.event_id in constructor:
        return constructor[sub_story_data.event_id](client)
    return None

@EventId(10148)
class tpr_substory(SubStoryReader):
    special = True

    def title(self, sub_story_id: int) -> str:
        return db.tpr_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_tpr_story(sub_story_id)

    async def special_read(self, sub_storys: EventSubStory, _log: Callable):
        all_ids = set(s.sub_story_id for s in sub_storys.sub_story_info_list)
        unread_ids = set(s.sub_story_id for s in sub_storys.sub_story_info_list if s.status == eEventSubStoryStatus.UNREAD)

        if unread_ids:
            for story_id in unread_ids:
                await self.client.story_check(story_id)
                await self.client.read_tpr_story(story_id)
                _log(f'阅读了{self.title(story_id)}')
            unread_ids.clear()

        for panel in db.tpr_panel_data:
            panel_data = db.tpr_panel_data[panel]
            for i, story_id in enumerate([panel_data.correct_sub_story_id, panel_data.another_sub_story_id], start=1):
                if story_id in all_ids:
                    continue
                correct_parts = panel_data.get_correct_parts() if i == 1 else panel_data.get_another_parts()
                correct_parts = list(correct_parts)
                if not correct_parts:
                    continue
                resp = await self.client.tpr_register_success(panel, i, correct_parts)
                unread_ids |= set(s.sub_story_id for s in resp.unlock_sub_story_info_list if s.status == eEventSubStoryStatus.UNREAD)
                _log(f'完成了第{panel}面板的{"" if i == 1 else "隐藏"}拼图')

        if unread_ids:
            for story_id in unread_ids:
                await self.client.story_check(story_id)
                await self.client.read_tpr_story(story_id)
                _log(f'阅读了{self.title(story_id)}')
            unread_ids.clear()

@EventId(10146)
class apg_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.apg_story_data[sub_story_id].sub_story_id

    async def prepare(self):
        await self.client.apg_story_top()

    async def read(self, sub_story_id: int):
        await self.client.read_apg_story(sub_story_id)

@EventId(10140)
class fpc_substory(SubStoryReader):
    special = True

    def title(self, sub_story_id: int) -> str:
        return db.fpc_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_fpc_story(sub_story_id)

    async def special_read(self, sub_storys: EventSubStory, _log: Callable):
        all_ids = set(s.sub_story_id for s in sub_storys.sub_story_info_list)
        unread_ids = set(s.sub_story_id for s in sub_storys.sub_story_info_list if s.status == eEventSubStoryStatus.UNREAD)
        cnt = 0;
        last_period = eFpcPeriod.DAY
        for period in eFpcPeriod:
            unread_in_period = flow(unread_ids).where(lambda id: db.fpc_story_data[id].period == period).to_list()
            fpc_op = eFpcOperationType.DAY_NIGHT_CHANGE if last_period != period else eFpcOperationType.SKIP
            last_period = period
            for _ in range(80): # should not be more than 80 times
                if len(unread_in_period) == 0:
                    break
                resp = await self.client.draw_fpc_story(period, fpc_op)
                fpc_op = eFpcOperationType.SKIP
                cnt += 1
                if resp.hit_sub_story_id in all_ids:
                    if resp.hit_sub_story_id in unread_in_period:
                        await self.read(resp.hit_sub_story_id)
                        _log(f'阅读了{self.title(resp.hit_sub_story_id)}')
                        unread_in_period.remove(resp.hit_sub_story_id)
                        next((s for s in sub_storys.sub_story_info_list if s.sub_story_id == resp.hit_sub_story_id)).status = eEventSubStoryStatus.READED
            else:
                _log(f'80次未能完成故事阅读，下次再试吧')
        if cnt:
            _log(f'观看了{cnt}次表演')


@EventId(10137)
@EventId(10136)
class ais_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.ais_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_ais_story(sub_story_id)

    async def confirm(self):
        await self.client.confirm_ais_story()

@EventId(10134)
class nyd_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.nyd_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_nyd_story(sub_story_id)

@EventId(10132)
class xac_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.xac_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_xac_story(sub_story_id)

@EventId(10130)
class asb_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.asb_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_asb_story(sub_story_id)

@EventId(10128)
class wtm_substory(SubStoryReader):

    def title(self, sub_story_id: int) -> str:
        return db.wtm_story_data[sub_story_id].title

    async def read(self, sub_story_id: int):
        await self.client.read_wtm_story(sub_story_id)

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
