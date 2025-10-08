from typing import Callable, Tuple, Union, Type, Any, Optional, List, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from ..core import pcrclient
from ..db.database import db
from ..util.pcr_data import CHARA_NAME, CHARA_NICKNAME
from copy import copy

def _wrap_init(cls, setter):
    old = cls.__init__
    def __init__(self, *args, **kwargs):
        old(self, *args, **kwargs)
        setter(self)
    cls.__init__ = __init__

    return cls

@dataclass_json
@dataclass
class Candidate:
    """Class representing a candidate for configuration."""
    value: Any
    display: str
    tags: Optional[List[str]] = None
    nickname: Optional[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class Config:
    """Base class for all configuration types."""
    
    def __init__(self, key: str, desc: str, default: Any, candidates: Union[Callable, List], short_display: bool = False):
        from .modulebase import Module
        self.key = key
        self.desc = desc
        self._default = default
        self._candidates = candidates
        self._parent: Module = None  # Will be set when the decorator is applied
        self.short_display = short_display
    
    @property
    def config_type(self) -> str:
        """Return the configuration type identifier."""
        return 'base'

    @property
    def candidates(self):
        """Get the available candidates for this configuration."""
        if callable(self._candidates):
            # If candidates is a callable, call it to get the candidates
            return self._candidates()
        else:
            return self._candidates

    def candidate_display(self, candidate) -> str:
        """Get the display names for the available candidates."""
        return str(candidate)

    def candidate_tag(self, candidate) -> List[str]:
        """Get the display names for the available candidates."""
        return []

    @property
    def candidates_json(self):
        """Get the available candidates for this configuration."""
        return [Candidate(
                    value = c, 
                    display = str(self.candidate_display(c)),
                    tags = self.candidate_tag(c),
                ) for c in self.candidates]
    
    @property
    def default(self):
        """Get the default value for this configuration."""
        if callable(self._default):
            return self._default()
        else:
            return self._default

    def dict(self) -> dict:
        """Return a dictionary representation of this configuration."""
        return {
            "key": self.key,
            "desc": self.desc,
            "default": self.default,
            "candidates": self.candidates_json,
            "config_type": self.config_type,
        }
    
    def get_value(self) -> Any:
        """Get the current value from the parent module."""
        raw_config = self._parent._get_raw_config(self.key)
        if raw_config is None:
            return self.default
        else:
            processed = self.process_value(raw_config)
            validated = self.validate_value(processed)
            return validated if validated is not None else self.default

    def get_display(self) -> str:
        """Get the display name for the current value."""
        value = self.get_value()
        ret = ""
        if isinstance(value, list):
            ret = ', '.join([str(self.candidate_display(v)) for v in value])
        else:
            ret = str(self.candidate_display(value))
        if self.short_display and len(ret) > 15:
            ret = ret[:15] + '...'
        return ret

    def get_raw_value(self):
        """Get the current value from the parent module."""
        return self._parent._get_raw_config(self.key)
    
    def process_value(self, value):
        """Process the raw value retrieved from storage."""
        # Base implementation that can be overridden
        return value
    
    def validate_value(self, value):
        """Validate the value against the constraints of this configuration."""
        # Base implementation with no constraints
        return value if value in self.candidates else None
    
    async def do_check(self, client: Optional[pcrclient] = None) -> Tuple[bool, str]:
        """Check if this configuration meets certain conditions."""
        return True, ""

    def wrap_init(self, cls: Type, sself: Type):
        """Wrap the class's __init__ method to set the config instance."""
        if not hasattr(cls, 'config'):
            cls.config = {}
        sself._parent = cls
        cls.config[self.key] = sself
    
    def __call__(self, cls):
        """Make the Config instance callable for use as a decorator."""
        return _wrap_init(cls, lambda cls: self.wrap_init(cls, copy(self)))

class BoolConfig(Config):
    @property
    def config_type(self):
        return 'bool'
    
    def __init__(self, key: str, desc: str, default: bool):
        # For Bool, we provide display values for true/false
        super().__init__(key, desc, default, [True, False])

    def candidate_display(self, candidate: bool) -> str:
        if candidate:
            return "开启"
        else:
            return "关闭"


    def get_value(self) -> bool:
        return bool(super().get_value())

class IntConfig(Config):
    @property
    def config_type(self):
        return 'int'

    def get_value(self) -> int:
        return int(super().get_value())

class SingleChoiceConfig(Config):
    @property
    def config_type(self):
        return 'single'

    @property
    def default(self):
        """Get the default value for this configuration."""
        if callable(self._default):
            return self._default()
        elif not self._default and callable(self._candidates) and self._candidates():
            return self._candidates()[0]
        else:
            return self._default

class MultiChoiceConfig(Config):
    @property
    def config_type(self):
        return 'multi'
    
    def process_value(self, value):
        if not isinstance(value, list):
            return [value]
        return value
    
    def validate_value(self, value: List):
        if value:
            return [v for v in value if v in self.candidates] or None
        else:
            return []

class TimeConfig(Config):
    @property
    def config_type(self):
        return 'time'

    def __init__(self, key: str, desc: str, default: str):
        super().__init__(key, desc, default, [])

    def process_value(self, value):
        if isinstance(value, str):
            return value.split(':')
        return value

    def validate_value(self, value):
        if not isinstance(value, list):
            return None
        if len(value) < 2:
            return None
        if len(value) > 2:
            value = value[:2]
        try:
            hour, minute = map(int, value)
            if 0 <= hour < 24 and 0 <= minute < 60:
                return value
        except ValueError:
            pass
        return None
        
    def get_value(self) -> str:
        """返回格式化的时间字符串 'HH:MM'"""
        value = super().get_value()
        if isinstance(value, list) and len(value) >= 2:
            return f"{value[0]}:{value[1]}"
        return self.default

class TextConfig(Config):
    @property
    def config_type(self):
        return 'text'

    def __init__(self, key: str, desc: str, default: str):
        super().__init__(key, desc, default, [])

    def process_value(self, value):
        return value

    def validate_value(self, value):
        return value

class UnitConfigMixin:
    def candidate_display(self, unit_id: int):
        return db.get_unit_name(unit_id)

    def candidate_tag(self, unit_id: int):
        return CHARA_NAME.get(unit_id // 100, [])

class UnitChoiceConfig(UnitConfigMixin, SingleChoiceConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, 100101, db.unlock_unit_condition)

    def process_value(self, value):
        if isinstance(value, str) and ':' in value: # Compatible with the old version
            value = int(value.split(':')[0])
        return value

class MultiSearchConfig(MultiChoiceConfig):
    @property
    def config_type(self):
        return 'multi_search'

class EquipListConfig(MultiSearchConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, [], db.equip_candidate(), short_display=True)

    def candidate_display(self, equip_id: int):
        return db.get_equip_name(equip_id)

class UnitListConfig(UnitConfigMixin, MultiSearchConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, [], db.unlock_unit_condition_candidate, short_display=True)

class LimitUnitListConfig(UnitConfigMixin, MultiSearchConfig):
    def __init__(self, key: str, desc: str):
        super().__init__(key, desc, [], db.limit_unit_condition_candidate, short_display=True)

class ConditionalExecutionWrapper(Config):
    def __init__(self, key: str, desc: str, default: Any, candidates: Union[Callable, List], check: bool):
        super().__init__(key, desc, default, candidates)
        self.check_enabled = check

    async def do_check(self, client: Union[pcrclient, None] = None) -> Tuple[bool, str]: ...

    def wrap_init(self, cls: Type, sself: Type):
        super().wrap_init(cls, sself)
        if sself.check_enabled and hasattr(cls, 'do_check'):
            old_do_check = cls.do_check

            async def new_do_check(*args, **kwargs):
                ok, msg = await old_do_check(*args, **kwargs)
                if not ok:
                    return False, msg

                ok, msg2 = await sself.do_check(*args, **kwargs)
                if not ok:
                    return False, msg + msg2
                return True, msg + msg2

            cls.do_check = new_do_check

class ConditionalExecutionClient(ConditionalExecutionWrapper):
    async def do_check(self, client: pcrclient) -> Tuple[bool, str]:
        run_time = self.get_value()
        hit = [campaign for campaign in run_time if client.data.is_campaign(campaign)]
        if hit:
            return True, "今日" + ','.join(hit) + "，执行"
        return False, "今日不符合执行条件"

class ConditionalExecutionDB(ConditionalExecutionWrapper, MultiChoiceConfig):
    async def do_check(self) -> Tuple[bool, str]:
        run_time = self.get_value()
        hit = [campaign for campaign in run_time if db.is_campaign(campaign)]
        if hit:
            return True, "今日" + ','.join(hit) + "，执行"
        return False, "今日不符合执行条件"

class ConditionalNotExecutionClient(ConditionalExecutionWrapper):
    async def do_check(self, client: pcrclient) -> Tuple[bool, str]:
        run_time = self.get_value()
        hit = [campaign for campaign in run_time if client.data.is_campaign(campaign)]
        if hit:
            return False, "今日" + ','.join(hit) + "，不执行"
        return True, ""

class ConditionalExecution1Config(ConditionalExecutionClient, MultiChoiceConfig):
    def __init__(self, key: str, desc: str = "执行条件", default=[], check: bool = True):
        super().__init__(key, desc, default, ['无庆典', 'n庆典', 'h庆典', 'vh庆典', '总是执行'], check)

class ConditionalExecution2Config(ConditionalExecutionDB, MultiChoiceConfig):
    def __init__(self, key: str, desc: str = "执行条件", default=[], check: bool = True):
        super().__init__(key, desc, default, ['n3以上前夕', 'n3以上首日午前', 'h3以上前夕', '会战前夕', '会战期间', '总是执行'], check)

class ConditionalExecution3Config(ConditionalExecutionClient, MultiChoiceConfig):
    def __init__(self, key: str, desc: str = "执行条件", default=[], check: bool = True):
        super().__init__(key, desc, default, ['n2', 'n3', 'n4及以上', 'h2', 'h3及以上', 'vh2', 'vh3及以上', '总是执行'], check)

class ConditionalNotExecutionConfig(ConditionalNotExecutionClient, MultiChoiceConfig):
    def __init__(self, key: str, desc: str = "不执行条件", default=[], check: bool = True):
        super().__init__(key, desc, default, ['n2', 'n3', 'n4及以上', 'h2', 'h3及以上', 'vh2', 'vh3及以上'], check)

class TravelQuestConfig(MultiChoiceConfig):
    """Configuration for travel quests."""
    
    def __init__(self, key: str, desc: str, default: List):
        super().__init__(key, desc, default, db.travel_quest_data)

    def candidate_display(self, quest_id: int):
        if quest_id not in db.travel_quest_data:
            return str(quest_id)
        quest = db.travel_quest_data[quest_id]
        return f"{quest.travel_area_id % 10}-{quest.travel_quest_id % 10}"

    def process_value(self, value: List):
        for i in range(len(value)):
            if isinstance(value[i], str) and '-' in value[i]: # Compatible with the old version
                area_id, quest_id = map(int, value[i].split('-'))
                value[i] = 11000000 + area_id * 1000 + quest_id
        return value

class LastNormalQuestConfig(MultiChoiceConfig):
    """Configuration for last normal quests."""
    
    def __init__(self, key: str, desc: str, default: List):
        super().__init__(key, desc, default, db.last_normal_quest)

    def candidate_display(self, quest_id: int):
        area = quest_id // 1000 % 1000
        quest = quest_id % 1000
        return f"{area}-{quest}"

    def process_value(self, value):
        if isinstance(value, str) and ':' in value: # Compatible with the old version
            quest_id = int(value.split(':')[0])
            value = quest_id
        return value

class ActiveHatsuneChoiceConfig(SingleChoiceConfig):
    """Configuration for active Hatsune."""
    
    def __init__(self, key: str, desc: str, default: str):
        super().__init__(key, desc, default, db.get_active_hatsune_id)

    def candidate_display(self, event_id: int):
        return db.event_name[event_id] if event_id in db.event_name else str(event_id)

    def process_value(self, value):
        if isinstance(value, str) and ':' in value: # Compatible with the old version
            event_id = int(value.split(':')[0])
            value = event_id
        return value

class ActiveHatsuneListConfig(MultiChoiceConfig):
    """Configuration for active Hatsune list."""
    
    def __init__(self, key: str, desc: str, default: List):
        super().__init__(key, desc, default, db.get_active_hatsune_id)

    def candidate_display(self, event_id: int):
        return db.event_name[event_id] if event_id in db.event_name else str(event_id)

    def process_value(self, value: List):
        ret = []
        for v in value:
            if isinstance(v, str) and ':' in value: # Compatible with the old version
                event_id = int(v.split(':')[0])
                v = event_id
            ret.append(v)
        return ret

class TalentConfig(MultiChoiceConfig):
    """Configuration for talent quests."""
    
    def __init__(self, key: str, desc: str, default: List):
        super().__init__(key, desc, default, db.talents)

    def candidate_display(self, talent_id: int):
        return db.talents[talent_id].talent_name

# Compatible with the old version
def booltype(key: str, desc: str, default: bool):
    return BoolConfig(key, desc, default)

def inttype(key: str, desc: str, default: int, candidates: Union[List, Callable]):
    return IntConfig(key, desc, default, candidates)

def singlechoice(key: str, desc: str, default, candidates: Union[List, Callable]):
    return SingleChoiceConfig(key, desc, default, candidates)

def multichoice(key: str, desc: str, default, candidates: Union[List, Callable]):
    return MultiChoiceConfig(key, desc, default, candidates)

def timetype(key: str, desc: str, default):
    return TimeConfig(key, desc, default)

def texttype(key: str, desc: str, default):
    return TextConfig(key, desc, default)

def unitchoice(key: str, desc: str):
    return UnitChoiceConfig(key, desc)

def unitlist(key: str, desc: str):
    return UnitListConfig(key, desc)

def conditional_execution1(key: str, default=None, desc: str = "执行条件", check: bool = True):
    return ConditionalExecution1Config(key, desc, default, check)

def conditional_execution2(key: str, default=None, desc: str = "执行条件", check: bool = True):
    return ConditionalExecution2Config(key, desc, default, check)

def conditional_not_execution(key: str, default=None, desc: str = "不执行条件", check: bool = True):
    return ConditionalNotExecutionConfig(key, desc, default, check)
