---
title: Usando google earth con ayuda de python y pykml (II)
date: 2013-02-04T20:02:13+00:00
author: Kiko Correoso
slug: usando-google-earth-con-ayuda-de-python-y-pykml-ii
tags: gis, google earth, googleearth, kml, kmz, pykml, python, sig

Esta es la segunda parte de la entrada 'Usando google earth con ayuda de python y pykml (I)'. En el ejemplo de hoy vamos a ver algo más relacionado con la ciencia que lo visto anteriormente, que no era más que un aburrido ejemplo para introduciros en google earth, kml/kmz y pykml.

**[Para esta entrada se ha usado numpy 1.6.1, matplotlib 1.1.1rc, netCDF4 1.0.2, pykml 0.1.0, lxml 2.3.2 (es un prerrequisito de pykml) en el notebook de IPython 0.13 corriendo todo sobre python 2.7.3]**

Primero importamos una serie de cosas que usaremos.

<pre><code class="language-python">import os
from zipfile import ZipFile
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import netCDF4 as nc
from lxml import etree</code></pre>

En este caso vamos a representar el huracán Iván, que se generó en 2004 en el Atlántico occidental y llegó a convertirse en un huracán muy potente. Vamos a representar la evolución de la presión al nivel del mar y las zonas de viento superiores a 50 km/h a medida que vamos viendo la trayectoria del huracán. El valor de viento se obtiene según los datos que vamos a usar, estos datos no son muy rigurosos en este sentido por lo que esto solo sirve como ejemplo.

<a href="http://data-portal.ecmwf.int/data/d/interim_full_daily/" target="_blank">Descargaremos datos</a> de <a href="http://es.wikipedia.org/wiki/Centro_Europeo_de_Previsiones_Meteorol%C3%B3gicas_a_Plazo_Medio" target="_blank">reanálisis del centro europeo de predicción a medio plazo (ECMWF, por sus siglas en inglés, European Center for Medium-range Weather Forecasts)</a> para las fechas de ocurrencia del huracán. Los datos usados en el ejemplo los podéis [descargar de aquí (al fichero le he puesto extensión .gif para poder subirlo a wordpress pero es un fichero netcdf, para que funcione el ejemplo deberéis quitar la extensión gif o cambiar el nombre del fichero en el código)](http://wp.me/a2hEpj-p8).

Ahora importamos todo lo necesario de pykml para este ejemplo:

<pre><code class="language-python">from pykml.factory import nsmap
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX</code></pre>

Ahora vamos a detallar la trayectoria del huracán con su posición, fecha y a en qué categoría se encontraba en cada fecha. La categoría del huracán puede ser de 1 a 5 siendo el 5 el más extremo, según la <a href="http://www.nhc.noaa.gov/aboutsshws.php" target="_blank">escala Saffir-Simpson</a>. En la categoría del huracán también vamos a detallar también los momentos en que no es huracán como tal sino que es tormenta tropical o depresión tropical.

<pre><code class="language-python"># Desde la versión 5.0, google ha añadido una serie de extensiones
# a kml que lo hacen más potente e interactivo
# https://developers.google.com/kml/documentation/kmlreference?hl=es#kmlextensions
# Definimos una variable para el espacio de nombres de las
# extensiones de google que vamos a usar.
gxns = '{' + nsmap['gx'] + '}'
# Ponemos la información referente al  huracán:
# La posición en longitud cada 6h desde que es tormenta tropical
lon_hur = [-30.3, -32.1, -33.6, -35, -36.5, -38.2, -39.9,
           -41.4, -43.4, -45.1, -46.8, -48.5, -50.5, -52.5,
           -54.4, -56.1, -57.8, -59.4, -61.1, -62.6, -64.1,
           -65.5, -67, -68.3, -69.5, -70.8, -71.9, -72.8,
           -73.8, -74.7, -75.8, -76.5, -77.6, -78.4, -79,
           -79.6, -80.4, -81.2, -82.1, -82.8, -83.5, -84.1,
           -84.7, -85.1, -85.6, -86, -86.5, -87, -87.4,
           -87.9, -88.2, -88.2, -87.9, -87.7, -87.4, -86.5,
           -85.7, -84, -82.3, -80.5, -78.5, -76.7, -75.5,
           -74, -74, -74.5, -75.8, -77.5, -78.5, -78.7, -79.1,
           -79.7, -80.6, -81.7, -82.8, -84.1, -86.1, -87.3,
           -88.6, -89.5, -91, -92.2, -92.7, -93.2, -94.2]
# La posición en latitud cada 6h desde que es tormenta tropical
lat_hur = [9.7, 9.5, 9.3, 9.1, 8.9, 8.9, 9, 9.3, 9.5, 9.8,
          10.2, 10.6, 10.8, 11, 11.3, 11.2, 11.3, 11.6,
          11.8, 12, 12.3, 12.6, 13, 13.3, 13.7, 14.2, 14.7,
          15.2, 15.7, 16.2, 16.8, 17.3, 17.4, 17.7, 18,
          18.2, 18.4, 18.8, 19.1, 19.5, 19.9, 20.4, 20.9,
          21.6, 22.4, 23, 23.7, 24.7, 25.6, 26.7, 27.9,
          28.9, 30, 31.4, 32.5, 33.8, 34.7, 35.4, 36.2,
          37, 37.7, 38.4, 38, 37.5, 36, 34.5, 32.8, 31,
          29, 27.5, 26.4, 26.1, 25.9, 25.8, 25.2, 24.8,
          25.1, 26, 26.5, 27.1, 27.9, 28.9, 29.2, 29.6, 30.1]
# El estado del huracan cada 6h
tipo = ['TS','TS','TS','TS','TS','TS','TS',
        'TS','H1','H2','H3','H4','H3','H3',
        'H2','H2','H2','H3','H3','H4','H4',
        'H4','H4','H4','H5','H5','H4','H4',
        'H4','H4','H4','H4','H4','H4','H5',
        'H5','H4','H4','H4','H5','H5','H5',
        'H5','H5','H5','H4','H4','H4','H4',
        'H4','H4','H3','H3','H1','TS','TD',
        'TD','TD','TD','TD','TD','TD','TD',
        'TS','TS','TS','TS','TS','TS','TD',
        'TD','TD','TD','TD','TD','TD','TD',
        'TD','TD','TS','TS','TS','TS','TD','TD']
# La fecha cada 6h desde el 21/09/1998 a las 18Z
fecha_inicial = dt.datetime(2004, 9, 3, 6, 0, 0)
deltat = dt.timedelta(hours = 6)
fechas = [fecha_inicial + deltat * i for i in range(len(tipo))]
# El icono que vamos a asignar a cada 6h, en función del estado de la tormenta.
iconos = {'TD':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/td.gif',
          'TS':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/ts.gif',
          'H1':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/h1.gif',
          'H2':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/h2.gif',
          'H3':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/h3.gif',
          'H4':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/h4.gif',
          'H5':'http://www.srh.noaa.gov/gis/kml/hurricanetrack/hurrhttp://new.pybonacci.org/images/h5.gif'}</code></pre>

Ahora vamos a definir una función que es la que usaremos para dibujar los datos de presión y viento que luego irán en el fichero kml/kmz

<pre><code class="language-python"># Función que crea las imágenes
def pinta_mapas(nombre, lon, lat, mslp, u, v, loni, lati):
    fig = plt.figure()
    fig.set_size_inches(8, 8. * lat.shape[0] / lon.shape[0])
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.contour(lon, lat, mslp / 100., np.arange(900,1100.,2.),
               colors='y',linewidths=2, aspect='normal')
    wspd = np.sqrt(u * u + v * v) * 3.6
    ax.contourf(lon, lat, wspd, np.arange(50, 250, 25),
                colors = plt.hot(), aspect='normal')
    plt.savefig(nombre, dpi = 80, transparent=True)</code></pre>

Y ahora vamos a leer los datos que os hayáis descargado:

<pre><code class="language-python"># Leemos los datos de presión, velocidad, latitud y longitud.
data = nc.Dataset('Usando google earth con ayuda de python y pykml (II)/data.nc')
lon = data.variables['longitude'][:]
lat = data.variables['latitude'][:]
# presión = mslp por mean sea level pressure,
# presión media al nivel del mar
mslp = data.variables['msl'][1:-2,:,:]
lon[lon &gt; 180] = lon - 360
u = data.variables['u10'][1:-2,:,:]
v = data.variables['v10'][1:-2,:,:]</code></pre>

Y ahora es cuando vamos a crear el fichero kml haciendo un bucle donde se van a ir añadiendo cosas tanto a la carpeta (folder) como al Tour. Voy explicándo lo que hace cada cosa mediante comentarios en el código:

<pre><code class="language-python"># Como vamos a crear un fichero kmz que incluirá todas las imágenes
# abrimos el fichero kmz donde iremos guardándolo todo
fich_kmz = ZipFile('HuracanIvan.kmz', 'w')
# Desde la versión 5.0, google ha añadido una serie de extensiones
# a kml que lo hacen más potente e interactivo
# https://developers.google.com/kml/documentation/kmlreference?hl=es#kmlextensions
# Definimos una variable para el espacio de nombres de las
# extensiones de google que vamos a usar.
gxns = '{' + nsmap['gx'] + '}'
# start with a base KML tour and playlist
fich_kml = KML.kml(
    KML.Document(
      GX.Tour(
        KML.name(u"¡Reprodúceme!"),
        GX.Playlist(),
      ),
      KML.Folder(
        KML.name('Ruta del huracan Ivan'),
        id='lugares',
      ),
    )
)
# Hacemos un bucle para recorrer todos los 'momentos'
# del huracán definidos en el bloque de código anterior
for i in range(len(tipo)):
    # Primero volamos hasta cada posición del huracán (cada 6h)
    # y nos quedamos observándolo desde el espacio
    # A unos 2000 km de altura.
    # Para ello usamos FlyTo donde especificamos
    # La duración en segundos, si queremos que vaya más rápido o más
    # lento, el modo de vuelo, que puede ser más suave (smooth) o
    # más rápido (bounce) y la posición.
    # La posición la determinan longitude, latitude y altitude,
    # tilt es el ángulo desde la vertical (en este caso lo vemos
    # verticalmente (0º)) y range es la distancia desde la posición
    # determinada por longitude, latitude y altitude, teniendo en
    # cuenta el ángulo tilt (en este caso hemos puesto 2.000 km)
    # Las unidades para latitude y longitude son grados, para altitude
    # y range son metros y para tilt son grados desde la vertical.
    # En el gráfico de este enlace se verá mejor:
    # https://developers.google.com/kml/documentation/http://new.pybonacci.org/images/lookAt.gif
    fich_kml.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(1),
        GX.flyToMode("bounce"),
        KML.LookAt(
          KML.longitude(lon_hur[i]),
          KML.latitude(lat_hur[i]),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(0),
          KML.range(10000000.0),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )
    fich_kml.Document[gxns+"Tour"].Playlist.append(GX.Wait(GX.duration(0.1)))
    # Añadimos información de cada lugar en la carpeta
    # como 'placemarks' o marcas de posición. En el nombre y en la descripción
    # del placemark se puede meter HTML y CSS, por si queréis ser un poco más
    # creativos y dejar la información de una forma visible y bonita.
    # extrude == 1 indica que el nombre del lugar se hará visible. Si queremos
    # hacerlo visible solo cuando lo seleccionemos pues le ponemos el valor 0
    desc = '&lt;![CDATA[{0}
lon: {1}
lat: {2}
Estado del huracan: {3}]]&gt;'
    desc = desc.format(fechas[i].isoformat()[0:13], lon_hur[i], lat_hur[i], tipo[i])
    fich_kml.Document.Folder.append(
      KML.Placemark(
        KML.name(fechas[i].isoformat()[0:13]),
        KML.description(
            "{0}&lt;br/&gt;{1}".format('IVAN', desc,)
        ),
        KML.Style(
          KML.IconStyle(
            KML.Icon(KML.href(iconos[tipo[i]]),)
          ),
        ),
        KML.Point(
          KML.extrude(1),
          KML.altitudeMode("relativeToGround"),
          KML.coordinates("{0},{1},0".format(lon_hur[i],
                                             lat_hur[i],)
          ),
        ),
        id=fechas[i].isoformat()[0:13]
      )
    )
    # Aquí le indicamos a la reproducción que nos
    # muestre el 'globo' o 'viñeta' con la información del sitio,
    # nombre y descripción. Visibility a 1 para
    # hacerlo visible.
    fich_kml.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(1.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.Placemark(
                KML.visibility(1),
                GX.balloonVisibility(1),
                targetId=fechas[i].isoformat()[0:13]
              )
            )
          )
        )
    )
    # creamos el mapa
    nombre = '{0}.png'.format(fechas[i].isoformat()[0:13])
    pinta_mapas(nombre, lon, lat, mslp[i,:,:], u[i,:,:], v[i,:,:], lon_hur[i], lat_hur[i])
    # añadimos el mapa al fichero kmz
    fich_kmz.write(nombre)
    # y eliminamos el fichero png
    os.remove(nombre)
    # añadimos la ruta de las imágenes en el
    # fichero kml (que estará contenido dentro
    # del fichero kmz.
    fich_kml.Document.Folder.append(
      KML.GroundOverlay(
        KML.name(nombre),
        KML.visibility(0),
        KML.Icon(KML.href(nombre)),
        KML.LatLonBox(KML.north(np.max(lat)),
                      KML.south(np.min(lat)),
                      KML.east(np.max(lon)),
                      KML.west(np.min(lon)),
        ),
        id = nombre
      )
    )
    fich_kml.Document[gxns+"Tour"].Playlist.append(GX.Wait(GX.duration(0.1)))
    # Aquí le indicamos a la reproducción que nos
    # muestre el 'mapa'. Visibility a 1 para
    # hacerlo visible.
    fich_kml.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(1.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.GroundOverlay(
                KML.visibility(1),
                #GX.balloonVisibility(1),
                targetId=nombre
              )
            )
          )
        )
    )
    # Esta parte de código hará que desaparezca el 'globo'
    # con la información así no tendremos el 'globo'
    fich_kml.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(0.1),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.Placemark(
                GX.balloonVisibility(0),
                targetId=fechas[i].isoformat()[0:13]
              )
            )
          )
        )
    )
    # Esta parte de código hará que desaparezca el 'mapa'
    fich_kml.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(1.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.GroundOverlay(
                KML.visibility(0),
                targetId=nombre
              )
            )
          )
        )
    )</code></pre>

En el siguiente código lo que hacemos es guardar el fichero kml final. Si os acordáis, en algún momento hemos puesto algunas etiquetas HTML. Algunos símbolos especiales se han transformado por lo que los volvemos a dejar como estaban ya que si no google earth no entenderá ese kml correctamente.

<pre><code class="language-python"># guardamos toda la información
# del kml en un fichero kml
outfile = file('HuracanIvan.kml','w')
salida = etree.tostring(fich_kml, pretty_print=True)
salida = salida.replace('&lt;code&gt;&lt;&lt;/code&gt;', '&lt;') salida = salida.replace('&lt;code&gt;&gt;&lt;/code&gt;', '&gt;')
outfile.write(salida)
outfile.close()
# guardamos el fichero kml dentro del
# fichero kmz
fich_kmz.write('HuracanIvan.kml')
# Eliminamos el fichero kml
os.remove('HuracanIvan.kml')
# Cerramos el fichero kmz
fich_kmz.close()</code></pre>

Por último, lanzamos google earth con el fichero que acabamos de crear. Las siguientes tres líneas funcionan en linux. Ahora mismo no tengo un windows cerca pero creo que deberéis cambiar googleearth por googleearth.exe y tener en cuenta los '' en lugar de '/' en la ruta al fichero.

<pre><code class="language-python">ruta = os.getcwd()
rutafich = ruta + '/HuracanIvan.kmz'
os.system('googleearth {0}'.format(rutafich))</code></pre>

A la izquierda de la pantalla de google earth, en mis 'lugares', dentro de 'lugares temporales' podréis ver 'HuracanIvan.kmz'. Si lo desplegáis veréis 'Reprodúceme'. Si hacéis doble click sobre 'Reprodúceme' podréis ver algo parecido a lo siguiente:

[youtube=http://www.youtube.com/watch?v=TPKZo4ez1V0]

El resultado tampoco es maravilloso pero la idea no era el resultado, la idea era mostrar el uso de pykml e introducir un poco de kml/kmz a los que les pueda resultar útil.

Por último, como comenté en el anterior capítulo, os dejo un enlace con un uso creativo de google earth [1].

[1] - http://www.fosslc.org/drupal/content/pykml-python-kml-library

P.D.: Como puede que wordpress me haya 'estropeado' algo al hacer copy&paste os dejo el enlace al [ipython notebook](https://gist.github.com/4708735) o lo podéis visualizar directamente en [nbviewer](http://nbviewer.ipython.org/4708735/).