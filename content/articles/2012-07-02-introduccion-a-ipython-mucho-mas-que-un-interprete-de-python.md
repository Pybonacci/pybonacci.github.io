---
title: Introducción a IPython: mucho más que un intérprete de Python
date: 2012-07-02T19:43:16+00:00
author: Juan Luis Cano
slug: introduccion-a-ipython-mucho-mas-que-un-interprete-de-python
tags: editores, IDEs, ipython, python

## Introducción

Hoy ha llegado el momento de hablar de [IPython](http://ipython.org/ "IPython"), aprovechando que [acaba de salir la versión 0.13](http://ipython.org/ipython-doc/rel-0.13/whatsnew/version0.13.html) después de 6 meses de duro trabajo. IPython es un intérprete de Python con unas cuantas características avanzadas que hemos usado desde que empezamos a escribir en el blog y que, sinceramente, si no conoces todavía no sé a qué estás esperando 😛

Decir que IPython es _solo_ un intérprete de Python es, no obstante, quedarse muy corto. Actualmente multitud de paquetes utilizan IPython como biblioteca o como intérprete interactivo, siendo el ejemplo más notable el proyecto [Sage](http://pybonacci.org/2012/05/06/sage-software-matematico-libre-como-alternativa/ "Sage: software matemático libre como alternativa"). IPython es multiplataforma, es software libre, tiene una enorme comunidad detrás, un desarrollo constante y bien organizado y es extremadamente potente. ¿Qué más se le puede pedir? 🙂<figure id="attachment_681" style="width: 560px" class="wp-caption aligncenter">

![Notebook de IPython](http://pybonacci.org/images/2012/07/ipy_013_notebook_spectrogram.png)

## Breve historia

IPython comenzó en 2001 de la mano de [Fernando Pérez](http://fperez.org/personal.html), investigador colombiano, cuando completaba su tesis sobre Física de partículas en la Universidad de Colorado. Pérez utilizaba mucho los notebooks de Mathematica, y el intérprete de Python le parecía «un juguete» en comparación[[1](http://blog.fperez.org/2012/01/ipython-notebook-historical.html)]. A partir de su propio trabajo y de otros dos proyectos, LazyPython e IPP, surgió lo que años después conocemos por IPython[[2](http://ipython.org/ipython-doc/dev/about/history.html)].

Lo importante para nosotros de este programa es que nació en un ámbito científico y de la mano de investigadores, pues, como el propio Fernando Pérez hizo notar, el flujo de trabajo en este tipo de ámbitos demanda un entorno interactivo. Ahí tenemos a MATLAB, Maple y Mathematica.

<!--more-->

**Nota**: ¿Sabes que escribimos hace tiempo sobre una [alternativa libre a Mathematica](http://pybonacci.org/2012/04/02/presentando-mathics-una-alternativa-libre-y-ligera-a-mathematica/ "Presentando Mathics: una alternativa libre y ligera a Mathematica") escrita en Python?

## Instalación

Si estás en **Linux** (que, por supuesto, es el mejor sistema operativo :P) la forma más directa de instalar IPython es utilizar el gestor de paquetes, centro de software o equivalente que viene en tu distribución, ya sea el Software Centre, `aptitude` o `apt-get` en Ubuntu, `yum` en Fedora y RHEL o `pacman` en Arch Linux. Si tienes algún problema para instalar IPython en tu distro, no dudes en decírnoslo en los comentarios.

Si estás en **Windows**, debes instalar primero `distribute` y `readline`. Como se puede leer [en la documentación](http://ipython.org/ipython-doc/stable/install/install.html#windows), los pasos son los siguientes:

**Nota**: ¿Sabes que puedes leer nuestra guía sobre [cómo instalar Python en Windows](http://pybonacci.org/2012/06/27/python-en-windows-hola-mundo-en-7-minutos/ "Python en Windows: «¡Hola mundo!» en 7 minutos") si no lo tienes aún?

  1. Instalar distribute. Para ello, descarga el archivo de [`distribute_setup.py`](http://python-distribute.org/distribute_setup.py) y haz doble clic sobre él.
  2. Instala pyreadline utilizando `easy_install`, el que acabas de añadir ahora. Para ello abre una ventana de línea de comandos (Ejecutar -> cmd -> OK) y escribe:

<pre>easy_install pyreadline</pre>

<ol start="3">
  <li>
    Instala IPython. Para ello, escribe ahora:
  </li>
</ol>

<pre>easy_install ipython</pre>

Si todo ha ido bien, si inicias IPython deberías ver algo como lo que aparece en la imagen.<figure id="attachment_695" style="width: 538px" class="wp-caption aligncenter">

![IPython en Windows](http://pybonacci.org/images/2012/07/ipython_windows.png)

Para **Mac**, tendrías que instalar IPython utilizando easy_install al igual que hemos hecho en Windows a través de una ventana de línea de comandos.

**Nota**: Aunque hayamos dado breves indicaciones de instalación en las tres plataformas mayoritarias, ten en cuenta que para el resto del tutorial se asumirá Linux. Si tienes problemas con alguna de las características descritas más adelante, no dudes en indicarlo en los comentarios.

## Funciones básicas de IPython

Nada más arrancar la interfaz por línea de comandos de IPython ya nos damos cuenta de que es un poco distinto del intérprete de Python por defecto. Hay algunas características que estaremos aprovechando todo el tiempo:

### Auto completado

El **auto completado** es una característica súper útil para no tener que escribir un código y también, por ejemplo, para inspeccionar objetos rápidamente. Se activa con la tecla Tab; por ejemplo, si tenemos NumPy instalado:

    :::python
    In [1]: import nu
    numbers  numpy
    In [1]: import num

y si escribimos la letra `p` y volvemos a presionar Tab, se terminaría de escribir `numpy`, ya que es la única opción disponible. Podemos explorar, por ejemplo, todas las propiedades del paquete `numpy` cuyo identificador empiece por `e`:

    :::python
    In [2]: np.e
    np.e            np.empty        np.exp          np.extract
    np.ediff1d      np.empty_like   np.exp2         np.eye
    np.einsum       np.equal        np.expand_dims
    np.emath        np.errstate     np.expm1

También funciona con variables definidas por nosotros:

    :::python
    In [2]: foobar = 24 ** 2
    In [3]: fo
    foobar    for       format
    In [3]: fo

### Historial

El **historial** es una manera de recuperar resultados antiguos que no hemos guardado en una variable. Como las entradas en IPython están numeradas, no hay más que hacer referencia a la salida correspondiente: por ejemplo, si queremos recuperar el resultado obtenido en <code style="color:red;">Out[3]</code>, utilizaremos la variable `_3`:

    :::python
    In [3]: 24 ** 2
    Out[3]: 576
    In [4]: _  # Esta variable almacena el último resultado
    Out[4]: 576
    In [5]: _ * 3  # Lo multiplicamos por 3
    Out[5]: 1728
    In [6]: _3  # Y volvemos a 24 ** 2
    Out[6]: 576

### Ayuda

La **ayuda** de IPython nos permite leer la documentación de objetos, funciones, etc. así como el código fuente donde se definieron cuando esté disponible. Ya la hemos utilizado en artículos anteriores, y se invoca utilizando el signo de interrogación `?`:

    :::python
    In [7]: import numpy
    In [8]: numpy?  # Signo de interrogación
    [Documentación del paquete numpy]
    In [9]: numpy.linspace?
    [Documentación de la función linspace]
    In [10]: numpy.linspace??  # Doble signo de interrogación
    [Código fuente de la función]

### Guardar, editar, cargar

Con IPython también podemos **guardar, editar y ejecutar archivos**. De esa forma, podemos aprovechar las ventajas del modo interactivo pero llevar un registro de nuestros progresos. Estas funciones se invocan utilizando los comandos «mágicos» `%save`, `%edit` y `%run`.

**Nota**: El comando `%edit` lanza el editor de texto en consola por defecto, que en el caso de Linux es Vim. Si te pasa como a mí y este programa te resulta incomprensible :P, tal vez te interese saber que para salir del programa hay que escribir `:q!`. <ins datetime="2013-08-01T21:24:50+00:00">Como sugiere Germán Racca en los comentarios, puedes añadir <code>EDITOR='nano'</code> en tu .bashrc para cambiar esto. ¡Gracias Germán!</ins>

La función `%save` recibe como argumentos el nombre del archivo que queremos y las líneas que queremos guardar en él. Veamos un ejemplo:

    :::python
    In [3]: import numpy as np
    In [4]: x = np.linspace(0, 1)
    In [5]: print np.sum(x)
    Out[5]: 25.0
    In [6]: %save foofile.py 3-5  # Guardamos las líneas 3 a 5 en foofile.py
    The following commands were written to file `foofile.py`:
    import numpy as np
    x = np.linspace(0, 1)
    print np.sum(x)
    In [7]: !cat foofile.py  # ¡Sorpresa! Ejecutamos comandos de Linux poniendo ! al principio
    # coding: utf-8
    import numpy as np
    x = np.linspace(0, 1)
    print np.sum(x)

Y, si salimos y volvemos a IPython:

    :::python
    In [1]: %run foofile.py  # Ejecutamos el archivo foofile.py
    25.0
    In [2]: %edit foofile.py  # Entramos en la ventana del editor, y dividimos la salida entre 3
     done. Executing edited code...
    8.33333333333

Nótese que el código se ejecuta cuando terminamos de editar el archivo. Si hay algún error, IPython nos lo dirá.

## Interfaz web: el notebook de IPython

**El notebook de IPython** está siendo una auténtica revolución. Inspirado en parte en el notebook de Sage, del que exprimió lo mejor y tomó nota de los errores cometidos, ha recibido mucha atención por parte de los desarrolladores en las últimas versiones y ahora es uno de los puntos más interesantes de IPython. Para disfrutar de las nuevas características necesitarás la versión 0.13 de IPython así como [Tornado](http://www.tornadoweb.org/). Para iniciar el notebook, escribe en la línea de comandos

<pre>$ ipython2 notebook</pre>

Aparecerán una serie de mensajes indicando la configuración del servidor y se abrirá una ventana del navegador.<figure id="attachment_701" style="width: 560px" class="wp-caption aligncenter">

![Notebook de IPython](http://pybonacci.org/images/2012/07/ipython_notebook.png)

A partir de aquí, si creas un nuevo notebook tendrás todo el poder de IPython con una interfaz mucho más rica en la que puedes editar y fusionar celdas, insertar texto y ecuaciones matemáticas, exportar los notebooks para compartirlos con otros usuarios y muchísimo más. Y lo vamos a dejar aquí, porque si no nos quedaría un artículo larguísimo.

Hay docenas de cosas que nos estamos dejando en el tintero, y podría hablarse largo y tendido sobre IPython. Si quieres ampliar información, siempre puedes consultar la [documentación oficial](http://ipython.org/ipython-doc/stable/index.html).

¿Te hemos convencido para utilizar IPython? ¿Te gustaría que escribiésemos más en profundidad sobre el notebook? ¿Ya lo conocías pero te hemos descubierto alguna función interesante? ¡Coméntanos!