from sqlalchemy import Column, DateTime, Float, String, Table
from sqlalchemy.orm import registry

from devmons.coingecko import CGCoin
from devmons.dependency import engine

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


def start_orm_mappers():
    mapper_registry.map_imperatively(CGCoin, cg_coin)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
