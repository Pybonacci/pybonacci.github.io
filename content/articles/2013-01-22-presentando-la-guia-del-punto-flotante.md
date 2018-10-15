---
title: Presentando «La guía del punto flotante»
date: 2013-01-22T14:19:13+00:00
author: Juan Luis Cano
slug: presentando-la-guia-del-punto-flotante
tags: coma flotante, punto flotante, python

Hoy interrumpimos un poco el flujo de artículos sobre Python para presentar [La guía del punto flotante](http://puntoflotante.org/ "La guía del punto flotante"), una web con información en formato amistoso y legible sobre la aritmética de punto flotante. Esta es una traducción de [_The floating point guide_](http://floating-point-gui.de/) por Michael Borgwardt y que hemos publicado, igual que la original, junto al código fuente.

<p style="text-align:center;">
  <a href="http://puntoflotante.org/"><img class="aligncenter  wp-image-1528" alt="La guía del punto flotante" src="https://pybonacci.org/images/2013/01/2013-01-22-131209_1366x768_scrot.png?w=700" width="560" height="306" srcset="https://pybonacci.org/wp-content/uploads/2013/01/2013-01-22-131209_1366x768_scrot.png 1346w, https://pybonacci.org/wp-content/uploads/2013/01/2013-01-22-131209_1366x768_scrot-300x164.png 300w, https://pybonacci.org/wp-content/uploads/2013/01/2013-01-22-131209_1366x768_scrot-1024x560.png 1024w, https://pybonacci.org/wp-content/uploads/2013/01/2013-01-22-131209_1366x768_scrot-1200x657.png 1200w" sizes="(max-width: 560px) 100vw, 560px" /></a>
</p>

La guía (llamada también «Lo que todo programador debería saber sobre aritmética de punto flotante») ofrece un punto de entrada para aquellas personas que están haciendo operaciones matemáticas con el ordenador y de repente se encuentran con un resultado que no cuadra. En Python:

    :::python
    &gt;&gt;&gt; 0.1 + 0.2
    0.30000000000000004

Y se preguntan [«¿qué está haciendo mal Python?»](https://twitter.com/pOverlord/status/281374749110710272), cuando resulta que es un «problema» generalizado.

Después de algunas explicaciones básicas sobre el [formato de punto flotante](http://puntoflotante.org/formats/fp/) (también llamado de coma flotante) y por qué los ordenadores lo utilizan, se ofrecen algunas alternativas y se detallan los diferentes errores que se cometen al hacer estas operaciones. Por último, también hay «chuletas» para varios lenguajes de programación, como por ejemplo esta chuleta de [aritmética de punto flotante en Python](http://puntoflotante.org/languages/python/).

En GitHub podéis encontrar el [código fuente](https://github.com/Pybonacci/puntoflotante.org) de la guía, y os invitamos a colaborar haciendo sugerencias o introduciendo cambios vosotros mismos 🙂

Por cierto, ¡no se te olvide hacer +1 tanto en la guía como en [nuestra página de Google+](https://plus.google.com/105361445330808607864/posts)!

Y tú, **¿has aprendido algo que no sabías con la guía?** ¿La recomendarías?