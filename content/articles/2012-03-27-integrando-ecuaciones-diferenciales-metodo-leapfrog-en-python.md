---
title: Integrando ecuaciones diferenciales: método leapfrog en Python
date: 2012-03-27T10:06:27+00:00
author: Juan Luis Cano
slug: integrando-ecuaciones-diferenciales-metodo-leapfrog-en-python
tags: ecuaciones diferenciales, integración, numpy, python

## Introducción

En Python tenemos numerosas herramientas listas para que podamos integrar ecuaciones diferenciales ordinarias sin tener que preocuparnos en implementar un esquema numérico. Sin ir más lejos, en el módulo integrate de [SciPy](http://scipy.org/ "SciPy") existen varias funciones a tal efecto. La función [odeint](http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html "Función odeint") es una interfraz en Python a la biblioteca ODEPACK, escrita en Fortran. Sin embargo, con un propósito didáctico vamos a estudiar cómo programaríamos la solución a un problema de ecuaciones diferenciales, en este caso utilizando la regla del punto medio o método leapfrog[1].

**_Para esta entrada se ha utilizado python 2.7.2, numpy 1.6.1 y matplotlib 1.1.0._**

## Enunciado

> Problema de Cauchy: integrar la siguiente ecuación diferencial
> 
> $\frac{d^2 x}{d t^2} + x = 0$
> 
> Con las condiciones iniciales $x(0) = 1, \dot{x}(0) = 0$.

<!--more-->

## Tratamiento matemático

Sabemos que la solución de este sistema es

$x(t) = \cos{t}$

Siento fastidiar la sorpresa 🙂

En primer lugar, hemos de darle a este problema el tratamiento matemático necesario para poder resolverlo numéricamente con facilidad. Para ello, transformaremos la EDO (Ecuación Diferencial Ordinaria) de 2º orden en un sistema de dos EDOs de 1º orden. Definiendo el vector

$U = \begin{pmatrix} x &#092;\ \dot{x} \end{pmatrix}$

tendremos

$\frac{d U}{d t} = \begin{pmatrix} \dot{x} &#092;\ -x \end{pmatrix} = \begin{pmatrix} 0 & 1 &#092;\ -1 & 0 \end{pmatrix} \begin{pmatrix} x &#092;\ \dot{x} \end{pmatrix} = A U = F(U)$

donde $A$ es la matriz del sistema. Utilizaremos el esquema leapfrog para resolver el sistema. Su EDD (Ecuación en Diferencias) es

$U^{n + 1} = U^{n - 1} + 2 \Delta t F(U^n)$

Como se puede ver, no podemos aplicar directamente el esuqema para el paso 1 porque no tenemos $U^{-1}$. Debemos arrancar con un esquema de un paso, como por ejemplo un [Euler explícito](http://es.wikipedia.org/wiki/M%C3%A9todo_de_Euler "Método de Euler"):

$U^{n + 1} = U^n + \Delta t F(U^n)$

Puesto que tenemos

$U^0 = \begin{pmatrix} x(0) &#092;\ \dot{x}(0) \end{pmatrix} = \begin{pmatrix} 1.0 &#092;\ 0.0 \end{pmatrix}$

ya podemos resolver el problema, sin más que escoger un valor del paso.

## Implementación

Aunque no sería estrictamente necesario, como la expresión de la matriz del sistema es muy sencilla vamos a utilizar las capacidades de NumPy para manejar matrices. La función $F(U)$ quedará, en Python,

<pre><code class="language-python">A = np.array([  # Matriz del sistema
    [ 0, 1],
    [-1, 0]
])
def F(t, u):
    return np.dot(A, u)</code></pre>

Aquí hemos utilizado la función `\dot(a, b)`, que para el caso de que `a` sea un array bidimensional y `b` un array unidimensional es el producto de matriz por vector al que estamos acostumbrados en Álgebra Lineal.

**Nota:**Nótese que no podíamos escribir directamente `A * u`. ¡Esto no sería el producto de matriz por vector, sería el producto de dos arrays!

Ahora llegó el momento de implementar los esquemas Euler y leapfrog. Como queremos que sea lo más general posible, aceptaremos que la función `F` sea cualquiera y pueda depender del tiempo, que el paso `dt` se pueda también escoger y que cada vez que llamemos a las funciones nos den solamente el paso siguiente.

Para el caso del Euler, los datos de entrada serán el instante `t_n`, el vector `u_n`, la función `F(t, u)` y el paso `dt`, y el método nos dará el vector `u_n1`.

<pre><code class="language-python">def euler_step(t_n0, u_n0, F, dt=0.1):
    """Método Euler explícito."""
    return u_n0 + dt * F(t_n0, u_n0)</code></pre>

Traducción literal de la EDD del esquema a Python. Más sencillo imposible 🙂

Hacemos lo mismo con el esquema leapfrog:

<pre><code class="language-python">def lf_step(t_n1, u_n0, u_n1, F, dt=0.1):
    """Método leapfrog."""
    return u_n0 + 2 * dt * F(t_n1, u_n1)</code></pre>

Ya sólo nos queda implementar la lógica del programa.

## Solución numérica

En primer lugar decidiremos el número `n` de pasos que queremos dar, o hasta dónde queremos hallar la solución, y guardaremos los sucesivos valores de x en un array de dimensión `n`. Para ello utilizamos la función `empty(shape)`, que nos inicializa un array con la forma dada por el primer argumento, y `linspace(a, b, n)`, que discretizará el intervalo $[a, b]$ con `n` puntos. El código correspondiente a esto y a dar las condiciones iniciales quedará:

<pre><code class="language-python"># Número de pasos
n = 100
# Paso del esquema
dt = 0.1
# Vector solución y vector de tiempos
t = np.linspace(0.0, (n - 1) * dt, n)
x = np.empty(n)
# Condición inicial
x[0] = 1.0</code></pre>

Ya podemos empezar a integrar. El primer paso lo daremos con el euler, y los que queden hasta `n` con el método leapfrog. Después de cada paso guardamos el valor x hallado, y vamos avanzando. Como necesitaremos guardar dos pasos del vector U para poder aplicar el método leapfrog, tendremos que escribir a continuación

<pre><code class="language-python"># Vector U^0
u_n0 = np.array([x[0], 0.0])
# Paso 1: Euler explícito
u_n1 = euler_step(t[0], u_n0, F, dt)
x[1] = u_n1[0]  # Primera componente del vector U
# Paso 2: Leapfrog
u_n2 = lf_step(t[1], u_n0, u_n1, F, dt)
x[2] = u_n2[0]</code></pre>

A partir de ahora, todos los pasos son iguales. Iremos sobreescribiendo en `u_n0` y `u_n1` los valores de los vectores que necesitemos para cada paso del leapfrog, y en `u_n2` escribiremos la solución dada por el método. El código del bucle será, finalmente,

<pre><code class="language-python">for i in range(3, n):
    u_n0 = u_n1
    u_n1 = u_n2
    u_n2 = lf_step(t[i - 1], u_n0, u_n1, F, dt)
    x[i] = u_n2[0]</code></pre>

¡Fácil, rápido y para toda la familia! 🙂

## Representación gráfica

Y ya, para dar el toque de gracia, representemos gráficamente la solución con estas sencillas líneas:

<pre><code class="language-python">plt.plot(t, x)
plt.show()</code></pre>

[<img class="aligncenter size-medium wp-image-108" title="Solución numérica" src="http://new.pybonacci.org/images/2012/03/sol_numerica.png?w=300" alt="" width="300" height="225" srcset="https://pybonacci.org/wp-content/uploads/2012/03/sol_numerica.png 800w, https://pybonacci.org/wp-content/uploads/2012/03/sol_numerica-300x225.png 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://new.pybonacci.org/images/2012/03/sol_numerica.png)

¿Esperabas que fuese más difícil? 😀

## Conclusión

El código final es este:

<pre><code class="language-python"># -*- coding: utf-8 -*-
#
# Problema de Cauchy con el método leapfrog
# Juan Luis Cano 
import numpy as np
import matplotlib.pyplot as plt
# Matriz del sistema
A = np.array([
    [ 0, 1],
    [-1, 0]
])
# Función
def F(t, u):
    return np.dot(A, u)
def euler_step(t_n0, u_n0, F, dt=0.1):
    """Método Euler explícito."""
    return u_n0 + dt * F(t_n0, u_n0)
def lf_step(t_n1, u_n0, u_n1, F, dt=0.1):
    """Método leapfrog."""
    return u_n0 + 2 * dt * F(t_n1, u_n1)
# Número de pasos
n = 100
# Paso del esquema
dt = 0.1
# Vector solución y vector de tiempos
t = np.linspace(0.0, (n - 1) * dt, n)
x = np.empty(n)
# Condición inicial
x[0] = 1.0
# Vector U^0
u_n0 = np.array([x[0], 0.0])
# Paso 1: Euler explícito
u_n1 = euler_step(t[0], u_n0, F, dt)
x[1] = u_n1[0]  # Primera componente del vector U
# Paso 2: Leapfrog
u_n2 = lf_step(t[1], u_n0, u_n1, F, dt)
x[2] = u_n2[0]
for i in range(3, n):
    u_n0 = u_n1
    u_n1 = u_n2
    u_n2 = lf_step(t[i - 1], u_n0, u_n1, F, dt)
    x[i] = u_n2[0]
# Representación gráfica
plt.plot(t, x)
plt.show()</code></pre>

Como se puede ver, en 60 líneas de código incluyendo abundantes comentarios y espacios en blanco hemos implementado un esquema numérico para resolver un problema de ecuaciones diferenciales y hemos representado la solución, sin salirnos de Python.

Espero que te haya resultado útil, nos vemos en Pybonacci 🙂

## Referencias

  * [1] Wikipedia: The Free Encyclopedia. _Leapfrog integration_ (inglés). Recuperado el 27 de marzo de 2012 de <<http://en.wikipedia.org/wiki/Leapfrog_integration>>.