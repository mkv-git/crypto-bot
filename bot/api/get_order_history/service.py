from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_order_history.model.request import GetOrderHistoryRequest
from api.get_order_history.model.response import GetOrderHistoryResponse


class GetOrderHistoryService(BaseRestServices):
    SERVICE = "get_order_history"

    @override
    def request_model(self) -> Type[GetOrderHistoryRequest]:
        return GetOrderHistoryRequest

    @override
    def response_model(self) -> Type[GetOrderHistoryResponse]:
        return GetOrderHistoryResponse

    @override
    def transform_success_response(
        self, request: GetOrderHistoryRequest, response: Any
    ) -> GetOrderHistoryResponse:
        result = response

        order_data = response['result']['list']
        if order_data:
            result['result'] = order_data[0]
        else:
            result['result'] = None
        return GetOrderHistoryResponse.model_validate(result)
