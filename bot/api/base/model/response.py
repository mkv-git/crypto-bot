from decimal import *
from typing import Generic, Optional, Any

from pydantic import BaseModel, Field

from config.const import RESP


class ErrorResponseData(BaseModel):
    result: str
    status_code: int


class ServiceResponse(BaseModel, Generic[RESP]):
    status: str
    data: RESP | ErrorResponseData
    duration: Decimal = Decimal('0')


class BybitBaseResponse(BaseModel):
    result: Any
    query_ts: int = Field(alias="time")
    status_code: int = Field(alias="retCode")
    status_message: str = Field(alias="retMsg")
    extra_info: dict = Field(alias="retExtInfo")
