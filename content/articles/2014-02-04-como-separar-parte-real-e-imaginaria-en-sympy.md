---
title: ¿Cómo separar parte real e imaginaria en SymPy?
date: 2014-02-04T10:26:29+00:00
author: Juan Luis Cano
slug: como-separar-parte-real-e-imaginaria-en-sympy
tags: números complejos, python, sympy

Andaba yo preguntándome esta mañana, a falta (¡sorprendentemente!) de dudas de los lectores:

> Si tengo un **número complejo en SymPy**, ¿cómo puedo separar la parte real y la parte imaginaria? Y ya puestos, ¿puedo separar también el módulo y el argumento?

Si utilizamos el tipo `complex` de Python el resultado es correcto pero puede no ser demasiado vistoso:

<pre><code class="language-python">$ isympy
In [1]: (1j + 1) / (5 - 2j)
Out[1]: (0.10344827586206896+0.24137931034482757j)</code></pre>

Queremos usar las capacidades simbólicas de SymPy. En SymPy, [como se indica en el tutorial](https://github.com/sympy/sympy/wiki/Tutorial), los complejos se declaran de esta manera:

<pre><code class="language-python">In [2]: (1 * I + 1) / (5 - 2 * I)
Out[2]:
 1 + ⅈ
───────
5 - 2⋅ⅈ</code></pre>

Y ya tenemos un objeto de SymPy con toda su potencia (que además se imprime bonito). Para extraer la parte real e imaginaria podemos usar las funciones [`re`](http://docs.sympy.org/latest/modules/functions/elementary.html#re) e [`im`](http://docs.sympy.org/latest/modules/functions/elementary.html#im) o el método [`as_real_imag`](http://docs.sympy.org/latest/modules/core.html#sympy.core.expr.Expr.as_real_imag).

<pre><code class="language-python">In [3]: a = (1 * I + 1) / (5 - 2 * I)
In [4]: re(a)
Out[4]: 3/29
In [5]: im(a)
Out[5]: 7/29
In [6]: a.as_real_imag()
Out[6]: (3/29, 7/29)</code></pre>

Estos métodos extraen la parte real y la imaginaria pero «pierdo» el número original. Para **reescribir** el número separando parte real e imaginaria lo mejor es emplear el método `expand(complex=True)`:

<pre><code class="language-python">In [9]: a.expand(complex=True)
Out[9]:
3    7⋅ⅈ
── + ───
29    29</code></pre>

Esto ya es otra cosa 😉

<!--more-->

¿Y qué pasa si tenemos una expresión simbólica? También podemos separarla, pero en este caso hay que tener cuidado con la definición de los símbolos:

<pre><code class="language-python">In [12]: f = 1 / (x + I * y)
In [13]: f
Out[13]:
   1
───────
x + ⅈ⋅y
In [14]: f.expand(complex=True)
Out[14]:
                              re(x)
───────────────────────────────────────────────────────────────── - ──────────
  2                        2                        2        2        2
re (x) - 2⋅re(x)⋅im(y) + re (y) + 2⋅re(y)⋅im(x) + im (x) + im (y)   re (x) - 2
                   ⅈ⋅re(y)
─────────────────────────────────────────────────────── - ────────────────────
                 2                        2        2        2
⋅re(x)⋅im(y) + re (y) + 2⋅re(y)⋅im(x) + im (x) + im (y)   re (x) - 2⋅re(x)⋅im(
         ⅈ⋅im(x)
───────────────────────────────────────────── - ──────────────────────────────
       2                        2        2        2                        2
y) + re (y) + 2⋅re(y)⋅im(x) + im (x) + im (y)   re (x) - 2⋅re(x)⋅im(y) + re (y
im(y)
───────────────────────────────────
                      2        2
) + 2⋅re(y)⋅im(x) + im (x) + im (y)</code></pre>

_¿Qué demonios?_ El problema es que, por defecto, los símbolos en SymPy pertenecen al cuerpo de los números complejos:

<pre><code class="language-python">In [25]: x.expand(complex=True)
Out[25]: re(x) + ⅈ⋅im(x)</code></pre>

Observa de hecho que algunas simplificaciones no se llevarán a cabo, [como se explica en la documentación](http://docs.sympy.org/latest/tutorial/simplification.html#powers):

<pre><code class="language-python">In [26]: sqrt(x ** 2)
Out[26]:
   ____
  ╱  2
╲╱  x</code></pre>

Pero podemos crear símbolos con las propiedades (en SymPy _assumptions_) que nosotros queramos:

<pre><code class="language-python">In [29]: x, y = symbols("x, y", real=True)
In [30]: f = 1 / (x + I * y)
In [31]: f
Out[31]:
   1
───────
x + ⅈ⋅y 
In [32]: f.expand(complex=True)  # ¡Mucho mejor!
Out[32]:
   x        ⅈ⋅y
─────── - ───────
 2    2    2    2
x  + y    x  + y
In [33]: x.assumptions0
Out[33]:
{'commutative': True,
 'complex': True,
 'hermitian': True,
 'imaginary': False,
 'real': True}
In [34]: x.is_real
Out[34]: True</code></pre>

Para hallar el módulo y el argumento, empleamos las funciones `abs` y `arg`, aunque tal vez haga falta expandir la expresión primero:

<pre><code class="language-python">In [47]: abs(f)
Out[47]:
│   1   │
│───────│
│x + ⅈ⋅y│
In [48]: abs(f.expand(complex=True))
Out[48]:
       _________________________
      ╱      2            2
     ╱      x            y
    ╱   ────────── + ──────────
   ╱             2            2
  ╱     ⎛ 2    2⎞    ⎛ 2    2⎞
╲╱      ⎝x  + y ⎠    ⎝x  + y ⎠ 
In [49]: arg(f.expand(complex=True))  # No funciona :(
Out[49]:
   ⎛   x        ⅈ⋅y  ⎞
arg⎜─────── - ───────⎟
   ⎜ 2    2    2    2⎟
   ⎝x  + y    x  + y ⎠
In [56]: a
Out[56]:
 1 + ⅈ
───────
5 - 2⋅ⅈ
In [54]: abs(a)
Out[54]:
  ___ │   1   │
╲╱ 2 ⋅│───────│
      │5 - 2⋅ⅈ│
In [55]: abs(a.expand(complex=True))
Out[55]:
  ____
╲╱ 58
──────
  29  
In [57]: arg(a)
Out[57]: atan(7/3)</code></pre>

Si especificamos las propiedades adecuadas, las simplificaciones se efectúan correctamente:

<pre><code class="language-python">In [35]: sqrt(x ** 2)
Out[35]: │x│</code></pre>

Quien esperase `x` como resultado tiene que repasar matemáticas 😉

También podemos utilizar el sistema de _assumptions_ de SymPy (¿cómo traduciría esto?):

<pre><code class="language-python">In [38]: refine(sqrt(z ** 2), Q.real(z))
Out[38]: │z│
In [39]: refine(sqrt(z ** 2), Q.positive(z))
Out[39]: z
In [41]: with assuming(Q.positive(z)):
   ....:     print(ask(Q.real(sqrt(z))))
   ....:
True</code></pre>

Y esto ya no responde a la pregunta de la semana, ¡pero seguro que resulta útil!

¡Recuerda [mandarnos tu pregunta](http://pybonacci.org/contacto/ "Contacto") para que la contestemos semanalmente en Pybonacci! Un saludo 😉