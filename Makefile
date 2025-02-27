.PHONY: db,venv, venvd, ssh, git


##### DEV & DEPLOY #####
image:
	docker build -t app:latest .

bash:
	docker run -it --rm --name app app bash

dev:
	fastapi run --host 0.0.0.0 --port 8000 src/devmons/app.py

prod:
	docker run --rm -p 8000:8000 --name app app:latest

##### DEV DATABASE MNGM ####
db:
	docker run -d --name postgres -e POSTGRES_USER=$${POSTGRES_USER} -e POSTGRES_PASSWORD=$${POSTGRES_PASSWORD} -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 -v postgres:/var/lib/postgresql/data postgres:15

dbd:
	sudo rm -rf ~/data
	docker rm -f postgres


##### REPOSITORY & VENV #####
ssh:
	ssh-keygen -t rsa -b 4096 -C "miroslav.mlynarik@gmail.com" -N '' -f ~/.ssh/id_rsa
	cat ~/.ssh/id_rsa.pub

git:
	git config --global user.name "Miroslav Mlynarik"
	git config --global user.email "miroslav.mlynarik@gmail.com"
	git config --global remote.origin.prune true

venv:
	uv sync

venvd:
	rm -rf .venv
