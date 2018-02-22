---
title: Teoría de control en Python con SciPy (II): Control PID
date: 2013-11-06T20:37:07+00:00
author: Juan Luis Cano
slug: teoria-de-control-en-python-con-scipy-ii-control-pid
tags: control, python, python 3, scipy, scipy.signal

## Introducción

En esta serie de artículos vamos a estudiar **cómo podemos aplicar Python al estudio de la teoría de control**, en este caso utilizando SciPy. La teoría de control se centra en los **sistemas dinámicos** con entradas: sistemas físicos cuyo estado evoluciona con el tiempo en función de la información que reciben del exterior. Como puedes ver, esta definición es enormemente amplia: el control toca aspectos de la ingeniería y de las matemáticas, y tiene aplicaciones también en las ciencias sociales: psicología, sociología, finanzas...

  1. [Conceptos básicos](http://pybonacci.org/2013/10/10/teoria-de-control-en-python-con-scipy-i/ "Teoría de control en Python con SciPy (I): Conceptos básicos")
  2. **Control PID**

En esta segunda parte, una vez vistos algunos conceptos básicos en la primera, vamos a retomar el problema del control de crucero del coche exactamente donde lo dejamos:

> La conclusión que podemos extraer de este gráfico es que **para pasar de 0 a 100 km/h, nuestro coche necesita casi un minuto**. ¡Fatal! ¿Cómo arreglamos esto? Aquí entra la belleza de la teoría de control, pero lo vamos a dejar para la segunda parte 😉

A las referencias que ya recomendé en la primera parte voy a añadir [Ogata, 2010], un excelente libro sobre ingeniería de control traducido al español por profesores de España y Argentina. De ahí he estudiado la parte matemática del control PID y me he inspirado para las figuras. Cualquier aspecto teórico se puede consultar en este libro.

_**En esta entrada se han usado python 3.3.2, numpy 1.8.0, scipy 0.13.0 y matplotlib 1.3.0.**_

## Concepto de realimentación

Si recordamos el modelo de nuestro coche, teníamos un sistema con una entrada (la fuerza de tracción que genera el motor) y una salida o variable a controlar (la velocidad del coche). Este tipo de sistemas se denominan **en lazo abierto** y se pueden esquematizar con un diagrama de bloques de este estilo:

<p style="text-align:center">
  <img class="aligncenter  wp-image-1943" alt="Lazo abierto" src="http://new.pybonacci.org/images/2013/11/open_loop.png" width="341" height="127" srcset="https://pybonacci.org/wp-content/uploads/2013/11/open_loop.png 568w, https://pybonacci.org/wp-content/uploads/2013/11/open_loop-300x111.png 300w" sizes="(max-width: 341px) 100vw, 341px" />
</p>

En este caso la **planta** sería el motor y el **controlador** un sistema que consiguiese esa tracción constante que consideramos en la primera parte. Este tipo de sistemas son poco útiles porque no podemos disponer de la información de la salida para controlar la entrada. No les prestaremos más atención.

Si queremos tener en cuenta las posibles perturbaciones de la salida deberíamos medirla continuamente para comprobar que cumple con nuestros requisitos. A esto se le denomina **control en lazo cerrado** y se puede esquematizar de la siguiente manera:

<p style="text-align:center">
  <img class="aligncenter  wp-image-1947" alt="Lazo cerrado" src="http://new.pybonacci.org/images/2013/11/closed_loop1.png" width="420" height="187" srcset="https://pybonacci.org/wp-content/uploads/2013/11/closed_loop1.png 720w, https://pybonacci.org/wp-content/uploads/2013/11/closed_loop1-300x133.png 300w" sizes="(max-width: 420px) 100vw, 420px" />
</p>

Ya vemos que se van complicando un poco las cosas. En este caso, la entrada de la planta la proporciona el **actuador**, y la entrada del actuador es **la diferencia entre la señal de referencia y la salida**. Esta diferencia se denomina señal **error** por razones obvias. Con este cambio de esquema y de filosofía tenemos en cada instante información sobre la salida del sistema y podemos por tanto ajustar el control del mismo. Veamos un método para llevar a cabo este control.

<!--more-->

Comprobábamos con nuestro ejemplo del coche que el tiempo que necesitaba para pasar de 0 a 100 km/h era muy grande. Este tiempo se define como **tiempo de subida**, $t_r$ (_rising time_ en inglés): el tiempo requerido para que la respuesta pase del 0 % al 100 % de su valor final. Otros márgenes utilizados son 5-95 % y 10-90 %. Más adelante, cuando empecemos a introducir oscilaciones, veremos otras definiciones similares.

## Control PID

El control PID combina una acción **proporcional**, una **integral** y otra **derivativa** sobre la señal de error para dar la entrada de la planta. La ecuación de un controlador de este tipo es:

$\displaystyle u(t) = K\_p e(t) + K\_i \int\_0^t e(t) dt + K\_d \frac{de(t)}{dt}$

y su función de transferencia, por tanto:

$\displaystyle H(s) = \frac{U(s)}{E(s)} = K\_p + \frac{K\_i}{s} + K_d s$

Podemos escribir también

$\displaystyle K\_p + \frac{K\_i}{s} + K\_d s = K\_p (1 + \frac{1}{T\_i s} + T\_d s)$

donde $T_i$ se denomina _tiempo integral_ y $T_d$ es el _tiempo derivativo_.

Cada uno de estos términos contribuye de una forma distinta al sistema de control, y la correcta ponderación de cada una de estas contribuciones es lo que tendremos que buscar para conseguir una solución satisfactoria. Este proceso se llama **sintonía de controladores PID** (_PID tuning_). Vamos a estudiarlos uno por uno.

### Proporcional

Lo primero que se nos puede ocurrir es hacer que la señal de control $u(t)$ (la salida del actuador y la entrada de la planta) sea **proporcional** al error entre la salida y el valor de referencia. Recuperando la función de transferencia de nuestro control de crucero, tendríamos un esquema como el siguiente:<figure id="attachment_1951" style="width: 372px" class="wp-caption aligncenter">

[<img class=" wp-image-1951 " alt="Sistema de control proporcional" src="http://new.pybonacci.org/images/2013/11/proportional.png" width="372" height="120" srcset="https://pybonacci.org/wp-content/uploads/2013/11/proportional.png 620w, https://pybonacci.org/wp-content/uploads/2013/11/proportional-300x96.png 300w" sizes="(max-width: 372px) 100vw, 372px" />](http://new.pybonacci.org/images/2013/11/proportional.png)<figcaption class="wp-caption-text">Sistema de control proporcional</figcaption></figure> 

Nótese que la naturaleza de nuestro sistema ha cambiado completamente: antes controlábamos directamente la fuerza del motor, ahora indicamos una velocidad de referencia y el sistema ajusta dicha fuerza. La nueva función de transferencia será:

$\displaystyle \frac{Y(s)}{R(s)} = \frac{Y(s)}{Y(s) + E(s)} = \dots = \frac{K}{ms + b + K}$

SciPy no proporciona un modo directo de operar con bloques, de modo que vamos a escribir nuestras propias funciones a tal efecto. Para ello, operaremos las funciones de transferencia de los sistemas como fracciones, extrayendo por separado el numerador y el denominador y utilizando las funciones de NumPy [`np.polymul`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.polymul.html) y [`np.polyadd`](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.polyadd.html). Este será el código:

<pre><code class="language-python">def series(sys1, sys2):
    """Series connection of two systems.
    """
    if not isinstance(sys1, signal.lti):
        sys1 = signal.lti(*sys1)
    if not isinstance(sys2, signal.lti):
        sys2 = signal.lti(*sys2)
    num = np.polymul(sys1.num, sys2.num)
    den = np.polymul(sys1.den, sys2.den)
    sys = signal.lti(num, den)
    return sys
def feedback(plant, sensor=None):
    """Negative feedback connection of plant and sensor.
    If sensor is None, then it is assumed to be 1.
    """
    if not isinstance(plant, signal.lti):
        plant = signal.lti(*plant)
    if sensor is None:
        sensor = signal.lti([1], [1])
    elif not isinstance(sensor, signal.lti):
        sensor = signal.lti(*sensor)
    num = np.polymul(plant.num, sensor.den)
    den = np.polyadd(np.polymul(plant.den, sensor.den),
                     np.polymul(plant.num, sensor.num))
    sys = signal.lti(num, den)
    return sys</code></pre>

Echemos ahora un vistazo a la respuesta unitaria del sistema, seleccionando por ejemplo un valor de 200 para la ganancia, y veremos que tenemos ciertos problemas:

<pre><code class="language-python">K = 200
# Sistema controlador-planta
sys_pc = series(([K], [1]), sys_car)
# Sistema realimentado
sys_prop = feedback(sys_pc)
# Respuesta a entrada escalón
t = np.linspace(0, 60, num=200)
t, y = signal.step2(sys_prop, T=t)
plt.plot(t, y)
plt.plot([0, t[-1]], [1] * 2, 'k--')</code></pre>

<p style="text-align:center">
  <img class="aligncenter  wp-image-1953" alt="k200" src="http://new.pybonacci.org/images/2013/11/k200.png" width="315" height="226" srcset="https://pybonacci.org/wp-content/uploads/2013/11/k200.png 394w, https://pybonacci.org/wp-content/uploads/2013/11/k200-300x215.png 300w" sizes="(max-width: 315px) 100vw, 315px" />
</p>

De acuerdo, ahora el tiempo de subida es de unos 20 segundos (en vez del minuto de antes) pero ¡la salida **no llega al nivel que queremos**! Esto es así porque los controladores proporcionales introducen un cierto **error en estado estacionario** $e_{ss}$. Para nuestro sistema, el valor de este error será:

$\displaystyle e\_{ss} = \lim\_{t \rightarrow \infty} e(t) = \frac{1}{1 + K / b}$

Parece lógico pensar que entonces debemos aumentar la $K$ para reducir el error. Si hacemos esto, tendríamos la siguiente respuesta:

<p style="text-align:center">
  <img class="aligncenter  wp-image-1954" alt="k2000" src="http://new.pybonacci.org/images/2013/11/k2000.png" width="315" height="226" srcset="https://pybonacci.org/wp-content/uploads/2013/11/k2000.png 394w, https://pybonacci.org/wp-content/uploads/2013/11/k2000-300x215.png 300w" sizes="(max-width: 315px) 100vw, 315px" />
</p>

Ahora el tiempo de subida es de menos de 5 segundos y el error de estado estacionario es $e_{ss} \simeq 3.6 %$. ¿Hemos conseguido ya lo que queríamos? Sobre el papel sí, pero ¿te has fijado en la pendiente de la curva en el punto inicial? **No podemos** aumentar indefinidamente la ganancia proporcional porque eso implica **aumentar indefinidamente la fuerza** del motor. Tenemos que buscar otros métodos.

### Integral

La desventaja del control proporcional es que, si la señal de error tiende a cero, la señal de control también. Con el término integral podemos añadir una contribución que depende del área encerrada bajo la curva de la señal error, y por tanto **eliminamos el error en estado estacionario**. Ahora nuestro esquema quedaría de la siguiente forma:<figure id="attachment_1957" style="width: 372px" class="wp-caption aligncenter">

[<img class=" wp-image-1957" title="Control PI" alt="" src="http://new.pybonacci.org/images/2013/11/pi.png" width="372" height="120" srcset="https://pybonacci.org/wp-content/uploads/2013/11/pi.png 620w, https://pybonacci.org/wp-content/uploads/2013/11/pi-300x96.png 300w" sizes="(max-width: 372px) 100vw, 372px" />](http://new.pybonacci.org/images/2013/11/pi.png)<figcaption class="wp-caption-text">Sistema de control proporcional-integral (PI)</figcaption></figure> 

Y la función de transferencia será:

$\displaystyle \frac{Y(s)}{R(s)} = \frac{K\_p s + K\_i}{m s^2 + (b + K\_p) s + K\_i}$

Exacto: hemos convertido el sistema **en uno de segundo orden**. Esto tendrá algunos efectos nuevos, como se puede ver en la gráfica de la respuesta a escalón unitario del sistema para $K\_p = 200$ y $K\_i = 50$:

<pre><code class="language-python">K_p = 200.0
K_i = 50.0
# Sistema controlador-planta
sys_pc = series(([K_p, K_i], [1, 0]), sys_car)
# Sistema realimentado
sys_prop = feedback(sys_pc)
# Respuesta a entrada escalón
t = np.linspace(0, 60, num=200)
t, y = signal.step2(sys_prop, T=t)
plt.plot(t, y)
plt.plot([0, t[-1]], [1] * 2, 'k--')</code></pre>

<p style="text-align:center">
  <img class="aligncenter  wp-image-1958" alt="Control PI" src="http://new.pybonacci.org/images/2013/11/kp200ki50.png" width="315" height="226" srcset="https://pybonacci.org/wp-content/uploads/2013/11/kp200ki50.png 394w, https://pybonacci.org/wp-content/uploads/2013/11/kp200ki50-300x215.png 300w" sizes="(max-width: 315px) 100vw, 315px" />
</p>

Tenemos un tiempo de subida menor a 10 segundos, pero por contra **hemos introducido una oscilación en el sistema**. En algunos problemas puede ser inadmisible, pero en este caso nos lo podemos permitir. Lo único que tenemos que hacer es controlar la oscilación; para ello tenemos otras dos magnitudes interesantes:

  * El **tiempo de pico** $t_p$ (_peak time_) definido como el tiempo requerido para que la respuesta llegue al primer máximo.
  * La **sobreelongación máxima** $M_p$ (_overshoot_) definida como el valor máximo de la respuesta, por encima del resultado estacionario.

En general, querremos ajustar nuestro sistema de control para que tenga:

  * Tiempo de subida pequeño,
  * sobreelongación pequeña, y
  * ausencia de error en estado estacionario.

Una cuestión que hay que tener muy en cuenta es que **no podemos optimizar estos tres requisitos a la vez**. Si reducimos el tiempo de subida, la sobreelongación máxima aumentará, y viceversa [Ogata, pp. 171].

Podemos marcar unos requisitos para nuestro caso concreto:

  * Tiempo de subida < 5 s
  * Máxima sobreelongación < 10 %
  * Error en estado estacionario < 2 %

Vamos a escribir un par de pequeñas funciones que nos calculen estas magnitudes:

<pre><code class="language-python">def tr(t, y, ys=None, margins=(0.0, 1.0)):
    """Rise time.
    Other possible margins: (0.05, 0.95), (0.1, 0.9). If no ys is given,
    then last value of y is assumed as stationary.
    """
    if ys is None:
        ys = y[-1]
    # Values between margins[0] * ys and margins[1] * ys
    mask = (y &gt; margins[0] * ys) & (y &lt; margins[1] * ys)
    # If response oscillates, only interested in limits of first region
    idx_change = np.nonzero(np.diff(mask))[0]
    # Initial and final indexes
    idx = idx_change[0], idx_change[1]
    # Time difference
    return t[idx[1]] - t[idx[0]]
def Ms(y, ys=None):
    """Maximum overshoot.
    Other possible margins: (0.05, 0.95), (0.1, 0.9). If no ys is given,
    then last value of y is assumed as stationary.
    """
    if ys is None:
        ys = y[-1]
    ymax = np.max(y)
    Ms = (ymax - ys) / ys
    return Ms</code></pre>

Se comprueba que para $K\_p = 700$ y $K\_i = 100$ cumplimos:

<pre><code class="language-python">K_p = 700.0
K_i = 100.0
# Sistema controlador-planta
sys_pc = series(([K_p, K_i], [1, 0]), sys_car)
# Sistema realimentado
sys_prop = feedback(sys_pc)
# Respuesta a entrada escalón
t = np.linspace(0, 60, num=200)
t, y = signal.step2(sys_prop, T=t)
print("Tiempo de subida: {:.2f} s".format(tr(t, y)))
print("Máxima sobreelongación: {:.1f} %".format(Ms(y) * 100))
# Tiempo de subida: 4.22 s
# Máxima sobreelongación: 6.3 %</code></pre>

<img class="aligncenter size-full wp-image-1960" alt="Parámetros finales de control PI" src="http://new.pybonacci.org/images/2013/11/kp700ki100.png" width="394" height="283" srcset="https://pybonacci.org/wp-content/uploads/2013/11/kp700ki100.png 394w, https://pybonacci.org/wp-content/uploads/2013/11/kp700ki100-300x215.png 300w" sizes="(max-width: 394px) 100vw, 394px" />

¡Genial!

### Derivativo

Ya hemos cumplido nuestros requisitos así que no tendríamos porqué añadir un término derivativo, y por tanto en este artículo no lo vamos a estudiar en detalle. Este tendrá como efecto **suavizar** la respuesta, aunque tiene una contrapartida importante: en presencia de ruido puede desestabilizar el sistema. El artículo ya es demasiado largo y el análisis es idéntico al efectuado anteriormente, así que se deja como ejercicio al lector 🙂

## Otros métodos

El control PID es ampliamente utilizado, especialmente para sistemas de los que desconocemos su funcionamiento interno («cajas negras») y es relativamente simple. Sin embargo, sintonizar controladores PID puede ser más complicado de lo que parece y en general no se consigue un control óptimo. Existen otros métodos como el del [lugar de las raíces](http://es.wikipedia.org/wiki/Lugar_de_ra%C3%ADces) o el estudio de la respuesta en frecuencia que son también útiles para diseñar sistemas de control. Pero de ellos ya hablaremos en entregas sucesivas, si el público lo reclama 😉

Espero que nos hagáis llegar vuestros comentarios y sugerencias a través del formulario más abajo y que os haya gustado el artículo.

¡Un saludo!

## Apéndice: Estado del arte

Aquí hemos visto que con Python hemos tenido que trabajar un poco más de lo que tendríamos que haber trabajado con MATLAB. Por un lado, hemos tenido que escribir nuestras propias funciones para operar con bloques, calcular tiempos de subida y sobreelongaciones... Y por otro lado, se echa en falta una interfaz gráfica con la que trabajar de una manera mucho más intuitiva (los diagramas del artículo están hechos con Inkscape, y ha sido un poco laborioso). En este área SciPy tiene aún mucho que mejorar, y de hecho ya hay algunas ideas.

Implementar operaciones con sistemas LTI o crear una interfaz gráfica son tareas relativamente sencillas, pero requieren que alguien se ponga con ellas. Si alguno de nuestros lectores quiere dar un paso adelante, le animamos a que contacte con nosotros, haga un fork de SciPy y se ponga a trabajar. El inglés no es un problema: podemos guiarle con el proceso en [nuestro propio fork, como ya anunciamos hace unos meses](http://pybonacci.org/2013/08/23/informando-de-bugs-en-numpy-y-scipy-en-castellano-a-traves-de-pybonacci/ "Informando de bugs en NumPy y SciPy en castellano a través de Pybonacci").

Como el título del artículo deja bien claro que íbamos a usar SciPy, he descartado la biblioteca [python-control](http://www.cds.caltech.edu/~murray/wiki/index.php/Python-control). En muchos sentidos está más avanzada que el paquete signal de SciPy **y proporciona compatibilidad con MATLAB**, pero no me queda claro si la están manteniendo activamente o no, y por tanto no me he decidido a utilizarla. Por si alguien tiene curiosidad, aquí hay un [ejemplo analizando el sistema de despegue y aterrizaje de un avión](http://www.cds.caltech.edu/~murray/wiki/index.php/Python-control/Example:_Vertical_takeoff_and_landing_aircraft).

## Referencias

  1. SEDRA, Adel S.; SMITH, Kenneth C. _Microelectronic circuits_. Oxford University Press, 2004.
  2. MESSNER, Bill et al. _Control Tutorials for MATLAB and Simulink_ [en línea]. 2011. Disponible en web: <<http://ctms.engin.umich.edu/>>. [Consulta: 10 de octubre de 2013]
  3. GIL, Jorge Juan; RUBIO, Ángel. _Fundamentos de Control Automático de Sistemas Continuos y Muestreados_. Universidad de Navarra, 2009.
  4. OGATA, Katsuhiko. _Ingeniería de control moderna_. 5ª ed. Pearson, 2010.