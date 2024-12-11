from decimal import *

from pydantic import BaseModel


class CancelAllOrdersRequest(BaseModel):
    symbol: str
    category: str
