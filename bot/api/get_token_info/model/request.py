from pydantic import BaseModel

class GetTokenInfoRequest(BaseModel):
    symbol: str
    category: str
