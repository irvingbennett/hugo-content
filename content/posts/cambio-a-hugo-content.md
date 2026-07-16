---
date: '2026-07-15T08:48:03-05:00'
draft: false
title: 'Cambio a Hugo Content'
author: Rompy
---
Después de más de 20 años usando WordPress he cambiado a [Hugo](https:gohugo.io). WordPress me sirvio
muy bien durante todo este tiempo pero ya me estaba cansando del tiempo y el costo de manejar ese 
sistema. Yo lo tenía hospedado en GoDaddy (que es un desastre) después que ellos compraron 
Media Temple donde tuve mi instalación por muchos años. Antes valía la pena pagar por un hospedaje
así por que tenía clientes que compartían mi instlación y así me salía gratis co-hospedar
mi sitio junto con los demás. Realmente, originalmente lo tenía en un servidor en mi oficina.

Ahora ya no tengo clientes de hospedaje de WordPress y no quiero seguir pagando por un servidor
que no aprovecho y que no me gusta. Buscando opciones regresé a Hugo. Ya lo había probado antes,
junto Gatsby, y otros más. Al final me fui por Hugo porque es sencillo y muy rápido. Exporté
todas mis entradas y bajas a un respaldo de WordPress en un archivo de exportación xml y luego
transformé ese archivo en entradas individuales en Markdown. [Markdown](https://www.markdownguide.org/)

Markdown usa un formato de texto que es muy fácil de leer para los humanos versus usar HTML. HTML es 
el formato estándar de la web. HTML, hypertext markup language, se usa para definir el contenido de
las páginas de internet y CSS, cascading style sheets, se usa para definir su presentación. Así se separa 
el contenido de su presentación. WordPress usaba un editor de texto que permitía ver cómo iba a 
quedar la página mientras uno la escribía. Eso era muy práctico y agradable. La verdad es que yo
soy de la vieja escuela, aprendí a usar las computadoras en los tiempos de CP/M, y luego MS-DOS.
En esos tiempos no existía el ratón, y las pantallas solo mostraban 24 líneas de 80 columnas. Usar
Markdown es, de cierta forma, regresar a esos tiempos.

La verdad es que ahora 80% de los usuarios navegan por internet usando su celular y todo esas
presentaciones sofisticadas han quedado reducidas a una columna con textos e imágenes. Reproducir
ese formato con Markdown es lo más sencillo del mundo. Me he pasado una semana revisando y editando
unas 576 páginas que habían en mi blog divididas entre unas 450 entradas y unas 125 páginas. A
través de más de 20 años muchas de esas páginas, entre entradas en la bitácora y las páginas sueltas,
quedaron con enlaces rotos. Cuando exporté el sitio quedé con unos 23,000 archivos entre imágenes y
archivos de Markdown (de texto). La cantidad tan alta de imágenes era porque WordPress creaba
muchas imágenes en distintos tamaños a partir de la imágen original para poder acomodar los diseños
que se creaban en su compositor de páginas.

Después de deshacerme de la multiplicidad de imágenes y quedarme solo con la original quedé con unas
2,083 imágenes. También tenía muchos enlaces rotos porque cuando moví mis sitios de mi servidor a 
Media Temple dejé atrás otra aplicación donde tenía mis fotos en galerías al estilo de Google Photos. 
Todos los enlaces a esas galerías quedaron rotos, junto con muchas imágenes que estában en esas 
galerías. Estos últimos siete días he estado enfocado al máximos en este proyecto y ya casi está
listo. De unos 500 enlaces rotos ya me quedan unos 50, el 10% apenas. 

```
import os
import json
import re
from pathlib import Path

# --- CONFIGURATION ---
# Path to your local Google Photos/Drive backup folder organized by year/month
PHOTOS_BACKUP_DIRECTORY = Path("/mnt/c/Users/irvin/Google Drive/Google Photos") 
OUTPUT_JSON_FILE = Path("/home/irving/hugo-content/photos_index.json")

# Ignore WordPress-style resized image suffixes just in case they slipped into the backup
RESIZED_SUFFIX_REGEX = re.compile(r'-(?:\d+x\d+|scaled|rotated|e\d+)(?=\.[a-zA-Z]{3,4}$)')
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

def build_photo_index():
    photo_index = {}
    
    if not PHOTOS_BACKUP_DIRECTORY.exists():
        print(f"❌ Error: Backup directory not found at {PHOTOS_BACKUP_DIRECTORY}")
        return

    print(f"🔍 Scanning for photos in: {PHOTOS_BACKUP_DIRECTORY}")
    
    # Recursively walk through all years and months
    for root, _, files in os.walk(PHOTOS_BACKUP_DIRECTORY):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                # Skip it if it's a resized duplicate pattern
                if RESIZED_SUFFIX_REGEX.search(file):
                    continue
                
                # Use lowercase filename as the unique lookup key for case-insensitivity
                photo_key = file.lower()
                absolute_path = os.path.join(root, file)
                
                # Store the exact path attribute
                photo_index[photo_key] = {
                    "filename": file,
                    "local_path": absolute_path
                }

    # Write out the JSON database
    print(f"💾 Saving index of {len(photo_index)} unique photos to {OUTPUT_JSON_FILE}...")
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(photo_index, f, indent=4, ensure_ascii=False)
        
    print("🏁 Indexing complete!")

if __name__ == "__main__":
    build_photo_index()

```

Me tocó usar programas de Python, como el anterior, para ir arreglando todo lo que andaba
enredado en los archivos de Markdown para que quedaran lo mejor posible. A través de 20+
años habian muchas iteraciones de temas que usé y cada uno dejó atajos \[shortcodes\] que
la exportación a Markdown dejó dispersos en muchísimas páginas. Bueno, fueron como 20
programas distintos de Python para ir moviendo, consolidando, arreglando y borrando cosas
para poder llegar a quedar con un sitio limpio y ordenado. Luego que dejé los archivos de
Markdown listos y los archivos de multimedia consolidados, me tocó buscar un tema para
poder presentar el contenido que estaba bastante a mi gusto en WordPress.

Al final, después de probar Zen, Congo, Stack, y otros temas, quedé con PaperMod. El tema
que está mostrando este contenido es bastante minimalista, con solo un pequeño menú arriba
del contenido. Organicé mis entradas en Bitácora (las entradas del blog), Páginas, y 
Panamá Paso a Paso (una serie de artículo que se publicaron en La Estrella de Panamá). Por
último en el menú está Buscar que permite encontrar entradas basadas en el contenido o 
en el título. Quedan más cosas por hacer, como permitir que dejen comentarios en las entradas
o páginas, arreglar los últimos enlaces rotos, y alguna que otra cosa más.

En todo esto tuve un aliado que resultó fantástico: Google Gemini. La mayoría del código de
Python (99%) lo escribió Gemini basado en lo que yo le decía que me tocaba hacer. Estoy muy
impresionado por su capacidad y el ahorro en tiempo que representó su ayuda. Me tocó a mí 
hacer todo el trabajo, pero tal vez me hubies tomado el doble del tiempo, o más.

Si llegaron hasta acá, son lectores muy interesados. Esta entrada tiene poco que ver con el 
contenido general de este sitio. Espero que les gusté este nuevo sitio y el tema que escogí.