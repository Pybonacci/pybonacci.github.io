---
title: Buscando esa playa en la isla a mediodía (usando Shapely)
date: 2012-09-20T20:38:59+00:00
author: Kiko Correoso
slug: buscando-esa-playa-en-la-isla-a-mediodia-usando-shapely
tags: gis, polígono, python, shapely, shp, sig

Hay un cuento de Julio Cortazar titulado 'la isla a mediodía' en el cual el protagonista, asistente de vuelo, se queda maravillado con una isla en el mar Egeo que sobrevuela a menudo gracias a su trabajo.

Bien, imaginemos por un rato que somos el protagonista del cuento, Marini se llama, que en lugar de sobrevolar el Egeo estamos sobre el Mediterráneo, que la isla es Mallorca en lugar de ser una de las perlas griegas y que sobrevolamos la isla de noroeste a sudeste. Cada vez que pasamos nos quedamos fascinados con esa isla y en especial con una playa que vemos cuando llegamos a la isla.

¿Cómo podemos adivinar cual es esa cala?, ¿cómo podemos conocer el tamaño de la isla?, ¿cómo podemos saber el perímetro de la costa la cual nos gustaría recorrer en bicicleta en nuestras próximas vacaciones?

Una persona normal pensaría, me compro una guía lonely planet, busco en la wikipedia,... Pero ya sabéis que en pybonacci nos falta alguna tuerca y para ello vamos a hacer uso de [Shapely](https://github.com/Toblerity/Shapely), una [librería que nos permite hacer una serie de operaciones típicas del mundo SIG](http://toblerity.github.com/shapely/manual.html) (Sistemas de Información Geográfica, GIS en inglés) sobre espacios bidimensionales. Hay que dejar claro que se usan proyecciones y las operaciones que hacemos, si el espacio geográfico usado es grande, puede sufrir distorsiones importantes y los valores obtenidos podrían distar bastante de los teóricos (avisados estáis, [leer más aquí](http://www.slideshare.net/kikocorreoso/python-gis-mapping)).

[Para esta entrada usamos numpy 1.6, matplotlib 1.1 y  shapely 1.2 en python 2.7]

Shapely permite manejar polígonos, líneas, puntos,..., y permite hacer operaciones con ellos. Primero de todo vamos a descargar la línea de costa de la isla de Mallorca desde <http://www.ngdc.noaa.gov/mgg/coast/>. He usado datos del World Data Bank II a escala 1:2000000 y los he pasado a coordenadas UTM [WGS84](http://es.wikipedia.org/wiki/WGS84) y [subido aquí](http://pybonacci.org/images/2012/09/mallorcautm_wgs84.xls) para que los podáis descargar y reproducir los ejemplos de esta entrada). El fichero a descargar tiene extensión xls pero en realidad es un fichero csv (restricciones de wordpress.com, disculpen las molestias). Las unidades de los datos son metros.

Una vez que tenemos los datos vamos a comenzar los cálculos. Leemos los datos del fichero recién descargados:

    :::python
    import numpy as np
    import matplotlib.pyplot as plt
    from shapely.geometry import Point, LineString, Polygon
    data = np.loadtxt('Mallorca(UTM_WGS84).xls', delimiter=',')

Leídos los datos vamos a crear un objeto 'polígono' y a dibujarlo:

    :::python
    poligono = Polygon(data[:,0:2])
    ## Dibujamos el polígono accediendo a los datos (valores x e y del polígono
    plt.ion()
    plt.plot(list(poligono.exterior.xy)[0], list(poligono.exterior.xy)[1])

Calcular el área y la longitud del polígono es tan sencillo como hacer lo siguiente (los expresamos en km2 y en km, respectivamente):

    :::python
    print poligono.area/(1000.**2), poligono.length/1000.

(vuelvo a avisar, estos valores son una aproximación). Perfecto, ya tenemos nuestra isla soñada. Vamos a por la ruta de nuestro avión para saber por donde llega a la isla. Para ello, vamos a usar un objeto 'línea' y la vamos a dibujar sobre la isla:

    :::python
    linea = LineString([(440000,4410000),(560000,4350000)])
    ## Dibujamos la isla (polígono) y la ruta del avión (línea) accediendo a los valores xy
    plt.plot(list(poligono.exterior.xy)[0], list(poligono.exterior.xy)[1])
    plt.plot(list(linea.xy)[0], list(linea.xy)[1])

Genial, ahora, ¿cómo puedo saber la localización de la ruta del avión sobre la isla?, ¿cómo puedo saber cuantos kilómetros recorre el avión sobre la isla?. Nos ayudaremos de los objetos 'punto'.

    :::python
    ## Para obtener la intersección entre la línea y el polígono
    intersecciones = linea.intersection(poligono)
    ## Sabiendo donde intersecciona la ruta del avión podemos extraer
    ## el punto donde el avión llega a la isla y por donde la abandona
    puntoNW = Point([intersecciones.xy[0][0], intersecciones.xy[1][0]])
    puntoSE = Point([intersecciones.xy[0][1], intersecciones.xy[1][1]])
    ## Imprimimos en pantalla esos valores
    print linea.intersection(poligono)
    ## Y, por último, calculamos la distancia entre los dos puntos
    ## (La distancia que el avión recorre sobre la isla en km)
    print puntoNW.distance(puntoSE)/1000.

Bien, ya sé donde está esa playa que veo cuando estamos llegando a la isla (punto NW). Voy a dibujar la isla (polígono), la ruta del avión (línea) y los puntos donde el avión llega y sale de la isla (punto NW y punto SE, respectivamente):

    :::python
    plt.plot(list(poligono.exterior.xy)[0], list(poligono.exterior.xy)[1])
    plt.plot(list(linea.xy)[0], list(linea.xy)[1])
    plt.plot(intersecciones.xy[0][0], intersecciones.xy[1][0], 'rs')
    plt.plot(intersecciones.xy[0][1], intersecciones.xy[1][1], 'ys')

Con este resultado:

![ejemplo_shapely](http://pybonacci.org/images/2012/09/ejemplo_shapely.png)

Hasta la próxima.