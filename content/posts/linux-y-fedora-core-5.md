---
_jetpack_related_posts_cache:
  8f6677c9d6b0f903e98ad32ec61f8deb:
    expires: 1781784399
    payload:
      - id: 150
      - id: 207
      - id: 195
author: Rompy
categories:
  - "General"
date: "2006-03-29T17:51:52+00:00"
guid: http://hbx.wvf.mybluehost.me.s39296.gridserver.com/?p=110
parent_post_id: null
post_id: "110"
title: Linux y Fedora Core 5
url: /2006/03/29/linux-y-fedora-core-5
wpb_post_views_count: "14"

---
Este no es un blog de tecnología, pero si no me gustara la tecnología lo más probable es que no existiera este blog. Comencé a jugar con Linux cuando compré una versión de RedHat Linux 6.0 para probarlo. La instalé en una computadora donde arrancaba Microsoft Small Business Server 4.5 y Linux. Después de no arrancar la máquina en SBS por mucho tiempo decidí eliminar el Small Business Server y dedicar la máquina a Linux.

Eso fue hace mucho tiempo ya. Desde entonces la misma instalación básica ha pasado por Linux 7, 8 y 9. Luego pasó a Fedora Core, y de ahí pasó a Core 2, 3, 4, y ahora Fedora Core 5. En el proceso he cambiado tarjetas madre, CPUs, discos duros, y monitores, pero Linux sigue caminando.

Ahora estoy terminando de pulir Fedora Core 5, que la verdad está muy bueno. Pero siempre da algo de problemas el cambio de versión. Ojalá fuera completamente indoloro. Pero es más indoloro que la opción de actualizar servidores de Microsoft que siempre requieren de una instalación nueva en otra máquina y luego una migración de todos los datos.

Para lo que me interesa, los principales problemas que encontré fueron el cambio a Apache httpd 2.2. Me costó un poco volver a poder arrancarlo. Parte del problema es que pasé a la versión de AMD 64 bits y me di de frente con el choque entre las librerías de 32 bits que quedaron en lib, y las nuevas estaban en lib64. Pero un poco de husmeo encontró el problema.

La nueva versión de Zope 2.8 todavía esta parada y no la he podido poner a caminar. Pero no le he dedicado mucho tiempo. De esa versión depende la instalación de Plone 2.1 que tengo en una parte de [alairelibre.net](http://localhost "Al Aire Libre!"). Ese sitio no lo visita mucha gente (por no decir nadie). También me queda por actualizar una tanda de RPMs que están encontrándose con choques con las versiones viejas que han quedado regadas por el disco. Pero eso lo arreglo con paciencia.

Lo importante ya está caminando. Ya tengo PHP5, MySQL 5, y Apache httpd 2.2, mi [LAMP](http://en.wikipedia.org/wiki/LAMP_%28software_bundle%29 "lamp") está encendido.
