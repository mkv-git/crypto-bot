from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.cancel_all_orders.model.request import CancelAllOrdersRequest
from api.cancel_all_orders.model.response import CancelAllOrdersResponse


class CancelAllOrdersService(BaseRestServices):
    SERVICE = "cancel_all_orders"

    @override
    def request_model(self) -> Type[CancelAllOrdersRequest]:
        return CancelAllOrdersRequest

    @override
    def response_model(self) -> Type[CancelAllOrdersResponse]:
        return CancelAllOrdersResponse

    @override
    def transform_success_response(
        self, request: CancelAllOrdersRequest, response: Any
    ) -> CancelAllOrdersResponse:
        result = response
        result["result"] = response["result"].pop("list")

        return CancelAllOrdersResponse.model_validate(result)
