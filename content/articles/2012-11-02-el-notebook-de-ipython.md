---
title: El notebook de IPython
date: 2012-11-02T17:52:30+00:00
author: Juan Luis Cano
slug: el-notebook-de-ipython
tags: ipython, notebook, python, video, web

## Introducción

Ya hablamos en su momento de [IPython, un intérprete de Python](http://pybonacci.org/2012/07/02/introduccion-a-ipython-mucho-mas-que-un-interprete-de-python/ "Introducción a IPython: mucho más que un intérprete de Python") con multitud de características avanzadas que lo hacían indispensable para ejecutar sesiones interactivas. Hoy vamos a continuar con lo que habíamos dejado a medias, y vamos a dedicar un artículo al [notebook de IPython](http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html), una herramienta que está verdaderamente revolucionando la manera en que se utiliza Python en ámbitos científicos y conferencias sobre el lenguaje, como se ha demostrado en la reciente [PyData NYC 2012](http://nyc2012.pydata.org/) que se ha celebrado en Nueva York (recuerda que en Pybonacci hemos seleccionado un [resumen de charlas de la PyData NYC 2012](http://pybonacci.org/2012/10/31/recopilacion-del-pydata-nyc-2012/ "Recopilación del PyData NYC 2012")).

<blockquote class="twitter-tweet" width="550">
  <p lang="en" dir="ltr">
    Biggest PyData winner: IPython notebook by a landslide. Everyone seems to be using it. Can't wait to try to teach <a href="https://twitter.com/swcarpentry">@swcarpentry</a> with it.
  </p>
  
  <p>
    &mdash; Richard T. Guy (@richardtguy84) <a href="https://twitter.com/richardtguy84/status/262289566009016320">October 27, 2012</a>
  </p>
</blockquote>



<blockquote class="twitter-tweet" width="550">
  <p lang="en" dir="ltr">
    Getting ready for <a href="https://twitter.com/hashtag/pydata?src=hash">#pydata</a> = Online Python Tutor on the <a href="https://twitter.com/hashtag/ipython?src=hash">#ipython</a> notebook. <a href="http://t.co/ZClSle9Y">pic.twitter.com/ZClSle9Y</a>
  </p>
  
  <p>
    &mdash; Brian Granger (@ellisonbg) <a href="https://twitter.com/ellisonbg/status/261568248993181696">October 25, 2012</a>
  </p>
</blockquote>



https://twitter.com/**dfm**/status/262245974334918656

<blockquote class="twitter-tweet" width="550">
  <p lang="en" dir="ltr">
    Awesome! IPython notebook slides (!) used in <a href="https://twitter.com/aterrel">@aterrel</a> 's talk on MPI.
  </p>
  
  <p>
    &mdash; Thomas Wiecki (@twiecki) <a href="https://twitter.com/twiecki/status/262267127510216704">October 27, 2012</a>
  </p>
</blockquote>



Aquí incluimos un vídeo que hemos grabado para mostrar las características fundamentales de IPython, porque ya se sabe que un vídeo vale más que mil imágenes 😉 No olvides suscribirte a nuestro canal en YouTube para futuras creaciones.



## El notebook de IPython

El **notebook de IPython** es una interfaz web para IPython, inspirada en los notebooks de Mathematica y [Sage](http://pybonacci.org/2012/05/06/sage-software-matematico-libre-como-alternativa/ "Sage: software matemático libre como alternativa"). Como puedes leer en esta [retrospectiva histórica](http://blog.fperez.org/2012/01/ipython-notebook-historical.html) escrita por Fernando Pérez, la idea de crear una interfaz de este tipo ya existía desde los inicios del proyecto IPython, allá por 2001, y después de muchos años, varios intentos fallidos y habiendo aprendido de la experiencia del propio notebook de Sage, que surgió antes pero estaba mucho menos pulido, fue finalmente presentado en la conferencia [EuroSciPy 2011](http://www.euroscipy.org/talk/4022).

<!--more-->

En la última versión de IPython se corrigieron algunos errores y se mejoró la parte de la interfaz y actualmente, como hemos señalado arriba, está atrayendo la atención de multitud de usuarios y [medios de comunicación](http://www.software.ac.uk/blog/2012-10-18-making-python-more-accessible-scientists-and-more-powerful). También hay artículos sobre cómo utilizarlo para escribir entradas en [Blogger](http://blog.fperez.org/2012/09/blogging-with-ipython-notebook.html) o [Octopress](http://jakevdp.github.com/blog/2012/10/04/blogging-with-ipython/).<figure id="attachment_1161" style="width: 614px" class="wp-caption aligncenter">

![Notebook de IPython](http://pybonacci.org/images/2012/11/2012-11-02-124946_1366x768_scrot.png?w=1024)

El notebook de IPython utiliza el servidor web Tornado y utiliza [ØMQ](http://zeromq.github.com/pyzmq/) para la comunicación entre procesos y websockets para la interacción con el navegador, con lo que se crea una conexión asíncrona y se consigue una buena velocidad de respuesta. En la parte de la interfaz utiliza [MathJax](http://www.mathjax.org/) para las fórmulas matemáticas y el editor CodeMirror.

## Características

Estas son algunas de las características del notebook de IPython:

  * Lista de notebooks.
  * Interfaz para el [procesamiento en paralelo](http://ipython.org/ipython-doc/stable/parallel/index.html) <ins datetime="2012-11-06T21:38:22+00:00">(esta característica no necesita el notebook)</ins>.
  * Edición y movimiento de celdas, inserción y eliminación arbitraria.
  * Gráficos y figuras integrados con el modo `--pylab inline` <ins datetime="2012-11-06T21:38:22+00:00">(esta característica tampoco necesita el notebook, puede usarse también en la interfaz Qt)</ins>.
  * Autocompletado de código.
  * Celdas con encabezados, puro HTML o Markdown.
  * Posibilidad de utilizar R, Octave, Cython...
  * Enlaces a la documentación del notebook, IPython, Python, NumPy, Scipy, SymPy y matplotlib.
  * Ayuda integrada.
  * Exportación a archivo `.ipynb`, basado en JSON, para compartir notebooks.
  * Atajos de teclado

<p style="text-align:left">
  Para mí, los atajos de teclado son uno de los mayores aciertos de este notebook. Aquí incluimos algunos de los más utilizados, la tabla completa se puede ver con el comando <code>Ctrl-m h</code>:
</p>

<table>
  <tr>
    <th>
      Comando
    </th>
    
    <th>
      Acción
    </th>
  </tr>
  
  <tr>
    <td>
      <code>Shift-Enter</code>
    </td>
    
    <td>
      Ejecutar celda
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-s</code>
    </td>
    
    <td>
      Guardar notebook
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m x</code>
    </td>
    
    <td>
      Cortar celda
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m c</code>
    </td>
    
    <td>
      Copiar celda
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m v</code>
    </td>
    
    <td>
      Pegar celda
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m d</code>
    </td>
    
    <td>
      Eliminar celda
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m a</code>
    </td>
    
    <td>
      Insertar celda encima
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m b</code>
    </td>
    
    <td>
      Insertar celda debajo
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m m</code>
    </td>
    
    <td>
      Celda Markdown
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m 1-6</code>
    </td>
    
    <td>
      Celda con encabezados HTML niveles 1 a 6
    </td>
  </tr>
  
  <tr>
    <td>
      <code>Ctrl-m h</code>
    </td>
    
    <td>
      Mostrar atajos de teclado
    </td>
  </tr>
</table>

## Compartir

Si bien el propio notebook de IPython es una herramienta extraordinaria, lo realmente valioso de ella es la posibilidad de compartir fácilmente notebooks con todo el mundo. La gente de IPython ha creado el [Visor de notebooks de IPython nbviewer](http://nbviewer.ipython.org/), con la que puedes visualizar cualquier notebook de IPython con tal de escribir la URL. Incluso si subes el archivo `.ipynb` al servicio Gist de GitHub, ¡no tienes más que incluir la ID del gist! El siguiente enlace lleva a la versión en notebook de nuestra entrada sobre transformadas discretas de Fourier:

<http://nbviewer.ipython.org/3804365/>

## Enlaces

  * Hay otros dos vídeos interesantes sobre el notebook de IPython en YouTube, [el primero por C. Titus Brown](http://youtu.be/HaS4NXxL5Qc) y [el segundo de la charla de Fernando Pérez](http://youtu.be/2G5YTlheCbw) en la PyCon 2012.
  * En este blog puedes encontrar una galería de imágenes con ejemplos de [representación de grafos con NetworkX dentro del notebook de IPython](http://bigsnarf.wordpress.com/2012/06/08/ipython-notebook-examples-of-youtube-html-and-networkx-visualizations/). Una transcripción de la segunda está disponible en las [notas de Marc Abramowitz de la PyCon 2012](http://pycon-2012-notes.readthedocs.org/en/latest/ipython.html).

Para terminar me gustaría agradecer a Joe di Castro, a quien admiro personalmente, todas las dudas que me contesta individualmente, y en concreto este tweet:

https://twitter.com/python_majibu/status/258640137020403713

Un saludo y gracias por leer 🙂