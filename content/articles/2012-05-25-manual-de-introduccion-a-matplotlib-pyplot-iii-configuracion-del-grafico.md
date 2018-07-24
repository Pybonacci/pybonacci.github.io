---
title: Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico
date: 2012-05-25T20:38:56+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico
tags: gráficos, matplotlib, matplotlib.pyplot, pyplot, python, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. **[Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")**
  4. [Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. [Tipos de gráfico III](http://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. [Tipos de gráfico IV](http://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")
  8. [Texto y anotaciones (arrow, annotate, table, text...)](http://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")
  9. <del>Herramientas estadísticas (acorr, cohere, csd, psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. [Miscelánea](http://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y matplotlib 1.1.0]**

[DISCLAIMER: Muchos de los gráficos que vamos a representar no tienen ningún sentido físico y los resultados solo pretenden mostrar el uso de la librería].

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

    :::python
    import matplotlib.pyplot as plt
    import numpy as np

Hasta ahora hemos visto como podemos configurar la ventana y la sesión, en esta ocasión nos vamos a centrar en configurar el área del gráfico. Para ello vamos a empezar con plt.axes(), que sirve para 'llamar' y/o configurar a un área de gráfico. Podemos definir la posición, el tamaño, el color del área del fondo,...:

    :::python
    plt.ion()  # Ponemos la sesión como interactiva si no está como tal
    plt.axes()  # Coloca un área de gráfico con los valores por defecto
    plt.plot(np.exp(np.linspace(0,10,100)))  # Dibuja una exponencial de 0 a 10
    plt.axes([0.2,0.55,0.3,0.3], axisbg = 'gray')  # Dibuja una nueva área de gráfica colocada y con ancho y largo definido por [0.2,0.55,0.3,0.3] y con gris como color de fondo
    plt.plot(np.sin(np.linspace(0,10,100)), 'b-o', linewidth = 2)

El resultado es el siguiente:

[<img class="aligncenter size-full wp-image-441" title="axesmultiples" alt="" src="http://new.pybonacci.org/images/2012/05/axesmultiples.png" height="553" width="652" srcset="https://pybonacci.org/wp-content/uploads/2012/05/axesmultiples.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/axesmultiples-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/05/axesmultiples.png)

Como podéis imaginar, podemos usar plt.axes() como sustituto de plt.subplot() si queremos dibujar gráficos que no tengan que tener una forma 'regular' dentro de la ventana. Si ahora queremos borrar el área del gráfico podemos usar plt.delaxes(), si queremos borrar el contenido que hay en el área del gráfico podemos usar plt.cla() y si queremos que no aparezca la 'caja' donde se dibuja el gráfico podemos usar plt.box() (si no hay 'caja' y queremos que aparezca podemos llamar a plt.box() y volverá a aparecer la 'caja').

[<img class="alignnone size-medium wp-image-443" title="concaja" alt="" src="http://new.pybonacci.org/images/2012/05/concaja.png?w=300" height="254" width="300" srcset="https://pybonacci.org/wp-content/uploads/2012/05/concaja.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/concaja-300x254.png 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://new.pybonacci.org/images/2012/05/concaja.png)[<img class="alignnone size-medium wp-image-444" title="sincaja" alt="" src="http://new.pybonacci.org/images/2012/05/sincaja.png?w=300" height="254" width="300" srcset="https://pybonacci.org/wp-content/uploads/2012/05/sincaja.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/sincaja-300x254.png 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://new.pybonacci.org/images/2012/05/sincaja.png)

El área del gráfico puede ser un área rectangular o un área para [un gráfico polar (ver ejemplo)](http://pybonacci.org/2012/03/24/dibujando-una-rosa-de-frecuencias/).

Podemos colocar una rejilla que nos ayude a identificar mejor las áreas del gráfico mediante plt.grid() (en un gráfico polar deberemos usar plt.rgrid() y plt.thetagrids()).

<!--more-->

Si os habéis fijado, matplotlib dibuja los ejes de forma que se ajusten al gráfico pero quizá eso no es lo que nos interese en algunos momentos, para ello podemos hacer uso de plt.axis(). Nos permite definir la longitud de los ejes, si queremos que aparezcan los mismos, si queremos que estos estén escalados,... Si solo nos interesa configurar uno de los ejes y dejar que el otro lo maneje matplotlib podemos usar plt.xlim(), plt.xscale(), plt.ylim() y plt.yscale(). Si queremos dejar el eje x o el eje y con escala logarítmica podemos usar, respectivamente, plt.semilogx() o plt.semilogy(). Podemos dibujar un segundo eje x o un segundo eje y usando plt.twinx() o plt.twiny, respectivamente. También podemos establecer unos márgenes alrededor de los límites de los ejes usando plt.margins(). Por último, podemos etiquetar nuestros ejes con plt.xlabel() y plt.ylabel(). Veamos un ejemplo de algunas de estas cosas:

    :::python
    plt.ion()
    plt.plot(np.arange(100), 'b')  # Dibujamos una línea recta azul
    plt.xlabel('Valores de x')  # Ponemos etiqueta al eje x
    plt.ylabel(u'Línea azul')  # Ponemos etiqueta al eje y
    plt.twinx()  # Creamos un segundo eje y
    plt.plot(np.exp(np.linspace(0,5,100)), 'g')  # Dibuja una exponencial de 0 a 5 con la y representada en el segundo eje y
    plt.ylabel(u'Línea verde')  # Ponemos etiqueta al segundo eje y
    plt.xlim(-10,110)  # Limitamos los valores del eje x para que vayan desde -10 a 110

[<img class="aligncenter size-full wp-image-445" title="ejesydemas" alt="" src="http://new.pybonacci.org/images/2012/05/ejesydemas.png" height="553" width="652" srcset="https://pybonacci.org/wp-content/uploads/2012/05/ejesydemas.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/ejesydemas-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/05/ejesydemas.png)

Ahora vamos a ver plt.axvline(), plt.axvspan(), plt.axhline(), plt.axhspan(). ¿Y para qué sirven estas 'cosas'? Pensad que, por ejemplo, queréis resaltar una zona de vuestro gráfico para focalizar la atención en esa área. Eso lo podríamos hacer usando lo anterio. plt.axvline() y plt.axhline() dibujan líneas verticales y horizontales en la x o en la y que le digamos mientras que plt.axvspan y plt.axhspan dibujan recuadros entre las coordenadas x o y que queramos, respectivamente.

    :::python
    plt.ion()  # Ponemos el modo interactivo
    plt.scatter(np.random.randn(1000), np.random.randn(1000))  # Dibujamos un scatterplot de valores aleatorios
    plt.axvline(-0.5, color = 'g')  # Dibujamos una línea vertical verde centrada en x = -0.5
    plt.axvline(-0.5, color = 'g')  # Dibujamos una línea vertical verde centrada en x = 0.5
    plt.axhline(-0.5, color = 'g')  # Dibujamos una línea horizontal verde centrada en x = -0.5
    plt.axhline(-0.5, color = 'g')  # Dibujamos una línea horizontal verde centrada en x = 0.5
    plt.axvspan(-0.5,0.5, alpha = 0.25)  #  Dibujamos un recuadro azul vertical entre x[-0.5,0.5] con transparencia 0.25
    plt.axhspan(-0.5,0.5, alpha = 0.25)  #  Dibujamos un recuadro azul horizontal entre x[-0.5,0.5] con transparencia 0.25

[<img class="aligncenter size-full wp-image-451" title="vhlinevhspan" alt="" src="http://new.pybonacci.org/images/2012/05/vhlinevhspan.png" height="553" width="652" srcset="https://pybonacci.org/wp-content/uploads/2012/05/vhlinevhspan.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/vhlinevhspan-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/05/vhlinevhspan.png)

¿Y como podemos controlar el texto básico sobre el gráfico? Hay muchas formas de meter texto y controlar las etiquetas de forma básica y sencilla. En algunos momentos hemos visto plt.legend(), también existe plt.figlegend(). Yo siempre uso plt.legend() el 100% de las veces. Para usos avanzados podéis mirar [este enlace](http://stackoverflow.com/a/4701285) y [este otro enlace](http://matplotlib.sourceforge.net/users/legend_guide.html). Si queremos poner un título al gráfico podemos usar plt.title() y plt.suptitle(). Si queremos poner título a los ejes podemos usar plt.xlabel() y plt.ylabel() para los ejes x e y, respectivamente. Por último, para controlar los valores de las etiquetas que se ponen sobre los ejes dispones de plt.locator\_params(), plt.minorticks\_on(), plt.minorticks\_off(), plt.tick\_params(), plt.tick\_label\_format(), plt.xticks() y plt.yticks(). Vamos a manejar la mayor parte de estas funciones mediante un ejemplo para que se vea más claro su uso. Imaginemos que queremos representar el valor medio diario de una variable durante un año, en el eje x queremos que aparezca solo los meses en el día del año en que empieza el mes

    :::python
    plt.ion()  # Ponemos modo interactivo
    import calendar
    dias = [np.array(calendar.mdays)[0:i].sum() + 1 for i in np.arange(12)+1]  # Para generar el lugar del primer días de cada mes en un año
    meses = calendar.month_name[1:13]  # Creamos una lista con los nombres de los meses
    plt.axes([0.1,0.2,0.8,0.65])
    plt.plot(np.arange(1,366), np.random.rand(365), label = 'valores al azar')  # Creamos un plot con 365 valores
    plt.xlim(-5,370)  # Los valores del eje y variarán entre -5 y 370
    plt.ylim(0,1.2)  # Los valores del eje y variarán entre 0 y 1.2
    plt.legend()  # Creamos la caja con la leyenda
    plt.title(u'Ejemplo de título')  # Ponemos un título
    plt.suptitle(u'Ejemplo de título superior')  # Ponemos un título superior
    plt.minorticks_on()  # Pedimos que se vean subrrayas de división en los ejes
    plt.xticks(dias, meses, size = 'small', color = 'b', rotation = 45)  # Colocamos las etiquetas, meses, en las posiciones, dias, con color azul y rotadas 45º
    plt.xlabel(u't (días)')
    plt.ylabel('Media diaria')

Cuyo resultado será algo parecido a lo siguiente:

[<img class="aligncenter size-full wp-image-452" title="textobasico" alt="" src="http://new.pybonacci.org/images/2012/05/textobasico.png" height="553" width="652" srcset="https://pybonacci.org/wp-content/uploads/2012/05/textobasico.png 652w, https://pybonacci.org/wp-content/uploads/2012/05/textobasico-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/05/textobasico.png)

Y con esto hemos visto, más o menos, la forma básica de configurar los elementos del gráfico. Si no los habéis visto aún, podéis leer el [capítulo 1](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/) y el [capítulo 2](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/) de esta serie.

Si quieres puedes pasar a [la siguiente parte](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)").
