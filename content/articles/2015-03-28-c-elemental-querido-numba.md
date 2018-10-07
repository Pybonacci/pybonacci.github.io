---
title: C elemental, querido numba
date: 2015-03-28T22:10:45+00:00
author: Kiko Correoso
slug: c-elemental-querido-numba
tags: blttlenec, cython, numba, numbagg, numpy, python, rendimiento

# Volvemos al torneo del rendimiento!!!

Recapitulando. Un artículo sobre Cython donde conseguíamos [mejoras de velocidad de código Python con numpy arrays de 40x usando Cython](http://pybonacci.org/2015/03/09/c-elemental-querido-cython/) desembocó [en mejoras de 70x usando numba](http://pybonacci.org/2015/03/13/como-acelerar-tu-codigo-python-con-numba/). En esta tercera toma vamos a ver si con Cython conseguimos las velocidades de numba tomando algunas ideas de la implementación de JuanLu y definiendo una función un poco más inteligente que mi implementación con Cython ([busca_min_cython9](http://pybonacci.org/2015/03/09/c-elemental-querido-cython/#Cythonizando,-que-es-gerundio-%28toma-9%29.)).

Preparamos el _setup inicial_.

    :::python
    import numpy as np
    import numba

    np.random.seed()

    data = np.random.randn(2000, 2000)

JuanLu hizo alguna trampa usando un numpy array en lugar de dos listas y devolviendo el resultado usando `numpy.nonzero`. En realidad no es trampa, es pura envidia mía al ver que ha usado una forma más inteligente de conseguir lo mismo que hacía mi función original 😛  
Usando esa implementación considero que es más inteligente tener un numpy array de salida por lo que el uso de `np.nonzero` sería innecesario y añadiría algo de pérdida de rendimiento si luego vamos a seguir trabajando con numpy arrays. Por tanto, la implementación de JuanLu eliminando el uso de `numpy.nonzero` sería:

    :::python
    def busca_min_np_jit(malla):
        minimos = np.zeros_like(malla, dtype=bool)
        _busca_min(malla, minimos)
        return minimos  # en lugar de 'return np.nonzero(minimos)'

    @numba.jit(nopython=True)
    def _busca_min(malla, minimos):
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
                    minimos[i, j] = True

    %timeit -n 100 busca_min_np_jit(data)

**OUTPUT:**

`100 loops, best of 3: 33 ms per loop`

Ejecutándolo 100 veces obtenemos un valor más bajo de 33.6 ms devolviendo un numpy.array de 1's y 0's con los 1's indicando la posición de los máximos.  
La implementación original la vamos a modificar un poco para que devuelva lo mismo.

    :::python
    def busca_min(malla):
        minimos = np.zeros_like(malla)
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
                    minimos[i, j] = 1

        return minimos

    %timeit busca_min(data)

**OUTPUT:**

`1 loops, best of 3: 3.4 s per loop`

Los tiempos son similares a la función original y, aunque estamos usando más memoria, tenemos una mejora con numba que ya llega a los dos órdenes de magnitud (alrededor de 100x!!) y una función más usable para trabajar con numpy.

Vamos a modificar la opción Cython más rápida que obtuvimos para que se comporte igual que las de Numba y Python.  
Primero cargamos la extensión Cython.

    # antes cythonmagic
    %load_ext Cython

Vamos a usar la opción `annotate` para ver cuanto 'blanco' tenemos y la nueva versión Cython la vamos a llamar `busca_min_cython10`.

    %%cython --annotate
    import numpy as np
    from cython cimport boundscheck, wraparound

    cpdef char[:,::1] busca_min_cython10(double[:, ::1] malla):
        cdef unsigned int i, j
        cdef unsigned int ii = malla.shape[1]-1
        cdef unsigned int jj = malla.shape[]-1
        cdef char[:,::1] minimos = np.zeros_like(malla, dtype = np.int8)
        #minimos[...] = 0
        cdef unsigned int start = 1
        #cdef float [:, :] malla_view = malla
        with boundscheck(False), wraparound(False):
            for j in range(start, ii):
                for i in range(start, jj):
                    if (malla[j, i] < malla[j-1, i-1] and
                        malla[j, i] < malla[j-1, i] and
                        malla[j, i] < malla[j-1, i+1] and
                        malla[j, i] < malla[j, i-1] and
                        malla[j, i] < malla[j, i+1] and
                        malla[j, i] < malla[j+1, i-1] and
                        malla[j, i] < malla[j+1, i] and
                        malla[j, i] < malla[j+1, i+1]):
                        minimos[i,j] = 1

        return minimos

<br>  
  
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

     02: from cython cimport boundscheck, wraparound

     03: 

    +04: cpdef char[:,::1] busca_min_cython10(double[:, ::1] malla):

    static PyObject *__pyx_pw_46_cython_magic_de7594aedda59602146d5e749862b110_1busca_min_cython10(PyObject *__pyx_self, PyObject *__pyx_arg_malla); /*proto*/
    static __Pyx_memviewslice __pyx_f_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(__Pyx_memviewslice __pyx_v_malla, CYTHON_UNUSED int __pyx_skip_dispatch) {
      unsigned int __pyx_v_i;
      unsigned int __pyx_v_j;
      unsigned int __pyx_v_ii;
      unsigned int __pyx_v_jj;
      __Pyx_memviewslice __pyx_v_minimos = { 0, 0, { 0 }, { 0 }, { 0 } };
      unsigned int __pyx_v_start;
      __Pyx_memviewslice __pyx_r = { 0, 0, { 0 }, { 0 }, { 0 } };
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython10", 0);
    /* … */
      /* function exit code */
      __pyx_L1_error:;
      __Pyx_XDECREF(__pyx_t_1);
      __Pyx_XDECREF(__pyx_t_2);
      __Pyx_XDECREF(__pyx_t_3);
      __Pyx_XDECREF(__pyx_t_4);
      __Pyx_XDECREF(__pyx_t_5);
      __PYX_XDEC_MEMVIEW(&__pyx_t_6, 1);
      __pyx_r.data = NULL;
      __pyx_r.memview = NULL;
      __Pyx_AddTraceback("_cython_magic_de7594aedda59602146d5e749862b110.busca_min_cython10", __pyx_clineno, __pyx_lineno, __pyx_filename);

      goto __pyx_L2;
      __pyx_L0:;
      if (unlikely(!__pyx_r.memview)) {
        PyErr_SetString(PyExc_TypeError,"Memoryview return value is not initialized");
      }
      __pyx_L2:;
      __PYX_XDEC_MEMVIEW(&__pyx_v_minimos, 1);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    /* Python wrapper */
    static PyObject *__pyx_pw_46_cython_magic_de7594aedda59602146d5e749862b110_1busca_min_cython10(PyObject *__pyx_self, PyObject *__pyx_arg_malla); /*proto*/
    static PyObject *__pyx_pw_46_cython_magic_de7594aedda59602146d5e749862b110_1busca_min_cython10(PyObject *__pyx_self, PyObject *__pyx_arg_malla) {
      __Pyx_memviewslice __pyx_v_malla = { 0, 0, { 0 }, { 0 }, { 0 } };
      PyObject *__pyx_r = 0;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython10 (wrapper)", 0);
      assert(__pyx_arg_malla); {
        __pyx_v_malla = __Pyx_PyObject_to_MemoryviewSlice_d_dc_double(__pyx_arg_malla); if (unlikely(!__pyx_v_malla.memview)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L3_error;}
      }
      goto __pyx_L4_argument_unpacking_done;
      __pyx_L3_error:;
      __Pyx_AddTraceback("_cython_magic_de7594aedda59602146d5e749862b110.busca_min_cython10", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __Pyx_RefNannyFinishContext();
      return NULL;
      __pyx_L4_argument_unpacking_done:;
      __pyx_r = __pyx_pf_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(__pyx_self, __pyx_v_malla);
      int __pyx_lineno = 0;
      const char *__pyx_filename = NULL;
      int __pyx_clineno = 0;

      /* function exit code */
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    static PyObject *__pyx_pf_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(CYTHON_UNUSED PyObject *__pyx_self, __Pyx_memviewslice __pyx_v_malla) {
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("busca_min_cython10", 0);
      __Pyx_XDECREF(__pyx_r);
      if (unlikely(!__pyx_v_malla.memview)) { __Pyx_RaiseUnboundLocalError("malla"); {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;} }
      __pyx_t_1 = __pyx_f_46_cython_magic_de7594aedda59602146d5e749862b110_busca_min_cython10(__pyx_v_malla, 0); if (unlikely(!__pyx_t_1.memview)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __pyx_t_2 = __pyx_memoryview_fromslice(__pyx_t_1, 2, (PyObject *(*)(char *)) __pyx_memview_get_char, (int (*)(char *, PyObject *)) __pyx_memview_set_char, 0);; if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_2);
      __PYX_XDEC_MEMVIEW(&__pyx_t_1, 1);
      __pyx_r = __pyx_t_2;
      __pyx_t_2 = 0;
      goto __pyx_L0;

      /* function exit code */
      __pyx_L1_error:;
      __PYX_XDEC_MEMVIEW(&__pyx_t_1, 1);
      __Pyx_XDECREF(__pyx_t_2);
      __Pyx_AddTraceback("_cython_magic_de7594aedda59602146d5e749862b110.busca_min_cython10", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __pyx_r = NULL;
      __pyx_L0:;
      __PYX_XDEC_MEMVIEW(&__pyx_v_malla, 1);
      __Pyx_XGIVEREF(__pyx_r);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

     05:     cdef unsigned int i, j

    +06:     cdef unsigned int ii = malla.shape[1]-1

      __pyx_v_ii = ((__pyx_v_malla.shape[1]) - 1);

    +07:     cdef unsigned int jj = malla.shape[]-1

      __pyx_v_jj = ((__pyx_v_malla.shape[0]) - 1);

    +08:     cdef char[:,::1] minimos = np.zeros_like(malla, dtype = np.int8)

      __pyx_t_1 = __Pyx_GetModuleGlobalName(__pyx_n_s_np); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_2 = __Pyx_PyObject_GetAttrStr(__pyx_t_1, __pyx_n_s_zeros_like); if (unlikely(!__pyx_t_2)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_2);
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_1 = __pyx_memoryview_fromslice(__pyx_v_malla, 2, (PyObject *(*)(char *)) __pyx_memview_get_double, (int (*)(char *, PyObject *)) __pyx_memview_set_double, 0);; if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_3 = PyTuple_New(1); if (unlikely(!__pyx_t_3)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_3);
      PyTuple_SET_ITEM(__pyx_t_3, 0, __pyx_t_1);
      __Pyx_GIVEREF(__pyx_t_1);
      __pyx_t_1 = 0;
      __pyx_t_1 = PyDict_New(); if (unlikely(!__pyx_t_1)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_4 = __Pyx_GetModuleGlobalName(__pyx_n_s_np); if (unlikely(!__pyx_t_4)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_4);
      __pyx_t_5 = __Pyx_PyObject_GetAttrStr(__pyx_t_4, __pyx_n_s_int8); if (unlikely(!__pyx_t_5)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_5);
      __Pyx_DECREF(__pyx_t_4); __pyx_t_4 = 0;
      if (PyDict_SetItem(__pyx_t_1, __pyx_n_s_dtype, __pyx_t_5) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
      __pyx_t_5 = __Pyx_PyObject_Call(__pyx_t_2, __pyx_t_3, __pyx_t_1); if (unlikely(!__pyx_t_5)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_GOTREF(__pyx_t_5);
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __Pyx_DECREF(__pyx_t_3); __pyx_t_3 = 0;
      __Pyx_DECREF(__pyx_t_1); __pyx_t_1 = 0;
      __pyx_t_6 = __Pyx_PyObject_to_MemoryviewSlice_d_dc_char(__pyx_t_5);
      if (unlikely(!__pyx_t_6.memview)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 8; __pyx_clineno = __LINE__; goto __pyx_L1_error;}
      __Pyx_DECREF(__pyx_t_5); __pyx_t_5 = 0;
      __pyx_v_minimos = __pyx_t_6;
      __pyx_t_6.memview = NULL;
      __pyx_t_6.data = NULL;

     09:     #minimos[...] = 0

    +10:     cdef unsigned int start = 1

      __pyx_v_start = 1;

     11:     #cdef float [:, :] malla_view = malla

     12:     with boundscheck(False), wraparound(False):

    +13:         for j in range(start, ii):

      __pyx_t_7 = __pyx_v_ii;
      for (__pyx_t_8 = __pyx_v_start; __pyx_t_8 < __pyx_t_7; __pyx_t_8+=1) {
        __pyx_v_j = __pyx_t_8;

    +14:             for i in range(start, jj):

        __pyx_t_9 = __pyx_v_jj;
        for (__pyx_t_10 = __pyx_v_start; __pyx_t_10 < __pyx_t_9; __pyx_t_10+=1) {
          __pyx_v_i = __pyx_t_10;

    +15:                 if (malla[j, i] < malla[j-1, i-1] and

          __pyx_t_12 = __pyx_v_j;
          __pyx_t_13 = __pyx_v_i;
          __pyx_t_14 = (__pyx_v_j - 1);
          __pyx_t_15 = (__pyx_v_i - 1);
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_12 * __pyx_v_malla.strides[0]) )) + __pyx_t_13)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_14 * __pyx_v_malla.strides[0]) )) + __pyx_t_15)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +16:                     malla[j, i] < malla[j-1, i] and

          __pyx_t_17 = __pyx_v_j;
          __pyx_t_18 = __pyx_v_i;
          __pyx_t_19 = (__pyx_v_j - 1);
          __pyx_t_20 = __pyx_v_i;
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_17 * __pyx_v_malla.strides[0]) )) + __pyx_t_18)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_19 * __pyx_v_malla.strides[0]) )) + __pyx_t_20)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +17:                     malla[j, i] < malla[j-1, i+1] and

          __pyx_t_21 = __pyx_v_j;
          __pyx_t_22 = __pyx_v_i;
          __pyx_t_23 = (__pyx_v_j - 1);
          __pyx_t_24 = (__pyx_v_i + 1);
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_21 * __pyx_v_malla.strides[0]) )) + __pyx_t_22)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_23 * __pyx_v_malla.strides[0]) )) + __pyx_t_24)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +18:                     malla[j, i] < malla[j, i-1] and

          __pyx_t_25 = __pyx_v_j;
          __pyx_t_26 = __pyx_v_i;
          __pyx_t_27 = __pyx_v_j;
          __pyx_t_28 = (__pyx_v_i - 1);
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_25 * __pyx_v_malla.strides[0]) )) + __pyx_t_26)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_27 * __pyx_v_malla.strides[0]) )) + __pyx_t_28)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +19:                     malla[j, i] < malla[j, i+1] and

          __pyx_t_29 = __pyx_v_j;
          __pyx_t_30 = __pyx_v_i;
          __pyx_t_31 = __pyx_v_j;
          __pyx_t_32 = (__pyx_v_i + 1);
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_29 * __pyx_v_malla.strides[0]) )) + __pyx_t_30)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_31 * __pyx_v_malla.strides[0]) )) + __pyx_t_32)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +20:                     malla[j, i] < malla[j+1, i-1] and

          __pyx_t_33 = __pyx_v_j;
          __pyx_t_34 = __pyx_v_i;
          __pyx_t_35 = (__pyx_v_j + 1);
          __pyx_t_36 = (__pyx_v_i - 1);
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_33 * __pyx_v_malla.strides[0]) )) + __pyx_t_34)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_35 * __pyx_v_malla.strides[0]) )) + __pyx_t_36)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +21:                     malla[j, i] < malla[j+1, i] and

          __pyx_t_37 = __pyx_v_j;
          __pyx_t_38 = __pyx_v_i;
          __pyx_t_39 = (__pyx_v_j + 1);
          __pyx_t_40 = __pyx_v_i;
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_37 * __pyx_v_malla.strides[0]) )) + __pyx_t_38)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_39 * __pyx_v_malla.strides[0]) )) + __pyx_t_40)) )))) != 0);
          if (__pyx_t_16) {
          } else {
            __pyx_t_11 = __pyx_t_16;
            goto __pyx_L8_bool_binop_done;
          }

    +22:                     malla[j, i] < malla[j+1, i+1]):

          __pyx_t_41 = __pyx_v_j;
          __pyx_t_42 = __pyx_v_i;
          __pyx_t_43 = (__pyx_v_j + 1);
          __pyx_t_44 = (__pyx_v_i + 1);
          __pyx_t_16 = (((*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_41 * __pyx_v_malla.strides[0]) )) + __pyx_t_42)) ))) < (*((double *) ( /* dim=1 */ ((char *) (((double *) ( /* dim=0 */ (__pyx_v_malla.data + __pyx_t_43 * __pyx_v_malla.strides[0]) )) + __pyx_t_44)) )))) != 0);
          __pyx_t_11 = __pyx_t_16;
          __pyx_L8_bool_binop_done:;
          if (__pyx_t_11) {

    +23:                     minimos[i,j] = 1

            __pyx_t_45 = __pyx_v_i;
            __pyx_t_46 = __pyx_v_j;
            *((char *) ( /* dim=1 */ ((char *) (((char *) ( /* dim=0 */ (__pyx_v_minimos.data + __pyx_t_45 * __pyx_v_minimos.strides[0]) )) + __pyx_t_46)) )) = 1;
            goto __pyx_L7;
          }
          __pyx_L7:;
        }
      }

     24: 

    +25:     return minimos

      __PYX_INC_MEMVIEW(&__pyx_v_minimos, 0);
      __pyx_r = __pyx_v_minimos;
      goto __pyx_L0;

Vemos que la mayor parte está en 'blanco'. Eso significa que estamos evitando usar la C-API de CPython y la mayor parte sucede en C. Estoy usando `typed memoryviews` que permite trabajar de forma 'transparente' con numpy arrays.  
Vamos a ejecutar la nueva versión 100 veces, de la misma forma que hemos hecho con Numba:

`%timeit -n 100 busca_min_cython10(data)`

**OUTPUT:`

`100 loops, best of 3: 27.6 ms per loop`

Wow, virtualmente obtenemos la misma velocidad entre Numba y Cython y dos órdenes de magnitud de mejora con respecto a la versión Python.

    res_numba = busca_min_np_jit(data)
    res_cython = busca_min_cython10(data)
    res_python = busca_min(data)

    np.testing.assert_array_equal(res_numba, res_cython)
    np.testing.assert_array_equal(res_numba, res_python)
    np.testing.assert_array_equal(res_cython, res_python)

    Parece que el resultado es el mismo en todo momento

    Probemos con arrays de menos y más tamaño.

    data = np.random.randn(500, 500)
    %timeit -n 3 busca_min_np_jit(data)
    %timeit -n 3 busca_min_cython10(data)
    %timeit busca_min(data)

**OUTPUT:**

    3 loops, best of 3: 2.04 ms per loop
    3 loops, best of 3: 1.75 ms per loop
    1 loops, best of 3: 209 ms per loop

<br>

    data = np.random.randn(5000, 5000)
    %timeit -n 3 busca_min_np_jit(data)
    %timeit -n 3 busca_min_cython10(data)
    %timeit busca_min(data)

**OUTPUT:**

    3 loops, best of 3: 216 ms per loop
    3 loops, best of 3: 174 ms per loop
    1 loops, best of 3: 21.6 s per loop

Parece que las distintas versiones escalan de la misma forma y el rendimiento parece, más o menos, lineal.

# Conclusiones de este nuevo capítulo.

Las conclusiones que saco yo de este mano a mano que hemos llevado a cabo JuanLu (featuring Numba) y yo (featuring Cython):

*  Cython: Si te restringes a cosas sencillas, es relativamente sencillo de usar. Básicamente habría que optimizar bucles y, solo en caso de que sea necesario, añadir tipos a otras variables para evitar pasar por la C-API de CPython en ciertas operaciones puesto que puede tener un coste elevado en el rendimiento. Para cosas más complejas, a pesar de que sigue siendo más placentero que C se puede complicar un poco más (pero no mucho más, una vez que has entendido cómo usarlo).
*  Numba: Es bastante sorprendente lo que se puede llegar a conseguir con poco esfuerzo. Parece que siempre introducirá un poco de _overhead_ puesto que hace muchas cosas entre bambalinas y de la otra forma (Cython) hace lo que le digamos que haga. También es verdad que muchas cosas no están soportadas, que los errores que obtenemos puede ser un poco crípticos y se hace difícil depurar el código. Pero a pesar de todo lo anterior y conociendo el historial de la gente que está detrás del proyecto Numba creo que su futuro será brillante. Por ejemplo, [Numbagg](https://github.com/shoyer/numbagg) es una librería que usa Numba y que pretende hacer lo mismo que [bottleneck](https://github.com/kwgoodman/bottleneck) (una librería muy especializada para determinadas operaciones de Numpy), que usa Cython consiguiendo [resultados comparables aunque levemente peores](https://github.com/shoyer/numbagg#benchmarks).

No sé si habrá algún capítulo más de esta serie... Lo dejo en manos de JuanLu o de cualquiera que nos quiera enviar un nuevo post relacionado.
