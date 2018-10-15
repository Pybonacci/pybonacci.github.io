---
title: Hoja de ruta para SciPy 1.0
date: 2013-09-22T14:52:43+00:00
author: Juan Luis Cano
slug: hoja-de-ruta-para-scipy-1-0
tags: euroscipy, python, scipy

Los desarrolladores de SciPy han anunciado, a través de la lista de correo, que se ha preparado un borrador con **la hoja de ruta hacia la consolidación de SciPy 1.0**.

Hoja de ruta:

https://github.com/rgommers/scipy/blob/roadmap/doc/ROADMAP.rst.txt

Anuncio en la lista de correo:

http://mail.scipy.org/pipermail/scipy-dev/2013-September/019237.html

Ralf Gommers, Pauli Virtanen y David Cournapeau se reunieron en la [EuroSciPy](https://pybonacci.org/tag/euroscipy/) que se celebró en Bruselas en agosto y han redactado un documento donde se recogen los pasos necesarios en términos de nueva funcionalidad, solución de fallos, etc. para llegar a SciPy 1.0. Cuando esto se consiga, significará que SciPy contiene lo esencial y que tiene una API y un código de buena calidad.

<blockquote class="twitter-tweet" width="550">
  <p>
    <a href="https://twitter.com/hashtag/scipy?src=hash">#scipy</a> 1.0 roadmap on github: here's your chance to influence the future direction of the package! <a href="https://t.co/vihVbOqsaU">https://t.co/vihVbOqsaU</a>
  </p>
  
  <p>
    &mdash; Jake Vanderplas (@jakevdp) <a href="https://twitter.com/jakevdp/statuses/381518435663892480">September 21, 2013</a>
  </p>
</blockquote>



Como dice Jake Vanderplas, es una oportunidad única para **participar e influir en la dirección que tomará el desarrollo de SciPy**, que es hoy por hoy la piedra angular del ecosistema Python científico junto con NumPy. La gran ventaja de esta hoja de ruta es que está pormenorizado, por cada paquete, en qué estado se encuentra el código y qué áreas necesitan más trabajo, de forma que **es mucho más fácil para potenciales colaboradores decidir en qué quieren ayudar**.

Durante los próximos meses (aunque este proceso se puede demorar todavía algunos años) se seguirán liberando versiones en la rama 0.x donde poco a poco se irán incorporando estos cambios, que incluyen:

  * Limpieza de código antiguo y supresión de duplicidades: `scipy.fftpack`, `scipy.misc`, eliminación de weave.
  * Cambios en la API que rompen la compatibilidad hacia atrás: `scipy.integrate`.
  * Revisión del código para asegurar que produce el resultado correcto: `scipy.stats`, `scipy.signal`.
  * Mejora de la documentación y de la cobertura por tests: `scipy.stats` y en general.
  * Aumento de la eficiencia de los algoritmos.
  * Reescritura en Cython de algunas partes de SciPy: `scipy.cluster`, `scipy.sparse`, `scipy.spatial`.

Cuando estos objetivos se alcancen se liberará SciPy 1.0.

Si estás interesado en empezar a contribuir código a SciPy, deberías también leerte esta guía:

http://docs.scipy.org/doc/scipy-dev/reference/hacking.html

En ella explican la estructura de paquetes de SciPy, cómo organizar el código, cómo disponer un entorno de desarrollo para que sea más fácil probar tus cambios, cómo ejecutar los tests y muchas cosas más.

Desde aquí animamos a todos aquellos lectores que alguna vez hayan pensado en contribuir a SciPy a leer detenidamente el _roadmap_ y la guía para desarrolladores y que nos cuenten qué les parece. **¿Es suficiente con esto? ¿Habéis tenido dificultades para aclararos por dónde empezar? ¿Creéis que hay algo que se podría mejorar? ¿Pensáis que esto puede ser importante para atraer nuevos desarrolladores a SciPy?**

Si tenéis alguna sugerencia que hacer podemos discutirlo juntos y transmitírselo al equipo de desarrolladores 🙂

¡Un saludo!