from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin
from devmons.utils import get_logger

LOGGER = get_logger(__name__)


class CGCoinRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, coin: CGCoin) -> CGCoin:
        self.session.add(coin)
        LOGGER.info("New coin added to database: %s", coin)
        return coin

    def exists(self, symbol: str) -> bool:
        return bool(self.session.query(CGCoin).filter(CGCoin.symbol == symbol).all())
