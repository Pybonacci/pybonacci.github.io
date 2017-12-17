---
title: De matplotlib a la web con plotly
date: 2014-08-05T09:07:03+00:00
author: Pablo Fernández
slug: de-matplotlib-a-la-web-con-plotly
tags: embed, matplotlib, plotly

(También podéis seguir las explicaciones de este post con <a href="http://nbviewer.ipython.org/github/Pybonacci/notebooks/blob/master/plotly/Brandshatch.ipynb" target="_blank">este Notebook</a>)

En esta entrada trataremos de dar a conocer `plotly`, un servicio web gratuito para generar gráficos interactivos y que permite la creación de proyectos colaborativos.

Los paquetes que vamos a emplear son,

  * <a href="http://pandas.pydata.org/" target="_blank"><code>pandas</code></a> 0.14.0, para importar y analizar estructuras de datos en Python.
  * <a href="http://matplotlib.org/" target="_blank"><code>matplotlib</code></a> 1.3.1, para generar diversisos tipos de gráficos con calidad de imprenta.
  * <a href="https://plot.ly/" target="_blank"><code>plotly</code></a> 1.1.2, para generar gráficos interactivos para la web.

Empezaremos por importar los datos con `pandas`. Podeis encontrar una introducción a `pandas` en <a href="http://pybonacci.org/2014/05/30/pandas-i/" target="_blank">éste</a> post de Pybonacci.

### Datos

La estructura de datos con la que vamos a trajar es un `CSV` con datos de telemetría correspondientes a un BMW Z4 GT3 compitiendo en el circuito <a href="http://www.brandshatch.co.uk/circuit-information.aspx" target="_blank">Brands Hatch Indy</a>. El paquete de datos nos lo ha proporcionado Steve Barker, un mecánico que pasa la mayor parte de su tiempo en la GP2. Pero aquí sólo vamos a trabajar con los datos de la vuelta 27 de la primera carrera.

<!--more Sigue leyendo!-->

En el siguiente vídeo podemos ver cómo sería una vuelta a dicho circuito con el mismo modelo de coche.

[youtube=http://youtu.be/puDccvGPHNU]

El propio `pandas` incluye rutinas para importar datos desde diversas fuentes, ya sea un simple `CSV` o un Excel de multiples hojas.

<pre><code class="language-python"># Importamos pandas de la manera habitual
import pandas as pd</code></pre>

Pero antes de proceder a cargar los datos debemos conocer un poco la estructura del archivo en cuestión del que he recortado una muestra.

<pre><code class="language-csv">Format;MoTeC CSV File;;;Workbook;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Venue;brandshatch indy;;;Worksheet;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Vehicle;bmwz4gt3;;;Vehicle Desc;bmwz4gt3;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Driver;Steve Barker;;;Engine ID;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Device;ADL;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Comment;;;;Session;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Log Date;02/07/2014;;;Origin Time;1196.94;s;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Log Time;23:05:43;;;Start Time;1196.95;s;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Sample Rate;60;Hz;;End Time;1240.017;s;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Duration;43.067;s;;Start Distance;49849;m;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Range;Lap 27;;;End Distance;51765;m;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Time;Distance;Gear;Engine RPM;Manifold Pres;Throttle Pos;Brake Pedal Pos;Clutch
s;m;;rpm;kpa;%;%;%;deg;N.m;;m;km/h;G;G;G;deg;deg;deg;deg/s;deg/s;deg/s;C;kPa;V;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
0;0;5;8657;0.99752352;100;0;100;-5.724613;1.5780677;26;0.6267;225.407808;-0.296
0.017;1;5;8658;0.9975208;100;0;100;-6.10625;1.7365016;26;1.66957;225.514112;-0.
0.033;2;5;8654;0.99751824;100;0;100;-6.160785;1.929843;26;2.71285;225.58688;-0.
0.05;3;5;8670;0.99751552;100;0;100;-6.160785;2.5375902;26;3.7565;225.653952;-0.</code></pre>

Como bien podemos apreciar, las primeras 11 líneas aportan información generada por MoTeC al exportar los datos. Las cabeceras de lo que realmente nos interesa son las líneas 14 y 15, siendo la primera la descripción del parámetro y la segunda las unidades de medida. Y ya en la línea 18 empiezan los datos.

Tomaremos como índice del DataFrame la variable tiempo, que sabemos que es la primera columna (aunque también podríamos haber optado por la distancia).

<pre><code class="language-python"># Cargamos el archivo. Recordemos que pandas, y Python en general, es 0-indexed.
data = pd.io.parsers.read_csv('brandshatch_lap27.csv', sep=';',
                              header=13, index_col=0, skiprows=[14,15,16])</code></pre>

Otra forma alternativa de leer los datos de un archivo CSV sería a través del propio `DataFrame` de `pandas`, pero éste no nos permite saltarnos filas de datos:

<pre><code class="language-python">data = pd.DataFrame.from_csv('brandshatch_lap27.csv', sep=';', header=13, index_col=0)</code></pre>

Si mostramos las primeras filas del archivo con `data.head(5)`, obtendremos algo como

    In [3]: data.head(5)
    Out[3]:
    Distance Gear Engine RPM Manifold Pres Throttle Pos ...
    Time
    0.000 0 5 8657 0.997524 100 ...
    0.017 1 5 8658 0.997521 100 ...
    0.033 2 5 8654 0.997518 100 ...
    0.050 3 5 8670 0.997516 100 ...
    0.067 4 5 8695 0.997512 100 ...
    [5 rows x 215 columns]

Podemos ver que el archivo es inmenso. Contiene 215 con diferentes parámetros como revoluciones del motor, posición del pedal del acelerador, velocidad, etc. Un sinfín de datos que marearían al más experto de los ingenieros de pista.

De todos modos, aquí no vamos a analizar en detalle la vuelta realizada por Steve Barker, si no que nos centraremos exclusivamente en visualizar los datos.

### Gráficas con `matplotlib`

`matplotlib` es el paquete más empleado en Python para generar diversos tipos de gráficos de alta calidad. Y es precisamente lo que utiliza `pandas` para generar sus propias gráficas como veremos a continuación.

Empezamos por importar `matplotlib` y, de paso, crear un mapa de colores personalizado más vistoso que el que viene por defecto. La idea la he tomado de <a href="http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/" target="_blank">Randal S. Olson</a>.

<pre><code class="language-python">import matplotlib.pyplot as plt
import matplotlib as mpl
# Color map
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
tableau10 = [tableau20[i*2] for i in range(10)]
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)
for i in range(len(tableau10)):
    r, g, b = tableau10[i]
    tableau10[i] = (r / 255., g / 255., b / 255.)
# Set the default color cycle
mpl.rcParams['axes.color_cycle'] = tableau10</code></pre>

#### Va de velocidad

Una de las primeras cosas que podemos visualizar son la velocidad en función del tiempo junto con otros parámetros relaciones como son la posición de los pedales y las revoluciones del motor.

Lo primero será crear un objeto **`figura`**, que necesitaremos para pasarle a `plotly`, con tres subgráficas para mostrar revoluciones del motor, velocidad del vehículo y posición de los pedales.

<pre><code class="language-python">fig, ax = plt.subplots(3, sharex=True, figsize=(15,6))
# Revoluciones del motor
data['Engine RPM'].plot(ax=ax[0], linewidth=2)
ax[0].set_xlabel('')
ax[0].set_ylabel('Engine RPM')
ax[0].legend(loc='lower right')
# Velocidad del vehículo
data['Ground Speed'].plot(ax=ax[1], linewidth=2)
ax[1].set_xlabel('')
ax[1].set_ylabel('Speed (kph)')
ax[1].legend(loc='lower right')
# Pedales
data['Throttle Pos'].plot(ax=ax[2], linewidth=2)
data['Brake Pedal Pos'].plot(ax=ax[2], linewidth=2)
ax[2].set_xlabel('Time (s)')
ax[2].set_ylabel('Position (%)')
ax[2].set_ylim(-10,105)
ax[2].legend(loc='center right')
for j in range(3):
    ax[j].set_axisbelow(True)
    # Quitamos los bordes superior y derecho
    ax[j].spines["top"].set_visible(False)
    ax[j].spines["right"].set_visible(False)
    # Dejamos sólo los ticks abajo y a la izquierda
    ax[j].get_xaxis().tick_bottom()
    ax[j].get_yaxis().tick_left()</code></pre>

[<img class="aligncenter wp-image-2383 size-full" src="http://pybonacci.files.wordpress.com/2014/07/velocidades.png" alt="velocidades" width="621" height="383" srcset="https://pybonacci.org/wp-content/uploads/2014/07/velocidades.png 621w, https://pybonacci.org/wp-content/uploads/2014/07/velocidades-300x185.png 300w" sizes="(max-width: 621px) 100vw, 621px" />](https://plot.ly/~pfsq/138)

Lo que vemos en la gráfica de arriba son tres subgráficas que comparten el mismo eje _x_. De ese modo podemos ver la relación entre los diversos parámetros.

#### Relaciones de cambio

Otro tipo de gráfico que nos puede dar mucha información es la relación entre la velocidad del vehículo y las revoluciones del motor.

Para ello podemos utilizar en `pandas` el tipo `scatter` y colorear los valores en función de la marcha engranada. Eso lo conseguimos con la herramientas `groupby` de `pandas`.

<pre><code class="language-python">fig1, ax1 = plt.subplots(figsize=(12,6))
for key, grp in data.groupby(['Gear']):
    grp.plot('Ground Speed', 'Engine RPM', kind='scatter',
             ax=ax1, label=key, color=tableau10[key])
ax1.set_xlabel('Ground Speed (kph)')
ax1.set_axisbelow(True)
ax1.legend(title='Gear', loc='upper left')
# Quitamos los márgenes derecho y superior
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
# Dejamos sólo los ticks abajo y a la izquierda
ax1.get_xaxis().tick_bottom()
ax1.get_yaxis().tick_left()</code></pre>

[<img class="aligncenter wp-image-2390 size-full" src="http://pybonacci.files.wordpress.com/2014/07/rpm.png" alt="rpm" width="624" height="383" srcset="https://pybonacci.org/wp-content/uploads/2014/07/rpm.png 624w, https://pybonacci.org/wp-content/uploads/2014/07/rpm-300x184.png 300w" sizes="(max-width: 624px) 100vw, 624px" />](https://plot.ly/~pfsq/139)

#### Histograma del acelerador

Mediante un histograma podemos analizar el uso que hace el piloto del pedal del acelerador.

<pre><code class="language-python">fig2, ax2 = plt.subplots(figsize=(10,6))
data['Throttle Pos'].hist(ax=ax2)
ax2.set_xlabel('Throttle position (%)')
ax2.set_xlim(0,100)
ax2.set_ylabel('Time spent (@ 60 Hz)')
ax2.set_axisbelow(True)
# Quitamos los márgenes derecho y superior
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
# Dejamos sólo los ticks abajo y a la izquierda
ax2.get_xaxis().tick_bottom()
ax2.get_yaxis().tick_left()</code></pre>

[<img class="aligncenter wp-image-2393 size-full" src="http://pybonacci.files.wordpress.com/2014/07/acelerador.png" alt="acelerador" width="623" height="383" srcset="https://pybonacci.org/wp-content/uploads/2014/07/acelerador.png 623w, https://pybonacci.org/wp-content/uploads/2014/07/acelerador-300x184.png 300w" sizes="(max-width: 623px) 100vw, 623px" />](https://plot.ly/~pfsq/140)

La mayor parte del tiempo, el piloto la pasa con el pedal a fondo.

### Gráficas con `plotly`

Ahora que disponemos de una buena muestra podemos publicar las gráficas en la web con `plotly`. Podéis encontrar la guía oficial <a href="http://nbviewer.ipython.org/github/plotly/python-user-guide/blob/master/s6_matplotlylib/s6_matplotlylib.ipynb" target="_blank">aquí</a>.

`plotly` ofrece un API excelente para crear gráficas interactivas que pueden ser incluidas en webs y blogs. El paquete no viene incluido en los repositorios de Continuum Analytics (conda) pero se puede instalar de manera muy sencilla con pip:

<pre><code class="language-python">pip install plotly</code></pre>

Para poder utilizar `plotly` necesitamos una credenciales. Registrarse es gratuito, y ofrecen almacenamiento ilimitado para gráficos públicos. Sin embargo, el número de archivos privados que podemos alojar es limitado en la versión gratuita.

Para mayor comodidad podemos guardar nuestras credenciales en el sistema de modo siguiente,

<pre><code class="language-python">>&gt;&gt; import plotly.tools as tls
>&gt;&gt; tls.set_credentials_file(username="your_username",
                             api_key="your_api_key")</code></pre>

que rellenaremos con nuestros datos, que encontraremos en la sección _Configuration_ de nuestra cuenta. Nuestras credenciales las podremos recuperar, a partir de entonces, de la siguiente manera.

<pre><code class="language-python">my_creds = py.get_credentials()
username = my_creds['username']
api_key = my_creds['api_key']
py.sign_in(username, api_key)</code></pre>

Podemos utilizar `plotly` de dos maneras. La primera de ellas es generar las gráficas directamente con la API. La segunda, y la que resultará más cómoda para la mayoría, es convertir directamente las figuras generadas con `matplotlib`.

Para transformar una figura de `matplotlib` emplearemos el comando `py.plot_mpl(fig, resize=True, strip_style=False, update=None, **plot_options)`. También podemos utilizar la versión `py.iplot_mpl()` para que nos presente el resultado directamente en el Notebook de IPython.

<pre><code class="language-python"># Publicar una figura de matplotlib en la web
unique_url = py.plot_mpl(fig, filename='pybonacci/velocidades', strip_style=True)</code></pre>

La URL la podemos incrustar en un blog con un <a href="https://plot.ly/python/embedding-plotly-graphs-in-HTML/" target="_blank"><code>iframe</code></a> o creando un shortcode para dicho `iframe`. Para ello, en WordPress, necesitamos crear o editar el archivo `functions.php` dentro de la carpeta de nuestro tema de WP e incluir las siguientes líneas de código

<pre><code class="language-php">function plotly_shortcode($atts, $content=null){
    extract(shortcode_atts(array(
        'id' =&gt; 'igraph',
        'height' =&gt; 400,
    ), $atts));
    return '&lt;iframe height="' . $height . '" id="' . $id . '" scrolling="no" seamless="seamless" src="' . $content . '" width="100%"&gt;&lt;/iframe&gt;';
}
add_shortcode('plotly', 'plotly_shortcode');</code></pre>

que emplearíamos de las siguientes maneras

  * `&#091;plotly&#093;https://plot.ly/~pfsq/138&#091;/plotly&#093;`

  * `&#091;plotly height=500&#093;https://plot.ly/~pfsq/139&#091;/plotly&#093;`

  * `&#091;plotly height=450 id=2&#093;https://plot.ly/~pfsq/140&#091;/plotly&#093;`

Hasta donde tengo conocimiento, un blog alojado en WordPress.com no permite incrustar `iframe`, lo cual es una verdadera pena. Sin embargo, como podéis ver en los enlaces, seguimos contando con un enlace a un gráfico interactivo al que podríamos redirigir pinchando en la imagen generada por `matplotlib` como hemos hecho con las imágenes arriba.

### Retocar `plotly`

Como podemos ver en las gráficas superiores, la conversión a `plotly` todavía no es perfecta. El conversor interpreta las leyendas de `matplotlib` como anotaciones de texto. Por suerte, eso lo podemos subsanar fácilmente.

Necesitaremos importar una serie de paquetes adicionales, disponibles en las versiones >1 de `plotly`.

<pre><code class="language-python"># Herramientas Python/Plotly
import plotly.tools as tls
# Objetos para componer Leyendas
from plotly.graph_objs import Legend</code></pre>

Convertimos la figura de `matplotlib` a una figura de `plotly`,

<pre><code class="language-python">py_fig = tls.mpl_to_plotly(fig, strip_style=True)</code></pre>

y eliminamos todas las anotaciones de texto y añadimos una leyenda en la esquina superior derecha.

<pre><code class="language-python"># Borrar anotaciones
py_fig['layout'].pop('annotations',None)
# Añadir leyenda
py_fig['layout'].update(dict(showlegend=True))</code></pre>

Ya podemos publicar la nueva gráfica, ésta vez sólo con `py.plot()` o `py.iplot()` pues ya hemos hecho la conversión a `plotly` unos pasos atrás.

<pre><code class="language-python">unique_url3 = py.iplot(py_fig, filename='pybonacci/velocidades_edit')</code></pre>

Podéis ver el resultado sin anotaciones en <a href="https://plot.ly/~pfsq/141" target="_blank">https://plot.ly/~pfsq/141</a>.
  


Repetimos el procedimiento para la segunda gráfica, pero en esta ocasión colocaremos la leyenda arriba a la izquierda y cambiamos el `hovermode` a `closest`.

Con `hovermode` controlamos cómo se comporta `plotly` al pasar el ratón por encima de la gráfica. En modo `closest` nos resaltará el valor más cercano al ratón, y en modo `compare`, para cada _x_ nos mostrará los diferentes valores que toma la variable.

<pre><code class="language-python">py_fig1 = tls.mpl_to_plotly(fig1, strip_style=True)
# Borrar anotaciones
py_fig1['layout'].pop('annotations',None)
# Añadir leyenda
py_fig1['layout'].update(dict(showlegend=True,
                              legend=Legend(x=0,y=1),
                              hovermode='closest'))</code></pre>

Pero esta vez tenemos que editar los nombres de los puntos que se muestran en la leyenda.

<pre><code class="language-python"># Editar leyenda
n=0
for key, grp in data.groupby(['Gear']):
    py_fig1['data'][n].update(dict(name='Gear {}'.format(key)))
    n += 1</code></pre>

y ya podemos crear la gráfica,

<pre><code class="language-python">unique_url4 = py.iplot(py_fig1, filename='pybonacci/rpm_edit')</code></pre>

que podéis ver en <a href="https://plot.ly/~pfsq/142" target="_blank">https://plot.ly/~pfsq/142</a>
  


Por último nos falta retocar el histograma de posiciones del pedal del acelerador. En ésta gráfica no quedan anotaciones, pero tampoco necesitamos mostrar la leyenda. Aprovechamos también para hacer las barras más anchar reduciendo el `bargap`.

<pre><code class="language-python">py_fig2 = tls.mpl_to_plotly(fig2, strip_style=True)
# Borrar leyenda
py_fig2['layout'].update(dict(showlegend=False,
                              bargap=0.01))</code></pre>

Publicamos la gráfica

<pre><code class="language-python">unique_url5 = py.iplot(py_fig2, filename='pybonacci/acelerador_edit')</code></pre>

y podemos disfrutar del resultado en <a href="https://plot.ly/~pfsq/143" target="_blank">https://plot.ly/~pfsq/143</a>
  


### Próximamente

En una próxima entrega daremos a conocer más en detalle `plotly`. Explicaremos su estructura de datos, basada en `JSON`, y enseñaremos a crear gráficas directamente con su API.