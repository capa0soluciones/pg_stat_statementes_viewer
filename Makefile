build:
	docker build -t capa0soluciones/pg_stats_statements_viewer:latest .

start:
	docker-compose up -d --force-recreate --build

stop:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d

bash:
	docker exec -it pg_stat_statements_dev bash


push:
        docker push capa0soluciones/pg_stats_statements_viewer:latest

pull:

        docker pull capa0soluciones/pg_stats_statements_viewer:latest
