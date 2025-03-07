from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin, get_coins_data
from devmons.repository import CGCoinRepository


def add_coins(symbol: str, repo: CGCoinRepository, session: Session) -> list[CGCoin]:
    coins = get_coins_data(symbol)
    if not repo.exists(symbol):
        for coin in coins:
            repo.add(coin)
        session.commit()
    return coins
