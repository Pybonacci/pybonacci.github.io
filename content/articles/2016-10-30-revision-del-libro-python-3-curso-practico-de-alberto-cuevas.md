---
title: Revisión del libro &#8220;Python 3, Curso Práctico&#8221; de Alberto Cuevas
date: 2016-10-30T00:48:19+00:00
author: Kiko Correoso
slug: revision-del-libro-python-3-curso-practico-de-alberto-cuevas
tags: alberto cuevas, libro, python 3, ra-ma

Nos han pedido una revisión de un nuevo libro sobre Python en español. El libro se titula 'Python 3, Curso Práctico' y lo ha escrito Alberto Cuevas Álvarez. Si seguís leyendo podréis ver cómo ganar una copia en papel del mismo ;-D

Primero de todo, algunas características del libro:

  * Título: Python 3, Curso Práctico.
  * Autor: Alberto Cuevas Álvarez
  * Año de edición: 2016
  * Nº páginas: 560
  * ISBN: 978-84-9964-658-9
  * Editorial: RA-MA EDITORIAL
  * Encuadernación: Rústica
  * Idioma: Español (de España).
  * Versión de Python usada en el libro: 3.3
  * Link: <http://www.ra-ma.es/libros/PYTHON-3-CURSO-PRACTICO/94627/978-84-9964-658-9>
  * Precio: 31.90 € para la versión en papel.
  * Versión electrónica: No disponible de momento.

<img class="aligncenter" src="http://www.tecno-libro.es/imagenes/9788499/978849964658.GIF" alt="" width="93" height="140" />

Le hemos pedido al autor que nos defina su intención al escribir el libro y esta es la frase resumen que nos ha enviado:

> "Mi intención a la hora de realizar el libro ha sido explicar los fundamentos básicos de Python y las herramientas necesarias dentro de su ecosistema para conseguir crear aplicaciones gráficas completas en 2D ."

Como venimos haciendo, vamos a ir viendo el libro capítulo a capítulo para poder comentar de forma pormenorizada las pequeñas piezas que componen el mismo:

## **INTRODUCCIÓN**

El libro empieza fuerte explicando, aunque sea muy por encima, cosas básicas de programación que pueden venir bien para fijar ciertos conceptos si no se dispone de cierto bagaje en ciencias de la computación.

## **EMPEZANDO A PROGRAMAR**

En este punto se introducen conceptos importantes como lo que son las variables, cómo se asignan, ciertas funciones integradas (builtin) en el intérprete, operadores,etc. Cosas básicas introducidas en el momento oportuno. Está bien lo detallado de algún punto con múltiples ejemplos útiles. Se comenta la instalación de PyScripter, un IDE solo windows 🙁

## **ELEMENTOS FUNDAMENTALES DE PROGRAMACIÓN: INSTRUCCIÓN CONDICIONAL Y BUCLES**

El capítulo habla de forma extensa del control de flujo, bucles y condiciones. Muy detallada la explicación de las condiciones. En este mismo capítulo se introducen algunas cosas que no tienen mucha relación como el mecanismo del `import` (explicado muy brevemente), el uso de números aleatorios (que no tiene mucha relación con el resto de contenidos del capítulo), depuración con PyScripter (menos útil para personas fuera de Windows),...

## **PROGRAMACIÓN FUNCIONAL**

El título del capítulo es algo desafortunado ya que no estamos hablando sobre programación funcional sino sobre el uso de funciones en Python y esto podría confundir a alguien. El capítulo es muy completo para aprender a usar funciones en Python, el '_scope_' de las variables, los parámetros y argumentos,... Nuevamente, algún ejemplo podría resultar confuso pero, en general, está bastante completo. Echo en falta que se nombre a las funciones _lambda_.

## **PROGRAMACIÓN ORIENTADA A OBJETOS**

Llegamos a la parte de clases y la programación orientada a objetos (POO). El capítulo es bastante extenso y se explican muchas cosas, algunas de ellas avanzadas. Sin duda, este es el capítulo del libro que me gusta menos. Los ejemplos que se usan no son muy ortodoxos, nuevamente se recurre a casos muy particulares que provocan, siempre en mi modesta opinión, que algunas cosas resulten en más complejas de lo que deberían en este punto. Una buena parte del capítulo se habla sobre como se hacen algunas cosas con PyScripter lo que le resta valor a usuarios fuera de Windows.

## **TIPOS DE DATOS EN PYTHON**

Este capítulo es muy detallado. Se explica con mucha profundidad los tipos básicos en Python, cadenas, listas, tuplas, conjuntos y diccionarios. Podría, incluso, servir como guía de referencia en español del uso de estos tipos  por lo detallado (son unas 90 páginas). Además, se usan muchísimos ejemplos para explicar los conceptos.

## **FICHEROS Y EXCEPCIONES**

Se habla sobre cómo poder usar ficheros para leer y escribir información. Esta parte es muy detallada y extensa con múltiples ejemplos útiles. La parte de excepciones es más que correcta con un alcance adecuado para introducirlos. Por último, se muestra el uso de `with` pero se despacha en menos de una página por lo que me parece insuficiente. Este capítulo y el anterior son los que más me gustan del libro.

## **PROGRAMACIÓN GRÁFICA EN PYTHON MEDIANTE PYQT**

No es normal encontrar una introducción a interfaces gráficas en un libro introductorio. Como mucho, se muestra un ejemplo básico para dejar al lector que se introduzca por su cuenta en el tópico si tiene interés. En este caso se hace una introducción mucho más extensa que el ejemplo típico por lo que si tienes interés en crear interfaces gráficas estás de suerte. Sin embargo, si no tienes mucho interés en ello, se van muchas páginas en ello. Se explican de forma detallada muchos de los widgets disponibles en PyQt y está muy enfocado a crear las interfaces usando Qt Designer.

## **GENERACIÓN DE GRÁFICOS EN PYTHON MEDIANTE MATPLOTLIB**

Nuevamente, se introduce otra librería que quizá no sea de interés para todo el mundo. En alrededor de 50 páginas se habla sobre cómo instalar la librería, cómo usar pyplot con muchos ejemplos, como usar matplotlib usando POO y cómo integrar matplotlib en una aplicación PyQt. Reitero, si tienes interés en hacer gráficas tienes suerte pero si no es así se te van otras 50 páginas de libro en ello.

# Apuntes varios sobre el libro:

Me gusta:

  * Lo detallado de la explicación del `if` en el capítulo 3.
  * Que no haya referencias a Python 2.
  * Lo detallado de la explicación de las funciones.
  * Lo detallado de la explicación de los tipos básicos de Python pudiendo servir, incluso, como guía de referencia en español.
  * La parte del tratamiendo de ficheros y excepciones se hace con un alto nivel de detalle.
  * La extensión del libro, que permite poder desarrollar algunos temas de forma muy completa.
  * Que sea en español.

No me gusta:

  * El uso de `eval` en muchos ejemplos del libro lo considero una mala práctica.
  * No se respeta el PEP8, enseñando malas prácticas, lo cual no me parece adecuado en un curso introductorio.
  * Algunos ejemplos usan casos extremos para explicar ciertos conceptos. Estos casos extremos pueden ser detalles de la implementación y no los considero adecuados ya que en lugar de ayudar pueden resultar más confusos.
  * Está muy enfocado a Windows (uso de PyScripter, instalaciones) haciendo que una buena parte de las páginas sea menos útil para gente que use otros sistemas operativos.

# Conclusión

El libro tiene algunos altibajos con partes que brillan con luz propia y partes que mejoraría.

Si de mi dependiera me gustaría que algunas cosas se explicasen un poco mejor, como el uso de `with`, las funciones _lambda_, el mecanismo del `import`, la parte de POO. Metería partes con muchas librerías útiles de la librería estándar (`math`, `itertools`, `datetime`, `os`, `sys`, `collections`,...), como crear paquetes y módulos,... Reduciría o eliminaría los dos últimos capítulos.

Como comentario general, considero que el libro está bien pero, como todo en esta vida, se podría mejorar en algunos aspectos.

# Sorteamos una copia entre nuestros lectores

El autor nos envió varias copias del libro. Una de ellas la vamos a sortear entre todos los lectores de Pybonacci residentes en España. Para participar:

  * Solo tienes que escribir un tweet indicando porqué te gustaría tener este libro incluyendo un enlace a <http://www.ra-ma.es/libros/PYTHON-3-CURSO-PRACTICO/94627/978-84-9964-658-9>
  * Una vez enviado el tweet nos lo enlazas en los comentarios de más abajo para que no se nos escape el tweet.
  * Si no tienes cuenta en twitter, déjanos un comentario más abajo indicando porqué te gustaría tener este libro.

Tenéis hasta el miércoles, 2 de noviembre a las 21:00:00 ([CET](https://es.wikipedia.org/wiki/Hora_central_europea)) para participar en el sorteo. Después de pasada la fecha indicaremos cómo se hará el sorteo (actualizando [algunas cosas de aquí](http://jsfiddle.net/1xtevgg0/1/)), usando el número ganador del sorteo de la ONCE de ese día (2016/11/02) y anunciaremos el ganador.

# Actualización: Resultado del sorteo

El número de la [ONCE fue el 69907](https://www.juegosonce.es/resultados-cupon-diario). Si introducís el código aquí:



sale que el ganador ha sido [@FlixUjo](https://twitter.com/flixujo). He usado los participantes por orden de fecha en su comentario, del más antiguo al más nuevo:

`participantes = ['FlixUjo', 'Javier @runjaj', 'Antonio Molina',<br />
'Raúl', 'José Carlos Juanos', 'Christian',<br />
'Kike', 'Eduardo Campillos']`

Enhorabuena al vencedor, por favor, mándanos un DM por twitter o [usa el formulario de contacto](http://pybonacci.org/contacto/) para mandarnos una dirección de correo/teléfono o lo que prefieras.

Saludos a todos.