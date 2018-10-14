---
title: Joyas Python del 2015
date: 2015-12-28T19:42:54+00:00
author: Kiko Correoso
slug: joyas-python-del-2015

Este es un resumen de algunas joyas que he descubierto este 2015 dentro del mundo Python. Que las haya descubierto en el 2015 no significa que necesariamente sean cosas novedosas pero la mayoría siguen de actualidad. Tampoco es un resumen ordenado. de hecho, es un pequeño cajón de sastre. Tampoco es temático sobre ciencia, aunque la mayoría están relacionadas con ciencia ya que es a lo que me dedico. En las siguientes líneas nombro muchas cosas pero solo incluyo enlaces sobre las joyas de las que quiero hablar.

WEB:

  * En el pasado he trasteado algo con Django para hacer cosas que se puedan compartir con mucha otra gente. Django es un framework web muy completo o, como se suele decir, con baterías incluidas y el de más amplio uso dentro del mundo Python. El hecho de incluir tantas cosas de uso habitual en un desarrollo web es su fuerte para la mayoría de desarrolladores pero también su talón de Aquiles para gente que solo lo usa de vez en cuando para hacer cosas simples. Demasiado sobrecargado para acordarte de todo ello cuando lo usas muy eventualmente y demasiado condicionante para hacer cosas simples sin un guión claro. Es por ello que este año he empezado a trastear con [Flask](https://flask.pocoo.org/). Lo recomiendo para gente que quiere convertir una [idea simple](https://pybonacci.org/2015/12/01/aprende-historia-gracias-a-geocodificacion-inversa-mapping-y-wikipedia/) en [algo usable](https://map2wiki.runbear.webfactional.com/) en poco tiempo. He prestado algo de atención a [wagtail](https://wagtail.io/) y me gustaría encontrar un tutorial para gente especialmente lerda en desarrollo web (que no se lo vendan a un desarrollador Django, vamos) y que no tiene tiempo.
  * Relacionado con el trasteo anterior, he empezado a trastear también con [SQLAlchemy](https://www.sqlalchemy.org/). Como Flask no te aporta de serie su propia idea de ORM, como sí hace Django, puedes acoplar el ORM que elijas, usar SQL a capón, Mongo,... Facilita mucho el trabajo con BBDD. Y aquí puedes encontrar una serie de [recursos relacionados con SQLAlchemy](https://github.com/dahlia/awesome-sqlalchemy).
  * También relacionado con el uso de Flask, he estado trasteando con [Babel](https://babel.pocoo.org/) para internacionalizar 'cosas' (poder hacer uso de distintos idiomas). Es increible la facilidad de uso pero he encontrado ciertos problemas que no he sabido resolver (aun no sé muy bien porqué, seguramente mi poca experiencia con la biblioteca).

GRÁFICAS:

  * ¿Quieres hacer un mapa interactivo con Python? Hasta ahora había usado [mis propias soluciones](https://nbviewer.jupyter.org/github/kikocorreoso/brythonmagic/blob/master/notebooks/OpenLayers%20%28python%29%20tutorial.ipynb). Mis soluciones son fáciles de usar y fácilmente portables a la web de forma independiente pero requieren aprender, por ejemplo, OpenLayers o Leaflet y para hacer algo simple puede resultar excesivo. Pero para otros casos de uso hay otras soluciones que pueden resultar más convenientes. Es por ello que en los últimos tiempos he estado usando [Folium](https://github.com/python-visualization/folium). Es muy simple de usar y para según que necesidad es muy apropiado. Por otra parte, quizá su diseño limite un poco las posibilidades reales. Es por ello que, después de investigar un poco, descubrí [mplleaflet](https://github.com/jwass/mplleaflet). Esta última librería sigue la misma filosofía que mpld3, usa matplotlib y exporta el código en algo que es capaz de interpretar la librería javascript de turno (d3js para el caso de mpld3 o leaflet para el caso de mplleaflet). Las posibilidades de uso que se me ocurren para mplleaflet son muchas.
  * Otra joyita para hacer análisis estadístico y visualización es [Seaborn](https://stanford.edu/~mwaskom/software/seaborn/). Es una delicia ver como con tan poco se puede hacer tanto. Una capa sobre otra capa sobre otra capa,..., dan un gran poder con un mínimo esfuerzo. Se pierde poder de personalización pero se gana inmediatez y, en el mundo del 'loquieroparahoy', es una gran ventaja eso de la inmediatez.
  * Una pequeña tontería pero que te puede resultar útil en algún sistema donde es difícil usar un interfaz gráfico o quieres tener algo ligero para hacer gráficas de ¿baja calidad? sería [bashplotlib](https://github.com/glamp/bashplotlib) (hasta el nombre mola).
  * He empezado a trastear algo con [Plotly](https://plot.ly/python/) pero los resultados no han sido especialmente buenos (le tendré que dar una nueva oportunidad en 2016):

<blockquote class="twitter-tweet" width="550">
  <p lang="es" dir="ltr">
    arghh!! plotly me ha reventado un i7 con 16 gb de ram o_O Reiniciando...
  </p>
  
  <p>
    &mdash; Pybonacci (@Pybonacci) <a href="https://twitter.com/Pybonacci/status/667067498454458368">November 18, 2015</a>
  </p>
</blockquote>



UTILIDADES:

  * Una pequeña tontada para el día a día sería [tqdm](https://github.com/tqdm/tqdm), que te añade una barra de progreso a los bucles de tu código.

RENDIMIENTO:

  * La depuración y optimización de código siempre es algo árido y gris. La optimización prematura es la raiz de todo mal. Juntamos las churras con las merinas y nos sale que tienes que probar [line_profiler](https://github.com/rkern/line_profiler) sin ningún género de dudas. Date un paseo por tú código paso a paso y descubre qué es lo que está haciendo que tooooodo sea tan lento.
  * Para correr código más rápido en Python mis opciones de hoy en día serían, por orden de qué es lo que intentaría antes, [numba](https://numba.pydata.org/) (si es código científico) o [pypy](https://pypy.org/) (si solo uso numpy mezclado con cosas más estándar que no dependan de bibliotecas que usan la C-API de CPython). Si Numba no funciona y pypy no resuleve la papeleta valoro si el código lo voy a necesitar ejecutar muchas veces y el tiempo que tarda es inasumible en la mayoría de ocasiones y, si es así, tiro de [Cython](http://cython.org/) que, con un poco de esfuerzo y afeando un poco el código Python original, permite obtener velocidades cercanas a o del mismo orden que C/C++/Fortran.

LIBRERÍA ESTÁNDAR Y ALGUNAS ALTERNATIVAS:

  * De la librería estándar he estado usando bastante [argparse](https://docs.python.org/dev/library/argparse.html), [collections](https://docs.python.org/dev/library/collections.html) e [itertools](https://docs.python.org/dev/library/itertools.html). Los tres no tienen nada que ver, los tres son muy potentes y, sabiendo usarlos, los tres se hacen imprescindibles. Quizá para el año que viene me ponga como deberes mirar más a fondo [click](http://click.pocoo.org/dev/) como mejora a argparse y [functools](https://docs.python.org/3.6/library/functools.html), [toolz](https://github.com/pytoolz/toolz) y/o [CyToolz](https://github.com/pytoolz/cytoolz/) en combinación con collections e itertools.

AÑO 2016 (DEBERES QUE ME PONGO):

  * [dask](https://github.com/blaze/dask)
  * Más [PyTables](https://github.com/PyTables/PyTables).
  * Creo que le voy a dar bastante más a [d3js](http://d3js.org/) (por dictadura del navegador).
  * [scikit-extremes](https://github.com/kikocorreoso/scikit-extremes), mi propia solución al análisis de extremos univariantes en Python (se aceptan ayudas).
  * [PyMC](https://github.com/pymc-devs/pymc) y/o [PyMC3.](https://github.com/pymc-devs/pymc3)

¿Y vuestras joyitas? Animáos a compartirlas en los comentarios, independientemente que estén relacionadas con ciencia o no.

Saludos y feliz año!!
