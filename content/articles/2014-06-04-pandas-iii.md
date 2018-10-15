---
title: Pandas (III)
date: 2014-06-04T06:00:49+00:00
author: Kiko Correoso
slug: pandas-iii
tags: big data, bigdata, datos, excel, hdf5, pandas, python 3, sql, Tutorial de pandas

Antes de nada, el contexto, para esta serie de entradas se va a usar lo siguiente:

```python
Versión de Python:      3.3.1 (default, Apr 10 2013, 19:05:32) 
[GCC 4.6.3]
Versión de Pandas:      0.13.1
Versión de Numpy:       1.8.1
Versión de Matplotlib:  1.3.1
```

Y sin más preámbulos seguimos con esta tercera parte de 
[la serie](https://pybonacci.org/tag/tutorial-de-pandas/).

**Trabajando con datos, indexación, selección,...**

¿Cómo podemos seleccionar, añadir, eliminar, mover,..., columnas, filas,...?

Para seleccionar una columna solo hemos de usar el nombre de la columna 
y pasarlo como si fuera un diccionario (o un atributo).

Para añadir una columna simplemente hemos de usar un nombre de columna 
no existente y pasarle los valores para esa columna.

Para eliminar una columna podemos usar `del` o el método `pop` del 
DataFrame.

Para mover una columna podemos usar una combinación de las metodologías 
anteriores.

Por ejemplo, vemos a seleccionar los valores de una columna:

```python
df = pd.DataFrame(np.random.randn(5,3),
                       index = ['primero','segundo','tercero','cuarto','quinto'],
                       columns = ['velocidad', 'temperatura','presion'])
print(df['velocidad'])
print(df.velocidad)
```

Hemos creado un DataFrame y para acceder a la columna velocidad lo 
podemos hacer de dos formas. O bien usando el nombre de la columna como 
si fuera una clave de un diccionario o bien usando el nombre de la 
columna como si fuera un atributo. En el caso de que los nombres de las 
columnas sean números, la segunda opción no podríais usarla...

Vamos a añadir una columna nueva al DataFrame. Es algo tan sencillo como 
usar un nombre de columna no existente y pasarle los datos:

```python
df['velocidad_maxima'] = np.random.randn(df.shape[0])
print(df)
```

Y el resultado sería:

```python
velocidad  temperatura   presion  velocidad_maxima
primero   0.175374     0.384571 -0.575126         -0.474630
segundo  -0.133466     0.987833  0.305844         -0.746577
tercero  -0.418224     0.603431  0.128822          1.545612
cuarto   -0.320517    -0.643183  0.319838          0.634203
quinto    0.955521    -0.295541 -1.277743          2.389485

[5 rows x 4 columns]
```

Pero qué pasa si quiero añadir la columna en un lugar específico. Para 
ello podemos usar el método `insert` (y de paso vemos como podemos 
borrar una columna):

```python
# forma 1 (borramos la columna 'velocidad_maxima' que está al final del df usando del)
#         (Colocamos la columna eliminada en la posición que especifiquemos)
print(df)
columna = df['velocidad_maxima']
del df['velocidad_maxima']
print(df)
print(columna)
df.insert(1, 'velocidad_maxima', columna)
print(df)
```

El resultado del DataFrame paso a paso sería:

```python
velocidad  temperatura   presion  velocidad_maxima
primero   0.175374     0.384571 -0.575126         -0.474630
segundo  -0.133466     0.987833  0.305844         -0.746577
tercero  -0.418224     0.603431  0.128822          1.545612
cuarto   -0.320517    -0.643183  0.319838          0.634203
quinto    0.955521    -0.295541 -1.277743          2.389485

[5 rows x 4 columns]
         velocidad  temperatura   presion
primero   0.175374     0.384571 -0.575126
segundo  -0.133466     0.987833  0.305844
tercero  -0.418224     0.603431  0.128822
cuarto   -0.320517    -0.643183  0.319838
quinto    0.955521    -0.295541 -1.277743

[5 rows x 3 columns]
primero   -0.474630
segundo   -0.746577
tercero    1.545612
cuarto     0.634203
quinto     2.389485
Name: velocidad_maxima, dtype: float64
         velocidad  velocidad_maxima  temperatura   presion
primero   0.175374         -0.474630     0.384571 -0.575126
segundo  -0.133466         -0.746577     0.987833  0.305844
tercero  -0.418224          1.545612     0.603431  0.128822
cuarto   -0.320517          0.634203    -0.643183  0.319838
quinto    0.955521          2.389485    -0.295541 -1.277743

[5 rows x 4 columns]
```

Una forma alternativa sería usando el método `pop`:

```python
# forma 2 (borramos usando el método pop y añadimos la columna borrada en la última posición de nuevo)
print(df)
columna = df.pop('velocidad_maxima')
print(df)
print(columna)
df.insert(3, 'velocidad_maxima', columna)
print(df)
```

Cuyo resultado, paso a paso sería:

```python
velocidad  velocidad_maxima  temperatura   presion
primero   0.175374         -0.474630     0.384571 -0.575126
segundo  -0.133466         -0.746577     0.987833  0.305844
tercero  -0.418224          1.545612     0.603431  0.128822
cuarto   -0.320517          0.634203    -0.643183  0.319838
quinto    0.955521          2.389485    -0.295541 -1.277743

[5 rows x 4 columns]
         velocidad  temperatura   presion
primero   0.175374     0.384571 -0.575126
segundo  -0.133466     0.987833  0.305844
tercero  -0.418224     0.603431  0.128822
cuarto   -0.320517    -0.643183  0.319838
quinto    0.955521    -0.295541 -1.277743

[5 rows x 3 columns]
primero   -0.474630
segundo   -0.746577
tercero    1.545612
cuarto     0.634203
quinto     2.389485
Name: velocidad_maxima, dtype: float64
         velocidad  temperatura   presion  velocidad_maxima
primero   0.175374     0.384571 -0.575126         -0.474630
segundo  -0.133466     0.987833  0.305844         -0.746577
tercero  -0.418224     0.603431  0.128822          1.545612
cuarto   -0.320517    -0.643183  0.319838          0.634203
quinto    0.955521    -0.295541 -1.277743          2.389485

[5 rows x 4 columns]
```

Para seleccionar datos concretos de un DataFrame podemos usar el índice, 
una rebanada, valores booleanos, la columna,...

```python
print('Seleccionamos la columna de velocidades')
print(df['velocidad'])
```

```python
Seleccionamos la columna de velocidades
primero    0.175374
segundo   -0.133466
tercero   -0.418224
cuarto    -0.320517
quinto     0.955521
Name: velocidad, dtype: float64
```

```python
print('Seleccionamos todas las columnas cuyo índice es igual a tercero')
print(df.xs('tercero'))
```

```python
Seleccionamos todas las columnas cuyo índice es igual a tercero
velocidad        -0.418224
temperatura       0.603431
presion           0.128822
velocidad_maxima  1.545612
Name: tercero, dtype: float64
```

```python
print('Seleccionamos todas las columnas cuyo índice está entre tercero y quinto')
print('Daos cuenta que en este caso los índices son inclusivos')
print(df.ix['tercero':'quinto'])
```

```python
Seleccionamos todas las columnas cuyo índice está entre tercero y quinto
Daos cuenta que en este caso los índices son inclusivos
         velocidad  temperatura   presion  velocidad_maxima
tercero  -0.418224     0.603431  0.128822          1.545612
cuarto   -0.320517    -0.643183  0.319838          0.634203
quinto    0.955521    -0.295541 -1.277743          2.389485

[3 rows x 4 columns]
```

```python
print('Seleccionamos todos los valores de velocidad donde la temperatura > 0')
print(df[df['temperatura' > 0]['velocidad'])
```

```python
Seleccionamos todos los valores de velocidad donde la temperatura > 0
primero    0.175374
segundo   -0.133466
tercero   -0.418224
Name: velocidad, dtype: float64
```

```python
print('Seleccionamos todos los valores de una columna por índice usando una')
print('rebanada (slice) de enteros')
print('Daos cuenta que en este caso el límite superior de la rebanada no se')
print('incluye (Python tradicional)')
print(df.ix[1:3])
```

```python
Seleccionamos todos los valores de una columna por índice usando una
rebanada (slice) de enteros
Daos cuenta que en este caso el límite superior de la rebanada no se
incluye (Python tradicional)
         velocidad  temperatura   presion  velocidad_maxima
segundo  -0.133466     0.987833  0.305844         -0.746577
tercero  -0.418224     0.603431  0.128822          1.545612

[2 rows x 4 columns]
```

```python
print(u'Seleccionamos filas y columnas')
print(df.ix[1:3, ['velocidad', 'presion']])
```

```python
Seleccionamos filas y columnas
         velocidad   presion
segundo  -0.133466  0.305844
tercero  -0.418224  0.128822

[2 rows x 2 columns]
```

```python
# Algunas de las cosas anteriores se pueden realizar sin usar los métodos .ix() o .xs()&lt;/span>
print(df['velocidad]
```

```python
segundo   -0.133466
tercero   -0.418224
Name: velocidad, dtype: float64
```

```python
# Da igual si colocamos el slice primero y después las columnas:
df['velocidad'][1:3] == df[1:3]['velocidad']
```

```python
segundo    True
tercero    True
Name: velocidad, dtype: bool
```

[Actualización: el método `ix` está discontinuado y se recomienda usar
los métodos `loc` e `iloc`.]

En lo anterior he estado usando los métodos `.ix()`, `.xs()` para 
obtener [partes del DataFrame](http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-advanced). 
Son [herramientas muy flexibles que nos permiten acceder a los datos de forma muy personalizada](http://pandas.pydata.org/pandas-docs/stable/indexing.html#different-choices-for-indexing-loc-iloc-and-ix). 
Otras opciones sería usar los métodos `.loc()`, `.iloc()`, `.select()`. 
Es importante tener en cuenta que las series devueltas cuando se indexa 
un DataFrame son solo vistas y no una copia de los propios datos. Por 
tanto, debes ser precavido cuando manipulas los datos (al igual que 
sucede con los numpy arrays y otros tipos de datos). Lo siguiente 
(hecho con numpy arrays) es equivalente para las estructuras de datos 
de Pandas.

```python
# Vista, ¡Cuidado!
a = np.random.rand(5)
data = a[0:2]
data[:] = -999
print(a)
# Copias
a = np.random.rand(5)
data = a[0:2].copy()
data[:] = -999
print(a)
a = np.random.rand(5)
data = 1 * a[0:2]
data[:] = -999
print(a)
a = np.random.rand(5)
np.copyto(data, a[0:2]) # En este caso, data tiene que existir
data[:] = -999
print(a)
a = np.random.rand(5)
data = np.array(a[0:2])
data[:] = -999
print(a)
```

```python
[ -9.99000000e+02  -9.99000000e+02   7.18723608e-01   5.30962716e-01
   3.43706883e-01]
[ 0.20812195  0.36386055  0.17570252  0.31071035  0.38838464]
[ 0.37175682  0.36962863  0.14481144  0.80786818  0.82803089]
[ 0.89958739  0.00190588  0.14769624  0.3378831   0.74536315]
[ 0.19285654  0.51489647  0.19612007  0.52342758  0.2006809 ]
```

Para acceder a los valores de los índices podemos usar `.index`.

```python
df.index
```

```python
Index(['primero', 'segundo', 'tercero', 'cuarto', 'quinto'], dtype='object')
```

Para acceder a los valores de las columnas podemos usar `.columns`.

```python
df.columns
```

```python
Index(['velocidad', 'temperatura', 'presion', 'velocidad_maxima'], dtype='object')
```

Otra vez hemos llegado al final. ¡¡Estad atentos a la próxima entrega!!
