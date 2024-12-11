from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_orders.model.request import GetOrdersRequest
from api.get_orders.model.response import GetOrdersResponse


class GetOrdersService(BaseRestServices):
    SERVICE = "get_open_orders"

    @override
    def request_model(self) -> Type[GetOrdersRequest]:
        return GetOrdersRequest

    @override
    def response_model(self) -> Type[GetOrdersResponse]:
        return GetOrdersResponse

    @override
    def transform_success_response(
        self, request: GetOrdersRequest, response: Any
    ) -> GetOrdersResponse:
        result = response
        order_data = response['result']['list']
        if order_data:
            result['result'] = order_data[0]
        else:
            result['result'] = None
        return GetOrdersResponse.model_validate(result)
