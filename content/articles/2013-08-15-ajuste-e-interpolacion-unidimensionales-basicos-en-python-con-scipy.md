---
title: Ajuste e interpolación unidimensionales básicos en Python con SciPy
date: 2013-08-15T13:14:15+00:00
author: Juan Luis Cano
slug: ajuste-e-interpolacion-unidimensionales-basicos-en-python-con-scipy
tags: interpolación, numpy, python, python 3, scipy, scipy.interpolate

## Introducción

En este artículo vamos a ver una introducción a **cómo hacer ajustes e interpolaciones en Python** utilizando NumPy y los módulos `interpolate` y `optimize` de SciPy.

Ajustes de curvas e interpolaciones son **dos tareas básicas que realizaremos con mucha frecuencia**. Por ejemplo, cuando recojamos los datos de un experimento: sabemos que se tienen que comportar como una parábola, pero obviamente por errores de medición u otro tipo no obtenemos una parábola exactamente. En este caso necesitaremos realizar un **ajuste de los datos**, conocido el modelo (una curva de segundo grado en este caso).

En otras ocasiones dispondremos de una serie de puntos y **querremos construir una curva que pase por todos ellos**. En este caso lo que queremos es realizar una **interpolación**: si tenemos pocos puntos podremos usar un polinomio, y en caso contrario habrá que usar trazadores (_splines_ en inglés). Vamos a empezar por este último método.

Si deseas consultar el código completo (incluyendo el que genera las figuras) puedes ver [el notebook que usé](http://nbviewer.ipython.org/6245476) para redactar el artículo.

**_En esta entrada se han usado python 3.3.2, numpy 1.7.1, scipy 0.12.0 y matplotlib 1.3.0._**

## Interpolación

### Polinomios no, ¡gracias!

Lo primero que vamos a hacer va a ser desterrar la idea de que, sea cual sea el número de puntos que tengamos, podemos construir un polinomio que pase por todos ellos «y que lo haga bien». Si tenemos $N$ puntos nuestro polinomio tendrá que ser de grado menor o igual que $N - 1$, pero cuando $N$ empieza a ser grande (del orden de 10 o más) a menos que los puntos estén muy cuidadosamente elegidos el polinomio oscilará salvajemente. Esto se conoce como [fenómeno de Runge](http://es.wikipedia.org/wiki/Fen%C3%B3meno_de_Runge).

<!--more-->

Para ver esto podemos estudiar el clásico ejemplo que dio Runge: tenemos la función

$\displaystyle f(x) = \frac{1}{1 + x^2}$

veamos qué sucede si la interpolamos en nodos equiespaciados. Para ello vamos a usar la función [`barycentric_interpolate`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.barycentric_interpolate.html) (según Berrut y Trefethen [II] «[El método de interpolación baricéntrica] merece ser conocido como el método estándar de interpolación polinómica»). Esta función recibe tres argumentos:

  * una lista de coordenadas `x_i` de los nodos,
  * una lista de coordenadas `y_i` de los nodos, y
  * un array `x` donde evaluar el polinomio interpolante que resulta.

El código será este:

<pre><code class="language-python">import numpy as np
from scipy.interpolate import barycentric_interpolate
def runge(x):
    """Función de Runge."""
    return 1 / (1 + x ** 2)
N = 11  # Nodos de interpolación
xp = np.arange(11) - 5  # -5, -4, -3, ..., 3, 4, 5
fp = runge(xp)
x = np.linspace(-5, 5)
y = barycentric_interpolate(xp, fp, x)</code></pre>

Y este es el resultado:<figure id="attachment_1754" style="width: 380px" class="wp-caption aligncenter">

![](http://pybonacci.org/images/2013/08/fenomeno_runge.png)

Y no os quiero contar nada si escogemos 20 o 100 puntos.

Existe una forma de mitigar este problema, que es, como ya hemos dicho, «escogiendo los puntos cuidadosamente». Una de las formas es elegir las raíces de los [polinomios de Chebyshev](http://es.wikipedia.org/wiki/Polinomios_de_Chebyshev), que podemos construir en NumPy usando el módulo [`polynomial.chebyshev`](http://docs.scipy.org/doc/numpy/reference/routines.polynomials.chebyshev.html). Por ejemplo, si queremos como antes 11 nodos tendremos que escoger el polinomio de Chebyshev de grado 11:

<pre><code class="language-python">from numpy.polynomial import chebyshev
coeffs_cheb = [0] * 11 + [1]  # Solo queremos el elemento 11 de la serie
T11 = chebyshev.Chebyshev(coeffs_cheb, [-5, 5])
xp_ch = T11.roots()
# -4.949, -4.548, -3.779, -2.703, ..., 4.548, 4.949</code></pre>

Utilizando estos puntos, la cosa no queda tan mal:<figure id="attachment_1759" style="width: 603px" class="wp-caption aligncenter">

![](http://pybonacci.org/images/2013/08/chebyshev1.png)

Aun así, aún tenemos varios problemas:

  * El polinomio sigue oscilando, y esto puede no ser deseable.
  * No siempre podemos escoger los puntos como nosotros queramos.

Por tanto, desde ya vamos a abandonar la idea de usar polinomios y vamos a hablar de **trazadores** (_splines_ en inglés).

### Trazadores

Los [trazadores](http://es.wikipedia.org/wiki/Spline) o _splines_ no son más que curvas polinómicas _definidas a trozos_, normalmente de grado 3 (casi nunca mayor de 5). Al ser cada uno de los trozos de grado pequeño se evita el fenómeno de Runge, y si se «empalman» los trozos inteligentemente la curva resultante será suave (matemáticamente: diferenciable) hasta cierto punto. Cuando queremos una curva que pase por todos los puntos disponibles un trazador es justamente lo que necesitamos.

El trazador más elemental, el lineal (grado 1), se puede construir rápidamente en NumPy usando [`np.interp`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.interp.html). El más común, el trazador cúbico (grado 3) se puede construir con la clase [`scipy.interpolate.InterpolatedUnivariateSpline`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.InterpolatedUnivariateSpline.html). Si pasamos a esta clase un argumento `k` podemos especificar el grado del trazador (entre 1 y 5). Como ejemplo vamos a tomar los datos de la silueta del pato de Villafuerte [III].

<pre><code class="language-python">from scipy.interpolate import InterpolatedUnivariateSpline
# Pato
P = [(0.9, 1.3), (1.3, 1.5), (1.9, 1.8), (2.1,2.1), (2.6, 2.6), (3.0, 2.7),
     (3.9, 2.3), (4.4, 2.1), (4.8, 2.0), (5.0, 2.1), (6, 2.2), (7, 2.3),
     (8, 2.2), (9.1, 1.9), (10.5, 1.4), (11.2, 0.9), (11.6, 0.8), (12, 0.6),
     (12.6, 0.5), (13, 0.4), (13.2, 0.2)]
xi, yi = zip(*P)  # 21 puntos de interpolación
x = np.linspace(min(xi), max(xi), num=1001)  # Dominio
y1d = np.interp(x, xi, yi)
#y1d = InterpolatedUnivariateSpline(xi, yi, k=1)(x)  # Mismo resultado
ysp = InterpolatedUnivariateSpline(xi, yi)(x)  # Llamamos a la clase con x</code></pre>

**_Nota_**: ¿[Quieres saber el truco de `zip(*P)`](http://pybonacci.org/2013/08/15/ajuste-e-interpolacion-unidimensionales-basicos-en-python-con-scipy/#comment-509)? 😉

Y si representamos el resultado obtenemos esto:<figure id="attachment_1767" style="width: 375px" class="wp-caption aligncenter">

![](http://pybonacci.org/images/2013/08/trazadores.png)

**¿Alguien se anima a enviarnos una gráfica de cómo quedaría la interpolación si usásemos un polinomio de grado 20? 😉**

<!-- Ojalá en SciPy existiera la función spline de MATLAB http://www.mathworks.es/es/help/matlab/ref/spline.html pero claro, si no me contestan qué visión tienen para el paquete no sé por dónde tirar http://mail.scipy.org/pipermail/scipy-dev/2013-August/019087.html -->

En ocasiones, sin embargo, puede que no necesitemos un trazador que pase por todos los puntos, sino una curva o un modelo más sencillo que _aproxime_ una serie de puntos, tratando de cometer el mínimo error posible. Si quieres saber cómo hacer esto, ¡sigue leyendo!

## Ajuste de curvas

### Ajuste polinómico

El **ajuste** más básico en el que podemos pensar es el ajuste polinómico: buscamos un polinomio que aproxime los datos con el menor error posible. Para ello utilizaremos la función [`polynomial.polyfit` del paquete `polynomial` de NumPy](http://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.polynomial.polyfit.html).

_**Nota**_: La función <del><code>np.polyfit</code></del> es **diferente** a la que vamos a usar aquí y está **obsoleta**, aparte de que tiene el convenio contrario para los coeficientes. Se recomienda no usarla. Ya sé que la otra tiene un nombre un poco largo y que los ejemplos de la documentación tienen fallos, pero [es lo que hay](https://github.com/numpy/numpy/issues/3615).

Esta función recibe tres argumentos obligatorios:

  * una lista de coordenadas `x` de los puntos,
  * una lista de coordenadas `y` de los puntos, y
  * el grado `deg` del polinomio interpolante.

Vamos a ver un ejemplo real con el que me encontré hace unos meses: hallar la polar parabólica aproximada de un avión. Para ello podéis utilizar [estos datos](https://gist.github.com/Juanlu001/6240182).

La polar de un avión es la relación entre la sustentación y la resistencia aerodinámica del mismo. Su forma teórica es:

$\displaystyle C\_D = C\_{D0} + k C_L^2$

podríamos estar tentados de intentar un ajuste parabólico, pero vemos que en realidad no aparece término lineal. Si llamamos $y = C\_D$ y $x = C\_L^2$ tenemos:

$\displaystyle y = y_0 + k x$

con lo que podemos realizar un ajuste lineal. Por otro lado, tengo que descartar los puntos que están más allá de la condición de entrada en pérdida (después del máximo del coeficiente de sustentación), porque esos no cuadran con el modelo teórico. Este es el código:

<pre><code class="language-python">import numpy.polynomial as P
# Cargamos los datos
data = np.loadtxt("polar.dat")
_, C_L, C_D = data
# Descarto los datos que no me sirven
stall_idx = np.argmax(C_L)
y = C_D[:stall_idx + 1]
x = C_L[:stall_idx + 1] ** 2
# Ajuste lineal, devuelve los coeficientes en orden creciente
C_D0, k = P.polynomial.polyfit(x, y, deg=1)
print(C_D0, k)</code></pre>

Una vez hemos obtenido los dos coeficientes, no hay más que evaluar el polinomio en un cierto dominio usando la función [`polynomial.polyval`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.polynomial.polyval.html), que acepta como argumentos

  * el dominio donde queremos evaluar la función y
  * una lista de coeficientes de grado creciente, tal y como los devuelve polyfit.

El código es simplemente:

<pre><code class="language-python">C_L_dom = np.linspace(C_L[0], C_L[stall_idx], num=1001)
C_D_int = P.polynomial.polyval(C_L_dom ** 2, (C_D0, k))</code></pre>

Y este es el resultado que obtenemos:<figure id="attachment_1776" style="width: 407px" class="wp-caption aligncenter">

![](http://pybonacci.org/images/2013/08/polar.png)

En la figura se aprecia perfectamente cómo he descartado los puntos más allá del máximo y cómo la parábola, aun no pasando por todos los puntos (tal vez no pase por ninguno) aproxima bastante bien los datos que tenemos. ¡Bien!

### General

En ocasiones las cosas son más complicadas que un polinomio (sí lectores, así es la vida). Pero no pasa nada, porque con la función [`scipy.optimize.curve_fit`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) podemos ajustar una serie de datos a cualquier modelo que se nos ocurra, no importa qué tan complicado sea. Sin ir más lejos, tomando el ejemplo de la documentación, supongamos que tenemos unos datos que se ajustan al modelo

$\displaystyle A e^{-B x^2} + C$

en Python nuestro modelo será una función que recibirá como primer argumento x y el resto serán los parámetros del mismo:

<pre><code class="language-python">def func(x, A, B, C):
    """Modelo para nuestros datos."""
    return A * np.exp(-B * x ** 2) + C</code></pre>

Ahora solo necesitamos algunos datos (añadiremos un poco de ruido gaussiano para que tenga más gracia) y podemos probar el ajuste. La función `scipy.optimize.curve_fit` recibe como argumentos:

  * el modelo `func` para los datos,
  * una lista de coordenadas `xdata` de los puntos, y
  * una lista de coordenadas `ydata` de los puntos.

Así realizamos el ajuste:

<pre><code class="language-python">from scipy.optimize import curve_fit
Adat, Bdat, Cdat = 2.5, 1.3, 0.5
xdat = np.linspace(-2, 4, 12)
ydat = func(xdat, Adat, Bdat, Cdat) + 0.2 * np.random.normal(size=len(xdat))
(A, B, C), _ = curve_fit(func, xdat, ydat)
print(A, B, C)</code></pre>

Y el resultado queda así:<figure id="attachment_1779" style="width: 372px" class="wp-caption aligncenter">

![](http://pybonacci.org/images/2013/08/curve_fit.png)

Fácil, ¿no?

### Mínimos cuadrados

Todas estas funciones emplean la solución por mínimos cuadrados de un sistema lineal. Nosotros podemos acceder a esta solución utilizando la función [scipy.optimize.leastsq](http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html), pero como es más general y este artículo ya se ha extendido bastante lo vamos a dejar aquí, de momento 😉

**Y tú, ¿te animas ya a realizar ajustes e interpolaciones con Python? ¿Qué dificultades ves? ¿Cómo piensas que podríamos mejorar el artículo? ¡Cuéntanoslo en los comentarios! 🙂**

## Referencias

  1. RIVAS, Damián; VÁZQUEZ, Carlos. _Elementos de Cálculo Numérico_. ADI, 2010.
  2. BERRUT, Jean-Paul; TREFETHEN, Lloyd N. _Barycentric lagrange interpolation_. _Siam Review_, 2004, vol. 46, no 3, p. 501-517.
  3. VILLAFUERTE, Héctor F. _Guías para Métodos Numéricos, parte 2_ [en línea]. 2010. Disponible en web: <<http://uvgmm2010.wordpress.com/guias/>>. [Consulta: 15 de agosto de 2013]