from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from devmons.settings import BACKEND_DB_URL

engine = create_engine(BACKEND_DB_URL, echo=False)

Session = sessionmaker(engine)
HTTPClient = AsyncClient()


def get_db_session():
    with Session() as session:
        yield session


async def get_http_client():
    return HTTPClient
