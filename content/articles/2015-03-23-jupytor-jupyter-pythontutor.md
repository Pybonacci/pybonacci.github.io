---
title: tutormagic: Jupyter + pythontutor
date: 2015-03-23T19:40:47+00:00
author: Kiko Correoso
slug: jupytor-jupyter-pythontutor
tags: enseñanza, ipython, jupyter, pythontutor

Esta será una microentrada para presentar una extensión para el notebook que estoy usando en un curso interno que estoy dando en mi empresa.  
Si a alguno más os puede valer para mostrar cosas básicas de Python (2 y 3, además de Java y Javascript) para muy principiantes me alegro.

# Nombre en clave: tutormagic

Esta extensión lo único que hace es embeber dentro de un IFrame la página de [pythontutor](http://www.pythontutor.com) usando el código que hayamos definido en una celda de código precedida de la _cell magic_ `%%tutor`.  
Como he comentado anteriormente, se puede escribir código Python2, Python3, Java y Javascript, que son los lenguajes soportados por pythontutor.

# Ejemplo

Primero deberemos instalar la extensión. Está disponible en pypi por lo que la podéis instalar usando `pip install tutormagic`. Una vez instalada, dentro de un notebook de IPython la deberías cargar usando:

`%load_ext tutormagic`

Una vez hecho esto ya deberiamos tener disponible la _cell magic_ para ser usada. Podéis ver un ejemplo en [este notebook](http://nbviewer.ipython.org/github/Pybonacci/notebooks/blob/master/tutormagic.ipynb).

# Y eso es todo

Lo dicho, espero que sea útil para alguien.

*  [tutormagic en pypi](https://pypi.python.org/pypi/tutormagic).
*  [tutormagic en github](https://github.com/kikocorreoso/tutormagic)

Saludos.
