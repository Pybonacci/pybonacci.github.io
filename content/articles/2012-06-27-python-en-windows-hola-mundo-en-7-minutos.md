---
title: Python en Windows: «¡Hola mundo!» en 7 minutos
date: 2012-06-27T18:00:42+00:00
author: Juan Luis Cano
slug: python-en-windows-hola-mundo-en-7-minutos
tags: instalación, python, windows

## Cómo instalar Python en Windows

En lugar de escribir un tutorial para todos, este asume dos cosas:

  * Eres un usuario de Windows curioso acerca de la programación, y
  * Te gustaría instalar el lenguaje de programación Python en tu ordenador con Windows, lanzar el intérprete de Python y ejecutar el clásico programa «¡Hola mundo!».

Si tienes preguntas del tipo «¿Qué es Python y por qué debería instalarlo en mi ordenador con Windows?» lee el principio de [Introducción a Python para científicos e ingenieros](https://pybonacci.org/2012/03/16/introduccion-a-python-para-cientificos-e-ingenieros/ "Introducción a Python para científicos e ingenieros"). Y si quieres instalar Python, vuelve.

¿Ya estás de vuelta? ¿No te habías ido? Vale. Seguimos.

De la [web oficial de Python](http://python.org/) podemos descargar directamente un sencillo instalador para poder utilizar Python en Windows.

¿Listo? Suponiendo que tienes una conexión de banda ancha, ya te quedan menos de siete minutos para tener Python instalado en tu ordenador y escribir tu primer comando en el intérprete. ¡Vamos!

<!--more-->

  * Abre otra pestaña (para poder seguir leyendo esta) haciendo Ctrl+clic en la [página de descargas de Python](http://python.org/download/) o en la imagen.

<p style="text-align:center;">
  <a href="http://python.org/download/"><img class=" wp-image-9 aligncenter" title="Python" alt="Página de descargas de Python" src="https://pybonacci.org/images/2012/03/python-logo-master-v3-tm-flattened.png" width="385" height="130" srcset="https://pybonacci.org/wp-content/uploads/2012/03/python-logo-master-v3-tm-flattened.png 601w, https://pybonacci.org/wp-content/uploads/2012/03/python-logo-master-v3-tm-flattened-300x101.png 300w" sizes="(max-width: 385px) 100vw, 385px" /></a>
</p>

  * El primer párrafo habla sobre implementaciones alternativas de Python. Ignóralo: vamos a instalar la «tradicional».
  * Python funciona en Windows, Mac y Linux así que hay varios enlaces para todos esos sistemas operativos. A nosotros nos interesa el de Windows.
  * <ins datetime="2013-12-23T10:39:18+00:00">Haz clic en «Python 3.3.3 Windows x86 MSI Installer» o «Python 3.3.3 Windows X86-64 MSI Installer» dependiendo de si tu procesador es de 32 bit o de 64 bit. Si no estás seguro, los ordenadores medianamente modernos son de 64 bit.</ins>
  * Cuando hagas clic en el enlace, Python se debería empezar a descargar.
  * Apunta dónde se va a guardar el archivo. Lleva algunos minutos completar la descarga, así que mientras puedes ver [la escena de la bruja de «Los caballeros de la Mesa Cuadrada»](http://youtu.be/O-El43VKZCw). ¿Ya? Bien, busca el archivo en tu ordenador.
  * En el momento de escribir esto, el archivo que has descargado se llama <ins datetime="2013-12-23T10:39:18+00:00"><code>python-3.3.3.msi</code> y pesa más o menos 20.1 MiB</ins>, que es más o menos lo que ocupa una docena de fotos de tu últimas vacaciones.
  * Abre el archivo <ins datetime="2013-12-23T10:39:18+00:00"><code>python-3.3.3.msi</code></ins>. Windows te preguntará si estás seguro de que quieres ejecutar el archivo. Dile que sí.
  * Sale la ventana de Python y te dice que se va a instalar Python. Siguiente.
  * Te pide que elijas una carpeta. Déjalo como está y Siguiente.
  * Te ofrece la opción de personalizar la instalación. Déjalo como está y Siguiente: se va a instalar Python.
  * Se empiezan a copiar los nuevos archivos.
  * ¡Ya está! Dale a Finalizar.
  * Ahora ve a Inicio -> Todos los programas -> <ins datetime="2013-12-23T10:39:18+00:00">Python 3.3</ins>.
  * Aparecen otros submenús. Te interesa el que pone «IDLE (Python GUI)». Haz clic.
  * Ya estás en la línea de comandos del intérprete de Python listo para hablar [Pársel](http://es.wikipedia.org/wiki/P%C3%A1rsel).
  * El cursor estará parpadeando justo a la derecha de algo como esto: >>>.
  * Escribe el siguiente comando, asegurándote de que "¡Hola, mundo!" está entre comillas:

`>>>print("¡Hola mundo!")`

  * Presiona Enter. Deberías ver «¡Hola mundo!» en un color diferente en la línea inferior.
  * Si es así, ¡ya está!
  * Si ves un mensaje de error que dice: "SyntaxError: invalid syntax" entonces te has olvidado de las comillas. __*En versiones antiguas de Python (Python 2.x) no hacían falta paréntesis. Te recomendamos que aprendas Python 3, pero si quieres puedes instalar también Python 2.7 porque no todas las bibliotecas están disponibles en las nuevas versiones.*__

![python3](https://pybonacci.org/images/2013/12/python3.png?style=centerme)

Estás dentro de la ventana del IDE (Integrated Development Environment) IDLE. Deja el intérprete de Python abierto, listo y esperando recibir tus comandos. ¡Ahora sólo tienes que aprender Python! Para eso, tienes varios recursos. Algunos los hemos sacado de la [página de lengua española de la wiki oficial de Python](http://wiki.python.org/moin/SpanishLanguage), y otros del sitio de P&R [Python Majibu](http://python.majibu.org/preguntas/154/libros-recomendados-de-programacion-en-python).

  * En la Universidad Jaume I tienen publicado un curso de Python titulado «[Introducción a la programación con Python](http://www.uji.es/bin/publ/edicions/ippython.pdf)» [PDF] que cuenta con explicaciones muy detalladas y numerosos ejemplos.
  * En Mundo geek tienes «[Python para todos](http://mundogeek.net/tutorial-python/)», un libro escrito por Raúl González Duque y que puedes leer en PDF. También muy recomendable.
  * La comunidad de Python Argentina PyAr tradujo el [tutorial oficial de Python](http://docs.python.org.ar/tutorial/) a nuestro idioma.
  * Si te interesa aplicar Python en ciencia o ingeniería, tal vez te interese «[Introducción a Python para ingenieros](http://picachu.dmt.upm.es/python/)», apuntes incompletos escritos por Guillem Borrell en proceso de revisión. O este blog 😉

Cuando empieces a trabajar con el lenguaje y te surjan dudas, siempre puedes preguntar en el sitio de preguntas y respuestas [Python Majibu](http://python.majibu.org/), al estilo Stack Overflow.

**Si has llegado hasta aquí, ¿por qué no [nos cuentas qué te ha parecido el artículo](#commentform)? ¿Te ha ayudado a empezar con Python en tu sistema? ¿Ha ido todo bien o has tenido que cambiar algún paso? ¡[Déjanos un comentario](#commentform)! 🙂**

__*Nota: Actualizado el artículo para los nuevos tiempos: ahora instalamos Python 3 por defecto. ¡Ya va siendo hora! 😉*__

_Esta es una traducción y adaptación del artículo [Python On XP: 7 Minutes To “Hello World!”](http://www.richarddooling.com/index.php/2006/03/14/python-on-xp-7-minutes-to-hello-world/), por Richard Dooling. Thank you RD!_
