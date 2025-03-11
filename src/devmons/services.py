from httpx import AsyncClient
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


async def add_coins(
    coin: CGCoinCreate, repo: CGCoinRepository, session: Session, client: AsyncClient
) -> list[CGCoin]:
    ids = await get_coin_ids_from_symbol(client, coin.symbol)
    coins = await get_coins_data(client, ids)
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


def update_coin(id: str, new_coin_values: CGCoinUpdate, repo: CGCoinRepository, session: Session) -> CGCoin:
    current_coin = repo.get_by_id(id)
    if not current_coin:
        raise CoinNotFound(f"Coin with id {id} not found in database")

    for attr in new_coin_values.__dict__:
        setattr(current_coin, attr, getattr(new_coin_values, attr))

    session.commit()
    return current_coin


async def refresh_coins(repo: CGCoinRepository, session: Session, client: AsyncClient):
    current_coins = repo.list()
    if not current_coins:
        return

    ids = [c.id for c in current_coins]
    refreshed_coins: list[CGCoin] = await get_coins_data(client, ids)
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
