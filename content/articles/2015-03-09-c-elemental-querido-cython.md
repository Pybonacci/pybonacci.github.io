---
title: C elemental, querido Cython
date: 2015-03-09T00:47:23+00:00
author: Kiko Correoso
slug: c-elemental-querido-cython
tags: c, cython, numba, performance, pypy, rendimiento

# Cython, que no CPython

No, no nos hemos equivocado en el título, hoy vamos a hablar de Cython.  
¿Qué es Cython?  
Cython son dos cosas:

*  Por una parte, Cython es un lenguaje de programación (un superconjunto de Python) que une Python con el sistema de tipado estático de C y C++.
*  Por otra parte, `cython` es un compilador que traduce codigo fuente escrito en Cython en eficiente código C o C++. El código resultante se podría usar como una extensión Python o como un ejecutable.

¡Guau! ¿Cómo os habéis quedado?

Lo que se pretende es, básicamente, aprovechar las fortalezas de Python y C, combinar una sintaxis sencilla con el poder y la velocidad.

Salvando algunas [excepciones](http://docs.cython.org/src/userguide/limitations.html#cython-limitations), el código Python (tanto Python 2 como Python 3) es código Cython válido. Además, Cython añade una serie de palabras clave para poder usar el sistema de tipado de C con Python y que el compilador `cython` pueda generar código C eficiente.

Pero, ¿quién usa Cython?  
Pues mira, igual no lo sabes pero seguramente estés usando Cython todos los días. Sage tiene casi medio millón de líneas de Cython (que se dice pronto), Scipy y Pandas más de 20000, scikit-learn unas 15000,...

# ¿Nos empezamos a meter en harina?

La idea principal de este primer acercamiento a Cython será empezar con un código Python que sea nuestro cuello de botella e iremos creando versiones que sean cada vez más rápidas, o eso intentaremos.

Por ejemplo, imaginemos que tenemos que detectar valores mínimos locales dentro de una malla. Los valores mínimos deberán ser simplemente valores más bajos que los que haya en los 8 nodos de su entorno inmediato. En el siguiente gráfico, el nodo en verde será un nodo con un mínimo y en su entorno son todo valores superiores:

<div align="center">
  <table>
    <tr>
      <td style="background:red">
        (2, 0)
      </td>
      
      <td style="background:red">
        (2, 1)
      </td>
      
      <td style="background:red">
        (2, 2)
      </td>
    </tr>
    
    <tr>
      <td style="background:red">
        (1, 0)
      </td>
      
      <td style="background:green">
        (1. 1)
      </td>
      
      <td style="background:red">
        (1, 2)
      </td>
    </tr>
    
    <tr>
      <td style="background:red">
        (0, 0)
      </td>
      
      <td style="background:red">
        (0, 1)
      </td>
      
      <td style="background:red">
        (0, 2)
      </td>
    </tr>
  </table>
</div>

*[INCISO]* Los números y porcentajes que veáis a continuación pueden variar levemente dependiendo de la máquina donde se ejecute. Tomad los valores como aproximativos.

# Setup

Como siempre, importamos algunas librerías antes de empezar a picar código:

    import numpy as np
    import matplotlib.pyplot as plt
    %matplotlib inline

Creamos una matriz cuadrada relativamente grande (4 millones de elementos).

    np.random.seed()
    data = np.random.randn(2000, 2000)

Ya tenemos los datos listos para empezar a trabajar.  
Vamos a crear una función en Python que busque los mínimos tal como los hemos definido.

    def busca_min(malla):
        minimosx = []
        minimosy = []
        for i in range(1, malla.shape[1]-1):
            for j in range(1, malla.shape[]-1):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

Veamos cuanto tarda esta función en mi máquina:

    %timeit busca_min(data)

**OUTPUT:**

    1 loops, best of 3: 3.63 s per loop

Buff, tres segundos y pico en un i7... Si tengo que buscar los mínimos en 500 de estos casos me va a tardar casi media hora.

Por casualidad, vamos a probar numba a ver si es capaz de resolver el problema sin mucho esfuerzo, es código Python muy sencillo en el cual no usamos cosas muy 'extrañas' del lenguaje.

    :::python
    from numba import jit

    @jit
    def busca_min_numba(malla):
        minimosx = []
        minimosy = []
        for i in range(1, malla.shape[1]-1):
            for j in range(1, malla.shape[]-1):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    %timeit busca_min_numba(data)

**OUTPUT:**

    1 loops, best of 3: 4.97 s per loop

Ooooops! Parece que la magia de numba no funciona aquí.

Vamos a especificar los tipos de entrada y de salida (y a modificar el output) a ver si mejora algo:

    :::python
    from numba import jit
    from numba import int32, float64

    @jit(int32[:,:](float64[:,:]))
    def busca_min_numba(malla):
        minimosx = []
        minimosy = []
        for i in range(1, malla.shape[1]-1):
            for j in range(1, malla.shape[]-1):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array([minimosx, minimosy], dtype = np.int32)

    %timeit busca_min_numba(data)

**OUTPUT:**

    1 loops, best of 3: 5.25 s per loop

Pues parece que no, el resultado es del mismo pelo. Usando la opción `nopython` me casca un error un poco feo,...  
Habrá que seguir esperando a que numba esté un poco más maduro. En mis pocas experiencias no he conseguido aun el efecto que buscaba y en la mayoría de los casos obtengo errores muy crípticos. No es que no tenga confianza en la gente que está detrás, solo estoy diciendo que aun no está listo para 'producción'. Esto no pretende ser una guerra Cython/numba, solo he usado numba para ver si a pelo era capaz de mejorar algo el tema. Como no ha sido así, nos olvidamos de numba de momento.

# Cythonizando, que es gerundio (toma 1).

Lo más sencillo y evidente es usar directamente el compilador `cython` y ver si usando el código python tal cual es un poco más rápido. Para ello, vamos a usar las funciones mágicas que Cython pone a nuestra disposición en el notebook. Solo vamos a hablar de la función mágica `%%cython`, de momento, aunque hay otras.

    # antes cythonmagic
    %load_ext Cython

EL comando `%%cython` nos permite escribir código Cython en una celda. Una vez que ejecutamos la celda, IPython se encarga de coger el código, crear un fichero de código Cython con extensión _.pyx_, compilarlo a C y, si todo está correcto, importar ese fichero para que todo esté disponible dentro del notebook.  
[INCISO] a la función mágica `%%cython` le podemos pasar una serie de argumentos. Veremos alguno en este análisis pero ahora vamos a definir uno que sirve para que podamos nombrar a la funcíon que se crea y compila al vuelo, `-n` o `--name`.

    :::python
    %%cython --name probandocython1
    import numpy as np

    def busca_min_cython1(malla):
        minimosx = []
        minimosy = []
        for i in range(1, malla.shape[1]-1):
            for j in range(1, malla.shape[]-1):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

El fichero se creará dentro de la carpeta _cython_ disponible dentro del directorio resultado de la función `get_ipython_cache_dir`. Veamos la localización del fichero en mi equipo:

    from IPython.utils.path import get_ipython_cache_dir

    print(get_ipython_cache_dir() + '/cython/probandocython1.c')

**OUTPUT:**

    /home/kiko/.cache/ipython/cython/probandocython1.c

No lo muestro por aquí porque el resultado son más de ¡¡2400!! líneas de código C.  
Veamos ahora lo que tarda.

    %timeit busca_min_cython1(data)

**OUTPUT:**

    1 loops, best of 3: 3.34 s per loop

Bueno, parece que sin hacer mucho esfuerzo hemos conseguido ganar en torno a un 5% - 25% de rendimiento (dependerá del caso). No es gran cosa pero Cython es capaz de mucho más...

Cythonizando, que es gerundio (toma 2).

En esta parte vamos a introducir una de las palabras clave que Cython introduce para extender Python, `cdef`. La palabra clave `cdef` sirve para 'tipar' estáticamente variables en Cython (luego veremos que se usa también para definir funciones). Por ejemplo:

    cdef int var1, var2
    cdef float var3

En el bloque de código de más arriba he creado dos variables de tipo entero, `var1` y `var2`, y una variable de tipo float, `var3`. Los [tipos anteriores son la nomenclatura C](http://docs.cython.org/src/userguide/language_basics.html#automatic-type-conversions).

Vamos a intentar usar `cdef` con algunos tipos de datos que tenemos dentro de nuestra función. Para empezar, veo evidente que tengo varias listas (`minimosx` y `minimosy`), tenemos los índices de los bucles (`i` y `j`) y voy a convertir los parámetros de los `range` en tipos estáticos (`ii` y `jj`):

    :::python
    %%cython --name probandocython2
    import numpy as np

    def busca_min_cython2(malla):
        cdef list minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        minimosx = []
        minimosy = []
        for i in range(1, ii):
            for j in range(1, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    %timeit busca_min_cython2(data)

**OUTPUT:**

    1 loops, best of 3: 3.55 s per loop

Vaya decepción... No hemos conseguido gran cosa, tenemos un código un poco más largo y estamos peor que en la **toma 1**.  
En realidad, estamos usando objetos Python como listas (no es un tipo C/C++ puro pero Cython lo declara como puntero a algún tipo `struct` de Python) o numpy arrays y no hemos definido las variables de entrada y de salida.  
[INCISO] Cuando existe un tipo Python y C que tienen el mismo nombre (por ejemplo, `int`) predomina el de C (porque es lo deseable, ¿no?).

# Cythonizando, que es gerundio (toma 3).

En Cython existen tres tipos de funciones, las definidas en el espacio Python con `def`, las definidas en el espacio C con `cdef` (sí, lo mismo que usamos para declarar los tipos) y las definidas en ambos espacios con `cpdef`.

*  `def`: ya lo hemos visto y funciona como se espera. Accesible desde Python
*  `cdef`: No es accesible desde Python y la tendremos que envolver con una función Python para poder acceder a la misma.
*  `cpdef`: Es accesible tanto desde Python como desde C y Cython se encargará de hacer el 'envoltorio' para nosotros. Esto meterá un poco más de código y empeorará levemente el rendimiento.

Si definimos una función con `cdef` debería ser una función que se usa internamente dentro del módulo Cython que vayamos a crear y que no sea necesario llamar desde Python.

Veamos un ejemplo de lo dicho anteriormente definiendo la salida de la función como tupla:

    :::python
    %%cython --name probandocython3
    import numpy as np

    cdef tuple cbusca_min_cython3(malla):
        cdef list minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = []
        minimosy = []
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    def busca_min_cython3(malla):
        return cbusca_min_cython3(malla)

    %timeit busca_min_cython3(data)

**OUTPUT:**

    1 loops, best of 3: 3.62 s per loop

Vaya, seguimos sin estar muy a gusto con estos resultados.  
Seguimos sin definir el tipo del valor de entrada.  
La función mágica `%%cython` dispone de una serie de funcionalidades entre la que se encuentra `-a` o `--annotate` (además del `-n` o `--name` que ya hemos visto). Si le pasamos este parámetro podremos ver una representación del código con colores marcando las partes más lentas (amarillo más oscuro) y más optmizadas (más claro) o a la velocidad de C (blanco). Vamos a usarlo para saber donde tenemos cuellos de botella (aplicado a nuestra última versión del código):

    %%cython --annotate
    import numpy as np

    cdef tuple cbusca_min_cython3(malla):
        cdef list minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = []
        minimosy = []
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    def busca_min_cython3(malla):
        return cbusca_min_cython3(malla)

*[INCISO]* En el código a continuación, si pulsáis sobre el símbolo '+' que está delante de cada número de línea podréis ver el código C que se genera

    Generated by Cython 0.22

    +01: import numpy as np

      __pyx_t_1 = __Pyx_Import(__pyx_n_s_numpy, 0, -1); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      if (PyDict_SetItem(__pyx_d, __pyx_n_s_np, __pyx_t_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

     02: 

    +03: cdef tuple cbusca_min_cython3(malla):

    static PyObject *__pyx_f_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_cbusca_min_cython3(PyObject *__pyx_v_malla) {
      PyObject *__pyx_v_minimosx = 0;
      PyObject *__pyx_v_minimosy = 0;
      unsigned int __pyx_v_i;
      unsigned int __pyx_v_j;
      unsigned int __pyx_v_ii;
      unsigned int __pyx_v_jj;
      unsigned int __pyx_v_start;
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("cbusca_min_cython3", 0);
    /* … */
      /* function exit code */
      __pyx_L1_error:;
      __Pyx_XDECREF(__pyx_t_1);
      __Pyx_XDECREF(__pyx_t_2);
      __Pyx_XDECREF(__pyx_t_8);
      __Pyx_XDECREF(__pyx_t_9);
      __Pyx_XDECREF(__pyx_t_12);
      __Pyx_AddTraceback("_cython_magic_b76d9f95ffc9db5b7e97e92e04623490.cbusca_min_cython3", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __pyx_r = 0;
      __pyx_L0:;
      __Pyx_XDECREF(__pyx_v_minimosx);
      __Pyx_XDECREF(__pyx_v_minimosy);
      __Pyx_XGIVEREF(__pyx_r);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

     04:     cdef list minimosx, minimosy

     05:     cdef unsigned int i, j

    +06:     cdef unsigned int ii = malla.shape[1]-1

      __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_v_malla, __pyx_n_s_shape); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_2 = __Pyx_GetItemInt(__pyx_t_1, 1, long, 1, __Pyx_PyInt_From_long, 0, 0, 1); if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
      __Pyx_GOTREF(__pyx_t_2);
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = PyNumber_Subtract(__pyx_t_2, __pyx_int_1); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_3 = __Pyx_PyInt_As_unsigned_int(__pyx_t_1); if (unlikely((__pyx_t_3 == (unsigned int)-1) && PyErr_Occurred())) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_v_ii = __pyx_t_3;

    +07:     cdef unsigned int jj = malla.shape[]-1

      __pyx_t_1 = __Pyx_PyObject_GetAttrStr(__pyx_v_malla, __pyx_n_s_shape); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_2 = __Pyx_GetItemInt(__pyx_t_1, 0, long, 1, __Pyx_PyInt_From_long, 0, 0, 1); if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
      __Pyx_GOTREF(__pyx_t_2);
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = PyNumber_Subtract(__pyx_t_2, __pyx_int_1); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_3 = __Pyx_PyInt_As_unsigned_int(__pyx_t_1); if (unlikely((__pyx_t_3 == (unsigned int)-1) && PyErr_Occurred())) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_v_jj = __pyx_t_3;

    +08:     cdef unsigned int start = 1

      __pyx_v_start = 1;

    +09:     minimosx = []

      __pyx_t_1 = PyList_New(0); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 9; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_v_minimosx = ((PyObject*)__pyx_t_1);
      __pyx_t_1 = 0;

    +10:     minimosy = []

      __pyx_t_1 = PyList_New(0); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 10; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_v_minimosy = ((PyObject*)__pyx_t_1);
      __pyx_t_1 = 0;

    +11:     for i in range(start, ii):

      __pyx_t_3 = __pyx_v_ii;
      for (__pyx_t_4 = __pyx_v_start; __pyx_t_4 < __pyx_t_3; __pyx_t_4+=1) {
        __pyx_v_i = __pyx_t_4;

    +12:         for j in range(start, jj):

        __pyx_t_5 = __pyx_v_jj;
        for (__pyx_t_6 = __pyx_v_start; __pyx_t_6 < __pyx_t_5; __pyx_t_6+=1) {
          __pyx_v_j = __pyx_t_6;

    +13:             if (malla[j, i] < malla[j-1, i-1] and

          __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_2 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_8 = PyTuple_New(2); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_8, 0, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_8, 1, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          __pyx_t_1 = 0;
          __pyx_t_2 = 0;
          __pyx_t_2 = PyObject_GetItem(__pyx_v_malla, __pyx_t_8); if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_2);
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __pyx_t_8 = __Pyx_PyInt_From_long((__pyx_v_j - 1)); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_1 = __Pyx_PyInt_From_long((__pyx_v_i - 1)); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_9 = PyTuple_New(2); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_9, 0, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_9, 1, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          __pyx_t_8 = 0;
          __pyx_t_1 = 0;
          __pyx_t_1 = PyObject_GetItem(__pyx_v_malla, __pyx_t_9); if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_1);
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __pyx_t_9 = PyObject_RichCompare(__pyx_t_2, __pyx_t_1, Py_LT); __Pyx_XGOTREF(__pyx_t_9); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_9); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 13; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +14:                 malla[j, i] < malla[j-1, i] and

          __pyx_t_9 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_2 = PyTuple_New(2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_2, 0, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_2, 1, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          __pyx_t_9 = 0;
          __pyx_t_1 = 0;
          __pyx_t_1 = PyObject_GetItem(__pyx_v_malla, __pyx_t_2); if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_1);
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __pyx_t_2 = __Pyx_PyInt_From_long((__pyx_v_j - 1)); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_9 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_8 = PyTuple_New(2); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_8, 0, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_8, 1, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          __pyx_t_2 = 0;
          __pyx_t_9 = 0;
          __pyx_t_9 = PyObject_GetItem(__pyx_v_malla, __pyx_t_8); if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_9);
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __pyx_t_8 = PyObject_RichCompare(__pyx_t_1, __pyx_t_9, Py_LT); __Pyx_XGOTREF(__pyx_t_8); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_8); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +15:                 malla[j, i] < malla[j-1, i+1] and

          __pyx_t_8 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_9 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_1 = PyTuple_New(2); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_1, 1, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          __pyx_t_8 = 0;
          __pyx_t_9 = 0;
          __pyx_t_9 = PyObject_GetItem(__pyx_v_malla, __pyx_t_1); if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_9);
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_1 = __Pyx_PyInt_From_long((__pyx_v_j - 1)); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_8 = __Pyx_PyInt_From_long((__pyx_v_i + 1)); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_2 = PyTuple_New(2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_2, 0, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_2, 1, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          __pyx_t_1 = 0;
          __pyx_t_8 = 0;
          __pyx_t_8 = PyObject_GetItem(__pyx_v_malla, __pyx_t_2); if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_8);
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __pyx_t_2 = PyObject_RichCompare(__pyx_t_9, __pyx_t_8, Py_LT); __Pyx_XGOTREF(__pyx_t_2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_2); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +16:                 malla[j, i] < malla[j, i-1] and

          __pyx_t_2 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_8 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_9 = PyTuple_New(2); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_9, 0, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_9, 1, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          __pyx_t_2 = 0;
          __pyx_t_8 = 0;
          __pyx_t_8 = PyObject_GetItem(__pyx_v_malla, __pyx_t_9); if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_8);
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __pyx_t_9 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_2 = __Pyx_PyInt_From_long((__pyx_v_i - 1)); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_1 = PyTuple_New(2); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_1, 1, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          __pyx_t_9 = 0;
          __pyx_t_2 = 0;
          __pyx_t_2 = PyObject_GetItem(__pyx_v_malla, __pyx_t_1); if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_2);
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_1 = PyObject_RichCompare(__pyx_t_8, __pyx_t_2, Py_LT); __Pyx_XGOTREF(__pyx_t_1); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_1); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +17:                 malla[j, i] < malla[j, i+1] and

          __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_2 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_8 = PyTuple_New(2); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_8, 0, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_8, 1, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          __pyx_t_1 = 0;
          __pyx_t_2 = 0;
          __pyx_t_2 = PyObject_GetItem(__pyx_v_malla, __pyx_t_8); if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_2);
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __pyx_t_8 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_1 = __Pyx_PyInt_From_long((__pyx_v_i + 1)); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_9 = PyTuple_New(2); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_9, 0, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_9, 1, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          __pyx_t_8 = 0;
          __pyx_t_1 = 0;
          __pyx_t_1 = PyObject_GetItem(__pyx_v_malla, __pyx_t_9); if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_1);
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __pyx_t_9 = PyObject_RichCompare(__pyx_t_2, __pyx_t_1, Py_LT); __Pyx_XGOTREF(__pyx_t_9); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_9); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +18:                 malla[j, i] < malla[j+1, i-1] and

          __pyx_t_9 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_2 = PyTuple_New(2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_2, 0, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_2, 1, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          __pyx_t_9 = 0;
          __pyx_t_1 = 0;
          __pyx_t_1 = PyObject_GetItem(__pyx_v_malla, __pyx_t_2); if (unlikely(__pyx_t_1 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_1);
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __pyx_t_2 = __Pyx_PyInt_From_long((__pyx_v_j + 1)); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_9 = __Pyx_PyInt_From_long((__pyx_v_i - 1)); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_8 = PyTuple_New(2); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_8, 0, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_8, 1, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          __pyx_t_2 = 0;
          __pyx_t_9 = 0;
          __pyx_t_9 = PyObject_GetItem(__pyx_v_malla, __pyx_t_8); if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_9);
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __pyx_t_8 = PyObject_RichCompare(__pyx_t_1, __pyx_t_9, Py_LT); __Pyx_XGOTREF(__pyx_t_8); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_8); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +19:                 malla[j, i] < malla[j+1, i] and

          __pyx_t_8 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_9 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_1 = PyTuple_New(2); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          PyTuple_SET_ITEM(__pyx_t_1, 1, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          __pyx_t_8 = 0;
          __pyx_t_9 = 0;
          __pyx_t_9 = PyObject_GetItem(__pyx_v_malla, __pyx_t_1); if (unlikely(__pyx_t_9 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_9);
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_1 = __Pyx_PyInt_From_long((__pyx_v_j + 1)); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          __pyx_t_8 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_2 = PyTuple_New(2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_2, 0, __pyx_t_1);
          __Pyx_GIVEREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_2, 1, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          __pyx_t_1 = 0;
          __pyx_t_8 = 0;
          __pyx_t_8 = PyObject_GetItem(__pyx_v_malla, __pyx_t_2); if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_8);
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __pyx_t_2 = PyObject_RichCompare(__pyx_t_9, __pyx_t_8, Py_LT); __Pyx_XGOTREF(__pyx_t_2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_2); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          if (__pyx_t_10) {
          } else {
            __pyx_t_7 = __pyx_t_10;
            goto __pyx_L8_bool_binop_done;
          }

    +20:                 malla[j, i] < malla[j+1, i+1]):

          __pyx_t_2 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_8 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_8);
          __pyx_t_9 = PyTuple_New(2); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_9, 0, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          PyTuple_SET_ITEM(__pyx_t_9, 1, __pyx_t_8);
          __Pyx_GIVEREF(__pyx_t_8);
          __pyx_t_2 = 0;
          __pyx_t_8 = 0;
          __pyx_t_8 = PyObject_GetItem(__pyx_v_malla, __pyx_t_9); if (unlikely(__pyx_t_8 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_8);
          __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
          __pyx_t_9 = __Pyx_PyInt_From_long((__pyx_v_j + 1)); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_9);
          __pyx_t_2 = __Pyx_PyInt_From_long((__pyx_v_i + 1)); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_2);
          __pyx_t_1 = PyTuple_New(2); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_GOTREF(__pyx_t_1);
          PyTuple_SET_ITEM(__pyx_t_1, 0, __pyx_t_9);
          __Pyx_GIVEREF(__pyx_t_9);
          PyTuple_SET_ITEM(__pyx_t_1, 1, __pyx_t_2);
          __Pyx_GIVEREF(__pyx_t_2);
          __pyx_t_9 = 0;
          __pyx_t_2 = 0;
          __pyx_t_2 = PyObject_GetItem(__pyx_v_malla, __pyx_t_1); if (unlikely(__pyx_t_2 == NULL)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;};
          __Pyx_GOTREF(__pyx_t_2);
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_1 = PyObject_RichCompare(__pyx_t_8, __pyx_t_2, Py_LT); __Pyx_XGOTREF(__pyx_t_1); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
          __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
          __pyx_t_10 = __Pyx_PyObject_IsTrue(__pyx_t_1); if (unlikely(__pyx_t_10 < 0)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
          __pyx_t_7 = __pyx_t_10;
          __pyx_L8_bool_binop_done:;
          if (__pyx_t_7) {

    +21:                 minimosx.append(i)

            __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_GOTREF(__pyx_t_1);
            __pyx_t_11 = __Pyx_PyList_Append(__pyx_v_minimosx, __pyx_t_1); if (unlikely(__pyx_t_11 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

    +22:                 minimosy.append(j)

            __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_GOTREF(__pyx_t_1);
            __pyx_t_11 = __Pyx_PyList_Append(__pyx_v_minimosy, __pyx_t_1); if (unlikely(__pyx_t_11 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
            goto __pyx_L7;
          }
          __pyx_L7:;
        }
      }

     23: 

    +24:     return np.array(minimosx), np.array(minimosy)

      __Pyx_XDECREF(__pyx_r);
      __pyx_t_2 = __Pyx_GetModuleGlobalName(__pyx_n_s_np); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_2);
      __pyx_t_8 = __Pyx_PyObject_GetAttrStr(__pyx_t_2, __pyx_n_s_array); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_8);
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = NULL;
      if (CYTHON_COMPILING_IN_CPYTHON && unlikely(PyMethod_Check(__pyx_t_8))) {
        __pyx_t_2 = PyMethod_GET_SELF(__pyx_t_8);
        if (likely(__pyx_t_2)) {
          PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_8);
          __Pyx_INCREF(__pyx_t_2);
          __Pyx_INCREF(function);
          __Pyx_DECREF_SET(__pyx_t_8, function);
        }
      }
      if (!__pyx_t_2) {
        __pyx_t_1 = __Pyx_PyObject_CallOneArg(__pyx_t_8, __pyx_v_minimosx); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_1);
      } else {
        __pyx_t_9 = PyTuple_New(1+1); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_9);
        PyTuple_SET_ITEM(__pyx_t_9, 0, __pyx_t_2); __Pyx_GIVEREF(__pyx_t_2); __pyx_t_2 = NULL;
        __Pyx_INCREF(__pyx_v_minimosx);
        PyTuple_SET_ITEM(__pyx_t_9, 0+1, __pyx_v_minimosx);
        __Pyx_GIVEREF(__pyx_v_minimosx);
        __pyx_t_1 = __Pyx_PyObject_Call(__pyx_t_8, __pyx_t_9, NULL); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_1);
        __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
      }
      __Pyx_DECREF(__pyx_t_8); __pyx_t_8 = 0;
      __pyx_t_9 = __Pyx_GetModuleGlobalName(__pyx_n_s_np); if (unlikely(!__pyx_t_9)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_9);
      __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_9, __pyx_n_s_array); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_2);
      __Pyx_DECREF(__pyx_t_9); __pyx_t_9 = 0;
      __pyx_t_9 = NULL;
      if (CYTHON_COMPILING_IN_CPYTHON && unlikely(PyMethod_Check(__pyx_t_2))) {
        __pyx_t_9 = PyMethod_GET_SELF(__pyx_t_2);
        if (likely(__pyx_t_9)) {
          PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_2);
          __Pyx_INCREF(__pyx_t_9);
          __Pyx_INCREF(function);
          __Pyx_DECREF_SET(__pyx_t_2, function);
        }
      }
      if (!__pyx_t_9) {
        __pyx_t_8 = __Pyx_PyObject_CallOneArg(__pyx_t_2, __pyx_v_minimosy); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_8);
      } else {
        __pyx_t_12 = PyTuple_New(1+1); if (unlikely(!__pyx_t_12)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_12);
        PyTuple_SET_ITEM(__pyx_t_12, 0, __pyx_t_9); __Pyx_GIVEREF(__pyx_t_9); __pyx_t_9 = NULL;
        __Pyx_INCREF(__pyx_v_minimosy);
        PyTuple_SET_ITEM(__pyx_t_12, 0+1, __pyx_v_minimosy);
        __Pyx_GIVEREF(__pyx_v_minimosy);
        __pyx_t_8 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_t_12, NULL); if (unlikely(!__pyx_t_8)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_8);
        __Pyx_DECREF(__pyx_t_12); __pyx_t_12 = 0;
      }
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __pyx_t_2 = PyTuple_New(2); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_2);
      PyTuple_SET_ITEM(__pyx_t_2, 0, __pyx_t_1);
      __Pyx_GIVEREF(__pyx_t_1);
      PyTuple_SET_ITEM(__pyx_t_2, 1, __pyx_t_8);
      __Pyx_GIVEREF(__pyx_t_8);
      __pyx_t_1 = 0;
      __pyx_t_8 = 0;
      __pyx_r = ((PyObject*)__pyx_t_2);
      __pyx_t_2 = 0;
      goto __pyx_L0;

     25: 

    +26: def busca_min_cython3(malla):

    /* Python wrapper */
    static PyObject *__pyx_pw_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3(PyObject *__pyx_self, PyObject *__pyx_v_malla); /*proto*/
    static PyMethodDef __pyx_mdef_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3 = {"busca_min_cython3", (PyCFunction)__pyx_pw_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3, METH_O, 0};
    static PyObject *__pyx_pw_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3(PyObject *__pyx_self, PyObject *__pyx_v_malla) {
      PyObject *__pyx_r = 0;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython3 (wrapper)", 0);
      __pyx_r = __pyx_pf_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_busca_min_cython3(__pyx_self, ((PyObject *)__pyx_v_malla));

      /* function exit code */
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    static PyObject *__pyx_pf_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_busca_min_cython3(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_malla) {
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython3", 0);
    /* … */
      /* function exit code */
      __pyx_L1_error:;
      __Pyx_XDECREF(__pyx_t_1);
      __Pyx_AddTraceback("_cython_magic_b76d9f95ffc9db5b7e97e92e04623490.busca_min_cython3", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __pyx_r = NULL;
      __pyx_L0:;
      __Pyx_XGIVEREF(__pyx_r);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }
    /* … */
      __pyx_tuple_ = PyTuple_Pack(1, __pyx_n_s_malla); if (unlikely(!__pyx_tuple_)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_tuple_);
      __Pyx_GIVEREF(__pyx_tuple_);
    /* … */
      __pyx_t_1 = PyCFunction_NewEx(&__pyx_mdef_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_1busca_min_cython3, NULL, __pyx_n_s_cython_magic_b76d9f95ffc9db5b7e); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      if (PyDict_SetItem(__pyx_d, __pyx_n_s_busca_min_cython3, __pyx_t_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

    +27:     return cbusca_min_cython3(malla)

      __Pyx_XDECREF(__pyx_r);
      __pyx_t_1 = __pyx_f_46_cython_magic_b76d9f95ffc9db5b7e97e92e04623490_cbusca_min_cython3(__pyx_v_malla); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 27; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_r = __pyx_t_1;
      __pyx_t_1 = 0;
      goto __pyx_L0;

El `if` parece la parte más lenta. Estamos usando el valor de entrada que no tiene un tipo Cython definido.  
Los bucles parece que están optimizados (las variables envueltas en el bucle las hemos declarado como `unsigned int`).  
Pero todas las partes por las que pasa el numpy array parece que no están muy optimizadas...

# Cythonizando, que es gerundio (toma 4).

Ahora mismo, haciendo `import numpy as np` tenemos acceso a la funcionalidad Python de numpy. Para poder acceder a la funcionalidad C de numpy hemos de hacer un `cimport` de numpy.  
El `cimport` se usa para importar información especial del módulo numpy en el momento de compilación. Esta información se encuentra en el fichero numpy.pxd que es parte de la distribución Cython. El `cimport` también se usa para poder importar desde la _stdlib_ de C.  
Vamos a usar esto para declarar el tipo del array de numpy.

    %%cython --name probandocython4
    import numpy as np
    cimport numpy as np

    cpdef tuple busca_min_cython4(np.ndarray[double, ndim = 2] malla):
        cdef list minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = []
        minimosy = []
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    %timeit busca_min_cython4(data)

**OUTPUT:**

    10 loops, best of 3: 147 ms per loop

Guauuuu!!! Acabamos de obtener un incremento de entre 25x a 30x veces más rápido.

Vamos a comprobar que el resultado sea el mismo que la función original:

    a, b = busca_min(data)
    print(a)
    print(b)

**OUTPUT:**

    [   1    1    1 ..., 1998 1998 1998]
    [   1    3   11 ..., 1968 1977 1985]

<br>

    aa, bb = busca_min_cython4(data)
    print(aa)
    print(bb)

**OUTPUT:**

    [   1    1    1 ..., 1998 1998 1998]
    [   1    3   11 ..., 1968 1977 1985]

<br>

    print(np.array_equal(a, aa))

**OUTPUT:**

    True

<br>

    print(np.array_equal(b, bb))

**OUTPUT:**

    True

Pues parece que sí 🙂

Vamos a ver si hemos dejado la mayoría del código anterior en blanco o más clarito usando `--annotate`.

    %%cython --annotate
    import numpy as np
    cimport numpy as np

    cpdef tuple busca_min_cython4(np.ndarray[double, ndim = 2] malla):
        cdef list minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = []
        minimosy = []
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

 **OUTPUT:** 
  
    Generated by Cython 0.22

    +01: import numpy as np

      __pyx_t_1 = __Pyx_Import(__pyx_n_s_numpy, 0, -1); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      if (PyDict_SetItem(__pyx_d, __pyx_n_s_np, __pyx_t_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
    /* … */
      __pyx_t_1 = PyDict_New(); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      if (PyDict_SetItem(__pyx_d, __pyx_n_s_test, __pyx_t_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

     02: cimport numpy as np

     03: 

    +04: cpdef tuple busca_min_cython4(np.ndarray[double, ndim = 2] malla):

    static PyObject *__pyx_pw_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_1busca_min_cython4(PyObject *__pyx_self, PyObject *__pyx_v_malla); /*proto*/
    static PyObject *__pyx_f_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(PyArrayObject *__pyx_v_malla, CYTHON_UNUSED int __pyx_skip_dispatch) {
      PyObject *__pyx_v_minimosx = 0;
      PyObject *__pyx_v_minimosy = 0;
      unsigned int __pyx_v_i;
      unsigned int __pyx_v_j;
      unsigned int __pyx_v_ii;
      unsigned int __pyx_v_jj;
      unsigned int __pyx_v_start;
      __Pyx_LocalBuf_ND __pyx_pybuffernd_malla;
      __Pyx_Buffer __pyx_pybuffer_malla;
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython4", 0);
      __pyx_pybuffer_malla.pybuffer.buf = NULL;
      __pyx_pybuffer_malla.refcount = 0;
      __pyx_pybuffernd_malla.data = NULL;
      __pyx_pybuffernd_malla.rcbuffer = &__pyx_pybuffer_malla;
      {
        __Pyx_BufFmt_StackElem __pyx_stack[1];
        if (unlikely(__Pyx_GetBufferAndValidate(&__pyx_pybuffernd_malla.rcbuffer->pybuffer, (PyObject*)__pyx_v_malla, &__Pyx_TypeInfo_double, PyBUF_FORMAT| PyBUF_STRIDES, 2, 0, __pyx_stack) == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      }
      __pyx_pybuffernd_malla.diminfo[0].strides = __pyx_pybuffernd_malla.rcbuffer->pybuffer.strides[0]; __pyx_pybuffernd_malla.diminfo[0].shape = __pyx_pybuffernd_malla.rcbuffer->pybuffer.shape[0]; __pyx_pybuffernd_malla.diminfo[1].strides = __pyx_pybuffernd_malla.rcbuffer->pybuffer.strides[1]; __pyx_pybuffernd_malla.diminfo[1].shape = __pyx_pybuffernd_malla.rcbuffer->pybuffer.shape[1];
    /* … */
      /* function exit code */
      __pyx_L1_error:;
      __Pyx_XDECREF(__pyx_t_1);
      __Pyx_XDECREF(__pyx_t_42);
      __Pyx_XDECREF(__pyx_t_43);
      __Pyx_XDECREF(__pyx_t_44);
      __Pyx_XDECREF(__pyx_t_45);
      { PyObject *__pyx_type, *__pyx_value, *__pyx_tb;
        __Pyx_ErrFetch(&__pyx_type, &__pyx_value, &__pyx_tb);
        __Pyx_SafeReleaseBuffer(&__pyx_pybuffernd_malla.rcbuffer->pybuffer);
      __Pyx_ErrRestore(__pyx_type, __pyx_value, __pyx_tb);}
      __Pyx_AddTraceback("_cython_magic_db10c794e43f00f7b90f23a8e05093c1.busca_min_cython4", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __pyx_r = 0;
      goto __pyx_L2;
      __pyx_L0:;
      __Pyx_SafeReleaseBuffer(&__pyx_pybuffernd_malla.rcbuffer->pybuffer);
      __pyx_L2:;
      __Pyx_XDECREF(__pyx_v_minimosx);
      __Pyx_XDECREF(__pyx_v_minimosy);
      __Pyx_XGIVEREF(__pyx_r);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    /* Python wrapper */
    static PyObject *__pyx_pw_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_1busca_min_cython4(PyObject *__pyx_self, PyObject *__pyx_v_malla); /*proto*/
    static PyObject *__pyx_pw_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_1busca_min_cython4(PyObject *__pyx_self, PyObject *__pyx_v_malla) {
      PyObject *__pyx_r = 0;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython4 (wrapper)", 0);
      if (unlikely(!__Pyx_ArgTypeTest(((PyObject *)__pyx_v_malla), __pyx_ptype_5numpy_ndarray, 1, "malla", 0))) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __pyx_r = __pyx_pf_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(__pyx_self, ((PyArrayObject *)__pyx_v_malla));
      CYTHON_UNUSED int __pyx_lineno = 0;
      CYTHON_UNUSED const char *__pyx_filename = NULL;
      CYTHON_UNUSED int __pyx_clineno = 0;

      /* function exit code */
      goto __pyx_L0;
      __pyx_L1_error:;
      __pyx_r = NULL;
      __pyx_L0:;
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    static PyObject *__pyx_pf_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(CYTHON_UNUSED PyObject *__pyx_self, PyArrayObject *__pyx_v_malla) {
      __Pyx_LocalBuf_ND __pyx_pybuffernd_malla;
      __Pyx_Buffer __pyx_pybuffer_malla;
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython4", 0);
      __pyx_pybuffer_malla.pybuffer.buf = NULL;
      __pyx_pybuffer_malla.refcount = 0;
      __pyx_pybuffernd_malla.data = NULL;
      __pyx_pybuffernd_malla.rcbuffer = &__pyx_pybuffer_malla;
      {
        __Pyx_BufFmt_StackElem __pyx_stack[1];
        if (unlikely(__Pyx_GetBufferAndValidate(&__pyx_pybuffernd_malla.rcbuffer->pybuffer, (PyObject*)__pyx_v_malla, &__Pyx_TypeInfo_double, PyBUF_FORMAT| PyBUF_STRIDES, 2, 0, __pyx_stack) == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      }
      __pyx_pybuffernd_malla.diminfo[0].strides = __pyx_pybuffernd_malla.rcbuffer->pybuffer.strides[0]; __pyx_pybuffernd_malla.diminfo[0].shape = __pyx_pybuffernd_malla.rcbuffer->pybuffer.shape[0]; __pyx_pybuffernd_malla.diminfo[1].strides = __pyx_pybuffernd_malla.rcbuffer->pybuffer.strides[1]; __pyx_pybuffernd_malla.diminfo[1].shape = __pyx_pybuffernd_malla.rcbuffer->pybuffer.shape[1];
      __Pyx_XDECREF(__pyx_r);
      __pyx_t_1 = __pyx_f_46_cython_magic_db10c794e43f00f7b90f23a8e05093c1_busca_min_cython4(__pyx_v_malla, 0); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_r = __pyx_t_1;
      __pyx_t_1 = 0;
      goto __pyx_L0;

      /* function exit code */
      __pyx_L1_error:;
      __Pyx_XDECREF(__pyx_t_1);
      { PyObject *__pyx_type, *__pyx_value, *__pyx_tb;
        __Pyx_ErrFetch(&__pyx_type, &__pyx_value, &__pyx_tb);
        __Pyx_SafeReleaseBuffer(&__pyx_pybuffernd_malla.rcbuffer->pybuffer);
      __Pyx_ErrRestore(__pyx_type, __pyx_value, __pyx_tb);}
      __Pyx_AddTraceback("_cython_magic_db10c794e43f00f7b90f23a8e05093c1.busca_min_cython4", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __pyx_r = NULL;
      goto __pyx_L2;
      __pyx_L0:;
      __Pyx_SafeReleaseBuffer(&__pyx_pybuffernd_malla.rcbuffer->pybuffer);
      __pyx_L2:;
      __Pyx_XGIVEREF(__pyx_r);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

     05:     cdef list minimosx, minimosy

     06:     cdef unsigned int i, j

    +07:     cdef unsigned int ii = malla.shape[1]-1

      __pyx_v_ii = ((__pyx_v_malla->dimensions[1]) - 1);

    +08:     cdef unsigned int jj = malla.shape[]-1

      __pyx_v_jj = ((__pyx_v_malla->dimensions[0]) - 1);

    +09:     cdef unsigned int start = 1

      __pyx_v_start = 1;

    +10:     minimosx = []

      __pyx_t_1 = PyList_New(0); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 10; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_v_minimosx = ((PyObject*)__pyx_t_1);
      __pyx_t_1 = 0;

    +11:     minimosy = []

      __pyx_t_1 = PyList_New(0); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 11; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_v_minimosy = ((PyObject*)__pyx_t_1);
      __pyx_t_1 = 0;

    +12:     for i in range(start, ii):

      __pyx_t_2 = __pyx_v_ii;
      for (__pyx_t_3 = __pyx_v_start; __pyx_t_3 < __pyx_t_2; __pyx_t_3+=1) {
        __pyx_v_i = __pyx_t_3;

    +13:         for j in range(start, jj):

        __pyx_t_4 = __pyx_v_jj;
        for (__pyx_t_5 = __pyx_v_start; __pyx_t_5 < __pyx_t_4; __pyx_t_5+=1) {
          __pyx_v_j = __pyx_t_5;

    +14:             if (malla[j, i] < malla[j-1, i-1] and

          __pyx_t_7 = __pyx_v_j;
          __pyx_t_8 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_7 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_8 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_10 = (__pyx_v_j - 1);
          __pyx_t_11 = (__pyx_v_i - 1);
          __pyx_t_9 = -1;
          if (__pyx_t_10 < 0) {
            __pyx_t_10 += __pyx_pybuffernd_malla.diminfo[0].shape;
            if (unlikely(__pyx_t_10 < 0)) __pyx_t_9 = 0;
          } else if (unlikely(__pyx_t_10 >= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (__pyx_t_11 < 0) {
            __pyx_t_11 += __pyx_pybuffernd_malla.diminfo[1].shape;
            if (unlikely(__pyx_t_11 < 0)) __pyx_t_9 = 1;
          } else if (unlikely(__pyx_t_11 >= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 14; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_7, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_8, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_10, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_11, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +15:                 malla[j, i] < malla[j-1, i] and

          __pyx_t_13 = __pyx_v_j;
          __pyx_t_14 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_13 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_14 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_15 = (__pyx_v_j - 1);
          __pyx_t_16 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (__pyx_t_15 < 0) {
            __pyx_t_15 += __pyx_pybuffernd_malla.diminfo[0].shape;
            if (unlikely(__pyx_t_15 < 0)) __pyx_t_9 = 0;
          } else if (unlikely(__pyx_t_15 >= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_16 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_13, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_14, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_15, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_16, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +16:                 malla[j, i] < malla[j-1, i+1] and

          __pyx_t_17 = __pyx_v_j;
          __pyx_t_18 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_17 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_18 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_19 = (__pyx_v_j - 1);
          __pyx_t_20 = (__pyx_v_i + 1);
          __pyx_t_9 = -1;
          if (__pyx_t_19 < 0) {
            __pyx_t_19 += __pyx_pybuffernd_malla.diminfo[0].shape;
            if (unlikely(__pyx_t_19 < 0)) __pyx_t_9 = 0;
          } else if (unlikely(__pyx_t_19 >= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (__pyx_t_20 < 0) {
            __pyx_t_20 += __pyx_pybuffernd_malla.diminfo[1].shape;
            if (unlikely(__pyx_t_20 < 0)) __pyx_t_9 = 1;
          } else if (unlikely(__pyx_t_20 >= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_17, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_18, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_19, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_20, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +17:                 malla[j, i] < malla[j, i-1] and

          __pyx_t_21 = __pyx_v_j;
          __pyx_t_22 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_21 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_22 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_23 = __pyx_v_j;
          __pyx_t_24 = (__pyx_v_i - 1);
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_23 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (__pyx_t_24 < 0) {
            __pyx_t_24 += __pyx_pybuffernd_malla.diminfo[1].shape;
            if (unlikely(__pyx_t_24 < 0)) __pyx_t_9 = 1;
          } else if (unlikely(__pyx_t_24 >= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_21, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_22, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_23, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_24, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +18:                 malla[j, i] < malla[j, i+1] and

          __pyx_t_25 = __pyx_v_j;
          __pyx_t_26 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_25 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_26 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_27 = __pyx_v_j;
          __pyx_t_28 = (__pyx_v_i + 1);
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_27 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (__pyx_t_28 < 0) {
            __pyx_t_28 += __pyx_pybuffernd_malla.diminfo[1].shape;
            if (unlikely(__pyx_t_28 < 0)) __pyx_t_9 = 1;
          } else if (unlikely(__pyx_t_28 >= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_25, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_26, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_27, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_28, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +19:                 malla[j, i] < malla[j+1, i-1] and

          __pyx_t_29 = __pyx_v_j;
          __pyx_t_30 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_29 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_30 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_31 = (__pyx_v_j + 1);
          __pyx_t_32 = (__pyx_v_i - 1);
          __pyx_t_9 = -1;
          if (__pyx_t_31 < 0) {
            __pyx_t_31 += __pyx_pybuffernd_malla.diminfo[0].shape;
            if (unlikely(__pyx_t_31 < 0)) __pyx_t_9 = 0;
          } else if (unlikely(__pyx_t_31 >= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (__pyx_t_32 < 0) {
            __pyx_t_32 += __pyx_pybuffernd_malla.diminfo[1].shape;
            if (unlikely(__pyx_t_32 < 0)) __pyx_t_9 = 1;
          } else if (unlikely(__pyx_t_32 >= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 19; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_29, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_30, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_31, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_32, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +20:                 malla[j, i] < malla[j+1, i] and

          __pyx_t_33 = __pyx_v_j;
          __pyx_t_34 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_33 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_34 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_35 = (__pyx_v_j + 1);
          __pyx_t_36 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (__pyx_t_35 < 0) {
            __pyx_t_35 += __pyx_pybuffernd_malla.diminfo[0].shape;
            if (unlikely(__pyx_t_35 < 0)) __pyx_t_9 = 0;
          } else if (unlikely(__pyx_t_35 >= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_36 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_33, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_34, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_35, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_36, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          if (__pyx_t_12) {
          } else {
            __pyx_t_6 = __pyx_t_12;
            goto __pyx_L8_bool_binop_done;
          }

    +21:                 malla[j, i] < malla[j+1, i+1]):

          __pyx_t_37 = __pyx_v_j;
          __pyx_t_38 = __pyx_v_i;
          __pyx_t_9 = -1;
          if (unlikely(__pyx_t_37 >= (size_t)__pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (unlikely(__pyx_t_38 >= (size_t)__pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_39 = (__pyx_v_j + 1);
          __pyx_t_40 = (__pyx_v_i + 1);
          __pyx_t_9 = -1;
          if (__pyx_t_39 < 0) {
            __pyx_t_39 += __pyx_pybuffernd_malla.diminfo[0].shape;
            if (unlikely(__pyx_t_39 < 0)) __pyx_t_9 = 0;
          } else if (unlikely(__pyx_t_39 >= __pyx_pybuffernd_malla.diminfo[0].shape)) __pyx_t_9 = 0;
          if (__pyx_t_40 < 0) {
            __pyx_t_40 += __pyx_pybuffernd_malla.diminfo[1].shape;
            if (unlikely(__pyx_t_40 < 0)) __pyx_t_9 = 1;
          } else if (unlikely(__pyx_t_40 >= __pyx_pybuffernd_malla.diminfo[1].shape)) __pyx_t_9 = 1;
          if (unlikely(__pyx_t_9 != -1)) {
            __Pyx_RaiseBufferIndexError(__pyx_t_9);
            {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
          }
          __pyx_t_12 = (((*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_37, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_38, __pyx_pybuffernd_malla.diminfo[1].strides)) < (*__Pyx_BufPtrStrided2d(double *, __pyx_pybuffernd_malla.rcbuffer->pybuffer.buf, __pyx_t_39, __pyx_pybuffernd_malla.diminfo[0].strides, __pyx_t_40, __pyx_pybuffernd_malla.diminfo[1].strides))) != 0);
          __pyx_t_6 = __pyx_t_12;
          __pyx_L8_bool_binop_done:;
          if (__pyx_t_6) {

    +22:                 minimosx.append(i)

            __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_i); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_GOTREF(__pyx_t_1);
            __pyx_t_41 = __Pyx_PyList_Append(__pyx_v_minimosx, __pyx_t_1); if (unlikely(__pyx_t_41 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;

    +23:                 minimosy.append(j)

            __pyx_t_1 = __Pyx_PyInt_From_unsigned_int(__pyx_v_j); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_GOTREF(__pyx_t_1);
            __pyx_t_41 = __Pyx_PyList_Append(__pyx_v_minimosy, __pyx_t_1); if (unlikely(__pyx_t_41 == -1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
            __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
            goto __pyx_L7;
          }
          __pyx_L7:;
        }
      }

     24: 

    +25:     return np.array(minimosx), np.array(minimosy)

      __Pyx_XDECREF(__pyx_r);
      __pyx_t_42 = __Pyx_GetModuleGlobalName(__pyx_n_s_np); if (unlikely(!__pyx_t_42)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_42);
      __pyx_t_43 = __Pyx_PyObject_GetAttrStr(__pyx_t_42, __pyx_n_s_array); if (unlikely(!__pyx_t_43)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_43);
      __Pyx_DECREF(__pyx_t_42); __pyx_t_42 = 0;
      __pyx_t_42 = NULL;
      if (CYTHON_COMPILING_IN_CPYTHON && unlikely(PyMethod_Check(__pyx_t_43))) {
        __pyx_t_42 = PyMethod_GET_SELF(__pyx_t_43);
        if (likely(__pyx_t_42)) {
          PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_43);
          __Pyx_INCREF(__pyx_t_42);
          __Pyx_INCREF(function);
          __Pyx_DECREF_SET(__pyx_t_43, function);
        }
      }
      if (!__pyx_t_42) {
        __pyx_t_1 = __Pyx_PyObject_CallOneArg(__pyx_t_43, __pyx_v_minimosx); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_1);
      } else {
        __pyx_t_44 = PyTuple_New(1+1); if (unlikely(!__pyx_t_44)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_44);
        PyTuple_SET_ITEM(__pyx_t_44, 0, __pyx_t_42); __Pyx_GIVEREF(__pyx_t_42); __pyx_t_42 = NULL;
        __Pyx_INCREF(__pyx_v_minimosx);
        PyTuple_SET_ITEM(__pyx_t_44, 0+1, __pyx_v_minimosx);
        __Pyx_GIVEREF(__pyx_v_minimosx);
        __pyx_t_1 = __Pyx_PyObject_Call(__pyx_t_43, __pyx_t_44, NULL); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_1);
        __Pyx_DECREF(__pyx_t_44); __pyx_t_44 = 0;
      }
      __Pyx_DECREF(__pyx_t_43); __pyx_t_43 = 0;
      __pyx_t_44 = __Pyx_GetModuleGlobalName(__pyx_n_s_np); if (unlikely(!__pyx_t_44)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_44);
      __pyx_t_42 = __Pyx_PyObject_GetAttrStr(__pyx_t_44, __pyx_n_s_array); if (unlikely(!__pyx_t_42)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_42);
      __Pyx_DECREF(__pyx_t_44); __pyx_t_44 = 0;
      __pyx_t_44 = NULL;
      if (CYTHON_COMPILING_IN_CPYTHON && unlikely(PyMethod_Check(__pyx_t_42))) {
        __pyx_t_44 = PyMethod_GET_SELF(__pyx_t_42);
        if (likely(__pyx_t_44)) {
          PyObject* function = PyMethod_GET_FUNCTION(__pyx_t_42);
          __Pyx_INCREF(__pyx_t_44);
          __Pyx_INCREF(function);
          __Pyx_DECREF_SET(__pyx_t_42, function);
        }
      }
      if (!__pyx_t_44) {
        __pyx_t_43 = __Pyx_PyObject_CallOneArg(__pyx_t_42, __pyx_v_minimosy); if (unlikely(!__pyx_t_43)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_43);
      } else {
        __pyx_t_45 = PyTuple_New(1+1); if (unlikely(!__pyx_t_45)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_45);
        PyTuple_SET_ITEM(__pyx_t_45, 0, __pyx_t_44); __Pyx_GIVEREF(__pyx_t_44); __pyx_t_44 = NULL;
        __Pyx_INCREF(__pyx_v_minimosy);
        PyTuple_SET_ITEM(__pyx_t_45, 0+1, __pyx_v_minimosy);
        __Pyx_GIVEREF(__pyx_v_minimosy);
        __pyx_t_43 = __Pyx_PyObject_Call(__pyx_t_42, __pyx_t_45, NULL); if (unlikely(!__pyx_t_43)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
        __Pyx_GOTREF(__pyx_t_43);
        __Pyx_DECREF(__pyx_t_45); __pyx_t_45 = 0;
      }
      __Pyx_DECREF(__pyx_t_42); __pyx_t_42 = 0;
      __pyx_t_42 = PyTuple_New(2); if (unlikely(!__pyx_t_42)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_42);
      PyTuple_SET_ITEM(__pyx_t_42, 0, __pyx_t_1);
      __Pyx_GIVEREF(__pyx_t_1);
      PyTuple_SET_ITEM(__pyx_t_42, 1, __pyx_t_43);
      __Pyx_GIVEREF(__pyx_t_43);
      __pyx_t_1 = 0;
      __pyx_t_43 = 0;
      __pyx_r = ((PyObject*)__pyx_t_42);
      __pyx_t_42 = 0;
      goto __pyx_L0;

Vemos que muchas de las partes oscuras ahora son más claras!!! Pero parece que sigue quedando espacio para la mejora.

# Cythonizando, que es gerundio (toma 5).

Vamos a ver si definiendo el tipo del resultado de la función como un numpy array en lugar de como una tupla nos introduce alguna mejora:

    %%cython --name probandocython5
    import numpy as np
    cimport numpy as np

    cpdef np.ndarray[int, ndim = 2] busca_min_cython5(np.ndarray[double, ndim = 2] malla):
        cdef list minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = []
        minimosy = []
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array([minimosx, minimosy])

    %timeit busca_min_cython5(data)

**OUTPUT:**

    10 loops, best of 3: 137 ms per loop

Vaya, parece que con respecto a la versión anterior solo obtenemos una ganancia de un 2% - 4%.

# Cythonizando, que es gerundio (toma 6).

Vamos a dejar de usar listas y vamos a usar numpy arrays vacios que iremos 'rellenando' con `numpy.append`. A ver si usando todo numpy arrays conseguimos algún tipo de mejora:

    %%cython --name probandocython6
    import numpy as np
    cimport numpy as np

    cpdef tuple busca_min_cython6(np.ndarray[double, ndim = 2] malla):
        cdef np.ndarray[long, ndim = 1] minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = np.array([], dtype = np.int)
        minimosy = np.array([], dtype = np.int)
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    np.append(minimosx, i)
                    np.append(minimosy, j)

        return minimosx, minimosy

    %timeit busca_min_cython6(data)

**OUTPUT:**

    1 loops, best of 3: 5.59 s per loop

En realidad, en la anterior porción de código estoy usando algo muy ineficiente. La función `numpy.append` no funciona como una lista a la que vas anexando elementos. Lo que estamos haciendo en realidad es crear copias del array existente para convertirlo a un nuevo array con un elemento nuevo. Esto no es lo que pretendiamos!!!!

# Cythonizando, que es gerundio (toma 7).

En Python existen [arrays](https://docs.python.org/3.4/library/array.html) eficientes para valores numéricos (según reza la documentación) que también pueden ser usados de la forma en que estoy usando las listas en mi función (arrays vacios a los que les vamos añadiendo elementos). Vamos a usarlos con Cython.

    %%cython --name probandocython7
    import numpy as np
    cimport numpy as np
    from cpython cimport array as c_array
    from array import array

    cpdef tuple busca_min_cython7(np.ndarray[double, ndim = 2] malla):
        cdef c_array.array minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = array('L', [])
        minimosy = array('L', []) 
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    %timeit busca_min_cython7(data)

**OUTPUT:**

    10 loops, best of 3: 98.1 ms per loop

Parece que hemos ganado otro 25% - 30% con respecto a lo anterior más eficiente que habíamos conseguido. Con respecto a la implementación inicial en Python puro tenemos una mejora de 30x - 35x veces la velocidad inicial.  
Vamos a comprobar si seguimos teniendo los mismos resultados.

    a, b = busca_min(data)
    print(a)
    print(b)
    aa, bb = busca_min_cython7(data)
    print(aa)
    print(bb)
    print(np.array_equal(a, aa))
    print(np.array_equal(b, bb))

**OUTPUT:**

    [   1    1    1 ..., 1998 1998 1998]
    [   1    3   11 ..., 1968 1977 1985]
    [   1    1    1 ..., 1998 1998 1998]
    [   1    3   11 ..., 1968 1977 1985]
    True
    True

¿Qué pasa si el tamaño del array se incrementa?

    data2 = np.random.randn(5000, 5000)
    %timeit busca_min(data2)
    %timeit busca_min_cython7(data2)

**OUTPUT:**

    1 loops, best of 3: 24.6 s per loop
    1 loops, best of 3: 687 ms per loop

<br>

    a, b = busca_min(data2)
    print(a)
    print(b)
    aa, bb = busca_min_cython7(data2)
    print(aa)
    print(bb)
    print(np.array_equal(a, aa))
    print(np.array_equal(b, bb))

**OUTPUT:**

    [   1    1    1 ..., 4998 4998 4998]
    [   7   12   18 ..., 4975 4978 4983]
    [   1    1    1 ..., 4998 4998 4998]
    [   7   12   18 ..., 4975 4978 4983]
    True
    True

Parece que al ir aumentando el tamaño de los datos de entrada a la función los números son consistentes y el rendimiento se mantiene. En este caso concreto parece que ya hemos llegado a rendimientos de más de ¡¡35x!! con respecto a la implementación inicial.

# Cythonizando, que es gerundio (toma 8).

Podemos usar [directivas de compilación](http://docs.cython.org/src/reference/compilation.html#compiler-directives) que ayuden al compilador a decidir mejor qué es lo que tiene que hacer. Entre ellas se encuentra una opción que es `boundscheck` que evita mirar la posibilidad de obtener `IndexError` asumiendo que el código está libre de estos errores de indexación. Lo vamos a usar conjuntamente con `wraparound`. Esta última opción se encarga de evitar mirar indexaciones relativas al final del iterable (por ejemplo, `mi_iterable[-1]`). En este caso concreto, la segunda opción no aporta nada de mejora de rendimiento pero la dijamos ya que la hemos probado.

    %%cython --name probandocython8
    import numpy as np
    cimport numpy as np
    from cpython cimport array as c_array
    from array import array
    cimport cython

    @cython.boundscheck(False) 
    @cython.wraparound(False)
    cpdef tuple busca_min_cython8(np.ndarray[double, ndim = 2] malla):
        cdef c_array.array minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        minimosx = array('L', [])
        minimosy = array('L', []) 
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    %timeit busca_min_cython8(data)

**OUTPUT:**

    10 loops, best of 3: 94.3 ms per loop

Parece que hemos conseguido arañar otro poquito de rendimiento.

# Cythonizando, que es gerundio (toma 9).

En lugar de usar numpy arrays vamos a usar [_memoryviews_](http://docs.cython.org/src/userguide/memoryviews.html#typed-memoryviews). Los _memoryviews_ son arrays de acceso rápido. Si solo queremos almacenar cosas y no necesitamos ninguna de las características de un numpy array pueden ser una buena solución. Si necesitamos alguna funcionalidad extra siempre lo podemos convertir en un numpy array usando `numpy.asarray`.

    %%cython --name probandocython9
    import numpy as np
    cimport numpy as np
    from cpython cimport array as c_array
    from array import array
    cimport cython

    @cython.boundscheck(False) 
    @cython.wraparound(False)
    #cpdef tuple busca_min_cython9(np.ndarray[double, ndim = 2] malla):
    cpdef tuple busca_min_cython9(double [:,:] malla):
        cdef c_array.array minimosx, minimosy
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef unsigned int start = 1
        #cdef float [:, :] malla_view = malla
        minimosx = array('L', [])
        minimosy = array('L', []) 
        for i in range(start, ii):
            for j in range(start, jj):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    %timeit busca_min_cython9(data)

**OUTPUT:**

    10 loops, best of 3: 97.6 ms per loop

Parece que, virtualmente, el rendimiento es parecido a lo que ya teniamos por lo que parece que nos hemos quedado igual.

# Bonus track

Voy a intentar usar pypy (2.4 (CPython 2.7)) conjuntamente con numpypy para ver lo que conseguimos.

    %%pypy
    import numpy as np
    import time

    np.random.seed(0)
    data = np.random.randn(2000,2000)

    def busca_min(malla):
        minimosx = []
        minimosy = []
        for i in range(1, malla.shape[1]-1):
            for j in range(1, malla.shape[0]-1):
                if (malla[j, i] < malla[j-1, i-1] and
                    malla[j, i] < malla[j-1, i] and
                    malla[j, i] < malla[j-1, i+1] and
                    malla[j, i] < malla[j, i-1] and
                    malla[j, i] < malla[j, i+1] and
                    malla[j, i] < malla[j+1, i-1] and
                    malla[j, i] < malla[j+1, i] and
                    malla[j, i] < malla[j+1, i+1]):
                    minimosx.append(i)
                    minimosy.append(j)

        return np.array(minimosx), np.array(minimosy)

    resx, resy = busca_min(data)
    print(data)
    print(len(resx), len(resy))
    print(resx)
    print(resy)

    t = []
    for i in range(100):
        t0 = time.time()
        busca_min(data)
        t1 = time.time() - t0
        t.append(t1)
    print(sum(t) / 100.)

**OUTPUT:**

    [[ 1.76405235  0.40015721  0.97873798 ...,  0.15843385 -1.14190142
      -1.31097037]
     [-1.53292105 -1.71197016  0.04613506 ..., -0.03057244  1.57708821
      -0.8128021 ]
     [ 0.61334917  1.84369998  0.27109098 ..., -0.53788475  0.39344443
       0.28651827]
     ..., 
     [-0.17117027  0.57332063 -0.89516715 ..., -0.01409412  1.28756456
      -0.6953778 ]
     [-1.53627571  0.57441228 -0.20564476 ...,  0.90499929  0.51428298
       0.72148202]
     [ 0.51262101 -0.90758583  1.78121159 ..., -1.12554283  0.95170926
      -1.15237806]]
    (443641, 443641)
    [   1    1    1 ..., 1998 1998 1998]
    [   1    3   11 ..., 1968 1977 1985]
    0.3795211339

El último valor del output anterior es el tiempo promedio después de repetir el cálculo 100 veces.  
Wow!! Parece que sin hacer modificaciones tenemos que el resultado es 10x - 15x veces más rápido que el obtenido usando la función inicial. Y llega a ser solo 3.5x veces más lento que lo que hemos conseguido con Cython.

# Resumen de resultados.

Vamos a ver los resultados completos en un breve resumen. Primero vamos a ver los tiempos de las diferentes versiones de la función `busca_min_xxx`:

    funcs = [busca_min, busca_min_numba, busca_min_cython1,
             busca_min_cython2, busca_min_cython3,
             busca_min_cython4, busca_min_cython5,
             busca_min_cython6, busca_min_cython7,
             busca_min_cython8, busca_min_cython9]
    t = []
    for func in funcs:
        res = %timeit -o func(data)
        t.append(res.best)

**OUTPUT:**

    1 loops, best of 3: 3.67 s per loop
    1 loops, best of 3: 5.34 s per loop
    1 loops, best of 3: 3.41 s per loop
    1 loops, best of 3: 3.54 s per loop
    1 loops, best of 3: 3.65 s per loop
    10 loops, best of 3: 139 ms per loop
    10 loops, best of 3: 136 ms per loop
    1 loops, best of 3: 5.65 s per loop
    10 loops, best of 3: 95.4 ms per loop
    10 loops, best of 3: 89 ms per loop
    10 loops, best of 3: 92.3 ms per loop

<br>

    index = np.arange(len(t))
    plt.figure(figsize = (12, 6))
    plt.bar(index, t)
    plt.xticks(index + 0.4, [func.__name__[9:] for func in funcs])
    plt.tight_layout()

![wpid](https://pybonacci.org/images/2015/03/wpid-C_elemental_querido_Cython1.png?style=centerme)

En el gráfico anterior, la primera barra corresponde a la función de partida (`busca_min`). Recordemos que la versión de pypy ha tardado unos 0.38 segundos.

Y ahora vamos a ver los tiempos entre `busca_min` (la versión original) y la última versión de cython que hemos creado, `busca_min_cython9` usando diferentes tamaños de la matriz de entrada:

    tamanyos = [10, 100, 500, 1000, 2000, 5000]
    t_p = []
    t_c = []
    for i in tamanyos:
        data = np.random.randn(i, i)
        res = %timeit -o busca_min(data)
        t_p.append(res.best)
        res = %timeit -o busca_min_cython9(data)
        t_c.append(res.best)

**OUTPUT:**

    10000 loops, best of 3: 67.9 µs per loop
    The slowest run took 4.77 times longer than the fastest. This could mean that an intermediate result is being cached 
    100000 loops, best of 3: 5.13 µs per loop
    100 loops, best of 3: 8.65 ms per loop
    10000 loops, best of 3: 177 µs per loop
    1 loops, best of 3: 223 ms per loop
    100 loops, best of 3: 5.51 ms per loop
    1 loops, best of 3: 890 ms per loop
    10 loops, best of 3: 26.6 ms per loop
    1 loops, best of 3: 3.64 s per loop
    10 loops, best of 3: 92.8 ms per loop
    1 loops, best of 3: 22.8 s per loop
    1 loops, best of 3: 605 ms per loop

<br>

    plt.figure(figsize = (10,6))
    plt.plot(tamanyos, t_p, 'bo-')
    plt.plot(tamanyos, t_c, 'ro-')

**OUTPUT:**

    [<matplotlib.lines.Line2D at 0x7f5b810a1d30>]

![wpid2](https://pybonacci.org/images/2015/03/wpid-C_elemental_querido_Cython2.png?style=centerme)

    ratio = np.array(t_p) / np.array(t_c)
    plt.figure(figsize = (10,6))
    plt.plot(tamanyos, ratio, 'bo-')

**OUTPUT:**

    [<matplotlib.lines.Line2D at 0x7f5b810af2e8>]

![wpid3](https://pybonacci.org/images/2015/03/wpid-C_elemental_querido_Cython3.png?style=centerme)

Parece que conseguimos rendimientos que son 40 veces más rápidos que con Python puro que usa un numpy array de por medio (excepto para tamaños de arrays muy pequeños en los que el rendimiento no sería una gran problema).

# Apuntes finales

Después de haber probado Python, Cython, Numba y Pypy:  
**Numba**:

*  Numba no parece fácilmente generalizable a día de hoy (experiencia personal) y no soporta ni parece que soportará todas las características del lenguaje. La idea me parece increible pero creo que le falta todavía un poco de madurez.
*  Me ha costado instalar numba y llvmlite en linux sin usar conda (con conda no lo he probado por lo que no puedo opinar).

(Creo que JuanLu estaba preparando un post sobre Numba. Habrá que esperar a ver sus conclusiones).  
**Pypy**:

*  Pypy ha funcionado como un titán sin necesidad de hacer modificaciones.
*  Destacar que no tengo excesivas experiencias con el mismo
*  Instalarlo no es tarea fácil (he intentado usar PyPy3 con numpypy y he fallado vilmente). Quería usar numpypy y al final he optado por descargar una versión portable con numpy de serie que quizá afecte al rendimiento ¿?.

**Cython**:

*  Me ha parecido el más generalizable de todos. Se pueden crear paquetes para CPython, para Pypy,...
*  No lo he probado en Windows por lo que no sé lo doloroso que puede llegar a ser. Mañana lo probaré en el trabajo y ya dejaré un comentario por ahí.
*  El manejo no es tan evidente como con Numba y Pypy. Requiere entender como funcionan los tipos de C y requiere conocer una serie de interioridades de C. Sin duda es el que más esfuerzo requiere de las alternativas aquí expuestas pra este caso concreto y no generalizable.
*  Creo que, una vez hecho el esfuerzo inicial de intentar entender un poco como funciona, se puede sacar un gran rendimiento del mismo en muchas situaciones.

Y después de haber leído todo esto pensad que, en la mayoría de situaciones, CPython no es tan lento como lo pintan (sobretodo con numpy) y que ¡¡¡LA OPTIMIZACIÓN PREMATURA ES LA RAÍZ DE TODOS LOS MALES!!!
