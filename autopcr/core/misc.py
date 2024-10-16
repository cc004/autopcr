import traceback
from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException, NetworkException
from ..model.modelbase import *
from traceback import print_exc
from pydantic.v1.error_wrappers import ValidationError

class errorhandler(Component[apiclient]):
    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        while True:
            try:
                return await next.request(request)
            except NetworkException:
                pass
            except ApiException:
                raise
            except Exception:
                print_exc()
                raise
