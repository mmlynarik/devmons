from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from devmons.coingecko import CGCoin, CGCoinCreate, InvalidCoinSymbol
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


@app.get("/api/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}


@app.post("/api/coins")
async def add_new_coins(
    coin: CGCoinCreate, session: Annotated[Session, Depends(get_session)]
) -> list[CGCoin]:
    repo = CGCoinRepository(session)
    try:
        return add_coins(coin.symbol, repo, session)
    except InvalidCoinSymbol:
        raise HTTPException(status_code=422, detail=f"Coin symbol {coin.symbol} does not exist.")
