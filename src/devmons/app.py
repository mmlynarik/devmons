from contextlib import asynccontextmanager

from fastapi import FastAPI

from devmons.orm import create_db_and_tables, start_mappers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    start_mappers()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}
