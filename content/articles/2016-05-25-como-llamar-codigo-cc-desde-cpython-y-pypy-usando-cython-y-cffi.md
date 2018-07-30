---
title: Cómo llamar código C/C++ desde CPython (y Pypy) usando Cython y CFFI
date: 2016-05-25T07:00:35+00:00
author: Kiko Correoso
slug: como-llamar-codigo-cc-desde-cpython-y-pypy-usando-cython-y-cffi
tags: c, cffi, cython, fortran, pypy

Hace unas semanas surgió esta pregunta en [StackOverflow en español](http://es.stackoverflow.com/): [¿Cómo llamar a código C++ desde Python?](http://es.stackoverflow.com/questions/9069/c%C3%B3mo-llamar-a-c%C3%B3digo-c-desde-python)

Y [la respuesta aceptada explica como hacer un wrapper sencillo usando Cython y CFFI](http://es.stackoverflow.com/a/9119/2816). Como da la casualidad que la respuesta es mía voy a extenderla un poco para añadir más cosas y poder explicarla un poco mejor.

## Prolegómenos

Antes de empezar a leer esta entrada deberías pasar a leer la entrada que hizo Juanlu hace un tiempo sobre CFFI titulada '[como crear extensiones en C para Python usando CFFI y Numba](http://pybonacci.org/2016/02/07/como-crear-extensiones-en-c-para-python-usando-cffi-y-numba/)' donde se dan más detalles de todo el proceso a realizar con CFFI.

Antes de probar el código de la presente entrada deberías instalar cffi y cython:

<pre><code class="language-python">conda install cffi cython # Válido en CPython</code></pre>

o

<pre><code class="language-python">pip install cffi cython # Válido en CPython y Pypy</code></pre>

Todo lo que viene a continuación lo he probado en Linux solo usando CPython 3.5 y Pypy 5.1.1, compatible con CPython 2.7 e instalado [usando esto](https://github.com/kikocorreoso/test_pypy_numpypy).

## Preliminares

Antes de pasar a la parte Cython y CFFI vamos a empezar creando los programas C/C++ que vamos a llamar desde Python.

Vamos a crear una librería que lo único que haga será sumar dos números enteros. Haremos una en C/C++ para Cython y una en C/C++ para CFFI.

### C/C++ para Cython

C y C++ no son el mismo lenguaje pero para este caso el código se puede considerar el mismo. Para el caso C++ tendremos un fichero _[*.hpp](https://gcc.gnu.org/onlinedocs/cpp/Header-Files.html)_ y un fichero _*.cpp_ (en C sería igual cambiando las extensiones a _*.h_ y _*.c_, respectivamente).

El fichero _*.hpp_ se llamará _milibrería.hpp_ y contendrá el siguiente código:

<pre><code class="language-cpp">long suma_enteros(long n, long m);</code></pre>

Mientras que el fichero _*.cpp_ se llamará _milibrería.cpp_ y contendrá el siguiente código:

<pre><code class="language-cpp">long suma_enteros(long n, long m){
    return n + m;
}</code></pre>

Lo que hace el código es bastante simple.

### C/C++ para CFFI

En este caso solo vamos a usar un fichero _*.cpp_ y se llamará _milibrería_cffi.cpp_ y contendrá el siguiente código:

<pre><code class="language-cpp">long suma_enteros(long n, long m){
    return n + m;
}

extern "C"
{
    extern long cffi_suma_enteros(long n, long m)
    {
        return suma_enteros(n, m);
    }
}</code></pre>

El código es el mismo de antes más una segunda parte que nos permite hacer el código accesible desde Python.

## Pegamento entre C/C++ y Python

En esta parte vamos a ver cómo unir el lenguaje compilado con el lenguaje interpretado.

### Mediante Cython

Antes de nada necesitamos definir un fichero _milibreria.pxd_. Este fichero es parecido a lo que hacen los ficheros _header_ en C/C++ o Fortran. Nos ayudará a 'encontrar' lo que hemos definido en c++ (más info sobre los ficheros pxd [aquí](http://docs.cython.org/src/tutorial/pxd_files.html)):

<pre><code class="language-python">cdef extern from "milibreria.hpp":
    long suma_enteros(long n, long m)</code></pre>

Un fichero _*.pxd_ se puede importar en un fichero _*.pyx_ usando la palabra clave `cimport`

Una vez 'enlazado' C/C++ con Cython mediante el fichero _*.pxd_ necesitamos hacer que la parte C/C++ sea accesible desde Python. Para ello creamos el fichero _pylibfromcpp.pyx_, que es una especie de código Python un poco 'cythonizado' (cython es un superconjunto de Python):

<pre><code class="language-python">cimport milibreria

def suma_enteros(n, m):
    return milibreria.suma_enteros(n, m)</code></pre>

### Mediante CFFI

En este caso resulta un poco más sencillo, para este caso concreto. Hemos de crear el fichero Python que, mediante CFFI, enlazará C/C++ con Python. Este ficheros se llamará _pylibfromCFFI.py_ y contendrá el siguiente código.:

<pre><code class="language-python">import cffi


ffi = cffi.FFI()
ffi.cdef("long cffi_suma_enteros(long n, long m);")
C = ffi.dlopen("./milibreria.so")


def suma_enteros(n, m):
    return C.cffi_suma_enteros(n, m)</code></pre>

## Setup

### Compilando con Cython

Para poder acceder a la librería C/C++ hemos de crear un fichero _setup.py_ que se encargará de la compilación que permitirá crear la extensión a la que accederemos desde Python. El fichero _setup.py_ contendrá:

<pre><code class="language-python">from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("pylibfromcpp",
              sources=["pylibfromcpp.pyx", "milibreria.cpp"],
              language="c++",)

setup(name = "cython_pylibfromcpp",
      ext_modules = cythonize(ext))</code></pre>

Para crear la extensión en sí, en la misma carpeta donde hemos dejado todos los ficheros anteriores y desde la línea de comandos, hacemos (como siempre, recomiendo hacer esto desde un entorno virtual):

<pre><code class="language-python">python setup.py build_ext -i</code></pre>

Y debería aparecer un fichero _pylibfromcpp.cpp_ y otro fichero _pylibfromcpp.pypy-41.so_ en la misma carpeta donde habéis ejecutado el comando anterior.

### Compilando con CFFI

Para poder hacer accesible la funcionalidad definida en C/C++ desde Python podemos compilar usando:

<pre><code class="language-cpp">g++ -o ./milibreria.so ./milibreria_cffi.cpp -fPIC -shared</code></pre>

Y deberíamos obtener el fichero _milibreria.so_.

## Llamando desde Python

### Usando nuestro 'wrapper' Cython

Ahora, si todo ha salido bien, dentro de un intérprete de python (como he comentado más arriba, lo he probado con CPython 3.5 y Pypy 5.1.1 y me ha funcionado en ambos) podemos hacer:

<pre><code class="language-python">import pylibfromcpp
print(pylibfromcpp.suma_enteros(2, 3))</code></pre>

### Usando nuestro 'wrapper' CFFI

De igual forma, si todo ha salido bien, podemos hacer:

<pre><code class="language-python">import pylibfromcpp
print(pylibfromcpp.suma_enteros(2, 3))</code></pre>

## Output completo en la consola pypy

### Para el caso Cython

<pre><code class="language-python">Python 2.7.10 (b0a649e90b6642251fb4a765fe5b27a97b1319a9, May 05 2016, 17:21:19)
[PyPy 5.1.1 with GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
&gt;&gt;&gt;&gt; import pylibfromcpp
&gt;&gt;&gt;&gt; print(pylibfromcpp.suma_enteros(2, 3))
5</code></pre>

### Para el caso CFFI

<pre><code class="language-python">Python 2.7.10 (b0a649e90b6642251fb4a765fe5b27a97b1319a9, May 05 2016, 17:21:19)
[PyPy 5.1.1 with GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
&gt;&gt;&gt;&gt; import pylibfromCFFI
&gt;&gt;&gt;&gt; print(pylibfromCFFI.suma_enteros(2, 3))
5</code></pre>

## Comentarios finales

Un esquema, grosso modo, de lo que hemos hecho:<figure id="attachment_3836" style="width: 723px" class="wp-caption aligncenter">

![](http://pybonacci.org/images/2016/05/Esquema.gif)

Pros y contras de cada una de las aproximaciones:

  * Cython permite usar Numpy sin problemas en CPython. Sin embargo, la última vez que intenté usar código Python con numpy arrays (Cython + Numpypy) reventaba todo en Pypy.
  * Cython lo podemos usar con CPython 2.x y 3.x. Cython funciona sin problemas en Pypy 5.1.1 (compatible con CPython 2.7). Numpypy NO funciona en Pypy3k.
  * El wrapper Cython que hemos hecho en este ejercicio es claramente más complejo que el que hemos hecho con CFFI (en este caso concreto).
  * Con Cython podemos usar el código compilado sin tocarlo mientras que con CFFI hemos de crear algo de código (muy simple) en el lenguaje compilado para acceder a su funcionalidad.
  * CFFI permite usar numpy arrays de forma sencilla, aunque, como con Cython, hay que 'ayudar con algo de código no Python' para que todo se pueda comunicar correctamente.

## Documentación

[Cython](http://cython.org/#documentation).

[CFFI](https://cffi.readthedocs.io/en/latest/).