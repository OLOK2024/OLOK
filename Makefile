init:
	python3 -m venv ./BackEnd/backend/myenv
	source ./BackEnd/backend/myenv/bin/activate
	pip install -r ./BackEnd/backend/requirements.txt
	source ~/.bashrc

build:
	docker-compose build

start:
	docker-compose up

stop:
	docker-compose down
