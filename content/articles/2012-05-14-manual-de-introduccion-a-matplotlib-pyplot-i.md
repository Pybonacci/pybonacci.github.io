---
title: Manual de introducción a matplotlib.pyplot (I): Primeros pasos
date: 2012-05-14T20:31:00+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-i
tags: gráficos, matplotlib, matplotlib.pyplot, pyplot, python, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. **[Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")**
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. [Tipos de gráfico III](http://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. [Tipos de gráfico IV](http://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")
  8. [Texto y anotaciones (arrow, annotate, table, text...)](http://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")
  9. <del>Herramientas estadísticas (acorr, cohere, csd,  psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. [Miscelánea](http://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y matplotlib 1.1.0]**

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

<pre><code class="language-python">import matplotlib.pyplot as plt
import numpy as np</code></pre>

Para empezar diremos que hay tres formas de usar la librería Matplotlib:

  * La podemos usar desde python usando el módulo pylab. El módulo pylab pretende mostrar un entorno de trabajo parecido al de [matlab](http://guillemborrell.es/blog/carta-abierta-a-mathworks/) mezclando las librerías numpy y matplotlib. Es la forma menos pythónica de usar matplotlib y se obtiene usando

<pre><code class="language-python">from pylab import *</code></pre>

Normalmente solo se recomienda para hacer pruebas rápidas desde la línea de comandos.

  * Una segunda forma, que es la que veremos en este tutorial, es usando el módulo pyplot.

<pre><code class="language-python">import matplotlib.pyplot as plt</code></pre>

  * Por último, la forma más recomendable y pythónica, pero más compleja, sería usar matplotlib mediante la interfaz orientada a objetos. Cuando se programa con matplotlib, no mientras se trabaja interactivamente, esta es la forma que permite tener más control sobre el código. Quizá veamos esto en el futuro si alguno nos animamos/os animáis a escribir sobre ello.

Absolutamente todo lo que vamos a usar en este tutorial y que está relacionado con matplotlib.pyplot lo podréis encontrar documentado y detallado [aquí](http://matplotlib.sourceforge.net/api/pyplot_api.html#module-matplotlib.pyplot "Documentación oficial de matplotlib.pyplot (1.1.0)"). Como he comentado, todo lo que vamos a ver está en el anterior enlace, pero no todo lo que está en el anterior enlace lo vamos a ver. Por ejemplo, en el índice veréis que he tachado los puntos 9 y 10, las funciones estadísticas y las funciones que permiten meter algo de interactividad en los gráficos dentro de pyplot. Las funciones estadísticas incluidas son pocas, algunas son complejas y muy específicas y las veo poco coherentes como grupo dentro de pyplot, para ello ya tenemos scipy y estas funciones estarían mejor ahí para separar lo que es 'gráficar' ([en español de Sudámerica existe la palabra](http://buscon.rae.es/draeI/SrvltGUIBusUsual?TIPO_HTML=2&TIPO_BUS=3&LEMA=graficar)) de lo que es analizar datos. Para interactividad con los gráficos tenemos el módulo [matplotlib.widgets](http://matplotlib.sourceforge.net/api/widgets_api.html#module-matplotlib.widgets), muchísimo más completo.

<!--more-->

Para que quede claro desde un principio, las dos zonas principales donde se dibujaran cosas o sobre las que se interactuará serán:

  * figure, que es una instancia de [matplotlib.figure.Figure](http://matplotlib.sourceforge.net/api/figure_api.html#matplotlib.figure.Figure). Y es la ventana donde irá el o los gráficos en sí:

![Figure](http://pybonacci.org/images/2012/04/pantallazo-del-2012-04-23-213736.png)

  * axes, que es una instancia de [matplotlib.axes.Axes](http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes), que es el gráfico en sí donde se dibujará todo lo que le digamos y está localizada dentro de una figure.

![Axes](http://pybonacci.org/images/2012/04/pantallazo-del-2012-04-23-213814.png)

Para lo primero (figure) usaremos la palabra 'ventana' mientras que para lo segundo (axes) usaremos la palabra 'gráfico'.

Si quieres puedes pasar a la [siguiente sección](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/).