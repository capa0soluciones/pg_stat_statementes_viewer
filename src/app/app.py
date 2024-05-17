import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import psycopg2
import configparser

app = Flask(__name__)

# Cargar variables de entorno desde .env
load_dotenv()

# Leer la configuración desde config.ini
config = configparser.ConfigParser()
config.read('/opt/pg_stat_statements/config/config.ini')

# Verificar si la sección [database] existe
if 'database' in config:
    # Obtener la configuración de la base de datos
    db_config = config['database']
    db_name = db_config.get('name')
    db_host = db_config.get('host')
    db_port = db_config.get('port')
    db_user = db_config.get('user')
    db_password = db_config.get('password')

    try:
        # Configuración de la conexión a PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
    except Exception as e:
        print(e)
else:
    print("ERROR - La sección [database] no existe en el archivo config.ini")

if 'query-config' in config:
    # Obtener la configuración de la base de datos
    query_config = config['query-config']
    query_config_limit = query_config.get('limit')
    query_config_filter = query_config.get('filter')
    limit = f"LIMIT {query_config_limit}"
else:
    limit = ""
    query_config_filter = "pss.mean_exec_time"
    print("La sección [query-config] no existe en el archivo config.ini, se usarán valores por defecto.")

@app.route('/', methods=['GET', 'POST'])
def index():
    # Obtener el listado de usuarios y bases de datos
    cur = conn.cursor()
    cur.execute("SELECT rolname FROM pg_roles;")
    users = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT datname FROM pg_database;")
    databases = [row[0] for row in cur.fetchall()]
    cur.close()

    if request.method == 'POST':
        if 'queries' in request.form:
            cur = conn.cursor()
            cur.execute(f"""SELECT
                                pss.queryid,
                                pss.query,
                                pss.calls AS cantidad_ejecuciones,
                                pss.total_exec_time AS tiempo_total,
                                pss.mean_exec_time,
                                pdb.datname AS databasename,
                                pua.rolname AS username
                            FROM
                                pg_stat_statements pss
                            JOIN
                                pg_catalog.pg_database pdb ON pss.dbid = pdb.oid
                            JOIN
                                pg_catalog.pg_authid pua ON pss.userid = pua.oid
                            ORDER by {query_config_filter} DESC 
                            {limit};""")
            data = cur.fetchall()
            cur.close()
            return jsonify(data)
        elif 'reset' in request.form:
            cur = conn.cursor()
            cur.execute("SELECT pg_stat_statements_reset();")
            conn.commit()
            cur.close()
            return '', 204  # No Content
    return render_template('index.html', users=users, databases=databases)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
