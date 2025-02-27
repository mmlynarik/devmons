from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}


class Coina(BaseModel):
    id: str
    name: str
    description: str
