import logging
import datetime

from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, ForeignKey, desc, or_, and_, func, text, UniqueConstraint
from sqlalchemy.types import Integer, String, Boolean, DateTime, Text, Enum, Float, Numeric

from db import Base, BaseModel
from db.models.position_orders import PositionOrdersSchema


class PositionOrders(Base, BaseModel):
    __tablename__ = "position_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot = Column(String(16), nullable=False)
    order_name = Column(String(32), nullable=False)
    token = Column(String(16), nullable=False)
    add_ts = Column(DateTime)
    buy_ts = Column(DateTime)
    end_ts = Column(DateTime)
    modified_ts = Column(DateTime)
    is_active = Column(Boolean)
    is_terminated = Column(Boolean)
    profit = Column(Numeric)
    start_qty = Column(Numeric)
    start_price = Column(Numeric)
    start_value = Column(Numeric, nullable=False)
    leverage = Column(Numeric)
    order_id = Column(String(64))
    order_link_id = Column(String(64))
    status = Column(String(32))
    stop_loss = Column(postgresql.JSONB)
    finalizer = Column(postgresql.JSONB)
    chunk_orders = Column(postgresql.JSONB)

    UniqueConstraint(bot, order_name)

    @classmethod
    def get_by_token(cls, token):
        res = cls.db_session().query(cls).filter(cls.token == token).all()
        if not res:
            return None

        return cls.serialize(PositionOrdersSchema, res)

    @classmethod
    def get_order(cls, order_name: str):
        res = (
            cls.db_session()
            .query(cls)
            .filter(cls.order_name == order_name)
            .filter(cls.is_active == True)
            .first()
        )

        if not res:
            return None

        return cls.serialize(PositionOrdersSchema, res)

    @classmethod
    def update_json_field(cls, order_name, field, json_path, value):
        json_field = "{%s}" % field
        cls.db_session().query(cls).filter(cls.order_name == order_name).update(
            {
                cls.modified_ts: func.now(),
                getattr(cls, field): func.jsonb_set(
                    getattr(cls, field), json_path, func.to_jsonb(value)
                ),
            }
        )

        cls.db_session().commit()
        cls.db_session().flush()
        return True
