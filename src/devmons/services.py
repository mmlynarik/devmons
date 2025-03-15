from httpx import AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

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
    coin: CGCoinCreate, repo: CGCoinRepository, session: AsyncSession, client: AsyncClient
) -> list[CGCoin]:
    ids = await get_coin_ids_from_symbol(client, coin.symbol)
    coins = await get_coins_data(client, ids)
    exists = await repo.exists(coin.symbol)
    if not exists:
        for c in coins:
            await repo.add(c)
        await session.commit()
        return coins

    raise CoinAlreadyExists(f"Symbol {coin.symbol} already exists in the database")


async def get_coins(symbol: str, repo: CGCoinRepository) -> list[CGCoin]:
    coins = await repo.get_by_symbol(symbol)
    if not coins:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    return coins


async def delete_coin(id: str, repo: CGCoinRepository, session: AsyncSession):
    coin = await repo.get_by_id(id)
    if not coin:
        raise CoinNotFound(f"Coin with id {id} not found in database")
    await repo.delete(id)
    await session.commit()


async def update_coin(
    id: str, new_coin_values: CGCoinUpdate, repo: CGCoinRepository, session: AsyncSession
) -> CGCoin:
    current_coin = await repo.get_by_id(id)
    if not current_coin:
        raise CoinNotFound(f"Coin with id {id} not found in database")

    for attr in new_coin_values.__dict__:
        setattr(current_coin, attr, getattr(new_coin_values, attr))

    await session.commit()
    return current_coin


async def refresh_coins(repo: CGCoinRepository, session: AsyncSession, client: AsyncClient):
    current_coins = await repo.list()
    if not current_coins:
        return

    ids = [c.id for c in current_coins]
    refreshed_coins: list[CGCoin] = await get_coins_data(client, ids)
    await session.execute(
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
    await session.commit()
