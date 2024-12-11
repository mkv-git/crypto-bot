from pydantic import BaseModel, Field
from api.base.model.response import BybitBaseResponse


class PlaceOrderData(BaseModel):
    order_id: str = Field(alias="orderId")
    order_link_id: str = Field(alias="orderLinkId")


class PlaceOrderResponse(BybitBaseResponse):
    result: PlaceOrderData
