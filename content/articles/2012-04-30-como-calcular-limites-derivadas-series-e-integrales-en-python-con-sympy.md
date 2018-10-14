---
title: Cómo calcular límites, derivadas, series e integrales en Python con SymPy
date: 2012-04-30T16:19:27+00:00
author: Juan Luis Cano
slug: como-calcular-limites-derivadas-series-e-integrales-en-python-con-sympy
tags: cálculo simbólico, derivadas, integrales, límites, python, series, sympy

## Introducción

Como buen paquete de cálculo simbólico que es, Sympy ofrece numerosas posibilidades para realizar tareas comunes del cálculo infinitesimal, como son calcular **límites, derivadas, series e integrales simbólicas**. Por ejemplo, mientras que con SciPy podemos calcular, utilizando [diferencias centradas](http://es.wikipedia.org/wiki/Derivaci%C3%B3n_num%C3%A9rica), la derivada de una función en un punto utilizando la función `<a href="http://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.derivative.html">scipy.misc.derivative</a>`, con SymPy podemos **calcular la derivada simbólica** de la función.

Si no conoces SymPy, puedes leer nuestra [Introducción al Cálculo Simbólico en Python con SymPy](https://pybonacci.org/2012/04/04/introduccion-al-calculo-simbolico-en-python-con-sympy/) para hacerte una idea del manejo del paquete. Este artículo está basado en la [sección de Cálculo Infinitesimal del tutorial de SymPy](http://docs.sympy.org/0.7.1/tutorial.html#calculus), y en él utilizaremos el intérprete interactivo de SymPy (`isympy`) que viene incluido con el paquete; para que el código funcione en un programa Python normal, sólo habría que incluir las correspondientes sentencias `import`.

<!--more-->

_**En esta entrada se ha usado python2 2.7.3 y sympy 0.7.1.**_

## Límites

Para calcular límites simbólicos con SymPy se utiliza la función `<a href="http://docs.sympy.org/0.7.1/modules/series.html#sympy.series.limits.limit">limit</a>`. Podemos calcular el límite de casi cualquier expresión [[1](#cite_note-0){#cite_ref-0}], con una o varias variables y por las dos direcciones:

    :::python
    In [1]: limit?
    Type:       function
    Base Class: &lt;type 'function'&gt;
    String Form:
    Namespace:  Interactive
    File:       /usr/lib/python2.7/site-packages/sympy/series/limits.py
    Definition: limit(e, z, z0, dir='+')
    Docstring:
    Compute the limit of e(z) at the point z0.
    [...]
    In [2]: limit(1 / x, x, oo)
    Out[2]: 0
    In [3]: limit(sin(x) / x, x, 0)
    Out[3]: 1
    In [4]: limit(1 / sin(x), x, 0)
    Out[4]: ∞
    In [5]: limit(1 / (x ** 2 + y ** 2), x, 0)
    Out[5]:
    1
    ──
     2
    y
    In [6]: limit(tan(x), x, pi / 2)
    Out[6]: -∞
    In [7]: limit(tan(x), x, pi / 2, dir='+')
    Out[7]: -∞
    In [8]: limit(tan(x), x, pi / 2, dir='-')
    Out[8]: ∞

Como indican en la documentación de la función, hay bastantes ejemplos de límites no triviales en el archivo [`https://github.com/sympy/sympy/blob/master/sympy/series/tests/test_demidovich.py`](https://github.com/sympy/sympy/blob/master/sympy/series/tests/test_demidovich.py).

## Derivadas

Para calcular la derivada simbólica en SymPy (esto es: la función derivada) se usa la función [`diff`](http://docs.sympy.org/0.7.1/modules/core.html#sympy.core.function.diff) o el método `.diff` de una expresión. Esta admite varias sintaxis para indicar las variables y el orden de las derivadas:

    :::python
    In [1]: cos(x) * (1 + x)
    Out[1]: (x + 1)⋅cos(x)
    In [2]: diff(_1, x)  # Derivada primera con respecto a x
    Out[2]: -(x + 1)⋅sin(x) + cos(x)
    In [3]: diff(_, x)  # Derivada primera con respecto a x de lo anterior
    Out[3]: -(x + 1)⋅cos(x) - 2⋅sin(x)
    In [4]: diff(_1, x, 2)  # Derivada segunda con respecto a x
    Out[4]: -(x + 1)⋅cos(x) - 2⋅sin(x)
    In [5]: diff(_1, x, x)  # Otra forma de escribir lo mismo
    Out[5]: -(x + 1)⋅cos(x) - 2⋅sin(x)
    In [6]: diff(log(x * y), y)  # Derivada parcial con respecto a y
    Out[6]:
    1
    ─
    y
    In [7]: diff(x * y * log(x * y), x, y)  # Derivada parcial con respecto a x e y
    Out[7]: log(x⋅y) + 2

También se pueden derivar funciones simbólicas, y se respeta la regla de la cadena:

    :::python
    In [8]: diff(f(x) * sin(x), x)
    Out[8]:
                         d
    f(x)⋅cos(x) + sin(x)⋅──(f(x))
                         dx   
    In [9]: diff(f(g(x)), x)
    Out[9]:
    d        ⎛ d        ⎞│
    ──(g(x))⋅⎜───(f(ξ₁))⎟│
    dx       ⎝dξ₁       ⎠│ξ₁=g(x)   
    In [10]: diff(f(x * y), y)
    Out[10]:
      ⎛ d        ⎞│
    x⋅⎜───(f(ξ₁))⎟│
      ⎝dξ₁       ⎠│ξ₁=x⋅y
    In [11]: diff(exp(f(x)), x, 2)
    Out[11]:
                  2           2
     f(x) d            f(x)  d
    ℯ    ⋅──(f(x))  + ℯ    ⋅───(f(x))
          dx                  2
                            dx       
    In [12]: diff(f(x), x, 3)
    Out[12]:
      3
     d
    ───(f(x))
      3
    dx

También, [utilizando sustitución como ya vimos en nuestra introducción](https://pybonacci.org/2012/04/04/introduccion-al-calculo-simbolico-en-python-con-sympy/#sustitucion), podemos calcular la derivada en un punto o dejar la derivada sin efectuar utilizando el argumento `evaluate`:

    :::python
    In [13]: diff(sin(x) ** 2, x)
    Out[13]: 2⋅sin(x)⋅cos(x)
    In [14]: diff(sin(x) ** 2, x).subs(x, pi / 4)
    Out[14]: 1
    In [15]: diff(tan(x), x)
    Out[15]:
       2
    tan (x) + 1
    In [16]: _.subs(x, pi / 6)
    Out[16]: 4/3
    In [17]: diff(cos(x), x, evaluate=False)
    Out[17]:
    d
    ──(cos(x))
    dx

## Series

Para calcular desarrollos en series de potencias en SymPy utilizamos la función `series` o el método [`.series`](http://docs.sympy.org/0.7.1/modules/core.html#sympy.core.expr.Expr.series) de una expresión [[2](#cite_note-1){#cite_ref-1}].

    :::python
    In [1]: Expr.series?
    Type:       instancemethod
    Base Class: &lt;type 'instancemethod'&gt;
    String Form:&lt;unbound method Expr.series&gt;
    Namespace:  Interactive
    File:       /usr/lib/python2.7/site-packages/sympy/core/expr.py
    Definition: Expr.series(self, x=None, x0=0, n=6, dir='+')
    Docstring:
    Series expansion of "self" around ``x = x0`` yielding either terms of
    the series one by one (the lazy series given when n=None), else
    all the terms at once when n != None.
    [...]
    In [2]: cos(x).series(x)  # Por defecto, desarrollo en torno al 0 con n = 6 términos
    Out[2]:
         2    4
        x    x
    1 - ── + ── + O(x**6)
        2    24          
    In [3]: log(1 + x).series(x, 0, n=5)
    Out[3]:
         2    3    4
        x    x    x
    x - ── + ── - ── + O(x**5)
        2    3    4           
    In [4]: log(z).series(z, 1, n=5)  # Desarrollo en torno a z = 1 (nótese que en la salida z es (z - 1))
    Out[4]:
         2    3    4
        z    z    z
    z - ── + ── - ── + O(z**5)
        2    3    4  
    In [5]: abs(x).series(x, 0, dir='+')  # Desarrollo por la derecha
    Out[5]: x
    In [6]: abs(x).series(x, 0, dir='-')  # Y por la izquierda
    Out[6]: -x

SymPy ofrece otros dos métodos relacionados con el cálculo de series interesantes:

  * El método [`.nseries`](http://docs.sympy.org/0.7.1/modules/core.html#sympy.core.expr.Expr.nseries). Calcula el desarrollo de una expresión de una manera distinta. Mientras que `.series` nos da el número de términos que hemos indicado con el argumento `n`, `.nseries` calcula los desarrollos de los diferentes factores con ese número de términos y luego opera con ellos, de tal forma que el resultado final puede no llegar al orden que pretendíamos conseguir. En cambio, es un método más rápido porque no requiere saber a priori el número de términos necesarios: 
        :::python
    In [7]: (sin(x) / x).series(x, n=3)
    Out[7]:
         2
        x
    1 - ── + O(x**3)
        6           
    In [8]: (sin(x) / x).nseries(x, n=3)  # El resultado sigue siendo correcto
    Out[8]: 1 + O(x**2)

  * El método [`.lseries`](http://docs.sympy.org/0.7.1/modules/core.html#sympy.core.expr.Expr.lseries) proporciona un iterador con los términos del desarrollo (es equivalente a llamar a `.series` con `n=None`: 
        :::python
    In [9]: s = cos(x).lseries(x)
    In [10]: for term in s:
       ....:     pprint(term)
       ....:
    1
      2
    -x
    ───
     2
     4
    x
    ──
    24
      6
    -x
    ───
    720
    ^C---------------------------------------------------------------------------
    KeyboardInterrupt                         Traceback (most recent call last)
    [...]
    In [11]: s = cos(x).series(x, n=None)  # Equivalente a lo anterior
    In [12]: type(s)
    Out[12]: generator
    In [13]: s.next()
    Out[13]: 1
    In [14]: s.next()
    Out[14]:
      2
    -x
    ───
     2 
    In [15]: s.next()
    Out[15]:
     4
    x
    ──
    24

## Integrales

Para calcular integrales definidas e indefinidas con SymPy emplearemos la función [`integrate`](http://docs.sympy.org/0.7.1/modules/integrals.html#sympy.integrals.integrate). Esta utiliza el [algoritmo de Risch-Norman extendido](http://es.wikipedia.org/wiki/Algoritmo_de_Risch) más algunas reglas heurísticas y búsqueda de patrones:

    :::python
    In [1]: integrate(6 * x ** 5, x)
    Out[1]:
     6
    x 
    In [2]: integrate(x * log(x), x)
    Out[2]:
     2           2
    x ⋅log(x)   x
    ───────── - ──
        2       4 
    In [3]: integrate(exp(-x ** 2), x)
    Out[3]:
      ⎽⎽⎽
    ╲╱ π ⋅erf(x)
    ────────────
         2      
    In [4]: integrate(x * y, y)
    Out[4]:
       2
    x⋅y
    ────
     2  
    In [5]: integrate(cos(x), y)
    Out[5]: y⋅cos(x)
    In [6]: integrate(x * y, x, y)
    Out[6]:
     2  2
    x ⋅y
    ─────
      4  
    In [7]: integrate(x, x, x, y)
    Out[7]:
     3
    x ⋅y
    ────
     6

También podemos efectuar integrales definidas, tanto propias como impropias:

    :::python
    In [8]: integrate(log(x), (x, 0, 1))
    Out[8]: -1
    In [9]: integrate(sin(x) ** 2, (x, 0, pi))
    Out[9]:
    π
    ─
    2
    In [10]: integrate(sin(x), (x, 0, oo))
    Out[10]: 1 - cos(∞)
    In [11]: integrate(exp(-x ** 2), (x, 0, oo))
    Out[11]:
      ⎽⎽⎽
    ╲╱ π
    ─────
      2

Y hasta aquí el artículo de hoy. Si te ha resultado útil o interesante (que espero que sí), recuerda comentar y difundir.

¡Un saludo!

## Notas

<li id="cite_note-0">
  [<a href="#cite_ref-0">^</a>] SymPy utiliza el <a href="http://docs.sympy.org/0.7.1/modules/series.html#the-gruntz-algorithm">algoritmo de Gruntz</a> para calcular límites y requiere evaluar la serie de las funciones, por lo que los límites no pueden involucrar funciones definidas por el usuario (véase [<a id="cite_ref-1" href="#cite_note-1">2</a>]).
</li>
<li id="cite_note-1">
  [<a href="#cite_ref-1">^</a>] Las series para funciones definidas por el usuario <a href="https://github.com/sympy/sympy/blob/sympy-0.7.1/sympy/core/function.py#L336">no están soportadas todavía</a> en la versión 0.7.1.
</li>