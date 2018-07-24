---
title: Gráficas de tiempo real con Plotly
date: 2014-08-30T13:15:15+00:00
author: Pablo Fernández
slug: graficas-de-tiempo-real-con-plotly
tags: geforce, gpu, monitor, nvidia, plotly, streaming api

Y aquí llega otra nueva entrada dedicada a Plotly, ésta vez sin notebook, para hacer una aplicación de «tiempo-real» que monitorice nuestra tarjeta gráfica. Por ahora, el código, que tenéis <a href="https://github.com/pfsq/gpu-monitor" title="gpu-monitor" target="_blank">disponible en GitHub</a>, hace uso de los datos que proporciona la <a href="https://developer.nvidia.com/nvidia-system-management-interface" title="NVIDIA System Management Interface" target="_blank">NVIDIA System Management Interface</a>. Pero éste método tiene un pega, y es que el SMI está pensado para la familia de gráficas Tesla&#153; y Quadro&#153;, con el soporte a la gama GeForce&#153; está limitado a un par de parámetros. En éste caso aprovecharemos sólo temperatura y velocidad del ventilador.

Si abrimos una ventana de comandos y ejecutamos `nvidia-smi` nos debería aparecer una tabla como ésta \---es posible que tengamos que <a href="http://furniman.blogspot.com.es/2012/02/anadir-un-directorio-al-path-del.html" title="Añadir un directorio al PATH del sistema" target="_blank">añadir la ruta al ejecutable a nuestro PATH</a>, en mi caso 'C:\Program Files\NVIDIA Corporation\NVSMI'.

    +------------------------------------------------------+
    | NVIDIA-SMI 340.62     Driver Version: 340.62         |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name            TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  GeForce GTX 460    WDDM  | 0000:01:00.0     N/A |                  N/A |
    | 40%   45C   P12    N/A /  N/A |    986MiB /  1023MiB |     N/A      Default |
    +-------------------------------+----------------------+----------------------+
    +-----------------------------------------------------------------------------+
    | Compute processes:                                               GPU Memory |
    |  GPU       PID  Process name                                     Usage      |
    |=============================================================================|
    |    0            Not Supported                                               |
    +-----------------------------------------------------------------------------+

<!--more ¡No te quedes sin ver el resto de la entrada!-->

## Monitor

Para monitorizar la tarjeta gráfica he tomado el módulo `gpuwatch.py`, de <a href="http://blog.erdemagaoglu.com/post/3074180322/monitoring-nvidia-gpu-metrics-with-ganglia" title="Monitoring nVidia GPU metrics with Ganglia" target="_blank">H. Çağlar Bilir</a>, modificando algunas partes para que casasen con la salida de mi _query_ a `nvidia-smi`. Si revisamos el código encontraremos, entre otras, estas tres funciones:

  * `getString`
  
        :::python
    import subprocess as sub
    def getString():
        test_file = "nvidia-smi -q --gpu=0"
        try:
            p = sub.Popen(test_file, stdout=sub.PIPE, stderr=sub.PIPE)
            out, err = p.communicate()
            return out
        except IOError:
            return "Error" que nos devuelve la salida del 
    
    _query_ a `nvidia-smi`;
  * `readl`
  
        :::python
    def readl(key):
        output=str(getString(), encoding='utf8')
        splittedoutput=output.split('\n')
        for line in splittedoutput:
            line=line.strip()
            if line.startswith(key):
                line=line.split(':')[1].strip()
                if key=='GPU Current Temp':
                    return line.split('C')[0].strip()
                elif key=='Fan Speed':
                    return line.split('%')[0].strip()
                else:
                    return line[:-1] que leerá cada línea de texto hasta encontrar lo que buscamos; y

  * `Gpu_Temp`
  
        :::python
    def Gpu_Temp():
        return int(readl('GPU Current Temp')) que nos devuelve el valor de la temperatura actual de la tarjeta gráfica.

## Streaming API de Plotly

La Streaming API de Plotly nos permite actualizar nuestras gráficas en tiempo real, sin necesidad de refrescar nuestro navegador. En otras palabras, los usuarios envían datos continuamente a los servidores de Plotly para visualizarlos en _tiempo real_. Y muy rápido. Las gráficas se pueden actualizar hasta 20 veces por segundo.

Esto nos permitiría, entre otras muchas cosas, monitorizar las lecturas de un termómetro conectado a un Arduino en nuestro ático desde nuestro portátil en cualquier otro lugar.

En palabras de Plotly:

> Everyone looking at a Plotly streaming plot sees the same data, updating at the same time. Like all Plotly plots, Plotly streaming plots are immediately shareable, by shortlink or as embedded in website or an IPython notebook. Owners of Plotly plot can edit their with the Plotly web GUI while all of the viewers of the plot will see the changes update live.

### Dependencias

Todo lo que tratemos a partir de este punto estará relacionado con el fichero `gpu-monitor.pyw`. La extensión PYW permite ejecutar scripts de Python en segundo plano sin que se abra el terminal \---al tratarse de un bucle infinito necesitaremos matar el proceso desde el Administrador de tareas.

El primer paso, como es costumbre, es importar los paquetes:

  * `gpuwatch`, para las funciones que leen los valores de la gráfica.
  * Plotly, para generar las gráficas
  
        :::python
    # (*) Para comunicarse con los servidores y loguearse
    import plotly.plotly as py  
    # (*) Herramientas útiles
    import plotly.tools as tls   
    # (*) Objetos para componer gráficas
    from plotly.graph_objs import *

  * `datetime`, para crear las marcas temporales.
  * `time.sleep`, para pausar la ejecución un intervalo de tiempo.

Aquellos que no estén familiarizados con las credenciales pueden dirigirse a la <a href="https://plot.ly/python/user-guide/#Step-6" title="User Guide, step 6" target="_blank">Guía de Usuario</a>.

### Stream tokens

Crear gráficas en tiempo real con Plotly no cambia en lo esencial con respecto al modo tradicional; sin embargo, será necesario <a href="https://plot.ly/python/streaming-tutorial/#Get-your-stream-tokens" target="_blank">generar un <em>token</em></a> o _id_ por cada trazo.

Para ello, una vez nos hemos logueado en plot.ly, nos dirigimos a _Settings_, en la esquina superior derecha de la ventana. Bajo la pestaña _Stream Tokens_ encontraremos el botón _Generate Token_. Recordad que debemos generar **un _stream token_ por trazo** por cada gráfica. Aunque podemos reutilizar los _tokens_ en diferentes gráficas siempre que no vayamos a actualizarlas a la vez.

En nuestro caso vamos a necesitar dos _stream tokens_, uno para la temperatura y otro para la velocidad del ventilador.

    :::python
    stream_ids = ["lj8k5sz7sx", "upxpfny8c1"]

¡Ya podemos empezar!

### Data

La metodología a seguir es la misma que hemos empleado en tutorial <a href="http://pybonacci.org/2014/08/22/graficas-interactivas-con-plotly/" title="Gráficas interactivas con Plotly" target="_blank">Gráficas interactivas con Plotly</a>.

Inicializamos las líneas a representar. Para ello, el objeto `Scatter` tomará arrays vacíos para las variables `x` e `y`. La temperatura la representaremos como líneas y puntos (`'lines+markers'`) de color verde lima y con un ajuste de tipo spline. Por su parte, la velocidad del ventilador, de color cyan y líneas verticales y horizontales (`'vh'`) utilizará el segundo eje _y_ `'y2'`.

    :::python
    trace1 = Scatter(x=[],
                     y=[],
                     mode='lines+markers',
                     line=Line(shape='spline', color='lime'),
                     marker=Marker(color='black', line=Line(color='lime', width=2)),
                     stream=Stream(token=stream_ids[0], maxpoints=60))
    trace2 = Scatter(x=[],
                     y=[],
                     yaxis='y2',
                     mode='lines',
                     line=Line(shape='vh', color='cyan'),
                     stream=Stream(token=stream_ids[1], maxpoints=60))
    data = Data([trace1, trace2])

La única novedad que introducimos en éste punto es el objeto `Stream` con el que identificamos cada trazo con su _token_. Éste objeto también nos permite limitar el número de punto a representar en la gráfica definiendo `maxpoints`.

Por ahora no hemos introducido ningún valor; ni temperatura ni velocidad del ventilador.

### Layout

Con `Layout` vamos a configurar la estética de la gráfica. Ponemos un título a la gráfica `'GeForce GTX460 GPU real-time monitor'` y definimos el color del texto como blanco con el objeto `Font`. En este punto también podríamos definir el tipo de letra con `family` y el tamaño con `size`.

Le damos un color verde oscuro a la rejilla con `gridcolor` y ajustamos nuestros dos ejes _y_. Puesto que hemos deshabilitado la leyenda (`showlegend=False`) damos a cada eje _y_ el color de la línea asociada. Cambiamos el color del nombre del eje con `titlefont` y el color de los números con `tickfont`. Para equilibrar el gráfico colocamos el segundo eje _y_ a la derecha, `side='right'`.

El color de fondo de la gráfica y el margen serán negros. Ello lo logramos con `plot_bgcolor` y `paper_bgcolor` respectivamente.

    :::python
    layout = Layout(title='GeForce GTX460 GPU real-time monitor',
                    font=Font(color='white'),
                    showlegend=False,
                    xaxis=XAxis(gridcolor='darkgreen'),
                    yaxis=YAxis(title='Temperature (C)',
                                titlefont=Font(color='lime'),
                                tickfont=Font(color='lime'),
                                gridcolor='darkgreen'),
                    yaxis2=YAxis(title='Fan speed (%)',
                                 overlaying='y',
                                 side='right',
                                 titlefont=Font(color='cyan'),
                                 tickfont=Font(color='cyan'),
                                 gridcolor='darkgreen'),
                    paper_bgcolor='black',
                    plot_bgcolor='black')

### Plot

Ya tenemos listos los datos y el layout para crear nuestra figura.

    :::python
    fig = Figure(data=data, layout=layout)

y enviarla a Plotly:

    :::python
    unique_url = py.plot(fig, filename='streaming/gpu-monitor')

### Stream

Para actualizar la gráfica creamos un objeto Stream por cada trazo a representar. Identificamos cada stream con el _stream token_ correspondiente,

    :::python
    # Make 1st instance of the stream link object
    s1 = py.Stream(stream_ids[0])
    # Make 2nd instance of the stream link object
    s2 = py.Stream(stream_ids[1])

y los abrimos,

    :::python
    # Open both streams
    s1.open()
    s2.open()

Ya podemos entrar al <a href="http://es.wikipedia.org/wiki/Bucle_infinito" target="_blank">bucle infinito</a>. Claro que en este caso es intencionado, y no un error de programación.

Asignamos al eje _x_ la hora actual y para los ejes _y_ empleamos dos funciones de las funciones que tenemos en `gpuwatch.py` que toman los valores proporcionados por el System Management Interface de NVIDIA. Por último escribimos cada uno de estos valores en el Stream de Plotly.

    :::python
    while True:
        # Hora actual en eje x, temperatura GPU en eje y, velocidad ventilador en eje y2
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y1 = gpuwatch.Gpu_Temp()
        y2 = gpuwatch.Fan_Speed()
        # Escribe al stream de Plotly
        s1.write(dict(x=x, y=y1))
        s2.write(dict(x=x, y=y2))
        # Esperar intervalo en segundos
        sleep(10)

**Muy importante**: hay que esperar un intervalo entre bucle y bucle. En éste caso he optado por 10 segundos. Por varios motivos: Plotly trabaja como mucho a 20 actualizaciones por segundo, pero si no esperamos un intervalo razonable, el gasto de CPU se nos irá al 100 % y nos petará la máquina. Y eso, con el agravante de utilizar un bucle infinito, sería una catástrofe. Pero nada que no se solucione matando el proceso.

## Resultado

Una de las ventajas de la Streaming API de Plotly es que permite ver la gráfica en tiempo real desde cualquier navegador, además de permitir compartirla con cualquier usuario de la red.

Junto con un smartphone o table se convierte en el compañero perfecto para las tardes/noches de juego. Como se puede ver en el video a continuación, utilizo mi iPad para visualizar la gráfica en tiempo real. Lo que se ve en pantalla es una prueba inicial; y al volver a ejecutar el script desde la línea de comandos se aprecia como se reinicia automáticamente. Para probarlo en funcionamiento inicio un juego para apreciar cómo, conforme avanza, la temperatura y la velocidad del ventilador van ascendiendo. Aunque en un momento de despiste se bloquea el iPad y hasta que no vuelvo a actualizar la ventana no sigue con el _stream_.


  
&nbsp;
  


La gráfica guarda únicamente los últimos 10 minutos de streaming: `maxpoints=60` a una actualización cada 10 segundos. Y cada vez que ejecutamos el script se resetea la gráfica. Si no queremos que se borren los últimos puntos, podríamos incluir un `fileopt="extend"` cuando llamamos a la función `py.plot()`.

Esperamos que haya sido instructivo y nos sorprendáis con vuestras propias gráficas. Cualquier sugerencia o aporte al código en <a href="https://github.com/pfsq/gpu-monitor" target="_blank">GitHub</a> será bien recibida.