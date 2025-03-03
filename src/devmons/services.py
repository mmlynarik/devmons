from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin
from devmons.repository import CGCoinRepository


def add_coins(coins: list[CGCoin], repo: CGCoinRepository, session: Session) -> list[CGCoin]:
    for coin in coins:
        repo.add(coin)
    session.commit()
    return coins
