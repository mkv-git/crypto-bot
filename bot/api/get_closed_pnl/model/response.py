from decimal import *

from pydantic import BaseModel, Field

from api.base.model.response import BybitBaseResponse


class ClosedPnlData(BaseModel):
    qty: Decimal
    pnl: Decimal = Field(alias='closedPnl')
    order_id: str = Field(alias='orderId')
    leverage: Decimal
    exit_price: Decimal = Field(alias='avgExitPrice')
    entry_price: Decimal = Field(alias='avgEntryPrice')
    order_update_time: int = Field(alias='updatedTime')
    order_created_time: int = Field(alias='createdTime')


class GetClosedPnlResponse(BybitBaseResponse):
    result: list[ClosedPnlData]
