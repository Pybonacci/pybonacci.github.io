---
title: Operador dos puntos (:) de MATLAB ¿en Python?
date: 2013-11-15T13:00:25+00:00
author: Juan Luis Cano
slug: operador-dos-puntos-de-matlab-en-python
tags: arange, linspace, matlab, octave, python

## Introducción

Hoy que es viernes os traemos un artículo un poco más relajado (y atípico): vamos a hablar sobre el operador dos puntos (:) de MATLAB, o más bien **de su ausencia en Python**. Tal vez algunos de quienes estáis ya considerando Python como una opción seria frente a MATLAB os estaréis preguntando: ¿qué hay de esta magnífica sintaxis para crear secuencias?

    $ octave -q
    octave:1> 0:0.1:1
    ans =
    0.000 0.100 0.200 0.300 0.400 0.500 0.600 0.700 0.800 0.900 1.000

Pues, como indican en el [mathesaurus](http://mathesaurus.sourceforge.net/matlab-numpy.html) y en otros sitios, tendré que usar la función `np.arange`:

    $ python -q
    >>> import numpy as np
    >>> np.arange(0, 1, 0.1)
    array([ 0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

¿Ein? ¿Solo me llega hasta 0.9? ¿Qué está pasando aquí? Voy a ver si lo consigo arreglar un poco:

    >>> np.arange(0, 1.01, 0.1)
    array([ 0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ])

Pffff... ¡Menuda chapuza! «¿En qué hora haría yo caso a la gente esta de Pybonacci?» En fin, a ver si dicen algo en la [documentación de `np.arange`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html):

> When using a non-integer step, such as 0.1, the results will often not be consistent. It is better to use <tt>linspace</tt> for these cases.

Rayos... ¿Tengo que usar `np.linspace` entonces? Pero este iba con el número de intervalos, no con el espaciado entre los puntos...

    >>> np.linspace(0, 1, 10) # >> np.linspace(0, 1, 11) # <-- Nótese el 11
    array([ 0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ])

Esto es un poco frustrante, me estoy empezando a arrepentir de haberme pasado a Python. ¿No habrá una forma un poco mejor de hacer esto? Veamos, parece que alguien más se ha hecho esta pregunta antes que yo: "[Python syntax for MATLAB/Octave colon operator a:dx:b](http://scicomp.stackexchange.com/questions/2336/python-syntax-for-matlab-octave-colon-operator-adxb)". Y el código sería algo así:

    def lrange(r1, inc, r2):
        """Provide spacing as an input and receive samples back by wrapping `numpy.linspace`"""
        n = ((r2-r1)+2*np.spacing(r2-r1))//inc
    return np.linspace(r1,r1+inc*n,n+1)

Anda ya, ¿en MATLAB tan fácil y en Python tan enrevesado? Pybonaccis, aquí os he pillado...

Vale vale, un poco de calma. ¡Que hoy es viernes, y hay que mantener el buen humor!

<blockquote class="twitter-tweet" width="550">
  <p>
    Python llegaste al mundo para cagarme la vida! Odio programar!!!
  </p>
  
  <p>
    &mdash; Martín Alejandro (@MScarlatto) <a href="https://twitter.com/MScarlatto/statuses/398948679903494144">November 8, 2013</a>
  </p>
</blockquote>



<blockquote class="twitter-tweet" width="550">
  <p>
    Definitivamente, odio integrales y el puto python
  </p>
  
  <p>
    &mdash; Patricia (@PatriciaPG94) <a href="https://twitter.com/PatriciaPG94/statuses/399631260508647424">November 10, 2013</a>
  </p>
</blockquote>



https://twitter.com/MarinaKevlar/status/399723875413413888

<blockquote class="twitter-tweet" width="550">
  <p>
    PUTA MIERDA PYTHON TE ODIO
  </p>
  
  <p>
    &mdash; Lady Musi (@slashina13) <a href="https://twitter.com/slashina13/statuses/400604133150838785">November 13, 2013</a>
  </p>
</blockquote>



<blockquote class="twitter-tweet" width="550">
  <p>
    Odio python, odio python, odio python,odio python, odio python, odio pythonn, odio python...
  </p>
  
  <p>
    &mdash; Criis. (@Criis_glez) <a href="https://twitter.com/Criis_glez/statuses/267271751472386048">November 10, 2012</a>
  </p>
</blockquote>



Sí sí, ¡también os lo digo a vosotros! Respirad hondo, contad hasta cinco (no queremos que nadie se ahogue) y vamos a estudiar despacio este problema para que veamos cómo solucionarlo 🙂

<!--more-->

## Siempre es el punto flotante

Ah, ¡ya sabía yo que algo no iba bien aquí! El punto flotante no nos trae más que sorpresas, y esta es otra de ellas.

<blockquote class="twitter-tweet" width="550">
  <p>
    Some programmers, when confronted with a problem, think "I know, I'll use floating point arithmetic." Now they have 1.999999999997 problems.
  </p>
  
  <p>
    &mdash; Tom Scott (@tomscott) <a href="https://twitter.com/tomscott/statuses/174143430170120192">February 27, 2012</a>
  </p>
</blockquote>



Es raro que estés leyendo este blog y no estés familiarizado con los problemas del punto flotante, pero si es tu caso, por favor no tardes en ejecutar este código:

    >>> 0.1 + 0.2
    0.30000000000000004

Si tu reacción al ver esto ha sido «WTF?» te recomiendo que leas [La guía del punto flotante](http://puntoflotante.org).

Pero ¿qué es exactamente lo que está sucediendo aquí? Es difícil decirlo a simple vista, pero podemos pedir a Python y a Octave que nos saquen más decimales, y entonces veremos la luz:

    octave:1> output_precision(18)
    octave:2> 0.1
    ans = 1.00000000000000006e-01

Vamos, que 0.1 no es 0.1, sino un poquito más. Esto es así en MATLAB, Octave, Python, C, FORTRAN y en todas partes[*](http://puntoflotante.org/formats/exact/). Ya vemos entonces que, por ejemplo, empezar en el punto inicial e ir sumando repetidamente 0.1 podría fallar de muchas maneras diferentes. Esto, unido a que np.arange _no_ incluye el punto final _salvo errores de punto flotante_ nos da los resultados que hemos visto antes en Python. Pero entonces, ¿cómo lo hacen MATLAB y Octave? El caso de MATLAB lo analizó más detenidamente el gran Mike Croucher de Walking Randomly en su artículo "[Fun with linspace and the colon operator in MATLAB](http://www.walkingrandomly.com/?p=789)", y el código fuente correspondiente, obtenido de los foros de soporte de este programa, es el siguiente:

https://gist.github.com/Juanlu001/7383894

Caramba, no es un problema tan fácil como parece, ¿no?

(El código fuente correspondiente de Octave está cerca de [aquí](http://hg.savannah.gnu.org/hgweb/octave/file/11a6c7445a71/liboctave/array/idx-vector.h#l482), pero C++ me resulta un [monstruo infumable](https://twitter.com/Pybonacci/status/399105227728494592))

## Cambio de filosofía

Si nos damos cuenta, estamos intentando forzar dos cosas que normalmente serán incompatibles entre sí: los puntos inicial y final del intervalo y el espaciado. ¿Qué debería devolver el ordenador si pido un intervalo de 0 a 1.2, con un espaciado de 1.0? Pues ya sabemos que o bien no incluye el 1.2, o bien me cambia el espaciado:

    octave:1> 0:1:1.2
    ans =
    0 1


  


    >>> np.arange(0, 1.2, 1.0)
    array([ 0., 1.])

Tanto Octave como Python me devuelven intervalos que no incluyen el punto final. Es ahora cuando tenemos que pensar: si especifico el espaciado, ¿es realmente tan importante para mí el punto final? Y si me interesa que los puntos inicial y final delimiten exactamente el intervalo, ¿es tan importante el espaciado?

Podemos extraer entonces estas conclusiones:

  * Las funciones para crear secuencias (`:` en MATLAB/Octave y `np.arange` en Python) funcionan sin problemas con enteros.
  * Cuando manejamos números de punto flotante, **las condiciones de especificar el punto final y el espaciado normalmente son incompatibles**.
  * Si lo más importante para nosotros es mantener un valor del espaciado, seguramente la exactitud del punto final es secundaria. En estos casos podemos usar la función `np.arange`, teniendo en cuenta que el punto final puede o no entrar.
  * Si lo más importante es que se mantengan los puntos inicial y final, seguramente el valor del espaciado nos importa menos. En este caso usaremos la función `np.linspace`, eligiendo primero un número de puntos adecuado a nuestras necesidades.
  * Siempre podremos construir una secuencia de enteros y luego dividir por un número para conseguir resultados más predecibles.

Sirva este post como referencia a toda la gente frustrada cuando viene de MATLAB y no encuentra el operador `:` y una luz al final del túnel para aquellos que odian Python con todo su ser, para que les ayude a superar su odio y a alcanzar la felicidad 🙂

¡Un saludo, buen fin de semana y nos vemos en la [PyConES](http://2013.es.pycon.org/)!