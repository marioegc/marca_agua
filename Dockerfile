# Usar una imagen base de Python
FROM marioegc/arigato:01

WORKDIR /app
RUN mkdir /static
RUN mkdir /destino
RUN apt-get update && apt-get install -y ffmpeg
RUN apt install python3-pip -y

# Copiar los archivos de requerimientos
COPY requirements.txt /static
COPY DejaVuSans-Bold.ttf /static
COPY npm.py /static
COPY npm2.py /static

# Instalar las dependencias
RUN pip install --no-cache-dir -r  /static/requirements.txt

# Comando para ejecutar la aplicación
CMD ["python", "/static/npm2.py"]