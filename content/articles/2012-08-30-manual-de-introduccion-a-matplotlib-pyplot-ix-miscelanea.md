---
title: Manual de introducción a matplotlib.pyplot (IX): Miscelánea
date: 2012-08-30T16:18:55+00:00
author: Kiko Correoso
slug: manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea
tags: matplotlib, matplotlib.pyplot, pyplot, tutorial matplotlib.pyplot

Esto pretende ser un tutorial del módulo pyplot de la librería matplotlib. El tutorial lo dividiremos de la siguiente forma (que podrá ir cambiando a medida que vayamos avanzando).

  1. [Primeros pasos](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos")
  2. [Creando ventanas, manejando ventanas y configurando la sesión](http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/ "Manual de introducción a matplotlib.pyplot (II): Creando y manejando ventanas y configurando la sesión")
  3. [Configuración del gráfico](http://pybonacci.org/2012/05/25/manual-de-introduccion-a-matplotlib-pyplot-iii-configuracion-del-grafico/ "Manual de introducción a matplotlib.pyplot (III): Configuración del gráfico")
  4. [Tipos de gráfico I](http://pybonacci.org/2012/06/04/manual-de-introduccion-a-matplotlib-pyplot-iv-tipos-de-grafico-i/ "Manual de introducción a matplotlib.pyplot (IV): Tipos de gráfico (I)")
  5. [Tipos de gráfico II](http://pybonacci.org/2012/06/23/manual-de-introduccion-a-matplotlib-pyplot-v-tipos-de-grafico-ii/ "Manual de introducción a matplotlib.pyplot (V): Tipos de gráfico (II)")
  6. [Tipos de gráfico III](http://pybonacci.org/2012/07/01/manual-de-introduccion-a-matplotlib-pyplot-vi-tipos-de-grafico-iii/ "Manual de introducción a matplotlib.pyplot (VI): Tipos de gráfico (III)")
  7. [Tipos de gráfico IV](http://pybonacci.org/2012/07/29/manual-de-introduccion-a-matplotlib-pyplot-vii-tipos-de-grafico-iv/ "Manual de introducción a matplotlib.pyplot (VII): Tipos de gráfico (IV)")
  8. [Texto y anotaciones (arrow, annotate, table, text...)](http://pybonacci.org/2012/08/24/manual-de-introduccion-a-matplotlib-pyplot-viii-texto-y-anotaciones/ "Manual de introducción a matplotlib.pyplot (VIII): Texto y anotaciones")
  9. <del>Herramientas estadísticas (acorr, cohere, csd, psd, specgram, spy, xcorr, ...)</del>
 10. <del>Eventos e interactividad (connect, disconnect, ginput, waitforbuttonpress...)</del>
 11. **[Miscelánea](http://pybonacci.org/2012/08/30/manual-de-introduccion-a-matplotlib-pyplot-ix-miscelanea/ "Manual de introducción a matplotlib.pyplot (IX): Miscelánea")**

**[Para este tutorial se ha usado python 2.7.1, ipython 0.11, numpy 1.6.1 y matplotlib 1.1.0 ]**

[DISCLAIMER: Muchos de los gráficos que vamos a representar no tienen ningún sentido físico y los resultados solo pretenden mostrar el uso de la librería].

En todo momento supondremos que se ha iniciado la sesión y se ha hecho

    :::python
    import matplotlib.pyplot as plt
    import numpy as np
    plt.ion()

Después de dar un repaso por toda la librería, obviando algunas funciones estadísticas y eventos, vamos a acabar este tutorial viendo algunas funciones que sirven para leer y guardar imágenes.

Imaginad que queréis usar una imagen de fondo, por ejemplo vuestro nombre, o las siglas de creative commons o una foto,..., en vuestros gráficos. Para el ejemplo que vamos a ver a continuación vamos a usar la imagen que está en [el siguiente enlace](https://upload.wikimedia.org/wikipedia/commons/9/94/Cc_large.png) como fondo (guárdala en local para poder leerla).

    :::python
    background = plt.imread('Cc.large.png')  # Leemos la imagen que queremos usar de fondo, lo que escribáis entre comillas es la ruta a la imagen
    x = np.arange(background.shape[1])  # Definimos valores de x
    y = np.random.rand(background.shape[0]) * background.shape[0]  # Definimos valores de y
    plt.plot(x, y)  # Dibujamos la serie
    plt.imshow(background, alpha = 0.25)  # Creamos el fondo con una transparencia del 0.10 (1 es opaco y 0 es transparente)

El resultado es el siguiente:

[<img class="aligncenter size-full wp-image-783" title="imagenconfondo" src="http://new.pybonacci.org/images/2012/08/imagenconfondo.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/08/imagenconfondo.png 652w, https://pybonacci.org/wp-content/uploads/2012/08/imagenconfondo-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/08/imagenconfondo.png)

Con [plt.imread](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.imread) lo que hacemos es leer una imagen y convertirla en un numpy array que más tarde podemos utilizar como queramos (en este caso, como fondo para la imagen). Con [plt.imshow](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.imshow) lo que hemos hecho es mostrar la imagen en pantalla. Por último, que sepáis que también existe [plt.imsave](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.imsave), que permite guardar un numpy array como una imagen.

<!--more-->

Por último, pero no por ello menos importante, quedaría el uso de [plt.savefig](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.savefig), que nos permite guardar cualquiera de las figuras que hemos ido creando a lo largo de todo el tutorial. Para el anterior caso, solo tenemos que añadir lo siguiente al código de más arriba:

    :::python
    plt.savefig('imagen_con_fondo_cc.png')

La función [plt.savefig](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.savefig) permite definir la resolución de la imagen, el formato de salida (por defecto, matplotlib solo permite los formatos png, eps, ps, png y svg, si queremos usar otros formatos haría falta instalar otras librerías ([o bibliotecas](https://twitter.com/Pybonacci/status/237517866646249472)) como [PIL](http://www.pythonware.com/products/pil/)), la orientación de la figura,...

Y esto es todo, de momento, espero que os haya resultado útil por lo menos alguna cosa. Lástima no disponer de más tiempo para poder ver todo lo anterior con más profundidad pero espero que, por lo menos, si no conocíais esta maravillosa librería/biblioteca 🙂 os haya servido para adentraros un poco en ella y poder profundizar más por vuestra cuenta.

He 'limpiado' y resumido [todo el tutorial en un documento pdf que podéis descargar a continuación](http://new.pybonacci.org/images/2012/08/tutorial-de-matplotlib-pyplotv0-1-201208311.pdf) (que, desgraciadamente, se ha convertido en un homenaje póstumo a [John D. Hunter, creador de Matplotlib y ](http://numfocus.org/johnhunter./)[recientemente fallecido](http://numfocus.org/johnhunter./) :-().

Hasta siempre, John.

P.D.: Por favor, si veis errores, conceptos erróneos o tenéis alguna crítica, podéis usar los comentarios para hacérnosla llegar y que la podamos corregir.
