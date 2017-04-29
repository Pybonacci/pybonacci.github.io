---
title: Optimización en Python: CVXOpt
date: 2013-12-13T18:00:13+00:00
author: Jorge Bernabé Ruiz
slug: optimizacion-en-python-cvxopt

## ¿Qué es CVXOpt?

CVXOpt es un paquete gratuito que se emplea para la optimización convexa y que está basado en el lenguaje de programación de Python. Su principal propósito es conseguir el desarrollo de software para aplicaciones de optimización convexa mediante la construcción de una librería estándar extensa de Python y empleando las fortalezas de Python como lenguaje de programación de alto nivel.

[CVXOpt](http://cvxopt.org/) fue desarrollado inicialmente por Martin Andersen, Joachim Dahl y Lieven Vandenberghe para emplearlo en su propio trabajo, haciéndolo disponible para otras personas.

## ¿Qué es la optimización convexa?

La optimización convexa es un tipo de programación matemática (programación convexa) en la que se estudia el caso en el que la función objetivo es convexa - minimización - y en la que el conjunto de restricciones del problema es convexa. Este tipo de optimización incluye la programación lineal (el conjunto de las ecuaciones del problema es lineal)

Matemáticamente, el problema se formula de la siguiente manera:

<p style="text-align:center;">
  <img alt="ec" src="http://www.subeimagenes.com/img/ecs-793019.jpg" />
</p>

Explicando de una manera más sencilla las ecuaciones anteriores: se tiene una función objetivo que se pretende minimizar (o maximizar, aunque este hecho es una trivialidad, ya que únicamente afecta al cambio de signo de la función objetivo) Dicha función objetivo está sujeta a una serie de restricciones convexas, que pueden ser de desigualdad o igualdad, y que determinan una región factible del problema. Todos los puntos del interior de dicha región constituyen soluciones del problema, pero en optimización se busca el mejor de todos ellos.

En la siguiente figura, se aprecia un ejemplo de lo anterior: los puntos verdes son puntos no factibles, ya que están fuera de la región factible y no cumplen las restricciones del problema. Los puntos amarillos constituyen un conjunto de soluciones del problema que cumplen las restricciones, pero que no son el punto óptimo. En cambio, el punto rojo sí que es el óptimo ya que es el mejor posible en el sentido de la función objetivo, indicado por la flecha negra.

<p style="text-align:center;">
  <img alt="grafo" src="http://www.subeimagenes.com/img/imagen-793020.jpg" />
</p>

### ¿Cómo se instala CVXOpt?

Para instalar CVXOpt se puede acudir a la página web de los desarrolladores del paquete: <http://cvxopt.org/install/index.html> donde se puede descargar gratuitamente y donde nos indican cómo realizar la instalación del mismo.

## Trabajando con CVXOpt

CVXOpt es un paquete de optimización que emplea notación matricial para resolver problemas de optimización. Incluye tanto matrices densas como matrices dispersas (matrices con muchos términos nulos o ceros)

  * Las matrices densas se llaman mediante la función _matrix_. Los argumentos especifican los valores de los coeficientes, las dimensiones y el tipo de la matriz, siguiendo la siguiente nomenclatura:

<p style="text-align:center;">
  <code>cvxopt.matrix(x[,size[,tc]])</code>
</p>

  1. `size` es un tuple (objeto que contiene otros objetos) con las dimensiones de la matriz y, por tanto, tiene longitud dos. El número de filas y/o columnas no puede ser cero.
  2. `tc` es el tipo de código. Los posibles valores son _‘i’_, _‘d’_, y _‘z’_ para matrices enteras (integer), reales (double) y complejas, respectivamente.
  3. `x` puede ser un número, una secuencia de números, una matriz densa o dispersa, un vector Numpy de una o dos dimensiones o una lista de matrices y números.

Para mostrar la notación empleada, se muestra el siguiente ejemplo:

<pre><code class="language-python">&gt;&gt;&gt; from cvxopt import matrix
&gt;&gt;&gt; A = matrix(1, (1,4))
&gt;&gt;&gt; print(A)
[ 1 1 1 1]
&gt;&gt;&gt; A = matrix(1.0, (1,4))
&gt;&gt;&gt; print(A)
[ 1.00e+00 1.00e+00 1.00e+00 1.00e+00]
&gt;&gt;&gt; A = matrix(1+1j)
&gt;&gt;&gt; print(A)
[ 1.00e+00+j1.00e+00]
&gt;&gt;&gt; print(matrix([[1., 2.], [3., 4.], [5., 6.]]))
[ 1.00e+00 3.00e+00 5.00e+00]
[ 2.00e+00 4.00e+00 6.00e+00]
&gt;&gt;&gt; A1 = matrix([1, 2], (2,1))
&gt;&gt;&gt; B1 = matrix([6, 7, 8, 9, 10, 11], (2,3))
&gt;&gt;&gt; B2 = matrix([12, 13, 14, 15, 16, 17], (2,3))
&gt;&gt;&gt; B3 = matrix([18, 19, 20], (1,3))
&gt;&gt;&gt; C = matrix([[A1, 3.0, 4.0, 5.0], [B1, B2, B3]])
&gt;&gt;&gt; print(C)
[ 1.00e+00 6.00e+00 8.00e+00 1.00e+01]
[ 2.00e+00 7.00e+00 9.00e+00 1.10e+01]
[ 3.00e+00 1.20e+01 1.40e+01 1.60e+01]
[ 4.00e+00 1.30e+01 1.50e+01 1.70e+01]
[ 5.00e+00 1.80e+01 1.90e+01 2.00e+01]</code></pre>

  * Las matrices dispersas se llaman mediante el comando `spmatrix`. Las matrices dispersas se suelen definir mediante tripletes en los que se indica el valor numérico, la posición en la fila y la posición en la columna. A modo de ejemplo, el valor 5 que se encuentra en la primera fila y en la segunda columna se nota como (5, 0, 1) Nótese que la primera fila o columna se indica mediante un cero.

<img class="aligncenter" alt="matriz" src="http://www.subeimagenes.com/img/matrix-793022.jpg" />
  
La llamada al comando `spmatrix` se hace de la siguiente forma:

<p style="text-align:center;">
  <code>cvxcopt.spmatrix(x,I,J[,size[,tc]])</code>
</p>

  1. `I` y `J` son secuencias de números enteros o matrices enteras que contienen los índices de las filas y las columnas de las entradas no cero. La longitud de I y J debe ser igual.
  2. `size` es un tuple de enteros no negativos con filas y columnas de las dimensiones de la matriz. Este argumento es únicamente necesario cuando se crea una matriz con una fila o columna con todos sus valores igual a cero.
  3. `tc` es tipo de código, _‘d’_ o _‘z’_ para matrices dobles o complejas, respectivamente.
  4. `x` puede ser un número, una secuencia de números o una matriz densa.

A continuación, se muestra cómo se escribe la notación para escribir estas matrices:

<pre><code class="language-python">&gt;&gt;&gt; from cvxopt import spmatrix
&gt;&gt;&gt; A = spmatrix(1.0, range(4), range(4))
&gt;&gt;&gt; print(A)
[ 1.00e+00 0 0 0 ]
[ 0 1.00e+00 0 0 ]
[ 0 0 1.00e+00 0 ]
[ 0 0 0 1.00e+00]
&gt;&gt;&gt; A = spmatrix([2,-1,2,-2,1,4,3], [1,2,0,2,3,2,0], [0,0,1,1,2,3,4])
&gt;&gt;&gt; print(A)
[ 0 2.00e+00 0 0 3.00e+00]
[ 2.00e+00 0 0 0 0 ]
[-1.00e+00 -2.00e+00 0 4.00e+00 0 ]
[ 0 0 1.00e+00 0 0 ]</code></pre>

Hay que reseñar que existen más formas para definir las matrices y muchas operaciones aritméticas que se realizan en el paquete CVXOpt. Para tener más información de las mismas, se recomienda visitar el siguiente enlace: <http://cvxopt.org/userguide/matrices.html>

Para resolver problemas de optimización CVXOpt llama a una serie de solvers siendo algunos muy generales como `cvxopt.umfpack` o `cvxopt.cholmod` que resuelven ecuaciones lineales agrupadas en matrices del tipo $AX = B$.

En cualquier caso, por lo general, es mejor opción emplear algún solver más potente, como ocurre con `cvxopt.solvers`, dentro de los cuales existen diferentes opciones de solvers, siendo `lp` – para programación lineal - y `qp` – para programación cuadrática - los principales (aunque en función de cómo sea el programa, sería conveniente emplear otro de los disponibles)

## Programación lineal con CVXOpt

La programación lineal supone el caso más común de la programación y, por ello, nos detenemos en cómo se lleva a cabo con CVXOpt. Como se ha mencionado anteriormente, el comando cvxopt.solvers.lp es el mejor para realizar programación de este tipo. La llamada al mismo se hace de la siguiente manera:

<p align="center">
  <code>cvxopt.solvers.lp(c, G, h[, A, b[, solver[, primalstart[, dualstart]]]])</code>
</p>

Esta sentencia nos va a permitir resolver tanto el problema principal - o primal  - y el problema secundario - o dual  - relacionado con el principal.

<p style="text-align:center;">
  <img alt="prim" src="http://www.subeimagenes.com/img/primal-793023.jpg" />   <img alt="" src="http://www.subeimagenes.com/img/dual-793024.jpg" />
</p>

El argumento _solver_ se puede dejar en blanco – con lo que el programa emplearía _conelp_ por defecto - o bien emplear algún solver instalado externamente a este paquete, como puede ser GLPK o MOSEK. A modo de ejemplo, se muestra la siguiente notación para el LP siguiente:

<p style="text-align:center;">
  <img alt="" src="http://www.subeimagenes.com/img/lp-793026.jpg" />
</p>

<pre><code class="language-python">&gt;&gt;&gt; from cvxopt import matrix, solvers
&gt;&gt;&gt; c = matrix([-4., -5.])
&gt;&gt;&gt; G = matrix([[2., 1., -1., 0.], [1., 2., 0., -1.]])
&gt;&gt;&gt; h = matrix([3., 3., 0., 0.])
&gt;&gt;&gt; sol = solvers.lp(c, G, h)
&gt;&gt;&gt; print(sol['x'])
[ 1.00e+00]
[ 1.00e+00]</code></pre>

## Optimización en CVXOpt

En los casos en los que se tiene una función objetivo y una serie de restricciones en las que es complicado modificar el problema – principalmente, la modificación de las desigualdades - es posible realizar un modelado del problema, especificando la función objetivo, las restricciones y las variables del mismo. Para ello, se puede llamar a la siguiente función:

<p style="text-align:center;">
  <code>cvxopt.modeling.op([objective[,constraints[,name]]])</code>
</p>

Por defecto, se va a minimizar la función objetivo, que se puede definir aparte o en esa misma línea. _Constraints_ hace referencia a las restricciones y puede ser tanto una restricción como una lista de restricciones. Finalmente, _name_ indica el nombre del problema.

Por lo general, en un problema de modelado, es conveniente incluir los siguientes atributos:

  * `objective` – Función objetivo, en muchas ocasiones relacionada con el coste.

  * `variables()` – Devuelve una lista con las variables del problema

  * `constraints()` – Devuelve una lista de restricciones

  * `inequalities()` – Devuelve una lista de restricciones de desigualdad

  * `equalities()` – Devuelve una lista de restricciones de igualdad

  * `solve([format[,solver]])` – esta función convierte el problema de optimización en un programa lineal en forma matricial y lo resuelve empleando el solver de la programación lineal.

Como ejemplo, se puede resolver el sistema lineal siguiente empleando dos notaciones distintas, la primera modelizando el problema con las ecuaciones independientes y la segunda agrupándolas en una única matriz:

<p style="text-align:center;">
  <img alt="" src="http://www.subeimagenes.com/img/lp2-793028.jpg" />
</p>

<pre><code class="language-python">&gt;&gt;&gt; from cvxopt.modeling import op
&gt;&gt;&gt; x = variable()
&gt;&gt;&gt; y = variable()
&gt;&gt;&gt; c1 = ( 2*x+y &gt;&gt; c2 = ( x+2*y &gt;&gt; c3 = ( x &gt;= 0 )
&gt;&gt;&gt; c4 = ( y &gt;= 0 )
&gt;&gt;&gt; lp1 = op(-4*x-5*y, [c1,c2,c3,c4])
&gt;&gt;&gt; lp1.solve()
&gt;&gt;&gt; lp1.status
'optimal'
&gt;&gt;&gt; print(lp1.objective.value())
[-9.00e+00]
&gt;&gt;&gt; print(x.value)
[ 1.00e+00]
&gt;&gt;&gt; print(y.value)
[ 1.00e+00]
&gt;&gt;&gt; print(c1.multiplier.value)
[ 1.00e+00]
&gt;&gt;&gt; print(c2.multiplier.value)
[ 2.00e+00]
&gt;&gt;&gt; print(c3.multiplier.value)
[ 2.87e-08]
&gt;&gt;&gt; print(c4.multiplier.value)
[ 2.80e-08]
&gt;&gt;&gt; from cvxopt.modeling import op, dot
&gt;&gt;&gt; x = variable(2)
&gt;&gt;&gt; A = matrix([[2.,1.,-1.,0.], [1.,2.,0.,-1.]])
&gt;&gt;&gt; b = matrix([3.,3.,0.,0.])
&gt;&gt;&gt; c = matrix([-4.,-5.])
&gt;&gt;&gt; ineq = ( A*x &gt;&gt; lp2 = op(dot(c,x), ineq)
&gt;&gt;&gt; lp2.solve()
&gt;&gt;&gt; print(lp2.objective.value())
[-9.00e+00]
&gt;&gt;&gt; print(x.value)
[ 1.00e+00]
[ 1.00e+00]
&gt;&gt;&gt; print(ineq.multiplier.value)
[1.00e+00]
[2.00e+00]
[2.87e-08]
[2.80e-08]</code></pre>

En definitiva, dentro de Python nos encontramos con una serie de paquetes de optimización (en este artículo hemos visto CVXOpt, aunque existen más como Pyomo) que nos permiten realizar problemas de optimización más o menos complejos con resultados totalmente satisfactorios y que nos pueden servir tanto a nivel académico como a nivel profesional.

Jorge M. Bernabé Ruiz ([@Jorge_Poti](http://twitter.com/Jorge_Poti)) de [@CAChemEorg](http://www.cacheme.org).