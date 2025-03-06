import os

# API
CG_API_URL = "https://api.coingecko.com/api/v3"

RUNTIME = "local"
BACKEND_DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
BACKEND_DB_NAME = os.getenv("POSTGRES_DB", "postgres")
BACKEND_DB_USER = os.getenv("POSTGRES_USER", "postgres")
BACKEND_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
BACKEND_DB_URL = f"postgresql://{BACKEND_DB_USER}:{BACKEND_DB_PASSWORD}@{BACKEND_DB_HOST}/{BACKEND_DB_NAME}"
