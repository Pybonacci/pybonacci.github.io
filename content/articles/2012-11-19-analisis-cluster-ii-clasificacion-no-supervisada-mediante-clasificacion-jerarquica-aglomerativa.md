---
title: Análisis Cluster (II): Clasificación no supervisada mediante clasificación jerárquica aglomerativa
date: 2012-11-19T23:47:13+00:00
author: Kiko Correoso
slug: analisis-cluster-ii-clasificacion-no-supervisada-mediante-clasificacion-jerarquica-aglomerativa
tags: agrupamiento clusters, ai, aprendizaje automático, aprendizaje no supervisado, clasificación clustering, ia, inteligencia artificial, machine learning, scipy, scipy.cluster, scipy.spatial, unsupervised learning

(Este es el segundo capítulo de la mini-serie de artículos sobre análisis cluster que estamos haciendo en pybonacci, si todavía [no has leído el artículo inicial échale un ojo ahora](http://pybonacci.org/2012/11/18/analisis-cluster-i-introduccion/)).

Como vimos anteriormente, existen diferentes formas de hacer clustering y, como también comentamos anteriormente, una de las más habituales es el clustering jerárquico.

El clustering jerárquico asociativo pretende, partiendo de m observaciones, ir encontrado agrupaciones de forma jerarquizada. Para ello, primero busca similitudes entre las observaciones y después procura asociar en grupos o 'clusters' las observaciones que se encuentran 'más cercanas' o presentan mayor similitud.

Si os acordáis, en el [primer capítulo de esta mini-serie](http://pybonacci.org/2012/11/18/analisis-cluster-i-introduccion/), entrecomillamos la palabra ‘similitud’. Vamos a ver qué significa esto de similitud en general y en nuestro ejemplo concreto (ver [capítulo anterior](http://pybonacci.org/2012/11/18/analisis-cluster-i-introduccion/) de la serie para conocer el ejemplo). Dependiendo del problema concreto necesitaremos asociar las variables para poder medir como son de similares o a qué distancia se encuentran entre sí. Estas medidas de asociación (similitud o distancia) dependerán del problema concreto con el que nos encontremos y no se usaría lo mismo para variables booleanas, binarias, reales,... Gracias al módulo [scipy.spatial.distance](http://docs.scipy.org/doc/scipy/reference/spatial.distance.html#module-scipy.spatial.distance) podemos ver muchas de estas medidas de asociación en las que no voy a entrar en detalle. Un resumen de la mayoría de ellas lo podéis ver en [el siguiente enlace del profesor José Ángel Gallardo San Salvador, nuevamente](http://www.ugr.es/~gallardo/pdf/cluster-2.pdf). En el ejemplo propuesto usaremos la correlación como medida de asociación ya que es una medida invariante aunque las variables se escalen y/o se les sumen/resten parámetros (algo muy útil para el caso que nos ocupa).

<!--more-->

Una vez que hemos calculado todas las medidas de asociación entre las _m_ observaciones hemos de establecer un método para las uniones de las observaciones para así ir creando los clusters. Nuevamente, scipy acude al rescate para poder establecer esto mediante el módulo [scipy.cluster](http://docs.scipy.org/doc/scipy/reference/cluster.html) y la función [scipy.cluster.hierarchy.linkage](http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage). El 'linkage', enlazado o amalgamiento se puede realizar mediante diferentes métodos. En la función anterior podemos elegir entre algunos de ellos como el método simple, completo, promedio, pesado, de Ward,... ¿Dónde los podéis ver [explicados de forma detallada y excelente](http://www.ugr.es/~gallardo/pdf/cluster-3.pdf)? Pues sí, en [los apuntes del profesor José Ángel Gallardo San Salvador, de la escuela de estadística de la Universidad de Granada](http://www.ugr.es/~gallardo/pdf/cluster-3.pdf) (perded 10 minutos en leer el enlace anterior y lo que sigue a continuación tendrá más sentido). El enlazado se realiza en el momento inicial, cuando se dispone de las _m_ observaciones, y después de hacer un nuevo grupo o cluster usando el método de enlazado (o linkage o amalgamiento) que se haya seleccionado. En las [siguientes transparencias](https://www.slideshare.net/pybonacci/linkage-15253227) se intenta detallar un ejemplo, paso a paso, de un enlazado simple para una distancia mínima.

Bueno, bueno,..., mucha palabrería, mucho enlace a apuntes,... Falta una cosa, ¡¡!SHOW ME THE CODE!! A eso vamos. Para ello vamos a hacer uso de unos datos de temperatura que descargaremos de la <a href="http://www.esrl.noaa.gov/psd/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis+Surface+Level&DB_did=3&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fair.sig995.1948.nc+air.sig995.%25y4.nc+94788&variable=air&DB_vid=20&DB_tid=35711&units=degK&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=60S&lat-end=15N&lon-begin=84W&lon-end=30W&dim0=time&year_begin=2009&mon_begin=Jan&day_begin=1&hour_begin=00+Z&year_end=2012&mon_end=Jan&day_end=1&hour_end=00+Z&X=lon&Y=lat&output=file&bckgrnd=black&use_color=on&fill=lines&cint=&range1=&range2=&scale=100&submit=Create+Plot+or+Subset+of+Data">siguiente url (pinchad sobre 'FTP a copy of the file')</a>. Una vez que tengáis el fichero descargado vamos a importar todo lo que vamos a necesitar:

<pre><code class="language-python">from scipy import cluster
import numpy as np
from matplotlib import pyplot as plt
import netCDF4 as nc
from mpl_toolkits import basemap as bm</code></pre>

Ahora vamos a preparar los datos:

<pre><code class="language-python">print('leyendo datos nc')
tsfc = nc.Dataset('X83.42.0.38.323.14.41.15.nc') #tsfc 'por temperature at surface'
lat = tsfc.variables['lat'][:]
lon = tsfc.variables['lon'][:]
tmp = tsfc.variables['air'][:]</code></pre>
  
Tenemos las series de temperatura (tmp) y su posición (lon, lat). Vamos a ver los nodos (series) que tenemos sobre un mapa.

<pre><code class="language-python">m = bm.Basemap(llcrnrlon = np.min(lon) - 1, llcrnrlat = np.min(lat) - 1,
               urcrnrlon = np.max(lon) + 1, urcrnrlat = np.max(lat) + 1,
projection = 'mill')
lon, lat = np.meshgrid(lon, lat)
x, y = m(lon, lat)
m.scatter(x, y, color= 'y')
m.drawcountries()
m.drawlsmask(land_color = 'g', ocean_color = 'c')
plt.show()</code></pre>

<a href="http://new.pybonacci.org/images/2012/11/nodos.png"><img class="aligncenter size-full wp-image-1267" title="nodos" alt="" src="http://new.pybonacci.org/images/2012/11/nodos.png" height="500" width="700" srcset="https://pybonacci.org/wp-content/uploads/2012/11/nodos.png 800w, https://pybonacci.org/wp-content/uploads/2012/11/nodos-300x214.png 300w" sizes="(max-width: 700px) 100vw, 700px" /></a>

Bueno, quizá son demasiadas series para ver el ejemplo pero luego podéis toquetear el código para usar menos series o vuestras propias series. Ahora es cuando hacemos los cálculos propios del análisis cluster:

<pre><code class="language-python">tmp = tmp.reshape(tmp.shape[0], tmp.shape[1] * tmp.shape[2])
print('calculando grupos')
enlaces = cluster.hierarchy.linkage(tmp.T, method = 'single', metric = 'correlation')
print('dibujando dendrograma')
cluster.hierarchy.dendrogram(enlaces, color_threshold=0)
plt.show()</code></pre>  

Y veremos algo como lo siguiente, que se conoce como dendrograma:

<a href="http://new.pybonacci.org/images/2012/11/dendrograma.png"><img class="aligncenter size-full wp-image-1268" title="dendrograma" alt="" src="http://new.pybonacci.org/images/2012/11/dendrograma.png" height="356" width="700" srcset="https://pybonacci.org/wp-content/uploads/2012/11/dendrograma.png 1600w, https://pybonacci.org/wp-content/uploads/2012/11/dendrograma-300x152.png 300w, https://pybonacci.org/wp-content/uploads/2012/11/dendrograma-1024x521.png 1024w, https://pybonacci.org/wp-content/uploads/2012/11/dendrograma-1200x611.png 1200w" sizes="(max-width: 700px) 100vw, 700px" /></a>

Desgraciadamente no se ve muy bien puesto que son muchas observaciones (682), lo dicho, toquetead para hacerlo con menos series y, si queréis, cambiando el método de 'linkage' y de distancias (en el ejemplo se usa el método simple y la correlación, respectivamente). Vemos que en el eje <em>y</em> hay unos valores, Pues bien, si cortamos el dendrograma horizontalmente por un valor nos quedaremos con tantos grupos como 'barritas verticales' o ramas cortemos. Vamos a hacer una prueba usando el valor 0.15 como valor de corte y vamos a representar a qué grupo pertenece cada una de las observaciones:

<pre><code class="language-python">clusters = cluster.hierarchy.fcluster(enlaces, 0.15, criterion = 'distance')
clusters = clusters.reshape(lat.shape)
m = bm.Basemap(llcrnrlon = np.min(lon) - 1, llcrnrlat = np.min(lat) - 1,
               urcrnrlon = np.max(lon) + 1, urcrnrlat = np.max(lat) + 1,
               projection = 'mill')
colores = np.linspace(0,1,np.max(clusters))
for j in range(clusters.shape[0]):
    for i in range(clusters.shape[1]):
        plt.text(x[j,i],y[j,i], str(clusters[j,i]),
                 color = str(colores[clusters[j,i] - 1]),
                 horizontalalignment='center',
                 verticalalignment='center')
plt.title(u'Número de grupos: %03d' % np.max(clusters))
m.drawcountries()
m.drawlsmask(land_color = 'g', ocean_color = 'c')
plt.show()</code></pre>

Y veremos un número sobre cada nodo que es el grupo al que pertenece cada observación si cortamos en 0.15 (los colores no indican nada, solo sirve para poder visualizar e identificar un poco más fácilmente los grupos).<a href="http://new.pybonacci.org/images/2012/11/resultado.png"><img class="aligncenter size-full wp-image-1270" title="resultado" alt="" src="http://new.pybonacci.org/images/2012/11/resultado.png" height="356" width="700" srcset="https://pybonacci.org/wp-content/uploads/2012/11/resultado.png 1600w, https://pybonacci.org/wp-content/uploads/2012/11/resultado-300x152.png 300w, https://pybonacci.org/wp-content/uploads/2012/11/resultado-1024x521.png 1024w, https://pybonacci.org/wp-content/uploads/2012/11/resultado-1200x611.png 1200w" sizes="(max-width: 700px) 100vw, 700px" /></a>
  
Y ahora es donde vendría el trabajo del experto para interpretar el resultado, para conocer si con 19 grupos es suficiente, es demasiado,... Haciendo una interpretación (no os creáis nada de lo que viene a continuación) de estos resultados podríamos decir que hay una clara separación entre temperaturas en el ecuador y el Caribe (grupo 11) y temperaturas por debajo del subtrópico (grupo 8), parece que hay varios grupos (17, 18, 6, 5, 12) que podrían estar diciendo que parece que estamos identificando un fenómeno de ¿<a href="http://es.wikipedia.org/wiki/El_Ni%C3%B1o">El Niño</a>?,...

He intentado sintetizar excesivamente y no sé si habréis entendido algo, pero bueno, si queréis profundizar en el tema, tenéis enlaces para leer información más en profundidad, hemos localizado bibliotecas python que nos ayudan a hacer este tipo de análisis y tenéis los comentarios para corregir, discutir, criticar, preguntar..., lo que consideréis oportuno.

Hasta la próxima!!
