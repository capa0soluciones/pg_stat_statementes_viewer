##  Web view to show and reset pg_stats_statements
***Use only for Development environmets***
####  You have to install  pg_stat_statements extension on your database

```
CREATE EXTENSION pg_stat_statements;
```

#### And add this variables on your postgresql.conf

```
logging_collector=on
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
```
