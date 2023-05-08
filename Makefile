up-redis:
	docker-compose -f redis/docker-compose.yml up -d

up-timescaledb:
	docker-compose -f timescaledb/docker-compose.yml up -d

down-timescaledb:
	docker-compose -f timescaledb/docker-compose.yml down

up-metabase:
	docker-compose -f metabase/docker-compose.yml up -d

image-base:
	docker build -f Dockerfile.base -t bunny_good:base .

image:
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down