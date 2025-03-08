from sqlalchemy.orm import Session

from devmons.coingecko import (
    CGCoin,
    CGCoinCreate,
    CoinAlreadyExists,
    CoinNotFound,
    get_coin_ids_from_symbol,
    get_coins_data,
)
from devmons.repository import CGCoinRepository


def add_coins(coin: CGCoinCreate, repo: CGCoinRepository, session: Session) -> list[CGCoin]:
    ids = get_coin_ids_from_symbol(coin.symbol)
    coins = get_coins_data(ids, coin.vs_currency)
    if not repo.exists(coin.symbol):
        for c in coins:
            repo.add(c)
        session.commit()
        return coins
    raise CoinAlreadyExists(f"Symbol {coin.symbol} already exists in the database")


def get_coins(symbol: str, repo: CGCoinRepository) -> list[CGCoin]:
    coins = repo.get(symbol)
    if not coins:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    return coins


def delete_coins(symbol: str, repo: CGCoinRepository, session: Session):
    repo.delete(symbol)
    session.commit()
