---
title: Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)
date: 2012-07-01T13:12:48+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii
tags: gráficos, matplotlib, matplotlib.pyplot, pyplot, python, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. **[Tipos de gráfico III](http://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")**
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

Hasta ahora hemos visto como configurar las ventanas, manejo de las mismas, definir áreas de gráfico, algunos tipos de gráficos... Ahora vamos a continuar viendo tipos de gráficos disponibles desde matplotlib.pyplot. En este caso nos vamos a centrar en otros gráficos que, quizá, sean menos usados que los vistos hasta ahora. Algunos ya los hemos visto en otras entradas, como [gráficos polares](http://pybonacci.org/2012/03/24/dibujando-una-rosa-de-frecuencias/), gráficos de contornos [[1]](http://pybonacci.org/2012/04/13/dibujando-lineas-de-nivel-en-python-con-matplotlib/) [[2]](http://pybonacci.org/2012/04/14/ejemplo-de-uso-de-basemap-y-netcdf4/),...

Vamos a empezar por ver un gráfico tipo tarta de quesitos o tipo tarta o como lo queráis traducir (en inglés se llama pie chart). Estos son los típicos gráficos que ponen en los periódicos con los resultados de elecciones o cosas así. En este caso vamos a ver un ejemplo real a partir de los datos de las visitas por países a este humilde blog:

<pre><code class="language-python">plt.ion()  # Ponemos el modo interactivo
visitas = [43.97, 9.70, 7.42, 6.68, 3.91, 3.85, 3.62, 3.43, 3.16, 3.04] # Definimos un vector con el % de visitas del top ten de países
visitas = np.append(visitas, 100. - np.sum(visitas)) # Introducimos un último elemento que recoge el % de visitas de otros países fuera del top ten
paises = [u'España', u'México', 'Chile', 'Argentina', 'Colombia', 'Ecuador', u'Perú', 'USA', 'Islandia', 'Venezuela', 'Otros']  # Etiquetas para los quesitos
explode = [0, 0, 0, 0, 0, 0, 0, 0.2, 0.2, 0, 0]  # Esto nos ayudará a destacar algunos quesitos
plt.pie(visitas, labels = paises, explode = explode)  # Dibuja un gráfico de quesitos
plt.title(u'Porcentaje de visitas por país')</code></pre>

El resultado se puede ver en el gráfico siguiente. Como habréis adivinado, explode sirve para separar quesitos del centro de la tarta. En este caso hemos separado los quesitos de USA e Islandia para destacar los países no hispanohablantes:

[<img class="aligncenter size-full wp-image-667" title="quesitos" src="http://new.pybonacci.org/images/2012/06/quesitos.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/06/quesitos.png 652w, https://pybonacci.org/wp-content/uploads/2012/06/quesitos-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/06/quesitos.png)

<!--more-->

Como ya hemos comentado anteriormente, ejemplos de gráficos de contornos ya hemos visto varios. Esos gráficos de contornos se hacen a partir de datos de mallas regulares. Pero, ¿qué sucede si tenemos datos que están repartidos de forma irregular? En este caso podemos hacer uso de plt.tricontour y de plt.tricontourf. Existen unas pocas diferencias de uso con respecto a plt.contour y plt.contourf. En este caso, el valor de Z no tiene que ser 2D. Para ver su funcionamiento pensemos en un caso real. Imaginad que tenéis una red de medidas (por ejemplo, temperaturas) repartidas geográficamente en una zona (AVISO, como siempre, los datos que vamos a representar no tienen ningún sentido físico ni pretender representar una situación real y solo se usan para ver el funcionamiento de tricontour y tricontourf, en este caso).

<pre><code class="language-python">plt.ion()  # Ponemos el modo interactivo
x = np.random.rand(20)  # posiciones X de nuestra red de medidas
y = np.random.rand(20)  # posiciones Y de nuestra red de medidas
t = np.random.rand(20)*3000  # valores de Temperatura (ºK) en las posiciones (X, Y)
plt.tricontourf(x, y, t)  # Pintamos las triangulaciones con contornos de color
plt.tricontour(x, y, t, colors = 'k')  # Pintamos las líneas de contorno en color negro
plt.scatter(x, y)  # Pintamos la posición de las estaciones de medida.</code></pre>

El resultado se puede ver en la siguiente figura. Se ha usado plt.scatter para representar la posición de las estaciones de medida:

[<img class="aligncenter  wp-image-672" title="tricontornos" src="http://new.pybonacci.org/images/2012/07/tricontornos.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/07/tricontornos.png 652w, https://pybonacci.org/wp-content/uploads/2012/07/tricontornos-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/07/tricontornos.png)

Por defecto usa una [triangulación de Delaunay](http://es.wikipedia.org/wiki/Triangulaci%C3%B3n_de_Delaunay) pero se puede definir la triangulación que queramos haciendo uso de matplotlib.tri.triangulation.

Todo esto está metido dentro del paquete matplotlib.tri, donde también podréis encontrar tripcolor y  triplot. Probad con todo ello y mandadnos ejemplos para saber como lo usáis y aprender.

También podemos dibujar cuadros de valores que correspondan a una matriz en lugar de interpolar los valores mediante contornos. Puede suceder que, en muchos casos, el número de datos que tengamos en una malla regular sea bajo y una interpolación (usando contour, por ejemplo) dé resultados que pueden quedar feos y no representan fielmente lo que queremos representar. En esos casos podemos usar plt.matshow, que lo que hace es dibujar una matriz con cuadros de colores en función del valor de cada uno de los elementos de la matriz. Vamos a hacer otro ejemplo para que se entienda mejor:

<pre><code class="language-python">plt.ion()  # Ponemos el modo interactivo
x = np.sort(np.random.randn(25))  # Valores de x que vamos a usar posteriormente para crear la matriz
y = np.sort(np.random.randn(25))  # Valores de y que vamos a usar posteriormente para crear la matriz
mat1, mat = np.meshgrid(x, y)  # Creamos dos matrices cuadradas que vamos a cruzar
mat = np.sqrt( mat1**2 + mat2 **2)  # Creamos una matriz final a partir de las dos anteriores
plt.matshow(mat)  # Representamos la última matriz con matshow
plt.contour(np.arange(25), np.arange(25), mat, 10, colors = 'k')  # Colocamos líneas de contorno para la matriz mat</code></pre>

El resultado lo podemos ver en el siguiente ejemplo. En la imagen de la izquierda vemos que las líneas de contorno, en este caso, quedan mal en los bordes y la representación solo usando matshow (imagen de la derecha) sería más adecuada (repito, todos los ejemplos no tienen más sentido que el de explicar el uso de matplotlib.pyplot).

<p style="text-align:center;">
  <a href="http://new.pybonacci.org/images/2012/07/matcont.png"><img class=" wp-image-676 alignnone" title="matcont" src="http://new.pybonacci.org/images/2012/07/matcont.png?w=266" alt="" width="266" height="300" srcset="https://pybonacci.org/wp-content/uploads/2012/07/matcont.png 492w, https://pybonacci.org/wp-content/uploads/2012/07/matcont-266x300.png 266w" sizes="(max-width: 266px) 100vw, 266px" /></a><a href="http://new.pybonacci.org/images/2012/07/matnocont.png"><img class="size-medium wp-image-677 alignnone" title="matnocont" src="http://new.pybonacci.org/images/2012/07/matnocont.png?w=266" alt="" width="266" height="300" srcset="https://pybonacci.org/wp-content/uploads/2012/07/matnocont.png 492w, https://pybonacci.org/wp-content/uploads/2012/07/matnocont-266x300.png 266w" sizes="(max-width: 266px) 100vw, 266px" /></a>
</p>

<p style="text-align:left;">
  Podéis echarle un ojo a plt.pcolor, plt.pcolomesh y plt.tripcolor que permiten hacer cosas similares a estas.
</p>

<p style="text-align:left;">
  plt.hexbin hace algo parecido a lo anterior pero teniendo en cuenta la ocurrencia en los intervalos que determinemos (esto mismo lo podemos hacer, por ejemplo, con plt.matshow aunque tendremos que calcular previamente las frecuencias para cada recuadro). Vamos a representar el número de veces que los valores de dos series (x e y) se encuentran en determinado intervalo de datos. Para ello vamos a recurrir, como siempre, a np.random.randn:
</p>

<pre><code class="language-python">plt.ion()  # Ponemos el modo interactivo
x = np.random.randn(10000)  # Creamos un vector de 10000 elementos distribuidos de forma normal
y = np.random.randn(10000)  # Creamos un vector de 10000 elementos distribuidos de forma normal
plt.hexbin(x,y, gridsize = 20)  # Representamos como están distribuidos bidimensionalmente con ayuda de hexbin, en este caso definimos un tamaño del grid de 20 (esto se puede elegir como se prefiera)
plt.colorbar()  # Colocamos una barra de colores para saber a qué valor corresponden los colores</code></pre>

<p style="text-align:left;">
  El resultado es el siguiente:
</p>

<p style="text-align:left;">
  <a href="http://new.pybonacci.org/images/2012/07/hexbin.png"><img class="aligncenter size-full wp-image-684" title="hexbin" src="http://new.pybonacci.org/images/2012/07/hexbin.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/07/hexbin.png 652w, https://pybonacci.org/wp-content/uploads/2012/07/hexbin-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" /></a>
</p>

<p style="text-align:left;">
  Por último por hoy vamos a dibujar gráficos de flechas. Esto se suele usar para dibujar viento, el movimiento de un fluido, movimiento de partículas, ... En este caso vamos usar plt.quiver (echadle un ojo también a plt.quiverkey y a plt.barbs). Vamos a dibujar flechas de un viento un poco loco en las latitudes y longitudes de la Península Ibérica (no voy a usar un mapa por debajo, si queréis completar el ejemplo usando un mapa podéis echarle un ojo a <a href="http://pybonacci.org/2012/04/14/ejemplo-de-uso-de-basemap-y-netcdf4/">este ejemplo</a>):
</p>

<pre><code class="language-python">plt.ion()  # Ponemos el modo interactivo
lon = np.arange(15) - 10.  # Creamos un vector de longitudes
lat = np.arange(15) + 30.  # Creamos un vector de latitudes
lon, lat = np.meshgrid(lon, lat)  # Creamos un array 2D para las longitudes y latitudes
u = np.random.randn(15 * 15)  # Componente x del vector viento que partirá desde una lon y una lat determinada
v = np.random.randn(15 * 15)  # Componente y del vector viento que partirá desde una lon y una lat determinada
colores = ['k','r','b','g','c','y','gray']  #  Definimos una serie de colores para las flechas
plt.title('Flechas de un viento un poco loco')  # Colocamos un título
plt.xlabel('longitud')  # Colocamos la etiqueta para el efe x
plt.ylabel('latitud')  # Colocamos la etiqueta para el eje y
plt.quiver(lon, lat, u, v, color = colores)  # Dibujamos las flechas 'locas'</code></pre>

El resultado es el siguiente:

[<img class="aligncenter size-full wp-image-685" title="quiver" src="http://new.pybonacci.org/images/2012/07/quiver.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/07/quiver.png 652w, https://pybonacci.org/wp-content/uploads/2012/07/quiver-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/07/quiver.png)

Los colores los hemos colocado de forma aleatoria solo definiendo ocho colores.

Y, de momento, hemos acabado por hoy. El próximo día veremos algún gráfico que no ha entrado dentro de los anteriores capítulos. Si quieres ver las [anteriores entregas del tutorial pulsa aquí](http://pybonacci.org/tag/tutorial-matplotlib-pyplot/). Y si quieres ver la nueva entrega tendrás que esperar que encontremos un ratico para poder hacerla.
