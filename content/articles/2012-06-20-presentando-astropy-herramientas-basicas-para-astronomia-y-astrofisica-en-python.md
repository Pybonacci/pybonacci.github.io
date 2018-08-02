---
title: Presentando Astropy: herramientas básicas para Astronomía y Astrofísica en Python
date: 2012-06-20T11:30:36+00:00
author: Juan Luis Cano
slug: presentando-astropy-herramientas-basicas-para-astronomia-y-astrofisica-en-python
tags: astrofísica, astronomía, astropy, foss, python

Ayer se liberó [Astropy](http://www.astropy.org/) 0.1, la primera versión de este paquete Python que aspira a unificar las herramientas y utilidades básicas necesarias en **astronomía** y **astrofísica**. Puedes leer [el anuncio](http://mail.scipy.org/pipermail/astropy/2012-June/002103.html) en la lista de correo de Astropy.<figure id="attachment_604" style="width: 560px" class="wp-caption aligncenter">

![Gráfica con APLpy](http://pybonacci.org/images/2012/06/aplpy-plot.png)

El lenguaje Python está teniendo bastante impulso en ámbitos científicos durante los últimos años, y uno de los campos donde es bastante activo es en **astronomía**. El [proyecto Astropy](http://www.astropy.org/vision.html) nació con el objetivo de incluir los paquetes usados para las tareas más básicas (manejo de imágenes FITS, tablas, coordenadas, ...). No pretende incluir _todo_ lo que un astrónomo necesita, sino que intenta ser una especie de base común sobre la que construir proyectos más complejos. Es una especie de NumPy de la astronomía.

Como dicen en la nota, la biblioteca Astropy no está completa todavía, pero la funcionalidad existente ya se puede utilizar y está muy probada. Esta incluye

  * Cálculos estándar de distancias astronómicas ([`astropy.cosmology`](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/cosmology/index.html)).
  * Tablas ([`astropy.table`](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/table/index.html)) incluyendo una gran variedad de formatos ASCII comunes en astronomía (astropy.io.ascii).
  * Manejo de archivos [FITS](http://es.wikipedia.org/wiki/FITS) (antes PyFITS) ([`astropy.io.fits`](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/io/fits/index.html)).
  * Lectura y escritura de archivos [VOTable](http://www.ivoa.net/cgi-bin/twiki/bin/view/IVOA/IvoaVOTable) ([`astropy.io.vo`](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/io/vo/index.html)).
  * Representaciones [WCS](http://fits.gsfc.nasa.gov/fits_wcs.html) (antes pywcs) ([`astropy.wcs`](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/wcs/index.html)).
  * [Documentación](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/index.html) completa y consistente.
  * Utilidades para la creación de nuevos paquetes independientes (paquetes «afiliados»).
  * Un [sistema de logging](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/logging.html) dedicado.

Puedes consultar en su web la [documentación de Astropy](http://astropy.readthedocs.org/en/tmp-v0.1-wcython/index.html), y puedes colaborar [informando sobre fallos](https://github.com/astropy/astropy/issues) o [contribuyendo código](https://github.com/astropy/astropy) a través de GitHub. También puedes seguir la [cuenta de Twitter de Astropy](https://twitter.com/#!/astropy) para estar al corriente de las últimas novedades.

Si la astronomía es tu campo y estás interesado en cómo puedes utilizar Python, hay más **recursos que pueden serte útiles**:

  * El curso [Practical Python for Astronomers](http://python4astronomers.github.com/) es imprescindible: contiene mucha información valiosa sobre por qué y cómo usar Python en astronomía, qué paquetes se utilizan, cómo manejar datos y crear gráficas y más. De este curso está sacada la imagen que acompaña la entrada, hecha con el paquete [APLpy](http://aplpy.github.com/) (Astronomical Plotting Library in Python).
  * En la web de [AstroPython](http://www.astropython.org/) puedes encontrar tutoriales, herramientas y ejemplos para investigación en astronomía. También puedes seguir la [cuenta de Twitter de AstroPython](https://twitter.com/#!/AstroPython).

Y tú, ¿ya estabas utilizando Python para desarrollar tu trabajo en astronomía? ¿Conoces algún otro recurso que pueda resultar interesante? Si no lo usabas ya, ¿te hemos convencido para probarlo? Déjanos tus comentarios [en la entrada](#respond) o [en Twitter](https://twitter.com/Pybonacci) 🙂