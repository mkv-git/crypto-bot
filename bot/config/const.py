from enum import StrEnum
from typing import TypeVar, Optional

from pydantic import BaseModel


REQ = TypeVar("REQ", bound=BaseModel)
RESP = TypeVar("RESP", bound=BaseModel)
MODEL = TypeVar("MODEL", bound=BaseModel)

START_PRICE_MAX_DIFF_PERCENT = 20
