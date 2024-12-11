from decimal import *

from pydantic import BaseModel, Field


class CancelOrderRequest(BaseModel):
    symbol: str
    category: str
    orderId: str | None = Field(alias="order_id", default="")
    orderLinkId: str | None = Field(alias="order_link_id", default="")
