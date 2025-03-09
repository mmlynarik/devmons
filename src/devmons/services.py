from sqlalchemy import update
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
    coins = get_coins_data(ids)
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


def delete_coin(id: str, repo: CGCoinRepository, session: Session):
    coin = repo.get_by_id(id)
    if not coin:
        raise CoinNotFound(f"Coin with id {id} not found in database")
    repo.delete(id)
    session.commit()


def update_coin(id: str, coin: CGCoinUpdate, repo: CGCoinRepository, session: Session) -> CGCoin:
    current_coin = repo.get_by_id(id)
    if not current_coin:
        raise CoinNotFound(f"Coin with id {id} not found in database")

    for attr in coin.__dict__:
        setattr(current_coin, attr, getattr(coin, attr))

    session.commit()
    return current_coin


def refresh_coins(repo: CGCoinRepository, session: Session):
    current_coins = repo.list()
    if not current_coins:
        return

    refreshed_coins = get_coins_data([c.id for c in current_coins])
    session.execute(
        update(CGCoin),
        [
            {
                "id": c.id,
                "current_price": c.current_price,
                "market_cap": c.market_cap,
                "circulating_supply": c.circulating_supply,
                "total_supply": c.total_supply,
                "max_supply": c.max_supply,
                "last_updated": c.last_updated,
            }
            for c in refreshed_coins
        ],
    )
    session.commit()
