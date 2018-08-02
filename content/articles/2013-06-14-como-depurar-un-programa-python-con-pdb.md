---
title: Cómo depurar un programa Python con pdb
date: 2013-06-14T14:51:42+00:00
author: Juan Luis Cano
slug: como-depurar-un-programa-python-con-pdb
tags: bugs, depuración, pdb, python

## Introducción

En este artículo vamos a explicar cómo **depurar un programa Python** usando el módulo **pdb** de la biblioteca estándar. Si no sabes qué es exactamente depurar un programa o para qué te puede servir, sigue leyendo.

Depurar consiste en seguir el flujo de un programa a medida que se ejecuta, de forma que podemos monitorizar qué es lo que está sucediendo en cada momento. Es un método muy efectivo para encontrar fallos, porque:

  * Permite detener momentáneamente la ejecución del programa usando **puntos de ruptura** (_breakpoints_).
  * Permite examinar en cada momento las variables que se están utilizando (no necesitas llenar tu código de `print`).
  * Permite cambiar el valor de una variable mientras está detenida la ejecución.

Si es la primera vez que oyes hablar de esto, en seguida descubrirás el mundo de posibilidades que ofrece la depuración.

Puedes leer online la [documentación del módulo `pdb`](http://docs.python.org/3.3/library/pdb.html).

_**En esta entrada se ha usado python 3.3.2.**_

<!--more-->

## Primeros pasos

Vamos a utilizar este programa extraído del libro «Dive into Python 3»:

    :::python
    SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
                1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
    def approximate_size(size, a_kilobyte_is_1024_bytes=True):
        '''Convert a file size to human-readable form.
        Keyword arguments:
        size -- file size in bytes
        a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                    if False, use multiples of 1000
        Returns: string
        '''
        if size &lt; 0:
            raise ValueError('number must be non-negative')
        multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
        for suffix in SUFFIXES[multiple]:
            size /= multiple
            if size &lt; multiple:
                return '{0:.1f} {1}'.format(size, suffix)
        raise ValueError('number too large')
    if __name__ == '__main__':
        print(approximate_size(1000000000000, False))
        print(approximate_size(1000000000000))

Que simplemente produce la siguiente salida:

    $ python example.py
    1.0 TB 931.3 GiB

La forma más directa de iniciar el depurador es con la línea:

    $ python -m pdb example.py
    > /home/juanlu/Development/Python/test/pdb/example.py(1)()
    -> SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    (Pdb)

De acuerdo, ¿qué acaba de suceder? Nos encontramos con un intérprete interactivo esperando órdenes, y la línea que empieza por `->` es **la línea donde se encuentra detenida la ejecución** ahora mismo.

Lo primero que observamos es que podemos ejecutar cualquier instrucción Python que queramos:

    (Pdb) 2 * 8
    16
    (Pdb) "Hello".lower()
    'hello'
    (Pdb) import numpy as np; np.sqrt(2)
    1.4142135623730951

Para mostrar una lista de comandos disponibles, escribimos **`help`**. También podemos mostrar la ayuda de cada comando individial:

    (Pdb) help
    Documented commands (type help ):
    ========================================
    EOF    cl         disable  interact  next     return  u          where
    a      clear      display  j         p        retval  unalias
    alias  commands   down     jump      pp       run     undisplay
    args   condition  enable   l         print    rv      unt
    b      cont       exit     list      q        s       until
    break  continue   h        ll        quit     source  up
    bt     d          help     longlist  r        step    w
    c      debug      ignore   n         restart  tbreak  whatis
    Miscellaneous help topics:
    ==========================
    exec  pdb
    (Pdb) help list
    l(ist) [first [,last] | .]
            List source code for the current file.  Without arguments,
            list 11 lines around the current line or continue the previous
            listing.  With . as argument, list 11 lines around the current
            line.  With one argument, list 11 lines starting at that line.
            With two arguments, list the given range; if the second
            argument is less than the first, it is a count.
            The current line in the current frame is indicated by "->".
            If an exception is being debugged, the line where the
            exception was originally raised or propagated is indicated by
            ">>", if it differs from the current line.
    (Pdb)

Como se puede leer, podemos usar el **comando `list`** para examinar el código fuente del archivo que estamos ejecutando. La primera vez que lo ejecutemos sin argumentos mostrará las 11 primeras líneas y marcará con `->` la línea actual, y si seguimos ejecutándolo proseguirá avanzando. Veamos:

    (Pdb) list
      1  ->	SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
      2  	            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB',
      3  	'YiB']}
      4
      5  	def approximate_size(size, a_kilobyte_is_1024_bytes=True):
      6  	    '''Convert a file size to human-readable form.
      7
      8  	    Keyword arguments:
      9  	    size -- file size in bytes
     10  	    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
     11  	                                if False, use multiples of 1000
    (Pdb) list
     12
     13  	    Returns: string
     14
     15  	    '''
     16  	    if size < 0:
     17  	        raise ValueError('number must be non-negative')
     18
     19  	    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
     20  	    for suffix in SUFFIXES[multiple]:
     21  	        size /= multiple
     22  	        if size < multiple:

Ahora, un par de trucos:

  * ¿Has visto que, al mostrar la lista de comandos, había muchos con una sola letra? Lo que sucede es que son **atajos**: por ejemplo, `l` es un atajo para `list`, así que no tienes que escribir el comando entero.
  * Para repetir el último comando introducido, simplemente presiona Enter. Si quieres repetir el comando list tres veces, introduce `l` una vez y Enter otras dos. Más fácil imposible 🙂

Por ejemplo, para mostrar dónde estamos detenidos podemos usar el **comando `where`** o simplemente `w`:

    (Pdb) w
      /usr/lib/python3.3/bdb.py(405)run()
    -> exec(cmd, globals, locals)
      (1)()
    > /home/juanlu/Development/Python/test/pdb/example.py(1)()
    -> SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],

Si queremos cerrar el depurador usaríamos **`quit`**, y si queremos que el programa continue hasta el final, usaremos **`continue`** o `c`:

    (Pdb) c
    1.0 TB
    931.3 GiB
    The program finished and will be restarted
    > /home/juanlu/Development/Python/test/pdb/example.py(1)()
    -> SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    (Pdb)

El programa termina, se reinicia y estamos en el mismo punto que antes. De momento no hemos hecho nada demasiado interesante: comencemos 😉

## Flujo e inspección de variables

Ahora, ¿cómo conseguimos ir avanzando en el flujo de ejecución? Para ello tenemos dos comandos: **`step`** (`s`) y **`next`** (`n`). Ambos ejecutan una línea del programa y avanzan a la siguiente, con la diferencia de que `step` se introduce dentro de las funciones cuando se invoca alguna. Volviendo a nuestro ejemplo:

    The program finished and will be restarted
    > /home/juanlu/Development/Python/test/pdb/example.py(1)()
    -> SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    (Pdb) n
    > /home/juanlu/Development/Python/test/pdb/example.py(2)<module>()
    -> 1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB',
    (Pdb) # Presionamos Enter, lo mismo que ejecutar next otra vez
    > /home/juanlu/Development/Python/test/pdb/example.py(3)<module>()
    (Pdb)
    > /home/juanlu/Development/Python/test/pdb/example.py(5)<module>()
    -> def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    (Pdb)
    > /home/juanlu/Development/Python/test/pdb/example.py(27)<module>()
    -> if __name__ == '__main__':
    (Pdb)
    > /home/juanlu/Development/Python/test/pdb/example.py(28)<module>()
    -> print(approximate_size(1000000000000, False))
    (Pdb) # next ejecuta la línea pero no se introduce en approximate_size
    1.0 TB
    > /home/juanlu/Development/Python/test/pdb/example.py(29)<module>()
    -> print(approximate_size(1000000000000))
    (Pdb)

Hemos ido ejecutando las líneas una a una, y al llegar a la línea `print` y usar `next` se ha ejecutado también y ha saltado a la siguiente. Si para la siguiente línea `print` usamos `step`, nos introduciremos en el cuerpo de la función `approximate_size` y seguiremos depurando desde ahí:

    > /home/juanlu/Development/Python/test/pdb/example.py(29)<module>()
    -> print(approximate_size(1000000000000))
    (Pdb) s
    --Call--
    > /home/juanlu/Development/Python/test/pdb/example.py(5)approximate_size()
    -> def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    (Pdb)
    > /home/juanlu/Development/Python/test/pdb/example.py(16)approximate_size()
    -> if size < 0:
    (Pdb) l .  # Para ver dónde estamos
     11  	                                if False, use multiples of 1000
     12
     13  	    Returns: string
     14
     15  	    '''
     16  ->	    if size < 0:
     17  	        raise ValueError('number must be non-negative')
     18
     19  	    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
     20  	    for suffix in SUFFIXES[multiple]:
     21  	        size /= multiple
    (Pdb)

Estamos ahora en esa línea y no sabemos lo que va a suceder. ¿Cómo averiguamos el valor de una variable? Usando el comando **`print`** (`p`):

    (Pdb) p size
    1000000000000
    (Pdb) p a_kilobyte_is_1024_bytes
    True
    (Pdb)

Y si ahora nos apetece salir del cuerpo de la función y volver al programa principal, escribimos **`return`** (`r`):

    (Pdb) r
    --Return--
    > /home/juanlu/Development/Python/test/pdb/example.py(23)approximate_size()->'931.3 GiB'
    -> return '{0:.1f} {1}'.format(size, suffix)
    (Pdb)
    931.3 GiB
    --Return--
    > /home/juanlu/Development/Python/test/pdb/example.py(29)<module>()->None
    -> print(approximate_size(1000000000000))
    (Pdb)

## Puntos de ruptura

Imagina que tienes un programa muy largo y no quieres ir línea por línea desde el principio hasta el punto que te interesa. Para eso existen los **puntos de ruptura**: si estableces un punto de ruptura en una línea, el comando `continue` ejecutará el programa sin depuración hasta que encuentre uno, y entonces se detendrá. Si vuelves a usar `continue` el depurador se volverá a detener en el siguiente punto de ruptura, y así sucesivamente hasta que ya no queden y el programa finalice, como vimos al principio del artículo.

Para establecer un punto de ruptura se utiliza el comando **`break`** (`b`):

    $ python -m pdb example.py
    > /home/juanlu/Development/Python/test/pdb/example.py(1)<module>()
    -> SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    (Pdb) l
      1  ->	SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
      2  	            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB',
      3  	'YiB']}
      4
      5  	def approximate_size(size, a_kilobyte_is_1024_bytes=True):
      6  	    '''Convert a file size to human-readable form.
      7
      8  	    Keyword arguments:
      9  	    size -- file size in bytes
     10  	    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
     11  	                                if False, use multiples of 1000
    (Pdb)
     12
     13  	    Returns: string
     14
     15  	    '''
     16  	    if size < 0:
     17  	        raise ValueError('number must be non-negative')
     18
     19  	    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
     20  	    for suffix in SUFFIXES[multiple]:
     21  	        size /= multiple
     22  	        if size < multiple:
    (Pdb) b 21
    Breakpoint 1 at /home/juanlu/Development/Python/test/pdb/example.py:21
    (Pdb) c
    > /home/juanlu/Development/Python/test/pdb/example.py(21)approximate_size()
    -> size /= multiple
    (Pdb)

Hemos establecido un punto de ruptura en la línea 21 del programa, y a continuación el depurador lo ha ejecutado hasta llegar a dicha línea. Y a partir de ahí todo funciona igual que antes 🙂

Otra forma de establecer un punto de ruptura en tu programa es incluir la siguiente línea:

    :::python
    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
        for suffix in SUFFIXES[multiple]:
            import pdb; pdb.set_trace()
            size /= multiple
            if size &lt; multiple:

De este modo, al ejecutarlo saltará el depurador directamente:

    $ python example.py
    > /home/juanlu/Development/Python/test/pdb/example.py(22)approximate_size()
    -> size /= multiple
    (Pdb)

¿Te ha ayudado esto a encontrar ese error que se te resistía? Cuéntanos en los comentarios 🙂

¡Un saludo!