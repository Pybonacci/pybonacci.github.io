---
title: ¿Cómo encontrar el mínimo de una función usando scipy?
date: 2012-03-28T11:55:12+00:00
author: Kiko Correoso
slug: como-encontrar-el-minimo-de-una-funcion-usando-scipy
tags: downhill simplex algorithm, matplotlib.pyplot, numpy, optimización, python, scipy.optimize

_**NOTICE: Esta entrada es una traducción libre (algunas cosas no serán traducidas por no existir una traducción sencilla en castellano) de un artículo publicado en [The Glowing Python](http://glowingpython.blogspot.com.es/2011/04/how-to-find-minimum-of-function-using.html) con permiso de su autor.**_

_**Para la siguiente entrada se ha usado python 2.7.2, numpy 1.6.1, scipy 0.9.0 y matplotlib 1.1.0**_

En este ejemplo veremos como usar la función **fmin** para minimizar una función. La función **fmin** se encuentra en el módulo optimize de la librería scipy. La función **fmin** usa el algoritmo _downhill simplex_ para encontrar el mínimo de la función objetivo empezando por un punto inicial dado por el usuario. En el ejemplo emezaremos a partir de dos puntos iniciales diferentes para comparar los resultados.

<pre><code class="language-python">import numpy
import matplotlib.pyplot as plt
from scipy.optimize import fmin
# Función objetivo
rsinc = lambda x: -1 * numpy.sin(x)/x
# Empezamos a partir de x = -5
x0 = -5
xmin0 = fmin(rsinc,x0)
# Empezamos a partir de x = -4
x1 = -4
xmin1 = fmin(rsinc,x1)
# Dibujamos la función
x = numpy.linspace(-15,15,100)
y = rsinc(x)
plt.plot(x,y)
# Dibujo de x0 y el mínimo encontrado empezando en x0
plt.plot(x0,rsinc(x0),'bd',xmin0,rsinc(xmin0),'bo')
# Dibujo de x1 y el mínimo encontrado empezando en x1
plt.plot(x1,rsinc(x1),'rd',xmin1,rsinc(xmin1),'ro')
plt.axis([-15,15,-1.3,0.3])
plt.show()</code></pre>

La función **fmin** escribirá algunos detalles sobre el proceso iterativo llevado a cabo (dejamos la salida en inglés, que es lo que encontraréis cuando corráis el ejemplo):

<pre>Optimization terminated successfully.
         Current function value: -0.128375
         Iterations: 18
         Function evaluations: 36
Optimization terminated successfully.
         Current function value: -1.000000
         Iterations: 19
         Function evaluations: 38</pre>

Y la siguiente gráfica aparecerá en la pantalla:

![Uso de la función fmin en scipy.optimize](http://pybonacci.org/wp-content/uploads/2012/03/uso_de_fmin.png)

El punto azul es el mínimo encontrado empezando a partir del diamante azul (x=-5) y el punto rojo es el mínimo encontrado a partir del diamante rojo (x=-4). En este caso, cuando empezamos a partir de x=-5 **fmin** se 'atasca' en un mínimo local mientras que si empezamos a partir de x=-4 **fmin** alcanza el mínimo global.

_**[Thanks to [@JustGlowing](http://twitter.com/#!/JustGlowing) to allow us to translate their articles]**_

Saludos.