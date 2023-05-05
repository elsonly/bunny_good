up-redis:
	docker-compose -f redis/docker-compose.yml up -d

up-timescaledb:
	docker-compose -f timescaledb/docker-compose.yml up -d

down-timescaledb:
	docker-compose -f timescaledb/docker-compose.yml down

up-metabase:
	docker-compose -f metabase/docker-compose.yml up -d