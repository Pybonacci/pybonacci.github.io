---
title: MicroEntradas: numpy.digitize
date: 2013-06-30T15:29:42+00:00
author: Kiko Correoso
slug: microentradas-numpy-digitize
tags: bincount, digitize, frecuencias, histogram, histograma, MicroEntradas, numpy, numpy.bincount, numpy.digitize, numpy.histogram

Con esta entrada voy a inaugurar una serie de entradas que serán cortas. La idea detrás de ellas sirve a dos propósitos, fundamentalmente:

  * Ver pequeñas y, quizás, desconocidas funcionalidades prácticas que están dentro de bibliotecas de uso típicas (numpy, scipy, matplotlib,...),
  * intentar aportar algo a Pybonacci dentro de mi apretada agenda (y que se apretará más en unos pocos meses, mi tiempo se ha reducido drásticamente en los últimos tiempos).

Y basta ya de preámbulos, que esto pretende ser corto y práctico.

Hoy vamos a ver [`numpy.digitize`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.digitize.html) que, como la documentación oficial indica, sirve para devolver los índices de los intervalos de datos a los que pertenece cada valor de un array de datos. Las entradas de la función son solo tres, el array en cuestión a evaluar (array), los valores que establecen los intervalos (bins) y una una palabra clave opcional que establece si los valores a tener en cuenta como extremos del intervalo incluyen el extremo derecho o el izquierdo del intervalo (el valor por defecto es right==False, lo cual indica que el intervalo no incluye el extremo derecho, es decir, tendríamos el siguiente caso, bins[i-1] <= x < bins[i]).

El uso puede ser algo tan simple como lo siguiente:

> Problema: Para un grupo de datos con valor comprendido entre 0 y 1 encontrar los datos asociados a los siguientes intervalos y saber qué función hay que aplicar en cada intervalo:
> 
> f(x) = x cuando x <= 0.25
> 
> f(x) = 2x cuando 0.25 > x >= 0.7
> 
> f(x) = 3x cuando x > 0.7

Una solución sencilla usando `np.digitize` podría ser la siguiente:

<pre><code class="language-python">import numpy as np
import matplotlib.pyplot as plt
xarray = np.random.rand(100)
intervalos = [0, 0.25, 0.7, 1]
indices = np.digitize(xarray, intervalos, right=True)
funcs = [lambda x: x, lambda x: 2*x, lambda x: 3*x]
yarray = [funcs[indice-1](x) for x, indice in zip(xarray, indices)]
plt.scatter(xarray, yarray)</code></pre>

El resultado final debería ser una imagen como la siguiente:

[<img class="aligncenter size-full wp-image-1683" alt="(Imagen PNG, 382 × 253 píxeles)" src="http://pybonacci.org/wp-content/uploads/2013/06/imagen-png-382-c397-253-pc3adxeles.png" width="382" height="253" srcset="https://pybonacci.org/wp-content/uploads/2013/06/imagen-png-382-c397-253-pc3adxeles.png 382w, https://pybonacci.org/wp-content/uploads/2013/06/imagen-png-382-c397-253-pc3adxeles-300x198.png 300w" sizes="(max-width: 382px) 100vw, 382px" />](http://pybonacci.org/wp-content/uploads/2013/06/imagen-png-382-c397-253-pc3adxeles.png)

Quizá lo más complicado de entender sea la línea 8 de la anterior porción de código, si no entiendes algo puedes preguntar en los comentarios.

La función `numpy.digitize` podría ser similar en su uso a [`numpy.histogram`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html#numpy.histogram) y a [`numpy.histogramdd`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogramdd.html#numpy.histogramdd). En la [última función se usa internamente](https://github.com/numpy/numpy/blob/v1.7.0/numpy/lib/function_base.py#L349) `numpy.digitize`.

Saludos.