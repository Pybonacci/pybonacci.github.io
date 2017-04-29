---
title: Aprende (funcionalidad básica de) PyTables paso a paso (I)
date: 2013-07-04T21:17:34+00:00
author: Kiko Correoso
slug: aprende-funcionalidad-basica-de-pytables-paso-a-paso-i
tags: bases de datos, bbdd, hdf5, pytables, tutorial pytables básico 3.0

## HDF5

El HDF5 (hierarchical dataset format, <a href="http://www.hdfgroup.org/HDF5/" target="_blank">http://www.hdfgroup.org/HDF5/</a>) es un formato que permite almacenar eficientemente grandes volúmenes de datos. Los datos se pueden almacenar de forma jerarquizada conjuntamente con metadatos. Es un formato portable que prácticamente no tiene límite en el tamaño de los datos.

## PyTables

Pytables está programado sobre el formato hdf5 con ayuda de Python y Numpy. La creación, modificación y búsquedas sobre grandes conjuntos de datos es relativamente sencilla. La utilización de memoria RAM y compresión de datos están optimizados en segundo plano por la biblioteca. El espacio de disco utilizado es mucho más pequeño y el acceso a los datos suele ser más rápido comparado con bases de datos relacionales.

La versión actual es la 3.0 y es compatible con python 2.7 y 3.1 o superiores.

Para instalarlo en un linux basado en Debian podéis hacer lo siguiente (asumo que tenéis pip y numpy instalado en vuestro virtualenv científico):

`sudo apt-get install libhdf5-serial-dev<br />
pip install numexpr cython<br />
pip install tables`

Para instalarlo en Windows podéis hacerlo usando un [ejecutable](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pytables) ya preparado por el gran [Christoph Gohlke](http://www.lfd.uci.edu/%7Egohlke/).

Si todo está correcto podemos empezar con el tutorial. Primero importamos la biblioteca

### Creación de ficheros h5

<pre><code class="language-python">import tables as tb</code></pre>

Ahora vamos a definir la estructura de una tabla creando una clase que deriva de la clase `IsDescription` (igual os suena a algo parecido a los modelos de Django). Nuestra tabla contará con una columna de fechas y tres columnas de datos 'float':

<pre><code class="language-python">class EstructuraTabla(tb.IsDescription):
    fecha = tb.Int64Col(pos = 0)
    x = tb.Float32Col(pos = 1)
    y = tb.Float32Col(pos = 2)
    z = tb.Float32Col(pos = 3)</code></pre>

Esta clase es un constructor de tabla. Se dan nombre predefinidos a las columnas, el tipo de datos que contendrán y su posición.

Ahora creamos un nuevo fichero `h5` en modo de escritura.

<pre><code class="language-python"># Donde pone "tabla_test.h5" y "Ejemplo pybonaccico"
# puedes poner la ruta y nombre de fichero que quieras
h5file = tb.openFile("tabla_test.h5",
                     mode = "w",
                     title = "Ejemplo pybonaccico")</code></pre>

En este caso, en el título hemos puesto algo muy estúpido pero en ese campo se puede poner algo más serio como 'Datos aportados por Google, fecha: 2012/01/01 14.23h, proyecto PRISM ;-P'

Creamos un "grupo" en la raiz del `h5` (parecido a una carpeta en un sistema de ficheros):

<pre><code class="language-python">grupo1 = h5file.createGroup("/",
                            'carpeta1',
                            'carpeta para un primer grupo de datos')</code></pre>

`carpeta1` será el nombre del grupo dentro del fichero `h5` y `carpeta para un primer grupo de datos` serán los metadatos descriptivos que podemos asociar al grupo `carpeta1`.

Y ahora, dentro del grupo que acabamos de crear, creamos una tabla (que sería como un fichero en un sistema de ficheros) con la estructura de tabla que hemos definido anteriormente (clase `EstructuraTabla`):

<pre><code class="language-python">tab = h5file.createTable(grupo1,
                         "datos_carpeta1_tabla1",
                         EstructuraTabla,
                         "ejemplo de tabla")</code></pre>

Aquí, `datos_carpeta1_tabla1` sería como el nombre del fichero (tabla) dentro de un sistema de archivos (dentro del fichero `h5`), `EstructuraTabla` es la estructura de los datos de la tabla que acabamos de definir y `ejemplo de tabla` es la información que asociamos a esta tabla.

En cualquier momento podemos inspeccionar la estructura que va tomando nuestro fichero `h5` haciendo un `print` del fichero `h5`.

<pre><code class="language-python">print(h5file)</code></pre>

Lo anterior nos debería de mostrar algo parecido a:

<pre><code class="language-python">tabla_test.h5 (File) 'Ejemplo pybonaccico'
Last modif.: 'Thu Jul  4 21:51:41 2013'
Object Tree:
/ (RootGroup) 'Ejemplo pybonaccico'
/carpeta1 (Group) 'carpeta para un primer grupo de datos'
/carpeta1/datos_carpeta1_tabla1 (Table(0,)) 'ejemplo de tabla'</code></pre>

Si queremos obtener más información podemos escribir simplemente en IPython:

<pre><code class="language-python">h5file</code></pre>

que nos mostrará lo siguiente:

<pre><code class="language-python">File(filename=tabla_test.h5, title='Ejemplo pybonaccico', mode='w', root_uep='/', filters=Filters(complevel=0, shuffle=False, fletcher32=False))
/ (RootGroup) 'Ejemplo pybonaccico'
/carpeta1 (Group) 'carpeta para un primer grupo de datos'
/carpeta1/datos_carpeta1_tabla1 (Table(0,)) 'ejemplo de tabla'
  description := {
  "fecha": Int64Col(shape=(), dflt=0, pos=0),
  "x": Float32Col(shape=(), dflt=0.0, pos=1),
  "y": Float32Col(shape=(), dflt=0.0, pos=2),
  "z": Float32Col(shape=(), dflt=0.0, pos=3)}
  byteorder := 'little'
  chunkshape := (3276,)</code></pre>

Finalmente, cerramos la tabla creada de la siguiente forma.

<pre><code class="language-python">h5file.close()</code></pre>

Y ya es suficiente por hoy, el próximo día veremos como rellenar tablas con datos ya que, de momento, solo hemos creado una estructura básica.

Saludos.