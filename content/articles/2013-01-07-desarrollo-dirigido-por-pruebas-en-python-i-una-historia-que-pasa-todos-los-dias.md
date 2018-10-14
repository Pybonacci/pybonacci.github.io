---
title: Desarrollo dirigido por pruebas en Python (I): Una historia que pasa todos los días
date: 2013-01-07T21:00:51+00:00
author: javierjus
slug: desarrollo-dirigido-por-pruebas-en-python-i-una-historia-que-pasa-todos-los-dias
tags: BDD, python, TDD, test, testing

Vamos a iniciar una serie de artículos sobre [desarrollo dirigido por pruebas](http://es.wikipedia.org/wiki/Desarrollo_guiado_por_pruebas) en Python ([TDD](http://en.wikipedia.org/wiki/Test-driven_development) en inglés) con el objetivo de acercarlo a científicos e ingenieros. En el primero presentaremos la idea principal del desarrollo dirigido por pruebas, y para ello empezamos una pequeña historia:

Una empresa de desarrollo de productor de jardinería a medida, GardenTech, tiene un nuevo cliente, el señor Sellers. La reunión de requisitos podría ser algo así:

> _Ingeniero GardenTech:_ Buenos días señor Seller, díganos qué es lo que necesita.
> 
> _Sellers_: Necesito una manera de poder regar mis plantas.
> 
> _GT:_ Podemos ayudarle, tenemos mucha experiencia en ese campo. ¿En qué ha pensado?
> 
> _S:_ Tengo 5 macetas, así que me gustaría llevar el agua para allá y echársela.
> 
> _GT:_ Perfecto, le pondremos a su aparato un agujero grande para que pueda llenarlo de agua y muchos pequeñitos para que no tronche las flores.
> 
> _S:_ Pero ¿y si se me cae?
> 
> _GT:_ Tranquilo, la usabilidad es nuestra especialidad, le añadiremos un asa para que pueda manejarlo y no será muy grande para que no pese.
> 
> _S:_ ¿no será grande? Entonces igual lo pierdo.
> 
> _GT:_ Todo está pensado, le daremos un color rojo brillante para que pueda encontrarlo a simple vista.
> 
> _S:_ ¿Y si me mojo?
> 
> _GT:_ Los agujeros pequeños estarán alejados del dispositivo mediante un tubo.
> 
> _S:_ Perfecto, veo que piensan en todo.
> 
> _GT:_ Somos buenos.

El señor Sellers y GardenTech están de acuerdo  en los requisitos que debe tener el artefacto, y GardenTech comienza a desarrollarlo. Un mes después la empresa llama al seños Sellers. En medio de la sala de reuniones hay una mesa con un bulto cubierto por una sábana.

<!--more-->

> _GT:_ Señor Sellers, prepárese porque ya tenemos su aparato. En su diseño han trabajo los mejores técnicos que han aportado las soluciones más modernas e innovadoras. Cumple todos sus requisitos.

El ingeniero tira de la manta y… sorpresa.

![regadera](https://pybonacci.org/images/2012/12/regadera.jpg?w=257)

> _GT_: Mire, está todo. Tiene un asa, un agujero grande para llenarlo, muchos pequeños para esparcir el agua alejados por un tubo, tiene el tamaño justo para que no puse mucho y un llamativo color rojo. ¿A que es perfecta?

Amigo lector, si te identificas con el señor Sellers y piensas que te has visto muchas veces en esa situación… te equivocas. Pongo mi mano en el fuego en que, si alguna vez has escrito código Python, has actuado como el ingeniero de GardenTech. Todos los hacemos, incluido yo.

¿Dónde está el fallo? ¿Por qué el cliente no ha objetico el programa, o la regadera, que quería? Los requisitos eran perfectos, todo lo que se pidió se ha cumplido. El problema es que tanto el ingeniero como el señor Sellers se han centrado en qué características querían que tuviera el producto pensando que eso era lo que necesitaban, pero se olvidaron de cómo querían utilizarlo para darse cuenta de qué era lo más práctico.

¿Y si el ingeniero le hubiera dado un vaso al señor Sellers y le hubiera pedido que le mostrara cómo deseaba regar las plantas? En esta serie de artículos sobre Test-Driven Development (TDD) vamos a aprender a hacer esto. TDD será nuestro vaso para evitar crear código que sea un infierno de utilizar, entender y modificar.

TDD utiliza las pruebas para poner ejemplos de cómo queremos utilizar el código que vamos a escribir. Así, cambiamos nuestro foco desde el qué (como el ingeniero de la historia) al cómo. El objetivo no es buscar el mejor código, sino aquel código que sea más sencillo de utilizar y adaptado a nuestras necesidades. Veamos un sencillo ejemplo antes de entrar en detalles en próximos artículos.

Vamos a crear una clase que implemente las operaciones de una lista. Con este ejemplo tan obvio vamos a centrarnos en cómo aplicar TDD en lugar de en el código que vamos a escribir. No pensamos en qué métodos tiene que tener la lista ni en los detalles de su implementación sino en ejemplos de cómo queremos utilizarla, como estos:

  1. Si creo una lista, entonces el número de elementos es cero.
  2. Si creo una lista y añado un elemento, el número de elementos es uno.
  3. Si creo una lista y añado los elementos A, B y C, entonces el elemento de índice 0 es A, el elemento de índice 1 es B y el elemento de índice 2 es C.

Podemos codificar estos ejemplos como pruebas en Python para tomar decisiones sobre cómo vamos a utilizar la clase lista y para ir verificando que todo funciona correctamente a medida que la programamos. Para ello utilizamos el módulo `unittest` que ya viene incluido en la distribución base de Python. Una posible implementación de los ejemplos anteriores se muestra a continuación.

    :::python
    class TestsCasesForMyList(unittest.TestCase):
        def test_GivenANewListThenItHasZeroElements(self):
            l = MyList()
            self.assertEqual(0, l.size())
        def test_GivenANewListWhenIAddAnElementThenItHasOneElement(self):
            l = MyList()
            l.add("A")
            self.assertEqual(1, l.size())
        def test_GivenANewListWhenIAdd_A_B_C_Then_A_HasInex_0_B_index_1_and_C_index_2(self):
            l = MyList("A", "B", "C")
            self.assertEqual("A", l.get(0))
            self.assertEqual("B", l.get(1))
            self.assertEqual("C", l.get(2))

Fijémonos en las decisiones de diseño y requisitos que hemos establecido puede que sin darnos cuenta. Por ejemplo, si nos fijamos en la tercera prueba vemos que, aunque nadie lo había mencionado, nos resulta muy cómodo indicar un grupo de elementos al momento de crear la lista, en vez de añadirlo uno a uno. Si no hubiéramos puesto este ejemplo puede que esto nos e nos hubiera ocurrido.

En el próximo artículo comenzaremos viendo algunos ejemplos de cómo aplicar TDD a la hora de programar en Python. En el tercer y último veremos un ejemplo más detallado. Aunque explicaremos TDD desde el punto de vista de ejemplos de uso en vez de pruebas, será necesario conocer los fundamentos de las pruebas automáticas de software. Repasaremos estos fundamentos al principio del próximo artículo. Mientras un buen enlace es: <http://software-carpentry.org/4_0/test/>

Nos vemos en el próximo artículo y acordaos de la historia del ingeniero y el señor Sellers la próxima vez que vayáis a escribir código y penséis en qué hacer (en vez cómo usarlo).

<div style="background-color:#eee;padding:.5em 1em .15em;margin-bottom:1em;">
  Este artículo es fruto de la colaboración entre Javier Gutiérrez y Juan Luis Cano, que aportó sugerencias y correcciones al original.
</div>
