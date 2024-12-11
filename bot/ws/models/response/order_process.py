from typing import Any

from pydantic import BaseModel, Field


class OrderData(BaseModel):
    order_id: str = Field(alias="orderId")
    order_link_id: str = Field(alias="orderLinkId")


class OrderProcessResponse(BaseModel):
    data: OrderData | dict[Any, Any]
    status_code: int = Field(alias="retCode")
    status_message: str = Field(alias="retMsg")

