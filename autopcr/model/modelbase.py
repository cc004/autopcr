#type: ignore
from re import T
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

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
    short_udid: str = None

class Response(GenericModel, Generic[TResponse]):
    data_headers: ResponseHeader = None
    data: Optional[TResponse] = None

from pydantic.main import validate_model, object_setattr
from typing import Any

class Request(Generic[TResponse], BaseModel):
    viewer_id: str = None
    
    @property
    def crypted(self) -> bool: return True

    @property
    def url(self) -> str:
        raise NotImplementedError()
    
    def __init__(__pydantic_self__, **data: Any) -> None:
        """
        Create a new model by parsing and validating input data from keyword arguments.

        Raises ValidationError if the input data cannot be parsed to form a valid model.
        """
        # Uses something other than `self` the first arg to allow "self" as a settable attribute
        values, fields_set, validation_error = validate_model(__pydantic_self__.__class__, data)
        try:
            object_setattr(__pydantic_self__, '__dict__', values)
        except TypeError as e:
            raise TypeError(
                'Model values must be a dict; you may not have returned a dictionary from a root validator'
            ) from e
        object_setattr(__pydantic_self__, '__fields_set__', fields_set)
        __pydantic_self__._init_private_attributes()
