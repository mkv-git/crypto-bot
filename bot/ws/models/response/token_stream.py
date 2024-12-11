from decimal import *

from pydantic import BaseModel, Field


class TokenData(BaseModel):
    last_price: Decimal = Field(alias='lastPrice')
    mark_price: Decimal = Field(alias='markPrice')
    index_price: Decimal = Field(alias='indexPrice')


class TokenStreamResponse(BaseModel):
    data: TokenData
    stream_ts: int = Field(alias='ts')    
