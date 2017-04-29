---
title: MicroEntradas: numpy.unravel_index
date: 2013-07-27T11:09:02+00:00
author: Kiko Correoso
slug: microentradas-numpy-unravel_index
tags: MicroEntradas, numpy, unravel_index

¿Cuántas veces te has encontrado que tienes que conocer un valor concreto de una matriz n-dimensional y conocer la posición en la que se encuentra ese valor en esa matriz? Yo me he visto en esa situación muchas veces y siempre he acabado creando mi función que me dijera la posición,..., hasta que he descubierto [numpy.unravel_index](http://docs.scipy.org/doc/numpy/reference/generated/numpy.unravel_index.html)!!!

[Para la siguiente entrada se ha usado python 2.7.3 y numpy 1.6.1 aunque debería ser compatible con python 3.x y versiones de numpy superiores a la 1.6.0, antes de la versión 1.6.0 de numpy la versión unravel_index solo permitía que le pasáramos un único índice]

Por ejemplo, imagina que quieres encontrar el valor máximo en una matriz 2D como la siguiente:

<pre><code class="language-python">import numpy as np
# Matriz bidimensional de números aleatorios distribuidos
# siguiendo una distribución normal de 100 x 100 elementos
matriz = np.random.randn(100,100)</code></pre>

Para encontrar el valor máximo de la matriz podemos usar [numpy.max](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.max.html?highlight=max#numpy.ndarray.max) (o [numpy.amax](http://docs.scipy.org/doc/numpy/reference/generated/numpy.amax.html#numpy.amax)) y para encontrar el valor de la posición de ese máximo en la matriz podemos usar [numpy.argmax](http://docs.scipy.org/doc/numpy/reference/generated/numpy.argmax.html#numpy.argmax).

<pre><code class="language-python">posicion_maximo = np.argmax(matriz)
print(posicion_maximo)</code></pre>

EL anterior código nos dará un único número. Ese valor que hemos obtenido es la posición del máximo en una matriz que ha sido 'aplanada' a un vector de 1D. Pero yo quiero conocer el valor de la x y de la y en la matriz bidimensional. Para ello existe numpy.unravel_index. Le pasamos el número que hemos encontrado y las dimensiones de la matriz original y nos dirá en qué posición se encuentra en la posición bidimensional. Veamos como se hace:

<pre><code class="language-python">posicion_maximo_2d = np.unravel_index(posicion_maximo, matriz.shape)
print(posicion_maximo_2d)</code></pre>

Et voilà, ya tenemos lo que estábamos buscando.

Antes he comentado que el código solo admite su uso en versiones de numpy superiores o iguales a la 1.6.0. Esto es debido a que si, por ejemplo, quiero buscar la posición de más de un índice de una sola vez lo puedo hacer y con versiones anteriores de numpy esto no era posible. Por ejemplo, si en lugar de solo buscar el máximo quiero el máximo y el mínimo puedo hacer lo siguiente:

<pre><code class="language-python">posicion_maximo = np.argmax(matriz)
posicion_minimo = np.argmin(matriz)
posiciones_2d = np.unravel_index([posicion_minimo, posicion_maximo], matriz.shape)
print(posiciones_2d)</code></pre>

Y listo. Sencillo, limpio y rápido 😀