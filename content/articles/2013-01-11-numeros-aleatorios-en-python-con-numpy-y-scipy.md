---
title: Números aleatorios en Python con NumPy y SciPy
date: 2013-01-11T18:00:31+00:00
author: Juan Luis Cano
slug: numeros-aleatorios-en-python-con-numpy-y-scipy
tags: aleatorio, números aleatorios, python, random

## Introducción

En este artículo vamos a hacer un repaso de algunos métodos que tenemos para **generar números aleatorios en Python**. Los números aleatorios son importantísimos en computación: aquí en Pybonacci ya los hemos aplicado en nuestra [simulación de Monte Carlo para calcular áreas de polígonos](http://pybonacci.org/2012/10/18/calculando-cosas-mientras-jugamos-a-la-ruleta/ "Calculando cosas mientras jugamos a la ruleta") y en nuestro artículo sobre [algoritmos heurísticos en Python](http://pybonacci.org/2012/10/31/nuestro-primer-algoritmo-heuristico/ "Nuestro primer algoritmo heurístico"). Como veremos, NumPy ofrece funciones para generar datos aleatorios simples y algunas distribuciones estadísticas, que luego amplía SciPy.

Vamos a mencionar sin explicar las distribuciones uniforme y normal, así que si quieres una explicación más detallada te recomiendo que leas nuestro artículo sobre [estadística en Python con SciPy](http://pybonacci.org/2012/04/21/estadistica-en-python-con-scipy/ "Estadística en Python con SciPy (I)"). Haremos referencia a él más adelante.

_**En esta entrada se han usado python 3.3.0, numpy 1.7.0rc1 y scipy 0.11.0.**_

## ¿Aleatorios?

Antes que nada, hay algo importante que tenemos que aclarar. En realidad, no hay algoritmos que generen números puramente aleatorios y que sean deterministas, por lo que usando solamente software es imposible obtener números verdaderamente aleatorios. Como dicen en Ask SciPy, para generar números aleatorios con un ordenador necesitas muestrear algún proceso físico real: por ejemplo, en [www.random.org](http://www.random.org) utilizan ruido atmosférico, y en [www.fourmilab.ch/hotbits/](http://www.fourmilab.ch/hotbits/) desintegración radiactiva.

En computación realmente se dispone de **números pseudoaleatorios**, que son secuencias determinadas a partir de unos ciertos datos iniciales que se parecen _bastante_ a una aleatoria. NumPy utiliza un algoritmo llamado "[Mersenne twister](http://en.wikipedia.org/wiki/Mersenne_twister)", creado por dos matemáticos japoneses y que utilizan otros programas como MATLAB.

Ahora que ya hemos hecho esta aclaración, en adelante llamaremos **aleatorios** a los números pseudoaleatorios - por brevedad 🙂

<!--more-->

En la librería estándar de Python viene ya incluido el módulo [`random`](http://docs.python.org/3.3/library/random.html), con funciones pensadas para trabajar con valores escalares y listas. Las que vamos a ver ahora pueden trabajar con arrays de NumPy.

**Nota**: Algunas de estas funciones tenían (o tienen) una documentación un poco deficiente pero afortunadamente están recibiendo algo del amor que necesitan. Voy a enlazar a la [_versión de desarrollo_ de la referencia](http://docs.scipy.org/doc/numpy-dev/reference/index.html), que es la que ha incorporado esos cambios, y lo dejaré así hasta que salga NumPy 1.7.0 final.

## Datos aleatorios simples con NumPy

### Generación de datos aleatorios

En el paquete [`random`](http://docs.scipy.org/doc/numpy-dev/reference/routines.random.html) de NumPy encontramos varias funciones para generar datos aleatorios de manera sencilla. La primera es [`np.random.rand`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.rand.html), que devuelve un número aleatorio procedente de una distribución uniforme en el intervalo $[0, 1)$. Admite como argumentos opcionales la forma del array de salida:

    :::python
    In [2]: np.random.rand()  # Sin argumentos devuelve escalar
    Out[2]: 0.3409858521482125
    In [3]: np.random.rand()
    Out[3]: 0.5945242017333028
    In [4]: np.random.rand()
    Out[4]: 0.32207347448156687
    In [15]: np.random.rand(4)  # Un array de 4 elementos
    Out[15]: array([ 0.72096635,  0.02161625,  0.20592277,  0.05077326])
    In [16]: np.random.rand(3, 2)
    Out[16]:
    array([[ 0.30227189,  0.66391029],
           [ 0.30811439,  0.58359128],
           [ 0.06957095,  0.86740448]])

La función `np.random.random_sample` hace lo mismo, pero recibe el argumento en forma de tupla. Tiene cuatro alias: `random`, `sample` y `ranf`.

    :::python
    In [28]: np.random.seed(0)
    In [29]: np.random.random_sample((2, 2))
    Out[29]:
    array([[ 0.5488135 ,  0.71518937],
           [ 0.60276338,  0.54488318]])
    In [30]: np.random.seed(0)
    In [31]: np.random.rand(*(2, 2))  # Se desempaqueta la tupla
    Out[31]:
    array([[ 0.5488135 ,  0.71518937],
           [ 0.60276338,  0.54488318]])

Antes de seguir, ¿recordáis que hemos dicho que estos números son pseudoaleatorios? A veces nos puede interesar, por ejemplo para pruebas, utilizar siempre una misma secuencia pseudoaleatoria. Utilizando la función [`np.random.seed`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.seed.html) imponemos las condiciones iniciales del generador; si no se llama (como hemos hecho antes), NumPy escoge la hora como semilla, de tal forma que cada programa utilice secuencias diferentes:

    :::python
    In [5]: np.random.seed(0)  # Ponemos la semilla a 0 (puede ser cualquier número)
    In [6]: np.random.rand()
    Out[6]: 0.5488135039273248
    In [7]: np.random.rand(3)
    Out[7]: array([ 0.71518937,  0.60276338,  0.54488318])
    In [8]: np.random.seed(0)  # Ponemos la semilla a 0 otra vez
    In [9]: np.random.rand()  # El mismo número
    Out[9]: 0.5488135039273248
    In [10]: np.random.rand(3)  # ¡Y el mismo array!
    Out[10]: array([ 0.71518937,  0.60276338,  0.54488318])

Si queremos generar datos enteros entonces tenemos que usar la función [`np.random.randint`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.randint.html), que admite un argumento obligatorio y dos opcionales:

  * Si se llama con un argumento, `np.random.randint(a)` devuelve una muestra de la distribución uniforme discreta en $[0, a)$.
  * Si se llama con dos argumentos, `np.random.randint(a, b)` devuelve una muestra de la distribución uniforme discreta en $[a, b)$.
  * Si se llama con tres argumentos, `np.random.randint(a, b, size)` devuelve un array de muestras en $[a, b)$ y de tamaño `size`.

    :::python
    In [33]: np.random.randint(10)
    Out[33]: 3
    In [34]: np.random.randint(10)
    Out[34]: 5
    In [35]: np.random.randint(100, 200)
    Out[35]: 136
    In [36]: np.random.randint(100, 200)
    Out[36]: 187
    In [37]: np.random.randint(100, 200)
    Out[37]: 170
    In [38]: np.random.randint(100, 1000, (3, 2))
    Out[38]:
    array([[572, 700],
           [496, 414],
           [805, 586]])
    In [39]: np.random.randint(100, 1000, (3, 2))
    Out[39]:
    array([[651, 187],
           [274, 700],
           [949, 777]])

### Mezclas y elecciones aleatorias

NumPy también nos permite, dado un array de datos ya existente, mezclarlo de manera aleatoria (como barajar un mazo de cartas) o escoger un elemento al azar.

La función [`np.random.choice`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.choice.html) (nueva en NumPy 1.7.0) recibe cuatro argumentos (uno obligatorio y tres opcionales) que dan bastante juego:

  * El argumento `a` es o bien el array del que vamos a extraer los elementos o un entero. En este último caso se utiliza `np.arange(a)`.
  * El argumento `size` es un entero o tupla de enteros y es el tamaño del array de salida. Por defecto es `None` ([y no 1 como indica la cadena de documentación de la función](https://github.com/numpy/numpy/commit/acf7421128b9d974d5153759650b7aaee3c2efec#commitcomment-2382830)), y en este caso se devuelve un escalar.
  * El argumento `replace` es un valor booleano que indica si se toma la muestra con reposición o sin ella, esto es, si se pueden repetir los elementos o no. Si se escoge muestra sin reposición, evidentemente la salida no puede tener más elementos que el array de partida. Por defecto se toma con reposición (`True`)
  * El argumento `p` es una lista de las probabilidades asociadas a cada elemento. Por defecto se asume que todos tienen la misma probabilidad de aparecer.

Vamos a ver algunos ejemplos:

    :::python
    In [16]: a = np.arange(10)
    In [17]: np.random.choice(a)  # Entero aleatorio entre 0 y 9
    Out[17]: 2
    In [18]: np.random.choice(10)  # Exactamente lo mismo
    Out[18]: 6
    In [19]: np.random.choice(a, 3)  # Tres enteros
    Out[19]: array([3, 4, 2])
    In [20]: np.random.choice(a, (2, 2))
    Out[20]:
    array([[4, 6],
           [0, 6]])
    In [21]: np.random.choice(a, 10, replace=True)  # Por defecto
    Out[21]: array([8, 1, 5, 2, 4, 3, 7, 4, 0, 1])
    In [22]: np.random.choice(a, 10, replace=False)  # Simplemente una ordenación
    Out[22]: array([4, 1, 8, 3, 2, 9, 7, 5, 0, 6])
    In [23]: np.random.choice(a, 12, replace=False)  # Esto falla
    ---------------------------------------------------------------------------
    ValueError                                Traceback (most recent call last)
     in ()
    ----&gt; 1 np.random.choice(a, 12, replace=False)  # Esto falla
    /home/juanlu/.local/lib/python3.3/site-packages/numpy/random/mtrand.cpython-33m.so in mtrand.RandomState.choice (numpy/random/mtrand/mtrand.c:7513)()
    ValueError: Cannot take a larger sample than population when 'replace=False'
    In [24]: np.random.choice(a, 20, replace=True)  # Pero esto no
    Out[24]: array([9, 7, 4, 3, 2, 2, 7, 4, 7, 3, 3, 8, 8, 5, 9, 4, 6, 7, 8, 9])
    In [33]: p = np.zeros_like(a, dtype=float)
    In [34]: p[0] = 0.9
    In [35]: p[1] = 0.1
    In [36]: p
    Out[36]: array([ 0.9,  0.1,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ])
    In [37]: np.random.choice(a, 20, p=p)  # El 0 es mucho más probable
    Out[37]: array([0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0])

Por último en este apartado tenemos dos funciones que reordenan de manera aleatoria los elementos de un array: [`shuffle`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.shuffle.html) y [`permutation`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.permutation.html). La primera lo hace _in situ_, y la segunda devuelve el array desordenado:

    :::python
    In [38]: a
    Out[38]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    In [39]: np.random.permutation(a)  # Se devuelve una copia desordenada
    Out[39]: array([4, 1, 9, 0, 5, 2, 8, 6, 3, 7])
    In [40]: np.random.shuffle(a)  # In situ, no se devuelve nada
    In [41]: a  # Pero el array ha cambiado
    Out[41]: array([6, 1, 4, 2, 3, 5, 9, 0, 8, 7])

## Distribuciones estadísticas

Hasta ahora hemos manejado básicamente distribuciones uniformes, pero NumPy incluye otras distribuciones estadísticas continuas y SciPy amplía con muchas más, añadiendo también distribuciones discretas. Estas se encuentran en el paquete [`scipy.stats`](http://docs.scipy.org/doc/scipy/reference/stats.html). Usando las distribuciones de NumPy:

    :::python
    In [129]: np.random.poisson()  # Muestra de una distribución de Poisson con lambda=1
    Out[129]: 1
    In [130]: np.random.standard_normal()  # Normal estándar
    Out[130]: -0.10313902268607797
    In [132]: np.random.randn()  # Lo mismo que lo anterior
    Out[132]: -1.425703117101493

Date cuenta de que se proporciona la función [`randn`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.random.randn.html) como atajo a la normal estándar, por ser enormemente común.

Si se utiliza SciPy, hay que llamar a la función [`rvs`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.rvs.html) de la distribución:

    :::python
    In [138]: sp.stats.chi(2).rvs()  # Chi de dos grados de libertad
    Out[138]: 0.52309303659860873
    In [139]: sp.stats.expon(1.5).rvs()  # Exponencial de lambda = 1.5
    Out[139]: 2.8403282013254163

Si quieres más información o utilizar el resto de funciones estadísticas que ofrece SciPy, puedes leer nuestro artículo sobre [estadística en Python con SciPy](http://pybonacci.org/2012/04/21/estadistica-en-python-con-scipy/).

Ahora ya puedes hacer sorteos de lotería, bonitas simulaciones de Monte Carlo o explorar juegos de azar con Python. Y tú, **¿para qué utilizarías números aleatorios?**