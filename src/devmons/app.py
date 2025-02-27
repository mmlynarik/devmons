from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Invoice Reader API!"}


class Coina(BaseModel):
    id: str
    name: str
    description: str
