---
title: MicroEntradas: scipy.constants
date: 2014-07-13T11:23:26+00:00
author: Kiko Correoso
slug: microentradas-scipy-constants
tags: constantes, constantes físicas, MicroEntradas, scipy

¿No te acuerdas de la constante de gravitación universal?, ¿no sabes cuanta área es un acre?, ¿por qué me pasan esos resultados en pulgadas?, ¿a qué altura estamos volando cuando me dicen que estamos a 10.000 pies?,... [Puedes responder a todo eso usando el, creo que infrautilizado, módulo _constants_ dentro del paquete _scipy_](http://docs.scipy.org/doc/scipy/reference/constants.html).

Primero de todo, vamos a importat el módulo en cuestión:

    :::python
    from scipy import constants as constantes

En este módulo disponemos de varias constantes físicas y matemáticas de uso muy habitual en determinados campos. El número pi, la constante de gravitación universal, la constante de Plank o la masa del electrón [están en la punta de tus dedos](http://docs.scipy.org/doc/scipy/reference/constants.html#mathematical-constants).</pre> 

    :::python
    print(constantes.pi,
          constantes.gravitational_constant,
          constantes.Plank,
          constantes.m_e)

Nos dará el siguiente resultado:

    :::python
    3.141592653589793 6.67384e-11 6.62606957e-34 9.10938291e-31

Podemos acceder a otras constantes ([no tan constantes](http://physics.nist.gov/cuu/pdf/RevModPhysCODATA2010.pdf)) usando un diccionario con el nombre de la constante según la base de datos del Committee on Data for Science and Technology (CODATA):

    :::python
    constantes.value('standard atmosphere')

Podemos obtener el valor de varias unidades en el sistema internacional simplemente poniendo su nombre

    :::python
    print(constantes.foot, constantes.inch)

Incluso tenemos funciones para hacer conversiones de unidades

    :::python
    print(constantes.C2K(10))

Nos daría el valor de 10ºC en grados Kelvin.

Saludos.

&nbsp;