---
title: Creando una animación con matplotlib y ffmpeg
date: 2012-12-16T12:27:36+00:00
author: Kiko Correoso
slug: creando-una-animacion-con-matplotlib-y-ffmpeg
tags: animación, ffmpeg, ipynb2wp, matplotlib, matplotlib.animation, video

En esta nueva entrada vamos a ver una revisión rápida al [módulo animation en matplotlib](http://matplotlib.org/api/animation_api.html), disponible desde la versión 1.1 de matplotlib.

**[Para esta entrada se ha usado matplotlib 1.1.1, numpy 1.6.1, ipython 0.13 sobre python 2.7.3 y [ffmpeg](http://ffmpeg.org/) como librería externa que usará matplotlib para crear el video de la animación (aunque también puede usar [mencoder](http://www.mplayerhq.hu/design7/news.html))] todo ello corriendo en linux. Puede que los usuarios de windows tengan problemas al guardar el video si ffmpeg no está instalado y/o correctamente configurado para que [matplotlib pueda trabajar con ffmpeg](https://github.com/matplotlib/matplotlib/issues/760).**

Hay varias formas de hacer una animación usando [FuncAnimation](http://matplotlib.org/api/animation_api.html#matplotlib.animation.FuncAnimation), [ArtistAnimation](http://matplotlib.org/api/animation_api.html#matplotlib.animation.ArtistAnimation) y/o [TimedAnimation](http://matplotlib.org/api/animation_api.html#matplotlib.animation.TimedAnimation). Las dos primeras formas son clases que heredan de la tercera mientras que la tercera hereda de la clase base [Animation](http://matplotlib.org/api/animation_api.html#matplotlib.animation.Animation).

Para este ejemplo de como hacer una animación con matplotlib y ffmpeg vamos a usar _`FuncAnimation`_ y vamos a representar la evolución de un [atractor de Lorenz](http://en.wikipedia.org/wiki/Lorenz_system) en 3D.

<!--more-->

Como siempre, primero importamos todo lo necesario:

<pre><code class="language-python">import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
from scipy.integrate import odeint</code></pre>

Ahora inicializamos la figura que se usará en la animación.

<pre><code class="language-python">fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = Axes3D(fig)
ax.azim = 45
ax.elev = 45
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')
ax.set_xticklabels('')
ax.set_yticklabels('')
ax.set_zticklabels('')
linea, = ax.plot([], [], [], label = 'Lorenz', lw = 0.5)
ax.legend()
ax.set_xlim(-20,20)
ax.set_ylim(-30,30)
ax.set_zlim(0,50)</code></pre>

La salida del anterior código mostrará:
  
![](http://new.pybonacci.org/images/2012/12/wpid-creando_una_animacic3b3n_con_matplotlib_y_ffmpeg0.png)

El cálculo de los parámetros del atractor de Lorenz los realiza la función _`integra`_ que podéis ver a continuación:

<pre><code class="language-python">def integra(ccii, t):
    x = ccii[0]            ## Posición inicial
    y = ccii[1]            ## Posición inicial
    z = ccii[2]            ## Posición inicial
    sigma = 10             ## Parámetros que se pueden ver en:
    rho = 28               ## http://en.wikipedia.org/wiki/Lorenz_system
    beta = 8.0/3           ##
    dx = sigma * (y - x)   ## Sistema de ecuaciones
    dy = x * (rho -z) - y  ## diferenciales de
    dz = x * y - beta* z   ## Lorenz
    return [dx, dy, dz]</code></pre>

FuncAnimation puede usar una función inicializadora, que es la que crearía el 'frame' o fotograma inicial. En el presente caso no usaremos una función inicializadora puesto que normalmente no he visto que sea muy necesario (puede que esté equivocado).

Además de la función inicializadora, _`FuncAnimation`_ necesitará otra función que es la que realiza la animación en sí y que llamaremos, en este caso, _`anima`_.

<pre><code class="language-python">def anima(i, x0, y0, z0):
    t = np.arange(0, (i + 1) / 10., 0.01) ## Paso temporal
    ccii = [x0, y0, z0]                   ## Posición inicial
    ## Integración de las
    ## ecs. de Lorenz mediante
    ## scipy.integrate.odeint
    ## http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
    ## odeint usa la función integra
    ## que hemos creado anteriormente
    ## con las condiciones iniciales (ccii)
    ## y los pasos temporales (t)
    soluc = odeint(integra, ccii, t)
    x = soluc[:,0]                        ## Posición x
    y = soluc[:,1]                        ## Posición y
    z = soluc[:,2]                        ## Posición z
    ax.elev = 45 + i / 2.                 ## Vamos rotando el
    ax.azim = 45 + i / 2.                 ## punto de vista
    linea.set_data(x, y)                  ## Asignamos datos para ir
    linea.set_3d_properties(z)            ## dibujando la trayectoria
    return linea,</code></pre>

Por último, nos faltaría crear la animación en sí. Eso lo conseguiremos usando el código de más abajo. A la clase _`FuncAnimation`_ le pasaremos una serie de parámetros. El primero será _`fig`_, que hemos creado anteriormente. Después hemos puesto la función que realiza la animación, en nuestro caso se llama _`anima`_ y ha sido definida en la anterior pieza de código. Después se le pasa el número de _`frames`_ que se va a usar. Este número de frames es el parámetro _`i`_ que recibe la función _`anima`_. El siguiente parámetro se llama _`fargs`_. que son los argumentos restantes que le pasamos a la función _`anima`_, en este caso _`(0, 1, 1.05)`_ son los valores para _`x0`_, _`y0`_, _`z0`_ en la función _`anima`_. Lo siguiente que aparece es el parámetro _`interval`_ que indica el intervalo entre frames en milisegundos y por último hemos puesto _`blit = True`_ que indica que la imagen no se recalcula entera sino que simplemente se actualizan las partes nuevas obtenidas en cada nuevo frame. Esto último permite que sea más rápido.

<pre><code class="language-python">anim = animation.FuncAnimation(fig, anima, frames = 500, fargs = (0, 1, 1.05),
                               interval = 5, blit = True)</code></pre>

Por último nos quedaría guardar el resultado. El siguiente código creara una serie de imágenes temporales que después usará `ffmpeg` para crear el video y que se eliminarán posteriormente. Aparecerán tantas imágenes como 'frames' o fotogramas hayamos puesto en el código anterior. Tened esto en cuenta si tenéis poco espacio en disco. En nuestro caso, el vídeo se llama **'Atractor\_de\_Lorenz(pybonacci).mp4'**.

<pre><code class="language-python">anim.save('Atractor_de_Lorenz(pybonacci).mp4', fps = 10)</code></pre>

Et voilà. Lo anterior, si no hay ningún error, nos daría el siguiente video que hemos subido previamente a youtube. En el vídeo subido aparecen las etiquetas de los ejes que en el código de este artículo he eliminado porque creo que os quedará más limpia la animación. Si queréis poner las etiquetas de valores de los ejes solo debéis eliminar las líneas de más arriba (segunda pieza de código) que contienen _`ax.set_(xyz)ticklabels('')`_.

<pre><code class="language-python">from IPython.display import YouTubeVideo
YouTubeVideo('bFfCG-N8R8E')</code></pre>

La salida del anterior código mostrará:
  
[youtube=http://www.youtube.com/watch?v=bFfCG-N8R8E]

Enlaces interesantes y referencias usadas para hacer esta entrada:

-[Ejemplos en el excelente blog de Jave Vanderplas.](http://jakevdp.github.com/blog/2012/08/18/matplotlib-animation-tutorial/)

-[Ejemplos de animaciones en matplotlib.org.](http://matplotlib.org/examples/animation/index.html)

-[Documentación oficial de matplotlib.animation para la última versión de matplotlib.](http://matplotlib.org/api/animation_api.html)

-[Recetario de animaciones en scipy.org.](http://www.scipy.org/Cookbook/Matplotlib/Animations) Son algo viejunas y no usan lo más moderno que matplotlib ofrece pero os puede valer para ver formas alternativas de hacer animaciones.

-[Ejemplo de código que he tomado como base para el atractor de Lorenz.](http://titanlab.org/2010/04/08/lorenz-attractor/)

-[El pedazo de cheat sheet sobre markdown que se ha currado Joe di Castro](http://joedicastro.com/pages/markdown.html) y que uso como referencia para escribir el Markdown en el ipynb.

Saludos a todos.

P.D.: glfo, va por tí, a ver si usas este artículo y me enseñas eso que tienes en mente, además de dejar de dar la brasa por el communicator. Ahora ya no tienes excusa 😉

##### _This post has been published on wordpress.com from an ipython notebook using [ipynb2wp](https://github.com/kikocorreoso/ipynb2wp)_