from decimal import *

from pydantic import BaseModel, Field

from api.base.model.response import BybitBaseResponse


class ChangeMarginData(BaseModel):
    size: Decimal | str
    leverage: Decimal
    position_type: int = Field(alias="positionIdx")
    auto_add_margin: bool = Field(alias="autoAddMargin")
    unrealised_pnl: Decimal | str = Field(alias="unrealisedPnl")
    position_value: Decimal | str = Field(alias="positionValue")
    position_margin: Decimal | str = Field(alias="positionIM")
    liquidation_price: Decimal | str = Field(alias="liqPrice")


class ChangeMarginResponse(BybitBaseResponse):
    result: ChangeMarginData
