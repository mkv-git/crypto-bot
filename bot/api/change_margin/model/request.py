from pydantic import BaseModel, Field


class ChangeMarginRequest(BaseModel):
    margin: str
    symbol: str
    category: str
    positionIdx: int = Field(alias="position_type")
