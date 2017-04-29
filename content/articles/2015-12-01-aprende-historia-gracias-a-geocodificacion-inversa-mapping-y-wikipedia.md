---
title: Aprende historia gracias a geocodificación inversa, mapping y wikipedia
date: 2015-12-01T08:40:18+00:00
author: Kiko Correoso
slug: aprende-historia-gracias-a-geocodificacion-inversa-mapping-y-wikipedia
tags: APIs, brython, flask, Jinja2, map2wiki, nominatim, openlayers, openstreetmap, wikipedia

El otro día, mientras esperaba en Juan Bravo a un amigo, tuve algo de tiempo para divagar y entre esas divagaciones junté Juan Bravo, Python, Internet, geolocalización, historia,... En fin, que estaba en Juan Bravo, no tenía ni idea de quien era ese señor (llamadme ignorante), tenía algo de tiempo y se me ocurrió poder obtener información de calles a partir de un mapa y de la wikipedia y, de aquellos polvos, estos lodos, y nació [map2wiki](http://map2wiki.runbear.webfactional.com/).

## ¿Qué es map2wiki?

En pocas palabras, es una aplicación web que te permite buscar una calle/avenida/plaza/... en un mapa y obtener información sobre lo que le da nombre a esa dirección.

## ¿Por qué no buscarlo directamente en la wikipedia?

Porque eso no es tan divertido y no hubiera aprendido nada sobre [Flask](http://flask.pocoo.org/), [Jinja2](http://jinja.pocoo.org/), [geocodificación inversa](https://es.wikipedia.org/wiki/Geocodificaci%C3%B3n_inversa), [OpenStreetMap](http://www.openstreetmap.org/), [Nominatim](http://wiki.openstreetmap.org/wiki/Nominatim), [OpenLayers](http://openlayers.org/), Javascript, [Brython](http://www.brython.info), la [API de la wikipedia](https://www.mediawiki.org/wiki/API:Main_page), mis nulas aptitudes para el diseño web (de forma expresa no quería usar cosas como bootstrap para mantenerlo lo más simple posible) [aunque podría ser peor](http://www.theworldsworstwebsiteever.com/), el infierno CSS...

<img class="aligncenter" src="https://raw.githubusercontent.com/kikocorreoso/map2wiki/master/img/CSSHell.gif" alt="CSS hell" />

Pero vayamos por partes...

## ¿Qué es la geocodificación inversa?

La geocodificación inversa (_reverse geocoding_ en inglés) permite, a partir de unas coordenadas geográficas, obtener información sobre una dirección, por ejemplo, u otras cosas que se encuentren en esas coordenadas o cerca.

OpenStreetMap ofrece una API, Nominatim, que permite hacer eso mismo, a partir de unas coordenadas geográficas se obtiene información de su base de datos.

## ¿Cómo funciona?

En este post voy a relatar un poco el **_Así se hizo_** sin ver código, que a veces es más interesante que la película en sí. En otro post comentaré un poco el código por si alguien quiere utilizar alguna parte para otros proyectos.

Existen varias partes que se conectan entre sí.

  * Accedes a una página servida por Flask que ofrece un mapa, gracias a openlayers + openstreetmap.
  * En el mapa, nos podemos mover hasta una dirección que debe estar en español, ya que solo está pensada para ser usada en español. En el frontend tenemos la dirección central del mapa almacenada en una variable para la latitud y otra para la longitud (gracias a Brython/JS).
  * Con la dirección definida, pulsamos sobre el botón de buscar en la wikipedia. Este botón conecta un formulario en HTML, en el cliente, con Flask, en el servidor. Tenemos un formulario con algunos campos ocultos al que le pasaremos las coordenadas obtenidas en el frontend para que sean manejadas en Python gracias a Flask.
  * Una vez que tenemos las coordenadas en Python hacemos varias cosas: 
      * Primero, vamos a la API de Nominatim y le metemos las coordenadas para que nos devuelva un JSON con la información de la dirección relacionada con esas coordenadas.
      * De ese JSON extraemos la información relevante a la dirección y la 'limpiamos' ([sanitizar no está en el diccionario de la RAE](http://lema.rae.es/drae/?val=sanitizar)). En la dirección se eliminan los siguientes términos junto con los posibles preposiciones y/o artículos que pueden acompañar a esa dirección ('calle _de_ ...', 'avenida _de los_ ...',...) 

<pre class=" language-python"><code class=" language-python">
["alameda", "avenida", "bulevar", "calle", "camino", 
 "carrera", "cuesta", "pasaje", "pasadizo", "paseo", "plaza", 
 "rambla", "ronda", "travesia", "via"]</code></pre>

  * Seguimos: 
      * Con la dirección _sanitizada_ solo nos debería quedar el nombre de la dirección ya limpio. Por ejemplo, 'Paseo de la Marquesa de Python' debería quedar como 'Marquesa de Python'. Esa dirección ya limpia se la pasamos a la API de la Wikipedia usando la librería **wikipedia** que podéis encontrar en [pypi](https://pypi.python.org/pypi/wikipedia). Si es posible encontrar algo en la wikipedia usando el valor que le hemos pasado nos devolverá un objeto con la información relevante del artículo.
      * Con el objeto con la información de la wikipedia obtenido extraemos parte de la información y la formateamos para mostrarla en la página.
      * Una vez tenemos la información de Nominatim (el JSON con la información de la dirección) y la información devuelta por la Wikipedia tenemos todo listo para que, mediante Flask, pasar esa información a una plantilla Jinja2, que construirá el HTML final con la información del JSON obtenido y de la Wikipedia, en caso de que sea posible, o un mensaje de error, en el caso de que no sea posible.

Y este es, principalmente, todo el proceso.

En el próximo artículo nos meteremos un poco más en las tripas para poder entender mejor como se unen las piezas. Lo que veamos no pretenderá ser algo exhaustivo sobre Flask, Jinja2 u otras tecnologías.

Espero que a alguien le resulte útil:

  1. la aplicación en sí, para aprender algo de historia, 
  2. la explicación del como se hizo la aplicación, para entender como se juntan las piezas del rompecabezas en una aplicación con una estructura extremadamente simple y sin base de datos detrás.

Hasta la próxima entrada.