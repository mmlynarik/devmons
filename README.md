# Virtual Crypto Exchange (VCE) Backend

## 1. Install virtual environment
This project uses `uv` package manager. To properly install virtual environment, uv executable needs to be present in the system. If it's not, you can download and install it using curl:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After cloning the repository, the virtual environment can be set up using the command:
```
uv sync
```

## 2. Run the FastAPI app in development mode 
The API application can be run using Makefile command which will spin up two docker containers - one for python app and one for postgres database
```
make rundev
```

## 3. API docs and usage:
API docs can be found at
```
http://127.0.0.1:8000/docs
```
