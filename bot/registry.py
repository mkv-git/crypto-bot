import time
import random
from decimal import *
from pprint import pprint

from api.get_token_info.service import GetTokenInfoService
from api.get_token_data.service import GetTokenDataService
from api.get_wallet_balance.service import GetWalletBalanceService
from api.get_positions.service import GetPositionsService
from api.set_leverage.service import SetLeverageService
from api.place_order.service import PlaceOrderService
from api.get_orders.service import GetOrdersService
from api.get_closed_pnl.service import GetClosedPnlService
from api.get_order_history.service import GetOrderHistoryService
from api.cancel_all_orders.service import CancelAllOrdersService
from api.cancel_order.service import CancelOrderService
from api.change_order.service import ChangeOrderService
from api.set_trading_stop.service import SetTradingStopService
from api.change_margin.service import ChangeMarginService
#from config.auth_conf import DEMO_KEY as API_KEY, DEMO_SECRET as API_SECRET
from config.auth_conf import TESTNET_API_KEY as API_KEY, TESTNET_API_SECRET as API_SECRET


DEMO = False
TESTNET = True

rest_services_registry = {
    "get_token_info": GetTokenInfoService,
    "get_token_data": GetTokenDataService,
    "get_wallet_balance": GetWalletBalanceService,
    "get_positions": GetPositionsService,
    "set_leverage": SetLeverageService,
    "get_orders": GetOrdersService,
    "get_order_history": GetOrderHistoryService,
    "get_closed_pnl": GetClosedPnlService,
    "place_order": PlaceOrderService,
    "change_order": ChangeOrderService,
    "cancel_order": CancelOrderService,
    "cancel_all_orders": CancelAllOrdersService,
    "set_trading_stop": SetTradingStopService,
    "change_margin": ChangeMarginService,
    "toggle_auto_margin": "",
}


def test_get_token_info():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {"category": "linear", "symbol": "BTCUSDT"},
    }

    obj = rest_services_registry["get_token_info"]
    return obj().process(params)


def test_get_token_data():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {"category": "linear", "symbol": "BTCUSDT"},
    }

    obj = rest_services_registry["get_token_data"]
    return obj().process(params)


def test_get_wallet_balance():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {"accountType": "UNIFIED", "coin": "USDT"},
    }

    obj = rest_services_registry["get_wallet_balance"]
    return obj().process(params)


def test_get_positions():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {"category": "linear", "symbol": "BTCUSDT"},
    }

    obj = rest_services_registry["get_positions"]
    return obj().process(params)


def test_set_leverage():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "buyLeverage": str(random.randint(1, 12)),
            "sellLeverage": str(random.randint(1, 12)),
        },
    }

    obj = rest_services_registry["set_leverage"]
    return obj().process(params)


def test_place_order(order_link_id='', price=90000):
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "side": "Buy",
            "qty": "0.01",
            "price": price,
            "order_type": "Limit",
            "position_type": 1,
            "order_link_id": order_link_id,
        },
    }

    obj = rest_services_registry["place_order"]
    return obj().process(params)


def test_get_orders():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "open_only": 1,
        },
    }

    obj = rest_services_registry["get_orders"]
    return obj().process(params)


def test_cancel_all_orders():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
        },
    }

    obj = rest_services_registry["cancel_all_orders"]
    return obj().process(params)


def test_get_closed_pnl():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "limit": 10,
            "category": "linear",
            "symbol": "BTCUSDT",
        },
    }

    obj = rest_services_registry["get_closed_pnl"]
    return obj().process(params)


def test_cancel_order(order_link_id=''):
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "order_link_id": order_link_id,
        },
    }

    obj = rest_services_registry["cancel_order"]
    return obj().process(params)


def test_order_history(order_link_id=''):
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "order_link_id": order_link_id,
        },
    }

    obj = rest_services_registry["get_order_history"]
    return obj().process(params)


def test_change_order(order_link_id=''):
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "order_link_id": order_link_id,
            "price": "90052",
        },
    }

    obj = rest_services_registry["change_order"]
    return obj().process(params)


def test_change_margin():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            'position_type': 1,
            'margin': '30',
        },
    }

    obj = rest_services_registry["change_margin"]
    return obj().process(params)


def test_set_trading_stop():
    params = {
        "demo": DEMO,
        'testnet': TESTNET,
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "payload": {
            "category": "linear",
            "symbol": "BTCUSDT",
            "tpsl_mode": "Partial",
            "tp_order_type": "Limit",
            "position_type": 1,
            "take_profit": "100000",
            "take_profit_price": "100000",
            "take_profit_qty": "0.02",
            "tp_trigger_by": "Indexprice",
        },
    }

    obj = rest_services_registry["set_trading_stop"]
    return obj().process(params)


# for error 'payload': {'category': 'linera', 'symbol': 'BTCUSDT'}
def main():
    DEMO = False
    TESTNET = True
    obj = test_get_positions()
    #obj = test_place_order('kamaluga')
    #obj = test_change_order('kamaluga')
    #obj = test_set_leverage()
    obj = test_get_orders()
    obj = test_cancel_all_orders()
    #obj = test_cancel_order('kamaluga')
    obj = test_order_history('kamaluga')
    obj = test_get_closed_pnl()
    #obj = test_set_trading_stop()
    obj = test_get_token_info()
    obj = test_get_token_data()
    #obj = test_get_wallet_balance()

    #obj = test_change_margin()
    print(obj)
    print()
    pprint(obj.data.model_dump())


if __name__ == "__main__":
    main()
