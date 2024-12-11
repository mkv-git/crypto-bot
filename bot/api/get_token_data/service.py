from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_token_data.model.request import GetTokenDataRequest
from api.get_token_data.model.response import GetTokenDataResponse


class GetTokenDataService(BaseRestServices):
    SERVICE = "get_tickers"

    @override
    def request_model(self) -> Type[GetTokenDataRequest]:
        return GetTokenDataRequest

    @override
    def response_model(self) -> Type[GetTokenDataResponse]:
        return GetTokenDataResponse

    @override
    def transform_success_response(
        self, request: GetTokenDataRequest, response: Any
    ) -> GetTokenDataResponse:
        result = response
        obj = response["result"].pop("list")[0]
        result["result"] = {
            "mark_price": obj["markPrice"],
            "last_price": obj["lastPrice"],
            "index_price": obj["indexPrice"],
        }

        return GetTokenDataResponse.model_validate(result)
