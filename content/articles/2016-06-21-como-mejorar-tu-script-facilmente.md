---
title: Como mejorar tu script fácilmente
date: 2016-06-21T11:15:39+00:00
author: Manuel Garrido
slug: como-mejorar-tu-script-facilmente
tags: principiante, python

[Esta entrada apareció originalmente en inglés en mi blog.](http://blog.manugarri.com/how-to-make-your-script-2x-better/ "Esta entrada apareció originalmente en inglés en mi blog.")

Nos ha pasado a todos. Ese momento en el que descubres que sabes suficiente sobre un lenguage de programacion que quieres ponerlo en práctica y construir "algo", lo que sea.
  
Una de las mejores cosas de la comunidad de Python es no sólo su habilidad para construir cosas increíbles, sino también para compartirlas con todo el mundo, mejorando la comunidad en el proceso.

Sin embargo, llevo un tiempo fijándome en un patrón que se repite en algunos de estos proyectos. Seguro que has visto alguno así. Hablo de esos proyectos con 2 ó 3 componentes, donde el README tiene una pequeña descripción del proyecto, quizás un par de lineas explicando como ejecutar el proyecto, y frases del tipo, _"Seguramente añadiré X o Y si tengo tiempo"_.

El caso es que muchos de estos proyectos son realmente interesantes, y tienen algún tipo de componentes que me gustaría usar sin tener que implementarlos yo mismo.

Te voy a mostrar 3 formas distintas de implementar uno de estos proyectos, cada una de ellas mejor (desde mi punto de vista) que la anterior:

Supongamos que queremos construir un script genial, donde la funcionalidad principal será que, dado un número entero por el usuario, realizará un calculo simple en base a ese entero, y devolverá el resultado.

# Implementación 1

<pre class=" language-python"><code class=" language-python">
#!/usr/bin/env python

"""
Super awesome script
Asks the user for a number:
 - If the number is less or equal to 100, it returns the 1st tetration of the number (power of itself)
 - else, it returns the number squared
"""

__version__ = '0.1'

if __name__ == '__main__':

    while 1:
        user_number = input('Choose a number:\n') #raw_input() in python2
        if user_number.isdigit():
            user_number = int(user_number)
            break
        else:
            print('{} is not a valid number'.format(user_number))

    if user_number &gt; 100:
        print(user_number**2)
    else:
        print(user_number**user_number)
</code></pre>

Ésta suele ser la implementación de alquien que lleva poco tiempo en python. Funciona, pregunta al usuario por el input, realiza la operación, e imprime en pantalla el resultado.

Veo dos problemas en esta implementación:

1. No hay ningún tipo de separación entre la lógica de la interacción del usuario y la lógica del cálculo. Todo esta incluido en el mismo macro bloque. Pese a ser funcional, esta implementación hace que sea díficil el modificar o expandir este script (para hacerlo tendrías que leerte todo el código).

2. Estamos gestionando toda la validación por nuestra cuenta. Python tiene formas de hacer esto para que tú no te tengas que molestar en hacerlo :).

Para la siguiente implementación, usaremos el módulo mas simple de la libreria standard para trabajar con inputs del usuario, .

# Implementación 2

<pre class=" language-python"><code class=" language-python">
#!/usr/bin/env python

"""
Super awesome script
Asks the user for a number:
 - If the number is less or equal to 100, it returns it to the power of itself
 - else, it returns the number squared
"""

import argparse

__version__ = '0.2'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--number', required=True, type=int,
                        help='number to perform calculation')
    values = parser.parse_args()
    user_number = values.number
    if user_number &gt; 100:
        print(user_number**2)
    else:
        print(user_number**user_number)
</code></pre>

En esta implementación hemos eliminado el problema #2 de la implementación anterior. En esta ocasión usamos `argparse`, de esta forma dejamos que la libreria estándar se encargue de la validación del input. Esta implementación no funciona a menos que el input sea válido.

Todavía tenemos el problema #1, la separación entre la lógica del input y la lógica primaria (la función de calculo).

En la siguiente implementación vemos como podemos arreglar esto.

# Implementación 3

<pre class=" language-python"><code class=" language-python">
#!/usr/bin/env python

"""
Super awesome script
Asks the user for a number:
 - If the number is less or equal to 100, it returns it to the power of itself
 - else, it returns the number squared
"""

import argparse

__version__ = '0.3'



def calculation(number):
    """Performs awesome calculation"""
    if number &gt; 100:
        return number**2
    else:
        return number**number

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--number', required=True, type=int,
                        help='number to perform calculation')
    values = parser.parse_args()
    user_number = values.number
    calculation_result = calculation(user_number)
    print(calculation_result)
</code></pre>

En esta implementación, hemos hecho dos cosas:

1. Hemos puesto la carga de la validación en un módulo bien mantenida como es `argparse`.
  
2. Hemos separado la lógica del input del usuario de la lógica del input de cálculo.

Éste último cambio tiene tres ventajas sobre #1 y #2.

- **Ventaja 1:** En primer lugar, si nos damos cuenta que por algún motivo queremos modificar el `100` por un `200`, ahora podemos fácilmente modificar eso, _sin tener que modificar ni leer todo el código_. Siempre y cuando la función `calculation` siga teniendo los mismos inputs y outputs, el resto de código seguirá funcionando sin problemas.

- **Ventaja 2:** Otro efecto, y para mi el más significativo, es que si ahora yo leo este script que otra persona ha escrito, y me gusta tanto que quiero añadirlo a un proyecto mio, **¡ahora puedo importarlo sin problemas!**.

En las implementacines #1 y #2, la única manera de usar el script era haciendo:

`python calculation_script.py --number INTEGER<br />
` 
  
Ahora, en la implementación #3, tenemos una manera **mucho mas útil** de usar la lógica mas importante (la del cálculo). Si yo tengo otro script en el que quiero usar la funcion de cálculo, puedo usarla de la forma:

<pre class=" language-python"><code class=" language-python">
from calculation_script import calculation

number = 10
calculation_result = calculation(number)
</code></pre>

**¿Increíble, no?** Simplemente haciendo una pequeña modificación a la estructura del proyecto, ahora cualquier persona se puede beneficiar del mismo.

- **Ventaja 3:** Supongamos que este simple proyecto empieza a crecer, más desarrolladores se interesan y empiezan a colaborar. El código empieza a crecer y alguien comenta que tendría sentido empezar a trabajar en el suite de testing. (si no sabes lo que es el testing, te recomiendo [este artículo](http://docs.python-guide.org/en/latest/writing/tests/ "este artículo").)

Con la implementación #3, testear la funcionalidad de `calculation` es super fácil (gracias a [/u/choffee](https://www.reddit.com/r/Python/comments/4hzam0/how_to_make_your_script_better/d2ydzn7 "/u/choffee") en reddit por el apunte):

<pre class=" language-python"><code class=" language-python">
import pytest
from calculation_script import calculation

class TestCalculation:
    """Calculation function does funky things to number
    More above 100 than below
    """
    def test_zero():
        x = 0
        assert calculation(x) == 0

    def test_border():
        x = 100
        assert calculation(x) == 10000

    def test_one():
        x = 1
        assert calculation(x) == 1
</code></pre>

Piensa en ello la próxima vez, no cuesta nada y hace que tu script sea mejor 🙂