---
title: Informando de bugs en NumPy y SciPy en castellano a través de Pybonacci
date: 2013-08-23T08:45:04+00:00
author: Juan Luis Cano
slug: informando-de-bugs-en-numpy-y-scipy-en-castellano-a-traves-de-pybonacci
tags: github, numpy, python, scipy

No sé si se llegará a usar esto mucho, pero he pensado que tal vez haya gente encontrando comportamientos extraños en NumPy o SciPy que pueden ser bugs pero que no puedan enviar un informe de errores en inglés a los repositorios oficiales. Por eso **he hecho un fork de ambos proyectos, y si pensáis que habéis encontrado un bug en NumPy o SciPy podéis decírnoslo en castellano aquí y nosotros nos encargamos de traducirlos**.

<https://github.com/Pybonacci/numpy/issues>
  
<https://github.com/Pybonacci/scipy/issues>

_**NOTA IMPORTANTE**_: Estos repositorios **no** son para consultas sobre código o dudas personales. Como para informar de cualquier otro bug se exigirá seriedad y compromiso por parte de la persona que informa. En particular, aplican estas tres sencillas reglas:

  1. El informe debe contener **en qué sistema operativo se trabaja y qué versiones de NumPy y/o SciPy se manejan**. Para ello se pueden ejecutar los comandos:

    $ uname -a
    Linux nebulae 3.10.7-1-ARCH #1 SMP PREEMPT Thu Aug 15 11:55:34 CEST 2013 x86_64 GNU/Linux
    $ python -c "import numpy; print(numpy.version.version)"
    1.7.1
    $ python -c "import scipy; print(scipy.version.version)"
    0.12.0</pre>
    <p></p>
    
    
    
    
    
      1. Se debe proporcionar **el mínimo fragmento de código que reproduce el problema**. Si es muy breve, puede incluirse en el informe; si no, es preferible usar <http://gist.github.com> u otros servicios. <del datetime="2014-10-28T09:34:05+00:00">Mandar un programa de 200 líneas donde el problema está en la 138 no ayuda a descubrir el bug.</del></p>
        
    
    
      2. 
        Se debe indicar **cuál era el comportamiento esperado, y cuál es el obtenido**. De esta forma podemos diagnosticar fácilmente dónde está el problema. Frases como «no va», «se cuelga» sin más explicaciones no son útiles tampoco.
        
    
    
    
    Se ruega difusión entre las personas que pudieran estar interesadas 🙂
    
    
    ¡Saludos!