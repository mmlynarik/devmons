from dataclasses import dataclass
from datetime import datetime

from httpx import AsyncClient

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
    last_updated: datetime


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


async def get_coin_ids_from_symbol(client: AsyncClient, symbol: str) -> list[str]:
    url = "/coins/list"
    res = await client.get(url)
    ids = []
    for coin in res.json():
        if coin["symbol"] == symbol:
            ids.append(coin["id"])
    if not ids:
        raise InvalidCoinSymbol(f"Symbol {symbol} does not exist")
    return ids


async def get_coins_data(client: AsyncClient, ids: list[str], vs_currency: str = VS_CURRENCY) -> list[CGCoin]:
    ids_string = ", ".join(ids)
    url = "/coins/markets"
    res = await client.get(url, params={"ids": ids_string, "vs_currency": vs_currency})
    coins = []
    for coin in res.json():
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
