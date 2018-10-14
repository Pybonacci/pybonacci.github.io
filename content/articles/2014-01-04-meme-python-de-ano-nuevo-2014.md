---
title: Meme Python de Año Nuevo 2014
date: 2014-01-04T11:55:01+00:00
author: Juan Luis Cano
slug: meme-python-de-ano-nuevo-2014

¡Feliz año a todo el mundo! Hoy queremos celebrar que ha empezado el 2014 ¡**con nuestro artículo número 100**! 😀 Para ello y como es costumbre desde el año pasado vamos con el Meme Python de Año Nuevo de Tarek Ziadé.

## 1. ¿Cuál es la aplicación, framework o biblioteca Python más interesante que has descubierto en el 2013?

He seguido utilizando mucho el notebook de IPython, y Anaconda me ha facilitado mucho la vida cuando me las he tenido que ver en Windows. La biblioteca que más me ha gustado usar ha sido [pytest](http://pytest.org), porque hace escribir tests y medir cobertura de código extremadamente sencillo.

## 2. ¿Qué nueva técnica de programación aprendiste en el 2013?

Progresé bastante con el desarrollo dirigido por tests (puedes leer cómo fue [mi primera auditoría de código](https://pybonacci.org/2013/12/09/mi-primera-auditoria-de-codigo-revisando-scikit-aero/ "Mi primera auditoría de código: revisando scikit-aero")) y utilicé por primera vez un servidor de integración continua, [Travis CI, para mi paquete poliastro](https://travis-ci.org/Pybonacci/poliastro). Este servidor corre todos los tests de tu paquete bajo diversas configuraciones (diferentes versiones de Python, por ejemplo), con lo cual es una herramienta perfecta para integrar pull requests y para comprobar que tu código funciona en plataformas a las que no puedes acceder. ¡Simplemente genial!

## 3. ¿A qué proyecto de software libre contribuiste más en el 2013? ¿Qué hiciste?

Este año fui tomando más confianza a la hora de contribuir código a los proyectos que más uso. Concretamente, [entre julio y septiembre trabajé un poco en el módulo signal de SciPy](https://github.com/scipy/scipy/commits/master?author=juanlu001), en la parte de sistemas LTI (estaba ya pensando en escribir un artículo sobre [teoría de control en Python](https://pybonacci.org/2013/10/10/teoria-de-control-en-python-con-scipy-i/ "Teoría de control en Python con SciPy (I): Conceptos básicos")). También [reescribí odeint desde cero en Fortran 90](https://github.com/scipy/scipy/pull/2818) utilizando f2py, pero por desgracia hice algunos cambios que rompían la compatibilidad hacia atrás y compilar Fortran 90 en Windows es mucho más difícil de lo que parecía así que de momento se ha quedado ahí.

También trabajé bastante en poliastro, una biblioteca para mecánica orbital en Python. Ahora mismo estaba [reescribiéndola](https://github.com/Pybonacci/poliastro/pull/14) para deshacerme del código Fortran existente (y así simplificar la instalación) y que tuviera una API más atractiva, pero está siendo más difícil de lo esperado y el tiempo de los exámenes se acerca 🙂

## 4. ¿Qué blog o web sobre Python leíste más en el 2013?

Un año más, la web sobre Python que más he leído es [la propia documentación de NumPy y SciPy](http://docs.scipy.org/). Estoy en un proceso de aprendizaje constante y me hace mucha falta para ir solucionando las dudas que me surgen. Sigo echando de menos más blogs sobre Python en español, aunque muy pronto vamos a relanzar el planet de Python Hispano y vamos a recolectar unos cuantos 🙂 Este año descubrí [CAChemE](http://www.cacheme.org/) y a menudo escriben sobre Python. ¡No les perdáis de vista!

He leído también mucho código ajeno, especialmente de SymPy y Astropy, en GitHub. Son una excelente fuente de inspiración.

## 5. ¿Cuáles son las tres cosas que más te gustaría aprender en el 2014?

  * Computación paralela
  * Aprendizaje automático (_machine learning_)
  * Creación de interfaces gráficas con Python (la mantengo desde el meme anterior :P)

## 6. ¿Cuál es el programa, aplicación o biblioteca que más te gustaría que alguien escribiera en 2014?

No sabría cuál elegir entre una wiki en Python decente (no considero MoinMoin decente en casi ningún sentido) o un motor de blogs tipo WordPress en Python (no considero que haya ninguno que se le acerque). O un editor WYSIWYG web para reStructuredText. O algo tipo wxWidgets pero que no sea ultra complicado de instalar y cuya web no parezca hecha a principios de los '90 🙂

* * *

Recuerda, las reglas del meme son:

  1. Copia y responde las preguntas en tu blog.
  2. Si tienes tuiter, anúncialo en el hashtag [#2014pythonmeme](https://twitter.com/search?q=%232014pythonmeme)

¡Anímate! Un saludo 😀