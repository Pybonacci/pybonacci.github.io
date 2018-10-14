---
title: Revisión del libro &#8220;Introducción a la programación con Python&#8221; de Nilo Menezes
date: 2016-09-19T08:27:37+00:00
author: Kiko Correoso
slug: revision-del-libro-introduccion-a-la-programacion-con-python-de-nilo-menezes
tags: libro, libros, Menezes, Nilo, revisión, sorteo

En esta entrada vamos a hablar sobre el libro ["Introducción a la programación con Python" escrito por Nilo Ney Coutinho Menezes.](https://librodepython.com/ "El libro de Python en español")

El autor del libro se puso en contacto gentilmente con la "_Pybonacci Crew_" para hacer una revisión de su libro. Nosotros, como no podía ser de otra forma, hemos intentado colaborar agradeciendo su confianza.

Algunas generalidades del libro:

  * Escrito en español, cosa que se agradece dentro del desierto de recursos en español.
  * La calidad del libro en papel está muy bien y el diseño es bonito.
  * La primera edición en español (Julio/2016), que es la que hemos revisado, tiene un total de 336 páginas. En todo el libro no hay páginas en blanco para hacer que el libro sea más gordo, las partes de códigos de ejemplo del libro se saltan la parte relevante de [saltos de línea del PEP-8](http://pep8.org/#blank-lines) para que el libro sea más compacto incluso. Por tanto, tenemos un libro donde la mayor parte de las 336 páginas son páginas escritas y condensadas para que quepa incluso más en menos (_less is more_).
  * El libro es una traducción de un texto escrito en portugués/brasileño que ya va por su segunda edición y que se usa como texto introductorio en algunas universidades brasileñas.
  * Usa Python 3 en todo el libro (Python 3.4 para ser más precisos, aunque todo el código funcionará en Python 3.5 sin problemas).
  * La [tabla de contenidos está aquí](https://static.nilo.pro.br/es/sumario9788575225134.pdf).
  * Su [precio es inferior a los 25€](https://www.amazon.es/Introducci%C3%B3n-Programaci%C3%B3n-Python-Coutinho-Menezes/dp/8575225138/ref=aag_m_pw_dp?ie=UTF8&m=A2DTG2PF4SPBZ0).
  * Si vas a la PyConES podrás hablar con el autor en persona y pedirle que te ¡¡firme un ejemplar!!
  * No está disponible en formato electrónico.<figure id="attachment_3909" style="width: 608px" class="wp-caption aligncenter">

![](https://pybonacci.org/images/2016/09/2016-09-08_12.43.151-1024x759.jpg)

Vamos a repasar un poco la estructura del libro capítulo a capítulo:

## 1. Motivación

El libro empieza con una declaración de intenciones sobre las motivaciones para aprender a programar y sobre porqué programar. Me parece una buena forma de empezar y de indicarle al lector que el camino que pretende empezar no es sencillo pero sí muy interesante y motivador y que le permitirá poder aprender a hacer cosas increibles que pueden incluso hacer cambiar el mundo (no sé si a mejor o a peor).

## 2. Preparando el ambiente

Aquí se hace una introducción muy detallada sobre como hacer funcionar (C)Python en tu sistema operativo paso a paso (sobre todo en el caso de Windows). Es obvio que es más detallado en Windows ya que en Linux o MacOS Python suele venir preinstalado. En el caso de Windows vienen pantallazos de todo el proceso. Además, enseña cómo usar el IDLE.

## 3. Variables y entrada de datos

En el capítulo 3 empezamos a programar en Python y a aprender código Python. Es una introducción muy sencilla a como usar variables y como introducir valores desde el intérprete.

## 4. Condiciones

Como era de esperar se explican un poco de control de flujo empezando por las condiciones y como ejecutar código si se cumplen determinados requerimientos. Nuevamente, la introducción a condiciones se hace de una forma simple y directa sin perdernos en casos extremos o singulares que nos harían perder el foco del aprendizaje.

## 5. Repeticiones

Todo el capítulo se dedica a hablar del uso de `while` y cómo romper el bucle y usar condiciones para realizar determinadas tareas. Se introducen conceptos como `break.`

## 6. Listas

En este momento se empieza a hablar de secuencias (listas, tuplas, diccionarios,...), sus métodos, cómo acceder a los elementos (indexación, clave),... Continuando con los bucles, que se introdujeron en el capítulo anterior, hay un pequeño apartado para hablar de `for`. Se habla de conceptos como pilas y colas de forma muy sencilla, se muestra un ejemplo del método de la burbuja para ordenación (_bubble sort_),... En fin, que mientras enseña tipos de datos muy comunes en programación, como por ejemplo las listas de python, enseña otros conceptos más generales de forma simple y amena.

Una cosa que no me gusta en exceso es que en este capítulo nombra el uso de objetos y métodos sin haber, siquiera, hablado sobre programación orientada a objetos. Un novato en programación no debería entender a qué se refiere en este momento cuando se usan palabras como 'objeto' y un pequeño inciso para nombrar lo que es la programación a objetos o la eliminación total de referencias a objetos y métodos quizá sería más adecuado. Sé que no es sencillo abstraerse totalmente de algunos conceptos e incluso obviarlos llegados a determinado punto. Aún así, el capítulo se entiende completamente sin grandes problemas.

## 7.Trabajando con cadenas de caracteres

Este es otro capítulo muy completo donde entramos en el mundo de las cadenas de caracteres (_strings_). Se habla del trabajo típico con cadenas y de la funcionalidad más básica como contar, sustituir, eliminar,..., caracteres. Además, se hace una gran y completa introducción a como formatear cadenas usando `format` ([muchísimo más completo que el que hicimos nosotros aquí hace un tiempo](https://pybonacci.org/2013/03/03/formateando-numeros/)). Acaba el capítulo programando un ejemplo del juego del ahorcado.

## 8. Funciones

El capítulo vuelve a ser una delicia de leer ya que introduce los diferentes términos poco a poco y de forma escalonada para ir de menos a más. Se habla de funciones `lambda`, del _scope_ de las variables, de los argumentos, las palabras clave, argumentos opcionales,... Además, se meten otros conceptos como los módulos para ordenar nuestro código, empaquetamiento y desempaquetamiento de parámetros,...

##  9. Archivos

En este momento se habla sobre cómo trabajar con archivos de texto. Un capítulo siempre necesario en cualquier texto introductorio. Nuevamente, se explica todo con sencillez y de forma ordenada yendo de menos a más. También se muestra como trabajar con directorios y archivos desde Python usando el módulo `os.path`. En este punto, se usan programas donde se incluye todo lo adquirido en el resto de capítulos de forma muy natural.

En este capítulo se usan ejemplos en los cuales se escriben documentos HTML los cuales los veo menos útiles que otros ejemplos típicos y, en mi opinión, más generales como usar un fichero _json_ o un fichero _csv_,...

## 10. Clases y objetos

Ahora es cuando se muestra como usar clases y objetos. Se habla sobre herencia, métodos mágicos, sobrecarga de operadores,..., y se realiza un ejemplo muy extenso sobre una aplicación de una agenda.

En este momento considero que hay un salto muy abrupto en la curva de aprendizaje del libro. Hasta el capítulo 9 todo está explicado de forma detallada y paso a paso. En este momento se introduce la explicación del uso de clases y objetos y conceptos de programación orientada a objetos de forma que la curva de aprendizaje cambia su pendiente hablando de conceptos relativamente avanzados como la sobrecarga de operadores (sin nombrar el término), se introduce el uso de decoradores sin apenas explicación, se meten conceptos como `super` sin ninguna referencia previa,... El ejemplo de aplicación que se realiza en el capítulo pienso que es un poco avanzado y la explicación de los objetos que se hace está muy enlazada a cómo son los objetos en Python y no sobre hablar de objetos en general y de forma más abstracta.

## 11. Banco de datos

Aquí se habla sobre SQL y SQLite con Python. Se enseñan cosas básicas del lenguaje SQL y algunas cosas específicas del uso de SQL con SQLite y Python. Se ahonda en el ejemplo del capítulo anterior de la aplicación de una agenda cambiando algunas cosas para poder trabajar con una BBDD por debajo.

Este capítulo lo veo más accesorio y podría ser un apéndice o un capítulo en un libro más extenso y que entra en más profundidad en otra serie de conceptos. Dentro de un curso introductorio dónde se usa Python para aprender programación, el hecho de que se incluya un nuevo apartado con un nuevo lenguaje, SQL, con cosas específicas de SQLite no me resulta de lo más apropiado.

## 12. Próximos pasos

Se dan recomendaciones de por dónde seguir en este vasto mundo de la programación con enlaces a sitios y libros interesantes.

El capítulo es muy cortito (4 páginas) y se podría prescindir de él sin problemas.

## Apéndice A. Mensajes de Error

Una pequeña revisión sobre los mensajes de error más típicos que nos podemos encontrar cuando empezamos a programar con Python.

Es muy útil tener una pequeña explicación sobre los errores más típicos que nos vamos a ir encontrando y cómo aprender a interpretarlos.

# Apuntes varios sobre el libro:

Me gusta:

  * Lo detallado de las explicaciones en todos los capítulos excepto en los capítulos 10 y 11. En general, todo el libro es muy sencillo de seguir, todos los ejemplos están en [formato digital para poderlos descargar](https://librodepython.com/listagem/index.html). Me gusta especialmente la introducción a conceptos como pilas y colas, lo detallado del uso de `format`,...
  * Que en la página web dispones de [varios vídeos](https://librodepython.com/videos.html) para la parte más inicial del libro.
  * Que está en español.
  * Que use Python 3.
  * Que el precio del libro está bastante ajustado.
  * La predisposición del autor a introducir mejoras en futuras ediciones del libro.

No me gusta:

  * No me gusta que use el '_old style formatting_' cuando en Python 3 se introdujo `format` y ahora se está introduciendo un nuevo formateo más potente incluso que `format`.
  * No me gusta que use _unicode_ en la definición de variables, funciones, etcétera. Por ejemplo, 
        def rectángulo(...):
            ...
        
    
    Esta práctica puede dar lugar a errores tontos por olvidar una tilde, puede dificultar el trabajo en equipos multiculturales,...</li> 
    
      * En general, la traducción es muy mejorable. El texto se puede entender sin problemas por cualquier hispanohablante pero la traducción se puede mejorar bastante y no haría deslucir a un gran libro de introducción a la programación.
      * El capítulo 10 es un poco errático y da un salto cuantitativo grande en lo que a complejidad se refiere.
      * El capítulo 11 es un capítulo que está bien tener pero que eliminaría del libro si el foco del autor es ponérselo lo más fácil posible a los que se están iniciando en un lenguaje de programación. Creo que desvía un poco el foco general del libro aunque los conceptos que se expliquen en ese capítulo sean extremadamente interesantes.
      * Me gustaría que todos los ejemplos del libro cumpliesen con el PEP-8. Cuando se está aprendiendo algo es cuando hay que introducir una serie de convenciones y buenas prácticas. Si se adquieren malos hábitos desde un principio luego es más difícil corregirlos.
      * Me gustaría que hubiera versión electrónica.</ul> 
    
    # ¿Compraría este libro?
    
    Si se cumple que no sé leer en inglés y no tengo nociones de programación sin duda SÍ que compraría este libro, a pesar de algunas cosas que he puesto más arriba en el 'No me gusta'. Algunos de esos 'No me gusta' hacen deslucir un poco el libro pero más a nivel formal que a nivel general y técnico. Es un libro de buena calidad a un precio ajustado pero que se puede mejorar en distintos partes de forma sencilla.
    
    # Sorteamos una copia entre nuestros lectores
    
    El autor nos envió tres copias del libro. Dos se han usado en los PyDay de Mallorca y de Madrid. El tercero lo vamos a sortear entre todos los lectores de Pybonacci que además tengan entrada para la PyConES de este año. Para participar:
    
      * Solo tienes que escribir un tweet indicando porqué te gustaría tener este libro incluyendo un enlace a https://librodepython.com/
      * Una vez enviado el tweet nos lo enlazas en los comentarios de más abajo para que no se nos escape el tweet.
      * Si no tienes cuenta en twitter, déjanos un comentario más abajo indicando porqué te gustaría tener este libro.
    
    Tenéis hasta el miércoles, 21 de septiembre, a las 23:59:59 par participar en el sorteo. Al día siguiente se hará público el ganador y se entregará físicamente en la PyConES de Almería.
    
    **[Actualización] Anoche se cerró el plazo por lo que el ganador saldrá entre:**
    
    Sergio, Manuti, Miguel, Aníbal, Alberto y José.
    
    Para saber quién ha ganado podréis meter el número ganador del sorteo de la ONCE de hoy (2016/09/22) en el formulario de más abajo.
    
    
    
    Nos pondremos en contacto con el ganador en breve.
    
    Saludos a todos.
