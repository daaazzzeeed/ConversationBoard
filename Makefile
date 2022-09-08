build:
	docker-compose build


up:
	docker-compose up -d


down:
	docker-compose down -v


migration:
	docker-compose run web alembic revision --autogenerate -m ""


upgrade:
	docker-compose run web alembic upgrade head


downgrade:
	docker-compose run web alembic downgrade -1


run: up upgrade


logs:
	docker logs conversations_web_1