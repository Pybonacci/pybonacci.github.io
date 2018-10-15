---
title: Presentando brythonmagic
date: 2014-03-03T06:00:50+00:00
author: Kiko Correoso
slug: presentando-brythonmagic
tags: brython, cliente, d3, frontend, ipython, javascript, openlayers

En esta entrada os voy a enseñar una extensión que he creado que 
funciona sobre el IPython notebook, es decir, está pensada para 
funcionar en un navegador. Si no sabéis muy bien que son las 
'cell magics' (no sé muy bien como traducir esto, podría ser algo así 
como magia que aplica sobre celdas) le podéis echar un ojo a 
[esta entrada](https://pybonacci.org/2014/01/24/157-cosas-de-ipython-que-no-sabias-y-nunca-preguntaste-i/) 
donde ya creamos alguna función mágica ('line magics') de ayuda. De 
todas formas, entre mis planes está el hacer una parte de la serie 
'157 cosas de IPython...' que hable sobre las 'cell magics'. No han 
salido nuevos capítulos ya que estoy viendo como evoluciona IPython 
2.0.0 y adaptar las entradas a la nueva versión de IPython para que no 
se queden desfasadas ya de salida...

Bueno, a lo que vamos,... ¿Qué es eso de `brythonmagic`? `Brythonmagic` 
pretende ayudar a los programadores Python a crear un puente entre el 
mundo de la programación científica en Python y el de la visualización 
interactiva en javascript a través del IPython notebook y con la ayuda 
de [Brython](http://brython.info/), una implementación de Python3 hecha 
en javascript y en Python y que funciona en el lado del cliente 
(navegador web). De esa forma, escribiendo en Python/subconjunto de 
Python/seudoPython/... (i.e., escribiendo en Brython) podemos acceder 
al navegador y a interesantes librerías javascript que funcionan en el 
navegador.

Brython es un proyecto que ya empieza a madurar y nos permite hacer 
cosas bastante interesantes que hasta ahora estaban vetadas para los 
pythonistas. Mediante `brythonmagic` he llevado las capacidades de 
Brython al notebook de IPython creando una 'cell magic', `%%brython`, 
que permite ejecutar código Brython dentro del navegador y nos permite 
manejar documentos HTML, acceder al DOM,...

El [funcionamiento es muy sencillo](https://github.com/kikocorreoso/brythonmagic#installation), 
añades la extensión al notebook de IPython, añades las librerías de 
Brython que vayas a necesitar y después ya puedes ejecutar celdas de 
código Brython dentro del notebook y ver el resultado al momento.

A día de hoy permite una [serie de opciones](https://github.com/kikocorreoso/brythonmagic#usage):

  * Obtener, mediante pantalla, el html que se usa para el output de la celda de código
  * Indicar qué librerías javascript vamos a usar en la celda de código
  * Usar datos de Python creados en otras celdas y que queramos usar en la celda de código Brython
  * Indicar el nombre del contenedor (elemento HTML `div`) de la salida.

En el siguiente vídeo podéis echarle un vistazo rápido a lo que se puede 
hacer con `brythonmagic`. En el vídeo, entre otras cosas, accedemos a 
las librerías d3js (gráficos interactivos) y openlayers (mapas interactivos):

[youtube=www.youtube.com/watch?v=adQzjuUX0kw]

El notebook usado en el vídeo está en el 
[repositorio](https://github.com/kikocorreoso/brythonmagic) por si lo 
queréis ejecutar de forma local.

El repo de Brython lo tenéis 
[aquí](https://bitbucket.org/olemis/brython/overview).

Además de para usarse para lo comentado anteriormente también lo podéis 
usar para probar cosas de Brython en un entorno amigable como el 
notebook de IPython (resaltado de sintáxis, autocompletado, formateo 
del código, comentarios en Markdown,...), es decir, si eres un 
'frontender' y quieres probar Brython puedes usar `brythonmagic` y 
IPython para ello :-).

Saludos.

P.D.: Se agradecen ideas para mejorar `brythonmagic`.
