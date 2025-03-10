from dataclasses import dataclass
from datetime import datetime

import requests

from devmons.settings import CG_API_URL, VS_CURRENCY


@dataclass
class CGCoin:
    id: str
    name: str
    symbol: str
    current_price: float
    market_cap: float
    circulating_supply: float
    total_supply: float
    max_supply: float
    last_updated: datetime  # needs fix to be treated as timestamp


@dataclass
class CGCoinCreate:
    symbol: str


@dataclass
class CGCoinUpdate:
    name: str
    symbol: str
    current_price: float
    market_cap: float
    circulating_supply: float
    total_supply: float
    max_supply: float
    last_updated: datetime


class InvalidCoinSymbol(Exception):
    pass


class CoinAlreadyExists(Exception):
    pass


class CoinNotFound(Exception):
    pass


def get_coin_ids_from_symbol(symbol: str) -> list[str]:
    url = CG_API_URL + "/coins/list"
    res: list[dict] = requests.get(url).json()
    ids = []
    for coin in res:
        if coin["symbol"] == symbol:
            ids.append(coin["id"])
    if not ids:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    return ids


def get_coins_data(ids: list[str], vs_currency: str = VS_CURRENCY) -> list[CGCoin]:
    ids_string = ", ".join(ids)
    url = CG_API_URL + f"/coins/markets?ids={ids_string}&vs_currency={vs_currency}"
    res: list[dict] = requests.get(url).json()
    coins = []
    for coin in res:
        coins.append(
            CGCoin(
                id=coin["id"],
                name=coin["name"],
                symbol=coin["symbol"],
                current_price=coin["current_price"],
                market_cap=coin["market_cap"],
                circulating_supply=coin["circulating_supply"],
                total_supply=coin["total_supply"],
                max_supply=coin["max_supply"],
                last_updated=coin["last_updated"],
            )
        )
    return coins
