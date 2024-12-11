import datetime
from decimal import *
from typing import Optional


from pydantic import BaseModel, ConfigDict


class OrdersSchema(BaseModel):
    qty: Decimal
    order_id: str
    price: Decimal
    profit: Optional[Decimal] = None
    add_ts: datetime.datetime
    update_ts: Optional[datetime.datetime]


class TrailingStopSchema(BaseModel):
    allowed: bool
    activator_type: str
    activator_value: int
    amount_percent: Optional[int] = None
    last_highest_price: Decimal
    retracement_percent: int
    split_percent: int
    splits: int
    orders: Optional[list[OrdersSchema]]


class FinalizerSchema(BaseModel):
    allowed: bool
    unfilled_orders: Optional[str]
    threshold_price: Optional[Decimal]
    activation_ts: Optional[datetime.datetime]
    trailing_stop: TrailingStopSchema


class StopLossSchema(BaseModel):
    auto: bool
    from_liquidate_percent: Decimal
    last_liquidation_price: Decimal
    fixed_stop_loss: Optional[Decimal]
    extra_margin_value: Optional[Decimal]


class ChunkOrdersSchema(BaseModel):
    max_cnt: int
    allowed: bool
    chunk_value: int
    price_percent: Decimal
    chunk_sell_percent: int
    chunk_sell_activation_percent: Decimal
    chunk_sell_retracement_percent: Decimal


class PositionOrdersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bot: str
    order_name: str
    token: str
    add_ts: Optional[datetime.datetime]
    buy_ts: Optional[datetime.datetime]
    end_ts: Optional[datetime.datetime]
    modified_ts: Optional[datetime.datetime]
    is_active: bool
    is_terminated: Optional[bool]
    profit: Optional[Decimal]
    start_qty: Optional[Decimal]
    start_price: Optional[Decimal]
    start_value: Decimal
    leverage: Decimal
    order_id: Optional[str]
    order_link_id: Optional[str]
    status: Optional[str]
    chunk_orders: ChunkOrdersSchema
    stop_loss: StopLossSchema
    finalizer: FinalizerSchema
