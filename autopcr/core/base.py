from typing import List, Callable, Coroutine, Any
from ..model.modelbase import *

TResponse = TypeVar('TResponse', bound=ResponseBase)
T = TypeVar('T', bound='Container[T]')

class Container(Generic[T]):
    def __init__(self):
        self._components: List["Component[T]"] = []
        self.request = self._request
    def register(self, component: "Component[T]"):
        self._components.append(component)
        component.register_to(self)
        next = self.request
        def request(request: Request[TResponse]) -> Coroutine[Any, Any, TResponse]:
            return component.request(request, next)
        self.request = request
    async def _request(self, request: Request[TResponse]) -> TResponse:
        raise NotImplementedError

class Component(Generic[T]):
    def register_to(self, container: T):
        self._container = container
    async def request(self, request: Request[TResponse],
        next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        return next(request)
    @property
    def name(self) -> str:
        return self.__class__.__name__
