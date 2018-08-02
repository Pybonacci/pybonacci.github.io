---
title: Python es lento
date: 2012-05-01T02:11:32+00:00
author: Davidmh
slug: python-es-lento

La programación científica consiste, en su mayor parte, en cálculos numéricos intensos. CPU en estado puro. Un lenguaje interpretado es, por construcción, más lento que su homólogo compilado, por lo que puede parecer un contrasentido usar Python para aplicaciones «pesadas».  Estamos perdiendo el tiempo, ¿o no?

Muchos programas científicos se ejecutan sólo una vez, son un cálculo concreto que no hará falta repetir. La mayor parte del tiempo del cálculo no es la ejecución del programa, sino escribirlo, trabajo de un humano. Aquí es donde entran las bondades de Python: es sencillo, rápido de escribir, y potente como el que más. Y, por lo sencillo que eso, aunque sea de naturaleza lenta (o precisamente por eso), se han creado muchas herramientas para mejorar su eficiencia de formas elegantes y pythónicas.

Muchas críticas sobre la lentitud de Python adolecen de alguno de estos problemas:

  * _Benchmarks_ irreales o incorrectos: ¿quién necesita un programa para imprimir [el primer millón de números naturales](http://theunixgeek.blogspot.com.es/2008/09/c-vs-python-speed.html)?
  * [Desconocimiento del lenguaje.](http://stackoverflow.com/questions/6964392/speed-comparison-with-project-euler-c-vs-python-vs-erlang-vs-haskell) A veces hay formas mejores de hacer las cosas, más sencillas y óptimas.
  * Se limitan a la biblioteca estándar, que se queda coja para el cálculo numérico (como veremos más adelante).
  * No tienen en cuenta el tiempo necesario para escribirlo y depurarlo. Cuanto más largo sea el programa, más difícil será encontrar los problemas o añadirle nuevas funcionalidades (tiempo del programador).
  * Por lo tanto, usar un lenguaje de más alto nivel permite, a igualdad de inteligencia, tiempo y habilidad, crear un programa potencialmente más complejo y eficiente.
  * No son guays (pero nosotros sí).<!--more-->

En este artículo pretendo hacer un repaso no exhaustivo y no muy riguroso de las principales formas de acelerar código Python para un científico. La mayoría requieren la instalación de bibliotecas específicas, y algunas de ellas, una configuración cuidadosa, por lo que no todas son adecuadas para distribuir un producto al público general. Vamos allá:

## 

## Optimiza, que algo queda.

Antes de empezar a pensar en optimizar debemos saber _qué_ optimizar. Si tenemos una rutina simple, es obvio, pero si el programa es complejo, no es trivial ver por dónde atacarlo. Podemos tirarnos horas tratando de mejorar el tiempo de una función que, de varias horas de simulación, sólo se lleva cinco minutos, mientras que cambiando una línea, podemos obtener una mejora del 33% (historia real).

Por lo tanto, antes de meter la zarpa de optimización debemos saber dónde se está empleando nuestro tiempo. Eso se hace con sistemas de _profiling_ ([véanse](http://docs.python.org/library/profile.html) [algunos](https://code.google.com/p/jrfonseca/wiki/Gprof2Dot#Examples) [ejemplos](http://wiki.jrfonseca.googlecode.com/git/gprof2dot.png)). Otro día trataremos este tema.

## 

## **Conociendo el lenguaje: _list comprehension_**

Como decía al principio, conocer el lenguaje es importante a la hora de escribir código eficiente, y Python guarda algunas sorpresas. Por ejemplo, sacar cosas por pantalla es lento, no imprimas todo lo que va haciendo, será más rápido (y más útil) imprimir sólo una docena de marcas clave, para saber por dónde va.

Otro de los pozos de tiempo son los bucles. La mayoría de las veces son inevitables, pero a veces hay opciones más rápidas. Imagina que queremos construir una lista resultado de aplicar una función a todos los elementos de una lista. Una forma obvia de hacerlo es:

    :::python
    lis2=[]
    for element in lis:
       lis2.append(f(element))

Pero la opción idiomática, usando list comprehensions, es:

    :::python
    # Una list comprehension básica:
    lis2=[f(element) for element in lis]

O incluso, restringiendo el dominio:

    :::python
    # Sólo a los elementos positivos.
    lis2=[f(element) for element in lis if element&gt;0]

Que es substancialmente más rápido.

<p style="text-align:right;">
  # Sugerencia avanzada: los comandos map y filter.
</p>

## 

## Optimización automágica: Psyco

[Psyco](http://psyco.sourceforge.net/) es un compilador JIT (_just in time_, «en tiempo real»), que optimiza en tiempo de ejecución el código.

> Cuando el compilador JIT detecta un bucle [función] en el código [...] se le hace un seguimiento.  Cuando esa función sea ejecutada, el intérprete la inspecciona y registra todas las instrucciones ejecutadas.
> 
> Cuando ha finalizado, el seguimiento se detiene y el registro es mandado a un optimizador, y de ahí a un ensamblador que genera código máquina optimizado. La próxima vez que se ejecute esa pieza de código, se usará esta versión mejorada.
> 
> (El código) depende de varias suposiciones sobre el código que van incluidas en la versión optimizada. Si alguna de esas suposiciones falla, la ejecución pasa de nuevo a la versión original.
> 
> <p style="text-align:right;">
>   <em>(Extraído del blog de <a href="http://www.huyng.com/posts/so-thats-how-tracing-jits-work/">Huy Nguyen </a>citando a su vez <a href="http://morepypy.blogspot.com.es/2011/04/tutorial-part-2-adding-jit.html">el blog de PyPy</a>)</em>
> </p>

El uso no podría ser más sencillo. Símplemente añade al principio de tu programa:

    :::python
    import psyco
    psyco.full()

Y obtiene una aceleración de un factor 2-3, que puede llegar hasta un factor 10 para el cálculo numérico puro. La gran ventaja de Psyco es que no requiere hacer modificaciones específicas en el código: añádelo y funciona. En casi todas partes. Y ya.

Pero no es siempre útil. Por ejemplo, cuando hacemos uso intensivo de NumPy, el código ya está optimizado, así que Psyco poco puede rascar, y su único efecto es ralentizar el programa (en cantidades inapreciables, eso sí). Además, tras años en los que sólo ha recibido mantenimiento básico (nadie llegó a portarlo a Python 2.7 ni a las versiones de 64 bits), desde el 12 de marzo está definitivamente muerto.  Hubo en algún momento una distribución de la Psyco 2, prometiendo una página web y nuevas características, pero nunca más se supo, y hace que otras bibliotecas como Matplotlib dejen de funcionar. Es mejor quedarse con la vieja versión 1.7.

Espera, ¿he dicho NumPy? ¿qué es NumPy?

## 

## NumPy y SciPy

[La Biblia](http://scipy.org/) cuando hablamos de cálculo numérico en Python. Su mayor contribución es una nueva estructura de datos: el array. Una lista (multidimensional) homogénea, en la que todos sus elementos han de ser del mismo tipo: entero, decimal en precisión arbitraria, complejo... y sobre la que se puede aplicar una gran cantidad de funciones. Veamos un ejemplo: ¿cuál es la suma de las raíces cuadradas de los diez primeros números y los senos de esos mismos números?

    :::python
    # Implementación estándar
    import psyco
    psyco.full()
    import math
    numbers=range(10)
    result=[math.sqrt(num)+math.sin(num) for num in numbers]

&nbsp;

    :::python
    # Implementación con NumPy
    import numpy as np
    numbers=np.range(10)
    result=np.sqrt(numbers)+np.sin(numbers)

Como vemos, ya no hace falta ir elemento a elemento, sino que le podemos dar la lista completa, y él solo hace la iteración. Esto no es sólo una cuestión de conveniencia, sino que también permite incrementar la velocidad de ejecución. En algunas operaciones, como las matriciales, esto es incluso más interesante, ya que de forma completamente transparente y automática, ejecuta el código en paralelo, mandando cada número a un núcleo del procesador, ahorrando mucho tiempo.

Y, por supuesto, NumPy y SciPy tienen muchísimas funciones muy potentes, como rutinas para integrar, interpolaciones, regresiones, funciones de Bessel, convoluciones, transformadas diversas... Prácticamente toda la matemática genérica que uno puede necesitar.

¿Cómo funciona? Np y Sc son una gran interfaz para bibliotecas matemáticas en C, por lo que, tu código Python no hace más que llamar la ejecución de código C compilado.

## 

## Paralelizando: Numexpr

La paralelización es una buena forma de acelerar la ejecución de un programa, siempre que sea suficientemente separable. El caso extremo son los problemas vergonzosamente paralelizables, en los que podemos dividir el espacio de parámetros a estudiar en suficientes compartimentos estancos. En este caso, la paralelización es tan fácil como lanzar tantos programas como núcleos tengamos, cada uno estudiando una parte. Ejemplo: colisiones de un acelerador de partículas, cada evento es completamente independiente de los demás.

Otras veces no tenemos tanta suerte y sólo podemos paralelizar algunas partes de nuestro programa. Python ofrece los módulos _threading_ y _multiprocessing_, pero su uso es más sutil y complicado de lo que quiero tratar en este artículo.

No obstante, no está todo perdido. Si queremos aplicar funciones básicas sobre grandes conjuntos de números y NumPy se nos queda corto, podemos usar [Numexpr](https://code.google.com/p/numexpr/). Nuestro viejo código quedaría:

    :::python
    # Implementación con NumPy y Numexpr
    import numpy as np
    import numexpr as ne
    numbers=np.range(10)
    result=ne.evaluate('sqrt(numbers)+sin(numbers)') # Nótese que va como texto

Numexpr tiene varias estrategias para acelerar el código. En primer lugar, cuando NumPy ejecuta el código, primero calcula las raíces y las guarda en memoria, después los senos y los guarda en memoria, y por último, los suma ambos y guarda el resultado final en memoria. Esto supone triplicar la memoria necesaria, y por tanto, el tráfico de datos entre la CPU y la RAM.

Podemos ahorrar memoria haciendo la cuenta elemento a elemento,  calculando la raíz y el seno del primero y sumarlos, etc. Esto fuerza a Python a comprobar qué tipo de dato es en cada momento para saber cómo hacer la cuenta, y esto ha de hacerse cada vez. Numexpr, en cambio, divide la operación en trozos manejables, que no castiguen mucho la memoria, y que eviten comprobaciones redundantes.

Además, incluye su propio compilador JIT, que genera código muy eficiente, y además intenta usar varios núcleos allí donde NumPy no sabe. Para tamaños suficientemente grandes de datos, podemos llegar a alcanzar la velocidad límite que da la memoria del ordenador, ¡y sin haber escrito una sola línea fuera de Python!

# Magia arcana: _blitz_

Llegamos a un problema en el que nada de lo anterior ha sido suficiente, sigue siendo demasiado lento. En realidad, sabemos que la causa son sólo unas pocas líneas de código... es la hora de la magia misteriosa.

_weave_ es un módulo dentro de NumPy para comunicar Python y C. Una de sus funciones es _[blitz](http://www.scipy.org/PerformancePython#head-cafc55bbf8fd74071b2c2ebcfb6f24ed1989d540)_, que toma una línea de Python, la traduce de forma transparente a C, y cada vez que la llames se ejecutará esta versión optimizada. En hacer esta primera conversión necesita entorno a un segundo, pero consigue velocidades generalmente superiores a todas las opciones anteriores. Ya no es _bytecode_ como Numexpr o Psyco, o una interfaz a C como NumPy, sino tu propia función escrita directamente en C y completamente compilada y optimizada.

Nota: aunque en Linux y Mac funciona según se instala, en Windows no he sido capaz de hacerlo funcionar nunca.

# Rindiéndonos al compilador

Está bien, vamos a compilar algo de código.Una opción previa es [Cython](http://cython.org/), una versión del lenguaje Python con declaración de variables opcional (pero recomendada) que puede ser compilada a código C y luego llamado desde Python. La gran ventaja es que este código es plenamente funcional dentro de Python, incluso antes del compilado. Además, soporta arrays de NumPy. Sin embargo, está limitado a tipos estáticos y el proceso de generar el código es un tanto complejo/pesado.

Otro proyecto interesante es [Shedskin](http://shed-skin.blogspot.com.es/). En este caso, toma código Python puro (con algunas restricciones, como el tipado estático) y genera código C++ (ilegible, pero funcional) optimizado. El proyecto parece ser llevado por una sola persona, y va lento, pero el resultado promete interesante y más sencillo que Cython. Como principal desventaja es que no soporta estructuras de NumPy o similares.

Podemos seguir aprovechando _weave_ a través de su función [_inline_](http://www.scipy.org/PerformancePython#head-a3f4dd816378d3ba4cbdd3d23dc98529e8ad7087).  Ésta toma como argumento código C dentro del programa Python. Al igual que blitz, la primera ejecución es la más lenta, pues tiene que compilarlo, pero las siguientes son mucho más rápidas. Su principal inconveniente es que requiere _escribir_ código en otro lenguaje... a menos que uses lo que te ha dado Shedskin, por ejemplo. También puede ser usado como método de inserción de piezas sencillas de código de un colaborador.

Por último, los de la vieja escuela quizá gusten de [F2py](http://www.scipy.org/F2py) para llamar a código Fortran desde Python.

# El futuro: PyPy.

[PyPy](http://pypy.org/) es un intérprete de Python... escrito en Python. Usando un lenguaje de mucho más alto nivel son capaces de optimizar ese mismo lenguaje. Es un gran proyecto aún en desarrollo, en el que se está invirtiendo mucho esfuerzo, pero que ha obtenido algunos [resultados impresionantes](http://speed.pypy.org/). ¡En un _benchmark_ se llega a una aceleración del 98%!

No es una opción todavía porque todavía le faltan muchas cosas, como soporte para bibliotecas externas como NumPy, aunque estamos [cerca](http://morepypy.blogspot.com.es/2012/04/numpy-on-pypy-progress-report.html). Ignoro si hay algún problema más allá de las bibliotecas.