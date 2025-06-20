from .pcrclient import pcrclient, eLoginStatus
from .apiclient import apiclient, ApiException
from .sdkclient import sdkclient
from .datamgr import datamgr
from .sessionmgr import sessionmgr
from ..model.error import PanicError
from .misc import errorhandler, mutexhandler
from .base import Component, Request, TResponse, RequestHandler
from ..model.sdkrequests import ToolSdkLoginRequest
from typing import Dict, Tuple
from ..constants import SESSION_ERROR_MAX_RETRY, CLIENT_POOL_SIZE_MAX, CLIENT_POOL_MAX_AGE, CACHE_DIR, CLIENT_POOL_MAX_CLIENT_ALIVE, CLIENT_POOL_MAX_FARMER_CLIENT_ALIVE
import time, os, asyncio, pickle
from ..util.logger import instance as logger

class ComponentWrapper(Component):
    def __init__(self, component: Component):
        self.component = component
    async def request(self, request: Request[TResponse],
        next: RequestHandler) -> TResponse:
        return await self.component.request(request, next)

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

class PreSessionHandler(Component[apiclient]):
    def __init__(self, pool: 'ClientPool'):
        self.pool = pool
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        assert isinstance(self._container, PoolClientWrapper)
        if self._container.session.is_session_expired:
            await self._container.logout()
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
            if (e.result_code == 6002 or e.result_code == 4) and self.retry < SESSION_ERROR_MAX_RETRY:
                self.retry += 1
                await self._container.logout()
                return await self.request(request, next)
            if "回到标题界面" in str(e):
                await self._container.logout()
            raise
        finally:
            self.retry = 0

class PoolClientWrapper(pcrclient):
    def __init__(self, pool: 'ClientPool', sdk: sdkclient):
        apiclient.__init__(self, sdk)
        self._base_keys = {}
        self._keys = {}
        self.data = datamgr()
        self._data_wrapper = ComponentWrapper(self.data)
        self.need_refresh = False
        self.session = sessionmgr(sdk)
        self.pool = pool
        self.uid: str = None
        self.last_access = int(time.time())
        self.register(errorhandler())
        self.register(self._data_wrapper)
        self.register(PreRequestHandler(pool))
        self.register(self.session)
        self.register(PreSessionHandler(pool))
        self.register(SessionErrorHandler(pool))
        self.register(mutexhandler())

    @property
    def logged(self) -> eLoginStatus:
        if not self.session._logged: return eLoginStatus.NOT_LOGGED
        elif self.need_refresh: return eLoginStatus.NEED_REFRESH
        else: return eLoginStatus.LOGGED

    @property
    def cache(self):
        return os.path.join(CACHE_DIR, 'pool', self.id)

    async def __aenter__(self):
        self._base_keys = {}
        self._keys = {}
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.pool._put_in_pool(self)

    async def logout(self):
        await super().logout()
        self.data = datamgr()
        self._data_wrapper.component = self.data

    async def activate(self):
        await self.pool.sema_require(self)
        try:
            if os.path.exists(self.cache):
                with open(self.cache, 'rb') as f:
                    tmp = pickle.loads(f.read())
                    if tmp.version == self.data.version:
                        self.data = tmp
                        self._data_wrapper.component = self.data
                logger.debug("Client %s data loaded", self.data.uid)
        except:
            self.dispose()

    def dispose(self):
        os.remove(self.cache)

    def deactivate(self):
        self.pool.sema_release(self)
        if self.data.ready:
            with open(self.cache, 'wb') as f:
                f.write(pickle.dumps(self.data))
            logger.debug("Client %s data saved", self.data.uid)
        self.data = datamgr()
        self._data_wrapper.component = self.data

class CountingSemaphore:
    def __init__(self, max_count):
        self._sema = asyncio.Semaphore(max_count)
        self.max_count = max_count
        self.running = 0
        self.waiting = 0

    async def acquire(self):
        self.waiting += 1
        await self._sema.acquire()
        self.waiting -= 1
        self.running += 1

    def release(self):
        self.running -= 1
        self._sema.release()

    def status(self) -> Tuple[int, int, int]:
        return self.running, self.waiting, self.max_count

class ClientPool:
    def __init__(self):
        self.active_uids: Dict[str, int] = dict()
        self._pool: Dict[Tuple[str, str], PoolClientWrapper] = dict()
        os.makedirs(os.path.join(CACHE_DIR, 'pool'), exist_ok=True)

        self._sema = CountingSemaphore(CLIENT_POOL_MAX_CLIENT_ALIVE)
        self._farm_sema = CountingSemaphore(CLIENT_POOL_MAX_FARMER_CLIENT_ALIVE)

    def _on_sdk_login(self, client: PoolClientWrapper):
        client_key = id(client)
        if self.active_uids.get(client.uid, client_key) != client_key:
            raise PanicError('用户的另一项请求正在进行中')
        self.active_uids[client.uid] = client_key

    def _put_in_pool(self, client: PoolClientWrapper):
        client_key = id(client)
        if self.active_uids.get(client.uid, -1) != client_key:
            logger.debug("Client key mismatch, discard client %s", client.uid)
            return
        self.active_uids.pop(client.uid)
        if client.logged == eLoginStatus.NOT_LOGGED: 
            logger.debug("Client %s session expired", client.uid)
            return

        pool_key = (client.session.sdk.account, type(client.session.sdk).__name__)

        if len(self._pool) >= CLIENT_POOL_SIZE_MAX:
            now = int(time.time())
            while self._pool:
                k, v = next(iter(self._pool.items()))
                if v.last_access + CLIENT_POOL_MAX_AGE < now:
                    self._pool.pop(k)
                else:
                    break

        logger.debug("Put client %s back to pool", client.uid)
        if len(self._pool) < CLIENT_POOL_SIZE_MAX:
            self._pool[pool_key] = client

    async def sema_require(self, pcrclient: PoolClientWrapper):
        if pcrclient.session.sdk._account.farm:
            await self._farm_sema.acquire()
        else:
            await self._sema.acquire()

    def sema_release(self, pcrclient: PoolClientWrapper):
        if pcrclient.session.sdk._account.farm:
            self._farm_sema.release()
        else:
            self._sema.release()

    def sema_status(self):
        return self._sema.status(), self._farm_sema.status()

    async def get_client(self, sdk: sdkclient) -> PoolClientWrapper:
        pool_key = (sdk.account, type(sdk).__name__)
        if pool_key in self._pool:
            client = self._pool.pop(pool_key)
            self._on_sdk_login(client)
            client.need_refresh = True
            client.session.sdk = sdk
        else:
            client = PoolClientWrapper(self, sdk)
        return client

instance = ClientPool()
