from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from devmons.coingecko import (
    CGCoin,
    CGCoinCreate,
    CGCoinUpdate,
    CoinAlreadyExists,
    CoinNotFound,
    InvalidCoinSymbol,
)
from devmons.db import get_session
from devmons.orm import create_db_and_tables, start_orm_mappers
from devmons.repository import CGCoinRepository
from devmons.services import add_coins, delete_coin, get_coins, refresh_coins, update_coin


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_orm_mappers()
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="CoinGecko Crypto API")


@app.get("/api/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}


@app.get("/api/coins/{symbol}")
async def get_coins_from_symbol(
    symbol: str, session: Annotated[Session, Depends(get_session)]
) -> list[CGCoin]:
    repo = CGCoinRepository(session)
    try:
        coins = get_coins(symbol, repo)
    except CoinNotFound:
        raise HTTPException(status_code=404, detail=f"Coins with symbol {symbol} not found in database")

    return coins


@app.post("/api/coins", status_code=201)
async def add_coins_from_symbol(
    coin: CGCoinCreate, session: Annotated[Session, Depends(get_session)]
) -> list[CGCoin]:
    repo = CGCoinRepository(session)
    try:
        coins = add_coins(coin, repo, session)
    except InvalidCoinSymbol:
        raise HTTPException(status_code=422, detail=f"Coin symbol {coin.symbol} is not valid")
    except CoinAlreadyExists:
        raise HTTPException(
            status_code=422, detail=f"Coins with symbol {coin.symbol} already exist in database"
        )

    return coins


@app.delete("/api/coins/{id}")
async def delete_coin_from_id(id: str, session: Annotated[Session, Depends(get_session)]) -> dict:
    repo = CGCoinRepository(session)
    try:
        delete_coin(id, repo, session)
    except CoinNotFound:
        raise HTTPException(status_code=404, detail=f"Coin with id {id} not found in database")
    return {"message": "OK"}


@app.put("/api/coins/{id}")
async def update_coin_from_id(
    id: str, coin: CGCoinUpdate, session: Annotated[Session, Depends(get_session)]
) -> CGCoin:
    repo = CGCoinRepository(session)
    try:
        updated_coin = update_coin(id, coin, repo, session)
    except CoinNotFound:
        raise HTTPException(status_code=404, detail=f"Coin with id {id} not found in database")
    return updated_coin


@app.get("/api/coins/refresh/all")
async def refresh_market_data(
    background_tasks: BackgroundTasks, session: Annotated[Session, Depends(get_session)]
):
    repo = CGCoinRepository(session)
    background_tasks.add_task(refresh_coins, repo=repo, session=session)
    return {"message": "Coins' market data update started in the background"}
