---
title: Nuestro primer algoritmo heurístico
date: 2012-10-31T06:00:42+00:00
author: Kiko Correoso
slug: nuestro-primer-algoritmo-heuristico
tags: algoritmos, búsqueda en escalada, heurística, hill-climbing, optimización, python

Normalmente, cuando se trata de optimizar 'algo' se pueden usar diferentes aproximaciones.

  * La primera sería el uso de algoritmos de búsqueda exhaustivos como la fuerza bruta. Estos algoritmos nos dan la solución exacta pero si el [espacio de búsqueda es muy amplio el tiempo de cálculo necesario puede ser inabordable](http://en.wikipedia.org/wiki/Combinatorial_explosion) (explosión combinatoria).
  * Otra aproximación, que es la que veremos hoy, sería el uso de algoritmos [heurísticos](http://es.wikipedia.org/wiki/Heur%C3%ADstica_%28inform%C3%A1tica%29). La palabra heurística viene del griego y vendría a significar algo así como 'relativo a la búsqueda'  (recordad, [eureka significa 'lo he encontrado' y tiene el mismo origen etimológico](http://es.wikipedia.org/wiki/%C2%A1Eureka!)). Estos algoritmos sacrifican la exactitud de la solución en favor del tiempo de respuesta, es decir, intentamos obtener soluciones lo suficientemente buenas con un tiempo de respuesta corto o aceptable.

Vamos a proponer un problema sencillo y lo vamos a resolver de forma aproximada usando un algoritmo heurístico de 'búsqueda en escalada' o 'hill-climbing'.

Vamos a ello, la resolución del problema es obvia en este caso, pero solo se trata de que veáis el funcionamiento de todo esto. Tenemos un conjunto de n números que se hallan dentro de un subconjunto de los números reales. ¿Cuál sería el conjunto de estos n números que me permiten minimizar lo siguiente?

$sum_{k=1}^N k^2$

Para simplificar permitiremos que los n números se puedan repetir por lo que la respuesta obvia es que el conjunto de los números sea [0, 0, 0, ..., 0] por lo que la solución exacta sería 0. Si pensamos por un momento que la solución no es obvia, la búsqueda exhaustiva nunca sería óptima puesto que estamos buscando entre los números reales. Por tanto, ¿como resolveríamos esto con una búsqueda heurística? Primero de todo pondremos un poco de código, lo explicamos y luego haremos uso del mismo para ver los resultados que obtenemos:

<pre><code class="language-python">import numpy as np
import matplotlib.pyplot as plt
plt.ion()
class Busqueda:
    u"""
    Clase (fea) para explicar el funcionamiento de
    un algoritmo heurístico
    """
    def __init__(self, ngeneraciones, ngenes, lim_sup, lim_inf):
        self.ngeneraciones = ngeneraciones
        self.ngenes = ngenes
        self.lim_sup = lim_sup
        self.lim_inf = lim_inf
    def padre(self):
        self.individuo0 = np.random.rand(self.ngenes) *
                          (self.lim_sup - self.lim_inf) + self.lim_inf
        return self.individuo0
    def fitness(self, individuo):
        funcion = individuo * individuo
        return np.sum(funcion)
    def hijo(self, individuo):
        nindividuo = individuo + np.random.normal(0,1, self.ngenes)
        nindividuo[nindividuo &lt; self.lim_inf] = self.lim_inf
        nindividuo[nindividuo &gt; self.lim_sup] = self.lim_sup
        return nindividuo
    def calculos(self):
        fit_acum = []
        individuo = self.individuo0
        poblacion = self.individuo0
        fit_acum = np.append(fit_acum, self.fitness(individuo))
        for generacion in xrange(self.ngeneraciones - 1):
            nindividuo = self.hijo(individuo)
            if self.fitness(nindividuo) &lt;= fit_acum[-1]:
                individuo = nindividuo
            fit_acum = np.append(fit_acum, self.fitness(individuo))
            poblacion = np.append(poblacion, individuo)
        return poblacion.reshape(self.ngeneraciones, self.ngenes), fit_acum
    def representa_proceso(self, poblacion, fitness_acumulado):
        plt.subplot(311)
        plt.xlim(self.lim_inf, self.lim_sup)
        plt.ylim(0., self.lim_sup ** 2.)
        for gen in range(self.ngenes):
            plt.text(poblacion[0, gen],
                     self.fitness(poblacion[0, gen]),
                     gen+1)
        plt.subplot(312)
        plt.xlim(self.lim_inf, self.lim_sup)
        plt.ylim(0., self.lim_sup ** 2.)
        for generacion in range(self.ngeneraciones):
            for gen in range(self.ngenes):
                plt.text(poblacion[generacion, gen],
                         self.fitness(poblacion[generacion, gen]),
                         gen+1)
        plt.subplot(313)
        plt.xlim(0, self.ngeneraciones)
        plt.ylim(0., np.max(fitness_acumulado))
        plt.plot(fitness_acumulado)</code></pre>

Vamos a guardar el anterior código en un fichero que se llame _heuristico.py_ y vamos a abrir **ipython** en el mismo lugar donde se encuentra el fichero _heuristico.py_.

Hemos creado una clase llamada _Busqueda_ que hemos de inicializar con una serie de parámetros, el primero sería el número de iteraciones que vamos a usar en nuestra búsqueda, el segundo sería el número de miembros que vamos a usar, n, y el tercer y cuarto serían el límite superior e inferior del intervalo de números reales donde vamos a restringir la búsqueda. Dentro de ipython hacemos lo siguiente:

<pre><code class="language-python">In [1]: from heuristico import Busqueda
In [2]: busqueda = Busqueda(1000, 3, 100, -100)</code></pre>

Vamos a hacer una simulación que contará con 1000 generaciones (o pasos, o iteraciones, como más os guste), la solución tendrá en cuenta un conjunto de 3 números que estarán restringidos entre [-100, 100].

Lo siguiente será crear la primera solución (la solución padre de la que derivarán todas las soluciones hijas siguientes) que no es más que una solución aleatoria para empezar la búsqueda. Lo hacemos de la siguiente forma:

<pre><code class="language-python">In [3]: busqueda.padre()
Out[3]: array([-56.14070247,  96.07815303,  31.11068139])</code></pre>

Veis que el primer miembro ha tomado un valor en torno a -56, el segundo un valor en torno a 96 y el tercero un valor en torno a 31.

Ahora vamos a ver la chicha del algoritmo. El cálculo completo se realiza en el método _calculos_, que a su vez hace uso de los métodos _fitness_ e _hijo_. El método _fitness_ es el que calcula la solución del problema (en este caso se trata de minimizar el valor). El método _hijo_ es el que crea una posible solución nueva cercana a la solución actual (solución padre). En el método _calculos_ hacemos las iteraciones (1000 en este ejemplo) para comparar al padre con el hijo y ver si tiene mejor fitness y en caso de que sea así actualizamos al padre con el hijo, es decir, le pasamos los valores del hijo al padre.

<pre><code class="language-python">In [4]: pob, fit_acum = busqueda.calculos()</code></pre>

Hemos calculado la población final, _pob_, el conjunto de 3 elementos que nos minimizan el resultado, y hemos obtenido el valor de la función fitness en cada iteración, _fit_acum_.

Por último, vamos a hacer una representación de los resultados de la siguiente manera:

<pre><code class="language-python">In [5]: busqueda.representa_proceso(pob, fit_acum)</code></pre>

Que nos mostraría la siguiente ventana:

[<img class="aligncenter size-full wp-image-1134" title="Heuristico" alt="" src="http://pybonacci.org/wp-content/uploads/2012/10/heuristico.png" height="553" width="652" srcset="https://pybonacci.org/wp-content/uploads/2012/10/heuristico.png 652w, https://pybonacci.org/wp-content/uploads/2012/10/heuristico-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/10/heuristico.png)

Donde el primer panel (arriba), nos muestra la posición de la primera solución aleatoria que hemos generado con el método _padre_. Como hemos visto anteriormente, el primer miembro ha tomado un valor en torno a -56, el segundo un valor en torno a 96 y el tercero un valor en torno a 31. En el segundo panel (en medio) vemos como va evolucionando la solución, cada uno de los miembros de la solución va descendiendo poco a poco hacia la solución final (cercana a cero). Por último, en el tercer panel (abajo) vemos el valor de nuestra solución y como se va a cercando a una solución cercana a 0, de hecho, vemos que a partir de las 300 iteraciones ya estaríamos cerca de 0. Aunque después de las 1000 iteraciones no hemos alcanzado la solución exacta, 0, puesto que estos algoritmos dan valores aproximados.

Veamos un segundo caso:

<pre><code class="language-python">In [1]: from heuristico import Busqueda # Solo necesario si habéis cerrado ipython
In [2]: busqueda = Busqueda(1000, 20, 200, 0)
In [3]: busqueda.padre()
Out[3]:
array([  71.65433435,   13.38201722,   57.30044929,   74.69591418,
197.39440847,   42.3185271 ,   69.08520774,    7.40961601,
79.87846973,  161.14232418,  135.47599187,  183.17622057,
30.69728341,   21.85297791,  157.85448115,  139.02125074,
98.8888481 ,   49.02073966,   46.10618954,  116.69194813])
In [4]: pob, fit_acum = busqueda.calculos()
In [5]: busqueda.representa_proceso(pob, fit_acum)</code></pre>

Que nos daría el siguiente resultado:

[<img class="aligncenter size-full wp-image-1136" title="Heuristico_ii" alt="" src="http://pybonacci.org/wp-content/uploads/2012/10/heuristico_ii1.png" height="553" width="652" srcset="https://pybonacci.org/wp-content/uploads/2012/10/heuristico_ii1.png 652w, https://pybonacci.org/wp-content/uploads/2012/10/heuristico_ii1-300x254.png 300w" sizes="(max-width: 652px) 100vw, 652px" />](http://pybonacci.org/wp-content/uploads/2012/10/heuristico_ii1.png)

En este caso vemos hemos usado un conjunto de 20 números y observamos que quizá serían necesarias más iteraciones para llegar a un número más aproximado.

Normalmente, el algoritmo se para cuando se han superado las iteraciones o cuando la solución no ha mejorado en un número determinado de pasos (esto segundo no lo he implementado por lo que lo tenéis como ejercicio).

Saludos.

P.D.: Como siempre, se agradece cualquier corrección, crítica constructiva, propuesta de mejora, debate,..., en los comentarios.