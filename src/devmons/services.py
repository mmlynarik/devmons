from sqlalchemy.orm import Session

from devmons.coingecko import (
    CGCoin,
    CGCoinCreate,
    CGCoinUpdate,
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
    coins = repo.get_by_symbol(symbol)
    if not coins:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    return coins


def delete_coins(symbol: str, repo: CGCoinRepository, session: Session):
    coins = repo.get_by_symbol(symbol)
    if not coins:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    repo.delete(symbol)
    session.commit()


def update_coin(id_: str, coin: CGCoinUpdate, repo: CGCoinRepository, session: Session) -> CGCoin:
    current_coin = repo.get_by_id(id_)
    if not current_coin:
        raise CoinNotFound(f"Symbol with id {id_} not found in database")

    for attr in coin.__dict__:
        setattr(current_coin, attr, getattr(coin, attr))

    session.commit()
    return current_coin
