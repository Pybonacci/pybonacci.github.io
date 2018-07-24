---
title: Trabajando con recarray
date: 2012-12-14T23:40:25+00:00
author: Kiko Correoso
slug: trabajando-con-recarray-3
tags: ipynb2wp, numpy, numpy.recarray, recarray, record array

En el artículo de hoy vamos a ver el uso de numpy.recarray (o [arrays estructurados](http://docs.scipy.org/doc/numpy/user/basics.rec.html)) y las posibilidades que tiene usar record arrays, que no son más que arrays numpy a los que se puede acceder usando atributos y donde podemos usar diferente tipo de dato (int, float, string,...) en cada uno de los campos como si fuera una tabla de una hoja de cálculo.

**[En esta entrada se ha usado numpy 1.6, ipython 0.13 sobre python 2.7]**

Primero de todo importamos lo necesario:

    :::python
    import numpy as np

Creamos una serie de vectores que serán los que usaremos a posteriori para 'poblar' nuestro recarray.

    :::python
    persona = ['juanlu', 'dapid',
               'kiko', 'eugenia',
               'fernando', 'maria',
               'lorena', 'angel',
                'tomas', 'susana']
    sexo = ['v', 'v', 'v', 'm', 'v', ## 'v' para varon y 'm' para mujer
            'm', 'm', 'v', 'v', 'm']
    altura = [185, 170, 175, 168, 183, 159, 152, 191, 179, 178]

Ahora imaginad que queremos esos tres vectores de datos en un array y queremos conservar el tipo de dato de cada vector (string para persona, string para sexo y entero para la altura en centímetros) y queremos 'titular' cada uno de esos vectores en nuestro nuevo array y queremos acceder a cada uno de esos vectores mediante un atributo. Esto lo podremos hacer de varias maneras creando un recarray:

<!--more-->

    :::python
    ## Una primera forma
    lista = zip(persona, sexo, altura)
    mirecarray1 = np.array(lista,
                           dtype = [('persona', str, 10),
                                    ('sexo', np.str_, 1),
                                    ('altura', np.int)])
    mirecarray1 = mirecarray1.view(np.recarray)
    ## Una segunda forma
    mirecarray2 = np.recarray((len(persona),),
                              dtype = [('persona', str, 10), ('sexo', np.str_, 1), ('altura', np.int)])
    mirecarray2.persona = persona
    mirecarray2.sexo = sexo
    mirecarray2.altura = altura
    ## Una tercera forma
    mirecarray3 = np.core.records.fromarrays([persona, sexo, altura],
                                             names = 'persona, sexo altura')
    ## Otras formas
    ## http://docs.scipy.org/doc/numpy/reference/routines.array-creation.html#creating-record-arrays-numpy-rec

Por último, veamos como podemos hacer operaciones con un recarray. Vamos a extraer la altura media de las mujeres, la altura media de los hombres, y los extremos (máximo y mínimo) de las alturas de las mujeres y de los hombres:

    :::python
    ## Altura promedio de las mujeres
    print 'altura promedio de las mujeres:', mirecarray1.altura[mirecarray1.sexo == 'm'].mean(), 'cm'
    ## Altura promedio de los hombres
    print'altura promedio de los hombres:', mirecarray1.altura[mirecarray1.sexo == 'v'].mean(), 'cm'
    ## Altura maxima y minima de una mujer
    print u'altura máxima de una mujer:', mirecarray1.altura[mirecarray1.sexo == 'm'].max(), 'cm'
    print u'altura mínima de una mujer:', mirecarray1.altura[mirecarray1.sexo == 'm'].min(), 'cm'
    ## Altura maxima y minima de un hombre
    print u'altura máxima de un hombre:', mirecarray1.altura[mirecarray1.sexo == 'v'].max(), 'cm'
    print u'altura mínima de un hombre:', mirecarray1.altura[mirecarray1.sexo == 'v'].min(), 'cm'

La salida del anterior código mostrará:

    :::python
    altura promedio de las mujeres: 164.25 cm
    altura promedio de los hombres: 180.5 cm
    altura máxima de una mujer: 178 cm
    altura mínima de una mujer: 152 cm
    altura máxima de un hombre: 191 cm
    altura mínima de un hombre: 170 cm

Y esto ha sido todo por hoy pero no desconectéis puesto que tenemos muchas novedades en cola (y poco tiempo).

Saludos.

##### _This post has been published on wordpress.com from an ipython notebook using [ipynb2wp](https://github.com/kikocorreoso/ipynb2wp)_