---
title: Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión
date: 2012-05-19T20:31:43+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion
tags: gráficos, matplotlib, matplotlib.pyplot, pyplot, python, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](https://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. **[Creando ventanas, manejando ventanas y configurando la sesión](https://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")**
  3. [Configuración del gráfico](https://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](https://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](https://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. [Tipos de gráfico III](https://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. [Tipos de gráfico IV](https://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")
  8. [Texto y anotaciones (arrow, annotate, table, text...)](https://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")
  9. <del>Herramientas estadísticas (acorr, cohere, csd, psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. [Miscelánea](https://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y matplotlib 1.1.0]**

[DISCLAIMER: Muchos de los gráficos que vamos a representar no tienen ningún sentido físico y los resultados solo pretenden mostrar el uso de la librería].

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

    :::python
    import matplotlib.pyplot as plt
    import numpy as np

Como ya comentamos anteriormente, el módulo pyplot de matplotlib se suele usar para hacer pruebas rápidas desde la línea de comandos, programitas cortos o programas donde los gráficos serán, en general, sencillos.

Normalmente, cuando iniciamos la sesión, esta no está puesta en modo interactivo. En modo interactivo, cada vez que metemos código nuevo relacionado con el gráfico o la ventana (recordad, una instancia de [matplotlib.axes.Axes](http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes) o de [matplotlib.figure.Figure](http://matplotlib.sourceforge.net/api/figure_api.html#matplotlib.figure.Figure), respectivamente), este se actualizará. Cuando no estamos en modo interactivo, el gráfico no se actualiza hasta que llamemos a show() (si no hay una ventana abierta) o draw() (normalmente no lo usaréis para nada) explícitamente. Veamos como es esto:

Si acabamos de iniciar sesión deberíamos estar en modo no interactivo. Para comprobarlo hacemos lo siguiente:

    :::python
    plt.isinteractive()
    False

Si el resultado es _False_ significa que estamos en modo no interactivo. Esto significa que si hacemos lo siguiente:

    :::python
    plt.plot([1,2,3,4,5])

No lanzará una ventana hasta que lo pidamos explícitamente mediante:

    :::python
    plt.show()

Podemos conmutar a modo interactivo o no usando plt.ion() y plt.ioff(), que lo que hacen es poner el modo interactivo en 'on' o en 'off', respectivamente. Como está en off (recordad que plt.isinteractive() nos ha dado _False_, lo que significa que está en 'off'), si ahora  hacemos lo siguiente (cerrad antes cualquier ventana de gráficos que tengáis abierta):

    :::python
    plt.ion()
    plt.plot([1,2,3,4])

Vemos que directamente se abre una ventana nueva sin necesidad de llamar a plt.show(). Yo suelo usar ipython así para ir probando cosas y cuando ya acierto con como quiero que me salgan los gráficos voy a spyder, donde tengo el programa que esté haciendo, y ya escribo el código que necesito con la interfaz orientada a objetos.

Jugad un poco con plt.isinteractive(), plt.ion(), plt.ioff(), plt.show() y plt.draw() para estar más familiarizados con el funcionamiento.

<!--more-->

Lo siguiente que veremos es plt.hold() y plt.ishold(). plt.hold es un conmutador para decir si queremos que los gráficos se sobreescriban, que en el mismo gráfico tengamos diferentes gráficas representadas, o para que el gráfico se limpie y se dibuje la nueva gráfica cada vez. Si usamos plt.ishold() nos 'responderá' _True_ o _False_. Si acabáis de iniciar sesión, normalmente estará en _True_.

    :::python
    plt.ishold()
    True

Como está en _True_, si hacemos lo siguiente:

    :::python
    plt.plot(np.random.rand(10))
    plt.plot(np.random.rand(10))
    plt.show()

Obtendremos lo siguiente:
  
![plt.ishold](https://pybonacci.org/images/2012/05/captura-de-pantalla-de-2012-05-12-164745.png)
  
Si el modo 'hold' estuviera en _False_, solo se habría conservado el último plot y solo veríamos una línea de las dos (probadlo usando plt.hold() y plt.ishold()).

Si estamos en modo interactivo (plt.ion()) y queremos borrar todos los gráficos ([matplotlib.axes.Axes](http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes)), títulos, ..., de la ventana ([matplotlib.figure.Figure](http://matplotlib.sourceforge.net/api/figure_api.html#matplotlib.figure.Figure)) podemos usar plt.clf() y nos volverá a dejar el 'lienzo' limpio.

Si seguimos en modo interactivo (plt.ion()) y queremos cerrar la ventana podemos usar plt.close().

Imaginaos que ahora queréis trabajar con varias ventanas de gráficos simultáneamente donde en una dibujáis unos datos y en la otra otro tipo de datos y los queréis ver simultáneamente. Podemos hacer esto dándole nombre (o número) a las ventanas con las que vamos a trabajar. Veamos un ejemplo:

    :::python
    plt.figure('scatter') # Crea una ventana titulada 'scatter'
    plt.figure('plot')    # Crea una ventana titulada 'plot'
    a = np.random.rand(100) # Generamos un vector de valores aleatorios
    b = np.random.rand(100) # Generamos otro vector de valores aleatorios
    plt.figure('scatter') # Le decimos que la ventana activa en la que vamos a dibujar es la ventana 'scatter'
    plt.scatter(a,b)  # Dibujamos un scatterplot en la ventana 'scatter'
    plt.figure('plot') # Ahora cambiamos a la ventana 'plot'
    plt.plot(a,b)

Y os quedaría algo como lo siguiente:
  
![figure-scatter](https://pybonacci.org/images/2012/05/figure-scatter.png?w=300)

Es decir, podemos ir dibujando en varias ventanas a la vez. Podéis probar a cerrar una de las dos ventanas, limpiar la otra, crear una nueva,... Haciendo una llamada a plt.figure() también podemos definir la resolución del gráfico, el tamaño de la figura,...

Pero yo no quiero dibujar los gráficos en dos ventanas, yo quiero tener varios gráficos en la misma. Perfecto, también podemos hacer eso sin problemas con la ayuda de plt.subplot(). Con plt.subplot() podemos indicar el número de filas y columnas que corresponderán a como dividimos la ventana. En el siguiente ejemplo se puede ver dos áreas de gráfico en la misma ventana:

    :::python
    plt.ion()  # Nos ponemos en modo interactivo
    plt.subplot(1,2,1)  # Dividimos la ventana en una fila y dos columnas y dibujamos el primer gráfico
    plt.plot((1,2,3,4,5))
    plt.subplot(1,2,2)  # Dividimos la ventana en una fila y dos columnas y dibujamos el segundo gráfico
    plt.plot((5,4,3,2,1))

Obteniendo el siguiente gráfico:

![subplot12](https://pybonacci.org/images/2012/05/subplot12.png)

Os dejo como ejercicio ver cómo podéis conseguir la siguiente gráfica (si no sabéis como dejad un comentario) y con ello creo que habréis entendido perfectamente el uso de plt.subplot():

![subplot22](https://pybonacci.org/images/2012/05/subplot22.png)

Por último, vamos a ver como configurar la sesión para ahorrarnos escribir código de más. Por ejemplo, imaginaos que queréis que todas las líneas sean más gruesas por defecto porque os gustan más así, que queréis usar otro tipo de fuente sin escribirlo explícitamente cada vez que hacéis un gráfico, que los gráficos se guarden siempre con una resolución superior a la que viene por defecto,... Para ello podéis usar plt.rc(), plt.rcParams, plt.rcdefaults(). En este caso vamos a usar plt.rc(), podréis encontrar más información sobre como configurar matplotlib [en este enlace](http://matplotlib.sourceforge.net/users/customizing.html). Veamos un ejemplo para ver como funciona todo esto:

    :::python
    plt.ion()  # Nos ponemos en modo interactivo
    plt.figure('valores por defecto')  # Creamos una ventana donde dibujamos el gráfico con la configuración por defecto
    plt.suptitle('Titulo valores por defecto')  # Esto sirve para poner título dentro de la ventana
    plt.plot((1,2,3,4,5), label = 'por defecto')  # Hacemos el plot
    plt.legend(loc = 2)  # Colocamos la leyenda en la esquina superior izquierda
    plt.rc('lines', linewidth = 2)  # A partir de aquí todas las líneas que dibujemos irán con ancho doble
    plt.rc('font', size = 18)  # A partir de aquí las fuentes que aparezcan en cualquier gráfico en la misma sesión tendrán mayor tamaño
    plt.figure('valores modificados')  # Creamos una ventana donde dibujamos el gráfico con la configuración por defecto
    plt.suptitle('Titulo valores modificados')  # Esto sirve para poner título dentro de la ventana
    plt.plot((1,2,3,4,5), label = u'linea más ancha y letra más grande')  # Hacemos el plot
    plt.legend(loc = 2)  # Colocamos la leyenda en la esquina superior izquierda

![plot-defecto](https://pybonacci.org/images/2012/05/plot-defecto.png?w=300)

Después de usar plt.rc() para modificar un parámetro esa modificación será para toda la sesión a no ser que lo volvamos a modificar explícitamente o a no ser que usemos plt.rcdefaults(), que devolverá todos los parámetros a los valores por defecto.

Si no has visto el primer capítulo de esta serie [échale un ojo ahora](http://www.pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/) o, si prefieres, puedes pasar a la [siguiente parte](https://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/).
