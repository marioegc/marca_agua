from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
# importar libreria para pasar arumentos al script
import sys
import random
import string
import os

print (sys.argv)

# Guardar los argumentos que se pasaron al ejecutar el script en variables para su uso de archivo de video y texto
archivo_video = sys.argv[1]
texto = sys.argv[2]

def create_nombre_video(video_path=archivo_video, text=texto):
    text = text.title()
    print(text)
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    #split the video_path
    video_path = video_path.split(".mp4")
    output_path = "C_" + video_path[0]  + id + ".mp4"
    return output_path

def agrega_marca(archivo_video, texto, output_path):
    
    # Paso 1: Crear una imagen con el texto
    width, height = 200, 200
    background = (255, 255, 255)
    font_color = (0, 0, 0)
    text = texto

    img = Image.new('RGB', (width, height), background)
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('DejaVuSans-Bold.ttf', 15)
    d.text((50,50), text, font=fnt, fill=font_color)

    # Paso 2: Crear un patrón repetitivo de la imagen
    video = VideoFileClip(archivo_video)
    video_width, video_height = video.size
    watermark = Image.new('RGB', (video_width, video_height), background)

    for i in range(0, video_width, width):
        for j in range(0, video_height, height):
            watermark.paste(img, (i, j))

    watermark.save("/static/watermark.png")

    # Paso 3: Superponer la imagen de marca de agua en el video
    #watermark_clip = ImageClip("watermark.png").set_duration(video.duration).set_opacity(0.5)
    #final_clip = CompositeVideoClip([video, watermark_clip])
    #final_clip.write_videofile("video_con_marca_de_agua.mp4")
    return None

def ejecutar_ffmpeg(archivo_video, output_path):
    #ffmpeg -i A_22074.mp4 -i watermark.png -filter_complex "[0:v][1:v]blend=all_mode='overlay':all_opacity=0.7[v]; [v]format=yuv420p"  -c:v h264_nvenc -c:a copy output.mp4
    cmd1 = "ffmpeg -i " + archivo_video + " -i /static/watermark.png -filter_complex \"[0:v][1:v]blend=all_mode='overlay':all_opacity=0.7[v]; [v]format=yuv420p\"  -c:v h264_nvenc -c:a copy /destino/" + sama
    os.system(cmd1)
    return None



sama= create_nombre_video(archivo_video, texto)
agrega_marca(archivo_video, texto, sama )
ejecutar_ffmpeg(archivo_video, sama)


