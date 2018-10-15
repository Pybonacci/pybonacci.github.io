---
title: Gráficas interactivas con Plotly
date: 2014-08-22T17:50:16+00:00
author: Pablo Fernández
slug: graficas-interactivas-con-plotly
tags: gráficas, plotly, python, tutorial

Podéis conseguir el [notebook](http://nbviewer.ipython.org/github/pybonacci/notebooks/blob/master/plotly/Heathrow.ipynb) y los archivos asociados en [GitHub](https://github.com/Pybonacci/notebooks/tree/master/plotly).

En un [artículo anterior](https://pybonacci.org/2014/08/05/de-matplotlib-a-la-web-con-plotly/) ya vimos como pasar las gráficas creadas con `matplotlib` a `plotly` para obtener cierto nivel de interacción con los datos en la web. Ahora, lo que vamos a ver es cómo crear gráficas directamente con `plotly`. Para ello vamos a utilizar:

  * `pandas 0.14.1`, para trabajar con tablas de datos.
  * `plotly 1.2.6`, para crear las gráficas.

Importamos los paquetes de la manera habitual en cada caso.

    :::python
    import pandas as pd
    import plotly.plotly as py
    from plotly.graph_objs import *

En el caso de Plotly hemos importado además unos objetos `graph_objs` que nos serán de ayuda a la hora de crear las gráficas. Trabajar con la API de Plotly en Python se resume en trabajar con _listas y diccionarios_ de Python. Los `graph_objs` de Plotly nos ayudarán a trabajar con estas listas y diccionarios proporcionando ayuda y validando los datos y parámetros introducidos.

Entre los objetos que importamos tenemos los bloques principales de trabajo:

  * **Figure**, diccionario que representa la figura a representar en `plotly`.
  * **Data**, lista para englobar todos los trazos a representar en una gráfica, ya sean tipo _Scatter_, _Heatmap_, _Box_, etc.
  * **Layout**, diccionario que define los detalles de la disposición de la figura.

<!--more Sigue leyendo-->

    :::python
    help(Figure)

    Help on class Figure in module plotly.graph_objs.graph_objs:
    class Figure(PlotlyDict)
     |  A dictionary-like object representing a figure to be rendered in plotly.
     |
     |      This is the container for all things to be rendered in a figure.
     |
     |      For help with setting up subplots, run:
     |      &#096;help(plotly.tools.get_subplots)&#096;
     |
     |
     |  Quick method reference:
     |
     |      Figure.update(changes)
     |      Figure.strip_style()
     |      Figure.get_data()
     |      Figure.to_graph_objs()
     |      Figure.validate()
     |      Figure.to_string()
     |      Figure.force_clean()
     |
     |  Valid keys:
     |
     |      data [required=False] (value=Data object | array-like of one or several
     |      dictionaries):
     |          A list-like array of the data trace(s) that is/are to be visualized.
     |
     |          For more, run &#096;help(plotly.graph_objs.Data)&#096;
     |
     |      layout [required=False] (value=Layout object | dictionary-like):
     |          A dictionary-like object that contains the layout parameters (e.g.
     |          information about the axis, global settings and layout information
     |          related to the rendering of the figure).
     |
     |          For more, run &#096;help(plotly.graph_objs.Layout)&#096;
     |
    [...]

    :::python
    help(Data)

    Help on class Data in module plotly.graph_objs.graph_objs:
    class Data(PlotlyList)
     |  A list of traces to be shown on a plot/graph.
     |
     |      Any operation that can be done with a standard list may be used with Data.
     |      Instantiation requires an iterable (just like list does), for example:
     |
     |      Data([Scatter(), Heatmap(), Box()])
     |
     |      Valid entry types: (dict or any subclass of Trace, i.e., Scatter, Box, etc.)
     |
    [...]

    :::python
    help(Layout)

    Help on class Layout in module plotly.graph_objs.graph_objs:
    class Layout(PlotlyDict)
     |  A dictionary-like object holding plot settings for plotly figures.
     |
     |
     |  Quick method reference:
     |
     |      Layout.update(changes)
     |      Layout.strip_style()
     |      Layout.get_data()
     |      Layout.to_graph_objs()
     |      Layout.validate()
     |      Layout.to_string()
     |      Layout.force_clean()
     |
     |  Valid keys:
     |
     |      title [required=False] (value=string):
     |          The title of the figure.
     |
    [...]

Como vemos, `Figure` y `Layout` son objetos de tipo diccionario y `Data` es un objeto de tipo lista. En el caso de `Data`, el orden es importante pues determina el orden de composición de los trazos, empezando por el primero objeto en `Data`. Por ejemplo, representar una línea sobre una barras no produce, normalmente, el mismo resultado que representar unas barras sobre una línea.

En Plotly cada tipo de gráfica tiene su propio objeto (_trace graph object_) como son `Scatter`, `Bar` o `Histogram`.

    :::python
    help(Scatter)

    Help on class Scatter in module plotly.graph_objs.graph_objs:
    class Scatter(PlotlyTrace)
     |  A dictionary-like object for representing a scatter plot in plotly.
     |
     |      Example:
     |
     |          py.plot([Scatter(name=';tacters';, x=[1,4,2,3], y=[1,6,2,1])])
     |
     |
     |  Quick method reference:
     |
     |      Scatter.update(changes)
     |      Scatter.strip_style()
     |      Scatter.get_data()
     |      Scatter.to_graph_objs()
     |      Scatter.validate()
     |      Scatter.to_string()
     |      Scatter.force_clean()
     |
     |  Valid keys:
     |
    [...]

## Ejemplo práctico: aeropuerto de Heathrow {#ejemplo-práctico-aeropuerto-de-heathrow}

Hecha la presentación de Plotly pasamos a un ejemplo práctico de uso de la herramienta. Para ello tomaremos datos de [estadísticas de tráfico](http://www.heathrowairport.com/about-us/investor-centre/results-and-performance/traffic-statistics) del aeropuerto de Heathrow, el tercer mayor del mundo por tráfico de pasajeros.

### Datos estadísticos {#datos-estadísticos}

Los datos son proporcionados en un fichero Excel que podemos importar con Pandas.

    :::python
    pasajeros = pd.io.excel.read_excel('07-Heathrow_Monthly_Traffic_Statistics_(Jan_2005-Jul_2014).xls',
                                       sheetname=0, # tomamos la primera hoja del archivo
                                       header=2, # la cebecera empieza en la fila 3
                                       index_col=0) # empleamos las fechas como indices
    pasajeros.head(5)

<div class="output_wrapper">
  <div class="output">
    <div class="output_html rendered_html output_subarea output_pyout">
      <div style="overflow:auto">
        <table border="1" class="dataframe">
          <tr style="text-align: right">
            <th>
            </th>
            
            <th>
              Heathrow
            </th>
            
            <th>
              Southampton
            </th>
            
            <th>
              Glasgow
            </th>
            
            <th>
              Aberdeen
            </th>
            
            <th>
              Non-London Airports
            </th>
            
            <th>
              UK Total
            </th>
          </tr>
          
          <tr>
            <th>
              Month
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
          </tr>
          
          <tr>
            <th>
              2005-01-01
            </th>
            
            <td>
              5141123
            </td>
            
            <td>
              99945
            </td>
            
            <td>
              504138
            </td>
            
            <td>
              186378
            </td>
            
            <td>
              790461
            </td>
            
            <td>
              5931584
            </td>
          </tr>
          
          <tr>
            <th>
              2005-02-01
            </th>
            
            <td>
              4753591
            </td>
            
            <td>
              109120
            </td>
            
            <td>
              506851
            </td>
            
            <td>
              189925
            </td>
            
            <td>
              805896
            </td>
            
            <td>
              5559487
            </td>
          </tr>
          
          <tr>
            <th>
              2005-03-01
            </th>
            
            <td>
              5708627
            </td>
            
            <td>
              131983
            </td>
            
            <td>
              603225
            </td>
            
            <td>
              227621
            </td>
            
            <td>
              962829
            </td>
            
            <td>
              6671456
            </td>
          </tr>
          
          <tr>
            <th>
              2005-04-01
            </th>
            
            <td>
              5573022
            </td>
            
            <td>
              145749
            </td>
            
            <td>
              641107
            </td>
            
            <td>
              232191
            </td>
            
            <td>
              1019047
            </td>
            
            <td>
              6592069
            </td>
          </tr>
          
          <tr>
            <th>
              2005-05-01
            </th>
            
            <td>
              5636621
            </td>
            
            <td>
              168971
            </td>
            
            <td>
              795732
            </td>
            
            <td>
              242493
            </td>
            
            <td>
              1207196
            </td>
            
            <td>
              6843817
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</div>

    :::python
    mercancias = pd.io.excel.read_excel('07-Heathrow_Monthly_Traffic_Statistics_(Jan_2005-Jul_2014).xls',
                                        sheetname=5, # tomamos la sexta hoja del archivo
                                        header=2, # la cebecera empieza en la fila 3
                                        index_col=0) # empleamos las fechas como indices
    mercancias.head(5)

<div class="output_wrapper">
  <div class="output">
    <div class="output_html rendered_html output_subarea output_pyout">
      <div style="overflow:auto">
        <table border="1" class="dataframe">
          <tr style="text-align: right">
            <th>
            </th>
            
            <th>
              Heathrow
            </th>
            
            <th>
              Southampton
            </th>
            
            <th>
              Glasgow
            </th>
            
            <th>
              Aberdeen
            </th>
            
            <th>
              Non-London Airports
            </th>
            
            <th>
              UK Total
            </th>
          </tr>
          
          <tr>
            <th>
              Month
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
          </tr>
          
          <tr>
            <th>
              2005-01-01
            </th>
            
            <td>
              98781.175
            </td>
            
            <td>
              16.237
            </td>
            
            <td>
              491.582
            </td>
            
            <td>
              304.274
            </td>
            
            <td>
              812.093
            </td>
            
            <td>
              99593.268
            </td>
          </tr>
          
          <tr>
            <th>
              2005-02-01
            </th>
            
            <td>
              99555.454
            </td>
            
            <td>
              16.554
            </td>
            
            <td>
              545.170
            </td>
            
            <td>
              310.282
            </td>
            
            <td>
              872.006
            </td>
            
            <td>
              100427.460
            </td>
          </tr>
          
          <tr>
            <th>
              2005-03-01
            </th>
            
            <td>
              109387.896
            </td>
            
            <td>
              18.830
            </td>
            
            <td>
              578.286
            </td>
            
            <td>
              368.156
            </td>
            
            <td>
              965.272
            </td>
            
            <td>
              110353.168
            </td>
          </tr>
          
          <tr>
            <th>
              2005-04-01
            </th>
            
            <td>
              108057.553
            </td>
            
            <td>
              18.277
            </td>
            
            <td>
              569.431
            </td>
            
            <td>
              321.004
            </td>
            
            <td>
              908.712
            </td>
            
            <td>
              108966.265
            </td>
          </tr>
          
          <tr>
            <th>
              2005-05-01
            </th>
            
            <td>
              110612.691
            </td>
            
            <td>
              17.466
            </td>
            
            <td>
              661.753
            </td>
            
            <td>
              369.324
            </td>
            
            <td>
              1048.543
            </td>
            
            <td>
              111661.234
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</div>

Como podemos ver, se trata de una serie temporal. Y puesto que los datos se proporcionan mes a mes, podríamos deshacernos del día del mes indicandole a Pandas que se trata de un periodo de frecuencia mensual con `to_period`. Pero no es necesario, pues como veremos más adelante, Plotly es capaz de _intuir_ que queremos representar los datos mes a mes.

    :::python
    pasajeros.to_period('M').head(2)

<div class="output_wrapper">
  <div class="output">
    <div class="output_html rendered_html output_subarea output_pyout">
      <div style="overflow:auto">
        <table border="1" class="dataframe">
          <tr style="text-align: right">
            <th>
            </th>
            
            <th>
              Heathrow
            </th>
            
            <th>
              Southampton
            </th>
            
            <th>
              Glasgow
            </th>
            
            <th>
              Aberdeen
            </th>
            
            <th>
              Non-London Airports
            </th>
            
            <th>
              UK Total
            </th>
          </tr>
          
          <tr>
            <th>
              Month
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
            
            <th>
            </th>
          </tr>
          
          <tr>
            <th>
              2005-01
            </th>
            
            <td>
              5141123
            </td>
            
            <td>
              99945
            </td>
            
            <td>
              504138
            </td>
            
            <td>
              186378
            </td>
            
            <td>
              790461
            </td>
            
            <td>
              5931584
            </td>
          </tr>
          
          <tr>
            <th>
              2005-02
            </th>
            
            <td>
              4753591
            </td>
            
            <td>
              109120
            </td>
            
            <td>
              506851
            </td>
            
            <td>
              189925
            </td>
            
            <td>
              805896
            </td>
            
            <td>
              5559487
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</div>

### Representación gráfica de los datos {#representación-gráfica-de-los-datos}

Si ya hemos guardado nuestras credenciales de Plotly en el ordenador, al importar el paquete como

    :::python
    import plotly.plotly as py

ya nos _logueamos_ automáticamente en el servidor sin tener que acceder mediante

    :::python
    py.sign_in('username', 'api_key')

Una figura (`Figure`) Plotly se compone de los datos a representar (`Data`) y de un formato (`Layout`), y estos a su vez no son más que un conjunto de listas y diccionarios que Plotly se encargará de convertir a un formato [JSON](http://en.wikipedia.org/wiki/Json). Como hemos mencionado arriba, Plotly proporciona una serie de `graph_objs` que nos facilitarán la tarea de componer gráficas interactivas y que veremos a continuación.

#### Data {#data}

Empezamos por el conjunto de datos a representar. En este caso vamos a representar el tráfico mensual de pasajeros en los aeropuertos británicos del grupo [Heathrow](http://en.wikipedia.org/wiki/Heathrow_Airport_Holdings), participada al 25% por [Ferrovial](http://es.wikipedia.org/wiki/Ferrovial), que incluye los aeropuertos de:

  * London Heathrow Airport
  * Southampton Airport
  * Glasgow Airport
  * Aberdeen Airport

Para representar estos datos nos valdremos de la herramienta `Data` que, como hemos visto anteriormente, admite una lista de objetos. En nuestro caso, líneas. Para ello nos valdremos de `Scatter` (_dispersión_) al cual pasaremos los siguentes parámetros:

  * `name`, nombre que damos a la línea, en nuestro caso, el nombre del aeropuerto.
  * `x`, array con los meses del año que corresponden al _index_ de nuestro `DataFrame`.
  * `y`, array con el número de pasajeros correspondientes a cada aeropuerto.
  * `mode`, cadena de texto que indica el tipo de representación que queremos, ya sea `'lines'`, `'markers'`, `'text'` o una combinación de ellos como podría ser `'lines+markers'`.

Puesto que se trata de una lista con cuatro líneas a representar, haremos uso de las [list comprehensions](https://docs.python.org/3.4/tutorial/datastructures.html#list-comprehensions) de Python.

    :::python
    p_data = Data([Scatter(name=col,
                           x=pasajeros.index,
                           y=pasajeros[col],
                           mode='lines') for col in pasajeros.columns.values[:4]])

#### Layout {#layout}

Ya con los datos a representar definidos, ahora podemos pasar a retocar el _layout_ de la figura. Para ello vamos a añadir un título a la gráfica y a los ejes _x_ e _y_. Otra cosa que haremos también es encuadrar la gráfica con

    :::python
    showline=True, mirror='ticks', linewidth=2

y reducir los margenes derecho `r` y superior `t` para aprovechar mejor el espacio.

    :::python
    p_layout = Layout(title='Tráfico mensual de pasajeros en aeropuertos del grupo Heathrow',
                      xaxis=XAxis(title='Mes', showgrid=False, showline=True, mirror='ticks', linewidth=2),
                      yaxis=YAxis(title='Pasajeros', zeroline=False, showline=True, mirror='ticks', linewidth=2),
                      margin=Margin(r=20, t=80))

#### Figure {#figure}

Una vez ya tenemos los datos y el _layout_ podemos pasar a componer la figura y subirla al servidor.

    :::python
    p_fig = Figure(data=p_data, layout=p_layout)
    p_plot = py.iplot(p_fig, filename='pybonacci/heathrow-pasajeros')

### Diccionarios y listas {#diccionarios-y-listas}

Tanto `Figure` como `Layout`, `XAxis`, `YAxis` y `Margin` se podrían substituir por la expresión `dict()` pues, como ya hemos mencionados, Plotly trabaja con diccionarios y listas de Python. Sin embargo, el utilizar estas herramientas de `plotly.graph_objs` nos da acceso a la ayuda, y nos permite validar los parámetros introducidos.

    :::python
    m_data = Data([Scatter(name=col,
                           x=mercancias.index,
                           y=mercancias[col],
                           mode='lines') for col in pasajeros.columns.values[:4]])

Podemos hacer lo mismo con `dict()`, pero cualquier error pasará desapercibido hasta el final.

    :::python
    m_layout = dict(title='Tráfico mensual de mercancías en aeropuertos del grupo Heathrow',
                    xaxis=dict(title='Mes', showgrid=False, showline=True, mirror='ticks', linewidth=2),
                    yaxis=dict(title='Mercancías (t)', zeroline=False, showline=True, mirror='ticks', linewidth=2),
                    margin=dict(r=20, t=80))

    :::python
    m_fig = Figure(data=m_data, layout=m_layout)
    m_plot = py.iplot(m_fig, filename='pybonacci/heathrow-mercancias')

### Interpretación de los datos {#interpretación-de-los-datos}

Disponemos de una muestra lo suficientemente grande como desaprovechar la oportunidad de extraer alguna conclusión al respecto. Y contamos con la ventaja de poder hacer zoom en los datos, lo cual resulta especialmente útil en le tráfico de mercancías, donde el aeropuerto de Heathrow está varios órdenes de magnitud por encima del resto.

#### Pasajeros {#pasajeros}

Vemos claramente que en los meses de verano hay un aumento del número de pasajeros en todos los aeropuertos del grupo. También se aprecia un ligero repunte en el mes de diciembre con motivo, previsiblemente, de las vacaciones de navidad. Esto lo podemos visualizar de otra manera mediante un `Heatmap` del aeropuerto de Heathrow.

Para ello vamos a utilizar el paquete `calendar` que nos permitirá crear una lista con los nombres de los meses; y Numpy para crear una lista con los años.

    :::python
    import calendar
    import numpy as np

Para representar el `Heatmap` necesitaremos agrupar los datos por años o meses, en función del eje _y_ que tomemos. En este caso hemos decido representar los meses en el eje de ordenadas, por lo tanto agruparemos los datos por meses. Para ello nos valdremos de una [función anónima](https://docs.python.org/3.4/reference/expressions.html#lambda).

    :::python
    gb = lambda x: x.month

    :::python
    data = Data([Heatmap(x=np.arange(2005,2015),
                         y=calendar.month_abbr[1:],
                         z=[grp['Heathrow'] for key, grp in pasajeros.groupby(gb)],
                         colorscale='Portland')])

En el eje _x_ hemos colocado los años, en el eje _y_ los meses, y la intensidad del color viene determinada por el número de pasajeros.

Con `Layout` añadimos el título de la gráfica y los nombres de los ejes, y también podemos especificar el tamaño de la gráfica deshabilitando el `autosize` y definiendo nuestro propio ancho y alto.

    :::python
    layout = Layout(title='Tráfico de pasajeros en el aeropuerto de Heathrow',
                    autosize=False,
                    width=550,
                    height=550,
                    xaxis=XAxis(title='Año', showgrid=False),
                    yaxis=YAxis(title='Mes', showgrid=False))

Ya podemos publicar nuestra gráfica de la manera habitual.

    :::python
    heatmap_plot = py.iplot(Figure(data=data,layout=layout), filename='pybonacci/heathrow-heatmap')

#### Mercancías {#mercancías}

Si en el transporte de pasajeros hay un patrón claro, el transporte de mercancías por avión no muestra signos de estacionalidad. Para verlo mejor podríamos volver a emplear un `Heatmap`, pero vamos a hacerlo con un [diagrama de caja](http://es.wikipedia.org/wiki/Diagrama_de_caja) `Box` para el aeropuerto de Heathrow.

Aprovecharemos nuevamente la agrupación por meses que hemos empleado para el `Heatmap` de pasajeros. Nuevamente hacemos uso de las list comprehensions de Python para crear una lista de bloques, cada uno correspondiente a un mes. Lo mismo podríamos conseguirlo sin crear una lista y sin necesidad de agrupar si en vez de asignar un `name` asignamos un único array `x` con el valor del mes correspondiente a cada `y`. Con `boxpoints='all'` lo que hacemos es mostrar los puntos de la muestra al lado de cada bloque.

    :::python
    data = Data([Box(name=calendar.month_abbr[key],
                     y=grp['Heathrow'].values,
                     boxpoints='all') for key, grp in mercancias.groupby(gb)])

Añadimos, como es costumbre, un título a la gráfica y aprovechamos para ocultar la leyenda y ajustar los margenes.

    :::python
    layout = Layout(title='Tráfico de mercancías en el aeropuerto de Heathrow (2005-2014)',
                    showlegend=False,
                    margin=Margin(r=20, t=90))

    :::python
    box_plot = py.iplot(Figure(data=data, layout=layout), filename='pybonacci/heathrow-box')

#### Pasajeros vs mercancías {#pasajeros-vs-mercancías}

Hasta ahora hemos visto por separado los datos de pasajeros y mercancías. Compararemos en una única gráfica los datos del aeropuerto de Glasgow. Para facilitar la visualización y compensar la diferencia de magnitud utilizaremos múltiples ejes y, de paso, emplearemos diferentes representaciones para el tráfico de pasajeros y el de mercancías.

Los pasajeros los representaremos mediante líneas y puntos `'lines+markers'` y le asignamos el segundo eje _y_ `'y2'`, pues vamos a querer que nos lo represente por encima de las barras de tráfico de mercancías. El orden en Plotly es importante. Vamos a representar las lineas de color dorado primero como horizontales y luego verticales de un valor a otro con `shape='hv'`. Los puntos serán de un color dorado más claro con el borde también dorado.

    :::python
    pas = Scatter(name='Pasajeros',
                  x=pasajeros.index,
                  y=pasajeros['Glasgow'],
                  yaxis='y2',
                  mode='lines+markers',
                  line=Line(shape='hv', color='darkgoldenrod'),
                  marker=Marker(color='goldenrod',
                                line=Line(color='darkgoldenrod', width=2)))

Por su parte, el tráfico de mercancías lo representaremos como barras verticales de color gris claro. Por defecto se le asigna el primer eje _y_.

    :::python
    mer = Bar(name='Mercancías',
              x=pasajeros.index,
              y=mercancias['Glasgow'],
              marker=Marker(color='lightgray'))

Creamos la lista con los elementos a representar.

    :::python
    data = Data([mer, pas])

Por último configuramos el _layout_ añadiendo un título a la gráfica y configurando los ejes.

    :::python
    layout = Layout(title='Tráfico de pasajeros y mercancías en el aeropuerto de Glasgow',
                    showlegend=False,
                    xaxis=XAxis(title='Mes'),
                    yaxis=YAxis(title='Mercancías (t)',
                                showgrid=False),
                    yaxis2=YAxis(title='Pasajeros',
                                 showgrid=False,
                                 overlaying='y',
                                 side='right'))

Incluimos también una nota de texto indicando la fuente de los datos. Plotly nos permite untilizar un subconjunto de etiquetas HTML para dar formato a los textos para por ejemplo incluir nuevas líneas (`<br>`) o añadir hipervínculos (`<a href='...'></a>`) que podremos utilizar en cualquier texto de la gráfica (títulos y anotaciones).

    :::python
    fuente = Annotation(text="Fuente: LHR Airports Limited",
                        xref='paper', # empleamos coordenadas 'paper', con ello la nota no se moverá al mover los ejes.
                        yref='paper',
                        x=0,
                        y=-0.15,
                        showarrow=False)

Actualizamos el diccionario de _layout_ de la gráfica.

    :::python
    layout.update(annotations=Annotations([fuente]))

    :::python
    ma_plot = py.iplot(Figure(data=data, layout=layout), filename='pybonacci/heathrow-multipleaxis')

## Mucho más {#mucho-más}

Aquí sólo hemos mostrado una pequeña parte del potencial de Plotly. Todo aquel que quiere ampliar detalles encontrará mucha más información en el [API library](https://plot.ly/python/) de Plotly. También se pueden sacar buenas ideas del [graphing news feed](https://plot.ly/) viendo lo que publican otros usuarios.

No dudeis en contactar con nosotros o el equipo de Plotly por [email](mailto:feedback@plot.ly) o [Twitter](https://twitter.com/plotlygraphs) para cualquier duda o sugerencia.