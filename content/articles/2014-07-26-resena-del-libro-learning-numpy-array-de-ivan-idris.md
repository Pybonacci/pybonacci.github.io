---
title: Reseña del libro &#8220;Learning NumPy Array&#8221; de Ivan Idris
date: 2014-07-26T11:11:34+00:00
author: Juan Luis Cano
slug: resena-del-libro-learning-numpy-array-de-ivan-idris

El otro día me contactaron desde la editorial Packt Publishing y me propusieron **hacer una reseña del libro "Learning NumPy Array", de Ivan Idris**, y no solo me regalaron la versión electrónica sino que encima me enviaron una copia física y **me propusieron hacer un concurso para los lectores**. ¡Genial! 🙂

Desde aquí agradezco su cordialidad y simpatía a la gente de Packt, y os dejo sin más dilación con la reseña del libro. Del concurso hablamos más abajo 😉

<blockquote class="twitter-tweet" width="550">
  <p>
    Ya nos ha llegado el libro "Learning NumPy Array", gracias <a href="https://twitter.com/PacktPub">@PacktPub</a>! <a href="http://t.co/CHljyGIfzS">pic.twitter.com/CHljyGIfzS</a>
  </p>
  
  <p>
    &mdash; Pybonacci (@Pybonacci) <a href="https://twitter.com/Pybonacci/statuses/489836965358227456">July 17, 2014</a>
  </p>
</blockquote>



> "Learning NumPy Array" es un libro escueto que va directo al grano, utilizando las versiones más modernas de todas las bibliotecas y muy instructivo. Sin embargo, puede sorprenderte por el nivel de matemáticas requerido y porque usa una multitud de paquetes más aparte de NumPy. Le doy un 3.5/5.

Si estás interesado como yo en empezar a hacer análisis de datos con Python y has oído hablar de pandas o StatsModels pero no sabes por qué los necesitas o cómo usarlos, este libro te va a gustar.

El capítulo 1 empieza desde el principio y explica cómo instalar Python, NumPy y el resto de paquetes necesarios en Windows, Linux y Mac OS X (este último es el sistema operativo usado por el autor), e incluso da instrucciones de cómo compilar el código fuente. A continuación abre el apetito del lector escribiendo un programa muy simple en Python haciendo uso de los arrays de NumPy.

<!--more-->

El capítulo 2 es una introducción a NumPy que abarca desde los conceptos más primitivos (arrays, tipos de datos) hasta operaciones muy sofisticadas como la indexación avanzada, [la expansión (_broadcasting_)](http://pybonacci.org/2012/06/07/algebra-lineal-en-python-con-numpy-i-operaciones-basicas/ "Álgebra Lineal en Python con NumPy (I): Operaciones básicas") o incluso el uso de _strides_, pasando por manipulación de arrays, distinción entre vistas y copias y mucho más. Al terminar el capítulo se tiene una visión bastante completa de la potencia de los arrays de NumPy y sus métodos.

Los capítulos 4, 5 y 6 son el cuerpo central del libro y tratan de cómo hacer análisis de datos con NumPy. En ellos se introducen numerosos conceptos matemáticos y estadísticos, y en ocasiones se echa mano de bibliotecas como pandas, SciPy o StatsModels. Por supuesto todas las gráficas del libro están hechas con [matplotlib](http://pybonacci.org/2012/05/14/manual-de-introduccion-a-matplotlib-pyplot-i/ "Manual de introducción a matplotlib.pyplot (I): Primeros pasos"). El capítulo 4 comienza analizando datos meteorológicos disponibles en abierto para después explorar varias técnicas de análisis predictivo en el capítulo 5 y hacer una introducción al análisis de series temporales (filtrado, suavizado...) en el capítulo 6.

Por último, en el capítulo 7 trata de cómo depurar programas en Python, analizar su rendimiento (_profiling_) y [escribir tests para mejorar la robustez de nuestros programas](http://pybonacci.org/2013/01/07/desarrollo-dirigido-por-pruebas-en-python-i-una-historia-que-pasa-todos-los-dias/ "Desarrollo dirigido por pruebas en Python (I): Una historia que pasa todos los días"). Sin duda se agradece que estos temas tan importantes aparezcan tratados en el libro. En el capítulo 8 se mencionan brevemente otras bibliotecas del ecosistema Python científico: SciPy para integración numérica e interpolación, Cython para acelerar el código, scikit-learn para hacer [agrupamiento (_clustering_)](http://pybonacci.org/2012/11/18/analisis-cluster-i-introduccion/ "Análisis cluster (I): Introducción") y finalmente se hace una sorprendente mención a Blaze como el futuro de NumPy.

Todos los capítulos traen numerosos ejemplos de código y gráficas, aunque en mi opinión el contexto o el programa en sí a veces necesitarían explicaciones más detalladas. El código además se puede descargar de la web de la editorial. Sin duda la mejor manera de aprovechar el libro es tenerlo junto al ordenador e ir explorando los conceptos a medida que se vayan aprendiendo.

Me sorprendió que a pesar del título realmente se utilizasen otras muchas bibliotecas del ecosistema Python científico, algo que no se menciona tampoco en la contraportada. Me he tomado la libertad de crear un [archivo de dependencias para instalar todos los paquetes necesarios](https://gist.github.com/Juanlu001/c0166f6a62f5bbb1ee0e).

La instalación de paquetes en Python es siempre un asunto delicado (aunque cada vez menos, afortunadamente), y tengo que decir que no estoy de acuerdo con el criterio elegido por el autor. Mi recomendación personal sería ignorar el gestor de paquetes del sistema operativo (si lo tiene) y utilizar algunas de las muchas distribuciones portables de Python que existen, ya que la experiencia es la misma en todos los sistemas. Para mí las mejores son, sin duda, Anaconda y Pyzo (esta última incluso se puede usar desde un lápiz USB, poniendo fin a los clásicos problemas de privilegios de instalación). Y como gestor de paquetes, sin duda conda es mucho mejor que pip en nuestro contexto, puesto que descarga paquetes binarios en todas las plataformas y gestiona las dependencias de manera más efectiva.

El libro da una visión muy rica de cómo hacer análisis de datos con Python, pero el lector debe conocer no solo el lenguaje, sino también los conceptos estadísticos y matemáticos utilizados. En la línea de [otros libros que he leído de Packt](http://www.amazon.es/review/R2Y5PRV82ZRKU3/ref=cm_cr_pr_perm?ie=UTF8&ASIN=1849514461), las largas explicaciones teóricas brillan por su ausencia y el texto va directamente al grano. Si ya has hecho análisis de datos en otros lenguajes o tienes la formación adecuada sin duda disfrutarás del libro; si no, es posible que te pierdas en algunas partes.

Lo que más me ha gustado de "Learning NumPy Array" es el hecho de que utilice NumPy para analizar los datos, porque de esta forma se ven rápidamente sus limitaciones a la hora de tratar con datos heterogéneos o datasets incompletos y se justifica sobradamente el uso de [pandas](http://pybonacci.org/2014/05/30/pandas-i/ "Pandas (I)"). Si alguna vez te has preguntado para qué necesitas pandas si tienes NumPy, este es tu libro.

En definitiva, una lectura interesante que sin duda resultará útil a muchos, directa al grano y con muchos ejemplos de código.

* * *

¿Te ha interesado la reseña? **¿Te gustaría ganar la copia electrónica que Packt Publishing sortea para los lectores de Pybonacci?** Solo tienes que echar un vistazo en http://www.packtpub.com/learning-numpy-array/book, donde puedes también descargar un capítulo de ejemplo del libro, y dejarnos un comentario diciendo qué es lo que más te interesa del libro.

El plazo termina el 15 de agosto de 2014 a las 00:00, y entre los mejores comentarios haremos un sorteo riguroso y avisaremos al ganador por email. ¡Mucha suerte y muchas gracias por leer! 🙂

&nbsp;