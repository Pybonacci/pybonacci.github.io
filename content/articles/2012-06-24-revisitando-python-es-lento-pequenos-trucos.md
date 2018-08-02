---
title: Revisitando &#8216;python es lento&#8217;: pequeños trucos
date: 2012-06-24T19:24:39+00:00
author: Kiko Correoso
slug: revisitando-python-es-lento-pequenos-trucos
tags: numexpr, numpy, performance, python, rendimiento

Hace un tiempo [David os habló sobre acelerar vuestros cálculos hechos con python (si no los has leído aún a qué esperas :-)).](https://www.pybonacci.org/2012/05/01/python-es-lento/) Hoy vamos a revisitar sus textos enfocándonos en pequeñas cositas que podemos hacer sin tener que usar algo que no sea programar en python.

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y numexpr 1.4.2]**

[DISCLAIMER: Por favor, no hagáis caso a los tiempos absolutos. Estos valores dependen mucho de lo que uséis para hacer los cálculos (32bits o 64bits, Sistema operativo, procesador,...). He usado distintas máquinas para hacer las pruebas y los resultados están mezclados. Fijaos mejor en las conclusiones.]

En todo momento supondremos que se ha iniciado la sesión en ipython y se ha hecho

    :::python
    import numpy as np
    import numexpr as ne

> **_Intenta usar (casi) siempre las funciones de numpy en lugar de las de python_**

El siguiente cálculo es 112 veces más rápido usando numpy.min en lugar de usar la función min de python para este ejemplo concreto y en mi portátil.

    :::python
    x = np.random.randn(1000000)
    timeit np.min(x)
    timeit min(x)

Sin embargo puede suceder que, dependiendo como hagamos el cálculo, no siempre resulte más rápido usar la función en numpy que la función en python. Lo mismo, vemos un ejemplo concreto y no generalizable en mi portátil:

    :::python
    x = np.arange(100000)  # Creamos un numpy array de enteros (int32)
    xl = range(100000)  # Creamos una lista de enteros (int)
    timeit np.sum(x)  # 10000 loops, best of 3: 115 us per loop
    timeit np.sum(xl)  # 10 loops, best of 3: 23.1 ms per loop
    timeit sum(x)  # 10 loops, best of 3: 76.5 ms per loop
    timeit sum(xl)  # 100 loops, best of 3: 6.32 ms per loop

Si hago la suma sobre un numpy array es más rápido usando la suma de numpy, si hago la suma sobre una lista, es más rápida la suma de python. Es decir, con excepciones, numpy funciona más rápido sobre numpy arrays y python funciona más rápido sobre listas. Numpy sobre un numpy array es, en este caso concreto en el portátil, 55 veces más rápido que la suma de python sobre una lista.

Veamos otro ejemplo similar para ver si os convence (ahora estoy usando otro PC):

    :::python
    import math
    x = np.arange(1000000)  # Creamos un numpy array de enteros (int32)
    xl = range(1000000)  # Creamos una lista de enteros (int)
    kk = []
    timeit [kk.append(math.sin(dato)) for dato in xl]  # 10 loops, best of 3: 184 ms per loop
    kk = []
    timeit [kk.append(math.sin(dato)) for dato in x]  # 1 loops, best of 3: 251 ms per loop
    timeit kk = np.sin(xl)  # 10 loops, best of 3: 117 ms per loop
    timeit kk = np.sin(x)  # 10 loops, best of 3: 31.4 ms per loop

Si vuestros cálculos se hacen sobre vectores/matrices más pequeños puede que los resultados sean diferentes pero en general se cumple lo anterior.

> _**Sí o sí usa numexpr cuando hagas cálculos sobre [funciones trascendentes o las operaciones que permite numexpr](http://code.google.com/p/numexpr/wiki/UsersGuide#Supported_operators) (y/o tienes varios núcleos en el/los procesador/es**_)

Veamos algo un poco marciano:

    :::python
    x = np.random.randn(1000000)
    timeit y = x**4  # 10 loops, best of 3: 76.1 ms per loop
    timeit y = x * x * x * x  # 100 loops, best of 3: 4.32 ms per loop

¿Y esto por qué sucede así?. En el primer caso (_y = x**4_) numpy usa la función numpy.power para hacer el cálculo. Esta es una función trascendente y no puede ser evaluada en un solo ciclo de procesador. Si vais a la explicación en la wikipedia en versión inglesa entenderéis mejor lo que es una [función trascendente](http://en.wikipedia.org/wiki/Transcendental_function). Además de la explicación de la wikipedia os recomiendo que le echéis un ojo a este [video](http://www.youtube.com/watch?v=J3-oN_TulTg) donde uno de los desarrolladores de numexpr y creador de PyTables, Francesc Alted, habla sobre el tema.

Si repetimos el cálculo anterior usando numexpr, que además permite, en ciertos casos, optimizar el uso de memoria, obtenemos lo siguiente:

    :::python
    x = np.random.randn(1000000)
    ne.set_num_threads(1)  # Hacemos que solo use un thread para poder comparar iguales con respecto a lo anterior
    timeit y = ne.evaluate('x**4')  # 1000 loops, best of 3: 1.57 ms per loop

Para este caso concreto es 48.5 veces más rápido que numpy puro y 2.75 veces más rápido que el python 'optimizado' anterior (recordad que el numpy 'optimizado' no usa la función numpy.power).

_(*) Si alguien se anima a explicar más detalladamente el tema de las funciones trascendentes y su cálculo lo puede hacer en los comentarios y lo podemos incluir en el post._

Para rizar el rizo, imaginad que tenéis un buen cacharro en casa (en este caso uso un intel i7 2600 que me permite usar hasta 8 threads). Con numexpr podéis hacer uso de la paralelización del cálculo y obtener aún más ganancia. Veamos un cálculo donde se pueda ver esto de forma muy clara:

    :::python
    x = np.random.randn(1000000)
    y = np.random.randn(1000000)
    z = np.random.randn(1000000)
    timeit resultado = x**3 + 2. * y**2 - 3. * x / z  # 10 loops, best of 3: 92.2 ms per loop
    ne.set_num_threads(1)  # Hacemos que solo use un thread para poder comparar iguales con respecto a lo anterior
    timeit resultado = ne.evaluate('x**3 + 2. * y**2 - 3. * x / z')  # 100 loops, best of 3: 10.6 ms per loop
    ne.set_num_threads(8)  # Hacemos que use todos los threads
    timeit resultado = ne.evaluate('x**3 + 2. * y**2 - 3. * x / z')  # 100 loops, best of 3: 2.6 ms per loop

Sin hacer gran cosa y sin salir de python obtenemos una ganancia sobre numpy de 35.5x (recordad, como siempre, el resultado es para este caso concreto). Haced la prueba usando solo python (sin numpy) para hacer el mismo cálculo y os asombrará el tiempo que os sale.

> **_Otras pequeñas chorraditas que podemos hacer_**

Cuando creamos un numpy array que vamos a rellenar con valores en cálculos posteriores se suele usar numpy.zeros o numpy.ones. Si sabéis que todos los elementos serán rellenados podéis usar np.empty que siempre será más veloz.

    :::python
    timeit np.zeros((10000,10000))  # 1 loops, best of 3: 266 ms per loop
    timeit np.ones((10000,10000))  # 1 loops, best of 3: 226 ms per loop
    timeit np.empty((10000,10000))  # 100000 loops, best of 3: 5.85 us per loop

La tercera opción es ¿¿40.000?? veces más rápida.

_(*) Si alguien sabe porque numpy.zeros tarda más que numpy.ones que lo explique en los comentarios que me he quedado con la duda_.

Numpy.where es una función que uso mucho pero que es extremadamente lenta en algunos casos. Para evitar su uso podéis intentar encontrar alternativas.

Ejemplo, queremos buscar los índices donde se encuentra el máximo de nuestro numpy array. Con numpy.where haríamos lo siguiente:

    :::python
    x = np.random.randn(1000000).reshape(1000,1000)
    timeit np.where(x == x.max())  # 100 loops, best of 3: 8 ms per loop
    timeit divmod(x.argmax(), x.shape[1])  # 1000 loops, best of 3: 638 us per loop

Este es un ejemplo donde python puede ser más rápido que numpy. Este ejemplo lo he sacado de [esta página](https://scipy.github.io/old-wiki/pages/PerformanceTips.html) donde he cambiado el ejemplo del mínimo por la localización del máximo para que no me acusen de plagio :-). En esa página/enlace tenéis más ejemplos de como optimizar un poco vuestro código.

Imaginad ahora que queréis hacer operaciones sobre una serie de valores del array que cumplen unas ciertas condiciones. Esto se puede hacer de forma más eficiente y legible sin usar numpy.where de la siguiente forma:

Vamos a buscar todos los elementos que estén entre 0 y 1 y vamos a asignarles el valor -999.

    :::python
    x = np.random.randn(1000000)
    x[(x &gt; 0) & (x &lt; 1)] = -999

Vamos a buscar todos los elementos que estén por debajo de 0 o por encima de 2 y los vamos a dividir por 10 (por decir algo):

    :::python
    x = np.random.randn(1000000)
    x[(x &lt; 0) | (x &gt; 2)] = x / 10.

Espero que alguna de estas cosita os resulte útil en vuestro día a día. Si veis algún error en el texto anterior os agradecemos que nos lo hagáis saber para poder corregirlo y mejorar. Si tienes pequeñas recetas que usas y que están relacionadas con lo anterior, ponlo en los comentarios para  aprendamos y para que lo incluyamos como parte del texto.
