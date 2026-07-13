---
_jetpack_related_posts_cache:
  8f6677c9d6b0f903e98ad32ec61f8deb:
    expires: 1781743190
    payload:
      - id: 197
      - id: 110
      - id: 150
  37550b67d263a3ce789993dc25046c5f:
    expires: 1781761502
    payload:
      - id: 197
      - id: 110
      - id: 150
      - id: 207
      - id: 187
      - id: 473
_wpcom_is_markdown: "1"
author: Rompy
categories:
  - "General"
date: "2007-03-01T23:02:52+00:00"
guid: http://hbx.wvf.mybluehost.me.s39296.gridserver.com/?p=195
parent_post_id: null
post_id: "195"
title: Ubuntu
url: /2007/03/01/ubuntu
wpb_post_views_count: "11"

---
![Logo Ubuntu](/wp-content/uploads/gallery_backup/975603.jpg)Estoy "Ubuntu"). Después de muchas versiones de [Red Hat](http://www.redhat.com/) y [Fedora](https://getfedora.org/), creo que esta distribución ha perdido algo de su atractivo y vigor. He estado tratando de instalar y usar Ruby on Rails en mi servidor. Todas las guías hacen referencia a apt-get con Debian o Ubuntu. Cuando choqué contra el obstáculo infranqueable que siempre sale en Linux, comencé la típica búsqueda en Google sobre comentarios en listas de correos que otros que ya se estrellaron con el mismo obstácula han hecho, y las soluciones que encontraron. Me ha resultado bastante claro que Debian (y Ubuntu, uno de sus derivados) han logrado mucho más tracción que Fedora.

Apt-get, y su repositorio de paquetes, duplica la cantidad de paquetes disponibles bajo el RPM de Redhat y Fedora. Aun que sería muy doloroso tener que borrar y reinstalar todo lo que me ha tomado mucho tiempo hacer en mi servidor de Fedora, creo que esa ruta, al final, me puede ahorrar tiempo y frustraciones a la larga. Debian tiene un grupo de desarrolladores (el mundo entero) un poco más amplio que Fedora y Red Hat. Fedora nunca ha logrado desasociarse por completo de su dependencia de Red Hat, y eso ha evitado que más gente se avoque a desarrollar para Fedora. En cambio, Debian, desde el principio, ha sido completamente abierto y nunca ha estado asociado directamente con un desarrollador comercial.

Tal vez, en un principio, [Debian](http://www.debian.org/) era mucho más difícil de manejar e instalar. Pero ahora esas barreras se han bajado y distribuciones como Ubuntu y [Knoppix](http://www.knopper.net) hacen muy fácil la adopción de Debian. [Apt](http://www.debian.org/doc/manuals/apt-howto/)-get también hace simple la instalación de nuevos paquetes una vez puesto en marcha el servidor.  Examinando más detalladamente los paso necesarios para hacer el cambio siempre trae a la luz las diferencias en criterio entre una distribución y otra. Por ejemplo, Ubuntu usa Postfix en lugar de Sendmail para el transporte del correo, el nombre del directorio de configuración de Apache es Apache2 en lugar de httpd, y la configuración de periféricos es completamente distinta.

En mi servidor hay servicios de correo, listas de distribución, acceso a archivos, web, y DHCP. Hay múltiples sitios web, todos relacionados, que tendría que mudar a la nueva configuración de Apache, aunque esto pareciera ser sencillo después de ver como viene estructurado Ubuntu con Apache. Tal vez lo más complicado sea el correo y las listas de distribución por el cambio de Sendmail a Postfix - el servidor de listas sigue siendo el mismo: Mailman. ¿Cuantas horas podrá tomar este cambio? ¿Cuantas horas podrá ahorrarme este cambio en el futuro? Creo que la ventaja más grande sería bajarme del tren que es Fedora: cada seis meses viene una versión nueva, y las versiones viejas rápidamente van quedando desatendidas. Esto casi que me obliga a estar cambiando regularmente.
