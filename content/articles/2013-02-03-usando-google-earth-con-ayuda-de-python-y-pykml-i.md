---
title: Usando google earth con ayuda de python y pykml (I)
date: 2013-02-03T21:47:19+00:00
author: Kiko Correoso
slug: usando-google-earth-con-ayuda-de-python-y-pykml-i
tags: gis, google earth, googleearth, kml, kmz, pykml, sig

El tema de la visualización de datos es extremadamente importante puesto que te ayuda a comprender mejor al información que estás procesando. Si, además, esos datos se pueden ver de forma 'natural' en el medio donde suceden, donde se registran o donde se simulan pues mucho mejor. Por ejemplo, no tiene nada que ver el hecho de mirar por la tele un tornado o el verlo en vivo, de ver a una leona cazando en un documental o verlo en el cráter del Ngorongoro.

Los sistemas de información geográfica (SIG o GIS por sus sigles en inglés) permiten mostrar información georeferenciada. <a href="http://www.google.com/earth/index.html" target="_blank">Google Earth</a> permite ver información georeferenciada permitiendo verlo, además, de forma tridimensional por lo que, para determinados fenómenos, podemos ser conscientes de como se relacionan con su entorno. No es igual a verlo en vivo pero puede ser algo más cercano.

Hoy vamos a ver como usar <a href="http://pypi.python.org/pypi/pykml" target="_blank">pykml</a> para crear ficheros kml (o kmz) para, posteriormente, ver el resultado en Google Earth. Los ficheros <a href="http://en.wikipedia.org/wiki/Keyhole_Markup_Language" target="_blank">kml</a> (pongo el enlace a la wikipedia en inglés puesto que en español la información es bastante limitada) no son más que ficheros basados en la sintáxis xml para mostrar información geográfica. Google compró la empresa que estaba detrás de ello y más tarde, en 2008, se hizo estándar de la Open Geospatial Consortium (OGC). Un fichero kmz no es más que un fichero kml comprimido y que puede contener otra información relacionada con el kml, por ejemplo, una imagen en formato jpeg georeferenciada. El fichero kmz es útil cuando queremos distribuir la información de forma autocontenida (aunque la imagen georeferenciada siempre podría estar en un disco duro local, en un servidor accesible a través de la red, etc).

Vamos a ver varios ejemplos. En el primero daremos una vuelta por el mundo visitando diferentes sitios interesantes y en el siguiente ejemplo veremos la evolución del huracán Ivan (2004) que llegó hasta huracán de categoría 5 en la escala <a href="http://www.nhc.noaa.gov/aboutsshws.php" target="_blank">Saffir-Simpson</a>.

**[Para esta entrada se ha usado pykml 0.1.0, lxml 2.3.2 (es un prerrequisito de pykml) en el notebook de IPython 0.13 corriendo todo sobre python 2.7.3]**

<pre><code class="language-python">import os
from lxml import etree</code></pre>

En un documento kml podemos tener 'carpetas' para organizar jerárquicamente nuestra información. Dentro de las 'carpetas' podemos meter 'marcas de posición', 'capas', otras 'carpetas', geometrías,... Aquí no voy a explicar mucho más puesto que nos desviamos de python. Si queréis algo concreto usad los comentarios o podéis ver toda la referencia de kml \[aquí\](https://developers.google.com/kml/documentation/kmlreference?hl=es).

También podemos hacer cosas muy potentes como mostrar líneas de tiempo y reproducir fenómenos de forma que podemos ver su evolución en el tiempo, mostrar modelos 3D,... Al final del segundo capítulo enlazaré una forma creativa de usar también google earth [1] pero no nos adelantemos.

Como he comentado, íbamos a ver dos ejemplos, Empecemos por el primero. Este primer ejemplo es un plagio remozado de un \[ejemplo de la documentación\](http://packages.python.org/pykml/examples/tour_examples.html) de pykml.

Primero importamos todo lo necesario de pykml para este ejemplo:

<pre><code class="language-python">from pykml.factory import nsmap
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX</code></pre>

Y ahora, con la ayuda de python, vamos a empezar a ir creando cosas en el documento kml y a explicarlas poco a poco:

<pre><code class="language-python"># Desde la versión 5.0, google ha añadido una serie de extensiones
# a kml que lo hacen más potente e interactivo
# https://developers.google.com/kml/documentation/kmlreference?hl=es#kmlextensions
# Definimos una variable para el espacio de nombres de las
# extensiones de google que vamos a usar.
gxns = '{' + nsmap['gx'] + '}'
# Ponemos un listado de sitios que vamos a visitar
desc = """&lt;![CDATA[
PyCon Spain 2013
&lt;H3&gt;Visitanos!!!&lt;/h3&gt;
&lt;img src="http://www.python.org/community/logos/python-logo-master-v3-TM.png"/&gt;
]]&gt;
"""
lugares = [
    {'name':"LHC",
     'desc':'En algun lugar ahi abajo esta el Gran Colisionador de Hadrones',
     'lon':6.053295,'lat':46.235339, 'tilt':45,
     'range':300, 'range2':10000000.0, 'vis':0,},
    {'name':"VLT",
     'desc':'ESO Very Large Telescope - VLT',
     'lon':-70.4042,'lat':-24.6275, 'tilt':45,
     'range':300, 'range2':10000000.0, 'vis':0,},
    {'name':"Rapa Nui",
     'desc':'Ahu Akivi',
     'lon':-109.395,'lat':-27.115, 'tilt':45,
     'range':50, 'range2':10000000.0, 'vis':0,},
    {'name':"Osaka Science Museum",
     'desc':'Museo de ciencia de Osaka',
     'lon':135.4915, 'lat':34.6912, 'tilt':45,
     'range':300, 'range2':10000000.0, 'vis':0,},
    {'name':"IMAX",
     'desc':'Cine IMAX de Glasgow',
     'lon':-4.2939, 'lat':55.8581, 'tilt':45,
     'range':300, 'range2':10000000.0, 'vis':0,},
    {'name':"PyConES",
     'desc':desc,
     'lon':-3.7, 'lat':40.4165, 'tilt':0,
     'range':15000, 'range2':10000.0, 'vis':1,},
]</code></pre>

En la anterior porción de código solo hemos detallado una serie de características de lugares que vamos a visitar. Ahora vamos a crear el esqueleto del documento que contendrá una carpeta (folder) donde se guardará información de los lugares que vamos a visitar (posición, descripción, nombre) y un elemento gx:Tour que hace uso de las extensiones de Google:

<pre><code class="language-python"># start with a base KML tour and playlist
fich_kml = KML.kml(
    KML.Document(
      GX.Tour(
        KML.name(u"¡Reprodúceme!"),
        GX.Playlist(),
      ),
      KML.Folder(
        KML.name('Lugares visitados'),
        id='lugares',
      ),
    )
)</code></pre>

Y ahora vamos a hacer un bucle donde se van a ir añadiendo cosas tanto a la carpeta (folder) como al Tour. Voy explicándo lo que hace cada cosa mediante comentarios en el código:

<pre><code class="language-python"># Hacemos un bucle para recorrer todos los lugares definidos en
# el bloque de código anterior
for lugar in lugares:
    # Primero volamos hasta cada lugar (transición entre lugares)
    # y nos quedamos observándolo desde el espacio.
    # Para ello usamos FlyTo donde especificamos
    # La duración en segundos, si queremos que vaya más rápido o más
    # lento, el modo de vuelo, que puede ser más suave (smooth) o
    # más rápido (bounce) y la posición.
    # La posición la determinan longitude, latitude y altitude,
    # tilt es el ángulo desde la vertical (en este caso lo vemos
    # verticalmente (0º)) y range es la distancia desde la posición
    # determinada por longitude, latitude y altitude, teniendo en
    # cuenta el ángulo tilt (en este caso hemos puesto 10.000 km)
    # Las unidades para latitude y longitude son grados, para altitude
    # y range son metros y para tilt son grados desde la vertical.
    # En el gráfico de este enlace se verá mejor:
    # https://developers.google.com/kml/documentation/images/lookAt.gif
    fich_kml.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(1),
        GX.flyToMode("bounce"),
        KML.LookAt(
          KML.longitude(lugar['lon']),
          KML.latitude(lugar['lat']),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(45),
          KML.range(10000000.0),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )
    # Volamos desde el punto anterior (que estaba a 10.000 km
    # de altura) hasta el punto de vista desde donde queremos
    # visualizar cada lugar. Vamos a ver todos los lugares con un
    # ángulo (tilt) de 45º y a una altura de unos 300m de altura
    # Altura relativa al suelo, no al nivel del mar), excepto para
    # el caso de Rapa Nui, que bajaremos un poco más para que se vea mejor.
    fich_kml.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(1),
        GX.flyToMode("bounce"),
        KML.LookAt(
          KML.longitude(lugar['lon']),
          KML.latitude(lugar['lat']),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(lugar['tilt']),
          KML.range(lugar['range']),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )
    # Damos una pequeña vuelta alrededor del lugar
    # en el que nos encontremos, para ello usamos
    # heading, que indica la dirección (azimut) de la
    # cámara
    for aspect in range(0,360,15):
        fich_kml.Document[gxns+"Tour"].Playlist.append(
          GX.FlyTo(
            GX.duration(0.1),
            GX.flyToMode("bounce"),
            KML.LookAt(
              KML.longitude(lugar['lon']),
              KML.latitude(lugar['lat']),
              KML.altitude(0),
              KML.heading(aspect),
              KML.tilt(lugar['tilt']),
              KML.range(lugar['range']),
              KML.altitudeMode("relativeToGround"),
            )
          )
        )
    fich_kml.Document[gxns+"Tour"].Playlist.append(GX.Wait(GX.duration(0.1)))
    # Añadimos información de cada lugar en la carpeta
    # como 'placemarks' o marcas de posición. En el nombre y en la descripción
    # del placemark se puede meter HTML y CSS, por si queréis ser un poco más
    # creativos y dejar la información de una forma visible y bonita.
    # extrude == 1 indica que el nombre del lugar se hará visible. Si queremos
    # hacerlo visible solo cuando lo seleccionemos pues le ponemos el valor 0
    fich_kml.Document.Folder.append(
      KML.Placemark(
        KML.name(lugar['name']),
        KML.description(
            "{name}&lt;br/&gt;{desc}".format(
                    name=lugar['name'],
                    desc=lugar['desc'],
            )
        ),
        KML.Point(
          KML.extrude(1),
          KML.altitudeMode("relativeToGround"),
          KML.coordinates("{lon},{lat},{alt}".format(
                  lon=lugar['lon'],
                  lat=lugar['lat'],
                  alt=0,
              )
          )
        ),
        id=lugar['name'].replace(' ','_')
      )
    )
    # Aquí le indicamos a la reproducción que en el
    # momento que haya dado la vuelta al lugar nos
    # muestre el 'globo' o 'viñeta' con la información del sitio,
    # nombre y descripción. Visibility a 1 para
    # hacerlo visible.
    fich_kml.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(2.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.Placemark(
                KML.visibility(1),
                GX.balloonVisibility(1),
                targetId=lugar['name'].replace(' ','_')
              )
            )
          )
        )
    )
    fich_kml.Document[gxns+"Tour"].Playlist.append(GX.Wait(GX.duration(1.0)))
    # Esta parte de código hará que desaparezca el 'globo'
    # con la información así no tendremos el 'globo'
    fich_kml.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(2.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.Placemark(
                GX.balloonVisibility(lugar['vis']),
                targetId=lugar['name'].replace(' ','_')
              )
            )
          )
        )
    )
    # Finalmente, esta parte nos separa de la tierra
    # para que tengamos una vista privilegiada del
    # planeta azul a 10.000 km de altura
    fich_kml.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(5),
        GX.flyToMode("bounce"),
        KML.LookAt(
          KML.longitude(lugar['lon']),
          KML.latitude(lugar['lat']),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(0),
          KML.range(lugar['range2']),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )</code></pre>

En el siguiente código lo que hacemos es guardar el fichero kml final. Si os acordáis, en algún momento hemos puesto algunas etiquetas HTML. Algunos símbolos especiales se han transformado por lo que los volvemos a dejar como estaban ya que si no google earth no entenderá ese kml correctamente.

<pre><code class="language-python"># output a KML file (named based on the Python script)
outfile = file('VolandoVoy.kml','w')
salida = etree.tostring(fich_kml, pretty_print=True)
salida = salida.replace('&lt;', '&lt;') salida = salida.replace('&gt;', '&gt;')
outfile.write(salida)
outfile.close()</code></pre>

Por último, lanzamos google earth con el fichero que acabamos de crear. Las siguientes tres líneas funcionan en linux. Ahora mismo no tengo un windows cerca pero creo que deberéis cambiar \`googleearth\` por \`googleearth.exe\` y tener en cuenta los '' en lugar de '/' en la ruta al fichero.

<pre><code class="language-python">ruta = os.getcwd()
rutafich = ruta + '/VolandoVoy.kml'
os.system('googleearth {0}'.format(rutafich))</code></pre>

A la izquierda de la pantalla de google earth, en mis 'lugares', dentro de 'lugares temporales' podréis ver 'VolandoVoy.kml'. Si lo desplegáis veréis 'Reprodúceme'. Si hacéis doble click sobre 'Reprodúceme' podréis ver algo parecido a lo siguiente:

[youtube=http://www.youtube.com/watch?v=P-0mn_9ixjk]

No es un maravilla de vídeo pero solo es para que veáis un ejemplo en vivo del resultado.

AVISO: el otro día estuve probando todo el código anterior en un windows XP y me daba un error extraño. Cuando introducía la etiqueta \`description\` en el kml se escribía en mayúscula y google earth no entendía bien el kml y no me mostraba la información de la descripción... Estuve una hora larga con ello intentando adivinar qué es lo que estaba mal ya que el fichero kml se creaba sin problemas y google earth lo abría sin errores (pero no mostraba correctamente la descripción). Si a alguno le pasa, antes de guardar el fichero puede hacer _salida = salida.replace('<Description>', '<description>')_.

Y esto es todo por hoy, en 24h tendréis la segunda parte disponible.

P.D.: Como puede que wordpress me haya 'estropeado' algo al hacer copy&paste os dejo el enlace al [ipython notebook](https://gist.github.com/4703577) o lo podéis visualizar directamente en [nbviewer](http://nbviewer.ipython.org/4703577/).