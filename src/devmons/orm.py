from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.orm import registry

from devmons.coingecko import CGCoin
from devmons.db import engine

mapper_registry = registry()
metadata = MetaData()


cg_coin = Table(
    "cg_coin",
    metadata,
    Column("id", String(30), primary_key=True),
    Column("name", String(256)),
    Column("symbol", String(30)),
)


def start_mappers():
    mapper_registry.map_imperatively(CGCoin, cg_coin)


def create_db_and_tables():
    metadata.create_all(engine)
