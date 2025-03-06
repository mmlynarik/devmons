.PHONY: venv, venvd, idev, iprod, bash, dev, prod, appb, app


##### DEV & DEPLOY #####
dev:
	fastapi run --host "0.0.0.0" --port 8000 src/devmons/app.py

appb:
	docker-compose up --build

app:
	docker-compose up

##### REPOSITORY & VENV #####
venv:
	uv sync

venvd:
	rm -rf .venv

uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh
