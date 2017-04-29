---
title: Basemap y Google Geocode para representar puntos sobre un mapa
date: 2014-10-07T12:27:15+00:00
author: Pablo Fernández
slug: basemap-y-google-geocode-para-representar-puntos-sobre-un-mapa
tags: basemap, circuitos, formula 1, google geocode

Como siempre, en GitHub podréis encontrar el <a href="http://nbviewer.ipython.org/github/pybonacci/notebooks/blob/master/basemap/Basemap.ipynb" target="_blank">notebook</a> y los <a href="https://github.com/pybonacci/notebooks/tree/master/basemap" target="_blank">ficheros adicionales</a> que forman parte de éste artículo.

Las gráficas pueden proporcionar mucha información de un sólo vistazo, pero no siempre son el mejor método de representación. A veces es necesario dar un paso más; y ese es precisamente el caso que vamos a tratar en éste artículo.

Representar valores sobre un mapa geográfico nos permite ubicar la información sobre el terreno. Lo datos a representar pueden ser desde contornos de temperatura hasta vectores de velocidad del viento pasando por la identificación de puntos geográficos. Para facilitarnos todo ese trabajo —en Python— disponemos de una serie de librerías. [PyNGL](http://www.pyngl.ucar.edu/), [CDAT](http://www-pcmdi.llnl.gov/software/cdat/support/vcs/vcs.html) o [Basemap](http://matplotlib.org/basemap/index.html) —del que Kiko ya ha hablado en <a href="http://pybonacci.org/2012/04/14/ejemplo-de-uso-de-basemap-y-netcdf4/" title="Ejemplo de uso de Basemap y NetCDF4 | Pybonacci" target="_blank">ésta entrada</a>— son librerías que nacieron para satisfacer las necesidades de ciertos colectivos de científicos, como meteorólogos u oceanógrafos.

En éste notebook vamos a utilizar:

  * [Basemap Matplotlib toolkit](http://matplotlib.org/basemap/index.html) 1.0.7, para representar información 2D sobre mapas
  * [Pandas](http://pandas.pydata.org) 0.14.1, para cargar los datos
  * [Requests](http://docs.python-requests.org/en/latest/) 2.4.1, para consultar la web

## Datos {#datos}

Lo primero es tener claro qué es lo que vamos a representar. Eso nos permitirá definir el tipo de representación a utilizar, así como las características del mapa —su proyección y límites geográficos.

### Circuitos de Formula 1 {#circuitos-de-formula-1}

La Formula 1 —categoría reina del automovilísmo— comenzó sus andanzas en el año 1950, con una primera prueba en Silverstone. Desde entonces, y aunque su foco de actividad se encuentra principalmente en Europa, ha ido expandiéndose para celebrar Grandes Premios por todo el mundo.

En Wikipedia podemos encontrar una simple [tabla](http://en.wikipedia.org/wiki/List_of_Formula_One_circuits#Circuits) con una lista de todos los circuitos que alguna vez han albergado un Gran Premio. La copiamos y generamos un fichero CSV o XLS en Excel o en un editor de texto como [Notepad++](http://notepad-plus-plus.org).

<pre><code class="language-python">import pandas as pd</code></pre>

<pre><code class="language-python">data = pd.DataFrame.from_csv('F1-circuits.csv', header=0, sep=';', index_col=None, parse_dates=False, encoding='latin-1')
data.head(5)</code></pre>

<table border="1" class="dataframe">
  <tr style="text-align: right">
    <th>
    </th>
    
    <th>
      Circuit
    </th>
    
    <th>
      Type
    </th>
    
    <th>
      Direction
    </th>
    
    <th>
      Location
    </th>
    
    <th>
      Current Length
    </th>
    
    <th>
      Grands Prix
    </th>
    
    <th>
      Season(s)
    </th>
    
    <th>
      Grands Prix held
    </th>
  </tr>
  
  <tr>
    <th>
    </th>
    
    <td>
      Adelaide Street Circuit
    </td>
    
    <td>
      Street
    </td>
    
    <td>
      Clockwise
    </td>
    
    <td>
      Adelaide, Australia
    </td>
    
    <td>
      3.780 km (2.349 mi)
    </td>
    
    <td>
      Australian Grand Prix
    </td>
    
    <td>
      1985-1995
    </td>
    
    <td>
      11
    </td>
  </tr>
  
  <tr>
    <th>
      1
    </th>
    
    <td>
      Ain-Diab Circuit
    </td>
    
    <td>
      Road
    </td>
    
    <td>
      Clockwise
    </td>
    
    <td>
      Casablanca, Morocco
    </td>
    
    <td>
      7.618 km (4.734 mi)
    </td>
    
    <td>
      Moroccan Grand Prix
    </td>
    
    <td>
      1958
    </td>
    
    <td>
      1
    </td>
  </tr>
  
  <tr>
    <th>
      2
    </th>
    
    <td>
      Aintree
    </td>
    
    <td>
      Road
    </td>
    
    <td>
      Clockwise
    </td>
    
    <td>
      Liverpool, United Kingdom
    </td>
    
    <td>
      4.828 km (3.000 mi)
    </td>
    
    <td>
      British Grand Prix
    </td>
    
    <td>
      1955, 1957, 1959, 1961-1962
    </td>
    
    <td>
      5
    </td>
  </tr>
  
  <tr>
    <th>
      3
    </th>
    
    <td>
      Albert Park
    </td>
    
    <td>
      Street
    </td>
    
    <td>
      Clockwise
    </td>
    
    <td>
      Melbourne, Australia
    </td>
    
    <td>
      5.303 km (3.295 mi)
    </td>
    
    <td>
      Australian Grand Prix
    </td>
    
    <td>
      1996-2014
    </td>
    
    <td>
      19
    </td>
  </tr>
  
  <tr>
    <th>
      4
    </th>
    
    <td>
      AVUS
    </td>
    
    <td>
      Street
    </td>
    
    <td>
      Anti-clockwise
    </td>
    
    <td>
      Berlin, Germany
    </td>
    
    <td>
      8.300 km (5.157 mi)
    </td>
    
    <td>
      German Grand Prix
    </td>
    
    <td>
      1959
    </td>
    
    <td>
      1
    </td>
  </tr>
</table>

## Google Geocode {#google-geocode}

Ya tenemos la tabla cargada con datos como el nombre del circuito, tipo y localización, así como el número de Grandes Premios albergados. Pero entre toda esa información no hay nada que le diga a Python dónde colocar el circuito en un mapa —aunque nosotros si sepamos ubicar Casablanca o Melbourne—. Aquí es donde entra en juego el [API de codificación geográfica de Google](https://developers.google.com/maps/documentation/geocoding/).

> La codificación geográfica es el proceso de transformar direcciones (como "1600 Amphitheatre Parkway, Mountain View, CA") en coordenadas geográficas (como 37.423021 de latitud y -122.083739 de longitud), que se pueden utilizar para colocar marcadores o situar el mapa. El API de codificación geográfica de Google proporciona una forma directa de acceder a un geocoder mediante solicitudes HTTP.

El uso del API de codificación geográfica de Google está sujeto a un límite de 2.500 solicitudes de codificación geográfica al día, más que suficientes para ubicar los cerca de 70 circuitos que han albergado alguna vez en su historia un Gran Premio de Fórmula 1.

Como bien indica la documentación, al geocoder se accede mediante solicitudes HTTP, y para ello nada mejor que [Requests](http://docs.python-requests.org/en/latest/). Todas las consultas se realizan a una dirección HTTP `http://maps.googleapis.com/maps/api/geocode/json` a la que se añaden una serie de parámetros obligatorios:

  * `address`: es la dirección que quieres codificar de forma geográfica.
  * `sensor`: indica si la solicitud de codificación geográfica procede de un dispositivo con un sensor de ubicación. Este valor debe ser `true` o `false`.

Hay, además, una serie de parámetros opcionales, pero no nos harán falta.

La consulta —`requests.get(url, params)`— devuelve una respuesta en formato [`json`](https://developers.google.com/maps/documentation/geocoding/#JSON) donde se incluyen las coordenadas geográficas que buscamos. El formato `json`, Python lo interpreta como un conjunto de diccionarios y arrays, para lo que indicaremos los `key` y los índices hasta llegar al punto donde se encuentra la información que buscamos. En éste caso: `['results'][0]['geometry']['location']`.

<pre><code class="language-python">import requests</code></pre>

<pre><code class="language-python">_GEOCODE_QUERY_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
def geocode(address, sensor='false'):
    """
    Given a string 'address', return a dictionary of information about
    that location, including its latitude and longitude.
    """
    params = dict(address=address, sensor=sensor)
    response = requests.get(url=_GEOCODE_QUERY_URL, params=params)
    return response.json()
def address_to_latlng(address):
    """
    Given a string 'address', return a '(latitude, longitude)' pair.
    """
    location = geocode(address)['results'][0]['geometry']['location']
    return tuple(location.values())</code></pre>

## Basemap {#basemap}

Basemap es un toolkit de matplotlib que nos facilita la tarea de representar información 2D sobre mapas. Ésta información pueden ser contornos, vectores o puntos entre otros como se puede ver en los [ejemplos](http://matplotlib.org/basemap/users/examples.html).

<pre><code class="language-python">from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt</code></pre>

Lo primero, vamos a definir es el tipo de proyección a emplear. Hay un montón de ellas descritas en la [Wikipedia](http://en.wikipedia.org/wiki/List_of_map_projections), y en Basemap [disponemos de 24](http://matplotlib.org/basemap/users/mapsetup.html) entre las que escoger. [Para gustos, proyecciones](http://xkcd.com/977/).

En este caso hemos optado por Eckert IV, una proyección pseudocilíndrica, para representar el mapamundi y la Albers Equal Area projection para Europa. Dibujaremos las líneas de costa, las fronteras entre países, los paralelos y meridianos y le daremos un toque de color a los continentes. Basemap, además de disponer de una base de datos con información para representar líneas costeras y fronteras políticas, permite utilizar una imagen como fondo para el mapa. Entre las opciones que ofrece Basemap podemos encontrar el [Blue Marble](http://visibleearth.nasa.gov/view_cat.php?categoryID=1484) de la NASA —`m.bluemarble()`—. Aquí hemos optado por una imagen [_shaded relief_](http://www.shadedrelief.com/) de tonos claros con `m.shadedrelief()`.

<pre><code class="language-python">def basic_world_map(ax=None, region='world'):
    if region=='world':
        m = Basemap(resolution='i',projection='eck4',
                    lat_0=0,lon_0=0)
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90.,91.,30.))
        m.drawmeridians(np.arange(-180.,181.,30.))
    elif region=='europe':
        m = Basemap(width=4000000,height=4000000,
                    resolution='l',projection='aea',\
                    lat_1=40.,lat_2=60,lon_0=10,lat_0=50)
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90.,91.,10.))
        m.drawmeridians(np.arange(-180.,181.,10.))
        m.shadedrelief(scale=0.5)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral', alpha=0.3)
    return m</code></pre>

Creamos un `subplot` y le asignamos un título a la figura. En esa figura vamos a representar las localizaciones de los circuitos con puntos con un área que vendrá determinada por el número de carreras disputadas —tanto mayor será el círculo cuantas más carreras se hayan disputado.

Para que los circulos no sean demasiado grandes —en Monza se han celebrado 64 Grandes Premios— limitaremos el radio del círculo a entre 3 y 20 puntos. Le damos a los cículos algo de transparencia con `alpha=0.7`, añadimos una nota de texto y guardamos la figura.

<pre><code class="language-python">maximum = data['Grands Prix held'].max()
minimum = data['Grands Prix held'].min()
f, ax = plt.subplots(figsize=(20, 8))
ax.set_title('Formula 1 Grand Prix Circuits since 1950\n(Radius by number of races held)')
m = basic_world_map(ax)
for cir, loc, num in zip(data['Circuit'].values, data['Location'].values, data['Grands Prix held'].values):
    lat, lng = address_to_latlng(cir + ', ' + loc)
    x, y = m(lat, lng)
    m.scatter(x, y, s=np.pi * (3 + (num-minimum)/(maximum-minimum)*17)**2, marker='o', c='red', alpha=0.7)
ax.annotate(u'\N{COPYRIGHT SIGN} 2014, Pablo Fernandez', (0, 0))
f.savefig('f1-circuits.png', dpi=72, transparent=False, bbox_inches='tight')</code></pre>

[<img src="http://pybonacci.org/wp-content/uploads/2014/10/f1-circuits.png" alt="f1-circuits" width="907" height="492" class="aligncenter size-full wp-image-2772" srcset="https://pybonacci.es/wp-content/uploads/2014/10/f1-circuits.png 907w, https://pybonacci.es/wp-content/uploads/2014/10/f1-circuits-300x162.png 300w" sizes="(max-width: 907px) 100vw, 907px" />](http://pybonacci.org/wp-content/uploads/2014/10/f1-circuits.png)

Podemos ver una gran concentración de Grandes Premios en Europa, continente que vio nacer a la Fórmula 1 y base de operaciones de la mayoría de equipos que compiten en ella. Si centramos la imagen sobre europa, a la cual hemos añadido un [fondo](http://matplotlib.org/basemap/users/geography.html), podremos ver con mayor claridad la distribución de las que han sido sedes de algún Gran Premio por el viejo continente.

<pre><code class="language-python">f, ax = plt.subplots(figsize=(20, 8))
ax.set_title('Formula 1 Grand Prix Circuits in Europe since 1950\n(Radius by number of races held)')
m = basic_world_map(ax, 'europe')
for cir, loc, num in zip(data['Circuit'].values, data['Location'].values, data['Grands Prix held'].values):
    lat, lng = address_to_latlng(cir + ', ' + loc)
    x, y = m(lat, lng)
    m.scatter(x, y, s=np.pi * (3 + (num-minimum)/(maximum-minimum)*17)**2, marker='o', c='red', alpha=0.7)
ax.annotate(u'\N{COPYRIGHT SIGN} 2014, Pablo Fernandez', (100000, 100000))
f.savefig('f1-circuits-europe.png', dpi=72, transparent=False, bbox_inches='tight')</code></pre>

[<img src="http://pybonacci.org/wp-content/uploads/2014/10/f1-circuits-europe.png" alt="f1-circuits-europe" width="460" height="490" class="aligncenter size-full wp-image-2771" srcset="https://pybonacci.es/wp-content/uploads/2014/10/f1-circuits-europe.png 460w, https://pybonacci.es/wp-content/uploads/2014/10/f1-circuits-europe-281x300.png 281w" sizes="(max-width: 460px) 100vw, 460px" />](http://pybonacci.org/wp-content/uploads/2014/10/f1-circuits-europe.png)