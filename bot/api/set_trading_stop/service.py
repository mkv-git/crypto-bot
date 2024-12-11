from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.set_trading_stop.model.request import SetTradingStopRequest
from api.set_trading_stop.model.response import SetTradingStopResponse

class SetTradingStopService(BaseRestServices):
    SERVICE = 'set_trading_stop'

    @override
    def request_model(self) -> Type[SetTradingStopRequest]:
        return SetTradingStopRequest

    @override
    def response_model(self) -> Type[SetTradingStopResponse]:
        return SetTradingStopResponse

    @override
    def transform_success_response(self, request: SetTradingStopRequest, response: Any) -> SetTradingStopResponse:
        return SetTradingStopResponse.model_validate(response)
