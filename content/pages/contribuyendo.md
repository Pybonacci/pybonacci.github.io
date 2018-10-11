title: ¿Cómo contribuir?
slug: como-contribuir
Template: page

# Normas básicas de convivencia en esta comunidad.

Quieres contribuir a Pybonacci, ¡genial!, pero antes de contribuir necesitamos
comentar una serie de normas básicas de convivencia de esta comunidad.

En general, nos adherimos al espíritu del [códido de conducta](http://documentos-asociacion.es.python.org/c%C3%B3digo%20de%20conducta.html#id1) elaborado por la [asociación Python España](https://es.python.org/pages/asociacion.html). Esto
significa que valoramos mucho más la comunidad que aportaciones individuales. Se espera que una comunidad fuerte sea respetuosa y un lugar divertido y seguro en el que estar. Si somos capaces de conseguir una comunidad diversa y con buena salud, esta misma comunidad sería capaz de soportar Pybonacci durante más tiempo, más allá de personas concretas que pueden estar yendo y viniendo. Para cualquier tipo de comunicación (normalmente escrita):

* Piensa que otros van a estar más de acuerdo que en desacuerdo con lo que comentes. Tendemos a olvidar lo que nos une, que es mucho, y a enfocarnos en unas pocas diferencias.
* Cuando tengas alguna duda, asume que estás malinterpretando algo y pide de forma amable que te confirmen que lo que has entendido es lo correcto.
* Cuando escribas asume que cada frase será malinterpretada. Revísa el texto y trata de reformularlo de la forma más clara posible.
* Si estás muy en desacuerdo con algún comentario (en un Pull Request, en el issue tracker, en twitter, en un correo,...), etiquétalo como importante y déjalo de lado. Léelo después de unas cuantas horas y vuelve a dejarlo de lado. Al día siguiente vuelve a leerlo y, en ese momento, será más fácil escribir algo pensado y calmado que la respuesta encendida inicial. De esta forma será más fácil ver que podemos llegar a trabajar 'con' en lugar de 'en contra de'.

# Formas de contribuir a Pybonacci.

La forma más evidente es escribiendo artículos pero no es la única. Además de:

* [Escribir artículos](#articulo).

También podrías:

* [Hacer de Guía para otros](#guia).
* [Ayudar con aspectos técnicos del sitio](#tecnico).
* [Ayudar en la comunicación](#comunicacion).
* [Ayudar en la edición](#editor).
* [Ayudar en la administración del sitio y de la comunidad](#admin).
* ...

<h1><a name="articulo">Escribir un articulo.</a></h1>

Pybonacci es un esfuerzo colaborativo entre personas de diversas industrias y ámbitos. Esto quiere decir que si crees que tienes algo interesante que aportar, seguro que podemos aprender de ti y nos encantará añadir tu artículo al blog.

Los artículos se añaden al blog mediante Pull Request al repositorio (a la rama `sources`, es la rama por defecto) con el tag `[ARTICULO]` (¿no tienes ni idea de lo que significa nada en esta frase? Quizá necesitas una [Guía](#guia)). 

Lo primero que habrá que hacer es un fork del repositorio mediante:

```
git clone url_a_tu_fork 
```

donde `url_a_tu_fork` será algo como `https://github.com/kikocorreoso/pybonacci.github.io.git`.

Los artículos pueden estar en dos formatos:

**Formato 1. Markdown**
[Pelican](#faq-pelican) soporta el formato [Markdown](#faq-markdown), que es un formato que amplía el texto plano con diversas capacidades. [Aquí](https://markdown.es/) hay una guía muy buena sobre como escribir en Markdown.

Los artículos en markdown tienen que estar en la carpeta `content\articles`

**Formato 2. Jupyter Notebook**
[Pelican](#faq-pelican) soporta el renderizado de [Jupyter Notebooks](#faq-jupyter) directamente. Para ello, hay que enviar 2 archivos en la [pull request](#guia).

- El archivo `ipynb` del notebook, guardado en la carpeta `content\downloads\notebooks\`

- Un archivo de markdown `formato .md` guardado en la carpeta `content\articles` con la siguiente estructura:

```
---
title: El título del artículo (por ejemplo "Las 5 ecuaciones mas sexys")
date: la fecha de escritura en formato "2015-01-05T11:19:00+00:00"
author: El nombre del autor (por ejemplo, Kiko Correoso)
slug: string de referencia del articulo (por ejemplo, "las-5-ecuaciones-mas-sexys")
tags: lista de tags separadas por comas (por ejemplo,  "tag1, ecuaciones diferenciales no balanceadas, python 3")

{% notebook downloads/notebooks/nombre_del_archivo_ipynb.ipynb cells[:] %}
```

[Aquí](https://github.com/Pybonacci/pybonacci.github.io-source/pull/9/files) se puede ver un ejemplo de Pull Request.

**Si es tu primera aportación al blog** seguramente no tengas una página de Autor. para crear una puedes seguir [estos ejemplos](https://github.com/Pybonacci/pybonacci.github.io/tree/sources/theme/templates/author) y llamarla con el mismo nombre que hayas usado para el autor del artículo (sección `author` más arriba) con un guión en cada espacio. Por ejemplo, si el autor del artículo lo has puesto así:

```
# ...
author: Pepe Gotera
# ...
```

La plantilla a colocar en https://github.com/Pybonacci/pybonacci.github.io/tree/sources/theme/templates/author deberá llamarse Pepe-Gotera.html

Si quieres añadir una imagen la deberás incluir en https://github.com/Pybonacci/pybonacci.github.io/tree/sources/content/images/author y enlazarla de forma correcta en la plantilla de autor. Mira los ejemplos que ya existen en https://github.com/Pybonacci/pybonacci.github.io/tree/sources/theme/templates/author.

[Aquí](https://github.com/Pybonacci/pybonacci.github.io/pull/64/files) se puede ver un ejemplo de Pull Request.

<h1><a name="guia">Hacer de guía</a></h1>

Guía será una persona que guiará a otros. Las personas guiadas serán aprendices, por llamarlos de alguna forma, y solo tienen que desear contribuir con su conocimiento a Pybonacci escribiendo algún artículo. Estos aprendices no tienen los conocimientos técnicos para manejar un sistema de control de versiones, manejar un notebook, no entienden muy bien como funciona Markdown,..., y el Guía se encargará de ayudarlos para que sean capaces de aportar a la comunidad.

Cualquier persona que lo desee y tenga las conocimientos necesarios puede ser Guía y puede hacerlo una única vez o tantas veces como quiera.

Si crees que necesitas una Guía puedes abrir un [issue añadiendo el prefijo `[GUÍA]` en el título del issue](https://github.com/Pybonacci/pybonacci.github.io/issues) o nos puedes mandar un <a href="mailto:contacto@pybonacci.org">correo</a> añadiendo en el asunto el prefijo `[GUÍA]`.

<h1><a name="tecnico">Mejorar el blog</a></h1>

La versión actual del proyecto usa [Pelican](#faq-pelican) para generar el contenido estatico. ¿Quieres mejorar el css, añadir plugins que creas que nos podrian ayudar? ¡Se admiten Pull Requests!

<h1><a name="comunicacion">Canales de comunicación</a></h1>

¿Tienes interés en ayudarnos a comunicar mejor todo lo que hacemos? Dale bombo a nuestra cuenta de twitter ([@pybonacci](https://twitter.com/pybonacci)). Enlaza a nuestros contenidos o proporciónanos ideas para mejorar en este aspecto.

<h1><a name="editor">¿Quieres ser editor?</a></h1>

¡Genial! Cuantos más seamos mejor. La manera de convertirse en editor es publicar al menos 3 artículos. Esta es una norma arbitraria para medir tu compromiso. Si se te ocurren mejoras formas háznoslo saber.

<h1><a name="admin">Administradores</a></h1>

Este sitio está administrado por (en orden alfabético):

* Juan Luís Cano
* Kiko Correoso
* Manuel Garrido
* Álex Saez

No tenemos claro como puedes convertirte en administrador de la comunidad pero te podemos comentar como hemos llegado a tener los administradores que tenemos. Juanlu y Kiko son fundadores del proyecto por lo que son administradores. En el caso de Manuel y Álex, después de un tiempo de gran implicación en el proyecto, se han convertido en administradores.

Los principales beneficios que obtienen los administradores son:

* Correr con los gastos que genera el sitio.
* Trabajar mucho.
* Tener más dolores de cabeza.

Con el tiempo cualquiera podría llegar a obtener estos beneficios.

# Notas sobre estilo

**Renderizado de codigo en artículos Markdown**
Pelican soporta *syntax highlight* en Markdown. Para ello hay que indentar los bloques de código con 4 espacios. Además, podemos indicar el lenguaje del código añadiendo `:::lenguaje` al inicio del bloque.

Por ejemplo, para que en un artículo se renderice un bloque de código de python se haría de la forma:

```
    :::python
    import this
    print("Hello World")
```

# Sobre la temática y complejidad de los artículos.

La gente que ha ido escribiendo en Pybonacci son físicos, ingenieros aeronáuticos, ingenieros informaticos, científicos de datos,... Obviamente no somos capaces de cubrir todas las temáticas. Échamos de menos artículos de biología, química, ciencias sociales, periodismo de datos, visualización, medicina,...

Los articulos pueden tener cualquier extensión, desde una [microentrada](https://www.pybonacci.org/tag/microentradas.html) que cuente algo puntual que te resulta interesante y que crees que no todo el mundo conoce, hasta un [macrotutorial](https://www.pybonacci.org/tag/tutorial-matplotlibpyplot.html) que contenga varias entradas, pasando por artículos típicos donde entramos en algo de detalle sobre un tema y cuyo objetivo es que sea algo introductorio.

Como lo de que sea algo introductorio es algo bastante ambiguo cualquier nivel vale puesto que el blog lo pueden leer desde expertos hasta niños que están empezando a interesarse por la tecnología y la ciencia. Por tanto, si sufres del síndrome del impostor supéralo porque siempre serás un experto para alguien más inexperto o que proviene de otros campos diferentes al tuyo. 

# Sobre la aceptación de artículos.

En Pybonacci creemos que cualquier persona que tenga ganas de compartir su conocimiento y que haga el (a veces gran) esfuerzo de escribir un artículo merece ser publicada.
No obstante, también debemos garantizar una cierta calidad en el blog. Por ello, una vez se ha creado una Pull Request para enviar un artículo dicho artículo deberá ser validado por al menos 2 editores y es posible que estos editores te pidan que cambies alguna cosa para que el resultado final sea mejor.

<h1><a name="faq">FAQ</a></h1>

<h1><a name="faq-pelican">Pelican</a></h1>

Pelican es la herramienta que usamos para generar el contenido. Es un generador estático de contenido. Normalmente, si no colaboras en tareas de administración o mantenimiento y mejora del sitio no es necesario que sepas mucho más sobre Pelican. Si aún así tienes interés puedes visitar el [sitio oficial](https://blog.getpelican.com/).

<h1><a name="faq-markdown">Markdown</a></h1>

Markdown es el lenguaje que usamos para escribir artículos. Es un lenguaje sencillo que nos permite hacer añadir ciertos formatos de forma sencilla. [Aquí](https://markdown.es/) hay una guía muy buena sobre como escribir en Markdown. Si aún así te resulta complejo puede que necesitas una [Guía](#guia).

<h1><a name="faq-jupyter">Jupyter Notebook</a></h1>

Una forma alternativa de escribir artículos en esti sitio es usando el notebook de Jupyter. Es una forma muy popular de escribir código "literaturizado", es decir, podemos escribir código mezclado con texto e imágenes de forma que sea más fácil de digerir. La página oficial del proyecto Jupyter la puedes encontrar [aquí](http://jupyter.org/).
