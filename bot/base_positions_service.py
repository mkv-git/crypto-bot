import os
import time
import datetime
from decimal import *
from pprint import pprint

from pybit.unified_trading import WebSocket, HTTP, WebSocketTrading

from utils.logger import log
from utils.classifiers import ServiceStatus, Bots, BybitErrors
from api.get_orders.service import GetOrdersService
from api.place_order.service import PlaceOrderService
from api.cancel_order.service import CancelOrderService
from api.change_order.service import ChangeOrderService
from api.set_leverage.service import SetLeverageService
from api.get_positions.service import GetPositionsService
from api.change_margin.service import ChangeMarginService
from api.get_token_info.service import GetTokenInfoService
from api.get_token_data.service import GetTokenDataService
from api.get_closed_pnl.service import GetClosedPnlService
from api.set_trading_stop.service import SetTradingStopService
from api.get_order_history.service import GetOrderHistoryService
from api.cancel_all_orders.service import CancelAllOrdersService
from api.get_wallet_balance.service import GetWalletBalanceService


class BasePositionsService:
    def __init__(self, order_name, bot):
        if bot not in [x.value for x in Bots]:
            log.error(f'Unknown bot: "{bot}", aborting...')
            return

        self.bot = bot
        self.vault = {}
        self.token = None
        self.category = self.CATEGORY
        self.demo = True if bot == "demo" else False
        self.testnet = True if bot == "testnet" else False
        self.order_name = order_name
        self.main_order_done = False
        self.order_finalized = False
        self.order_terminated = False
        self.long_position_info = None
        self.short_position_info = None

        if not self._load_api_secrets():
            log.error("Failed to load api secrets")
            raise

    def _load_api_secrets(self):
        self.api_key = os.getenv(f"{self.bot.upper()}_API_KEY")
        self.api_secret = os.getenv(f"{self.bot.upper()}_API_SECRET")
        return self.api_key and self.api_secret

    def init_ws(self):
        self.public_ws = WebSocket(
            testnet=self.testnet,
            channel_type=self.CATEGORY,
        )

        self.private_ws = WebSocket(
            demo=self.demo,
            testnet=self.testnet,
            channel_type="private",
            api_key=self.api_key,
            api_secret=self.api_secret,
        )

        # self.trade_ws = WebSocketTrading(
        #    demo=self.demo,
        #    testnet=self.testnet,
        #    api_key=self.api_key,
        #    api_secret=self.api_secret,
        # )

    def convert_ts(self, in_val):
        return datetime.datetime.fromtimestamp(in_val / 1000)

    def calc_percentage(self, in_val, percent):
        return Decimal(in_val * Decimal((100 + percent) / 100))

    def validate_price(self, price, rounding=ROUND_DOWN):
        if float(self.price_precision) < 1:
            price = Decimal(price).quantize(Decimal(str(self.price_precision)), rounding=rounding)
        return Decimal(price)

    def validate_quantity(self, quantity, rounding=ROUND_DOWN):
        if float(self.quantity_precision) < 1:
            quantity = Decimal(quantity).quantize(
                Decimal(str(self.quantity_precision)), rounding=ROUND_DOWN
            )
        else:
            quantity = int(
                round(int(quantity / int(self.quantity_precision)), 2)
                * int(self.quantity_precision)
            )

        return quantity

    def generate_id(self, row, direction, stage=0):
        return "{}-{}-{}-{}-{}-{}".format(
            self.order_name,
            row,
            self.CATEGORY,
            direction,
            stage,
            self.position_order_id,
        )

    def make_api_query(self, obj, payload=None, default_values=True):
        params = {
            "demo": self.demo,
            "testnet": self.testnet,
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "payload": {},
        }
        if payload:
            params["payload"] = payload
        if default_values:
            params["payload"].update(
                {
                    "symbol": self.token,
                    "category": self.category,
                }
            )
        return obj().process(params)

    def set_token_info(self):
        res = self.make_api_query(GetTokenInfoService)
        data = res.data.result

        if res.status == ServiceStatus.ERROR:
            log.error(f"ERR: {res.data.result}")
            return

        self.price_precision = data.price_precision
        self.max_leverage = data.max_leverage
        self.min_order_qty = data.min_order_qty
        self.quantity_precision = data.qty_precision
        self.max_order_qty = data.max_order_qty
        return True

    def get_active_order(self, order_link_id=None, order_id=None):
        payload = {
            "order_id": order_id,
            "order_link_id": order_link_id,
        }

        res = self.make_api_query(GetOrdersService, payload)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to get active orders: {res.data.result}")

        return res

    def get_order_history(self, order_link_id=None, order_id=None):
        payload = {
            "order_id": order_id,
            "order_link_id": order_link_id,
        }

        res = self.make_api_query(GetOrderHistoryService, payload)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to get order history: {res.data.result}")

        return res

    def load_token_data(self):
        res = self.make_api_query(GetTokenDataService)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to load token data: {res.data.result}")

        return res

    def load_wallet_balance(self):
        payload = {"accountType": "UNIFIED", "coin": "USDT"}
        res = self.make_api_query(GetWalletBalanceService, payload)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to load wallet balance: {res.data.result}")

        return res

    def set_leverage(self, leverage):
        payload = {
            "buy_leverage": leverage,
            "sell_leverage": leverage,
        }
        res = self.make_api_query(SetLeverageService, payload)
        if (
            res.status == ServiceStatus.ERROR
            and res.data.status_code != BybitErrors.LEVERAGE_NOT_MODIFIED
        ):
            log.error(f"Failed to set leverage: {res.data.result}")

        return res

    def load_positions_data(self):
        res = self.make_api_query(GetPositionsService)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to load positions data: {res.data.result}")

        return res

    def place_order(self, payload):
        res = self.make_api_query(PlaceOrderService, payload)
        if res.status == ServiceStatus.ERROR:
            if res.data.status_code == BybitErrors.INTERNAL_SYSTEM_ERROR:
                time.sleep(0.5)
                log.error(f"{res}")
                return self.place_order(payload)
            else:
                log.error(f"Failed to place order: {res.data.result}")

        return res

    def change_order(self, payload):
        res = self.make_api_query(ChangeOrderService, payload)
        if res.status == ServiceStatus.ERROR:
            if res.data.status_code == BybitErrors.INTERNAL_SYSTEM_ERROR:
                time.sleep(0.5)
                log.error(f"{res}")
                return self.change_order(payload)
            else:
                log.error(f"Failed to change order: {res.data.result}")

        return res

    def cancel_order(self, payload):
        res = self.make_api_query(CancelOrderService, payload)

        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to cancel order: {res.data.result}")

        return res

    def get_closed_pnl(self, limit=10):
        payload = {"limit": limit}
        res = self.make_api_query(GetClosedPnlService, payload)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to get closed pnl: {res.data.result}")

        return res

    def cancel_all_orders(self):
        res = self.make_api_query(CancelAllOrdersService)
        if res.status == ServiceStatus.ERROR:
            log.error(f"Failed to cancel all orders: {res.data.result}")

        return res

    def set_trading_stop(self, payload):
        res = self.make_api_query(SetTradingStopService, payload)
        if res.status == ServiceStatus.ERROR:
            if res.data.status_code == BybitErrors.INTERNAL_SYSTEM_ERROR:
                time.sleep(0.5)
                log.error(f"{res}")
                return self.set_trading_stop(payload)
            else:
                log.error(f"Failed to set trading stop service: {res.data.result}")

        return res
