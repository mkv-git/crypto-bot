from pydantic import BaseModel


class GetTokenDataRequest(BaseModel):
    symbol: str
    category: str
