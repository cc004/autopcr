# type: ignore
import typing
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo


def _is_optional(annotation) -> bool:
    origin = typing.get_origin(annotation)
    if origin is typing.Union:
        return type(None) in typing.get_args(annotation)
    return annotation is type(None) or annotation is typing.Any


class ImplicitOptionalMeta(ModelMetaclass):
    """adapter"""
    def __new__(mcs, name, bases, namespace, **kwargs):
        annotations = namespace.get('__annotations__', {})
        for field_name in list(annotations.keys()):
            if field_name.startswith('_'):
                annotations.pop(field_name, None)
                namespace.pop(field_name, None)
                continue

            annotation = annotations[field_name]
            if isinstance(annotation, str):
                # is humanwrite annotation, skip it
                continue

            default = namespace.get(field_name, ...)
            is_none_default = default is None
            if isinstance(default, FieldInfo):
                is_none_default = default.default is None

            if is_none_default and not _is_optional(annotation):
                annotations[field_name] = Optional[annotation]

        namespace['__annotations__'] = annotations
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class GameBaseModel(BaseModel, metaclass=ImplicitOptionalMeta):
    pass


class ErrorInfo(GameBaseModel):
    title: str = None
    message: str = None
    status: int = 0

    def __str__(self) -> str:
        return f'{self.title}: {self.message} (code={self.status})'

class ResponseBase(GameBaseModel):
    server_error: ErrorInfo = None
    update_bank_gold: int = None
    async def update(self, mgr: "datamgr", request): ...

TResponse = TypeVar('TResponse', bound=ResponseBase, covariant=True)

class ResponseHeader(GameBaseModel):
    sid: str = None
    request_id: str = None
    viewer_id: str = None
    servertime: int = 0
    result_code: int = -1
    short_udid: str = None

class Response(GameBaseModel, Generic[TResponse]):
    data_headers: ResponseHeader = None
    data: Optional[TResponse] = None

class Request(Generic[TResponse], GameBaseModel):
    viewer_id: str = None

    @property
    def crypted(self) -> bool: return True

    @property
    def url(self) -> str:
        raise NotImplementedError()
