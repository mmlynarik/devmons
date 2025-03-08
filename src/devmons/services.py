from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin, CoinAlreadyExists, CoinNotFound, get_coins_data
from devmons.repository import CGCoinRepository


def add_coins(symbol: str, repo: CGCoinRepository, session: Session) -> list[CGCoin]:
    coins = get_coins_data(symbol)
    if not repo.exists(symbol):
        for coin in coins:
            repo.add(coin)
        session.commit()
        return coins
    raise CoinAlreadyExists(f"Symbol {symbol} already exists in the database")


def get_coins(symbol: str, repo: CGCoinRepository) -> list[CGCoin]:
    coins = repo.get(symbol)
    if not coins:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    return coins


def delete_coins(symbol: str, repo: CGCoinRepository, session: Session):
    repo.delete(symbol)
    session.commit()
