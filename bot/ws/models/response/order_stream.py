from decimal import *
from typing import Any

from pydantic import BaseModel, Field, field_validator


class OrderData(BaseModel):
    @field_validator("price")
    @classmethod
    def empty_str(cls, v: str) -> Any:
        return Decimal(v) if v else None

    side: str
    symbol: str
    qty: Decimal
    price: Decimal | str
    order_id: str = Field(alias="orderId")
    tpsl_mode: str = Field(alias="tpslMode")
    create_type: str = Field(alias="createType")
    order_status: str = Field(alias="orderStatus")
    created_time: int = Field(alias="createdTime")
    updated_time: int = Field(alias="updatedTime")
    order_link_id: str = Field(alias="orderLinkId")
    position_type: int = Field(alias="positionIdx")
    stop_order_type: str = Field(alias="stopOrderType")


class OrderStreamResponse(BaseModel):
    data: list[OrderData]
    stream_ts: int = Field(alias="creationTime")
