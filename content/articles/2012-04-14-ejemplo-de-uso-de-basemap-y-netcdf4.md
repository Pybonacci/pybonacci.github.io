---
title: Ejemplo de uso de Basemap y NetCDF4
date: 2012-04-14T12:14:50+00:00
author: Kiko Correoso
slug: ejemplo-de-uso-de-basemap-y-netcdf4
tags: basemap, mapas, matplotlib, meteorología, netcdf, netcdf4-python, numpy, python

Continuando lo que enseñó Juanlu en la anterior entrada vamos a mostrar líneas de nivel y temperatura del aire en la superficie, en este caso la presión al nivel del mar del día 01 de enero de 2012 a las 00.00 UTC según los datos extraídos del [reanálisis NCEP/NCAR](http://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis.html), sobre un mapa con la ayuda de la librería [Basemap](http://matplotlib.github.com/basemap/).

Como los datos del reanálisis NCEP/NCAR vienen en formato [netCDF](http://www.unidata.ucar.edu/software/netcdf/) usaremos la librería [netcdf4-python](https://unidata.github.io/netcdf4-python/). El formato netCDF es un estándar abierto y es ampliamente usado en temas de ciencias de la tierra, atmósfera, climatología, meteorología,... No es estrictamente necesario usar netcdf4-python para acceder a ficheros netCDF puesto que desde [scipy tenéis esta funcionalidad](https://docs.scipy.org/doc/scipy/reference/tutorial/io.html#module-scipy.io.netcdf). Pero bueno, yo uso esta por una serie de ventajas que veremos otro día.

**En la presente entrada se ha usado python 2.7.2, numpy 1.6.1, matplotlib 1.1.0, netCDF4 0.9.7 y Basemap 1.0.2.**

Primero de todo vamos a importar todo lo que necesitamos:

    :::python
    ## Importamos las librerías que nos hacen falta
    import numpy as np
    import netCDF4 as nc
    import matplotlib.pyplot as plt
    from mpl_toolkits import basemap as bm

Los ficheros netCDF de presión al nivel del mar y de Temperatura del aire de la superficie los podéis descargar de [aquí](https://www.esrl.noaa.gov/psd/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+102476&variable=slp&DB_vid=30&DB_tid=66680&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2010&mon_begin=Jan&day_begin=1&hour_begin=00+Z&year_end=2010&mon_end=Jan&day_end=1&hour_end=00+Z&X=lon&Y=lat&output=file&bckgrnd=black&use_color=on&fill=lines&cint=&range1=&range2=&scale=100&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data) y [aquí](https://www.esrl.noaa.gov/psd/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fair.sig995.1948.nc+air.sig995.%25y4.nc+102476&variable=air&DB_vid=20&DB_tid=66680&units=degK&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2010&mon_begin=Jan&day_begin=1&hour_begin=00+Z&year_end=2010&mon_end=Jan&day_end=1&hour_end=00+Z&X=lon&Y=lat&output=file&bckgrnd=black&use_color=on&fill=lines&cint=&range1=&range2=&scale=100&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data), respectivamente. Veréis un enlace que pone 'FTP a copy of the file', lo pincháis y guardáis en el mismo sitio donde tengáis el script que estamos haciendo en la presente entrada.

Una vez que tenemos los ficheros los podemos abrir usando la librería netCDF4-python:

    :::python
    ## Abrimos los ficheros de datos,
    ## el nombre de los ficheros lo tendréis que cambiar
    ## con el nombre de los ficheros que os habéis descargado
    slp = nc.Dataset('X83.34.8.250.104.4.18.19.nc') #slp por 'sea level pressure'
    tsfc = nc.Dataset('X83.34.8.250.104.4.15.31.nc') #tsfc 'por temperature at surface'

Para saber las variables que tenemos en cada fichero netCDF podemos escribir lo siguiente:

    :::python
    ## Qué variables hay dentro de cada netCDF
    print(slp.variables)
    print(tsfc.variables)

El output que veremos para slp será:

    :::python
    OrderedDict([(u'lat', &lt;netCDF4.Variable object at 0x05F72FA8&gt;), (u'lon', &lt;netCDF4.Variable object at 0x0603C198&gt;), (u'time', &lt;netCDF4.Variable object at 0x0603C150&gt;), (u'slp', &lt;netCDF4.Variable object at 0x060A1FA8&gt;)])

De la misma forma, para tsfc tendremos:

    :::python
    OrderedDict([(u'lat', &lt;netCDF4.Variable object at 0x060AE108&gt;), (u'lon', &lt;netCDF4.Variable object at 0x060AE030&gt;), (u'time', &lt;netCDF4.Variable object at 0x060AE078&gt;), (u'air', &lt;netCDF4.Variable object at 0x060AE150&gt;)])

Nos interesa acceder a las variables 'slp', 'air', 'lat'  y 'lon'. Las dos últimas variables son las mismas tanto en slp como en tsfc ya que nos hemos descargado el campo de presión y temperatura para la misma fecha y para la misma área. Por tanto, para acceder a los datos y poder dibujarlos hacemos lo siguiente:

    :::python
    slpdata = slp.variables['slp'][:] #Obtenemos los datos en Pa
    tsfcdata = tsfc.variables['air'][:] #Obtenemos los datos en ºK
    lat = slp.variables['lat'][:] #Obtenemos los datos en º
    lon = slp.variables['lon'][:] #Obtenemos los datos en º

Los datos se han guardado en las variables slpdata, tsfcdata, lat y lon como numpy arrays. Para que la presión esté en hPa  o mb (hectopascales o milibares), la temperatura en ºC y las longitudes vayan en una escala de -180º a 180º hacemos lo siguiente:

    :::python
    slpdata = slpdata * 0.01
    tsfcdata = tsfcdata - 273.15
    lon[lon &gt; 180] = lon - 360.

Ahora creamos una instancia a Basemap:

    :::python
    m = bm.Basemap(llcrnrlon = -20,
                   llcrnrlat = 25,
                   urcrnrlon = 60,
                   urcrnrlat = 80,
                   projection = 'mill')

En el anterior código hemos puesto lo siguiente:

|      llcrnrlon        longitud de la esquina inferior izquierda del dominio del mapa seleccionado.
  
|      llcrnrlat        latitud de la esquina inferior izquierda del dominio del mapa seleccionado.
  
|      urcrnrlon        longitud de la esquina superior derecha del dominio del mapa seleccionado.
  
|      urcrnrlat        latitud de la esquina superior derecha del dominio del mapa seleccionado.

Para _projection_ hemos usado _mill_ que será para una proyección [Miller cylindrical](http://en.wikipedia.org/wiki/Miller_cylindrical_projection). Si queréis ver todas las proyecciones disponibles podéis escribir:

    :::python
    print(bm.supported_projections)

Y veréis el siguiente output:

    :::python
    aeqd             Azimuthal Equidistant
    poly             Polyconic
    gnom             Gnomonic
    moll             Mollweide
    tmerc            Transverse Mercator
    nplaea           North-Polar Lambert Azimuthal
    gall             Gall Stereographic Cylindrical
    mill             Miller Cylindrical
    merc             Mercator
    stere            Stereographic
    npstere          North-Polar Stereographic
    hammer           Hammer
    geos             Geostationary
    nsper            Near-Sided Perspective
    vandg            van der Grinten
    laea             Lambert Azimuthal Equal Area
    mbtfpq           McBryde-Thomas Flat-Polar Quartic
    sinu             Sinusoidal
    spstere          South-Polar Stereographic
    lcc              Lambert Conformal
    npaeqd           North-Polar Azimuthal Equidistant
    eqdc             Equidistant Conic
    cyl              Cylindrical Equidistant
    omerc            Oblique Mercator
    aea              Albers Equal Area
    spaeqd           South-Polar Azimuthal Equidistant
    ortho            Orthographic
    cass             Cassini-Soldner
    splaea           South-Polar Lambert Azimuthal
    robin            Robinson

Buscamos los valores x e y que representarán a las latitudes y longitudes de la proyección del mapa seleccionada:

    :::python
    ## Encontramos los valores x,y para el grid de la proyección del mapa.
    lon, lat = np.meshgrid(lon, lat)
    x, y = m(lon, lat)

Vamos a representar el campo de presiones en el mapa:

    :::python
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.05,0.05,0.9,0.85])
    cs = m.contour(x,y,slpdata[0,:,:],np.arange(900,1100.,5.),colors='y',linewidths=1.25)
    m.drawparallels(np.arange(0,360,10),labels=[1,1,0,0])
    m.drawmeridians(np.arange(-180,180,10),labels=[0,0,0,1])
    m.bluemarble()
    plt.show()

Este último código mostrará la siguiente figura:

![Ejemplo_BlueMarble](http://pybonacci.org/images/2012/04/ejemplo_bluemarble.png)

En el anterior mapa hemos mostrado las líneas de nivel de la presión, hemos dibujado meridianos y paralelos y lo hemos representado con una proyección cilíndrica de Miller usando como fondo los datos [Blue Marble de la NASA](http://en.wikipedia.org/wiki/The_Blue_Marble).

Ahora vamos a introducir también los datos de temperatura usando contourf (la f viene de fill, relleno y son contornos rellenados). Metemos lo siguiente en nuestro script:

    :::python
    # create figure.
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.05,0.05,0.9,0.85])
    cs = m.contour(x,y,slpdata[0,:,:],np.arange(900,1100.,5.),colors='k',linewidths=1.)
    csf = m.contourf(x,y,tsfcdata[0,:,:],np.arange(-50,50.,2.))
    m.drawcoastlines(linewidth=1.25, color='grey')
    m.drawparallels(np.arange(0,360,10),labels=[1,1,0,0])
    m.drawmeridians(np.arange(-180,180,10),labels=[0,0,0,1])
    plt.show()

Y obtenemos el siguiente resultado:

![Ejemplo_P_y_T](http://pybonacci.org/images/2012/04/ejemplo_p_y_t.png)

Donde hemos representado la presión al nivel del mar (isolíneas en color negro), las temperaturas en superficie (contornos de color rellenos), las líneas de costa (líneas continuas grises), paralelos y meridianos.

El script final quedaría algo así:

    :::python
    ## Importamos las librerías que vamos a usar
    import numpy as np
    import netCDF4 as nc
    import matplotlib.pyplot as plt
    from mpl_toolkits import basemap as bm
    ## Abrimos los ficheros de datos
    slp = nc.Dataset('X83.34.8.250.104.4.18.19.nc') #slp por 'sea level pressure'
    tsfc = nc.Dataset('X83.34.8.250.104.4.15.31.nc') #tsfc 'por temperature at surface'
    print(slp.variables)
    print(tsfc.variables)
    slpdata = slp.variables['slp'][:] #Obtenemos los datos en Pa
    tsfcdata = tsfc.variables['air'][:] #Obtenemos los datos en ºK
    lat = slp.variables['lat'][:] #Obtenemos los datos en º
    lon = slp.variables['lon'][:] #Obtenemos los datos en º
    slpdata = slpdata * 0.01
    tsfcdata = tsfcdata - 273.15
    lon[lon &gt; 180] = lon - 360.
    ## Creamos una instancia a Basemap
    m = bm.Basemap(llcrnrlon = -20,
                   llcrnrlat = 25,
                   urcrnrlon = 60,
                   urcrnrlat = 80,
                   projection = 'mill')
    print(bm.supported_projections)
    ## Encontramos los valores x,y para el grid de la proyección del mapa.
    lon, lat = np.meshgrid(lon, lat)
    x, y = m(lon, lat)
    # Creamos la figura con P sobre fondo Blue Marble.
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.05,0.05,0.9,0.85])
    cs = m.contour(x,y,slpdata[0,:,:],np.arange(900,1100.,5.),colors='y',linewidths=1.25)
    m.drawparallels(np.arange(0,360,10),labels=[1,1,0,0])
    m.drawmeridians(np.arange(-180,180,10),labels=[0,0,0,1])
    m.bluemarble()
    plt.show()
    # Creamos la figura con P y T.
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.05,0.05,0.9,0.85])
    cs = m.contour(x,y,slpdata[0,:,:],np.arange(900,1100.,5.),colors='k',linewidths=1.)
    csf = m.contourf(x,y,tsfcdata[0,:,:],np.arange(-50,50.,2.))
    m.drawcoastlines(linewidth=1.25, color='grey')
    m.drawparallels(np.arange(0,360,10),labels=[1,1,0,0])
    m.drawmeridians(np.arange(-180,180,10),labels=[0,0,0,1])
    plt.show()

Y eso es todo por hoy. En algún momento, siempre que el tiempo lo permita, veremos más en profundidad Basemap y Netcdf4-python.

Saludos.

P.D.: Lo de siempre, si encontráis errores, queréis criticar (constructivamente) mis bajas dotes como programador o queréis aportar alguna cosa usad los comentarios.
