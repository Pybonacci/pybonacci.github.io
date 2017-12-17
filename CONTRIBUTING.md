# Como contribuir a Pybonacci

## Escribir un articulo.

Pybonacci es un esfuerzo colaborativo entre personas de diversas industrias y ámbitos. Esto quiere decir que si crees que tienes algo interesante que aportar, seguro que podemos aprender de ti y nos encantará añadir tu artículo al blog.

Los artículos se añaden al blog mediante Pull Request al repositorio (a la rama `sources`, es la rama por defecto) con el tag `[ARTICULO]`. Los artículos pueden estar en dos formatos:

**Formato 1. Markdown**
Pelican soporta el formato Markdown, que es un formato que amplía el texto plano con diversas capacidades. [Aquí](https://markdown.es/) hay una guía muy buena sobre como escribir en Markdown.

Los artículos en markdown tienen que estar en la carpeta `content\articles`

**Formato 2. Jupyter Notebook**
Pelican soporta el renderizado de Jupyter Notebooks directamente. Para ello, hay que enviar 2 archivos en la pull request.

- El archivo `ipynb`del notebook, guardado en la carpeta `content\downloads\notebooks\`

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

## Mejorar el blog

La versión actual del proyecto usa Pelican para generar el contenido estatico. Quieres mejorar el css, añadir plugins que creas que nos podrian ayudar? Se admiten Pull Requests!


# Notas sobre estilo

**Renderizado de codigo en artículos Markdown**
Pelican soporta syntax highlight enn Markdown. Para ello hay que indentar los bloques de código con 4 espacios. Ademas, podemos indicar el lenguaje del código añadiendo `:::lenguaje` al inicio del bloque.

Por ejemplo, para que en un artículo se renderice un bloque de código de python se haría de la forma:

```
    :::python
    import this
    print("Hello World")
```

## Sobre la aceptación de artículos.

En Pybonacci creemos que cualquier persona que tenga ganas de compartir su conocimiento y que haga el (a veces gran) esfuerzo de escribir un artículo merece ser publicada.
No obstante, también debemos garantizar una cierta calidad en el blog. Por ello, una vez se ha creado una Pull Request para enviar un artículo dicho artículo deberá ser validado por al menos 2 editores.

## ¿Quieres ser editor?

¡Genial! Cuantos más seamos mejor. La manera de convertirse en editor es publicar al menos 3 artículos.
