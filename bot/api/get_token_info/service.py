from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_token_info.model.request import GetTokenInfoRequest
from api.get_token_info.model.response import GetTokenInfoResponse


class GetTokenInfoService(BaseRestServices):
    SERVICE = "get_instruments_info"

    @override
    def request_model(self) -> Type[GetTokenInfoRequest]:
        return GetTokenInfoRequest

    @override
    def response_model(self) -> Type[GetTokenInfoResponse]:
        return GetTokenInfoResponse

    @override
    def transform_success_response(
        self, request: GetTokenInfoRequest, response: Any
    ) -> GetTokenInfoResponse:
        result = response
        obj = response["result"].pop("list")[0]
        result['result'].update({
            "maxLeverage": obj["leverageFilter"]["maxLeverage"],
            "minOrderQty": obj["lotSizeFilter"]["minOrderQty"],
            "maxMktOrderQty": obj["lotSizeFilter"]["maxMktOrderQty"],
            "qtyStep": obj["lotSizeFilter"]["qtyStep"],
            "tickSize": obj["priceFilter"]["tickSize"],
        })
        return GetTokenInfoResponse.model_validate(result)
