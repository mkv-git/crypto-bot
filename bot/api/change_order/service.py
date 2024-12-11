from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.change_order.model.request import ChangeOrderRequest
from api.change_order.model.response import ChangeOrderResponse


class ChangeOrderService(BaseRestServices):
    SERVICE = "amend_order"

    @override
    def request_model(self) -> Type[ChangeOrderRequest]:
        return ChangeOrderRequest

    @override
    def response_model(self) -> Type[ChangeOrderResponse]:
        return ChangeOrderResponse

    @override
    def transform_success_response(
        self, request: ChangeOrderRequest, response: Any
    ) -> ChangeOrderResponse:
        return ChangeOrderResponse.model_validate(response)
