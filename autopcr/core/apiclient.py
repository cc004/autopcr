from .base import Container
from ..model.modelbase import *
from asyncio import Lock
from typing import Tuple, TypeVar
from msgpack import packb, unpackb
from ..util import aiorequests
from random import randint
from json import loads
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from ..util.serializer import dump, load
import json
from enum import Enum

version = "4.9.6"

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

class CuteResultCode(Enum):
    API_RESULT_SUCCESS_CODE = 1
    RESULT_CODE_MAINTENANCE_COMMON = 101
    RESULT_CODE_SERVER_ERROR = 102
    API_RESULT_SESSION_ERROR = 201
    RESULT_CODE_ACCOUNT_BLOCK_ERROR = 203
    API_RESULT_VERSION_ERROR = 204
    RESULT_CODE_PROCESSED_ERROR = 213
    RESULT_CODE_DMM_ONETIMETOKEN_EXPIRED = 318
    API_RESULT_APPRES_VERSION_ERROR = 217
    API_RESULT_REQUEST_DECODE_ERROR = 218
    API_RESULT_RESPONSE_DECODE_ERROR = 219
    RESULT_CODE_MAINTENANCE_FROM = 2700
    RESULT_CODE_MAINTENANCE_TO = 2999
    

class ApiException(Exception):

    def __init__(self, message, status, result_code):
        super().__init__(message)
        self.status = status
        self.result_code = CuteResultCode(result_code)


TResponse = TypeVar('TResponse', bound=ResponseBase)

class apiclient(Container["apiclient"]):
    server_time: int = 0
    viewer_id: int = 0
    urlroot: str = 'http://l3-prod-all-gs-gzlj.bilibiligame.net/'
    _requestid: str = ''
    _sessionid: str=  ''
    def __init__(self):
        super().__init__()
        self._headers = {}
        for key in defaultHeaders.keys():
            self._headers[key] = defaultHeaders[key]
    
    @property
    def name(self) -> str:
        return 'undefined'

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

        response = await (await aiorequests.post(self.urlroot + request.url, data=apiclient._pack(dump(request), key) if request.crypted else
            str(request).encode('utf8'), headers=self._headers, timeout=10)).content

        response = apiclient._unpack(response)[0] if request.crypted else loads(response)

        cls = request.__class__.__orig_bases__[0].__args__[0]

        response: Response[cls] = load(response, Response[cls])

        
        with open('req.log', 'a') as fp:
            fp.write(f'{self.name} requested {request.__class__.__name__} at /{request.url}\n')
            fp.write(json.dumps(dump(request), indent=4, ensure_ascii=False) + '\n')
            fp.write(json.dumps(dump(response), indent=4, ensure_ascii=False) + '\n')
        
        
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
            raise ApiException(response.data.server_error.message,
                response.data.server_error.status,
                response.data_headers.result_code
            )
        return response.data

    _lck: Lock = Lock()
    async def _request(self, request: Request[TResponse]) -> TResponse:
        async with self._lck:
            return await self._request_internal(request)
