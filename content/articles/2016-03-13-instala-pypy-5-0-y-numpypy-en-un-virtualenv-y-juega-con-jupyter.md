---
title: Instala pypy 5.0 y numpypy en un virtualenv y juega con Jupyter
date: 2016-03-13T21:10:52+00:00
author: Kiko Correoso
slug: instala-pypy-5-0-y-numpypy-en-un-virtualenv-y-juega-con-jupyter
tags: jupyter, numpy, numpypy, pypy, pypy-portable, virtualenv

Hoy voy a mostrar como usar la última versión de pypy y numpypy en vuestro linux. Para instalar pypy usaremos la versión [portable](https://github.com/squeaky-pl/portable-pypy) creada por [squeaky-pl](https://github.com/squeaky-pl). Numpypy lo instalaremos en un entorno virtual juntamente con Jupyter para poder hacer las pruebas en un entorno más amigable que la consola de pypy.

## Requerimientos

Necesitaremos tener instalada una versión reciente de virtualenv y git.

## Al lío

¡Si queréis la versión TL;DR [pinchad aquí](https://github.com/kikocorreoso/test_pypy_numpypy#usage-of-the-script)! Si sois un poco más pacientes y queréis entender un poco lo que vamos a hacer seguid leyento.

Todos los comandos que vienen a continuación los tenéis que meter en un terminal. Primero creamos un directorio que se llamará **pypy50** en vuestro **$HOME**

    :::bash
    mkdir $HOME/pypy50

Ahora nos vamos al directorio recién creado y nos descargamos el fichero comprimido que contiene el pypy portable de 64 bits

    :::bash
    cd $HOME/pypy50
    wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.0-linux_x86_64-portable.tar.bz2

Lo desempaquetamos:

    :::bash
    tar xvfj pypy-5.0-linux_x86_64-portable.tar.bz2

Ahora creamos un directorio **bin** en nuestro **$HOME**. Si ya existe te puedes saltar este paso:

    :::bash
    mkdir $HOME/bin

Creamos un enlace simbólico al ejecutable del pypy portable que hemos descargado que se encontrará en la carpeta **bin** del directorio **$HOME**:

    :::bash
    ln -s $HOME/pypy50/pypy-5.0-linux_x86_64-portable/bin/pypy $HOME/bin

Cambiamos los permisos al ejecutable para darle permisos de ejecución:

    :::bash
    chmod +x $HOME/pypy50/pypy-5.0-linux_x86_64-portable/bin/pypy

Al final de nuestro **.bashrc** vamos a añadir unas pocas líneas para que se añada el directorio **bin** de nuestro **$HOME** al **$PATH**:

    :::bash
    echo "" &gt;&gt; $HOME/.bashrc
    echo "# Added path to include pypy by $USER" &gt;&gt; $HOME/.bashrc
    echo "export PATH=$PATH:$HOME/bin" &gt;&gt; $HOME/.bashrc
    source $HOME/.bashrc

Creamos el virtualenv con pypy (en este paso necesitaréis tener virtualenv instalado). El virtualenv se creará en la carpeta **bin** de nuestro **$HOME** y se llamará **pypyvenv**:

    :::bash
    virtualenv -p pypy $HOME/bin/pypyvenv

Instalamos numpypy (numpy para pypy) en el nuevo virtualenv creado (aquí necesitarás tener git instalado). Para ello usamos el pip del entorno virtual.

    :::bash
    $HOME/bin/pypyvenv/bin/pip install git+https://bitbucket.org/pypy/numpy.git

Instalamos Jupyter haciendo algo parecido a lo anterior (aunque esta vez lo instalamos desde [pypi](https://pypi.python.org/pypi), no confundir con pypy):

    :::bash
    $HOME/bin/pypyvenv/bin/pip install jupyter
    

Y, por último, hacemos un poco de limpieza eliminando el fichero comprimido del pypy portable que hemos descargado anteriormente:

    :::bash
    rm $HOME/pypy50/pypy*.tar.bz2

¡¡¡Listo!!!

## Usando pypy

Para usar pypy (sin numpy) puedes lanzar una consola con pypy 5.0 (compatible con CPython 2.7) escribiendo en el terminal:

    :::bash
    pypy

## Usando pypy con numpy en un notebook de jupyter

Activamos el entorno virtual recien creado. Desde el terminal escribimos:

    :::bash
    . ~/bin/pypyvenv/bin/activate

Y arrancamos jupyter:

    :::bash
    jupyter notebook

Y después venís aquí y me contáis vuestras experiencias con pypy y numpypy o, si habéis encontrado fallos o queréis añadir mejoras, os vais a [github](https://github.com/kikocorreoso/test_pypy_numpypy) y abrís un issue o mandáis un Pull Request y salimos ganando todos.

## Ideas para mejorar el script (con vuestros pull requests)

  * Que pregunte donde instalar el pypy portable.
  * Que pregunte si queremos una carpeta **bin** o no.
  * Que pregunte cómo queremos llamar al entorno virtual y dónde lo queremos instalar.
  * Que pregunte si queremos instalar Jupyter y/u otras librerías.
  * ...

Saludos.

&nbsp;