import datetime
from decimal import *
from typing import Optional


from pydantic import BaseModel, ConfigDict


class ChunkOrdersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_row_id: int
    position_order_id: int
    is_active: bool
    stage: int
    add_ts: datetime.datetime
    buy_ts: Optional[datetime.datetime]
    buy_qty: Decimal
    buy_price: Decimal
    buy_order_id: str
    buy_order_link_id: str
    buy_status: Optional[str]
    sell_ts: Optional[datetime.datetime]
    sell_qty: Decimal
    sell_price: Decimal
    sell_order_id: Optional[str]
    sell_order_link_id: Optional[str]
    trailing_stop_start_ts: Optional[datetime.datetime]
    trailing_stop_start_price: Optional[Decimal]
    sell_status: Optional[str]
    profit: Optional[Decimal]
    is_terminated: bool
