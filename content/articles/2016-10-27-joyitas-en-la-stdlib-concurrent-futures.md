---
title: Joyitas en la stdlib: concurrent.futures
date: 2016-10-27T14:37:36+00:00
author: Kiko Correoso
slug: joyitas-en-la-stdlib-concurrent-futures
tags: asincronia, asyncio, concurrent.futures, deferred, delayed, futures, multiprocessing, promises, stdlib, threading

El módulo que vamos a ver, `concurrent.futures`, tiene una funcionalidad limitada. Trata de introducir una capa de simplificación sobre los módulos `threading` y `multiprocessing`.

**Solo disponible en Python 3!!!!**

Según la [documentación oficial](https://docs.python.org/3/library/concurrent.futures.html), el módulo proporciona una interfaz de alto nivel para ejecutar _callables (¿invocables?)_ de forma asíncrona. Por su parte, [según la Wikipedia](https://es.wikipedia.org/wiki/Valor_futuro_(inform%C3%A1tica)), los futuros (no vamos a hablar de bolsa ni de especulación), en Programación, son un reemplazo para un resultado que todavía no está disponible, generalmente debido a que su cómputo todavía no ha terminado, o su transferencia por la red no se ha completado. El término _futures_ también lo podéis encontrar como _promises, delay, deferred_,... En general, independientemente de cómo lo queráis llamar, lo podéis ver como un resultado pendiente.

El módulo posee una base abstracta, `Executor`, que se usa para las subclases `ThreadPoolExecutor` y `ProcessPoolExecutor` que, si sois un poco deductivos, sirven para usar multihilo (`threading`) o multiproceso (`multiprocessing`) por debajo, respectivamente.

Veamos un ejemplo de la primera subclase, `ThreadPoolExecutor`, con un caso práctico que hice el otro día. Tenía que descargar cosas y lo quise hacer asíncrono, es un ejemplo muy típico, pero, además, quisé mostrar en pantalla un mensaje dinámico para que se viese que el programa estaba 'haciendo algo' y que no se había quedado 'tostado'. Pongamos el ejemplo y luego lo comentamos y vemos el resultado:

<pre class=" language-python"><code class=" language-python">from concurrent.futures import ThreadPoolExecutor
from urllib import request
import itertools
from time import sleep

# Vamos a descargar algunas fotos de mi (abandonado) flickr.
# TODO: retomar la fotografía, hijos mediante.
pics = [
    'https://farm5.staticflickr.com/4117/4787042405_37e548cf3a_o_d.jpg', # Siria :_·(
    'https://farm3.staticflickr.com/2375/2457990042_e6d6982cb2_o_d.jpg', # Cuba, a ver si puedo volver para la ScipyLa'17
    'https://farm4.staticflickr.com/3149/3104818507_06cf582ba3_o_d.jpg', # Boston, amigos
    'https://farm3.staticflickr.com/2801/4084837185_4c12f32b1f_o_d.jpg', # Serengeti, una y mil veces
]

def tareas(pictures, workers=4):
    
    def get_pic(url):
        # No vamos a guardar las imágenes
        pic = request.urlopen(url).read()
        return pic
    
    msg = 'Descargando imágenes de https://www.flickr.com/photos/runbear1976 '
    ciclo = itertools.cycle('\|/-')
    executor = ThreadPoolExecutor(max_workers=workers)
    ex = [executor.submit(get_pic, url) for url in pictures]
    while not all([exx.done() for exx in ex]):
        print(msg + next(ciclo), end='\r')
        sleep(0.1)
    return ex

raw_data = tareas(pics, workers=4)
print()</code></pre>

Si ejecutáis el anterior código en una terminal, yo lo he llamado _temp.py_, podéis ver el efecto que andaba buscando:

![futures](https://pybonacci.org/images/2016/10/futures.gif)

Vamos a comentar la función `tareas` un poco más en detalle.

  1. Dentro de esa función he escrito otra que se llama `get_pic`. Esa función lo único que hace es descargar la información bruta de las imágenes. Las imágenes no las vamos a guardar en nuestro disco duro ya que no es necesario.
  2. Luego vamos a crear `msg` y `ciclo` que serán el mensaje que mostraremos en pantalla. `ciclo` es un [iterador infinito](https://docs.python.org/3/library/itertools.html#itertools.cycle).
  3. Más tarde instanciamos `ThreadPoolExecutor` y creamos una lista, `ex`, donde guardar los ['futuros'](https://docs.python.org/3/library/concurrent.futures.html#future-objects). Los objetos instanciados de la clase `Future` (cada uno de los elementos de la lista `ex`) encapsulan la ejecución asíncrona del _callable ('invocable')_. Cada uno de estos objetos provienen de `Executor.submit()`.
  4. Dentro del bloque `while` le preguntamos a cada una de las tareas si han terminado usando el método `Future.done()`. Si ha terminado nos devolverá `True` o, en caso contrario, nos devolverá `False`. Como quiero mostrar el mensaje de la imagen de más arriba mientras no hayan terminado todas las descargas en el bucle exijo que todas hayan terminado usando la función builtin `all`.
  5. Y, por último, devuelvo la lista con los 'futuros'.

En la función `tareas` podéis definir el número de _workers_ a usar.

Si hacéis un print de raw_data, lo que devuelve la llamada a tareas, veréis que es algo parecido a lo siguiente:

<pre class=" language-python"><code class=" language-python">[&lt;Future at 0x7fb50f324dd8 state=finished returned bytes&gt;,
 &lt;Future at 0x7fb50f324828 state=finished returned bytes&gt;,
 &lt;Future at 0x7fb50c08ed30 state=finished returned bytes&gt;,
 &lt;Future at 0x7fb50c08ea58 state=finished returned bytes&gt;]</code></pre>

Si queréis la información bruta de una de las descargas podéis usar el método `Future.result()`. Si, además, volvéis a llamar al método `Future.done()` veréis ahora que os devuelve `True`, ya que está terminada la tarea.:

<pre class=" language-python"><code class=" language-python">futuro_x = raw_data[0]
print(futuro_x.result())
print(futuro_x.done())</code></pre>

Espero que la mini introducción os haya resultado de utilidad y de interés. Como siempre, si veis alguna incorrección, falta de ortografía,..., avisadnos en los comentarios.
