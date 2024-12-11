from decimal import *

from pydantic import BaseModel, Field


class PlaceOrderRequest(BaseModel):
    side: str
    symbol: str
    qty: Decimal
    category: str
    orderType: str = Field(alias='order_type')
    price: Decimal
    orderLinkId: str = Field(alias='order_link_id')
    positionIdx: int = Field(alias='position_type')
