---
title: La importancia de inspeccionar los datos
date: 2012-10-05T19:43:39+00:00
author: Kiko Correoso
slug: la-importancia-de-inspeccionar-los-datos
tags: Charlas Ted, Estadística, Francis Anscombe, Hans Rosling, representación, Ted, Ted talks, video, visualización

Muchas veces, cuando analizo datos, se me cuelan datos erróneos que me llevan a dolores de cabeza posteriores. Para evitar o minimizar esto, una buena práctica consiste en realizar una representación previa de esos datos para ver si los resultados posteriores son coherentes. Un buen ejercicio para entender la importancia de esto es echarle un ojo al [cuartero de Anscombe](http://es.wikipedia.org/wiki/Cuarteto_de_Anscombe). En el siguiente script se representa el cuarteto de Anscombe y sus principales estadísticos:

<pre><code class="language-python">import numpy as np
import matplotlib.pyplot as plt
plt.ion()
ans_x_I = np.array([10.0, 8.0, 13.0, 9.0, 11.0,
                    14.0, 6.0, 4.0, 12.0, 7.0, 5.0])
ans_y_I = np.array([8.04, 6.95, 7.58, 8.81, 8.33,
                    9.96, 7.24, 4.26, 10.84, 4.82, 5.68])
ans_x_II = np.array([10.0, 8.0, 13.0, 9.0, 11.0,
                     14.0, 6.0, 4.0, 12.0, 7.0, 5.0])
ans_y_II = np.array([9.14, 8.14, 8.74, 8.77, 9.26,
                     8.10, 6.13, 3.10, 9.13, 7.26, 4.74])
ans_x_III = np.array([10.0, 8.0, 13.0, 9.0, 11.0,
                      14.0, 6.0, 4.0, 12.0, 7.0, 5.0])
ans_y_III = np.array([7.46, 6.77, 12.74, 7.11, 7.81,
                      8.84, 6.08, 5.39, 8.15, 6.42, 5.73])
ans_x_IV = np.array([8.0, 8.0, 8.0, 8.0, 8.0,
                     8.0, 8.0, 19.0, 8.0, 8.0, 8.0])
ans_y_IV = np.array([6.58, 5.76, 7.71, 8.84, 8.47,
                     7.04, 5.25, 12.50, 5.56, 7.91, 6.89])
x = [ans_x_I, ans_x_II, ans_x_III, ans_x_IV]
y = [ans_y_I, ans_y_II, ans_y_III, ans_y_IV]
def pinta(x, y, grupo, pos):
    plt.subplot(pos)
    minimo = np.min([x, y])
    maximo = np.max([x, y])
    plt.xlim(minimo - 1, maximo + 1)
    plt.ylim(minimo - 1, maximo + 1)
    plt.plot(x[grupo], y[grupo], 'yo')
    a1, a0 = np.polyfit(x[grupo], y[grupo], 1)
    plt.plot(x[grupo], a0 + a1 * x[grupo], 'b')
    plt.text(minimo, maximo - 0.5, 'y=%5.3f+%5.3fx' % (a0, a1))
    plt.text(minimo, maximo - 2.0, 'r=%5.3f' % np.corrcoef(x[grupo], y[grupo])[0,1])
    plt.text(minimo, maximo - 3.5, 'x media=%5.3f' % np.mean(x[grupo]))
    plt.text(minimo, maximo - 5, 'y media=%5.3f' % np.mean(y[grupo]))
    plt.text(minimo, maximo - 6.5, 'x std=%5.3f' % np.var(x[grupo]))
    plt.text(minimo, maximo - 8.0, 'y std=%5.3f' % np.var(y[grupo]))
pinta(x, y, 0, 221)
pinta(x, y, 1, 222)
pinta(x, y, 2, 223)
pinta(x, y, 3, 224)</code></pre>

Cuyo resultado sería el siguiente:

[<img class="aligncenter size-full wp-image-957" title="Anscombe" src="http://new.pybonacci.org/images/2012/10/anscombe.png" alt="" width="652" height="553" srcset="https://pybonacci.org/wp-content/uploads/2012/10/anscombe.png 652w, https://pybonacci.org/wp-content/uploads/2012/10/anscombe-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://new.pybonacci.org/images/2012/10/anscombe.png)

Se observa que los estadísticos representados son similares. Mismo ajuste lineal, coeficiente de correlación, media de los valores de x, media de los valores de y, varianza de los valores de x y varianza de los valores de y. Sin embargo, viendo los datos representados vemos que en el segundo no deberíamos usar un ajuste lineal para relacionar los valores de x y de y, en el tercer y cuarto grupos vemos que tenemos un dato que podría representar un dato erróneo (una mala medida, por ejemplo) y que en el tercer caso, al no haberlo filtrado correctamente, obtenemos un ajuste que nos llevaría a errores apreciables en el ajuste de los datos y en el cuarto caso nos llevaría a errores muy grandes en el ajuste de los datos mostrando una relación lineal que no parece existir.

Gracias a este plagio que acabo de hacer del artículo de la Wikipedia (traducido a python :-)) vemos la importancia de tratar nuestros datos con mimo, de realizar exploraciones iterativas y de refinar el conjunto final de datos 'limpios de impurezas' para hacer un análisis correcto de la 'realidad'. También vemos la importancia de compartir los datos base de los experimentos así como el código usado para el análisis de los mismos para que otros puedan reproducir los resultados y comprobar la veracidad de los mismos o poder corregir el análisis en caso necesario.

Finalmente os dejo un delirante vídeo de una charla TED de Hans Rosling donde se muestra la necesidad de mostrar de forma creativa los datos para poder llegar a un mejor entendimiento del universo que nos rodea.

[ted id=92 lang=es width=560 height=315]

P.D.: Sirva esta entrada para volver a homenajear a [John Hunter](http://numfocus.org/johnhunter/) y darle las gracias por permitirnos, mediante matplotlib, separarnos de los árboles para poder ver el bosque.

P.D.2: ¡¡¡¡¡No dejéis de ver el vídeo!!!!!