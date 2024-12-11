from decimal import *

from pydantic import BaseModel, Field


class WalletData(BaseModel):
    wallet_balance: Decimal = Field(alias="walletBalance")
    unrealised_pnl: Decimal = Field(alias="unrealisedPnl")
    available_balance: Decimal = Field(alias="availableToWithdraw")
    total_booked_margin: Decimal = Field(alias="totalOrderIM")
    total_position_margin: Decimal = Field(alias="totalPositionIM")


class WalletStreamResponse(BaseModel):
    data: WalletData
    stream_ts: int = Field(alias="creationTime")
