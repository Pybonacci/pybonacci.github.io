---
title: ¿Cómo trabajar con arrays de binarios en Python?
date: 2014-01-21T19:00:31+00:00
author: Juan Luis Cano
slug: como-trabajar-con-arrays-de-binarios-en-python
tags: arrays, bitset, numpy, python

Esta semana vamos con una pregunta de Gonzalo, que nos dice por email:

> Saludos. Últimamente he estado trabajado en python y me gusta mucho. En estos momentos estoy haciendo un algoritmo genético con codificación en numeros binarios utilizando bitset de C++. ¿Tendran información acerca de como trabajar con cadenas de binarios en python? Gracias y Felicidades por el blog.

He investigado un poco [acerca de bitset en la referencia de C++](http://www.cplusplus.com/reference/bitset/bitset/), y leo que se trata básicamente de un **array de valores booleanos**, optimizados para su almacenamiento en memoria.

<!--more-->

Esto es exactamente lo que puedes conseguir con los arrays de NumPy: son contenedores de datos homogéneos, que se almacenan eficientemente en memoria e implementados en C para que su manejo sea mucho más rápido. En nuestro blog tienes muchos artículos sobre NumPy, como por ejemplo este tutorial sobre los distintos métodos para crear arrays:

<http://pybonacci.org/2012/06/11/como-crear-matrices-en-python-con-numpy/>

Para que los arrays funcionen como bitset, **tienen que tener el `dtype bool`**. Puedes conseguir esto de varias maneras:

  * Creando el array a partir de una lista de valores True y False:

<pre><code class="language-python">&gt;&gt;&gt; np.array([True, False, True])
array([ True, False,  True], dtype=bool</code></pre>

  * Utilizando el argumento dtype=bool para hacer una conversión explícita:

<pre><code class="language-python">&gt;&gt;&gt; np.array([1, 0, -2.5], dtype=bool)
array([ True, False,  True], dtype=bool)</code></pre>

  * Utilizando el método astype:

<pre><code class="language-python">&gt;&gt;&gt; np.arange(-3, 3).astype(bool)
array([ True,  True,  True, False,  True,  True], dtype=bool)</code></pre>

  * Utilizando las funciones lógicas de NumPy:

<pre><code class="language-python">&gt;&gt;&gt; np.arange(-3, 3) &lt; 0
array([ True,  True,  True, False, False, False], dtype=bool)
&gt;&gt;&gt; np.isinf(np.arange(-2, 2) / 0)
array([ True,  True, False,  True], dtype=bool)</code></pre>

(Puedes consultar un listado en <http://docs.scipy.org/doc/numpy/reference/routines.logic.html>)

A partir de ahí, tienes todas las funciones de NumPy y toda la potencia de Python a tu disposición.

¡Y hasta aquí la pregunta de la semana! 🙂 **Y tú, ¿has trabajado con arrays booleanos en NumPy? ¿Crees que hay algo que otros lenguajes tienen y que a Python le falta en este sentido? O al contrario, ¿te has encontrado con que con NumPy tienes ventajas que de otra forma no tendrías?** ¡Cuéntanoslo en los comentarios!