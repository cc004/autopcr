from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException, NetworkException
from ..model.modelbase import *
from ..model.error import *
from asyncio import Lock
from ..util.logger import instance as logger
from .region import set_region, reset_region

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
            except ApiException as e:
                if any(word in str(e) for word in ("维护", "維護")):
                    raise PanicError(str(e))
                raise
            except Exception:
                logger.exception("Unhandled exception in request handler")
                raise

class mutexhandler(Component[apiclient]):
    def __init__(self):
        self._lck = Lock()
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        async with self._lck:
            return await next.request(request)


class regionhandler(Component[apiclient]):
    """Keep database/profile routing attached to the current async request."""

    def __init__(self, region: str):
        self.region = region

    async def request(self, request: Request[TResponse],
                      next: RequestHandler) -> TResponse:
        token = set_region(self.region)
        try:
            return await next.request(request)
        finally:
            reset_region(token)
