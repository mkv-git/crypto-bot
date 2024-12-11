from decimal import *
from typing import Any

from pydantic import BaseModel, Field, field_validator


class PositionData(BaseModel):
    @field_validator(
        "entry_price",
        "realised_pnl",
        "unrealised_pnl",
        "position_value",
        "position_margin",
        "liquidation_price",
    )
    @classmethod
    def empty_str(cls, v: str) -> Any:
        return Decimal(v) if v else None

    @field_validator(
        "updated_time",
    )
    @classmethod
    def empty_str2(cls, v: str) -> Any:
        return int(v) if v else None

    side: str
    size: Decimal
    symbol: str
    leverage: Decimal
    updated_time: int | str = Field(alias="updatedTime")
    position_type: int = Field(alias="positionIdx")
    auto_add_margin: bool = Field(alias="autoAddMargin")
    entry_price: Decimal | str = Field(alias="entryPrice")
    position_margin: Decimal | str = Field(alias="positionIM")
    liquidation_price: Decimal | str = Field(alias="liqPrice")
    realised_pnl: Decimal | str = Field(alias="curRealisedPnl")
    unrealised_pnl: Decimal | str = Field(alias="unrealisedPnl")
    position_value: Decimal | str = Field(alias="positionValue")


class PositionStreamResponse(BaseModel):
    data: list[PositionData]
    stream_ts: int = Field(alias="creationTime")
