from pydantic import BaseModel, Field

from api.base.model.response import BybitBaseResponse


class CancelOrderData(BaseModel):
    order_id: str = Field(alias="orderId")
    order_link_id: str = Field(alias="orderLinkId")


class CancelOrderResponse(BybitBaseResponse):
    result: CancelOrderData
