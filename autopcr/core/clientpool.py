from .pcrclient import pcrclient
from .apiclient import apiclient, ApiException
from .sdkclient import sdkclient
from .datamgr import datamgr
from .sessionmgr import sessionmgr
from ..model.error import PanicError
from .misc import errorhandler, mutexhandler
from .base import Component, Request, TResponse, RequestHandler
from ..model.sdkrequests import ToolSdkLoginRequest
from typing import Dict, Tuple, Set
from ..constants import SESSION_ERROR_MAX_RETRY, CLIENT_POOL_SIZE_MAX, CLINET_POOL_MAX_AGE
import time

class PreRequestHandler(Component[apiclient]):
    def __init__(self, pool: 'ClientPool'):
        self.pool = pool
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        assert isinstance(self._container, PoolClientWrapper)
        self._container.last_access = int(time.time())
        if isinstance(request, ToolSdkLoginRequest):
            self._container.uid = request.uid
            self.pool._on_sdk_login(self._container)
        return await next.request(request)

class SessionErrorHandler(Component[apiclient]):
    def __init__(self, pool: 'ClientPool'):
        self.pool = pool
        self.retry = 0
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        assert isinstance(self._container, PoolClientWrapper)
        try:
            return await next.request(request)
        except ApiException as e:
            if e.result_code == 6002 and self.retry < SESSION_ERROR_MAX_RETRY:
                self.retry += 1
                await self._container.session.clear_session()
                return await self.request(request, next)
            raise
        finally:
            self.retry = 0

class PoolClientWrapper(pcrclient):
    def __init__(self, pool: 'ClientPool', sdk: sdkclient):
        apiclient.__init__(self, sdk)
        self._base_keys = {}
        self._keys = {}
        self.data = datamgr()
        self.session = sessionmgr(sdk)
        self.pool = pool
        self.uid: str = None
        self.last_access = int(time.time())
        self.register(errorhandler())
        self.register(self.data)
        self.register(PreRequestHandler(pool))
        self.register(self.session)
        self.register(SessionErrorHandler(pool))
        self.register(mutexhandler())

    async def __aenter__(self):
        self._base_keys = {}
        self._keys = {}
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.pool._put_in_pool(self)

class ClientPool:
    def __init__(self):
        self.active_uids: Dict[str, int] = dict()
        self._pool: Dict[Tuple[str, str], PoolClientWrapper] = dict()

    def _on_sdk_login(self, client: PoolClientWrapper):
        client_key = id(client)
        if self.active_uids.get(client.uid, client_key) != client_key:
            raise PanicError('用户的另一项请求正在进行中')
        self.active_uids[client.uid] = client_key

    def _put_in_pool(self, client: PoolClientWrapper):
        if self.active_uids.get(client.uid, -1) != client.uid:
            # client disposed without being activated
            return
        self.active_uids.pop(client.uid)
        if not client.logged: # client session expired and not successfully recovered
            return
        
        pool_key = (client.session.sdk.account, type(client.session.sdk).__name__)
        # remove old client from pool, which session has been overrided by self.
        # removed here to save one client pool slot.
        self._pool.pop(pool_key, None) 

        if len(self._pool) >= CLIENT_POOL_SIZE_MAX:
            now = int(time.time())
            while self._pool:
                k, v = next(iter(self._pool.items()))
                if v.last_access + CLINET_POOL_MAX_AGE < now:
                    self._pool.pop(k)
                else:
                    break

        if len(self._pool) < CLIENT_POOL_SIZE_MAX:
            self._pool[pool_key] = client

    '''
    returns a client from the pool if available, otherwise creates a new one
    client.session.sdk is always set to the provided sdk
    '''
    def get_client(self, sdk: sdkclient) -> PoolClientWrapper:
        pool_key = (sdk.account, type(sdk).__name__)
        if pool_key in self._pool:
            client = self._pool.pop(pool_key)
            # no need to check for last password used, as the client is already logged in, when the session expires, the client will use the new sdk to re-login
            # assert item.client.uid not in self.active_uids
            # Sessions of any clients in pool which are active should be expired and imply a uid conflict.
            self._on_sdk_login(client)
            client.session.sdk = sdk
            return client
        return PoolClientWrapper(self, sdk)
        

instance = ClientPool()