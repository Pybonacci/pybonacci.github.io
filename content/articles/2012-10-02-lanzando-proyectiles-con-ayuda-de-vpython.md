---
title: Lanzando proyectiles (con ayuda de vpython)
date: 2012-10-02T22:31:24+00:00
author: Kiko Correoso
slug: lanzando-proyectiles-con-ayuda-de-vpython
tags: cinemática, física, movimiento parabólico, python, vpython

La mayoría de vosotros habréis resuelto el típico problema del lanzamiento de un proyectil que describe una trayectoria parabólica. Las [ecuaciones que describen el movimiento](http://es.wikipedia.org/wiki/Movimiento_parab%C3%B3lico) son:

  * Vector posición

$x = v\_{0x} t + x\_0$

$y = -frac{1}{2} g t^{2} + v\_{0y} t + y\_0$

  * Vector velocidad

$v\_x = v\_{0x}$ con $v\_{0x} = v\_0 cos alpha$

$v\_y = -g t + v\_{0y}$ con $v\_{0y} = v\_0 sin alpha$

Hoy vamos a intentar resolverlo de forma gráfica con la ayuda de python y [vpython](http://www.vpython.org/index.html). La biblioteca vpython une python con una librería gráfica 3D de forma que, como vamos a ver, hacer [animaciones 3D sencillas](http://www.vpython.org/contents/docs/visual/index.html) se convierte en un juego.

<pre><code class="language-python">import visual as vs
import numpy as np
## valores iniciales (modifícalos bajo tu responsabilidad)
v0 = 20 ## v en m/s
alfa = 60 ## ángulo en grados
vel_fotogramas = 10  ## la velocidad del video
## Constantes
g = 9.81 ## Aceleración de la gravedad
## ecuaciones
v0x = v0 * np.cos(np.deg2rad(alfa))
v0z = v0 * np.sin(np.deg2rad(alfa))
t_total = 2 * v0z / g
x_final = v0x * t_total
## Empezamos con visual python (vpython)
## Creamos el 'suelo'
suelo = vs.box(pos = (x_final/2., -1, 0),
               size = (x_final, 1, 10), color = vs.color.green)
## Creamos el 'cañón'
canyon = vs.cylinder(pos = (0, 0, 0),
                     axis = (2 * np.cos(np.deg2rad(alfa)), 2 * np.sin(np.deg2rad(alfa)), 0))
## Creamos el proyectil y una línea que dejará la estela del proyectil
bola = vs.sphere(pos = (0, 0, 0))
bola.trail = vs.curve(color=bola.color)
## Creamos la flecha que indica la dirección del movimiento (vector velocidad)
flecha = vs.arrow(pos = (0, 0, 0),
                  axis = (v0x, v0z, 0), color = vs.color.yellow)
## texto (ponemos etiquetas para informar de la posición del proyectil)
labelx = vs.label(pos = bola.pos, text= 'posicion x = 0 m', xoffset=1,
                  yoffset=80, space=bola.radius, font='sans', box = False,
                  height = 10)
labely = vs.label(pos = bola.pos, text= 'posicion y = 0 m', xoffset=1,
                  yoffset=40, space=bola.radius, font='sans', box = False,
                  height = 10)
## Animamos todo el cotarro!!!
t = 0
while t &lt;= t_total:
    bola.pos = (v0x * t, v0z * t - 0.5 * g * t**2, 0)
    flecha.pos = (v0x * t, v0z * t - 0.5 * g * t**2, 0)
    flecha.axis = (v0x, v0z - g * t, 0)
    bola.trail.append(pos=bola.pos)
    labelx.pos = bola.pos
    labelx.text = 'posicion x = %s m' % str(v0x * t)
    labely.pos = bola.pos
    labely.text = 'posicion y = %s m' % str(v0z * t - 0.5 * g * t**2)
    t = t + t_total / 100.
    vs.rate(vel_fotogramas)</code></pre>

Voy a explicar brevemente lo que hace el código:

<!--more-->

  1. Primero definimos la velocidad inicial del proyectil y el ángulo con que sale disparado (podéis tocar estos valores para jugar y experimentar)
  2. Calculamos los resultados para definir un poco el escenario que vamos a dibujar
  3. En visual python definimos una caja (que asimilamos a la tierra plana en la que aún creen algunos :-()
  4. En visual python definimos el cañón (un simple cilindro)
  5. En visual python definimos el proyectil y su estela (una esfera)
  6. En visual python colocamos unas etiquetas que informarán de la posición del proyectil durante todo el movimiento
  7. Finalmente hacemos un bucle hasta llegar al t final (rate sirve para definir la velocidad de la animación)

El resultado que os debería salir debería ser algo parecido a lo que se puede ver en el siguiente vídeo.

[youtube=http://www.youtube.com/watch?v=Il5wYLQEllI]

Espero que os haya gustado. Si alguno se anima a hacer algún ejemplo (científico) similar nos encantaría que lo compartiera en los comentarios. Por otro lado, siempre estamos abiertos a críticas, sugerencias y colaboraciones.

Saludos.

[Edito] He cometido una errata, en la línea 54 ponía 'posición x' y debería poner 'posición y'. En el vídeo salen dos etiquetas x, la segunda corresponde a la y. En cuanto pueda vuelvo a hacer y a subir el vídeo. Disculpad las molestias.