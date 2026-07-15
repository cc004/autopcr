from re import search

from ..model.error import PanicError

from .base import Container
from ..model.modelbase import *
from asyncio import Lock
from typing import Tuple, TypeVar
from msgpack import packb, unpackb
from ..util import aiorequests, freqlimiter
from random import randint
from json import loads
from hashlib import md5, sha1
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
        self._sdk = sdk
        self._headers = sdk.header()
        self.servers = list(getattr(sdk, 'apiroots', [sdk.apiroot]))
        if sdk.initial_uid is not None:
            self.viewer_id = int(sdk.initial_uid)
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
    def _encrypt(data: bytes, key: bytes,
                 iv: bytes = b'7Fk9Lm3Np8Qr4Sv2') -> bytes:
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.encrypt(apiclient._add_to_16(data)) + key
    @staticmethod
    def _decrypt(data: bytes,
                 iv: bytes = b'7Fk9Lm3Np8Qr4Sv2') -> Tuple[bytes, bytes]:
        data = b64decode(data.decode('utf8'))
        aes = AES.new(data[-32:], AES.MODE_CBC, iv)
        return aes.decrypt(data[:-32]), data[-32:]

    @staticmethod
    def _pack(data: object, key: bytes,
              iv: bytes = b'7Fk9Lm3Np8Qr4Sv2') -> bytes:
        return apiclient._encrypt(packb(data, use_bin_type=False), key, iv)
    @staticmethod
    def _unpack(data: bytes, iv: bytes = b'7Fk9Lm3Np8Qr4Sv2'):
        dec, key = apiclient._decrypt(data, iv)
        return unpackb(dec[:-dec[-1]], strict_map_key=False), key

    @property
    def _request_iv(self) -> bytes:
        if self._sdk.is_tw:
            return self._sdk.udid.replace('-', '')[:16].encode('utf-8')
        return b'7Fk9Lm3Np8Qr4Sv2'

    @staticmethod
    def _encode_short_udid(short_udid: str) -> str:
        alphabet = '0123456789'
        body = []
        for char in short_udid:
            encoded = [alphabet[randint(0, 9)] for _ in range(4)]
            encoded[2] = chr(ord(char) + 10)
            body.extend(encoded)
        tail = ''.join(alphabet[randint(0, 9)] for _ in range(32))
        return f'{len(short_udid):04x}' + ''.join(body) + tail

    def _prepare_request(self, request: Request[TResponse], key: bytes) -> bytes:
        """Serialize a request and update transport-specific dynamic headers."""
        if not self._sdk.is_tw:
            request.viewer_id = (
                b64encode(apiclient._encrypt(
                    str(self.viewer_id).encode('utf8'), key
                )).decode('ascii')
                if request.crypted else str(self.viewer_id)
            )
            return (
                apiclient._pack(request.dict(by_alias=True), key)
                if request.crypted
                else request.json(by_alias=True).encode('utf8')
            )

        payload = request.dict(by_alias=True, exclude_none=True)
        viewer_id = str(self.viewer_id or self._sdk.viewer_id)
        payload['viewer_id'] = b64encode(
            apiclient._encrypt(viewer_id.encode('utf-8'), key, self._request_iv)
        ).decode('ascii')
        payload['tw_server_id'] = str(self._sdk.server_id)

        packed = packb(payload, use_bin_type=False)
        api_path = '/' + request.url.lstrip('/')
        param = (
            self._sdk.udid
            + api_path
            + b64encode(packed).decode('ascii')
            + viewer_id
        )
        self._headers['PARAM'] = sha1(param.encode('utf-8')).hexdigest()
        self._headers['SHORT-UDID'] = self._encode_short_udid(
            self._sdk.short_udid
        )
        return apiclient._encrypt(packed, key, self._request_iv)

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

    @staticmethod
    def _safe_for_log(obj):
        """Redact reusable TW session identifiers from diagnostic output."""
        if isinstance(obj, dict):
            redacted = {}
            for key, value in obj.items():
                normalized = str(key).lower().replace('_', '-')
                if normalized in {
                    'access-key', 'authorization', 'challenge', 'cookie',
                    'device-id', 'param', 'password', 'seccode',
                    'set-cookie', 'short-udid', 'sid', 'token', 'udid',
                    'validate', 'viewer-id',
                }:
                    redacted[key] = '<redacted>'
                else:
                    redacted[key] = apiclient._safe_for_log(value)
            return redacted
        if isinstance(obj, list):
            return [apiclient._safe_for_log(value) for value in obj]
        return obj

    @freqlimiter.RunningLimiter(MAX_API_RUNNING)
    async def _request_internal(self, request: Request[TResponse]) -> TResponse:
        if not request: return None
        logger.info(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}')
        key = apiclient._createkey()
        urlroot = self.servers[self.active_server]
        request_data = self._prepare_request(request, key)

        try:
            url = urlroot.rstrip('/') + '/' + request.url.lstrip('/')
            transport_options = {}
            if (
                self._sdk.is_tw
                and not getattr(self._sdk, 'use_system_proxy', False)
            ):
                # requests also reads the Windows Internet Settings proxy.  A
                # stale local proxy must not prevent TW direct connections (or
                # receive reusable game-session traffic).  Users who require a
                # system proxy can opt in explicitly.
                transport_options['proxies'] = {'http': '', 'https': ''}
            resp = await aiorequests.post(
                url,
                data=request_data,
                headers=self._headers,
                timeout=10,
                **transport_options,
            )

            if resp.status_code != 200:
                raise NetworkException

            response0 = await resp.content
            apiclient._local_time = time.time()

            response0 = (
                apiclient._unpack(response0, self._request_iv)[0]
                if self._sdk.is_tw or request.crypted else loads(response0)
            )
        except Exception as ex:
            self.active_server = (self.active_server + 1) % len(self.servers)
            raise NetworkException from ex

        cls = request.__class__.__orig_bases__[0].__args__[0]

        response1 = apiclient._no_null_key(response0)

        if DEBUG_LOG:
            with open('req.log', 'a') as fp:
                fp.write(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}\n')
                fp.write(json.dumps(apiclient._safe_for_log(self._headers), indent=4, ensure_ascii=False) + '\n')
                fp.write(json.dumps(apiclient._safe_for_log(json.loads(request.json(by_alias=True))), indent=4, ensure_ascii=False) + '\n')
                fp.write(f'response from {urlroot}\n')
                fp.write(json.dumps(apiclient._safe_for_log(dict(resp.headers)), indent=4, ensure_ascii=False) + '\n')
                fp.write(json.dumps(apiclient._safe_for_log(response0), indent=4, ensure_ascii=False) + '\n')

        response: Response[TResponse] = Response[cls].parse_obj(response1)

        # with open('req.log', 'a') as fp:
           # fp.write(f'{self.name} requested {request.__class__.__name__} at /{request.url}\n')
           # fp.write(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
           # fp.write(json.dumps(json.loads(response.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')

        if response.data_headers.servertime:
            apiclient._server_time = response.data_headers.servertime
        else:
            apiclient._server_time = apiclient._local_time
            
        if response.data_headers.sid and not self._sdk.is_tw:
            t = md5()
            t.update((response.data_headers.sid + 'c!SID!n').encode('utf8'))
            self._headers['SID'] = t.hexdigest()

        if response.data_headers.request_id and not self._sdk.is_tw:
            self._headers['REQUEST-ID'] = response.data_headers.request_id

        if response.data_headers.viewer_id:
            self.viewer_id = int(response.data_headers.viewer_id)

        if self._sdk.is_tw:
            required_res_ver = response0.get('data_headers', {}).get(
                'required_res_ver'
            )
            if required_res_ver:
                required_res_ver = str(required_res_ver)
                self._headers['RES-VER'] = (
                    required_res_ver.zfill(8)
                    if required_res_ver.isdigit()
                    else required_res_ver
                )
            # A viewer id returned during account migration changes the TW SID.
            if response.data_headers.viewer_id:
                self._headers['SID'] = md5(
                    (
                        str(self.viewer_id)
                        + self._sdk.udid
                        + 'r!I@nt8e5i='
                    ).encode('utf-8')
                ).hexdigest()

        if (not self._sdk.is_tw
            and r"source_ini/get_maintenance_status?format=json" == request.url
            and "store_url" in response0['data_headers']):
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
            logger.error(json.dumps(apiclient._safe_for_log(self._headers), indent=4, ensure_ascii=False) + '\n')
            logger.error(json.dumps(apiclient._safe_for_log(json.loads(request.json(by_alias=True))), indent=4, ensure_ascii=False) + '\n')
            logger.error(f'response from {urlroot}\n')
            logger.error(json.dumps(apiclient._safe_for_log(dict(resp.headers)), indent=4, ensure_ascii=False) + '\n')
            logger.error(json.dumps(apiclient._safe_for_log(response0), indent=4, ensure_ascii=False) + '\n')

            if response.data_headers.result_code == 203:
                raise PanicError(f"{response.data.server_error.message}")

            if not self._sdk.is_tw:
                self.active_server = (self.active_server + 1) % len(self.servers)

            if any(word in response.data.server_error.message for word in ("维护", "維護")):
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
