.PHONY: db,venv, venvd, ssh, git


##### DEV & DEPLOY #####
idev:
	docker build --target dev -t app-dev:latest .

iprod:
	docker build --target prod -t app-prod:latest .

bash:
	docker run -it --rm --name app app-dev:latest bash

dev:
	docker run --rm -p 8000:8000 --name app-dev app-dev:latest

prod:
	docker run --rm -p 8000:8000 --name app-prod app-prod:latest

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

