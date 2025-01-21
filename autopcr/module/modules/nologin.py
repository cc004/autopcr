from abc import ABC
from enum import Enum
from ...db.database import db
from ...model.enums import eCampaignCategory
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *
from collections import defaultdict

@dataclass
class ISchedule(ABC):
    start_time: str
    end_time: str
    description: str = ""

    @property
    def enabled(self) -> bool:
        return db.parse_time(self.start_time) > datetime.now()

    def get_description(self) -> str:
        return self.description

class SeasonpassFoundation(ISchedule):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    @property
    def get_description(self) -> str:
        return self.name

class ClanBattlePeriod(ISchedule):
     description = "公会战"

class SecretDungeonSchedule(ISchedule):
     description = "特别地下城"

class GachaDatum(ISchedule):
    def __init__(self, gacha_id: int, exchange_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gacha_id = gacha_id
        self.exchange_id = exchange_id

    @property
    def enabled(self) -> bool:
        return super().enabled and self.gacha_id / 10000 > 2

    def get_description(self) -> str:
        if self.exchange_id != 0:
            exchange_lineups = [e.unit_id for e in db.gacha_exchange_chara[self.exchange_id]]
            return f"up {','.join(db.get_unit_name(id) for id in exchange_lineups)}"
        return db.gacha_data[self.gacha_id].gacha_name

class CampaignSchedule(ISchedule):
    class eCampaignCategoryLow(Enum):
        ARENA = "竞技场"
        GRAND_ARENA = "公主竞技场"
        DUNGEON = "地下城"
        SECRET_DUNGEON = "特别地下城"
        NORMAL = "normal"
        HARD = "hard"
        BOTH = "normal&hard"
        HATSUNE_NORMAL = "活动normal"
        HATSUNE_HARD = "活动hard"
        HATSUNE_BOTH = "活动"
        HATSUNE_REVIVAL_NORMAL = "复刻活动normal"
        HATSUNE_REVIVAL_HARD = "复刻活动hard"
        HATSUNE_REVIVAL_BOTH = "复刻活动"
        REVIVAL_NORMAL = "复刻活动normal"
        REVIVAL_HARD = "复刻活动hard"
        REVIVAL_BOTH = "复刻活动"
        SHIORI_NORMAL = "外传normal"
        SHIORI_HARD = "外传hard"
        SHIORI_BOTH = "外传"
        VERY_HARD = "vh"
        UNIQUE_EQUIP = "圣迹"
        EXP_TRAINING = "探索"
        GOLD_TRAINING = "探索"
        TRAINING = "探索"
        HIGH_RARITY_EQUIP = "神殿"
        EVENT_NORMAL = "活动normal"
        EVENT_HARD = "活动hard"

    class eCampaignCategoryHigh(Enum):
        HALF_STAMINA = "体力消耗"
        ITEM_DROP_RARE = "掉率"
        ITEM_DROP_AMOUNT = "掉落"
        GOLD_DROP_AMOUNT = "mana"
        COIN_DROP_AMOUNT = "金币"
        COOL_TIME = "冷却时间"
        CHALLENGE_NUM = "挑战次数"
        PLAYER_EXP_AMOUNT = "玩家经验值"
        MASTER_COIN_DROP = "大师币"

    def __init__(self, campaign_category: int, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.campaign_category = campaign_category
        self.value = value

    def get_description(self) -> str:
        cat = eCampaignCategory(self.campaign_category).name.split('_')
        for i in range(1, len(cat)):
            high_part = '_'.join(cat[:i])
            low_part = '_'.join(cat[i:])
            try:
                high = CampaignSchedule.eCampaignCategoryHigh[high_part].value
                low = CampaignSchedule.eCampaignCategoryLow[low_part].value
                return f"{low} {high}*{self.value / 1000.0}"
            except KeyError:
                continue
        return '_'.join(cat)

class CampaignFreegacha(ISchedule):
    description = "免费十连"

class HatsuneSchedule(ISchedule):
    def __init__(self, event_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_id = event_id

    def get_description(self) -> str:
        event_name = db.event_name[self.event_id]
        return event_name

class TowerSchedule(ISchedule):
    description = "露娜塔"

class CharaFortuneSchedule(ISchedule):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def get_description(self) -> str:
        return self.name

class LoginBonusDatum(ISchedule):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def get_description(self) -> str:
        return self.name

@description('查看日程')
@name("半月刊")
@default(True)
@notlogin()
class half_schedule(Module):
    schedules = [
        (db.clan_battle_period, lambda x: ClanBattlePeriod(x.start_time, x.end_time, "公会战")),
        (db.secret_dungeon_schedule, lambda x: SecretDungeonSchedule(x.start_time, x.end_time, "特别地下城")),
        (db.seasonpass_foundation, lambda x: SeasonpassFoundation(x.name, x.start_time, x.end_time, "季卡")),
        (db.gacha_data, lambda x: GachaDatum(x.gacha_id, x.exchange_id, x.start_time, x.end_time, "扭蛋")),
        (db.campaign_schedule, lambda x: CampaignSchedule(x.campaign_category, x.value, x.start_time, x.end_time, "庆典")),
        (db.campaign_free_gacha, lambda x: CampaignFreegacha(x.start_time, x.end_time, "免费十连")),
        (db.hatsune_schedule, lambda x: HatsuneSchedule(x.event_id, x.start_time, x.end_time, "活动")),
        (db.tower_schedule, lambda x: TowerSchedule(x.start_time, x.end_time, "露娜塔")),
        (db.chara_fortune_schedule, lambda x: CharaFortuneSchedule(x.name, x.start_time, x.end_time, "赛马")),
        (db.login_bonus_data, lambda x: LoginBonusDatum(x.name, x.start_time, x.end_time, "登录奖励")),
    ]
    async def do_task(self, _: pcrclient):
        schedules = defaultdict(list)
        for table, factory in self.schedules:
            for row in table.values():
                schedule = factory(row)
                if schedule.enabled:
                    schedules[(db.format_date(db.parse_time(schedule.start_time)), db.format_date(db.parse_time(schedule.end_time)))].append(schedule.get_description())
        times = sorted(schedules.keys())
        for time in times:
            st = time[0]
            ed = time[1]
            self._log(f"{st} - {ed}")
            for msg in schedules[time]:
                self._log(f"    {msg}")
