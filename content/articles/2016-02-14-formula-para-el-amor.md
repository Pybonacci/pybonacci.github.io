---
title: Fórmula para el amor
date: 2016-02-14T06:00:41+00:00
author: Kiko Correoso
slug: formula-para-el-amor
tags: amor, love, Love supreme, mami je t'aime

Esta entrada [se proyectó hace unos doscientos cuarenta y pico días](https://twitter.com/Pybonacci/status/478209983595962368).

Vamos a representar la siguiente fórmula:

${x}^2 + (y - \sqrt{x^2})^2 = 1$

Si despejamos la $y$ nos quedarán las siguientes soluciones:

$y_{1} = \sqrt{x^2} + \sqrt{1 - x^2}$
  
$y_{2} = \sqrt{x^2} - \sqrt{1 - x^2}$

En código Python usando Numpy y Matplotlib tendremos lo siguiente:

<pre><code class="language-python">import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
x = np.linspace(-1,1,50)
y1 = np.sqrt(x * x) + np.sqrt(1 - x * x)
y2 = np.sqrt(x * x) - np.sqrt(1 - x * x)
plt.plot(x, y1, c='r', lw = 3)
plt.plot(x, y2, c='r', lw = 3)
plt.show()</code></pre>

Felicidades a quien corresponda.

Idea copiada literalmente de [aquí](https://news.ycombinator.com/item?id=2218311).