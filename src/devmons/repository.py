from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from devmons.coingecko import CGCoin
from devmons.utils import get_logger

LOGGER = get_logger(__name__)


class CGCoinRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, coin: CGCoin) -> CGCoin:
        self.session.add(coin)
        LOGGER.info("New coin added to database: %s", coin)
        return coin

    async def exists(self, symbol: str) -> bool:
        stmt = select(CGCoin).where(CGCoin.symbol == symbol)
        result = await self.session.execute(stmt)
        return bool(result.scalars().all())

    async def get_by_symbol(self, symbol: str) -> list[CGCoin]:
        stmt = select(CGCoin).where(CGCoin.symbol == symbol)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> CGCoin | None:
        return await self.session.get(CGCoin, id)

    async def list(self) -> list[CGCoin]:
        stmt = select(CGCoin)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, id: str):
        obj = await self.session.get(CGCoin, id)
        await self.session.delete(obj)
