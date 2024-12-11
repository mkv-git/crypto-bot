from enum import IntEnum, StrEnum


class OrderSideTypes(StrEnum):
    BUY = "Buy"
    SELL = "Sell"


class PriceAlertTypes(StrEnum):
    TRACK_CHUNK_TS_ORDER = "TrackChunTSOrder"
    TRACK_ACTIVE_CHUNK_TS_ORDER = "TrackActiveChunkTSOrder"


class TpSlModes(StrEnum):
    FULL = "Full"
    PARTIAL = "Partial"


class TriggerTypes(StrEnum):
    LAST_PRICE = "LastPrice"
    MARK_PRICE = "MarkPrice"
    INDEX_PRICE = "IndexPrice"


class OrderTypes(StrEnum):
    LIMIT = "Limit"
    MARKET = "Market"


class CreateTypes(StrEnum):
    CREATE_BY_PARTIAL_STOP_LOSS = "CreateByPartialStopLoss"


class StopOrderTypes(StrEnum):
    STOP = "Stop"
    STOP_LOSS = "StopLoss"
    TAKE_PROFIT = "TakeProfit"
    TRAILING_STOP = "TrailingStop"
    PARTIAL_STOP_LOSS = "PartialStopLoss"
    PARTIAL_TAKE_PROFIT = "PartialTakeProft"


class OrderStatuses(StrEnum):
    NEW = "New"
    FILLED = "Filled"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"
    PARTIALLY_FILLED = "PartiallyFilled"


class Bots(StrEnum):
    DEMO = "demo"
    TESTNET = "testnet"


class ServiceStatus(StrEnum):
    ERROR = "error"
    SUCCESS = "success"


class OrdersCategories(StrEnum):
    SPOT = "spot"
    FUTURES = "linear"


class TrailingStopActivators(StrEnum):
    ROI = "roi"
    PRICE = "last_mark_price"
    CHUNK = "last_chunk_sell_price_percent"


class HedgeTypes(IntEnum):
    LONG = 1
    SHORT = 2


class BybitErrors(IntEnum):
    ORDER_NOT_EXISTS = 110001
    INTERNAL_SYSTEM_ERROR = 10016
    LEVERAGE_NOT_MODIFIED = 110043
    DUPLICATE_ORDER_LINK_ID = 110072
    AUTO_ADD_MARGIN_NOT_MODIFIED = 10001
