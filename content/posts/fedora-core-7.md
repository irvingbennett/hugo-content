---
_edit_last: "1"
_jetpack_related_posts_cache:
  8f6677c9d6b0f903e98ad32ec61f8deb:
    expires: 1781673396
    payload:
      - id: 110
      - id: 150
      - id: 197
author: Rompy
categories:
  - "General"
date: "2007-06-08T20:47:37+00:00"
guid: http://hbx.wvf.mybluehost.me.s39296.gridserver.com/?p=207
parent_post_id: null
post_id: "207"
title: Fedora Core 7
url: /2007/06/08/fedora-core-7
wpb_post_views_count: "7"

---
He estado enredado y no había podido escribir nada hasta ahora. La mayor parte del problema se la debo a un disco duro que se me murió de repente. Como el disco no me había dado indicios de fallo, y era relativamente nuevo, me había relajado un poco con mis respaldos: tenía respaldo de mis datos, pero no tenía un respaldo que me trajera mi servidor de vuelta de un cuajo, desde el metal limpio. Ya tenía como siete años con la misma configuración de Linux, y la había ido avanzando a través de muchas versiones de Fedora, inclusive con cambios de discos, tarjeta madre y procesadores.

Pero esta vez me toco iniciar desde el piso y reconfigurar todo mi servidor para poder volver a montarle mis datos. Inicié el proceso con Fedora Core 6 y lo acabo de pasar a Fedora 7, sin ningún problema. Los problemas que me persiguen son de otra naturaleza, que no tiene nada que ver con Fedora. Todavía no he podido hacer que mi vieja instalación de Drupal aparezca en pantalla, no he tratado de reinstalar Gallery 2 para las fotos de este blog, y mi [wiki](http://wiki.alairelibre.net "PanaWiki") lo acabo de volver a habilitar.

Mis primeras prioridades fueron el correo electrónico, luego las listas de distribución de correo, y luego este sitio. El correo fue sencillo ya que Fedora practicamente se instala con el correo funcionando y solamente hay que configurar el dominio y otra para de cosas más. Y, además, tenía respaldo de la configuración de [SendMail](http://es.wikipedia.org/wiki/sendmail "SendMail"). La lista de correo, [Mailman](http://list.org "Mailman"), me dió algo de problema, principalmente por que hacía mucho que la había instalado y no recordaba nada del proceso de configuración del correo saliente de la lista. Al final resultó ser una preferencia medio oscura la que me robó la mayoría del tiempo que me tomó habilitar la lista de correo.

[WordPress](http://wordpress.org "WordPress") fue fácil de habilitar, pero he tenido problemas con la codificación de los datos. Wordpress cambió la codificación de su conjunto de caracteres a UTF-8, al igual que Fedora. Pero mi base de datos MySQL se había quedados en Latin-1, y creo que sigue en esa codificación. Cuando importé mis datos, todos los caracteres especiales salían mal. Hasta que me retorcía de la tristeza pensando en editar todas las entradas (100+) y comentarios de este lugar. Al final logre importar los datos y mantener la codificación original, pero me queda la tarea necesaria de migrar a UTF-8 en un futuro cercano. La imágenes asociadas con muchas de las entradas de este blog todavía están esperando que las restaure a sus respectivos directorios (que pereza).

El otro lugar donde tenía contenido que me interesaba restaurar era el http://wiki.alairelibre.net, pero para mi desdicha, tuve problemas con el respaldo más reciente y tuve que restaurar la data de mi respaldo de diciembre del 2006. Nada realmente mayor se perdió por que es poco el contenido que contribuyo regularmente a ese lugar. Se que tengo que volver a escribir sobre el sendero de Las Brujas, y algunas otras entradas que contribuí antes del 1 de mayo, cuando se me daño el disco. Pero también me costó poner el sistema de MediaWiki a caminar para poder mostrar mis datos. La página principal salía en blanco y no había forma que diera con la solución. El problema con MediaWiki giró en torno a detalles de autenticación y unos módulos de PHP que hacían falta.

En todo este cuento Fedora resultó una gran ayuda por que ya tenían preconfigurado la inmensa mayoría de los programas principales que necesitaba para rehabilitar todos mis servicios: Apache, Sendmail, Mailman, PHP, MySQL, Python, SpamAssassin, y varios otros servidores ya vienen instalados en Fedora. Solo me quedaba la tarea de configurar los servicios para devolverlos a su funcionabilidad anterior. Todavía me queda Gallery y Drupal por trabajar, pero creo que voy a eliminar Drupal y volver a iniciar con algo nuevo para http://localhost - donde no había mayor cosa de importancia, ningún contenido que voy a hechar de menos. Fedora se reinstaló en el equipo que tenía con gran facilidad.
