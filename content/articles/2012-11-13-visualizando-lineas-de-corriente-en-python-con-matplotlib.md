---
title: Visualizando líneas de corriente en Python con matplotlib
date: 2012-11-13T23:26:29+00:00
author: Juan Luis Cano
slug: visualizando-lineas-de-corriente-en-python-con-matplotlib
tags: matplotlib, python, python 3

## Introducción

Hoy vamos a ver cómo representar diagramas de corriente en Python usando matplotlib. Este tipo de diagramas aparecen en Mecánica de Fluidos para visualizar el movimiento del fluido que estamos estudiando.

Hace unos días nos hicimos eco en Pybonacci de que se había liberado matplotlib 1.2.0, que introducía entre otras cosas [soporte para Python 3](http://matplotlib.org/users/whats_new.html#streamplot) y [la nueva función `streamplot`](http://matplotlib.org/users/whats_new.html#streamplot):

<blockquote class="twitter-tweet" width="550">
  <p>
    Liberado matplotlib 1.2.0, con soporte para Python 3 (al fin) y muchas cosas nuevas más <a href="http://t.co/5Kg4hFm7">http://t.co/5Kg4hFm7</a> ¡Difusión!
  </p>
  
  <p>
    &mdash; Pybonacci (@Pybonacci) <a href="https://twitter.com/Pybonacci/statuses/266798396654882816">November 9, 2012</a>
  </p>
</blockquote>



Así que vamos a estrenar las entradas con Python 3.3 y matplotlib 1.2 con un bonito ejemplo de Aerodinámica básica 🙂 El ejemplo y las gráficas están basados en la página de la Wikipedia sobre [flujo potencial alrededor de un cilindro circular](http://en.wikipedia.org/wiki/Potential_flow_around_a_circular_cylinder).

_**En esta entrada se han usado python 3.3.0, numpy 1.7.0b2 y matplotlib 1.2.0.**_

<!--more-->

## Campo de velocidades

Supongamos que tenemos un cilindro circular y que queremos visualizar el flujo a su alrededor. Lejos del cilindro este es unidireccional y uniforme, y nos vamos a centrar en el caso de fluido potencial y sin vorticidad. Al final, lo que tendremos será un campo de velocidades del tipo

$\displaystyle \vec{v} = \vec{f}(\vec{r})$

donde $\vec{r}$ es el vector de posición del punto considerado, y con la función `streamplot` lo visualizaremos en el plano. Además, incluiremos una representación del coeficiente de presiones $c_p$.

Sin entrar en mucho detalle matemático, la función potencial $\phi$ que satisface este problema, siendo $\vec{v} = \nabla{\phi}$, es, en coordenadas polares centradas en el cilindro,

$\displaystyle \phi(r, \theta) = U \left( r + \frac{R^2}{r} \right) \cos{\theta}$.

Por otro lado, la función de corriente $psi$ será

$\displaystyle \psi(r, \theta) = U \left( r - \frac{R^2}{r} \right) \sin{\theta}$

y el coeficiente de presiones $c_p$ será

$\displaystyle c_p = 2 \frac{R^2}{r^2} \cos(2 \theta) - \frac{R^4}{r^4}$.

El campo de velocidades se obtendrá derivando el potencial, de forma que será

$\displaystyle v_r = \frac{\partial \phi}{\partial r} = U\left(1-\frac{R^2}{r^2}\right)\cos\theta$
  
$\displaystyle v_{\theta} = \frac{1}{r}\frac{\partial \phi}{\partial \theta} = - U\left(1+\frac{R^2}{r^2}\right)\sin\theta$.

Vamos a ver cómo trasladamos todo esto a código Python.

## Código Python

Para nuestro problema concreto vamos a asumir $R = U_{\infty} = 1$ y que nuestro dominio bidimensional es un cuadrado cuya diagonal va de $(-3, -3)$ a $(3, 3)$.

La función [`streamplot`](http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.streamplot) recibe como mínimo cuatro argumentos:

  * Dos arrays `x` e `y`, que representan el plano, y
  * dos arrays `v_x` y `v_y`, que son las componentes del campo de velocidades según `x` e `y`.

Como vemos, `streamplot` asume que vamos a dar el campo de velocidades en coordenadas rectangulares, así que tenemos que trabajar un poco. En primer lugar generamos el dominio plano utilizando la función `meshgrid`, que ya vimos en nuestro [artículo sobre líneas de nivel en Python](http://pybonacci.org/2012/04/13/dibujando-lineas-de-nivel-en-python-con-matplotlib/ "Dibujando líneas de nivel en Python con matplotlib"):

    :::python
    x = np.linspace(-3, 3, 151)
    y = np.linspace(-3, 3, 151)
    xx, yy = np.meshgrid(x, y)

Ahora lo tenemos que transformar a coordenadas polares, y vamos a tener la precacución de enmascarar la parte central del dominio para evitar singularidades. Ya empleamos los arrays enmascarados en nuestro [artículo sobre estadística en Python con SciPy](http://pybonacci.org/2012/04/21/estadistica-en-python-con-scipy/ "Estadística en Python con SciPy (I)"):

    :::python
    rr = np.sqrt(xx ** 2 + yy ** 2)
    tt = np.arctan2(yy, xx)
    # Enmascaramos el centro para evitar singularidades
    rr = ma.masked_less_equal(rr, R * 0.9)

Ahora ya podemos calcular nuestras funciones potencial y de corriente, nuestro coeficiente de presiones y nuestras velocidades:

    :::python
    # Función potencial
    phi = U * (rr + R ** 2 / rr) * np.cos(tt)
    # Función de corriente
    psi = U * (rr - R ** 2 / rr) * np.sin(tt)
    # Coeficiente de presiones
    c_p = 2 * R ** 2 / rr ** 2 * np.cos(2 * tt) - R ** 4 / rr ** 4
    # Velocidad (polares)
    v_r = U * (1 - R ** 2 / rr ** 2) * np.cos(tt)
    v_theta = -U * (1 + R ** 2 / rr ** 2) * np.sin(tt)
    # Velocidad (rectangulares)
    v_x = v_r * np.cos(tt) - v_theta * np.sin(tt)
    v_y = v_r * np.sin(tt) + v_theta * np.cos(tt)

Para la gráfica vamos a combinar la función `streamplot` para representar las líneas de corriente con la función `contourf`, que también mencionamos en nuestro artículo sobre [líneas de nivel](http://pybonacci.org/2012/04/13/dibujando-lineas-de-nivel-en-python-con-matplotlib/ "Dibujando líneas de nivel en Python con matplotlib"), para representar el coeficiente de presiones en nuestro dominio:

    :::python
    # Creamos la figura
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Cilindro
    c = Circle((0, 0), R, color='#bbbbbb', linewidth=0, zorder=10)
    ax.add_patch(c)
    # Líneas de corriente
    ax.streamplot(xx, yy, v_x, v_y, linewidth=0.8, color='k')
    # Representación del coeficiente de presiones
    cs = ax.contourf(xx, yy, c_p, np.linspace(-3, 1, 1000), cmap=cm.GnBu)
    cb = fig.colorbar(cs, ticks=(-3 + np.arange(5)))

El código completo lo puedes ver [a través de nbviewer](http://nbviewer.ipython.org/4046447/) y este es el resultado:<figure id="attachment_1219" style="width: 560px" class="wp-caption aligncenter">

![Líneas de corriente](http://pybonacci.org/images/2012/11/lineas-corriente1.png)

Como ves, la única diferencia que hay en el código respecto a lo que habríamos escrito en Python 2.x es que no hace falta especificar que las cadenas contienen Unicode, [porque este es ya el tipo por defecto](http://docs.python.org/3.0/whatsnew/3.0.html#text-vs-data-instead-of-unicode-vs-8-bit).

Quisiera dedicar esta no demasiado lúcida entrada a todos mis compañeros aeronáuticos, a quienes se les echa mucho de menos desde la distancia 🙂

¡Un saludo!