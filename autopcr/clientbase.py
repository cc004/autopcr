from asyncio import Lock
from traceback import print_exc
from typing import Dict, Set, Tuple, TypeVar

from torch import os
from msgpack import packb, unpackb
from .aiorequests import post
from random import randint
from json import loads
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from .bsgamesdk import login
from asyncio import sleep
from re import search
from datetime import datetime
from dateutil.parser import parse
from .serializer import dump, load
import json
from .requests import *
from .sdkrequests import *
from os.path import dirname, join, exists

curpath = dirname(__file__)
config = join(curpath, 'version.txt')
version = "4.9.6"
if exists(config):
    with open(config, encoding='utf-8') as fp:
        version = fp.read().strip()

defaultHeaders = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux, U, Android 5.1.1, PCRT00 Build/LMY48Z)',
    'X-Unity-Version': '2018.4.30f1',
    'APP-VER': version,
    'BATTLE-LOGIC-VERSION': '4',
    'BUNDLE-VER': '',
    'DEVICE': '2',
    'DEVICE-ID': '7b1703a5d9b394e24051d7a5d4818f17',
    'DEVICE-NAME': 'OPPO PCRT00',
    'EXCEL-VER': '1.0.0',
    'GRAPHICS-DEVICE-NAME': 'Adreno (TM) 640',
    'IP-ADDRESS': '10.0.2.15',
    'KEYCHAIN': '',
    'LOCALE': 'CN',
    'PLATFORM-OS-VERSION': 'Android OS 5.1.1 / API-22 (LMY48Z/rel.se.infra.20200612.100533)',
    'REGION-CODE': '',
    'RES-KEY': 'ab00a0a6dd915a052a2ef7fd649083e5',
    'RES-VER': '10002200',
    'SHORT-UDID': '0'
}


class ApiException(Exception):

    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class bsdkclient:
    '''
        acccountinfo = {
            'account': '',
            'password': '',
            'platform': 2, # indicates android platform
            'channel': 1, # indicates bilibili channel
        }
    '''

    def __init__(self, acccountinfo, captchaVerifier, errlogger):
        self.account = acccountinfo['account']
        self.pwd = acccountinfo['password']
        self.platform = acccountinfo['platform']
        self.channel = acccountinfo['channel']
        self.captchaVerifier = captchaVerifier
        self.errlogger = errlogger

    async def login(self):
        while True:
            resp = await login(self.account, self.pwd, self.captchaVerifier)
            if resp['code'] == 0:
                await self.errlogger("geetest or captcha succeed")
                break
            await self.errlogger(resp['message'])

        return resp['uid'], resp['access_key']

TResponse = TypeVar('TResponse', bound=ResponseBase)
class apiclient:
    server_time: int = 0
    dungeon_area_id: int = 0
    viewer_id: int = 0
    urlroot: str = 'http://l3-prod-all-gs-gzlj.bilibiligame.net/'
    _requestid: str = ''
    _sessionid: str=  ''
    def __init__(self):
        self._headers = {}
        for key in defaultHeaders.keys():
            self._headers[key] = defaultHeaders[key]
    
    @staticmethod
    def _createkey() -> bytes:
        return bytes([ord('0123456789abcdef'[randint(0, 15)]) for _ in range(32)])
    @staticmethod
    def _add_to_16(b: bytes) -> bytes:
        n = len(b) % 16
        n = n // 16 * 16 - n + 16
        return b + (n * bytes([n]))

    @staticmethod
    def _encrypt(data: bytes, key: bytes) -> bytes:
        aes = AES.new(key, AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        return aes.encrypt(apiclient._add_to_16(data)) + key
    @staticmethod
    def _decrypt(data: bytes) -> Tuple[bytes, bytes]:
        data = b64decode(data.decode('utf8'))
        aes = AES.new(data[-32:], AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        return aes.decrypt(data[:-32]), data[-32:]

    @staticmethod
    def _pack(data: object, key: bytes) -> bytes:
        return apiclient._encrypt(packb(data, use_bin_type=False), key)
    @staticmethod
    def _unpack(data: bytes):
        dec, key = apiclient._decrypt(data)
        return unpackb(dec[:-dec[-1]], strict_map_key=False), key


    async def _request_internal(self, request: Request[TResponse]) -> TResponse:
        if not request: return None
        print(f'{self.name} requested {request.__class__.__name__} at /{request.url}')
        key = apiclient._createkey()
        request.viewer_id = b64encode(apiclient._encrypt(str(self.viewer_id).encode('utf8'), key)).decode('ascii') if request.crypted else str(self.viewer_id)

        response = await (await post(self.urlroot + request.url, data=apiclient._pack(dump(request), key) if request.crypted else
            str(request).encode('utf8'), headers=self._headers, timeout=10)).content

        response = apiclient._unpack(response)[0] if request.crypted else loads(response)

        cls = request.__class__.__orig_bases__[0].__args__[0]

        response: Response[cls] = load(response, Response[cls])

        if response.data_headers.servertime:
            self.server_time = response.data_headers.servertime

        if response.data_headers.sid:
            t = md5()
            t.update((response.data_headers.sid + 'c!SID!n').encode('utf8'))
            self._headers['SID'] = t.hexdigest()

        if response.data_headers.request_id:
            self._headers['REQUEST-ID'] = response.data_headers.request_id

        if response.data_headers.viewer_id:
            self.viewer_id = int(response.data_headers.viewer_id)
        # 傻逼python这个类型提示都做不出来？
        if response.data.server_error:
            print(f'pcrclient: /{request.url} api failed {response.data.server_error}')
            raise ApiException(response.data.server_error.message, response.data.server_error.status)
        return response.data

    _lck: Lock = Lock()

    async def _request(self, request: Request[TResponse]) -> TResponse:
        while True:
            try:
                async with self._lck:
                    return await self._request_internal(request)
            except ApiException:
                raise
            except Exception:
                print_exc()

    async def prepare(self) -> SourceIniGetMaintenanceStatusResponse:
        self.urlroot = f'http://{(await self._request(SourceIniIndexRequest())).server[0]}'.replace('\t', '')
        manifest = await self._request(SourceIniGetMaintenanceStatusRequest())
        self._headers['MANIFEST-VER'] = manifest.required_manifest_ver
        return manifest
    
class sessionclient(apiclient):
    @staticmethod
    async def _logger(msg): print(f'farm::{__class__}: {msg}')

    def __init__(self, account, validator):
        super().__init__()
        self.cacheDir = os.path.join(__file__, '..', 'cache')
        self.bsdk = bsdkclient(account, validator, sessionclient._logger)
        self._headers['PLATFORM'] = str(account['platform'])
        self._headers['PLATFORM-ID'] = str(account['platform'])
        self._headers['CHANNEL-ID'] = str(account['channel'])
        self._logging = False
        self._logged = False
        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)
        self.cacheFile = os.path.join(self.cacheDir, account['account'])

    async def _bililogin(self):
        uid, access_key = await self.bsdk.login()
        self._sdkaccount = {
                'uid': uid,
                'access_key': access_key
        }
        self._platform = self.bsdk.platform
        self._channel = self.bsdk.channel
        with open(self.cacheFile, 'w') as fp:
            json.dump(self._sdkaccount, fp)
    
    async def _login(self):
        self._logging = True

        if os.path.exists(self.cacheFile):
            with open(self.cacheFile, 'r') as fp:
                self._sdkaccount = json.load(fp)
        while True:
            try:
                while True:
                    manifest = await self.prepare()
                    if not manifest.maintenance_message: break
                    match = search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', manifest.maintenance_message)
                    if match is not None:
                        end = parse(match.group())
                        while datetime.now() < end:
                            await sleep(1)
                    else:
                        await sleep(60)

                while True:
                    await self._bililogin()
                    if not self._sdkaccount or not self._sdkaccount['access_key']:
                        self._sdkaccount = None
                        continue
                    req = ToolSdkLoginRequest()
                    req.uid = self._sdkaccount['uid']
                    req.access_key = self._sdkaccount['access_key']
                    req.platform = str(self._platform)
                    req.channel_id = str(self._channel)
                    if not (await self._request(req)).is_risk:
                        break
                    self._sdkaccount = None

                req = CheckGameStartRequest()
                req.apptype = 0
                req.campaign_data = ''
                req.campaign_user = randint(0, 100000) & ~1
                if (await self._request(req)).now_tutorial:
                    raise Exception("账号未过完教程")
                
                await self._request(CheckAgreementRequest())

                req = LoadIndexRequest()
                req.carrier = "OPPO"
                await self._request(req)

                req = HomeIndexRequest()
                req.message_id = 1
                req.gold_history = 0
                req.is_first = 1
                req.tips_id_list = []
                await self._request(req)

                self._logged = True
                self._logging = False
                break
            except ApiException:
                pass
    
    async def _request(self, request: Request[TResponse]) -> TResponse:
        if not self._logged and not self._logging:
            await self._login()
        try:
            return await super()._request(request)
        except ApiException:
            if self._logging:
                self._logged = False
            raise

class dataclient(sessionclient):
    settings: IniSetting = None
    dungeon_avaliable: bool = False
    finishedQuest: Set[int] = set()
    jewel: UserJewel = None
    clan: int = 0
    donation_num: int = 0
    team_level: int = 0
    stamina: int = 0
    recover_stamina_exec_count: int = 0
    training_quest_count: TrainingQuestCount = None
    quest_dict: Dict[int, UserQuestInfo] = None
    name: str = None
    clan_like_count: int = 0
    user_my_quest: List[UserMyQuest] = None
    _inventory: Dict[Tuple[eInventoryType, int], int] = {}

    def clear_inventory(self):
        self._inventory.clear()

    def update_inventory(self, item: InventoryInfo):
        self._inventory[(item.type, item.id)] = item.stock

    def get_inventory(self, item: Tuple[eInventoryType, int]):
        return self._inventory.get(item, 0)

    def set_inventory(self, item: Tuple[eInventoryType, int], value: int):
        self._inventory[item] = value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def _request(self, request: Request[TResponse]) -> TResponse:
        resp = await super()._request(request)
        if resp: resp.update(self, request)
        return resp
