#type: ignore
from inspect import get_annotations
from typing import ClassVar, Generic, TypeVar, Optional
from pydantic import VERSION as PYDANTIC_VERSION
from pydantic import BaseModel as PydanticBaseModel

PYDANTIC_V2 = PYDANTIC_VERSION.split(".", 1)[0] == "2"

if PYDANTIC_V2:
    from pydantic import ConfigDict, model_validator
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
else:
    from pydantic.generics import GenericModel as PydanticGenericModel

    class BaseModel(PydanticBaseModel):
        class Config:
            allow_population_by_field_name = True
            smart_union = True

        def model_dump(self, **kwargs):
            return self.dict(**kwargs)

        def model_dump_json(self, **kwargs):
            return self.json(**kwargs)

        @classmethod
        def model_validate(cls, value):
            return cls.parse_obj(value)

if PYDANTIC_V2:
    GenericModel = BaseModel
else:
    class GenericModel(PydanticGenericModel, BaseModel):
        pass

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

class Response(GenericModel, Generic[TResponse]):
    data_headers: ResponseHeader = None
    data: Optional[TResponse] = None

class Request(GenericModel, Generic[TResponse]):
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
