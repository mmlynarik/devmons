import os
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Table, create_engine
from sqlalchemy.orm import registry, sessionmaker

BACKEND_DB_HOST = os.getenv("POSTGRES_SERVER", "postgres")
BACKEND_DB_NAME = os.getenv("POSTGRES_DB", "postgres")
BACKEND_DB_USER = os.getenv("POSTGRES_USER", "postgres")
BACKEND_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
BACKEND_DB_URL = f"postgresql://{BACKEND_DB_USER}:{BACKEND_DB_PASSWORD}@localhost:5433/{BACKEND_DB_NAME}"

mapper_registry = registry()


@dataclass
class User:
    id: int
    name: str


user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


mapper_registry.map_imperatively(User, user_table)

engine = create_engine(BACKEND_DB_URL)
mapper_registry.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user = User(id=23223, name="Joe")
print(user)
session.add(user)
session.commit()
