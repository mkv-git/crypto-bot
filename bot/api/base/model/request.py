from typing import Type, Generic

from pydantic import BaseModel, Field

from api.utils.const import REQ


class RequestParams(BaseModel, Generic[REQ]):
    demo: bool
    testnet: bool = Field(default=False)
    api_key: str
    api_secret: str
    payload: REQ
