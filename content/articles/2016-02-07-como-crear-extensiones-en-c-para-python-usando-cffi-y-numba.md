---
title: Cómo crear extensiones en C para Python usando CFFI y numba
date: 2016-02-07T23:23:18+00:00
author: Juan Luis Cano
slug: como-crear-extensiones-en-c-para-python-usando-cffi-y-numba
tags: c, cffi, numba, performance, python, python 3

## Introducción

En este artículo vamos a ver **cómo crear extensiones en C para Python usando CFFI y aceleradas con numba**. El proyecto [CFFI](http://cffi.readthedocs.org/) ("C Foreign Function Interface") pretende ofrecer una manera de llamar a bibliotecas escritas en C desde Python de una manera simple, mientras que [numba](http://pybonacci.org/tag/numba/), como podéis leer en nuestro blog, es un compilador JIT para código Python numérico. Mientras que hay algo de literatura sobre cómo usar CFFI, muy poco se ha escrito sobre cómo usar funciones CFFI desde numba, una característica que estaba desde las primeras versiones pero que no se completó [hasta hace cuatro meses](https://github.com/numba/numba/pull/1454). Puede parecer contradictorio mezclar estos dos proyectos pero en seguida veremos la justificación y por qué hacerlo puede abrir nuevos caminos para escribir código Python extremadamente eficiente.

Este trabajo ha surgido a raíz de mis intentos de utilizar funciones hipergeométricas escritas en C desde funciones aceleradas con numba para el artículo que estoy escribiendo sobre [poliastro](http://pybonacci.org/tag/poliastro/). El resultado, si bien no es 100 % satisfactorio aún, es bastante bueno y ha sido relativamente fácil de conseguir, teniendo en cuenta que partía sin saber nada de C ni CFFI hace tres días.

<blockquote class="twitter-tweet" data-width="550">
  <p lang="es" dir="ltr">
    Pasatiempo de esta tarde: tratar de crear una interfaz Python para una función de C usando CFFI. ¡Deseadme suerte!
  </p>
  
  <p>
    &mdash; Juan Luis Cano (@astrojuanlu) <a href="https://twitter.com/astrojuanlu/status/695295966887428099">February 4, 2016</a>
  </p>
</blockquote>



## ¿Por qué CFFI + numba?

Como decíamos CFFI y numba, aunque tienen que ver con hacer nuestros programas más rápidos, tienen objetivos bastante diferentes:

  * CFFI nos permite usar C desde Python. De este modo, si encontramos algún algoritmo que merece la pena ser optimizado, lo podríamos escribir en C y llamarlo gracias a CFFI.
  * [numba nos permite acelerar código Python numérico](http://pybonacci.org/2015/03/13/como-acelerar-tu-codigo-python-con-numba/). Si encontramos algún algoritmo que merece la pena ser optimizado, adecentamos un poco la función correspondiente y un decorador la compilará a LLVM al vuelo.

<!--more-->

¿En qué situaciones nos puede interesar combinar las dos? En mi caso, quería implementar un algoritmo para poliastro en Python y en un momento dado me di cuenta de que tenía que utilizar [la función hipergeométrica de Gauss ${}\_2{F}\_1$](http://functions.wolfram.com/HypergeometricFunctions/Hypergeometric2F1/). En este punto tenía varias opciones:

  * Escribir todo el código en C, y llamarlo desde CFFI. Sonaba como una trampa mortal puesto que no sé C, y además volvería al problema de los dos lenguajes que de alguna forma estoy tratando de evitar o minimizar.
  * Reimplementar la función hipergeométrica en Python y acelerarla con numba. Esta sería una opción bastante buena de no ser porque la función en cuestión [tiene una definición endemoniada](http://functions.wolfram.com/HypergeometricFunctions/Hypergeometric2F1/02/02/) si la quería implementar para todos los casos. Lo que me lleva a las siguientes dos opciones.
  * Implementar una versión simplificada de la función. En mi caso solo estoy interesado en los valores ${}\_2{F}\_1(3, 1, \frac{5}{2}, x)$. Habría sido lo más fácil y no me habrían salido tantas canas, pero entonces se me ocurrió una mejor:
  * Aprovechar la implementación de la biblioteca CEPHES, que es la que usa `scipy.special`, hacer un wrapper usando CFFI y acelerarlo con numba.

Aquí la pregunta clave es: ¿qué es esto de acelerar con numba algo escrito en C? La cuestión es que si quiero usar numba _en modo estricto_ (es decir: aprovechando el modo `nopython`) todas las funciones que se utilicen tienen que estar compiladas en modo `nopython` también. Un meme vale más que mil palabras.

![](http://pybonacci.org/images/2016/02/nopython-300x300.jpg)

En definitiva: una de las ventajas sustanciales que tendríamos con esto es que **podríamos reutilizar código legado con código nuevo acelerado con numba**. ¿Lo intentamos? ¡Vamos allá!

## 0. CFFI: ¡Hola mundo!

[La documentación de CFFI](http://cffi.readthedocs.org/) es bastante buena, aunque desde mi punto de vista le faltan una referencia y una explicación para novatos que no saben nada. Hay cuatro formas de utilizar CFFI, que surgen de combinar dos parámetros:

  * **ABI/API**: En el modo ABI utilizamos la función `ffi.dlopen` para cargar el código «a nivel binario», de donde se leen en crudo las estructuras y las funciones. En el modo API, en cambio, creamos una biblioteca compartida utilizando el compilador de C: esta forma de trabajar es mucho más portable.
  * **"in-line"/"out-of-line"**: En el modo "in-line" importamos las definiciones al vuelo cada vez, mientras que en el modo "out-of-core" hay dos pasos: uno de creación y otro de importación. El segundo es más apropiado cuando vamos a distribuir código.

Dicho esto nosotros vamos a trabajar a nivel de API creando módulos "out-of-line", tal y como se explica en [los ejemplos de CFFI](http://cffi.readthedocs.org/en/latest/overview.html#real-example-api-level-out-of-line).

Para la estructura de los archivos me voy a basar en el excelente proyecto [pyca/cryptography](https://github.com/pyca/cryptography), que utiliza CFFI para ser compatible con PyPy. Dicho proyecto sigue la [guía de Donald Stufft de cómo distribuir un proyecto CFFI](https://caremad.io/2015/06/distributing-a-cffi-project-redux/).

Empezando por una función extremadamente sencilla (pero que tenga las mismas cabeceras que lo que ando persiguiendo) vamos a necesitar dos funciones:

  * `ffi.cdef`, en la que incluiremos las cabeceras de las funciones.
  * `ffi.set_source`, en la que incluiremos bien el código de las funciones (si las estamos definiendo directamente) o bien de nuevo solo las cabeceras (si pertenecen a una biblioteca externa).

El orden de llamada de estas funciones es irrelevante. Este sería nuestro código:

    :::python
    
    from cffi import FFI
    ffi = FFI()
    
    ffi.cdef(
        """
    double hyp2f1x ( double a, double b, double c, double x );
    """
    )
    ffi.set_source(
        "_hyper",  # Nombre del módulo
        """
    double hyp2f1x ( a, b, c, x )
    double a, b, c, x;
    {
        return 1.0;  // De hipergeométrico, poco
    }
    """
    )
    
    
    if __name__ == '__main__':
        ffi.compile()
    
    

Peeeeero para usarlo desde Python nos falta un paso importante... ¡escribir un `setup.py` y ejecutarlo! Sí, sé que lo odiáis. Yo también, pero en esta ocasión (olvidándonos de algunos casos muy particulares, que de todas formas explica Donald Stufft) es bastante sencillo:

    :::python
    
    from setuptools import setup, find_packages
    
    setup(
        name="hyper",
        version="0.1.dev0",
        packages=find_packages("src"),
        package_dir={"": "src"},
        setup_requires=["cffi&gt;=1.0.0"],
        install_requires=["cffi&gt;=1.0.0"],
        cffi_modules=["src/_cffi_src/build_hyper.py:ffi"],
    )
    

Una vez hecho esto, podemos instalar nuestro recién creado paquete y usarlo. Primero creamos el "wrapper":

    :::python
    
    from _hyper.lib import hyp2f1x as _hyp2f1
    
    def hyp2f1(a, b, c, x):
        return _hyp2f1(a, b, c, x)
    

Y ahora lo instalamos y lo usamos:

    :::bash
    
    $ pip install -e .  # Sí. No preguntéis. https://twitter.com/Pybonacci/status/681189810057383936
    [...]
    $ python
    &gt;&gt;&gt; from hyper import hyper          
    &gt;&gt;&gt; hyper._hyp2f1(3, 1, 5/2, 0.1)
    1.0
    

¡Perfecto! Ya hemos conseguido un ejemplo trivial. Para tener algo que funcione necesito hacer un "wrapper" _de verdad_ para CEPHES, para seguir me gustaría que diese el mismo resultado que [scipy.special.hyp2f1](http://docs.scipy.org/doc/scipy/reference/generated/scipy.special.hyp2f1.html) y para terminar me gustaría poder acelerar el resultado con numba. ¡Seguimos!

## 1. Haciendo un wrapper para una biblioteca C

Seguro que hay bibliotecas de funciones especiales escritas en C, FORTRAN y COBOL por todas partes, pero para poder verificar con SciPy yo me he empeñado en que tengo que usar CEPHES. Una vez que conseguí [encontrar el código de CEPHES](https://github.com/jeremybarnes/cephes), tenía que decidir entre dos opciones:

  * Podría incluir directamente en mi proyecto todos los archivos C y compilarlos con un poco de magia distutils + CFFI + ?. El problema es que el Makefile tenía cosas relacionadas con lenguaje ensamblador (!) y solo de pensar en que eso podría interferir con distutils me asusté bastante.
  * Distribuir de alguna forma CEPHES como un proyecto aparte de forma que pudiese instalarlo en mi sistema y hacer referencia a la biblioteca compartida correspondiente.

La segunda opción tenía mucha menos incertidumbre para mí, porque a pesar de que no encontré paquetes para ninguna distribución de Linux que proporcionasen esta biblioteca, tenía un arma secreta: [conda](http://conda.pydata.org/docs/building/build.html).

Los que me conocéis ya sabéis que soy un <del datetime="2016-02-07T20:02:58+00:00">fanático</del> <ins datetime="2016-02-07T20:02:58+00:00">gran admirador</ins> del trabajo de Continuum en general, y de numba y conda en particular. En este caso, conda me venía perfecto porque podría crear un paquete a mi medida (conda sirve para cualquier lenguaje) y luego instalarlo en un entorno conda apropiado para que CFFI encontrase la biblioteca a la primera sin tener que hacer manipulaciones con el `PATH`. La [receta para el paquete conda de CEPHES](https://github.com/Pybonacci/cffi_test/tree/548196c/buildscripts/condarecipes/cephes) también está en GitHub, y las explicaciones me las reservo para otro artículo 😉

    :::bash
    
    $ source activate hyper35
    (hyper35) $ conda build cephes
    (hyper35) $ conda install cephes --use-local
    

Una vez que tengo CEPHES instalado y accesible, no tengo más que hacer referencia a ello a la hora de crear el módulo CFFI:

    :::python
    
    ffi.set_source(
        "_hyper",
        """
    double hyp2f1 ( double a, double b, double c, double x );
    """,
        libraries=["md"],  # libmd.a
    )
    

Y reconstruir el "wrapper" haciendo `pip install -e .` de nuevo.

¡Ya está! Hasta aquí todo sorprendentemente fácil. Ahora es cuando viene lo divertido, porque mi intención es usar estas funciones desde numba, así que tendremos que seguir puliendo el código un poco más.

## 2. Añadiendo numba en modo `nopython`

numba trae soporte para módulos CFFI "out-of-line" desde la versión 0.22. Esto quiere decir que podremos utilizar funciones de módulos CFFI desde funciones aceleradas con numba, sin más que "registrar" el módulo en primer lugar usando la función `cffi_support.register_module`. Nuestro "wrapper" Python quedaría así ahora:

    :::python
    
    from numba import njit, cffi_support
    
    import _hyper
    cffi_support.register_module(_hyper)  # Registramos el módulo
    
    _hyp2f1 = _hyper.lib.hyp2f1x  # Ver más abajo
    
    
    @njit
    def hyp2f1(a, b, c, x):
        return _hyp2f1(a, b, c, x)
    

Aquí ya hay que empezar a tener cuidado, porque noté que [no se puede escribir `_hyper.lib.hyp2f1x` directamente dentro de la función de numba](https://github.com/numba/numba/issues/1688). Con esta precaución, ¡el código funciona sin problemas!

## _Intermezzo_: Los _benchmarks_

En el fondo los ingenieros no dejamos de ser gente primaria y visceral, y aunque en principio se nos enseña pensamiento racional en la Universidad se nos olvida en cuanto ponemos un pie fuera del mundo académico (si es que alguna vez lo llegamos a interiorizar). Por eso nos encanta hablar de rendimiento, con más motivo si no hay cifras de por medio. Si en una cena de Navidad juntaran a un montón de ingenieros y programadores, entre langostino y langostino hablarían de rendimiento.

</sarcasm>

Llegados a este punto sin embargo merece la pena hacer un microbenchmark y un pequeño comentario entre la función que acabamos de incorporar con CFFI y numba y su equivalente en SciPy. Para ello utilizaremos [pytest-benchmark](https://github.com/ionelmc/pytest-benchmark), que acabo de usar por primera vez hace cinco minutos y que me ha dejado boquiabierto (tanto por la buena presentación de los resultados como por los números en sí).

![](http://pybonacci.org/images/2016/02/benchmark-300x76.png)

Habéis leído bien: **nuestra función con CFFI + numba es, en media, 5 veces más rápida que la versión de SciPy**. Hay que puntualizar una cosa importante, y es que la función de SciPy tiene interfaz de ufunc: esto puede suponer una sobrecarga considerable (si bien ["de utilidad cuestionable"](https://github.com/scipy/scipy/blob/maintenance/0.17.x/scipy/special/README)). Aun así, me parece que los resultados son excelentes y que podría plantearse incluso aprovechar esta estrategia de forma más generalizada en el futuro.

## 3. Pasar arrays como argumentos

Aún nos falta una cosa más y es saber cómo se pueden pasar arrays a estas funciones CFFI. Aquí numba y CFFI nos ayudan porque proveen una función, `ffi.from_buffer`, precisamente para esta tarea. Supongamos que creamos una función a nivel de C que en vez de tomar un escalar toma un array de valores sobre los que evaluarse:

    :::python
    
    ffi.set_source(
        "_hyper",
        """
    double hyp2f1 ( double a, double b, double c, double x );
    
    // Función nueva, vectorizada para arrays de doble precisión
    double vd_hyp2f1 ( int n, double a, double b, double c, double* x, double* res) {
        int i;
        for (i=0; i&lt;n; i++)
            res[i] = hyp2f1(a, b, c, x[i]);
    }
    """,
        libraries=["md"],
    )
    

Tendríamos que llamarla desde Python de esta manera:

    :::python
    
    @njit
    def vd_hyp2f1(a, b, c, x):
        res = np.empty_like(x)
        _vd_hyp2f1(
                len(x), a, b, c,
                ffi.from_buffer(x), ffi.from_buffer(res)  # ¡Nótese!
        )
    
        res[x == 1.0] = np.inf
        return res
    

¡Y de nuevo vuelve a funcionar! ¿Se nota mi entusiasmo?

## y 4. Sobrecargando la función

Como colofón final y visto que nuestra función y la de SciPy aún no son exactamente equivalentes ¿sabéis qué sería genial? ¡Poder sobrecargar la función y que se comporte de manera vectorizada si la llamamos con arrays! numba ya permite este mecanismo (conocido como ["multiple dispatch"](http://numba.pydata.org/numba-doc/0.23.1/developer/dispatching.html)), pero el problema es que <del datetime="2016-02-08T20:20:51+00:00">en el momento de escribir estas líneas <a href="https://github.com/numba/numba/issues/1691">no funciona para funciones CFFI</a></del> <ins datetime="2016-02-08T20:20:51+00:00">no estaba interpretando bien la semántica de Python y <a href="https://groups.google.com/a/continuum.io/d/msg/numba-users/Q3LfRbpWP6w/aHuXoL_JDwAJ">no tengo claro que esto sea posible</a></ins>. Esto es lo único que me falta para llegar a un 100 % de satisfacción 🙂

## Conclusiones

Personalmente era la primera vez en mi vida que probaba CFFI y me ha parecido extremadamente sencillo. He pasado de un ejemplo trivial a algo serio y que funciona en cuestión de pocas tardes. Faltaría tener alguna forma automática de generar los wrappers y compatibilidad total con numba.

Algunas cosas que no he tratado son:

  * Llamada de código Fortran desde CFFI. ¡Habéis leído bien! Una vez que la interoperabilidad Python C está resuelta, solo hay que resolver C Fortran. En este artículo de Dorota Jarecka tenéis un ejemplo de [cómo usar CFFI para llamar Fortran desde Python](http://scientific-software-diary.com/?p=29). ¿Quién se anima a construir un f2py de segunda generación capaz de generar "wrappers" a código Fortran que use ISO\_C\_BINDING?
  * [Uso de CFFI para "embedding" de código Python en C](http://cffi.readthedocs.org/en/latest/embedding.html). Esta característica se introdujo hace menos de un mes (!) y para algunos es ["lo más guay que se ha añadido a CFFI hasta la fecha"](https://groups.google.com/d/msg/python-cffi/D6I9spmLwug/SgVm36HTAwAJ). ¿Quién se anima a invertir totalmente esta relación de dependencia?

Vuelvo a señalar que [todo el código está en GitHub](https://github.com/Pybonacci/cffi_test), que se aceptan forks y pull requests y que estoy deseando oír vuestros comentarios sobre esto 🙂 ¿Qué opináis los que usáis Cython para crear wrappers por ejemplo? ¿Cómo puede afectar esto a la expansión de PyPy? ¿Qué echáis en falta?

¡Un saludo y hasta el próximo artículo!