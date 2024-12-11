"""create position_orders table

Revision ID: 40513a60b588
Revises: 
Create Date: 2024-11-30 15:25:03.970091

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "40513a60b588"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_CHUNK_ORDERS_JSON = {
    "max_cnt": 10,
    "allowed": True,
    "chunk_value": 20,
    "price_percent": 1,
    "chunk_sell_percent": 80,
    "chunk_sell_activation_percent": 3,
    "chunk_sell_retracement_percent": 1,
}

DEFUALT_FINALIZER_JSON = {
    "allowed": True,
    "activation_ts": None,
    "threshold_price": None,
    "unfilled_orders": None,
    "trailing_stop": {
        "splits": 3,
        "orders": [],
        "allowed": True,
        "split_percent": 1,
        "retracement": None,
        "amount_percent": 80,
        "activator_type": "roi",
        "activator_value": 100,
        "last_highest_price": 0,
        "retracement_percent": 2,
    },
}

DEFAULT_STOP_LOSS_JSON = {
    "auto": True,
    "fixed_stop_loss": None,
    "extra_margin_value": None,
    "last_liquidation_price": 0,
    "from_liquidate_percent": 0.5,
}


def upgrade() -> None:
    op.create_table(
        "position_orders",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("bot", sa.String(16), nullable=False),
        sa.Column("order_name", sa.String(32), nullable=False),
        sa.Column("token", sa.String(16), nullable=False),
        sa.Column("add_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("buy_ts", sa.DateTime(timezone=True)),
        sa.Column("end_ts", sa.DateTime(timezone=True)),
        sa.Column("modified_ts", sa.DateTime(timezone=True)),
        sa.Column('status', sa.String(32)),
        sa.Column("is_active", sa.Boolean),
        sa.Column("is_terminated", sa.Boolean),
        sa.Column("profit", sa.Numeric),
        sa.Column("start_qty", sa.Numeric),
        sa.Column("start_price", sa.Numeric),
        sa.Column("start_value", sa.Numeric, nullable=False, server_default="50"),
        sa.Column("leverage", sa.Numeric, server_default="5"),
        sa.Column("order_id", sa.String(64)),
        sa.Column("order_link_id", sa.String(64)),
        sa.Column("finalizer", postgresql.JSONB, server_default=json.dumps(DEFUALT_FINALIZER_JSON)),
        sa.Column("stop_loss", postgresql.JSONB, server_default=json.dumps(DEFAULT_STOP_LOSS_JSON)),
        sa.Column(
            "chunk_orders", postgresql.JSONB, server_default=json.dumps(DEFAULT_CHUNK_ORDERS_JSON)
        ),
    )
    op.create_unique_constraint('uq_bot_order_name', 'position_orders', ['bot', 'order_name'])


def downgrade() -> None:
    op.drop_constraint('uq_bot_order_name', 'position_orders')
    op.drop_table('position_orders')
