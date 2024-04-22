build:
	docker build -t flask-app:latest .

start:
	docker-compose up -d --force-recreate --build

stop:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d

bash:
	docker exec -it pg_stat_statements_dev bash
