from typing import Type, Any

from overrides import override

from config.const import RESP, REQ
from api.base.model.request import RequestParams
from api.base.rest_service import BaseRestServices
from api.get_wallet_balance.model.request import GetWalletBalanceRequest
from api.get_wallet_balance.model.response import GetWalletBalanceResponse


class GetWalletBalanceService(BaseRestServices):
    SERVICE = "get_wallet_balance"

    @override
    def request_model(self) -> Type[GetWalletBalanceRequest]:
        return GetWalletBalanceRequest

    @override
    def response_model(self) -> Type[GetWalletBalanceResponse]:
        return GetWalletBalanceResponse

    @override
    def transform_success_response(
        self, request: GetWalletBalanceRequest, response: Any
    ) -> GetWalletBalanceResponse:
        result = response
        obj = response["result"].pop("list")[0]
        result['result'] = obj['coin'][0]

        return GetWalletBalanceResponse.model_validate(result)
