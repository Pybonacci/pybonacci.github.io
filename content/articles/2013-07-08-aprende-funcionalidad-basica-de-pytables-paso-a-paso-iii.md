---
title: Aprende (funcionalidad básica de) PyTables paso a paso (III)
date: 2013-07-08T21:33:09+00:00
author: Kiko Correoso
slug: aprende-funcionalidad-basica-de-pytables-paso-a-paso-iii
tags: bases de datos, bbdd, hdf5, pytables, tutorial pytables básico 3.0

En los [anteriores capítulos](https://pybonacci.org/tag/tutorial-pytables-basico-3-0/) vimos como crear una estructura básica para nuestro fichero `h5` y como rellenar una tabla de datos. Ahora vamos a ver como volver a la tabla que ya rellenamos para añadir nuevos registros sin eliminar los anteriores.

### Modificar tablas existentes

Podemos añadir datos a tablas existentes de la siguiente forma. Para hacerlo primero abrimos el fichero que ya creamos anteriormente en modo "append", obtenemos el nodo que nos lleva a la tabla en cuestión que queremos rellenar (`tab` será una instancia de la clase `Table`) y establecemos un 'puntero' donde guardar los nuevos datos (con ayuda de `tab.row` donde `mis_datos` serán una instancia de la clase `Row`):

```python
# Si no habéis importado las librerías necesarias
# descomentad las siguientes tres líneas:
# import numpy as np
# import datetime as dt
# import tables as tb
h5file = tb.openFile("tabla_test.h5", mode = "a")
tab = h5file.getNode("/carpeta1/datos_carpeta1_tabla1")
mis_datos = tab.row
```

Ahora vamos a recuperar la última fecha que habíamos introducido en la columna fechas para seguir metiendo registros con fechas a continuación.

```python
# En la siguiente línea recuperamos el último elemento
# de la columna fecha
# No os preocupéis por esto ahora, lo veremos más adelante
ult_fecha = str(tab.cols.fecha[-1])
yy = int(ult_fecha[:4])
mm = int(ult_fecha[4:6])
dd = int(ult_fecha[6:])
fecha0 = dt.date(yy, mm, dd) + dt.timedelta(days = 1)
# Creamos 2000 nuevas fechas a continuación de la última que
# habíamos introducido con sus valores x, y, z correspondientes
fechas = np.array([int((fecha0 +
                  dt.timedelta(days = 1) * i).strftime("%Y%m%d"))
                  for i in range(2000)],
                  dtype = np.int32)
x = np.random.randn(2000)
y = np.random.randn(2000)
z = np.random.randn(2000)
```

Y, finalmente, añadimos los nuevos valores tal como vimos en el anterior capítulo:

```python
for i in range(2000):
    mis_datos['fecha'] = fechas[i]
    mis_datos['x'] = x[i]
    mis_datos['y'] = y[i]
    mis_datos['z'] = z[i]
    mis_datos.append()
tab.flush()
```

En la siguiente imagen se muestra un ejemplo de lo que acabamos de hacer:

<img class="aligncenter" src="http://new.pybonacci.org/images/2013/07/hdfview_nuevos-valores-ac3b1adidos.png" width="335" height="128" />

¿Qué pasa si ahora queremos modificar un valor de una columna? Eso lo podemos hacer usando la clase \`Cols\`. Imaginad que los primeros diez elementos de la columna \`x\` son erróneos y los queremos representar con 'NaNs'. Lo podemos hacer así:

```python
tab.cols.x[0:10] = np.repeat(np.NAN, 10)
tab.flush()
```

Si ahora inspeccionamos la tabla veremos que los diez primeros elementos de la columna 'x' han cambiado al valor NaN:

<img class="aligncenter" src="http://new.pybonacci.org/images/2013/07/hdfview_reemplazar-valores.png" width="403" height="284" />

¿Y si queremos cambiar una columna entera de datos? Pues siguiendo el mismo procedimiento podemos hacer lo siguiente para modificar la columna 'z':

```python
tab.cols.z[:] = np.repeat(-999.99, tab.cols.z.shape[0])
tab.flush()
```

Con lo que la tabla quedaría con la última columna (columna 'z') con todos sus elementos con valor '-999.99'

<img class="aligncenter" src="http://new.pybonacci.org/images/2013/07/hdfview_reemplazar-columna.png" width="453" height="529" />

Finalmente, para terminar este capítulo, cerramos la tabla creada como vimos en anteriores capítulos.

```python
h5file.close()
```

Veremos un poco más en los próximos días, estad atentos.

Saludos.
