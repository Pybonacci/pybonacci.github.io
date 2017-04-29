---
title: Analizando datos sobre el Brexit con Pandas
date: 2016-07-11T15:38:31+00:00
author: Bob Belderbos
slug: analizando-datos-sobre-el-brexit-con-pandas

<a href="http://bobbelderbos.com/2016/06/analyzing-brexit-data-with-pandas/" target="_blank">Esta entrada apareció en inglés en mi blog.</a>

Desde hace tiempo quería aprender [Pandas](http://pandas.pydata.org). Por fin llegó la oportunidad: Brexit = datos.

Como siempre empecé con un ejercicio / objetivo práctico, en este caso procesar los datos del referéndum. Usé Pandas para analizar los datos (CSV) publicados por [electoralcommission.org.uk](http://www.electoralcommission.org.uk/find-information-by-subject/elections-and-referendums/upcoming-elections-and-referendums/eu-referendum/electorate-and-count-information).

Aunque quería responder a más preguntas este CSV era suficiente para estrenarme con Pandas (¡es inmenso!). Además aprendí a usar [Jupyter notebook](http://jupyter.readthedocs.io/en/latest/) para documentar todo. El notebook lo [puedes ver / bajar desde Github](https://github.com/bbelderbos/brexit-pandas/blob/master/Analyze_Brexit_Pandas_ES.ipynb).

Consegui mi objetivo de representar los datos mostrados [aquí](https://ig.ft.com/sites/elections/2016/uk/eu-referendum/index.html). Aquí algunos pantallazos del notebook:

&nbsp;

<img class="alignnone" src="http://bobbelderbos.com/assets/notebook_screenshot1.png" alt="" width="745" height="260" />

<img class="alignnone" src="http://bobbelderbos.com/assets/notebook_screenshot2.png" alt="" width="592" height="429" />

<img class="alignnone" src="http://bobbelderbos.com/assets/notebook_screenshot3.png" alt="" width="615" height="465" />

<img class="alignnone" src="http://bobbelderbos.com/assets/notebook_screenshot4.png" alt="" width="935" height="443" />

### Añadiendo datos demográficos

Vinculé los datos del voto con los [datos de censo](http://www.ons.gov.uk/census/2011census/2011censusdata) públicamente disponibles (como sugirió [Pybonacci](https://twitter.com/Pybonacci)), gracias). Encontré unas correlaciones interesantes (y aprendí algunas cosas de matplotlib usándolo), puedes ver el notebook [aquí](https://github.com/bbelderbos/brexit-pandas/blob/master/brexit_demographics.ipynb):

#### ¿Cómo influye la edad en el voto por salir / quedar?

<img class="alignnone" src="http://bobbelderbos.com/assets/median_age.png" alt="" width="432" height="432" />

#### ¿Cómo influye el porcentaje de paro?

<img class="alignnone" src="http://bobbelderbos.com/assets/perc_unemployed.png" alt="" width="432" height="432" />

#### ¿Cómo influye un nivel más alto de estudios (educación)?

<img class="alignnone" src="http://bobbelderbos.com/assets/perc_high_education.png" alt="" width="432" height="432" />

#### Y, ¿cómo influye el porcentaje de gente nacida fuera de Inglaterra?

<img class="alignnone" src="http://bobbelderbos.com/assets/perc_born_outside_uk.png" alt="" width="432" height="432" />

Claramente, áreas con una población mayor y una tasa de paro más alta votan por salir. Por otro lado, áreas con un alto porcentaje de estudios superiores, y regiones donde más gente nacieron fuera de Inglaterra prefieren (por lo general) que Inglaterra se quede en la unión.

Lo dicho, para ver como llegué a estos resultados con Pandas el notebook está [aquí](https://github.com/bbelderbos/brexit-pandas/blob/master/brexit_demographics.ipynb).

### Y por último: datos de ingresos por región

Los datos de ingresos (sueldo) eran más dificiles de obtener en [los datos del censo](http://webarchive.nationalarchives.gov.uk/20160105160709/http://www.ons.gov.uk/ons/publications/re-reference-tables.html?edition=tcm%3A77-286262) entonces usé [este enlace](https://www.gov.uk/government/statistics/income-and-tax-by-county-and-region-2010-to-2011) para comprobar la relación entre la mediana de ingresos y el voto. Encontré un patrón interesante:

<img class="alignnone" src="http://bobbelderbos.com/assets/median_income.png" alt="" width="720" height="720" />

(el parsing de los datos está documentado en el [mismo notebook](https://github.com/bbelderbos/brexit-pandas/blob/master/brexit_demographics.ipynb))

Se ve claramente que regiones con una mediana de ingresos más baja prefieren salir de la unión, aunque no es 100% consistente: Irlanda tiene una mediana relativamente baja pero vota por quedarse, y South East tiene un sueldo mediano más alto y, no obstante, vota por salir. Es interesante como se ve este tipo de tendencias combinando varias fuentes de datos.

### Enlaces de referencia para aprender Pandas

* [Pandas home y docs](http://pandas.pydata.org)
  
* [Python’s pandas make data analysis easy and powerful with a few lines of code](https://www.oreilly.com/learning/pythons-pandas-make-data-analysis-easy-and-powerful-with-a-few-lines-of-code?imm_mid=0e520d&cmp=em-prog-na-na-newsltr_20160625) - tutorial breve y fácil para empezar.
  
* [Python for Data Analysis](https://www.safaribooksonline.com/library/view/python-for-data/9781449323592/) - libro del creador de Pandas Wes McKinney.
  
* [Introduction to Pandas for Developers](https://www.safaribooksonline.com/library/view/introduction-to-pandas/9781771375764/) / [Data Wrangling and Analysis with Python](https://www.safaribooksonline.com/library/view/data-wrangling-and/9781491960820/) - ya he visto algunos videos, son buenos.