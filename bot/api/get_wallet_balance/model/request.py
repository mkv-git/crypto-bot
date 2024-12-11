from decimal import *
from typing import Optional

from pydantic import BaseModel


class GetWalletBalanceRequest(BaseModel):
    accountType: str
    coin: Optional[str]
