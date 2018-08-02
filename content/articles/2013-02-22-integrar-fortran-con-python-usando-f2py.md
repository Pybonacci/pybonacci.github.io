---
title: Integrar Fortran con Python usando F2PY
date: 2013-02-22T17:29:37+00:00
author: Juan Luis Cano
slug: integrar-fortran-con-python-usando-f2py
tags: f2py, fortran, numpy, python

## Introducción

En este artículo vamos a explicar cómo podemos utilizar bibliotecas escritas en Fortran (o FORTRAN) desde Python utilizando **F2PY**, cómo preparar el código Fortran para que este proceso sea lo más sencillo posible y cómo solventar los problemas que nos pueden surgir por el camino.

Hay dos casos en los que nos puede venir bien usar F2PY:

  * Queremos escribir una **parte de cálculo intensivo en Fortran** para que sea eficiente, pero queremos **controlar la lógica del programa desde Python**.
  * Tenemos **código legado** y el esfuerzo de portarlo a otro lenguaje es demasiado grande (código ilegible, ausencia de comentarios, fragilidad). Aún podemos aprovecharlo: con F2PY podemos llamarlo desde Python.

He utilizado numerosas referencias para escribir este artículo, y una fundamental es [ČERTÍK]. En esta web Ondrej Čertík, también un colaborador clave en proyectos como SymPy y NumPy, recoge una serie de buenas prácticas para escribir código Fortran moderno y portable, enlaza a los estándares del lenguaje, compara la sintaxis de Fortran y Python y detalla algunos métodos para integrar los dos. Por otro lado, [DOWLING] hace un desarrollo completo desde un programa en Python sin optimizar hasta un programa Fortran optimizado, y compara la velocidad de ejecución. Esta es otra referencia excelente, y merece la pena echarle un vistazo al resto de cursos de la Universidad de Cambridge.

Por supuesto, se puede consultar en Internet la [referencia de F2PY](http://cens.ioc.ee/projects/f2py2e/usersguide/index.html) original.

_**En esta entrada se han usado python 2.7.3, numpy 1.6.2 y gfortran 4.7.2.**_

**Nota**: Es posible que más adelante aparezca código todo en mayúsculas y sin sangrar. Quedáis avisados 🙂

<!--more-->

## ¿Qué es F2PY?

[F2PY](http://www.scipy.org/F2py) es una herramienta que permite la comunicación entre Python y Fortran. F2PY genera módulos de extensión (_extension modules_) para Python a partir de código Fortran, lo que permite:

  * Utilizar subrutinas, datos en bloques COMMON y variables en módulos de FORTRAN 77 o Fortran 90/95 desde Python.
  * Llamar funciones de Python desde Fortran (_callbacks_).
  * Manejar automáticamente la diferencia entre arrays NumPy-contiguos (esto es, C-contiguos) y Fortran-contiguos.

Fue creado en 1999 por Pearu Peterson mientras era estudiante de doctorado en la Universidad Técnica de Tallin, y en 2005 después de varias versiones estables quedó incluido dentro de NumPy. Si quieres saber más sobre el autor o sobre la historia de F2PY, puedes leer [entrevista a Pearu Peterson](http://www.indicthreads.com/1057/once-i-learned-about-python-i-stopped-trying-out-different-languages/) de 2004 o la entrada de su blog (abandonado) donde cuenta la [historia de F2PY](http://pearu.blogspot.it/2006/07/f2py-history-and-future.html). En la nueva web del proyecto se puede encontrar una [lista de artículos y diapositivas sobre F2PY](http://www.f2py.com/home/references), escritos por el propio Peterson.

### Algunos problemas

En este momento, aunque hay bastante material sobre F2PY, está bastante desordenado y disperso, y el desarrollo, por lo que se ve, estancado. En las diapositivas de una [charla que Peterson dio en 2007](http://www.it.uu.se/research/conf/SCSE07/material/Peterson.pdf), se puede leer:

> _Current F2PY code is readable to too few people (me, ...?)_
> 
> [El código fuente actual de F2PY es legible por pocas personas (yo, ...?)]

F2PY funciona de maravilla con FORTRAN 77 o Fortran 90/95 que no incluya características «modernas» como punteros, tipos derivados o arrays en forma asumida; prueba de ello es, como dije al principio, SciPy. Pero realmente el soporte de Fortran 90/95 es incompleto, a veces hay que editar las cabeceras manualmente (ya hablaremos de ellas), hay algunos bugs sin solucionar (uno de los cuales impide que funcione correctamente en Python 3), y el desarrollo de la «nueva generación» de F2PY, con un nuevo analizador sintáctico y soporte completo de Fortran 90/95 parece estancado desde hace un par de años. Este no parece un problema exclusivo de F2PY: Fwrap, una alternativa que utiliza Cython como capa intermedia, está estancado también.

Me parece justo mencionar esto al principio porque yo mismo me he encontrado con bastantes problemas en el pasado y a la hora de escribir este artículo. Para código antiguo, especialmente para el muy antiguo, no tendrás ningún problema; para código nuevo y moderno hará falta un poco más de maña, pero el resultado merece la pena.

## Ejemplos básicos

Para ir despacio, vamos a empezar con el clásico «¡Hola, mundo!», escrito, eso sí, en Fortran 95 moderno. Para ello voy a usar la opción `-std=f95` del compilador. Este es nuestro programa:

    print *, 'Hola, mundo!'
    end

pero si queremos controlar el flujo en Python, tendremos que convertir esto en una **subrutina**. De esta manera:

    ! hola_mundo_sub.f90
    subroutine hola_mundo(msg)
        character(len=12), intent(out) :: msg
        msg = 'Hola, mundo!'
    end subroutine

De esta manera, tenemos una única subrutina que devuelve la cadena `'¡Hola, mundo!'`. Ya podemos compilarlo con F2PY, escribiendo

`$ f2py -c hola_mundo_sub.f90 -m hola_mundo_sub`

Con el argumento `-`c indicamos qué fichero queremos compilar, y con `-m` el nombre del módulo resultante. Esto creó un archivo llamado `hola_mundo_sub.so`. Si ahora abrimos un intérprete de IPython:

    :::python
    In [1]: !ls
    hola_mundo.f90	hola_mundo_sub.f90  hola_mundo_submodule.c  hola_mundo_sub.so
    In [2]: import hola_mundo_sub
    In [3]: hola_mundo_sub?  # Documentación automática del módulo
    Type:       module
    String Form:&lt;module 'hola_mundo_sub' from 'hola_mundo_sub.so'&gt;
    File:       /home/juanlu/Development/Python/fortran/f2py_pybonacci/basico/hola_mundo_sub.so
    Docstring:
    This module 'hola_mundo_sub' is auto-generated with f2py (version:2).
    Functions:
    msg = hola_mundo()
    .
    In [4]: hola_mundo_sub.hola_mundo?  # Documentación automática de la subrutina
    Type:       fortran
    String Form:
    Docstring:
    hola_mundo - Function signature:
    msg = hola_mundo()
    Return objects:
    msg : string(len=12)
    In [5]: hola_mundo_sub.hola_mundo()  # ¡Funciona!
    Out[5]: 'Hola, mundo!'

¡Funcionó! Y además ha sucedido una cosa interesante: **F2PY ha transformado los argumentos de la función**. En Fortran declaramos una subrutina con el argumento `msg` solo de salida con `intent(out)`, y F2PY lo ha transformado en un valor de retorno de la función en Python. Genial, ¿no?

De todas formas, a nosotros lo que nos interesa casi siempre son los arrays, así que vamos a escribir un pequeño módulo con dos operaciones vectoriales: producto escalar y producto vectorial. Este es el código:

https://gist.github.com/4650350

Ahora no tenemos más que compilarlo como hemos hecho antes:

`$ f2py -c vectores.f90 -m vectores`

y ya podemos utilizarlo desde Python:

    :::python
    In [1]: !ls
    hola_mundo.f90	    hola_mundo_submodule.c  vectores.f90  vectores.so
    hola_mundo_sub.f90  vectores2.pyf	    vectores.pyf
    In [2]: from vectores import *  # Importamos el módulo
    In [3]: import numpy as np
    In [4]: u = np.array([1, 2, 3])
    In [5]: v = np.array([1, 0, -1])
    In [6]: vectores.producto_escalar(u, v)
    Out[6]: -2.0
    In [7]: vectores.producto_vectorial(u, v)
    Out[7]: array([-2.,  4., -2.])
    In [8]: w = _
    In [9]: type(w)  # El tipo devuelto es un array de NumPy
    Out[9]: numpy.ndarray
    In [10]: w.dtype  # Y los datos son float de 64 bits
    Out[10]: dtype('float64')
    In [11]: vectores.producto_escalar?
    Type:       fortran
    String Form:
    Docstring:
    producto_escalar - Function signature:
      p = producto_escalar(u,v,[n])
    Required arguments:
      u : input rank-1 array('d') with bounds (n)
      v : input rank-1 array('d') with bounds (n)
    Optional arguments:
      n := len(u) input int
    Return objects:
      p : float

Fíjate en el último bloque. F2PY ha interpretado correctamente que el argumento `n` es el tamaño de los arrays, y lo ha convertido en un parámetro opcional. Cuando manejamos arrays de esta manera se dice que se dan los arrays «en forma explícita»; existe otra manera, denominada «en forma asumida», que da más problemas con F2PY y que no vamos a utilizar.

Hasta aquí todo muy sencillo, ahora vamos a ver algunos ejemplos más interesantes.

## Ficheros .pyf

Hasta ahora hay un paso que F2PY estaba haciendo «entre bastidores» y devolviendo solamente el resultado final. Este paso intermedio es la generación de **ficheros de cabecera** de extensión `.pyf`, que son los que definen la interfaz a los subprogramas Fortran que se llamarán desde Python.

Por ejemplo, vamos a generar el fichero de cabecera de nuestro módulo de operaciones vectoriales:

`$ f2py -h vectores.pyf -m vectores vectores.f90`

Con el argumento `-h` indicamos cómo queremos que se llame el fichero de cabecera, con `-m` el módulo correspondiente y por último incluimos el código fuente. Veremos algo como esto:

    !    -*- f90 -*-
    ! Note: the context of this file is case sensitive.
    python module vectores ! in
        interface  ! in :vectores
            module vectores ! in :vectores:vectores.f90
                function producto_escalar(n,u,v) result (p) ! in :vectores:vectores.f90:vectores
                    integer, optional,intent(in),check(len(u)>=n),depend(u) :: n=len(u)
                    double precision dimension(n),intent(in) :: u
                    double precision dimension(n),intent(in),depend(n) :: v
                    double precision :: p
                end function producto_escalar
                function producto_vectorial(u,v) result (w) ! in :vectores:vectores.f90:vectores
                    double precision dimension(3),intent(in) :: u
                    double precision dimension(3),intent(in) :: v
                    double precision dimension(3) :: w
                end function producto_vectorial
            end module vectores
        end interface
    end python module vectores
    ! This file was auto-generated with f2py (version:2).
    ! See http://cens.ioc.ee/projects/f2py2e/

La sintaxis de los archivos `.pyf` es muy parecida a la de Fortran, pero no igual. No necesitamos entenderla exactamente para trabajar, pero a veces puede ser útil modificarla para ajustar algunas cosas. Las posibilidades están documentadas en la [referencia de F2PY](http://cens.ioc.ee/projects/f2py2e/usersguide/index.html).

Por ejemplo, hemos visto antes que F2PY ha transformado el argumento n de producto_escalar en opcional, y realmente desde Python nunca lo vamos a utilizar. ¿Por qué no ocultarlo? Podemos hacerlo utilizando la clave `intent(hide)`. Así, la línea correspondiente al argumento n quedaría

`integer, optional,intent(hide),check(len(u)>=n),depend(u) :: n=len(u)`

Simplemente hemos añadido la palabra hide después de in separada por una coma. Ahora podemos decirle a F2PY que genere un nuevo módulo de extensión, esta vez utilizando la cabecera que acabamos de editar.

`f2py2 -c vectores.f90 -m vectores vectores.pyf`

Y si ahora probamos el módulo:

    :::python
    In [2]: vectores.producto_escalar?
    Type:       fortran
    String Form:&lt;fortran object&gt;
    Docstring:
    producto_escalar - Function signature:
      p = producto_escalar(u,v)
    Required arguments:
      u : input rank-1 array('d') with bounds (n)
      v : input rank-1 array('d') with bounds (n)
    Return objects:
      p : float

¡El argumento n ha desaparecido! Nos queda una interfaz completamente pythonica 🙂

## Directivas

A veces estos ajustes de la interfaz se pueden incluir en el propio código fuente, sin necesidad de modificar las cabeceras. Esto se puede hacer utilizando **directivas**. Las directivas son comentarios en el código Fortran que F2PY puede entender e interpretar. Por ejemplo, si introducimos debajo de la línea 10 de nuestro archivo vectores.f90

`!f2py intent(hide) :: n`

La cabecera automáticamente incorporará la clave hide. Todas las directivas empiezan por `!f2py`, o `Cf2py` para código FORTRAN 77.

## Conclusión

Este artículo ya se ha alargado bastante, pero creo que he conseguido transmitir una idea aproximada de las posibilidades de F2PY. Desde luego, si tienes código legado antiguo en Fortran o FORTRAN 77 y quieres utilizarlo desde Python F2PY es tu opción más segura. No te olvides de compartir el artículo y de dejarnos tus sugerencias y dudas en los comentarios.

## Referencias

  1. ČERTÍK, Ondřej et al. _Fortran 90_ [en línea]. Disponible en Web: <<http://fortran90.org/>>. [Consulta: 19 de enero de 2013]
  2. DOWNLING, John. _Interfacing Python with Fortran_ [en línea]. Disponible en Web: <<http://www.ucs.cam.ac.uk/docs/course-notes/unix-courses/pythonfortran>>. [Consulta: 21 de enero de 2013]

## Enlaces

  * http://dsnra.jpl.nasa.gov/software/Python/F2PY_tutorial.pdf
  * http://fortran90.org/src/best-practices.html
  * http://www.ucs.cam.ac.uk/docs/course-notes/unix-courses/pythonfortran/files/f2py.pdf
  * http://www.scipy.org/Cookbook/F2Py
  * http://websrv.cs.umt.edu/isis/index.php/F2py_example
  * http://www.engr.ucsb.edu/~shell/che210d/f2py.pdf
  * http://cens.ioc.ee/~pearu/papers/IJCSE4.4\_Paper\_8.pdf
  * http://cens.ioc.ee/projects/f2py2e/usersguide/f2py_usersguide.pdf