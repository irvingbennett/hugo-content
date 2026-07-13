---
_g_feedback_shortcode_6d1f1913b0875a496a4c563749e805481693fe14: |-
  [contact-field label="Nombre" type="name"  required="true" /]
  				[contact-field label="Correo electrónico" type="email" required="true" /]
  				[contact-field label="Web" type="url" /]
  				[contact-field label="Mensaje" type="textarea" /]
_g_feedback_shortcode_atts_6d1f1913b0875a496a4c563749e805481693fe14:
  block_template: null
  block_template_part: null
  className: null
  customThankyou: ""
  customThankyouHeading: Tu mensaje se ha enviado
  customThankyouMessage: ¡Gracias por tu envío!
  customThankyouRedirect: ""
  hiddenFields: null
  id: 5665
  jetpackCRM: true
  postToUrl: null
  salesforceData: null
  show_subject: "no"
  subject: '[Al Aire Libre] Corriendo La Ciudad'
  submit_button_text: Enviar
  to: irving@alairelibre.net
  widget: 0
_jetpack_related_posts_cache:
  8f6677c9d6b0f903e98ad32ec61f8deb:
    expires: 1781848808
    payload:
      - id: 2378
      - id: 2266
      - id: 1949
_last_editor_used_jetpack: block-editor
_publicize_twitter_user: '@irvingbennett'
_thumbnail_id: "5666"
_wpas_done_all: "1"
_wpcom_is_markdown: "1"
author: Rompy
categories:
  - "Correr"
cover:
  image: "/wp-content/uploads/2021/12/IrvingBennett-CallesDePanama.jpg"
date: "2021-12-20T18:59:50+00:00"
guid: http://u8z.3d5.mywebsitetransfer.com/?p=5665
parent_post_id: null
post_id: "5665"
tags:
  - correr
  - hash
title: Corriendo La Ciudad
url: /2021/12/20/corriendo-la-ciudad

---
De noviembre 1 a diciembre 15, 2018, Ricky Gates se corrió todas las calles de la ciudad de San Francisco, California, Estados Unidos. Le tomó 45 días, corriendo 7 horas, 22 minutos por día, y 46.5 kilómetros por día, recorrer todas las calles de San Francisco. Su esfuerzo quedó bien documentado con una cámara Gopro y su reloj con gps dejó guardado cada recorrido. Luego unos amigos suyos hicieron una presentación gráfica excelente de lo que hizo.

{{< figure src="/wp-content/uploads/gallery_backup/RickyGateEverySingleStreet-SanFrancisco-DataVisualisationbyYvanFornes.png" alt="" caption="" >}}

El recorrido de Ricky ha servido de ejemplo e inspiración para muchos que se han propuesto hacer lo mismo en sus respectivas ciudades. Yo soy uno de los que me he entusiasmado con la idea y he estado haciendo el recorrido de las calles de Panamá poco a poco. Ricky hizo todo su recorrido, sin parar, siguiendo un plan y corriendo mucho todos los días. Yo mas bien he estado recogiendo los datos de mis corridas de 10 años y los he estado graficando al estilo de los mapas de calor de [Strava](https://www.strava.com/heatmap#7.00/-120.90000/38.36000/hot/all).

{{< figure src="/wp-content/uploads/gallery_backup/PanamaHeatMap.jpg" alt="" caption="" >}}

Para hacer mis mapas de calor encontré una rutina en python, un lenguaje de programación, que me permitía generar la imagen a partir de mis pistas de gpx. Primero tuve que bajar mis pistas de MovesCount donde tenía recorridos guardados desde el 2012 cuando conseguí mi primer Suunto Ambit. Antes había tenido un Garmin ForeRunner 301 pero ese reloj solo guardaba la distancia y el tiempo recorrido (en el 2009 la tecnología era muy básica). MovesCount y Garmin Connect permiten que uno descargue sus recorridos para guardarlos.

Mis recorridos también estaban en Strava, pero solo a partir del 2016 cuando comencé a cargarlos en ese servicio. Todo esto es muy interesante para mí porque es un recorrido histórico que mezcla tecnologías diversas con actividades que me gustan enormemente. Todo el proceso tomó su rato porque hubo que pedir mis actividades a MovesCount. Luego tuve que procesar esos archivos para transformarlos en tipo gpx ( **gp** s e **x** change files) a partir del formato fit en que me los entregaron. Y luego los procesé con la rutina [Strava Local Heatmap](https://github.com/remisalmon/strava-local-heatmap) de Remi Salmon. Esto es lo que conseguí hacer:

{{< figure src="/wp-content/uploads/gallery_backup/heatmap.png" alt="" caption="" >}}

Me encanta ver el resultado en ese formato que expresa en colores más intensos los recorridos que más he hecho. Pero no se puede comparar un mapa de calor tan burdo contra algo como lo que le hicieron a Ricky Gates. La otra cosa que hace falta es saber cuanto de las calles de la ciudad me falta por recorrer. Es evidente que he corrido bastantes calles de la ciudad. ¿Pero cuantas son? ¿Cuáles me faltan? Nada de eso se puede ver en ese mapa de color tan básico. De paso, se pueden ver claramente delineados los senderos del Parque Metropolitano de Panamá que es lo que más corro regularmente.

Buscando herramientas para responder las preguntas que quedan pendientes con la gráfica anterior encontré muchas herramientas interesantes. Entre ellas encontré un sitio web que se llama [CityStrides](https://citystrides.com/users/23216). Este sitio se conecta con Strava y te da un listado de todas las calles recorridas, y las que faltan por correr, por ciudad. Curiosamente, no existe Panamá como ciudad en Open Street Maps. Es un tema interesante porque el asunto es a [nivel de gobierno](https://es.wikipedia.org/wiki/Ciudad_de_Panam%C3%A1). Solamente están definidos los corregimientos, pero no hay un solo límite que se pueda tomar para definir como está comprendida la ciudad.

{{< figure src="/wp-content/uploads/gallery_backup/Distrito_de_Panama.jpg" alt="" caption="" >}}

Por la razón anterior, City Strides solo puede dar la información por corregimiento. [Street Ferret](https://www.streetferret.com/), otra aplicación que también da estadísticas de calles recorridas, también tiene el mismo problema de no poder dar información de la Ciudad de Panamá, solo de los corregimientos.

{{< figure src="/wp-content/uploads/gallery_backup/IrvingBennett-CityStrides.jpg" alt="" caption="" >}}

En el último año he agregado un montón de calles y terminé San Felipe, Bella Vista y la mayoría de Calidonia. Para el 2022 termino Bethania y San Franciso, por lo menos.
