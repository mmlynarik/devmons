from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Coina(BaseModel):
    id: str
    name: str
    description: str
