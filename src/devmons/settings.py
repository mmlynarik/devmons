import os

# API
CG_API_URL = "https://api.coingecko.com/api/v3"

# DB
BACKEND_DB_HOST = "postgres"  # Must match postgres service name in docker-compose.yml
BACKEND_DB_NAME = os.getenv("POSTGRES_DB", "postgres")
BACKEND_DB_USER = os.getenv("POSTGRES_USER", "postgres")
BACKEND_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
BACKEND_DB_URL = f"postgresql://{BACKEND_DB_USER}:{BACKEND_DB_PASSWORD}@{BACKEND_DB_HOST}/{BACKEND_DB_NAME}"
