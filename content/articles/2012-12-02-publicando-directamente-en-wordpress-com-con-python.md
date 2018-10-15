---
title: Publicando directamente en wordpress.com con python
date: 2012-12-02T02:05:11+00:00
author: Kiko Correoso
slug: publicando-directamente-en-wordpress-com-con-python
tags: ipynb, ipython, notebook, prueba de concepto, XML-RPC

Este es un notebook de prueba publicado directamente en <https://pybonacci.org> (aunque se puede publicar en cualquier plataforma [wordpress](http://wordpress.org/) que tenga habilitado [xml-rpc](http://codex.wordpress.org/XML-RPC_Support)) desde un ipython notebook (ipynb de ahora en adelante).

Este ipynb consta de celdas con código python, celdas con texto formateado con markdown, con output de celdas con imágenes que se muestran 'inline', con celdas que enlazan a videos de youtube, con celdas que enlazan a imágenes online, con celdas que enlazan a páginas web,...

  1. Las celdas con código python se mostrarán como si en wordpress se envolviese el código con las etiquetas
        :::python
    

  1. Las celdas con texto formateado con markdown se transforman a html con la ayuda de <http://pypi.python.org/pypi/Markdown/>

  1. Los output de imágenes (por ejemplo, matplotlib) se suben directamente a wordpress como imágenes y se enlazan en la entrada

  1. Los output con videos de youtube se enlazan con la etiqueta _[youtube]_ de wordpress

  1. Los output de imágenes online harán una copia de la imagen que estéis enlazando y la subirán a vuestro wordpress por lo que tened cuidado si enlazáis imágenes con copyright y/o posibles restricciones.

  1. Los output de HTML de ipython se convierten en un enlace en lugar de meter un frame en wordpress.

  1. Podéis añadir lo que queráis...

    :::python
    ## Ejemplo de celda que muestra una imagen inline
    import matplotlib.pyplot as plt
    plt.plot([1,2,3,4,3,2,1])

La salida del anterior código mostrará lo siguiente
  
![wpid](https://pybonacci.org/images/2012/12/wpid-publicando_directamente_en_wordpress-com_con_python0.png)

    :::python
    ## Ejemplo de celda que muestra un video de youtube
    from IPython.display import YouTubeVideo
    YouTubeVideo("9sEI1AUFJKw")

La salida del anterior código mostrará lo siguiente
  
{% youtube 9sEI1AUFJKw%}

    :::python
    ## Ejemplo de celda que muestra una imagen enlazada como output
    from IPython.display import Image
    Image("https://pybonacci.org/images/2012/11/pybofractal1.png")

La salida del anterior código mostrará lo siguiente
  
![wpid2](https://new.pybonacci.org/images/2012/12/wpid-publicando_directamente_en_wordpress-com_con_python1.png)

    :::python
    ## Ejemplo de celda que muestra un frame html como output
    from IPython.display import HTML
    HTML('')

La salida del anterior código mostrará lo siguiente
  
Link a <http://ipython.org>

Todo esto es solo una prueba de concepto. Tengo que estudiarme nbconvert o ver si se podría integrar el [script que ha creado esta entrada](https://gist.github.com/4186007) (pero bien hecho) a partir de este [ipynb](http://nbviewer.ipython.org/4185988/) directamente en los menus de ipynb para poder publicar directamente un ipynb en wordpress (y otros) directamente con un par de clicks.

Nos vemos próximamente con más novedades.

Saludos.
