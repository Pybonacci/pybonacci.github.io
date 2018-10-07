---
title: Cómo acelerar tu código Python con numba
date: 2015-03-13T16:45:25+00:00
author: Juan Luis Cano
slug: como-acelerar-tu-codigo-python-con-numba
tags: conda, numba, python, python 3, rendimiento

Introducción

En este artículo vamos a hacer un repaso exhaustivo de **cómo acelerar sustancialmente tu código Python usando numba**. Ya hablamos sobre [la primera versión de numba](http://pybonacci.org/2012/08/21/probando-numba-compilador-para-python-basado-en-llvm/) en el blog, allá por 2012, pero ha habido importantes cambios desde entonces y la herramienta ha cambiado muchísimo. Recientemente Continuum publicó numba 0.17 con una [nueva documentación](http://numba.pydata.org/numba-doc/0.17.0/index.html) mucho más fácil de seguir, pero aun así no siempre queda claro cuál es el camino para hacer que funcione, como quedó patente con el [artículo sobre Cython](http://pybonacci.org/2015/03/09/c-elemental-querido-cython/) de Kiko. Por ello, en este artículo voy a aclarar qué puede y qué no puede hacer numba, cómo sacarle partido y voy a detallar un par de ejemplos exitosos que he producido en los últimos meses.

Hablando de las nuevas versiones de numba, en su web podéis ver una [evolución temporal del rendimiento](http://numba.pydata.org/numba-benchmark/) de algunas tareas que utiliza [asv](http://spacetelescope.github.io/asv/) para la visualización.

# Entendiendo numba: el modo _nopython_

Como podemos leer en la documentación, [numba tiene dos modos de funcionamiento básicos](http://numba.pydata.org/numba-doc/0.17.0/user/jit.html#nopython): el modo _object_ y el modo _nopython_.

*  El modo _object_ genera código que gestiona todas las variables como objetos de Python y utiliza la API C de Python para operar con ellas. En general en este modo **no habrá ganancias de rendimiento** (e incluso puede ir más lento), con lo cual mi recomendación personal es directamente no utilizarlo. Hay casos en los que numba puede detectar los bucles y optimizarlos individualmente (_loop-jitting_), pero no le voy a prestar mucha atención a esto.
*  El modo _nopython_ **genera código independiente de la API C de Python**. Esto tiene la desventaja de que no podemos usar todas las características del lenguaje, **pero tiene un efecto significativo en el rendimiento**. Otra de las restricciones es que **no se puede reservar memoria para objetos nuevos**.

Por defecto numba usa el modo _nopython_ siempre que puede, y si no pasa a modo _object_. Nosotros vamos a **forzar el modo nopython** (o «modo estricto» como me gusta llamarlo) porque es la única forma de aprovechar el potencial de numba.

# Ámbito de aplicación

El problema del modo _nopython_ es que los mensajes de error son totalmente inservibles en la mayoría de los casos, así que antes de lanzarnos a compilar funciones con numba conviene hacer un repaso de qué no podemos hacer para anticipar la mejor forma de programar nuestro código. Podéis consultar en la documentación [el subconjunto de Python soportado por numba](http://numba.pydata.org/numba-doc/0.17.0/reference/pysupported.html) en modo _nopython_, y ya os aviso que, al menos de momento, no tenemos [_list comprehensions_](https://github.com/numba/numba/issues/504), [generadores](https://github.com/numba/numba/issues/984) ni algunas cosas más. Permitidme que resalte una frase sacada de la página principal de numba:

> "_With a few annotations, **array-oriented and math-heavy Python code** can be just-in-time compiled to native machine instructions, similar in performance to C, C++ and Fortran_". [Énfasis mío]

Siento decepcionar a la audiencia pero _numba no acelerará todo el código Python_ que le echemos: está enfocado a operaciones matemáticas con arrays. Aclarado este punto, vamos a ponernos manos a la obra con un ejemplo aplicado 🙂

# Antes de empezar: instalación

Puedes instalar numba en Windows, OS X y Linux con [conda](http://conda.io/) usando este comando:  
`conda install numba`  
conda se ocupará de instalar una versión correcta de LLVM, así que no tendrás que compilarla tú mismo. _Y ya está_.  
Ahora viene una opinión personal pero que considero importante: si eres usuario de paquetes científicos y aún no estás utilizando conda (o Anaconda) para gestionarlos, **estás en la edad de piedra**. Me declaro fanboy absoluto de Continuum Analytics por crear una herramienta de código abierto ([conda está en GitHub](http://github.com/conda/conda)) que soluciona _por fin y de una vez por todas_ los problemas y frustración que hemos tenido como comunidad [desde hace 15 años](https://twitter.com/fperez_org/status/569896953875722240) y que Guido y otros se negaron a atajar. Yo llevo en esto solo desde 2011 pero aún recuerdo lo que es intentar compilar SciPy en Windows. Hazte un favor e [instala Miniconda](http://conda.pydata.org/miniconda.html).

# Acelerando una función con numba

Voy a tomar directamente el ejemplo que usó Kiko para su artículo sobre Cython y vamos a ver cómo podemos utilizar numba (y un poco de astucia) para acelerar esta función:

> "Por ejemplo, imaginemos que tenemos que detectar valores mínimos locales dentro de una malla. Los valores mínimos deberán ser simplemente valores más bajos que los que haya en los 8 nodos de su entorno inmediato. En el siguiente gráfico, el nodo en verde será un nodo con un mínimo y en su entorno son todo valores superiores:

<div>
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

¡Vamos allá!

`%install_ext http://raw.github.com/jrjohansson/version_information/master/version_information.py`

**OUTPUT:**

    Installed version_information.py. To use it, type:

    %load_ext version_information
    %load_ext version_information

<br>

`%version_information numpy, numba, cython`

**OUTPUT:**

<div>
  <table>
    <tr>
      <th>
        Software
      </th>
      
      <th>
        Version
      </th>
    </tr>
    
    <tr>
      <td>
        Python
      </td>
      
      <td>
        3.4.3 64bit [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)]
      </td>
    </tr>
    
    <tr>
      <td>
        IPython
      </td>
      
      <td>
        3.0.0
      </td>
    </tr>
    
    <tr>
      <td>
        OS
      </td>
      
      <td>
        Linux 3.18.6 1 ARCH x86_64 with arch
      </td>
    </tr>
    
    <tr>
      <td>
        numpy
      </td>
      
      <td>
        1.9.2
      </td>
    </tr>
    
    <tr>
      <td>
        numba
      </td>
      
      <td>
        0.17.0
      </td>
    </tr>
    
    <tr>
      <td>
        cython
      </td>
      
      <td>
        0.22
      </td>
    </tr>
    
    <tr>
      <td colspan='2'>
        Fri Mar 13 13:44:39 2015 CET
      </td>
    </tr>
  </table>
</div>
      
Vamos a empezar por importar los paquetes necesarios e inicializar la semilla del generador de números aleatorios:

    import numpy as np
    import numba

    np.random.seed()

Creamos nuestro array de datos:

`data = np.random.randn(2000, 2000)`

Y voy a copiar descaradamente la función de Kiko:

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

    busca_min(data)

**OUTPUT:**

    (array([   1,    1,    1, ..., 1998, 1998, 1998]),
     array([   1,    3,   11, ..., 1968, 1977, 1985]))

# Paso 1: analizar el código

Lo primero que pensé cuando vi esta función es que no me gustaba nada hacer `append` a esas dos listas tantas veces. Pero a continuación me pregunté si realmente tendrían tantos elementos... averigüémoslo:

    mx, my = busca_min(data)
    mx.size / data.size

**OUTPUT:**

    0.11091025

Tenemos que más de un 10 % de los elementos de la matriz cumplen la condición de ser «mínimos locales», así que no es nada despreciable. Esto en nuestro ejemplo hace _un total de más de 400 000 elementos_:

    mx.size

**OUTPUT:**

    443641

Ahora la idea de crear dos listas y añadir los elementos uno a uno me gusta todavía menos, así que voy a cambiar de enfoque. Lo que voy a hacer va a ser crear otro array, de la misma forma que nuestros datos, y almacenar un valor `True` en aquellos elementos que cumplan la condición de mínimo local. De esta forma cumplo también una de las reglas de oro de Software Carpentry: "_Always initialize from data_".

    def busca_min_np(malla):
        minimos = np.zeros_like(malla, dtype=bool)
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

        return np.nonzero(minimos)

Encima puedo aprovechar la estupenda función `nonzero` de NumPy. Compruebo que las salidas son iguales:

    np.testing.assert_array_equal(busca_min(data)[], busca_min_np(data)[])
    np.testing.assert_array_equal(busca_min(data)[1], busca_min_np(data)[1])

Y evalúo los rendimientos:

    %timeit busca_min(data)

**OUTPUT:**

    1 loops, best of 3: 4.75 s per loop

<br>

    %timeit busca_min_np(data)

**OUTPUT:**

    1 loops, best of 3: 4.62 s per loop

Parece que los tiempos son más o menos parecidos, pero al menos ya no tengo dos objetos en memoria que van a crecer de manera aleatoria. Vamos a ver ahora cómo nos puede ayudar numba a acelerar este código.

# Paso 2: aplicando `numba.jit(nopython=True)`

Como hemos dicho antes, vamos a forzar que numba funcione en modo _nopython_ para garantizar que obtenemos una mejora en el rendimiento. Si intentamos compilar la función definida en primer lugar va a fallar, porque ya hemos dicho más arriba que una de las condiciones es que _no se puede asignar memoria a objetos nuevos_:

    busca_min_jit = numba.jit(nopython=True)(busca_min)
    busca_min_jit(data)

**OUTPUT:**

    NotImplementedError                       Traceback (most recent call last)
    <ipython-input-14-3ca127791a45> in <module>()
     1 busca_min_jit = numba.jit(nopython=True)(busca_min)
    ----> 2  busca_min_jit(data)

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py in _compile_for_args(self, *args, **kws)
     155         assert not kws
     156         sig = tuple([self.typeof_pyval(a) for a in args])
    --> 157  return self.compile(sig)
     158 
     159     def inspect_types(self, file=None):

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py in compile(self, sig)
     275                                           self.py_func,
     276                                           args=args, return_type=return_type,
    --> 277 flags=flags, locals=self.locals) 278 
     279             # Check typing error if object mode is used

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in compile_extra(typingctx, targetctx, func, args, return_type, flags, locals, library)
     545     pipeline = Pipeline(typingctx, targetctx, library,
     546                         args, return_type, flags, locals)
    --> 547  return pipeline.compile_extra(func)
     548 
     549 

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in compile_extra(self, func)
     291                 raise e
     292 
    --> 293  return self.compile_bytecode(bc, func_attr=self.func_attr)
     294 
     295     def compile_bytecode(self, bc, lifted=(),

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in compile_bytecode(self, bc, lifted, func_attr)
     299         self.lifted = lifted
     300         self.func_attr = func_attr
    --> 301  return self._compile_bytecode()
     302 
     303     def compile_internal(self, bc, func_attr=DEFAULT_FUNCTION_ATTRIBUTES):

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in _compile_bytecode(self)
     532 
     533         pm.finalize()
    --> 534  return pm.run(self.status)
     535 
     536 

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in run(self, status)
     189                     # No more fallback pipelines?
     190                     if is_final_pipeline:
    --> 191  raise patched_exception
     192                     # Go to next fallback pipeline
     193                     else:

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in run(self, status)
     181             for stage, stage_name in self.pipeline_stages[pipeline_name]:
     182                 try:
    --> 183  res = stage()
     184                 except _EarlyPipelineCompletion as e:
     185                     return e.result

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in stage_nopython_frontend(self)
     387                 self.args,
     388                 self.return_type,
    --> 389 self.locals) 390 
     391         with self.fallback_context(';Function "%s" has invalid return type';

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in type_inference_stage(typingctx, interp, args, return_type, locals)
     662         infer.seed_type(k, v)
     663 
    --> 664  infer.build_constrain()
     665     infer.propagate()
     666     typemap, restype, calltypes = infer.unify()

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in build_constrain(self)
     375         for blk in utils.itervalues(self.blocks):
     376             for inst in blk.body:
    --> 377  self.constrain_statement(inst)
     378 
     379     def propagate(self):

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in constrain_statement(self, inst)
     480     def constrain_statement(self, inst):
     481         if isinstance(inst, ir.Assign):
    --> 482  self.typeof_assign(inst)
     483         elif isinstance(inst, ir.SetItem):
     484             self.typeof_setitem(inst)

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in typeof_assign(self, inst)
     514             self.typeof_global(inst, inst.target, value)
     515         elif isinstance(value, ir.Expr):
    --> 516  self.typeof_expr(inst, inst.target, value)
     517         else:
     518             raise NotImplementedError(type(value), value)

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in typeof_expr(self, inst, target, expr)
     618                                              loc=inst.loc))
     619         else:
    --> 620  raise NotImplementedError(type(expr), expr)
     621 
     622     def typeof_call(self, inst, target, call):

    NotImplementedError: Failed at nopython (nopython frontend)
    (<class ';numba.ir.Expr';>, build_list(items=[]))

En este caso la traza es inservible y especificar los tipos de entrada no va a ayudar. Solo para verificar, vamos a ver qué pasa con el rendimiento si no forzamos el modo estricto:

    busca_min_jit_object = numba.jit()(busca_min)

    %timeit busca_min_jit_object(data)

**OUTPUT:**

    1 loops, best of 3: 4.32 s per loop

Pocas ganancias respecto a la función sin compilar. ¿Qué pasa si intentamos lo mismo con la segunda función?

    busca_min_np_jit = numba.jit(nopython=True)(busca_min_np)
    busca_min_np_jit(data)

**OUTPUT:**

    ---------------------------------------------------------------------------
    UntypedAttributeError                     Traceback (most recent call last)
    <ipython-input-17-bb9282bb2bfc> in <module>()
     1 busca_min_np_jit = numba.jit(nopython=True)(busca_min_np)
    ----> 2  busca_min_np_jit(data)

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py in _compile_for_args(self, *args, **kws)
     155         assert not kws
     156         sig = tuple([self.typeof_pyval(a) for a in args])
    --> 157  return self.compile(sig)
     158 
     159     def inspect_types(self, file=None):

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/dispatcher.py in compile(self, sig)
     275                                           self.py_func,
     276                                           args=args, return_type=return_type,
    --> 277 flags=flags, locals=self.locals) 278 
     279             # Check typing error if object mode is used

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in compile_extra(typingctx, targetctx, func, args, return_type, flags, locals, library)
     545     pipeline = Pipeline(typingctx, targetctx, library,
     546                         args, return_type, flags, locals)
    --> 547  return pipeline.compile_extra(func)
     548 
     549 

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in compile_extra(self, func)
     291                 raise e
     292 
    --> 293  return self.compile_bytecode(bc, func_attr=self.func_attr)
     294 
     295     def compile_bytecode(self, bc, lifted=(),

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in compile_bytecode(self, bc, lifted, func_attr)
     299         self.lifted = lifted
     300         self.func_attr = func_attr
    --> 301  return self._compile_bytecode()
     302 
     303     def compile_internal(self, bc, func_attr=DEFAULT_FUNCTION_ATTRIBUTES):

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in _compile_bytecode(self)
     532 
     533         pm.finalize()
    --> 534  return pm.run(self.status)
     535 
     536 

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in run(self, status)
     189                     # No more fallback pipelines?
     190                     if is_final_pipeline:
    --> 191  raise patched_exception
     192                     # Go to next fallback pipeline
     193                     else:

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in run(self, status)
     181             for stage, stage_name in self.pipeline_stages[pipeline_name]:
     182                 try:
    --> 183  res = stage()
     184                 except _EarlyPipelineCompletion as e:
     185                     return e.result

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in stage_nopython_frontend(self)
     387                 self.args,
     388                 self.return_type,
    --> 389 self.locals) 390 
     391         with self.fallback_context(';Function "%s" has invalid return type';

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/compiler.py in type_inference_stage(typingctx, interp, args, return_type, locals)
     663 
     664     infer.build_constrain()
    --> 665  infer.propagate()
     666     typemap, restype, calltypes = infer.unify()
     667 

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in propagate(self)
     388                 print("propagate".center(80, ';-';))
     389             oldtoken = newtoken
    --> 390  self.constrains.propagate(self.context, self.typevars)
     391             newtoken = self.get_state_token()
     392             if config.DEBUG:

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in propagate(self, context, typevars)
     110         for constrain in self.constrains:
     111             try:
    --> 112  constrain(context, typevars)
     113             except TypingError:
     114                 raise

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typeinfer.py in __call__(self, context, typevars)
     267         for ty in valtys:
     268             try:
    --> 269  attrty = context.resolve_getattr(value=ty, attr=self.attr)
     270             except KeyError:
     271                 args = (self.attr, ty, self.value.name, self.inst)

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typing/context.py in resolve_getattr(self, value, attr)
     82                 raise
     83 
    ---> 84  ret = attrinfo.resolve(value, attr)
     85         assert ret
     86         return ret

    /home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numba/typing/templates.py in resolve(self, value, attr)
     241         ret = self._resolve(value, attr)
     242         if ret is None:
    --> 243  raise UntypedAttributeError(value=value, attr=attr)
     244         return ret
     245 

    UntypedAttributeError: Failed at nopython (nopython frontend)
    Unknown attribute "zeros_like" of type Module(<module ';numpy'; from ';/home/juanlu/.miniconda3/envs/py34/lib/python3.4/site-packages/numpy/__init__.py';>)

Me dice que no conoce la función `zeros_like`. Si acudimos a la documentación, podemos ver las [características de NumPy soportadas por numba](http://numba.pydata.org/numba-doc/0.17.0/reference/numpysupported.html) y las funciones de creación de arrays _no_ figuran entre ellas. Esto es consistente con lo que hemos dicho más arriba: no vamos a poder asignar memoria a objetos nuevos.

# Paso 3: Reestructurar el código

¿Estamos en un callejón sin salida entonces? ¡En absoluto! Lo que vamos a hacer va a ser separar la parte intensiva de la función para aplicar `numba.jit` sobre ella, e inicializar todos los valores desde fuera. Para los que hayan usado subrutinas en Fortran este enfoque les resultará familiar 🙂

    :::python
    def busca_min_np_jit(malla):
        minimos = np.zeros_like(malla, dtype=bool)

        _busca_min(malla, minimos)

        return np.nonzero(minimos)

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

Veamos qué ocurre ahora:

    busca_min_np_jit(data)

**OUTPUT:**

    (array([   1,    1,    1, ..., 1998, 1998, 1998]),
     array([   1,    3,   11, ..., 1968, 1977, 1985]))

<br>

    np.testing.assert_array_equal(busca_min(data)[], busca_min_np_jit(data)[])
    np.testing.assert_array_equal(busca_min(data)[1], busca_min_np_jit(data)[1])

    %timeit busca_min_np_jit(data)

**OUTPUT:**

    10 loops, best of 3: 62.9 ms per loop

Habéis leído bien: **70x más rápido** 🙂  
¡Lo hemos conseguido! Ahora nuestro código funciona en numba sin problemas y encima es endemoniadamente rápido. Para completar la comparación en mi ordenador, voy a reproducir también la función hecha en Cython:

    :::python
    %load_ext cython

    %%cython --name probandocython9
    import numpy as np
    cimport numpy as np
    from cpython cimport array as c_array
    from array import array
    cimport cython

    @cython.boundscheck(False) 
    @cython.wraparound(False)
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

    10 loops, best of 3: 151 ms per loop

Por tanto, vemos que **la versión con numba es el doble de rápida que la versión con Cython**. Sobre gustos no hay nada escrito: yo por ejemplo valoro no «salirme» de Python usando numba mientras que a otro puede no importarle incluir especificaciones de tipos como en Cython. Los números, eso sí, son los números 🙂

# Más casos de éxito

# La atmósfera estándar

El **cálculo de propiedades termodinámicas de la atmósfera estándar** es un problema clásico que todo aeronáutico ha afrontado alguna vez muy al principio de su carrera formativa. La teoría es simple: imponemos una ley de variación de la temperatura con la altura $T = T(h)$, la presión se obtiene por consideraciones hidrostáticas $p = p(T)$ y la densidad por la ecuación de los gases ideales $rho = rho(p, T)$. La particularidad de la atmósfera estándar es que imponemos que la variación de la temperatura con la altura es una función simplificada _y definida a trozos_, así que calcular temperatura, presión y densidad dada una altura se parece mucho a hacer esto:

    if 0.0 <= h < 11000.0:
        T = T0 + alpha * h
        p = ...  # Algo que depende de T
        rho = p / (R_a * T)
    elif 11000.0 <= h < 20000.0:
        T = T1
        p = ...
        rho = p / (R_a * T)
    elif 20000.0 <= h <= 32000.0:
        ...

El problema viene cuando se quiere **vectorizar** esta función y permitir que `h` pueda ser un array de alturas. Esto es muy conveniente cuando queremos pintar alguna propiedad con matplotlib, por ejemplo.  
Se intuye que hay dos formas de hacer esto: utilizando funciones de NumPy o iterando por cada elemento del array. La primera solución se hace farragosa, y la segunda, gracias a la proverbial lentitud de Python, es extremadamente lenta. Mi amigo [Álex](http://twitter.com/Alex__S12) y yo llevamos pensando sobre este problema _años_, y nunca hemos llegado a una solución satisfactoria (incluso [encontramos algunos bugs en `numpy.piecewise`](https://github.com/numpy/numpy/pull/331) por el camino). Este año decidimos cerrar este asunto definitivamente así que con [el equipo AeroPython](https://github.com/AeroPython) exploramos varias implementaciones distintas. Hasta que por fin lo conseguimos: **usamos numba para acelerar los bucles**.  
![numba gana a C++](https://cloud.githubusercontent.com/assets/316517/6236738/63dabc48-b6ed-11e4-822f-2c36c0d96f76.png)  
Como podéis leer [en la discusión original](https://github.com/AeroPython/aeropy/issues/4#issuecomment-74748524), la función de la primera columna está escrita en C++. ¿Impresionado? 😉

# Solución de Navier de una placa plana

Para mi proyecto fin de carrera me encontré con la necesidad de calcular la deflexión de una placa rectangular, simplemente apoyada en sus cuatro bordes (es decir, los bordes pueden girar: no están empotrados) sometida a una carga transversal. Este problema tiene solución analítica conocida desde hace tiempo, hallada por Navier:  
$displaystyle w(x,y) = sum_{m=1}^infty sum_{n=1}^infty frac{a_{mn}}{pi^4 D},left(frac{m^2}{a^2}+frac{n^2}{b^2}right)^{-2},sinfrac{m pi x}{a}sinfrac{n pi y}{b}$

siendo $a_{mn}$ los coeficientes de Fourier de la carga aplicada. Como veis, para cada punto $(x, y)$ hay que hacer una doble suma en serie; si encima queremos evaluar esto en un `meshgrid`, necesitamos **un cuádruple bucle**. Ya se anticipa que por muy hábiles que estemos, a Python le va a costar.  
La clave estuvo, una vez más, en usar numba para optimizar los bucles. En GitHub tenéis [el código completo](https://gist.github.com/Juanlu001/cf19b1c16caf618860fb), pero la parte importante es esta:

    @numba.jit(nopython=True)
    def a_mn_point(P, a, b, xi, eta, mm, nn):
        """Navier series coefficient for concentrated load.

     """
        return 4 * P * sin(mm * pi * xi / a) * sin(nn * pi * eta / b) / (a * b)
     
     
    @numba.jit(nopython=True)
    def plate_displacement(xx, yy, ww, a, b, P, xi, eta, D, max_m, max_n):
        max_i, max_j = ww.shape
        for mm in range(1, max_m):
            for nn in range(1, max_n):
                for ii in range(max_i):
                    for jj in range(max_j):
                        a_mn = a_mn_point(P, a, b, xi, eta, mm, nn)
                        ww[ii, jj] += (a_mn / (mm**2 / a**2 + nn**2 / b**2)**2
                                       * sin(mm * pi * xx[ii, jj] / a)
                                       * sin(nn * pi * yy[ii, jj] / b)
                                       / (pi**4 * D)) 

![](https://www.pybonacci.org/images/2015/03/solucion_placa_plana.png?style=centerme)

Podéis comprobar vosotros mismos que las diferencias de rendimiento en este caso son brutales. _Y solo hemos añadido una línea a cada función_.

# Conclusiones

numba aún no es una herramienta estable, pero está rápidamente alcanzando un grado de madurez suficiente para optimizar código orientado a operar con arrays. Gracias a conda es trivial de instalar y los resultados respecto a soluciones más maduras como Cython son aplastantes, tanto en velocidad de ejecución como en la complejidad del código resultante.  
De momento yo me quedo con numba, ¿y tú? 😉
