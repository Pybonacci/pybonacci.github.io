---
title: Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones
date: 2012-08-24T20:19:21+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones
tags: matplotlib, matplotlib.pyplot, pyplot, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. [Tipos de gráfico III](http://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. [Tipos de gráfico IV](http://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")
  8. **[Texto y anotaciones (arrow, annotate, table, text...)](http://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")**
  9. <del>Herramientas estadísticas (acorr, cohere, csd, psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. [Miscelánea](http://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y matplotlib 1.1.0 ]**

[DISCLAIMER: Muchos de los gráficos que vamos a representar no tienen ningún sentido físico y los resultados solo pretenden mostrar el uso de la librería].

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

<pre><code class="language-python">import matplotlib.pyplot as plt
import numpy as np
plt.ion()</code></pre>

Hasta ahora hemos visto como configurar las ventanas, manejo de las mismas, definir áreas de gráfico, algunos tipos de gráficos... En esta ocasión nos interesa ver como podemos meter anotaciones, tablas,..., en nuestros gráficos.

A lo largo de las anteriores entregas del tutorial hemos podido ver algunas formas de tener anotaciones típicas para el título, los ejes, leyenda,... (title, suptitle, xlabel, ylabel, figtext, legend,...). En este caso vamos a revisar las posibilidades de escribir texto personalizado mediante el uso de [plt.text](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.text), [plt.arrow](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.arrow), [plt.annotate](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.annotate) y [plt.table](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.table).

<!--more-->

Como caso sencillo para anotar texto en nuestro gráfico podemos usar [plt.text](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.text). En el siguiente ejemplo vamos a resaltar donde está el valor máximo y el valor mínimo de una serie de datos:

<pre><code class="language-python">a = np.random.rand(10)  # Creamos una serie de 10 valores pseudo-aleatorios entre 0 y 1
plt.plot(a)  # Los dibujamos
plt.ylim(-0.2, 1.2)  # Definimos el rango de valores para el eje y
plt.text(np.argmin(a), np.min(a) - 0.1, u'Mínimo', fontsize = 10, horizontalalignment='center', verticalalignment='center')  # Colocamos texto cerca del valor donde se encuentra el mínimo
plt.text(np.argmax(a), np.max(a) + 0.1, u'Máximo', fontsize = 10, horizontalalignment='center', verticalalignment='center')  # Colocamos texto cerca del valor donde se encuentra el máximo</code></pre>

El resultado es el siguiente:

[<img class="aligncenter size-full wp-image-762" title="texto" alt="" src="http://new.pybonacci.org/images/2012/08/texto.png" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/08/texto.png 652w, https://pybonacci.org/wp-content/uploads/2012/08/texto-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/08/texto.png)

Lo que hemos hecho en [plt. text](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.text) es definir la posición del texto con un valor para la x y un valor para la y (en el sistema de referencia de los datos), la cadena de texto a mostrar, como queremos que sea la fuente, donde queremos que vaya colocado, si la queremos rotar, si la queremos en negrita,...

Al anterior ejemplo le podemos incluir una flecha que una el texto con la representación del valor máximo y del valor mínimo. Para ello podemos usar [plt.arrow](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.arrow) modificando ligeramente el anterior código:

<pre><code class="language-python">plt.plot(a)
plt.ylim(-0.5, 1.5)  # Extendemos un poco el rango del eje y
plt.text(np.argmax(a), np.max(a) + 0.4, u'Máximo', fontsize = 10, horizontalalignment='center', verticalalignment='center')  # Recolocamos el texto del máximo
plt.text(np.argmin(a), np.min(a) - 0.4, u'Mínimo', fontsize = 10, horizontalalignment='center', verticalalignment='center')  # Recolocamos el texto del mínimo
plt.arrow(np.argmax(a), np.max(a) + 0.3, 0, -0.3, length_includes_head = "True", shape = "full", width=0.07, head_width=0.1)  # Unimos el texto al valor representado
plt.arrow(np.argmin(a), np.min(a) - 0.3, 0, 0.3, length_includes_head = "True", shape = "full", width=0.07, head_width=0.1)  # Unimos el texto al valor representado</code></pre>

El resultado obtenido es el siguiente:

[<img class="aligncenter size-full wp-image-763" title="texto y flecha" alt="" src="http://new.pybonacci.org/images/2012/08/texto-y-flecha.png" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/08/texto-y-flecha.png 652w, https://pybonacci.org/wp-content/uploads/2012/08/texto-y-flecha-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/08/texto-y-flecha.png)

En [plt.arrow](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.arrow) hemos de definir el origen de la flecha, la distancia desde ese origen hasta el otro extremo de la flecha, si queremos que tenga cabecera, si queremos que la cabecera esté en el origen, el color de la flecha,...

Lo que hemos hecho con [plt.text](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.text) y con [plt.arrow](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.arrow) lo podemos hacer de forma más compacta y elegante con [plt.annotate](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.annotate). Como anteriormente, hacemos uso de un ejemplo y vamos viendo las partes a modificar de [plt.annotate](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.annotate):

<pre><code class="language-python">plt.plot(a)
plt.ylim(-0.5, 1.5)  # Extendemos un poco el rango del eje y
plt.annotate(u'Máximo', xy = (np.argmax(a), np.max(a)), xycoords = 'data', xytext = (np.argmax(a) - 1.5, np.max(a) + 0.4), textcoords = 'data', arrowprops = dict(arrowstyle = "-&gt;"))
plt.annotate(u'Mínimo', xy = (np.argmin(a), np.min(a)), xycoords = 'data', xytext = (np.argmin(a) + 1, np.min(a) + 1.2), textcoords = 'data', arrowprops = dict(arrowstyle = "-&gt;"))</code></pre>

Siendo el resultado el siguiente:

[<img class="aligncenter size-full wp-image-765" title="annotate" alt="" src="http://new.pybonacci.org/images/2012/08/annotate.png" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/08/annotate.png 652w, https://pybonacci.org/wp-content/uploads/2012/08/annotate-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/08/annotate.png)

En [plt.annotate](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.annotate) introducimos la cadena de caracteres a mostrar, indicamos hacia donde apuntará esa cadena de caracteres (xy, en este caso estamos usando el sistema de referencia de los datos, 'data', pero podemos usar píxeles, puntos,...), la posición del texto (xytext), y como se representará la flecha. Con [plt.annotate](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.annotate) podemos tener anotaciones elegantes de forma sencilla como puedes ver en estos enlaces [[1]](http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/annotation_demo2_00.png), [[2].](http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/annotation_demo2_01.png)

Por último, vamos a ver como podemos dibujar una tabla de forma sencilla. Con [plt.table](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.table) podemos meter rápidamente una tabla pero por defecto la mete debajo del eje x. Vamos a ver un [ejemplo que he encontrado en SO](http://stackoverflow.com/questions/8524401/how-can-i-place-a-table-on-a-plot-in-matplotlib) donde metemos la tabla dentro de los ejes.

<pre><code class="language-python">valores = [[np.argmax(a), np.argmin(a)], [np.max(a), np.min(a)]]
etiquetas_fil = ('x', 'y')
etiquetas_col = (u'Máximo', u'Mínimo')
plt.plot(a)
plt.table(cellText=valores, rowLabels=etiquetas_fil, colLabels = etiquetas_col, colWidths = [0.3]*len(a), loc='upper center')</code></pre>

Cuyo resultado es el siguiente:

[<img class="aligncenter size-full wp-image-766" title="table" alt="" src="http://new.pybonacci.org/images/2012/08/table.png" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/08/table.png 652w, https://pybonacci.org/wp-content/uploads/2012/08/table-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/08/table.png)

Donde hemos definido los valores de las celdas internas (cellText), Las etiquetas de filas y columnas (rowLabels y colLabels), el ancho de las celdas y la localización de la tabla.

Y, después de este breve entrada, hemos acabado por hoy haciendo un montón de anotaciones. Si quieres ver las [anteriores entregas del tutorial pulsa aquí](http://pybonacci.org/tag/tutorial-matplotlib-pyplot/). Y si quieres ver la nueva entrega tendrás que esperar un poquito (pero muy poquito esta vez, espero).