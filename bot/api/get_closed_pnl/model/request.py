from pydantic import BaseModel


class GetClosedPnlRequest(BaseModel):
    limit: int
    symbol: str
    category: str
