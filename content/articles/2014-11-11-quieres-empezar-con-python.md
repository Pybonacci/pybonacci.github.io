---
title: ¿Quieres empezar con Python?
date: 2014-11-11T15:01:11+00:00
author: Kiko Correoso
slug: quieres-empezar-con-python
tags: cursos, formación, libros, principiante, recursos, tutoriales

Voy a intentar hacer una  pequeña guía para iniciarse en Python que, más allá de ser una compilación de enlaces a muchos sitios, pretende ser útil dentro de la abrumadora cantidad de información disponible ahí fuera.

¿No sabes lo que es un sistema de control de versiones, ni el desarrollo por pruebas, ni la programación orientada a objetos? No te preocupes ahora ni te vuelvas loco a ponerte a buscarlo por internet, muchas de las cosas y conceptos que pongo en esta mini guía se adquieren con el tiempo y la experiencia.

# Paso 0. Python 2 o Python 3.

Esta es una duda importante que tienen muchos recien llegados al lenguaje. En Python existen dos versiones oficiales en mantenimiento, la versión 2 se seguirá manteniendo durante unos cuantos años y se usa bastante debido a que hay mucho código que depende de esta versión, la versión 3 salió hace unos cuantos años y es la actual rama de desarrollo y la que va evolucionando por lo que es el presente y futuro de Python. Rompe la compatibilidad con la versión 2 en algunas cosas pero hay formas de hacer código que sea compatible tanto con Python 2 como con Python 3 sin excesivos problemas.

Si partes de cero en el lenguaje te recomiendo encarecidamente que empieces por Python 3 y no mires nunca más para atrás. Si dependes de código que no funciona en Python 3 te recomiendo que lo hagas funcionar en Python 3 porque Python 2, más pronto que tarde, el tiempo pasa volando, se dejará de mantener y estarás listo para ese momento. No es tan difícil y nos puedes preguntar para que te ayudemos.

# Paso 1. El tutorial oficial.

El [tutorial oficial lo tenéis disponible en español](http://docs.python.org.ar/tutorial/index.html) traducido por la gente de Python Argentina.

[Aquí te explicarán como instalar Python](https://docs.python.org/release/3.4.2/using/index.html#python-setup-and-usage) (si tienes dudas pregúntanos) y el tutorial será donde empezarás a ver la sintaxis de Python, como hacer bucles, condicionales, asignar valores, crear funciones,...

En este paso no pierdas el tiempo buscando herramientas y cosas así, de hecho, es contraproducente. Cualquier editor de texto simple es más que suficiente y recomendable para empezar: vim, emacs, el bloc de notas de tu windows, Geany, TextPad,... ¡¡No necesitas nama más!!

# Paso 2. Ponte a programar.

Una vez leído el tutorial no mires más información ni busques en google e imponte un proyecto sencillo para empezar. Te pongo algunos ejemplos:

  * Un algoritmo para ordenar palabras.
  * Un conversor de grados celsius a Farenheit o viceversa (o Julios a calorias, o km/h a m/s,...).
  * Abrir un fichero de texto, por ejemplo un csv, leerlo y a una columna de números sumarle 1000 a cada uno de los valores.
  * Cualquier [problema sencillo del proyecto Euler](https://projecteuler.net/problems).
  * ...

Si no eres capaz de resolverlo solo con el tutorial oficial ve al paso 3.

# Paso 3. Internet.

Es un pozo infinito de información. Por suerte hay varios sitios disponibles para poder preguntar de forma más acotada.

### En español:

  * [Lista de correo oficial de Python en castellano](https://mail.python.org/mailman/listinfo/python-es).
  * [Lista de correo de Python Argentina](http://python.org.ar/ListaDeCorreo).
  * [Majibu](http://python.majibu.org). Sitio de preguntas y respuestas sobre Python en español.

### En inglés:

  * [StackOverflow](http://stackoverflow.com/). Acostumbraos a él, en algunos momentos de vuestra vida no saldréis de ahí.
  * [Subreddit learnpython](http://www.reddit.com/r/learnpython).

### Recomendaciones de uso:

En todos los sitios que he enlazado en este paso podéis hacer preguntas. Las preguntas las responden personas que tienen ganas de ayudarte pero que también son gente ocupada que tienen cosas importantes que hacer.

  1. Primero deberías de buscar si tu pregunta ya ha sido hecha (lo más seguro) y ver si las respuestas que dieron te resuelven el problema. Si ya tienes la solución, perfecto, no has hecho perder el tiempo de nadie y tú ya puedes continuar.
  2. Si no has encontrado una respuesta, formula la pregunta en un único sitio (todos son buenas opciones) y procura dar el mayor número de detalles posibles para que la gente entienda tu problema. Si tienes código, enséñalo para que los demás puedan ver qué has intentado hacer o en qué punto te encuentras. Un ejemplo de [pregunta mal formulada y que no será bienvenida la puedes encontrar aquí](http://python.majibu.org/preguntas/2660/ejercicio-basico).
  3. Algunos han respondido tu pregunta. Te solucionen o no la vida, por favor, sé agradecido, la comunidad se convierte en más amena e inclusiva si todos somos educados y agradecidos. Esas personas han perdido su tiempo y han usado conocimientos que les ha costado un tiempo adquirir para intentar ayudarte de forma desinteresada.
  4. Alguien se muestra soberbio y/o maleducado. DON'T FEED THE TROLL.

# Paso 4. Ya eres capaz de resolver pequeños problemas.

Empieza a profundizar en temas más avanzados: Programación orientada a objetos, organización del código para hacerlo más mantenible/legible, desarrollo dirigido por pruebas,...

Algunos libros libres y gratis para ver cosas un poco más avanzadas:

  * [Dive into Python](http://www.diveintopython3.net/). Empieza por lo básico pero poco a poco va profundizando en cosas un poco más avanzadas. como orientación a objetos,  testing,... (EN INGLÉS).
  * [Think Python](http://www.greenteapress.com/thinkpython/thinkpython.html). Este libro está escrito por un profesor y basado en su experiencia enseñando Python. (EN INGLÉS).

# Paso 5. De Padawan a Jedi.

Crea pequeños proyectos, métete a colaborar en algún proyecto de código libre, comparte código, ayuda a jóvenes padawanes a convertirse en Jedis, da pequeñas charlas,... Todo ello te permite salir de tu zona de confort y te obliga a aprender.

Existen varios sitios para compartir proyectos y código. Entre los más conocidos tenéis:

  * [BitBucket](https://bitbucket.org/). Permite tener repositorios de código privados o públicos, funciona con varios sistemas de control de versiones (Mercurial y Git).
  * [Github](https://github.com/). Es el más famoso, el facebook del código. No te permite tener repositiorios privados si no es pagando o solo te permite interactuar con los repositorios usando Git.

Lee código. En muchas ocasiones no hay más remedio que leer código de otros, a ratos puede ser poco agradable pero te permite conocer cómo otros son capaces de resolver sus problemas, cómo aplican determinados patrones, cómo organizan su código, que librerías usan que tú desconocías,...

Acércate a tu grupo local. Estamos hablando de Python pero hay grupos locales de muchas cosas. Algunos relacionados con Python en España los puedes encontrar en:

  * [Calendario de eventos Python](http://calendario.es.python.org/). Mantenido por [@jcea](https://twitter.com/jcea) (si tienes un evento y quieres que aparezca en el calendario ponte en contacto con él).
  * [Meetup](http://www.meetup.com/).

Sé curioso para seguir aprendiendo.

# ¿Has llegado al último paso?

Espero que hayas disfrutado este viaje que, seguramente, te haya ocupado días (no vaciles), semanas (te quiero conocer), meses (eres muy aplicado) o años (tú eres de los mios). Poco más se puede decir que no sepas ya resolver por ti mismo.

P.D.: En ningún momento menciono cursos MOOC porque, en mi modesta opinión, muchas veces no se ajustan a las necesidades reales del alumno, tienen saltos importantes de conocimiento, a veces el guión a seguir no está claro, son excesivamente básicos o complejos,... Todo esto, en algunas ocasiones provoca pérdidas de tiempo y frustración. Puedo estar equivocado y no te costará encontrar cursos MOOC para aprender a programar.

P.D.2: Si quieres incluir algo más o crees que algo es incorrecto, lo podemos discutir en los comentarios y llegado el caso, actualizo esta mini guía.