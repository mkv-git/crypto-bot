import sys
import json
import argparse
import datetime
import subprocess
from decimal import *
from pprint import pprint

from utils.classifiers import Bots
from db.position_orders import PositionOrders


def create_args_parser():
    parser = argparse.ArgumentParser(prog="CryptoBot")
    parser.add_argument("-b", "--bot", required=True)
    parser.add_argument("-t", "--token", required=True)
    parser.add_argument("-sp", "--start_price", type=Decimal)
    parser.add_argument("-l", "--leverage", type=int, default=5)
    parser.add_argument("-sv", "--start_value", type=int, default=50)
    parser.add_argument("-cv", "--chunk_value", type=int, default=20)

    args = parser.parse_args()
    return args


def create_order():
    args = create_args_parser()
    print()

    bot = args.bot
    token = args.token.upper()
    order = token.rstrip("USDT").lower()

    token_orders = PositionOrders.get_by_token(token)
    if not token_orders:
        order_name = f"{order}_{bot}_1"
    else:
        last_idx = max([int(x.order_name.rsplit("_")[2]) for x in token_orders])
        order_name = f"{order}_{bot}_{last_idx+1}"

    chunk_orders = {
        "max_cnt": 5,
        "allowed": True,
        "chunk_value": args.chunk_value,
        "price_percent": 1,
        "chunk_sell_percent": 80,
        "chunk_sell_activation_percent": 1,
        "chunk_sell_retracement_percent": 1,
    }

    payload = {
        "bot": bot,
        "order_name": order_name,
        "token": token,
        "add_ts": datetime.datetime.now(),
        "is_active": True,
        "leverage": args.leverage,
        "start_value": args.start_value,
        "chunk_orders": chunk_orders,
    }
    if args.start_price:
        payload["start_price"] = args.start_price
    pprint(payload)
    print()
    accept = input("Correct (y/N)?: ")

    if accept.lower() == "y":
        PositionOrders.insert(payload)

        print(order_name)
        subprocess.run(["python", "futures.py", order_name], check=True)


if __name__ == "__main__":
    create_order()
