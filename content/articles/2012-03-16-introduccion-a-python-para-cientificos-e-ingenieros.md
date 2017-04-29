---
title: Introducción a Python para científicos e ingenieros
date: 2012-03-16T19:25:50+00:00
author: Juan Luis Cano
slug: introduccion-a-python-para-cientificos-e-ingenieros
tags: python, python 3

## El lenguaje Python

[Python](http://python.org "Python") es un lenguaje de programación de propósito general muy fácil de aprender, con una sintaxis característica que hace que los programas escritos en él sean muy legibles, [ampliamente utilizado](http://wiki.python.org/moin/OrganizationsUsingPython) por empresas como Google o la NASA y, además, [libre](http://docs.python.org/license.html). Fue creado en 1991 por [Guido van Rossum](http://es.wikipedia.org/wiki/Guido_van_Rossum "Guido van Rossum"), un programador holandés.

Un programa escrito en Python tiene esta pinta:

<pre><code class="language-python">#!/usr/bin/python
# -*- coding: utf-8 -*-
# Suma dos números (suma.py)
from __future__ import print_function
def suma(a, b):
  c = a + b
  return c
x = 1
y = 2.3
print('La suma de x e y es: {}'.format(suma(x, y)))</code></pre>

Este programa imprimiría por pantalla

    $ pyton suma.py
    La suma de x e y es: 3.3

y funciona tanto con Python 2.7 como con Python 3.2. Ya hablaremos de qué es lo que hace exactamente y de esto de las versiones más adelante.

Técnicamente, el lenguaje Python tiene las siguientes características:

<!--more-->

  * Es **interpretado**, en lugar de _compilado_.En lenguajes compilados como Fortran o C, después de escribir el programa en el fichero fuente este se _compila_, dando lugar a un archivo binario que llamamos _ejecutable_. Aquí un _intérprete_ lee las instrucciones contenidas en el fichero fuente secuencialmente cada vez que queremos ejecutar el programa. Esto tendrá sus ventajas y sus inconvenientes, como tendremos ocasión de ver.
  * Es **dinámico**, en lugar de _estático_.No es necesario declarar explícitamente el _tipo_ de las variables: es el intérprete quien hace automáticamente la asignación, otra vez al contrario de lo que ocurre en lenguajes como Fortran o C.
  * Tiene tipado **fuerte**, en lugar de _débil_.Una vez una variable tiene un tipo asignado, no se producirán conversiones implícitas, sino que se producirá un error, al contrario de lo que pasa en JavaScript o en PHP.
  * Soporta diversos **paradigmas de programación**.El paradigma más usual en Fortran es la programación por procedimientos, y existen también la programación orientada a objetos (POO), programación funcional, etc.

Por último, para hacernos una idea rápida de cuál es la filosofía detrás de Python, no hay más que escribir en el intérprete `import this` y obtendremos el _Zen de Python_, escrito por Tim Peters:

>   * Bonito es mejor que feo.
>   * Explícito es mejor que implícito.
>   * Simple es mejor que complejo.
>   * Complejo es mejor que complicado.
>   * Plano es mejor que anidado.
>   * Disperso es mejor que denso.
>   * La legibilidad cuenta.
>   * Los casos especiales no lo son tanto como para romper las reglas.
>   * Aunque lo práctico gana a la pureza.
>   * Los errores nunca deberían dejarse pasar silenciosamente.
>   * A menos que hayan sido silenciados explícitamente.
>   * Frente a la ambigüedad, rechaza la tentación de adivinar.
>   * Debería haber una –y preferiblemente sólo una– manera obvia de hacerlo.
>   * Aunque esa manera puede no ser obvia al principio a menos que usted sea holandés.
>   * Ahora es mejor que nunca.
>   * Aunque nunca es a menudo mejor que _ya mismo_.
>   * Si la implementación es difícil de explicar, es una mala idea.
>   * Si la implementación es fácil de explicar, puede que sea una buena idea.
>   * Los espacios de nombres (namespaces) son una gran idea ¡hagamos más de esos!

¿Interesante, no crees? ¡Sigamos!

## Utilidad de Python en ciencia e ingeniería

El lenguaje Python ha recibido desde sus orígenes mucha atención de la comunidad científica. El propio van Rossum es matemático, y ya en 1995 apareció un paquete llamado Numeric que permitía manipular arrays multidimensionales, lo que permitió programar algoritmos matemáticos en Python que se ejecutaban mucho más rápido. Este paquete fue el origen de [Numpy](http://numpy.scipy.org/ "Numpy"), quien será el protagonista de este blog.

(Sí, diré “array” en lugar de “vector”, con el permiso de los académicos de la RAE)

Python tiene numerosas alicientes para el mundo científico e ingenieril:

  * Los paquetes [Numpy](http://numpy.scipy.org/ "Numpy") y [Scipy](http://www.scipy.org/ "Scipy") pueden convertirlo, con poco trabajo, en un sustituto completo a programas prohibitivamente caros pero de uso común en este ámbito como Matlab.
  * El proyecto [Sage](http://www.sagemath.org/ "Sage") constituye un esfuerzo titánico para reunir todo el software libre relacionado con las matemáticas para crear una alternativa viable a programas como Maple o Mathematica. Y van por muy buen camino.
  * Python es [mucho más consistente, sólido e intuitivo](http://iimyo.forja.rediris.es/inconsistencias.html "Inconsistencias de Matlab") de lo que el lenguaje Matlab podrá nunca llegar a ser.
  * Python es un lenguaje de propósito general, por lo que puedes mezclar tu “number crunching” con multitud de funcionalidades que nunca encontrarás en lenguajes de dominio específico, como puedan ser Maple o Mathematica.
  * La [documentación de Python](http://docs.python.org/ "Documentación") es enorme y está muy bien escrita, y hay cantidad de recursos sobre él en Internet disponibles sin coste alguno. Es muy sencillo de aprender por cuenta propia.
  * Python se puede integrar muy fácilmente con código escrito en Fortran gracias a [F2PY](http://www.scipy.org/F2py "F2PY"), con lo que podemos conseguir la velocidad inigualable de este con la sencillez de aquel.
  * Ya hay escritas para Python multitud de bibliotecas relacionadas con la física o la ingeniería.
  * ¿He dicho ya que es **libre** y se puede instalar en Linux, Windows y Mac?

Y hablando de instalar, ya que se te ha hecho la boca agua… ¿cómo lo instalo?

## Instalación

Ya que vamos a hablar de instalar Python, hagamos primero un pequeño comentario sobre versiones. Actualmente hay dos versiones de Python en activo:

  * La **versión 2.7** es la última revisión de la rama 2.x, y es la que ha estado en activo durante los últimos años.
  * La **versión 3.2** es la revisión actual (a 31 de diciembre de 2011) de la rama 3.x, y es donde se están añadiendo nuevas características.

Python 3 fue introducido para solucionar algunas inconsistencias que tenía la versión anterior y que requerían _romper la compatibilidad_. Esto significa que no todo el código que se ejecute en Python 3 funcionará en Python 2.

No todos los paquetes que usaremos aquí “se han pasado” todavía a la nueva versión, aunque esperemos que lo hagan pronto. Sin embargo, es altamente recomendable que los programadores se vayan habituando a las bondades de Python 3.

En este blog intentaré escribir código que pueda ejecutarse en las dos versiones de Python indistintamente, como el programa que hemos visto más arriba, siempre que estén disponibles los paquetes necesarios. Por tanto, **te recomiendo que instales la versión 2.7**.

Bien, y dicho esto, vamos con la instalación.

Si estás en **Windows**:

  1. Vamos a la web de [Python](http://python.org "Python"), y accedemos a la sección “Download”, o directamente a [descargar Python](http://python.org/download/). En la parte de arriba hay un comentario sobre diversas implementaciones de Python. Ya hablaremos de eso otro día, nosotros vamos a instalar la implementación principal, **CPython**, escrita en lenguaje C.
  2. En la sección “Download Python”, escoge Python Windows Installer o Mac OS X Installer, dependiendo de tu sistema operativo.
  3. Sigue las instrucciones del instalador, ¡y listo!

<ins datetime="2012-08-18T08:01:17+00:00">En nuestro blog puedes leer instrucciones más detalladas para <a title="Python en Windows: «¡Hola mundo!» en 7 minutos" href="http://pybonacci.org/2012/06/27/python-en-windows-hola-mundo-en-7-minutos/">instalar Python en Windows</a>.</ins>

Si estás en **Mac**, la opción más recomendada es usar [Macports](http://www.macports.org/ "Macports"):

    sudo ports install py26-matplotlib

Si estás en **Linux**, posiblemente Python ya venga instalado con tu sistema operativo. Para comprobarlo, abre una ventana de terminal y escribe:

    which python

y también:

    which python2

Si alguno de estos comandos escupe algo como `/usr/bin/python` o `/usr/bin/python2` entonces ya puedes utilizar Python. En caso contrario, deberás instalar de la manera habitual el paquete python o python2, bien utilizando tu gestor de paquetes o bien compilando desde el código fuente. Si existe python2 en tu distribución, posiblemente python2 es la versión 2.7 y python la 3.2.

## ¡Hola, Python!

En entradas posteriores veremos más en profundidad cómo escribir programas en Python, pero de momento os tendré que dejar con la miel en los labios 😛 Para abrir un poco el apetito ya que lo tenemos instalado y para estrenar el intérprete, ábrelo y escribe:

    >>> 2 + 2
    4
    >>> 2 + 2 == 5
    False
    >>> a = 1
    >>> a + 6
    7
    >>> print 'Hola, Python!'
    Hola, Python!
    >>> for i in range(1, 13): print i
    ...
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    >>> print 'Feliz 2012!'
    Feliz 2012!

Puedes hacer todos los experimentos que quieras, que lo peor que te podrá pasar es que te aparezca un mensaje de error. ¡No vas a destruir tu ordenador!

Si quieres cacharrear un poco más, ¡puedes ir al [tutorial oficial de Python](http://docs.python.org/tutorial/introduction.html#using-python-as-a-calculator "Tutorial") ahora mismo!

## Para saber más

Para finalizar, aquí os pongo más enlaces interesantes:

  * Página para promocionar [Python 3](http://getpython3.com/), con recursos, tutoriales e información útil. Muy recomendable. (Inglés)
  * ¿Debo usar [Python 2 o Python 3](http://wiki.python.org/moin/Python2orPython3)? Si te surgen las dudas, aquí encontrarás algunas respuestas. (Inglés)
  * En este curso de [Iniciación a Python](http://w3.iaa.es/python/) del Instituto de Astrofísica de Andalucía encontrarás las diapositivas de las charlas y más información útil.
  * Y, por supuesto, [siempre nos quedará Google](http://lmgtfy.com/?q=python).

¡Y hasta aquí la entrada de hoy! Espero que os haya resultado útil. ¡Nos vemos!