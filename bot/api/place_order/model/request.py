from decimal import *

from pydantic import BaseModel, Field


class PlaceOrderRequest(BaseModel):
    side: str
    symbol: str
    qty: Decimal
    category: str
    price: Decimal
    orderType: str = Field(alias="order_type")
    positionIdx: int = Field(alias="position_type")
    orderLinkId: str = Field(alias="order_link_id", default="")
