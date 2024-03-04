import requests
import json
import os
import time
import subprocess
import re

WORKER=1
SERVIDOR= "127.0.0.1"
FOLDER_TELEPRESENCIA= "/stg-trans"

while True:
    try:
        url = "http://192.168.1.30:5000/tarea?worker=1"
        response = requests.get(url)
        data = json.loads(response.content.decode())

        archivo = data["archivo"]
        folder = data["folder"]
        id = data["id"]
        texto = data["texto"]
        print("archivo:", archivo)
        print("folder:", folder)
        print("id:", id)
        print("texto:", texto)

        # Comparar si la carpeta es igual a 100
        if str(folder) == "100":
            print("La carpeta es igual a 100")
            #armar la constante de la carpeta
            RUTA2= str(FOLDER_TELEPRESENCIA)

            #armar el nombre del archivo
            ARCHIVO = archivo

            comando = "sudo docker run --rm  --gpus 'device=0'  -v {}:/app marioegc/arigato:01 sh /arigato/run.sh {}".format(str(RUTA2), str(ARCHIVO))
            print (comando)
            os.system(comando)
            #FINALIZA
            url2 = "http://{}:5000/finaliza?id={}".format(SERVIDOR, str(id))
            response = requests.get(url2)

        elif str(folder) == "200":
            print("entramos al proceso")
            RUTA= "/IAXON-1"
            print(RUTA)
            ARCHIVO_M = str(archivo)
            print(ARCHIVO_M)
            print("paso1")
            TEXTO_MARCA_AGUA = str(texto)
            print(TEXTO_MARCA_AGUA)
            print("paso3")
            comando = "sudo docker run --rm --runtime=nvidia --gpus 'device=0'  -e NVIDIA_VISIBLE_DEVICES=all  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,video -v " +  RUTA+":/app -v /copias:/destino marioegc/marca_agua:02 python3 /static/npm.py " + ARCHIVO_M + " " + '\"' + TEXTO_MARCA_AGUA + '\"'
            print(comando)
            
            proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True)
            salida, error = proceso.communicate()

            if error:
                print("Error:", error)
            else:
                print("Salida:", salida)
                
                # Salida: b"['/static/npm.py', 'A_2003.mp4', 'Nombre1 Nombre2 Apellido1 Apellido2']\nNombre1 Nombre2 Apellido1 Apellido2\nC_A_20033M0R8D.mp4\nC_A_20033M0R8D.mp4\n"
               # Asumiendo que 'salida' es una variable que contiene la salida del comando
                #salida = b"['/static/npm.py', 'A_2003.mp4', 'Nombre1 Nombre2 Apellido1 Apellido2']\nNombre1 Nombre2 Apellido1 Apellido2\nC_A_20033M0R8D.mp4\nC_A_20033M0R8D.mp4\n"

                # Convertir la salida de bytes a string si es necesario
                salida_str = salida.decode('utf-8') if isinstance(salida, bytes) else salida

                # Ajustar la expresión regular para capturar el nombre del archivo, teniendo en cuenta los saltos de línea y otros caracteres
                match = re.search(r'C_A_\w+\.mp4', salida_str)

                if match:
                    ARCHIVO_COPIA = match.group()
                    print(f"Archivo encontrado: {ARCHIVO_COPIA}")
                    url2 = "http://{}:5000/finalizacopia?id={}&archivo_copia={}".format(SERVIDOR, str(id), ARCHIVO_COPIA)
                    response = requests.get(url2)
                else:
                    print("No se encontró el patrón en la salida")

            #FINALIZA
            url2 = "http://{}:5000/finalizacopia?id={}&archivo_copia={}".format(SERVIDOR, str(id), ARCHIVO_COPIA)
            response = requests.get(url2)

        else:
            #armar la constante de la carpeta
            RUTA= "/IAXON-" + str(folder)

            #armar el nombre del archivo
            ARCHIVO = archivo
            #EJECUTA COMANDO

            comando = "sudo docker run --rm  --gpus 'device=0'  -v {}:/app marioegc/arigato:01 sh /arigato/run.sh {}".format(str(RUTA), str(ARCHIVO))
            print (comando)
            os.system(comando)
            #FINALIZA
            url2 = "http://{}:5000/finaliza?id={}".format(SERVIDOR, str(id))
            response = requests.get(url2)
    except:
        pass


