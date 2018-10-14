---
title: Funciones definidas a trozos con arrays de NumPy
date: 2012-10-10T22:16:47+00:00
author: Juan Luis Cano
slug: funciones-definidas-a-trozos-con-arrays-de-numpy
tags: arrays, numpy, piecewise, python

## Introducción

Hoy vamos a ver cómo crear **funciones definidas a trozos** que manejen arrays de NumPy. Seguro que todos conocéis este tipo de funciones, pero a la hora de crearlas en NumPy me encontré con un par de obstáculos en el camino que me gustaría compartir con vosotros.

Como ya sabéis, las funciones definidas a trozos son ubicuas en matemáticas y se utilizan cuando queremos ensamblar varias funciones en una sola. Vamos a ver cómo construirlas en Python utilizando la función [`numpy.piecewise`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.piecewise.html) y vamos a revisar un par de conceptos sobre comparación de arrays e indexación avanzada utilizando valores booleanos. Esto último suena un poco a magia negra pero ya veréis cómo no es para tanto 😛

_**En esta entrada se ha usado python 2.7.3 y numpy 1.6.2.**_

## Funciones definidas a trozos

La función de NumPy `numpy.piecewise` acepta, como mínimo, tres argumentos:

  * un **array** de valores en los que evaluar la función `x`,
  * una **lista** de **arrays** booleanos `condlist` que son los «trozos» en los que se divide la función, que deben tener la misma forma que `x`,
  * y una **lista** de **funciones** `funclist` que se corresponden con cada uno de los trozos.

<!--more-->

De esta forma, si se cumple la condición i-ésima se evaluará la función i-ésima. Vamos a verlo con un ejemplo, construyendo la siguiente función:

$latex displaystyle y(x) =
  
begin{cases}
  
-x & x le 3 \
  
2 x & 3 leq x
  
end{cases}$

    :::python
    In [1]: import numpy as np
    In [2]: x = np.arange(8)
    In [3]: np.piecewise(x, [x &lt; 3, x &gt;= 3], [lambda x: -x, lambda x: 2 * x])
    Out[3]: array([ 0, -1, -2,  6,  8, 10, 12, 14])
    In [4]: condlist = [x &lt; 3, 3 &lt;= x]  # Forma más larga de hacer lo mismo
    In [5]: def f1(x):
       ...:     return -x
       ...:
    In [6]: def f2(x):
       ...:     return 2 * x
       ...:
    In [7]: funclist = [f1, f2]
    In [8]: np.piecewise(x, condlist, funclist)
    Out[8]: array([ 0, -1, -2,  6,  8, 10, 12, 14])

¡Y tan fácil como esto! Sin embargo, y antes de ponernos a analizar un poco más en profundidad voy a puntualizar dos cosas. La primera es que si en lugar de funciones en `funclist` pones una lista de números, también funciona. Y la segunda, que si incluyes una función más que condiciones tienes, la última función se toma como condición por defecto. Comprobémoslo:

    :::python
    In [9]: np.piecewise(x, [x &lt; 3], [lambda x: -x, -1])
    Out[9]: array([ 0, -1, -2, -1, -1, -1, -1, -1])

## Comparaciones con arrays

Ahora es el punto en el que a lo mejor alguno se está preguntando: «¿Dónde está esa lista de arrays booleanos que ibas a pasar? Yo solo veo `x < 3`». Pues esta es una buena pregunta, y vamos a tratar de responderla con un poco de detalle.

Las operaciones entre arrays en NumPy primero expanden los arrays que se van a operar (ya explicamos la expansión o «broadcasting» en nuestro artículo sobre [Álgebra Lineal en Python](https://pybonacci.org/2012/06/07/algebra-lineal-en-python-con-numpy-i-operaciones-basicas/ "Álgebra Lineal en Python con NumPy (I): Operaciones básicas")). Por tanto, cuando hacemos una operación como `x < 3`, al ser 3 un array de dimensión cero se expande y el resultado es un array con la forma de x:

    :::python
    In [10]: x
    Out[10]: array([0, 1, 2, 3, 4, 5, 6, 7])
    In [11]: x &lt; 3
    Out[11]: array([ True,  True,  True, False, False, False, False, False], dtype=bool)

De hecho, Python tiene una cosa buena que es que las operaciones de comparación se pueden encadenar, como por ejemplo `1 <= x < 3`. ¿Se puede hacer esto con arrays de NumPy?

    :::python
    In [12]: 1 &lt;= x &lt; 3
    ---------------------------------------------------------------------------
    ValueError                                Traceback (most recent call last)
    &lt;ipython-input-12-80c709037a5e&gt; in &lt;module&gt;()
    ----&gt; 1 1 &lt;= x &lt; 3
    ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

Este críptico y desconcertante mensaje de error tiene su explicación en la documentación de Python: según la sección de [operadores de comparación](http://docs.python.org/library/stdtypes.html#comparisons), la expresión `1 <= x < 3` se convierte en `1 <= x and x < 3`; y según la sección de [operadores booleanos](http://docs.python.org/library/stdtypes.html#boolean-operations-and-or-not), el operador `and` devuelve la primera expresión si es verdadera y, si es falsa, la segunda. El problema es que un array de valores booleanos no se puede evaluar como verdadero o falso, y de ahí el mensaje de error.

¿Cómo podemos especificar condiciones múltiples en Python entonces? Como explican [en la documentación de NumPy](http://docs.scipy.org/doc/numpy/reference/ufuncs.html#comparison-functions): en lugar de utilizar `and` y `or`, utilizaremos `&` y `|` (y poniendo los paréntesis adecuados):

    :::python
    In [14]: x
    Out[14]: array([0, 1, 2, 3, 4, 5, 6, 7])
    In [15]: (1 &lt;= x) & (x &lt; 3)
    Out[15]: array([False,  True,  True, False, False, False, False, False], dtype=bool)

## Indexación con valores booleanos

¿Y qué es eso de la indexación con valores booleanos, y qué tiene que ver con esto? Pues mucho, porque podemos conseguir un resultado parecido al del principio del artículo utilizando un array de valores booleanos. Ya sabemos indexar arrays utilizando la sintaxis `x[n1:n2]`, por ejemplo. Pero si utilizamos un array de valores booleanos, solo recuperamos los valores correspondientes a un registro verdadero. Un ejemplo:

    :::python
    In [16]: b = np.array([False, True, False, True, True], dtype=bool)
    In [18]: x = np.arange(5)
    In [19]: x
    Out[19]: array([0, 1, 2, 3, 4])
    In [20]: x[b]
    Out[20]: array([1, 3, 4])

¿Lo ves? En el array de indexado había valores verdaderos en las posiciones 1, 3 y 4, y esos son exactamente los valores que hemos recuperado. Mira lo que podemos conseguir con esto:

    :::python
    In [21]: x = np.arange(8)  # Recuperamos el primer ejemplo
    In [22]: np.piecewise(x, [x &lt; 3, x &gt;= 3], [lambda x: -x, lambda x: 2 * x])
    Out[22]: array([ 0, -1, -2,  6,  8, 10, 12, 14])
    In [23]: y = np.zeros_like(x)
    In [24]: x &lt; 3
    Out[24]: array([ True,  True,  True, False, False, False, False, False], dtype=bool)
    In [25]: y[x &lt; 3] = -x[x &lt; 3]
    In [26]: y
    Out[26]: array([ 0, -1, -2,  0,  0,  0,  0,  0])
    In [27]: y[x &gt;= 3] = 2 * x[x &gt;= 3]
    In [28]: y
    Out[28]: array([ 0, -1, -2,  6,  8, 10, 12, 14])

Se obtiene el mismo resultado de las dos maneras. De hecho, es así más o menos como trabaja internamente la función `piecewise`.

Espero que te haya resultado útil el artículo, porque yo he aprendido mucho escribiéndolo 🙂 ¡Un saludo y hasta el próximo!