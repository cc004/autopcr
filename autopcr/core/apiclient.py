from re import search

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
from traceback import print_exc
from ..constants import DEFAULT_HEADERS, IOS_HEADERS, refresh_headers

import json
from enum import Enum

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
        try:
            self.result_code = CuteResultCode(result_code)
        except ValueError:
            self.result_code = result_code

class NetworkException(Exception):
    pass

TResponse = TypeVar('TResponse', bound=ResponseBase, covariant=True)

class apiclient(Container["apiclient"]):
    server_time: int = 0
    viewer_id: int = 0
    servers: list = ['https://l3-prod-all-gs-gzlj.bilibiligame.net/']
    active_server: int = 0
    _requestid: str = ''
    _sessionid: str=  ''
    def __init__(self, account):
        super().__init__()
        self._headers = {}
        platform = account['platform']
        if platform == 2:
            for key in DEFAULT_HEADERS.keys():
                self._headers[key] = DEFAULT_HEADERS[key]
        else:
            for key in IOS_HEADERS.keys():
                self._headers[key] = IOS_HEADERS[key]
        self._lck = Lock()

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

    @staticmethod
    def _no_null_key(obj):
        if type(obj) == dict:
            if None in obj and not [1 for k in obj if type(k) is not int and k is not None]:
                return [apiclient._no_null_key(v1) for k1, v1 in sorted(((k, v) for k, v in obj.items() if k is not None), key=lambda x: x[0])]
            return {k: apiclient._no_null_key(v) for k, v in obj.items() if k is not None}
        elif type(obj) == list:
            return [apiclient._no_null_key(v) for v in obj]
        else:
            return obj

    async def _request_internal(self, request: Request[TResponse]) -> TResponse:
        if not request: return None
        print(f'{self.name} requested {request.__class__.__name__} at /{request.url}')
        key = apiclient._createkey()
        request.viewer_id = b64encode(apiclient._encrypt(str(self.viewer_id).encode('utf8'), key)).decode('ascii') if request.crypted else str(self.viewer_id)

        urlroot = self.servers[self.active_server]
        
        try:
            resp = await aiorequests.post(urlroot + request.url, data=apiclient._pack(request.dict(by_alias=True), key) if request.crypted else
                request.json(by_alias=True).encode('utf8'), headers=self._headers, timeout=10)

            if resp.status_code != 200:
                raise NetworkException

            response0 = await resp.content

            response0 = apiclient._unpack(response0)[0] if request.crypted else loads(response0)
        except:
            raise NetworkException

        cls = request.__class__.__orig_bases__[0].__args__[0]

        response1 = apiclient._no_null_key(response0)

        # with open('req.log', 'a') as fp:
        #     fp.write(json.dumps(response0))
        #     fp.write("\n-------\n")
        #     fp.write(json.dumps(response1))

        response: Response[TResponse] = Response[cls].parse_obj(response1)

        # with open('req.log', 'a') as fp:
           # fp.write(f'{self.name} requested {request.__class__.__name__} at /{request.url}\n')
           # fp.write(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
           # fp.write(json.dumps(json.loads(response.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')

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

        if "check/game_start" == request.url and "store_url" in response0['data_headers']:
            version = search(r'_v?([4-9]\.\d\.\d).*?_', response0['data_headers']["store_url"]).group(1)
            self._headers['APP-VER'] = version
            refresh_headers(version)
            print(f"版本已更新至{version}")
            raise ApiException(f"版本已更新:{version}",
                               response.data.server_error.status,
                               response.data_headers.result_code
                               )


        if response.data.server_error and "维护" not in response.data.server_error.message:
            print(f'pcrclient: /{request.url} api failed {response.data.server_error}')

            with open('error.log', 'a') as fp:
               fp.write(f'{self.name} requested {request.__class__.__name__} at /{request.url}\n')
               fp.write(json.dumps(self._headers, indent=4, ensure_ascii=False) + '\n')
               fp.write(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
               fp.write(json.dumps(json.loads(response.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')

            raise ApiException(response.data.server_error.message,
                response.data.server_error.status,
                response.data_headers.result_code
            )
        return response.data

    async def request(self, request: Request[TResponse]) -> TResponse:
        async with self._lck:
            return await self._request_internal(request)
