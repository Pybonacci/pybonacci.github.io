---
title: Liberado poliastro 0.2: Mecánica Orbital y Astrodinámica en Python
date: 2014-08-16T18:32:13+00:00
author: Juan Luis Cano
slug: liberado-poliastro-0-2-mecanica-orbital-y-astrodinamica-en-python
tags: astropy, poliastro, python, python 3

Después de meses de trabajo he liberado **poliastro 0.2.0**, una biblioteca Python y Fortran destinada a estudiar problemas de Mecánica Orbital y Astrodinámica en Python:

<https://pybonacci.github.io/poliastro>

La versión 0.1.0 nació en 2013 mientras estudiaba _Orbital Mechanics_ en el Politecnico di Milano: tomé unas subrutinas escritas en Fortran por el profesor David A. Vallado para su libro "Fundamentals of Astrodynamics and Applications" y escribí una interfaz en Python para poder optimizar una transferencia entre la Tierra y Venus.

Sin embargo la biblioteca era muy engorrosa de utilizar y tuve muchos problemas a la hora de manejar cantidades con unidades. Inspirado por el paquete abandonado Plyades, decidí refactorizar drásticamente todo el código y el resultado es poliastro 0.2.

Gracias al módulo `astropy.units` es sencillo utilizar **cantidades con unidades** que se integran de manera _casi_ transparente con NumPy. Además, he incluido un módulo para representar órbitas en dos dimensiones con matplotlib y he cambiado la forma en la que se usa la biblioteca.

<!--more-->

Solo hacen falta tres líneas para empezar a probar el potencial de poliastro:

    :::python
    
    from poliastro.examples import molniya
    from poliastro.plotting import plot
    
    plot(molniya)
    
    

[<img src="http://new.pybonacci.org/images/2014/08/molniya.png" alt="Órbita Molniya" width="432" height="320" class="aligncenter size-full wp-image-2624" srcset="https://pybonacci.org/wp-content/uploads/2014/08/molniya.png 432w, https://pybonacci.org/wp-content/uploads/2014/08/molniya-300x222.png 300w" sizes="(max-width: 432px) 100vw, 432px" />](http://new.pybonacci.org/images/2014/08/molniya.png)

La piedra angular del paquete son los objetos `State`, que representan el estado de un objeto (un planeta, un satélite artificial) con respecto a un atractor principal (el Sol, la Tierra). Podemos acceder a sus vectores posición y velocidad, sus elementos keplerianos o pintar su órbita osculatriz.

    :::python
    
    from astropy import units as u
    from poliastro.bodies import Earth
    from poliastro.twobody import State
    
    # Data from Curtis, example 4.3
    r = [-6045, -3490, 2500] * u.km
    v = [-3.457, 6.618, 2.533] * u.km / u.s
    
    ss = State.from_vectors(Earth, r, v)
    
    

Así mismo, podemos definir maniobras (`Maneuver`) que alteran estas órbitas. Una forma es definir directamente los incrementos de velocidad que queremos aplicar, y otra es utilizar las funciones de poliastro para calcular maniobras comunes como las transferencias de Hohmann.

[<img src="http://new.pybonacci.org/images/2014/08/hohmann.png" alt="Transferencia de Hohmann" width="432" height="432" class="aligncenter size-full wp-image-2625" srcset="https://pybonacci.org/wp-content/uploads/2014/08/hohmann.png 432w, https://pybonacci.org/wp-content/uploads/2014/08/hohmann-150x150.png 150w, https://pybonacci.org/wp-content/uploads/2014/08/hohmann-300x300.png 300w" sizes="(max-width: 432px) 100vw, 432px" />](http://new.pybonacci.org/images/2014/08/hohmann.png)

Podéis leer la documentación completa en inglés en la web de poliastro, y el código fuente está disponible en GitHub. Os animo a que le echéis un vistazo y me hagáis llegar todas las sugerencias que se os ocurran: he dedicado mucho tiempo a organizar el código de forma que fuese fácil de usar y me gustaría conocer vuestra opinión al respecto.

¡Muchas gracias y un saludo! 🙂