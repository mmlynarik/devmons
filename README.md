# Devmons Crypto API Assignment

## 1. Install virtual environment
This project uses `uv` package and project manager to define project and its dependencies. To properly install virtual environment, uv executable needs to be present in the system. If it's not, you can download and install it through Makefile command:
```
make uv
```

After cloning the repository, the virtual environment, along with all dependencies can be installed using the command:
```
uv sync
```

## 2. Run the FastAPI app
The API application can be run using the docker compose command, which spins up two containers - the postgres database and the python application:
```
docker-compose up
```

## 3. API docs and usage:
API docs can be found at
```
http://127.0.0.1:8000/docs
```
