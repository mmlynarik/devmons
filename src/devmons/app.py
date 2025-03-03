from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin, CGCoinCreate, get_coins_data
from devmons.db import get_session
from devmons.orm import create_db_and_tables, start_orm_mappers
from devmons.repository import CGCoinRepository
from devmons.services import add_coins


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_orm_mappers()
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/", response_model=None)
async def root():
    return {"message": "Welcome to the FastAPI app!"}


@app.post("/api/coins", response_model=None)
async def add_new_coins(
    coin: CGCoinCreate, session: Annotated[Session, Depends(get_session)]
) -> list[CGCoin]:
    repo = CGCoinRepository(session)
    coins = get_coins_data(coin.symbol)
    if not coins:
        raise HTTPException(status_code=422, detail=f"Coin symbol {coin.symbol} does not exist.")
    return add_coins(coins, repo, session)
