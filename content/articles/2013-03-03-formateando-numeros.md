---
title: Formateando números
date: 2013-03-03T09:38:36+00:00
author: Kiko Correoso
slug: formateando-numeros
tags: format, formateando texto, formato, python

Muy a menudo tengo que andar leyendo datos de sensores de medida conectados a 'loggers' con formatos muy variopintos y transformarlos a algo legible por un ser humano (echadle un ojo a [regex mediante ejemplos](https://pybonacci.org/2013/02/21/regex-mediante-ejemplos/) para conocer el maravilloso mundo de las expresiones regulares y no ser tan bruto como yo a la hora de tratar esos variopintos formatos).

Hoy vamos a estar muy centrados en una sola cosa, vamos a ver como usar el método [`format`](http://docs.python.org/3.3/library/stdtypes.html#str.format) de la clase [`string`](http://docs.python.org/3.3/library/stdtypes.html#text-sequence-type-str).

Vamos a empezar por muy algo sencillo, vamos a mostrar números en pantalla (o los podéis grabar en un fichero) de forma secuencial:

    :::python
    datos = range(1,200, 20)
    for dato in datos: print(dato)

La salida del anterior código mostrará:

    :::python
    1
    21
    41
    61
    81
    101
    121
    141
    161
    181

Lo anterior está bien, pero no tenemos mucha libertad para poder alinear la salida como queramos. Por ello vamos a ver como podríamos representar lo anterior usando el método `format`. En una _cadena_ o _string_ podemos meter llaves ('_{}_') y lo que vaya entre las llaves irá asociado a algún objeto que queremos formatear, lo que vaya entre las llaves se llama _campo de reemplazo_. En el siguiente ejemplo ponemos una llave y lo que se escriba dentro, en este caso no ponemos nada, irá asociado a la variable que coloquemos dentro del `format`.

    :::python
    for dato in datos: print('{}'.format(dato))

La salida del anterior código mostrará:

    :::python
    1
    21
    41
    61
    81
    101
    121
    141
    161
    181

Ahora hemos conseguido lo mismo que al principio solo que ahora tenemos libertad para formatear mejor la salida. ¿Si tengo más de una variable cómo sabría qué variable hay que usar para cada par de llaves? Para resolver esto podemos usar números dentro de las llaves, lo que hemos llamado anteriormente _campo de reemplazo_, así el 0 corresponderá a la primera variable, el 1 corresponderá a la segunda,...

    :::python
    for i, dato in enumerate(datos): print('{0} {1}'.format(i, dato))

La salida del anterior código mostrará:

    :::python
    0 1
    1 21
    2 41
    3 61
    4 81
    5 101
    6 121
    7 141
    8 161
    9 181

Lo anterior es equivalente a usar un nombre para las variables donde el nombre será el _campo de reemplazo_ y será reemplazado por su valor, de esta forma no tenemos que conocer el orden en que se colocan las variables en el format como en el ejemplo anterior:

    :::python
    for i, dato in enumerate(datos): print('{contador} {valor}'.format(contador = i, valor = dato))

La salida del anterior código mostrará:

    :::python
    0 1
    1 21
    2 41
    3 61
    4 81
    5 101
    6 121
    7 141
    8 161
    9 181

También podríamos usar un diccionario y acceder mediante sus claves:

    :::python
    for i, dato in enumerate(datos):
        texto = {'contador' : i, 'valor' : dato}
        print('{contador} {valor}'.format(**texto))

La salida del anterior código mostrará:

    :::python
    0 1
    1 21
    2 41
    3 61
    4 81
    5 101
    6 121
    7 141
    8 161
    9 181

O no usar absolutamente nada, que no lo recomiendo a no ser que solo haya una cosa a sustituir dentro del _string_:

    :::python
    for i, dato in enumerate(datos): print('{} {}'.format(i, dato))

La salida del anterior código mostrará:

    :::python
    0 1
    1 21
    2 41
    3 61
    4 81
    5 101
    6 121
    7 141
    8 161
    9 181

Pero todo lo anterior es muy feo, la segunda columna está alineada a la izquierda. ¿Cómo podemos hacer que se alinee a la derecha? Podemos usar los símbolos de alineación de los que disponemos:

'<' fuerza al campo a estar alineado a la izquierda dentro del espacio disponible y es el comportamiento por defecto

'>' fuerza al campo a estar alineado a la derecha y este sería el comportamiento por defecto para números pero, de momento, no usamos números, sino _strings_

'=' fuerza al 'relleno' a ser colocado después del signo (si lo hubiera) pero antes de los dígitos. Esto se usa para escribir campos de la forma ‘+000000120’ y solo válido para valores numéricos

'^' fuerza al campo a estar centrado dentro del espacio disponible.

Vamos a representar lo anterior para que veáis como funciona. La primera y última línea del código siguiente solo sirve para que tengáis una referencia. El 10 colocado dentro de las claves indica que vamos a usar 10 espacios para cada campo, más adelante veremos más sobre esto.

    :::python
    print('{0} {0} {0} {0}'.format('='*10))
    for i, dato in enumerate(datos):
        print('{0:&lt;10} {1:&gt;10} {2:=10} {3:^10}'.format(dato, dato, dato, dato))
    print('{0} {0} {0} {0}'.format('='*10))

La salida del anterior código mostrará:

    :::python
    ========== ========== ========== ==========
    1                   1          1     1
    21                 21         21     21
    41                 41         41     41
    61                 61         61     61
    81                 81         81     81
    101               101        101    101
    121               121        121    121
    141               141        141    141
    161               161        161    161
    181               181        181    181
    ========== ========== ========== ==========

Pero entre el segundo y el tercero no vemos diferencia,... Vamos a ver donde estaría la diferencia usando un símbolo '+' para los números y así veremos donde se coloca en un caso y en el otro:

    :::python
    print('{0} {0} {0} {0}'.format('='*10))
    for dato in datos:
        print('{0:&lt;10} {1:&gt;+10} {2:=+10} {3:^10}'.format(dato, dato, dato, dato))
    print('{0} {0} {0} {0}'.format('='*10))

La salida del anterior código mostrará:

    :::python
    ========== ========== ========== ==========
    1                  +1 +        1     1
    21                +21 +       21     21
    41                +41 +       41     41
    61                +61 +       61     61
    81                +81 +       81     81
    101              +101 +      101    101
    121              +121 +      121    121
    141              +141 +      141    141
    161              +161 +      161    161
    181              +181 +      181    181
    ========== ========== ========== ==========

Esto ya empieza a ser un poco más excitante (que frikazo que soy). Si quisiéramos que en el espacio que dejamos a cada número no hubiera espacios vacios y se rellenaran con '0' haríamos lo siguiente:

    :::python
    print('{0} {0}'.format('='*10))
    for i, dato in enumerate(datos): print('{0:^10} {1:&gt;010}'.format(i, dato))
    print('{0} {0}'.format('='*10))

La salida del anterior código mostrará:

    :::python
    ========== ==========
        0      0000000001
        1      0000000021
        2      0000000041
        3      0000000061
        4      0000000081
        5      0000000101
        6      0000000121
        7      0000000141
        8      0000000161
        9      0000000181
    ========== ==========

¿Colocamos dos decimales en la segunda columna? Esto lo podemos conseguir usando los tipos de datos disponibles. En este caso vamos a usar 'f' para float colocándole dos puntos decimales dentro de los 10 espacios disponibles que definimos para la segunda columna:

    :::python
    print('{0} {0}'.format('='*10))
    for i, dato in enumerate(datos): print('{0:^10} {1:&gt;10.2f}'.format(i, dato))
    print('{0} {0}'.format('='*10))

La salida del anterior código mostrará:

    :::python
    ========== ==========
        0            1.00
        1           21.00
        2           41.00
        3           61.00
        4           81.00
        5          101.00
        6          121.00
        7          141.00
        8          161.00
        9          181.00
    ========== ==========

¿Y si usamos notación exponencial? Pues lo mismo pero usando ahora el tipo 'e' o el tipo 'E'.

    :::python
    print('{0} {0}'.format('='*10))
    for i, dato in enumerate(datos): print('{0:^10} {1:&gt;10.3e}'.format(i, dato))
    print('{0} {0}'.format('='*10))

La salida del anterior código mostrará:

    :::python
    ========== ==========
        0       1.000e+00
        1       2.100e+01
        2       4.100e+01
        3       6.100e+01
        4       8.100e+01
        5       1.010e+02
        6       1.210e+02
        7       1.410e+02
        8       1.610e+02
        9       1.810e+02
    ========== ==========

Si nuestros datos fueran valores en tanto por uno y los queremos transformar a valores en tanto por ciento (_'%'_) podemos usar el tipo % solo válido para números.

    :::python
    print('{0} {1}'.format('='*10, '='*15))
    for i, dato in enumerate(datos): print('{0:^10} {1:&gt;15%}'.format(i, dato))
    print('{0} {1}'.format('='*10, '='*15))

La salida del anterior código mostrará:

    :::python
    ========== ===============
        0          100.000000%
        1         2100.000000%
        2         4100.000000%
        3         6100.000000%
        4         8100.000000%
        5        10100.000000%
        6        12100.000000%
        7        14100.000000%
        8        16100.000000%
        9        18100.000000%
    ========== ===============

Como resumen, entre las claves podéis poner el campo a reemplazar, cómo se formateará el texto, qué ancho (en caracteres) se usará el para el campo a reemplazar, qué tipo de dato se escribirá (decimal, entero, string, caracter,...).

Si queréis ampliar vuestros conocimientos en el uso del método format o en como formatear texto con python podéis echarle un ojo a:

[Format String Syntax](http://docs.python.org/3.3/library/string.html#format-string-syntax)

[Fancier Ouput Formatting](http://docs.python.org/2/tutorial/inputoutput.html#fancier-output-formatting)

##### _This post has been published on wordpress.com from an ipython notebook using [ipynb2wp](https://github.com/kikocorreoso/ipynb2wp)_
