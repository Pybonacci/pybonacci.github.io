---
title: Usando el GPS sin perdernos (usando pyproj)
date: 2012-10-27T03:31:55+00:00
author: Kiko Correoso
slug: usando-el-gps-sin-perdernos-usando-pyproj
tags: cartografía, geografía, gps, mapeo, mapping, proj, proj.4, pyproj

Como todos sabéis, la tierra no es una esfera perfecta ya que su forma es irregular y sus polos están achatados. Esto complica la vida en muchos ámbitos de la vida como, por ejemplo, conocer una posición sobre la superficie terrestre con el menor error posible.

Está bien, Houston, tenemos un problema. Vamos a ver una serie de conceptos básicos, vamos a plantear un problema y lo vamos a resolver con la ayuda de nuestro lenguaje de programación preferido.

**[Para este artículo se ha usado python 2.7.2 y pyproj 1.9.2]**

**Conceptos básicos**

La tierra no es esférica (ni plana, como algunos creen aun), ya lo sabemos (algunos). Tampoco tiene una forma regular por lo que no existe una única definición de la forma de la tierra. Dependiendo de la zona del mundo en que nos encontremos deberemos aproximar la forma de la tierra mediante un modelo que tenga los menores errores posibles en nuestra área de interés. El geoide sería la forma que tendría la Tierra si se midiera sobre el nivel del mar. Esto es, una superficie ondulada que varía unos 100 m arriba y debajo de una elipsoide bien ajustada. Las elevaciones y las líneas de contorno de la tierra están referidas al geoide y no al elipsoide, mientras que la latitud y la longitud están refereridas al elipsoide. ¿Por qué es ondulada la forma del geoide? Debido a irregularidades en el campo gravitatorio.

![](http://kartoweb.itc.nl/geometrics/Bitmaps/refsurface%203.12f.gif)

Por otra parte, normalmente, no llevamos un globo terráqueo con nosotros ya que no nos cabe en un bolsillo, llevamos mapas, que son más cómodos de transportar para irnos de excursión al monte. ¿Dónde quiero llegar con esto? Para el que no se haya dado cuenta, acabamos de convertir un objeto tridimensional en un objeto bidimensional y esto provoca que haya distorsiones. Es imposible que al pasar de 3D a 2D seamos capaces de mantener las mismas distancias, direcciones, formas y áreas. Al menos uno de estos parámetros cambiará (se distorsionará) al plasmarlo en un mapa 2D. Y llegamos al punto en el que entran en juego las proyecciones geográficas. [Proyecciones geográficas hay muchas, algunas conservan áreas, otras distancias](http://www.progonos.com/furuti/MapProj/Normal/ProjTbl/projTbl.html),...

Jo, siento que lo he explicado fatal pero es que el tema no es sencillo de explicar en dos párrafos. Un esquema de lo que he querido decir en los anteriores párrafos sería el siguiente:

![](http://mapref.org/NotesImages/Zweig16NotesImage5.gif)

**Problema**

Bueno, veamos el problema a ver si se entiende mejor lo que quiero mostrar:

> Imaginad que hemos subido al monte, está nevado y nos hemos perdido. Llevamos nuestro receptor GPS que nos da la información en coordenadas geográficas refereridas al sistema de coordenadas [WGS84](http://es.wikipedia.org/wiki/WGS84) (todos los GPS funcionan con WGS84). Queremos que nos rescaten pero sabemos que la persona que nos puede rescatar solo tiene mapas en [ED50](http://es.wikipedia.org/wiki/ED50) en coordenadas cartesianas (proyección [UTM](http://es.wikipedia.org/wiki/Sistema_de_Coordenadas_Universal_Transversal_de_Mercator)). Como son [datums](http://es.wikipedia.org/wiki/Datum) diferentes puede que si le paso las coordenadas en WGS84 no me encuentre porque su mapa esté desplazado (ya que está en otro datum). ¿Cómo puedo transformar mis coordenadas a las suyas para que me encuentre y no me congele? Exacto, usando pyproj.

**Solución**

Imaginad que me encuentro en el punto con longitud y latitud (-3.368620º, 37.054883º) en WGS84. Vamos a transformar esas coordenadas con [pyproj.](http://code.google.com/p/pyproj/) Pyproj es una pequeña biblioteca que permite acceder a la biblioteca de proyecciones cartográficas [proj.4](https://trac.osgeo.org/proj/) escrita en C. Pyproj permite hacer transformaciones de coordenadas y calcular [círculos máximos](http://es.wikipedia.org/wiki/Gran_c%C3%ADrculo). Vamos a usarla para hacer una transformación de coordenadas (ya llegamos al código python):

<pre><code class="language-python">import pyproj
## http://pyproj.googlecode.com/svn/trunk/docs/pyproj.Proj-class.html
## Creamos el primer sistema de coordenadas en WGS84
## epsg:4326, http://spatialreference.org/ref/epsg/4326/
p1 = pyproj.Proj(init = "epsg:4326")
## Creamos el segundo sistema de coordenadas en ED50 UTM huso horario 30
## epsg:23030, http://spatialreference.org/ref/epsg/23030/
p2 = pyproj.Proj(init = "epsg:23030")
## Mi posición en WGS84
lon = -3.368620
lat = 37.054883
## Transformamos del sistema de coordenadas p1 (WGS84 en grográficas)
## al sistema de coordenadas p1 (ED50, UTM, Z30)
x2, y2 = pyproj.transform(p1, p2, lon, lat)
print x2, y2</code></pre>

Si lo hemos hecho todo bien el resultado que obtendremos será:

467327.137963, 4101226.2785 (las unidades son metros).

Y estas coordenadas serán las correctas en el mapa ED50 en UTM de nuestro salvador para que nos pueda encontrar sin ningún tipo de error. Imaginad por un momento que os habéis equivocado y en lugar de pasarle las coordenadas en ED50 UTM se las pasáis en WGS84 UTM. El resultado sería:

<pre><code class="language-python">## epsg:4326, http://spatialreference.org/ref/epsg/4326/
p1 = pyproj.Proj(init = "epsg:4326")
## epsg:32630, http://spatialreference.org/ref/epsg/32630/
p2 = pyproj.Proj(init = "epsg:32630")
## Mi posición en WGS84
lon = -3.368620
lat = 37.054883
## Transformamos del sistema de coordenadas p1 (WGS84 en grográficas)
## al sistema de coordenadas p1 (ED50, UTM, Z30)
x2, y2 = pyproj.transform(p1, p2, lon, lat)
print x2, y2</code></pre>

Cuyo resultado sería:

467225.167945, 4101024.2792 (las unidades son metros).

Que estaría a unos 226 m al suroeste en el mapa de mi salvador. Imaginad lo trágico del error en un día de ventisca en la montaña nevada...

Algo menos trágico podría ser un error como el siguiente :-):

<img class="aligncenter" alt="" src="http://celebrating200years.noaa.gov/magazine/tct/01_misaligned_bridge_503.jpg" width="503" height="375" />

**Miscelánea**

Bueno, no sé si se ha entendido muy bien la complejidad del tema, no sé si he cometido algún error gordo en alguna explicación de más arriba pero os he presentado pyproj, una pequeña biblioteca con la que poder jugar. También queda claro que detrás de unas pocas líneas de código en python hay mucho tiempo, recursos y personas detrás de muy diversos campos, geógrafos, físicos, matemáticos, programadores,... Me gustaría resaltar que gracias a todo el trabajo de esta gente podemos hacer de forma sencilla lo que hemos visto hoy en esta entrada. Todo ello no es gratis, aunque lo podamos usar libremente. 😉

Hasta la próxima.

P.D.: Como siempre, tenéis los comentarios para corregirme, criticarme (de forma constructiva), mejorar las explicaciones (entre nuestros seguidores de twitter hay algunos mapólogos, ¿no? [1](https://twitter.com/saleiva), [2,](https://twitter.com/javisantana) [3](https://twitter.com/jatorre))...

P.D.2: En python tambien existen [bindings](http://trac.osgeo.org/gdal/wiki/GdalOgrInPython) para [gdal](http://www.gdal.org/) y [ogr](http://www.gdal.org/ogr/index.html), una librería más compleja y completa que pyproj, con lo que podríamos [resolver este problema de otra forma](http://stackoverflow.com/a/10239676). Algún día caerá algo también usando gdal y ogr.
