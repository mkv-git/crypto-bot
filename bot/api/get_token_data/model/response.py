from decimal import *

from pydantic import BaseModel

from api.base.model.response import BybitBaseResponse


class TokenData(BaseModel):
    last_price: Decimal
    mark_price: Decimal
    index_price: Decimal


class GetTokenDataResponse(BybitBaseResponse):
    result: TokenData
