.PHONY: venv, venvd, idev, iprod, bash, dev, prod, appb, app

##### DEV & DEPLOY #####

# Requires postgres container running and setting BACKEND_DB_* env variables in .env file
dev:
	fastapi dev --host "0.0.0.0" --port 8002 --reload src/devmons/app.py

buildprod:
	docker-compose -f docker-compose-prod.yaml build

runprod:
	docker-compose -f docker-compose-prod.yaml up

builddev:
	docker-compose -f docker-compose-dev.yaml build

rundev:
	docker-compose -f docker-compose-dev.yaml up



##### REPOSITORY & VENV #####
venv:
	uv sync

venvd:
	rm -rf .venv

uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh
