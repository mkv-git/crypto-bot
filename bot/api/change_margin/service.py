from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.change_margin.model.request import ChangeMarginRequest
from api.change_margin.model.response import ChangeMarginResponse

class ChangeMarginService(BaseRestServices):
    SERVICE = 'add_or_reduce_margin'

    @override
    def request_model(self) -> Type[ChangeMarginRequest]:
        return ChangeMarginRequest

    @override
    def response_model(self) -> Type[ChangeMarginResponse]:
        return ChangeMarginResponse

    @override
    def transform_success_response(self, request: ChangeMarginRequest, response: Any) -> ChangeMarginResponse:
        return ChangeMarginResponse.model_validate(response)
