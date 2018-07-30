---
title: Calculando cuantiles con python
date: 2012-09-14T05:59:40+00:00
author: Kiko Correoso
slug: calculando-cuantiles-con-python
tags: cuantiles, cuartiles, deciles, numpy, percentil, percentiles, scipy.stats, scoreatpercentile

Como sabiamente dice la wikipedia, los cuantiles son [medidas de posición no central](http://es.wikipedia.org/wiki/Medidas_de_posici%C3%B3n_no_central) que permiten conocer otros puntos característicos de la distribución. El cuantil de orden _p_ de una distribución (con 0 < p < 1) es el valor de la variable $x\_p$ que marca un corte de modo que una proporción p de valores de la población es menor o igual que $x\_p$. Por ejemplo, el cuantil de orden 0.36 dejaría un 36% de valores por debajo y el cuantil de orden 0.50 se corresponde con la [mediana](http://es.wikipedia.org/wiki/Mediana_%28estad%C3%ADstica%29 "Mediana (estadística)") de la distribución.

Vale, esto es un resumen de la teoría, pero vayamos a practicar un poco con nuestras amadas herramientas (en este caso numpy 1.6.1, matplotlib 1.1.1rc, scipy 0.9.0 y ipython 0.12.1 sobre python 2.7.3).

Iniciamos haciendo lo siguiente:

<pre><code class="language-python">import numpy as np
from scipy import stats
import matplotlib.pyplot as plt</code></pre>

Imaginad que tenéis una distribución normal discreta (la altura de 10.000 chavales de 18 años de vuestro pueblo, por ejemplo) con desviación estándar 20 y media 180.

<pre><code class="language-python">alturas = 20 * np.random.randn(10000) + 180
plt.hist(alturas, 50)
plt.show()</code></pre>

Obtendríamos la siguiente distribución que tiene, aproximadamente, la media y desviación estándar que hemos comentado anteriormente.

![histograma](http://pybonacci.org/images/2012/09/histograma.png)

Vamos ahora al lío que nos ha traído aquí, vamos a calcular un percentil de esa distribución para saber cuanto mide el chaval que está en el percentil 75. Para hacer ese cálculo podemos acudir tanto a [numpy](http://docs.scipy.org/doc/numpy/reference/generated/numpy.percentile.html) como a la librería [stats de scipy](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.scoreatpercentile.html). Vamos a usar ambas para ver el resultado:

<pre><code class="language-python">perc75np = np.percentile(alturas, 75)
perc75sc = stats.scoreatpercentile(alturas, 75)</code></pre>

Deberíamos obtener exactamente lo mismo, en mi caso me sale un valor de 190.311633094 (recordad que hemos generado la muestra de forma aleatoria y vuestro resultado no debe ser exactamente igual al mío).

Si queremos calcular los deciles del 1 al 9 podemos hacerlo mediante las funciones que hemos visto y con ayuda de una [list comprehension](http://docs.python.org/tutorial/datastructures.html#list-comprehensions):

<pre><code class="language-python">deciles = np.arange(1, 10) * 10
deciles_dist = [np.percentile(alturas, dec) for dec in deciles]</code></pre>

El primer decil dejaría el 10% de los datos de la distribución a la izquierda, el segundo decil el 20% y así hasta el 9 decil que dejaría el 90% de datos a la izquierda. Si dibujamos estos datos sobre la distribución anterior obtendríamos la siguiente imagen:

<pre><code class="language-python">plt.hist(alturas, 50)
y = np.repeat(100,9)  # http://docs.scipy.org/doc/numpy/reference/generated/numpy.repeat.html
plt.plot(deciles_dist, y, 'ko')
plt.show()</code></pre>

Cuya representación sería:

![Hist_con_deciles](http://pybonacci.org/images/2012/09/hist_con_deciles.png)

Espero que os resulte útil el descubrimiento de np.percentile o de scipy.stats.scoreatpercentile para vuestros cálculos.

Saludos.