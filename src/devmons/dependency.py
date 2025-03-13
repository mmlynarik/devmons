from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from devmons.settings import BACKEND_DB_URL, CG_API_URL

engine = create_async_engine(BACKEND_DB_URL, echo=False)

Session = async_sessionmaker(engine, expire_on_commit=False)
HTTPClient = AsyncClient(base_url=CG_API_URL)


async def get_db_session():
    async with Session() as session:
        yield session


async def get_http_client():
    return HTTPClient
