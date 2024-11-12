from autopcr.core.pcrclient import pcrclient
from autopcr.core.sdkclient import platform, account
from autopcr.sdk.sdkclients import create
from typing import Dict, Tuple
from ..constants import CLIENT_POOL_SIZE_MAX, CLINET_POOL_MAX_AGE
import time

class ClientCache:
    client: pcrclient
    password: str
    platform: platform
    last_access: int

class ClientPool:

    def __init__(self):
        self._pool: Dict[Tuple[str, str], ClientCache] = dict()

    def get_client(self, channel: str, account: account, *args, **kwargs) -> pcrclient:
        now = int(time.time())
        key = (channel, account.username)
        if key in self._pool:
            cache = self._pool[key]
            if cache.platform == account.type and cache.password == account.password and cache.client.logged:
                cache.last_access = now
                self._pool[key] = self._pool.pop(key)
                return cache.client
            else:
                self._pool.pop(key)
        

        cache = ClientCache()
        cache.client = pcrclient(create(channel, account, *args, **kwargs))
        cache.password = account.password
        cache.platform = account.type

        if len(self._pool) >= CLIENT_POOL_SIZE_MAX:
            while True:
                k, v = next(iter(self._pool.items()))
                if v.last_access + CLINET_POOL_MAX_AGE < now:
                    self._pool.pop(k)
                else:
                    break

        if len(self._pool) < CLIENT_POOL_SIZE_MAX:
            self._pool[key] = cache

        return cache.client


instance = ClientPool()