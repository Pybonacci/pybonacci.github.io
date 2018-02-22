---
title: Mi primera auditoría de código: revisando scikit-aero
date: 2013-12-09T16:59:34+00:00
author: Juan Luis Cano
slug: mi-primera-auditoria-de-codigo-revisando-scikit-aero
tags: python, TDD, testing

## Introducción

Como ya sabéis Javier Gutiérrez, profesor de la Universidad de Sevilla, está escribiendo una serie de entradas en Pybonacci sobre [desarrollo dirigido por pruebas en Python](http://pybonacci.org/author/javierjus/), que os animo a leer si no lo habéis hecho todavía. Pues bien, después de conocernos en la PyConES rescatamos la idea de aplicar estos conceptos a problemas no tan genéricos y más cercanos al software científico que escribimos nosotros. Fruto de esta idea Javier se ha tomado la molestia de revisar nuestra biblioteca scikit-aero, y ha escrito [una entrada en su blog sobre el proceso](http://iwt2-javierj.tumblr.com/post/69258809610/analizando-scikit-aero-en-python-2-x):

> Como comenté en la entrada [Auditorias de código o aprendamos juntos a ser mejores](http://iwt2-javierj.tumblr.com/post/64940568924/auditorias-de-codigo-o-aprendamos-juntos-a-ser-mejores "Auditorias de código o aprendamos juntos a ser mejores"), una de las cosas que más me gusta hacer es analizar código de otras personas para aprender y también para aplicar la [regla del buen boy scout](http://programmer.97things.oreilly.com/wiki/index.php/The_Boy_Scout_Rule "regla del buen boy scout") e intentar contribuir a que ese código sea un poquito mejor.
> 
> El último proyecto que he analizado por el momento ha sido ha sido [Scikit-Aero en Github](https://github.com/Pybonacci/scikit-aero "Scikit-Aero en Github") del fenomenal Juan Luis Pibonacci que lleva el proyecto del [blog Pybonacci](http://pybonacci.org/ "blog Pybonacci") (enlace) y en el que colaboro son una serie de entradas sobre TDD / Desarollo Dirigido por Pruebas.

En este artículo voy a contar brevemente cómo las cosas que he aprendido 🙂

## Sobre scikit-aero

[scikit-aero](https://github.com/Pybonacci/scikit-aero) es una pequeña biblioteca Python que escribí mientras estudiaba flujos isentrópicos, ondas de choque, expansiones de Prandtl-Meyer y similares en una materia llamada «Aerothermodynamics». Es, por tanto, algo bastante específico. De ella me serví por ejemplo para producir este diagrama:<figure id="attachment_2028" style="width: 367px" class="wp-caption aligncenter">

[<img class=" wp-image-2028 " src="http://new.pybonacci.org/images/2013/12/oblique_shocks.png" alt="Diagrama de ondas de choque oblicuas" width="367" height="297" srcset="https://pybonacci.org/wp-content/uploads/2013/12/oblique_shocks.png 612w, https://pybonacci.org/wp-content/uploads/2013/12/oblique_shocks-300x242.png 300w" sizes="(max-width: 367px) 100vw, 367px" />](http://new.pybonacci.org/images/2013/12/oblique_shocks.png)<figcaption class="wp-caption-text">Diagrama de ondas de choque oblicuas</figcaption></figure> 

Podéis consultar el código en [este notebook de ejemplo](http://nbviewer.ipython.org/github/Pybonacci/scikit-aero/blob/master/examples/Oblique%20shocks%20chart.ipynb). Mi idea era además tratar de crear un código bien documentado, bien estructurado y bien probado.

<!--more-->

Para los tests utilicé [pytest](http://pytest.org/), y para la cobertura el plugin [pytest-cov](https://pypi.python.org/pypi/pytest-cov).

Según el artículo de Javier no hice un mal trabajo, aunque quedaban unas cuantas cosas por mejorar en los tests del módulo `isentropic.py`.

## Pruebas para una biblioteca científica: mi enfoque

scikit-aero consiste fundamentalmente en funciones que hacen cálculos matemáticos. No hay, por tanto, interacción con el sistema o con elementos del exterior, jerarquías de objetos complejas, tratamiento sofisticado de entradas del usuario... Mi enfoque para probar estas funciones fue **acudir a referencias reconocidas** y asegurar que producen el resultado numérico esperado. En este caso me basé en:

  * Tablas de informes técnicos de la NASA o la NACA, como por ejemplo NACA-TR-1135-1953 "Equations, tables, and charts for compressible flow" http://hdl.handle.net/2060/19930091059
  * Problemas resueltos de textos universitarios, como por ejemplo "Modern compressible flow" de J. D. Anderson.

Además, incluí en cada archivo y a veces en cada función de dónde están obtenidos los datos para que cualquier persona los pudiera comprobar. La ventaja de usar informes de la NACA es que [los documentos que proceden del gobierno de Estados Unidos están bajo el dominio público](http://www.usa.gov/copyright.shtml) y por tanto no tienen restricciones de copyright. Intenté usar este tipo de fuentes cuando fuese posible.

(Inciso: ¿Qué tal si los gobiernos de otros países toman nota?)

Puesto que estamos lidiando en la mayoría de los casos con resultados que tienen imprecisiones, para cada prueba decidí de manera más o menos arbitraria la precisión que iba a manejar para las comparaciones, usando las funciones `assert_almost_equal` y `assert_array_almost_equal` de `numpy.testing`. Si no conseguía un resultado correcto hasta 2 decimales, solía adimensionalizar las variables o directamente comprobar si algo estaba fallando.

Para scikit-aero he conseguido una precisión de al menos 2 decimales en la mayoría de las funciones, salvo en la parte de propiedades de la atmósfera estándar que está menos trabajada (se aceptan pull requests).

## Lecciones aprendidas

Voy a comentar algunas cosas que aprendí revisando la pull request. Podéis [leer los comentarios](https://github.com/Pybonacci/scikit-aero/pull/13/files) vosotros mismos en GitHub.

### Dialogar con tus colaboradores

Cuando recibí las mejoras tardé varios días en reaccionar y solo cuando Javier me lo pidió: ¡mal! Como creador de una biblioteca, si quieres que sea atractivo para otros mejorar tu código es fundamental comentar qué te parece el suyo y **entablar un diálogo con potenciales colaboradores**. A veces habrá cosas que no te gusten y las tendrás que discutir, pero con eso no harás sino aprender más.

### Probar todo el código

En primer lugar, vimos que había un test que se había quedado a medio escribir y faltaban algunas funciones por probar. Este es el fallo más evidente y más trivial: **es importante que todo el código esté probado**. La _cobertura_ es el porcentaje de código probado frente al código total, y cuanta más alta sea más seguros podremos estar que que no hay casos especiales que pueden producir fallos inesperados. Lo ideal es que esté en el 100 % 😉 (aunque por encima del 90 % está bien en general) y esto suele llevar a una proporción de líneas de test / líneas de programa mayor que 1.

### Consistencia en las pruebas

Esto lo explica mucho mejor Javier:

> Veo falta de consistencia en las pruebas. En algunas pruebas se usa un bucle _for_ para verificar varios resultados esperados uno a uno, pero en otras se utiliza un _assert_array_ (definida en _NumPy_)  que verifica todos los resultados son una sola llamada. El bucle for ambién aumenta la complejidad ciclomática y hace necesario escribir más código, con lo que hay más probabilidades de equivocarse, así que cambio todos los bucles _for_ por llamadas a _assert_array._

Me falló que las pruebas fuesen **más homogéneas**. Esto se ha corregido ya 🙂

### Incluir lo justo y necesario

Es desable **eliminar todo código superfluo de las pruebas**, para que estas sean lo más simples posible. De esta forma será más fácil descubrir posibles fallos.

### ¡Complejidad ciclomática!

Estos palabros me espantaron un poco al principio, pero he aprendido que la [complejidad ciclomática](http://en.wikipedia.org/wiki/Cyclomatic_complexity) es una métrica muy utilizada y para valorar la complejidad de un programa. La de scikit-aero era bastante baja (eso es bueno) pero la de los tests debería haber sido un poco menor. En Python se puede medir con la biblioteca [radon](https://radon.readthedocs.org/en/latest/intro.html). La tendré muy en cuenta de ahora en adelante cuando escriba código nuevo.

## Conclusiones

Los científicos e ingenieros que escribimos programas de ordenador mientras trabajamos (¿todos?) tenemos **mucho, mucho** que aprender de los informáticos. Ellos sabrán menos ecuaciones diferenciales y menos resistencia de materiales, pero en lo que respecta a software estamos en la Edad de Piedra en comparación. Seguimos cayendo en problemas superados desde hace años: aún nos enviamos correo en adjuntos de correo electrónico, aún no probamos ni documentamos el software y un largo etcétera. Creo que tenemos que establecer una relación más estrecha con los programadores profesionales para mejorar nuestros programas y hacer nuestra vida más fácil (¿a quién le gusta sufrir porque no se acuerda de qué versión de todas las que hay en la cadena de emails es la buena?).

**Y vosotros, ¿escribís ya pruebas en vuestros programas? ¿Conocíais ya las herramientas que hemos mencionado para ello? En caso contrario, ¿crees que empezarás a tomártelo más en serio? ¡Cuéntanos en los comentarios!**