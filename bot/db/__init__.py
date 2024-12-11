#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from urllib import parse

from sqlalchemy.pool import NullPool
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine, asc, desc, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

ALLOWED_OPERATORS = {
    "like": "like",
    "ilike": "ilike",
    "in": "in_",
    "notin": "notin_",
    "eq": "__eq__",
    "ne": "__ne__",
    "lt": "__lt__",
    "le": "__le__",
    "gt": "__gt__",
    "ge": "__ge__",
}

log = logging.getLogger(__name__)
Base = declarative_base()


class ResourceNotFound(Exception):
    def __init__(self, message):
        super(ResourceNotFound, self).__init__()
        self.message = message
        self.code = 404

    def __str__(self):
        return repr(self.message)


class EmptyDataSetException(Exception):
    def __init__(self, message):
        super(EmptyDataSetException, self).__init__()
        self.message = message
        self.code = 409

    def __str__(self):
        return repr(self.message)


url = "postgresql://%s:%s@%s:%s/%s" % (
    os.getenv("BYBIT_DATABASE_USERNAME"),
    os.getenv("BYBIT_DATABASE_PASSWORD"),
    os.getenv("BYBIT_DATABASE_HOST"),
    os.getenv("BYBIT_DATABASE_PORT"),
    os.getenv("BYBIT_DATABASE_SID"),
)

session = scoped_session(sessionmaker())
engine = create_engine(url, pool_recycle=True)
session.configure(bind=engine)
DB = session


class BaseModel:
    @classmethod
    def db_session(cls):
        return DB

    @classmethod
    def serialize(cls, schema, obj):
        ret_val = []
        if isinstance(obj, list):
            ret_val = [schema(**row.__dict__) for row in obj]
        else:
            ret_val = schema(**obj.__dict__)
        return ret_val

    @classmethod
    def all(cls):
        return DB.query(cls).all()

    @classmethod
    def get_by_primary_key(cls, id):
        session = DB
        return session.query(cls).filter(cls.__mapper__.primary_key[0] == id).first()

    @classmethod
    def get_by_id(cls, id):
        session = DB
        return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def insert(cls, payload, flush_changes=False):
        session = DB
        record_to_insert = cls()
        columns_to_add = set()

        for key, value in payload.items():
            column_obj = getattr(cls, key, None)
            if column_obj is None:
                continue

            columns_to_add.add(key)
            setattr(record_to_insert, key, value)

        if not columns_to_add:
            raise EmptyDataSetException("No columns were found")

        session.add(record_to_insert)
        session.commit()
        return record_to_insert

    @classmethod
    def update(cls, record_filter, payload):
        query = cls.db_session().query(cls)
        for column, column_value in record_filter.items():
            f_column_obj = getattr(cls, column, None)
            if f_column_obj is None:
                return False

            query = query.filter(f_column_obj == column_value)

        record_to_update = query.first()
        if record_to_update is None:
            raise ResourceNotFound("Resource not found")

        columns_to_add = set()
        for key, value in payload.items():
            column_obj = getattr(cls, key, None)
            if column_obj is None:
                continue
            columns_to_add.add(key)
            setattr(record_to_update, key, value)

        if not columns_to_add:
            raise EmptyDataSetException

        cls.db_session().commit()
        return True

    @classmethod
    def delete(cls, record_filter):
        query = cls.db_session().query(cls)
        for column, column_value in record_filter.items():
            f_column_obj = getattr(cls, column, None)
            if f_column_obj is None:
                return False

            query = query.filter(f_column_obj == column_value)

        record_to_delete = query.first()
        if record_to_delete is None:
            raise ResourceNotFound("Resource not found")

        cls.db_session().delete(record_to_delete)
        cls.db_session().commit()

        return True
