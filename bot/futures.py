import os
import sys
import time
import datetime
from decimal import *
from pprint import pprint
from dataclasses import asdict

from utils.logger import log
from db.chunk_orders import ChunkOrders
from models.vault_item import VaultItem
from db.position_orders import PositionOrders
from base_positions_service import BasePositionsService
from ws.models.request.place_order import PlaceOrderRequest
from ws.models.request.change_order import ChangeOrderRequest
from ws.models.request.cancel_order import CancelOrderRequest
from ws.models.response.order_stream import OrderStreamResponse
from ws.models.response.token_stream import TokenStreamResponse
from ws.models.response.order_process import OrderProcessResponse
from ws.models.response.wallet_stream import WalletStreamResponse
from ws.models.response.position_stream import PositionStreamResponse
from api.get_orders.model.response import OrdersData as OrdersResponseData
from utils.classifiers import (
    Bots,
    TpSlModes,
    HedgeTypes,
    OrderTypes,
    BybitErrors,
    CreateTypes,
    TriggerTypes,
    OrderStatuses,
    ServiceStatus,
    StopOrderTypes,
    OrderSideTypes,
    PriceAlertTypes,
    OrdersCategories,
    TrailingStopActivators,
)

START_PRICE_MAX_DIFF_PERCENT = 20


class FuturesService(BasePositionsService):
    CATEGORY = OrdersCategories.FUTURES

    def __init__(self, *args, **kwargs):
        s = super().__init__(*args, **kwargs)

        self.order = None
        self.vault = {}
        self.wallet = None

        self.buy_orders = {}
        self.sell_orders = {}
        self.price_alerts = {}

        self.mark_price = None
        self.order_closed = False
        self.long_position = None
        self.short_position = None
        self.main_order_done = False
        self.order_terminated = False

        if not self.load_position_order():
            log.error("Order not found")
            self.order_closed = True
            return

        if not self.set_token_info():
            log.error("Missing token (%s) info" % (self.token))
            return

        self.order_link_id = self.generate_id("init", "buy")

        self.validate_main_order()
        if self.order_closed:
            return

        self.init_ws()
        self.subscribe_to_ws()
        log.debug("Websocket initiated")

        if not self.order.order_id:
            if not self.init_trading():
                log.error("Failed to init trading")
                return

        self.init_vault()

    def update_wallet_balance(self):
        wallet_data = self.load_wallet_balance()
        if wallet_data.status == ServiceStatus.ERROR:
            self.wallet = None
            return

        self.wallet = wallet_data.data.result

    def load_position_order(self):
        self.order = PositionOrders.get_order(self.order_name)
        if not self.order:
            log.error('No active order with name: "%s" found' % (self.order_name))
            return False

        self.bot = self.order.bot
        self.token = self.order.token
        self.position_order_id = self.order.id
        if self.order.buy_ts:
            self.main_order_done

        return True

    def get_order_data(self, order_id: str | None = None, order_link_id: str | None = None):
        order = self.get_active_order(order_link_id, order_id)
        if order.status == ServiceStatus.ERROR:
            return order

        if not order.data.result:
            order = self.get_order_history(order_link_id, order_id)

        return order

    def validate_main_order(self):
        if not self.order.order_id:
            return

        order_data = self.get_order_data(order_link_id=self.order_link_id)
        if order_data.status == ServiceStatus.ERROR or not order_data.data.result:
            return

        self.check_main_order(order_data.data.result)
        self.set_position_data()

        if not self.long_position:
            self.order_closed = True

        if self.long_position.size == 0 and not self.long_position.position_value:
            self.terminate_main_order()

    def check_main_order(self, in_val):
        if in_val.order_link_id != self.order_link_id:
            return

        if in_val.order_status == OrderStatuses.NEW:
            db_update_payload = {
                "status": OrderStatuses.NEW,
                "order_id": in_val.order_id,
                "start_qty": in_val.qty,
                "start_price": in_val.price,
                "order_link_id": self.order_link_id,
                "modified_ts": self.convert_ts(in_val.updated_time),
            }

            self.update_main_order(db_update_payload)
        elif in_val.order_status == OrderStatuses.FILLED:
            db_update_payload = {
                "order_id": in_val.order_id,
                "status": OrderStatuses.FILLED,
                "start_qty": in_val.qty,
                "buy_price": in_val.price,
                "order_link_id": self.order_link_id,
                "buy_ts": self.convert_ts(in_val.created_time),
                "modified_ts": self.convert_ts(in_val.updated_time),
            }

            self.update_main_order(db_update_payload)
            self.main_order_done = True
            self.load_position_order()
            log.info(f"Order {self.order_name} done.")
        elif in_val.order_status == OrderStatuses.CANCELLED:
            log.info(f"Order {self.order_name} cancelled.")
            self.terminate_main_order(True)

    def terminate_main_order(self, cancelled=False):
        now = datetime.datetime.now()
        payload = {
            "is_active": False,
            "modified_ts": now,
            "end_ts": datetime.datetime.now(),
        }
        if cancelled:
            self.order_terminated = True
            payload["status"] = OrderStatuses.CANCELLED
            payload["is_terminated"] = True

        PositionOrders.update({"id": self.position_order_id}, payload)
        self.cancel_all_orders()
        self.order_closed = True

    def update_main_order(self, payload):
        PositionOrders.update({"id": self.position_order_id}, payload)

    def validate_chunk_order(self, in_val, vault_item: VaultItem):
        if not in_val:
            self.terminate_chunk_order(vault_item.order_row_id)
            return

        order_type = in_val.side.lower()
        order_ts = f"{order_type}_ts"

        db_update_payload = {
            f"{order_type}_status": in_val.order_status,
            "modified_ts": self.convert_ts(in_val.updated_time),
        }

        if in_val.order_status == OrderStatuses.NEW:
            pass
        elif in_val.order_status == OrderStatuses.FILLED:
            created_ts = self.convert_ts(in_val.created_time)
            setattr(vault_item, order_ts, created_ts)
            db_update_payload.update(
                {
                    order_ts: created_ts,
                }
            )
        elif in_val.order_status == OrderStatuses.CANCELLED:
            self.terminate_chunk_order(vault_item.order_row_id)
            return False

        ChunkOrders.update({"id": vault_item.id}, db_update_payload)

        return True

    def terminate_chunk_order(self, vault_id):
        vault_obj = self.vault[vault_id]

        db_update_payload = {
            "is_active": False,
            "modified_ts": datetime.datetime.now(),
        }

        if not vault_obj.buy_ts:
            db_update_payload["buy_status"] = OrderStatuses.CANCELLED
        if not vault_obj.sell_ts:
            db_update_payload["sell_status"] = OrderStatuses.CANCELLED

        if vault_obj.buy_order_id in self.buy_orders:
            del self.buy_orders[vault_obj.buy_order_id]
        if vault_obj.sell_order_id in self.sell_orders:
            del self.sell_orders[vault_obj.sell_order_id]

        log.info(f"Terminating chunk order, ID: {vault_obj.id}")
        ChunkOrders.update({"id": vault_obj.id}, db_update_payload)
        self.reset_vault_item(vault_obj)

    def reset_vault_item(self, vault_item: VaultItem):
        vault_obj = self.vault[vault_item.order_row_id]
        vault_obj.is_active = False
        vault_obj.buy_ts = None
        vault_obj.buy_order_id = None
        vault_obj.buy_order_link_id = None
        vault_obj.sell_ts = None
        vault_obj.sell_order_id = None
        vault_obj.sell_order_link_id = None

    def subscribe_to_ws(self):
        self.public_ws.ticker_stream(symbol=self.token, callback=self.handle_token_stream)
        self.private_ws.position_stream(callback=self.handle_position_stream)
        self.private_ws.order_stream(callback=self.handle_order_stream)
        self.private_ws.wallet_stream(callback=self.handle_wallet_stream)

    def handle_token_stream(self, msg):
        try:
            token_data = TokenStreamResponse.model_validate(msg)
            self.mark_price = token_data.data.mark_price
        except Exception as err:
            print(f"{err}")
            return

        if self.price_alerts:
            try:
                self.handle_price_alerts()
            except Exception as err:
                print(f"{err}")

    def handle_wallet_stream(self, msg):
        try:
            obj = msg
            obj["data"] = msg["data"][0]["coin"][0]
            self.wallet = WalletStreamResponse.model_validate(msg).data
        except Exception as err:
            log.error(f"{err}")

    def handle_order_stream(self, msg):
        try:
            order_data = OrderStreamResponse.model_validate(msg)
            if order_data.data[0].symbol == self.token:
                self.update_orders(order_data)
        except Exception as err:
            log.error(f"{err}")

    def handle_order_process_stream(self, msg):
        try:
            OrderProcessResponse.model_validate(msg)
        except Exception as err:
            log.error(f"{err}")

    def handle_position_stream(self, msg):
        try:
            position_data = PositionStreamResponse.model_validate(msg)
            for pd in position_data.data:
                if pd.position_type == HedgeTypes.LONG:
                    self.long_position = pd
                elif pd.position_type == HedgeTypes.SHORT:
                    self.short_position = pd

            self.update_positions()
        except Exception as err:
            log.error(f"{err}")

    def set_position_data(self):
        position_data = self.load_positions_data()
        if position_data.status == ServiceStatus.ERROR:
            return False

        for pd in position_data.data.result:
            if pd.position_type == HedgeTypes.LONG:
                self.long_position = pd
            elif pd.position_type == HedgeTypes.SHORT:
                self.short_position = pd

        return True

    def init_trading(self):
        if not self.mark_price:
            token_data = self.load_token_data()
            if token_data.status == ServiceStatus.ERROR:
                return False

            self.mark_price = token_data.data.result.mark_price

        if self.order.start_price:
            price_diff = abs(self.order.start_price / self.mark_price * 100 - 100)
            if price_diff > START_PRICE_MAX_DIFF_PERCENT:
                log.debug(
                    "Start price: %.2f, current price: %.2f"
                    % (self.order.start_price, self.mark_price)
                )
                log.error("Start price diff to current price, is too big (%.2f%%)" % (price_diff))
                return False

        if not self.wallet:
            self.update_wallet_balance()

        available_balance = self.wallet.available_balance
        if available_balance < self.order.start_value:
            log.debug(
                "Available balance: %.2f, start value: %.2f"
                % (available_balance, self.order.start_value)
            )
            log.error("Insufficient funds")
            return False

        res = self.set_leverage(self.order.leverage)

        if not self.long_position:
            self.set_position_data()

        if self.order.leverage != self.long_position.leverage:
            log.error("Leverage wasn" "t changed, aborting")
            return False

        if not self.order.start_price:
            buy_price = self.mark_price
        else:
            buy_price = self.order.start_price
        buy_price = self.validate_price(buy_price)
        qty = self.validate_quantity(self.order.start_value / buy_price * self.order.leverage)
        payload = {
            "qty": qty,
            "side": "Buy",
            "price": buy_price,
            "order_type": "Limit",
            "position_type": HedgeTypes.LONG,
            "order_link_id": self.order_link_id,
        }

        order_res = self.place_order(payload)
        if order_res.status == ServiceStatus.ERROR:
            if order_res.data.status_code == BybitErrors.DUPLICATE_ORDER_LINK_ID:
                self.check_main_order()
                if self.order_closed:
                    return False
                if self.main_order_done:
                    return True
            else:
                return False

        order_obj = order_res.data.result
        db_payload = {
            "start_qty": qty,
            "start_price": buy_price,
            "order_id": order_obj.order_id,
            "modified_ts": datetime.datetime.now(),
            "order_link_id": order_obj.order_link_id,
        }
        self.update_main_order(db_payload)
        return True

    def update_orders(self, payload):
        for pd in payload.data:
            if pd.symbol != self.token:
                continue

            if pd.order_link_id == self.order_link_id:
                self.check_main_order(pd)
            elif pd.order_id in self.buy_orders:
                vault_obj = self.buy_orders[pd.order_id]

                if pd.order_status == OrderStatuses.FILLED:
                    try:
                        self.handle_buy_chunk_order(pd)
                    except Exception as err:
                        log.exception(f"{err}")
                else:
                    self.validate_chunk_order(pd, vault_obj)
            elif pd.order_id in self.sell_orders:
                if pd.order_status != OrderStatuses.FILLED:
                    continue
                try:
                    self.handle_sell_chunk_order(pd)
                except Exception as err:
                    log.exception(f"{err}")

            elif not pd.order_link_id:
                pass  # self.handle_unknown_orders(pd)

    def handle_price_alerts(self):
        pass

    def update_positions(self):
        if self.main_order_done:
            if not self.long_position.symbol == self.token:
                return
            self.validate_main_order()

    def init_vault(self):
        fields = list(VaultItem.__dataclass_fields__.keys())
        res = ChunkOrders.load_last_state(self.position_order_id)
        if not res:
            return

        for k, obj in res.items():
            if not obj.is_active:
                continue

            dummy = {f: getattr(obj, f) for f in fields if hasattr(obj, f)}
            vault_item = VaultItem(**dummy)
            self.vault[obj.order_row_id] = vault_item

            if vault_item.buy_ts and vault_item.sell_ts:
                self.terminate_chunk_order(vault_item.order_row_id)
                continue

            buy_order_data = self.get_order_data(
                vault_item.buy_order_id, vault_item.buy_order_link_id
            )
            if buy_order_data.status == ServiceStatus.SUCCESS:
                self.validate_chunk_order(buy_order_data.data.result, vault_item)

            if vault_item.buy_ts:
                sell_order_data = self.get_order_data(
                    vault_item.sell_order_id, vault_item.sell_order_link_id
                )
                if sell_order_data.status == ServiceStatus.SUCCESS:
                    self.validate_chunk_order(sell_order_data.data.result, vault_item)

        for obj in self.vault.values():
            if not obj.is_active:
                continue

            if not obj.buy_ts:
                self.buy_orders[obj.buy_order_id] = vault_item

            if not obj.sell_ts and obj.sell_order_id:
                self.sell_orders[obj.sell_order_id] = vault_item

    def run_trader(self):
        if self.order_closed:
            log.info("Order closed, cancelling trade...")
            return

        if not self.main_order_done:
            return

        if not self.order.chunk_orders.allowed:
            return

        if not self.buy_orders:
            self.place_chunk_buy_order(0)

    def place_chunk_buy_order(self, row_id):
        if self.order_closed:
            return

        active_buy_slots = [k for k, v in self.vault.items() if v.buy_order_id]

        if len(active_buy_slots) >= self.order.chunk_orders.max_cnt:
            return

        if row_id in active_buy_slots:
            return

        if not self.order.start_price:
            self.load_position_order()

        entry_price = self.order.start_price
        chunk_value = self.order.chunk_orders.chunk_value

        if not self.wallet:
            self.update_wallet_balance()

        if self.wallet.available_balance < chunk_value:
            log.warning(f"Insufficiend balance: {self.wallet.available_balance} - {chunk_value}")
            return False

        if row_id not in self.vault:
            res = ChunkOrders.load_last_chunk_order(self.position_order_id, row_id)
            if not res:
                stage = 1
            else:
                stage = res.stage + 1
        else:
            stage = self.vault[row_id].stage + 1

        buy_order_link_id = self.generate_id(row_id, "buy", stage)
        sell_order_link_id = self.generate_id(row_id, "sell", stage)

        chunk_price_percent = self.order.chunk_orders.price_percent
        buy_price = self.validate_price(
            self.calc_percentage(entry_price, -chunk_price_percent * (row_id + 1))
        )
        buy_qty = self.validate_quantity(chunk_value / buy_price * self.order.leverage)

        if buy_price < self.long_position.entry_price:
            chunk_sell_percent = self.order.chunk_orders.chunk_sell_percent
            sell_qty = self.validate_quantity(buy_qty * chunk_sell_percent / 100, rounding=ROUND_UP)
        else:
            sell_qty = buy_qty

        sell_price = self.validate_price(self.calc_percentage(buy_price, 1))
        vault_obj = VaultItem(
            id=None,
            stage=stage,
            is_active=True,
            order_row_id=row_id,
            position_order_id=self.position_order_id,
            buy_qty=buy_qty,
            buy_price=buy_price,
            buy_order_link_id=buy_order_link_id,
            sell_qty=sell_qty,
            sell_price=sell_price,
            sell_order_link_id=sell_order_link_id,
        )

        order_payload = {
            "side": "Buy",
            "order_type": "Limit",
            "qty": buy_qty,
            "price": buy_price,
            "position_type": HedgeTypes.LONG,
            "order_link_id": buy_order_link_id,
        }
        order_res = self.place_order(order_payload)
        if order_res.status != ServiceStatus.SUCCESS:
            return False

        buy_order_id = order_res.data.result.order_id
        vault_obj.buy_order_id = buy_order_id

        self.vault[row_id] = self.buy_orders[buy_order_id] = vault_obj

        now = datetime.datetime.now()
        db_payload = asdict(vault_obj)
        db_payload.update(
            {
                "add_ts": now,
                "modified_ts": now,
            }
        )
        create_res = ChunkOrders.insert(db_payload)
        vault_obj.id = create_res.id

    def handle_buy_chunk_order(self, obj):
        vault_obj = self.buy_orders[obj.order_id]
        order_row_id = vault_obj.order_row_id
        if vault_obj.sell_order_id:
            return

        buy_order_link_id = vault_obj.buy_order_link_id
        sell_order_link_id = vault_obj.sell_order_link_id

        order_payload = {
            "side": OrderSideTypes.SELL,
            "order_type": "Limit",
            "qty": vault_obj.sell_qty,
            "price": vault_obj.sell_price,
            "position_type": HedgeTypes.LONG,
            "order_link_id": sell_order_link_id,
        }
        order_res = self.place_order(order_payload)
        if order_res.status != ServiceStatus.SUCCESS:
            return False

        sell_order_id = order_res.data.result.order_id
        vault_obj.sell_order_id = sell_order_id
        self.sell_orders[sell_order_id] = vault_obj

        db_update_payload = {
            "sell_order_id": sell_order_id,
            "modified_ts": datetime.datetime.now(),
            "buy_ts": self.convert_ts(obj.updated_time),
            "buy_status": obj.order_status,
        }
        ChunkOrders.update({"buy_order_link_id": buy_order_link_id}, db_update_payload)

        if order_row_id < self.order.chunk_orders.max_cnt:
            log.info("Creating new buy order from buy")
            self.place_chunk_buy_order(order_row_id + 1)

    def handle_sell_chunk_order(self, obj):
        sell_order_id = obj.order_id
        vault_obj = self.sell_orders[sell_order_id]
        order_row_id = vault_obj.order_row_id
        sell_order_link_id = vault_obj.sell_order_link_id

        del self.buy_orders[vault_obj.buy_order_id]
        del self.sell_orders[sell_order_id]
        self.reset_vault_item(vault_obj)

        db_update_payload = {
            "is_active": False,
            "sell_status": obj.order_status,
            "sell_ts": self.convert_ts(obj.updated_time),
        }
        ChunkOrders.update({"sell_order_link_id": sell_order_link_id}, db_update_payload)

        log.info("Creating new buy order from sell")
        self.place_chunk_buy_order(order_row_id)


if __name__ == "__main__":
    os.system("clear")
    log.info("Bot started")
    order_name = sys.argv[1]
    futures = FuturesService(order_name, Bots.DEMO)
    while not futures.order_closed:
        futures.run_trader()
        time.sleep(0.5)

    log.info("Bot finished")
