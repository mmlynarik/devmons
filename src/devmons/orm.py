from sqlalchemy import Column, DateTime, Float, Integer, String, Table
from sqlalchemy.orm import registry

from devmons.coingecko import CGCoin
from devmons.di import engine
from devmons.users import User

mapper_registry = registry()


cg_coin = Table(
    "cg_coin",
    mapper_registry.metadata,
    Column("id", String(256), primary_key=True),
    Column("name", String(256)),
    Column("symbol", String(30)),
    Column("current_price", Float),
    Column("market_cap", Float),
    Column("circulating_supply", Float),
    Column("total_supply", Float),
    Column("max_supply", Float),
    Column("last_updated", DateTime(timezone=True)),
)


user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(256)),
    Column("password", String(256)),
    Column("salt", String(64)),
    Column("github_id", Integer),
    Column("github_name", String(64)),
)


def start_orm_mappers():
    mapper_registry.map_imperatively(CGCoin, cg_coin)
    mapper_registry.map_imperatively(User, user)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
