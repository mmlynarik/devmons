from dataclasses import dataclass

import requests

from devmons.settings import CG_API_URL


@dataclass
class CGCoin:
    id: str
    name: str
    symbol: str


@dataclass
class CGCoinCreate:
    symbol: str


class InvalidCoinSymbol(Exception):
    pass


def get_coins_data(symbol: str) -> list[CGCoin]:
    url = CG_API_URL + "/coins/list"
    res: list[dict] = requests.get(url).json()
    coins = []
    for coin in res:
        if coin["symbol"] == symbol:
            coins.append(CGCoin(**coin))

    if not coins:
        raise InvalidCoinSymbol(f"Symbol {symbol} is not a valid coin.")
    return coins
