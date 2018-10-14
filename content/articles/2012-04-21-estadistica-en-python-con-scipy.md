---
title: Estadística en Python con SciPy (I)
date: 2012-04-21T17:46:31+00:00
author: Juan Luis Cano
slug: estadistica-en-python-con-scipy
tags: Estadística, matplotlib, numpy, python, scipy

## Introducción

Hoy vamos a ver cómo trabajar con variable aleatoria con el módulo `stats` de la biblioteca Scipy. Scipy viene con numerosas [distribuciones de probabilidad](http://docs.scipy.org/doc/scipy/reference/stats.html), tanto discretas como continuas, y además pone a nuestra disposición herramientas para crear nuestras propias distribuciones y multitud de herramientas para hacer cálculos estadísticos. En esta primera parte nos centraremos en cómo manejar esas distribuciones y sus funciones de distribución, cómo representarlas con matplotlib y cómo definir nuevas distribuciones.

_**En esta entrada se ha usado python 2.7.3, numpy 1.6.1, matplotlib 1.1.0 y scipy 0.10.1.**_

<!--more-->

**Nota:** En mi opinión la documentación de este módulo deja un poco que desear. No resulta demasiado didáctica, hay algunas imprecisiones y cosas que directamente no tienen sentido o están mal. En cuanto sepas manejarlo un poco puedes usar de referencia en primer enlace de la entrada.

## Distribuciones de variable continua

Entre las muchas [distribuciones continuas](http://docs.scipy.org/doc/scipy/reference/stats.html#continuous-distributions) que tiene SciPy vamos a ver un ejemplo de cómo manejar la distribución normal o gaussiana. Primero vamos a importar un par de módulos

    :::python
    In [1]: import numpy as np
    In [2]: import scipy.stats as st

Todas las distribuciones continuas están definidas en función de dos **parámetros**: `loc` y `scale`, que juegan distinto papel en función de la distribución que manejemos. Por ejemplo, para la normal, `loc` es la media y por tanto el centro de la distribución y `scale` es la desviación típica y puede verse como un factor de escala (de ahí los nombres de los parámetros). Por otro lado, para la distribución uniforme, `loc` y `scale` son los extremos del intervalo en el que toma valores la variable.

Tenemos dos formas de manejar las distribuciones: una de ellas es crear un objeto que represente a **la distribución con los parámetros fijados**, y acceder después a todos sus métodos («frozen distribution»), de esta manera:

    :::python
    In [3]: rv1 = st.norm()  # Normal estándar
    In [4]: rv1.cdf(0.5)  # Evaluamos la función de distribución en 0.5
    Out[4]: 0.69146246127401312
    In [5]: x = np.linspace(0.0, 1.0)
    In [6]: rv1.pdf(x)  # Densidad de probabilidad en el intervalo [0.0, 1.0]
    Out[6]:
    array([ 0.39894228,  0.39885921,  0.39861011,  0.39819528,  0.39761524,
            0.39687072,  0.39596264,  0.39489214,  0.39366054,  0.39226937,
            0.39072035,  0.38901539,  0.38715659,  0.38514623,  0.38298676,
            0.38068082,  0.37823119,  0.37564085,  0.37291289,  0.37005059,
            0.36705736,  0.36393672,  0.36069236,  0.35732807,  0.35384775,
            0.35025541,  0.34655518,  0.34275126,  0.33884794,  0.33484957,
            0.3307606 ,  0.3265855 ,  0.32232884,  0.31799518,  0.31358916,
            0.30911541,  0.30457861,  0.29998342,  0.29533453,  0.29063661,
            0.28589432,  0.28111231,  0.27629519,  0.27144753,  0.26657387,
            0.26167871,  0.25676648,  0.25184154,  0.24690821,  0.24197072])
    In [7]: rv2 = st.norm(2.0, 0.0)  # Normal (2.0, 0.0)
    In [8]: rv3 = st.norm(loc=-1.0, scale=np.sqrt(0.5))  # Media -1.0 y varianza 0.5

La otra manera sería llamar en cada momento a la función que queramos evaluar, pasando los parámetros correspondientes, de manera que no se crea una distribución concreta:

    :::python
    In [9]: st.norm.cdf(0.5)  # Función de distribución de una normal estándar en 0.5
    Out[9]: 0.69146246127401312
    In [10]: st.norm.pdf(x, -1.0, np.sqrt(0.5))  # Densidad de una normal (-1.0, 0.5) en [0.0, 1.0]
    Out[10]:
    array([ 0.20755375,  0.19916976,  0.1909653 ,  0.18294635,  0.17511819,
            0.16748543,  0.16005198,  0.15282109,  0.14579538,  0.13897686,
            0.13236692,  0.12596638,  0.11977553,  0.11379411,  0.10802137,
            0.10245611,  0.09709665,  0.09194093,  0.08698648,  0.08223049,
            0.0776698 ,  0.07330098,  0.0691203 ,  0.06512379,  0.06130727,
            0.05766636,  0.05419651,  0.05089303,  0.04775112,  0.04476588,
            0.04193231,  0.0392454 ,  0.03670008,  0.03429126,  0.03201387,
            0.02986284,  0.02783314,  0.0259198 ,  0.02411789,  0.02242256,
            0.02082904,  0.01933266,  0.01792884,  0.01661312,  0.01538113,
            0.01422864,  0.01315155,  0.01214588,  0.01120776,  0.01033349])

Esto será útil cuando queramos hacer ajustes o estimaciones sobre los parámetros de la distribución, como veremos en la próxima entrega.

Para quien no conozca los nombres en inglés, los métodos más importantes son

  * Salida pseudoaleatoria («random variates» `rvs`)
  * Función densidad de probabilidad («probability density function» `pdf`)
  * Función de distribución («cumulative distribution function» `cdf`)

y todos ellos, y alguno más, están **vectorizados**, lo que significa que les podemos pasar un array de NumPy y obtendremos un array de valores.

### Representación gráfica

Como los métodos básicos están vectorizados, es muy sencillo representarlos gráficamente en la manera a la que estamos acostumbrados, utilizando arrays de NumPy. Simplemente tenemos que escribir

    :::python
    In [11]: import matplotlib.pyplot as plt
    In [12]: x = np.linspace(0.0, 1.0)
    In [13]: plt.plot(x, st.norm.pdf(x, -1.0, np.sqrt(0.5)))
    Out[13]: []
    In [14]: plt.show()

Y podemos obtener bonitas figuras como esta.<figure id="attachment_217" style="width: 448px" class="wp-caption aligncenter">

![Distribuciones normales](https://pybonacci.org/images/2012/04/normal_pdf1.png)

### Definir distribuciones

La manera de crear nuestras propias distribuciones continuas con SciPy es extender la clase [`rv_continuous`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html) y definir o bien su función de densidad o su función de distribución. Las clases y la herencia son conceptos de la [Programación Orientada a Objetos](http://es.wikipedia.org/wiki/Programaci%C3%B3n_orientada_a_objetos), pero no es nuestra intención meternos a fondo en estos temas. De igual manera que hemos hecho `rv = st.norm()` para crear un objeto distribución al que manipular, queremos un mecanismo parecido para hacer `rv = nueva_dist()`, y para eso hemos de definir `nueva_dist` primero.

Por ejemplo, supongamos que queremos definir una distribución uniforme cuya función de densidad es

$f(x) = -ln{x} quad x in (0, 1],$

el código sería el siguiente

    :::python
    In [15]: from scipy.stats import rv_continuous
    In [16]: class variable_gen(rv_continuous):
       ....:     """Variable aleatoria continua de distribución logarítmica."""
       ....:     def _pdf(self, x):
       ....:         return -log(x)
       ....:
    In [17]: variable_gen?
    Type:       type
    Base Class: &lt;type 'type'&gt;
    String Form:&lt;class '__main__.variable_gen'&gt;
    Namespace:  Interactive
    Definition: variable_gen(self, *args, **kwds)
    Docstring:  Variable aleatoria continua de distribución logarítmica.
    Constructor information:
     Definition:variable_gen(self, momtype=1, a=None, b=None, xa=-10.0, xb=10.0, xtol=1e-14, badvalue=None, name=None, longname=None, shapes=None, extradoc=None)
    In [18]: variable = variable_gen(a=0.0, b=1.0, name="variable")
    In [19]: variable.pdf(0.0)
    /usr/bin/ipython2:4: RuntimeWarning: divide by zero encountered in log
    Out[19]: inf
    In [20]: from scipy.integrate import quad
    In [21]: from numpy import inf
    In [22]: quad(variable.pdf, -inf, inf)
    Out[22]: (0.9999999999999962, 6.149525333398742e-12)

Lo que hemos hecho ha sido

  1. Definir la clase `variable_gen`, que hereda las propiedades de `rv_continuous`.
  2. Escribir la cadena de documentación de la clase.
  3. Definir su función de densidad de probabilidad.
  4. Crear una nueva variable, `variable`, en la que guardamos un objeto distribución cuya variable recorre el intervalo $[0.0, 1.0]$ (nótese que es cerrado).
  5. Comprobar qué pasa en 0. Nada que no supiéramos.
  6. Comprobar que la función densidad está normalizada integrándola sobre la recta real (el primer número es el valor de la integral y el segundo una estimación del error, como podemos ver en la documentación de la función `<a href="http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html">quad</a>)`.

A partir de ahora podemos hacer lo mismo que hemos hecho antes: o bien crear una distribución fija o acceder a los métodos de la misma directamente. Aunque sólo hemos dado la función de densidad, comprobamos que también podemos llamar al resto:

    :::python
    In [23]: rv = variable()  # Nótense los paréntesis
    In [24]: rv.cdf(0.5)
    Out[24]: 0.84657359027997248
    In [25]: x = np.linspace(0.0, 1.0)
    In [25]: rv.cdf(x)
    Out[25]:
    array([ 0.        ,  0.09983307,  0.17137441,  0.23223723,  0.28616538,
            0.33493698,  0.37959929,  0.42084431,  0.45916388,  0.49492574,
            0.52841535,  0.55986072,  0.58944824,  0.61733311,  0.64364656,
            0.66850105,  0.69199398,  0.71421058,  0.73522599,  0.75510704,
            0.77391348,  0.79169908,  0.8085125 ,  0.82439796,  0.83939582,
            0.8535431 ,  0.86687383,  0.87941944,  0.89120902,  0.90226958,
            0.91262628,  0.92230257,  0.93132042,  0.93970041,  0.94746188,
            0.95462303,  0.961201  ,  0.96721201,  0.97267137,  0.97759362,
            0.98199253,  0.98588117,  0.98927201,  0.99217689,  0.99460713,
            0.9965735 ,  0.99808632,  0.99915544,  0.99979032,  1.        ])
    In [26]: rv.rvs()
    Out[26]: 0.11391190950607678
    In [27]: rv.rvs()
    Out[27]: 0.41700479602973284
    In [28]: rv.rvs()
    Out[28]: 0.00019824204606004107

## Distribuciones de variable discreta

Scipy también trae unas cuantas [distribuciones discretas](http://docs.scipy.org/doc/scipy/reference/stats.html#discrete-distributions) para que no las tengamos que definir nosotros, y se usan de manera similar a las continuas. Por ejemplo, la distribución binomial:

    :::python
    In [29]: rv = st.binom(5, 0.5)  # Experimento de Bernoulli 5 veces con probabilidad 0.5
    In [30]: k = np.arange(6)
    In [31]: pk = rv.pmf(k)
    In [32]: pk
    Out[32]: array([ 0.03125,  0.15625,  0.3125 ,  0.3125 ,  0.15625,  0.03125])

Para el caso de distribuciones discretas, la función de densidad se distribuye por la función de probabilidad («probability mass function» `pmf`).

### Representación gráfica

Ahora representar gráficamente una distribución discreta tiene un poco más de enjundia que en el caso de distribuciones continuas. Para la función de probabilidad hay al menos dos opciones, en función de los gustos de cada cual: hacer un diagrama de barras con [`bar`](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.bar) o uno de líneas verticales con [`vlines`](http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.vlines), como vemos en este fragmento de código:

    :::python
    In [33]: plt.vlines(k, 0, pk)  # El segundo argumento da el extremo inferior de las líneas
    Out[33]:
    In [34]: plt.plot(k, pk, 'o')  # Añadimos puntos en los extremos
    Out[34]: []
    In [35]: plt.show()
    In [36]: plt.bar(k - 0.5, _81, width=1.0)  # Se resta 0.5 para que las barras estén centradas
    Out[36]:
    In [37]: plt.show()

Se obtienen resultados similares a estos:<figure id="attachment_232" style="width: 300px" class="wp-caption aligncenter">

![Binomial (5, 1/2)](https://pybonacci.org/images/2012/04/binomial5_05_pmf.png?w=300)

Para la función de distribución, sabemos que en el caso discreto esta tiene discontinuidades de salto. Para no obtener una gráfica horrible con puntos unidos que no deberían estarlo, o bien hacemos otro diagrama de barras o utilizamos **arrays enmascarados** («masked arrays» suena menos chistoso). Los [masked arrays](http://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html#what-is-a-masked-array) con arrays de NumPy en los que, bien manualmente o bien siguiendo alguna regla o patrón, hemos marcado algunas entradas como inválidas. Son de utilidad cuando, por ejemplo, estamos recogiendo datos y queremos descartar los que sean erróneos o se alejen demasiado de la media.

Si representamos gráficamente arrays enmascarados, matplotlib _no_ unirá los puntos correspondientes a entradas inválidas, que es exactamente lo que queremos (como podemos leer [en esta respuesta de StackOverflow](http://stackoverflow.com/a/2543391/554319)). Los elementos que queremos marcar como inválidos son aquellos en los que la función da un salto, por lo que comprobaremos la diferencia entre un elemento y el siguiente del array. Para ello usaremos la función `roll` de NumPy:

    :::python
    In [38]: rv = st.binom(5, 0.5)
    In [39]: x = np.linspace(-0.5, 5.5)
    In [40]: cdf = rv.cdf(x)
    In [41]: deltas = cdf - np.roll(cdf, 1)  # Array de diferencias
    In [42]: deltas
    Out[42]:
    array([-1.     ,  0.     ,  0.     ,  0.     ,  0.     ,  0.03125,
            0.     ,  0.     ,  0.     ,  0.     ,  0.     ,  0.     ,
            0.     ,  0.15625,  0.     ,  0.     ,  0.     ,  0.     ,
            0.     ,  0.     ,  0.     ,  0.3125 ,  0.     ,  0.     ,
            0.     ,  0.     ,  0.     ,  0.     ,  0.     ,  0.3125 ,
            0.     ,  0.     ,  0.     ,  0.     ,  0.     ,  0.     ,
            0.     ,  0.15625,  0.     ,  0.     ,  0.     ,  0.     ,
            0.     ,  0.     ,  0.     ,  0.03125,  0.     ,  0.     ,
            0.     ,  0.     ])
    In [43]: cdf = np.ma.masked_where(abs(deltas) &gt; tol, cdf)
    In [44]: cdf
    Out[44]:
    masked_array(data = [-- 0.0 0.0 0.0 0.0 -- 0.03125 0.03125 0.03125 0.03125 0.03125 0.03125
     0.03125 -- 0.1875 0.1875 0.1875 0.1875 0.1875 0.1875 0.1875 -- 0.5 0.5 0.5
     0.5 0.5 0.5 0.5 -- 0.8125 0.8125 0.8125 0.8125 0.8125 0.8125 0.8125 --
     0.96875 0.96875 0.96875 0.96875 0.96875 0.96875 0.96875 -- 1.0 1.0 1.0 1.0],
                 mask = [ True False False False False  True False False False False False False
     False  True False False False False False False False  True False False
     False False False False False  True False False False False False False
     False  True False False False False False False False  True False False
     False False],
           fill_value = 1e+20)

Y se obtiene un diagrama similar a este:<figure id="attachment_237" style="width: 300px" class="wp-caption aligncenter">

![Distribución binomial (5, 1/2)](https://pybonacci.org/images/2012/04/binomial5_05_cdf.png?w=300)

### Definir distribuciones

Definir nuevas distribuciones discretas es aún más sencillo que en el caso continuo. Igual que antes, podemos crear una clase que extienda de, en este caso, [`rv_discrete`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.html), pero ahora demás podemos construir la distribución directamente pasando los $(x\_k, p\_k)$ al constructor. Por ejemplo, si queremos construir una distribución discreta con los siguientes datos:

<table>
  <tr>
    <th>
      $x_k$
    </th>
    
    <td>
      1
    </td>
    
    <td>
      2
    </td>
    
    <td>
      3
    </td>
    
    <td>
      4
    </td>
  </tr>
  
  <tr>
    <th>
      $p_k$
    </th>
    
    <td>
      0.1
    </td>
    
    <td>
      0.4
    </td>
    
    <td>
      0.2
    </td>
    
    <td>
      0.3
    </td>
  </tr>
</table>

el código será el siguiente:

    :::python
    In [45]: xk = [1, 2, 3, 4]
    In [46]: pk = [0.1, 0.4, 0.2, 0.3]
    In [47]: rv = st.rv_discrete(xk[0], xk[-1], values=(xk, pk))

y ya podemos acceder a todos los métodos que hemos visto anteriormente con normalidad.

Aquí se termina la primera parte de esta introducción al cálculo estadístico con SciPy. Espero que te haya resultado útil; no olvides difundirlo en las redes sociales y comentar lo que te apetezca.

¡Un saludo!
