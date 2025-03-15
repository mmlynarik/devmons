import os

CG_API_URL = "https://api.coingecko.com/api/v3"

BACKEND_DB_HOST = os.getenv("BACKEND_DB_HOST")
BACKEND_DB_NAME = os.getenv("BACKEND_DB_NAME")
BACKEND_DB_USER = os.getenv("BACKEND_DB_USER")
BACKEND_DB_PASSWORD = os.getenv("BACKEND_DB_PASSWORD")
BACKEND_DB_URL = (
    f"postgresql+asyncpg://{BACKEND_DB_USER}:{BACKEND_DB_PASSWORD}@{BACKEND_DB_HOST}/{BACKEND_DB_NAME}"
)

VS_CURRENCY = os.getenv("VS_CURRENCY", "usd")
