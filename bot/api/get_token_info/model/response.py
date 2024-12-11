from decimal import *

from pydantic import BaseModel, Field

from api.base.model.response import BybitBaseResponse


class TokenInfoData(BaseModel):
    max_leverage: Decimal = Field(alias='maxLeverage')
    min_order_qty: Decimal = Field(alias='minOrderQty')
    max_order_qty: Decimal = Field(alias='maxMktOrderQty')
    qty_precision: Decimal = Field(alias='qtyStep')
    price_precision: Decimal = Field(alias='tickSize')


class GetTokenInfoResponse(BybitBaseResponse):
    result: TokenInfoData
