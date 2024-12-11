"""create chunk_orders table

Revision ID: 06e02d7e41d3
Revises: 40513a60b588
Create Date: 2024-11-30 15:36:09.750134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "06e02d7e41d3"
down_revision: Union[str, None] = "40513a60b588"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chunk_orders",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("position_order_id", sa.Integer, sa.ForeignKey("position_orders.id")),
        sa.Column("order_row_id", sa.Integer),
        sa.Column("stage", sa.Integer),
        sa.Column("is_active", sa.Boolean),
        sa.Column("add_ts", sa.DateTime(timezone=True)),
        sa.Column('modified_ts', sa.DateTime(timezone=True)),
        sa.Column("buy_ts", sa.DateTime(timezone=True)),
        sa.Column("sell_ts", sa.DateTime(timezone=True)),
        sa.Column("buy_qty", sa.Numeric),
        sa.Column("buy_price", sa.Numeric),
        sa.Column("sell_qty", sa.Numeric),
        sa.Column("sell_price", sa.Numeric),
        sa.Column('buy_status', sa.String(32)),
        sa.Column("buy_order_id", sa.String(64)),
        sa.Column("buy_order_link_id", sa.String(64)),
        sa.Column('sell_status', sa.String(32)),
        sa.Column("sell_order_id", sa.String(64)),
        sa.Column("sell_order_link_id", sa.String(64)),
        sa.Column('trailing_stop_start_ts', sa.DateTime(timezone=True)),
        sa.Column('trailing_stop_start_price', sa.Numeric),
        sa.Column('last_sell_price', sa.Numeric),
        sa.Column("profit", sa.Numeric),
        sa.Column("is_terminated", sa.Boolean, server_default=sa.text("false"))
    )


def downgrade() -> None:
    op.drop_table("chunk_orders")
