from decimal import *

from pydantic import BaseModel, Field, model_validator


class GetOrderHistoryRequest(BaseModel):
    @model_validator(mode="after")
    def check_order_id(self):
        if not self.orderId and not self.orderLinkId:
            raise ValueError("either order_id or order_link_id is required")
        return self

    symbol: str
    category: str
    orderId: str | None = Field(alias="order_id", default="")
    orderLinkId: str | None = Field(alias="order_link_id", default="")
