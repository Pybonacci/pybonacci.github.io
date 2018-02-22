---
title: Haz una librería de la que me pueda fiar… o no la hagas
date: 2014-03-18T09:14:47+00:00
author: javierjus
slug: haz-una-libreria-de-la-que-me-pueda-fiar-o-no-la-hagas
tags: librería, python

Cuando creas código, debes poder confiar en algunas cosas, como el sistema operativo o el intérprete de Python. Si no, sería casi imposible encontrar un error. Por suerte casi todo lo que usamos es lo suficientemente maduro para tener la certeza de que si algo no funciona la causa está en nuestro código.

¿Qué pasa con las librerías de terceros? También tenemos que confiar en ellas y para ello hay que comprobar los parámetros de entrada. Esta entrada te propone que hagamos juntos una reflexión sobre este tema.

## Verificando parámetros

Una librería es un fragmento de código muy delicado. No está pensada para ser utilizada por un usuario final a través de una interfaz que limite y controle lo que el usuario pueda hacer. Una librería está pensada para ser parte de otro código y para permitir que sean programadores o [software craftmen](http://manifesto.softwarecraftsmanship.org/ "manifesto softwarecraftsmanship") quienes la utilicen a veces de manera muy ingeniosa.

Para que una librería tenga éxito y los desarrolladores la utilicen es fundamental que sea de fiar. Una librería podrá hacer su trabajo mejor o peor, incluso puede no ser capaz de trabajar en determinadas circunstancias, pero si obtenemos un error de nuestro código siempre debe estar claro si el error es interno de la propia librería y hemos encontrado un bug o nos topamos con una limitación documentada, si el error es de nuestro código que usa mal la librería o si el error es de nuestro código y no tiene nada que ver con la librería.

Para conseguir esto es fundamental tratar los parámetros que reciben los métodos o funciones de la librería adecuadamente. Tomemos como ejemplo una sencilla librerías de funciones matemáticas básicas: potencia, exponencial, divisores, mínimo común divisor, máximo común múltiplo, etc.

Algunas de estas funciones no aceptan números negativos,  ¿tenemos que comprobar todos los métodos? _**Sí**_.

Si un parámetro negativo producirá una excepción más adelante, ¿para qué esperar?. Una buena alternativa es comprobar el parámetro justo al comienzo de la llama al método o función y lanzar una excepción. Por ejemplo, imagina esta implementación básica de la función de Fibonacci.

<pre><code class="language-python">def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)</code></pre>

¿Cuál es la diferencia entre verificar el valor del parámetro o dejar que el código falle dónde tenga que fallar? Compruébalo tú mismo viendo cuál de los dos siguientes errores es más claro.

_Sin comprobar valores de entrada._

[<img class="size-medium wp-image-2266" alt="Error en función de Fibonacci sin comprobar parámetros" src="http://new.pybonacci.org/images/2014/03/res01.jpg?w=300" width="300" height="295" srcset="https://pybonacci.org/wp-content/uploads/2014/03/res01.jpg 621w, https://pybonacci.org/wp-content/uploads/2014/03/res01-300x295.jpg 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://new.pybonacci.org/images/2014/03/res01.jpg)

_Comprobando valores de entrada._

[<img class="alignnone size-medium wp-image-2267" alt="res02" src="http://new.pybonacci.org/images/2014/03/res02.jpg?w=300" width="300" height="83" srcset="https://pybonacci.org/wp-content/uploads/2014/03/res02.jpg 621w, https://pybonacci.org/wp-content/uploads/2014/03/res02-300x83.jpg 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://new.pybonacci.org/images/2014/03/res02.jpg)

Si comprobamos todos los parámetros de entrada, estaremos escribiendo una librería sólida que ayuda a sus usuarios a escribir buen código. Pero también podemos estar repitiendo muchas veces el código de comprobación y repetir código siempre es malo.

Por suerte tenemos varias alternativas. Además, resolver este problema nos da una indicación de nuestro nivel de programación. Algunas opciones son:

  * Creamos un método interno auxiliar que compruebe los parámetros. Todos nuestros métodos llamarían a dicho método (así está implementada las clases de java.collection, por ejemplo).
  * Creamos un decorador que compruebe los parámetros (los decoradores no son tan difíciles como parece).
  * Utilizamos alguna librería de comparaciones, como [sure](https://github.com/gabrielfalcao/sure "sure") o [expects](https://expects.readthedocs.org/en/0.2.0/ "Expects").

Si se te ocurren más soluciones ponlas como comentario de este artículo. No te preocupes si crees que no son mejores que las que ya hemos visto, porque siempre nos servirá para aprender un poco más.

## Unidades con magnitudes

Otro tema interesante es cómo trabajar con magnitudes que tienen una unidad asociada. Por ejemplo, pensemos en la temperatura. Si nos dan estas temperaturas: 10, 283 y 50, ya podemos cruzar los dedos para que el termómetro se haya estropeado.

Pero si nos dicen que la temperatura es 10 grados centígrados, 283 grados kelvin y 50 grados Fahrenheit descubrimos que, en verdad, estamos hablando de la misma temperatura y que mejor vamos abrigados o pasaremos frio.

A Python y a nuestras librerías le pasa lo mismo, a veces necesita las unidades porque un un número no les dice nada. Pero Python no tiene ningún tipo de dato nativo para empresar magnitudes y unidades. Lo mejor es crearlo nosotros mismos con una clase. ¿Cómo podría ser una clase temperara (llamada _temp_ para abreviar)?

  * Podríamos crear métodos estáticos, por ejemplo  tem.kelvin(50) o temp.celcius(-4) que comprobaran que una temperatura es válida en el rango de sus unidades.
  * Podríamos crear métodos de conversión para obtener la temperatura en la magnitud que deseemos, por ejemplo si creamos temp.kelvin(283) y vemos el valor de temp. celcius () obtenemos un correcto 10.
  * Podríamos sobrecargar los operadores para comparar y operar con temperaturas más intuitivamente.
  * Y podríamos buscar si alguien ya lo ha hecho por nosotros.

Nos evitaríamos, por ejemplo el problema de mezclar distintas magnitudes, ya que la clase  verificaría por nosotros que las operaciones se realicen siempre con la misma unidad.

### Bola extra

Existe una técnica de diseño 7 programación conocida como diseño por contratos (_design by contract_) en las que, para cada operación se especifican sus precondiciones, post-condiciones e invariantes y luego se implementan en el código.

Esta técnica alcanzó popularidad a finales de los 90 por el [desastre el cohete Ariane 5](http://www.around.com/ariane.html "Ariane 5 crashes"), el cual se podría haber evitado especificando los contratos de las operaciones.<figure id="attachment_2268" style="width: 300px" class="wp-caption alignnone">

[<img class="size-medium wp-image-2268" alt="Ariadne 5, o lo que queda." src="http://new.pybonacci.org/images/2014/03/ariane_5_self-destruction.jpg?w=300" width="300" height="197" srcset="https://pybonacci.org/wp-content/uploads/2014/03/ariane_5_self-destruction.jpg 400w, https://pybonacci.org/wp-content/uploads/2014/03/ariane_5_self-destruction-300x197.jpg 300w" sizes="(max-width: 300px) 100vw, 300px" />](http://new.pybonacci.org/images/2014/03/ariane_5_self-destruction.jpg)<figcaption class="wp-caption-text">Ariane 5, o lo que queda.</figcaption></figure> 

Si os manejáis por el mundo Java, podéis ver esta técnica en aplicación por ejemplo en java.collection, aunque luego no implementéis todas las precondiciones, poscondiciones e invariante sí es una buena idea pensar en los contratos de vuestras librerías. Además, también sirve de ayuda para diseñar casos de prueba.