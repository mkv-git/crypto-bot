from pydantic import BaseModel, Field

from api.base.model.response import BybitBaseResponse


class OrdersData(BaseModel):
    order_id: str = Field(alias="orderId")
    order_link_id: str = Field(alias="orderLinkId")


class CancelAllOrdersResponse(BybitBaseResponse):
    result: list[OrdersData]
