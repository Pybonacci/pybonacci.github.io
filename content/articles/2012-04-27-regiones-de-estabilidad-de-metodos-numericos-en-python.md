---
title: Regiones de estabilidad de métodos numéricos en Python
date: 2012-04-27T09:36:19+00:00
author: Juan Luis Cano
slug: regiones-de-estabilidad-de-metodos-numericos-en-python
tags: ecuaciones diferenciales, matplotlib, métodos numéricos, numpy, python

## Introducción

Hoy veremos cómo computar con Python la **región de estabilidad absoluta** de un método numérico para resolver problemas de valores iniciales en ecuaciones diferenciales ordinarias, una herramienta muy importante a la hora de escoger un método numérico adecuado para integrar nuestro problema concreto. Se trata simplemente de otro ejemplo aplicado de lo que publicamos hace unos días sobre [cómo pintar curvas de nivel con matplotlib](http://pybonacci.org/2012/04/13/dibujando-lineas-de-nivel-en-python-con-matplotlib/); si quieres ver otro más, puedes leer nuestro [ejemplo de uso de Basemap y NetCDF4](http://pybonacci.org/2012/04/14/ejemplo-de-uso-de-basemap-y-netcdf4/), donde vimos cómo representar datos climatológicos.

_**En esta entrada se ha usado python 2.7.3, numpy 1.6.1 y matplotlib 1.1.0.**_

<!--more-->

## Región de estabilidad absoluta

A la hora de integrar numéricamente un problema diferencial del tipo

$\frac{d U}{d t} = A U$

nos interesa que la solución numérica tenga el mismo carácter de estabilidad que la solución analítica y saber para qué valores del paso de integración podemos conseguir esto [Hernández]. Mediante los autovalores $\lambda$ de la matriz del sistema o los de la matriz jacobiana que resulta de linealizar el sistema [LeVeque], podemos definir la

> **Región de estabilidad absoluta**: región del plano complejo $\mathcal{R} \subset \mathbb{C}$ tal que el método es estable $\forall \, \omega = \lambda \Delta t \in \mathcal{R}$.

Si la solución de la ecuación en diferencias resultante de discretizar el problema diferencial es de la forma

$u^n = {\displaystyle \sum\_k c\_k r_k^n},$

entonces los $r_k$ deben ser raíces del **polinomio característico de estabilidad** del método numérico:

$\pi(r) |&#095;{\omega} = {\displaystyle \sum\_{j = 0}^p (\alpha\_j - \omega \beta_j) r^{p - j}}$

que no depende del problema que estamos integrando. Si se cumple que el mayor de los valores absolutos de las raíces es menor o igual que 1 entonces la solución numérica será estable (asintóticamente estable en el caso estrictamente menor), e inestable si hay alguna raíz mayor que 1 en valor absoluto. Con esta información, vamos a computar la región de estabilidad absoluta siguiendo el algoritmo que propone [Hernández]:

### Algoritmo

>   1. Discretizar una región del plano complejo $(x\_i, y\_j)$.
>   2. Sea $rho$ una matriz. Para cada $\omega\_{ij} \leftarrow x\_i + i y_j$, 
>       1. Obtener las raíces $r\_k \quad (k = 1, \, \dots, p)$ de $\pi(r) |\_{\omega_{ij}}$.
>       2. $\rho\_{ij} \leftarrow \max(|r\_k|)$
>   3. Representar las curvas de nivel de $\rho$. La $\rho = 1$ será la frontera de la región de estabilidad absoluta y las $\rho < 1$ serán el interior de la misma.

## Código y representación

Vamos a incluir el código en un módulo para poder acceder a esta funcionalidad más fácilmente. El código completo, añadiendo documentación y ejemplos con el [estándar de documentación de NumPy/SciPy](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt), quedaría así:

<pre><code class="language-python"># -*- coding: utf-8 -*-
#
# Región de estabilidad absoluta
# Juan Luis Cano Rodríguez
import numpy as np
def region_estabilidad(p, X, Y):
    """Región de estabilidad absoluta
    Computa la región de estabilidad absoluta de un método numérico, dados
    los coeficientes de su polinomio característico de estabilidad.
    Argumentos
    ----------
    p : function
        Acepta un argumento w y devuelve una lista de coeficientes
    X, Y : numpy.ndarray
        Rejilla en la que evaluar el polinomio de estabilidad generada por
        numpy.meshgrid
    Devuelve
    --------
    Z : numpy.ndarray
        Para cada punto de la malla, máximo de los valores absolutos de las
        raíces del polinomio de estabilidad
    Ejemplos
    --------
    &gt;&gt;&gt; import numpy as np
    &gt;&gt;&gt; x = np.linspace(-3.0, 1.5)
    &gt;&gt;&gt; y = np.linspace(-3.0, 3.0)
    &gt;&gt;&gt; X, Y = np.meshgrid(x, y)
    &gt;&gt;&gt; Z = region_estabilidad(lambda w: [1,
    ... -1 - w - w ** 2 / 2 - w ** 3 / 6 - w ** 4 / 24], X, Y)  # RK4
    &gt;&gt;&gt; import matplotlib.pyplot as plt
    &gt;&gt;&gt; cs = plt.contour(X, Y, Z, np.linspace(0.05, 1.0, 9))
    &gt;&gt;&gt; plt.clabel(cs, inline=1, fontsize=10)  # Para etiquetar los contornos
    &gt;&gt;&gt; plt.show()
    """
    Z = np.zeros_like(X)
    w = X + Y * 1j
   
    for j in range(len(X)):
        for i in range(len(Y)):
            r = np.roots(p(w[i, j]))
            Z[i, j] = np.max(abs(r if np.any(r) else 0))
    return Z</code></pre>

Como sucede casi siempre en Python, el código es casi una traducción literal del algoritmo. Vamos a explicar un poco el código:

  1. Obtenemos los coeficientes del polinomio para `w[i, j]`.
  2. Calculamos las raíces de dicho polinomio con [`np.roots`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.roots.html), que acepta un array de rango 1 o equivalente (por esto no se puede vectorizar el bucle) y devuelve un array con las raíces del polinomio.
  3. La expresión `r if np.any(r) else 0` es un [condicional ternario](http://docs.python.org/reference/expressions.html#conditional-expressions), y tiene la misión de devolver un 0 si el polinomio no tiene raíces (porque todos los coeficientes se han hecho nulos, por ejemplo) para que la función `np.max` no reciba un array vacío. Es equivalente a
  
    <pre><code class="language-python">if np.any(r):
    return r
else:
    return 0</code></pre>

  4. Calculamos el valor absoluto de estas raíces.
  5. Con la función [`np.max`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.amax.html#numpy.amax) calculamos el mayor de estos valores.
  6. Lo asignamos a `Z[i, j]`.

## Resultados

Una vez tenemos esto en un archivo `region_estabilidad.py`, si abrimos un intérprete de IPython en el mismo directorio será tan sencillo como

<pre><code class="language-python">In [1]: import numpy as np
In [2]: x = np.linspace(-3.0, 1.5)
In [3]: y = np.linspace(-3.0, 3.0)
In [4]: X, Y = np.meshgrid(x, y)
In [5]: def p(w):
   ...:     """Polinomio de estabilidad del método RK4."""
   ...:     return [1, -1 - w - w ** 2 / 2 - w ** 3 / 6 - w ** 4 / 24]
   ...:
In [6]: from region_estabilidad import region_estabilidad
In [7]: Z = region_estabilidad(p, X, Y)
In [8]: import matplotlib.pyplot as plt
In [9]: plt.contour(X, Y, Z, np.linspace(0.0, 1.0, 9))
Out[9]:
In [10]: plt.show()</code></pre>

El segundo argumento de `plt.contour` es para especificar los niveles que queremos pintar (normalmente sólo nos interesará hasta el 1.0). Podemos obtener resultados similares a estos:<figure id="attachment_327" style="width: 350px" class="wp-caption aligncenter">

![Adams-Bashfort 3](http://pybonacci.org/images/2012/04/ab3.png)

<p style="text-align:left">
  Y hasta aquí llega el artículo de hoy. Espero que os haya resultado interesante y útil, no olvidéis difundir y comentar 🙂
</p>

<p style="text-align:left">
  ¡Un saludo!
</p>

## Referencias

  * HERNÁNDEZ, Juan A. _Cálculo Numérico en Ecuaciones Diferenciales Ordinarias_. ADI, 2001.
  * LEVEQUE, Randall J. _Finite Difference Methods for Ordinary and Partial Differential Equations_. Society for Industrial and Applied Mathematics, 2007.