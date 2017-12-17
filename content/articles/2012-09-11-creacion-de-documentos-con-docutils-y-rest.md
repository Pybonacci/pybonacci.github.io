---
title: Creación de documentos con Docutils y reST
date: 2012-09-11T13:14:52+00:00
author: Juan Luis Cano
slug: creacion-de-documentos-con-docutils-y-rest
tags: documentación, docutils, python, rest

## Introducción

Hoy vamos a ver una introducción a cómo **crear documentos** utilizando **Docutils** y el lenguaje de marcado **reStructuredText**, o simplemente **reST**. [El proyecto Docutils](http://docutils.sourceforge.net/) nació en la década de los años 2000 como parte del esfuerzo para [mejorar la documentación del lenguaje Python](http://docutils.sourceforge.net/docs/ref/rst/introduction.html#history), y en los últimos años tanto el lenguaje reST como las herramientas para procesarlo se han convertido en una manera excelente no sólo de documentar proyectos en Python, sino también en otros lenguajes o para escribir documentos que nada tienen que ver con la programación.

Docutils es compatible con Python 2.4 en adelante y funciona en Windows, Mac OS X y Linux. Para instalarlo en cualquiera de estos sistemas operativos, no tienes más que seguir el procedimiento habitual para instalar paquetes Python:

  1. Descargar el código fuente desde [la web de Docutils](http://sourceforge.net/projects/docutils/files/docutils/) y extraerlo.
  2. Escribir desde un terminal `python setup.py install`. Este paso puede requerir privilegios de administrador.

## El lenguaje reST

El lenguaje [reStructuredText](http://docutils.sourceforge.net/rst.html) o reST es un lenguaje de marcado de texto plano flexible y potente. reST tiene las ventajas de otros lenguajes de marcado de texto plano similares como Markdown, como puede ser la **portabilidad**: en cualquier sistema operativo y con cualquier editor de texto básico puedes abrir y modificar archivos de texto plano. Pero además, reST tiene otra serie de características que otros no tienen:

  * Es **extensible**: en reST puedes definir tus propios roles y directivas, de tal forma que puedes automatizar estructuras que utilices con frecuencia.
  * Está **integrado con** $LaTeX$: utilizando la directiva y el rol `math`, puedes incluir fácilmente ecuaciones matemáticas en tus documentos. Esto nos viene muy bien a los científicos e ingenieros 😉
  * Se puede exportar a **múltiples formatos**: HTML, $LaTeX$, man, ODT, XML, S5... y si lo necesitas se puede adaptar para exportarlo al formato que desees (como por ejemplo [HTML5](https://github.com/marianoguerra/rst2html5)).

Uno de los objetivos de reST es que sea **legible**. La manera de marcar los encabezados y las secciones del documento hace que alguien que no conozca el lenguaje pueda leer perfectamente el contenido. Vamos a ver algunos ejemplos.

<!--more-->

## Nuestro primer documento reST

Vamos a crear un archivo llamado `intro_rest.rst` (normalmente esta será la extensión que utilicemos) y vamos a escribir este código:

    Docutils
    ========
    El programa Docutils (http://docutils.sourceforge.net/) es un sistema de
    procesamiento de texto escrito en Python, que puede pasar ficheros escritos en
    el lenguaje reStructuredText (reST, http://docutils.sourceforge.net/rst.html)
    a HTML, LaTeX y más formatos.
    ¿Por qué reST?
    --------------
    La gracia de escribir reST en lugar de LaTeX o incluso de utilizar un editor
    tipo LyX es que
    * Es muy *visual*
    * Es **texto plano** (igual que LaTeX o un programa Fortran) así que no hay
      problemas de formatos binarios, incompatibilidades... es igual en todas partes.
    Lo anterior es una lista en reST. Fíjate también en la cursiva y en la negrita.
    En LaTeX habría que escribir::
      begin{itemize}
      item Es muy emph{visual}
      item Es textbf{texto plano} [...]
      end{itemize}
    Conclusión
    ----------
    Si es verdad que se cumple
    .. math::
      E = m c^2
    entonces no hay más que hablar: es hora de aprender reST. Para generar un
    documento a partir de este texto, solamente hay que ejecutar en un
    terminal::
      $ rst2html intro_rest.rst intro_rest.html
    Y fin de la cuestión.

En este pequeño documento están recogidas las estructuras básicas que usaremos con más frecuencia. Aún no lo hemos convertido en HTML, LaTeX u otro formato, pero aun así nos damos cuenta de que lo podemos leer perfectamente. Si ahora en un terminal ejecutamos, tal y como se recoge en el mismo texto

    $ rst2html intro_rest.rst intro_rest.html

Se genera algo muy similar a esto:<figure id="attachment_808" style="width: 560px" class="wp-caption aligncenter">

[<img class=" wp-image-808 " title="Archivo HTML generado por Docutils" alt="" src="http://pybonacci.org/wp-content/uploads/2012/09/intro_rest.png" width="560" height="526" srcset="https://pybonacci.org/wp-content/uploads/2012/09/intro_rest.png 774w, https://pybonacci.org/wp-content/uploads/2012/09/intro_rest-300x282.png 300w" sizes="(max-width: 560px) 100vw, 560px" />](http://pybonacci.org/wp-content/uploads/2012/09/intro_rest.png)<figcaption class="wp-caption-text">Archivo HTML generado a partir del fichero reST por Docutils</figcaption></figure> 

Y si queremos generar un PDF y tenemos instalado LaTeX, no hay más que ejecutar

    $ rst2latex intro_rest.rst intro_rest.tex
    $ pdflatex intro_rest.tex

Y se obtiene [este archivo PDF](http://pybonacci.org/wp-content/uploads/2012/09/intro_rest.pdf).

¿No es una maravilla? 🙂 Vamos a analizar con un poco más de detalle las estructuras que hemos usado. No pretendo dar una referencia completa del lenguaje reST, si quieres puedes consultar la [referencia oficial](http://docutils.sourceforge.net/docs/user/rst/quickref.html).

### Encabezados

Como se puede ver, los encabezados se delimitan con una línea de caracteres simbolizando una especie de subrayado. En este caso hemos utilizado `===` para el título del documento y `---` para las secciones de primer nivel, pero hay muchas combinaciones posibles. Los caracteres disponibles para delimitar las secciones son muchos, pero los recomendados son, [como indica la documentación del lenguaje](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections),

<pre>= - ` : . ' " ~ ^ _ * + #</pre>

El caracter que escojamos para el primer encabezado del documento se asignará al **título**, el segundo a las secciones de primer nivel, el tercero a las de segundo nivel y así sucesivamente.

### Enlaces

En el documento que hemos creado simplemente hemos escrito una URL y esta se ha convertido en un hipervínculo en el caso del fichero HTML y en un enlace en el caso del PDF. Pero también podemos hacer que el texto del enlace sea distinto a una URL, utilizando la siguiente sintaxis:

    Ve a la web de Python_ para más información.
    `Escríbenos con tus comentarios`_ en el formulario.
    .. _Python: http://www.python.org
    .. _`Escríbenos con tus comentarios`: jdoe@example.com

### Formato y listas

Esto es sencillo: el texto en cursiva _\*se marca entre asteriscos\*_, y en negrita **\*\*se marca con doble asterisco\*\***. Las listas, por otro lado, se crean con una serie de puntos que se pueden marcar con los caracteres

<pre>* + - • ‣ ⁃</pre>

aunque lo más normal suele ser usar el asterisco `*` o el símbolo de suma `+`.

### Bloques literales y código fuente

Para incluir bloques literales o código fuente, el bloque debe estar sangrado dos espacios y la línea que lo precede debe estar terminada con un doble signo de dos puntos `::`.

### Matemáticas y bloques especiales

En el ejemplo que hemos puesto hemos visto cómo utilizar la directiva math. Las directivas en reST son bloques especiales marcados con una sintaxis particular. El contenido del bloque también va sangrado dos espacios. Hay varios tipos que se usan frecuentemente:

    Bloque para fórmulas matemáticas:
    .. math::
      E = m c^2
    Bloques para notas y avisos:
    .. note::
      Esto es una nota.
    .. warning::
      Más vale que tengas cuidado.

<ins datetime="2012-09-12T07:51:23+00:00"><strong>Edición</strong>: Por último</ins>, para aquellos que han llegado hasta el final, Kiko nos enlaza en los comentarios una [chuleta de reST](https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.pdf?raw=true) hecha por el gran Roberto Alsina ([@ralsina](http://twitter.com/ralsina)).

Espero que te haya resultado útil el artículo y que nos cuentes en los comentarios si has tenido algún problema o si, por el contrario, te hemos descubierto un mundo nuevo. Yo empecé a tomar mis apuntes de clase a ordenador utilizando Docutils (incluyendo fórmulas) y, si tienes una buena velocidad de escritura, los resultados son más que satisfactorios.

¡Un saludo!