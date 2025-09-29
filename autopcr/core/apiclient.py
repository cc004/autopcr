from re import search

from .base import Container
from ..model.modelbase import *
from asyncio import Lock
from typing import Tuple, TypeVar
from msgpack import packb, unpackb
from ..util import aiorequests, freqlimiter
from random import randint
from json import loads
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from .sdkclient import sdkclient
from ..constants import refresh_headers, DEBUG_LOG, MAX_API_RUNNING
import time, datetime
import json
from ..util.logger import instance as logger

class ApiException(Exception):

    def __init__(self, message, status, result_code):
        super().__init__(message)
        self.status = status
        self.result_code = result_code

class NetworkException(Exception):
    pass

TResponse = TypeVar('TResponse', bound=ResponseBase, covariant=True)

class staticproperty:
    def __init__(self, func):
        self.fget = func
    def __get__(self, instance, owner):
        return self.fget()

class apiclient(Container["apiclient"]):
    _server_time: int = 0
    _local_time: float = 0.0
    viewer_id: int = 0
    servers: list = [] #['https://l3-prod-all-gs-gzlj.bilibiligame.net/']
    active_server: int = 0
    _requestid: str = ''
    _sessionid: str=  ''
    def __init__(self, sdk: sdkclient):
        super().__init__()
        self._headers = sdk.header()
        self.servers = [
            sdk.apiroot
        ]
        self._lck = Lock()

    @staticproperty
    def time() -> int:
        return int(time.time() - apiclient._local_time + apiclient._server_time)
        
    @staticproperty
    def datetime() -> datetime.datetime:
        return datetime.datetime.fromtimestamp(apiclient.time)
        
    @property
    def user_name(self) -> str: ...

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

    @freqlimiter.RunningLimiter(MAX_API_RUNNING)
    async def _request_internal(self, request: Request[TResponse]) -> TResponse:
        if not request: return None
        logger.info(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}')
        key = apiclient._createkey()
        request.viewer_id = b64encode(apiclient._encrypt(str(self.viewer_id).encode('utf8'), key)).decode('ascii') if request.crypted else str(self.viewer_id)

        urlroot = self.servers[self.active_server]
        
        try:
            resp = await aiorequests.post(urlroot + request.url, data=apiclient._pack(request.dict(by_alias=True), key) if request.crypted else
                request.json(by_alias=True).encode('utf8'), headers=self._headers, timeout=10)

            if resp.status_code != 200:
                raise NetworkException

            response0 = await resp.content
            apiclient._local_time = time.time()

            response0 = apiclient._unpack(response0)[0] if request.crypted else loads(response0)
        except:
            raise NetworkException

        cls = request.__class__.__orig_bases__[0].__args__[0]

        response1 = apiclient._no_null_key(response0)

        if DEBUG_LOG:
            with open('req.log', 'a') as fp:
                fp.write(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}\n')
                fp.write(json.dumps(self._headers, indent=4, ensure_ascii=False) + '\n')
                fp.write(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
                fp.write(f'response from {urlroot}\n')
                fp.write(json.dumps(dict(resp.headers), indent=4, ensure_ascii=False) + '\n')
                fp.write(json.dumps(response0, indent=4, ensure_ascii=False) + '\n')

        response: Response[TResponse] = Response[cls].parse_obj(response1)

        # with open('req.log', 'a') as fp:
           # fp.write(f'{self.name} requested {request.__class__.__name__} at /{request.url}\n')
           # fp.write(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
           # fp.write(json.dumps(json.loads(response.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')

        if response.data_headers.servertime:
            apiclient._server_time = response.data_headers.servertime
        else:
            apiclient._server_time = apiclient._local_time
            
        if response.data_headers.sid:
            t = md5()
            t.update((response.data_headers.sid + 'c!SID!n').encode('utf8'))
            self._headers['SID'] = t.hexdigest()

        if response.data_headers.request_id:
            self._headers['REQUEST-ID'] = response.data_headers.request_id

        if response.data_headers.viewer_id:
            self.viewer_id = int(response.data_headers.viewer_id)

        if r"source_ini/get_maintenance_status?format=json" == request.url and "store_url" in response0['data_headers']:
            match = search(r'(?<=gzlj_)(\d+\.\d+\.\d+)', response0['data_headers']["store_url"])
            if not match:
                raise ValueError("无法解析版本号，请手动修改constants.py的default_ver")
            version = match.group(1)
            self._headers['APP-VER'] = version
            refresh_headers(version)
            logger.info(f"版本已更新至{version}")
            raise ApiException(f"版本已更新:{version}",
                               response.data.server_error.status,
                               response.data_headers.result_code
                               )


        if response.data and response.data.server_error:
            logger.error(f'pcrclient: /{request.url} api failed={response.data_headers.result_code} {response.data.server_error}')
            logger.error(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}\n')
            logger.error(json.dumps(self._headers, indent=4, ensure_ascii=False) + '\n')
            logger.error(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
            logger.error(f'response from {urlroot}\n')
            logger.error(json.dumps(dict(resp.headers), indent=4, ensure_ascii=False) + '\n')
            logger.error(json.dumps(response0, indent=4, ensure_ascii=False) + '\n')

            self.active_server = (self.active_server + 1) % len(self.servers)

            if "维护" in response.data.server_error.message:
                try:
                    response.data.server_error.message = response.data.maintenance_message
                except:
                    pass

            raise ApiException(response.data.server_error.message,
                response.data.server_error.status,
                response.data_headers.result_code
            )
        return response.data

    async def request(self, request: Request[TResponse]) -> TResponse:
        async with self._lck:
            return await self._request_internal(request)
