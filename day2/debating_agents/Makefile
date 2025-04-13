.PHONY: build up down logs api-logs streamlit-logs

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

api-logs:
	docker-compose logs -f app

streamlit-logs:
	docker-compose logs -f streamlit 