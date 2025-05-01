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
from devmons.repository import CGCoinRepository, UsersRepository
from devmons.users import User, UserAlreadyExists, UserCreate, UserCreated


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


async def get_user_by_email(email: str, repo: UsersRepository) -> User | None:
    return await repo.get_by_email(email=email)


async def get_user_by_id(id: int, repo: UsersRepository) -> User | None:
    return await repo.get_by_id(id=id)


async def get_user_by_github_id(github_id: int, repo: UsersRepository) -> User | None:
    return await repo.get_by_github_id(github_id=github_id)


async def register_user_by_email(
    user_create: UserCreate, repo: UsersRepository, session: AsyncSession
) -> UserCreated:
    existing_user = await get_user_by_email(user_create.email, repo=repo)
    if existing_user:
        raise UserAlreadyExists
    user = User(
        id=None,
        email=user_create.email,
        password=user_create.password,
        salt=user_create.salt,
        github_id=None,
        github_name=None,
    )
    await repo.add(user=user)
    await session.commit()
    await session.refresh(user)
    return UserCreated(user.id)


async def register_user_by_github(
    user_create: UserCreate, repo: UsersRepository, session: AsyncSession
) -> UserCreated:
    existing_user = await get_user_by_github_id(user_create.github_id, repo=repo)
    if existing_user:
        raise UserAlreadyExists
    user = User(
        id=None,
        email=None,
        password=None,
        salt=None,
        github_id=user_create.github_id,
        github_name=user_create.github_name,
    )
    await repo.add(user=user)
    await session.commit()
    await session.refresh(user)
    return UserCreated(user.id)
