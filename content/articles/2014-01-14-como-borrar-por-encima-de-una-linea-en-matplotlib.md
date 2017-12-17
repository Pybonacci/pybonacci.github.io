---
title: ¿Cómo borrar por encima de una línea en matplotlib?
date: 2014-01-14T13:18:01+00:00
author: Juan Luis Cano
slug: como-borrar-por-encima-de-una-linea-en-matplotlib
tags: clip, matplotlib, python

Inauguramos sección nueva en el 2014 con **las preguntas que nos llegan de nuestros lectores** por las redes sociales o el correo electrónico 🙂 Nos llegan unas cuantas, ¡así que tenemos material para al menos una pregunta semanal! Estas serán entradas breves que publicaremos cada martes y que tratarán de responder vuestras dudas sin rodeos. ¡Si queréis mandar las vuestras no dudéis en [contactar con nosotros](http://pybonacci.org/contacto/ "Contacto")!

Empezamos con Alberto, que me comenta:

> ¿Cómo puedo «borrar» lo que tengo por encima de una línea en matplotlib? He intentado con `fill_between` entre la línea de estabilidad funcional (línea roja) pero solo rellena con color, no sobreescribe que es lo que pretendo. ¿Se te ocurre alguna forma?
> 
> <p style="text-align:center;">
>   <img class="aligncenter  wp-image-2107" alt="Mapa compresor - Primera versión" src="http://pybonacci.org/wp-content/uploads/2014/01/compmap_nozorder.png" width="420" height="316" srcset="https://pybonacci.org/wp-content/uploads/2014/01/compmap_nozorder.png 812w, https://pybonacci.org/wp-content/uploads/2014/01/compmap_nozorder-300x226.png 300w" sizes="(max-width: 420px) 100vw, 420px" />
> </p>

Alberto está escribiendo un programa para dibujar [mapas de actuaciones de turbomáquinas](http://en.wikipedia.org/wiki/Compressor_map) en Python, similares a los que producen programas privativos como GSP ([ejemplos](http://www.gspteam.com/GSPsupport/OnlineHelp/index.html?compressor_map.htm)) o GasTurb ([ejemplos](http://www.gasturb.de/check-the-map.html)). En esos mapas aparece la _línea de estabilidad funcional_ (_surge line_ o _stall line_) por encima de la cual la turbomáquina no puede funcionar. Es preciso, por tanto, borrar todo lo que quede por encima de ella para suprimir información innecesaria del gráfico. El código es un poco complicado, así que voy a comentar solo los conceptos fundamentales.

Lo primero que hice (después de admitir que no tenía ni idea) fue intentar trabajar sobre lo que ya había intentado. Efectivamente, si usas la función `fill_between` el relleno se queda «por debajo» de las líneas que ya había, en lugar de taparlas. Consultando la [documentación de `fill_between`](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.fill_between) vi que admitía un parámetro zorder, que controla la visibilidad de los elementos de la gráfica: por defecto vale 0, y cuanto mayor es más arriba aparece el elemento. Usando un valor lo suficientemente alto se llega a este resultado:

<div>
  <img class="aligncenter  wp-image-2109" alt="Mapa compresor - Segunda versión" src="http://pybonacci.org/wp-content/uploads/2014/01/compmap_zorder.png" width="420" height="316" srcset="https://pybonacci.org/wp-content/uploads/2014/01/compmap_zorder.png 812w, https://pybonacci.org/wp-content/uploads/2014/01/compmap_zorder-300x226.png 300w" sizes="(max-width: 420px) 100vw, 420px" />
</div>

Que es más o menos lo que se pretendía... pero en mi ordenador se vio el detalle fatal: **el color de fondo y la rejilla quedan tapados**. Esta solución no es suficiente.

<!--more-->

A continuación me puse a pensar en si habría alguna manera de calcular la intersección de esas líneas con matplotlib. Ya Kiko escribió un artículo que [utilizaba Shapely para calcular intersecciones entre formas geométricas](http://pybonacci.org/2012/09/20/buscando-esa-playa-en-la-isla-a-mediodia-usando-shapely/ "Buscando esa playa en la isla a mediodía (usando Shapely)"), así que tenía un punto de partida, pero introducir Shapely para resolver algo tan aparentemente simple no me gustaba.

Otra opción era [crear funciones interpolantes usando SciPy](http://pybonacci.org/2013/08/15/ajuste-e-interpolacion-unidimensionales-basicos-en-python-con-scipy/ "Ajuste e interpolación unidimensionales básicos en Python con SciPy") y [calcular intersecciones entre funciones](http://pybonacci.org/2012/10/25/como-resolver-ecuaciones-algebraicas-en-python-con-scipy/ "Cómo resolver ecuaciones algebraicas en Python con SciPy") usando cualquiera de los métodos de optimización disponibles. El problema es que las curvas negras de la figura, que se obtienen con la función contour, no se pueden trasformar en una función tan fácilmente y eso me causaría problemas.

Estaba ya desempolvando mi ejemplar de «Computational Geometry: Algorithms and Applications» cuando se me ocurrió que tal vez matplotlib tuviese el concepto de **máscaras**, es decir, poder utilizar una forma geométrica para enmascarar otra, de la misma forma que usamos máscaras en arrays de NumPy. Y efectivamente, después de un rato buscando en Google encontré justo lo que buscaba: el método [set\_clip\_path](http://matplotlib.org/api/artist_api.html?highlight=set_clip_path#matplotlib.artist.Artist.set_clip_path).

La palabra clave aquí era _clip_, que en inglés quiere decir algo así como «recortar»: hay que pasarle al método la forma que queremos usar para recortar la línea. En este caso, podemos extraer el área que resulta de `fill_between` (hacia abajo esta vez).

Si queremos además incluir etiquetas para las curvas de nivel, podemos definir manualmente su posición para que no queden fuera de la máscara. Esto se hace con el parámetro `manual` de la función [`clabel`](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.clabel).

El código quedaría así:

<pre><code class="language-python">from matplotlib.patches import PathPatch
# Relleno desde la línea hacia abajo
fillb = plt.fill_between(surge_line_x, surge_line_y, color='none')
# Extraemos el Path
path, = fillb.get_paths()
# Lo convertimos en un Patch
mask = PathPatch(path, fc='none')
# Y lo añadimos a la figura
plt.gca().add_patch(mask)
# Lo aplicamos a las curvas de nivel
cs = plt.contour(cx, cy, cz, colors="black")
for contour in cs.collections:
    cs.set_clip_path(mask)
# Posicionamos las etiquetas
labels_xy = [(10.8, 2.0), (12.4, 2.7), (12.4, 3.3)]
plt.clabel(cs, fmt='%1.2f', manual=labels_xy)
# Y aplicamos la máscara a las líneas normales
ll, = plt.plot(lx, ly, color="blue")
ll.set_clip_path(mask)</code></pre>

Y este sería el resultado:

<p style="text-align:center;">
  <a href="http://pybonacci.org/wp-content/uploads/2014/01/compmap_final.png"><img class="aligncenter  wp-image-2111" alt="Mapa compresor - Final" src="http://pybonacci.org/wp-content/uploads/2014/01/compmap_final.png" width="560" height="422" srcset="https://pybonacci.org/wp-content/uploads/2014/01/compmap_final.png 812w, https://pybonacci.org/wp-content/uploads/2014/01/compmap_final-300x226.png 300w" sizes="(max-width: 560px) 100vw, 560px" /></a>
</p>

¡Ahora sí! 🙂

¡Y hasta aquí la pregunta de la semana! **¿Qué te ha parecido el método para llegar a la solución? ¿Se te ocurre una manera mejor? ¿Crees que te será útil para algo que estás haciendo ahora mismo? ¡Cuéntanos en los comentarios!** Y si quieres mandarnos tu pregunta, ya sabes dónde estamos 😉