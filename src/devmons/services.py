from sqlalchemy.orm import Session

from devmons.coingecko import (
    CGCoin,
    CGCoinCreate,
    CGCoinUpdate,
    CoinAlreadyExists,
    CoinNotFound,
    get_coin_ids_from_symbol,
    get_coins_data,
)
from devmons.repository import CGCoinRepository


def add_coins(coin: CGCoinCreate, repo: CGCoinRepository, session: Session) -> list[CGCoin]:
    ids = get_coin_ids_from_symbol(coin.symbol)
    coins = get_coins_data(ids, coin.vs_currency)
    if not repo.exists(coin.symbol):
        for c in coins:
            repo.add(c)
        session.commit()
        return coins
    raise CoinAlreadyExists(f"Symbol {coin.symbol} already exists in the database")


def get_coins(symbol: str, repo: CGCoinRepository) -> list[CGCoin]:
    coins = repo.get_by_symbol(symbol)
    if not coins:
        raise CoinNotFound(f"Symbol {symbol} not found in database")
    return coins


def delete_coins(symbol: str, repo: CGCoinRepository, session: Session):
    repo.delete(symbol)
    session.commit()


# TODO: Refactor so that enumerating the updated attrs is not needed
def update_coin(id: str, coin: CGCoinUpdate, repo: CGCoinRepository, session: Session) -> CGCoin:
    current_coin = repo.get_by_id(id)
    if not coin:
        raise CoinNotFound(f"Symbol with id {id} not found in database")
    current_coin.name = coin.name
    current_coin.symbol = coin.symbol
    current_coin.circulating_supply = coin.circulating_supply
    current_coin.current_price = coin.current_price
    current_coin.market_cap = coin.market_cap
    current_coin.max_supply = coin.max_supply
    current_coin.total_supply = coin.total_supply
    current_coin.last_updated = coin.last_updated
    session.commit()
    return current_coin
