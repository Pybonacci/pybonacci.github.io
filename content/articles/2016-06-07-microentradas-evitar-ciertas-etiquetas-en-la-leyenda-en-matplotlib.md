---
title: Microentradas: Evitar ciertas etiquetas en la leyenda en Matplotlib
date: 2016-06-07T01:51:59+00:00
author: Kiko Correoso
slug: microentradas-evitar-ciertas-etiquetas-en-la-leyenda-en-matplotlib
tags: labels, Legend, matplotlib, MicroEntradas

A veces, me llegan ficheros de datos con datos cada hora o cada día y los quiero representar en un _plot_. Para ello, podría acumular los ficheros en uno solo y luego pintarlo pero como lo debo hacer en 'tiempo casi-real' se puede meter todo en un bucle `while` que espera los ficheros cada hora/día/lo que sea y va pintando cada variable por tramos. Por ejemplo, una aproximación podría ser la siguiente:

    :::python
    import numpy as np
    import matplotlib.pyplot as plt
    plt.style.use('bmh')
    %matplotlib inline

    plt.figure(figsize \= (12, 6))
    for i in range(10):
        x \= np.arange(i \* 10, i \* 10 + 10)
        y\_var1 \= np.random.randint(1, 5, 10)
        y\_var2 \= np.random.randint(5, 8, 10)
        plt.plot(x, y\_var1, color \= 'k', label \= 'variable1')
        plt.plot(x, y\_var2, color \= 'g', label \= 'variable2')
        plt.legend()
        plt.ylim(, 9)

![wpid1](https://pybonacci.org/images/2016/06/wpid-Microentradas_Evitar_ciertas_etiquetas_en_la_leyenda_en_Matplotlib-ipynb1.png?style=centerme

Como véis, en la gráfica anterior hay varios problemas pero como esta es una [MicroEntrada](https://pybonacci.org/tag/microentradas/) solo nos vamos a centrar en el problema de las etiquetas repetidas en la leyenda.

¿Cómo podríamos evitar el meter tantas veces una etiqueta repetida?
--------------------------------------------------------------------------------------------------------------

Mi problema es que el bucle es o podría ser 'infinito' y tengo que inicializar las etiquetas de alguna forma. Si miro en esta respuesta encontrada en [Stackoverflow](http://stackoverflow.com/a/19386045) dice que en la documentación se indica que *"If label attribute is empty string or starts with “_”, those artists will be ignored."* pero si busco [aquí](http://matplotlib.org/api/artist_api.html#matplotlib.artist.Artist.set_label) o [en el enlace que indican en la respuesta en Stackoverflow](http://matplotlib.org/users/legend_guide.html) no veo esa funcionalidad indicada en ningún sitio. Eso es porque aparecía en la versión [1.3.1](https://github.com/matplotlib/matplotlib/blob/v1.3.1/doc/users/legend_guide.rst) pero [luego desapareció](https://github.com/matplotlib/matplotlib/blob/v1.4.0/doc/users/legend_guide.rst)... Sin embargo podemos seguir usando esa funcionalidad aunque actualmente no esté documentada:

    :::python
    plt.figure(figsize = (12, 6))
    for i in range(10):
        x = np.arange(i * 10, i * 10 + 10)
        y_var1 = np.random.randint(1, 5, 10)
        y_var2 = np.random.randint(5, 8, 10)
        plt.plot(x, y_var1, color = 'k', label = 'variable1' if i ==  else "_esto_no_se_pintará")
        plt.plot(x, y_var2, color = 'g', label = 'variable2' if i ==  else "_esto_tampoco")
        plt.legend()
        plt.ylim(, 9)

![wpid2](https://pybonacci.org/images/2016/06/wpid-Microentradas_Evitar_ciertas_etiquetas_en_la_leyenda_en_Matplotlib-ipynb2.png?style=centerme

Espero que a alguien le resulte útil.
