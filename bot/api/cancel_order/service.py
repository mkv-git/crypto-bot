from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.cancel_order.model.request import CancelOrderRequest
from api.cancel_order.model.response import CancelOrderResponse


class CancelOrderService(BaseRestServices):
    SERVICE = "cancel_order"

    @override
    def request_model(self) -> Type[CancelOrderRequest]:
        return CancelOrderRequest

    @override
    def response_model(self) -> Type[CancelOrderResponse]:
        return CancelOrderResponse

    @override
    def transform_success_response(
        self, request: CancelOrderRequest, response: Any
    ) -> CancelOrderResponse:
        return CancelOrderResponse.model_validate(response)
