---
title: Juego de la vida de Conway con Python usando NumPy
date: 2012-11-30T10:26:06+00:00
author: Juan Luis Cano
slug: juego-de-la-vida-de-conway-con-python-usando-numpy
tags: autómatas celulares, matplotlib.animation, numpy, python

## Introducción

En esta breve entrada vamos a ver cómo implementar el **juego de la vida de Conway** en Python utilizando arrays de NumPy. El [juego de la vida](http://es.wikipedia.org/wiki/Juego_de_la_vida) es posiblemente el ejemplo más famoso de [autómata celular](http://es.wikipedia.org/wiki/Aut%C3%B3mata_celular), es decir, _un sistema dinámico que evoluciona en pasos discretos_. Actualmente están siendo estudiados en profundidad por Stephen Wolfram (creador además del software Mathematica) y tienen aplicaciones en campos tan diversos como la biología o la economía.

Aunque existe una implementación muy inteligente en Rosetta Code utilizando objetos `defaultdict`, voy a escribir la mía propia porque me parece «visualmente» más intuitiva. Para eso me voy a basar en el algoritmo seguido por Michael Gertelman[I] para escribir el programa en una línea usando APL (!) y en una entrada de Peter Collingridge[II], basada a su vez en la primera, donde aplica la misma idea en Python. Ambos están en las referencias al final de este texto.

¡Vamos allá!

<ins datetime="2013-08-12T19:03:31+00:00"><strong>Nota</strong>: <a href="http://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/">Jake VanderPlas ofrece una versión todavía más corta del juego de la vida</a>. Básicamente es la misma idea pero resumida en una línea 🙂 La otra versión emplea la función `scipy.signal.convolve2d`.</ins>

## El juego de la vida de Conway

Aunque hay muchas variantes del juego de la vida, nosotros nos vamos a centrar en la que publicó originalmente Conway en 1970. El juego de la vida es un juego de cero jugadores, _lo que quiere decir que su evolución está determinada por el estado inicial y no necesita ninguna entrada de datos posterior_ (Wikipedia). Las reglas son las siguientes:

  * El tablero es una rejilla de celdas cuadradas que tienen dos posibles estados: **viva** y **muerta**.
  * Cada célula tiene **ocho** células vecinas: se cuentan también las de las diagonales.
  * En cada paso, todas las células se actualizan instantáneamente teniendo en cuenta la siguiente regla: 
      * Cada célula viva con 2 o 3 células vecinas vivas sobrevive.
      * Cada célula con 4 o más células vecinas vivas muere por superpoblación. Cada célula con 1 o ninguna célula vecina viva muere por soledad.
      * Cada célula muerta con 3 células vecinas vivas nace.

¡Vamos con la implementación!

<!--more-->

## Código Python

Para recrear el tablero voy a utilizar un array de NumPy de tipo `int`, donde el valor 0 corresponderá a célula muerta y el 1 a célula viva. La clave para calcular el número de células vivas va a estar en la función [`roll`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.roll.html), que toma un array de NumPy y desplaza todos los elementos en la dirección indicada. Veamos un ejemplo:

    :::python
    &gt;&gt;&gt; b = np.diag([1, 2, 3])
    &gt;&gt;&gt; b
    array([[1, 0, 0],
           [0, 2, 0],
           [0, 0, 3]])
    &gt;&gt;&gt; np.roll(b, 1, axis=0)  # Eje 0: filas
    array([[0, 0, 3],
           [1, 0, 0],
           [0, 2, 0]])
    &gt;&gt;&gt; np.roll(b, 2, axis=0)  # Dos posiciones
    array([[0, 2, 0],
           [0, 0, 3],
           [1, 0, 0]])
    &gt;&gt;&gt; np.roll(b, -1, axis=0)  # Una posición hacia atrás
    array([[0, 2, 0],
           [0, 0, 3],
           [1, 0, 0]])
    &gt;&gt;&gt; np.roll(b, 1, axis=1)  # Eje 1: columnas
    array([[0, 1, 0],
           [0, 0, 2],
           [3, 0, 0]])

Pues bien, vamos a desplazar nuestro tablero una posición en las ocho direcciones posibles (recuerda que se cuenta la diagonal también) y vamos a sumar el resultado. Como cada célula viva tendrá el valor 1, esto me dará, en cada celda, el número de células vecinas vivas.

    :::python
    def vecindario(b):
        """Array de células vivas en el vecindario."""
        vecindario = (
            np.roll(np.roll(b, 1, 1), 1, 0) +  # Arriba-izquierda
            np.roll(b, 1, 0) +  # Arriba
            np.roll(np.roll(b, -1, 1), 1, 0) +  # Arriba-derecha
            np.roll(b, -1, 1) +  # Derecha
            np.roll(np.roll(b, -1, 1), -1, 0) +  # Abajo-derecha
            np.roll(b, -1, 0) +  # Abajo
            np.roll(np.roll(b, 1, 1), -1, 0) +  # Abajo-izquierda
            np.roll(b, 1, 1)  # Izquierda
        )
        return vecindario

date cuenta de que para desplazar en diagonal tenemos que aplicar la función `roll` dos veces.

**Nota**: Los elementos _dan la vuelta_ en la frontera del tablero, así que será como si considerásemos que es «esférico». En otras versiones del juego se considera siempre que las células de fuera del tablero están muertas.

Una vez que tenemos el array `vecindario`, es sencillísimo determinar qué células sobreviven, cuáles mueren y cuáles nacen:

    :::python
    def paso(b):
        """Paso en el juego de la vida de Conway."""
        v = vecindario(b)  # Se calcula el vecindario
        buffer_b = b.copy()  # Hacemos una copia de la matriz
        for i in range(buffer_b.shape[0]):
            for j in range(buffer_b.shape[1]):
                if v[i, j] == 3 or (v[i, j] == 2 and buffer_b[i, j]):
                    buffer_b[i, j] = 1
                else:
                    buffer_b[i, j] = 0
        return buffer_b

Y el tablero en el nuevo paso será el resultado de la función anterior.

Y esto ya está, casi la parte más complicada del código es conseguir crear una animación a partir de aquí. Como llevo un rato frustrado, y aunque podría arreglar esto de manera limpia leyendo un rato más el [tutorial de Jake Vanderplas sobre `matplotlib.animation`](http://jakevdp.github.com/blog/2012/08/18/matplotlib-animation-tutorial/), voy a hacer algo de lo que no me siento orgulloso y nunca, [nunca](http://xkcd.com/292/) tienes que intentar hacer en tu casa: usar una variable global. Si el gran KvdP lo hizo, yo también puedo 😛<figure id="attachment_1291" style="width: 400px" class="wp-caption aligncenter">

[<img class="size-full wp-image-1291" alt="Animación del juego de la vida de Conway" src="http://new.pybonacci.org/images/2012/11/juego_vida1.gif" width="400" height="400" />](http://new.pybonacci.org/images/2012/11/juego_vida1.gif)<figcaption class="wp-caption-text">Animación del juego de la vida de Conway</figcaption></figure> 

Y este es el código:

https://gist.github.com/4025886

Espero que os haya gustado, ¡un saludo!

P.D.: Perdonad la ligera inactividad y las prisas en escribir esta entrada, pero estamos muy ocupados organizando la que será la primera PyCon en España. Más información en [#PyConES](https://twitter.com/search?q=%23PyConES) 😉

## Referencias

  1. GERTELMAN, Michael. _Conway's Game of Life in one line of APL_ [en línea]. Disponible en Web: <<http://catpad.net/michael/apl/>>. [Consulta: 30 de noviembre de 2012]
  2. COLLINGRIDGE, Peter. _Game of Life in one line of Python_ [en línea]. Disponible en Web: <<http://www.petercollingridge.co.uk/blog/python-game-of-life-in-one-line>>. [Consulta: 30 de noviembre de 2012]
  3. GARDNER, Martin. _Mathematical Games - The fantastic combinations of John Conway's new solitaire game "life"_ [en línea]. Disponible en Web: <[http://ddi.cs.uni-potsdam.de/HyFISCH/Produzieren/lis\_projekt/proj\_gamelife/ConwayScientificAmerican.htm](http://ddi.cs.uni-potsdam.de/HyFISCH/Produzieren/lis_projekt/proj_gamelife/ConwayScientificAmerican.htm)>. [Consulta: 30 de noviembre de 2012]