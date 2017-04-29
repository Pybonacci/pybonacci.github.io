---
title: Comprobando presencia de subconjuntos dentro de conjunto de forma eficiente
date: 2015-01-07T21:39:45+00:00
author: Kiko Correoso
slug: comprobando-presencia-de-subconjuntos-dentro-de-conjunto-de-forma-eficiente
tags: conjuntos, diferencia, intersección, numpy, optimización, set, sets, unión

Hoy estaba trabajando con fechas y tenía que encontrar subconjuntos de fechas que estaban presentes o no en otros conjuntos. Numpy nos ofrece varias funciones de ayuda para comprobar este tipo de cosas. Ahora mismo se me vienen a la cabeza [`numpy.in1d`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.in1d.html) y [`numpy.setdiff1d`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.setdiff1d.html). El tema es que necesitaba hacer muchas operaciones de este tipo y he estado buscando la forma de poder optimizar el código un poco y resulta que, dependiendo de la operación, numpy puede resultar hasta 10 veces más lento (según mis pruebas de hoy) que usar puro CPython3. Veamos un ejemplo sencillo:

1) Imaginemos que mis datos son arrays de numpy y quiero conocer los datos de un array `a` que no están presentes en `b`:

<pre class="language-python"><code class="language-python">import numpy as np
a = np.arange(1000000)
b = np.arange(10, 1000010)
%timeit np.setdiff1d(a, b)</code></pre>

Usando IPython y en mi máquina el anterior código me da el siguiente resultado:

<pre class="language-python"><code>10 loops, best of 3: 148 ms per loop</code></pre>

2) Si ahora hago lo mismo usando conjuntos (sets) obtendría el siguiente resultado:

<pre class="language-python"><code class="language-python">a = set(np.arange(1000000))
b = set(np.arange(10, 1000010))
%timeit a.difference(b)</code></pre>

De la misma forma, usando IPython y en mi máquina el anterior código me da el siguiente resultado:

<pre class="language-python"><code>10 loops, best of 3: 30.2 ms per loop</code></pre>

Para este caso concreto numpy es ¡¡¡hasta 5 veces más lento!!!

Esto es una micro-optimización que me ha servido a mi en un caso concreto y si aplica espero que os resulte útil pero ya sabéis que **la optimización prematura es la fuente de todos los males** 🙂

Saludos

**Actualización:**

Como bien comentan tanto Jaime como Chema más abajo, la comparación es tramposa ya que, normalmente, lo que mido no es lo que se hace en un programa completo, se debería de medir el proceso completo. La pretensión de este post era baja y solo mostrar la diferencia de implementaciones entre lo que hace numpy y lo que hace CPython. Os recomiendo que leáis los comentarios para aprender más.

Gracias, Jaime y Chema.