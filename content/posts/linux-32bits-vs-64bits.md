---
_jetpack_related_posts_cache:
  8f6677c9d6b0f903e98ad32ec61f8deb:
    expires: 1782028357
    payload:
      - id: 110
      - id: 207
      - id: 187
author: Rompy
categories:
  - "General"
date: "2006-07-11T14:38:59+00:00"
guid: http://hbx.wvf.mybluehost.me.s39296.gridserver.com/?p=150
parent_post_id: null
post_id: "150"
title: Linux 32bits vs. 64bits
url: /2006/07/11/linux-32bits-vs-64bits
wpb_post_views_count: "8"

---
En [marzo](/) de este año hice una serie de cambios en mi servidor Linux. Primero cambié la tarjeta de madre de una que usaba un AMD Athlon a una que usada un AMD Athlon 64. Y luego actualicé la versión de Linux a Fedora Core 5. Todo esto fué bastante sencillo por que era una actualización razonable: mismo tipo de tarjeta madre, mismo procesador, y una actualización del sistema operativo en el mismo sistema. ¡No traten de hacer esto con Windows 2003 server! Yo solo me tire una curva cuando decidí que, además de la actualización a Core 5, también instalaría la versión de 64 bits de Linux.

La verdad es que esto hubiese estado bien si hacía una instalación fresca y no mezclaba las cosas. Pero en realidad todavía hay muchas cosas que no han sido portadas a 64 bits y el sistema trata de vivir en un mundo de librerías mixtas. Las cosas se enredaron un poco y no es hasta hace poco que he deshecho el enredo que ocasioné. Hice una instalación fresca de Fedora Core 5 32bits en discos vírgenes y movi mis datos de un lado al otro. Esto también resultó fácil por el uso de LVM para virtualizar los disco duros.

La versión de Fedora Core 5 64bits estaba en un solo disco IDE de 200 gigas y la nueva instalación la hice en dos discos ATA, uno de 200 gigas y otro de 150 gigas, ambos actuando como una sola unidad. Definí el disco IDE como un subdirectorio de la instalación fresca y con solo cambiar los discos desde los cuales iniciaba el sistema (IDE o ATA) arrancaba en una versión o en la otra. Esto me permitió ir mudando el sistema en etapas. Cuando podía dedicarle un poco de tiempo a la migración arrancaba los discos ATA y configuraba mis sistemas y luego volvía a arrancar desde el disco IDE.

Al cabo de un par de días he vuelto a estar con todo andando: el correo, los servidores web, Samba, y una versión que no sufre de problemas de personalidad múltiple. Me decidí por la versión de 32 bits por qué todavía faltan muchas librerías que no son de fuentes abiertas y que sus dueños no las han pasado a 64 bits. Adobe Flash es un ejemplo clásico de este problema. Otro ejemplo son los controladores de las tarjetas de vídeo que también siguen siendo propietarios y no todos han sido pasados a 64 bits. Si solamente usará mi servidor para servicios de servidor, me hubiese quedado con los 64 bits.

Pero a menudo dejo mi máquina de Windows XP apagada y navego y escribo cartas con el Servidor, y la falta de las pequeñeces del escritorio y de uso personal me afectaban. Imagino que este problema durará mucho tiempo, al igual que cuando hicimos el cambio de procesadores de 16bits a procesadores de 32bits. ¿Se acuerdan de esto, si? Yo me acuerdo de cuando pasamos de 8bits a 16bits también... ¿CP/M?
