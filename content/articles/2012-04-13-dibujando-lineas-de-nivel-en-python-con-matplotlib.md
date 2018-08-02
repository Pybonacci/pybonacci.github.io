---
title: Dibujando líneas de nivel en Python con matplotlib
date: 2012-04-13T12:08:04+00:00
author: Juan Luis Cano
slug: dibujando-lineas-de-nivel-en-python-con-matplotlib
tags: gráficos, matplotlib, numpy, python, vectorización

## Introducción

En este artículo vamos a ver cómo representar en Python un mapa de _curvas de nivel_ o de _isolíneas_, esto es, curvas que conectan los puntos en los que una función tiene un mismo valor constante, utilizando NumPy y matplotlib. Los mapas de curvas de nivel («contour lines» en inglés) son muy útiles, porque ayudan a ver la información de una manera mucho más cómoda que las representaciones de superficies en tres dimensiones, por muy espectaculares que estas últimas puedan quedar. Un ejemplo muy cotidiano es el mapa de isobaras que nos dan en la predicción del tiempo como el que se ve en la imagen: los puntos que están sobre la misma línea están todos a la misma presión.<figure id="attachment_156" style="width: 448px" class="wp-caption aligncenter">

![Mapa de isobaras](http://pybonacci.org/images/2012/04/2012041300006_ww_i1x0w006.gif)

<!--more-->

En este artículo nos ceñiremos a funciones

$f: D \longrightarrow \mathbb{R}, D \subset \mathbb{R}^2,$

es decir, funciones que están definidas en un conjunto del plano y que a cada punto del mismo le asignan un número real. En el caso del ejemplo que hemos puesto, la función estaría definida (aceptando por un segundo que la Tierra es plana) en un conjunto del mapa que comprende la zona de la imagen y a cada punto le asigna el valor de presión atmosférica en dicho punto.

_**Para la siguiente entrada se ha usado python 2.7.2, numpy 1.6.1, scipy 0.9.0 y matplotlib 1.1.0.**_

## Creación del mallado {#mallado}

Vamos a representar el mapa de curvas de nivel de la función

$f(x, y) = \cos(-10 x y)+\sinh(x+y)-\log(\frac{3+x^2}{1+y^2}).$

en el dominio $D = [-3 / 2, 3 / 2] \times [-3 / 2, 3 / 2]$. Me la acabo de inventar, y quedan las líneas curiosas.

Para empezar tenemos que _discretizar_ este dominio: generaremos una malla o rejilla de puntos y evaluaremos la función en cada uno de ellos. Para ello, utilizaremos la función [`meshgrid()`](http://docs.scipy.org/doc/numpy-1.6.0/reference/generated/numpy.meshgrid.html) de NumPy:

    :::python
    $ ipython2
    Python 2.7.2 (default, Jan 31 2012, 13:19:49)
    Type "copyright", "credits" or "license" for more information.
    IPython 0.12 -- An enhanced Interactive Python.
    ?         -&gt; Introduction and overview of IPython's features.
    %quickref -&gt; Quick reference.
    help      -&gt; Python's own help system.
    object?   -&gt; Details about 'object', use 'object??' for extra details.
    In [1]: import numpy as np
    In [2]: xx = np.linspace(-1.5, 1.5)
    In [3]: yy = xx.copy()
    In [4]: X, Y = np.meshgrid(xx, yy)
    In [5]: X
    Out[5]:
    array([[-1.5       , -1.43877551, -1.37755102, ...,  1.37755102,
             1.43877551,  1.5       ],
           [-1.5       , -1.43877551, -1.37755102, ...,  1.37755102,
             1.43877551,  1.5       ],
           [-1.5       , -1.43877551, -1.37755102, ...,  1.37755102,
             1.43877551,  1.5       ],
           ...,
           [-1.5       , -1.43877551, -1.37755102, ...,  1.37755102,
             1.43877551,  1.5       ],
           [-1.5       , -1.43877551, -1.37755102, ...,  1.37755102,
             1.43877551,  1.5       ],
           [-1.5       , -1.43877551, -1.37755102, ...,  1.37755102,
             1.43877551,  1.5       ]])
    In [6]: Y
    Out[6]:
    array([[-1.5       , -1.5       , -1.5       , ..., -1.5       ,
            -1.5       , -1.5       ],
           [-1.43877551, -1.43877551, -1.43877551, ..., -1.43877551,
            -1.43877551, -1.43877551],
           [-1.37755102, -1.37755102, -1.37755102, ..., -1.37755102,
            -1.37755102, -1.37755102],
           ...,
           [ 1.37755102,  1.37755102,  1.37755102, ...,  1.37755102,
             1.37755102,  1.37755102],
           [ 1.43877551,  1.43877551,  1.43877551, ...,  1.43877551,
             1.43877551,  1.43877551],
           [ 1.5       ,  1.5       ,  1.5       , ...,  1.5       ,
             1.5       ,  1.5       ]])

En primer lugar hemos creado dos vectores `xx` e `yy` donde hemos almacenado los dos intervalos, y después hemos llamado a la función `meshgrid(xx, yy)` y nos ha devuelto dos arrays de dimensión 2: el primero de ellos varía sólo a lo largo de las columnas, y el segundo sólo a lo largo de las filas. A los que vengan de MATLAB esto les parecerá obvio, pero el resto tal vez se estén preguntando ¿por qué? y ¿para qué?

Para entender por qué esto es útil, es fundamental recordar que en NumPy las operaciones están **vectorizadas**. Observa que si para cada fila `i` y columna `j` creamos el par $(X\_{ij}, Y\_{ij})$, ya tenemos la rejilla de puntos creada y almacenada en una matriz _que tiene la misma dimensión que X e Y_. Si ahora hiciésemos

    :::python
    Z = np.cos(X ** 2 + Y ** 2)

en realidad sería como escribir

    :::python
    for i in range(len(X)):
        for j in range(len(Y)):
            Z[i, j] = np.cos(X[i, j] ** 2 + Y[i, j] ** 2)

y en el array _bidimensional_ Z tendríamos los valores de la función coseno _para cada punto de la malla_. Esta forma abreviada de escribir el código es la que se denomina **vectorizada** y funciona porque X, Y y Z tienen la misma dimensión y el mismo tamaño. Es muy importante porque, además de escribir menos código, las operaciones se ejecutan **órdenes de magnitud** más deprisa.

Dicho esto, justamente lo que queremos es la matriz Z donde almacenar el valor de nuestra función para cada uno de los puntos de la malla:

    :::python
    In [7]: from numpy import cos, sinh, log
    In [8]: Z = cos(-10 * X * Y) + sinh(X + Y) - log((3 + X ** 2) / (1 + Y ** 2))
    In [9]: Z
    Out[9]:
    array([[-11.37075265, -10.78189814,  -9.50784471, ...,  -0.77338623,
             -1.42327703,  -1.35287772],
           [-10.87372363,  -9.63560489,  -8.22976433, ...,   0.03672752,
             -0.77839121,  -1.39257702],
           [ -9.69207397,  -8.3221681 ,  -7.36241976, ...,   0.46710156,
              0.06684924,  -0.71210509],
           ...,
           [ -0.95761549,  -0.05567626,   0.46710156, ...,   8.29662289,
              8.33334108,   8.02235339],
           [ -1.51510252,  -0.77839121,   0.15925301, ...,   8.42574485,
              8.07882247,   7.96604409],
           [ -1.35287772,  -1.30075153,  -0.52787582, ...,   8.20658265,
              8.05786958,   8.66499721]])

Ya tenemos la parte de cálculo lista, y ahora sólo queda representar.

## Representación de las líneas de nivel

La biblioteca matplotlib ofrece dos funciones para representar curvas de nivel: [`contour()`](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.contour) y [`contourf()`](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.contourf). La única diferencia entre las dos es que en la primera se representan sólo las líneas, y en la segunda se rellena el espacio entre ellas.

Para obtener ayuda sobre estas funciones sin acudir a la documentación, recuerda que en IPython podemos escribir

    :::python
    In [10]: import matplotlib.pyplot as plt
    In [11]: plt.contour?
    ...

Para crear la figura bastan dos líneas:

    :::python
    In [12]: plt.contour(X, Y, Z)
    Out[12]:
    In [13]: plt.show()

<p style="text-align:center">
  <a href="http://pybonacci.org/images/2012/04/rare_contour.png"><img class="aligncenter  wp-image-164" title="Curvas de nivel" src="http://pybonacci.org/images/2012/04/rare_contour.png" alt="Curvas de nivel" width="448" height="336" srcset="https://pybonacci.org/wp-content/uploads/2012/04/rare_contour.png 800w, https://pybonacci.org/wp-content/uploads/2012/04/rare_contour-300x225.png 300w" sizes="(max-width: 448px) 100vw, 448px" /></a>
</p>

E voilà! Sencillo como siempre 🙂 Incluso podemos rizar más el rizo:

    :::python
    In [14]: cs1 = plt.contourf(X, Y, Z, 25)  # Pintamos 25 niveles con relleno
    In [15]: cs2 = plt.contour(X, Y, Z, cs1.levels, colors='k')  # Añadimos bordes negros
    In [16]: plt.show()

<p style="text-align:center">
  <a href="http://pybonacci.org/images/2012/04/rare_contour_f.png"><img class="aligncenter  wp-image-165" title="Curvas de nivel con relleno" src="http://pybonacci.org/images/2012/04/rare_contour_f.png" alt="Curvas de nivel con relleno" width="448" height="336" srcset="https://pybonacci.org/wp-content/uploads/2012/04/rare_contour_f.png 800w, https://pybonacci.org/wp-content/uploads/2012/04/rare_contour_f-300x225.png 300w" sizes="(max-width: 448px) 100vw, 448px" /></a>
</p>

La biblioteca matplotlib es enorme y da docenas de opciones para configurar la apariencia: colores, ejes... es cuestión de bucear en la documentación y experimentar.

Espero que el artículo os haya resultado útil, no olvidéis recomendar el artículo y hacernos vuestras aportaciones en los comentarios. ¡Nos vemos pronto!