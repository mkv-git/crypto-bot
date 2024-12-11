from decimal import *

from pydantic import BaseModel, Field


class ChangeOrderRequest(BaseModel):
    symbol: str
    category: str
    price: Decimal
    qty: Decimal | str = ""
    orderLinkId: str | None = Field(alias="order_link_id", default="")
    orderId: str | None = Field(alias="order_id", default="")
