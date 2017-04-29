---
title: Cómo crear una matriz tridiagonal en Python con NumPy y SciPy
date: 2012-05-10T10:41:37+00:00
author: Juan Luis Cano
slug: como-crear-una-matriz-tridiagonal-en-python-con-numpy-y-scipy
tags: ecuaciones diferenciales, EDOs, EDPs, matrices, numpy, python, scipy, scipy.sparse

## Introducción

En este rápido apunte vamos a ver cómo construir una [matriz tridiagonal](http://en.wikipedia.org/wiki/Tridiagonal_matrix) en Python utilizando NumPy y SciPy. Una **matriz tridiagonal** es una matriz _cuadrada _que solamente tiene elementos distintos de cero en su diagonal principal y en las dos diagonales adyacentes a esta (la superdiagonal y la subdiagonal). Las matrices tridiagonales aparecen mucho en cálculo numérico, por ejemplo en la discretización de ecuaciones diferenciales, y tienen la característica de ser **matrices dispersas** (en lugar de _densas_) al ser la mayoría de sus elementos cero.

Sin que sirva de precedente, hoy vamos a escribir código que sea compatible tanto con Python 2 como con Python 3. Es un cambio nimio, pero merece la pena ir acostumbrándose a pensar que tarde o temprano habrá que abandonar Python 2 🙂

_**En esta entrada se ha usado python 2.7.3, numpy 1.6.1 y scipy 0.10.1**_ **y es compatible con ****python 3.2.3**_**.**_

<!--more-->

## Problema matemático

Como ejemplo, vamos a construir la matriz del sistema de ecuaciones diferenciales ordinarias que resulta de discretizar la ecuación del calor unidimensional

${displaystyle frac{partial u}{partial t} = mathcal{L}(u) = frac{partial^2 u}{partial x^2}}$

en el dominio $x in [0, 1]$. Aproximando el operador $mathcal{L}$ mediante [diferencias centradas](http://es.wikipedia.org/wiki/Diferencia_finita) de orden 2 en los puntos de colocación $x\_0,, x\_1,, dots,, x_N$, se obtiene para los puntos interiores

${displaystyle frac{d u\_j}{d t} = frac{1}{Delta x^2} (u\_{j + 1} - 2 u\_j + u\_{j - 1})}$

que, expresado matricialmente, queda

${displaystyle frac{d U}{d t} = A U + b}$

con

$U = begin{pmatrix} u\_1 \ u\_2 \ vdots \ u_{N - 1} end{pmatrix}$

y

$latex

A = begin{pmatrix}
  
-2 & 1 & 0 & 0 & dots & 0 & 0 & 0 \
  
1 & -2 & 1 & 0 & dots & 0 & 0 & 0 \
  
0 & 1 & -2 & 1 & dots & 0 & 0 & 0 \
  
vdots & vdots & vdots & vdots & ddots & vdots & vdots & vdots \
  
0 & 0 & 0 & 0 & dots & 0 & 1 & -2
  
end{pmatrix}

$

Esta matriz es la que vamos a construir.

## Matriz tridiagonal

Para crear la matriz tridiagonal, vamos a utilizar la función [`spdiags`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.spdiags.html#scipy.sparse.spdiags) del [módulo `sparse` de SciPy](http://docs.scipy.org/doc/scipy/reference/sparse.html), que contiene diversas funciones para trabajar con matrices dispersas. Los argumentos de esta función son una lista de las diagonales de la matriz y una lista de posiciones donde colocar cada una de esas diagonales. En este caso nos interesan las posiciones `k = 0` (diagonal principal), `k = 1` (superdiagonal) y `k = -1` (subdiagonal).

<ins datetime="2013-08-18T08:32:34+00:00"><em><strong>Nota</strong></em>: En SciPy 0.11 se introdujo <a href="http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.diags.html"><code>scipy.sparse.diags</code></a>, que es el nuevo método recomendado para construir matrices disperas a partir de las diagonales.</ins>

Para escribir **código compatible con Python 3**, al principio del programa escribiremos la línea

<pre><code class="language-python">from __future__ import print_function</code></pre>

que sustituye la sentencia `print` de Python 2 por la nueva **función** `print` de Python 3. El [módulo `__future__`](http://www.python.org/dev/peps/pep-0236/) de Python 2 contiene varias sentencias que importan características de versiones de Python posteriores, de tal manera que podemos aprovechar nuevas posibilidades o simplemente hacer nuestro código más portable. Para lo que vamos a hacer hoy no necesitamos más.

En primer lugar construimos las tres diagonales, haciendo uso de la función [`ones`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ones.html#numpy.ones) de NumPy que nos da un array lleno de unos, y utilizando la función [`vstack`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.vstack.html#numpy.vstack) de Numpy las apilamos (de ahí el nombre) por filas:

<pre><code class="language-python"># Número de puntos de colocación
N = 100
dl = np.ones(N - 1)
du = np.ones(N - 1)
d0 = -2 * np.ones(N - 1)
d = np.vstack((dl, d0, du))</code></pre>

Ahora simplemente tenemos que llamar a la función `spdiags` para construir la matriz:

<pre><code class="language-python">A = sparse.spdiags(d, (-1, 0, 1), N - 1, N - 1)</code></pre>

El código quedará finalmente de esta manera:

<pre><code class="language-python"># coding: utf-8
#
# Crea una matriz tridiagonal
# Juan Luis Cano Rodríguez &lt;juanlu001@gmail.com&gt;
from __future__ import print_function
import numpy as np
from scipy import sparse
# Número de puntos de colocación
N = 100
dl = du = np.ones(N - 1)
d0 = -2 * np.ones(N - 1)
d = np.vstack((dl, d0, du))
A = sparse.spdiags(d, (-1, 0, 1), N - 1, N - 1)
print(A.todense())</code></pre>

Si lo ejecutamos desde IPython:

<pre><code class="language-python">In [1]: %run tridiag.py
[[-2.  1.  0. ...,  0.  0.  0.]
 [ 1. -2.  1. ...,  0.  0.  0.]
 [ 0.  1. -2. ...,  0.  0.  0.]
 ...,
 [ 0.  0.  0. ..., -2.  1.  0.]
 [ 0.  0.  0. ...,  1. -2.  1.]
 [ 0.  0.  0. ...,  0.  1. -2.]]
In [2]: A
Out[2]:
&lt;99x99 sparse matrix of type '&lt;class 'numpy.float64'&gt;'
	with 295 stored elements (3 diagonals) in DIAgonal format&gt;
In [3]: type(A)
Out[3]: scipy.sparse.dia.dia_matrix
In [4]: sparse.dia?
Type:       module
Base Class: &lt;class 'module'&gt;
String Form:&lt;module 'scipy.sparse.dia' from '/usr/lib/python3.2/site-packages/scipy/sparse/dia.py'&gt;
Namespace:  Interactive
File:       /usr/lib/python3.2/site-packages/scipy/sparse/dia.py
Docstring:  Sparse DIAgonal format</code></pre>

¡Y ya está! 🙂 Espero que te haya resultado útil, no dudes mandarnos tus dudas y sugerencias así como de difundir el artículo.

¡Un saludo!