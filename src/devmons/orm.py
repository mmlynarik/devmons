from sqlalchemy import Column, String, Table
from sqlalchemy.orm import registry

from devmons.coingecko import CGCoin
from devmons.db import engine

mapper_registry = registry()


cg_coin = Table(
    "cg_coin",
    mapper_registry.metadata,
    Column("id", String(256), primary_key=True),
    Column("name", String(256)),
    Column("symbol", String(30)),
)


def start_orm_mappers():
    mapper_registry.map_imperatively(CGCoin, cg_coin)


def create_db_and_tables():
    mapper_registry.metadata.create_all(engine)
