---
title: Cómo crear matrices en Python con NumPy
date: 2012-06-11T10:19:28+00:00
author: Juan Luis Cano
slug: como-crear-matrices-en-python-con-numpy
tags: arrays, matrices, numpy, python

## Introducción

En este breve apunte vamos a ver **cómo crear matrices en Python** usando la biblioteca NumPy. Para ello, vamos a hacer un repaso rápido de los métodos que ofrece NumPy para crear arrays y matrices.

Si buscas por Internet encontrarás varias recetas de [cómo crear una matriz en Python utilizando listas](http://python.majibu.org/preguntas/1614/como-crear-una-matriz-vacia-en-python-con-listas), es decir, haciendo uso solamente de la biblioteca estándar. Sin embargo, aquí asumimos que vamos a emplear la matriz básicamente para hacer cálculos matemáticos con ella, y por otro lado en nuestro caso no supone un problema añadir NumPy como dependencia porque por unas razones o por otras lo íbamos a necesitar 😉

Esta entrada es básicamente una recopilación de los [métodos listados en la documentación de NumPy](http://docs.scipy.org/doc/numpy/reference/routines.array-creation.html). <del datetime="2012-08-18T07:59:04+00:00">Otro día veremos</del><ins datetime="2012-08-18T08:03:17+00:00">En este artículo en nuestro blog puedes leer <a title="Cómo leer y escribir datos en archivos con NumPy" href="http://pybonacci.org/2012/08/17/como-leer-y-escribir-datos-en-archivos-con-numpy/">cómo construir arrays a partir de ficheros externos</a>.</ins>

**Editado el 13 de junio de 2012**: Añadidas funciones para crear arrays de NumPy a partir de listas y una nota sobre el peligro de la función `empty`.

_**En esta entrada se ha usado python 2.7.3 y numpy 1.6.1 **_**y es compatible con ****python 3.2.3**

## Arrays vacíos, unos y ceros

Con estas funciones podemos **crear una matriz en Python** cuando conocemos el tamaño pero no conocemos los datos que va a contener, o cuando por cualquier motivo queremos matrices llenas de unos o de ceros. Para ello utilizaremos las funciones [`empty`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.empty.html), [`zeros`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html) y [`ones`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ones.html), que aceptan como argumento una tupla con las dimensiones del array:

<pre><code class="language-python">In [1]: import numpy as np
In [2]: np.empty((2, 3))  # Matriz vacía, con valores residuales de la memoria
Out[2]:
array([[  0.00000000e+000,   1.19528827e-316,   6.94132801e-310],
       [  1.41077362e-316,   6.94132772e-310,   6.94132772e-310]])
In [3]: np.zeros((3, 1))  # Matriz de ceros
Out[3]:
array([[ 0.],
       [ 0.],
       [ 0.]])
In [4]: np.ones((3, 2))  # Matriz de unos
Out[4]:
array([[ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.]])</code></pre>

<!--more-->

Todas estas funciones tienen una contrapartida con el sufijo `_like`, con la que podemos crear matrices **con la misma dimensión que una dada**. Son [`empty_like`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.empty_like.html), [`zeros_like`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros_like.html) y [`ones_like`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ones_like.html):

<pre><code class="language-python">In [5]: a = np.zeros((3, 2))
In [6]: np.empty_like(a)  # Matriz vacía con la forma de a
Out[6]:
array([[  6.94132772e-310,   1.85559990e-316],
       [  6.94132801e-310,   1.41077362e-316],
       [  0.00000000e+000,   6.68964884e-321]])
In [7]: np.zeros_like(a)  # Matriz de ceros con la forma de a
Out[7]:
array([[ 0.,  0.],
       [ 0.,  0.],
       [ 0.,  0.]])
In [8]: np.ones_like(a)  # Matriz de unos con la forma de a
Out[8]:
array([[ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.]])</code></pre>

**Nota**: Como bien dice la documentación y [David](#comment-113) en los comentarios, hay que usar la función `empty` con cuidado. Aunque es ligeramente más rápida que `zeros`, al rellenar todas las posiciones con valores aleatorios hay que asegurarse de que vamos a sobreescribir dichos valores, porque si no obtendremos resultados desastrosos.

Para crear una **matriz identidad**, esto es, una matriz cuadrada con unos en la diagonal, podemos usar la función [`identity`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.identity.html). Para un caso un poco más general, sin que sean matrices necesariamente cuadradas, podemos usar [`eye`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.eye.html):

<pre><code class="language-python">In [9]: np.identity(3)  # Matriz identidad de tamaño 3
Out[9]:
array([[ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.]])
In [10]: np.identity(5)  # Matriz identidad de tamaño 4
Out[10]:
array([[ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  0.,  0.,  0.],
       [ 0.,  0.,  1.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.],
       [ 0.,  0.,  0.,  0.,  1.]])
In [11]: np.eye(4, 3)  # Matriz de 4x3 con unos en una diagonal y ceros en el resto de elementos
Out[11]:
array([[ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.],
       [ 0.,  0.,  0.]])
In [12]: np.eye(4, 3, k=-1)  # Con el parámetro k podemos controlar qué diagonal está llena de unos
Out[12]:
array([[ 0.,  0.,  0.],
       [ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.]])</code></pre>

## Arrays a partir de listas

Cuando conocemos todos los valores del array antes de crearlo, podemos utilizar la función [`array`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html) y pasarle como argumento una lista, tupla o, en general, una [secuencia](http://docs.python.org/library/stdtypes.html#sequence-types-str-unicode-list-tuple-bytearray-buffer-xrange).

<pre><code class="language-python">In [3]: np.array(
   ...: [1, 2, 3]  # Lista
   ...: )
Out[3]: array([1, 2, 3])
In [4]: np.array(  # Lista de listas
   ...: [
   ...: [1, -1],
   ...: [2, 0]
   ...: ]
   ...: )
Out[4]:
array([[ 1, -1],
       [ 2,  0]])
In [7]: np.array(
   ...: (0, 1, -1)  # Tupla
   ...: )
Out[7]: array([ 0,  1, -1])
In [8]: np.array(range(5))
Out[8]: array([0, 1, 2, 3, 4])</code></pre>

Este será el método que utilizaremos con más frecuencia para arrays pequeños en los que ya conocemos los valores. Gracias a [ozroc](http://pybonacci.org/2012/06/11/como-crear-matrices-en-python-con-numpy/?preview=true&preview_id=577&preview_nonce=55fcd1e8ce#comment-72) por el apunte 🙂

## Rangos numéricos

NumPy también ofrece funciones para crear rangos numéricos, particiones de intervalos, discretizaciones o como queráis llamarlos. Por ejemplo, la función [`arange`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html) está pensada rangos de números enteros, de manera similar a la función [`range`](http://docs.python.org/library/functions.html#range) de la biblioteca estándar de Python:

<pre><code class="language-python">In [13]: np.arange(4)
Out[13]: array([0, 1, 2, 3])
In [14]: np.arange(2, 5)
Out[14]: array([2, 3, 4])
In [15]: np.arange(2, 10, 3)
Out[15]: array([2, 5, 8])</code></pre>

**Nota:** Ya puedes ver que al crear un rango el límite superior no se incluye, [como ya explicó Edsger W. Dijkstra](http://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html) 😛

¿Qué pasa si queremos un rango en el que el paso no sea un número entero? La documentación de `arange` especifica que para estos casos los resultados pueden ser inconsistentes. Recurrimos a las funciones `linspace` y `logspace`, que quienes vengan de MATLAB reconocerán al instante. Estas funciones aceptan como argumento el número de elementos en lugar del paso:

<pre><code class="language-python">In [16]: np.linspace(0, 1, 11)  # 11 puntos equiespaciados entre 0 y 1
Out[16]: array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ])
In [22]: np.logspace(2, 5, 4, base=10)  # 4 puntos equiespaciados según una escala logarítmica entre 10^2 y 10^5
Out[22]: array([    100.,    1000.,   10000.,  100000.])</code></pre>

¡Y con esto terminamos! Espero que te haya resultado útil la entrada, no olvides [comentar](#respond) y [seguirnos en Twitter](http://twitter.com/Pybonacci). ¡Un saludo!