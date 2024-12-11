from decimal import *

from pydantic import BaseModel, Field


class SetTradingStopRequest(BaseModel):
    symbol: str
    category: str
    tpslMode: str = Field(alias="tpsl_mode")
    positionIdx: int = Field(alias="position_type")
    stopLoss: Decimal | str = Field(alias="stop_loss", default="")
    slSize: Decimal | str = Field(alias="stop_loss_qty", default="")
    tpOrderType: str | None = Field(alias="tp_order_type", default="")
    slOrderType: str | None = Field(alias="sl_order_type", default="")
    tpTriggerBy: str | None = Field(alias="tp_trigger_by", default="")
    slTriggerBy: str | None = Field(alias="sl_trigger_by", default="")
    takeProfit: Decimal | str = Field(alias="take_profit", default="")
    tpSize: Decimal | str = Field(alias="take_profit_qty", default="")
    slLimitPrice: Decimal | str = Field(alias="stop_loss_price", default="")
    tpLimitPrice: Decimal | str = Field(alias="take_profit_price", default="")
