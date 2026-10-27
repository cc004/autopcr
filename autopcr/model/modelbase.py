#type: ignore
from inspect import get_annotations
from typing import ClassVar, Generic, TypeVar, Optional
from pydantic import BaseModel as PydanticBaseModel, ConfigDict, model_validator
from pydantic.fields import FieldInfo

class BaseModel(PydanticBaseModel):
    """Keep the generated models' implicit nullable defaults."""
    model_config = ConfigDict(coerce_numbers_to_str=True, validate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def normalize_empty_model(cls, value):
        return {} if isinstance(value, list) and not value else value

    def __init_subclass__(cls, **kwargs):
        # Normalize annotations before Pydantic builds nested model schemas.
        annotations = get_annotations(cls)
        for name, annotation in annotations.items():
            default = cls.__dict__.get(name, ...)
            if default is None or isinstance(default, FieldInfo) and default.default is None:
                annotations[name] = Optional[annotation]
        cls.__annotations__ = annotations
        super().__init_subclass__(**kwargs)

class ErrorInfo(BaseModel):
    title: str = None
    message: str = None
    status: int = 0

    def __str__(self) -> str:
        return f'{self.title}: {self.message} (code={self.status})'

class ResponseBase(BaseModel):
    server_error: ErrorInfo = None
    update_bank_gold: int = None
    async def update(self, mgr: "datamgr", request): ...

TResponse = TypeVar('TResponse', bound=ResponseBase, covariant=True)

class ResponseHeader(BaseModel):
    sid: str = None
    request_id: str = None
    viewer_id: str = None
    servertime: int = 0
    result_code: int = -1
    short_udid: str | bool = None

class Response(BaseModel, Generic[TResponse]):
    data_headers: ResponseHeader = None
    data: Optional[TResponse] = None

class Request(BaseModel, Generic[TResponse]):
    response_type: ClassVar[type[ResponseBase]]
    viewer_id: str = None

    @classmethod
    def __class_getitem__(cls, response_type):
        # Record the response type for the API client's parser.
        request_type = super().__class_getitem__(response_type)
        request_type.response_type = response_type
        return request_type
    
    @property
    def crypted(self) -> bool: return True

    @property
    def url(self) -> str:
        raise NotImplementedError()
