from decimal import *
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class GetOrdersRequest(BaseModel):
    @model_validator(mode="after")
    def check_order_id(self):
        if not self.orderId and not self.orderLinkId:
            raise ValueError("either order_id or order_link_id is required")
        return self

    symbol: str
    category: str
    open_only: int | None = 0
    orderId: str | None = Field(alias="order_id", default="")
    orderLinkId: str | None = Field(alias="order_link_id", default="")
