---
title: Introducción al Cálculo Simbólico en Python con SymPy
date: 2012-04-04T10:00:04+00:00
author: Juan Luis Cano
slug: introduccion-al-calculo-simbolico-en-python-con-sympy
tags: cálculo simbólico, python, sympy

## Introducción

En este artículo voy a hacer una introducción a [SymPy](http://sympy.org/ "SymPy"), una biblioteca para hacer Cálculo Simbólico en Python a la vez que un [sistema de álgebra computacional](http://es.wikipedia.org/wiki/Sistema_algebraico_computacional "Sistema de álgebra computacional") (o CAS en inglés) muy prometedor. Si alguna vez te has preguntado cómo hacer derivadas y resolver ecuaciones con Python o conoces ya sistemas como Mathematica o Maple pero prefieres utilizar una solución libre, has venido al sitio correcto.

Actualmente [el desarrollo de SymPy](https://github.com/sympy/sympy) está muy activo: a pesar de ser un CAS bastante completo, todavía tiene algunas cosas que sus desarrolladores piensan pulir a lo largo de los próximos meses y están trabajando duro para ello. Personalmente es uno de mis proyectos de software libre favoritos, por la buenísima documentación que escriben, por lo elegante que queda el código y por lo bonita que es su web 😛

SymPy tiene una característica que no tienen ninguno de sus competidores, tanto libres como no libres: se puede utilizar de manera interactiva como los CAS a los que estamos acostumbrados, pero también se puede integrar con nuestro código Python como una biblioteca más.

Se puede [probar online](http://live.sympy.org/ "SymPy Live"), y también se puede descargar e instalar fácilmente. Para lanzar la consola interactiva (basada en IPython) sólo tendremos que escribir

<pre>$ isympy</pre>

Para este tutorial se asumirá que estamos trabajando con la consola interactiva de **SymPy 0.7.1**. Para que el código funcione también en modo no interactivo solamente habrá que incluir los oportunos `import` y sustituir las variables dinámicas de IPython (`_`, `_n`, etc.) por variables reales. Podéis encontrar en Internet la [documentación de SymPy 0.7.1](http://docs.sympy.org/0.7.1/index.html). ¡Vamos allá!

<!--more-->

## Primeros pasos

El alma del Cálculo Simbólico son, naturalmente, las variables simbólicas, que en SymPy son instancias de la clase `Symbol`. Una explicación intuitiva sería que, mientras que las variables ordinarias tienen un valor que puede ser un número, una cadena, un valor verdadero / falso, una secuencia, etc. las variables simbólicas juegan el papel de "contenedores": no sabemos a priori lo que pueden ser. Veamos un ejemplo:

<pre><code class="language-python">$ isympy
IPython console for SymPy 0.7.1 (Python 2.7.2-64-bit) (ground types: python)
These commands were executed:
&gt;&gt;&gt; from __future__ import division
&gt;&gt;&gt; from sympy import *
&gt;&gt;&gt; x, y, z, t = symbols('x y z t')
&gt;&gt;&gt; k, m, n = symbols('k m n', integer=True)
&gt;&gt;&gt; f, g, h = symbols('f g h', cls=Function)
Documentation can be found at http://www.sympy.org
In [1]: w = Symbol('omega', real=True)
In [2]: w
Out[2]: ω
In [3]: n = Symbol('n', integer=True)
In [4]: n
Out[4]: n
In [5]: cos(w * t)
Out[5]: cos(ω⋅t)
In [6]: cos(2 * n * pi)
Out[6]: 1</code></pre>

Analicemos estas líneas:

  * En SymPy, _todas las variables simbólicas que vayamos a utilizar se tienen que definir antes_. Parece que no lo he hecho con `t`, pero en realidad lo ha hecho el programa automáticamente al empezar, como se lee en la cabecera.
  * Al definir una variable, podemos añadir una serie de suposiciones sobre ella (_assumptions_): por ejemplo, hemos dicho que ω será de tipo real y que n será un número entero. Esto es muy importante a la hora de trabajar.
  * No sabemos cuánto vale ω ni cuánto vale t, y por tanto no podemos decir nada sobre su coseno. Sin embargo, aunque no sabemos si n es 1, 5, 10 o -2, n es entero, por lo que el segundo coseno valdrá 1 en todos los casos.

A veces no será todo tan bonito y tendré que trabajar un poco. Esto no es algo propio de Python, también sucede en la mayoría de CAS. Cuanto más inteligente es el sistema menos tendré que trabajar yo, pero aún los ordenadores no pueden solucionarlo todo 😛

Por ejemplo, sé que el coseno de los múltiplos de π valdrá 1 o -1, así que si lo elevo al cuadrado debería salir siempre 1. Sin embargo, SymPy no se da cuenta de esto a priori, pero se le puede ayudar:

<pre><code class="language-python">In [18]: cos(n * pi)
Out[18]: cos(π⋅n)
In [19]: _ ** 2
Out[19]:
   2
cos (π⋅n)
In [20]: simplify(_)
Out[20]:
   2
cos (π⋅n)
In [21]: _.subs(cos(n * pi) ** 2, 1 - sin(n * pi) ** 2)
Out[21]: 1</code></pre>

Veamos qué más posibilidades para manipular expresiones ofrece SymPy.

## Manipulación de expresiones

Para manipular expresiones algebraicas que involucren variables simbólicas en SymPy hay tres herramientas básicas: la [sustitución](http://docs.sympy.org/0.7.1/modules/core.html#sympy.core.basic.Basic.subs), las funciones de [simplificación](http://docs.sympy.org/0.7.1/modules/simplify/simplify.html) y [expansión](http://docs.sympy.org/0.7.1/modules/core.html#expand) y las [suposiciones](http://docs.sympy.org/0.7.1/modules/assumptions.html).

### Sustitución {#sustitucion}

Esta es la parte más elemental de todas: utilizando la función [`subs()`](http://docs.sympy.org/0.7.1/modules/core.html#sympy.core.basic.Basic.subs) de las instancias de `Basic`, sustituimos una parte de la expresión por otra. Se puede dar una pareja de argumentos `(antiguo, nuevo)`, un diccionario `{a1: n1, a2: n2, ...}` o una lista `[(a1, n1), (a2, n2), ...]`.

<pre><code class="language-python">In [1]: 1 + y ** 2
Out[1]:
 2
y  + 1
In [2]: _.subs(1 + y ** 2, t)
Out[2]: t
In [3]: _.subs({t: x ** 2})
Out[3]:
 2
x
In [4]: _.subs([(x, z - 1)])
Out[4]:
       2
(z - 1)</code></pre>

### Suposiciones

Las **suposiciones** (assumptions en inglés, como ya hemos dicho antes) afectan directamente a cómo trata SymPy a la variable simbólica en cuestión.

**Nota:** Actualmente, [como me dijeron en la lista de correo](https://groups.google.com/d/msg/sympy/Ks5YNg_6bEM/dzjH-UXPOGsJ), los desarrolladores están haciendo algunos cambios en el sistema de suposiciones y [hay cosas que no están documentadas](http://code.google.com/p/sympy/issues/detail?id=2196) y [otras que aún no funcionan](https://groups.google.com/d/msg/sympy/ZZyA0RLKu_s/jY2jFReBZy8J). Paciencia.

  * Para imponer que la variable cumple ciertas propiedades en el momento de la creación se utilizan los argumentos `positive`, `real`, etc. en el constructor, indicando su valor de verdadero o falso.
  * Por otro lado, para simplificar una expresión a posteriori con nuevas suposiciones hemos de utilizar la clase `Q` del módulo `assumptions`.
  * Para comprobar si una variable o expresión cumple determinadas propiedades, tendremos que utilizar las funciones `is_real`, `is_integer`, etc.

Veamos algunos ejemplos:

<pre><code class="language-python">In [1]: n.is_integer  # En modo interactivo se ejecutaba k, m, n = symbols('k m n', integer=True)
Out[1]: True
In [2]: x.is_real is None  # En modo interactivo se ejecutaba x, y, z, t = symbols('x y z t')
Out[2]: True
In [3]: sqrt(x ** 2)
Out[3]:
   ⎽⎽⎽⎽
  ╱  2
╲╱  x
In [4]: _.refine(Q.real(x))  # Refinar la expresión sqrt(x ** 2) sabiendo que x es real
Out[4]: │x│
In [5]: _.refine(Q.positive(x))  # Refinar la expresión |x| sabiendo que x es positivo
Out[5]: x
In [6]: p = Symbol('p', positive=True)
In [7]: (1 + p).is_positive
Out[7]: True
In [8]: (1 + p).is_integer  # No sale nada porque no podemos decir la expresión es entera o no
In [8]: (1 + p).is_integer is None  # El valor de is_integer es None
Out[8]: True
In [9]: ask(Q.integer(1 + p), Q.integer(p))  # En cambio, si p es entero entonces 1 + p también
Out[9]: True</code></pre>

### Simplificación y expansión

SymPy pone a nuestra disposición multitud de funciones para reescribir las expresiones en una forma que nos sea más cómoda o que nos aporte algún tipo de beneficio. Están listadas en la [documentación de la clase `Expr`](http://docs.sympy.org/0.7.1/modules/core.html#expr "Expr"), donde se remite en cada caso a la explicación de cada una de las funciones si pertenecen a otro módulo. Sin un orden particular:

<pre><code class="language-python">In [1]: (1 - x ** 2) / (1 + x)
Out[1]:
   2
- x  + 1
────────
 x + 1
In [2]: cancel(_)  # Cancela factores comunes en una función racional
Out[2]: -x + 1
In [3]: cos(3 * x)
Out[3]: cos(3⋅x)
In [4]: expand_trig(_)  # Expansiones trigonométricas
Out[4]:
     3
4⋅cos (x) - 3⋅cos(x)
In [5]: expand(cos(3 * x), trig=True)  # Esta forma es equivalente
Out[5]:
     3
4⋅cos (x) - 3⋅cos(x)
In [6]: y/(x + 2)/(x + 1)
Out[6]:
       y
───────────────
(x + 1)⋅(x + 2)
In [7]: apart(_, x)  # Descompone en fracciones simples
Out[7]:
    y       y
- ───── + ─────
  x + 2   x + 1
In [8]: together(_)  # Denominador común
Out[8]:
       y
───────────────
(x + 1)⋅(x + 2)
In [9]: (1 + I) * (1 + sin(x))
Out[9]: (1 + ⅈ)⋅(sin(x) + 1)
In [10]: expand(_)  # Hace los productos y expande la expresión
Out[10]: sin(x) + ⅈ⋅sin(x) + 1 + ⅈ
In [11]: collect(_, sin(x))  # Saca factor común
Out[11]: (1 + ⅈ)⋅sin(x) + 1 + ⅈ
In [12]: collect(_, 1 + I)  # ¿Puedo volver al principio?
Out[12]: (1 + ⅈ)⋅sin(x) + 1 + ⅈ
In [13]: cse(_)  # Detecta y elimina subexpresiones
Out[13]: ([(x₀, 1 + ⅈ)], [x₀⋅sin(x) + x₀])
In [14]: _12.subs(1 + I, t)  # Voy a hacer un cambio de variable para que sea más sencillo
Out[14]: t⋅sin(x) + t
In [15]: collect(_, t)  # Ahora espero que sí
Out[15]: t⋅(sin(x) + 1)
In [16]: _.subs(t, 1 + I)  # Deshago el cambio
Out[16]: (1 + ⅈ)⋅(sin(x) + 1)</code></pre>

Para simplificar al máximo las expresiones que manejemos normalmente habrá que mezclar estos tres tipos de herramientas e ir manipulándolas secuencialmente hasta llegar a la forma deseada.

## Números

SymPy, como buen CAS que es, ofrece precisión arbitraria para sus tipos numéricos. Al contrario que los números almacenados en [coma flotante](http://es.wikipedia.org/wiki/IEEE_coma_flotante), al utilizar precisión arbitraria podemos conseguir un resultado numérico con un número arbitrario de cifras decimales exactas. SymPy utiliza la biblioteca [mpmath](http://code.google.com/p/mpmath/), escrita en Python.

No obstante, hay que tener cuidado porque si utilizamos los tipos nativos de Python no podremos manejar precisión arbitraria o directamente podremos obtener resultados erróneos, como es el caso de la famosa división de enteros en Python 2:

<pre><code class="language-python">$ ipython2
Python 2.7.2 (default, Jan 31 2012, 13:19:49)
Type "copyright", "credits" or "license" for more information.
IPython 0.12 -- An enhanced Interactive Python.
?         -&gt; Introduction and overview of IPython's features.
%quickref -&gt; Quick reference.
help      -&gt; Python's own help system.
object?   -&gt; Details about 'object', use 'object??' for extra details.
In [1]: 1 / 2
Out[1]: 0
In [2]: from __future__ import division
In [3]: 1 / 2
Out[3]: 0.5</code></pre>

Este punto en concreto está solucionado en modo interactivo, porque se importa la división de enteros moderna automáticamente, pero aun así si queremos mantener los números en su forma racional tendremos que usar la clase `Rational`.

Finalmente, para pasar de un resultado simbólico a uno numérico con cualquier número de decimales utilizaremos las funciones `N()` o `.evalf()`, que son equivalentes.

<pre><code class="language-python">In [1]: 3 / 5
Out[1]: 0.5
In [2]: type(_)
Out[2]: float
In [3]: Rational(3, 5)
Out[3]: 3/5
In [4]: type(_)
Out[4]: sympy.core.numbers.Rational
In [5]: x / 5  # Al aparecer la x ahora no hacen falta precauciones adicionales
Out[5]:
x
─
5
In [6]: N(3 / 5)
Out[6]: 0.600000000000000
In [7]: N(3 / 5, n=30)
Out[7]: 0.599999999999999977795539507497
In [8]: N(Rational(3, 5), n=30)
Out[8]: 0.600000000000000000000000000000
In [9]: pi
Out[9]: π
In [10]: pi.evalf()
Out[10]: 3.14159265358979
In [11]: pi.evalf(n=100)
Out[11]: 3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117068</code></pre>

También podemos hacer el proceso inverso: dado un número decimal, tratar de buscar una representación simbólica del mismo. Esto se puede hacer con la función [`nsimplify()`](http://docs.sympy.org/0.7.1/modules/simplify/simplify.html#sympy.simplify.simplify.nsimplify):

<pre><code class="language-python">In [1]: nsimplify(0.1)
Out[1]: 1/10
In [2]: nsimplify(6.28, [pi], tolerance=0.01)
Out[2]: 2⋅π
In [3]: nsimplify(pi, tolerance=0.001)
Out[3]:
355
───
113
In [4]: nsimplify(1.25992104989, tolerance=0.0001)
Out[4]:
         ⎽⎽⎽⎽⎽⎽
  9    ╲╱ 3235
- ── + ────────
  38      38
In [5]: nsimplify(1.25992104989, tolerance=0.0001, full=True)
Out[5]:
3 ⎽⎽⎽
╲╱ 2
In [6]: cos(atan(1/3))
Out[6]: 0.948683298050514
In [7]: nsimplify(_)
Out[7]:
    ⎽⎽⎽⎽
3⋅╲╱ 10
────────
   10</code></pre>

Esto ha sido una introducción al manejo básico de SymPy. Una vez que ya sabes cómo utilizarlo es sencillo [consultar la documentación](http://docs.sympy.org/0.7.1/index.html "Documentación de SymPy 0.7.1") para saber cuáles son las posibilidades del programa o cómo resolver un problema concreto, aunque ya adelanto que escribiremos sobre SymPy en el futuro 🙂 Espero que te haya resultado útil y recuerda que en los comentarios puedes hacer todas las preguntas que te surjan al respecto.