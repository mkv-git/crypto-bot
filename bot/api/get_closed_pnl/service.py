from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_closed_pnl.model.request import GetClosedPnlRequest
from api.get_closed_pnl.model.response import GetClosedPnlResponse


class GetClosedPnlService(BaseRestServices):
    SERVICE = "get_closed_pnl"

    @override
    def request_model(self) -> Type[GetClosedPnlRequest]:
        return GetClosedPnlRequest

    @override
    def response_model(self) -> Type[GetClosedPnlResponse]:
        return GetClosedPnlResponse

    @override
    def transform_success_response(
        self, request: GetClosedPnlRequest, response: Any
    ) -> GetClosedPnlResponse:
        result = response
        result["result"] = response["result"].pop("list")
        return GetClosedPnlResponse.model_validate(result)
