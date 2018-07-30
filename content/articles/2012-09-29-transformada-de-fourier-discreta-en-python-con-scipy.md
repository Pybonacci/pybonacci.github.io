---
title: Transformada de Fourier discreta en Python con SciPy
date: 2012-09-29T23:43:37+00:00
author: Juan Luis Cano
slug: transformada-de-fourier-discreta-en-python-con-scipy
tags: fft, fftpack, python, scipy

## Introducción

En este artículo vamos a ver **cómo calcular la transformada de Fourier discreta** (o DFT) de una señal en Python utilizando la **transformada rápida de Fourier** (o FFT) implementada en SciPy. El análisis de Fourier es la herramienta fundamental en procesamiento de señales y resulta útil en otras áreas como en la resolución de ecuaciones diferenciales o en el tratamiento de imágenes.

<ins datetime="2012-10-02T13:51:56+00:00"><strong>Nota</strong>: Puedes <a href="http://nbviewer.ipython.org/3804365/">ver el artículo en forma de notebook de IPython</a> mediante la herramienta nbviewer.</ins>

La transformada rápida de Fourier o FFT es en realidad una familia de algoritmos muy eficientes ($O(n \log n)$) para calcular la DFT de una señal discreta, de los cuales el más utilizado es el algoritmo de Cooley-Tukey. Este es el que está implementado en SciPy a través de las subrutinas FFTPACK, escritas en FORTRAN 77, y es el que vamos a utilizar. También podríamos haber utilizado la biblioteca FFTW, más moderna y escrita en C, o la implementación presente en NumPy, que es una traducción a C de FFTPACK y que funciona igual que la de SciPy, pero no lo vamos a hacer.

Nótese que estos métodos no nos permiten calcular ni la serie de Fourier de una función periódica ni la transformada de Fourier de una función no periódica. Estas operaciones forman parte del cálculo simbólico y deben llevarse a cabo con otro tipo de programas, como SymPy o Sage. En Pybonacci puedes leer una [introducción a SymPy](http://pybonacci.org/2012/04/04/introduccion-al-calculo-simbolico-en-python-con-sympy/ "Introducción al Cálculo Simbólico en Python con SymPy") y [cómo calcular series con SymPy](http://pybonacci.org/2012/04/30/como-calcular-limites-derivadas-series-e-integrales-en-python-con-sympy/ "Cómo calcular límites, derivadas, series e integrales en Python con SymPy"), así como una [reseña sobre Sage](http://pybonacci.org/2012/05/06/sage-software-matematico-libre-como-alternativa/ "Sage: software matemático libre como alternativa").

En este artículo nos vamos a centrar en el caso unidimensional, aunque el código es fácilmente extrapolable al caso de dos y más dimensiones.

_**En esta entrada se ha usado python 2.7.3, numpy 1.6.2, scipy 0.10.1 y matplotlib 1.1.1.**_

## Definiciones

Antes de empezar de lleno con las FFTs vamos a hacer una brevísima introducción matemática. He intentado que esto no se convierta en una larga introducción al procesamiento de señales digitales, pero si te interesa el tema y quieres más rigor puedes acudir a cualquiera de las referencias que doy más abajo además de la [documentación de `scipy.fftpack`](http://docs.scipy.org/doc/numpy/reference/routines.fft.html).

<!--more-->

En este artículo vamos a manejar **señales discretas reales**, bien creadas por nosotros o procedentes de _muestrear_ una señal analógica a una frecuencia de muestreo fs. La **transformada discreta de Fourier** o DFT de la señal de entrada, que diremos que está _en el dominio del tiempo_, será otra señal discreta, n general _compleja_, cuyos coeficientes vienen definidos en SciPy por la expresión

<p style="text-align: center">
  $ \displaystyle A_k = \sum_{m=0}^{n-1} a_m \exp\left(-2\pi j{mk \over n}\right) \qquad k = 0,\ldots,n-1,$
</p>

siendo $a\_n$ los coeficientes de la señal de entrada y $A\_k$ los de la señal obtenida. Diremos que $A_k$ está _en el dominio de la frecuencia_ y que es el **espectro** o **transformada** de $a_n$. La resolución en frecuencia será mayor cuanto mayor sea el número de intervalos $n$ de la señal de entrada. La DFT se calcula con el algoritmo de la **transformada rápida de Fourier** o FFT, que es más eficiente si $n$ es una potencia entera de 2.

Cada uno de los componentes de frecuencia se puede expresar en forma compleja como $A \exp(j \omega t)$. El espectro complejo de una función seno, por ejemplo, se obtiene directamente de su expresión en forma compleja

<p style="text-align: center">
  $ \displaystyle A \sin(\omega t) = A \frac{e^{j \omega t} - e^{-j \omega t}}{2 j} = -j \frac{A}{2} e^{j \omega t} + j \frac{A}{2} e^{-j \omega t}$
</p>

y tendrá, por tanto, una raya espectral a la frecuencia $\omega$ y otra a la frecuencia $-\omega$, como ya comprobaremos.

La DFT de una señal _siempre_ asume que la señal de entrada es **un período de una secuencia periódica**. Esto será importante por lo que luego veremos. Sería, por tanto, el equivalente en tiempo discreto a las series de Fourier.

## FFT de una función senoidal sencilla

Vamos a **calcular la FFT de una función senoidal en Python utilizando SciPy**. Para que sea verdaderamente sencilla tenemos que preparar un poco los datos, o si no acabaremos observando efectos adversos. Estos los estudiaremos más adelante.

Para manejar números redondos, vamos a recrear una señal con un armónico de $f = 400~Hz$ y otro del doble de frecuencia:

<p style="text-align: center">
  $ \displaystyle y(t) = \sin(2 \pi f) - \frac{1}{2} \sin(2 \pi \cdot 2 f)$
</p>

donde $2 \pi f = \omega$. Nótese que, por lo que hemos visto en el apartado anterior, veremos cuatro rayas en el espectro de esta función: dos para la frecuencia $f$ y otras dos para la $2 f$. Vamos a imponer a priori el número de intervalos y la distancia entre ellos y de ahí vamos a calcular el intervalo de tiempo. Evidentemente así no se funciona cuando muestreamos un archivo de audio, pongo por caso, pero como digo así obtendremos el resultado exacto. El código y la salida serían las siguientes:

<pre><code class="language-python">import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
n = 2 ** 6  # Número de intervalos
f = 400.0  # Hz
dt = 1 / (f * 16)  # Espaciado, 16 puntos por período
t = np.linspace(0, (n - 1) * dt, n)  # Intervalo de tiempo en segundos
y = np.sin(2 * pi * f * t) - 0.5 * np.sin(2 * pi * 2 * f * t)  # Señal
plt.plot(t, y)
plt.plot(t, y, 'ko')
plt.xlabel('Tiempo (s)')
plt.ylabel('$y(t)$')</code></pre>

![Señal 1](http://pybonacci.org/images/2012/09/sec3b1al1.png)

Esta es la señal que vamos a transformar. Fijáos en el último punto representado. Como el intervalo va desde 0 hasta `n - 1`, los trozos «empalman» perfectamente. Ahora vamos a hallar la DFT de la señal `y`. Para ello necesitamos dos funciones, que se importan del paquete scipy.fftpack:

  * La función [`fft`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.fft.html), que devuelve la DFT de la señal de entrada. Si queremos que esté normalizada, tenemos que dividir después por el número de intervalos N.
  * La función [`fftfreq`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.fftfreq.html), que devuelve las frecuencias a las que corresponde cada punto de la DFT. Se usa conjuntamente con la función anterior y acepta dos argumentos: el número de elementos n y el espacio entre intervalos dt, que ya hemos calculado antes.

Como en este caso solo hay dos frecuencias fundamentales, vamos a representarlas utilizando la función vlines de matplotlib. El código y la salida quedarían así:

<pre><code class="language-python">from scipy.fftpack import fft, fftfreq
Y = fft(y) / n  # Normalizada
frq = fftfreq(n, dt)  # Recuperamos las frecuencias
plt.vlines(frq, 0, Y.imag)  # Representamos la parte imaginaria
plt.annotate(s=u'f = 400 Hz', xy=(400.0, -0.5), xytext=(400.0 + 1000.0, -0.5 - 0.35), arrowprops=dict(arrowstyle = "-&gt;"))
plt.annotate(s=u'f = -400 Hz', xy=(-400.0, 0.5), xytext=(-400.0 - 2000.0, 0.5 + 0.15), arrowprops=dict(arrowstyle = "-&gt;"))
plt.annotate(s=u'f = 800 Hz', xy=(800.0, 0.25), xytext=(800.0 + 600.0, 0.25 + 0.35), arrowprops=dict(arrowstyle = "-&gt;"))
plt.annotate(s=u'f = -800 Hz', xy=(-800.0, -0.25), xytext=(-800.0 - 1000.0, -0.25 - 0.35), arrowprops=dict(arrowstyle = "-&gt;"))
plt.ylim(-1, 1)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Im($Y$)')</code></pre>

![Transformada 1](http://pybonacci.org/images/2012/09/transformada1.png)

**Nota**: Si quieres leer más sobre añadir texto y anotaciones a una gráfica en matplotlib, puedes leer la parte VIII del nuestro [magnífico tutorial de matplotlib](http://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones") por Kiko 🙂

¡Y ya hemos hecho nuestra primera transformada discreta de Fourier con el algoritmo FFT! Pero las cosas en la realidad son bastante más complicadas. Vamos a ver algunos de los problemas que apareceran con frecuencia.

## Fuga, «zero-padding» y funciones ventana

Vamos a analizar el ejemplo anterior, pero en esta ocasión vamos a poner menos cuidado con la preparación de los datos. Veamos qué ocurre:

<pre><code class="language-python">n2 = 2 ** 5
t2 = np.linspace(0, 0.012, n2)  # Intervalo de tiempo en segundos
dt2 = t2[1] - t2[0]
y2 = np.sin(2 * pi * f * t2) - 0.5 * np.sin(2 * pi * 2 * f * t2)  # Señal
Y2 = fft(y2) / n2  # Transformada normalizada
frq2 = fftfreq(n2, dt2)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(211)
ax1.plot(t2, y2)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('$y_2(t)$')
ax2 = fig.add_subplot(212)
ax2.vlines(frq2, 0, Y2.imag)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Im($Y_2$)')</code></pre>

![Señal 2](http://pybonacci.org/images/2012/09/sec3b1al2.png)

Como se puede ver, el fenómeno no es extremadamente importante pero han aparecido otras rayas espectrales que no esperábamos. Esto se conoce como «leaking» (y yo lo voy a traducir por fuga) y es debido a que, en este caso, los trozos «no empalman exactamente». Recuerda que la DFT, y por extensión la FFT asume que estamos transformando un período de una señal periódica. Si utilizamos más puntos y extendemos la señal con ceros (esto se conoce como «zero-padding») la DFT da más resolución en frecuencia pero la fuga se magnifica:

<pre><code class="language-python">t3 = np.linspace(0, 0.012 + 9 * dt2, 10 * n2)  # Intervalo de tiempo en segundos
y3 = np.append(y2, np.zeros(9 * n2))  # Señal
Y3 = fft(y3) / (10 * n2)  # Transformada normalizada
frq3 = fftfreq(10 * n2, dt2)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(211)
ax1.plot(t3, y3)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('$y_3(t)$')
ax2 = fig.add_subplot(212)
ax2.vlines(frq3, 0, Y3.imag)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Im($Y_3$)')</code></pre>

![Señal 3](http://pybonacci.org/images/2012/09/sec3b1al3.png)

Existe una manera de reducir la fuga y es mediante el uso de **funciones ventana**. Las funciones ventana no son más que funciones que valen cero fuera de un cierto intervalo, y que en procesamiento de señales digitales se utilizan para «suavizar» o filtrar una determinada señal. NumPy trae [unas cuantas funciones ventana](http://docs.scipy.org/doc/numpy/reference/routines.window.html) por defecto; por ejemplo, la ventana de Blackman tiene este aspecto:

![Ventana de Blackman](http://pybonacci.org/images/2012/09/blackman.png)

Como se puede ver, en los extremos del intervalo es nula. Las funciones ventana reciben un único argumento que es el número de puntos. Si multiplicamos la ventana por la señal, obtenemos una nueva señal que vale cero en los extremos. Comprobemos el resultado, representando ahora el espectro de amplitud y comparando cómo es el resultado si aplicamos o no la ventana de Blackman:

<pre><code class="language-python">n4 = 2 ** 8
t4 = np.linspace(0, 0.05, n4)
dt4 = t4[1] - t4[0]
y4 = np.sin(2 * pi * f * t4) - 0.5 * np.sin(2 * pi * 2 * f * t4)
y5 = y4 * np.blackman(n4)
t4 = np.linspace(0, 0.12 + 4 * dt4, 5 * n4)
y4 = np.append(y4, np.zeros(4 * n4))
y5 = np.append(y5, np.zeros(4 * n4))
Y4 = fft(y4) / (5 * n4)
Y5 = fft(y5) / (5 * n4)
frq4 = fftfreq(5 * n4, dt4)
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(411)
ax1.plot(t4, y4)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$y_4(t)$')
ax2 = fig.add_subplot(412)
ax2.vlines(frq4, 0, abs(Y4))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_4$)')
ax3 = fig.add_subplot(413)
ax3.plot(t4, y5)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('$y_5(t)$')
ax4 = fig.add_subplot(414)
ax4.vlines(frq4, 0, abs(Y5))  # Espectro de amplitud
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Abs($Y_5$)')</code></pre>

![Aplicación de la ventana de Blackman](http://pybonacci.org/images/2012/09/windowing.png)

Esto ya ha sido más interesante, ¿no? 🙂

## Otros ejemplos: procesamiento de audio, espectrogramas

Para acabar de manera triunfal, vamos a ver **cómo representar el espectrograma de un fragmento de audio**, utilizando la función [`specgram`](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.specgram) de matplotlib. El espectrograma se obtiene de aplicar la transformada corta de Fourier (STFT) a una señal, que es como aplicar una DFT a pequeños fragmentos de la misma, para ver la evolución de las frecuencias a lo largo del tiempo. Para ello, vamos a usar este [fragmento de una melodía tocada con un violín](http://commons.wikimedia.org/wiki/File:Violin_for_spectrogram.ogg), disponible libremente en Wikimedia Commons y que está muestreado a 44,1 kHz:

<p style="text-align:center">
</p>

Al tratarse de un archivo OGG, vamos a utilizar el [SciKit audiolab](http://scikits.appspot.com/audiolab).

<pre><code class="language-python">import matplotlib.pyplot as plt
import scikits.audiolab as audiolab
sound = audiolab.sndfile('Violin_for_spectrogram.ogg', 'read')
y = sound.read_frames(sound.get_nframes())
Pxx, freqs, bins, im = plt.specgram(y, NFFT=512, Fs=44100)
plt.xlim(0, len(y) / 44100.0)
plt.ylim(0, 22050.0)
plt.colorbar(im).set_label(u'Intensidad (dB)')
plt.xlabel(u'Tiempo (s)')
plt.ylabel(u'Frecuencia (Hz)')</code></pre>

![Espectrograma](http://pybonacci.org/images/2012/09/specgram.png)

Se puede apreciar cómo va cambiando la frecuencia fundamental (barras horizontales inferiores) y los armónicos (todas las que están encima, cada vez más débiles) a medida que el intérprete toca una nota distinta. En definitiva, una preciosidad 😛

Espero que te haya gustado el artículo. Más abajo tienes las referencias en las que me he basado y unos cuantos enlaces que me han sido muy útiles para aprender procesamiento de señales digitales, porque cuando empecé a escribir el artículo no sabía nada sobre el tema. Sobre todo he aprendido la teoría con [II] y los ejemplos están inspirados en el capítulo «Example Applications of the DFT» de [I]. Si ves algún error o quieres apuntar alguna sugerencia, no dudes en decirlo en los comentarios.

¡Un saludo desde Milano! 🙂

## Referencias

  1. SMITH, Julius O. _Mathematics of the discrete Fourier transform (DFT) with audio applications_ [en línea]. Segunda edición. Disponible en Web: <<https://ccrma.stanford.edu/~jos/mdft/mdft.html>>. [Consulta: 28 de septiembre de 2012]
  2. LOPEZ-LEZCANO, Fernando; CACERES, Juan-Pablo. _Introducción al Procesamiento Digital de Señales y a la Música por Computador_ [en línea]. Disponible en Web: <[https://ccrma.stanford.edu/workshops/cm2007/index.shtml](https://ccrma.stanford.edu/~jos/mdft/mdft.html)>. [Consulta: 28 de septiembre de 2012]

## Enlaces

  * Análisis espectral de una sinusoide <a href="https://ccrma.stanford.edu/%7Ejos/mdft/Spectrum_Analysis_Sinusoid_Windowing.html" target="_blank">https://ccrma.stanford.edu/~jos/mdft/Spectrum_Analysis_Sinusoid_Windowing.html</a>
  * Teoría general <a href="http://paulbourke.net/miscellaneous/dft/" target="_blank">http://paulbourke.net/miscellaneous/dft/</a>
  * NumPy no es adecuado para _series de Fourier_ <a href="http://stackoverflow.com/questions/4258106/how-to-calculate-a-fourier-series-in-numpy" target="_blank">http://stackoverflow.com/questions/4258106/how-to-calculate-a-fourier-series-in-numpy</a>
  * Reconstrucción de la señal a partir de algunos términos calculados con fft <a href="http://stackoverflow.com/questions/5843085/fourier-series-in-numpy-question-about-previous-answer" target="_blank">http://stackoverflow.com/questions/5843085/fourier-series-in-numpy-question-about-previous-answer</a>
  * Uso de fftfreq <a href="http://stackoverflow.com/questions/9456037/scipy-numpy-fft-frequency-analysis" target="_blank">http://stackoverflow.com/questions/9456037/scipy-numpy-fft-frequency-analysis</a>
  * Unidades de fftfreq <a href="http://stackoverflow.com/questions/8573702/units-of-frequency-when-using-fft-in-numpy" target="_blank">http://stackoverflow.com/questions/8573702/units-of-frequency-when-using-fft-in-numpy</a>
  * Frecuencias de fftfreq <a href="http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python" target="_blank">http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python</a>
  * Artículo de The Glowing Python <a href="http://glowingpython.blogspot.com.es/2011/08/how-to-plot-frequency-spectrum-with.html" target="_blank">http://glowingpython.blogspot.com.es/2011/08/how-to-plot-frequency-spectrum-with.html</a>
  * Demo de MathWorks <a href="http://www.mathworks.es/products/matlab/examples.html?file=/products/demos/shipping/matlab/fftdemo.html" target="_blank">http://www.mathworks.es/products/matlab/examples.html?file=/products/demos/shipping/matlab/fftdemo.html</a>
  * Documentación de MATLAB <a href="http://www.mathworks.es/help/matlab/ref/fft.html" target="_blank">http://www.mathworks.es/help/matlab/ref/fft.html</a>
  * Diferencias entre NumPy y SciPy <a href="http://stackoverflow.com/questions/6363154/what-is-the-difference-between-numpy-fft-and-scipy-fftpack" target="_blank">http://stackoverflow.com/questions/6363154/what-is-the-difference-between-numpy-fft-and-scipy-fftpack</a>
  * Zero-padding of a signal <a href="http://dsp.stackexchange.com/questions/741/why-should-i-zero-pad-a-signal-before-taking-the-fourier-transform" target="_blank">http://dsp.stackexchange.com/questions/741/why-should-i-zero-pad-a-signal-before-taking-the-fourier-transform</a>
  * Uso de funciones ventana <a href="https://docs.google.com/open?id=1FliaqX0ModFkrPEvCtconY4vNlzU0r3luLkSl9Zk3WB48YyyAd12oD-Pw9IQ" target="_blank">https://docs.google.com/open?id=1FliaqX0ModFkrPEvCtconY4vNlzU0r3luLkSl9Zk3WB48YyyAd12oD-Pw9IQ</a>
  * Para ampliar: DSP con SciPy <a href="http://docs.scipy.org/doc/scipy/reference/signal.html" target="_blank">http://docs.scipy.org/doc/scipy/reference/signal.html</a>
  * Python para procesamiento de audio <a href="http://lac.linuxaudio.org/2011/papers/40.pdf" target="_blank">http://lac.linuxaudio.org/2011/papers/40.pdf</a>
  * Definición de intervalos de frecuencia <a href="http://www.maximintegrated.com/glossary/definitions.mvp/term/frequency_bin/gpk/136" target="_blank">http://www.maximintegrated.com/glossary/definitions.mvp/term/frequency_bin/gpk/136</a>