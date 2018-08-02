---
title: Curso de Python en la ETSIAE: 4ª edición
date: 2015-10-15T12:05:25+00:00
author: Juan Luis Cano
slug: curso-de-python-en-la-etsiae-4a-edicion
tags: #aeropython, curso, etsiae, python

¡Ya vamos a por la **cuarta edición de nuestro curso de Python para aeronáuticos**! Esta vez durará <del datetime="2015-10-25T22:10:48+00:00">15</del><ins datetime="2015-10-25T22:10:48+00:00">12</ins> horas y este es el temario:

  1. Introducción a la sintaxis de **Python**
  2. Uso del Notebook de **IPython**
  3. Arrays de **NumPy**
  4. Representación gráfica con **matplotlib**
  5. Análisis numérico con **SciPy**
  6. Cálculo simbólico con **SymPy**

![](http://pybonacci.org/images/2015/10/cartel-213x300.png)

El curso se desarrollará en la **sala II del centro de cálculo de la ETSI Aeronáutica y del Espacio** de <del datetime="2015-10-25T22:05:45+00:00">17:30</del><ins datetime="2015-10-25T22:05:45+00:00">18:00</ins> a 20:00 a lo largo de **dos semanas**, los días 3, 4, 5, 10, 11 y 12.

<!--more-->

<ins datetime="2015-10-29T17:07:38+00:00">La inscripción se ha cerrado.</ins> ¡Estad atentos vuestro email institucional estos días!

Lo impartiremos conjuntamente el equipo AeroPython y estará pensado para que sea un curso eminentemente práctico, con ejemplos extraídos de asignaturas de la carrera. Con los conocimientos básicos de programación que se imparten en la carrera es suficiente: no vamos a explicar qué es un bucle y un condicional, pero con haber escrito alguno en Fortran o MATLAB es suficiente 😉

## Bases del sorteo

Aquellas personas que ya hayan solicitado el curso de Python en ocasiones anteriores obtendrán plaza automáticamente. El resto se asignarán de esta forma:

El jueves, después del cierre del plazo de inscripción, se enviará a los inscritos un número que corresponderá con su orden de inscripción. [El número del Cuponazo de la ONCE del viernes 30 de octubre](https://www.juegosonce.es/resultados-cuponazo-30-octubre-2015) se dividirá por el número de inscritos, y el resto será tomado como punto de partida para asignar las 45 plazas correlativamente.

## Admitidos

[El número del Cuponazo de la ONCE del viernes 30 de octubre](https://www.juegosonce.es/resultados-cuponazo-30-octubre-2015) es el **33328**.

    :::python
    &gt;&gt;&gt; N = 33328
    &gt;&gt;&gt; plazas = 34
    &gt;&gt;&gt; inscritos = 42
    &gt;&gt;&gt; N % inscritos
    22
    &gt;&gt;&gt; admitidos = [((N % inscritos) + ii) % inscritos for ii in range(plazas)]
    &gt;&gt;&gt; admitidos
    [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

## Preguntas frecuentes

### ¿Vais a subir los materiales del curso?

¡Sí! Los podéis encontrar en <https://github.com/AeroPython/Curso_AeroPython> (o <http://bit.ly/notebooksaeropython>).

### ¿Lo vais a grabar en vídeo?

Estas cosas son más complicadas de lo que parecen y además el curso será muy práctico, así que no lo creo. Si queréis un curso de Python en vídeo y en español, echad un vistazo a [Introducción a Python para científicos e ingenieros](http://bit.ly/curso-python-vid):



### ¿Qué versión de Python se va a utilizar en el curso?

El curso se hará con **Python 3.4**, y utilizaremos el intérprete IPython que viene con la distribución Anaconda.

  * Podéis ver el [vídeo demo de 5 minutos que grabamos sobre IPython](http://youtu.be/C0D9KQdigGk).
  * Podéis [instalar Anaconda en vuestro ordenador](http://continuum.io/downloads), es totalmente gratis y sin restricciones y funciona en Windows, OS X y Linux por igual. Es la mejor forma de tener todos los paquetes necesarios.

### ¿Podré seguir el curso si nunca he cursado programación?

Python es el lenguaje de programación más fácil de aprender que existe. Con todo y con eso, hay un par de conceptos que pueden resultar un poco novedosos o chocantes y, aunque se captan en seguida, conviene que no se vean la primera vez en el curso porque no nos podemos detener a explicarlos. En la primera edición tuvimos gente que nunca había programado y se adaptó bastante bien; otros tuvieron que abandonar.

### ¿Puedo llevar portátil?

Sí 🙂 El curso se dará en las aulas de informática, pero si queréis traer vuestro portátil naturalmente lo podéis hacer. Tan solo tenéis que traer Anaconda instalado. Lo bueno de llevar vuestro portátil es que podréis seguir con el trabajo en casa.

### ¿Cómo instalo Anaconda?

Solo tienes que acceder a la [página de descargas de Anaconda](http://continuum.io/downloads), escoger vuestro sistema operativo y descargar la versión de Python 3.4. Si aun así no podéis, esperad a venir al curso, traed vuestro portátil y os ayudaremos.

### ¿Hay que pagar matrícula?

<del datetime="2015-10-25T16:12:42+00:00">Sí, el curso tiene un coste de 10 € de los cuales 3 € son para el fondo de mecenazgo de Delegación de Alumnos, para ayudar a estudiantes sin recursos.</del>

<ins datetime="2015-10-25T16:12:42+00:00">No, la inscripción del curso será gratuita.</ins>

### ¿Se darán créditos?

Lamentablemente tampoco podremos dar créditos en esta ocasión.

* * *

Para cualquier duda que tengáis podéis usar los comentarios, [nuestra lista de correo](https://groups.google.com/forum/#!forum/aeropython) o [escribirnos por Twitter](http://twitter.com/AeroPython).

¡Un saludo! 😉