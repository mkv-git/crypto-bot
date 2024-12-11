from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_positions.model.request import GetPositionsRequest
from api.get_positions.model.response import GetPositionsResponse


class GetPositionsService(BaseRestServices):
    SERVICE = "get_positions"

    @override
    def request_model(self) -> Type[GetPositionsRequest]:
        return GetPositionsRequest

    @override
    def response_model(self) -> Type[GetPositionsResponse]:
        return GetPositionsResponse

    @override
    def transform_success_response(
        self, request: GetPositionsRequest, response: Any
    ) -> GetPositionsResponse:

        result = response
        result['result'] = response['result'].pop('list')
        return GetPositionsResponse.model_validate(result)
