from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app = FastAPI()


class Coin(BaseModel):
    id: str
    name: str
    description: str
