---
title: Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)
date: 2012-06-23T10:15:09+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii
tags: gráficos, matplotlib, matplotlib.pyplot, pyplot, python, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. **[Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")**
  6. [Tipos de gráfico III](http://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. [Tipos de gráfico IV](http://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")
  8. [Texto y anotaciones (arrow, annotate, table, text...)](http://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")
  9. <del>Herramientas estadísticas (acorr, cohere, csd, psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. [Miscelánea](http://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y matplotlib 1.1.0]**

[DISCLAIMER: Muchos de los gráficos que vamos a representar no tienen ningún sentido físico y los resultados solo pretenden mostrar el uso de la librería].

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

<pre><code class="language-python">import matplotlib.pyplot as plt
import numpy as np</code></pre>

Hasta ahora hemos visto como configurar las ventanas, manejo de las mismas, definir áreas de gráfico, algunos tipos de gráficos... Ahora vamos a continuar viendo tipos de gráficos disponibles desde matplotlib.pyplot. En este caso nos vamos a centrar en los gráficos de barras.

Para dibujar un [histograma](http://es.wikipedia.org/wiki/Histograma) podemos hacer uso de plt.hist. Un histograma suele ser un gráfico de barras donde se representa la ocurrencia de datos (frecuencia) en intervalos definidos. Lo que hace plt.hist es dibujar el histograma de un vector en función del número de intervalos (bins) que definamos. Como siempre, vamos a ver esto con un ejemplo:

<pre><code class="language-python">plt.ion()  # Ponemos el modo interactivo
x = np.random.randn(10000)  # Definimos un vector de números aleatorios de una distribución normal
plt.hist(x, bins = 20)  # Dibuja un histograma dividiendo el vector x en 20 intervalos del mismo ancho</code></pre>

El resultado sería el siguiente, donde se representa el cálculo que haría la función [np.histogram](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html) gráficamente y en un solo paso:

[<img class="aligncenter size-full wp-image-611" title="histograma" src="http://pybonacci.org/wp-content/uploads/2012/06/histograma.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/06/histograma.png 652w, https://pybonacci.org/wp-content/uploads/2012/06/histograma-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/06/histograma.png)

Podéis jugar también con [np.histogram2d](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html#numpy.histogram2d), [np.histogramdd](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogramdd.html#numpy.histogramdd) y [np. bincount](http://docs.scipy.org/doc/numpy/reference/generated/numpy.bincount.html#numpy.bincount)

Si en lugar de dibujar histogramas queremos dibujar gráficos de barras para representar, que se yo, la evolución de la prima de riesgo en los últimos días podemos usar plt.bar<!--more-->

<pre><code class="language-python">import datetime as dt  # Importamos el módulo datetime
prima = 600 + np.random.randn(5) * 10  # Valores inventados para la prima de riesgo
fechas = (dt.date.today() - dt.timedelta(5)) + dt.timedelta(1) * np.arange(5) # generamos las fechas de los últimos cinco días
plt.axes((0.1, 0.3, 0.8, 0.6))  # Definimos la posición de los ejes
plt.bar(np.arange(5), prima)  # Dibujamos el gráfico de barras
plt.ylim(550,650)  # Limitamos los valores del eje y al range definido [450, 550]
plt.title('prima de riesgo')  # Colocamos el título
plt.xticks(np.arange(5), fechas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas</code></pre>

Obtendríamos un resultado como este:

[<img class="aligncenter size-full wp-image-612" title="prima" src="http://pybonacci.org/wp-content/uploads/2012/06/prima.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/06/prima.png 652w, https://pybonacci.org/wp-content/uploads/2012/06/prima-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/06/prima.png)

Si las barras las queréis dibujar en dirección horizontal en lugar de vertical podéis echarle un ojo a matplotlib.pyplot.barh. Siguiendo con los gráficos de barras vamos a ver un caso un poco más especial haciendo uso de matplotlib.pyplot.broken_barh. Queremos representar el tipo de nubosidad que ha habido en un día concreto para saber cuando juanlu ha podido mirar las estrellas con su telescopio. El tipo de nubosidad lo vamos a desglosar en nubes bajas, medias y altas.

<pre><code class="language-python">plt.axes((0.2,0.1,0.7,0.8))  # Creamos los ejes en la posición que queremos
plt.title(u'Evolución para hoy de los tipos de nubosidad')  # Ponemos un título al gráfico
plt.broken_barh([(0,1),(3,3), (10,5), (21,3)], (9500, 1000))  # Dibujamos los momentos en que ha habido nubes altas
plt.broken_barh([(0,24)], (4500, 1000))  # Dibujamos los momentos en que ha habido nubes medias
plt.broken_barh([(0,9), (12,5), (20,2)], (1500, 1000))  # Dibujamos los momentos en que ha habido nubes bajas
plt.xlim(-1,25)  # Limitamos el rango de valores del eje x
plt.yticks([2000, 5000, 10000], ['nubes bajas', 'nubes medias','nubes altas'])  # Colocamos etiquetas en el eje y
plt.xlabel('t(h)')  # Y finalmente ponemos un título al eje x, el eje de tiempos</code></pre>

Además de poder ver que juanlu no ha podido usar su telescopio más que para mirar a la piscina de los vecinos porque el cielo estaba tapado, obtendríamos un resultado como este:

[<img class="aligncenter size-full wp-image-614" title="nubes" src="http://pybonacci.org/wp-content/uploads/2012/06/nubes1.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/06/nubes1.png 652w, https://pybonacci.org/wp-content/uploads/2012/06/nubes1-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/06/nubes1.png)

En plt.broken_barh se define primero los valores de x donde irá una barra y la longitud de esta barra y luego se pone el rango de valores de y para todas las barras definidas en x (además de poder cambiar colores y demás de las barras):

_plt.broken_barh([(x0+longitud para la barra que empieza en x0), (x1+ longitud para la barra que empieza en x1), ..., (tantos x como queramos)], (valor mínimo del rango para y, longitud del rango de y desde el y mínimo), [demás etiquetas que queramos incluir](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.broken_barh))_

Por último para hoy y siguiendo con los gráficos de barras vamos a ver [plt.step](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.step). Esta función nos permite dibujar un gráfico de 'escaleras'. Viendo esto en acción entenderéis mejor a lo que me refiero:

<pre><code class="language-python">x = np.arange(10) + 1
y = np.random.rand(10)
plt.step(x, y, where = 'mid', color = 'r', linewidth = 3)
plt.title(u"Gráfico ejemplo de 'escaleras'")
plt.xlim(0,11)</code></pre>

El where sirve para situar el centro de la escalera (trastead con ello, que es gratis). El resultado sería:

[<img class="aligncenter size-full wp-image-618" title="step" src="http://pybonacci.org/wp-content/uploads/2012/06/step.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/06/step.png 652w, https://pybonacci.org/wp-content/uploads/2012/06/step-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/06/step.png)

Y, de momento, hemos acabado por hoy. El próximo día veremos más tipos de gráfico que podemos hacer con matplotlib.pyplot. Si quieres ver las [anteriores entregas del tutorial pulsa aquí](http://pybonacci.org/tag/tutorial-matplotlib-pyplot/). Y si quieres ver la nueva entrega tendrás que esperar que encontremos un ratico para poder hacerla.