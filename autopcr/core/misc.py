from .base import Component
from .apiclient import apiclient, ApiException, CuteResultCode
from ..model.modelbase import *
from typing import Callable, Coroutine, Any
from traceback import print_exc
import asyncio

class errorhandler(Component[apiclient]):
    async def request(self, request: Request[TResponse], next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        while True:
            try:
                return await next(request)
            except ApiException as ex:
                raise
            except Exception:
                print_exc()

class ratelimiter(Component[apiclient]):
    pass

class code213handler(Component[apiclient]):
    pass

