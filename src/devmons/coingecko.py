import requests
from pydantic import BaseModel

from devmons.settings import CG_API_URL


class CGCoin(BaseModel):
    id: str
    name: str
    symbol: str


def verify_coin_symbol(symbol: str) -> bool:
    url = CG_API_URL + "/coins/list"
    res = requests.get(url).json()
    api_symbols = {coin["symbol"] for coin in res}
    return symbol in api_symbols
