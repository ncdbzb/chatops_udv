up:
	docker compose -f docker-compose-local.yml up -d --build

migrate:
	docker compose -f docker-compose-local.yml exec fastapi alembic upgrade head

logs:
	docker compose -f docker-compose-local.yml logs

down:
	docker compose -f docker-compose-local.yml down
