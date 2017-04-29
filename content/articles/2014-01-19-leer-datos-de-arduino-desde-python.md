---
title: Leer datos de Arduino desde Python
date: 2014-01-19T21:50:05+00:00
author: Juan Luis Cano
slug: leer-datos-de-arduino-desde-python
tags: arduino, datos, numpy, python

## Introducción

En este artículo vamos a ver **cómo leer datos procedentes de una plataforma Arduino con Python.** Para quienes no lo conozcáis, [Arduino](http://www.arduino.cc/) es una plataforma de _hardware libre_ concebida para crear prototipos de manera rápida y fácil usando componentes electrónicos. Gracias a Arduino vamos a alejarnos un poco de lo que solemos ver en este blog, que es solo software, y vamos a poder interactuar con el mundo real de una manera más directa.

<img src="http://pybonacci.org/wp-content/uploads/2014/01/arduino_uno_-_r3.jpg" alt="Arduino Uno" width="560" height="400" class="aligncenter size-full wp-image-2165" srcset="https://pybonacci.es/wp-content/uploads/2014/01/arduino_uno_-_r3.jpg 560w, https://pybonacci.es/wp-content/uploads/2014/01/arduino_uno_-_r3-300x214.jpg 300w" sizes="(max-width: 560px) 100vw, 560px" />

Este artículo nace gracias a mi reciente incorporación a [Aerobot](http://aerobot.org.es/), el club de robótica de mi escuela, donde iré explorando las posibilidades de Arduino y Python 🙂

_**En esta entrada se han usado python 3.3.3, numpy 1.8.0, pyserial 2.7 y matplotlib 1.3.1.**_

### Prefacio: ¿cómo funciona?

En este artículo no vamos a ver en detalle qué es Arduino o el lenguaje con el que se programa. Para ello os remito a gente que sabe mucho más que nosotros: al final del artículo incluyo unos enlaces que os pueden interesar si queréis profundizar en este tema. Sin embargo, sí que vamos a explicar brevemente cómo es el proceso de escribir un programa para Arduino, por razones que en seguida veremos.

Tal y como se detalla en la documentación, el [proceso de compilación en Arduino](http://arduino.cc/es/Hacking/BuildProcess) funciona a grandes rasgos de la siguiente manera:

  1. Se escribe un programa (sketch) en el IDE de Arduino en C o C++.
  2. El IDE comprueba que la sintaxis es correcta y añade `#include "Arduino.h"` y una función `main()` propia de la placa.
  3. El programa se compila con avr-gcc y se manda el binario a la placa.
  4. Una vez Arduino tiene el programa y mientras esté alimentado, el programa se ejecutará, normalmente de manera indefinida.

Esta explicación viene para aclarar que, al menos en este artículo, __**_no_ vamos a programar nuestra placa en Python**. Por el proceso que hemos visto, las únicas maneras de hacer esto serían:

  * Traducir un subconjunto de Python a C/C++, compilarlo y subirlo a la placa. Después de una búsqueda rápida en Google no tengo noticias de que nadie haya intentado esto.
  * Escribir un sketch que defina un protocolo de comunicación entre Arduino y Python. Este es el enfoque tomado por estos proyectos: 
      * https://github.com/vascop/Python-Arduino-Proto-API-v2
      * https://github.com/thearn/Python-Arduino-Command-API
      * https://github.com/lekum/pyduino

Con el segundo método no tenemos disponibles todas las funciones de Arduino, de modo que solo sirve para prototipar programas. Hoy me voy a olvidar de esto y voy a usar Arduino para programar la placa y Python para obtener los datos.

<!--more-->

_**En esta entrada se han usado python 3.3.3, pyserial 2.7.**_

## Comunicación por puerto serie con pySerial

### El código mínimo

Para comunicarnos con nuestra placa Arduino por puerto serie utilizaremos la biblioteca [pySerial](http://pyserial.sourceforge.net/), disponible también en PyPI. Una vez que tenemos nuestra placa enchufada, lo único que necesitamos para acceder a ella es esto:

<pre><code class="language-python">import serial
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)</code></pre>

La clase Serial puede recibir muchos parámetros, pero los fundamentales son estos:

  * El puerto (en nuestro caso `'/dev/ttyACM0'`) que identifica la placa. En Windows sería `'COM3'`.
  * La velocidad en baudios (en nuestro caso 9600). Algunos valores estándares son 9600, 19200, 38400...
  * El `timeout` (en nuestro caso 1 segundo) o tiempo máximo de espera para una lectura. Es importante poner un valor mayor que 0 para que en caso de error la lectura no «se cuelgue» indefinidamente.

**Nota**: La función `readline()` esperará a que se reciba una nueva línea, independientemente del timeout.

A partir de este momento podemos leer de la variable `arduino` como si fuera un fichero normal (de hecho los objetos `Serial` heredan de [`RawIOBase`](http://docs.python.org/3.3/library/io.html#io.RawIOBase)). Supongamos que en nuestra placa Arduino hemos cargado el [ejemplo AnalogInOutSerial](http://arduino.cc/en/Tutorial/AnalogInOutSerial), y que por tanto nuestra placa está escribiendo datos al puerto serie:

<pre><code class="language-python">while True:
    line = arduino.readline()
    print(line)</code></pre>

Y la salida será algo así:

<pre>$ python arduino_python.py 
b'sensor = 0toutput = 0rn'
b'sensor = 0toutput = 0rn'
b'sensor = 0toutput = 0rn'
b'sensor = 0toutput = 0rn'
b'sensor = 0toutput = 0rn'
^CTraceback (most recent call last):
  File "arduino_python.py", line 34, in 
    line = arduino.readline()
  File "arduino_python.py", line 22, in readline
    time.sleep(0.1)
KeyboardInterrupt

</pre>

Y podríamos dejarlo aquí, pero podemos hacer el código un poco más robusto.

### Algunas mejoras

Con esto ya estamos leyendo los datos, pero podemos mejorar algunas cosas:

  * La función `readline` devuelve un objeto `bytes`: por eso vemos "rn" al final, los caracteres especiales de terminación de línea. Desde Arduino [solo podemos mandar caracteres ASCII](http://arduino.cc/es/Serial/Print), así que podemos decodificar los bytes a una cadena. No obstante, habrá que indicar que en caso de recibir un byte erróneo no queremos que la función falle, sino que escriba algo como �.
  * Al detener el programa (Ctrl+C en la consola) no queremos ver una traza de error. Podemos capturar la excepción KeyboardInterrupt con un bloque try-except.
  * Faltaría incluir una llamada a arduino.close() al final del programa por seguridad, pero en vez de eso podemos utilizar la sentencia with y Python se encarga de cerrar la comunicación por nosotros.

El código final sería este:

https://gist.github.com/Juanlu001/8256958

¡Y ya lo tenemos! Esto es todo lo que necesitamos para leer datos desde una placa Arduino 🙂

### Precauciones en el MundoReal™

La conexión a Arduino no siempre funcionará de manera ideal, y puede haber momentos en los que recibamos bytes erróneos. Hay un par de comentarios importantes que hacer al código anterior:

  * No se puede leer la placa desde dos fuentes a la vez. Si mientras corre este programa abres el monitor Serial del IDE de Arduino uno de los dos acabará fallando.
  * Podríamos iterar sobre el flujo de datos con un bucle `for line in arduino`, y Python se encargaría de ir invocando sucesivamente la función `readline`, pero este método puede fallar si se recibe algún byte corrupto. He comprobado que es más seguro hacerlo manualmente.

Esto afecta también a la hora de almacenar los datos recibidos, como veremos en la sección siguiente.

Por otro lado, hay otro asunto que hay que tener en cuenta: [la placa Arduino se reinicia automáticamente al abrir una conexión por puerto serie](http://arduino.cc/en/Guide/Environment#uploading), y al probar este código en Linux estaba dándome problemas. En los primeros segundos, entre el inicio de la conexión y el reinicio de la placa recibía datos erróneos. Por eso pregunté en Stack Overflow [cómo reiniciar manualmente la placa usando pySerial](http://stackoverflow.com/questions/21073086/wait-on-arduino-auto-reset-using-pyserial) y me dieron la solución:

<pre><code class="language-python">import serial
import time
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)
# Provocamos un reseteo manual de la placa para leer desde
# el principio, ver http://stackoverflow.com/a/21082531/554319
arduino.setDTR(False)
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)</code></pre>

De este modo, si empezamos a leer justo después deja de haber problemas. Dejo esta solución aquí en caso de que otros hayan experimentado este problema; en Windows, por ejemplo, no es necesario.

## Almacenando los datos

Una vez que ya podemos leer los datos desde Arduino, vamos a dar algunas ideas sobre cómo almacenarlos y cómo procesarlos.

### Leer un bloque de datos y cerrar

El caso más sencillo es leer un número predeterminado de líneas desde la placa y cerrar la conexión, para después procesar esos datos de la manera que queramos. Para ello, lo mejor es que empleemos un array de NumPy y que incorporemos los datos utilizando la función [np.fromstring](http://docs.scipy.org/doc/numpy/reference/generated/numpy.fromstring.html). Esta función acepta como argumentos la cadena que se va a leer y un argumento que indica cuál es el separador entre datos. Para cadenas ASCII como los que manejamos ahora, debemos especificar que los datos están separados por espacios. Utilizando de nuevo el sketch AnalogInOutSerial pero con las líneas de escritura de esta forma:

    // print the results to the serial monitor:
    //Serial.print("sensor = " );
    Serial.print(sensorValue);
    Serial.print("t");
    Serial.println(outputValue);

Este sería el código Python:

<pre><code class="language-python">import time
import serial
import numpy as np
N = 10
data = np.zeros((N, 2))
# Abrimos la conexión con Arduino
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)
with arduino:
    ii = 0
    while ii &lt; N:
        try:
            line = arduino.readline()
            if not line:
                # HACK: Descartamos líneas vacías porque fromstring produce
                # resultados erróneos, ver
                # https://github.com/numpy/numpy/issues/1714
                continue
            data[ii] = np.fromstring(line.decode('ascii', errors='replace'),
                                     sep=' ')
            ii += 1
        except KeyboardInterrupt:
            print("Exiting")
            break
print(data)</code></pre>

¿Por qué usamos un contador con un bucle while en este caso, que parece que no queda muy pythonico? El motivo es que en algunos casos tendremos que descartar líneas (como se ha visto en el código por culpa de un fallo de NumPy) y esta estructura es más adecuada.

### Procesar una cola de datos

Otra cosa que podemos necesitar es almacenar los datos en una cola e ir procesándolos sobre la marcha. Esto puede ser interesante si, por ejemplo, queremos **representar gráficamente en tiempo real la evolución de una variable**, pero solo nos interesan los últimos segundos. En este caso el módulo collections de la biblioteca estándar de Python nos proporciona la estructura [deque](http://docs.python.org/3.3/library/collections.html#collections.deque) (_double-ended queue_, que podríamos traducir por cola doblemente terminada), que funciona de manera que si añadimos elementos al final, a partir de una cierta longitud máxima se descartan elementos del principio.

Si quisiéramos usar una deque, el código sería este:

<pre><code class="language-python">N = 10
data = deque(maxlen=N)  # deque con longitud máxima N
while True:
    # ...
    data.append(dd)  # Añadimos elementos al final de la cola</code></pre>

Y para usar arrays de NumPy, podemos usar un truco para ir recorriendo cíclicamente sus elementos:

<pre><code class="language-python">N = 10
data = np.zeros(N)  # deque con longitud máxima N
ii = 0
while True:
    data[ii % N] = dd  # Recorremos cíclicamente el array
    ii += 1</code></pre>

Puedo tener dos efectos diferentes: con buff[i % N] tengo «efecto barrido», que sería similar a como representa los datos un osciloscopio, y con deque tengo «efecto pasada», que podríamos comparar con una ventana que se va desplazando.

## _Finale_: Representación en tiempo real

Ahora no tenemos más que integrar todo lo que hemos visto arriba, y ya podremos **representar en tiempo real datos procedentes de una placa Arduino con Python**.

<pre><code class="language-python">import time
import warnings
from collections import deque
import serial
import numpy as np
import matplotlib.pyplot as plt
N = 200
data = deque([0] * N, maxlen=N)  # deque con longitud máxima N
#Creamos la figura
plt.ion()
fig, ax = plt.subplots()
ll, = ax.plot(data)
# Abrimos la conexión con Arduino
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)
arduino.setDTR(False)
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)
with arduino:
    while True:
        try:
            line = arduino.readline()
            if not line:
                # HACK: Descartamos líneas vacías porque fromstring produce
                # resultados erróneos, ver
                # https://github.com/numpy/numpy/issues/1714
                continue
            xx, yy = np.fromstring(line.decode('ascii', errors='replace'),
                                   sep=' ')
            data.append(yy)
            ll.set_ydata(data)
            ax.set_ylim(min(data) - 10, max(data) + 10)
            plt.pause(0.001)
        except ValueError:
            warnings.warn("Line {} didn't parse, skipping".format(line))
        except KeyboardInterrupt:
            print("Exiting")
            break</code></pre>

Y este es el resultado:<figure id="attachment_2157" style="width: 560px" class="wp-caption aligncenter">

[<img class=" wp-image-2157 " alt="Datos Arduino en tiempo real" src="http://pybonacci.org/wp-content/uploads/2014/01/2014-01-19-200435_1366x768_scrot.png" width="560" height="408" srcset="https://pybonacci.es/wp-content/uploads/2014/01/2014-01-19-200435_1366x768_scrot.png 894w, https://pybonacci.es/wp-content/uploads/2014/01/2014-01-19-200435_1366x768_scrot-300x218.png 300w" sizes="(max-width: 560px) 100vw, 560px" />](http://pybonacci.org/wp-content/uploads/2014/01/2014-01-19-200435_1366x768_scrot.png)<figcaption class="wp-caption-text">Datos Arduino en tiempo real</figcaption></figure> 

Aunque mejor que lo ejecutes en tu ordenador 😉

## Para saber más

No soy ni mucho menos un experto en Arduino. Si estáis buscando un blog especializado os recomiendo [GeekyTheory](http://geekytheory.com/), y si queréis saber más acerca de Python + Arduino os interesará la charla de Núria Pujol sobre [tracking GPS con Python y Arduino](http://www.slideshare.net/llevaNEUS/easy-gps-tracker-using-arduino-and-python) que dio recientemente en el grupo Python Barcelona. Además Núria accedió amablemente a revisar el borrador de esta entrada, ¡mil gracias! 🙂

Y tú, **¿tienes ya pensado cómo vas a combinar Python y Arduino? ¿Alguna idea o proyecto interesante que nos quieras contar? ¡Escríbenos en los comentarios!**