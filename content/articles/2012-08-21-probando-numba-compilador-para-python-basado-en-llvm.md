---
title: Probando numba: compilador para Python basado en LLVM
date: 2012-08-21T15:28:03+00:00
author: Juan Luis Cano
slug: probando-numba-compilador-para-python-basado-en-llvm
tags: cython, numba, python, rendimiento

## Introducción

Hace unos días [Travis E. Oliphant](http://continuum.io/our-team.html#travis), creador de NumPy e importante contribuidor de SciPy entre otras muchas cosas, anunciaba [en su Twitter](https://twitter.com/teoliphant/status/235789560678858752) y [en su blog](http://technicaldiscovery.blogspot.com.es/2012/08/numba-and-llvmpy.html) la liberación de [numba 0.1](http://numba.pydata.org/), un proyecto que **pretende ser el mejor compilador orientado a arrays** del mundo, como puedes ver en la presentación que dio en la conferencia SciPy 2012 celebrada en Austin, Texas ([vídeo](http://youtu.be/WYi1cymszqY) y [diapositivas](http://www.slideshare.net/teoliphant/numba)).

<blockquote class="twitter-tweet" width="550">
  <p>
    Just released Numba 0.1. Thanks Jon Riehl from Resilient Science for all the hard work. Binaries to follow. <a href="http://t.co/o80rn7By">http://t.co/o80rn7By</a>
  </p>
  
  <p>
    &mdash; Travis Oliphant (@teoliphant) <a href="https://twitter.com/teoliphant/statuses/235789560678858752">August 15, 2012</a>
  </p>
</blockquote>



Aunque el proyecto está en una fase bastante precaria todavía y hay unos cuantos fallos pendientes de solucionar todavía, hemos hecho algunas pruebas y los resultados son impresionantes. Vamos a hablar un poco de numba y a explicar cómo puedes probarlo tú mismo.

<!--more-->

## Motivación

Ya hemos hablado en dos ocasiones sobre la lentitud de Python y hemos dado algunas soluciones para evitarla, bien [utilizando bibliotecas que aceleren el código escrito en Python](http://pybonacci.org/2012/05/01/python-es-lento/ "Python es lento") o [teniendo en cuenta pequeños trucos](http://pybonacci.org/2012/06/24/revisitando-python-es-lento-pequenos-trucos/ "Revisitando ‘python es lento’: pequeños trucos") a la hora de escribir nuestros programas. En la charla que hemos mencionado antes, Oliphant menciona algunas de ellas, concretamente **PyPy** y **Cython** (David ya habló de las dos en su artículo). Estas dos soluciones tienen sus inconvenientes:

  * PyPy **no** funciona con CPython, la implementación principal de Python. Esto significa que las extensiones escritas para Python no se pueden utilizar fácilmente en PyPy, y hay una que es fundamental para nosotros: NumPy.
  * Cython supone otra sintaxis que hay que aprender, y si se quiere optimizar mucho se va perdiendo la legibilidad de Python poco a poco.

Con **numba**, tenemos una forma de acelerar código escrito en Python que:

  * Está especialmente pensada y optimizada para **códigos numéricos**,
  * Entiende los tipos de **NumPy**, su API y sus estructuras de datos,
  * **No requiere aprender una nueva sintaxis**, conservando así la belleza y legibilidad de Python, y
  * Produce programas con **velocidades cercanas a las de C**.



¿Y cómo se consigue esto? numba genera código [LLVM](http://es.wikipedia.org/wiki/LLVM) y crea un wrapper para llamarlo desde Python. De esta forma conseguimos un compilador JIT para Python, en la línea de otros proyectos como el abandonado Unladen Swallow.

Interesante, ¿no? Si quieres probar numba en tu propio ordenador, sigue leyendo.

## Instalación

Para no complicarnos la vida, vamos a dar las instrucciones de instalación para Linux. Parece ser que <del datetime="2012-08-21T19:29:56+00:00">Windows no está soportado</del> <ins datetime="2012-08-21T19:31:50+00:00">en Windows hay un par de problemas (<a href="https://github.com/numba/numba/issues/27">#27</a>, <a href="https://github.com/numba/numba/issues/28">#28</a>)</ins>, y en cuanto a Mac OS X no tengo ni idea.

En la web de numba tienes los [pasos que hay que seguir](http://numba.pydata.org/#quickstart) para instalarlo. Los requisitos son:

  1. [llvm 3.1](http://www.llvm.org/) compilado con las opciones `--enable-pic` y `--disable-libffi`. La segunda opción soluciona un bug que afecta a algunos, incluido yo.
  2. [llvm-py](https://github.com/llvmpy/llvmpy). Con la versión del repositorio ha funcionado.

En primer lugar, descarga y extrae las fuentes de llvm 3.1 y ejecuta los siguientes comandos para compilar la biblioteca:

    :::bash
    $ ./configure --enable-pic --disable-libffi
    $ make
    $ make install

A continuación, clona el repositorio de llvm-py e instala la biblioteca:

    :::bash
    $ git clone https://github.com/llvmpy/llvmpy.git
    $ cd llvmpy
    $ python setup.py install

Por último, ya puedes instalar numba directamente del repositorio también:

    :::bash
    $ git clone https://github.com/numba/numba.git
    $ cd numba
    $ git submodule init
    $ git submodule update
    $ python setup.py install

En principio estas instrucciones funcionan en el caso más general, pero si tienes algún problema concreto durante el proceso o más adelante probando los ejemplos, dínoslo en los comentarios.

## Ejemplos

Las fuentes de numba contienen algunos ejemplos y benchmarks que puedes probar para evaluar las capacidades de la biblioteca. Además, [Alex Wiltschko](http://twitter.com/awiltsch) ha estado haciendo pruebas e informando de algunos fallos y nos ha dejado que hagamos uso de los programas que ha escrito (_thanks Alex!_).

Las capacidades de numba se aprecian mejor si se aplican con programas con muchos bucles anidados, como algoritmos de procesamiento de imágenes. De todos modos, para empezar vamos a probar un ejemplo sencillo, que puedes encontrar en <https://github.com/numba/numba/blob/master/examples/sum.py>.

**Nota**: En el momento de escribir el artículo se imprime todo el código LLVM creado por numba cuando se aplica a una función. Para evitar este comportamiento, puedes ejecutar los ejemplos añadiendo la opción `-O`, que activa optimizaciones básicas.

El código del ejemplo es el siguiente:

    :::python
    from numba import d
    from numba.decorators import jit as jit
    def sum2d(arr):
        M, N = arr.shape
        result = 0.0
        for i in range(M):
            for j in range(N):
                result += arr[i,j]
        return result
    csum2d = jit(ret_type=d, arg_types=[d[:,:]])(sum2d)
    from numpy import random
    arr = random.randn(100,100)
    import time
    start = time.time()
    res = sum2d(arr)
    duration = time.time() - start
    print "Result from python is %s in %s (msec)" % (res, duration*1000)
    start = time.time()
    res = csum2d(arr)
    duration2 = time.time() - start
    print "Result from compiled is %s in %s (msec)" % (res, duration2*1000)
    print "Speed up is %s" % (duration / duration2)

Como se puede ver, en la línea 12 se aplica la función `jit` (que también funciona como decorador, como ya veremos) al pequeño programa que hemos escrito para sumar los elementos de una matriz. El argumento `arg_types` indica que a la función sum2d se le va a pasar un array de NumPy de dos dimensiones. Esto viene a ser como una declaración de tipos.

Comprobemos los resultados:

    :::bash
    $ python -O sum.py
    Result from python is -72.8742506632 in 4.33301925659 (msec)
    Result from compiled is -72.8742506632 in 0.028133392334 (msec)
    Speed up is 154.016949153

Conseguimos **un aumento de 150x**, solamente añadiendo una línea.

Probemos otro de los ejemplos, <https://github.com/numba/numba/blob/master/examples/example.py>. En este caso se trata de comparar numba con una función de SciPy, y podemos ver cómo se utiliza el decorador:

    :::python
    @jit(arg_types=[int32[:,:], int32[:,:]], ret_type=int32[:,:])
    def filter2d(image, filt):
        M, N = image.shape
        Mf, Nf = filt.shape
        Mf2 = Mf // 2
        Nf2 = Nf // 2
        result = numpy.zeros_like(image)
        for i in range(Mf2, M - Mf2):
            for j in range(Nf2, N - Nf2):
                num = 0.0
                for ii in range(Mf):
                    for jj in range(Nf):
                        num += (filt[Mf-1-ii, Nf-1-jj] * image[i-Mf2+ii, j-Nf2+jj])
                result[i, j] = num
        return result

Ahora estamos indicando que la función requiere dos arrays de enteros. Nótese que tenemos cuatro (4) bucles anidados. Si ahora probamos el ejemplo:

    :::bash
    $ python -O example.py
    Time for LLVM code = 0.028516
    Time for convolve = 0.041848

Aquí hemos conseguido una ganancia de **1.47x**. Nótese que la versión de SciPy está **escrita en C**.

Por último, vamos a ver uno de los experimentos llevados a cabo por Alex Wiltschko creado a raíz de [un artículo sobre Cython](http://jakevdp.github.com/blog/2012/08/08/memoryview-benchmarks). Podemos ver los resultados del experimento en el [IPython Notebook Viewer](http://nbviewer.ipython.org/), una web que utiliza la nueva interfaz web de IPython en la que podemos compartir notebooks.

El notebook del experimento está en <http://nbviewer.ipython.org/3362653>, y aunque según los comentarios hay resultados dispares, en el ordenador de Wiltschko la versión con numba fue **2 veces más rápida** que la mejr versión de Cython. Si ahora contamos el número de líneas:

  * Python: 17 líneas.
  * Cython + memviews (sin slicing): 39 líneas.
  * numba: 13 líneas.

Aun considerando que las velocidades sean del mismo orden, es una mejora **espectacular**.

## Comentarios finales

Estos resultados son bastante impresionantes, pero como hemos dicho más arriba la biblioteca está todavía en pruebas y _aún no tiene documentación_. Por ejemplo, _dentro_ de las funciones que compilemos con `jit` [no funcionan la mayoría de las funciones de NumPy](https://github.com/numba/numba/issues/22#issuecomment-7832739), como `array.zeros`.

Sin embargo, numba es un notable paso hacia adelante y, si no se queda estancada, puede que abra un nuevo camino lleno de posibilidades en la popularización de Python en entornos científicos.

Nosotros estamos muy entusiasmados con numba, ¿y tú? 🙂