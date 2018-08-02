Title: ¿Cómo crear un mapa interactivo con Folium?
Date: 2017-09-07 12:58
Author: kiario
Category: Artículos, Tutoriales
Tags: aemet, folium, gis, leaflet, mapa, mapping, opendata, sig
Slug: como-crear-un-mapa-interactivo-con-folium
Status: published

En esta entrada voy a describir el proceso usado para crear
<https://kikocorreoso.github.io/datos_aemet/> con la ayuda de la
librería Folium.

¿Qué es Folium?
---------------

[Folium](http://folium.readthedocs.io/en/latest/) es una librería Python
que permite crear mapas interactivos usando
[Leaflet.js](http://leafletjs.com/). Lo que hace, de forma elegante, es
crear código javascript que usa la maravillosa librería de mapas
interactivos leaflet.

¿Crear el mapa?
---------------

En la rama *gh-pages* del repositorio git *datos\_aemet* en github
(<https://github.com/kikocorreoso/datos_aemet/tree/gh-pages>) hay una
serie de ficheros. Los ficheros *index.html*, *map.html* y *readme.html*
los generaremos a partir de los ficheros:

-   *custom.css*: Algo de css para que la página cuadre. Por debajo usa,
    además, bootstrap.
-   *src/create\_base\_map.py*: Esta es la madre del cordero y lo que
    vamos a comentar.
-   *src/template.html*: Aquí tenemos la estructura principal del HTML
    usado y que sirve de plantilla a *index.html* y *readme.html.*

El fichero *src/create\_base\_map.py* hace una serie de cosas:

-   Por un lado lee *template.html* y modifica una parte del mismo para
    crear *readme.html*. Lo importante ocurre de las líneas
    [11](https://github.com/kikocorreoso/datos_aemet/blob/gh-pages/src/create_base_map.py#L11)
    a
    [53](https://github.com/kikocorreoso/datos_aemet/blob/gh-pages/src/create_base_map.py#L53).
    Básicamente lee un texto identificativo que he dejado en
    *template.html* y lo reemplaza por código explicativo sobre la
    página.
-   Por otro lado, lee el fichero hdf5 de datos,
    [aemet.h5](https://github.com/kikocorreoso/datos_aemet/blob/master/hdf5/aemet.h5.gz)
    y de los datos diarios extrae los metadatos de la estación y las
    fechas de inicio y fin de los registros. Esta información se
    formatea e incluye en un marcador usando `folium.Marker`. Cada
    marcador tendrá un color en función del periodo de datos disponible.
    Si una estación tiene, por ejemplo, más de 50 años de registros se
    incluye en un grupo usando `folium.FeatureGroup`. Estos grupos de
    estaciones discretizadas por periodo de medidas se pueden manejar
    mediante un control que aparece en la parte superior derecha del
    mapa y que incluimos usando `folium.LayerControl`. Tanto los grupos
    de marcadores discretizados por periodos de medidas como el control
    de capas lo incluimos en el mapa creado usando `folium.Map`. Cuando
    tenemos todo colocadito guardamos el mapa en formato html. El
    guardado del mapa nos crea una página donde el mapa ocupa el 100% de
    la misma.
-   Por último, la página con el mapa la incluimos en *index.html*
    mediante un IFrame usando el mismo *template.html* que hemos usando
    para el *readme.html*.

Creación de un mapa en detalle
------------------------------

Primero los imports

```python
import folium
import branca
```

`branca` sirve para ayudarnos a meter HTML en los popup de los
marcadores. Sin ello solo he conseguido ver texto plano.

Creamos el mapa:

```python
mi_mapa = folium.Map(location=(39.7, 2.2), zoom_start=8)
```

Indicamos donde estará centrado el mapa usando `location` y el nivel de
zoom inicial.

Podéis guardar el mapa

```python
mi_mapa.save("mapa.html")
```

y abrirlo en vuestro [navegador
favorito](https://www.mozilla.org/es-ES/firefox/new/?scene=2) y veréis
un bonito mapa centrado cerca de unas hermosas islas.

![](https://www.pybonacci.org/images/2017/09/mapa1-300x148.png?style=centerme)

Pero este mapa está muy tímido sin mostrar muchas cosas. Vamos a crear
varios marcadores:

```python
# creamos el mapa de nuevo para partir de 0
mi_mapa = folium.Map(location=(39.7, 2.2), zoom_start=8)
# creamos 4 marcadores
marcador1 = folium.Marker(location=(40, 2.1))
marcador2 = folium.Marker(location=(40, 3.5))
marcador3 = folium.Marker(location=(39, 2.1))
marcador4 = folium.Marker(location=(39, 3.5))
```

Y los incluimos en el mapa y guardamos el mapa:

```python
marcador1.add_to(mi_mapa)
marcador2.add_to(mi_mapa)
marcador3.add_to(mi_mapa)
marcador4.add_to(mi_mapa)
mi_mapa.save("mapa.html")
```

Si abrís el mapa veréis cuatro marcadores alrededor de la isla de
Mallorca. Si pulsáis sobre los marcadores no harán nada.

![](https://www.pybonacci.org/images/2017/09/mapa2-300x147.png?style=centerme)

Vamos a incluir información en un popup y vamos a cambiar el color de
los iconos de los marcadores usando `folium.Icon`:

```python
# creamos el mapa de nuevo para partir de 0
mi_mapa = folium.Map(location=(39.7, 2.2), zoom_start=8)
# La información de los popups la añadiremos usando branca
# La información solo será la posición del marcador
# os dejo a vosotros la innovación
html = "<p>Latitud: 40.0</p><p>Longitud: 2.1</p>"
iframe1 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 40.0</p><p>Longitud: 3.5</p>"
iframe2 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 39.0</p><p>Longitud: 2.1</p>"
iframe3 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 39.0</p><p>Longitud: 3.5</p>"
iframe4 = branca.element.IFrame(html=html, width=500, height=300)
# creamos 4 marcadores y añadimos la información del popup usando folium.Popup
# además, añadimos un icono que será de un color para los marcadores al este
# y de otro color para los marcadores del oeste.
marcador1 = folium.Marker(
    location=(40, 2.1),
    popup=folium.Popup(iframe1, max_width=500),
    icon=folium.Icon(color="black")
)
marcador2 = folium.Marker(
    location=(40, 3.5),
    popup=folium.Popup(iframe2, max_width=500),
    icon=folium.Icon(color="gray")
)
marcador3 = folium.Marker(
    location=(39, 2.1),
    popup=folium.Popup(iframe3, max_width=500),
    icon=folium.Icon(color="black")
)
marcador4 = folium.Marker(
    location=(39, 3.5),
    popup=folium.Popup(iframe4, max_width=500),
    icon=folium.Icon(color="gray")
)
# Añadimos los marcadores al mapa
marcador1.add_to(mi_mapa)
marcador2.add_to(mi_mapa)
marcador3.add_to(mi_mapa)
marcador4.add_to(mi_mapa)
# Y guardamos el mapa
mi_mapa.save("mapa.html")
```

![](https://www.pybonacci.org/images/2017/09/mapa3-300x147.png?style=centerme)

Por último, vamos a modificar un poco todo esto para añadir los
marcadores del este (grises) a una capa y los del oeste (negros) a otra
capa y añadir, además, el control de capas. Añado, además, los imports
del principio para tener un script completo que podéis modificar a
vuestro gusto.

```python
import folium
import branca

# creamos el mapa de nuevo para partir de 0
mi_mapa = folium.Map(location=(39.7, 2.2), zoom_start=8)
# La información de los popups la añadiremos usando branca
# La información solo será la posición del marcador
# os dejo a vosotros la innovación
html = "<p>Latitud: 40.0</p><p>Longitud: 2.1</p>"
iframe1 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 40.0</p><p>Longitud: 3.5</p>"
iframe2 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 39.0</p><p>Longitud: 2.1</p>"
iframe3 = branca.element.IFrame(html=html, width=500, height=300)
html = "<p>Latitud: 39.0</p><p>Longitud: 3.5</p>"
iframe4 = branca.element.IFrame(html=html, width=500, height=300)
# creamos 4 marcadores y añadimos la información del popup usando folium.Popup
# además, añadimos un icono que será de un color para los marcadores al este
# y de otro color para los marcadores del oeste.
marcador1 = folium.Marker(
    location=(40, 2.1),
    popup=folium.Popup(iframe1, max_width=500),
    icon=folium.Icon(color="black")
)
marcador2 = folium.Marker(
    location=(40, 3.5),
    popup=folium.Popup(iframe2, max_width=500),
    icon=folium.Icon(color="gray")
)
marcador3 = folium.Marker(
    location=(39, 2.1),
    popup=folium.Popup(iframe3, max_width=500),
    icon=folium.Icon(color="black")
)
marcador4 = folium.Marker(
    location=(39, 3.5),
    popup=folium.Popup(iframe4, max_width=500),
    icon=folium.Icon(color="gray")
)
# Creamos dos grupos para los marcadores
grp_este = folium.FeatureGroup(name='Este')
grp_oeste = folium.FeatureGroup(name='Oeste')
# Añadimos los marcadores AL GRUPO AL QUE CORRESPONDAN (NO AL MAPA)
marcador1.add_to(grp_oeste)
marcador2.add_to(grp_este)
marcador3.add_to(grp_oeste)
marcador4.add_to(grp_este)
# Y ahora añadimos los grupos al mapa
grp_este.add_to(mi_mapa)
grp_oeste.add_to(mi_mapa)
# Y añadimos, además, el control de capas
folium.LayerControl().add_to(mi_mapa)
# Y guardamos el mapa
mi_mapa.save("mapa.html")
```

![](https://www.pybonacci.org/images/2017/09/mapa4-1-300x148.png?style=centerme)

*Et voilà*, tenemos un precioso mapa interactivo con mucha funcionalidad
en unas pocas líneas de Python.

Fin del 'así se hizo' de <https://kikocorreoso.github.io/datos_aemet/>.
