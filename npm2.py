from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip
import sys
import random
import string
import os
import textwrap

# Imprimir los argumentos pasados al script
print(sys.argv)

# Guardar los argumentos que se pasaron al ejecutar el script en variables
archivo_video = sys.argv[1]
texto = sys.argv[2]

def create_nombre_video(video_path, text):
    text = text.title()
    print(text)
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # Dividir la ruta del video
    video_path = video_path.split(".mp4")
    output_path = "C_" + video_path[0] + id + ".mp4"
    return output_path

def draw_text(draw, text, position, font, container_width):
    """Función para dibujar texto ajustado dentro de un contenedor."""
    lines = textwrap.wrap(text, width=30)  # Ajustar según sea necesario
    y = position[1]
    for line in lines:
        width, height = draw.textsize(line, font=font)
        draw.text(((container_width - width) / 2, y), line, font=font, fill=(0, 0, 0))
        y += height

def agrega_marca(archivo_video, texto, output_path):
    # Paso 1: Crear una imagen con el texto
    font_path = 'DejaVuSans-Bold.ttf'
    font_size = 15
    fnt = ImageFont.truetype(font_path, font_size)
    text = texto.title()  # Asegurar que el texto esté en formato título

    # Calcular el tamaño del texto para ajustar el tamaño de la imagen de fondo
    dummy_img = Image.new('RGB', (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    text_width, text_height = dummy_draw.textsize(text, font=fnt)

    # Crear la imagen de la marca de agua para un solo bloque de texto
    img_width, img_height = text_width + 20, text_height + 10  # Agregar algo de margen
    img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_text(d, text, (10, 5), fnt, img_width)

    # Paso 2: Crear un patrón repetitivo de la imagen
    video = VideoFileClip(archivo_video)
    video_width, video_height = video.size
    watermark = Image.new('RGB', (video_width, video_height), (255, 255, 255))

    for i in range(0, video_width, img_width):
        for j in range(0, video_height, img_height):
            watermark.paste(img, (i, j))

    watermark.save("/static/watermark.png")

def ejecutar_ffmpeg(archivo_video, output_path):
    cmd = f"ffmpeg -i {archivo_video} -i /static/watermark.png -filter_complex \"[0:v][1:v] blend=all_mode='overlay':all_opacity=0.7[v]; [v]format=yuv420p\" -c:v h264_nvenc -c:a copy /destino/ {output_path}"
    os.system(cmd)
    print(output_path)

# Generar nombre del video y ejecutar funciones
output_path = create_nombre_video(archivo_video, texto)
agrega_marca(archivo_video, texto, output_path)
ejecutar_ffmpeg(archivo_video, output_path)
print(output_path)
