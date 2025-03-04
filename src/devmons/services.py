from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin, CGCoinCreate, get_coins_data
from devmons.repository import CGCoinRepository


def add_coins(coin: CGCoinCreate, repo: CGCoinRepository, session: Session) -> list[CGCoin]:
    coins = get_coins_data(coin.symbol)
    for c in coins:
        repo.add(c)
    session.commit()
    return coins
