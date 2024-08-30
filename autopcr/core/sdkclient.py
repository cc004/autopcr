from enum import Enum
from typing import Tuple
from abc import abstractmethod
from ..sdk.validator import Validator
from ..sdk.bsgamesdk import captch
from copy import deepcopy
from ..constants import DEFAULT_HEADERS, IOS_HEADERS

class platform(Enum):
    Android = 0,
    IOS = 1

class account:
    type: platform
    username: str
    password: str
    
    def __init__(self, usr: str, pwd: str, type: platform):
        self.username = usr
        self.password = pwd
        self.type = type

async def _defaultLogger(msg):
    print(msg)

class sdkclient:
    
    def __init__(self, info: account, captchaVerifier=Validator, errlogger=_defaultLogger):
        self.captchaVerifier = captchaVerifier
        self.errlogger = errlogger
        if info.type == platform.Android:
            self.platform = '2'
        elif info.type == platform.IOS:
            self.platform = '1000'
        else:
            raise ValueError(f"Invalid platform {info.type}")
        self._account = info
    '''
    returns: uid, access_key
    '''
    @abstractmethod
    async def login(self) -> Tuple[str, str]: ...

    async def do_captcha(self):                                
        cap = await captch()
        return await self.captchaVerifier(self.account, cap['gt'], cap['challenge'], cap['gt_user_id'])
    
    def header(self):
        if self._account.type == platform.Android:
            headers = deepcopy(DEFAULT_HEADERS)
        elif self._account.type == platform.IOS:
            headers = deepcopy(IOS_HEADERS)
        else:
            raise ValueError(f"Invalid platform {self._account.type}")
        
        headers['RES-KEY'] = self.reskey
        headers['PLATFORM'] = self.platform
        headers['PLATFORM-ID'] = self.platform_id
        headers['CHANNEL-ID'] = self.channel
        
        return headers

    @property
    @abstractmethod
    def apiroot(self) -> str: ...
    
    @property
    @abstractmethod
    def platform_id(self) -> str: ...
    
    @property
    def channel(self):
        return '1'
    
    @property
    def account(self):
        return self._account.username
    
    @property
    @abstractmethod
    def reskey(self) -> str: ...
    
