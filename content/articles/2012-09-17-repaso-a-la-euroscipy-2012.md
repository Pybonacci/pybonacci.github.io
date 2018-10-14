---
title: Repaso a la EuroScipy 2012
date: 2012-09-17T08:27:34+00:00
author: Kiko Correoso
slug: repaso-a-la-euroscipy-2012
tags: acikit-learn, cython, euroscipy, matplotlib, numexpr, numpy, opengl, scipy, timeseries, visvis

Como todos sabéis, hace un par de semanas se celebró la [Euroscipy 2012 con mucho material interesante que repasar](http://www.euroscipy.org/conference/euroscipy2012). Voy a hablar de los que tienen algo de material para poder juzgar sobre algo.

Tutoriales básicos para científicos (o no):

  * [Introduction to python for scientist](http://www.euroscipy.org/talk/6563) ([material del curso](http://www.euroscipy.org/file/9018?vid=download)): Le he echado un ojo por encima y me parece un buen curso para empezar en el mundo python
  * [Scientific plotting with matplotlib](http://www.euroscipy.org/talk/6573) ([Curso](http://webloria.loria.fr/~rougier/teaching/matplotlib/) y [código del curso](https://github.com/rougier/scipy-lecture-notes/tree/euroscipy-2012/intro/matplotlib)): El curso está genial para ver matplotlib por encima, donde todo se ve con ejemplos y donde la documentación completa de cada una de las cosas que se usan la tienes disponible a un click. Si el inglés no es lo tuyo puedes echarle un ojo a nuestro tutorial de matplotlib ([en el blog](https://pybonacci.org/tag/tutorial-matplotlib-pyplot/) o todo junto [en pdf](http://new.pybonacci.org/images/2012/08/tutorial-de-matplotlib-pyplotv0-1-201208311.pdf)).
  * [Introducción a la computación científica con python](http://www.euroscipy.org/talk/6578): En este curso se hace uso de las excelentes [scipy-lecture-notes. Si no las conoces ya estás tardando.](http://scipy-lectures.github.com/)

Tutoriales avanzados (estos sí que son más bien para científicos):

  * [Beyond Numpy: NumExpr, carray and blosc](http://www.euroscipy.org/talk/6602) ([presentación](http://www.euroscipy.org/file/8920?vid=download) y [ejercicios](http://www.euroscipy.org/file/8921?vid=download)): Cuando Numpy no es suficientemente rápido para algunas operaciones, cuando el acceso a disco es lento, cuando nuestra memoria (RAM) es limitada no está todo perdido. Se habla sobre tres excelentes herramientas como son numexpr (aquí [una introducción en español](http://www.slideshare.net/kikocorreoso/numexpr-python-madrid-13428246)), carray y blosc que permiten hacer cosas muy interesantes.
  * [Parallel computing with multiprocessing, parallelpython and ipython](http://www.euroscipy.org/talk/6612) ([presentación](http://www.euroscipy.org/file/9017?vid=download)): Las presentaciones de este chico son bastante inútiles si no has asistido o no tienes el video o, por lo menos, a mi me lo parecen (y dicho esto con todo el respeto y admiración del mundo hacia Ian). Habla sobre acelerar python paralelizando de diversas formas.
  * [Better numerics with scipy](http://www.euroscipy.org/talk/6617): De momento no está el material pero si, por casualidad, os enteráis, por favor, avisad por los comentarios, nuestro twitter o como sea puesto que es una charla que me interesa.
  * [Time series data analysis with python](http://www.euroscipy.org/talk/6629): lo mismo que la anterior, por favor, avisad si encontráis algo.
  * [Writing robust scientific code with testing (and python)](http://www.euroscipy.org/talk/6634) ([presentación](http://www.euroscipy.org/file/8962?vid=download)): Algo importante y que yo no uso 🙁 en mi chorri-código. En el momento que tenga tiempo me pondré con ello (quizá nunca :-().

Charlas (solo alguna puesto que otras no tocan mi campo de acción y no he perdido mucho tiempo con ellas y no podría opinar con rigor):

  * [VisVis, an object oriented approach to visualization](http://www.euroscipy.org/talk/6784) ([presentación](http://www.euroscipy.org/file/9036?vid=download)): Un wrapper OO para openGL. ¿¿¿¿Que aún no has usado [openGL](http://pyopengl.sourceforge.net/)???? A ver si encuentro un rato para trastear con ello para mis campos tridimensionales y sale alguna entrada nueva de aquí.

  * [New developments with scikit-learn: machine learning in python](http://www.euroscipy.org/talk/6856) ([presentación](http://www.euroscipy.org/file/9010?vid=download)): Aprendizaje automático hecho fácil en python. Una delicia de librería. Lo mismo que la anterior, si no la has usado aún [échale un vistazo](http://scikit-learn.org/stable/) y seguro que le encuentras [alguna utilidad](http://scikit-learn.org/stable/auto_examples/index.html). Hay excelentes [tutoriales](http://scikit-learn.org/stable/user_guide.html) en su web y una lista de [presentaciones increible que ya me gustaría para muchas de las cosas que uso](http://scikit-learn.org/stable/presentations.html). Yo ya he estado trabajando con SVRs (máquinas de vectores soporte usadas para problemas de regresión) y a ver si sale algo para pybonacci.

Espero que le echéis un vistazo a todo ese gran material, que nos contéis si lo usáis y como, que nos aviséis si veis los vídeos o material complementario y que disfrutéis tanto como yo 🙂

Hasta la próxima.