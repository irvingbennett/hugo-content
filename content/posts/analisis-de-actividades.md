---
_jetpack_related_posts_cache:
  8f6677c9d6b0f903e98ad32ec61f8deb:
    expires: 1782182267
    payload:
      - id: 2388
      - id: 5759
      - id: 732
_last_editor_used_jetpack: block-editor
_publicize_twitter_user: '@irvingbennett'
_thumbnail_id: "5680"
_wpas_done_all: "1"
_wpcom_is_markdown: "1"
author: Rompy
categories:
  - "Correr"
cover:
  image: "/wp-content/uploads/2022/01/poster_2021_grid.svg"
date: "2022-01-05T20:42:10+00:00"
guid: http://u8z.3d5.mywebsitetransfer.com/?p=5681
parent_post_id: null
post_id: "5681"
tags:
  - correr
title: Análisis de Actividades
url: /2022/01/05/analisis-de-actividades

---
Ahora que terminó el 2021 Strava le presenta a cada atleta un resumen de su año deportivo. Esto me dejó con curiosidad por reproducir los análisis que hizo Strava usando las mismas pistas que se cargaron desde mi reloj. Ya tenía avanzado algo del trabajo tal como lo describí en la entrada anterior a esta. El enfoque de esta entrada, en lugar de ser las calles recorridas, es ver como ha estada mejorando, o empeorando, mi rendimiento al correr.

Aunque he logrado mantener algo de forma a través de los años, estos no pasan en vano. Cada año uno pierde al menos un latido en la capacidad máxima del corazón. Ese es tema de otra entrada. En esta vuelta quería repetir algo del resumen de Strava. Un ejemplo:

{{< figure src="/wp-content/uploads/gallery_backup/strava6720715044720163829.jpg" alt="" caption="" >}}

Como la gráfica anterior hay varias otras muy bien logradas. En lugar de inventar la rueda traté de ver qué había ya hecho que pudiese utilizar para lograr algo parecido. Encontré que hay muchas herramientas para el propósito pero la mayoría son trabajos superficiales y someros, más por la línea de "así se hace esto". En general son programadores que corren y están haciendo lo mismo que yo ahora mismo. Algunos que tiene picazón y no encuentran como rascarla han hecho un buen trabajo.

Uno de los que encontré se llama [Running\_Page](https://github.com/irvingbennett/running_page) y crea un sitio web completo donde ver todas las actividades que uno ha hecho y produce unas gráficas agradables. Me tomó bastante trabajo hacerlo andar porque está basado en una versión vieja de [Gatsby](https://www.gatsbyjs.com/) (la 2.4) y ahora Gatsby está en la versión 4.0. Al final logré hacerlo andar. Hice una bifurcación del código original y subí la actualización a mi repositorio de Github. Arriba compartí el enlace. Una de las imágenes que produjo el sitio es la siguiente:

{{< figure src="/wp-content/uploads/gallery_backup/grid.svg" alt="Malla de Actividades" caption="Malla de Actividades" >}}

La página de correr hace bastante más que solo la gráfica anterior. Pero viendo el código encontré las rutinas que habían usado para crear esa gráfica. Las rutinas están basadas en otro desarrollo que se llama [GPX Track Poster](https://github.com/irvingbennett/GpxTrackPoster) y permite crear imágenes partiendo de los archivos GPX locales. También creé una bifurcación de esas rutinas y las usé para crear mis propios afiches usando mis archivos GPX. Este programa resultó más sencillo que el anterior, pero también tenía problemas porque cuando descargué mis archivos de Strava vinieron con textos en español y la rutina no soporta las etiquetas de actividades en ese idioma (no las entiende).

![Corridas 2021](https://i0.wp.com/alairelibre.net/wp-content/uploads/2022/01/poster_2021_grid.svg)

![](https://i2.wp.com/alairelibre.net/wp-content/uploads/2022/01/poster_2021_circular.svg)

![](https://i1.wp.com/alairelibre.net/wp-content/uploads/2022/01/poster_2021_calendar.svg)

![Malla de Actividades](https://i1.wp.com/alairelibre.net/wp-content/uploads/2022/01/grid.svg)

La galería anterior usa gráficas SVG y no se muestran correctamente en WordPress. Toca alguno de los recuadros para ver las imágenes individualmente.

![](https://i2.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava8872277446906519317-576x1024.jpg)

![](https://i2.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava8444967887952864962-576x1024.jpg)

![](https://i0.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava6720715044720163829-576x1024.jpg)

![](https://i1.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava6100114889416321916-576x1024.jpg)

![](https://i2.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava4686537925213484809-576x1024.jpg)

![](https://i1.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava4495281725112844481-576x1024.jpg)

![](https://i2.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava2666841444904265683-576x1024.jpg)

![](https://i0.wp.com/alairelibre.net/wp-content/uploads/2022/01/strava1230423794665724043-576x1024.jpg)

Las últimas gráficas las produjo Strava y son muy buenas. Cada año las hacen mejor. No he encontrado algo que lo haga tan bien como ellos, pero he encontrado varios flujos que me permiten sacar los datos de las pistas de mis actividades. Poco a poco voy a programar algo que me permita hacer esos análisis dinámicamente y hacer comparaciones de año contra año.

Yo he ido aumentando el volumen de mis actividades con la edad sencillamente porque a mis 61 años recién cumplidos no puedo darme el lujo de parar de moverme. Antes podía ser un guerrero de fin de semana y el cuerpo se quejaba pero me lo permitía. Ahora cada vez que paró de hacer ejercicio comienza la entropía a deteriorarme rápidamente. Así es que uno de los estudios que quiero hacer es cuánto he podido frenar mi pérdida de forma. Lo que quiero lograr es poder mantener lo que tengo por el tiempo que pueda.
