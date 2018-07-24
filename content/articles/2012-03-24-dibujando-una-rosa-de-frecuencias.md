---
title: Dibujando una rosa de frecuencias
date: 2012-03-24T13:46:44+00:00
author: Kiko Correoso
slug: dibujando-una-rosa-de-frecuencias
tags: gráficos, math, matplotlib, numpy, python, python 2

**[Este post ha sido actualizado para usar nuevas funcionalidades de matplotlib. Pincha sobre este enlace para ver la nueva versión.](http://pybonacci.org/2014/07/31/dibujando-una-rosa-de-frecuencias-reloaded-3/)**

_**Para la siguiente entrada se ha usado python 2.7.2, math (de la librería estándar), numpy 1.6.1 y matplotlib 1.1.0**_

Imaginaos que estáis de vacaciones en Agosto en la playa y la única preocupación que tenéis es observar las nubes. Como sois un poco frikis y no podéis desconectar de vuestra curiosidad científica decidís apuntar las ocurrencias de la procedencia de las nubes y al final de las vacaciones decidís representar esos datos. La forma más normal de hacerlo sería usando una rosa de frecuencias.

Primero de todo vamos a importar los módulos que nos harán falta:

    :::python
    ## De la librería estándar
    import math
    ## De librerías de terceros
    import numpy as np
    import matplotlib.pyplot as plt

A continuación creamos nuestra muestra de datos totalmente inventada. Para ello vamos a usar el módulo random incluido en numpy:

    :::python
    ## Creamos un conjunto de 1000 datos entre 0 y 1 de forma aleatoria
    ## a partir de una distribución estándar normal
    datos = np.random.randn(1000)
    ## Discretizamos el conjunto de valores en n intervalos,
    ## en este caso 8 intervalos
    datosbin = np.histogram(datos,
                           bins = np.linspace(np.min(datos), np.max(datos), 9))[0]
    ## Los datos los queremos en tanto por ciento
    datosbin = datosbin * 100. / len(datos)

En el bloque anterior de código lo único que hemos hecho es obtener una muestra aleatoria de una distribución normal y la hemos separado en 8 intervalos que pretenden ser las 8 direcciones de donde provienen las nubes empezando por el Norte y en el sentido de las agujas del reloj. Finalmente los datos los expresamos como frecuencia en tanto por ciento en cada una de las 8 direcciones.

Matplotlib nos permite hacer gráficos polares pero estos gráficos están pensados para gráficos en sentido contrario a las agujas del reloj y empezando a las tres en punto (o al este). Por ello debemos modificar como se verán los datos en el gráfico polar. Para ello hacemos lo siguiente:

    :::python
    ## Los datos los queremos en n direcciones/secciones/sectores,
    ## en este caso usamos 8 sectores de una circunferencia
    sect = np.array([90, 45, 0, 315, 270, 225, 180, 135]) * 2. * math.pi / 360.
    nombresect = ['E','NE','N','NW','W','SW','S','SE']

[Actualización: después de escribir este script he vsto que desde la versión 1.1 de matplotlib se puede definir como quieres que sean los ejes en un gráfico polar. Podéis investigar por vuestra cuenta con la información de este [enlace](http://matplotlib.sourceforge.net/devel/add_new_projection.html#matplotlib.projections.polar.PolarAxes).]

Por último solo nos queda dibujar la rosa de frecuencias:

    :::python
    ## Dibujamos la rosa de frecuencias
    plt.axes([0.1,0.1,0.8,0.8], polar = True)
    plt.bar(sect, datosbin, align='center', width=45 * 2 * math.pi / 360.,
            facecolor='b', edgecolor='k', linewidth=2, alpha=0.5)
    plt.thetagrids(np.arange(0, 360, 45),nombresect,frac = 1.1, fontsize = 10)
    plt.title(u'Procedencia de las nubes en marzo')
    plt.show()

Definimos el tipo de gráfico y el área que ocupará. definimos colores de las barras, anchos de las líneas, transparencia de las barras,..., colocamos el nombre de la dirección en cada sector definido (en este caso hemos usado 8 sectores), ponemos un título a nuestro gráfico y hemos acabado.

![Rosa de frecuencias de las nubes durante mis últimas vacaciones](http://new.pybonacci.org/images/2012/03/rosafrecuencias.png)

Vuestra gráfica no tiene porque ser igual a esta, recordad que los datos los obtenemos de una muestra aleatoria.

Aquí os dejo el script completo:

    :::python
    ## Importamos las librerías que necesitamos
    ## De la librería estándar
    import math
    ## De librerías de terceros
    import numpy as np
    import matplotlib.pyplot as plt
    ## Creamos un conjunto de 1000 datos entre 0 y 1 de forma aleatoria
    ## a partir de una distribución estándar normal
    datos = np.random.randn(1000)
    ## Discretizamos el conjunto de valores en n intervalos,
    ## en este caso 8 intervalos
    datosbin = np.histogram(datos,
                           bins = np.linspace(np.min(datos), np.max(datos), 9))[0]
    ## Los datos los queremos en tanto por ciento
    datosbin = datosbin * 100. / len(datos)
    ## Los datos los queremos en n direcciones/secciones/sectores,
    ## en este caso usamos 8 sectores de una circunferencia
    sect = np.array([90, 45, 0, 315, 270, 225, 180, 135]) * 2. * math.pi / 360.
    nombresect = ['E','NE','N','NW','W','SW','S','SE']
    ## Dibujamos la rosa de frecuencias
    plt.axes([0.1,0.1,0.8,0.8], polar = True)
    plt.bar(sect, datosbin, align='center', width=45 * 2 * math.pi / 360.,
            facecolor='b', edgecolor='k', linewidth=2, alpha=0.5)
    plt.thetagrids(np.arange(0, 360, 45),nombresect,frac = 1.1, fontsize = 10)
    plt.title(u'Procedencia de las nubes en marzo')
    plt.show()

Saludos.