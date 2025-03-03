from collections import defaultdict
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


def get_coins_data(symbol: str) -> list[CGCoin]:
    url = CG_API_URL + "/coins/list"
    res: list[dict] = requests.get(url).json()
    coins = defaultdict(list)
    for coin in res:
        coins[coin["symbol"]].append(CGCoin(**coin))

    return coins[symbol]
