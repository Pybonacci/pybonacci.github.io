---
title: Presentando Mathics: una alternativa libre y ligera a Mathematica
date: 2012-04-02T15:42:02+00:00
author: Juan Luis Cano
slug: presentando-mathics-una-alternativa-libre-y-ligera-a-mathematica
tags: cas, foss, mathematica, mathics, python, sympy

A través de la lista de correo sage-dev acabo de descubrir hace un momento [Mathics](http://www.mathics.org/): un sistema de álgebra computacional (CAS) libre y gratuito con una interfaz web y basado en SymPy y Sage.<figure id="attachment_126" style="width: 560px" class="wp-caption aligncenter">

![Interfaz web de Mathics](http://pybonacci.org/images/2012/04/2012-04-02-161414_1366x768_scrot.png)

En el momento de escribir estas líneas se trata de un proyecto personal de [Jan Pöschko](http://www.poeschko.com/), un estudiante austríaco. Me parece impresionante que [una sola persona haya llevado esto adelante](http://www.mathics.net/doc/manual/introduction/who-is-behind-it/): este hombre tiene mi más sincera admiración.

Aunque está basado en SymPy y tiene soporte para Sage también, Mathics toma la sintaxis de Mathematica, el popular CAS de Wolfram Research. Como se menciona en la [introducción](http://www.mathics.net/doc/manual/introduction/), Mathics busca parecerse a Mathematica lo máximo posible. Puedes leer [las motivaciones del proyecto](http://www.mathics.net/doc/manual/introduction/why-yet-another-cas/) <del datetime="2012-04-02T17:12:32+00:00">(hay por ahí quien dice que tienen un punto de ironía, cada uno que lo interprete a su manera :P)</del>.

Al contrario que CAS como Mathematica, Maple o Derive, Mathics [es libre y gratuito](http://www.mathics.net/doc/manual/introduction/) ([GPLv3](http://www.mathics.net/doc/license/gnu-general-public-license/)):

> «It is free both as in “free beer” and as in “freedom”».

La interfaz web disponible en <http://www.mathics.net/> hace que podamos utilizarlo también como sustituto de Wolfram|Alpha (no te dice el sentido de la vida, el Universo y todo lo demás... pero resuelve ecuaciones :)). Además, se puede [instalar localmente](http://www.mathics.net/doc/manual/installation/installation-prerequisites/) y ejecutarlo como cualquier otro programa de nuestro ordenador, preferiblemente en Linux y Mac OS X aunque también, en principio, puede instalarse en Windows (aunque no hay de momento un instalador que haga el proceso rápido y directo).

Algunas de las características más reseñables de Mathics son

  * Un poderoso lenguaje de programación funcional (el que usa Mathematica),
  * Un sistema de reglas y búsqueda de patrones,
  * Números racionales, complejos y aritmética de precisión arbitraria,
  * Numerosos métodos de manipulación de listas y estructuras,
  * Una interfaz gráfica interactiva en el navegador que usa [MathML](http://www.w3.org/Math/) y [MathJax](http://www.mathjax.org/demos/mathml-samples/), además de una interfaz de línea de comandos,
  * Creación de imágenes y gráficas y representación en el navegador usando [SVG](http://www.w3.org/Graphics/SVG/),
  * Una versión online en [http://www.mathics.net](http://www.mathics.net/) para acceso instantáneo,
  * Exportación de resultados a $LaTeX$ usando [Asymptote](http://asymptote.sourceforge.net/) para los gráficos,
  * Una forma muy sencilla de definir nuevas funciones en Python y
  * Un sistema integrado de documentación y pruebas.

En la misma interfaz web podéis ver [una pequeña muestra de las posibilidades de Mathics](http://www.mathics.net/#queries=1%20%2B%202%20-%20x%20*%203%20x%20%2F%20y&queries=Sin%5BPi%5D&queries=N%5BE%2C%2030%5D&queries=Plot%5B%7BSin%5Bx%5D%2C%20Cos%5Bx%5D%7D%2C%20%7Bx%2C%20-Pi%2C%20Pi%7D%5D&queries=D%5BSin%5B2x%5D%20%2B%20Log%5Bx%5D%20%5E%202%2C%20x%5D&queries=Integrate%5BTan%5Bx%5D%20%5E%205%2C%20x%5D&queries=A%20%3D%20%7B%7B1%2C%202%2C%203%7D%2C%20%7B4%2C%205%2C%206%7D%2C%20%7B7%2C%208%2C%209%7D%7D%3B%20MatrixForm%5BA%5D&queries=LinearSolve%5BA%2C%20%7B1%2C%201%2C%201%7D%5D%20%2F%2F%20MatrixForm&queries=Eigenvalues%5BA%5D&queries=%23%20%5E%202%20%26%20%2F%40%20Range%5B10%5D&queries=Graphics%5BTable%5B%7BEdgeForm%5B%7BGrayLevel%5B0%2C%200.5%5D%7D%5D%2C%20Hue%5B(-11%2Bq%2B10r)%2F72%2C%201%2C%201%2C%200.6%5D%2C%20Disk%5B(8-r)%7BCos%5B2Pi%20q%2F12%5D%2C%20Sin%20%5B2Pi%20q%2F12%5D%7D%2C%20(8-r)%2F3%5D%7D%2C%20%7Br%2C%206%7D%2C%20%7Bq%2C%2012%7D%5D%5D). Es, además, muy fácil compartir cuadernos y resultados, simplemente haciendo clic en el asterisco de la esquina superior derecha.

Jan anda buscando desarrolladores, así que si queréis ayudar o tal vez escribir documentación, tutoriales, ... o simplemente ver cómo funciona un CAS por dentro, aquí tenéis [el código fuente de Mathics](https://github.com/poeschko/Mathics) en GitHub.

Un saludo a todos y larga vida al software libre 🙂