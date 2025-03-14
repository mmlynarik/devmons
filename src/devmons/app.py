from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from devmons.coingecko import (
    CGCoin,
    CGCoinCreate,
    CGCoinUpdate,
    CoinAlreadyExists,
    CoinNotFound,
    InvalidCoinSymbol,
)
from devmons.dependency import HTTPClient, get_db_session, get_http_client
from devmons.orm import create_db_and_tables, start_orm_mappers
from devmons.repository import CGCoinRepository
from devmons.services import add_coins, delete_coin, get_coins, refresh_coins, update_coin


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_orm_mappers()
    await create_db_and_tables()
    yield
    HTTPClient.aclose()


app = FastAPI(lifespan=lifespan, title="CoinGecko Crypto API")


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
HTTPClientDep = Annotated[AsyncClient, Depends(get_http_client)]


@app.get("/api/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}


@app.get("/api/coins/{symbol}")
async def get_coins_from_symbol(symbol: str, session: DBSessionDep) -> list[CGCoin]:
    repo = CGCoinRepository(session)
    try:
        coins = await get_coins(symbol, repo)
    except CoinNotFound:
        raise HTTPException(status_code=404, detail=f"Coins with symbol {symbol} not found in database")

    return coins


@app.post("/api/coins", status_code=201)
async def add_coins_from_symbol(
    coin: CGCoinCreate, session: DBSessionDep, client: HTTPClientDep
) -> list[CGCoin]:
    repo = CGCoinRepository(session)
    try:
        coins = await add_coins(coin, repo, session, client)
    except InvalidCoinSymbol:
        raise HTTPException(status_code=422, detail=f"Coin symbol {coin.symbol} is not valid")
    except CoinAlreadyExists:
        raise HTTPException(
            status_code=422, detail=f"Coins with symbol {coin.symbol} already exist in database"
        )
    return coins


@app.delete("/api/coins/{id}")
async def delete_coin_from_id(id: str, session: DBSessionDep) -> dict:
    repo = CGCoinRepository(session)
    try:
        await delete_coin(id, repo, session)
    except CoinNotFound:
        raise HTTPException(status_code=404, detail=f"Coin with id {id} not found in database")
    return {"message": "OK"}


@app.put("/api/coins/{id}")
async def update_coin_from_id(id: str, new_coin_values: CGCoinUpdate, session: DBSessionDep) -> CGCoin:
    repo = CGCoinRepository(session)
    try:
        updated_coin = await update_coin(id, new_coin_values, repo, session)
    except CoinNotFound:
        raise HTTPException(status_code=404, detail=f"Coin with id {id} not found in database")
    return updated_coin


@app.get("/api/coins/refresh/all")
async def refresh_market_data(
    background_tasks: BackgroundTasks, session: DBSessionDep, client: HTTPClientDep
):
    repo = CGCoinRepository(session)
    background_tasks.add_task(refresh_coins, repo=repo, session=session, client=client)
    return {"message": "Coins' market data update started in the background"}
