---
title: El producto de matrices y el nuevo operador @
date: 2016-02-22T15:00:46+00:00
author: Álex Sáez
slug: el-producto-de-matrices-y-el-nuevo-operador
tags: arrays, científico, dot, matrices, matrix, multiplicación, numpy, pep 465, product, python 3.5

## Introducción.

El 13 de septiembre de 2015 fue lanzada la versión 3.5 de Python. Entre las <a href="https://docs.python.org/3/whatsnew/3.5.html" target="_blank">novedades</a> podemos encontrar la inclusión del <a href="http://legacy.python.org/dev/peps/pep-0465/" target="_blank">PEP 465</a> que trata sobre el nuevo operador `@` para la multipliación matricial y del que hablaremos en este post. Como bien sabrán los lectores de este blog, los arrays son la piedra angular de numerosísimas áreas de la programación científica y sirven para realizar operaciones de forma masiva y mucho más eficiente. Esto, sumado a la posibilidad de utilizarlos como matrices, proporciona una herramienta muy potente para llevar a cabo operaciones algebraicas. NumPy es la librería que nos permite utilizar esta maravillosa estructura de datos y según figura en el ya citado <a href="http://legacy.python.org/dev/peps/pep-0465/#but-isn-t-matrix-multiplication-a-pretty-niche-requirement" target="_blank">PEP</a>, podría ser la librería fuera de la librería estándar más importada del mundo Python.

<!--more-->

A modo de recordatorio de la eficiencia de los arrays:

<pre><code class="language-python">import numpy as np

a = np.random.rand(1000, 1000)
b = np.random.rand(1000, 1000)

%timeit c = a + b
# 100 loops, best of 3: 4.01 ms per loop

c = np.empty_like(a)

%%timeit
for ii in range(a.shape[0]):
 for jj in range(a.shape[1]):
 c[ii, jj] = a[ii, jj] + b[ii, jj]
# 1 loop, best of 3: 857 ms per loop
</code></pre>

No hace falta decir nada acerca de las ventajas de una u otra implementación.

##  La situación previa.

Todo esto está muy bien, pero el problema se presentaba a la hora de hacer multiplicaciones. El operador `*` en los `numpy.ndarray` realiza multiplicaciones elemento a elemento por lo que, hasta ahora, había dos posibilidades si lo que uno quería era hacer una multiplicación matricial:

  1. Usar la función o el método `dot`.
  2. Usar la clase `numpy.matrix` para la cual el operador `*` sí devuelve el producto matricial.

Los inconvenientes de la primera opción resultan evidentes cuando hay que implementar una fórmula del tipo:

$\displaystyle \textbf{K}\_{k} = \textbf{P}\_{k|k-1}\textbf{H}\_k^{\text{T}}(\textbf{H}\_{k} \textbf{P}\_{k|k-1} \textbf{H}\_{k}^{\text{T}} + \textbf{R}_{k})^{-1} $

que para los curiosos es la ganancia óptima de un <a style="color: #337ab7" href="https://en.wikipedia.org/wiki/Kalman_filter" target="_blank">filtro de Kalman</a> y que plasmado en código quedaría algo así como:

<pre><code class="language-python">from scipy.linalg import inv
K = np.dot(np.dot(P, H.T), inv(np.dot(np.dot(H, P), H.T) + R))
</code></pre>

Utilizando el método `dot,` en lugar de la función, la cosa mejora algo en cuando a la longitud de la línea, pero poco en cuanto a la legibilidad:

<pre><code class="language-python">K = P.dot(H.T).dot(inv(H.dot(P).dot(H.T) + R))
</code></pre>

en estas circunstancias podríamos pensar en utilizar la clase `numpy.matrix` en vez de la clase `numpy.ndarray` e implementar la fórmula anterior de una manera mucho más natural:

<pre><code class="language-python">K = P * H.T + (H * P * H.T + R )
</code></pre>

que como vemos es inmediatamente equiparable a lo que se puede leer en un libro. El problema viene cuando empaquetamos esta fórmula en una función y a alguien se le ocurre pasarle como entrada un `numpy.ndarray`: la función **devolverá un resultado, sí, pero un resultado incorrecto** y que es probable que sea de un orden de magnitud comparable al esperado. Conclusión: estaríamos ante el problema que a cualquiera le gustaría encontrarse en un código, un resultado erróneo y del orden de magnitud del esperado que viene de vaya usted a saber dónde... Por este motivo `numpy.matrix` está altamente desaconsejado por la propia comunidad NumPy. Se podría utilizar utilizar la programación defensiva para detectar y corregir esta situación, sin emabrgo, en ese caso nuestras funciones comenzarían a estar plagadas de `isinstance(arr, np.ndarray)` y similares, que tampoco favorecerán la simplicidad de nuestro script.

## La solución.

El ejemplo anterior muestra que de las <a href="http://legacy.python.org/dev/peps/pep-0465/#rejected-alternatives-to-adding-a-new-operator" target="_blank">múltiples soluciones posibles</a>, la de asociar la multiplicación matricial a una clase a través de un operador y la multiplicación elemento a elemento a otra con el mismo operador no era la más recomendable. En lugar de diferenciar por clases, parecía más lógico **diferenciar por operador binario** para poder realizar esta operación de forma cómoda. Además, en el PEP 465 se lleva a cabo una estimación de lo útil que sería tener un operador cómo este comparando el número de veces que se usa la función dot con respecto a los operadores binarios en varios proyectos y la conclusión es abrumadora: la multiplicación de matrices es, en estos paquetes, más frecuente que la mayoría de operadores de comparación (`<=`, `>=`, != ...), la división entera (`//`) o las operaciones "inline" (`+=`, `*=` ...). Una vez justificada la necesidad, la siguiente pregunta es tan obvia como difícil de consensuar: ¿qué símbolo asociamos al operador?

El resultado final resultó ser utilizar el caracter `@,` ya que parecía ser una buena elección por los siguientes motivos (algunos incluso graciosos):

  * Los usuarios están acostumbrados a usarlo en los decoradores y sin embargo no introduce ninguna incompatibilidad. Tampoco resulta fácil confundir un decorador como `@property` con una multiplicación como `H @ P @ H.T`.
  * Está presente en numerosas disposiciones de teclado.
  * Es redondo como `*` y `·`
  * La regla nemotécnica m**AT**rices es ingeniosa.
  * Su forma curvada recuerda a las pasadas sobre filas y columnas que hay que hacer en un producto matricial (este es mi motivo favorito).
  * Su asimetría evoca la no conmutatividad de la operación.
  * Y por último: _da igual, había que escoger alguno..._

## Funcionamiento

Repasada la historia que precede a la introducción de este operador, vayamos a la parte práctica: ¿cómo se usa? Volviendo al ejemplo anterior, la fórmula quedaría:

<pre><code class="language-python">K = P @ H.T + (H @ P @ H.T + R )</code></pre>

En este caso, todos las operaciones son entre "matrices", o siendo puristas, entre arrays de dos dimensiones. Si las dimensiones son las adecuadas, los productos y sumas se calcularán sin problemas.

Además, esta operación también está definida entre arrays de una dimensión y arrays de dos. Este caso coresponde a premultiplicar una matriz por un vector fila, dando como resultado un vector fila; o postmultiplicar por un vector columna, obteniendo otro vector columna. Pero veamos qué ocurre realmente:

<pre><code class="language-python">mat = np.array([[1, 5, 8, 5],
                [0, 6, 4, 2],
                [9, 3, 1, 6]])

vec1 = np.array([5, 6, 2])

vec1 @ mat

# array([23, 67, 66, 49])
</code></pre>

<pre><code class="language-python">vec2 = np.array([2, 0, 3, 1])
mat @ vec2

# array([31, 14, 27])
</code></pre>

Vemos que en ambos casos el resultado es <em style="color: #000000">casi</em> el descrito arriba. La diferencia radica en que no hemos obtenido un vector fila o columna, sino simplemente un array unidimensional. Entonces, ¿cuál es el procedimiento interno? El atributo `shape` de un array de una dimensión devuelve una tupla con un solo valor igual al número de elementos, en una "matriz" devuelve dos elementos que corresponden al número de filas y columnas:

<pre><code class="language-python">vec1.shape
# (3,)
mat.shape
# (3, 4)
</code></pre>

Si estamos multiplicando por una matriz, _al vector se le añadirá una dimensión más de tamaño unidad por el exterior_. Esto quiere decir que:

  * `vec1(3) @ mat(3, 4)` pasará a ser `vec1(`**1**`, 3) @ mat(3, 4)`.
  * `mat(3, 4) @ vec2(4)` pasará a ser `mat(3, 4) @ vec2(4,`**1**`)`.

_La operación se realiza, en realidad, entre arrays bidimensionales y finalmente el resultado se convierte a un array unidimensional_. Esto nos evita el tener que explicar a un principiante que la forma de hacer esta operación es:

<pre><code class="language-python">vec1[np.newaxis, :] @ mat
# array([[23, 67, 66, 49]])
vec1.reshape(1, -1) @ mat
# array([[23, 67, 66, 49]])
</code></pre>

Que sin embargo, sí devuelven "vectores fila" o "columna" según corresponda. Pero... ¿quién querría escribir algo como esto?

<pre><code class="language-python">(vec1[np.newaxis, :] @ mat @ vec2[:, np.newaxis])[0, 0]
# 293
</code></pre>

en lugar de:

<pre><code class="language-python">vec1 @ mat @ vec2
# 293
</code></pre>

Cabe resaltar que la asociatividad del operador indica que la operación se realizará en el siguiente orden:

<pre><code class="language-python">(vec1 @ mat) @ vec2
# 293
</code></pre>

Por lo que en algunos casos los paréntesis pueden hacernos ganar algo de velocidad:

<pre><code class="language-python">mat = np.random.randn(1000, 1000)
vec = np.random.randn(1000)
%timeit mat.T @ mat @ vec
# 10 loops, best of 3: 131 ms per loop

% timeit mat.T @ (mat @ vec)
# 100 loops, best of 3: 2.39 ms per loop
</code></pre>

¿Se te ocurre por qué?

La última característica que resaltaremos muy rápidamente es el **broadcasting**, que nos permite hacer multiplicaciones matriciales de forma masiva. Así: `arr(100, 10, 3) @ arr(100, 3, 5)` realizará 100 multiplicaciones de matrices de `(10x3) @ (3X5)` devolviendo `arr(100, 10, 5)` con el resultado de cada multiplicación a lo largo de la primera dimensión. Incluso podríamos hacer algo como: `arr(100, 10, 5) @ vec(5)` ¿Te atreves a explicarnos lo que saldrá de aquí? Este tipo de operaciones no se pueden hacer con la función `dot` y habría que recurrir a la función `matmul.`

## Conclusiones

El nuevo operador `@` es realmente útil para una parte amplia de la comunidad Python. Prueba de ello es la rápida acogida que ha tenido en paquetes tan relevantes como: pandas, numpy, blaze o theano. Su introducción no supone ninguna incompatibilidad y además facilitará enormemente la lectura y escritura de código científico.

No menos importante, es que Python se mostrará como un lenguaje mucho más cómodo y fácil para los principiantes (y no tan principiantes) manteniendo la coherencia con varios puntos de su Zen (`import this`): "Beautiful is better than ugly", "flat is better than nested", "readability counts", "there should be one-- and preferably only one --obvious way to do it"; y, por supuesto, "now is better than never" y "special cases <del>aren't</del> **are sometimes** special enough to <del>break</del> **change** the rules".

Por último, cabe destacar que una de nuestras librerías favoritas, SymPy, seguirá usando `*` para la multiplicación de matrices, al menos de momento, ya que la multiplicación elemento a elemento no tiene gran relevancia en el contexto del cálculo simbólico.

¿Qué te parece a ti el nuevo operador? ¿Lo usas actualmente? ¿Adaptarás tu código antiguo? Cuéntanoslo en los comentarios.

## Referencias.

  * [1] [PEP 465](http://legacy.python.org/dev/peps/pep-0465/)
  * [2] [Stackoverflow: Difference between numpy dot() and Python 3.5+ matrix multiplication @](http://stackoverflow.com/questions/34142485/difference-between-numpy-dot-and-python-3-5-matrix-multiplication)