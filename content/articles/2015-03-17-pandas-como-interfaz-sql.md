---
title: Pandas como interfaz SQL
date: 2015-03-17T03:37:25+00:00
author: Kiko Correoso
slug: pandas-como-interfaz-sql
tags: dataanalytics, datascience, pandas, pytables, sql, sqlite

# Mini tutorial de SQL para científicos

Hoy en día no se puede seguir trabajando con ficheros de texto habiendo tantas alternativas y, sobretodo, a medida que el tamaño de la información crece y crece y se hace inmanejable tratar ficheros de varios cientos de Mb. Es por ello que hoy vamos a ver por encima cómo podemos hacer consultas, modificar y crear nueva información en una base de datos SQL.  

**[Descargo de responsabilidad]** Esto no pretende ser un tutorial ni algo serio y riguroso, solo un análisis superficial sobre lo que puede ofrecer el manejo de SQL para trabajar con datos y va dirigido, principalmente, a científicos (o no) que se manejan todo el día con ficheros *.dat, *.txt o *.csv.

# ¿Qué es SQL?

SQL es un acrónimo para **S**tructured **Q**uery **L**anguage. Es un lenguaje que nos permite acceder a bases de datos SQL (bases de datos relacionales). Un RDBMS (**R**elational **D**ata**B**ase **M**anagement **S**ystem) es un sistema que nos permite acceder, crear, editar y gestionar bases de datos relacionales. Existen RDBMS muy populares como MySQL (MariaDB), PostgreSQL o SQLite. En el presente tutorial vamos a trabajar con SQLite por simplicidad y porque viene disponible con CPython.

# ¿Y Pandas?

Pandas dispone de funcionalidad que nos permite leer y escribir información en bases de datos relacionales.

# Vamos a crear una base de datos SQLite

Las bases de datos SQLite son bases de datos que no necesitan un servidor y que se guardan en disco. Para más información [pulsa aquí](https://duckduckgo.com/?q=sqlite). Podéis inspeccionar la base de datos que vayamos a crear, bastante simple, con [SQLite manager, un addon para firefox](https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/).

Como siempre, primero importamos todo lo necesario

    :::ptyhon
    import sqlite3
    import datetime as dt

    import pandas as pd
    import numpy as np

Mi configuración es la siguiente:

    %load_ext version_information
    %version_information pandas, numpy

**OUTPUT:**

<div>
  <table>
    <tr>
      <th>
        Software
      </th>
      
      <th>
        Version
      </th>
    </tr>
    
    <tr>
      <td>
        Python
      </td>
      
      <td>
        3.4.0 64bit [GCC 4.8.2]
      </td>
    </tr>
    
    <tr>
      <td>
        IPython
      </td>
      
      <td>
        3.0.0
      </td>
    </tr>
    
    <tr>
      <td>
        OS
      </td>
      
      <td>
        Linux 3.13.0 24 generic x86_64 with LinuxMint 17 qiana
      </td>
    </tr>
    
    <tr>
      <td>
        pandas
      </td>
      
      <td>
        0.15.2
      </td>
    </tr>
    
    <tr>
      <td>
        numpy
      </td>
      
      <td>
        1.9.2
      </td>
    </tr>
    
    <tr>
      <td colspan='2'>
        Thu Mar 12 20:07:15 2015 CET
      </td>
    </tr>
  </table>
</div>

Primero necesitamos poder conectar con la base de datos. Esto es de lo poco que diferirá con respecto a otros RDBMSs.

    conn = sqlite3.connect('pybodb.sqlite')

    # ejemplo con PostgreSQL usando psycopg2
    # import psycopg2
    # conn = psycopg2.connect(database='ejemplodb', user='kiko') 

    # ejemplo con MS ACCESS usando pyodbc (sí, en el trabajo tengo que usar estas cosas)
    # import pyodbc
    # conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=ejemplodb;") 

    # ...

Ahora que ya tenemos una conexión a la base de datos Pandas se puede encargar del trabajo sucio de 'hablar' con la base de datos y ayudarnos a interactuar directamente con los datos de la forma habitual y potente de Pandas.

Vamos a crear un DataFrame que usaremos como una tabla para insertar en la base de datos. Este DataFrame tendrá una columna de fechas, una de medidas de temperatura promedio diaria (inventada), una de precipitación acumulada en 24h (inventada), una columna con el tipo de sensor que midió la temperatura ese día y una última con el sensor que midió la precipitación.

    # fechas para cada día del 2014
    fechas = pd.date_range(dt.datetime(2014, 1, 1), dt.datetime(2014, 12, 31))
    # Temperatura media diaria durante 2014 en algún lugar del hemisferio Norte
    tmed = (np.random.randint(-5, 5, size = 365) + 
            20 * np.cos(np.arange( - 180, 365 - 180) * 2 * np.pi / 365) 
            + 10)
    # Precipitación acumulada en 24h
    prec = (20 * np.abs(np.random.randn(365) * 
            np.cos(np.arange(, 365) * 2 * np.pi / 365)))
    # Sensor que midió la temperatura
    marcaT = np.random.choice(['marcaT1', 'marcaT2', 'marcaT3'], size = 365)
    # Sensor midió la precipitación
    marcaP = np.random.choice(['marcaP1', 'marcaP2'], size = 365)

    # Creamos el dataframe y lo guardamos en una tabla llamada 'datos'
    df = pd.DataFrame(
            np.array([fechas.values, tmed, prec, marcaT, marcaP]).T,
            columns = ['fecha', 'tmedia','precipitacion','sensorT','sensorP'])
    df['fecha'] = pd.to_datetime(df['fecha'])
    df.to_sql('datos', con = conn, dtype = {'time': 'TIMESTAMP'})

Vamos a crear una segunda tabla para añadir un poco de complejidad a las consultas que hagamos posteriormente a la base de datos. Esta tabla contendrá información de los sensores usados para las medidas.

    # fechas para cada día del 2014
    sensores = ['marcaT1', 'marcaT2', 'marcaT3',
                'marcaP1', 'marcaP2']

    # Precisión de los sensores
    precision = [0.1, 0.5, 1,
                 2, 5]

    df = pd.DataFrame({'sensores': sensores, 'precision': precision})
    df.to_sql('sensores', con = conn)

Consultando la base de datos

Dentro de SQL tenemos comandos que se pueden integrar en diferentes categorías. Ahora vamos a usar _dql (data query language)_ que se usa para hacer consultas a la base de datos. Mirad en [esta chuleta para conocer más](http://www.sql-tutorial.net/SQL-Cheat-Sheet.pdf).

Como SQL no hace distinción de mayúsculas y minúsculas usaré mayúsculas para las palabras clave de SQL y así las distinguiremos un poco mejor. Para hacer una petición se usa `SELECT`. Veamos como es una consulta para conocer las tablas que existen en la base de datos (esta consulta es específica para SQLite):

    # Esto es específico para sqlite
    print(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn))
    # Para otras BBDD puedes buscar en internet :-)

**OUTPUT:**

           name
    0     datos
    1  sensores

En la consulta anterior hemos usados varias palabras clave: `SELECT`, `FROM`, `WHERE`. Este tipo de consultas serán de lo más habitual. Vamos a explotar lo que ya sabemos.  
Quiero los datos de todas las columnas de la tabla sensores (y pandas me lo meterá en un DataFrame, maravilloso!!!)

    df = pd.read_sql("SELECT * FROM sensores;", conn)
    print(df)

**OUTPUT:**

    :::
       index  precision sensores
    0      0        0.1  marcaT1
    1      1        0.5  marcaT2
    2      2        1.0  marcaT3
    3      3        2.0  marcaP1
    4      4        5.0  marcaP2

Ahora queremos los datos de precipitación de Junio junto con su fecha. Fijaos que el valor superior del rango no es inclusivo (`BETWEEN '2014-06-01' AND '2014-07-01'` nos da el dato hasta antes de `fecha = '2014-07-01'`):

    df = pd.read_sql("SELECT fecha, precipitacion FROM datos WHERE fecha BETWEEN '2014-06-01' AND '2014-07-01';", conn)
    print(df)

**OUTPUT:**

    :::
                      fecha  precipitacion
    0   2014-06-01 00:00:00      21.090544
    1   2014-06-02 00:00:00      19.514893
    2   2014-06-03 00:00:00       1.356933
    3   2014-06-04 00:00:00      14.466592
    4   2014-06-05 00:00:00      12.780801
    5   2014-06-06 00:00:00      28.293163
    6   2014-06-07 00:00:00       7.841272
    7   2014-06-08 00:00:00      22.278980
    8   2014-06-09 00:00:00      24.386602
    9   2014-06-10 00:00:00       4.158349
    10  2014-06-11 00:00:00       8.850627
    11  2014-06-12 00:00:00      24.572156
    12  2014-06-13 00:00:00      30.675862
    13  2014-06-14 00:00:00       5.986650
    14  2014-06-15 00:00:00      19.186014
    15  2014-06-16 00:00:00      36.980785
    16  2014-06-17 00:00:00      11.822683
    17  2014-06-18 00:00:00       1.774325
    18  2014-06-19 00:00:00       8.043394
    19  2014-06-20 00:00:00       9.909083
    20  2014-06-21 00:00:00      26.050138
    21  2014-06-22 00:00:00      32.829371
    22  2014-06-23 00:00:00       1.067285
    23  2014-06-24 00:00:00      41.178811
    24  2014-06-25 00:00:00       4.357684
    25  2014-06-26 00:00:00      36.863093
    26  2014-06-27 00:00:00      18.923454
    27  2014-06-28 00:00:00       5.641863
    28  2014-06-29 00:00:00       5.831242
    29  2014-06-30 00:00:00      45.159804

Ahora quiero los datos de temperatura de los sensores con una precisión superior a 0.5 (el sensor _marcaT1_ es el único que me da precisión superior a 0.5):

    df = pd.read_sql("SELECT fecha, tmedia FROM datos WHERE datos.sensorT = 'marcaT1';", conn)
    print(df)

**OUTPUT:**

    :::
                       fecha     tmedia
    0    2014-01-01 00:00:00  -5.981482
    1    2014-01-08 00:00:00  -9.733159
    2    2014-01-09 00:00:00 -12.674186
    3    2014-01-11 00:00:00  -5.538770
    4    2014-01-13 00:00:00  -5.380197
    5    2014-01-15 00:00:00 -13.198654
    6    2014-01-17 00:00:00 -12.994357
    7    2014-01-19 00:00:00  -8.767548
    8    2014-01-31 00:00:00  -8.950818
    9    2014-02-02 00:00:00  -4.575402
    10   2014-02-03 00:00:00  -7.380298
    11   2014-02-09 00:00:00  -4.109866
    12   2014-02-10 00:00:00  -7.882079
    13   2014-02-13 00:00:00  -8.172534
    14   2014-02-16 00:00:00  -1.425199
    15   2014-02-18 00:00:00  -0.906962
    16   2014-02-20 00:00:00  -7.373428
    17   2014-02-24 00:00:00  -1.263014
    18   2014-02-27 00:00:00  -3.394876
    19   2014-03-05 00:00:00  -1.577839
    20   2014-03-07 00:00:00   4.049144
    21   2014-03-08 00:00:00   0.366216
    22   2014-03-20 00:00:00   3.320033
    23   2014-03-24 00:00:00  10.681308
    24   2014-03-28 00:00:00  11.053572
    25   2014-03-29 00:00:00   5.397594
    26   2014-03-31 00:00:00  14.086071
    27   2014-04-08 00:00:00  15.830806
    28   2014-04-15 00:00:00  16.190236
    29   2014-04-18 00:00:00  11.180340
    ..                   ...        ...
    94   2014-10-11 00:00:00   6.982189
    95   2014-10-12 00:00:00   6.645535
    96   2014-10-13 00:00:00   3.310172
    97   2014-10-16 00:00:00   8.312816
    98   2014-10-18 00:00:00   4.656174
    99   2014-10-20 00:00:00  -1.992949
    100  2014-10-22 00:00:00   3.366216
    101  2014-10-30 00:00:00   1.900779
    102  2014-11-04 00:00:00  -6.545832
    103  2014-11-08 00:00:00  -4.642068
    104  2014-11-11 00:00:00   0.574801
    105  2014-11-15 00:00:00  -5.413343
    106  2014-11-18 00:00:00  -8.109866
    107  2014-11-21 00:00:00  -2.766101
    108  2014-11-22 00:00:00  -4.975587
    109  2014-11-25 00:00:00  -6.575402
    110  2014-11-28 00:00:00  -9.131020
    111  2014-11-30 00:00:00  -5.476142
    112  2014-12-03 00:00:00  -5.954868
    113  2014-12-10 00:00:00  -4.883750
    114  2014-12-11 00:00:00 -13.994357
    115  2014-12-12 00:00:00  -8.099335
    116  2014-12-14 00:00:00 -13.292284
    117  2014-12-16 00:00:00  -8.462367
    118  2014-12-18 00:00:00  -8.609383
    119  2014-12-21 00:00:00 -13.786284
    120  2014-12-23 00:00:00 -12.874932
    121  2014-12-25 00:00:00  -7.940023
    122  2014-12-26 00:00:00 -11.963711
    123  2014-12-27 00:00:00  -8.981482

    [124 rows x 2 columns]

Si os fijáis, en la consulta anterior he usado `datos.sensorT` (_tabla.columna_). Esto solo será necesario si estamos trabajando con varias tablas y una columna se puede llamar igual en varias tablas. De esta forma no hay posibilidad de equivocarse ya que usamos 'nombres y apellidos'.  
Vamos a hacer una consulta que nos dé el mismo resultado pero que enlaza varias consultas (un `SELECT` dentro de un `SELECT`). También la represento de forma un poco más estructurada para que sea más legible:

    :::
    # La misma consulta de antes pero sin saber la precisión de cada uno de los sensores a priori
    q = """
    SELECT 
     fecha, tmedia 
    FROM 
     datos 
    WHERE 
     datos.sensorT = 
     (SELECT 
     sensores 
     FROM 
     sensores 
     WHERE 
     precision < 0.5);"""

    df = pd.read_sql(q, conn)

    print(df)

**OUTPUT:**

    :::
                       fecha     tmedia
    0    2014-01-01 00:00:00  -5.981482
    1    2014-01-08 00:00:00  -9.733159
    2    2014-01-09 00:00:00 -12.674186
    3    2014-01-11 00:00:00  -5.538770
    4    2014-01-13 00:00:00  -5.380197
    5    2014-01-15 00:00:00 -13.198654
    6    2014-01-17 00:00:00 -12.994357
    7    2014-01-19 00:00:00  -8.767548
    8    2014-01-31 00:00:00  -8.950818
    9    2014-02-02 00:00:00  -4.575402
    10   2014-02-03 00:00:00  -7.380298
    11   2014-02-09 00:00:00  -4.109866
    12   2014-02-10 00:00:00  -7.882079
    13   2014-02-13 00:00:00  -8.172534
    14   2014-02-16 00:00:00  -1.425199
    15   2014-02-18 00:00:00  -0.906962
    16   2014-02-20 00:00:00  -7.373428
    17   2014-02-24 00:00:00  -1.263014
    18   2014-02-27 00:00:00  -3.394876
    19   2014-03-05 00:00:00  -1.577839
    20   2014-03-07 00:00:00   4.049144
    21   2014-03-08 00:00:00   0.366216
    22   2014-03-20 00:00:00   3.320033
    23   2014-03-24 00:00:00  10.681308
    24   2014-03-28 00:00:00  11.053572
    25   2014-03-29 00:00:00   5.397594
    26   2014-03-31 00:00:00  14.086071
    27   2014-04-08 00:00:00  15.830806
    28   2014-04-15 00:00:00  16.190236
    29   2014-04-18 00:00:00  11.180340
    ..                   ...        ...
    94   2014-10-11 00:00:00   6.982189
    95   2014-10-12 00:00:00   6.645535
    96   2014-10-13 00:00:00   3.310172
    97   2014-10-16 00:00:00   8.312816
    98   2014-10-18 00:00:00   4.656174
    99   2014-10-20 00:00:00  -1.992949
    100  2014-10-22 00:00:00   3.366216
    101  2014-10-30 00:00:00   1.900779
    102  2014-11-04 00:00:00  -6.545832
    103  2014-11-08 00:00:00  -4.642068
    104  2014-11-11 00:00:00   0.574801
    105  2014-11-15 00:00:00  -5.413343
    106  2014-11-18 00:00:00  -8.109866
    107  2014-11-21 00:00:00  -2.766101
    108  2014-11-22 00:00:00  -4.975587
    109  2014-11-25 00:00:00  -6.575402
    110  2014-11-28 00:00:00  -9.131020
    111  2014-11-30 00:00:00  -5.476142
    112  2014-12-03 00:00:00  -5.954868
    113  2014-12-10 00:00:00  -4.883750
    114  2014-12-11 00:00:00 -13.994357
    115  2014-12-12 00:00:00  -8.099335
    116  2014-12-14 00:00:00 -13.292284
    117  2014-12-16 00:00:00  -8.462367
    118  2014-12-18 00:00:00  -8.609383
    119  2014-12-21 00:00:00 -13.786284
    120  2014-12-23 00:00:00 -12.874932
    121  2014-12-25 00:00:00  -7.940023
    122  2014-12-26 00:00:00 -11.963711
    123  2014-12-27 00:00:00  -8.981482

    [124 rows x 2 columns]

Podemos decirle que nos pase solo una serie de valores. Por ejemplo, solo quiero los tres valores más altos de precipitación de diciembre:

    :::
    q = """
    SELECT 
     fecha, precipitacion 
    FROM 
     datos 
    WHERE 
     fecha > '2014-11-30'
    ORDER BY
     precipitacion DESC
    LIMIT
     3"""

    df = pd.read_sql(q, conn)
    print(df)

**OUTPUT:**

                     fecha  precipitacion
    0  2014-12-31 00:00:00      50.047120
    1  2014-12-01 00:00:00      43.913895
    2  2014-12-04 00:00:00      37.344830

En la consulta anterior le hemos pedido que nos ordenase por los valores de precipitación de forma descendente (es decir, por el final) y le hemos pedido que nos limitase la búsqueda a tres valores, los tres valores más altos.

# ¿Os ha picado el gusanillo?

Todo esto era para ver si os picaba un poco el gusanillo y dejáis (dejamos) de usar tanto fichero de texto/excel/csv y usamos opciones más ricas y potentes que existen por ahí.

# Enlaces

*  Un [minitutorial sobre SQL](http://opentechschool.github.io/sql-tutorial/index.html) muy ameno.
*  Nuestro (inacabado) [tutorial sobre PyTables](http://pybonacci.org/tag/pytables/).
*  Y [¿por qué no usar netCDF?](http://pybonacci.org/2012/12/03/por-que-usar-netcdf/)
*  Funcionalidad [SQL en pandas](http://pandas.pydata.org/pandas-docs/stable/io.html?highlight=read_sql#io-sql).
*  [IPython-sql](https://github.com/catherinedevlin/ipython-sql), para trabajar con sql en el notebook.
*  [SQLAlchemy](http://www.sqlalchemy.org/) para facilitarnos la vida cuando trabajamos con Pandas y bases de datos.
*  [SQLite manager, un addon para firefox](https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/).

# Y cerramos la conexión (literal) por hoy.

`conn.close() # :-)`

Y el [notebook en el repositorio](http://nbviewer.ipython.org/github/Pybonacci/notebooks/blob/master/Pandas%20como%20interfaz%20SQL.ipynb), como siempre.
