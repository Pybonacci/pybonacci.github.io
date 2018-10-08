---
title: Joyitas en la stdlib: collections
date: 2016-05-08T18:48:58+00:00
author: Kiko Correoso
slug: joyitas-en-la-stdlib-collections
tags: collections, contenedores, secuencias, stdlib

Dentro de la biblioteca estándar de Python dispones de auténticas joyas, muchas veces ignoradas u olvidadas. Es por ello que voy a empezar un breve pero intenso recorrido por algunas piezas de arte disponibles de serie.

# Módulo `collections`

Con la ayuda de este módulo puedes aumentar las estructuras de datos típicas disponibles en Python (listas, tuplas, diccionarios,...).

Veamos algunas utilidades disponibles:

# `ChainMap`

**Solo Python 3. Actualízate!!**

Dicho en bruto, es un conglomerado de diccionarios (también conocidos como _mappings_ o _hash tables_).

Para que puede ser útil:

*   [Ejemplos en la documentación de Python](https://docs.python.org/3/library/collections.html#chainmap-examples-and-recipes).
*   Actualizar partes de una configuración.
*   Actualizar un diccionario pero que pueda ser de forma reversible.
*   [Ejemplos de uso en github](https://github.com/search?l=python&q=from+collections+import+Chainmap&ref=searchresults&type=Code&utf8=%E2%9C%93).
*   ...

Ejemplo, imaginemos que tenemos un diccionario de configuración `dict_a`, que posee las claves `a` y `b`, y queremos actualizar sus valores con otros pares _clave:valor_ que están en el diccionario `dict_b`, que posee las claves `b` y `c`. Podemos hacer:

    :::python
    from collections import ChainMap

    dict_a = {'a': 1, 'b': 10}
    dict_b = {'b': 100, 'c': 1000}

    cm = ChainMap(dict_a, dict_b)
    for key, value in cm.items():
        print(key, value)

**OUTPUT:**

    a 1
    c 1000
    b 10

Hemos añadido el valor de la clave `c` de `dict_b` sin necesidad de modificar nuestro diccionario original de configuración `dict_a`, es decir, hemos hecho un 'cambio' reversible. También podemos 'sobreescribir' las claves que están en nuestro diccionario original de configuración, `dict_b` variando los parámetros del constructor:

    :::python
    cm = ChainMap(dict_b, dict_a)
    for key, value in cm.items():
        print(key, value)


**OUTPUT:**


    b 100
    a 1
    c 1000

Vemos que, además de añadir la clave `c`, hemos sobreescrito la clave `b`.

Los diccionarios originales están disponibles haciendo uso del atributo `maps`:

`cm.maps`

**OUTPUT:**

`[{'b': 100, 'c': 1000}, {'a': 1, 'b': 10}]`

Ejercicio: haced un `dir` de `cm` y un `dir` de `dict_a` y veréis que los atributos y métodos disponibles son parecidos.

Más información en [este hilo de stackoverflow](https://stackoverflow.com/questions/23392976/what-is-the-purpose-of-collections-chainmap) en el que me he basado para el ejemplo anterior (¿basar y copiar no son sinónimos?).

# `Counter`

Permite contar ocurrencias de forma simple. En realidad, su funcionalidad se podría conseguir sin problemas con algunas líneas extra de código pero ya que lo tenemos, está testeado e implementado por gente experta vamos a aprovecharnos de ello.

En la documentación oficial hay [algunos ejemplos interesantes](https://docs.python.org/3/library/collections.html#counter-objects) y en github podéis encontrar [unos cuantos más](https://github.com/search?l=python&q=from+collections+import+Counter&ref=searchresults&type=Code&utf8=%E2%9C%93). Veamos un ejemplo simple pero potente, yo trabajo mucho con datos meteorológicos y uno de los problemas recurrentes es tener fechas repetidas que no deberían existir (pero pasa demasiado a menudo). Una forma rápida de buscar problemas de estos en ficheros y lanzar una alarma cuando ocurra lo que buscamos, sería:

    from io import StringIO
    from collections import Counter

    virtual_file = StringIO("""2010/01/01 2.7
    2010/01/02 2.2
    2010/01/03 2.1
    2010/01/04 2.3
    2010/01/05 2.4
    2010/01/06 2.2
    2010/01/02 2.2
    2010/01/03 2.1
    2010/01/04 2.3
    """)

    if Counter(virtual_file.readlines()).most_common(1)[][1] > 1:
        print('fichero con fecha repetida')

**OUTPUT:**

`fichero con fecha repetida`

# `namedtuple`

A veces me toca crear algún tipo de estructura que guarda datos y algunos metadatos. Una forma simple sin crear una clase ad-hoc sería usar un diccionario. Un ejemplo simple sería:

    :::python
    import numpy as np
    import datetime as dt
    from pprint import pprint

    datos = {
        'valores': np.random.randn(100),
        'frecuencia': dt.timedelta(minutes = 10),
        'fecha_inicial': dt.datetime(2016, 1, 1, , ),
        'parametro': 'wind_speed',
        'unidades': 'm/s'
    }

    pprint(datos)

**OUTPUT:**

    {'fecha_inicial': datetime.datetime(2016, 1, 1, 0, 0),
     'frecuencia': datetime.timedelta(0, 600),
     'parametro': 'wind_speed',
     'unidades': 'm/s',
     'valores': array([-3.02664796, -0.59492715, -1.36233816, -0.27333458,  0.34971592,
            1.43105631,  1.12980511,  0.49542105,  0.37546829,  1.37230197,
           -1.00757915,  1.39334713,  0.73904326,  0.01129817,  0.12431242,
            0.4388826 , -0.49561972, -0.9777947 ,  0.6009799 ,  0.89101799,
            0.48529884,  1.80287157,  1.56321415, -0.62089358, -2.22113341,
           -0.04751354,  0.89715794, -0.23252567,  0.2259216 ,  0.35214745,
           -1.50915239, -1.46547279, -0.4260315 ,  0.20851012,  1.60555432,
            0.4221521 , -1.03399518,  1.68276277,  0.5010984 ,  0.01294853,
           -0.80004557,  1.72141514, -1.38314354,  0.41374512,  0.32861028,
           -2.22385654,  0.80125671, -0.84757451,  0.66896035, -0.26901047,
           -0.06195842, -0.60743183, -0.15538184,  1.16314508, -0.42198419,
            0.61174838,  0.97211057, -1.19791368, -0.68773007,  2.96956504,
           -1.13000346, -0.24523032,  1.6312053 ,  0.77060561, -1.69925633,
           -0.31417013,  0.44196826, -0.59763569,  0.91595894,  1.47587324,
            0.5520219 , -0.62321715,  0.32543574, -1.26181508,  0.94623275,
           -0.25690824,  1.36108942,  0.15445091, -1.25607974,  0.50635589,
            0.65698443, -0.82418166, -0.34054522,  0.23511397, -1.5096761 ,
           -1.12291338, -1.82440698, -0.47433931, -1.86537903,  1.29256869,
            1.78898905,  0.72081117, -0.15169929, -1.24106944,  0.68920997,
            0.36932816, -1.15901835, -0.93990956,  0.37258685, -0.41316085])}

Lo anterior es simple y rápido pero usando una `namedtuple` dispongo de algo parecido con algunas cosas extra. Veamos un ejemplo similar usando `namedtuple`:

    :::python
    from collections import namedtuple

    Datos = namedtuple('Datos', 'valores frecuencia fecha_inicial parametro unidades')

    datos = Datos(np.random.randn(100), 
                  dt.timedelta(minutes = 10),
                  dt.datetime(2016, 1, 1, , ),
                  'wind_speed',
                  'm/s')
    print(datos)

**OUTPUT:**

    Datos(valores=array([ 1.50377059, -1.48083897, -0.76143985,  0.15346996, -0.01094251,
            0.42117233,  1.07136364, -0.24586714,  1.2001748 ,  0.56880926,
            0.56959121,  0.63811853,  0.4621489 ,  1.06636058,  0.32129287,
            2.42264145, -1.25830559, -0.27102862,  2.04853711,  2.07166845,
           -0.27138347, -0.07075163, -0.43547714,  1.69140984,  2.57150371,
            0.80336641, -0.78767876, -2.22281324,  0.23112338, -0.0605485 ,
            0.58304378,  3.33116997, -1.1285789 , -0.2047658 , -0.39240644,
           -1.69724959, -0.0313781 , -0.22892613, -0.06029154, -0.32368036,
           -0.12969429,  1.06231438,  0.05429922, -1.12206555,  1.33383161,
            0.92582424,  0.51615352,  0.93188459,  0.65273332,  0.39108396,
            1.56345696, -0.33158622, -0.27455745,  0.69101563,  1.61244861,
            0.7961402 ,  0.38661924, -0.99864208, -0.10720116,  0.40919342,
           -0.43784138, -3.06455306,  1.69280852,  1.82180641,  0.03604298,
            0.17515747,  1.4370723 , -0.47437528,  1.14510249,  1.36360776,
            0.34575948, -0.14623582,  1.1048332 , -0.2266261 ,  1.34319382,
            0.75608216, -0.62416011, -0.27821722,  0.45365802, -0.98537653,
            0.20172051,  1.70476797,  0.55529542, -0.07833625, -0.62619796,
           -0.02892921, -0.07349236,  0.94659497,  0.20823509,  0.91628769,
           -1.14603843, -0.20748714,  1.13008222, -0.93365802, -0.48125316,
            0.45564591, -0.03136778, -0.86333962,  1.04590165, -0.51757806]), frecuencia=datetime.timedelta(0, 600), fecha_inicial=datetime.datetime(2016, 1, 1, 0, 0), parametro='wind_speed', unidades='m/s')

Ventajas que le veo con respecto a lo anterior:

*  Puedo acceder a los 'campos' o claves del diccionario usando _dot notation_

`print(datos.valores)`

**OUTPUT:**

    [ 1.50377059 -1.48083897 -0.76143985  0.15346996 -0.01094251  0.42117233
      1.07136364 -0.24586714  1.2001748   0.56880926  0.56959121  0.63811853
      0.4621489   1.06636058  0.32129287  2.42264145 -1.25830559 -0.27102862
      2.04853711  2.07166845 -0.27138347 -0.07075163 -0.43547714  1.69140984
      2.57150371  0.80336641 -0.78767876 -2.22281324  0.23112338 -0.0605485
      0.58304378  3.33116997 -1.1285789  -0.2047658  -0.39240644 -1.69724959
     -0.0313781  -0.22892613 -0.06029154 -0.32368036 -0.12969429  1.06231438
      0.05429922 -1.12206555  1.33383161  0.92582424  0.51615352  0.93188459
      0.65273332  0.39108396  1.56345696 -0.33158622 -0.27455745  0.69101563
      1.61244861  0.7961402   0.38661924 -0.99864208 -0.10720116  0.40919342
     -0.43784138 -3.06455306  1.69280852  1.82180641  0.03604298  0.17515747
      1.4370723  -0.47437528  1.14510249  1.36360776  0.34575948 -0.14623582
      1.1048332  -0.2266261   1.34319382  0.75608216 -0.62416011 -0.27821722
      0.45365802 -0.98537653  0.20172051  1.70476797  0.55529542 -0.07833625
     -0.62619796 -0.02892921 -0.07349236  0.94659497  0.20823509  0.91628769
     -1.14603843 -0.20748714  1.13008222 -0.93365802 -0.48125316  0.45564591
     -0.03136778 -0.86333962  1.04590165 -0.51757806]

*  Puedo ver el código usado para crear la estructura de datos usando `verbose = True`. Usa `exec` [entre bambalinas](https://hg.python.org/cpython/file/3.5/Lib/collections/__init__.py#l301) (o_O). Puedo ver que todas las claves se transforman en `property`'s. Puedo ver que se crea documentación... MAGIA en estado puro!!!

*(Si no quieres usar la keyword `verbose = True` puedes seguir teniendo acceso en un objeto usando `obj._source`)*

    :::python
    Datos = namedtuple('Datos', 'valores frecuencia fecha_inicial parametro unidades', verbose = True)

    from builtins import property as _property, tuple as _tuple
    from operator import itemgetter as _itemgetter
    from collections import OrderedDict

    class Datos(tuple):
        'Datos(valores, frecuencia, fecha_inicial, parametro, unidades)'

        __slots__ = ()

        _fields = ('valores', 'frecuencia', 'fecha_inicial', 'parametro', 'unidades')

        def __new__(_cls, valores, frecuencia, fecha_inicial, parametro, unidades):
            'Create new instance of Datos(valores, frecuencia, fecha_inicial, parametro, unidades)'
            return _tuple.__new__(_cls, (valores, frecuencia, fecha_inicial, parametro, unidades))

        @classmethod
        def _make(cls, iterable, new=tuple.__new__, len=len):
            'Make a new Datos object from a sequence or iterable'
            result = new(cls, iterable)
            if len(result) != 5:
                raise TypeError('Expected 5 arguments, got %d' % len(result))
            return result

        def _replace(_self, **kwds):
            'Return a new Datos object replacing specified fields with new values'
            result = _self._make(map(kwds.pop, ('valores', 'frecuencia', 'fecha_inicial', 'parametro', 'unidades'), _self))
            if kwds:
                raise ValueError('Got unexpected field names: %r' % list(kwds))
            return result

        def __repr__(self):
            'Return a nicely formatted representation string'
            return self.__class__.__name__ + '(valores=%r, frecuencia=%r, fecha_inicial=%r, parametro=%r, unidades=%r)' % self

        def _asdict(self):
            'Return a new OrderedDict which maps field names to their values.'
            return OrderedDict(zip(self._fields, self))

        def __getnewargs__(self):
            'Return self as a plain tuple.  Used by copy and pickle.'
            return tuple(self)

        valores = _property(_itemgetter(0), doc='Alias for field number 0')

        frecuencia = _property(_itemgetter(1), doc='Alias for field number 1')

        fecha_inicial = _property(_itemgetter(2), doc='Alias for field number 2')

        parametro = _property(_itemgetter(3), doc='Alias for field number 3')

        unidades = _property(_itemgetter(4), doc='Alias for field number 4')

    # Lo mismo de antes
    print(datos._source)

    from builtins import property as _property, tuple as _tuple
    from operator import itemgetter as _itemgetter
    from collections import OrderedDict

    class Datos(tuple):
        'Datos(valores, frecuencia, fecha_inicial, parametro, unidades)'

        __slots__ = ()

        _fields = ('valores', 'frecuencia', 'fecha_inicial', 'parametro', 'unidades')

        def __new__(_cls, valores, frecuencia, fecha_inicial, parametro, unidades):
            'Create new instance of Datos(valores, frecuencia, fecha_inicial, parametro, unidades)'
            return _tuple.__new__(_cls, (valores, frecuencia, fecha_inicial, parametro, unidades))

        @classmethod
        def _make(cls, iterable, new=tuple.__new__, len=len):
            'Make a new Datos object from a sequence or iterable'
            result = new(cls, iterable)
            if len(result) != 5:
                raise TypeError('Expected 5 arguments, got %d' % len(result))
            return result

        def _replace(_self, **kwds):
            'Return a new Datos object replacing specified fields with new values'
            result = _self._make(map(kwds.pop, ('valores', 'frecuencia', 'fecha_inicial', 'parametro', 'unidades'), _self))
            if kwds:
                raise ValueError('Got unexpected field names: %r' % list(kwds))
            return result

        def __repr__(self):
            'Return a nicely formatted representation string'
            return self.__class__.__name__ + '(valores=%r, frecuencia=%r, fecha_inicial=%r, parametro=%r, unidades=%r)' % self

        def _asdict(self):
            'Return a new OrderedDict which maps field names to their values.'
            return OrderedDict(zip(self._fields, self))

        def __getnewargs__(self):
            'Return self as a plain tuple.  Used by copy and pickle.'
            return tuple(self)

        valores = _property(_itemgetter(0), doc='Alias for field number 0')

        frecuencia = _property(_itemgetter(1), doc='Alias for field number 1')

        fecha_inicial = _property(_itemgetter(2), doc='Alias for field number 2')

        parametro = _property(_itemgetter(3), doc='Alias for field number 3')

        unidades = _property(_itemgetter(4), doc='Alias for field number 4')

* Puedo seguir obteniendo un diccionario (un `OrderedDict`, también incluido en el módulo `collections`) si así lo deseo:

`datos._asdict()['valores']`

**OUTPUT:**

    array([ 1.50377059, -1.48083897, -0.76143985,  0.15346996, -0.01094251,
            0.42117233,  1.07136364, -0.24586714,  1.2001748 ,  0.56880926,
            0.56959121,  0.63811853,  0.4621489 ,  1.06636058,  0.32129287,
            2.42264145, -1.25830559, -0.27102862,  2.04853711,  2.07166845,
           -0.27138347, -0.07075163, -0.43547714,  1.69140984,  2.57150371,
            0.80336641, -0.78767876, -2.22281324,  0.23112338, -0.0605485 ,
            0.58304378,  3.33116997, -1.1285789 , -0.2047658 , -0.39240644,
           -1.69724959, -0.0313781 , -0.22892613, -0.06029154, -0.32368036,
           -0.12969429,  1.06231438,  0.05429922, -1.12206555,  1.33383161,
            0.92582424,  0.51615352,  0.93188459,  0.65273332,  0.39108396,
            1.56345696, -0.33158622, -0.27455745,  0.69101563,  1.61244861,
            0.7961402 ,  0.38661924, -0.99864208, -0.10720116,  0.40919342,
           -0.43784138, -3.06455306,  1.69280852,  1.82180641,  0.03604298,
            0.17515747,  1.4370723 , -0.47437528,  1.14510249,  1.36360776,
            0.34575948, -0.14623582,  1.1048332 , -0.2266261 ,  1.34319382,
            0.75608216, -0.62416011, -0.27821722,  0.45365802, -0.98537653,
            0.20172051,  1.70476797,  0.55529542, -0.07833625, -0.62619796,
           -0.02892921, -0.07349236,  0.94659497,  0.20823509,  0.91628769,
           -1.14603843, -0.20748714,  1.13008222, -0.93365802, -0.48125316,
            0.45564591, -0.03136778, -0.86333962,  1.04590165, -0.51757806])

*  Puedo crear subclases de forma simple para añadir funcionalidad. Por ejemplo, creamos una nueva clase con un nuevo método que calcula la media de los `valores`:

    :::python
    class DatosExtendidos(Datos):
        def media(self):
            "Calcula la media de los valores."
            return self.valores.mean()

    datos_ext = DatosExtendidos(**datos._asdict())

    print(datos_ext.media())

`0.27764229179`

**WOW!!!!!**

Los ejemplos en la [documentación oficial son muy potentes y dan nuevas ideas de potenciales usos](https://docs.python.org/3/library/collections.html?highlight=collections#collections.namedtuple).

# `deque`

Otra joyita que quizá debería usar más a menudo sería `deque`. Es una secuencia mutable (parecido a una lista), pero con una serie de ventajas. Es una [cola/lista](https://es.wikipedia.org/wiki/Cola_%28inform%C3%A1tica%29) cuyo principio y fin es 'indistinguible', es _thread-safe_ y está diseñada para poder insertar y eliminar de forma rápida en ambos extremos de la cola (ahora veremos qué significa todo esto). Un uso evidente es el de usar, por ejemplo, una secuencia como _stream_ de datos con un número de elementos fijo y/o rápidamente actualizable:

*  Podemos limitar su tamaño y si añadimos elementos por un lado se eliminan los del otro extremo.
*  Podemos rotar los datos de forma eficiente.
*  ...

Veamos un ejemplo:

    :::python
    from collections import deque

    dq = deque(range(10), maxlen = 10)
    lst = list(range(10))
    print(dq)
    print(lst)

**OUTPUT:**

    deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
___

    :::python
    # los tres últimos elementos los anexa nuevamente al principio de la secuencia.
    dq.rotate(3)
    print(dq)
    lst = lst[-3:] + lst[:-3]
    print(lst)

**OUTPUT:**

    deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
    [7, 8, 9, 0, 1, 2, 3, 4, 5, 6]

Veamos la eficiencia de esta operación:

    tmp = deque(range(100000), maxlen = 100000)
    %timeit dq.rotate(30000)
    tmp = list(range(100000))
    %timeit tmp[-30000:] + tmp[:-30000]

    The slowest run took 9.62 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000000 loops, best of 3: 519 ns per loop
    100 loops, best of 3: 3.07 ms per loop

Con una `queue` podemos anexar de forma eficiente a ambos lados:

    dq.append(100)
    print(dq)
    dq.appendleft(10000)
    print(dq)

**OUTPUT:**

    deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 100], maxlen=10)
    deque([10000, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)

___

    dq.extend(range(10))
    print(dq)
    dq.extendleft([10, 100])
    print(dq)

**OUTPUT:**

    deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
    deque([100, 10, 0, 1, 2, 3, 4, 5, 6, 7], maxlen=10)

Etc.

Puedes hacer cosas similares a las hechas con listas pero de forma más eficiente y práctica en determinados casos!!

Recordad que, además, disponemos del [módulo `queue` en la librería estándar](https://docs.python.org/3/library/queue.html).

# Conclusión

Este módulo esconde cosas muy interesantes, algunas que no hemos visto. Por tanto, si no lo conocéis, deberíais explorar el módulo `collections`, si lo conocéis nos podéis indicar como lo usáis en los comentarios que puedes encontrar más abajo.
