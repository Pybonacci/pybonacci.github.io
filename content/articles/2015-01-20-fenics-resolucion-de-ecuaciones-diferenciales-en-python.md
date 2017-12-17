---
title: FEniCS: Resolución de ecuaciones diferenciales en Python
date: 2015-01-20T22:48:28+00:00
author: Juan Luis Cano
slug: fenics-resolucion-de-ecuaciones-diferenciales-en-python
tags: conda, ecuaciones diferenciales, EDPs, fenics, python

## Introducción

En este artículo os voy a presentar el **[proyecto FEniCS](http://fenicsproject.org/)**, una colección de _bibliotecas escritas con interfaz en Python_ para la _resolución de ecuaciones diferenciales por el [método de los elementos finitos](http://es.wikipedia.org/wiki/M%C3%A9todo_de_los_elementos_finitos)_. FEniCS proporciona un método muy inteligente para automatizar los procesos más laboriosos de la solución de este tipo de ecuaciones, de forma que podemos atacar cualquier problema que se nos ocurra. Las posibilidades son inmensas y la documentación es bastante exhaustiva, así que aquí veremos una introducción a **cómo resolver ecuaciones en derivadas parciales con FEniCS**.<figure id="attachment_3098" style="width: 300px" class="wp-caption aligncenter">

[<img src="http://pybonacci.org/wp-content/uploads/2015/01/plate-300x237.png" alt="Placa rectangular simplemente apoyada resuelta con FEniCS" width="300" height="237" class="size-medium wp-image-3098" srcset="https://pybonacci.org/wp-content/uploads/2015/01/plate-300x237.png 300w, https://pybonacci.org/wp-content/uploads/2015/01/plate.png 749w" sizes="(max-width: 300px) 100vw, 300px" />](http://pybonacci.org/wp-content/uploads/2015/01/plate.png)<figcaption class="wp-caption-text">Placa rectangular simplemente apoyada resuelta con FEniCS</figcaption></figure> 

<!--more-->

Sin duda alguna el mejor recurso para aprender en profundidad a manejar las diferentes bibliotecas que conforman el proyecto es ["The FEniCS book"](http://fenicsproject.org/book/), disponible gratuitamente en Internet y en papel en la web de Springer. Muchas partes de este artículo están inspiradas o directamente traducidas de él. Está siendo mi biblia durante estas semanas y lo recomiendo al 100 %.

**_En esta entrada se han usado python 2.7.9, numpy 1.9.1 y fenics 1.5.0._**

**Este artículo tiene licencia GNU Free Documentation License, versión 1.3.**

## Alcance y objetivos

El proyecto FEniCS busca automatizar la resolución de ecuaciones diferenciales, utilizando el método de los elementos finitos. Este método, que data de mediados del siglo XX y que hoy por hoy es tremendamente importante en la resolución de problemas ingenieriles, se puede automatizar en tres pasos:

  1. Automatización de la discretización.
  2. Automatización de la solución discreta.
  3. Automatización del control del error.

FEniCS se creó en 2003 y se ocupa fundamentalmente de la **automatización de la discretización**. Una vez que se ha discretizado el problema y se han ensamblado los correspondientes sistemas lineales, su resolución (es decir, la segunda tarea) se deja a bibliotecas especializadas como PETSc, UMFPACK y otras.<figure id="attachment_3095" style="width: 297px" class="wp-caption aligncenter">

[<img src="http://pybonacci.org/wp-content/uploads/2015/01/fenics_project-297x300.png" alt="Componentes del proyecto FEniCS (un poco desactualizado)" width="297" height="300" class="size-medium wp-image-3095" srcset="https://pybonacci.org/wp-content/uploads/2015/01/fenics_project-297x300.png 297w, https://pybonacci.org/wp-content/uploads/2015/01/fenics_project.png 739w" sizes="(max-width: 297px) 100vw, 297px" />](http://pybonacci.org/wp-content/uploads/2015/01/fenics_project.png)<figcaption class="wp-caption-text">Componentes del proyecto FEniCS (un poco desactualizado)</figcaption></figure> 

FEniCS proporciona una interfaz en Python para todos estos paquetes, la mayoría escritos en Fortran o C++, y eso le da una sencillez de uso inigualable. Pero primero tenemos que ver cómo lo instalamos.

## Instalación

Debido al gran número de dependencias de FEniCS, instalarlo puede resultar un desafío para los menos pacientes. Los desarrolladores proporcionan [paquetes para Ubuntu](http://fenicsproject.org/download/ubuntu_details.html) (olvídate de Windows), y hay diversas [soluciones para instalarlo en otras distribuciones](https://bitbucket.org/fenics-project/fenics-developer-tools).

Estas vacaciones invernales he puesto mi granito de arena y **he creado unos paquetes y [recetas conda](https://github.com/juanlu001/fenics-recipes) para que se pueda instalar FEniCS junto a la distribución Anaconda**. Si tienes suerte, es posible que puedas instalarlo en tres comandos:

<pre><code class="language-bash">
$ conda create -n fenics27 python=2.7  # Creamos un entorno apropiado
$ source activate fenics27  # Lo activamos
(fenics27) $ conda install fenics mkl --channel juanlu001  # Instalamos FEniCS y MKL
(fenics27) $ python ~/.miniconda3/envs/fenics27/share/dolfin/demo/documented/poisson/python/demo_poisson.py  # ¡Cruza los dedos!

</code></pre>

Los he compilado con la extensión MKL que proporciona Continuum, así que necesitarás una licencia académica gratuita.

Si por cualquier motivo la instalación falla ([¡abre una incidencia!](https://github.com/juanlu001/fenics-recipes/issues)) o quieres modificar el proceso de compilación, no tienes más que bajarte las recetas y modificarlas a tu gusto. En el repositorio hay instrucciones sobre cómo utilizarlas. No me voy a detener mucho sobre esto porque sería material para otro artículo... 😉

En última instancia no te cuesta nada bajarte Linux Mint o Ubuntu, configurarlo en una máquina virtual como VirtualBox y empezar a trabajar. **¡Vamos allá!** 😀

## La ecuación de Poisson

Antes de lanzarnos al código, como gente seria y ordenada que somos vamos a empezar con las matemáticas. Vamos a seguir los primeros apartados del [tutorial de FEniCS](http://fenicsproject.org/documentation/tutorial/), y vamos a resolver la ecuación de Poisson:

$\displaystyle -\nabla^2 u = f \quad u \in \Omega.$

De las condiciones de contorno hablaremos en seguida. Lo primero y más importante es definir el dominio, y en este caso resolveremos la ecuación en un **cuadrado unitario** $\Omega = [0, 1] \times [0, 1] \subset \mathbb{R}^2$.

Vamos a ir escribiendo el programa paso a paso: después de importar todo FEniCS (sí, está hecho así en todas las demos, ¡no hay que alarmarse!), creamos el dominio correspondiente utilizando [`UnitSquareMesh`](http://fenicsproject.org/documentation/dolfin/1.5.0/python/programmers-reference/cpp/mesh/UnitSquareMesh.html):

<pre><code class="language-python">
# coding: utf-8
"""Ecuación de Poisson.

"""
from dolfin import *

# Tenemos que especificar el número de elementos
mesh = UnitSquareMesh(10, 10)

</code></pre>

### Espacios de funciones

Tenemos que establecer a qué espacios van a pertenecer nuestras funciones. Este es un paso muy delicado porque si no lo hacemos bien nuestros resultados serán absurdos, o lo que es peor, ligeramente incorrectos.

El tema tiene bastante enjundia, así que solo mencionaré que los espacios que se utilizan en el método de los elementos finitos se llaman **espacios de Sobolev**</a> y que para este caso nos interesan funciones incluidas en $H^1(\Omega)$. Ejemplos de elementos finitos tipo $H^1(\Omega)$ son los clásicos elementos polinómicos de Lagrange.

Veamos cómo se traduce esto a código Python:

<pre><code class="language-python">
V = FunctionSpace(mesh, 'Lagrange', 1) # Polinomios de orden 1

u = TrialFunction(V)
v = TestFunction(V)

</code></pre>

Hemos definido un espacio de funciones $V = H^1(\Omega)$ sobre el dominio con [`FunctionSpace`](http://fenicsproject.org/documentation/dolfin/1.5.0/python/programmers-reference/functions/functionspace/FunctionSpace.html#dolfin.functions.functionspace.FunctionSpace), y hemos creado ya nuestra función incógnita y nuestra función. ¡Seguimos!

### Formulación variacional y condiciones de contorno

Lo siguiente que tenemos que hacer es escribir la ecuación en **forma variacional**, débil o integral. Para ello:

  * Multiplicaremos por una _función test_ $v$,
  * integraremos sobre todo el dominio $\Omega$,
  * aplicaremos integración por partes para relajar las condiciones de derivabilidad sobre la función incógnita $u$, y
  * impondremos las condiciones de contorno.

En nuestro caso nos quedaría:

$\displaystyle -\int\_\Omega (\nabla^2 u) v dx = \int\_\Omega f v dx$

Y aplicando integración por partes (que en dimensiones superiores a uno se conoce como [primera identidad de Green](http://es.wikipedia.org/wiki/Identidades_de_Green#Primera_Identidad_de_Green)),

$\displaystyle -\int\_\Omega (\nabla^2 u) v dx = \int\_\Omega \nabla u \cdot \nabla v dx - \oint_{\partial\Omega} \frac{\partial u}{\partial n} v ds$

Y ahora viene la parte importante en la que imponemos las condiciones de contorno, en la integral sobre $\partial\Omega$. Hay dos opciones:

  1. Condiciones tipo Dirichlet: $u = u_0$. En este caso hacemos desaparecer la última integrar imponiendo que $v = 0$ en $\partial\Omega$. En este caso las condiciones se denominan **esenciales**.
  2. Condiciones tipo Neumann: $\frac{\partial u}{\partial n} = g$. En este caso la condición de contorno se traslada de manera _natural_ a la formulación variacional (¡solo hay que sustituir!), y por esto se llaman condiciones **naturales**.

Esta distinción es importante porque se reflejará de manera clara en el código. Si quieres una explicación más profunda cualquier libro de elementos finitos o de cálculo variacional lo explicará mejor que yo.

Para este caso vamos a imponer condiciones de contorno Dirichlet (esenciales): $u = 1 + x^2 + 2 y^2$ en $\partial\Omega$ utilizando [`DirichletBC`](http://fenicsproject.org/documentation/dolfin/1.5.0/python/programmers-reference/cpp/fem/DirichletBC.html). Necesitamos trasladar esta expresión al programa (mediante la clase [`Expression`](http://fenicsproject.org/documentation/dolfin/1.5.0/python/programmers-reference/functions/expression/Expression.html) y una función que defina en qué parte del contorno se aplican. El código será el siguiente:

<pre><code class="language-python">
def boundary(x, on_boundary):
    """El parámetro on_boundary es verdadero si el punto está
    sobre el contorno. Podríamos hacer otro tipo de comprobaciones,
    pero en este caso basta con devolver este mismo valor.

    """
    return on_boundary

u0 = Expression('1 + x[0] * x[0] + 2 * x[1] * x[1]')
bc = DirichletBC(V, u0, boundary)

</code></pre>

En FEniCS la forma variacional se expresa con un lenguaje simbólico de la siguiente manera:

$\displaystyle a(u, v) = L(v)$

Nuestro término fuente será $f(x, y) = -6$. Al haber aplicado condiciones de contorno esenciales, la última integral será nula. El código es:

<pre><code class="language-python">
f = Constant(-6.0)  # Término fuente
a = inner(nabla_grad(u), nabla_grad(v)) * dx  # Miembro izquierdo
L = f * v * dx  # Miembro derecho

</code></pre>

Ya estamos a punto de sacar una bonita gráfica 😉

### Resolución del sistema

La forma más directa de resolver el sistema es utilizando la función [`solve`](fenicsproject.org/documentation/dolfin/1.5.0/python/programmers-reference/fem/solving/solve.html). Vamos a reutilizar la variable `u` para la solución, de esta forma:

<pre><code class="language-python">
u = Function(V)
solve(a == L, u, bc)

print max(abs(u.vector().array()))  # Array de valores numéricos
</code></pre>

Y para terminar, la gráfica correspondiente:

<pre><code class="language-python">
plot(u)
interactive()

</code></pre>

¡Y este es el resultado!

[<img src="http://pybonacci.org/wp-content/uploads/2015/01/poisson-300x233.png" alt="Ecuación de Poisson" width="300" height="233" class="aligncenter size-medium wp-image-3105" srcset="https://pybonacci.org/wp-content/uploads/2015/01/poisson-300x233.png 300w, https://pybonacci.org/wp-content/uploads/2015/01/poisson.png 741w" sizes="(max-width: 300px) 100vw, 300px" />](http://pybonacci.org/wp-content/uploads/2015/01/poisson.png)

## Conclusiones

Alguno se ha podido marear con tanta ecuación, y es normal. En realidad, esto es solo la punta del iceberg: el tutorial básico de FEniCS continúa particionando la frontera para poner diferentes condiciones de contorno en cada parte, utilizando formulaciones mixtas, calculando el error cometido con respecto a la formulación exacta... Y aún queda una treintena de capítulos en el libro.

Durante los últimos días he estado publicando gists de problemas resueltos con FEniCS. Por ejemplo, la ecuación de Helmholtz:

<blockquote class="twitter-tweet" data-width="550">
  <p lang="es" dir="ltr">
    Me lo estoy pasando en grande resolviendo la ecuación de Helmholtz en FEniCS 😀<a href="https://t.co/EeWz7uZoCo">https://t.co/EeWz7uZoCo</a> <a href="http://t.co/0djpJoGHyW">pic.twitter.com/0djpJoGHyW</a>
  </p>
  
  <p>
    &mdash; Pybonacci (@Pybonacci) <a href="https://twitter.com/Pybonacci/status/553932429720055808">January 10, 2015</a>
  </p>
</blockquote>



Lo fundamental es tener pericia matemática y sobre todo muchas ganas de sacarle jugo a FEniCS. Espero que os haya gustado el artículo, no dudéis en ponerme vuestras dudas y sugerencias en los comentarios y, si tiene éxito, habrá segunda parte 😉 ¡Un saludo!

## Referencias

  * WELLS, Garth; MARDAL, Kent-Andre; LOGG, Anders. _Automated Solution of Differential Equations by the Finite Element Method: The FEniCS Book_. Springer, 2012.

## Agradecimientos

Desde aquí quiero agradecer a Pepe Cercós el haberme animado a empezar mi proyecto fin de carrera y a Fernando Varas por haberme devuelto la fe en los profesores de mi escuela con sus aclaraciones y dedicación. _A hombros de gigantes_ 🙂