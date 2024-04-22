## Flask APP para mostrar Queries ejecutadas en Postgres

# Es necesario tener instalada la extensión pg_stat_statements en la base de datos de postgres

CREATE EXTENSION pg_stat_statements;

Y realizar estas configuraciones en el archivo postgresql.conf

logging_collector=on
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all


