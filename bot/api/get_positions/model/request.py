from decimal import *

from pydantic import BaseModel


class GetPositionsRequest(BaseModel):
    symbol: str
    category: str
