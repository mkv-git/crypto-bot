from decimal import *

from pydantic import BaseModel, Field


class SetLeverageRequest(BaseModel):
    symbol: str
    category: str
    buyLeverage: Decimal = Field(alias="buy_leverage")
    sellLeverage: Decimal = Field(alias="sell_leverage")
