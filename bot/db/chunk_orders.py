import logging
import datetime

from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, ForeignKey, desc, or_, and_, func, text, UniqueConstraint
from sqlalchemy.types import Integer, String, Boolean, DateTime, Text, Enum, Float, Numeric

from db import Base, BaseModel
from db.models.chunk_orders import ChunkOrdersSchema


class ChunkOrders(Base, BaseModel):
    __tablename__ = "chunk_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_order_id = Column(Integer, ForeignKey("position_orders.id"))
    order_row_id = Column(Integer)
    is_active = Column(Boolean)
    stage = Column(Integer)
    add_ts = Column(DateTime(timezone=True))
    modified_ts = Column(DateTime(timezone=True))
    buy_ts = Column(DateTime(timezone=True))
    buy_qty = Column(DateTime(timezone=True))
    buy_price = Column(Numeric)
    buy_order_id = Column(String(64))
    buy_order_link_id = Column(String(64))
    sell_ts = Column(DateTime(timezone=True))
    sell_qty = Column(Numeric)
    sell_price = Column(Numeric)
    sell_order_id = Column(String(64))
    sell_order_link_id = Column(String(64))
    trailing_stop_start_ts = Column(DateTime(timezone=True))
    trailing_stop_start_price = Column(Numeric)
    last_sell_price = Column(Numeric)
    profit = Column(Numeric)
    buy_status = Column(String(64))
    sell_status = Column(String(64))
    is_terminated = Column(Boolean, default=False)

    @classmethod
    def load_last_state(cls, position_order_id):
        res = (
            cls.db_session()
            .query(cls)
            .filter(cls.position_order_id == position_order_id)
            .order_by(cls.order_row_id.asc())
            .order_by(cls.stage.asc())
            .all()
        )

        if not res:
            return None

        return {r.order_row_id: cls.serialize(ChunkOrdersSchema, r) for r in res}

    @classmethod
    def load_last_chunk_order(cls, position_order_id, order_row_id):
        res = (
            cls.db_session()
            .query(cls)
            .filter(cls.position_order_id == position_order_id)
            .filter(cls.order_row_id == order_row_id)
            .filter(cls.is_active == False)
            .order_by(cls.stage.desc())
            .first()
        )
        if not res:
            return None

        return cls.serialize(ChunkOrdersSchema, res)
