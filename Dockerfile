# Utiliza la imagen base de Python
FROM python:3.9-slim

RUN apt-get update && apt-get install -y python3-dev libpq-dev gcc

# Crea un directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY ./src/app .

# Instala las dependencias
RUN pip3 install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para acceder a la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]