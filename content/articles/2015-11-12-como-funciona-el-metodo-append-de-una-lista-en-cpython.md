---
title: ¿Cómo funciona el método append de una lista en CPython?
date: 2015-11-12T23:01:56+00:00
author: Kiko Correoso
slug: como-funciona-el-metodo-append-de-una-lista-en-cpython
tags: append, CPython, implementación, lista

Vamos a empezar con más preguntas que respuestas.

Como sabéis, las listas de Python son _arrays_ dinámicos. Por otro lado, las tuplas son _arrays_ estáticos.

**¿Qué implica que las listas sean _arrays_ dinámicos?**

Al ser un array dinámico podemos modificar sus elementos así como extender el array (lista).

**¿Cómo funciona lo de extender el _array_ (lista)?**

Cada vez que usamos el método `append` de las listas se crea una copia de la lista original y se añade un elemento a esa copia para luego borrar el array original.

**¿Es esto último cierto?**

Más o menos.

Todos estaréis conmigo que si cada vez que añadimos un nuevo elemento tenemos que crear una copia y luego eliminar el _array_ original podríamos crear cierto coste/gasto de recursos (en memoria, principalmente, creando copias).

Veamos un poco de código:

    :::python
    import sys

    lista = []
    for i in range(100):
        lista.append(i)
        txt = 'número de elementos = {0:>3} , tamaño de la lista = {1:>4}'
        print(txt.format(i + 1, sys.getsizeof(lista)))

**OUTPUT:**

    número de elementos =   1 , tamaño de la lista =   96
    número de elementos =   2 , tamaño de la lista =   96
    número de elementos =   3 , tamaño de la lista =   96
    número de elementos =   4 , tamaño de la lista =   96
    número de elementos =   5 , tamaño de la lista =  128
    número de elementos =   6 , tamaño de la lista =  128
    número de elementos =   7 , tamaño de la lista =  128
    número de elementos =   8 , tamaño de la lista =  128
    número de elementos =   9 , tamaño de la lista =  192
    número de elementos =  10 , tamaño de la lista =  192
    número de elementos =  11 , tamaño de la lista =  192
    número de elementos =  12 , tamaño de la lista =  192
    número de elementos =  13 , tamaño de la lista =  192
    número de elementos =  14 , tamaño de la lista =  192
    número de elementos =  15 , tamaño de la lista =  192
    número de elementos =  16 , tamaño de la lista =  192
    número de elementos =  17 , tamaño de la lista =  264
    número de elementos =  18 , tamaño de la lista =  264
    número de elementos =  19 , tamaño de la lista =  264
    número de elementos =  20 , tamaño de la lista =  264
    número de elementos =  21 , tamaño de la lista =  264
    número de elementos =  22 , tamaño de la lista =  264
    número de elementos =  23 , tamaño de la lista =  264
    número de elementos =  24 , tamaño de la lista =  264
    número de elementos =  25 , tamaño de la lista =  264
    número de elementos =  26 , tamaño de la lista =  344
    número de elementos =  27 , tamaño de la lista =  344
    número de elementos =  28 , tamaño de la lista =  344
    número de elementos =  29 , tamaño de la lista =  344
    número de elementos =  30 , tamaño de la lista =  344
    número de elementos =  31 , tamaño de la lista =  344
    número de elementos =  32 , tamaño de la lista =  344
    número de elementos =  33 , tamaño de la lista =  344
    número de elementos =  34 , tamaño de la lista =  344
    número de elementos =  35 , tamaño de la lista =  344
    número de elementos =  36 , tamaño de la lista =  432
    número de elementos =  37 , tamaño de la lista =  432
    número de elementos =  38 , tamaño de la lista =  432
    número de elementos =  39 , tamaño de la lista =  432
    número de elementos =  40 , tamaño de la lista =  432
    número de elementos =  41 , tamaño de la lista =  432
    número de elementos =  42 , tamaño de la lista =  432
    número de elementos =  43 , tamaño de la lista =  432
    número de elementos =  44 , tamaño de la lista =  432
    número de elementos =  45 , tamaño de la lista =  432
    número de elementos =  46 , tamaño de la lista =  432
    número de elementos =  47 , tamaño de la lista =  528
    número de elementos =  48 , tamaño de la lista =  528
    número de elementos =  49 , tamaño de la lista =  528
    número de elementos =  50 , tamaño de la lista =  528
    número de elementos =  51 , tamaño de la lista =  528
    número de elementos =  52 , tamaño de la lista =  528
    número de elementos =  53 , tamaño de la lista =  528
    número de elementos =  54 , tamaño de la lista =  528
    número de elementos =  55 , tamaño de la lista =  528
    número de elementos =  56 , tamaño de la lista =  528
    número de elementos =  57 , tamaño de la lista =  528
    número de elementos =  58 , tamaño de la lista =  528
    número de elementos =  59 , tamaño de la lista =  640
    número de elementos =  60 , tamaño de la lista =  640
    número de elementos =  61 , tamaño de la lista =  640
    número de elementos =  62 , tamaño de la lista =  640
    número de elementos =  63 , tamaño de la lista =  640
    número de elementos =  64 , tamaño de la lista =  640
    número de elementos =  65 , tamaño de la lista =  640
    número de elementos =  66 , tamaño de la lista =  640
    número de elementos =  67 , tamaño de la lista =  640
    número de elementos =  68 , tamaño de la lista =  640
    número de elementos =  69 , tamaño de la lista =  640
    número de elementos =  70 , tamaño de la lista =  640
    número de elementos =  71 , tamaño de la lista =  640
    número de elementos =  72 , tamaño de la lista =  640
    número de elementos =  73 , tamaño de la lista =  768
    número de elementos =  74 , tamaño de la lista =  768
    número de elementos =  75 , tamaño de la lista =  768
    número de elementos =  76 , tamaño de la lista =  768
    número de elementos =  77 , tamaño de la lista =  768
    número de elementos =  78 , tamaño de la lista =  768
    número de elementos =  79 , tamaño de la lista =  768
    número de elementos =  80 , tamaño de la lista =  768
    número de elementos =  81 , tamaño de la lista =  768
    número de elementos =  82 , tamaño de la lista =  768
    número de elementos =  83 , tamaño de la lista =  768
    número de elementos =  84 , tamaño de la lista =  768
    número de elementos =  85 , tamaño de la lista =  768
    número de elementos =  86 , tamaño de la lista =  768
    número de elementos =  87 , tamaño de la lista =  768
    número de elementos =  88 , tamaño de la lista =  768
    número de elementos =  89 , tamaño de la lista =  912
    número de elementos =  90 , tamaño de la lista =  912
    número de elementos =  91 , tamaño de la lista =  912
    número de elementos =  92 , tamaño de la lista =  912
    número de elementos =  93 , tamaño de la lista =  912
    número de elementos =  94 , tamaño de la lista =  912
    número de elementos =  95 , tamaño de la lista =  912
    número de elementos =  96 , tamaño de la lista =  912
    número de elementos =  97 , tamaño de la lista =  912
    número de elementos =  98 , tamaño de la lista =  912
    número de elementos =  99 , tamaño de la lista =  912
    número de elementos = 100 , tamaño de la lista =  912

En el anterior código hemos creado una lista vacía y le hemos ido añadiendo elementos y hemos obtenido el tamaño de la lista usando la función `getsizeof` que nos [indica el tamaño del objeto en _bytes_](https://docs.python.org/3/library/sys.html?highlight=sys%20getsizeof#sys.getsizeof). Luego hemos mostrado en pantalla el número de elementos que tiene la lista y el tamaño que ocupa.

**Pero, ¿qué ocurre?, ¿por qué aumentando el número de elementos, a veces, no aumenta el tamaño del objeto?, ¿por qué luego cambia?, ¿por qué a medida que hay más elementos en la lista tarda más en cambiar el tamaño de la misma?**

Veamos qué dice el código original de las listas en el repo de Python localizado en [Objects/listobject.c](https://hg.python.org/releasing/3.5/file/tip/Objects/listobject.c#l42).

A partir de la línea 42 del código C podemos leer:

    :::[]
    /* This over-allocates proportional to the list size, making room
     * for additional growth.  The over-allocation is mild, but is
     * enough to give linear-time amortized behavior over a long
     * sequence of appends() in the presence of a poorly-performing
     * system realloc().
     * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
     */
    new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6);
    
La última línea traducida a Python sería algo así:

`new_allocated = (newsize >> 3) + (3 if newsize < 9 else 6)`

En el primer paréntesis tenemos el [operador _bitwise right shift_](https://wiki.python.org/moin/BitwiseOperators), similar a la versión en C (no hay que olvidar que CPython está escrito en C) mientras que en el segundo paréntesis tenemos el operador ternario (sin duda, un poco más legible que la versión en C).

**¿Qué está pasando aquí?**

Los buenos de los _core developers_ de CPython han pensado que si usas un _array_ dinámico será porque quieres hacer 'perrerías' con él, como ampliarlo. Y si lo amplías una vez es probable que lo amplíes varias veces. Es por ello que, normalmente, se usa un un tamaño un poco mayor, basado en el tamaño y siquiendo la regla mostrada más arriba, para el _array_ (lista) y, de esta forma, podemos ampliarlo sin necesidad de crear tantas copias.

Veamos esto gráficamente:

Importamos matplotlib para poder crear los gráficos.

    :::python
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    %matplotlib inline

Creamos nuestra `lista` y otra lista que almacenará los tamaños en bytes, `sizes`.

    :::python
    lista = list([1])
    sizes = [sys.getsizeof(lista)]

    for i in range(2, 100000):
        lista.append(i)
        sizes.append(sys.getsizeof(lista))

Y ahora dibujamos los tamaños en función del número de elementos dentro de la lista:

    :::python
    plt.figure(figsize = (10,10))
    plt.plot(lista, sizes)
    plt.xlabel('Número de elementos en la lista')
    plt.ylabel('Tamaño en bytes para la lista de tamaño $N$')

**OUTPUT**

`<matplotlib.text.Text at 0x7f0655169c88>`

![wpid](https://pybonacci.org/images/2015/11/wpid-¿Cómo_funciona_el_método_append_de_una_lista_en_CPython1.png?style=centerme)

Vemos como los "escalones" en el tamaño de la lista con _N_ elementos va aumentando y el escalón cada vez es más largo a medida que aumenta el tamaño de la `lista`.

Veamos como es el valor del tamaño dividido por el número de elementos de la lista a medida que va aumentando el mismo (los ejes de la gráfica tienen escala logarítmica):

    :::python
    increment = [s/l for s, l in zip(sizes, lista)]

    plt.figure(figsize = (10,10))
    plt.yscale('log')
    plt.xscale('log')
    plt.ylim(7, max(increment))
    plt.plot(lista, increment)
    plt.xlabel('Número de elementos en la lista')
    plt.ylabel('Bytes por número de elementos')

**OUTPUT:**

`<matplotlib.text.Text at 0x7f06552ada20>`

![wpid2](https://pybonacci.org/images/2015/11/wpid-¿Cómo_funciona_el_método_append_de_una_lista_en_CPython2.png?style=centerme)

Curioso, ¿no?

Espero que hayáis aprendido tanto como he aprendido yo elaborando esta entrada.
