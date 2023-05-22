import traceback
from .base import Component
from .apiclient import apiclient, ApiException, CuteResultCode
from ..model.modelbase import *
from typing import Callable, Coroutine, Any
from traceback import print_exc
from pydantic.error_wrappers import ValidationError

class errorhandler(Component[apiclient]):
    async def request(self, request: Request[TResponse], next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        while True:
            try:
                return await next(request)
            except ApiException as e:
                # print(e)
                # print_exc()
                raise
            except Exception:
                print_exc()
                raise

class ratelimiter(Component[apiclient]):
    pass

class code213handler(Component[apiclient]):
    pass

