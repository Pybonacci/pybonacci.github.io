---
title: Teoría de control en Python con SciPy (I): Conceptos básicos
date: 2013-10-10T19:45:23+00:00
author: Juan Luis Cano
slug: teoria-de-control-en-python-con-scipy-i
tags: control, python, python 3, scipy, scipy.signal

## Introducción

En esta serie de artículos vamos a estudiar **cómo podemos aplicar Python al estudio de la teoría de control**, en este caso utilizando SciPy. La teoría de control se centra en los **sistemas dinámicos** con entradas: sistemas físicos cuyo estado evoluciona con el tiempo en función de la información que reciben del exterior. Como puedes ver, esta definición es enormemente amplia: el control toca aspectos de la ingeniería y de las matemáticas, y tiene aplicaciones también en las ciencias sociales: psicología, sociología, finanzas...

  1. **Conceptos básicos**
  2. [Control PID](http://pybonacci.org/2013/11/06/teoria-de-control-en-python-con-scipy-ii-control-pid/ "Teoría de control en Python con SciPy (II): Control PID")

En esta primera parte vamos a hacer una breve introducción matemática para centrar el tema y vamos a ver el manejo básico de sistemas LTI.

Cuando uno piensa en estudiar sistemas dinámicos con un ordenador, automáticamente se le viene a la cabeza **MATLAB**, y no sin motivo. Este programa tiene unas capacidades extraordinarias en este campo, y aunque nos duela decirlo _Python no está al mismo nivel_. Sin embargo, queremos mostrar en este artículo que Python tiene el potencial de ser una alternativa real a MATLAB, enseñando los fundamentos del análisis de sistemas dinámicos utilizando el paquete `scipy.signal`. Yo mismo he trabajado un poco en este paquete en los últimos meses, así que he tenido la oportunidad de ver cómo funciona y también de conocer sus carencias; algunas de mis contribuciones han visto la luz en la recién liberada versión 0.13 de SciPy, pero aún queda mucho por mejorar.<figure id="attachment_1904" style="width: 418px" class="wp-caption aligncenter">

[<img class=" wp-image-1904 " src="http://new.pybonacci.org/images/2013/10/lti_laplace.png" alt="Equivalencia entre los dominios del tiempo y de la frecuencia a través de la transformada de Laplace" width="418" height="296" srcset="https://pybonacci.org/wp-content/uploads/2013/10/lti_laplace.png 696w, https://pybonacci.org/wp-content/uploads/2013/10/lti_laplace-300x212.png 300w" sizes="(max-width: 418px) 100vw, 418px" />](http://new.pybonacci.org/images/2013/10/lti_laplace.png)<figcaption class="wp-caption-text">Equivalencia entre los dominios del tiempo y de la frecuencia a través de la transformada de Laplace</figcaption></figure> 

Los ejemplos para este artículo los he sacado de [Sedra y Smith, 2004], un excelente libro de electrónica, y de [Messner et al. 2011], unos tutoriales para MATLAB y Simulink. Para la teoría, recomiendo el excelente [Gil y Rubio 2009], un libro editado por la Universidad de Navarra y disponible para visualización, impresión y copia para uso personal sin fines de lucro (¡gracias @Alex__S12!).

_**En esta entrada se han usado python 3.3.2, numpy 1.8.0, scipy 0.13.0 y matplotlib 1.3.0.**_

## Sistemas lineales invariantes en el tiempo o LTI

Vamos a centrarnos en los **sistemas lineales e invariantes en el tiempo** (en inglés, sistemas _LTI_), que como su propio nombre indica tienen estas propiedades:

  * **Linealidad**: el sistema cumple el principio de superposición.
  * **Invarianza en el tiempo**: el comportamiento del sistema no varía con el tiempo: una misma entrada en dos instantes de tiempo diferentes siempre producirá la misma salida.

Concretamente, muchos de estos sistemas pueden modelarse como un sistema de ecuaciones diferenciales ordinarias lineales de coeficientes constantes. Restringiendo aún más nuestro objeto de estudio, para **sistemas de una sola entrada y una sola salida** (_SISO_ en inglés) tendremos:

$\displaystyle a\_n \frac{d^n y}{dt^n} + a\_{n-1} \frac{d^{n-1} y}{dt^{n-1}} + \dots + y(t) = b\_m \frac{d^m x}{dt^m} + b\_{m-1} \frac{d^{m-1} x}{dt^{m-1}} + \dots + x(t)$

donde $y(t)$ es la respuesta del sistema y $x(t)$ es la entrada, conocida. Aplicando la **transformada de Laplace** a la ecuación tendremos:

$\displaystyle Y(s) = \frac{b\_m s^m + b\_{m-1} s^{m-1} + \dots + 1}{a\_n s^n + a\_{n-1} s^{n-1} + \dots + 1} X(s) = H(s) X(s) $

siendo $Y(s)$ y $X(s)$ las transformadas de laplace de $y(t)$ y $x(t)$ y $H(s)$ la **función de transferencia del sistema**. Vemos que la ecuación resultante es algebraica y por tanto muy fácil de resolver.

<!--more-->

Precisamente la función de transferencia es una de las formas que tenemos de definir un sistema LTI en Python. Para ello simplemente tenemos que usar la función [`signal.lti`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lti.html), que acepta como argumento una tupla de dos, tres o cuatro elementos:

  * Si damos **dos** elementos, deberán ser dos listas con los coeficientes de los polinomios del numerador y del denominador, **siguiendo la convención antigua de coeficientes decrecientes** (la convención contraria a la usada en nuestro [artículo sobre ajuste e interpolación](http://pybonacci.org/2013/08/15/ajuste-e-interpolacion-unidimensionales-basicos-en-python-con-scipy/ "Ajuste e interpolación unidimensionales básicos en Python con SciPy")).
  * Si damos **tres** elementos, deberán ser los ceros, polos y ganancia del sistema (ver más adelante).
  * Si damos **cuatro** elementos, deberán ser las matrices de espacio de estado A, B, C y D (ver más adelante).

En la siguiente sección veremos cómo se utiliza.

### Respuesta en frecuencia

Por ejemplo, representemos la respuesta en frecuencia de un **filtro pasabajos** sencillo:

$\displaystyle H(s) = \frac{K}{(s / omega_0) + 1}$

usando el diagrama de Bode. Este es el código:

<pre><code class="language-python">from scipy import signal
import matplotlib.pyplot as plt
K = 1
w0 = 1e3 # rad / s
sys1 = signal.lti([K], [1 / w0, 1]) # Creamos el sistema
w, mag, phase = signal.bode(sys1) # Diagrama de bode: frecuencias, magnitud y fase
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
ax1.semilogx(w, mag) # Eje x logarítmico
ax2.semilogx(w, phase) # Eje x logarítmico</code></pre><figure id="attachment_1914" style="width: 341px" class="wp-caption aligncenter">

[<img class=" wp-image-1914 " src="http://new.pybonacci.org/images/2013/10/bode_lp1.png" alt="Diagrama de Bode de un filtro pasabajos." width="341" height="351" srcset="https://pybonacci.org/wp-content/uploads/2013/10/bode_lp1.png 426w, https://pybonacci.org/wp-content/uploads/2013/10/bode_lp1-291x300.png 291w" sizes="(max-width: 341px) 100vw, 341px" />](http://new.pybonacci.org/images/2013/10/bode_lp1.png)<figcaption class="wp-caption-text">Diagrama de Bode de un filtro pasabajos.</figcaption></figure> 

¿Qué sucede si queremos acceder a las otras representaciones de nuestro sistema? Tenemos los atributos (`zeros`, `poles`, `gain`) y (`A`, `B`, `C`, `D`):

<pre><code class="language-python">print(sys1.zeros, sys1.poles, sys1.gain) # [] [-1000.] 1000.0
print(sys1.A, sys1.B, sys1.C, sys1.D) # [[-1000.]] [[ 1.]] [[ 1000.]] [ 0.]</code></pre>

Otras dos herramientas que nos pueden ser útiles para analizar un sistema LTI son su **diagrama de Nyquist** y su **mapa de ceros-polos**. Para el primero podemos valernos de la función [`signal.freqresp`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.freqresp.html), que devuelve la respuesta compleja en frecuencia de un sistema, y representar la parte imaginaria respecto a la parte real. Para el segundo, lo que hemos visto en el párrafo anterior:

<pre><code class="language-python">sys2 = signal.lti([1, 2], [1, 6, 25]) # H(s) = (s + 2) / (s ** 2 + 6 * s + 25)
w, H = signal.freqresp(sys2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
ax1.plot(H.real, H.imag)
ax1.plot(H.real, -H.imag)
ax2.plot(sys2.zeros.real, sys2.zeros.imag, 'o')
ax2.plot(sys2.poles.real, sys2.poles.imag, 'x')</code></pre><figure id="attachment_1923" style="width: 513px" class="wp-caption aligncenter">

[<img class="size-full wp-image-1923" src="http://new.pybonacci.org/images/2013/10/nyquist_pzmap1.png" alt="Diagrama de Nyquist y mapa de polos-ceros." width="513" height="283" srcset="https://pybonacci.org/wp-content/uploads/2013/10/nyquist_pzmap1.png 513w, https://pybonacci.org/wp-content/uploads/2013/10/nyquist_pzmap1-300x165.png 300w" sizes="(max-width: 513px) 100vw, 513px" />](http://new.pybonacci.org/images/2013/10/nyquist_pzmap1.png)<figcaption class="wp-caption-text">Diagrama de Nyquist y mapa de polos-ceros.</figcaption></figure> 

### Respuesta temporal

Vamos a trabajar ahora sobre un ejemplo más elaborado: **el control de velocidad de crucero de un coche**. El objetivo es mantener constante la velocidad frente a perturbaciones externas, como por ejemplo cambios en la pendiente o ráfagas de viento. Si asumimos que las fuerzas de resistencia varían linealmente con la velocidad, tendremos:

$\displaystyle m \frac{d^2 x}{d t^2} = F - b v \Rightarrow m \dot{v} + b v = F$

siendo $m$ la masa del vehículo.<figure id="attachment_1911" style="width: 435px" class="wp-caption aligncenter">

[<img class=" wp-image-1911 " src="http://new.pybonacci.org/images/2013/10/lti_cruise.png" alt="Diagrama de fuerzas sobre nuestro coche" width="435" height="140" srcset="https://pybonacci.org/wp-content/uploads/2013/10/lti_cruise.png 622w, https://pybonacci.org/wp-content/uploads/2013/10/lti_cruise-300x96.png 300w" sizes="(max-width: 435px) 100vw, 435px" />](http://new.pybonacci.org/images/2013/10/lti_cruise.png)<figcaption class="wp-caption-text">Diagrama de fuerzas sobre nuestro coche</figcaption></figure> 

La **entrada** de nuestro sistema será la **fuerza de tracción** aplicada, y la **salida** o variable que queremos controlar será la **velocidad**. La función de transferencia será:

$\displaystyle H(s) = frac{V(s)}{F(s)} = \frac{1}{m s + b}$

Ya podemos definir el sistema:

<pre><code class="language-python">m = 1200  # kg
b = 75  # Ns / m
sys_car = signal.lti(1, [m, b])</code></pre>

Con estos datos, necesitaría una fuerza de 2250 N para conseguir una velocidad de 30 m/s. Podemos ver cómo será la respuesta del sistema utilizando la función [`signal.step2`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.step2.html).

_**Nota**_: La función <del><code>signal.step</code></del> [tiene](https://github.com/scipy/scipy/issues/1104) [problemas](https://github.com/scipy/scipy/issues/2652) y se escribió `signal.step2` como reemplazo. En un futuro estas dos funciones se fusionarán bajo el mismo nombre, pero mientras tanto se recomienda usar `signal.step2`.

Esta función **calcula la respuesta a una entrada escalón unidad**. Como el sistema es lineal, podemos multiplicar la salida por el valor de la fuerza y este resultado será igual a la respuesta a un escalón de altura ese valor:

<pre><code class="language-python">t, y = signal.step2(sys_car) # Respuesta a escalón unitario
plt.plot(t, 2250 * y) # Equivalente a una entrada de altura 2250</code></pre><figure id="attachment_1916" style="width: 394px" class="wp-caption aligncenter">

[<img class="size-full wp-image-1916" src="http://new.pybonacci.org/images/2013/10/cruise_step.png" alt="Respuesta del sistema a una entrada escalón." width="394" height="283" srcset="https://pybonacci.org/wp-content/uploads/2013/10/cruise_step.png 394w, https://pybonacci.org/wp-content/uploads/2013/10/cruise_step-300x215.png 300w" sizes="(max-width: 394px) 100vw, 394px" />](http://new.pybonacci.org/images/2013/10/cruise_step.png)<figcaption class="wp-caption-text">Respuesta del sistema a una entrada escalón.</figcaption></figure> 

Vemos que la velocidad va aumentando, al principio rápidamente y luego más despacio (producto de las fuerzas de resistencia), hasta llegar a un valor límite, que es 30 m/s como habíamos dicho al principio. En la gráfica hemos incluido también:

  * El **tiempo de subida** (_rising time_), definido como el tiempo necesario para pasar de un 5 % a un 95 % de la solución estacionaria, y
  * el **tiempo de establecimiento** (_settling time_), definido como el tiempo necesario para que la respuesta se mantenga dentro de un margen del 2 % de la solución estacionaria.

La conclusión que podemos extraer de este gráfico es que **para pasar de 0 a 100 km/h, nuestro coche necesita casi un minuto**. ¡Fatal! ¿Cómo arreglamos esto? Aquí entra la belleza de la teoría de control, pero lo vamos a dejar para la segunda parte 🙂

Este artículo ha sido muy difícil de escribir, y el siguiente probablemente también lo será. Por eso os pedimos que **nos contéis en los comentarios** qué os ha parecido, qué partes se podrían mejorar, y puesto que hemos reconocido la debilidad de SciPy en este campo, qué cosas positivas podría tomar de MATLAB.

¡Un saludo!

## Referencias

  1. SEDRA, Adel S.; SMITH, Kenneth C. _Microelectronic circuits_. Oxford University Press, 2004.
  2. MESSNER, Bill et al. _Control Tutorials for MATLAB and Simulink_ [en línea]. 2011. Disponible en web: <<http://ctms.engin.umich.edu/>>. [Consulta: 10 de octubre de 2013]
  3. GIL, Jorge Juan; RUBIO, Ángel. _Fundamentos de Control Automático de Sistemas Continuos y Muestreados_. Universidad de Navarra, 2009.