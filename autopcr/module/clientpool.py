from ..core.pcrclient import pcrclient
from ..core.sdkclient import platform, account
from ..sdk.sdkclients import create
from typing import Dict, Tuple
from ..constants import CLIENT_POOL_SIZE_MAX

class ClientCache:
    client: pcrclient
    password: str
    platform: platform

class ClientPool:

    def __init__(self):
        self._pool: Dict[Tuple[str, str], ClientCache] = dict()

    def get_client(self, channel: str, account: account, *args, **kwargs) -> pcrclient:
        key = (channel, account.username)
        if key in self._pool:
            cache = self._pool[key]
            if cache.platform == account.type and cache.password == account.password and cache.client.logged:
                return cache.client
            else:
                self._pool.pop(key)
        
        while len(self._pool) >= CLIENT_POOL_SIZE_MAX:
            self._pool.pop(next(iter(self._pool)))

        cache = ClientCache()
        cache.client = pcrclient(create(channel, account, *args, **kwargs))
        cache.password = account.password
        cache.platform = account.type

        self._pool[key] = cache

        return cache.client


instance = ClientPool()
