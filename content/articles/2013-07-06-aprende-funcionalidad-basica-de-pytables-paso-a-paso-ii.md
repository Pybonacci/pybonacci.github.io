---
title: Aprende (funcionalidad básica de) PyTables paso a paso (II)
date: 2013-07-06T22:02:09+00:00
author: Kiko Correoso
slug: aprende-funcionalidad-basica-de-pytables-paso-a-paso-ii
tags: bases de datos, bbdd, hdf5, pytables, tutorial pytables básico 3.0

En el [anterior capítulo](https://pybonacci.org/2013/07/04/aprende-funcionalidad-basica-de-pytables-paso-a-paso-i/) vimos como crear una estructura básica para nuestro fichero `h5`. Ahora vamos a ver como rellenar tablas de ese mismo fichero.

### Rellenar tablas

Ahora es tiempo de rellenar la tabla con datos sin sentido (datos aleatorios) y fechas. `numpy` y `datetime` nos facilitarán la tarea por lo que vamos a importarlos antes).

    :::python
    import numpy as np
    import datetime as dt

Abrimos de nuevo el fichero h5 que creamos en el anterior capítulo, pero en lugar de abrirlo en modo "write" lo abriremos en modo "append".

    :::python
    h5file = tb.openFile("tabla_test.h5", mode = "a")

Recuperamos la tabla que queremos llenar (indicando la ruta en la estructura del fichero hdf5) y usando la función `getNode`:

    :::python
    tab = h5file.getNode("/carpeta1/datos_carpeta1_tabla1")

Para rellenar la tabla creamos un puntero (o constructor de líneas propio a la tabla) `row`.

    :::python
    mis_datos = tab.row

Creamos los datos que usaremos para rellenar la tabla:

    :::python
    fechas = np.array([int((dt.date(2000, 1, 1) +
                            dt.timedelta(days = 1) * i).strftime("%Y%m%d"))
                            for i in range(10000)],
                            dtype = np.int32)
    x = np.random.randn(10000)
    y = np.random.randn(10000)
    z = np.random.randn(10000)

Llenamos la tabla de manera recursiva con el constructor de líneas `mis_datos` y el método `append`:

    :::python
    for i in range(10000):
        mis_datos['fecha'] = fechas[i]
        mis_datos['x'] = x[i]
        mis_datos['y'] = y[i]
        mis_datos['z'] = z[i]
        mis_datos.append()

Se llama al método `flush` sobre la tabla para volcar y registrar efectivamente los datos en la tabla.

    :::python
    tab.flush()

Si queremos, podemos añadir meta-información a la tabla:

    :::python
    tab.attrs.nombre_sensor="medidas de un escaterómetro"
    tab.attrs.numero_columnas = 3

Además de la meta-información que hemos añadido, el objeto tabla contenía ya un cierto número de atributos que podemos ver escribiendo lo siguiente en IPython

    :::python
    tab.attrs

que nos mostrará lo siguiente:

    :::python
    /carpeta1/datos_carpeta1_tabla1._v_attrs (AttributeSet), 14 attributes:
       [CLASS := 'TABLE',
        FIELD_0_FILL := 0,
        FIELD_0_NAME := 'fecha',
        FIELD_1_FILL := 0.0,
        FIELD_1_NAME := 'x',
        FIELD_2_FILL := 0.0,
        FIELD_2_NAME := 'y',
        FIELD_3_FILL := 0.0,
        FIELD_3_NAME := 'z',
        NROWS := 0,
        TITLE := 'ejemplo de tabla',
        VERSION := '2.7',
        nombre_sensor := 'medidas de un escaterómetro',
        numero_columnas := 3]

Finalmente, cerramos la tabla creada como vimos en el primer capítulo.

    :::python
    h5file.close()

Si queréis usar una aplicación gráfica para ver el alrchivo que hemos creado podéis usar hdfview (`sudo apt-get install hdfview`) o vitables. En este caso os muestro un ejemplo con hdfview ya que vitables posiblemente lo veamos en uno de los próximos capítulos.

<img class=" wp-image-1705" alt="hdfview" src="http://new.pybonacci.org/images/2013/07/hdfview1.png?w=700" width="420" height="253" srcset="https://pybonacci.org/wp-content/uploads/2013/07/hdfview1.png 1680w, https://pybonacci.org/wp-content/uploads/2013/07/hdfview1-300x180.png 300w, https://pybonacci.org/wp-content/uploads/2013/07/hdfview1-1024x617.png 1024w, https://pybonacci.org/wp-content/uploads/2013/07/hdfview1-1200x723.png 1200w" sizes="(max-width: 420px) 100vw, 420px" />

Bueno, ya tenemos algunos datos guardados en nuestro fichero HDF5. El próximo día veremos como anexar datos a una tabla ya existente.

Saludos.
