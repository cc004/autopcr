from typing import List, Callable, Coroutine, Any
from ..model.modelbase import *

T = TypeVar('T', bound="Container")


class RequestHandler:
    def __init__(self, next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]):
        self._next = next

    async def request(self, request: Request[TResponse]) -> TResponse:
        return await self._next(request)


class Component(Generic[T]):
    def register_to(self, container: T):
        self._container = container

    async def request(self, request: Request[TResponse],
                      next: RequestHandler) -> TResponse:
        return await next.request(request)

    @property
    def name(self) -> str:
        return self.__class__.__name__


class Container(Generic[T]):
    def __init__(self):
        self._components: List[Component[T]] = []

    def register(self, component: Component[T]):
        self._components.append(component)
        component.register_to(self)
        next = RequestHandler(self.request)

        def request(request: Request[TResponse]) -> Coroutine[Any, Any, TResponse]:
            return component.request(request, next)

        self.request = request

    async def request(self, request: Request[TResponse]) -> TResponse:
        raise NotImplementedError
