from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.set_leverage.model.request import SetLeverageRequest
from api.set_leverage.model.response import SetLeverageResponse

class SetLeverageService(BaseRestServices):
    SERVICE = 'set_leverage'

    @override
    def request_model(self) -> Type[SetLeverageRequest]:
        return SetLeverageRequest

    @override
    def response_model(self) -> Type[SetLeverageResponse]:
        return SetLeverageResponse

    @override
    def transform_success_response(self, request: SetLeverageRequest, response: Any) -> SetLeverageResponse:
        return SetLeverageResponse.model_validate(response)
