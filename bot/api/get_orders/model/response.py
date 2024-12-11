from decimal import *
from typing import Any

from pydantic import BaseModel, Field, field_validator

from api.base.model.response import BybitBaseResponse


class OrdersData(BaseModel):
    @field_validator("price")
    @classmethod
    def empty_str(cls, v: str) -> Any:
        return Decimal(v) if v else None

    side: str
    symbol: str
    qty: Decimal
    price: Decimal | str
    order_id: str = Field(alias="orderId")
    order_status: str = Field(alias="orderStatus")
    order_link_id: str = Field(alias="orderLinkId")
    position_type: int = Field(alias="positionIdx")
    created_time: int = Field(alias="createdTime")
    updated_time: int = Field(alias="updatedTime")


class GetOrdersResponse(BybitBaseResponse):
    result: OrdersData | None = None
