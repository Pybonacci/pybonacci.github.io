---
title: Cómo leer y escribir datos en archivos con NumPy
date: 2012-08-17T23:21:55+00:00
author: Juan Luis Cano
slug: como-leer-y-escribir-datos-en-archivos-con-numpy
tags: archivos, datos, numpy, python

## Introducción

Hoy vamos a ver rápidamente **cómo leer datos desde un archivo con NumPy** y también **cómo escribirlos**. Es algo a lo que tendremos que recurrir con mucha frecuencia, ya sea porque hemos recogido nuestros datos de un experimento y los tenemos almacenados en un fichero de texto, porque los hemos recibido por otras fuentes o porque queremos separar lo que es la lógica del programa de los datos con los que opera.

Ya comentamos hace tiempo [cómo crear matrices en Python](http://pybonacci.org/2012/06/11/como-crear-matrices-en-python-con-numpy/ "Cómo crear matrices en Python con NumPy") a partir de listas, utilizando rangos numéricos, etc. Lo bueno que tienen las funciones de NumPy que nos ayudan a desempeñar estas tareas es que no tenemos que preocuparnos por el manejo de ficheros con Python, así que leer o escribir será tan fácil como invocar una función.

_**En esta entrada se ha usado python 2.7.3 y numpy 1.6.2 **_**y es compatible con ****python 3.2.3**

## Lectura

NumPy nos ofrece varias funciones para cargar datos en forma matricial, pero la que usaremos con más frecuencia es la función [`loadtxt`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html). Su único argumento obligatorio es un nombre de archivo o un objeto `file` desde el que leer los datos.

<!--more-->

El comportamiento por defecto de `loadtxt` será:

  * Leer **todas las líneas** (se pueden saltar las `n` primeras utilizando el argumento `skiprows`,
  * salvo las que empiecen por `#` (se puede cambiar esto utilizando el argumento `comments`),
  * esperará que los datos estén separados por espacios (se puede cambiar utilizando el argumento `delimiter`),
  * y devolverá un array de NumPy de tipo `float` (el tipo se puede asignar con el argumento `dtype`).

Veamos algunos ejemplos sencillos:

    :::python
    In [1]: !cat matriz_a.dat # Evidentemente, tengo el archivo creado de antes... ¿magia?
    1.0000e+00 2.0000e+00
    -1.0000e+00 0.0000e+00
    In [2]: np.loadtxt('matriz_a.dat')
    Out[2]:
    array([[ 1.,  2.],
    [-1.,  0.]])
    In [3]: !cat matriz_b.dat # Nótese la primera línea
    # Datos del experimento
    1.0000e+00 2.0000e+00
    -1.0000e+00 0.0000e+00
    In [17]: B = np.loadtxt('matriz_b.dat') # NumPy la ignora sin más
    In [18]: B
    Out[18]:
    array([[ 1., 2.],
    [-1., 0.]])

Otras funciones que también sirven para leer datos son:

  * La función [`load`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.load.html) sirve para leer datos en el formato comprimido de NumPy, que suele tener las extensiones `.npy` o `.npz`.
  * La función [`fromfile`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.fromfile.html) sirve para leer datos en formato binario.
  * La función [`genfromtxt`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html) es mucho más flexible que `loadtxt`, y es crucial cuando el archivo está mal formateado o faltan valores en los datos. En la gran mayoría de los casos es suficiente con usar `loadtxt`.

## Escritura

Ya que hemos visto cómo leer archivos con NumPy, es lógico que aprendamos también cómo guardar nuestros datos en ficheros de texto. La contrapartida de la función `loadtxt` para escritura es, ¡sorpresa! la función [`savetxt`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html). Tiene dos argumentos obligatorios: el nombre del archivo y el array que se guardará. Su comportamiento por defecto es guardar los datos con 18 cifras decimales, pero esto se puede cambiar con el argumento `fmt`.

Para guardar nuestro array en un archivo, simplemente tendremos que hacer:

    :::python
    In [3]: A = np.array([[1, 2], [-1, 0]])
    In [4]: A
    Out[4]:
    array([[ 1,  2],
           [-1,  0]])
    In [5]: np.savetxt('matriz_a.dat', A, fmt='%.4e')
    In [6]: !cat matriz_a.dat
    1.0000e+00 2.0000e+00
    -1.0000e+00 0.0000e+00

¡Y esto es todo por hoy! No dudes en dejarnos tus comentarios [en el blog](#respond), [en Twitter](https://twitter.com/Pybonacci) o [en Facebook](https://www.facebook.com/Pybonacci). ¡Un saludo!