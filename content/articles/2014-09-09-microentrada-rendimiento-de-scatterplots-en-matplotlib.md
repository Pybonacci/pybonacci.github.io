---
title: Microentrada: Rendimiento de scatterplots en matplotlib
date: 2014-09-09T18:22:39+00:00
author: Kiko Correoso
slug: microentrada-rendimiento-de-scatterplots-en-matplotlib
tags: matplotlib, MicroEntradas, rendimiento, scatter, scatterplots

Normalmente, si vas a dibujar pocos puntos en un scatter plot lo normal es usar `scatter` en matplotlib. Sin embargo, si tienes que dibujar una cantidad considerable de puntos, el rendimiento puede ser un factor importante. Como alternativa se puede usar `plot` en lugar de `scatter`.

Veamos un ejemplo muy sencillo de esto y el rendimiento obtenido. vamos a dibujar 100.000 puntos aleatorios y ver los tiempos que obtenemos usando `scatter` y `plot`.

Primero importamos las librerías a usar:

<pre class="language-python"><code class="language-python">import numpy as np
import matplotlib.pyplot as plt
%%matplotlib inline
</code></pre>

Creamos 100.000 puntos aleatorios:

<pre class="language-python"><code class="language-python">x = np.random.rand(100000)
y = np.random.rand(100000)
</code></pre>

Veamos lo que tarda un scatter plot

<pre class="language-python"><code class="language-python">plt.scatter(x,y)
</code></pre>

    1 loops, best of 3: 598 ms per loop

![wpid1](https://pybonacci.org/images/2014/09/wpid-Microentrada_Rendimiento_de_scatterplots_en_matplotlib1.png)

Y ahora lo mismo pero con un plot normal

<pre class="language-python"><code class="language-python">plt.plot(x,y, 'bo')
</code></pre>

    100 loops, best of 3: 9.09 ms per loop

![wpid2](https://pybonacci.org/images/2014/09/wpid-Microentrada_Rendimiento_de_scatterplots_en_matplotlib2.png)

La diferencia entre ambas opciones es:

<center>
  $Rendimiento = \frac{scatter}{plot} = \frac{598}{9.09} \approx 65 $
</center>

_Motivación de esta entrada: hoy en el trabajo he tenido que escribir unos cuantos paneles de figuras 8x8, es decir, 64 figuras en cada panel, con más de 50.000 datos en cada figura y me ha parecido interesante compartir este pequeño truco que tengo por ahí guardado para estos casos_ 🙂
