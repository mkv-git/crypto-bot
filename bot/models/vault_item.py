import datetime
from decimal import *
from dataclasses import dataclass, asdict, KW_ONLY


@dataclass
class VaultItem:
    _: KW_ONLY
    id: int
    stage: int
    is_active: bool
    order_row_id: int
    position_order_id: int
    buy_order_id: str | None = None
    buy_order_link_id: str | None
    buy_ts: datetime.datetime | None = None
    buy_qty: Decimal
    buy_price: Decimal
    sell_order_id: str | None = None
    sell_order_link_id: str | None
    sell_ts: datetime.datetime | None = None
    sell_qty: Decimal
    sell_price: Decimal
    last_high_price: Decimal | None = None
    last_sell_price: Decimal | None = None
    trailing_stop_start_price: Decimal | None = None


if __name__ == "__main__":
    vi = VaultItem(
        stage=0,
        is_active=True,
        order_row_id=0,
        position_order_id=0,
        buy_qty=Decimal('10.2'),
        buy_price=Decimal('12'),
        sell_qty=Decimal('1'),
        sell_price=Decimal('13'),
        buy_order_link_id='sad',
        sell_order_link_id='saas',
        trailing_stop_start_price=Decimal('1221')
    )

    print(vi)
    print(asdict(vi))
