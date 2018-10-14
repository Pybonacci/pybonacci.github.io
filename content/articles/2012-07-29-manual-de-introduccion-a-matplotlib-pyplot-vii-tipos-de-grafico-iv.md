---
title: Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)
date: 2012-07-29T10:36:08+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv
tags: basemap, gráficos, matplotlib, matplotlib.pyplot, netcdf4, pyplot, python, thredds, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](https://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](https://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](https://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](https://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](https://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. [Tipos de gráfico III](https://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. **[Tipos de gráfico IV](https://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")**
  8. [Texto y anotaciones (arrow, annotate, table, text...)](https://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")
  9. <del>Herramientas estadísticas (acorr, cohere, csd, psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. [Miscelánea](https://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1, matplotlib 1.1.0, netcdf4-python 0.9.9 y Basemap 1.0.2]**

[DISCLAIMER: Muchos de los gráficos que vamos a representar no tienen ningún sentido físico y los resultados solo pretenden mostrar el uso de la librería].

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

    :::python
    import matplotlib.pyplot as plt
    import numpy as np
    import netCDF4 as nc
    from mpl_toolkits.basemap import Basemap as Bm

Hasta ahora hemos visto como configurar las ventanas, manejo de las mismas, definir áreas de gráfico, algunos tipos de gráficos... Ahora vamos a ver un último capítulo sobre tipos de gráficos. En esta última entrada sobre los tipos de gráfico hemos metido gráficos que quizá no estén muy relacionados entre sí por lo que quizá este capítulo puede parecer un poco cajón desastre.

<!--more-->

[Anteriormente](https://pybonacci.org/2012/04/14/ejemplo-de-uso-de-basemap-y-netcdf4/) ya hemos usado [Basemap](http://matplotlib.github.com/basemap/), un toolkit que da capacidades de generar mapas a matplotlib. En este momento vamos a volver a recurrir a esta librería para mostrar datos sobre mapas. En el primer caso vamos a dibujar gráficos de barbas de viento ([wind barbs](http://en.wikipedia.org/wiki/Station_model#Plotted_winds)) sobre un mapa. También vamos a usar la librería [netcdf4-python,](https://unidata.github.io/netcdf4-python/) que permite leer, modificar y crear ficheros [netcdf](http://www.unidata.ucar.edu/software/netcdf/) así como descargarlos desde diferentes TDS (servidores de datos [THREDDS](https://www.unidata.ucar.edu/software/thredds/current/tds/)) de forma muy sencilla. Los datos que usaremos serán datos de viento obtenidos del reanálisis [CFSR](http://journals.ametsoc.org/doi/pdf/10.1175/2010BAMS3001.1) de la atmósfera pero podéis usar cualquier otro tipo de datos que se os ocurra:

    :::python
    plt.ion()  # Ponemos el modo interactivo
    url = 'http://nomads.ncdc.noaa.gov/thredds/dodsC/cfsr1hr/200912/wnd10m.l.gdas.200912.grb2' # Ruta al fichero que usaremos
    datos = nc.Dataset(url) # Accedemos a los datos

El fichero al que hemos accedido no es un fichero netcdf, sino que tiene formato [grib2](http://www.wmo.int/pages/prog/www/WMOCodes/Guides/GRIB/GRIB2_062006.pdf), pero netcdf4-python es 'todoterreno' y nos permite también acceder a este tipo de ficheros. Los datos a los que corresponden a diciembre de 2009 con pasos temporales de 6 horas. Usaremos solo el campo de vientos que corresponde a las 00:00 UTC del 01/12/2009. Si ponéis en el prompt datos.variables veréis un diccionario con las variables disponibles. Vamos a usar 'U-component\_of\_wind', 'V-component\_of\_wind', 'lon' y 'lat'.

    :::python
    u = datos.variables['U-component_of_wind'][0,:,:,:] # Guardamos en memoria el valor u del vector de viento para las 00:00 UTC del 01/12/2009
    v = datos.variables['V-component_of_wind'][0,:,:,:] # Guardamos en memoria el valor v del vector de viento para las 00:00 UTC del 01/12/2009
    lon = datos.variables['lon'][:] # Guardamos los valores de longitud
    lat = datos.variables['lat'][:] # Guardamos los valores de latitud
    lons, lats = np.meshgrid(lon, lat) # Hacemos una malla regular 2D para las latitudes y las longitudes

Una vez que disponemos de todas las variables pasamos a hacer el gráfico representando las barbas de viento. Como en diciembre hace mucho frío por Europa vamos a ver los vientos veraniegos que tuvimos en América Central y en América del sur durante en esa fecha.

    :::python
    m = Bm(llcrnrlon = 230, llcrnrlat = -60, urcrnrlon = 340, urcrnrlat = 38, projection = 'mill') # Definimos el área del gráfico y la proyección
    m.drawparallels(np.arange(-180,180,10),labels=[1,1,0,0]) # Dibujamos los paralelos
    m.drawmeridians(np.arange(0,360,10),labels=[0,0,0,1]) # Dibujamos los meridianos
    m.bluemarble() # Ponemos un mapa 'bonito' de fondo
    x, y = m(lons, lats)
    m.barbs(x,y,u[0,:,:],v[0,:,:],length=5,barbcolor='w',flagcolor='w',linewidth=0.5) # Y dibujamos los valores del vector viento

El resultado quedaría de la siguiente forma:

![barbs](https://pybonacci.org/images/2012/07/barbs.png)

Y un detalle de la parte sur:

![barbs_detalle](https://pybonacci.org/images/2012/07/barbs_detalle.png)

El código completo del ejemplo:

    :::python
    import matplotlib.pyplot as plt
    import numpy as np
    import netCDF4 as nc
    from mpl_toolkits.basemap import Basemap as Bm
    plt.ion()  # Ponemos el modo interactivo
    url = 'http://nomads.ncdc.noaa.gov/thredds/dodsC/cfsr1hr/200912/wnd10m.l.gdas.200912.grb2' # Ruta al fichero que usaremos
    datos = nc.Dataset(url) # Accedemos a los datos
    u = datos.variables['U-component_of_wind'][0,:,:,:] # Guardamos en memoria el valor u del vector de viento para las 00:00 UTC del 01/12/2009
    v = datos.variables['V-component_of_wind'][0,:,:,:] # Guardamos en memoria el valor v del vector de viento para las 00:00 UTC del 01/12/2009
    lon = datos.variables['lon'][:] # Guardamos los valores de longitud
    lat = datos.variables['lat'][:] # Guardamos los valores de latitud
    lons, lats = np.meshgrid(lon, lat) # Hacemos una malla regular 2D para las latitudes y las longitudes
    m = Bm(llcrnrlon = 230, llcrnrlat = -60, urcrnrlon = 340, urcrnrlat = 38, projection = 'mill') # Definimos el área del gráfico y la proyección
    m.drawparallels(np.arange(-180,180,10),labels=[1,1,0,0]) # Dibujamos los paralelos
    m.drawmeridians(np.arange(0,360,10),labels=[0,0,0,1]) # Dibujamos los meridianos
    m.bluemarble() # Ponemos un mapa 'bonito' de fondo
    x, y = m(lons, lats)
    m.barbs(x,y,u[0,:,:],v[0,:,:],length=5,barbcolor='w',flagcolor='w',linewidth=0.5) # Y dibujamos los valores del vector viento

En realidad no hemos usado 'matplotlib.pyplot.barbs' sino que hemos hecho uso de 'barbs' dentro de 'basemap' pero su uso es similar. Si no queréis dibujar barbas y queréis dibujar flechas echadle un ojo a matplotlib.pyplot.quiver y a matplotlib.pyplot.quiverkey (aquí tenéis ejemplos que os pueden ayudar <http://matplotlib.github.com/basemap/users/examples.html>).

Podéis encontrar muchos ejemplos de como usar matplotlib.pyplot (en algunos casos usando pylab) en [http://matplotlib.sourceforge.net/examples/pylab_examples/index.html.](http://matplotlib.sourceforge.net/examples/pylab_examples/index.html)

Y, después de este breve entrada, hemos acabado por hoy y hemos acabado los tipos de gráfico que vamos a ver. Esto ha sido solo una muestra de las cosas que se suelen usar más. El próximo día veremos como hacer anotaciones en un gráfico. Si quieres ver las [anteriores entregas del tutorial pulsa aquí](https://pybonacci.org/tag/tutorial-matplotlib-pyplot/).
