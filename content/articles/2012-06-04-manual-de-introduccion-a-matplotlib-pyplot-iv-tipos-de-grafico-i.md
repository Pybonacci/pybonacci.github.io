---
title: Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)
date: 2012-06-04T18:49:12+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i
tags: gráficos, matplotlib, matplotlib.pyplot, pyplot, python, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. **[Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")**
  5. [Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
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

Hasta ahora hemos visto como configurar las ventanas, manejo de las mismas, definir áreas de gráfico,... Ahora vamos a ir viendo los diferentes tipos de gráficos que existen.

Como habéis podido comprobar, en los ejemplos anteriores hemos estado viendo mucho plt.plot() que es lo que se suele usar para dibujar un gráfico simple de líneas representando los valores (x, f(x)). Ahora vamos a ver un ejemplo explicado para que veáis todas las posibilidades de plt.plot().

<pre><code class="language-python">plt.ion()  # Nos ponemos en modo interactivo
x = np.arange(100)  # Valores de x
y = np.random.rand(100)  # Valores de y
plt.plot(x,y, color = 'black', label = '(x, f(x)')  # Dibujamos la evolución de f(x), frente a x
plt.plot(x[y &gt; 0.9], y[y &gt; 0.9], 'bo', label = 'f(x) &gt; 0.9')  # Destacamos los valores por encima de 0.9 colocándoles un marcador circular azul
plt.axhspan(0.9, 1, alpha = 0.1)  # Colocamos una banda de color para los valores f(x) &gt; 0.9
plt.ylim(0,1.2)  # Limitamos el eje x
plt.legend()  # Colocamos la leyenda
plt.title(u'Representación de (x, f(x))')  # Colocamos el título del gráfico
plt.xlabel('valores x')  # Colocamos la etiqueta en el eje x
plt.ylabel('valores f(x)')  # Colocamos la etiqueta en el eje y</code></pre>

[<img class="aligncenter size-full wp-image-484" title="ejemplo plot" src="http://pybonacci.org/wp-content/uploads/2012/05/ejemplo-plot.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/05/ejemplo-plot.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/ejemplo-plot-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/05/ejemplo-plot.png)

Este es el tipo de gráfico que suelo usar un 75% de las veces. Tipos de gráfico análogos a este son plt.plot_date(), que es similar a plt.plot() considerando uno o ambos ejes como fechas, y plt.plotfile(), que dibuja directamente desde los datos de un fichero.

Otro tipo de gráfico sería el que podemos obtener con plt.stem(). Dibuja líneas verticales desde una línea base. Imaginaros, por ejemplo, que tenéis una serie temporal, la normalizamos (restándole su <!--more-->media y dividiendo por su desviación estándar) de forma que nos queda una serie de media 0 y desviación estándar 1. Esta nueva serie la podemos representar con plt.stem() donde la línea horizontal sería el valor medio (en este caso la media sería 0, recuerda que la hemos normalizado la serie) y las líneas verticales sería lo que se desvía el valor individual respecto de la media de la serie. Vamos a ver un ejemplo con los valores por encima de la media en verde y los valores por debajo de la media en rojo.

<pre><code class="language-python">plt.ion()  # Nos ponemos en modo interactivo
x = np.arange(25) + 1  # Valores de x
y = np.random.rand(25) * 10.  # Valores de y
y_norm = (y - y.mean()) / y.std()  # Valores de y normalizados. Esta nueva serie tiene media 0 y desvicación estándar 1 (comprobadlo como ejercicio)
plt.xlim(np.min(x) - 1, np.max(x) + 1)  # Colocamos los límites del eje x
plt.ylim(np.min(y_norm)-1, np.max(y_norm)+1)  # Colocamos los límites del eje y
plt.stem(x[y_norm &gt; 0],y_norm[y_norm &gt; 0], linefmt='k-.', markerfmt='go', basefmt='b-')  # Dibujamos los valores por encima de la media
plt.stem(x[y_norm &lt; 0],y_norm[y_norm &lt; 0], linefmt='k-.', markerfmt='ro', basefmt='b-')  # Dibujamos los valores por debajo de la media
plt.title(u'Representación de (x, f(x))')  # Colocamos el título del gráfico
plt.xlabel('valores x')  # Colocamos la etiqueta en el eje x
plt.ylabel('valores f(x)')  # Colocamos la etiqueta en el eje y</code></pre>

[<img class="aligncenter size-full wp-image-487" title="ejemplo_stem" src="http://pybonacci.org/wp-content/uploads/2012/05/ejemplo_stem.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/05/ejemplo_stem.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/ejemplo_stem-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/05/ejemplo_stem.png)

En algunos casos, nos interesa ver cuando una serie está por encima o por debajo de la otra. Eso, con un gráfico tipo plt.plot() lo podemos hacer sin problemas, pero nos gustaría resaltarlo visualmente de forma sencilla. Para ello podemos usar plt.fill_between(). Imaginemos un ejemplo donde tenemos dos series temporales y queremos localizar fácilmente cuando la primera está por encima de la segunda y cuando está por debajo.

<pre><code class="language-python">plt.ion()  # Nos ponemos en modo interactivo
x = np.arange(25) + 1  # Valores de x
y1 = np.random.rand(25) * 10.  # Valores de y1
y2 = np.random.rand(25) * 10.  # Valores de y2
plt.xlim(np.min(x) - 1, np.max(x) + 1)  # Colocamos los límites del eje x
plt.ylim(np.min([y1, y2])-1, np.max([y1, y2])+1)  # Colocamos los límites del eje y
plt.plot(x, y1, 'k-', linewidth = 2, label = 'Serie 1')  # Dibujamos los valores de (x,y1) con una línea contínua
plt.plot(x, y2, 'k-.', linewidth = 2, label = 'Serie 2')  # Dibujamos los valores de (x,y2) con una línea de punto y raya
plt.fill_between(x, y1, y2, where = (y1 &lt; y2), color = 'g', interpolate = True)  # Pinta polígonos color verde entre las líneas cuando y1 &lt; y2 plt.fill_between(x, y1, y2, where = (y1 &gt; y2), color = 'r', interpolate = True)  # Pinta polígonos color rojo entre las líneas cuando y1 &gt; y2
plt.legend()
plt.title('Ejemplo de plt.fill_between()')  # Colocamos el título del gráfico
plt.xlabel('valores x')  # Colocamos la etiqueta en el eje x
plt.ylabel('valores y')  # Colocamos la etiqueta en el eje y</code></pre>

[<img class="aligncenter size-full wp-image-491" title="ejemplo_fillbetween" src="http://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fillbetween.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fillbetween.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fillbetween-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fillbetween.png)
  
Recordad que usamos valores aleatorios para y1 e y2 por lo que si usáis ese código no os tiene porque dar lo mismo. Como veis, cuando los valores de y2 son mayores que los de y1 dibuja polígonos verdes, en caso contrario dibuja polígonos rojos. Algo parecido pero para el eje y en lugar de para el eje x lo podemos hacer usando plt.fill_betweenx(). También podemos dibujar el polígono que queramos sobre el gráfico usando plt.fill().Veamos una 'ki-cutrez' usando plt.fill():

<pre><code class="language-python">plt.ion()  # Nos ponemos en modo interactivo
s1x = [0.3,0.3,0.7,0.7,0.5,0.5,1,1,0.7,0.7]
s1y = [0.5,1.4,1.4,1.5,1.5,1.9,1.9,1.1,1.1,0.5]
o1x = [0.6,0.6,0.7,0.7]
o1y = [1.7,1.8,1.8,1.7]
s2x = [0.8,0.8,1.1,1.1,1.5,1.5,1.1,1.1,1.3,1.3]
s2y = [0.2,1,1,1.6,1.6,0.7,0.7,0.6,0.6,0.2]
o2x = [1.1,1.1,1.2,1.2]
o2y = [0.3,0.4,0.4,0.3]
plt.fill(s1x, s1y, color = 'b')
plt.fill(o1x,o1y, color = 'w')
plt.fill(s2x, s2y, color = 'g')
plt.fill(o2x,o2y, color = 'w')
plt.title(u'Símbolo de python cutre')
plt.ylim(0.1,2)</code></pre>

[<img class="aligncenter size-medium wp-image-492" title="ejemplo_fill" src="http://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fill.png?w=300" alt="" width="300" height="254" srcset="https://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fill.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fill-300x254.png 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://pybonacci.org/wp-content/uploads/2012/05/ejemplo_fill.png)

Y ya lo último que vamos a ver hoy es un diagrama de caja-bigote ([box plot o box-whisker diagram](http://polimedia.upv.es/visor/?id=f28a58a0-ef5d-8643-9113-15fdcab1489e#)). Este es un diagrama donde se puede ver un resumen de una serie de forma rápida y sencilla. En él se representa el primer cuartil y el tercer cuartil, que son los extremos de la caja, el valor de la mediana (o segundo cuartil), que se representa mediante una línea dentro de la caja, y los extremos de la serie que no se consideran anómalos, los llamados 'bigotes', que son los valores extremos que están dentro del rango de 1.5 veces el rango intercuartílico (IQR por sus siglas en inglés, Inter Quartil Range). Los valores que quedan fuera de este rango que definamos, que como hemos comentado suele ser 1.5xIQR, se consideran valores anómalos u '[outliers](http://en.wikipedia.org/wiki/Outlier)' y se representan como puntos fuera de los bigotes. Por tanto, imaginemos que estamos representando la altura de las mujeres que viven en España, las mujeres que viven en Alemania y las mujeres que viven en Tailandia. Con un diagrama de caja-bigote podemos ver rápidamente como se distribuyen cada uno de estos conjuntos de datos y podemos compararlos visualmente entre ellos.

<pre><code class="language-python">plt.ion()  # Nos ponemos en modo interactivo
alt_esp = np.random.randn(100)+165 + np.random.randn(100) * 10  # Creamos unos valores para la altura de 100 españolas
alt_ale = np.random.randn(100)+172 + np.random.randn(100) * 12  # Creamos unos valores para la altura de 100 alemanas
alt_tai = np.random.randn(100)+159 + np.random.randn(100) * 9   # Creamos unos valores para la altura de 100 tailandesas
plt.boxplot([alt_esp, alt_ale, alt_tai], sym = 'ko', whis = 1.5)  # El valor por defecto para los bigotes es 1.5*IQR pero lo escribimos explícitamente
plt.xticks([1,2,3], ['Esp', 'Ale', 'Tai'], size = 'small', color = 'k')  # Colocamos las etiquetas para cada distribución
plt.ylabel(u'Altura (cm)')</code></pre>

[<img class="aligncenter size-full wp-image-497" title="boxplot" src="http://pybonacci.org/wp-content/uploads/2012/05/boxplot.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/05/boxplot.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/boxplot-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/05/boxplot.png)

[TODO ESTE COMENTARIO ES PARA COMENTAR EL GRÁFICO, CUALQUIER PARECIDO CON LA REALIDAD SERÍA MUY RARUNO Y HABRÍA QUE LLAMAR A [FRIKER JIMÉNEZ](https://en.wikipedia.org/wiki/Iker_Jim%C3%A9nez)] Vemos como las alemanas presentan alturas superiores y las tailandesas son las que, en general, mostrarían alturas inferiores. En las alemanas hay algunas mujeres que quedan por encima de lo que hemos considerado como valores normales llegando a alturas por encima de los 200 cm. Las españolas se encontrarían entre unas alturas de unos 140 cm y unos 190 cm.

Y, de momento, hemos acabado por hoy. El próximo día veremos más tipos de gráfico que podemos hacer con matplotlib.pyplot. Si quieres ver las [anteriores entregas del tutorial pulsa aquí](http://pybonacci.org/tag/tutorial-matplotlib-pyplot/). Y si quieres ver la nueva entrega [pincha aquí](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/).
