bash:
	docker-compose exec random bash

test:
	python3 -m pytest

up:
	docker-compose up -d --build

ps:
	docker-compose ps

stop:
	docker-compose stop -t0 random

logs:
	docker-compose logs -f
