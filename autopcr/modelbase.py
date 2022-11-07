from re import T
from typing import Generic, TypeVar

class ErrorInfo:
    title: str = None
    message: str = None
    status: int = 0

    def __str__(self) -> str:
        return f'{self.title}: {self.message} (code={self.status})'

class ResponseBase:
    server_error: ErrorInfo = None
    def update(self, client: "dataclient"): ...

TResponse = TypeVar('TResponse', bound=ResponseBase)

class ResponseHeader:
    sid: str = None
    request_id: str = None
    viewer_id: str = None
    servertime: int = 0
    result_code: int = -1
    short_udid: str = None

class Response(Generic[TResponse]):
    data_headers: ResponseHeader = None
    data: TResponse = None

class Request(Generic[TResponse]):
    viewer_id: str = None
    
    @property
    def crypted(self) -> bool: return True

    @property
    def url(self) -> str:
        raise NotImplementedError()