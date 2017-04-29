---
title: Ecuaciones no lineales: método de bisección y método de Newton en Python
date: 2012-04-18T19:53:50+00:00
author: Juan Luis Cano
slug: ecuaciones-no-lineales-metodo-de-biseccion-y-metodo-de-newton-en-python
tags: biseccion, ecuaciones no lineales, newton, python

En este artículo vamos a ver cómo implementar en Python el **método de bisección** y el **método de Newton**, dos métodos iterativos clásicos para hallar raíces de ecuaciones no lineales de la forma $f(x) = 0$, con $f: [a, b] \longrightarrow \mathbb{R}$ y $f \in C^1([a, b])$. Estos métodos y muchos otros más refinados están ya implementados en multitud de bibliotecas muy utilizadas, sin ir más lejos en el módulo [`optimize`](http://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#root-finding) del paquete Scipy ([referencia](http://docs.scipy.org/doc/scipy/reference/optimize.html#root-finding)).

Crearemos un módulo `ceros.py` en el que incluiremos los dos métodos que vamos a desarrollar aquí, y así veremos un ejemplo de código limpio y fácilmente reutilizable.

## Módulo `ceros.py`

Vamos a ver la anatomía de un módulo en Python. Este es el código del archivo:

<!--more-->

<pre><code class="language-python"># -*- coding: utf-8 -*-
"""Búsqueda de raíces
Este módulo contiene métodos para la búsqueda de raíces de ecuaciones de la
forma f(x) = 0, con f función real de variable real, continua y de derivada
continua.
"""
def biseccion():
    """Método de bisección"""
    pass
def newton():
    """Método de Newton"""
    pass</code></pre>

Analicemos el código:

  * La primera línea es fundamental en Python 2 si vamos a usar caracteres que se salen de ASCII. En ella especificamos que la codificación sea UTF-8, como viene recogido en la [PEP 263](http://www.python.org/dev/peps/pep-0263/ "PEP 263 -- Defining Python Source Code Encodings").
  * La línea entre triples comillas dobles es lo que se llama _docstring_ o cadena de documentación del módulo, y siempre es una cadena que se pone al principio del archivo, como viene especificado en la [PEP 257](http://www.python.org/dev/peps/pep-0257/ "PEP 257 -- Docstring Conventions - Python"). Lo de usar triples comillas nos aseguramos de que podemos incluir saltos de línea.
  * Definimos dos funciones, también con su _docstring_. La palabra clave `pass` se utiliza para que cuadre el sangrado del código: no hace nada.
  * Las convenciones en cuanto a espacios, longitud de las líneas, etc. están definidas en la [PEP 8](http://www.python.org/dev/peps/pep-0008/ "PEP 8 -- Style Guide for Python Code"), que viene a ser como el manual de estilo oficial para programas en Python. Puedes comprobar si tu código se adhiere a esta convención con la herramienta [pep8](http://pypi.python.org/pypi/pep8/0.6.1 "pep8 en el PyPI") disponible en el Índice de Paquetes de Python (PyPI).

Para utilizar este módulo, simplemente lenzaríamos un intérprete Python en la carpeta donde esté el archivo `ceros.py` y escribiríamos:

<pre><code class="language-python">&gt;&gt;&gt; import ceros
&gt;&gt;&gt; dir(ceros)
['__builtins__', '__doc__', '__file__', '__name__', '__package__', 'biseccion', 'newton']
&gt;&gt;&gt; print ceros.__doc__
Búsqueda de raíces
Este módulo contiene métodos para la búsqueda de raíces de ecuaciones de la
forma f(x) = 0, con f función real de variable real, continua y de derivada
continua.
&gt;&gt;&gt; print ceros.biseccion
&lt;function biseccion at 0x7fc17efb5668&gt;</code></pre>

Ahora no hay más que _implementar_ estos métodos.

## Método de la bisección

### Descripción y algoritmo

El [método de bisección](http://es.wikipedia.org/wiki/M%C3%A9todo_de_bisecci%C3%B3n "Método de bisección") es un método geométricamente muy intuitivo: partiendo de un intervalo $[a, b]$ tal que $f(a) f(b) < 0$ (es decir: la función cambia de signo en el intervalo), se va dividiendo en dos generando una [sucesión de intervalos encajados](http://es.wikipedia.org/wiki/Principio_de_los_intervalos_encajados) hasta que se converge con la precisión deseada a la raíz de la ecuación que, como asegura el [teorema de Bolzano](http://es.wikipedia.org/wiki/Teorema_del_valor_intermedio#Teorema_de_Bolzano "Teorema de Bolzano"), tiene que existir; es decir, el $\alpha in ]a, b[$ tal que $f(\alpha) = 0$.

El algoritmo del método de bisección sería el siguiente:

> <ol start="0">
>   <li>
>     Sean $f$, $a$ y $b$. <ol>
>       <li>
>         Sea $c \leftarrow \frac{a + b}{2}$.
>       </li>
>       <li>
>         Si $f(c) = 0$, terminar.
>       </li>
>       <li>
>         Si $f(c) f(a) < 0$, entonces $b \leftarrow c$ y volver al paso 1.
>       </li>
>       <li>
>         Si no, entonces $a \leftarrow c$ y volver al paso 1.
>       </li>
>     </ol>
>   </li>
> </ol>

Este método, aunque es lento, **tiene convergencia garantizada**.

### Método de bisección en Python

A la vista del algoritmo anterior, ya podemos implementar el método de bisección en Python. Nos vamos a saltar la parte de escribir el pseudocódigo.

**_Nota_**: Cambiado por sugerencia de David para evitar errores de precisión.

<pre><code class="language-python">import numpy as np
def biseccion(f, a, b, tol=1.0e-6):
    """Método de bisección
    Halla una raíz de la función f en el intervalo [a, b] mediante el método
    de bisección.
    Argumentos
    ----------
    f - Función, debe ser tal que f(a) f(b) &lt; 0
    a - Extremo inferior del intervalo
    b - Extremo superior del intervalo
    tol (opcional) - Cota para el error absoluto de la x
    Devuelve
    --------
    x - Raíz de f en [a, b]
    Excepciones
    -----------
    ValueError - Intervalo mal definido, la función no cambia de signo en el
                 intervalo o cota no positiva
    Ejemplos
    --------
    &gt;&gt;&gt; def f(x): return x ** 2 - 1
    ...
    &gt;&gt;&gt; biseccion(f, 0, 2)
    1.0
    &gt;&gt;&gt; biseccion(f, 0, 5)
    1.000000238418579
    &gt;&gt;&gt; biseccion(f, -2, 2)
    Traceback (most recent call last):
        File "&lt;stdin&gt;", line 1, in &lt;module&gt;
        File "ceros.py", line 35, in biseccion
        raise ValueError("La función debe cambiar de signo en el intervalo")
    ValueError: La función debe cambiar de signo en el intervalo
    &gt;&gt;&gt; biseccion(f, -3, 0, tol=1.0e-12)
    -1.0000000000004547
    """
    if a &gt; b:
        raise ValueError("Intervalo mal definido")
    if f(a) * f(b) &gt;= 0.0:
        raise ValueError("La función debe cambiar de signo en el intervalo")
    if tol &lt;= 0:
        raise ValueError("La cota de error debe ser un número positivo")
    x = (a + b) / 2.0
    while True:
        if b - a &lt; tol:
            return x
        # Utilizamos la función signo para evitar errores de precisión
        elif np.sign(f(a)) * np.sign(f(x)) &gt; 0:
            a = x
        else:
            b = x
        x = (a + b) / 2.0</code></pre>

Vamos a señalar algunas cosas:

  * Como se puede observar, el código se parece bastante al algoritmo.
  * Podemos pasar una función como argumento sin ningún esfuerzo.
  * Hemos incluido en la documentación información sobre los argumentos que recibe la función, de manera que si escribimos en el intérprete`help(ceros.biseccion)` podremos consultarla.
  * No he incluido un número máximo de iteraciones: fijada una precisión, el método convergerá siempre.

Por último, nótese que el programa produce un error si el límite inferior de intervalo es mayor que el límite superior, si la función no cambia de signo o si la cota de error es un número negativo. Python hace muy sencillas este tipo de construcciones: se denomina [manejo de excepciones](http://docs.python.org/tutorial/errors.html#handling-exceptions "Manejo de excepciones").

Podíamos haber tomado la decisión de no incluir este manejo de errores, y dejar que el programa falle inesperadamente si el usuario hace «cosas raras». Esto que lo decida cada uno.

Para gestionar los errores que se pueden producir, utilizamos el bloque `try...except`:

<pre><code class="language-python">try:
    biseccion(f, a, b)
except ValueError:
    pass  # Este bloque se ejecuta si se produce un error</code></pre>

Gracias a esta característica de Python podemos evitar cosas como que una división por cero mate al programa, por ejemplo.

## Método de Newton

### Descripción y algoritmo

El [método de Newton](http://es.wikipedia.org/wiki/M%C3%A9todo_de_Newton "Método de Newton") o método de Newton-Raphson linealiza la función a cada paso utilizando su derivada, que se debe proporcionar como argumento, para hallar la raíz de la ecuación en las proximidades de un punto inicial $x_0$. Este método puede no converger, pero si el punto inicial está lo suficientemente próximo a la raíz, la convergencia será muy rápida.

El algoritmo del método de Newton es este:

> <ol start="0">
>   <li>
>     Sean $f$, $f'$ y $x_0$.
>   </li>
>   <li>
>     Sea $x \leftarrow x_0$. <ol start="2">
>       <li>
>         Sea $x \leftarrow x - \frac{f(x)}{f'(x)}$.
>       </li>
>       <li>
>         Si $f(x) = 0$, terminar.
>       </li>
>       <li>
>         Si no, volver al paso 2.
>       </li>
>     </ol>
>   </li>
> </ol>

### Método de Newton en Python

Aquí, debido a que el método no tiene garantizada la convergencia, habrá que considerar un número máximo de iteraciones y cotas de error tanto para la raíz como para el valor de la función.

El código sería este:

<pre><code class="language-python">def newton(f, df, x_0, maxiter=50, xtol=1.0e-6, ftol=1.0e-6):
    """Método de Newton
    Halla la raíz de la función f en el entorno de x_0 mediante el método de
    Newton.
    Argumentos
    ----------
    f - Función
    df - Función, debe ser la función derivada de f
    x_0 - Punto de partida del método
    maxiter (opcional) - Número máximo de iteraciones
    xtol (opcional) - Cota para el error relativo para la raíz
    ftol (opcional) - Cota para el valor de la función
    Devuelve
    --------
    x - Raíz de la ecuación en el entorno de x_0
    Excepciones
    -----------
    RuntimeError - No hubo convergencia superado el número máximo de
                   iteraciones
    ZeroDivisionError - La derivada se anuló en algún punto
    Exception - El valor de x se sale del dominio de definición de f
    Ejemplos
    --------
    &gt;&gt;&gt; def f(x): return x ** 2 - 1
    ...
    &gt;&gt;&gt; def df(x): return 2 * x
    ...
    &gt;&gt;&gt; newton(f, df, 2)
    1.000000000000001
    &gt;&gt;&gt; newton(f, df, 5)
    1.0
    &gt;&gt;&gt; newton(f, df, 0)
    Traceback (most recent call last):
      File "&lt;stdin&gt;", line 1, in &lt;module&gt;
      File "ceros.py", line 102, in newton
        dx = -f(x) / df(x)  # ¡Aquí se puede producir una división por cero!
    ZeroDivisionError: float division by zero
    """
    x = float(x_0)  # Se convierte a número de coma flotante
    for i in xrange(maxiter):
        dx = -f(x) / df(x)  # ¡Aquí se puede producir una división por cero!
                            # También x puede haber quedado fuera del dominio
        x = x + dx
        if abs(dx / x) &lt; xtol and abs(f(x)) &lt; ftol:
            return x
    raise RuntimeError("No hubo convergencia después de {}
                        iteraciones".format(maxiter))</code></pre>

Se deja como ejercicio (qué placentero es decir esto) programar el [método de la secante](http://es.wikipedia.org/wiki/M%C3%A9todo_de_la_secante "Método de la secante") que se utilice como alternativa si no se dispone de la derivada de la función.

¡Y con eso terminamos el artículo de hoy! Espero que te haya resultado provechoso, no olvides comentar, retwittear y demás zarandajas 🙂

## Referencias

  * RIVAS, Damián y VÁZQUEZ, Carlos. _Elementos de Cálculo Numérico_. ADI, 2010.