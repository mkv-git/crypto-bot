from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.place_order.model.request import PlaceOrderRequest
from api.place_order.model.response import PlaceOrderResponse


class PlaceOrderService(BaseRestServices):
    SERVICE = "place_order"

    @override
    def request_model(self) -> Type[PlaceOrderRequest]:
        return PlaceOrderRequest

    @override
    def response_model(self) -> Type[PlaceOrderResponse]:
        return PlaceOrderResponse

    @override
    def transform_success_response(
        self, request: PlaceOrderRequest, response: Any
    ) -> PlaceOrderResponse:
        return PlaceOrderResponse.model_validate(response)
