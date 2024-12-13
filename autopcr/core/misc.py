import traceback
from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException, NetworkException
from ..model.modelbase import *
from traceback import print_exc
from asyncio import Lock

class errorhandler(Component[apiclient]):
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        retry_cnt = 5
        while True:
            try:
                return await next.request(request)
            except NetworkException:
                if retry_cnt <= 0:
                    raise
                retry_cnt -= 1
            except ApiException:
                raise
            except Exception:
                print_exc()
                raise

class mutexhandler(Component[apiclient]):
    def __init__(self):
        self._lck = Lock()
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        async with self._lck:
            return await next.request(request)
