from decimal import *

from pydantic import BaseModel, Field

from api.base.model.response import BybitBaseResponse


class WalletData(BaseModel):
    wallet_balance: Decimal = Field(alias='walletBalance')
    unrealised_pnl: Decimal = Field(alias='unrealisedPnl')
    available_balance: Decimal = Field(alias='availableToWithdraw')
    total_booked_margin: Decimal = Field(alias='totalOrderIM')
    total_position_margin: Decimal = Field(alias='totalPositionIM')


class GetWalletBalanceResponse(BybitBaseResponse):
    result: WalletData
