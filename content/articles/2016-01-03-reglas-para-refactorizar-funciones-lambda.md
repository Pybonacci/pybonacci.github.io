---
title: Reglas para refactorizar funciones lambda
date: 2016-01-03T14:27:12+00:00
author: Kiko Correoso
slug: reglas-para-refactorizar-funciones-lambda
tags: programación funcional, python, refactoring, trol

Un gran ejercicio que podéis hacer de vez en cuando es revisar la documentación oficial de Python. La misma me parece increiblemente completa aunque también un poco anárquica o sin un guión mínimamente claro para seguir diferentes tópicos.

Hoy, revisando el [HOWTO de programación funcional, casi al final del documento y sin llamar la atención](https://docs.python.org/3.6/howto/functional.html#small-functions-and-the-lambda-expression), he encontrado la siguiente documentación para refactorizar funciones lambda sugerida por [Fredrik Lundh](https://wiki.python.org/moin/FredrikLundh). Las reglas que propone para la refactorización de las funciones lambda dicen lo siguiente:

<ol class="arabic simple">
  <li>
    Escribe una función Lambda.
  </li>
  <li>
    Escribe un comentario explicando qué se supone que hace la función lambda.
  </li>
  <li>
    Estudia el comentario durante un rato y piensa un nombre que capture la esencia del comentario.
  </li>
  <li>
    Convierte la función lambda a una declaración <code>def</code> usando el nombre pensado en el anterior paso.
  </li>
  <li>
    Elimina el comentario.
  </li>
</ol>

😛

Feliz año 2016.