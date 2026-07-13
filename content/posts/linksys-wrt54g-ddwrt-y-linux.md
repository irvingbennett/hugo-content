---
_jetpack_related_posts_cache:
  37550b67d263a3ce789993dc25046c5f:
    expires: 1781889045
    payload:
      - id: 110
      - id: 282
      - id: 207
      - id: 150
      - id: 195
      - id: 2460
author: Rompy
categories:
  - "General"
date: "2006-12-03T19:46:10+00:00"
guid: http://hbx.wvf.mybluehost.me.s39296.gridserver.com/?p=187
parent_post_id: null
post_id: "187"
title: Linksys WRT54G, DDwrt y Linux
url: /2006/12/03/linksys-wrt54g-ddwrt-y-linux
wpb_post_views_count: "16"

---
![wrt54g](/wp-content/uploads/2006/12/wrt54g.jpg)El Linksys WRT54g es un router inalámbrico con funciones básicas que puede ser fácilmente ampliado con una instalación de varios programas basados en el que originalmente vino instalado en el equipo. Linksys uso un equipo genérico que ya venía con su programación basada en Linux y luego se vieron obligados a entregar las fuentes internas al mundo por que así lo estipula la licencia GPL de Linux. El resultado es que todos salimos ganando: Linksys sigue vendiendo sus routers, y nosotros podemos recibir más por la misma plata al instalar un programa más sofisticado sobre el equipo genérico.

Esto lo aprendí por que estaba tratando de conectar un WRT54G a otro router inalámbrico que tengo, el WRV54G, para unir dos redes separadas dentro de mi casa. Resultó que el WRT54G y su programa interno no permite este tipo de conexión. Esto se debe a que Linksys no quiso programas esta funcionalidad en el aparato. Para este propósito Linksys vende otro aparato dedicado a la función de unir dos redes remotas, un puente. En realidad nada dentro de las funciones del equipo impiden que el WRT54G también sirva de puente, y esto lo comprobé después que le instalé [DDwrt](http://www.dd-wrt.com/dd-wrtv2/index.php "Firmware DDwrt") a mi equipo.

Me tomó un rato de búsqueda en la red para encontrar que existen varias variante de programación de fuentes abiertas que se le pueden instalar al WRT54G para darle nuevas funciones. Este equipo es realmente muy capaz una vez que se aprovecha al máximo lo que se puede hacer usando las funciones de los circuitos integrados dentro del equipo. En pocos minutos después de cargar el nuevo "firmware" pude lograr lo que me había tomado, infructuosamente, varias horas con el programa que venía de fábrica dentro del equipo.
