---
title: MicroEntradas: numpy.vectorize
date: 2014-01-31T06:30:47+00:00
author: Kiko Correoso
slug: microentradas-numpy-vectorize
tags: MicroEntradas, np.vectorize, numpy, numpy.vectorize, vectorización

Hoy vamos a ver [`numpy.vectorize`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.vectorize.html) 
que, como la documentación oficial indica, sirve para 'vectorizar' 
funciones que solo aceptan escalares como entrada. La entrada que 
podemos meter es una lista de objetos o un 'numpyarray' y nos devolverá 
como resultado un 'numpyarray'.

No os engañéis, normalmente, cuando hablamos de vectorizar pensamos en 
varios órdenes de magnitud de mejora en el rendimiento pero eso no es 
lo que hace esta función :-). Podéis pensar en esta función como algo 
parecido a usar [`map`](http://docs.python.org/3.3/library/functions.html#map).

Por ejemplo, la función [`abs`](http://docs.python.org/3.3/library/functions.html#abs) 
solo acepta un entero o un _float_. Por ejemplo, lo siguiente:

```python
print(abs(-3))
```

Nos devolvería el valor `3`. Hasta ahí bien. Pero si queremos hacer lo siguiente:

```python
print(abs([-3, -2]))
```

Nos devolverá un `TypeError: bad operand type for abs(): 'list'.`

Podríamos usar `map` para ello pero no obtendríamos un 'numpyarray' como 
salida y en Python 3 devuelve un iterador que para transformarlo a, 
por ejemplo, una lista o un 'numpyarray' debemos añadir un paso más, 
la conversión a lista (en Python 2 devuelve directamente una lista) o 
dos pasos, la conversión a lista y esta a 'numpyarray'.

Vamos a ver cómo podemos 'vectorizar' la función `abs` sin usar `map` y 
usando `numpy.vectorize` (antes deberéis importar `numpy` como `np`):

```python
vectabs = np.vectorize(abs)
```

que podemos usar de la siguiente forma:

```python
print(vectabs([-3, -2]))
```

Et voilà. ya tenemos lo que queríamos. Veamos como va el rendimiento de 
lo que acabamos de hacer:

```python
In [1]: import numpy as np
In [2]: kk = np.random.randn(1000000)
In [3]: timeit np.abs(kk)
100 loops, best of 3: 4.13 ms per loop
In [4]: vectabs = np.vectorize(abs)
In [5]: timeit vectabs(kk)
10 loops, best of 3: 87.6 ms per loop
In [6]: timeit np.array([abs(i) for i in kk])
1 loops, best of 3: 241 ms per loop
```

La última opción es equivalente a hacer `np.array(list(map(abs, kk)))` 
en tiempo. La versión vectorizada, `vectabs`, es 21 veces más lenta que 
la que podemos obtener usando `numpy.abs` por lo que no tendríamos una 
gran ganancia pero, sin embargo, vemos que es casi tres veces más rápida 
que la versión usando map (o una 'list comprehension') por lo que algo 
ganariamos respecto a Python 3 puro :-). 

Como apuntes finales, si sabéis de alguna función en CPython que no 
existe equivalente en numpy y la necesitáis usar quizá podéis obtener 
una ganancia usando numpy.vectorize. Si tenéis que escribir la función 
vosotros, escribidla pensando en operaciones vectorizadas usando 
'numpyarrays' y no os hará falta usar `numpy.vectorize`.

Como punto final. recordad que np.vectorize no es más que un decorador 
por lo que lo siguiente sería perfectamente válido:

```python
@np.vectorize
def mi_funcion(*args):
    ...
```

Saludos.

[Editado: corrección de algún bug, disculpas!!]
